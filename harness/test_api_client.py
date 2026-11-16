"""Offline tests for api_client / envfile. No network, no real .env, no real ledger.

    uv run --quiet --no-project python -I harness/test_api_client.py
"""
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client as ac  # noqa: E402
import design  # noqa: E402
import envfile  # noqa: E402

FAKE = {"OPENAI_API_KEY": "sk-test-OPENAI-0123456789", "ANTHROPIC_API_KEY": "sk-ant-test-ANTH-0123456789",
        "GEMINI_API_KEY": "AIzaTEST-GEMINI-0123456789", "OPENROUTER_API_KEY": "sk-or-test-OR-0123456789",
        "OPENAI_ORG_ID": "org-TESTORG123", "OPENAI_PROJECT_ID": "proj_TESTPROJ123",
        "BUDGET_USD_OPENAI": "1", "BUDGET_USD_ANTHROPIC": "1", "BUDGET_USD_GOOGLE": "1",
        "BUDGET_USD_OPENROUTER": "1"}
SECRETS = [v for k, v in FAKE.items() if not k.startswith("BUDGET")]
ITEM = {"id": 1, "question": "What colour is a clear daytime sky?",
        "options": ["Blue", "Green", "Red", "Black", "White", "Purple", "Orange", "Grey", "Pink", "Brown"]}
MSGS = {m: design.build_messages(ITEM, "A", "B", "reliable", "certain", m, "A") for m in ("instant", "reasoned")}
ONE_PER_PROVIDER = ["anthropic:claude-haiku-5-5", "anthropic:claude-sonnet-5-5", "anthropic:claude-opus-5-5",
                    "openai:gpt-6-luna", "openai:gpt-6-luna-pro", "google:gemini-3.5-flash-lite",
                    "google:gemini-4-argon", "openrouter:meta-llama/llama-3.3-70b-instruct",
                    "openrouter:deepseek/deepseek-v3.2"]

# ---- canned responses written from the documented shapes ----
ANT_OK = {"id": "msg_1", "type": "message", "role": "assistant", "model": "claude-haiku-5-5",
          "content": [{"type": "text", "text": "{\"answer\": \"A\"}"}], "stop_reason": "end_turn",
          "usage": {"input_tokens": 300, "output_tokens": 8, "output_tokens_details": {"thinking_tokens": 0}}}
ANT_THINK_LEN = {"model": "claude-opus-5-5", "content": [{"type": "thinking", "thinking": "", "signature": "x"}],
                 "stop_reason": "max_tokens",
                 "usage": {"input_tokens": 300, "output_tokens": 4128, "output_tokens_details": {"thinking_tokens": 4128}}}
OAI_OK = {"id": "chatcmpl-1", "object": "chat.completion", "model": "gpt-6-luna",
          "choices": [{"index": 0, "message": {"role": "assistant", "content": "{\"answer\":\"B\"}"},
                       "finish_reason": "stop"}],
          "usage": {"prompt_tokens": 310, "completion_tokens": 7, "completion_tokens_details": {"reasoning_tokens": 0}}}
OAI_LEN = {"model": "gpt-6-luna", "choices": [{"index": 0, "message": {"role": "assistant", "content": ""},
                                               "finish_reason": "length"}],
           "usage": {"prompt_tokens": 310, "completion_tokens": 32, "completion_tokens_details": {"reasoning_tokens": 32}}}
RESP_INCOMPLETE = {"object": "response", "model": "gpt-6-luna", "status": "incomplete",
                   "incomplete_details": {"reason": "max_output_tokens"},
                   "output": [{"type": "reasoning", "summary": []},
                              {"type": "message", "role": "assistant",
                               "content": [{"type": "output_text", "text": "Thinking... {\"answer\": \"C\"}"}]}],
                   "usage": {"input_tokens": 320, "output_tokens": 4000,
                             "output_tokens_details": {"reasoning_tokens": 3900}}}
GEM_OK = {"candidates": [{"content": {"role": "model", "parts": [{"text": "hidden", "thought": True},
                                                                  {"text": "{\"answer\": \"D\"}"}]},
                          "finishReason": "STOP"}],
          "usageMetadata": {"promptTokenCount": 305, "candidatesTokenCount": 9, "thoughtsTokenCount": 40},
          "modelVersion": "gemini-3.5-flash-lite"}
