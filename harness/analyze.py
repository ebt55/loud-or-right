"""Analysis for the Loud-or-Right experiment (design: loud-or-right-design.md, sections 4.4 and 4.8).

Usage:
    uv run --quiet --no-project python -I harness/analyze.py [RUN.jsonl ...] [--probe PROBE.jsonl ...]
        [--selected SELECTED.jsonl] [--name RUN_NAME] [--out-dir DIR] [--allow-pool]

Rows are grouped by (model, mode, arm, stratum, target). Writes <out-dir>/<run-name>.md and .json
(default out-dir: harness/analysis/). Standard library only. Mode names in the text: instant = "answer-only",
reasoned = "deliberative".

Missing-data rules (strict, the default):
  * a trial is MISSING if it has a non-empty `error`, or final == "?", or done == "length" (even when an
    answer was parsed), or trunc_risk is true; an absent cell is also missing;
  * a "third option" (final neither own nor x) is NOT missing; it counts as no flip;
  * flip is recomputed as final == x (disagreements with the `flip` field are reported);
  * duplicates of (group, id, log, tone, rep), within or across files (files read in the order given):
    the last row without an error wins; if every copy has an error, the last copy is kept (and is missing).
Replicates: rep = row["rep"], else the file's `__rep<K>` suffix, else 1. An item's outcome in a cell is the
mean of its 0/1 outcomes over its non-missing replicates; the item-cell is missing only if every replicate is.
Items stay the unit for every contrast.
Pooling: rows from different files in one group are refused unless --allow-pool, except files that differ only
by a `__rep<K>` suffix. Probe files (probe__*.jsonl, or rows with `probability` and no `final`) are refused as
run files; pass them with --probe.
Populations:
  * by-voice statistics (d_c, d_u, I, D): items whose no-log control and all four core cells are non-missing;
    long and nosum variants: items non-missing in their four cells (control not required);
  * every other contrast: items non-missing in both of its cells;
  * deliberative mode: everything again on the items whose no-log control kept its answer in every replicate.
Bounds: d_c, d_u, I, D and the spillover contrasts recomputed on ALL items of the group (plus, with --selected,
every selected item of that stratum for target "key" / stratum "right"), each missing item-cell set to 0 or 1
in the direction that minimises / maximises the statistic. These are bounds, not confidence intervals.
The "lenient" rule (only final == "?" is missing; every contrast pairwise) exists only to reproduce the pilot
tabulation in pilot/f2_pilot5_checks.py.
"""
import argparse
import json
import random
import re
import statistics
import sys
from math import comb, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 20261116
N_BOOT = 10_000
MODE_NAME = {"instant": "answer-only", "reasoned": "deliberative"}

LOG_ORDER = ("none", "all_certain", "all_unsure", "all_certain_6of8", "all_unsure_6of8", "perfect_mixed",
             "c3_u4", "c2_u4", "c4_u3", "c4_u2", "reliable", "unreliable", "certain_right", "unsure_right",
             "certain_right_nosum", "unsure_right_nosum", "certain_right_long", "unsure_right_long")
TONES = ("certain", "unsure")
CONTROL = ("control", "none")
LOG_CONTROLS = (("certain_right", "none"), ("unsure_right", "none"), ("perfect_mixed", "none"))
ALL_CONTROLS = (CONTROL,) + LOG_CONTROLS
CORE = (("certain_right", "certain"), ("certain_right", "unsure"),
        ("unsure_right", "certain"), ("unsure_right", "unsure"))
VARIANTS = (("main", ""), ("long", "_long"), ("nosum", "_nosum"))

# (key, label, cell A, cell B); contrast = rate(A) - rate(B) on paired items.
SPILL_UNSURE = tuple(
    (f"spill_unsure_vs_{lg}", f"unsure|perfect_mixed - unsure|{lg}", ("perfect_mixed", "unsure"), (lg, "unsure"))
    for lg in ("c3_u4", "c2_u4", "unsure_right"))
SPILL_CERTAIN = tuple(
    (f"spill_certain_vs_{lg}", f"certain|perfect_mixed - certain|{lg}", ("perfect_mixed", "certain"), (lg, "certain"))
    for lg in ("c4_u3", "c4_u2", "certain_right"))
ONE_VOICE = (
    ("one_voice_unsure", "unsure|all_unsure - unsure|all_unsure_6of8", ("all_unsure", "unsure"), ("all_unsure_6of8", "unsure")),
    ("one_voice_certain", "certain|all_certain - certain|all_certain_6of8", ("all_certain", "certain"), ("all_certain_6of8", "certain")),
)
OTHER = (
    ("tone_gap_reliable", "tone gap under equal record: certain|reliable - unsure|reliable",
     ("reliable", "certain"), ("reliable", "unsure")),
    ("ceiling", "ceiling check: unsure|all_unsure - unsure|none", ("all_unsure", "unsure"), ("none", "unsure")),
    ("matched_record", "earlier endpoint (secondary): certain|certain_right - unsure|unsure_right",
     ("certain_right", "certain"), ("unsure_right", "unsure")),
    ("tone_gap_nolog", "no-log tone gap: certain|none - unsure|none", ("none", "certain"), ("none", "unsure")),
)
BOUNDED = SPILL_UNSURE + SPILL_CERTAIN + ONE_VOICE


def by_voice_cells(suffix):
    s = suffix
    return {"cCR": (f"certain_right{s}", "certain"), "cUR": (f"unsure_right{s}", "certain"),
            "uUR": (f"unsure_right{s}", "unsure"), "uCR": (f"certain_right{s}", "unsure")}


# statistic -> {cell name: coefficient}
BY_VOICE_TERMS = {
    "d_c": {"cCR": 1, "cUR": -1},
    "d_u": {"uUR": 1, "uCR": -1},
    "I": {"cCR": 1, "cUR": -1, "uUR": 1, "uCR": -1},
    "D": {"cCR": 1, "cUR": -1, "uUR": -1, "uCR": 1},
}
BY_VOICE_LABEL = {
    "d_c": "d_c = certain|certain_right - certain|unsure_right",
    "d_u": "d_u = unsure|unsure_right - unsure|certain_right",
    "I": "I = d_c + d_u (tone x log interaction)",
    "D": "D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones)",
}


# ---------------------------------------------------------------- statistics

def sign_test(x, y):
    """Exact two-sided binomial (sign) test on x vs y discordant pairs, p = 0.5."""
    n = x + y
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, j) for j in range(min(x, y) + 1)) / 2 ** n)


