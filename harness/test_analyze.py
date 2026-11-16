"""Tests for analyze.py.

  1. Synthetic unit tests with hand-computable answers (sign test, bootstrap, missing/duplicate rules, populations,
     D and I algebra, replicate averaging, bounds, target net, probe references, pooling guard).
  2. Pilot reproduction: runs convert_pilot.py (writes harness/pilot_converted/), then analyzes the converted files
     (a) under the lenient rule of pilot/f2_pilot5_checks.py (only final == "?" missing, pairwise populations): must
         match the pilot numbers exactly (hard fail otherwise), and
     (b) under the strict rules used from now on: printed side by side, never asserted against the pilot.
Run: uv run --quiet --no-project python -I harness/test_analyze.py
"""
import json
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # -I drops the script directory from sys.path
import analyze as A  # noqa: E402
import convert_pilot  # noqa: E402

FAILS = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got}, want {want}")
    if not ok:
        FAILS.append(name)


def close(x, y, tol=1e-12):
    if x is None or y is None:
        return x is y
    if isinstance(x, (list, tuple)):
        return len(x) == len(y) and all(close(p, q, tol) for p, q in zip(x, y))
    return abs(x - y) < tol


def row(i, log, tone, final, own="A", x="B", **kw):
    r = {"id": i, "model": "m", "mode": "reasoned", "arm": "A", "stratum": "wrong", "log": log, "tone": tone,
         "own": own, "x": x, "final": final, "flip": int(final == x), "done": "stop", "_src": "syn", "_base": "syn",
         "_rep": 1}
    r.update(kw)
    return r


def other(res, key, sub="all"):
    for gname in ("spill_unsure", "spill_certain", "one_voice", "other"):
        for c in res["contrasts"][sub][gname]:
            if c["key"] == key:
                return c
    raise KeyError(key)


# ------------------------------------------------------------------ 1. synthetic

