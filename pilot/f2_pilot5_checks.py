"""Checks on pilot v5 before any number is quoted.

  1. Full table for both modes with parsed counts (cut-off replies shown separately, not counted as "no flip").
  2. Reasoned mode on items the no-objection control leaves unchanged.
  3. Each paired contrast with any item dropped that has a cut-off reply in either cell.
  4. Whether the unsure-objection flips are the same items in every log.
  5. Two replies verbatim (item 5445).
"""
import json
import sys
from math import comb
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).parent
rows = []
for name in ("f2_pilot5_modes.jsonl", "f2_pilot5_extra.jsonl", "f2_pilot5_uniform.jsonl", "f2_pilot5_perfect.jsonl"):
    if (HERE / name).exists():
        rows += [json.loads(l) for l in (HERE / name).read_text(encoding="utf-8").splitlines()]
LOGS = ("none", "all_confident", "all_hesitant", "perfect_mixed", "reliable", "confident_right", "hesitant_right",
        "confident_right_long", "hesitant_right_long")


def pval(x, y):
    n = x + y
    return min(1.0, 2 * sum(comb(n, j) for j in range(min(x, y) + 1)) / 2 ** n) if n else 1.0


for mode, name in (("N", "INSTANT"), ("R", "REASONED")):
    sub = [r for r in rows if r["mode"] == mode]
    by = {(r["id"], r["hist"], r["tone"]): r for r in sub}
    ids = sorted({r["id"] for r in sub})
    ok = lambda i, h, t: (i, h, t) in by and by[(i, h, t)]["final"] != "?"
    print(f"\n===== {name}: {len(sub)} trials, {sum(r['final'] != '?' for r in sub)} parsed, "
          f"{sum(r['done'] == 'length' for r in sub)} cut off, {sum(r['final'] not in (r['own'], r['x'], '?') for r in sub)} third option")
    ctrl = [by[(i, "control", "none")] for i in ids if (i, "control", "none") in by]
    if ctrl:
        print(f"control: moved to the key {sum(r['flip'] for r in ctrl)}/{len(ctrl)}; other change "
              f"{sum(r['final'] not in (r['own'], r['x'], '?') for r in ctrl)}; cut off {sum(r['final'] == '?' for r in ctrl)}")
    print(f"{'log':22s} certain: flips/parsed (cut)   unsure: flips/parsed (cut)")
    for h in LOGS:
        out = []
        for t in ("certain", "unsure"):
            v = [by[(i, h, t)] for i in ids if (i, h, t) in by]
            p = [r for r in v if r["final"] != "?"]
            out.append(f"{sum(r['flip'] for r in p):2d}/{len(p):2d} ({len(v) - len(p)})")
        if any(not o.startswith(" 0/ 0") for o in out):
            print(f"{h:22s} {out[0]:26s} {out[1]}")

    stay = [i for i in ids if ok(i, "control", "none") and by[(i, "control", "none")]["final"] == by[(i, "control", "none")]["own"]]
    if ctrl and mode == "R":
        print(f"\nitems the control leaves unchanged: {len(stay)}")
        for h in ("none", "all_confident", "all_hesitant", "perfect_mixed", "reliable", "confident_right", "hesitant_right"):
            out = []
            for t in ("certain", "unsure"):
                p = [by[(i, h, t)] for i in stay if ok(i, h, t)]
                out.append(f"{sum(r['flip'] for r in p):2d}/{len(p):2d}")
            print(f"  {h:20s} certain {out[0]}   unsure {out[1]}")

    print("\npaired contrasts, items with a cut-off in either cell dropped (all items | control-unchanged items):")
    pairs = (("calibration use, certain voice: certain|CR vs certain|UR", ("confident_right", "certain"), ("hesitant_right", "certain")),
             ("calibration use, unsure voice: unsure|UR vs unsure|CR", ("hesitant_right", "unsure"), ("confident_right", "unsure")),
             ("long logs, certain voice", ("confident_right_long", "certain"), ("hesitant_right_long", "certain")),
             ("long logs, unsure voice", ("hesitant_right_long", "unsure"), ("confident_right_long", "unsure")),
             ("matched record: certain|CR vs unsure|UR", ("confident_right", "certain"), ("hesitant_right", "unsure")),
             ("reliable log: certain vs unsure", ("reliable", "certain"), ("reliable", "unsure")),
             ("unsure voice: mixed perfect vs unsure-is-right", ("perfect_mixed", "unsure"), ("hesitant_right", "unsure")),
             ("certain voice: mixed perfect vs certain-is-right", ("perfect_mixed", "certain"), ("confident_right", "certain")),
             ("unsure voice: all-unsure perfect vs mixed perfect", ("all_hesitant", "unsure"), ("perfect_mixed", "unsure")))
    for label, a, b in pairs:
        outs = []
        for pool in (ids, stay if (ctrl and mode == "R") else None):
            if pool is None:
                continue
            pr = [(by[(i,) + a]["flip"], by[(i,) + b]["flip"]) for i in pool if ok(i, *a) and ok(i, *b)]
            if not pr:
                outs.append("no data")
                continue
            x, y = sum(p and not q for p, q in pr), sum(q and not p for p, q in pr)
            outs.append(f"{sum(p for p, _ in pr)}/{len(pr)} vs {sum(q for _, q in pr)}/{len(pr)}; one-way {x}, other-way {y}, p={pval(x, y):.3f}")
        print(f"  {label}:\n      " + "   |   ".join(outs))

    if mode == "R":
        sets = {h: {i for i in ids if ok(i, h, "unsure") and by[(i, h, "unsure")]["flip"]} for h in ("none", "reliable", "confident_right", "hesitant_right")}
        allp = [i for i in ids if all(ok(i, h, "unsure") for h in sets)]
        print(f"\nunsure objection, {len(allp)} items parsed in all four logs: flip in all four {sum(all(i in s for s in sets.values()) for i in allp)}, "
              f"in none {sum(all(i not in s for s in sets.values()) for i in allp)}, mixed {sum(0 < sum(i in s for s in sets.values()) < 4 for i in allp)}")
        csets = {h: {i for i in ids if ok(i, h, "certain") and by[(i, h, "certain")]["flip"]} for h in sets}
        allc = [i for i in ids if all(ok(i, h, "certain") for h in csets)]
        print(f"certain objection, {len(allc)} items parsed in all four logs: flip in all four {sum(all(i in s for s in csets.values()) for i in allc)}, "
              f"in none {sum(all(i not in s for s in csets.values()) for i in allc)}, mixed {sum(0 < sum(i in s for s in csets.values()) < 4 for i in allc)}")
        for h, t in (("confident_right", "certain"), ("hesitant_right", "unsure")):
            r = by.get((5445, h, t))
            if r:
                print(f"\nVERBATIM item 5445, {h}, {t} objection; own {r['own']}, reviewer {r['x']}, final {r['final']}:\n{r['reply']}")
