"""Hosted-API chat client with the same return shape as client.chat (the local Ollama client).

    chat_api(model, messages, mode, n_opts=10, temperature=0.0, seed=7) -> dict

model = "<provider>:<model id>", provider in {openai, anthropic, google, openrouter}. Never raises.
Standard library only (urllib). Keys come from the project .env via envfile.load(); key values are never
printed, logged, saved or put in error strings (all error text passes through envfile.scrub).

Return dict: text, letter, prompt_tokens, out_tokens, done ("stop" | "length" | provider value), error,
plus extras: reasoning_tokens, cost_usd, provider_model, sampling ("temperature=0" | "default"),
out_limit, reasoning_setting, latency_s, api.
  out_tokens = ALL billed output tokens (visible + hidden reasoning), so cost = in*p_in + out*p_out.
  reasoning_tokens = the hidden part when the provider reports it (None otherwise).

Docs read on 15 Nov 2026 (official pages; URLs repeated next to the code that relies on them):
  Anthropic  https://platform.claude.com/docs/en/api/messages/create.md
             https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md
             https://platform.claude.com/docs/en/build-with-claude/thinking.md
             https://platform.claude.com/docs/en/api/models/list.md
  OpenAI     https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create.md
             https://developers.openai.com/api/reference/resources/responses/methods/create.md
             https://developers.openai.com/api/docs/guides/reasoning.md
             https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md   ("Using GPT-6")
             https://developers.openai.com/api/docs/models/gpt-6-luna.md
             https://developers.openai.com/api/reference/resources/models/methods/list.md
  Google     https://aistudio.google.com/api-reference/generate-content.md
             https://aistudio.google.com/docs/thinking.md?generate-content=true
             https://aistudio.google.com/docs/structured-output.md?generate-content=true
             https://aistudio.google.com/api-reference/models.md
  OpenRouter https://openrouter.ai/docs/api/api-reference/chat/create-a-chat-completion.md
             https://openrouter.ai/docs/guides/best-practices/reasoning-tokens.md
             https://openrouter.ai/docs/guides/features/structured-outputs.md
             https://openrouter.ai/api/v1/models
"""
import contextlib
import copy
import http.client
import json
import os
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # `python -I` drops the script dir
import envfile  # noqa: E402
from design import SCHEMA, parse_letter  # noqa: E402

USER_AGENT = "loud-or-right-harness"
TIMEOUT = 120
RETRIES = 4                       # extra attempts after the first, for 429 / 5xx / network errors
INSTANT_LIMIT = 32                # visible tokens for {"answer": "X"}
REASONED_LIMIT = 1500             # visible tokens for <=100 words + JSON line
REASONING_RESERVE = 4096          # added to the limit whenever hidden reasoning cannot be fully off
LEDGER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "spend.json")
PROVIDERS = ("openai", "anthropic", "google", "openrouter", "deepseek")
BUDGET_VAR = {p: f"BUDGET_USD_{p.upper()}" for p in PROVIDERS}
KEY_VAR = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "google": "GEMINI_API_KEY",
           "openrouter": "OPENROUTER_API_KEY", "deepseek": "DEEPSEEK_API_KEY"}
# harness_x: the main experiment's ledger, read-only, for the combined OpenRouter cap.
MAIN_LEDGER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "harness", "data",
                                "spend.json")

# Strict copy of design.SCHEMA: Anthropic structured outputs require additionalProperties:false on every
# object (structured-outputs.md, "JSON Schema limitations"); OpenAI strict mode uses it in every example
# (developers.openai.com/api/docs/guides/structured-outputs.md); Gemini accepts it (structured-output.md,
# "additionalProperties"). design.SCHEMA itself is not modified.
STRICT_SCHEMA = copy.deepcopy(SCHEMA)
STRICT_SCHEMA["additionalProperties"] = False