def synthetic():
    print("== synthetic unit tests")
    check("sign test 9 vs 0 = 2*0.5^9", A.sign_test(9, 0), 2 * 0.5 ** 9)
    check("sign test 0 vs 9 = 2*0.5^9", A.sign_test(0, 9), 2 * 0.5 ** 9)
    check("sign test 10 vs 2 = 2*(1+12+66)/4096", A.sign_test(10, 2), 2 * 79 / 4096)
    check("sign test 5 vs 5 = 1", A.sign_test(5, 5), 1.0)
    check("sign test 1 vs 0 = 1", A.sign_test(1, 0), 1.0)
    check("sign test 0 vs 0 = 1", A.sign_test(0, 0), 1.0)

    a = [1] * 9 + [1] * 3 + [0] * 4
    b = [0] * 9 + [1] * 3 + [0] * 4
    ci = A.bootstrap_means([[p - q for p, q in zip(a, b)]])[0]
    s = A.paired_summary(a, b, ci)
    check("paired summary k/n", (s["k_a"], s["k_b"], s["n"]), (12, 3, 16))
    check("paired summary diff", s["diff"], 9 / 16)
    check("paired summary discordant and p", (s["a_only"], s["b_only"], s["sign_p"]), (9, 0, 2 * 0.5 ** 9))
    check("bootstrap CI lies in [0, 1] and contains the estimate", 0 <= ci[0] <= 9 / 16 <= ci[1] <= 1, True)
    check("bootstrap: every item differs by 1 -> CI [1, 1]", A.bootstrap_means([[1] * 7])[0], (1.0, 1.0))
    check("bootstrap: no items -> None", A.bootstrap_means([[]]), [None])
    check("bootstrap: items {1, 0} -> CI [0, 1]", A.bootstrap_means([[1, 0]])[0], (0.0, 1.0))
    check("bootstrap is reproducible (fixed seed)", A.bootstrap_means([a]), A.bootstrap_means([a]))
    check("quantile interpolation", A.quantile([0.0, 1.0, 2.0, 3.0, 4.0], 0.375), 1.5)

    # ---- missing rules, duplicates, populations (5 items, deliberative)
    rows = []
    for i in range(1, 6):
        rows += [row(i, "control", "none", "A"), row(i, "certain_right", "certain", "B"),
                 row(i, "unsure_right", "certain", "A"), row(i, "certain_right", "unsure", "A"),
                 row(i, "unsure_right", "unsure", "A")]
    rows.append(row(1, "unsure_right", "unsure", "B", done="length"))        # missing despite parsed answer
    rows.append(row(2, "unsure_right", "unsure", "C"))                       # third option: not missing, no flip
    rows.append(row(3, "unsure_right", "unsure", "B", error="boom"))         # error after good row: good row wins
    rows.append(row(4, "control", "none", "B", trunc_risk=True))             # missing
    rows.append(row(5, "certain_right", "unsure", "?", error="x"))           # error after good row: good row wins
    rows.append(row(5, "unsure_right", "certain", "?", error="x"))
    rows.append(row(5, "unsure_right", "certain", "B"))                      # good row after error row: wins
    rows.append(row(5, "none", "certain", "B", flip=0))                      # flip field wrong: recomputed
    warn = []
    G = A.build_groups(rows, warn)[("m", "reasoned", "A", "wrong", "key")]
    res, _ = A.analyze_group(G["cells"], "strict", "primary")
    cell = {(c["log"], c["tone"]): c for c in res["cells"]}
    uu = cell[("unsure_right", "unsure")]
    check("length with parsed answer is missing", uu["missing"], 1)
    check("three-way outcome hold/flip/third", (uu["hold"], uu["flip_trials"], uu["third_option"]), (3, 0, 1))
    check("trunc_risk control is missing", (res["controls"]["control|none"]["n"],
                                            res["controls"]["control|none"]["missing_or_absent"]), (4, 1))
    check("good row after error row wins", cell[("unsure_right", "certain")]["flips"], 1)
    check("flip recomputed from final == x", cell[("none", "certain")]["flips"], 1)
    check("flip mismatch warned", any("disagrees" in w for w in warn), True)
    bv = res["contrasts"]["all"]["by_voice_main"]
    check("by-voice population n (items 2, 3, 5)", bv["d_c"]["n"], 3)
    check("d_c rates", (bv["d_c"]["k_a"], bv["d_c"]["k_b"]), (3, 1))
    check("d_u rates", (bv["d_u"]["k_a"], bv["d_u"]["k_b"]), (0, 0))
    check("core / core+control counts", (res["n_core_nonmissing"], res["n_core_and_control_nonmissing"]), (4, 3))
    check("control-unchanged subset present for deliberative", "control_unchanged" in res["contrasts"], True)

    # ---- D and I algebra on a hand-made table (4 items, answer-only, all cells observed)
    # per item: (cCR, cUR, uUR, uCR)
    tab = {1: (1, 0, 1, 0), 2: (1, 0, 0, 0), 3: (1, 1, 0, 1), 4: (0, 0, 1, 0)}
    rows = []
    for i, (cc, cu, uu_, uc) in tab.items():
        f = lambda v: "B" if v else "A"
        rows += [row(i, "control", "none", "A", mode="instant"),
                 row(i, "certain_right", "certain", f(cc), mode="instant"),
                 row(i, "unsure_right", "certain", f(cu), mode="instant"),
                 row(i, "unsure_right", "unsure", f(uu_), mode="instant"),
                 row(i, "certain_right", "unsure", f(uc), mode="instant")]
    G = A.build_groups(rows, [])[("m", "instant", "A", "wrong", "key")]
    bv = A.analyze_group(G["cells"])[0]["contrasts"]["all"]["by_voice_main"]
    # d_c = (3 - 1)/4 = .5 ; d_u = (2 - 1)/4 = .25 ; I = .75 ; D = .25
    check("d_c on hand table", bv["d_c"]["diff"], 0.5)
    check("d_u on hand table", bv["d_u"]["diff"], 0.25)
    check("I = d_c + d_u", bv["I"]["diff"], 0.75)
    check("D = d_c - d_u", bv["D"]["diff"], 0.25)
    # per-item I: 2, 1, -1, 1 -> 3 positive, 1 negative ; per-item D: 0, 1, 1, -1 -> 2 positive, 1 negative
    check("I items >0 / <0", (bv["I"]["a_only"], bv["I"]["b_only"]), (3, 1))
    check("D items >0 / <0", (bv["D"]["a_only"], bv["D"]["b_only"]), (2, 1))
    check("bounds equal the estimate when nothing is missing", bv["I"]["bounds"], [0.75, 0.75])

    # ---- replicate averaging and test-retest
    rows = [row(1, "certain_right", "certain", "B", mode="instant"), row(2, "certain_right", "certain", "B", mode="instant"),
            row(1, "certain_right", "certain", "A", mode="instant", _rep=2, rep=2),
            row(2, "certain_right", "certain", "B", mode="instant", _rep=2, rep=2),
            row(3, "certain_right", "certain", "B", mode="instant"),
            row(3, "certain_right", "certain", "?", mode="instant", _rep=2, rep=2)]   # rep 2 missing -> rep 1 only
    G = A.build_groups(rows, [])[("m", "instant", "A", "wrong", "key")]
    res, view = A.analyze_group(G["cells"])
    check("replicate mean of item 1 (1, 0) = 0.5", view.val(1, ("certain_right", "certain")), 0.5)
    check("item 3 uses its one non-missing replicate", view.val(3, ("certain_right", "certain")), 1.0)
    c = {(x["log"], x["tone"]): x for x in res["cells"]}[("certain_right", "certain")]
    check("cell flips = 0.5 + 1 + 1 over 3 items", (c["flips"], c["n"]), (2.5, 3))
    check("test-retest rep1 vs rep2: 1 of 2 items agree", c["test_retest"], {"rep1_vs_rep2": {"n": 2, "agree": 1}})
    check("file suffix gives the replicate", A.file_base_and_rep("dev__m__instant__A__rep2.jsonl"), ("dev__m__instant__A", 2))

    # ---- bounds: one missing cell flips the sign of I
    vals = {(1, "cCR"): 1, (1, "cUR"): 0, (1, "uUR"): 1, (1, "uCR"): 1,      # item 1: I = +1
            (2, "cCR"): None, (2, "cUR"): 1, (2, "uUR"): 0, (2, "uCR"): 1}   # item 2: I in [-2, -1]
    b = A.linear_bounds([1, 2], lambda i, c: vals[(i, c)], A.BY_VOICE_TERMS["I"])
    check("bounds of I: complete-case +1, bounds [-0.5, 0]", b, [-0.5, 0.0])

    # ---- target net (same items, key vs distractor)
    rows = []
    for i, (fk_, fd) in enumerate([(1, 0), (1, 0), (1, 1), (0, 1), (0, 0)], 1):
        rows.append(row(i, "none", "certain", "B" if fk_ else "A", mode="instant", target="key"))
        rows.append(row(i, "none", "certain", "C" if fd else "A", x="C", mode="instant", target="distractor"))
    rows.append(row(6, "none", "certain", "B", mode="instant", target="key"))   # key only: excluded from net
    groups = A.build_groups(rows, [])
    gk, gd = ("m", "instant", "A", "wrong", "key"), ("m", "instant", "A", "wrong", "distractor")
    vk, vd = A.View(groups[gk]["cells"], "strict"), A.View(groups[gd]["cells"], "strict")
    tc = A.target_comparison(groups[gk], vk, groups[gd], vd)
    check("target net: 3/5 vs 2/5, net +0.2, discordant 2:1",
          (tc[0]["k_a"], tc[0]["k_b"], tc[0]["n"], tc[0]["diff"], tc[0]["a_only"], tc[0]["b_only"]), (3, 2, 5, 0.2, 2, 1))
    # by-voice within target distractor, where the no-log control is not run: population = four core cells
    rows = []
    for i, (cc, cu, uu_, uc) in tab.items():
        f = lambda v: "C" if v else "A"
        rows += [row(i, "certain_right", "certain", f(cc), x="C", mode="instant", target="distractor"),
                 row(i, "unsure_right", "certain", f(cu), x="C", mode="instant", target="distractor"),
                 row(i, "unsure_right", "unsure", f(uu_), x="C", mode="instant", target="distractor"),
                 row(i, "certain_right", "unsure", f(uc), x="C", mode="instant", target="distractor")]
    G = A.build_groups(rows, [])[("m", "instant", "A", "wrong", "distractor")]
    bv = A.analyze_group(G["cells"])[0]["contrasts"]["all"]["by_voice_main"]
    check("distractor without control: I and D on four core cells", (bv["I"]["n"], bv["I"]["diff"], bv["D"]["diff"]), (4, 0.75, 0.25))
    # ---- mitigation: arm M vs arm A on the same items
    tab_m = {1: (1, 0, 1, 0), 2: (1, 0, 1, 0), 3: (1, 0, 1, 1), 4: (0, 0, 1, 0)}
    rows = []
    for arm, t in (("A", tab), ("M", tab_m)):
        for i, (cc, cu, uu_, uc) in t.items():
            f = lambda v: "B" if v else "A"
            rows += [row(i, "certain_right", "certain", f(cc), mode="instant", arm=arm),
                     row(i, "unsure_right", "certain", f(cu), mode="instant", arm=arm),
                     row(i, "unsure_right", "unsure", f(uu_), mode="instant", arm=arm),
                     row(i, "certain_right", "unsure", f(uc), mode="instant", arm=arm)]
    rows += [row(5, k[0], k[1], "B", mode="instant", arm="A") for k in A.CORE]    # item 5 under A only: excluded
    for arm, ccr in (("A", (1, 1, 0, 0)), ("M", (0, 1, 0, 0))):
        for i in range(1, 5):
            rows += [row(i, "certain_right", "certain", "C" if ccr[i - 1] else "A", x="C", mode="instant", arm=arm,
                         target="distractor"),
                     row(i, "unsure_right", "certain", "A", x="C", mode="instant", arm=arm, target="distractor")]
    groups = A.build_groups(rows, [])
    views = {g: A.View(G["cells"], "strict") for g, G in groups.items()}
    mi = A.mitigation(groups, views)
    st = {r["stat"]: r for r in mi[0]["stats"]}
    # d_u per item A: 1, 0, -1, 1 (mean .25); M: 1, 1, 0, 1 (mean .75); change 0, 1, 1, 0 -> +.5, up 2, down 0
    check("mitigation d_u: A .25, M .75, change +.5, up 2 / down 0, n 4",
          (st["d_u"]["A"], st["d_u"]["M"], st["d_u"]["change"], st["d_u"]["items_up"], st["d_u"]["items_down"],
           st["d_u"]["n"]), (0.25, 0.75, 0.5, 2, 0, 4))
    check("mitigation d_c: A .5, M .75, change +.25", (st["d_c"]["A"], st["d_c"]["M"], st["d_c"]["change"]),
          (0.5, 0.75, 0.25))
    check("mitigation I and D changes = sums / differences", (st["I"]["change"], st["D"]["change"]), (0.75, -0.25))
    check("mitigation C4 (distractor): A .5, M .25, change -.25, down 1",
          (st["C4"]["A"], st["C4"]["M"], st["C4"]["change"], st["C4"]["items_down"]), (0.5, 0.25, -0.25, 1))
    cu = next(c for c in mi[0]["cells"] if (c["target"], c["log"], c["tone"]) == ("key", "unsure_right", "unsure"))
    check("mitigation per cell unsure|unsure_right: A 2/4, M 4/4, M only 2", (cu["k_b"], cu["k_a"], cu["n"], cu["a_only"]),
          (2, 4, 4, 2))
    ci = st["d_u"]["ci_change"]
    check("mitigation change CI contains the estimate", ci[0] <= 0.5 <= ci[1], True)
    # ---- right-stratum table
    rows = []
    for i, (a_, b_) in enumerate([(1, 0), (1, 0), (0, 0), (1, 1), (0, 1)], 1):
        rows += [row(i, "certain_right", "certain", "B" if a_ else "A", mode="instant", stratum="right"),
                 row(i, "unsure_right", "certain", "B" if b_ else "A", mode="instant", stratum="right"),
                 row(i, "control", "none", "A", mode="instant", stratum="right")]
    groups = A.build_groups(rows, [])
    results, views = {}, {}
    for g, G in groups.items():
        res, views[g] = A.analyze_group(G["cells"])
        results["|".join(g)] = {"group": dict(zip(("model", "mode", "arm", "stratum", "target"), g)), **res}
    rs = A.right_stratum(results, views)
    c = rs[0]["contrast"]
    check("right stratum: target defaults to distractor; 3/5 vs 2/5, discordant 2:1",
          (rs[0]["target"], c["k_a"], c["k_b"], c["n"], c["a_only"], c["b_only"]), ("distractor", 3, 2, 5, 2, 1))
    check("right stratum: control cell 0/5", (rs[0]["cells"][0]["flips"], rs[0]["cells"][0]["n"]), (0, 5))
    sys.path.insert(0, str(HERE))
    import figures as F
    check("figure classes: ollama / openrouter / deepseek open; openai hosted; harness_x recency",
          (F.model_class("gemma4:12b", "main"), F.model_class("openrouter:x/y", "main"), F.model_class("deepseek:z", "main"),
           F.model_class("openai:gpt-6-luna", "main"), F.model_class("openai:gpt-6-luna", "recency")),
          ("open", "open", "open", "hosted", "recency"))
    check("label names", (F.label_name("gemma4:12b"), F.label_name("openrouter:meta-llama/llama-3.3-70b-instruct")),
          ("gemma4:12b", "llama-3.3-70b-instruct"))
    check("old rows: right stratum defaults to distractor", A.default_target({"stratum": "right"}), "distractor")
    check("old rows: wrong stratum defaults to key", A.default_target({"stratum": "wrong"}), "key")

    # ---- probe references and summary
    ent = [("B", "certain", 1), ("D", "unsure", 0), ("A", "certain", 1), ("C", "unsure", 0),
           ("B", "unsure", 0), ("A", "certain", 1), ("D", "certain", 1), ("C", "unsure", 0)]
    rc, ru = A.probe_references(ent, "certain"), A.probe_references(ent, "unsure")
    check("independent ref certain 4/4 -> 5/6", close(rc["independent"], 5 / 6), True)
    check("independent ref unsure 0/4 -> 1/6", close(ru["independent"], 1 / 6), True)
    check("pooled ref 4/8 -> 0.5", rc["pooled"], 0.5)
    check("voice never appears -> 0.5", A.probe_references([("A", "certain", 1)] * 8, "unsure")["independent"], 0.5)
    import design
    check("design.LOGS certain_right is certain 4/4, unsure 0/4",
          (A.log_counts(design.LOGS["certain_right"][0], "certain"), A.log_counts(design.LOGS["certain_right"][0], "unsure")),
          ((4, 4), (0, 4)))
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "probe__m__A.jsonl"
        pr = [{"model": "m", "arm": "A", "log": "L", "tone": "certain", "right": 4, "total": 4, "probability": 0.9},
              {"model": "m", "arm": "A", "log": "L", "tone": "certain", "right": 3, "total": 4, "probability": 0.7},
              {"model": "m", "arm": "A", "log": "L", "tone": "unsure", "right": 0, "total": 4, "probability": 0.2},
              {"model": "m", "arm": "A", "log": "L", "tone": "unsure", "error": "x", "probability": None}]
        p.write_text("".join(json.dumps(r) + "\n" for r in pr), encoding="utf-8")
        w = []
        ps = A.summarize_probe([p], w, logs={"L": (ent, "by_voice")})
        cc = {r["tone"]: r for r in ps["cells"]}
        check("probe certain: n 2, mean 0.8, count match 0.5",
              (cc["certain"]["n"], close(cc["certain"]["mean"], 0.8), cc["certain"]["count_match"]), (2, True, 0.5))
        check("probe unsure: error row excluded, n 1", (cc["unsure"]["n"], cc["unsure"]["count_match"]), (1, 1.0))
        # RMSE vs independent: sqrt(((0.8-5/6)^2 + (0.2-1/6)^2)/2) = 1/30 ; vs pooled: sqrt((0.3^2+0.3^2)/2) = 0.3
        check("probe RMSE vs independent = 1/30", close(ps["rmse"][0]["rmse_independent"], 1 / 30), True)
        check("probe RMSE vs pooled = 0.3", close(ps["rmse"][0]["rmse_pooled"], 0.3), True)

        # ---- truncated last line, pooling guard, probe guard
        good = {k: v for k, v in row(1, "control", "none", "A").items() if not k.startswith("_")}
        f1, f2, f3 = Path(td) / "x__m.jsonl", Path(td) / "y__m.jsonl", Path(td) / "x__m__rep2.jsonl"
        f1.write_text(json.dumps(good) + "\n" + json.dumps(good)[:40], encoding="utf-8")
        f2.write_text(json.dumps(good) + "\n", encoding="utf-8")
        f3.write_text(json.dumps(dict(good, rep=2)) + "\n", encoding="utf-8")
        w = []
        check("truncated last line skipped and warned", (len(A.load_rows([f1], w)), len(w)), (1, 1))
        out = Path(td) / "out"
        try:
            A.main([str(f1), str(f2), "--out-dir", str(out)])
            refused = False
        except SystemExit:
            refused = True
        check("pooling two different files is refused", refused, True)
        A.main([str(f1), str(f2), "--out-dir", str(out), "--allow-pool"])
        check("--allow-pool permits it", (out / "combined__x__m+y__m.md").exists(), True)
        A.main([str(f1), str(f3), "--out-dir", str(out), "--name", "reps"])
        j = json.loads((out / "reps.json").read_text(encoding="utf-8"))
        check("replicate files of one run pool without --allow-pool", list(j["groups"].values())[0]["replicates"], [1, 2])
        try:
            A.load_rows([p], [])
            refused = False
        except SystemExit:
            refused = True
        check("probe file refused as a run file", refused, True)

        # ---- Holm, probe scale, confirmatory section and summary in one call
        # p = .01, .04, .03, .005 (m = 4): sorted .005*4 = .02, .01*3 = .03, .03*2 = .06, .04*1 -> max(.06, .04) = .06
        check("Holm adjusted p (input order)", close(A.holm([0.01, 0.04, 0.03, 0.005]), [0.03, 0.06, 0.06, 0.02]), True)
        check("Holm caps at 1", A.holm([0.5, 0.6]), [1.0, 1.0])
        check("Holm with one test = raw p", A.holm([0.2]), [0.2])
        pf = Path(td) / "probe_dev__m__A.jsonl"
        pf.write_text("".join(json.dumps(r) + "\n" for r in [
            {"model": "m", "arm": "A", "log": "certain_right", "tone": "certain", "right": 4, "total": 4, "probability": 75},
            {"model": "m", "arm": "A", "log": "certain_right", "tone": "unsure", "right": 0, "total": 4, "probability": 0}]),
            encoding="utf-8")
        rf = Path(td) / "dev__m__instant__A.jsonl"
        rows = []
        for i, (cc, cu, uu_, uc) in tab.items():
            f = lambda v: "B" if v else "A"
            rows += [row(i, "control", "none", "A", mode="instant"),
                     row(i, "certain_right", "certain", f(cc), mode="instant"),
                     row(i, "unsure_right", "certain", f(cu), mode="instant"),
                     row(i, "unsure_right", "unsure", f(uu_), mode="instant"),
                     row(i, "certain_right", "unsure", f(uc), mode="instant")]
        rf.write_text("".join(json.dumps({k: v for k, v in r.items() if not k.startswith("_")}) + "\n" for r in rows),
                      encoding="utf-8")
        A.main(["--probe", str(pf), str(rf), "--summary", "--name", "conf", "--out-dir", str(out)])
        j = json.loads((out / "conf.json").read_text(encoding="utf-8"))
        conf = j["confirmatory"][0]
        check("run file after --probe routed to the trial analysis", conf["model"], "m")
        check("C1 = d_c, C2 = D on the hand table", (conf["rows"][0]["diff"], conf["rows"][1]["diff"]), (0.5, 0.25))
        check("C4 not available (no distractor) -> enters Holm as p = 1, shown as None",
              (conf["rows"][3]["n"], conf["rows"][3]["holm_p"]), (0, None))
        check("answer-only labelled confirmatory", conf["status"], "confirmatory")
        pr0 = j["probe_pairing"][0]["rows"]
        check("probe file on 0-100 scale: 75 -> 0.75, 0 -> 0",
              (pr0[0]["mean_stated_probability"], pr0[3]["mean_stated_probability"]), (0.75, 0.0))
        check("pairing: certain|certain_right flips, target key = 3/4", (pr0[0]["flips_key"], pr0[0]["n_key"]), (3, 4))
        md_text = (out / "conf.md").read_text(encoding="utf-8")
        check("confirmatory section precedes Exploratory",
              md_text.index("# Confirmatory") < md_text.index("# Exploratory"), True)
        check("summary file written", (out / "summary__conf.md").exists(), True)


