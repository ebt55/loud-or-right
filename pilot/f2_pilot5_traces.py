"""Reasoned-mode traces from pilot v5: how often the reply mentions the log, and what it says when it does."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).parent
rows = []
for name in ("f2_pilot5_modes.jsonl", "f2_pilot5_extra.jsonl"):
    p = HERE / name
    if p.exists():
        rows += [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()]
rows = [r for r in rows if r["mode"] == "R" and r["hist"] not in ("none", "control")]
LOG = re.compile(r"practice|\blog\b|track record|out of \d+|of the \d+|\d+/\d+|100%|historically|past objections", re.I)
print(f"{'log':22s} {'tone':8s}  mentions log / trials   flips among mentions   flips among non-mentions")
for h in sorted({r["hist"] for r in rows}):
    for t in ("certain", "unsure"):
        sub = [r for r in rows if r["hist"] == h and r["tone"] == t and r["final"] != "?"]
        m = [r for r in sub if LOG.search(r["reply"])]
        n = [r for r in sub if not LOG.search(r["reply"])]
        print(f"{h:22s} {t:8s}  {len(m):3d} / {len(sub):3d}            {sum(r['flip'] for r in m):3d} / {len(m):3d}             {sum(r['flip'] for r in n):3d} / {len(n):3d}")
show = int(sys.argv[1]) if len(sys.argv) > 1 else 6
for h, t in (("hesitant_right", "unsure"), ("hesitant_right", "certain"), ("confident_right", "certain"), ("reliable", "unsure")):
    print(f"\n--- {h} / {t}: sentences that mention the log")
    k = 0
    for r in rows:
        if r["hist"] == h and r["tone"] == t and LOG.search(r["reply"]):
            sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", " ".join(r["reply"].split())) if LOG.search(s) or "Dana" in s]
            print(f"[item {r['id']}; own {r['own']}, reviewer {r['x']}, final {r['final']}] " + " ".join(sents)[:380])
            k += 1
            if k >= show:
                break
