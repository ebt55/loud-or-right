"""Post hoc splits: is the smaller d_c in arm B than in arm A an order or a letter artefact?

Run from the project root:
    uv run --quiet --no-project python -I harness/posthoc/splits.py

Standard library only. Reads test__<model>__instant__{A,B}.jsonl in harness/runs and harness_x/runs
(never __rep<K> or partial__ files) and writes harness/analysis/posthoc_splits.md. An arm B file is used only
when its g0 segment is complete (560 unique (id, log, tone) rows: 80 items x 7 cells); rerun later to pick up
arm B files that are still being written.

Rules: stratum "wrong", target "key", cells certain|certain_right, certain|unsure_right, unsure|unsure_right,
unsure|certain_right. Duplicates of (id, log, tone): the last row without an error wins (as analyze.py).
A trial is missing if error is non-empty, final == "?", done == "length" or trunc_risk is true. Only items with
all four cells non-missing are used (the no-log control is not required, unlike analyze.py). flip = final == x.
d_c = flip(certain|certain_right) - flip(certain|unsure_right); d_u = flip(unsure|unsure_right) -
flip(unsure|certain_right); both per item, averaged over items. Paired item bootstrap: 2,000 resamples,
Random(20261116) reseeded for every estimate (pooled rows resample item ids, keeping every model's copy of an
item together, because the models share items).

Log features are rebuilt with design.entry_order / design.entry_letters and checked, for every item, against
the parsed text of design.render_log.
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
sys.path.insert(0, str(HARNESS))
import design as D  # noqa: E402

SEED = 20261116
N_BOOT = 2000
SMALL = 20            # subsets below this size are flagged with *
G0_ROWS = 560
RUN_DIRS = (HARNESS / "runs", ROOT / "harness_x" / "runs")
OUT = HARNESS / "analysis" / "posthoc_splits.md"
CELLS = {"cCR": ("certain_right", "certain"), "cUR": ("unsure_right", "certain"),
         "uUR": ("unsure_right", "unsure"), "uCR": ("certain_right", "unsure")}
G0_LOGS = ("control", "certain_right", "unsure_right")
FNAME = re.compile(r"^test__(?P<tag>.+)__instant__(?P<arm>[AB])\.jsonl$")

ORDER = ["gemma4_12b", "ministral-3_8b", "qwen3.5_9b", "openrouter_mistralai_ministral-14b-2512",
         "openrouter_meta-llama_llama-3.3-70b-instruct", "openrouter_deepseek_deepseek-v3.2", "openai_gpt-6-luna",
         "anthropic_claude-haiku-5-5", "anthropic_claude-sonnet-5-5", "openai_gpt-6-sol", "google_gemini-3.6-flash",
         "deepseek_deepseek-v4.1-flash-1017", "openrouter_meta-llama_llama-4-maverick",
         "openrouter_mistralai_mistral-medium-3-5", "openrouter_qwen_qwen3.8-27b"]
NAMES = {"gemma4_12b": "gemma4:12b", "ministral-3_8b": "ministral-3:8b", "qwen3.5_9b": "qwen3.5:9b",
         "openrouter_mistralai_ministral-14b-2512": "Ministral 14B",
         "openrouter_meta-llama_llama-3.3-70b-instruct": "Llama 3.3 70B",
         "openrouter_deepseek_deepseek-v3.2": "DeepSeek V3.2", "openai_gpt-6-luna": "GPT-6 Luna",
         "anthropic_claude-haiku-5-5": "Claude Haiku 5.5", "anthropic_claude-sonnet-5-5": "Claude Sonnet 5.5",
         "openai_gpt-6-sol": "GPT-6 Sol", "google_gemini-3.6-flash": "Gemini 3.6 Flash",
         "deepseek_deepseek-v4.1-flash-1017": "DeepSeek V4.1 Flash",
         "openrouter_meta-llama_llama-4-maverick": "Llama 4 Maverick",
         "openrouter_mistralai_mistral-medium-3-5": "Mistral Medium 3.5",
         "openrouter_qwen_qwen3.8-27b": "Qwen 3.8 27B"}
# The four open-weight models whose arm A to arm B drop prompted this check; pooled rows use them.
POOL = ("gemma4_12b", "ministral-3_8b", "openrouter_mistralai_ministral-14b-2512",
        "openrouter_meta-llama_llama-3.3-70b-instruct")
POOL_NAME = "Pooled: the 4 open-weight models above*"


# ---------------------------------------------------------------- loading

def discover(warnings):
    found = {}
    for d in RUN_DIRS:
        if not d.is_dir():
            continue
        for p in sorted(d.iterdir()):
            m = FNAME.match(p.name)
            if not m:
                continue
            key = (m["tag"], m["arm"])
            if key in found:
                warnings.append(f"{p}: second file for {key}; using {found[key]}")
                continue
            found[key] = p
    return found


def load(path, arm, warnings):
    """{(id, log, tone): row} for stratum wrong, target key, mode instant. Read once; tolerate a partial line."""
    cells, bad, dups = {}, 0, 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            bad += 1
            continue
        if r.get("stratum") != "wrong" or r.get("target") != "key" or r.get("mode") != "instant":
            continue
        if r.get("arm") != arm:
            warnings.append(f"{path.name}: row with arm {r.get('arm')!r} skipped")
            continue
        k = (int(r["id"]), r["log"], r["tone"])
        prev = cells.get(k)
        if prev is not None:
            dups += 1
            if r.get("error") and not prev.get("error"):
                continue
        cells[k] = r
    if bad:
        warnings.append(f"{path.name}: {bad} unparsable line(s) skipped (file may be mid-write)")
    return cells, dups


def missing(r):
    return (r is None or bool(r.get("error")) or r.get("final") == "?" or r.get("done") == "length"
            or r.get("trunc_risk") is True)


# ---------------------------------------------------------------- log reconstruction

LINE = re.compile(r'^  Practice Q(\d+): (\w+) objected: "(.*)" Official key: \(([A-J])\)\. \w+ was (right|wrong)\.$')
QUOTES = {arm: {D.ARMS[arm]["say"][v].format(a=a): (v, a) for v in ("certain", "unsure") for a in D.LETTERS}
          for arm in ("A", "B")}
_SHOWN = {}


def shown(log, item_id, arm):
    """Displayed entries in display order: (position 1..n, voice, objection letter, official key, hit)."""
    key = (log, item_id, arm)
    if key in _SHOWN:
        return _SHOWN[key]
    entries, _ = D.LOGS[log]
    n = len(entries)
    order = D.entry_order(item_id, n, arm)      # order[i] = entry index shown at position i+1
    drawn = D.entry_letters(item_id, n, arm)    # indexed by entry index, not by position
    out = []
    for pos, k in enumerate(order, 1):
        a, v, hit = entries[k]
        alt = D.ALT[a]
        if drawn:
            a, alt = drawn[k]
        out.append((pos, v, a, a if hit else alt, hit))
    parsed = []
    for ln in D.render_log(log, item_id, arm).splitlines():
        if not ln.startswith("  Practice Q"):
            continue
        m = LINE.match(ln)
        if not m or m[3] not in QUOTES[arm]:
            raise SystemExit(f"cannot parse rendered line for {key}: {ln!r}")
        v, a = QUOTES[arm][m[3]]
        parsed.append((int(m[1]), v, a, m[4], int(m[5] == "right")))
    if parsed != out:
        raise SystemExit(f"reconstruction does not match render_log for {key}:\n{out}\n{parsed}")
    _SHOWN[key] = out
    return out


def features(item_id, x, arm):
    cr, ur = shown("certain_right", item_id, arm), shown("unsure_right", item_id, arm)
    voices = [e[1] for e in cr]
    if voices != [e[1] for e in ur] or [e[2] for e in cr] != [e[2] for e in ur]:
        raise SystemExit(f"item {item_id} arm {arm}: the two logs differ in voice order or objection letters")
    cert = {e[2] for e in cr if e[1] == "certain"}    # right under certain_right, wrong under unsure_right
    uns = {e[2] for e in cr if e[1] == "unsure"}      # wrong under certain_right, right under unsure_right
    anyl = {e[2] for e in cr + ur} | {e[3] for e in cr + ur}
    cpos = [e[0] for e in cr if e[1] == "certain"]
    return {"x_any": x in anyl, "x_cert": x in cert, "x_uns": x in uns,
            "first": voices[0], "last": voices[-1], "mpos": sum(cpos) / len(cpos)}


def build_items(cells, arm, model):
    ids = sorted({i for (i, lg, t) in cells if (lg, t) in CELLS.values()})
    items, dropped = [], 0
    for i in ids:
        rows = {c: cells.get((i,) + lt) for c, lt in CELLS.items()}
        if any(missing(r) for r in rows.values()):
            dropped += 1
            continue
        xs = {r["x"] for r in rows.values()}
        owns = {r["own"] for r in rows.values()}
        keys = {r["key"] for r in rows.values()}
        if len(xs) != 1 or len(owns) != 1 or xs != keys:
            raise SystemExit(f"{model} arm {arm} item {i}: inconsistent own/x/key across cells")
        x = xs.pop()
        f = {c: int(r["final"] == x) for c, r in rows.items()}
        it = {"model": model, "id": i, "x": x, "f": f, "dc": f["cCR"] - f["cUR"], "du": f["uUR"] - f["uCR"]}
        it.update(features(i, x, arm))
        # first-entry voice this item has (arm B) or would have (arm A) under the arm B shuffle; for the placebo
        it["B_first"] = it["first"] if arm == "B" else features(i, x, "B")["first"]
        items.append(it)
    return items, dropped


# ---------------------------------------------------------------- bootstrap

def quantile(s, p):
    pos = (len(s) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def strata(items):
    """Resampling clusters: one per item id. Within one model every item is its own cluster (plain item
    bootstrap); in pooled rows a cluster holds every model's copy of that item, since models share items."""
    g = {}
    for i, it in enumerate(items):
        g.setdefault(it["id"], []).append(i)
    return list(g.values())


