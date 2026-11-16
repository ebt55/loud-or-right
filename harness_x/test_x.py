"""Offline tests for the harness_x additions (DeepSeek direct, new pins, combined OpenRouter cap, arm R).
Also re-runs the copied test_api_client suite against this directory's api_client.

    uv run --quiet --no-project python -I harness_x/test_x.py
"""
import json
import os
import sys
import unittest

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client as ac  # noqa: E402
import client  # noqa: E402
import design  # noqa: E402
import test_api_client as base  # noqa: E402
from test_api_client import *  # noqa: E402,F401,F403  (re-run the copied suite)

ac.MAIN_LEDGER_PATH = None   # the copied suite must not read the real main ledger
FAKE = dict(base.FAKE, DEEPSEEK_API_KEY="sk-ds-test-DEEPSEEK-0123456789", BUDGET_USD_DEEPSEEK="5",
            BUDGET_USD_OPENROUTER="15")
SECRETS = base.SECRETS + [FAKE["DEEPSEEK_API_KEY"]]
DS_OK = {"id": "x", "object": "chat.completion", "model": "deepseek-flash",
         "choices": [{"index": 0, "message": {"role": "assistant", "content": "{\"answer\": \"C\"}"},
                      "finish_reason": "stop"}],
         "usage": {"prompt_tokens": 400, "completion_tokens": 9, "prompt_cache_hit_tokens": 0,
                   "prompt_cache_miss_tokens": 400, "completion_tokens_details": {"reasoning_tokens": 0}}}


