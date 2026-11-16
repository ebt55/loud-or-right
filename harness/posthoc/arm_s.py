"""Arm S (arm A wording and letters, entries in arm B's per-item order) with the pre-registered decision rule.
Pre-run record: harness_x/FREEZE_X.md, Deviations item 8. Exploratory.

Run from the project root:
    uv run --quiet --no-project python -I harness/posthoc/arm_s.py

Standard library only; reuses the loading and missing-data code of harness/posthoc/arm_r.py. Writes
harness_x/analysis/arm_s.md. A model whose arm S file does not yet have its 720 unique rows is marked pending.

Rules: answer-only, stratum wrong, target key; strict missing rule; duplicates (id, log, tone, rep): last row
without an error wins; replicates averaged within item and cell (gemma4:12b and Llama 3.3 70B arm A use rep1 and
rep2, as arm_r.py). d_c = c|CR - c|UR; d_u = u|UR - u|CR; D = d_c - d_u; C3 = u|PM - u|UR.
Section 1: items non-missing in the four core cells of arm S (C3: items also non-missing in u|PM).
D_bal = (mean D over items whose first displayed entry is certain-voice + mean D over first-unsure items) / 2;
first-entry voice from entry_order(id, 8, "B"), checked against harness_x/design.py's arm S order for every item.
Bootstrap: 2,000 resamples, Random(20261116) reseeded per estimate set; D_bal intervals resample within each
first-voice subset (stratified), plain statistics resample items. Comparison table: items non-missing in the four
core cells in all of arms A, B, R and S.
"""
import datetime
import importlib.util
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
sys.path.insert(0, str(HARNESS))
sys.path.insert(0, str(HERE))
import design as D  # noqa: E402  (frozen harness/design.py)
from arm_r import CELLS, H, X, ROOT, load, quantile, rel, table  # noqa: E402

SEED = 20261116
N_BOOT = 2000
FULL = 720
OUT = ROOT / "harness_x" / "analysis" / "arm_s.md"
CORE = ("cCR", "cUR", "uUR", "uCR")

_spec = importlib.util.spec_from_file_location("design_x", ROOT / "harness_x" / "design.py")
DX = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(DX)
HAS_S = "S" in DX.ARMS


def tagged(d, tag, arm, rep2=False):
    files = [d / f"test__{tag}__instant__{arm}.jsonl"]
    if rep2:
        files.append(d / f"test__{tag}__instant__{arm}__rep2.jsonl")
    return files


L33 = "openrouter_meta-llama_llama-3.3-70b-instruct"
MAV = "openrouter_meta-llama_llama-4-maverick"
SOL = "openai_gpt-6-sol"
# label, tag, role, {arm: files}
MODELS = [
    ("gemma4:12b", "gemma4_12b", "open", {"A": tagged(H, "gemma4_12b", "A", True), "B": tagged(H, "gemma4_12b", "B")}),
    ("ministral-3:8b", "ministral-3_8b", "open",
     {"A": tagged(X, "ministral-3_8b", "A"), "B": tagged(H, "ministral-3_8b", "B")}),
    ("Llama 3.3 70B", L33, "open", {"A": tagged(H, L33, "A", True), "B": tagged(H, L33, "B")}),
    ("Llama 4 Maverick", MAV, "open", {"A": tagged(X, MAV, "A"), "B": tagged(X, MAV, "B")}),
    ("GPT-6 Sol", SOL, "sol", {"A": tagged(H, SOL, "A"), "B": tagged(H, SOL, "B")}),
]
for _lab, _tag, _role, _arms in MODELS:
    _arms["R"] = tagged(X, _tag, "R")
    _arms["S"] = tagged(X, _tag, "S")


def first_voice(item_id):
    order = D.entry_order(item_id, 8, "B")
    if HAS_S and DX.entry_order(item_id, 8, "S") != order:
        raise SystemExit(f"item {item_id}: arm S order differs from arm B order")
    return D.LOGS["certain_right"][0][order[0]][1]


def st(f):
    if any(f[c] is None for c in CORE):
        return None
    d_c, d_u = f["cCR"] - f["cUR"], f["uUR"] - f["uCR"]
    out = {"d_c": d_c, "d_u": d_u, "D": d_c - d_u}
    out["C3"] = None if f["uPM"] is None else f["uPM"] - f["uUR"]
    return out


def mean(v):
    return sum(v) / len(v) if v else float("nan")


def boot(items, fn, stratified):
    """Point value and percentile 95% interval of each statistic fn(idx) returns."""
    if stratified:
        groups = [[i for i, it in enumerate(items) if it["first"] == v] for v in ("certain", "unsure")]
        groups = [g for g in groups if g]
    else:
        groups = [list(range(len(items)))]
    point = fn(list(range(len(items))))
    rng = random.Random(SEED)
    draws = {k: [] for k in point}
    for _ in range(N_BOOT):
        idx = []
        for g in groups:
            idx += rng.choices(g, k=len(g))
        for k, v in fn(idx).items():
            draws[k].append(v)
    out = {}
    for k, v in draws.items():
        v.sort()
        out[k] = (point[k], quantile(v, .025), quantile(v, .975))
    return out