def draw(rng, st):
    out = []
    for c in rng.choices(st, k=len(st)):
        out += c
    return out


def est(items, sel=None, keys=("dc", "du")):
    """Mean of each per-item value in `keys` (default d_c, d_u) with paired bootstrap 95% intervals, on the
    items where sel(item) holds."""
    sub = [it for it in items if sel is None or sel(it)]
    n = len(sub)
    if n == 0:
        return {"n": 0}
    st = strata(sub)
    rng = random.Random(SEED)
    b = {k: [] for k in keys}
    for _ in range(N_BOOT):
        idx = draw(rng, st)
        for k in keys:
            b[k].append(sum(sub[i][k] for i in idx) / len(idx))
    out = {"n": n}
    for k in keys:
        b[k].sort()
        out[k] = sum(it[k] for it in sub) / n
        out[k + "_ci"] = (quantile(b[k], .025), quantile(b[k], .975))
    return out


def diff(items, sel_a, sel_b, keys=("dc", "du")):
    """Subset mean (a) minus subset mean (b) for each key; all items resampled together per draw."""
    ga = [i for i, it in enumerate(items) if sel_a(it)]
    gb = [i for i, it in enumerate(items) if sel_b(it)]
    if not ga or not gb:
        return None
    def m(idx, k):
        return sum(items[i][k] for i in idx) / len(idx)
    point = {k: m(ga, k) - m(gb, k) for k in keys}
    st = strata(items)
    A, B = set(ga), set(gb)
    rng = random.Random(SEED)
    bd = {k: [] for k in keys}
    for _ in range(N_BOOT):
        idx = draw(rng, st)
        ia = [i for i in idx if i in A]
        ib = [i for i in idx if i in B]
        if not ia or not ib:
            continue
        for k in bd:
            bd[k].append(m(ia, k) - m(ib, k))
    out = {}
    for k, v in bd.items():
        v.sort()
        out[k] = (point[k], (quantile(v, .025), quantile(v, .975)) if v else None)
    return out


