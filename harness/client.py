"""Model client. Local models go to Ollama with the pilot's settings; provider-prefixed models
(openai:, anthropic:, google:, openrouter:) go to api_client.chat_api (written elsewhere).
Never raises on a failed call: returns an error marker."""
import json
import time
import urllib.request

from design import SCHEMA, parse_letter

URL = "http://127.0.0.1:11434/api/chat"
NUM_PREDICT = {"instant": 24, "reasoned": 1500}
NUM_CTX = 4096
TIMEOUT = 300
RETRIES = 3
PROVIDERS = ("openai:", "anthropic:", "google:", "openrouter:")
BASE_KEYS = ("text", "letter", "prompt_tokens", "out_tokens", "done", "error")


def is_api(model):
    return model.startswith(PROVIDERS)


def chat(model, messages, mode, n_opts=10, temperature=0.0, seed=7, schema=None, max_tokens=None):
    """Returns dict: text, letter ("?" if unparsable), prompt_tokens, out_tokens, done, error (None if ok).
    For API models, any extra keys from chat_api are kept and collected under "meta".
    schema: replaces design.SCHEMA as the instant-mode format (used by probe.py).
    max_tokens: replaces the output-token limit (local num_predict). Both go straight to chat_api."""
    if is_api(model):
        try:
            import api_client  # lazy: only needed for provider models
            r = dict(api_client.chat_api(model, messages, mode, n_opts=n_opts, temperature=temperature, seed=seed,
                                         schema=schema, max_tokens=max_tokens))
        except Exception as e:
            return {"text": "", "letter": "?", "prompt_tokens": None, "out_tokens": None, "done": None,
                    "error": f"api_client {type(e).__name__}: {e}", "meta": None}
        out = {k: r.get(k) for k in BASE_KEYS}
        if out["letter"] is None:
            out["letter"] = parse_letter(out["text"] or "", n_opts)
        extra = {k: v for k, v in r.items() if k not in BASE_KEYS}
        out["meta"] = extra or None
        return out
    body = {"model": model, "messages": messages, "stream": False, "think": False,
            "options": {"temperature": temperature, "num_ctx": NUM_CTX, "seed": seed,
                        "num_predict": max_tokens or NUM_PREDICT[mode]}}
    if mode == "instant":
        body["format"] = schema or SCHEMA
    data = json.dumps(body).encode()
    err = None
    for attempt in range(RETRIES + 1):
        try:
            req = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                d = json.loads(r.read())
            text = d["message"]["content"]
            out = {"text": text, "letter": parse_letter(text, n_opts), "prompt_tokens": d.get("prompt_eval_count"),
                   "out_tokens": d.get("eval_count"), "done": d.get("done_reason"), "error": None}
            if d["message"].get("thinking"):   # should not happen with think false; record it if it does
                out["meta"] = {"thinking_chars": len(d["message"]["thinking"])}
            return out
        except Exception as e:  # network, timeout, HTTP error, bad JSON
            err = f"{type(e).__name__}: {e}"
            if attempt < RETRIES:
                time.sleep(5 * 2 ** attempt)
    return {"text": "", "letter": "?", "prompt_tokens": None, "out_tokens": None, "done": None,
            "error": err or "unknown"}