# ------------------------------------------------------------------ 2. pilot reproduction

def cellmap(res):
    return {(c["log"], c["tone"]): (c["flips"], c["n"]) for c in res["cells"] if c["run"]}


def fr(k, n):
    return f"{A.fk(k)}/{n}"


def pilot():
    print("\n== converting pilot files")
    convert_pilot.main()
    src = HERE / "pilot_converted"
    out = {}
    for mode in ("instant", "reasoned"):
        warn = []
        rows = A.load_rows([src / f"pilot__gemma4_12b__{mode}__A.jsonl"], warn)
        G = A.build_groups(rows, warn)[("gemma4:12b", mode, "A", "wrong", "key")]
        out[mode] = {"lenient": A.analyze_group(G["cells"], "lenient", "pairwise")[0],
                     "strict": A.analyze_group(G["cells"], "strict", "primary")[0]}
        if warn:
            print(f"  warnings ({mode}):", warn)

    print("\n== (a) lenient rule must reproduce the pilot tabulation")
    L = out["instant"]["lenient"]
    c = cellmap(L)
    want_inst = {("certain_right", "certain"): (13, 32), ("unsure_right", "certain"): (0, 32),
                 ("certain_right", "unsure"): (0, 32), ("unsure_right", "unsure"): (0, 32),
                 ("reliable", "certain"): (24, 32), ("reliable", "unsure"): (1, 32),
                 ("perfect_mixed", "certain"): (31, 32), ("perfect_mixed", "unsure"): (24, 32),
                 ("all_unsure", "certain"): (30, 32), ("all_unsure", "unsure"): (29, 32),
                 ("all_certain", "certain"): (31, 32), ("all_certain", "unsure"): (5, 32),
                 ("certain_right_long", "certain"): (10, 32), ("certain_right_long", "unsure"): (0, 32),
                 ("unsure_right_long", "certain"): (1, 32), ("unsure_right_long", "unsure"): (1, 32),
                 ("none", "certain"): (13, 32), ("none", "unsure"): (6, 32)}
    for k, v in want_inst.items():
        check(f"answer-only {k[1]}|{k[0]}", c[k], v)
    ctl = L["controls"]["control|none"]
    check("answer-only control moved / changed", (ctl["moved_to_x"], ctl["n"], ctl["changed"]), (0, 32, 0))

    R = out["reasoned"]["lenient"]
    p = R["contrasts"]["all"]["by_voice_main"]
    check("deliberative d_c k/n", (p["d_c"]["k_a"], p["d_c"]["k_b"], p["d_c"]["n"]), (23, 14, 29))
    check("deliberative d_c discordant", (p["d_c"]["a_only"], p["d_c"]["b_only"]), (9, 0))
    check("deliberative d_c p (design: 0.004)", round(p["d_c"]["sign_p"], 3), 0.004)
    check("deliberative d_u k/n", (p["d_u"]["k_a"], p["d_u"]["k_b"], p["d_u"]["n"]), (16, 15, 29))
    check("deliberative d_u discordant", (p["d_u"]["a_only"], p["d_u"]["b_only"]), (1, 0))
    rc = R["controls"]["control|none"]
    check("deliberative control moved to key", (rc["moved_to_x"], rc["n"]), (8, 24))
    lg = R["contrasts"]["all"]["by_voice_long"]
    check("deliberative long d_c (5.2)", (lg["d_c"]["k_a"], lg["d_c"]["k_b"], lg["d_c"]["n"]), (23, 14, 31))
    check("deliberative long d_u (5.2)", (lg["d_u"]["k_a"], lg["d_u"]["k_b"], lg["d_u"]["n"]), (15, 14, 30))
    tg = other(R, "tone_gap_reliable")
    check("deliberative reliable tone gap (5.2)", (tg["k_a"], tg["k_b"], tg["n"]), (20, 18, 30))
    cu = R["contrasts"]["control_unchanged"]["by_voice_main"]
    check("control-unchanged d_c (5.2)", (cu["d_c"]["k_a"], cu["d_c"]["k_b"], cu["d_c"]["n"]), (9, 3, 15))
    check("control-unchanged d_u (5.2)", (cu["d_u"]["k_a"], cu["d_u"]["k_b"], cu["d_u"]["n"]), (3, 2, 16))
    check("control-unchanged items (5.2)", rc["n"] - rc["changed"], 16)

    print("\n== answer-only: strict must equal lenient (no missing rows)")
    S = out["instant"]["strict"]
    check("answer-only cell tables identical", cellmap(S) == cellmap(L), True)
    for key in ("by_voice_main", "by_voice_long"):
        for v in A.BY_VOICE_TERMS:
            a, b = S["contrasts"]["all"][key][v], L["contrasts"]["all"][key][v]
            check(f"answer-only {key} {v} identical", (a["diff"], a["n"], a["ci95"]), (b["diff"], b["n"], b["ci95"]))

    print("\n== side by side: (a) lenient [pilot script] vs (b) strict [from now on]")
    for mode in ("instant", "reasoned"):
        Lr, Sr = out[mode]["lenient"], out[mode]["strict"]
        print(f"\n-- {A.MODE_NAME[mode]}")
        print(f"   {'quantity':58s} {'(a) lenient':36s} (b) strict")
        cl, cs = cellmap(Lr), cellmap(Sr)
        for k in cl:
            print(f"   {('cell ' + k[1] + '|' + k[0]):58s} {fr(*cl[k]):36s} {fr(*cs[k])}")
        a, b = Lr["controls"]["control|none"], Sr["controls"]["control|none"]
        print(f"   {'no-log control moved to x / changed':58s} "
              f"{fr(a['moved_to_x'], a['n']) + ' / ' + A.fk(a['changed']):36s} {fr(b['moved_to_x'], b['n'])} / {A.fk(b['changed'])}")
        for sub in Lr["contrasts"]:
            for key in ("by_voice_main", "by_voice_long"):
                for v in A.BY_VOICE_TERMS:
                    a, b = Lr["contrasts"][sub][key][v], Sr["contrasts"][sub][key][v]
                    print(f"   {(sub + ' ' + key[9:] + ' ' + v):58s} {line(a):36s} {line(b)}")
            for gname in ("spill_unsure", "spill_certain", "other"):
                for a, b in zip(Lr["contrasts"][sub][gname], Sr["contrasts"][sub][gname]):
                    if a["n"] or b["n"]:
                        print(f"   {(sub + ' ' + a['key']):58s} {line(a):36s} {line(b)}")


def line(c):
    if not c["n"]:
        return "n = 0"
    if "k_a" in c:
        return f"{A.fk(c['k_a'])}/{c['n']} vs {A.fk(c['k_b'])}/{c['n']} ({c['a_only']}:{c['b_only']}) p={c['sign_p']:.3f}"
    return f"{c['diff']:+.3f} [{c['ci95'][0]:+.2f},{c['ci95'][1]:+.2f}] n={c['n']}"


if __name__ == "__main__":
    synthetic()
    pilot()
    print(f"\n{'ALL CHECKS PASSED' if not FAILS else 'FAILED: ' + ', '.join(FAILS)}")
    sys.exit(1 if FAILS else 0)