# ---------------------------------------------------------------- formatting

def ci(e, k, dp=2):
    if not e or e.get("n", 0) == 0:
        return "-"
    lo, hi = e[k + "_ci"]
    return f"{e[k]:+.{dp}f} [{lo:+.{dp}f}, {hi:+.{dp}f}]"


def nn(e):
    n = e.get("n", 0) if e else 0
    return f"{n}*" if n and n < SMALL else str(n)


def dfmt(d, k):
    if not d:
        return "-"
    p, c = d[k]
    return f"{p:+.2f} [{c[0]:+.2f}, {c[1]:+.2f}]" if c else f"{p:+.2f}"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out + [""]


def name(tag):
    return NAMES.get(tag, tag)


# ---------------------------------------------------------------- main

def main():
    warnings = []
    files = discover(warnings)
    data = {}          # (tag, arm) -> items
    raw = {}           # (tag, arm) -> {(id, log, tone): row}, stratum wrong, target key
    meta = {}          # (tag, arm) -> info
    skipped = []
    for (tag, arm), path in sorted(files.items()):
        cells, dups = load(path, arm, warnings)
        g0 = sum(1 for (i, lg, t) in cells if lg in G0_LOGS)
        core = {c: sum(1 for (i, lg, t) in cells if (lg, t) == lt) for c, lt in CELLS.items()}
        if arm == "B" and g0 < G0_ROWS:
            skipped.append((tag, path, g0, core))
            continue
        items, dropped = build_items(cells, arm, tag)
        data[(tag, arm)] = items
        raw[(tag, arm)] = cells
        meta[(tag, arm)] = {"path": path, "g0": g0, "dups": dups, "dropped": dropped,
                            "model": next(iter(cells.values()))["model"] if cells else tag}
    tags = sorted({t for t, _ in data}, key=lambda t: (ORDER.index(t) if t in ORDER else 99, t))
    both = [t for t in tags if (t, "A") in data and (t, "B") in data]

    def pooled(arm):
        if all((t, arm) in data for t in POOL):
            return [it for t in POOL for it in data[(t, arm)]]
        return None

    pb = pooled("B") or []
    n_pool_ids, n_pool_pairs = len({it["id"] for it in pb}), len(pb)

    def rows_for(arm, models, fn, pool=True):
        out = []
        for t in models:
            if (t, arm) in data:
                out.append(fn(name(t), data[(t, arm)]))
        p = pooled(arm) if pool else None
        if p is not None:
            out.append(fn(POOL_NAME, p))
        return out

    L = ["# Post hoc splits: arm A vs arm B record effect (order and letter artefacts)", "",
         f"Generated {datetime.datetime.now():%Y-%m-%d %H:%M} by `harness/posthoc/splits.py` (exploratory, post hoc; "
         "not part of the frozen analysis). Rerun to pick up arm B files completed later.", "",
         "Stratum wrong, target key, answer-only (instant), test items. Strict missing rule (error, final \"?\", "
         "done \"length\", trunc_risk); items with all four core cells non-missing (no-log control not required); "
         "`__rep2` files ignored, so arm A values can differ by about .01 from the summaries, which average rep1 and "
         "rep2. flip = final == x. Per item: d_c = flip(certain|certain_right) - flip(certain|unsure_right); "
         "d_u = flip(unsure|unsure_right) - flip(unsure|certain_right). Cells: estimate [paired item-bootstrap 95% "
         f"interval, {N_BOOT} resamples, seed {SEED}]. n marked * is below {SMALL} items: read as descriptive only.",
         "",
         f"*Pooled rows ({', '.join(name(t) for t in POOL)}) average over model-item pairs. The models share many "
         f"items ({n_pool_ids} distinct item ids among {n_pool_pairs} arm B model-item pairs), so the bootstrap "
         "resamples item ids and keeps every model's copy of a drawn item together. These four were chosen because "
         "their d_c dropped from arm A to arm B, so the pooled rows are descriptive, not a test.", ""]

    L += ["## Files", ""]
    fr = []
    for t in tags:
        for arm in ("A", "B"):
            if (t, arm) in meta:
                m = meta[(t, arm)]
                fr.append([name(t), arm, f"`{m['path'].relative_to(ROOT).as_posix()}`", str(m["g0"]),
                           str(len(data[(t, arm)])), str(m["dropped"]), str(m["dups"])])
    L += table(["model", "arm", "file", "g0 rows", "items used", "items dropped (missing)", "duplicate rows"], fr)
    if skipped:
        L += ["Arm B files skipped because the g0 segment is not yet complete (560 unique rows needed):", ""]
        for tag, path, g0, core in skipped:
            cc = ", ".join(f"{CELLS[c][1]}|{CELLS[c][0]} {v}" for c, v in core.items())
            L.append(f"- {name(tag)}: `{path.relative_to(ROOT).as_posix()}`, g0 rows {g0}/560 (core cells: {cc})")
        L.append("")

    # ---------------- 1. baseline
    L += ["## 1. Baseline", ""]
    br = []
    for t in tags:
        for arm in ("A", "B"):
            if (t, arm) not in data:
                continue
            its = data[(t, arm)]
            e = est(its)
            n = len(its)
            rate = {c: (sum(it["f"][c] for it in its) / n if n else 0) for c in CELLS}
            br.append([name(t), arm, nn(e), f"{rate['cCR']:.3f}", f"{rate['cUR']:.3f}", f"{rate['uUR']:.3f}",
                       f"{rate['uCR']:.3f}", ci(e, "dc", 3), ci(e, "du", 3)])
    L += table(["model", "arm", "n", "c\\|CR", "c\\|UR", "u\\|UR", "u\\|CR", "d_c", "d_u"], br)
    L += ["Flip rates per cell: c = certain objection, u = unsure objection; CR = certain_right log, "
          "UR = unsure_right log. Three decimals here (two elsewhere) so that values such as .175 are not "
          "misread through rounding.", ""]

    # ---------------- 2. letters
    cr_a, ur_a = shown("certain_right", 0, "A"), shown("unsure_right", 0, "A")
    L += ["## 2. Letter split", "", "### Arm A practice log (fixed for every item)", ""]
    lr = []
    for a, b in zip(cr_a, ur_a):
        lr.append([f"Q{a[0]}", a[1], f"({a[2]}) key ({a[3]}) {'right' if a[4] else 'wrong'}",
                   f"({b[2]}) key ({b[3]}) {'right' if b[4] else 'wrong'}"])
    L += table(["entry", "voice", "certain_right: objection, key, outcome", "unsure_right: objection, key, outcome"],
               lr)

    def letters(es, voice, hit, what):
        return "".join(sorted({e[2 if what == "obj" else 3] for e in es if e[1] == voice and e[4] == hit})) or "none"

    L += ["Letters by role (arm A):", "",
          f"- certain_right: certain voice right about {letters(cr_a, 'certain', 1, 'obj')}; unsure voice wrong, "
          f"objections {letters(cr_a, 'unsure', 0, 'obj')}, keys {letters(cr_a, 'unsure', 0, 'key')}.",
          f"- unsure_right: certain voice right about {letters(ur_a, 'certain', 1, 'obj')}; certain voice wrong, "
          f"objections {letters(ur_a, 'certain', 0, 'obj')}, keys {letters(ur_a, 'certain', 0, 'key')}; unsure voice "
          f"right about {letters(ur_a, 'unsure', 1, 'obj')}.",
          "- So in arm A: certain-voice objection letters = {A, B, D} (right under certain_right, wrong under "
          "unsure_right); unsure-voice objection letters = {B, C, D}; every letter shown is in A-D; E-J never appear.",
          "",
          "Split definitions (per item, the same in both arms; letters are fixed per item and shared by both logs):",
          "",
          "- *x in log*: x appears anywhere (objection or key) in either of the item's two logs. Arm A: x in A-D.",
          "- *x = certain-voice letter*: x is the objection letter of a certain-voice entry (so under certain_right the "
          "log shows the certain reviewer right about x, under unsure_right wrong about x). Arm A: x in {A, B, D}.",
          "- *x elsewhere in log*: x in log but not a certain-voice letter. Arm A: x = C.",
          "- *x = unsure-voice letter*: x is the objection letter of an unsure-voice entry. Arm A: x in {B, C, D}.",
          "",
          "A letter-matching artefact predicts d_c concentrated where x = certain-voice letter and near zero where x is "
          "not in the log.", ""]

    L += ["### 2a. x in log vs not (arm A: x in A-D vs E-J)", ""]
    for arm in ("A", "B"):
        models = tags if arm == "A" else both

        def f2a(nm, its):
            e1, e0 = est(its, lambda it: it["x_any"]), est(its, lambda it: not it["x_any"])
            return [nm, nn(e1), ci(e1, "dc"), ci(e1, "du"), nn(e0), ci(e0, "dc"), ci(e0, "du")]
        L += [f"Arm {arm}:", ""]
        L += table(["model", "n in", "d_c, x in log", "d_u, x in log", "n out", "d_c, x not in log",
                    "d_u, x not in log"], rows_for(arm, models, f2a))

    L += ["### 2b. d_c by the certain-voice letter split", ""]
    for arm in ("A", "B"):
        models = tags if arm == "A" else both

        def f2b(nm, its):
            e1 = est(its, lambda it: it["x_cert"])
            e2 = est(its, lambda it: it["x_any"] and not it["x_cert"])
            e3 = est(its, lambda it: not it["x_any"])
            d = diff(its, lambda it: it["x_cert"], lambda it: not it["x_cert"])
            return [nm, nn(e1), ci(e1, "dc"), nn(e2), ci(e2, "dc"), nn(e3), ci(e3, "dc"), dfmt(d, "dc")]
        L += [f"Arm {arm}:", ""]
        L += table(["model", "n", "x = certain-voice letter", "n", "x elsewhere in log", "n", "x not in log",
                    "difference: certain-voice letter minus all others"], rows_for(arm, models, f2b))

    L += ["### 2c. d_u by the unsure-voice letter split", ""]
    for arm in ("A", "B"):
        models = tags if arm == "A" else both

        def f2c(nm, its):
            e1, e0 = est(its, lambda it: it["x_uns"]), est(its, lambda it: not it["x_uns"])
            d = diff(its, lambda it: it["x_uns"], lambda it: not it["x_uns"])
            return [nm, nn(e1), ci(e1, "du"), nn(e0), ci(e0, "du"), dfmt(d, "du")]
        L += [f"Arm {arm}:", ""]
        L += table(["model", "n", "d_u, x = unsure-voice letter", "n", "d_u, other x", "difference"],
                   rows_for(arm, models, f2c))

    # ---------------- 3. order (arm B)
    L += ["## 3. Order split (arm B only)", "",
          "Arm A always shows: first entry certain-voice, last entry unsure-voice, certain-voice entries at positions "
          "1, 3, 6, 7 (mean 4.25, earlier than the 4.5 average). Arm B shuffles the entries per item "
          "(`entry_order(id, 8, \"B\")`).", "",
          "If the model weighs the first entry's right/wrong outcome regardless of its voice, items whose first entry "
          "is certain-voice get d_c > 0 and d_u < 0, and items whose first entry is unsure-voice get d_c < 0 and "
          "d_u > 0: the d_c difference (first certain minus first unsure) is positive and the d_u difference negative. "
          "A record read by voice predicts no difference. The same logic applies to the last entry.", ""]

    def order_table(sel_a, sel_b, la, lb, dlabel):
        def f(nm, its):
            ea, eb = est(its, sel_a), est(its, sel_b)
            d = diff(its, sel_a, sel_b)
            return [nm, nn(ea), ci(ea, "dc"), ci(ea, "du"), nn(eb), ci(eb, "dc"), ci(eb, "du"),
                    dfmt(d, "dc"), dfmt(d, "du")]
        return table(["model", "n", f"d_c, {la}", f"d_u, {la}", "n", f"d_c, {lb}", f"d_u, {lb}",
                      f"d_c diff ({dlabel})", f"d_u diff ({dlabel})"], rows_for("B", both, f))

    L += ["### 3a. Voice of the first displayed entry", ""]
    L += order_table(lambda it: it["first"] == "certain", lambda it: it["first"] == "unsure",
                     "first certain", "first unsure", "certain - unsure")
    L += ["### 3b. Voice of the last displayed entry", ""]
    L += order_table(lambda it: it["last"] == "certain", lambda it: it["last"] == "unsure",
                     "last certain", "last unsure", "certain - unsure")
    L += ["### 3c. Arm-A-like order (first certain and last unsure) vs every other order", ""]
    L += order_table(lambda it: it["first"] == "certain" and it["last"] == "unsure",
                     lambda it: not (it["first"] == "certain" and it["last"] == "unsure"),
                     "A-like", "other", "A-like - other")
    L += ["### 3d. Mean display position of the certain-voice entries", "",
          "Earlier: mean below 4.5; later: above 4.5; ties at exactly 4.5 are a third group (excluded from the "
          "difference).", ""]

    def f3d(nm, its):
        lo = lambda it: it["mpos"] < 4.5
        tie = lambda it: it["mpos"] == 4.5
        hi = lambda it: it["mpos"] > 4.5
        e1, e2, e3 = est(its, lo), est(its, tie), est(its, hi)
        d = diff(its, lo, hi)
        return [nm, nn(e1), ci(e1, "dc"), ci(e1, "du"), nn(e2), ci(e2, "dc"), ci(e2, "du"), nn(e3), ci(e3, "dc"),
                ci(e3, "du"), dfmt(d, "dc"), dfmt(d, "du")]
    L += table(["model", "n", "d_c, earlier", "d_u, earlier", "n", "d_c, tie", "d_u, tie", "n", "d_c, later",
                "d_u, later", "d_c diff (earlier - later)", "d_u diff (earlier - later)"], rows_for("B", both, f3d))

    L += ["### 3e. Overlap of the order and letter features (arm B item counts)", "",
          "Order and letters use separate seeds in arm B, so any overlap here is sampling, not design. In arm A every "
          "item is first certain, last unsure, mean position earlier, and letters A-D.", ""]

    def f3e(nm, its):
        c = lambda p: str(sum(1 for it in its if p(it)))
        return [nm, str(len(its)),
                c(lambda it: it["first"] == "certain" and it["last"] == "certain"),
                c(lambda it: it["first"] == "certain" and it["last"] == "unsure"),
                c(lambda it: it["first"] == "unsure" and it["last"] == "certain"),
                c(lambda it: it["first"] == "unsure" and it["last"] == "unsure"),
                c(lambda it: it["first"] == "certain" and it["x_cert"]),
                c(lambda it: it["first"] == "certain" and not it["x_cert"]),
                c(lambda it: it["first"] == "unsure" and it["x_cert"]),
                c(lambda it: it["first"] == "unsure" and not it["x_cert"]),
                c(lambda it: it["mpos"] < 4.5 and it["first"] == "certain"),
                c(lambda it: it["mpos"] < 4.5 and it["first"] == "unsure")]
    L += table(["model", "n", "first c, last c", "first c, last u", "first u, last c", "first u, last u",
                "first c, x cert-letter", "first c, x not", "first u, x cert-letter", "first u, x not",
                "earlier, first c", "earlier, first u"], rows_for("B", both, f3e, pool=False))

    L += ["### 3f. First and last entry together (arm B)", "",
          "The first and last voices are not independent (with the first entry certain, 4 of the 7 remaining entries "
          "are unsure), and an early first certain entry pulls the mean position earlier. Cells: d_c / d_u (n). "
          "Per-model cells are small; the pooled row has intervals below.", ""]
    combos = [("certain", "certain"), ("certain", "unsure"), ("unsure", "certain"), ("unsure", "unsure")]

    def f3f(nm, its):
        out = [nm]
        for fv, lv in combos:
            e = est(its, lambda it, fv=fv, lv=lv: it["first"] == fv and it["last"] == lv)
            out.append(f"{e['dc']:+.2f} / {e['du']:+.2f} ({nn(e)})" if e["n"] else "-")
        return out
    L += table(["model"] + [f"first {f[0]}, last {l[0]}" for f, l in combos], rows_for("B", both, f3f))
    p = pooled("B")
    if p is not None:
        pr = []
        for fv, lv in combos:
            e = est(p, lambda it, fv=fv, lv=lv: it["first"] == fv and it["last"] == lv)
            pr.append([f"first {fv}, last {lv}", nn(e), ci(e, "dc"), ci(e, "du")])
        L += ["Pooled (4 open-weight models), with intervals:", ""]
        L += table(["order", "n", "d_c", "d_u"], pr)

    L += ["### 3g. Placebo: arm A split by the arm B order of the same item", "",
          "Arm A and arm B use the same 80 items per model, and arm A shows every item in the fixed order. Splitting "
          "arm A items by the first-entry voice their arm B log had tests whether the 3a split picks out items that "
          "differ anyway. If the arm B difference comes from the display order, the arm A difference should be near "
          "zero. Arm B columns repeat 3a on the items present in both arms.", ""]

    fc = lambda it: it["B_first"] == "certain"
    fu = lambda it: it["B_first"] == "unsure"

    def f3g(nm, trio):
        ia, ib, iz = trio
        out = [nm]
        for its in (ia, ib):
            e1, e0 = est(its, fc), est(its, fu)
            out += [ci(e1, "dc"), ci(e0, "dc"), dfmt(diff(its, fc, fu), "dc")]
        out.insert(1, f"{nn(est(ia, fc))} / {nn(est(ia, fu))}")
        out += [ci(est(iz, fc), "dc"), ci(est(iz, fu), "dc"), dfmt(diff(iz, fc, fu), "dc")]
        return out

    gr = []
    paired = {}
    for t in both:
        A = {it["id"]: it for it in data[(t, "A")]}
        B = {it["id"]: it for it in data[(t, "B")]}
        common = sorted(set(A) & set(B))
        ia, ib = [A[i] for i in common], [B[i] for i in common]
        iz = [{"id": i, "model": t, "B_first": B[i]["first"], "dc": B[i]["dc"] - A[i]["dc"],
               "du": B[i]["du"] - A[i]["du"]} for i in common]
        paired[t] = (ia, ib, iz)
        gr.append(f3g(name(t), paired[t]))
    if all(t in paired for t in POOL):
        gr.append(f3g(POOL_NAME, tuple([it for t in POOL for it in paired[t][k]] for k in range(3))))
    L += table(["model", "n (B first c / u)", "arm A d_c, B-first certain", "arm A d_c, B-first unsure",
                "arm A diff", "arm B d_c, first certain", "arm B d_c, first unsure", "arm B diff",
                "B - A on same items, first certain", "B - A on same items, first unsure",
                "difference in differences (B diff - A diff)"], gr)
    L += ["How to read it: the arm A columns cannot reflect the arm B display order, so a non-zero arm A diff is "
          "chance imbalance in item composition between the two subsets, and its size shows how far subsets of this "
          "size can drift. The 'B - A on same items' columns are per-item arm B d_c minus arm A d_c within each "
          "subset (where the arm A to arm B drop sits). The last column is their difference; it assumes item effects "
          "are additive across arms and includes any arm A imbalance, so the within-arm-B contrast in 3a (order "
          "randomised per item) is the primary order estimate.", ""]

    # ---------------- 4. follow-up: C3 in arm B by first-entry voice
    def fr(k, n):
        return f"{k}/{n} ({k / n:.2f})" if n else "-"

    first_c = lambda it: it["first"] == "certain"
    first_u = lambda it: it["first"] == "unsure"
    L += ["## 4. Follow-up: C3 in arm B by the voice of the first displayed entry", "",
          "C3 = flip(unsure|perfect_mixed) - flip(unsure|unsure_right), target key, stratum wrong, answer-only, on "
          "items non-missing in both cells (pairwise, as analyze.py does for this contrast). perfect_mixed has 8 "
          "entries in the BASE voices, so `entry_order(id, 8, \"B\")` gives it the same display order (and "
          "`entry_letters` the same objection letters) as unsure_right; this is checked for every item. With the first "
          "entry unsure-voice, both logs open with an unsure entry marked right, so C3 there compares 8/8 with 4/8 "
          "overall without a difference in the first line's label. With the first entry certain-voice, perfect_mixed "
          "opens with a certain entry marked right and unsure_right with one marked wrong. Models: the four open-weight "
          "models with arm B perfect_mixed cells.", ""]
    c3 = {}
    for t in POOL:
        if (t, "B") not in raw:
            continue
        cells = raw[(t, "B")]
        its = []
        for i in sorted({i for (i, lg, tn) in cells if (lg, tn) == ("perfect_mixed", "unsure")}):
            a, b = cells.get((i, "perfect_mixed", "unsure")), cells.get((i, "unsure_right", "unsure"))
            if missing(a) or missing(b):
                continue
            if a["x"] != b["x"] or a["own"] != b["own"]:
                raise SystemExit(f"{t} item {i}: own/x differ between perfect_mixed and unsure_right")
            pm, ur = shown("perfect_mixed", i, "B"), shown("unsure_right", i, "B")
            if [e[1] for e in pm] != [e[1] for e in ur] or [e[2] for e in pm] != [e[2] for e in ur]:
                raise SystemExit(f"{t} item {i}: perfect_mixed and unsure_right differ in order or letters")
            fa, fb = int(a["final"] == a["x"]), int(b["final"] == b["x"])
            its.append({"id": i, "model": t, "first": pm[0][1], "pm": fa, "ur": fb, "c3": fa - fb})
        if its:
            c3[t] = its

    def f4(nm, its):
        ec, eu, ea = est(its, first_c, ("c3",)), est(its, first_u, ("c3",)), est(its, None, ("c3",))
        sc, su = [it for it in its if first_c(it)], [it for it in its if first_u(it)]
        return [nm, f"{nn(ec)} / {nn(eu)}", ci(ea, "c3"), ci(ec, "c3"),
                f"{fr(sum(it['pm'] for it in sc), len(sc))} vs {fr(sum(it['ur'] for it in sc), len(sc))}",
                ci(eu, "c3"),
                f"{fr(sum(it['pm'] for it in su), len(su))} vs {fr(sum(it['ur'] for it in su), len(su))}",
                dfmt(diff(its, first_c, first_u, ("c3",)), "c3")]

    c3rows = [f4(name(t), c3[t]) for t in POOL if t in c3]
    if all(t in c3 for t in POOL):
        c3rows.append(f4(POOL_NAME, [it for t in POOL for it in c3[t]]))
    L += table(["model", "n (first c / u)", "C3, all items", "C3, first certain",
                "u\\|PM vs u\\|UR, first certain", "C3, first unsure", "u\\|PM vs u\\|UR, first unsure",
                "C3 diff (certain - unsure)"], c3rows)

    # ---------------- 5. follow-up: raw cell rates behind the first-entry split
    L += ["## 5. Follow-up: cell rates behind the first-entry split (arm B)", "",
          "Same items as 3a (all four core cells non-missing). Flips/n (rate). What the first line says: with the "
          "first entry certain-voice, certain_right opens 'certain, right' and unsure_right opens 'certain, wrong'; "
          "with it unsure-voice, certain_right opens 'unsure, wrong' and unsure_right opens 'unsure, right'.", "",
          "- If switching rises in both voices under whichever log opens with a 'right' line: first certain gives "
          "c|CR > c|UR and u|CR > u|UR; first unsure gives c|UR > c|CR and u|UR > u|CR.",
          "- If the first voice's record is credited only to objections in that voice: first certain gives "
          "c|CR > c|UR with u|CR = u|UR; first unsure gives u|UR > u|CR with c|CR = c|UR.", ""]

    def f5(nm, its):
        out = []
        for lab, sel in (("certain", first_c), ("unsure", first_u)):
            s = [it for it in its if sel(it)]
            n = len(s)
            e = est(s)
            out.append([nm, lab, nn(e)] + [fr(sum(it["f"][c] for it in s), n) for c in ("cCR", "cUR", "uUR", "uCR")]
                       + [ci(e, "dc"), ci(e, "du")])
        return out

    r5 = []
    for t in POOL:
        if (t, "B") in data:
            r5 += f5(name(t), data[(t, "B")])
    pbB = pooled("B")
    if pbB is not None:
        r5 += f5(POOL_NAME, pbB)
    L += table(["model", "first entry", "n", "c\\|CR", "c\\|UR", "u\\|UR", "u\\|CR", "d_c", "d_u"], r5)

    # ---------------- shared helper for pairwise two-cell contrasts (items non-missing in both cells)
    def contrast(cells, tag, a, b):
        its = []
        for i in sorted({i for (i, lg, tn) in cells if (lg, tn) in (a, b)}):
            ra, rb = cells.get((i,) + a), cells.get((i,) + b)
            if missing(ra) or missing(rb):
                continue
            if (ra["own"], ra["x"]) != (rb["own"], rb["x"]):
                raise SystemExit(f"{tag} item {i}: own/x differ between {a} and {b}")
            fa, fb = int(ra["final"] == ra["x"]), int(rb["final"] == rb["x"])
            its.append({"id": i, "model": tag, "a": fa, "b": fb, "d": fa - fb})
        return its

    def cfmt(its):
        n = len(its)
        if not n:
            return ["absent", "-"]
        e = est(its, None, ("d",))
        return [f"{sum(it['a'] for it in its)}/{n} vs {sum(it['b'] for it in its)}/{n}", ci(e, "d")]

    # ---------------- 6. follow-up: dose cells (arm A, segment g2)
    DOSE = ("c4_u2", "c2_u4", "c4_u3", "c3_u4")
    L += ["## 6. Follow-up: dose cells (arm A, answer-only, stratum wrong, target key; segment g2)", "",
          "Pairs of logs with the same overall score but different per-voice records. A reader who uses the record "
          "of the objection's own voice gives positive contrasts; a reader who uses only the overall score gives "
          "about 0. Pairwise items (non-missing in both cells); `__rep2` files ignored (they have no g2 cells).", ""]

    def lab(e):
        return f"Q{e[0]} {e[1]} ({e[2]}) {'right' if e[4] else 'wrong'}"

    lr6 = []
    for lg in DOSE:
        ents = D.LOGS[lg][0]
        c = sum(h for _, v, h in ents if v == "certain")
        u = sum(h for _, v, h in ents if v == "unsure")
        sh = shown(lg, 0, "A")
        lr6.append([lg, f"{c}/4", f"{u}/4", f"{c + u}/8", lab(sh[0]), lab(sh[-1])])
    L += ["Log structure in arm A (fixed order for every item):", ""]
    L += table(["log", "certain voice right", "unsure voice right", "overall", "first displayed entry",
                "last displayed entry"], lr6)
    for la, lb in (("c4_u2", "c2_u4"), ("c4_u3", "c3_u4")):
        sa, sb = shown(la, 0, "A"), shown(lb, 0, "A")
        dif = [f"Q{x[0]} {x[1]}: {'right' if x[4] else 'wrong'} in {la}, {'right' if y[4] else 'wrong'} in {lb}"
               for x, y in zip(sa, sb) if x[4] != y[4]]
        L.append(f"- {la} vs {lb}, entries whose label differs: " + "; ".join(dif) + ".")
    L.append("")

    dose_models = [t for t in tags if (t, "A") in raw
                   and any(lg in DOSE for (_, lg, _) in raw[(t, "A")])]
    no_dose = [name(t) for t in tags if (t, "A") in raw and t not in dose_models]
    L += [f"Models with g2 cells in their arm A file: {', '.join(name(t) for t in dose_models)}. "
          f"Without: {', '.join(no_dose) or 'none'}.", ""]
    U = ((("c2_u4", "unsure"), ("c4_u2", "unsure")), (("c3_u4", "unsure"), ("c4_u3", "unsure")))
    C = ((("c4_u2", "certain"), ("c2_u4", "certain")), (("c4_u3", "certain"), ("c3_u4", "certain")))
    for title, pairs in (("Unsure objection", U), ("Certain objection", C)):
        rows6 = []
        for t in dose_models:
            row = [name(t)]
            for a, b in pairs:
                row += cfmt(contrast(raw[(t, "A")], t, a, b))
            rows6.append(row)
        h = [f"{a[1][0]}\\|{a[0]} - {b[1][0]}\\|{b[0]}" for a, b in pairs]
        L += [f"{title} (flips a vs b, then the paired difference a - b):", ""]
        L += table(["model", f"flips, {h[0]}", h[0], f"flips, {h[1]}", h[1]], rows6)

    # ---------------- 7. follow-up: tone gap without a log, arm B vs arm A
    main_set = [t for t in tags if (t, "B") in meta and meta[(t, "B")]["path"].parent == HARNESS / "runs"]
    L += ["## 7. Follow-up: confident wording without a log (log \"none\")", "",
          "certain|none vs unsure|none, answer-only, stratum wrong, target key; pairwise items. Main-set models "
          "with an arm B file; arm A alongside. 'absent' = the file has no none cells (arm B ran g0 only).", ""]
    rows7 = []
    for t in main_set:
        row = [name(t)]
        for arm in ("B", "A"):
            row += cfmt(contrast(raw[(t, arm)], t, ("none", "certain"), ("none", "unsure")) if (t, arm) in raw
                        else [])
        rows7.append(row)
    L += table(["model", "arm B: certain\\|none vs unsure\\|none", "arm B: difference",
                "arm A: certain\\|none vs unsure\\|none", "arm A: difference"], rows7)

    if warnings:
        L += ["## Warnings", ""] + [f"- {w}" for w in warnings] + [""]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"arm A models: {len([t for t in tags if (t, 'A') in data])}; arm B models used: {len(both)} "
          f"({', '.join(name(t) for t in both)}); arm B skipped (incomplete): "
          f"{', '.join(name(t) + f' {g0}/560' for t, _, g0, _ in skipped) or 'none'}")
    for w in warnings:
        print("warning:", w)


if __name__ == "__main__":
    main()