GEM_LEN = {"candidates": [{"content": {"role": "model", "parts": []}, "finishReason": "MAX_TOKENS"}],
           "usageMetadata": {"promptTokenCount": 305, "candidatesTokenCount": 0, "thoughtsTokenCount": 4128},
           "modelVersion": "gemini-4-argon"}
OR_OK = {"model": "meta-llama/llama-3.3-70b-instruct",
         "choices": [{"message": {"role": "assistant", "content": "Because... {\"answer\": \"A\"}"},
                      "finish_reason": "stop"}],
         "usage": {"prompt_tokens": 300, "completion_tokens": 80, "cost": 0.0002}}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.ledger = os.path.join(self.tmp, "data", "spend.json")
        with ac._flags_lock:
            ac._no_sampling.clear()
            ac._level_idx.clear()
            ac._gemini_alt.clear()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def call(self, model, mode, reply, env=None, **kw):
        sent = []

        def transport(method, url, headers, body=None):
            sent.append((url, headers, body))
            if isinstance(reply, Exception):
                raise reply
            return reply(body) if callable(reply) else reply
        r = ac.chat_api(model, MSGS[mode], mode, env=env or FAKE, ledger_path=self.ledger, transport=transport, **kw)
        return r, sent


class TestRequests(Base):
    def test_bodies_all_models_both_modes(self):
        for model in ac.MODELS:
            for mode in ("instant", "reasoned"):
                with self.subTest(model=model, mode=mode):
                    url, hdr, body, meta = ac.build_request(model, MSGS[mode], mode, FAKE)
                    blob = json.dumps(body) + url
                    for s in SECRETS:
                        self.assertNotIn(s, blob, "secret leaked into body/url")
                    self.assertEqual(hdr["User-Agent"], "loud-or-right-harness")
                    self.assertNotIn("user", body)          # no user-identifying fields
                    self.assertNotIn("safety_identifier", body)
                    prov = model.split(":")[0]
                    if prov == "google":
                        roles = [c["role"] for c in body["contents"]]
                        self.assertTrue(set(roles) <= {"user", "model"})
                        self.assertEqual(roles, ["user", "model", "user", "model", "user"])
                        self.assertEqual(body["contents"][3]["parts"][0]["text"], '{"answer": "A"}')
                        self.assertNotIn("key=", url)
                    else:
                        msgs = body.get("messages", body.get("input"))
                        self.assertEqual([m["role"] for m in msgs], ["user", "assistant", "user", "assistant", "user"])
                    has_schema = self._schema_of(prov, meta["api"], body)
                    if mode == "instant":
                        self.assertEqual(has_schema["properties"]["answer"]["enum"], list(design.LETTERS))
                        self.assertFalse(has_schema["additionalProperties"])
                    else:
                        self.assertIsNone(has_schema)
                    lim = meta["out_limit"]
                    base = ac.INSTANT_LIMIT if mode == "instant" else ac.REASONED_LIMIT
                    self.assertIn(lim, (base, base + ac.REASONING_RESERVE))

    @staticmethod
    def _schema_of(prov, api, body):
        if prov == "anthropic":
            return (body["output_config"].get("format") or {}).get("schema")
        if api == "openai.responses":
            return ((body.get("text") or {}).get("format") or {}).get("schema")
        if prov in ("openai", "openrouter"):
            return ((body.get("response_format") or {}).get("json_schema") or {}).get("schema")
        return ((body["generationConfig"].get("responseFormat") or {}).get("text") or {}).get("schema")

    def test_design_schema_not_mutated(self):
        self.assertNotIn("additionalProperties", design.SCHEMA)

    def test_reasoning_controls(self):
        b = ac.build_request("anthropic:claude-haiku-5-5", MSGS["instant"], "instant", FAKE)[2]
        self.assertEqual(b["thinking"], {"type": "disabled"})
        self.assertNotIn("temperature", b)
        b = ac.build_request("anthropic:claude-sonnet-5-5", MSGS["instant"], "instant", FAKE)[2]
        self.assertEqual(b["thinking"], {"type": "between_tools"})
        b = ac.build_request("anthropic:claude-opus-5-5", MSGS["instant"], "instant", FAKE)[2]
        self.assertNotIn("thinking", b)
        self.assertEqual(b["output_config"]["effort"], "low")
        self.assertEqual(b["max_tokens"], ac.INSTANT_LIMIT + ac.REASONING_RESERVE)
        b = ac.build_request("openai:gpt-6-luna", MSGS["reasoned"], "reasoned", FAKE)[2]
        self.assertEqual((b["reasoning_effort"], b["temperature"], b["seed"], b["max_completion_tokens"]),
                         ("none", 0.0, 7, ac.REASONED_LIMIT))
        b = ac.build_request("openai:gpt-6-luna-pro", MSGS["instant"], "instant", FAKE)[2]
        self.assertEqual(b["model"], "gpt-6-luna")
        self.assertEqual(b["reasoning"], {"mode": "pro", "effort": "none"})
        self.assertIs(b["store"], False)
        b = ac.build_request("google:gemini-4-argon", MSGS["instant"], "instant", FAKE)[2]
        self.assertEqual(b["generationConfig"]["thinkingConfig"], {"thinkingLevel": "low"})
        self.assertNotIn("temperature", b["generationConfig"])
        b = ac.build_request("openrouter:deepseek/deepseek-v3.2", MSGS["instant"], "instant", FAKE)[2]
        self.assertEqual(b["reasoning"], {"enabled": False})
        self.assertTrue(b["provider"]["require_parameters"])
        b = ac.build_request("openrouter:mistralai/ministral-14b-2512", MSGS["reasoned"], "reasoned", FAKE)[2]
        self.assertNotIn("reasoning", b)
        self.assertNotIn("require_parameters", b["provider"])

    def test_openai_effort_ladder_drops_temperature(self):
        b = ac.build_request("openai:gpt-6-luna", MSGS["instant"], "instant", FAKE, level_idx=2)[2]
        self.assertEqual(b["reasoning_effort"], "low")
        self.assertNotIn("temperature", b)
        self.assertEqual(b["max_completion_tokens"], ac.INSTANT_LIMIT + ac.REASONING_RESERVE)