# ---- price + model table ------------------------------------------------------------------------
# USD per 1M tokens, standard (non-batch, non-fast) tier, short prompts. "long" = (prompt-token threshold,
# input, output) when the page lists a long-prompt rate. "off" = how hidden reasoning is minimised;
# "reserve" = True when it cannot be fully switched off (limit gets REASONING_RESERVE added).
# A model missing from this table is refused.
_ANT = "https://platform.claude.com/docs/en/about-claude/pricing.md (read 15 Nov 2026)"
_OAI = "https://developers.openai.com/api/docs/pricing.md (read 15 Nov 2026)"
_GOO = "https://ai.google.dev/gemini-api/docs/pricing (served as aistudio.google.com markdown; read 15 Nov 2026)"
_ORT = "https://openrouter.ai/api/v1/models (official Models API, per-token prices x 1e6; read 15 Nov 2026)"
MODELS = {
    # Anthropic. thinking.md: Haiku 5.5 accepts thinking {"type":"disabled"} at effort <= high; Sonnet 5.5
    # rejects "disabled", lowest is {"type":"between_tools"} (no other field allowed, effort <= high);
    # Opus 5.5 rejects "disabled": thinking cannot be turned off, only effort lowered.
    "anthropic:claude-haiku-5-5": dict(inp=0.10, out=0.50, long=(100_000, 0.50, 2.50), src=_ANT,
                                       thinking={"type": "disabled"}, effort="low", reserve=False),
    "anthropic:claude-sonnet-5-5": dict(inp=2.00, out=10.00, src=_ANT,
                                        thinking={"type": "between_tools"}, effort="low", reserve=False),
    "anthropic:claude-opus-5-5": dict(inp=4.00, out=20.00, src=_ANT,
                                      thinking=None, effort="low", reserve=True),
    # OpenAI. Chat Completions `reasoning_effort`; "Using GPT-6": GPT-6.1 Terra, GPT-6 Sol and GPT-6 Luna
    # support "none" (GPT-6 Astra / GPT-6.1 Sol do not). Long rate: prompts > 272K = 2x input, 1.5x output.
    "openai:gpt-6-luna": dict(inp=0.10, out=0.50, long=(272_000, 0.20, 0.75), src=_OAI + "; also models/gpt-6-luna.md",
                              api="chat", ladder=["none", "minimal", "low"]),
    "openai:gpt-6-sol": dict(inp=2.00, out=10.00, long=(272_000, 4.00, 15.00), src=_OAI,
                             api="chat", ladder=["none", "minimal", "low"]),
    "openai:gpt-6.1-terra": dict(inp=1.00, out=5.00, long=(272_000, 2.00, 7.50), src=_OAI,
                                 api="chat", ladder=["none", "minimal", "low"]),
    # HARNESS ALIAS, not an OpenAI model id (models/gpt-6-luna-pro.md is a 404 and the pricing table has no
    # such row). reasoning.md "Reasoning mode": pro is `reasoning.mode: "pro"` on the Responses API, billed at
    # the selected model's standard token rates. Sent as model "gpt-6-luna" to /v1/responses.
    # UNVERIFIED: that effort "none" is accepted together with mode "pro" (only OpenRouter's metadata for
    # openai/gpt-6-luna-pro lists "none"). Reserve added because pro aggregates extra hidden model work.
    "openai:gpt-6-luna-pro": dict(inp=0.10, out=0.50, long=(272_000, 0.20, 0.75), src=_OAI + " (gpt-6-luna rates)",
                                  api="responses", real_id="gpt-6-luna", mode="pro",
                                  ladder=["none", "minimal", "low"], reserve=True),
    # Google Gemini API (generateContent). thinking.md?generate-content=true table: lowest thinkingLevel
    # "minimal" only on 3.6 Flash, 3.5 Flash-Lite, 3.1 Flash-Lite, 3 Flash Preview; "low" on Gemini 4 and
    # 3.8 Flash. Thinking counts against maxOutputTokens (thinking.md: MAX_TOKENS with truncated/empty output)
    # so every Gemini entry gets the reserve. generate-content.md GenerationConfig.temperature: "silently
    # ignored on Gemini 3.6 Flash and newer models" -> temp_ok=False there.
    "google:gemini-3.1-flash-lite": dict(inp=0.25, out=1.50, src=_GOO, level="minimal", temp_ok=True),
    "google:gemini-3.5-flash-lite": dict(inp=0.30, out=2.50, src=_GOO, level="minimal", temp_ok=True),  # temp: unverified
    "google:gemini-3.6-flash": dict(inp=0.75, out=3.75, src=_GOO + " (promo to 31 Dec 2026, then 1.50/7.50)",
                                    level="minimal", temp_ok=False),
    "google:gemini-3.8-flash": dict(inp=0.75, out=3.75, src=_GOO + " (promo to 31 Dec 2026, then 1.50/7.50)",
                                    level="low", temp_ok=False),
    "google:gemini-4-hydrogen": dict(inp=1.50, out=7.50, src=_GOO, level="low", temp_ok=False),
    "google:gemini-4-argon": dict(inp=2.00, out=10.00, src=_GOO + " (promo to 30 Nov 2026, then 4/20)",
                                  level="low", temp_ok=False),
    "google:gemini-4-carbon": dict(inp=2.00, out=10.00, src=_GOO + " (promo to 30 Nov 2026, then 4/20)",
                                   level="low", temp_ok=False),
    # OpenRouter. `reasoning` sent only where the model's metadata has a reasoning object:
    # deepseek-v3.2 {default_enabled: false} -> {"enabled": false}; gpt-6-luna(-pro) supported_efforts incl. "none".
    # pin = one provider endpoint slug, sent as provider.order=[pin] with allow_fallbacks=false
    # (https://openrouter.ai/docs/guides/routing/provider-selection.md: `order`, `allow_fallbacks`,
    # `require_parameters`; exact endpoint slugs like "google-vertex/us-east5" are allowed). Chosen 15 Nov 2026
    # from GET https://openrouter.ai/api/v1/models/<id>/endpoints
    # (https://openrouter.ai/docs/api/api-reference/endpoints/list-all-endpoints-for-a-model.md); each pinned
    # endpoint lists structured_outputs, response_format, temperature and seed. Prices are that endpoint's.
    #  - Llama 3.3 70B: no bf16 endpoint listed; CoreWeave serves fp16 ("coreweave/fp16", $0.71/$0.71).
    #  - DeepSeek-V3.2: DeepSeek itself does not serve it on OpenRouter; AtlasCloud fp8 ("atlas-cloud/fp8").
    #  - Ministral 3 14B: the maker, Mistral ("mistral/zdr"; quantisation reported as "unknown").
    # ---- harness_x exploratory tier (read 15 Nov 2026) ----------------------------------------------
    # DeepSeek direct. https://api-docs.deepseek.com/quick_start/pricing : API model name "deepseek-flash",
    # "now served by DeepSeek-V4.1-Flash-1017"; PEAK prices used (conservative): cache-miss input $0.30,
    # output $1.20 per 1M (off-peak is half). JSON Output = response_format {"type": "json_object"} only
    # (https://api-docs.deepseek.com/guides/json_mode; API reference lists only text | json_object, no schema).
    # Thinking off: {"thinking": {"type": "disabled"}} (https://api-docs.deepseek.com/guides/thinking_mode).
    # temperature works in non-thinking mode; no `seed` parameter (https://api-docs.deepseek.com/api/create-chat-completion).
    "deepseek:deepseek-v4.1-flash-1017": dict(inp=0.30, out=1.20, real_id="deepseek-flash",
                                              src="https://api-docs.deepseek.com/quick_start/pricing (peak)"),
    # OpenRouter, pinned endpoints from GET /api/v1/models/<id>/endpoints (15 Nov 2026), endpoint prices:
    #  - Qwen3.8 27B: the maker's endpoint (Alibaba) lacks structured_outputs; DeepInfra bf16 pinned.
    #  - Llama 4 Maverick: no bf16 endpoint; Parasail fp8 pinned.
    #  - Mistral Medium 3.5: the maker, Mistral ("mistral/zdr").
    "openrouter:qwen/qwen3.8-27b": dict(inp=0.15, out=1.875, src=_ORT + " (deepinfra/bf16 endpoint)",
                                        reasoning={"effort": "none"}, pin="deepinfra/bf16"),
    "openrouter:meta-llama/llama-4-maverick": dict(inp=0.35, out=1.00, src=_ORT + " (parasail/fp8 endpoint)",
                                                   reasoning=None, pin="parasail/fp8"),
    "openrouter:mistralai/mistral-medium-3-5": dict(inp=1.50, out=7.50, src=_ORT + " (mistral/zdr endpoint)",
                                                    reasoning={"effort": "none"}, pin="mistral/zdr"),
    "openrouter:meta-llama/llama-3.3-70b-instruct": dict(inp=0.71, out=0.71, src=_ORT, reasoning=None,
                                                         pin="coreweave/fp16"),
    "openrouter:deepseek/deepseek-v3.2": dict(inp=0.26, out=0.38, src=_ORT, reasoning={"enabled": False},
                                              pin="atlas-cloud/fp8"),
    "openrouter:mistralai/ministral-14b-2512": dict(inp=0.20, out=0.20, src=_ORT, reasoning=None,  # "Ministral 3 14B 2512"
                                                    pin="mistral/zdr"),
    "openrouter:openai/gpt-6-luna": dict(inp=0.10, out=0.50, long=(272_000, 0.20, 0.75), src=_ORT,
                                         reasoning={"effort": "none"}, temp_ok=False),
    "openrouter:openai/gpt-6-luna-pro": dict(inp=0.10, out=0.50, long=(272_000, 0.20, 0.75), src=_ORT,
                                             reasoning={"effort": "none"}, reserve=True, temp_ok=False),
    # temp_ok=False: these two list `seed` but not `temperature` in supported_parameters, and instant mode
    # sends provider.require_parameters=true, so an unlisted parameter could leave no eligible endpoint.
}

