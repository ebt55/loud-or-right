"""Arm R (log entries shown in reverse order) vs arm A, on the same items. Exploratory; pre-run record and
predictions: harness_x/FREEZE_X.md, Deviations item 5.

Run from the project root:
    uv run --quiet --no-project python -I harness/posthoc/arm_r.py

Standard library only. Writes harness_x/analysis/arm_r_vs_a.md. A pair whose arm R file (or the same-day
ministral arm A repeat) does not yet have its 720 unique rows is marked pending; rerun once it is complete.

Rules (as harness/posthoc/splits.py): stratum "wrong", target "key", answer-only. Duplicates of
(id, log, tone, rep): the last row without an error wins. A trial is missing if error is non-empty, final == "?",
done == "length" or trunc_risk is true. rep = row["rep"], else the file's __rep<K> suffix, else 1; an item's value
in a cell is the mean over its non-missing replicates (missing only if every replicate is), as analyze.py.
Items: non-missing in all five needed cells (certain|certain_right, certain|unsure_right, unsure|unsure_right,
unsure|certain_right, unsure|perfect_mixed) in both arms. flip = final == x.
d_c = c|CR - c|UR; d_u = u|UR - u|CR; D = d_c - d_u; C3 = u|PM - u|UR (per item, then averaged).
Paired item bootstrap: 2,000 resamples, Random(20261116) reseeded per model; the same draws for every statistic.
"""
import datetime
import json
import random
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
HARNESS = HERE.parent
ROOT = HARNESS.parent
H = HARNESS / "runs"
X = ROOT / "harness_x" / "runs"
OUT = ROOT / "harness_x" / "analysis" / "arm_r_vs_a.md"
SEED = 20261116
N_BOOT = 2000
FULL = 720            # g0 (7 cells) + perfect_mixed certain and unsure, 80 items each
CELLS = {"cCR": ("certain_right", "certain"), "cUR": ("unsure_right", "certain"),
         "uUR": ("unsure_right", "unsure"), "uCR": ("certain_right", "unsure"),
         "uPM": ("perfect_mixed", "unsure")}
FULL_LOGS = ("control", "certain_right", "unsure_right", "perfect_mixed")

R = lambda tag: X / f"test__{tag}__instant__R.jsonl"
# (label, arm R file, arm A files, role, files that must reach FULL unique rows)
PAIRS = [
    ("gemma4:12b", R("gemma4_12b"),
     [H / "test__gemma4_12b__instant__A.jsonl", H / "test__gemma4_12b__instant__A__rep2.jsonl"], "open"),
    ("Llama 3.3 70B", R("openrouter_meta-llama_llama-3.3-70b-instruct"),
     [H / "test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl",
      H / "test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A__rep2.jsonl"], "open"),
    ("Llama 4 Maverick", R("openrouter_meta-llama_llama-4-maverick"),
     [X / "test__openrouter_meta-llama_llama-4-maverick__instant__A.jsonl"], "open"),
    ("ministral-3:8b", R("ministral-3_8b"), [X / "test__ministral-3_8b__instant__A.jsonl"], "open"),
    ("ministral-3:8b vs 15 Nov arm A (secondary)", R("ministral-3_8b"),
     [H / "test__ministral-3_8b__instant__A.jsonl"], "secondary"),
    ("GPT-6 Sol", R("openai_gpt-6-sol"), [H / "test__openai_gpt-6-sol__instant__A.jsonl"], "sol"),
    # added 16 Nov 03:10: FREEZE_X item 6, same prediction as P2
    ("Claude Sonnet 5.5", R("anthropic_claude-sonnet-5-5"), [H / "test__anthropic_claude-sonnet-5-5__instant__A.jsonl"], "sol"),
]
MUST_BE_FULL = {R("ministral-3_8b"), X / "test__ministral-3_8b__instant__A.jsonl"}   # plus every arm R file


def rel(p):
    return p.relative_to(ROOT).as_posix()


def missing(r):
    return (r is None or bool(r.get("error")) or r.get("final") == "?" or r.get("done") == "length"
            or r.get("trunc_risk") is True)