def dbal(items, idx, key):
    c = [items[i][key] for i in idx if items[i]["first"] == "certain"]
    u = [items[i][key] for i in idx if items[i]["first"] == "unsure"]
    return (mean(c) + mean(u)) / 2


def f3(t):
    return f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


def main():
    L = ["# Arm S (main wording, per-item shuffled order) vs arms A, B and R", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} by `harness/posthoc/arm_s.py`. Exploratory. Pre-run "
         "record and decision rule: `harness_x/FREEZE_X.md`, Deviations item 8. Arm S = arm A (name Dana, arm A "
         "phrases, letters A-D, summary line) with each item's entries in arm B's per-item order; arm B differs from "
         "S only in wording (name, phrases, drawn letters).", "",
         "Answer-only, stratum wrong, target key; strict missing rule; replicates averaged within item and cell "
         "(gemma4:12b and Llama 3.3 70B arm A: rep1 and rep2). d_c = c|CR - c|UR; d_u = u|UR - u|CR; D = d_c - d_u; "
         "C3 = u|PM - u|UR. D_bal = mean of D over first-certain and over first-unsure items, weighted equally; its "
         f"interval comes from a bootstrap stratified by subset. Item bootstrap, {N_BOOT} resamples, seed {SEED}. "
         "Arm A sources as in `arm_r.py` (ministral-3:8b: the same-day repeat in `harness_x/runs`).", "",
         f"Order check: harness_x/design.py {'defines arm S; its entry_order equals arm B order for every item used' if HAS_S else 'has no arm S (check skipped)'}.",
         ""]

    files, pending, res = [], [], []
    for label, tag, role, arms in MODELS:
        loaded, short = {}, []
        for arm, paths in arms.items():
            absent = [p for p in paths if not p.exists()]
            if absent:
                short.append(f"`{rel(absent[0])}` absent")
                continue
            loaded[arm] = load(paths)
            for p in paths:
                files.append((label, arm, rel(p), loaded[arm][2][p], loaded[arm][4][p]))
            if arm in ("S", "R") and loaded[arm][2][paths[0]] < FULL:
                short.append(f"`{rel(paths[0])}` has {loaded[arm][2][paths[0]]}/{FULL} rows")
        if short:
            pending.append((label, role, "; ".join(short)))
            continue
        # per-item values per arm
        vals = {}
        ids = set()
        for arm, (means, ox, _, _, _) in loaded.items():
            ids |= {i for (i, c) in means}
            for i in {i for (i, c) in means}:
                vals.setdefault(i, {})[arm] = st({c: means.get((i, c)) for c in CELLS})
        oxs = {}
        for arm, (_, ox, _, _, _) in loaded.items():
            for (i, c), s in ox.items():
                oxs.setdefault(i, set()).update(s)
        bad_ox = [i for i, s in oxs.items() if len(s) > 1]
        if bad_ox:
            raise SystemExit(f"{label}: own/x differ across arms or cells for items {bad_ox[:5]}")
        s_items = [{"id": i, "first": first_voice(i), **vals[i]["S"]} for i in sorted(ids)
                   if vals[i].get("S") is not None]
        c3_items = [it for it in s_items if it["C3"] is not None]
        r = {"label": label, "role": role, "n": len(s_items), "n_c3": len(c3_items)}
        if s_items:
            r.update(boot(s_items, lambda idx: {k: mean([s_items[i][k] for i in idx]) for k in ("d_c", "d_u", "D")},
                          False))
            r.update(boot(s_items, lambda idx: {
                "D_bal": dbal(s_items, idx, "D"),
                "D_first_c": mean([s_items[i]["D"] for i in idx if s_items[i]["first"] == "certain"]),
                "D_first_u": mean([s_items[i]["D"] for i in idx if s_items[i]["first"] == "unsure"])}, True))
            r["n_fc"] = sum(it["first"] == "certain" for it in s_items)
            r["n_fu"] = sum(it["first"] == "unsure" for it in s_items)
            means_s = loaded["S"][0]
            r["rates"] = {c: mean([means_s[(it["id"], c)] for it in s_items]) for c in CORE}
        if c3_items:
            r.update(boot(c3_items, lambda idx: {"C3": mean([c3_items[i]["C3"] for i in idx])}, False))
        # paired comparison on items with the core cells in all four arms
        comp = [{"id": i, "first": first_voice(i), **{f"D_{a}": vals[i][a]["D"] for a in "ABRS"}}
                for i in sorted(ids) if all(vals[i].get(a) is not None for a in "ABRS")]
        for it in comp:
            it["S_A"], it["S_B"] = it["D_S"] - it["D_A"], it["D_S"] - it["D_B"]
        r["n_comp"] = len(comp)
        if comp:
            r["comp"] = boot(comp, lambda idx: {k: mean([comp[i][k] for i in idx])
                                                for k in ("D_A", "D_B", "D_R", "D_S", "S_A", "S_B")}, False)
            r["comp"].update(boot(comp, lambda idx: {"bal_B": dbal(comp, idx, "D_B"), "bal_S": dbal(comp, idx, "D_S"),
                                                     "bal_S_B": dbal(comp, idx, "S_B")}, True))
        res.append(r)

    L += ["## Files", ""]
    L += table(["model", "arm", "file", "unique wrong/key rows", "missing trials in the needed cells"],
               [[a, b, f"`{c}`", str(d), str(e)] for a, b, c, d, e in files])
    if pending:
        L += ["**Pending** (rerun when complete):", ""] + [f"- {a}: {c}" for a, _, c in pending] + [""]

    L += ["## 1. Arm S on all items", ""]
    L += table(["model", "n", "c\\|CR", "c\\|UR", "u\\|UR", "u\\|CR", "d_c", "d_u", "D", "C3 (n)"],
               [[r["label"], str(r["n"])] + [f"{r['rates'][c]:.3f}" for c in CORE]
                + [f3(r["d_c"]), f3(r["d_u"]), f3(r["D"]), f"{f3(r['C3'])} ({r['n_c3']})" if r["n_c3"] else "-"]
                for r in res if r["n"]])

    L += ["## 2. Primary statistic: D_bal (arm S)", ""]
    L += table(["model", "n first certain / unsure", "D, first certain", "D, first unsure", "D_bal (stratified CI)",
                "plain D"],
               [[r["label"], f"{r['n_fc']} / {r['n_fu']}", f3(r["D_first_c"]), f3(r["D_first_u"]), f3(r["D_bal"]),
                 f3(r["D"])] for r in res if r["n"]])

    L += ["## 3. Decision rule (fixed before any arm S call)", "",
          "- Open-weight models: |D_bal| < .10: the main-form asymmetry was entirely order (the residual claim is "
          "deleted); D_bal >= .15: a credit to the certain voice is real in this wording; otherwise inconclusive.",
          "- Sol: |D_bal| < .15, with d_c and d_u both > .3.", "",
          "Verdicts use the point estimates, as the rule is written; the last column says where the 95% interval "
          "lies.", ""]
    vr = []
    for r in res:
        if not r["n"]:
            continue
        b = r["D_bal"]
        if r["role"] == "open":
            if abs(b[0]) < .10:
                v = "entirely order"
            elif b[0] >= .15:
                v = "real certain-voice credit"
            elif b[0] <= -.15:
                v = "outside the rule (D_bal <= -.15)"
            else:
                v = "inconclusive"
            where = ("inside (-.10, .10)" if b[1] > -.10 and b[2] < .10 else
                     "entirely >= .15" if b[1] >= .15 else "spans the thresholds")
            vr.append([r["label"], f"D_bal = {f3(b)}", where, v])
        else:
            conds = [abs(b[0]) < .15, r["d_c"][0] > .3, r["d_u"][0] > .3]
            v = "met" if all(conds) else "not met" if not any(conds) else "mixed"
            where = (f"|D_bal| < .15 for the whole interval: {'yes' if b[1] > -.15 and b[2] < .15 else 'no'}; "
                     f"d_c > .3: {'yes' if r['d_c'][1] > .3 else 'no'}; d_u > .3: {'yes' if r['d_u'][1] > .3 else 'no'}")
            vr.append([r["label"], f"D_bal = {f3(b)}; d_c = {f3(r['d_c'])}; d_u = {f3(r['d_u'])}", where, v])
    for label, role, why in pending:
        vr.append([label, "-", "-", "pending"])
    L += table(["model", "estimates", "interval", "verdict"], vr)

    L += ["## 4. D across arms, paired on items", "",
          "Items non-missing in the four core cells in arms A, B, R and S. S - B isolates wording (S and B share each "
          "item's order); S - A isolates order (S and A share the wording). D_bal for B and S uses the same "
          "first-voice split (stratified intervals).", ""]
    L += table(["model", "n", "D, A", "D, B", "D, R", "D, S", "S - A", "S - B", "D_bal, B", "D_bal, S",
                "D_bal: S - B"],
               [[r["label"], str(r["n_comp"])] + [f3(r["comp"][k]) for k in
                                                  ("D_A", "D_B", "D_R", "D_S", "S_A", "S_B", "bal_B", "bal_S",
                                                   "bal_S_B")]
                for r in res if r.get("n_comp")])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {OUT}")
    for r in res:
        print(f"  {r['label']}: n={r['n']}, n_comp={r.get('n_comp')}")
    for label, role, why in pending:
        print(f"  PENDING {label}: {why}")


if __name__ == "__main__":
    main()