# ---- env -----------------------------------------------------------------------------------------
_env_lock = threading.Lock()
_env_cache = None


def get_env(reload=False):
    global _env_cache
    with _env_lock:
        if _env_cache is None or reload:
            _env_cache = envfile.load()
        return _env_cache


def _budget(env, provider):
    try:
        return float(env.get(BUDGET_VAR[provider], "") or 0)
    except ValueError:
        return 0.0


# ---- ledger --------------------------------------------------------------------------------------
_ledger_tlock = threading.Lock()


LOCK_STALE_S = 60
LOCK_WAIT_S = 30


@contextlib.contextmanager
def _file_lock(path):
    """Cross-process lock: `<ledger>.lock` created with O_CREAT | O_EXCL, retried with a short sleep, removed
    in a finally block. A lock older than LOCK_STALE_S is treated as stale (crashed holder) and broken.
    Always taken inside the thread lock, so threads of one process do not spin on the file."""
    lock = path + ".lock"
    os.makedirs(os.path.dirname(lock) or ".", exist_ok=True)
    deadline = time.time() + LOCK_WAIT_S
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except (FileExistsError, PermissionError):   # Windows may give PermissionError mid-delete
            try:
                if time.time() - os.path.getmtime(lock) > LOCK_STALE_S:
                    os.remove(lock)
                    continue
            except OSError:
                pass
            if time.time() > deadline:
                raise TimeoutError(f"ledger lock busy for {LOCK_WAIT_S} s: {lock}")
            time.sleep(0.005)
    try:
        yield
    finally:
        try:
            os.remove(lock)
        except OSError:
            pass