def load(paths):
    """Returns ({(id, cell): mean flip over non-missing replicates or None}, {(id, cell): (own, x)},
    unique wrong/key rows per file, unparsable lines)."""
    rows, counts, bad = {}, {}, 0
    for p in paths:
        m = re.search(r"__rep(\d+)\.jsonl$", p.name)
        frep = int(m[1]) if m else 1
        keys = set()
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            if r.get("stratum") != "wrong" or r.get("target") != "key" or r.get("mode") != "instant":
                continue
            rep = int(r["rep"]) if r.get("rep") is not None else frep
            r["_src"] = p
            k = (int(r["id"]), r["log"], r["tone"], rep)
            if r["log"] in FULL_LOGS and r["tone"] in ("none", "certain", "unsure"):
                keys.add(k[:3])
            prev = rows.get(k)
            if prev is not None and r.get("error") and not prev.get("error"):
                continue
            rows[k] = r
        counts[p] = len(keys)
    val, ox = {}, {}
    miss = {p: 0 for p in paths}   # missing trials (after dedup) in the five needed cells, per file
    for (i, lg, t, rep), r in rows.items():
        for c, lt in CELLS.items():
            if (lg, t) != lt:
                continue
            miss[r["_src"]] += missing(r)
            ox.setdefault((i, c), set()).add((r["own"], r["x"]))
            val.setdefault((i, c), [])
            if not missing(r):
                val[(i, c)].append(int(r["final"] == r["x"]))
    means = {k: (sum(v) / len(v) if v else None) for k, v in val.items()}
    return means, ox, counts, bad, miss