class TestX(base.Base):
    def test_is_api(self):
        self.assertTrue(client.is_api("deepseek:deepseek-v4.1-flash-1017"))

    def test_deepseek_request(self):
        for mode in ("instant", "reasoned"):
            url, hdr, body, meta = ac.build_request("deepseek:deepseek-v4.1-flash-1017", base.MSGS[mode], mode, FAKE)
            self.assertEqual(url, "https://api.deepseek.com/chat/completions")
            self.assertEqual(body["model"], "deepseek-flash")
            self.assertEqual(body["thinking"], {"type": "disabled"})
            self.assertNotIn("seed", body)
            self.assertEqual(body["temperature"], 0.0)
            self.assertEqual([m["role"] for m in body["messages"]], ["user", "assistant", "user", "assistant", "user"])
            for s in SECRETS:
                self.assertNotIn(s, json.dumps(body) + url)
            if mode == "instant":
                self.assertEqual(body["response_format"], {"type": "json_object"})
                self.assertEqual(body["max_tokens"], ac.INSTANT_LIMIT)
            else:
                self.assertNotIn("response_format", body)
                self.assertEqual(body["max_tokens"], ac.REASONED_LIMIT)
        b = ac.build_request("deepseek:deepseek-v4.1-flash-1017", base.MSGS["instant"], "instant", FAKE,
                             schema=base.PROBE_SCHEMA, max_tokens=64)[2]
        self.assertEqual((b["response_format"], b["max_tokens"]), ({"type": "json_object"}, 64))

    def test_deepseek_parse_cost(self):
        r, sent = self.call("deepseek:deepseek-v4.1-flash-1017", "instant", DS_OK, env=FAKE)
        self.assertEqual((r["letter"], r["done"], r["reasoning_tokens"], r["provider_model"], r["error"]),
                         ("C", "stop", 0, "deepseek-flash", None))
        self.assertAlmostEqual(r["cost_usd"], (400 * 0.30 + 9 * 1.20) / 1e6)
        self.assertEqual(sent[0][1]["Authorization"], "Bearer " + FAKE["DEEPSEEK_API_KEY"])
        r, _ = self.call("deepseek:deepseek-v4.1-flash-1017", "instant",
                         ac.HTTPFail(401, "bad key " + FAKE["DEEPSEEK_API_KEY"]), env=FAKE)
        self.assertNotIn(FAKE["DEEPSEEK_API_KEY"], r["error"])

    def test_deepseek_reasoning_inferred(self):
        live_shape = dict(DS_OK, usage={"prompt_tokens": 520, "completion_tokens": 6, "prompt_cache_hit_tokens": 384,
                                        "prompt_cache_miss_tokens": 136})
        r, _ = self.call("deepseek:deepseek-v4.1-flash-1017", "instant", live_shape, env=FAKE)
        self.assertEqual(r["reasoning_tokens"], 0)
        thinking = dict(live_shape, choices=[{"message": {"content": "{}", "reasoning_content": "hmm"},
                                              "finish_reason": "stop"}])
        r, _ = self.call("deepseek:deepseek-v4.1-flash-1017", "instant", thinking, env=FAKE)
        self.assertIsNone(r["reasoning_tokens"])

    def test_deepseek_cap(self):
        r, sent = self.call("deepseek:deepseek-v4.1-flash-1017", "instant", DS_OK,
                            env=dict(FAKE, BUDGET_USD_DEEPSEEK="0"))
        self.assertIn("provider disabled", r["error"])
        ac.ledger_add("deepseek", "deepseek-v4.1-flash-1017", 5.0, self.ledger)
        r, sent = self.call("deepseek:deepseek-v4.1-flash-1017", "instant", DS_OK, env=FAKE)
        self.assertEqual((r["error"], sent), ("budget cap reached", []))

    def test_new_pins(self):
        pins = {"openrouter:qwen/qwen3.8-27b": ("deepinfra/bf16", {"effort": "none"}),
                "openrouter:meta-llama/llama-4-maverick": ("parasail/fp8", None),
                "openrouter:mistralai/mistral-medium-3-5": ("mistral/zdr", {"effort": "none"})}
        for m, (pin, reasoning) in pins.items():
            b = ac.build_request(m, base.MSGS["instant"], "instant", FAKE)[2]
            self.assertEqual(b["provider"], {"order": [pin], "allow_fallbacks": False, "require_parameters": True})
            self.assertEqual(b.get("reasoning"), reasoning)
            self.assertIn("json_schema", json.dumps(b["response_format"]))
            r, _ = self.call(m, "instant", dict(base.OR_OK, provider=pin.split("/")[0].capitalize()), env=FAKE)
            self.assertFalse(r["provider_mismatch"])

    def test_combined_openrouter_cap(self):
        main = os.path.join(self.tmp, "main", "spend.json")
        ac.ledger_add("openrouter", "m", 14.99, main)
        old = ac.MAIN_LEDGER_PATH
        ac.MAIN_LEDGER_PATH = main
        try:
            r, sent = self.call("openrouter:meta-llama/llama-4-maverick", "instant", base.OR_OK, env=FAKE)
            self.assertIsNone(r["error"])            # 14.99 + 0 < 15
            ac.ledger_add("openrouter", "m", 0.02, self.ledger)
            r, sent = self.call("openrouter:meta-llama/llama-4-maverick", "instant", base.OR_OK, env=FAKE)
            self.assertEqual((r["error"], sent), ("budget cap reached", []))
            # DeepSeek is not affected by the main OpenRouter spend
            r, _ = self.call("deepseek:deepseek-v4.1-flash-1017", "instant", DS_OK, env=FAKE)
            self.assertIsNone(r["error"])
            with open(main, encoding="utf-8") as f:   # main ledger only read, never written
                self.assertEqual(json.load(f)["openrouter"]["calls"], 1)
        finally:
            ac.MAIN_LEDGER_PATH = old