def _read_ledger(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def ledger_total(provider, path=None):
    """Provider total, read under the thread lock and the cross-process file lock (used for the cap check)."""
    path = path or LEDGER_PATH
    with _ledger_tlock, _file_lock(path):
        return float(_read_ledger(path).get(provider, {}).get("usd", 0.0))


def ledger_add(provider, model_id, usd, path=None):
    """Add usd to the provider's running total (read-modify-write under thread + file lock). Returns new total."""
    path = path or LEDGER_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with _ledger_tlock, _file_lock(path):
        d = _read_ledger(path)
        p = d.setdefault(provider, {"usd": 0.0, "calls": 0, "by_model": {}})
        p["usd"] = p.get("usd", 0.0) + usd
        p["calls"] = p.get("calls", 0) + 1
        p.setdefault("by_model", {})[model_id] = p["by_model"].get(model_id, 0.0) + usd
        tmp = f"{path}.{os.getpid()}.{threading.get_ident()}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=1, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())   # temp file complete on disk before the atomic os.replace
        for i in range(50):   # Windows: replace fails while another process has the file open for reading
            try:
                os.replace(tmp, path)
                break
            except PermissionError:
                if i == 49:
                    raise
                time.sleep(0.02)
        return p["usd"]


def price_cost(cfg, prompt_tokens, out_tokens):
    pi, po = cfg["inp"], cfg["out"]
    if cfg.get("long") and (prompt_tokens or 0) > cfg["long"][0]:
        pi, po = cfg["long"][1], cfg["long"][2]
    return ((prompt_tokens or 0) * pi + (out_tokens or 0) * po) / 1e6


# ---- request builders (pure; tested without network) --------------------------------------------
def _limit(mode, reserve, max_tokens=None):
    """Visible limit (max_tokens override, else the mode default) plus hidden-reasoning headroom."""
    base = max_tokens if max_tokens is not None else (INSTANT_LIMIT if mode == "instant" else REASONED_LIMIT)
    return int(base) + (REASONING_RESERVE if reserve else 0)


def strict_schema(schema):
    """Deep copy with additionalProperties:false on every object node (Anthropic requires it; OpenAI strict
    mode uses it; Gemini accepts it). No numeric/length constraints are added: Anthropic's structured outputs
    do not support minimum/maximum (structured-outputs.md, "Not supported"), so callers range-check."""
    s = copy.deepcopy(schema)

    def walk(n):
        if isinstance(n, dict):
            if n.get("type") == "object":
                n["additionalProperties"] = False
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(s)
    return s


def build_request(model, messages, mode, env, temperature=0.0, seed=7, send_sampling=True, level_idx=0,
                  gemini_alt_format=False, schema=None, max_tokens=None):
    """Returns (url, headers, body, meta). meta: api, out_limit, reasoning_setting, sampling, provider_id.
    schema: custom instant-mode schema (default design.SCHEMA); max_tokens: visible-limit override."""
    provider, mid = model.split(":", 1)
    cfg = MODELS[model]
    sch = STRICT_SCHEMA if schema is None else strict_schema(schema)
    hdr = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
    meta = {"api": None, "sampling": "default"}
    if provider == "anthropic":
        # POST /v1/messages; headers x-api-key + anthropic-version (messages/create.md). Version 2026-10-21
        # rejects temperature/top_p/top_k on every model (and the 5.5 models reject non-default values on
        # older versions too), so sampling is never sent: sampling = "default".
        hdr.update({"x-api-key": env.get(KEY_VAR[provider], ""), "anthropic-version": "2026-10-21"})
        reserve = cfg["reserve"]
        body = {"model": mid, "max_tokens": _limit(mode, reserve, max_tokens), "messages": messages,
                "output_config": {"effort": cfg["effort"]}}
        if cfg["thinking"] is not None:
            body["thinking"] = dict(cfg["thinking"])
        if mode == "instant":
            body["output_config"]["format"] = {"type": "json_schema", "schema": sch}
        meta.update(api="anthropic.messages", out_limit=body["max_tokens"],
                    reasoning_setting=f"thinking={cfg['thinking'] and cfg['thinking']['type'] or 'adaptive(always on)'}"
                                      f", effort={cfg['effort']}")
        return "https://api.anthropic.com/v1/messages", hdr, body, meta

    if provider == "deepseek":
        # POST https://api.deepseek.com/chat/completions (OpenAI format; base URL from the pricing page).
        hdr["Authorization"] = "Bearer " + env.get(KEY_VAR[provider], "")
        body = {"model": cfg["real_id"], "messages": messages, "thinking": {"type": "disabled"},
                "max_tokens": _limit(mode, False, max_tokens)}
        if send_sampling:
            body["temperature"] = temperature
            meta["sampling"] = "temperature=0" if temperature == 0 else f"temperature={temperature}"
        if mode == "instant":
            # JSON mode only (no schema parameter); the prompts already say "Reply with JSON only".
            body["response_format"] = {"type": "json_object"}
        meta.update(api="deepseek.chat", out_limit=body["max_tokens"], reasoning_setting="thinking=disabled",
                    structured="json_object")
        return "https://api.deepseek.com/chat/completions", hdr, body, meta

    if provider in ("openai", "openrouter"):
        hdr["Authorization"] = "Bearer " + env.get(KEY_VAR[provider], "")
        if provider == "openai":
            if env.get("OPENAI_ORG_ID"):
                hdr["OpenAI-Organization"] = env["OPENAI_ORG_ID"]   # reference/overview.md
            if env.get("OPENAI_PROJECT_ID"):
                hdr["OpenAI-Project"] = env["OPENAI_PROJECT_ID"]
        if provider == "openai" and cfg.get("api") == "responses":
            # POST /v1/responses (responses/methods/create.md): input = EasyInputMessage list (role/content),
            # reasoning {mode, effort}, max_output_tokens, text.format json_schema {name, schema, strict},
            # store (default true -> sent false). No `seed` parameter exists on Responses.
            level = cfg["ladder"][min(level_idx, len(cfg["ladder"]) - 1)]
            reserve = cfg.get("reserve", False) or level != "none"
            body = {"model": cfg["real_id"], "input": messages, "store": False,
                    "reasoning": {"mode": cfg["mode"], "effort": level},
                    "max_output_tokens": _limit(mode, reserve, max_tokens)}
            if send_sampling and level == "none":   # Using GPT-6: remove temperature when effort is not none
                body["temperature"] = temperature
                meta["sampling"] = "temperature=0" if temperature == 0 else f"temperature={temperature}"
            if mode == "instant":
                body["text"] = {"format": {"type": "json_schema", "name": "answer", "schema": sch,
                                           "strict": True}}
            meta.update(api="openai.responses", out_limit=body["max_output_tokens"],
                        reasoning_setting=f"reasoning.mode={cfg['mode']}, reasoning.effort={level}")
            return "https://api.openai.com/v1/responses", hdr, body, meta
        # Chat Completions (OpenAI chat/completions/methods/create.md; OpenRouter create-a-chat-completion.md)
        body = {"model": mid, "messages": messages}
        rs = "n/a"
        reserve = cfg.get("reserve", False)
        if provider == "openai":
            level = cfg["ladder"][min(level_idx, len(cfg["ladder"]) - 1)]
            body["reasoning_effort"] = level
            body["store"] = False
            reserve = reserve or level != "none"
            body["max_completion_tokens"] = _limit(mode, reserve, max_tokens)
            rs = f"reasoning_effort={level}"
            sampling_ok = level == "none"           # Using GPT-6: temperature only with effort none
        else:
            if cfg["reasoning"] is not None:
                body["reasoning"] = dict(cfg["reasoning"])   # reasoning-tokens.md: effort / enabled
                rs = "reasoning=" + json.dumps(cfg["reasoning"])
            body["max_tokens"] = _limit(mode, reserve, max_tokens)
            sampling_ok = cfg.get("temp_ok", True)
        if send_sampling and sampling_ok:
            body["temperature"] = temperature
            body["seed"] = seed
            meta["sampling"] = "temperature=0" if temperature == 0 else f"temperature={temperature}"
        elif send_sampling and provider == "openrouter":
            body["seed"] = seed      # listed for the Luna entries; temperature is not -> sampling "default"
        if provider == "openrouter" and cfg.get("pin"):
            body["provider"] = {"order": [cfg["pin"]], "allow_fallbacks": False}
            meta["pinned_provider"] = cfg["pin"]
        if mode == "instant":
            body["response_format"] = {"type": "json_schema",
                                       "json_schema": {"name": "answer", "schema": sch, "strict": True}}
            if provider == "openrouter":
                body.setdefault("provider", {})["require_parameters"] = True   # structured-outputs.md step 2
        url = ("https://api.openai.com/v1/chat/completions" if provider == "openai"
               else "https://openrouter.ai/api/v1/chat/completions")
        meta.update(api=f"{provider}.chat", out_limit=body.get("max_completion_tokens", body.get("max_tokens")),
                    reasoning_setting=rs)
        return url, hdr, body, meta

    if provider == "google":
        # POST v1beta/models/{model}:generateContent, key in x-goog-api-key header (never in the URL).
        # Content.role must be 'user' or 'model' (generate-content.md, Content).
        hdr["x-goog-api-key"] = env.get(KEY_VAR[provider], "")
        contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
                    for m in messages]
        gc = {"maxOutputTokens": _limit(mode, True, max_tokens), "thinkingConfig": {"thinkingLevel": cfg["level"]}}
        if send_sampling and cfg["temp_ok"]:
            gc["temperature"] = temperature
            gc["seed"] = seed
            meta["sampling"] = "temperature=0" if temperature == 0 else f"temperature={temperature}"
        if mode == "instant":
            # REST spelling from structured-output.md?generate-content=true curl example;
            # generate-content.md also documents responseMimeType + responseJsonSchema as an alternative.
            # UNVERIFIED live (Gemini returned 402 during the check). If the API rejects it, chat_api retries
            # once per process with the alternative (gemini_alt_format=True) and remembers the choice.
            if gemini_alt_format:
                gc["responseMimeType"] = "application/json"
                gc["responseJsonSchema"] = sch
            else:
                gc["responseFormat"] = {"text": {"mimeType": "APPLICATION_JSON", "schema": sch}}
        body = {"contents": contents, "generationConfig": gc}
        meta.update(api="google.generateContent", out_limit=gc["maxOutputTokens"],
                    reasoning_setting=f"thinkingLevel={cfg['level']}")
        return (f"https://generativelanguage.googleapis.com/v1beta/models/{mid}:generateContent", hdr, body, meta)
    raise ValueError(provider)