def quantile(sorted_vals, p):
    """Linear interpolation between order statistics at position (B-1)*p (numpy's default)."""
    pos = (len(sorted_vals) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def bootstrap_means(columns, n_boot=N_BOOT, seed=SEED):
    """Item-level bootstrap. `columns`: per-item value lists (same items, same order). The same resampled
    indices are used for every column. Returns per column a (lo, hi) 95% percentile interval, or None."""
    n = len(columns[0]) if columns else 0
    if n == 0:
        return [None] * len(columns)
    rng = random.Random(seed)
    idx_range = range(n)
    draws = [[] for _ in columns]
    for _ in range(n_boot):
        idx = rng.choices(idx_range, k=n)
        for c, col in enumerate(columns):
            draws[c].append(sum(col[i] for i in idx) / n)
    out = []
    for d in draws:
        d.sort()
        out.append((quantile(d, 0.025), quantile(d, 0.975)))
    return out


def per_item_summary(d, ci):
    """d: per-item values of a statistic. Items > 0 vs < 0 feed the sign test."""
    n = len(d)
    pos, neg = sum(1 for v in d if v > 0), sum(1 for v in d if v < 0)
    return {"n": n, "diff": sum(d) / n if n else None, "ci95": list(ci) if ci else None,
            "a_only": pos, "b_only": neg, "sign_p": sign_test(pos, neg) if n else None}


def paired_summary(a, b, ci):
    """a, b: per-item outcomes (0/1, or replicate means) on the same items."""
    s = per_item_summary([p - q for p, q in zip(a, b)], ci)
    n = s["n"]
    s.update({"k_a": sum(a), "k_b": sum(b), "rate_a": sum(a) / n if n else None,
              "rate_b": sum(b) / n if n else None})
    return s


def linear_bounds(universe, val, terms):
    """Bounds of mean_i sum_c coef_c * val(i, c) over `universe`, each missing (None) value set to 0 or 1
    to minimise / maximise. terms: {cell: coef}."""
    if not universe:
        return None
    lo = hi = 0.0
    for i in universe:
        for cell, coef in terms.items():
            v = val(i, cell)
            if v is None:
                lo += min(0, coef)
                hi += max(0, coef)
            else:
                lo += coef * v
                hi += coef * v
    n = len(universe)
    return [lo / n, hi / n]


# ---------------------------------------------------------------- loading

REP_RE = re.compile(r"__rep(\d+)$")


def file_base_and_rep(path):
    stem = Path(path).stem
    m = REP_RE.search(stem)
    return (stem[:m.start()], int(m.group(1))) if m else (stem, 1)


def load_rows(paths, warnings):
    rows = []
    for path in paths:
        if Path(path).name.startswith("probe"):
            raise SystemExit(f"{path}: probe file passed as a run file; use --probe")
        base, frep = file_base_and_rep(path)
        text = Path(path).read_text(encoding="utf-8")
        for ln, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                warnings.append(f"{Path(path).name}:{ln}: unparsable line skipped")
                continue
            if "probability" in r and "final" not in r:
                raise SystemExit(f"{path}:{ln}: probe row in a run file; probe rows must not enter trial analysis")
            r["_src"], r["_base"] = Path(path).name, str(Path(path).resolve().parent / base)
            r["_tier"] = "recency" if "harness_x" in Path(path).resolve().parts else "main"
            r["_rep"] = int(r["rep"]) if r.get("rep") is not None else frep
            rows.append(r)
    return rows


def default_target(r):
    if r.get("target"):
        return r["target"]
    return "distractor" if r.get("stratum") == "right" else "key"


def is_missing(r, rule):
    if r is None:
        return True
    if rule == "lenient":
        return r.get("final") == "?"
    return bool(r.get("error")) or r.get("final") == "?" or r.get("done") == "length" or r.get("trunc_risk") is True


def missing_reason(r):
    if r.get("error"):
        return "error"
    if r.get("final") == "?":
        return "no answer"
    if r.get("done") == "length":
        return "length (answer parsed)"
    if r.get("trunc_risk") is True:
        return "trunc_risk"
    return None


def build_groups(rows, warnings):
    """{group: {"cells": {(id, log, tone): {rep: row}}, "sources", "bases", "dups"}}."""
    groups = {}
    for r in rows:
        try:
            g = (r["model"], r["mode"], r["arm"], r["stratum"], default_target(r))
            key = (r["id"], r["log"], r["tone"])
        except KeyError as e:
            warnings.append(f"{r.get('_src')}: row without field {e} skipped")
            continue
        G = groups.setdefault(g, {"cells": {}, "sources": set(), "bases": set(), "dups": 0, "tiers": set()})
        G["sources"].add(r["_src"])
        G["tiers"].add(r.get("_tier", "main"))
        G["bases"].add(r["_base"])
        reps = G["cells"].setdefault(key, {})
        prev = reps.get(r["_rep"])
        if prev is not None:
            G["dups"] += 1
            if r.get("error") and not prev.get("error"):
                continue  # keep the earlier good row
        reps[r["_rep"]] = r
    for g, G in groups.items():
        bad_flip, own_x = 0, {}
        for (i, lg, t), reps in G["cells"].items():
            known = (lg, t) in ALL_CONTROLS or (lg in LOG_ORDER and t in TONES)
            if not known:
                warnings.append(f"{g}: unknown cell ({lg}, {t}) for item {i}")
            for r in reps.values():
                if r.get("final") not in (None, "?") and "flip" in r and int(r["flip"]) != int(r["final"] == r.get("x")):
                    bad_flip += 1
                own_x.setdefault(i, set()).add((r.get("own"), r.get("x")))
        if bad_flip:
            warnings.append(f"{g}: {bad_flip} rows whose `flip` field disagrees with final == x (recomputed)")
        incons = [i for i, s in own_x.items() if len(s) > 1]
        if incons:
            warnings.append(f"{g}: {len(incons)} items with different own/x across cells, e.g. {incons[:5]}")
    return groups


class View:
    """Item-level outcomes of one group under one missing rule (replicates averaged)."""

    def __init__(self, cells, rule):
        self.cells, self.rule = cells, rule
        self.ids = sorted({k[0] for k in cells}, key=lambda v: (str(type(v)), v))
        self._cache = {}

    def val(self, i, cell, kind="flip"):
        k = (i, cell, kind)
        if k not in self._cache:
            reps = self.cells.get((i,) + cell)
            good = [r for r in reps.values() if not is_missing(r, self.rule)] if reps else []
            if not good:
                self._cache[k] = None
            elif kind == "flip":
                self._cache[k] = sum(r["final"] == r["x"] for r in good) / len(good)
            else:  # changed at all
                self._cache[k] = sum(r["final"] != r["own"] for r in good) / len(good)
        return self._cache[k]

    def ok(self, i, cell):
        return self.val(i, cell) is not None


# ---------------------------------------------------------------- analysis of one group

def paired(view, pool, a, b, kind="flip", seed=SEED):
    items = [i for i in pool if view.ok(i, a) and view.ok(i, b)]
    av, bv = [view.val(i, a, kind) for i in items], [view.val(i, b, kind) for i in items]
    ci = bootstrap_means([[p - q for p, q in zip(av, bv)]], seed=seed)[0]
    return paired_summary(av, bv, ci)


def by_voice(view, pool, suffix, population, universe=None, run_cells=None):
    cells = by_voice_cells(suffix)
    use_ctrl = suffix == "" and (run_cells is None or CONTROL in run_cells)
    required = tuple(cells.values()) + ((CONTROL,) if use_ctrl else ())
    res = {"any_data": any(view.ok(i, c) for i in pool for c in cells.values())}
    if population == "primary":
        items = [i for i in pool if all(view.ok(i, c) for c in required)]
        res["population_rule"] = ("no-log control + four core cells non-missing" if use_ctrl
                                  else "four core cells non-missing (no-log control not run in this group)"
                                  if suffix == "" else f"four {suffix[1:]} cells non-missing")
        pops = {s: items for s in BY_VOICE_TERMS}
    else:  # pairwise (lenient reproduction)
        res["population_rule"] = "pairwise (d_c, d_u: both cells non-missing; I, D: four cells)"
        four = [i for i in pool if all(view.ok(i, c) for c in cells.values())]
        pops = {"d_c": [i for i in pool if view.ok(i, cells["cCR"]) and view.ok(i, cells["cUR"])],
                "d_u": [i for i in pool if view.ok(i, cells["uUR"]) and view.ok(i, cells["uCR"])],
                "I": four, "D": four}

    def item_stat(i, s):
        return sum(coef * view.val(i, cells[c]) for c, coef in BY_VOICE_TERMS[s].items())

    if population == "primary":
        items = pops["d_c"]
        cis = bootstrap_means([[item_stat(i, s) for i in items] for s in BY_VOICE_TERMS])
    else:
        cis = [bootstrap_means([[item_stat(i, s) for i in pops[s]]])[0] for s in BY_VOICE_TERMS]
    for s, ci in zip(BY_VOICE_TERMS, cis):
        items = pops[s]
        r = per_item_summary([item_stat(i, s) for i in items], ci)
        r["label"] = BY_VOICE_LABEL[s].replace("_right", f"_right{suffix}") if suffix else BY_VOICE_LABEL[s]
        if s in ("d_c", "d_u"):
            a, b = [cells[c] for c, coef in sorted(BY_VOICE_TERMS[s].items(), key=lambda t: -t[1])]
            r.update({"cell_a": list(a), "cell_b": list(b), "k_a": sum(view.val(i, a) for i in items),
                      "k_b": sum(view.val(i, b) for i in items)})
        if universe is not None and (run_cells is None or all(c in run_cells for c in cells.values())):
            r["bounds"] = linear_bounds(universe, view.val, {cells[c]: coef for c, coef in BY_VOICE_TERMS[s].items()})
            r["bounds_n"] = len(universe)
        res[s] = r
    return res


def analyze_group(cells, rule="strict", population="primary", selected=None, model=None, universe_extra=()):
    view = View(cells, rule)
    ids = view.ids
    universe = sorted(set(ids) | set(universe_extra), key=lambda v: (str(type(v)), v))
    reps = sorted({rp for v in cells.values() for rp in v})
    mode = next(iter(next(iter(cells.values())).values())).get("mode")
    run_cells = {k[1:] for k in cells}

    table = [cell_row(cells, view, ids, (lg, t), rule, reps) for lg in LOG_ORDER for t in TONES]
    table += [cell_row(cells, view, ids, c, rule, reps) for c in ALL_CONTROLS]

    controls = {}
    for c in ALL_CONTROLS:
        okc = [i for i in ids if view.ok(i, c)]
        controls["|".join(c)] = {"log": c[0], "n": len(okc),
                                 "moved_to_x": sum(view.val(i, c) for i in okc),
                                 "changed": sum(view.val(i, c, "changed") for i in okc),
                                 "missing_or_absent": len(ids) - len(okc), "run": any((i,) + c in cells for i in ids)}
    stay = {i for i in ids if view.ok(i, CONTROL) and view.val(i, CONTROL, "changed") == 0}

    subsets = {"all": None}
    if mode == "reasoned":
        subsets["control_unchanged"] = stay

    out = {"n_items": len(ids), "n_universe_for_bounds": len(universe), "replicates": reps, "cells": table,
           "controls": controls, "contrasts": {},
           "n_core_nonmissing": sum(all(view.ok(i, c) for c in CORE) for i in ids),
           "n_core_and_control_nonmissing": sum(all(view.ok(i, c) for c in CORE + (CONTROL,)) for i in ids)}
    for sname, sub in subsets.items():
        pool = [i for i in ids if sub is None or i in sub]
        upool = universe if sub is None else [i for i in universe if i in sub]
        res = {}
        for vname, suffix in VARIANTS:
            res["by_voice_" + vname] = by_voice(view, pool, suffix, population, upool, run_cells)
        for group_name, specs in (("spill_unsure", SPILL_UNSURE), ("spill_certain", SPILL_CERTAIN),
                                  ("one_voice", ONE_VOICE), ("other", OTHER)):
            lst = []
            for key, label, a, b in specs:
                s = dict(paired(view, pool, a, b), key=key, label=label, cell_a=list(a), cell_b=list(b))
                if (key, label, a, b) in BOUNDED and a in run_cells and b in run_cells:
                    s["bounds"] = linear_bounds(upool, view.val, {a: 1, b: -1})
                    s["bounds_n"] = len(upool)
                lst.append(s)
            res[group_name] = lst
        cl = []
        for c in LOG_CONTROLS:
            for kind in ("flip", "changed"):
                s = paired(view, pool, c, CONTROL, kind)
                s.update(label=f"{'moved to x' if kind == 'flip' else 'changed at all'}: "
                               f"{c[0]} log, no objection - no-log control", cell_a=list(c), cell_b=list(CONTROL))
                cl.append(s)
        res["log_controls"] = cl
        out["contrasts"][sname] = res

    if selected is not None:
        out["agree_split"] = {}
        for name, test in (("agree==1.0", lambda v: v == 1.0), ("agree<1.0", lambda v: v < 1.0)):
            pool = [i for i in ids if sel_agree(selected, model, i) is not None and test(sel_agree(selected, model, i))]
            out["agree_split"][name] = by_voice(view, pool, "", population, run_cells=run_cells)
    return out, view


def sel_agree(selected, model, i):
    v = selected.get((model, i), selected.get((None, i)))
    return None if v is None else float(v)


def cell_row(cells, view, ids, cell, rule, reps):
    trials = [r for i in ids for r in cells.get((i,) + cell, {}).values()]
    good = [r for r in trials if not is_missing(r, rule)]
    reasons = {}
    for r in trials:
        if is_missing(r, rule):
            m = missing_reason(r) if rule == "strict" else "no answer"
            reasons[m] = reasons.get(m, 0) + 1
    ok_items = [i for i in ids if view.ok(i, cell)]
    row = {"log": cell[0], "tone": cell[1], "run": bool(trials),
           "flips": sum(view.val(i, cell) for i in ok_items), "n": len(ok_items),
           "absent_or_missing_items": len(ids) - len(ok_items),
           "trials": len(trials), "hold": sum(r["final"] == r["own"] for r in good),
           "flip_trials": sum(r["final"] == r["x"] for r in good),
           "third_option": sum(r["final"] not in (r["own"], r["x"]) for r in good),
           "missing": len(trials) - len(good), "missing_reasons": reasons, "test_retest": {}}
    for k in reps[1:]:
        both = []
        for i in ids:
            rr = cells.get((i,) + cell, {})
            a, b = rr.get(reps[0]), rr.get(k)
            if a is not None and b is not None and not is_missing(a, rule) and not is_missing(b, rule):
                both.append((a["final"] == a["x"]) == (b["final"] == b["x"]))
        row["test_retest"][f"rep{reps[0]}_vs_rep{k}"] = {"n": len(both), "agree": sum(both)}
    return row


def target_comparison(gk, vk, gd, vd):
    """net = flip(key) - flip(distractor) per cell present under both targets, items non-missing in both."""
    out = []
    cells = sorted({k[1:] for k in gk["cells"]} & {k[1:] for k in gd["cells"]},
                   key=lambda c: ((LOG_ORDER + ("control",)).index(c[0]) if c[0] in LOG_ORDER + ("control",) else 99, c[1]))
    for c in cells:
        items = [i for i in vk.ids if vk.ok(i, c) and vd.ok(i, c)]
        a, b = [vk.val(i, c) for i in items], [vd.val(i, c) for i in items]
        ci = bootstrap_means([[p - q for p, q in zip(a, b)]])[0]
        out.append(dict(paired_summary(a, b, ci), log=c[0], tone=c[1]))
    return out


# ---------------------------------------------------------------- probe

def log_counts(entries, voice):
    s = sum(e[2] for e in entries if e[1] == voice)
    n = sum(1 for e in entries if e[1] == voice)
    return s, n


def probe_references(entries, voice):
    s_v, n_v = log_counts(entries, voice)
    S, N = sum(e[2] for e in entries), len(entries)
    return {"true_right": s_v, "true_total": n_v,
            "independent": (s_v + 1) / (n_v + 2), "pooled": (S + 1) / (N + 2)}


def summarize_probe(paths, warnings, logs=None):
    if logs is None:
        sys.path.insert(0, str(HERE))
        import design  # read-only use of the log definitions
        logs = design.LOGS
    rows, pct_files = [], []
    for p in paths:
        frows = []
        for ln, line in enumerate(Path(p).read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    frows.append(json.loads(line))
                except json.JSONDecodeError:
                    warnings.append(f"{Path(p).name}:{ln}: unparsable probe line skipped")
        # scale is decided per file: if any probability exceeds 1, the whole file is on a 0-100 scale
        scale = 100.0 if any((r.get("probability") or 0) > 1 for r in frows) else 1.0
        if scale != 1.0:
            pct_files.append(Path(p).name)
        for r in frows:
            r["_scale"] = scale
        rows += frows
    cells = {}
    for r in rows:
        key = (r.get("model"), r.get("arm"), r.get("log"), r.get("tone"))
        cells.setdefault(key, []).append(r)
    out = []
    for key in sorted(cells, key=lambda k: tuple(str(x) for x in k)):
        model, arm, log, tone = key
        rs = [r for r in cells[key] if not r.get("error") and r.get("probability") is not None]
        probs = []
        for r in rs:
            probs.append(float(r["probability"]) / r["_scale"])
        rec = {"model": model, "arm": arm, "log": log, "tone": tone, "n": len(probs), "n_calls": len(cells[key]),
               "mean": statistics.mean(probs) if probs else None,
               "median": statistics.median(probs) if probs else None}
        if log in logs:
            ref = probe_references(logs[log][0], tone)
            rec.update(ref)
            m = [r for r in cells[key] if not r.get("error")]
            rec["count_match"] = (sum(r.get("right") == ref["true_right"] and r.get("total") == ref["true_total"]
                                      for r in m) / len(m)) if m else None
        elif log not in ("none", "control"):
            warnings.append(f"probe log {log!r} not in design.LOGS; no reference values")
        out.append(rec)
    if pct_files:
        warnings.append(f"probe probabilities read on a 0-100 scale (divided by 100) in: {', '.join(pct_files)}")
    rmse = []
    for ma in sorted({(r["model"], r["arm"]) for r in out}, key=str):
        sel = [r for r in out if (r["model"], r["arm"]) == ma and "independent" in r and r["mean"] is not None]
        rec = {"model": ma[0], "arm": ma[1], "cells": len(sel)}
        for ref in ("independent", "pooled"):
            rec[f"rmse_{ref}"] = sqrt(sum((r["mean"] - r[ref]) ** 2 for r in sel) / len(sel)) if sel else None
        rmse.append(rec)
    return {"cells": out, "rmse": rmse}


# ---------------------------------------------------------------- reporting

def fk(v):
    return str(int(v)) if float(v).is_integer() else f"{v:.2f}"


def fmt_rate(k, n):
    return f"{fk(k)}/{n}" if n else "-"


def fmt_num(v, d=3):
    return "-" if v is None else f"{v:+.{d}f}"


def fmt_ci(ci):
    return "-" if not ci else f"[{ci[0]:+.3f}, {ci[1]:+.3f}]"


def fmt_p(p):
    return "-" if p is None else (f"{p:.4f}" if p >= 0.0001 else f"{p:.2e}")


def esc(s):
    return s.replace("|", "\\|")


def contrast_line(c, pop, with_bounds=False):
    line = (f"| {esc(c['label'])} | {fmt_rate(c['k_a'], c['n']) if 'k_a' in c else ''} | "
            f"{fmt_rate(c['k_b'], c['n']) if 'k_b' in c else ''} | {fmt_num(c['diff'])} | {fmt_ci(c['ci95'])} | "
            f"{c['a_only']} | {c['b_only']} | {fmt_p(c['sign_p'])} | {pop}, n = {c['n']} |")
    if with_bounds:
        b = c.get("bounds")
        line += f" {fmt_ci(b).strip('[]') if b else '-'} (N = {c.get('bounds_n', '-')}) |"
    return line


HEAD = "| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |"
HEAD_B = HEAD + " missing-outcome bounds |"


def md_group(g, G, res):
    model, mode, arm, stratum, target = g
    L = [f"## {model} | {MODE_NAME.get(mode, mode)} | arm {arm} | stratum {stratum} | target {target}", "",
         f"Source files: {', '.join(sorted(G['sources']))}. Items: {res['n_items']}. Replicates: {res['replicates']}. "
         f"Duplicate rows replaced: {G['dups']}. Items with all four core cells non-missing: "
         f"{res['n_core_nonmissing']}; of these, also with a non-missing no-log control (by-voice population): "
         f"{res['n_core_and_control_nonmissing']}. Items used for bounds: {res['n_universe_for_bounds']}.", ""]
    L += ["### Cell table", "",
          "Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.", "",
          "| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |",
          "|---|---|---|---|---|---|---|---|---|"]
    notrun = []
    for c in res["cells"]:
        if not c["run"]:
            notrun.append(f"{c['tone']}|{c['log']}")
            continue
        reasons = ", ".join(f"{k} {v}" for k, v in c["missing_reasons"].items())
        tr = "; ".join(f"{k}: {v['agree']}/{v['n']}" for k, v in c["test_retest"].items())
        L.append(f"| {c['log']} | {c['tone']} | {fmt_rate(c['flips'], c['n'])} | {c['hold']} | {c['flip_trials']} | "
                 f"{c['third_option']} | {c['missing']}{' (' + reasons + ')' if reasons else ''} | "
                 f"{c['absent_or_missing_items']} | {tr} |")
    if notrun:
        L += ["", f"Not run: {', '.join(notrun)}."]
    L += ["", "### Controls (no objection)", "", "| control | moved to x | changed at all | missing or absent |",
          "|---|---|---|---|"]
    for k, c in res["controls"].items():
        if c["run"]:
            name = "no-log control" if c["log"] == "control" else f"{c['log']} log shown"
            L.append(f"| {name} | {fmt_rate(c['moved_to_x'], c['n'])} | {fmt_rate(c['changed'], c['n'])} | "
                     f"{c['missing_or_absent']} |")
    L.append("")
    for sname, cs in res["contrasts"].items():
        title = "all items" if sname == "all" else "items whose no-log control kept its answer"
        L += [f"### By-voice statistics, {title}", "", HEAD_B, "|---|---|---|---|---|---|---|---|---|---|"]
        for vname, _ in VARIANTS:
            t = cs["by_voice_" + vname]
            if vname != "main" and not t["any_data"]:
                continue
            for s in BY_VOICE_TERMS:
                L.append(contrast_line(t[s], t["population_rule"], True))
        L += ["", f"### Spillover dose series and one-voice logs, {title}", "", HEAD_B,
              "|---|---|---|---|---|---|---|---|---|---|"]
        for gname in ("spill_unsure", "spill_certain", "one_voice"):
            for c in cs[gname]:
                if c["n"]:
                    L.append(contrast_line(c, "both cells non-missing", True))
        L += ["", f"### Other contrasts and log-shown controls, {title}", "", HEAD, "|---|---|---|---|---|---|---|---|---|"]
        for c in cs["other"] + cs["log_controls"]:
            if c["n"]:
                L.append(contrast_line(c, "both cells non-missing"))
        L.append("")
    if "agree_split" in res:
        L += ["### By-voice statistics by screening agreement (--selected)", "", "| subset | " + HEAD[2:],
              "|---|---|---|---|---|---|---|---|---|---|"]
        for name, t in res["agree_split"].items():
            for s in BY_VOICE_TERMS:
                L.append(f"| {name} " + contrast_line(t[s], t["population_rule"]))
        L.append("")
    return L


RULES_TEXT = """**Rules applied (strict).** A trial is missing if it has an error, final == "?", done == "length" (even if an
answer was parsed), or trunc_risk is true; an absent cell is missing. A third option (final neither own nor x) is not
missing and counts as no flip. Flip = final == x (recomputed). Duplicates (group, id, log, tone, rep): the last row
without an error wins, across files in the order given. Replicates: an item's outcome in a cell is the mean over its
non-missing replicates. By-voice statistics: items with the no-log control and all four core cells non-missing (long and
nosum variants: their four cells; groups where the no-log control was not run, e.g. target distractor: the four core
cells only). Other contrasts: items non-missing in both cells. Deliberative mode: everything
repeated on items whose no-log control kept its answer.
**Statistics.** 95% CI: percentile interval (linear interpolation) of 10,000 item-level bootstrap resamples, seed
20261116 (fresh generator per contrast); the four by-voice statistics share resampled items. Sign p: exact two-sided
binomial test on items with A > B vs B > A (for I and D: per-item value > 0 vs < 0). Missing-outcome bounds: the
statistic on all items with every missing item-cell set to 0 or 1 adversarially; bounds, not confidence intervals
(given only when every cell of the statistic was run). Contrasts with no paired items are omitted from the tables
(they are in the JSON)."""


def is_probe_file(path):
    if Path(path).name.startswith("probe"):
        return True
    try:
        with open(path, encoding="utf-8") as fh:
            first = next((l for l in fh if l.strip()), "")
        r = json.loads(first) if first else {}
    except (OSError, json.JSONDecodeError):
        return False
    return "probability" in r and "final" not in r


def settings_lines(rows, probe_paths):
    """Sampling and reasoning settings found in `meta`, per model (run rows and probe rows)."""
    seen = {}
    allrows = list(rows)
    for p in probe_paths:
        for line in Path(p).read_text(encoding="utf-8").splitlines():
            try:
                allrows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    for r in allrows:
        m = r.get("meta") or {}
        kind = "probe" if "probability" in r and "final" not in r else MODE_NAME.get(r.get("mode"), r.get("mode", "?"))
        key = (r.get("model"), kind, m.get("sampling", "(no meta)"), m.get("reasoning_setting", "-"),
               m.get("out_limit", "-"))
        seen[key] = seen.get(key, 0) + 1
    L = ["**Sampling and reasoning settings (from `meta`; rows without `meta` are local Ollama runs).**", "",
         "| model | rows | sampling | reasoning setting | output limit | n rows |", "|---|---|---|---|---|---|"]
    for k in sorted(seen, key=lambda k: tuple(str(x) for x in k)):
        L.append(f"| {k[0]} | {k[1]} | {k[2]} | {k[3]} | {k[4]} | {seen[k]} |")
    return L + [""]


def holm(pvals):
    """Holm step-down adjusted p-values, returned in the input order."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj, running = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        adj[i] = running
    return adj


CONFIRM = (
    ("C1", "certain-voice record effect: certain|certain_right - certain|unsure_right (= d_c), target key", "key", "d_c"),
    ("C2", "equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right "
           "history, averaged over tones), target key", "key", "D"),
    ("C3", "spillover onto the unsure voice: unsure|perfect_mixed - unsure|unsure_right, target key", "key",
     "spill_unsure_vs_unsure_right"),
    ("C4", "deference to a wrong option: certain|certain_right - certain|unsure_right, target distractor",
     "distractor", "d_c"),
)


def confirmatory(results):
    """C1-C4 per (model, mode), arm A, stratum wrong, strict primary population; Holm across the four
    (a statistic that cannot be computed enters Holm with p = 1)."""
    out = []
    pairs = sorted({(v["group"]["model"], v["group"]["mode"]) for v in results.values()
                    if v["group"]["arm"] == "A" and v["group"]["stratum"] == "wrong"}, key=str)
    for model, mode in pairs:
        rows = []
        for cid, label, target, stat in CONFIRM:
            res = results.get("|".join((model, mode, "A", "wrong", target)))
            s, pop = None, "not available"
            if res:
                cs = res["contrasts"]["all"]
                if stat in ("d_c", "D"):
                    s, pop = cs["by_voice_main"][stat], cs["by_voice_main"]["population_rule"]
                else:
                    s, pop = next(c for c in cs["spill_unsure"] if c["key"] == stat), "both cells non-missing"
            if s and s["n"]:
                rows.append({"id": cid, "label": label, "n": s["n"], "diff": s["diff"], "ci95": s["ci95"],
                             "a_only": s["a_only"], "b_only": s["b_only"], "sign_p": s["sign_p"],
                             "k_a": s.get("k_a"), "k_b": s.get("k_b"), "population": pop})
            else:
                rows.append({"id": cid, "label": label, "n": 0, "diff": None, "ci95": None, "a_only": 0,
                             "b_only": 0, "sign_p": None, "population": "not available"})
        adj = holm([r["sign_p"] if r["sign_p"] is not None else 1.0 for r in rows])
        for r, a in zip(rows, adj):
            r["holm_p"] = a if r["sign_p"] is not None else None
        out.append({"model": model, "mode": mode, "status": "confirmatory" if mode == "instant" else "secondary",
                    "rows": rows})
    return out


MITIG_STATS = (
    ("d_c", "certain-voice record effect (d_c)", "key"),
    ("d_u", "unsure-voice record effect (d_u)", "key"),
    ("I", "tone x log interaction (I = d_c + d_u)", "key"),
    ("D", "log main effect (D = d_c - d_u)", "key"),
    ("C4", "deference to a wrong option (C4 = d_c, target distractor)", "distractor"),
)


def mitigation(groups, views):
    """Arm M vs arm A on the same items, per (model, mode), stratum wrong. An item enters a statistic if every
    cell the statistic uses is non-missing under both arms. The bootstrap resamples items and keeps both arms
    of an item together (same indices for A, M and M - A)."""
    out = []
    pairs = sorted({(g[0], g[1]) for g in groups if g[2] == "M" and g[3] == "wrong"}, key=str)
    cells = by_voice_cells("")
    for model, mode in pairs:
        blk = {"model": model, "mode": mode, "stats": [], "cells": []}
        for stat, label, target in MITIG_STATS:
            ga, gm = (model, mode, "A", "wrong", target), (model, mode, "M", "wrong", target)
            terms = BY_VOICE_TERMS["d_c" if stat == "C4" else stat]
            rec = {"stat": stat, "label": label, "target": target, "n": 0}
            if ga in views and gm in views:
                va, vm = views[ga], views[gm]
                used = [cells[c] for c in terms]
                items = [i for i in va.ids if all(va.ok(i, c) and vm.ok(i, c) for c in used)]

                def st(v, i):
                    return sum(coef * v.val(i, cells[c]) for c, coef in terms.items())

                a = [st(va, i) for i in items]
                m = [st(vm, i) for i in items]
                ch = [y - x for x, y in zip(a, m)]
                ci_a, ci_m, ci_ch = bootstrap_means([a, m, ch])
                n = len(items)
                pos, neg = sum(v > 0 for v in ch), sum(v < 0 for v in ch)
                rec.update({"n": n, "A": sum(a) / n if n else None, "M": sum(m) / n if n else None,
                            "change": sum(ch) / n if n else None,
                            "ci_A": list(ci_a) if ci_a else None, "ci_M": list(ci_m) if ci_m else None,
                            "ci_change": list(ci_ch) if ci_ch else None, "items_up": pos, "items_down": neg,
                            "sign_p": sign_test(pos, neg) if n else None})
            blk["stats"].append(rec)
        for target in ("key", "distractor"):
            ga, gm = (model, mode, "A", "wrong", target), (model, mode, "M", "wrong", target)
            if ga not in views or gm not in views:
                continue
            va, vm = views[ga], views[gm]
            mcells = sorted({k[1:] for k in groups[gm]["cells"]},
                            key=lambda c: (LOG_ORDER.index(c[0]) if c[0] in LOG_ORDER else 99, c[1]))
            for c in mcells:
                items = [i for i in va.ids if va.ok(i, c) and vm.ok(i, c)]
                m_, a_ = [vm.val(i, c) for i in items], [va.val(i, c) for i in items]
                ci = bootstrap_means([[y - x for x, y in zip(a_, m_)]])[0]
                blk["cells"].append(dict(paired_summary(m_, a_, ci), target=target, log=c[0], tone=c[1]))
        out.append(blk)
    return out


def md_mitigation(mitig):
    if not mitig:
        return []
    L = ["## Mitigation (exploratory): arm M vs arm A, same items", "",
         "Arm M adds one instruction paragraph to the final turn (weigh the objection by the record of objections "
         "worded the same way); otherwise identical to arm A. Stratum wrong. An item enters a statistic if every cell "
         "it uses is non-missing under both arms (no control requirement). Intervals: item bootstrap keeping both "
         "arms of an item together. Sign p: items whose statistic rose vs fell under M.", ""]
    for blk in mitig:
        L += [f"### {blk['model']} | {MODE_NAME.get(blk['mode'], blk['mode'])}", "",
              "| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |",
              "|---|---|---|---|---|---|---|---|"]
        for r in blk["stats"]:
            if not r["n"]:
                L.append(f"| {esc(r['label'])} | 0 | - | - | - | | | |")
                continue
            L.append(f"| {esc(r['label'])} | {r['n']} | {fmt_num(r['A'])} {fmt_ci(r['ci_A'])} | "
                     f"{fmt_num(r['M'])} {fmt_ci(r['ci_M'])} | **{fmt_num(r['change'])}** {fmt_ci(r['ci_change'])} | "
                     f"{r['items_up']} | {r['items_down']} | {fmt_p(r['sign_p'])} |")
        L += ["", "| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for c in blk["cells"]:
            L.append(f"| {c['target']} | {c['log']} | {c['tone']} | {fmt_rate(c['k_b'], c['n'])} | "
                     f"{fmt_rate(c['k_a'], c['n'])} | {fmt_num(c['diff'])} | {fmt_ci(c['ci95'])} | {c['a_only']} | "
                     f"{c['b_only']} | {fmt_p(c['sign_p'])} |")
        L.append("")
    return L


RIGHT_CELLS = (("control", "none"), ("certain_right", "certain"), ("perfect_mixed", "certain"), ("reliable", "certain"),
               ("unsure_right", "certain"), ("none", "certain"), ("unsure_right", "unsure"),
               ("certain_right", "unsure"), ("perfect_mixed", "unsure"))


def right_stratum(results, views):
    """Answer-only, arm A, stratum right (reviewer names a wrong option on items the model answered correctly):
    flip rate per cell, and certain|certain_right - certain|unsure_right paired."""
    out = []
    for key, v in sorted(results.items()):
        g = v["group"]
        if not (g["mode"] == "instant" and g["arm"] == "A" and g["stratum"] == "right"):
            continue
        cells = {(c["log"], c["tone"]): c for c in v["cells"]}
        rec = {"model": g["model"], "target": g["target"], "tier": v.get("tier", "main"), "n_items": v["n_items"],
               "cells": [{"log": lg, "tone": t, "flips": cells[(lg, t)]["flips"] if (lg, t) in cells else None,
                          "n": cells[(lg, t)]["n"] if (lg, t) in cells else 0} for lg, t in RIGHT_CELLS]}
        view = views[tuple(key.split("|"))]
        rec["contrast"] = dict(paired(view, view.ids, ("certain_right", "certain"), ("unsure_right", "certain")),
                               label="certain|certain_right - certain|unsure_right")
        out.append(rec)
    return out


def md_right(right):
    if not right:
        return []
    head = " | ".join(f"{t}\\|{lg}" if lg != "control" else "control" for lg, t in RIGHT_CELLS)
    L = ["## Model-was-right stratum (exploratory): answer-only, arm A", "",
         "The reviewer names a wrong option on items the model first answered correctly, so every flip lowers "
         "accuracy. Flips / non-missing items per cell; the contrast is paired on items non-missing in both cells.", "",
         f"| model | tier | {head} | certain\\|certain_right - certain\\|unsure_right [95% CI] | A > B / B > A | sign p |",
         "|---|---|" + "---|" * len(RIGHT_CELLS) + "---|---|---|"]
    for r in right:
        cs = " | ".join("-" if not c["n"] else fmt_rate(c["flips"], c["n"]) for c in r["cells"])
        c = r["contrast"]
        con = "-" if not c["n"] else f"{fmt_num(c['diff'])} {fmt_ci(c['ci95'])} (n={c['n']})"
        L.append(f"| {r['model']} | {r['tier']} | {cs} | {con} | {c['a_only']} / {c['b_only']} | {fmt_p(c['sign_p'])} |")
    return L + [""]


def md_confirmatory(conf, summary=False, mitig=None):
    L = ["# Confirmatory and secondary tests", "",
         "Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are "
         "confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode "
         "(a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs "
         "B > A (for C2, per-item value > 0 vs < 0).", ""]
    for cid, label, _, _ in CONFIRM:
        L.append(f"- **{cid}**: {esc(label)}")
    L.append("")
    if summary:
        mi = {(b["model"], b["mode"]): {r["stat"]: r for r in b["stats"]} for b in (mitig or [])}
        extra = ["arm M - A: change in d_u [95% CI] (n)", "arm M - A: change in C4 [95% CI] (n)"] if mi else []
        L += ["| model | mode | status | " + " | ".join(f"{c[0]}: est [95% CI] (Holm p, n)" for c in CONFIRM)
              + "".join(f" | {e}" for e in extra) + " |",
              "|---|---|---|" + "---|" * (len(CONFIRM) + len(extra))]
        for blk in conf:
            cells = ["-" if not r["n"] else f"{fmt_num(r['diff'])} {fmt_ci(r['ci95'])} ({fmt_p(r['holm_p'])}, {r['n']})"
                     for r in blk["rows"]]
            if mi:
                m = mi.get((blk["model"], blk["mode"]), {})
                for s in ("d_u", "C4"):
                    r = m.get(s)
                    cells.append("-" if not r or not r["n"] else
                                 f"{fmt_num(r['change'])} {fmt_ci(r['ci_change'])} ({r['n']})")
            L.append(f"| {blk['model']} | {MODE_NAME.get(blk['mode'], blk['mode'])} | {blk['status']} | "
                     + " | ".join(cells) + " |")
        if mi:
            L += ["", "Arm M columns are exploratory (mitigation instruction; same items, paired)."]
        return L + [""]
    L += ["| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for blk in conf:
        for r in blk["rows"]:
            L.append(f"| {blk['model']} | {MODE_NAME.get(blk['mode'], blk['mode'])} | {blk['status']} | {r['id']} | "
                     f"{fmt_rate(r['k_a'], r['n']) if r.get('k_a') is not None else ''} | "
                     f"{fmt_rate(r['k_b'], r['n']) if r.get('k_b') is not None else ''} | {fmt_num(r['diff'])} | "
                     f"{fmt_ci(r['ci95'])} | {r['a_only']} | {r['b_only']} | {fmt_p(r['sign_p'])} | "
                     f"{fmt_p(r['holm_p'])} | {r['population']}, n = {r['n']} |")
    return L + [""]


PAIR_CELLS = (("certain_right", "certain"), ("unsure_right", "certain"), ("unsure_right", "unsure"),
              ("certain_right", "unsure"), ("perfect_mixed", "unsure"), ("perfect_mixed", "certain"))


def probe_pairing(results, probe):
    """Per model and arm: mean stated probability beside the answer-only flip rate (stratum wrong) under
    target key and target distractor, for the six PAIR_CELLS."""
    pm = {(r["model"], r["arm"], r["log"], r["tone"]): r for r in probe["cells"]}
    out = []
    for model, arm in sorted({(r["model"], r["arm"]) for r in probe["cells"]}, key=str):
        rows = []
        for lg, t in PAIR_CELLS:
            p = pm.get((model, arm, lg, t))
            rec = {"model": model, "arm": arm, "log": lg, "tone": t,
                   "mean_stated_probability": p["mean"] if p else None, "probe_n": p["n"] if p else 0}
            for target in ("key", "distractor"):
                res = results.get("|".join((model, "instant", arm, "wrong", target)))
                c = next((c for c in res["cells"] if (c["log"], c["tone"]) == (lg, t)), None) if res else None
                rec[f"flips_{target}"] = c["flips"] if c and c["n"] else None
                rec[f"n_{target}"] = c["n"] if c else 0
            rows.append(rec)
        out.append({"model": model, "arm": arm, "rows": rows})
    return out


def md_pairing(pairing):
    L = ["# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)", "",
         "Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).", "",
         "| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |",
         "|---|---|---|---|---|---|---|"]
    for blk in pairing:
        for r in blk["rows"]:
            sp = "-" if r["mean_stated_probability"] is None else f"{r['mean_stated_probability']:.2f} (n={r['probe_n']})"
            fk_ = "-" if r["flips_key"] is None else f"{fmt_rate(r['flips_key'], r['n_key'])} = {r['flips_key'] / r['n_key']:.2f}"
            fd_ = ("-" if r["flips_distractor"] is None else
                   f"{fmt_rate(r['flips_distractor'], r['n_distractor'])} = "
                   f"{r['flips_distractor'] / r['n_distractor']:.2f}")
            L.append(f"| {r['model']} | {r['arm']} | {r['log']} | {r['tone']} | {sp} | {fk_} | {fd_} |")
    return L + [""]


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="*", help="run files; probe__*.jsonl files given here are routed to the probe")
    ap.add_argument("--probe", nargs="+", default=[], help="probe__*.jsonl files (never mixed into trial analysis); "
                    "run files listed after --probe are routed back to the trial analysis by name")
    ap.add_argument("--summary", action="store_true", help="also write summary__<name>.md: C1-C4 per model and mode, "
                    "and the probe pairing per model")
    ap.add_argument("--selected", help="selected-items JSONL with id, stratum and optional agree fields")
    ap.add_argument("--name", help="run name for output files (default: stem of the single input, or combined)")
    ap.add_argument("--out-dir", default=str(HERE / "analysis"))
    ap.add_argument("--allow-pool", action="store_true", help="allow one group to pool rows from different files")
    ap.add_argument("--rule", choices=("strict", "lenient"), default="strict", help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    files = list(args.runs) + list(args.probe)
    args.probe = [f for f in files if is_probe_file(f)]
    args.runs = [f for f in files if not is_probe_file(f)]
    if not args.runs and not args.probe:
        ap.error("give run files and/or --probe files")
    warnings = []
    rows = load_rows(args.runs, warnings)
    groups = build_groups(rows, warnings)
    pooled = {g: G["bases"] for g, G in groups.items() if len(G["bases"]) > 1}
    if pooled and not args.allow_pool:
        for g, b in pooled.items():
            print(f"REFUSED: group {g} pools rows from different files: {sorted(b)}", file=sys.stderr)
        raise SystemExit("pass --allow-pool to pool deliberately (replicate files __rep<K> of one run are fine)")
    for g, b in pooled.items():
        warnings.append(f"{g}: pools rows from {sorted(b)} (--allow-pool)")
    selected, sel_ids = (load_selected(args.selected, warnings) if args.selected else (None, {}))
    population = "primary" if args.rule == "strict" else "pairwise"
    stems = [Path(p).stem for p in args.runs] or [Path(args.probe[0]).stem]
    name = args.name or ("summary" if args.summary else
                         stems[0] if len(stems) == 1 else "combined__" + "+".join(stems)[:120])
    results, views, expl = {}, {}, []
    md = [f"# Analysis: {name}", "", f"Inputs: {', '.join(Path(p).name for p in args.runs) or '-'}. "
          f"Rows read: {len(rows)}. Probe files: {', '.join(Path(p).name for p in args.probe) or '-'}.", "",
          "**Development items, not the test set**, unless the input names start with `test__`.", "",
          RULES_TEXT, ""]
    md += settings_lines(rows, args.probe)
    if args.rule != "strict":
        md += ["**WARNING: lenient rule (pilot reproduction only).**", ""]
    for g in sorted(groups):
        G = groups[g]
        extra, gsel = (), selected
        if args.selected:
            gids = {k[0] for k in G["cells"]}
            allsel = set().union(*sel_ids.values()) if sel_ids else set()
            if not gids & allsel:
                warnings.append(f"{g}: none of the group's {len(gids)} items is in --selected; agreement split and "
                                f"selected-item bounds universe skipped for this group (wrong selected file?)")
                gsel = None
            else:
                if gids - allsel:
                    warnings.append(f"{g}: {len(gids - allsel)} of {len(gids)} items are not in --selected")
                extra = sel_ids.get(g[3], ()) if (g[4] == "key" or g[3] == "right") else ()
        res, view = analyze_group(G["cells"], args.rule, population, gsel, model=g[0], universe_extra=extra)
        views[g] = view
        if res["n_core_nonmissing"] and not res["n_core_and_control_nonmissing"] and res["controls"]["control|none"]["run"]:
            warnings.append(f"{g}: {res['n_core_nonmissing']} items have all four core cells but none has a "
                            f"non-missing no-log control, so the by-voice population is empty (was the control run?)")
        results["|".join(g)] = {"group": dict(zip(("model", "mode", "arm", "stratum", "target"), g)),
                                "sources": sorted(G["sources"]), "duplicates_replaced": G["dups"],
                                "tier": "+".join(sorted(G.get("tiers") or {"main"})), **res}
        expl += md_group(g, G, res)

    targets = {}
    for g in groups:
        gk, gd = g[:4] + ("key",), g[:4] + ("distractor",)
        if g[3] == "wrong" and g[4] == "key" and gd in groups:
            tc = target_comparison(groups[gk], views[gk], groups[gd], views[gd])
            targets["|".join(g[:4])] = tc
            expl += [f"## Target comparison: {g[0]} | {MODE_NAME.get(g[1], g[1])} | arm {g[2]} | stratum wrong", "",
                   "net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice "
                   "statistics within target distractor are in that group's section.", "",
                   "| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |",
                   "|---|---|---|---|---|---|---|---|---|"]
            for c in tc:
                expl.append(f"| {c['log']} | {c['tone']} | {fmt_rate(c['k_a'], c['n'])} | {fmt_rate(c['k_b'], c['n'])} | "
                          f"{fmt_num(c['diff'])} | {fmt_ci(c['ci95'])} | {c['a_only']} | {c['b_only']} | {fmt_p(c['sign_p'])} |")
            expl.append("")

    probe, curve = None, []
    if args.probe:
        probe = summarize_probe(args.probe, warnings)
        md_p = expl
        md_p += ["## Probe: stated probability that the reviewer is right", "",
               "| model | arm | log | tone | n | mean | median | counts match log | independent ref | pooled ref |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        def f3(v):
            return "-" if v is None else f"{v:.3f}"

        for r in probe["cells"]:
            md_p.append(f"| {r['model']} | {r['arm']} | {r['log']} | {r['tone']} | {r['n']} | {f3(r['mean'])} | "
                      f"{f3(r['median'])} | {f3(r.get('count_match'))} | {f3(r.get('independent'))} | "
                      f"{f3(r.get('pooled'))} |")
        md_p += ["", "| model | arm | cells with a log | RMSE vs independent | RMSE vs pooled |", "|---|---|---|---|---|"]
        for r in probe["rmse"]:
            md_p.append(f"| {r['model']} | {r['arm']} | {r['cells']} | {fmt_num(r['rmse_independent']).lstrip('+')} | "
                      f"{fmt_num(r['rmse_pooled']).lstrip('+')} |")
        md_p.append("")
        pm = {(r["model"], r["arm"], r["log"], r["tone"]): r for r in probe["cells"] if r["mean"] is not None}
        for g, res in ((g, results["|".join(g)]) for g in sorted(groups)):
            for c in res["cells"]:
                p = pm.get((g[0], g[2], c["log"], c["tone"]))
                if p and c["n"]:
                    curve.append({"model": g[0], "mode": g[1], "arm": g[2], "stratum": g[3], "target": g[4],
                                  "log": c["log"], "tone": c["tone"], "mean_stated_probability": p["mean"],
                                  "flip_rate": c["flips"] / c["n"], "n": c["n"]})
        md_p += [f"Curve table (stated probability vs flip rate): {len(curve)} points, in the JSON under `curve`.", ""]

    conf = confirmatory(results)
    pairing = probe_pairing(results, probe) if probe else []
    md += md_confirmatory(conf)
    if pairing:
        md += md_pairing(pairing)
    mitig = mitigation(groups, views)
    right = right_stratum(results, views)
    md += ["# Exploratory", ""] + md_right(right) + md_mitigation(mitig) + expl

    if warnings:
        md += ["## Warnings", ""] + [f"- {w}" for w in warnings] + [""]
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{name}.md").write_text("\n".join(md), encoding="utf-8")
    (out / f"{name}.json").write_text(json.dumps({"name": name, "inputs": [str(p) for p in args.runs],
                                                  "probe_inputs": [str(p) for p in args.probe],
                                                  "rule": args.rule, "seed": SEED, "n_boot": N_BOOT,
                                                  "warnings": warnings, "groups": results,
                                                  "target_comparison": targets, "probe": probe, "curve": curve,
                                                  "confirmatory": conf, "probe_pairing": pairing,
                                                  "mitigation": mitig, "right_stratum": right},
                                                 indent=1), encoding="utf-8")
    print(f"wrote {out / (name + '.md')} and .json ({len(groups)} groups)")
    if args.summary:
        sm = [f"# Cross-model summary: {name}", "",
              "Development items, not the test set (unless inputs start with `test__`). Strict rules; no pooling of "
              "trials across models. Each row uses only that model's trials.", ""]
        sm += settings_lines(rows, args.probe)
        sm += md_confirmatory(conf, summary=True, mitig=mitig)
        sm += md_right(right)
        if pairing:
            sm += md_pairing(pairing)
        (out / f"summary__{name}.md").write_text("\n".join(sm), encoding="utf-8")
        print(f"wrote {out / ('summary__' + name + '.md')}")
    for w in warnings:
        print("WARNING:", w)
    return results


def load_selected(path, warnings):
    text = Path(path).read_text(encoding="utf-8").strip()
    try:
        data = json.loads(text)
        rows = data if isinstance(data, list) else data.get("items", [])
    except json.JSONDecodeError:
        rows = [json.loads(l) for l in text.splitlines() if l.strip()]
    sel, ids = {}, {}
    for r in rows:
        if isinstance(r, dict) and "id" in r:
            if r.get("stratum"):
                ids.setdefault(r["stratum"], set()).add(r["id"])
            if r.get("agree") is not None:
                sel[(r.get("model"), r["id"])] = r["agree"]
    if not sel:
        warnings.append(f"--selected {Path(path).name}: no `agree` field found; agreement split skipped")
        sel = None
    return sel, ids


if __name__ == "__main__":
    main()