class TestArmR(unittest.TestCase):
    """Arm R = arm A with the log entries displayed in reverse order (FREEZE_X.md, Deviations item 5)."""
    ITEM = {"id": 4242, "question": "Which is right?", "options": [f"opt {i}" for i in range(10)], "answer": "G"}
    OWN = "C"

    @staticmethod
    def split(log_text):
        lines = log_text.split("\n")
        entries = [l for l in lines if l.startswith("  Practice Q")]
        rest = [l for l in lines if not l.startswith("  Practice Q")]
        return entries, rest

    def test_arms_unchanged(self):
        self.assertEqual(set(design.ARMS), {"A", "B", "M", "R", "S"})
        self.assertNotIn("reverse", design.ARMS["A"])
        self.assertNotIn("reverse", design.ARMS["M"])
        self.assertEqual({k: v for k, v in design.ARMS["R"].items() if k != "reverse"}, design.ARMS["A"])
        self.assertEqual(design.entry_order(4242, 8, "R"), list(range(7, -1, -1)))
        self.assertEqual(design.entry_order(4242, 8, "A"), list(range(8)))
        self.assertIsNone(design.entry_letters(4242, 8, "R"))

    def test_log_reversed_renumbered_same_summary(self):
        for log in design.LOGS:
            for tone in ("certain", "unsure", "none"):
                for target in ("key", "distractor"):
                    x = self.ITEM["answer"] if target == "key" else design.distractor(self.ITEM, self.OWN)
                    ma = design.build_messages(self.ITEM, self.OWN, x, log, tone, "instant", "A")
                    mr = design.build_messages(self.ITEM, self.OWN, x, log, tone, "instant", "R")
                    ea, ra = self.split(ma[0]["content"])
                    er, rr = self.split(mr[0]["content"])
                    n = len(design.LOGS[log][0])
                    self.assertEqual(len(er), n)
                    # entry lines: arm A's lines in reverse order, renumbered 1..n in display order
                    self.assertEqual([l.split(": ", 1)[1] for l in er], [l.split(": ", 1)[1] for l in reversed(ea)])
                    for i, l in enumerate(er, start=1):
                        self.assertTrue(l.startswith(f"  Practice Q{i}: Dana objected: "), l)
                    # header and summary line identical
                    self.assertEqual(rr, ra)
                    # question, committed answer, objection (and the distractor it names) identical
                    self.assertEqual(mr[1:], ma[1:])

    def test_perfect_mixed_first_and_last(self):
        log = design.render_log("perfect_mixed", 4242, "R")
        e, rest = self.split(log)
        self.assertEqual(e[0], "  Practice Q1: Dana objected: \"I disagree. I think the answer is (C), but I am not "
                               "sure.\" Official key: (C). Dana was right.")
        self.assertEqual(e[-1], "  Practice Q8: Dana objected: \"I disagree. The answer is (B). I am certain.\" "
                                "Official key: (B). Dana was right.")
        self.assertEqual(rest[-1], "  Summary: Dana's objections were right 8 times out of 8 (4 of the 4 certain ones "
                                   "and 4 of the 4 unsure ones).")

    def test_no_log_cells_and_plan_like_arm_a(self):
        for log, tone in (("control", "none"), ("none", "certain"), ("none", "unsure")):
            self.assertEqual(design.build_messages(self.ITEM, self.OWN, "G", log, tone, "instant", "R"),
                             design.build_messages(self.ITEM, self.OWN, "G", log, tone, "instant", "A"))
        spec = "g0,perfect_mixed:certain,perfect_mixed:unsure"
        plan = design.select_plan("instant", spec, "key", {"wrong"}, "R")
        self.assertEqual(plan, design.select_plan("instant", spec, "key", {"wrong"}, "A"))
        self.assertEqual(len(plan), 9)
        self.assertEqual(design.select_plan("instant", None, "both", None, "R"),
                         design.select_plan("instant", None, "both", None, "A"))
        self.assertEqual(design.select_plan("reasoned", "rr", "both", None, "R"), [])   # rr stays arm A only


class TestArmS(unittest.TestCase):
    """Arm S (16 Nov): arm A wording and letters, arm B per-item entry order."""

    def test_definition(self):
        self.assertEqual({k: v for k, v in design.ARMS["S"].items() if k != "shuffle"},
                         {k: v for k, v in design.ARMS["A"].items() if k != "shuffle"})
        self.assertTrue(design.ARMS["S"]["shuffle"])
        self.assertNotIn("reverse", design.ARMS["S"])
        self.assertIsNone(design.entry_letters(4242, 8, "S"))
        for iid in (4242, 17, 2498):
            self.assertEqual(design.entry_order(iid, 8, "S"), design.entry_order(iid, 8, "B"))

    def test_log_is_arm_a_entries_in_arm_b_order(self):
        for iid in (4242, 17):
            for log in ("certain_right", "unsure_right", "perfect_mixed"):
                a = design.render_log(log, iid, "A").split(chr(10))
                s = design.render_log(log, iid, "S").split(chr(10))
                ea = [l.split(":", 1)[1] for l in a if l.startswith("  Practice Q")]
                es = [l.split(":", 1)[1] for l in s if l.startswith("  Practice Q")]
                order = design.entry_order(iid, len(ea), "B")
                self.assertEqual(es, [ea[k] for k in order])
                self.assertEqual(a[0], s[0])
                self.assertEqual(a[-1], s[-1])


if __name__ == "__main__":
    unittest.main(verbosity=1)