# ---- response parsers (pure) ---------------------------------------------------------------------
def _norm_done(v):
    return {"end_turn": "stop", "stop": "stop", "STOP": "stop", "completed": "stop",
            "max_tokens": "length", "length": "length", "MAX_TOKENS": "length",
            "max_output_tokens": "length"}.get(v, v)


def parse_response(provider, api, d):
    """Returns dict text, prompt_tokens, out_tokens, reasoning_tokens, done, provider_model, cost_reported."""
    r = {"text": "", "prompt_tokens": None, "out_tokens": None, "reasoning_tokens": None, "done": None,
         "provider_model": d.get("model"), "cost_reported": None}
    if provider == "anthropic":
        # content blocks: read type == "text" only (thinking blocks may come first); usage.input_tokens,
        # usage.output_tokens (includes thinking), usage.output_tokens_details.thinking_tokens;
        # stop_reason: end_turn | max_tokens | stop_sequence | tool_use | pause_turn | refusal |
        # model_context_window_exceeded (messages/create.md).
        r["text"] = "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
        u = d.get("usage") or {}
        r["prompt_tokens"] = u.get("input_tokens")
        r["out_tokens"] = u.get("output_tokens")
        r["reasoning_tokens"] = (u.get("output_tokens_details") or {}).get("thinking_tokens")
        r["done"] = _norm_done(d.get("stop_reason"))
    elif api == "openai.responses":
        # output[]: items of type "message" with content[] of type "output_text"; status completed |
        # incomplete (+ incomplete_details.reason: max_output_tokens | content_filter | ...);
        # usage.input_tokens, usage.output_tokens, usage.output_tokens_details.reasoning_tokens.
        parts = []
        for item in d.get("output") or []:
            if item.get("type") == "message":
                parts += [c.get("text", "") for c in item.get("content") or [] if c.get("type") == "output_text"]
        r["text"] = "".join(parts)
        u = d.get("usage") or {}
        r["prompt_tokens"] = u.get("input_tokens")
        r["out_tokens"] = u.get("output_tokens")
        r["reasoning_tokens"] = (u.get("output_tokens_details") or {}).get("reasoning_tokens")
        st = d.get("status")
        r["done"] = _norm_done((d.get("incomplete_details") or {}).get("reason") if st == "incomplete" else st)
    elif provider in ("openai", "openrouter", "deepseek"):
        # choices[0].message.content, choices[0].finish_reason: stop | length | tool_calls | content_filter |
        # function_call; usage.prompt_tokens, usage.completion_tokens (includes reasoning),
        # usage.completion_tokens_details.reasoning_tokens; OpenRouter adds usage.cost (USD credits).
        ch = (d.get("choices") or [{}])[0]
        r["text"] = (ch.get("message") or {}).get("content") or ""
        u = d.get("usage") or {}
        r["prompt_tokens"] = u.get("prompt_tokens")
        r["out_tokens"] = u.get("completion_tokens")
        r["reasoning_tokens"] = (u.get("completion_tokens_details") or {}).get("reasoning_tokens")
        r["done"] = _norm_done(ch.get("finish_reason"))
        if provider == "deepseek" and r["reasoning_tokens"] is None:
            # Non-thinking replies carry no completion_tokens_details (seen live 15 Nov 2026); thinking replies
            # carry message.reasoning_content. No reasoning_content => 0 hidden reasoning tokens.
            r["reasoning_tokens"] = 0 if not (ch.get("message") or {}).get("reasoning_content") else None
        if provider == "openrouter":
            # top-level `provider` = the provider that served the call (create-a-chat-completion.md example)
            r["serving_provider"] = d.get("provider")
            if isinstance(u.get("cost"), (int, float)):
                r["cost_reported"] = float(u["cost"])
    elif provider == "google":
        # candidates[0].content.parts[] (skip parts with thought: true); finishReason STOP | MAX_TOKENS | SAFETY
        # | ...; usageMetadata.promptTokenCount, candidatesTokenCount, thoughtsTokenCount; modelVersion.
        # The reference does not say whether candidatesTokenCount includes thoughts; the pricing page bills
        # output "including thinking tokens", so out_tokens = candidates + thoughts (may over-count if
        # candidates already includes them -> budget errs on the safe side). UNVERIFIED.
        cands = d.get("candidates") or []
        if cands:
            c = cands[0]
            r["text"] = "".join(p.get("text", "") for p in (c.get("content") or {}).get("parts") or []
                                if not p.get("thought"))
            r["done"] = _norm_done(c.get("finishReason"))
        else:
            r["done"] = "blocked:" + str((d.get("promptFeedback") or {}).get("blockReason"))
        u = d.get("usageMetadata") or {}
        r["prompt_tokens"] = u.get("promptTokenCount")
        th = u.get("thoughtsTokenCount")
        cc = u.get("candidatesTokenCount")
        r["reasoning_tokens"] = th
        r["out_tokens"] = None if cc is None and th is None else (cc or 0) + (th or 0)
        r["provider_model"] = d.get("modelVersion")
    return r