PROBE_SCHEMA = {"type": "object", "properties": {"right": {"type": "integer"}, "total": {"type": "integer"},
                                                 "probability": {"type": "integer"}},
                "required": ["right", "total", "probability"]}


class TestSchemaAndMaxTokens(Base):
    def test_every_model_both_modes(self):
        before = json.dumps(PROBE_SCHEMA, sort_keys=True)
        for model in ac.MODELS:
            for mode in ("instant", "reasoned"):
                for alt in (False, True):
                    with self.subTest(model=model, mode=mode, alt=alt):
                        url, hdr, body, meta = ac.build_request(model, MSGS[mode], mode, FAKE, gemini_alt_format=alt,
                                                                schema=PROBE_SCHEMA, max_tokens=64)
                        prov = model.split(":")[0]
                        sch = TestRequests._schema_of(prov, meta["api"], body)
                        if prov == "google" and alt and mode == "instant":
                            sch = body["generationConfig"]["responseJsonSchema"]
                        self.assertIn(meta["out_limit"], (64, 64 + ac.REASONING_RESERVE))
                        if mode == "instant":
                            self.assertEqual(sorted(sch["properties"]), ["probability", "right", "total"])
                            self.assertFalse(sch["additionalProperties"])
                            self.assertNotIn("answer", json.dumps(sch))
                            self.assertNotIn("minimum", json.dumps(sch))
                        else:
                            self.assertIsNone(sch)
                        for s in SECRETS:
                            self.assertNotIn(s, json.dumps(body))
        self.assertEqual(json.dumps(PROBE_SCHEMA, sort_keys=True), before)   # caller's schema not mutated

    def test_limits_keep_reserve(self):
        lim = lambda m: ac.build_request(m, MSGS["instant"], "instant", FAKE, schema=PROBE_SCHEMA, max_tokens=64)[3]["out_limit"]
        self.assertEqual(lim("anthropic:claude-haiku-5-5"), 64)
        self.assertEqual(lim("anthropic:claude-opus-5-5"), 64 + ac.REASONING_RESERVE)
        self.assertEqual(lim("openai:gpt-6-luna"), 64)
        self.assertEqual(lim("openai:gpt-6-luna-pro"), 64 + ac.REASONING_RESERVE)
        self.assertEqual(lim("google:gemini-3.1-flash-lite"), 64 + ac.REASONING_RESERVE)
        self.assertEqual(lim("openrouter:mistralai/ministral-14b-2512"), 64)

    def test_chat_api_custom_schema_each_provider(self):
        probe = '{"right": 6, "total": 8, "probability": 75}'
        replies = {
            "anthropic:claude-haiku-5-5": dict(ANT_OK, content=[{"type": "text", "text": probe}]),
            "openai:gpt-6-luna": dict(OAI_OK, choices=[{"message": {"content": probe}, "finish_reason": "stop"}]),
            "openai:gpt-6-luna-pro": dict(RESP_INCOMPLETE, status="completed", incomplete_details=None,
                                          output=[{"type": "message", "content": [{"type": "output_text", "text": probe}]}]),
            "google:gemini-3.5-flash-lite": dict(GEM_OK, candidates=[{"content": {"parts": [{"text": probe}]},
                                                                      "finishReason": "STOP"}]),
            "openrouter:deepseek/deepseek-v3.2": dict(OR_OK, choices=[{"message": {"content": probe}, "finish_reason": "stop"}]),
        }
        for model, rep in replies.items():
            with self.subTest(model=model):
                r, sent = self.call(model, "instant", rep, schema=PROBE_SCHEMA, max_tokens=64)
                self.assertEqual((r["text"], r["letter"], r["error"], r["done"]), (probe, "?", None, "stop"))
                self.assertIn('"probability"', json.dumps(sent[0][2]))


