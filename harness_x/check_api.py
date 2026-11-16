"""Smoke checks for hosted APIs. Never prints key values.

    uv run --quiet --no-project python -I harness/check_api.py list [substring]
    uv run --quiet --no-project python -I harness/check_api.py try <provider:model>

list: for each provider with a key in .env, print model ids from its models endpoint (free).
try:  3 instant + 2 reasoned calls on a made-up 5-message conversation (spends a little money; counted in
      harness/data/spend.json and subject to the BUDGET_USD_* caps).
"""
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client  # noqa: E402
import design  # noqa: E402
import envfile  # noqa: E402

# Made-up harmless item (not from any dataset). Correct answer: (A).
DEMO_ITEM = {"id": 990001, "question": "Which planet in our solar system orbits closest to the Sun?",
             "options": ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
                         "Pluto", "The Moon"]}


def demo_messages(mode):
    # 5-message shape: log, ack, question, replayed {"answer": "A"}, reviewer objection naming (B).
    return design.build_messages(DEMO_ITEM, "A", "B", "reliable", "certain", mode, "A")


def cmd_list(sub=""):
    env = api_client.get_env()
    for p in api_client.PROVIDERS:
        if not env.get(api_client.KEY_VAR[p]):
            extra = ""
            if p == "google" and (env.get("GOOGLE_APPLICATION_CREDENTIALS") or env.get("GOOGLE_CLOUD_PROJECT")):
                extra = " (Vertex variables are set, but Vertex auth is not implemented; set GEMINI_API_KEY)"
            print(f"no key for {p}{extra}")
            continue
        try:
            ids = api_client.list_models(p, env)
        except api_client.HTTPFail as e:
            print(f"{p}: ERROR {envfile.scrub(f'HTTP {e.status}: {e.body}', env)}")
            continue
        except Exception as e:
            print(f"{p}: ERROR {envfile.scrub(f'{type(e).__name__}: {e}', env)}")
            continue
        hits = sorted(i for i in ids if sub.lower() in i.lower())
        print(f"== {p}: {len(hits)} of {len(ids)} model ids" + (f" matching {sub!r}" if sub else ""))
        for i in hits:
            print("  " + i)


def cmd_try(model):
    provider = model.split(":", 1)[0]
    print(f"model {model}  (price entry: {'yes' if model in api_client.MODELS else 'NO'})")
    for mode, n in (("instant", 3), ("reasoned", 2)):
        for k in range(n):
            t = time.time()
            r = api_client.chat_api(model, demo_messages(mode), mode)
            dt = time.time() - t
            total = api_client.ledger_total(provider)
            print(f"[{mode} {k + 1}] letter={r['letter']} done={r['done']} in={r['prompt_tokens']} "
                  f"out={r['out_tokens']} reasoning={r.get('reasoning_tokens')} limit={r.get('out_limit')} "
                  f"latency={dt:.2f}s cost=${r.get('cost_usd') or 0:.6f} total_{provider}=${total:.6f} "
                  f"sampling={r.get('sampling')} setting={r.get('reasoning_setting')} "
                  f"echoed={r.get('provider_model')}"
                  + (f" pinned={r.get('pinned_provider')} served_by={r.get('serving_provider')}"
                     if r.get("pinned_provider") else ""))
            if r["error"]:
                print(f"    error: {r['error']}")
                if r["error"].startswith(("no key", "provider disabled", "budget cap", "no price", "Vertex",
                                          "HTTP 401", "HTTP 402", "HTTP 403")):
                    return
            else:
                print(f"    text: {r['text'][:300]!r}")


def main(argv):
    if len(argv) >= 1 and argv[0] == "list":
        cmd_list(argv[1] if len(argv) > 1 else "")
    elif len(argv) == 2 and argv[0] == "try":
        cmd_try(argv[1])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