# ---- transport -----------------------------------------------------------------------------------
# On this machine IPv6 routes are broken (TCP connects to the APIs' IPv6 addresses time out; IPv4 connects
# in 0.2 s, tested 15 Nov 2026), and urllib tries the IPv6 address first, waiting the whole timeout. This
# connection class tries IPv4 addresses first with a 10 s connect timeout per address.
CONNECT_TIMEOUT = 10


class _V4FirstHTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        infos = socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_STREAM)
        infos.sort(key=lambda i: i[0] != socket.AF_INET)
        err, sock = None, None
        for fam, typ, proto, _, addr in infos:
            sock = socket.socket(fam, typ, proto)
            sock.settimeout(min(CONNECT_TIMEOUT, self.timeout or CONNECT_TIMEOUT))
            try:
                sock.connect(addr)
                break
            except OSError as e:
                err = e
                sock.close()
                sock = None
        if sock is None:
            raise err or OSError(f"cannot connect to {self.host}")
        sock.settimeout(self.timeout)
        self.sock = self._context.wrap_socket(sock, server_hostname=self.host)


class _V4FirstHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_V4FirstHTTPSConnection, req, context=self._context)


_OPENER = urllib.request.build_opener(_V4FirstHTTPSHandler(context=ssl.create_default_context()))