class TestParse(Base):
    def test_anthropic_ok_and_cost(self):
        r, sent = self.call("anthropic:claude-haiku-5-5", "instant", ANT_OK)
        self.assertEqual((r["letter"], r["done"], r["error"], r["prompt_tokens"], r["out_tokens"]),
                         ("A", "stop", None, 300, 8))
        self.assertEqual(r["reasoning_tokens"], 0)
        self.assertEqual(r["sampling"], "default")
        self.assertAlmostEqual(r["cost_usd"], (300 * 0.10 + 8 * 0.50) / 1e6)
        self.assertEqual(sent[0][1]["x-api-key"], FAKE["ANTHROPIC_API_KEY"])
        self.assertAlmostEqual(ac.ledger_total("anthropic", self.ledger), r["cost_usd"])

    def test_anthropic_output_limit_with_thinking(self):
        r, _ = self.call("anthropic:claude-opus-5-5", "instant", ANT_THINK_LEN)
        self.assertEqual((r["done"], r["letter"], r["text"], r["reasoning_tokens"]), ("length", "?", "", 4128))
        self.assertAlmostEqual(r["cost_usd"], (300 * 4 + 4128 * 20) / 1e6)

    def test_openai_ok_and_length(self):
        r, sent = self.call("openai:gpt-6-luna", "instant", OAI_OK)
        self.assertEqual((r["letter"], r["done"], r["sampling"], r["provider_model"]),
                         ("B", "stop", "temperature=0", "gpt-6-luna"))
        self.assertEqual(sent[0][1]["Authorization"], "Bearer " + FAKE["OPENAI_API_KEY"])
        r, _ = self.call("openai:gpt-6-luna", "instant", OAI_LEN)
        self.assertEqual((r["done"], r["letter"], r["reasoning_tokens"]), ("length", "?", 32))

    def test_responses_incomplete_reasoning(self):
        r, sent = self.call("openai:gpt-6-luna-pro", "reasoned", RESP_INCOMPLETE)
        self.assertTrue(sent[0][0].endswith("/v1/responses"))
        self.assertEqual((r["done"], r["letter"], r["reasoning_tokens"], r["out_tokens"]), ("length", "C", 3900, 4000))

    def test_gemini_thoughts_and_length(self):
        r, sent = self.call("google:gemini-3.5-flash-lite", "instant", GEM_OK)
        self.assertEqual((r["letter"], r["done"], r["text"], r["reasoning_tokens"], r["out_tokens"]),
                         ("D", "stop", '{"answer": "D"}', 40, 49))
        self.assertEqual(sent[0][1]["x-goog-api-key"], FAKE["GEMINI_API_KEY"])
        r, _ = self.call("google:gemini-4-argon", "instant", GEM_LEN)
        self.assertEqual((r["done"], r["letter"], r["reasoning_tokens"]), ("length", "?", 4128))

    def test_openrouter_reported_cost(self):
        r, _ = self.call("openrouter:meta-llama/llama-3.3-70b-instruct", "reasoned", OR_OK)
        self.assertEqual((r["letter"], r["cost_usd"]), ("A", 0.0002))