def quantile(s, p):
    pos = (len(s) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def stats(f):
    d_c, d_u = f["cCR"] - f["cUR"], f["uUR"] - f["uCR"]
    return {"d_c": d_c, "d_u": d_u, "D": d_c - d_u, "C3": f["uPM"] - f["uUR"]}


def analyse(label, rpath, apaths):
    mr, oxr, cr, br, xr = load([rpath])
    ma, oxa, ca, ba, xa = load(apaths)
    ids = sorted({i for (i, c) in mr} | {i for (i, c) in ma})
    items = []
    for i in ids:
        fr = {c: mr.get((i, c)) for c in CELLS}
        fa = {c: ma.get((i, c)) for c in CELLS}
        if any(v is None for v in list(fr.values()) + list(fa.values())):
            continue
        ox = set().union(*(oxr[(i, c)] for c in CELLS), *(oxa[(i, c)] for c in CELLS))
        if len(ox) != 1:
            raise SystemExit(f"{label} item {i}: own/x differ across cells or arms: {ox}")
        sr, sa = stats(fr), stats(fa)
        it = {"id": i, "fR": fr, "fA": fa}
        for k in sr:
            it[k + "_R"], it[k + "_A"], it[k + "_diff"] = sr[k], sa[k], sr[k] - sa[k]
            it[k + "_avg"] = (sr[k] + sa[k]) / 2      # order-averaged (arm A and arm R equally weighted)
        items.append(it)
    cols = [f"{k}_{s}" for s in ("A", "R", "diff", "avg") for k in ("d_c", "d_u", "D", "C3")]
    n = len(items)
    res = {"n": n, "n_ids": len(ids), "counts": {**cr, **ca}, "bad": br + ba, "miss": {**xr, **xa}}
    if n == 0:
        return res
    rng = random.Random(SEED)
    boot = {c: [] for c in cols}
    for _ in range(N_BOOT):
        idx = rng.choices(range(n), k=n)
        for c in cols:
            boot[c].append(sum(items[j][c] for j in idx) / n)
    for c in cols:
        boot[c].sort()
        res[c] = (sum(it[c] for it in items) / n, quantile(boot[c], .025), quantile(boot[c], .975))
    for arm in ("A", "R"):
        res["rate_" + arm] = {c: sum(it["f" + arm][c] for it in items) / n for c in CELLS}
    return res


def f3(t):
    return f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


def table(head, rows):
    return (["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
            + ["| " + " | ".join(r) + " |" for r in rows] + [""])


def verdict(conds):
    k = sum(conds)
    return "met" if k == len(conds) else "not met" if k == 0 else "mixed"


def main():
    L = ["# Arm R (reversed entry order) vs arm A", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} by `harness/posthoc/arm_r.py`. Exploratory. Pre-run "
         "record and predictions: `harness_x/FREEZE_X.md`, Deviations item 5. Arm R is arm A with the eight log "
         "entries shown in reverse order: the first entry is (C) unsure-voice and the last (B) certain-voice.", "",
         "Answer-only, stratum wrong, target key. Strict missing rule (error, final \"?\", done \"length\", "
         "trunc_risk). Items: non-missing in c|CR, c|UR, u|UR, u|CR and u|PM in both arms. Replicates are averaged "
         "within item and cell (gemma4:12b and Llama 3.3 70B arm A: rep1 and rep2 for the four core cells; their "
         "rep2 did not run perfect_mixed, so u|PM is rep1 only). d_c = c|CR - c|UR; d_u = u|UR - u|CR; "
         "D = d_c - d_u; C3 = u|PM - u|UR. Estimate [paired item-bootstrap 95% interval, "
         f"{N_BOOT} resamples, seed {SEED}]. CR = certain_right, UR = unsure_right, PM = perfect_mixed.", "",
         "ministral-3:8b: the primary arm A is the same-day repeat in `harness_x/runs` (its system prompt carries the "
         "date; the original arm A ran on 15 Nov); the line against the original 15 Nov file is secondary.", ""]

    results, pending, files = [], [], []
    for label, rpath, apaths, role in PAIRS:
        need_full = [rpath] + [p for p in apaths if p in MUST_BE_FULL]
        absent = [p for p in [rpath] + apaths if not p.exists()]
        if absent:
            pending.append((label, role, f"file not present: {', '.join('`' + rel(p) + '`' for p in absent)}"))
            continue
        res = analyse(label, rpath, apaths)
        short = [p for p in need_full if res["counts"][p] < FULL]
        for p in [rpath] + apaths:
            files.append((label, rel(p), res["counts"][p], res["miss"][p]))
        if not short and res["n"] == 0:
            pending.append((label, role, "no item has all needed cells non-missing in both arms"))
            continue
        if short:
            pending.append((label, role, "; ".join(f"`{rel(p)}` has {res['counts'][p]}/{FULL} rows" for p in short)))
            continue
        results.append((label, role, res))

    L += ["## Files", ""]
    L += table(["pair", "file", "unique wrong/key rows (g0 + perfect_mixed)", "missing trials in the 5 needed cells"],
               [[a, f"`{b}`", str(c), str(d)] for a, b, c, d in files])
    if pending:
        L += ["**Pending** (incomplete or absent; rerun the script when complete):", ""]
        L += [f"- {a}: {b}" for a, _, b in pending] + [""]

    L += ["## 1. Per arm", ""]
    rows = []
    for label, role, r in results:
        if r["n"] == 0:
            rows.append([label, "-", "0"] + ["-"] * 9)
            continue
        for arm in ("A", "R"):
            rt = r["rate_" + arm]
            rows.append([label, arm, str(r["n"])] + [f"{rt[c]:.3f}" for c in CELLS]
                        + [f3(r[f"{k}_{arm}"]) for k in ("d_c", "d_u", "D", "C3")])
    L += table(["model", "arm", "n", "c\\|CR", "c\\|UR", "u\\|UR", "u\\|CR", "u\\|PM", "d_c", "d_u", "D", "C3"], rows)

    L += ["## 2. Paired differences, arm R minus arm A (same items)", ""]
    L += table(["model", "n", "D: R - A", "C3: R - A", "d_c: R - A", "d_u: R - A"],
               [[lab, str(r["n"])] + [f3(r[f"{k}_diff"]) for k in ("D", "C3", "d_c", "d_u")]
                for lab, role, r in results if r["n"]])

    L += ["## 3. Predictions (fixed before any arm R call)", "",
          "- P1, each open-weight model: \"D is lower in arm R than in arm A on the same items, and negative.\"",
          "- P2, Sol (item 5) and Claude Sonnet 5.5 (item 6, added later): \"|D| in arm R < 0.15, and both d_c and d_u > 0.3.\"", "",
          "Verdicts use the point estimates: met = every condition holds, mixed = some hold, not met = none. The "
          "interval column says whether each condition also holds for the whole 95% interval.", ""]
    pr = []
    for label, role, r in results:
        if not r["n"]:
            continue
        if role in ("open", "secondary"):
            dd, dr = r["D_diff"], r["D_R"]
            conds = [dd[0] < 0, dr[0] < 0]
            pr.append(["P1" + (" (secondary)" if role == "secondary" else ""), label,
                       f"D_R - D_A = {f3(dd)}; D_R = {f3(dr)}",
                       f"R - A below 0: {'yes' if dd[2] < 0 else 'no'}; D_R below 0: {'yes' if dr[2] < 0 else 'no'}",
                       verdict(conds)])
        elif role == "sol":
            dr, dc, du = r["D_R"], r["d_c_R"], r["d_u_R"]
            conds = [abs(dr[0]) < .15, dc[0] > .3, du[0] > .3]
            pr.append(["P2", label, f"D_R = {f3(dr)}; d_c_R = {f3(dc)}; d_u_R = {f3(du)}",
                       f"|D_R| < .15: {'yes' if -.15 < dr[1] and dr[2] < .15 else 'no'}; d_c_R > .3: "
                       f"{'yes' if dc[1] > .3 else 'no'}; d_u_R > .3: {'yes' if du[1] > .3 else 'no'}",
                       verdict(conds)])
    for label, role, why in pending:
        tag = {"sol": "P2", "secondary": "P1 (secondary)"}.get(role, "P1")
        pr.append([tag, label, "-", "-", "pending"])
    L += table(["prediction", "model", "estimates", "holds for the whole interval?", "verdict"], pr)
    p1 = [row[-1] for row in pr if row[0] == "P1"]
    if p1:
        L += [f"P1 across the open-weight models (primary lines): {p1.count('met')} met, {p1.count('mixed')} mixed, "
              f"{p1.count('not met')} not met, {p1.count('pending')} pending.", ""]

    L += ["## 4. C3 in arm R (descriptive; no prediction was made)", "",
          "In arm R both perfect_mixed and unsure_right open with an unsure-voice entry marked right, so the first "
          "line does not differ between the two logs.", ""]
    L += table(["model", "n", "u\\|PM, R", "u\\|UR, R", "C3, R", "C3, A", "C3: R - A"],
               [[lab, str(r["n"]), f"{r['rate_R']['uPM']:.3f}", f"{r['rate_R']['uUR']:.3f}", f3(r["C3_R"]),
                 f3(r["C3_A"]), f3(r["C3_diff"])] for lab, role, r in results if r["n"]])

    L += ["## 5. Order-averaged effects (follow-up)", "",
          "Per item, the mean of arm A and arm R (entries shown in BASE order and in reverse order), then averaged "
          "over items; same items and bootstrap draws as above. If entry order explained everything, the "
          "order-averaged D would be about 0. 'Excludes 0' refers to the 95% interval.", ""]

    def excl(t):
        return "yes (above)" if t[1] > 0 else "yes (below)" if t[2] < 0 else "no"

    L += table(["model", "n", "d_c, avg(A, R)", "excludes 0", "d_u, avg(A, R)", "excludes 0", "D, avg(A, R)",
                "excludes 0"],
               [[lab, str(r["n"])] + [x for k in ("d_c", "d_u", "D") for x in (f3(r[k + "_avg"]),
                                                                               excl(r[k + "_avg"]))]
                for lab, role, r in results if r["n"] and role != "secondary"])

    bad = sum(r["bad"] for _, _, r in results)
    if bad:
        L += [f"Unparsable lines skipped (files mid-write): {bad}.", ""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {OUT}")
    for label, role, r in results:
        print(f"  {label}: n={r['n']}, missing per file {[v for v in r['miss'].values()]}")
    for label, role, why in pending:
        print(f"  PENDING {label}: {why}")


if __name__ == "__main__":
    main()