class HTTPFail(Exception):
    def __init__(self, status, body):
        super().__init__(status)
        self.status, self.body = status, body


def http_json(method, url, headers, body=None, timeout=TIMEOUT, retries=RETRIES, sleep=time.sleep):
    """JSON request with retries on 429 / 5xx / network errors / timeouts (exponential backoff, honours
    Retry-After). Raises HTTPFail(status, text) for other HTTP errors or after the last retry."""
    data = json.dumps(body).encode() if body is not None else None
    last = None
    for attempt in range(retries + 1):
        wait = min(60.0, 2.0 * 2 ** attempt)
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with _OPENER.open(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")[:600]
            last = HTTPFail(e.code, text)
            if e.code != 429 and e.code < 500:
                raise last
            ra = e.headers.get("Retry-After") if e.headers else None
            try:
                wait = max(wait, min(120.0, float(ra)))
            except (TypeError, ValueError):
                pass
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
            last = HTTPFail(None, f"{type(e).__name__}: {getattr(e, 'reason', e)}")
        except json.JSONDecodeError as e:
            raise HTTPFail(None, f"bad JSON in response: {e}")
        if attempt < retries:
            sleep(wait)
    raise last


# ---- main entry ----------------------------------------------------------------------------------
_flags_lock = threading.Lock()
_no_sampling = set()       # models that rejected sampling params this process
_level_idx = {}            # model -> index into its reasoning ladder after a rejection
_gemini_alt = set()        # Gemini models that rejected generationConfig.responseFormat this process

_SAMPLING_WORDS = ("temperature", "seed", "top_p", "top_k", "sampling")
_REASONING_WORDS = ("reasoning", "effort", "thinking")


def _blank(error, **extra):
    d = {"text": "", "letter": "?", "prompt_tokens": None, "out_tokens": None, "done": None, "error": error,
         "reasoning_tokens": None, "cost_usd": 0.0, "provider_model": None, "sampling": None}
    d.update(extra)
    return d


def chat_api(model, messages, mode, n_opts=10, temperature=0.0, seed=7, *, schema=None, max_tokens=None,
             env=None, ledger_path=None, transport=None):
    """See module docstring. env / ledger_path / transport are for tests (defaults: .env, data/spend.json,
    http_json)."""
    try:
        return _chat_api(model, messages, mode, n_opts, temperature, seed, env, ledger_path, transport,
                         schema, max_tokens)
    except Exception as e:  # never raise
        env_ = env if env is not None else (_env_cache or {})
        return _blank(envfile.scrub(f"internal {type(e).__name__}: {e}", env_))


def _chat_api(model, messages, mode, n_opts, temperature, seed, env, ledger_path, transport,
              schema=None, max_tokens=None):
    env = get_env() if env is None else env
    transport = transport or http_json
    if not isinstance(model, str) or ":" not in model:
        return _blank("model must be '<provider>:<model id>'")
    provider, mid = model.split(":", 1)
    if provider not in PROVIDERS:
        return _blank(f"unknown provider {provider!r}")
    if mode not in ("instant", "reasoned"):
        return _blank(f"unknown mode {mode!r}")
    if model not in MODELS:
        return _blank(f"no price entry for {model}; add it to api_client.MODELS from the official pricing page")
    if not env.get(KEY_VAR[provider]):
        if provider == "google" and (env.get("GOOGLE_APPLICATION_CREDENTIALS") or env.get("GOOGLE_CLOUD_PROJECT")):
            return _blank("Vertex AI auth is not implemented (service-account JWT needs RS256 signing, not in the "
                          "standard library). Set GEMINI_API_KEY to use the Gemini API instead.")
        return _blank(f"no key: {KEY_VAR[provider]} is empty or missing in .env")
    cap = _budget(env, provider)
    if cap <= 0:
        return _blank(f"provider disabled: {BUDGET_VAR[provider]} is 0 or missing")
    spent = ledger_total(provider, ledger_path)
    if provider in ("openrouter", "anthropic") and MAIN_LEDGER_PATH:
        # harness_x: the OpenRouter and Anthropic caps cover the main experiment's spend too (read under its lock file).
        spent += ledger_total(provider, MAIN_LEDGER_PATH)
    if spent >= cap:
        return _blank("budget cap reached")

    cfg = MODELS[model]
    with _flags_lock:
        send_sampling = model not in _no_sampling
        lvl = _level_idx.get(model, 0)
        alt = model in _gemini_alt
    t0 = time.time()
    tries = 0
    while True:
        tries += 1
        url, hdr, body, meta = build_request(model, messages, mode, env, temperature, seed, send_sampling, lvl, alt,
                                             schema=schema, max_tokens=max_tokens)
        try:
            d = transport("POST", url, hdr, body)
            break
        except HTTPFail as e:
            msg = (e.body or "").lower()
            if e.status == 400 and tries <= 4:
                if (provider == "google" and mode == "instant" and not alt
                        and any(w in msg for w in ("responseformat", "response_format", "unknown name",
                                                   "invalid json payload"))):
                    alt = True
                    with _flags_lock:
                        _gemini_alt.add(model)
                    continue
                if send_sampling and meta["sampling"] != "default" and any(w in msg for w in _SAMPLING_WORDS):
                    send_sampling = False
                    with _flags_lock:
                        _no_sampling.add(model)
                    continue
                ladder = cfg.get("ladder")
                if ladder and lvl + 1 < len(ladder) and any(w in msg for w in _REASONING_WORDS):
                    lvl += 1
                    with _flags_lock:
                        _level_idx[model] = max(_level_idx.get(model, 0), lvl)
                    continue
            err = f"HTTP {e.status}: {e.body}" if e.status else str(e.body)
            return _blank(envfile.scrub(err, env), sampling=meta["sampling"], out_limit=meta["out_limit"],
                          reasoning_setting=meta["reasoning_setting"], api=meta["api"], pinned_provider=meta.get("pinned_provider"),
                          latency_s=round(time.time() - t0, 3))
    latency = time.time() - t0
    p = parse_response(provider, meta["api"], d)
    cost = p["cost_reported"] if p["cost_reported"] is not None else price_cost(cfg, p["prompt_tokens"], p["out_tokens"])
    ledger_error = None
    if p["prompt_tokens"] is not None or p["out_tokens"] is not None or p["cost_reported"] is not None:
        try:
            ledger_add(provider, mid, cost, ledger_path)
        except Exception as e:   # the call succeeded and was paid for: keep the answer, flag the ledger
            ledger_error = f"{type(e).__name__}: {e}"
    text = p["text"] or ""
    pin, served = meta.get("pinned_provider"), p.get("serving_provider")
    mismatch = None
    if pin and served:
        norm = lambda s: "".join(ch for ch in s.lower() if ch.isalnum())
        mismatch = not norm(served).startswith(norm(pin.split("/")[0]))
    return {"ledger_error": ledger_error, "provider_mismatch": mismatch, "text": text, "letter": parse_letter(text, n_opts), "prompt_tokens": p["prompt_tokens"],
            "out_tokens": p["out_tokens"], "done": p["done"], "error": None,
            "reasoning_tokens": p["reasoning_tokens"], "cost_usd": cost, "provider_model": p["provider_model"],
            "sampling": meta["sampling"], "out_limit": meta["out_limit"],
            "reasoning_setting": meta["reasoning_setting"], "api": meta["api"], "latency_s": round(latency, 3),
            "pinned_provider": meta.get("pinned_provider"), "serving_provider": p.get("serving_provider")}


# ---- model lists (used by check_api.py) ----------------------------------------------------------
def list_models(provider, env=None, transport=None):
    """Model ids from the provider's models endpoint. Raises HTTPFail (scrub before printing)."""
    env = get_env() if env is None else env
    transport = transport or http_json
    key = env.get(KEY_VAR[provider], "")
    hdr = {"User-Agent": USER_AGENT}
    ids = []
    if provider == "deepseek":   # GET https://api.deepseek.com/models (api-docs.deepseek.com/api/list-models)
        hdr["Authorization"] = "Bearer " + key
        return [m["id"] for m in transport("GET", "https://api.deepseek.com/models", hdr).get("data", [])]
    if provider == "openai":   # GET /v1/models -> {"object": "list", "data": [{"id": ...}]}
        hdr["Authorization"] = "Bearer " + key
        ids = [m["id"] for m in transport("GET", "https://api.openai.com/v1/models", hdr).get("data", [])]
    elif provider == "openrouter":   # GET /api/v1/models -> {"data": [{"id": ...}]}
        hdr["Authorization"] = "Bearer " + key
        ids = [m["id"] for m in transport("GET", "https://openrouter.ai/api/v1/models", hdr).get("data", [])]
    elif provider == "anthropic":    # GET /v1/models?limit&after_id -> data, has_more, last_id (models/list.md)
        hdr.update({"x-api-key": key, "anthropic-version": "2026-10-21"})
        after = None
        for _ in range(50):
            url = "https://api.anthropic.com/v1/models?limit=1000" + (f"&after_id={after}" if after else "")
            d = transport("GET", url, hdr)
            ids += [m["id"] for m in d.get("data", [])]
            if not d.get("has_more") or not d.get("last_id"):
                break
            after = d["last_id"]
    elif provider == "google":       # GET /v1beta/models (models.md); paging params pageSize/pageToken UNVERIFIED
        hdr["x-goog-api-key"] = key
        tok = None
        for _ in range(50):
            url = "https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000" + (f"&pageToken={tok}" if tok else "")
            d = transport("GET", url, hdr)
            ids += [m["name"].split("/", 1)[-1] for m in d.get("models", [])]
            tok = d.get("nextPageToken")
            if not tok:
                break
    return ids