class TestErrors(Base):
    def test_sampling_rejected_retry_once(self):
        def reply(body):
            if "temperature" in body:
                raise ac.HTTPFail(400, '{"error": {"message": "Unsupported parameter: temperature"}}')
            return OAI_OK
        r, sent = self.call("openai:gpt-6-luna", "instant", reply)
        self.assertEqual((len(sent), r["sampling"], r["error"], r["letter"]), (2, "default", None, "B"))
        self.assertNotIn("seed", sent[1][2])
        r, sent = self.call("openai:gpt-6-luna", "instant", reply)   # remembered: no second 400
        self.assertEqual(len(sent), 1)

    def test_gemini_format_fallback(self):
        def reply(body):
            if "responseFormat" in body["generationConfig"]:
                raise ac.HTTPFail(400, 'Invalid JSON payload received. Unknown name "responseFormat" at '
                                       "'generation_config': Cannot find field.")
            return GEM_OK
        r, sent = self.call("google:gemini-3.5-flash-lite", "instant", reply)
        self.assertEqual((len(sent), r["error"], r["letter"]), (2, None, "D"))
        gc = sent[1][2]["generationConfig"]
        self.assertEqual((gc["responseMimeType"], gc["responseJsonSchema"]["required"]), ("application/json", ["answer"]))
        r, sent = self.call("google:gemini-3.5-flash-lite", "instant", reply)   # remembered
        self.assertEqual(len(sent), 1)

    def test_openrouter_luna_no_temperature(self):
        b = ac.build_request("openrouter:openai/gpt-6-luna", MSGS["instant"], "instant", FAKE)[2]
        self.assertNotIn("temperature", b)
        self.assertEqual(b["seed"], 7)
        r, _ = self.call("openrouter:openai/gpt-6-luna", "instant", OAI_OK)
        self.assertEqual(r["sampling"], "default")
        b = ac.build_request("openrouter:meta-llama/llama-3.3-70b-instruct", MSGS["instant"], "instant", FAKE)[2]
        self.assertEqual(b["temperature"], 0.0)

    def test_openrouter_provider_pinning(self):
        pins = {"openrouter:mistralai/ministral-14b-2512": "mistral/zdr",
                "openrouter:deepseek/deepseek-v3.2": "atlas-cloud/fp8",
                "openrouter:meta-llama/llama-3.3-70b-instruct": "coreweave/fp16"}
        for model, pin in pins.items():
            with self.subTest(model=model):
                b = ac.build_request(model, MSGS["instant"], "instant", FAKE)[2]
                self.assertEqual(b["provider"], {"order": [pin], "allow_fallbacks": False, "require_parameters": True})
                b = ac.build_request(model, MSGS["reasoned"], "reasoned", FAKE)[2]
                self.assertEqual(b["provider"], {"order": [pin], "allow_fallbacks": False})
                b = ac.build_request(model, MSGS["instant"], "instant", FAKE, schema=PROBE_SCHEMA, max_tokens=64)[2]
                self.assertEqual(b["provider"]["order"], [pin])
        # unpinned entries keep only require_parameters in instant mode
        b = ac.build_request("openrouter:openai/gpt-6-luna", MSGS["instant"], "instant", FAKE)[2]
        self.assertEqual(b["provider"], {"require_parameters": True})

    def test_openrouter_serving_provider_recorded(self):
        r, _ = self.call("openrouter:deepseek/deepseek-v3.2", "instant", dict(OR_OK, provider="AtlasCloud"))
        self.assertEqual((r["serving_provider"], r["pinned_provider"], r["provider_mismatch"]),
                         ("AtlasCloud", "atlas-cloud/fp8", False))
        r, _ = self.call("openrouter:meta-llama/llama-3.3-70b-instruct", "instant", dict(OR_OK, provider="DeepInfra"))
        self.assertTrue(r["provider_mismatch"])
        r, _ = self.call("openrouter:mistralai/ministral-14b-2512", "reasoned", dict(OR_OK, provider="Mistral"))
        self.assertFalse(r["provider_mismatch"])
        r, _ = self.call("openrouter:deepseek/deepseek-v3.2", "instant", ac.HTTPFail(404, "No endpoints found"))
        self.assertEqual((r["letter"], r["pinned_provider"]), ("?", "atlas-cloud/fp8"))

    def test_http_error_scrubbed(self):
        err = ac.HTTPFail(401, "invalid key " + FAKE["OPENROUTER_API_KEY"])
        r, _ = self.call("openrouter:deepseek/deepseek-v3.2", "instant", err)
        self.assertEqual(r["letter"], "?")
        self.assertIn("401", r["error"])
        self.assertNotIn(FAKE["OPENROUTER_API_KEY"], r["error"])

    def test_no_key_and_vertex_only(self):
        env = dict(FAKE, GEMINI_API_KEY="", GOOGLE_CLOUD_PROJECT="p", GOOGLE_APPLICATION_CREDENTIALS="c.json")
        r, sent = self.call("google:gemini-4-argon", "instant", GEM_OK, env=env)
        self.assertIn("Vertex", r["error"])
        self.assertEqual(sent, [])
        r, sent = self.call("openai:gpt-6-luna", "instant", OAI_OK, env=dict(FAKE, OPENAI_API_KEY=""))
        self.assertTrue(r["error"].startswith("no key"))
        self.assertEqual(sent, [])

    def test_bad_model_never_raises(self):
        for m in ("nocolon", "foo:bar", "openai:gpt-unknown"):
            r, sent = self.call(m, "instant", OAI_OK)
            self.assertEqual(r["letter"], "?")
            self.assertTrue(r["error"])
            self.assertEqual(sent, [])
        self.assertIn("no price entry", self.call("openai:gpt-unknown", "instant", OAI_OK)[0]["error"])

    def test_retry_429_then_ok(self):
        import io
        import urllib.error
        calls, sleeps = [], []
        orig = ac._OPENER.open

        class Resp(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        def fake_urlopen(req, timeout=None):
            calls.append(timeout)
            if len(calls) < 3:
                raise urllib.error.HTTPError(req.full_url, 429, "rate", {"Retry-After": "7"}, io.BytesIO(b"slow"))
            return Resp(json.dumps(OAI_OK).encode())
        ac._OPENER.open = fake_urlopen
        try:
            d = ac.http_json("POST", "https://example.invalid/x", {}, {"a": 1}, sleep=sleeps.append)
        finally:
            ac._OPENER.open = orig
        self.assertEqual(d["model"], "gpt-6-luna")
        self.assertEqual(calls, [120, 120, 120])
        self.assertEqual(sleeps, [7.0, 7.0])


class TestLedger(Base):
    def test_cap_reached(self):
        ac.ledger_add("openai", "gpt-6-luna", 1.0, self.ledger)
        r, sent = self.call("openai:gpt-6-luna", "instant", OAI_OK)
        self.assertEqual((r["error"], r["letter"], sent), ("budget cap reached", "?", []))

    def test_cap_zero_or_missing(self):
        for env in (dict(FAKE, BUDGET_USD_ANTHROPIC="0"), {k: v for k, v in FAKE.items() if k != "BUDGET_USD_ANTHROPIC"}):
            r, sent = self.call("anthropic:claude-haiku-5-5", "instant", ANT_OK, env=env)
            self.assertIn("provider disabled", r["error"])
            self.assertEqual(sent, [])

    def test_missing_price(self):
        r, sent = self.call("anthropic:claude-haiku-9", "instant", ANT_OK)
        self.assertIn("no price entry", r["error"])
        self.assertEqual(sent, [])

    def test_concurrent_8_threads(self):
        def work():
            for _ in range(50):
                ac.ledger_add("google", "m", 0.001, self.ledger)
        ts = [threading.Thread(target=work) for _ in range(8)]
        [t.start() for t in ts]
        [t.join() for t in ts]
        with open(self.ledger, encoding="utf-8") as f:
            d = json.load(f)
        self.assertEqual(d["google"]["calls"], 400)
        self.assertAlmostEqual(d["google"]["usd"], 0.4, places=9)

    def test_concurrent_4_processes(self):
        import subprocess
        here = os.path.dirname(os.path.abspath(__file__))
        code = ("import sys; sys.path.insert(0, sys.argv[1]); import api_client as ac\n"
                "for _ in range(50): ac.ledger_add('openrouter', 'm', 0.001, sys.argv[2])\n")
        procs = [subprocess.Popen([sys.executable, "-I", "-c", code, here, self.ledger]) for _ in range(4)]
        self.assertEqual([p.wait(timeout=120) for p in procs], [0, 0, 0, 0])
        with open(self.ledger, encoding="utf-8") as f:
            d = json.load(f)
        self.assertEqual(d["openrouter"]["calls"], 200)
        self.assertAlmostEqual(d["openrouter"]["usd"], 0.2, places=9)
        self.assertFalse(os.path.exists(self.ledger + ".lock"))
        self.assertEqual([n for n in os.listdir(os.path.dirname(self.ledger)) if n.endswith(".tmp")], [])

    def test_stale_lock_broken(self):
        os.makedirs(os.path.dirname(self.ledger), exist_ok=True)
        lock = self.ledger + ".lock"
        open(lock, "w").close()
        old = time.time() - ac.LOCK_STALE_S - 5
        os.utime(lock, (old, old))
        ac.ledger_add("openai", "m", 0.5, self.ledger)
        self.assertAlmostEqual(ac.ledger_total("openai", self.ledger), 0.5)
        self.assertFalse(os.path.exists(lock))

    def test_fresh_lock_waits(self):
        os.makedirs(os.path.dirname(self.ledger), exist_ok=True)
        lock = self.ledger + ".lock"
        open(lock, "w").close()
        orig = ac.LOCK_WAIT_S
        ac.LOCK_WAIT_S = 0.2
        try:
            with self.assertRaises(TimeoutError):
                ac.ledger_add("openai", "m", 0.5, self.ledger)
        finally:
            ac.LOCK_WAIT_S = orig
            os.remove(lock)
        r, sent = self.call("openai:gpt-6-luna", "instant", OAI_OK)   # works once the lock is gone
        self.assertIsNone(r["error"])

    def test_concurrent_chat_api_calls(self):
        out = []

        def work():
            for _ in range(10):
                out.append(ac.chat_api("openai:gpt-6-luna", MSGS["instant"], "instant", env=FAKE,
                                       ledger_path=self.ledger, transport=lambda *a, **k: OAI_OK))
        ts = [threading.Thread(target=work) for _ in range(8)]
        [t.start() for t in ts]
        [t.join() for t in ts]
        self.assertTrue(all(r["error"] is None and r["letter"] == "B" for r in out))
        self.assertAlmostEqual(ac.ledger_total("openai", self.ledger), 80 * (310 * 0.10 + 7 * 0.50) / 1e6)


class TestEnvfile(unittest.TestCase):
    def test_parse(self):
        d = tempfile.mkdtemp()
        try:
            p = os.path.join(d, ".env")
            with open(p, "w", encoding="utf-8") as f:
                f.write("# comment\n\nOPENAI_API_KEY=sk-abc#123\n  GEMINI_API_KEY = g-val  \nEMPTY=\n"
                        "export ANTHROPIC_API_KEY=a-val\nnot a line\nBUDGET_USD_OPENAI=2.5\n")
            before = dict(os.environ)
            env = envfile.load(p)
            self.assertEqual(dict(os.environ), before)   # os.environ untouched
            self.assertEqual(env, {"OPENAI_API_KEY": "sk-abc#123", "GEMINI_API_KEY": "g-val", "EMPTY": "",
                                   "ANTHROPIC_API_KEY": "a-val", "BUDGET_USD_OPENAI": "2.5"})
            self.assertEqual(envfile.scrub("x sk-abc#123 y g-val", env), "x [REDACTED] y [REDACTED]")
            self.assertEqual(envfile.load(os.path.join(d, "missing.env")), {})
        finally:
            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=1)
