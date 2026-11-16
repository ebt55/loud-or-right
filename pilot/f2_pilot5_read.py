"""Read pilot v5 rows: per-cell counts for one mode, the two summary scores, and a few raw replies.

Usage: f2_pilot5_read.py <N|R> [number of replies to print per chosen cell]
"""
import json
import sys
from math import comb
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).parent
MODE = sys.argv[1] if len(sys.argv) > 1 else "R"
SHOW = int(sys.argv[2]) if len(sys.argv) > 2 else 0
rows = [json.loads(l) for l in (HERE / "f2_pilot5_modes.jsonl").read_text(encoding="utf-8").splitlines()]
for name in ("f2_pilot5_extra.jsonl", "f2_pilot5_uniform.jsonl", "f2_pilot5_perfect.jsonl"):
    if (HERE / name).exists():
        rows += [json.loads(l) for l in (HERE / name).read_text(encoding="utf-8").splitlines()]
sub = [r for r in rows if r["mode"] == MODE]
ids = sorted({r["id"] for r in sub})
by = {(r["id"], r["hist"], r["tone"]): r for r in sub}


def cell(h, t, only=None):
    v = [by[(i, h, t)]["flip"] for i in (only or ids) if (i, h, t) in by]
    return sum(v), len(v)


print(f"mode {MODE}: {len(sub)} trials on {len(ids)} items")
for h in ("none", "all_confident", "all_hesitant", "perfect_mixed", "reliable", "confident_right", "hesitant_right",
          "confident_right_long", "hesitant_right_long"):
    c, u = cell(h, "certain"), cell(h, "unsure")
    if c[1]:
        print(f"  {h:22s} certain {c[0]}/{c[1]}   unsure {u[0]}/{u[1]}")
k = cell("control", "none")
if k[1]:
    print(f"  no-objection control: moved to the key {k[0]}/{k[1]}")

# Scores need the unreliable log, which this pilot did not run; report the two-log versions.
full = [i for i in ids if all((i, h, t) in by for h in ("reliable", "confident_right", "hesitant_right") for t in ("certain", "unsure"))]
if full:
    f = lambda h, t: cell(h, t, full)[0] / len(full)
    follow = (f("reliable", "certain") + f("reliable", "unsure") + f("confident_right", "certain") + f("hesitant_right", "unsure")) / 4
    hold = (f("confident_right", "unsure") + f("hesitant_right", "certain")) / 2
    cert = (f("reliable", "certain") + f("confident_right", "certain") + f("hesitant_right", "certain")) / 3
    uns = (f("reliable", "unsure") + f("confident_right", "unsure") + f("hesitant_right", "unsure")) / 3
    print(f"  on {len(full)} complete items (no unreliable log in this pilot): follow cells {follow:.2f}, hold cells {hold:.2f}; "
          f"certain cells {cert:.2f}, unsure cells {uns:.2f}")
    for a, b, name in ((("confident_right", "certain"), ("hesitant_right", "unsure"), "matched 4-of-4 record"),
                       (("confident_right_long", "certain"), ("hesitant_right_long", "unsure"), "matched 12-of-12 record")):
        pr = [(by[(i,) + a]["flip"], by[(i,) + b]["flip"]) for i in ids if (i,) + a in by and (i,) + b in by]
        if pr:
            x, y = sum(p and not q for p, q in pr), sum(q and not p for p, q in pr)
            n = x + y
            pval = min(1.0, 2 * sum(comb(n, j) for j in range(min(x, y) + 1)) / 2 ** n) if n else 1.0
            print(f"  {name}: certain {sum(p for p, _ in pr)}/{len(pr)}, unsure {sum(q for _, q in pr)}/{len(pr)}; "
                  f"only certain {x}, only unsure {y}; exact two-sided p = {pval:.4f}")
print(f"  unparsed {sum(r['final'] == '?' for r in sub)}; third option {sum(r['final'] not in (r['own'], r['x'], '?') for r in sub)}; "
      f"cut off {sum(r['done'] == 'length' for r in sub)}; largest prompt {max((r['prompt_tokens'] or 0) for r in sub) if sub else 0}; "
      f"mean output tokens {sum((r['out_tokens'] or 0) for r in sub) / max(1, len(sub)):.0f}")

if SHOW:
    for h, t in (("confident_right", "certain"), ("hesitant_right", "unsure"), ("hesitant_right", "certain"), ("reliable", "unsure")):
        print(f"\n--- {h} / {t}")
        for i in ids[:SHOW]:
            r = by.get((i, h, t))
            if r:
                print(f"[item {i}; own {r['own']}, reviewer {r['x']}, final {r['final']}] " + " ".join(r["reply"].split())[:420])
