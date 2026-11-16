"""Figures and tables for the "Loud or Right?" paper.

Usage (system Python with matplotlib and numpy; no network, no model calls):
    python paper/make_figs.py

Reads harness/analysis/all_final2.json (written by harness/analyze.py --summary); for one heatmap row,
harness_x/runs/test__anthropic_claude-sonnet-5-5__reasoned__A.jsonl; for Fig 1 panel (c), the arm R analysis
harness_x/analysis/arm_r.json; for Table 5, harness_x/analysis/arm_r_vs_a.md. Writes paper/figs/fig1_profiles.png,
fig2_confirmatory.png, fig3_right_stratum.png (300 dpi, white background, 16 cm wide) and paper/figs/tables.md.
It also checks C1-C4 and the right-stratum counts against harness/analysis/summary__all_final2.md.

Model class, short name and order come only from the MODELS table below. The JSON's `tier` and `status` fields
are not used: `tier` tags Claude Sonnet 5.5's deliberative file as "recency" (it is a main-set model), and
`status` prints "confirmatory" for the four recency-tier models, which are exploratory.
"""
import json
import math
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.transforms import blended_transform_factory  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "harness" / "analysis" / "all_final2.json"
SUMMARY_MD = ROOT / "harness" / "analysis" / "summary__all_final2.md"
SONNET_DELIB = ROOT / "harness_x" / "runs" / "test__anthropic_claude-sonnet-5-5__reasoned__A.jsonl"
ARM_R = ROOT / "harness_x" / "analysis" / "arm_r.json"
ARM_R_VS_A = ROOT / "harness_x" / "analysis" / "arm_r_vs_a.md"
ALL_FINAL3 = ROOT / "harness" / "analysis" / "all_final3.json"
ARM_S_JSON = ROOT / "harness_x" / "analysis" / "arm_s.json"
SONNET_INSTANT_A = ROOT / "harness" / "runs" / "test__anthropic_claude-sonnet-5-5__instant__A.jsonl"
ARM_S_TAGS = {"gemma4:12b": "gemma4_12b", "ministral-3:8b": "ministral-3_8b",
              "openrouter:meta-llama/llama-3.3-70b-instruct": "openrouter_meta-llama_llama-3.3-70b-instruct",
              "openrouter:meta-llama/llama-4-maverick": "openrouter_meta-llama_llama-4-maverick",
              "openai:gpt-6-sol": "openai_gpt-6-sol"}
N_WRONG_ITEMS = 80
X_FINAL = ROOT / "harness_x" / "analysis" / "x_final.json"
ARM_S_MD = ROOT / "harness_x" / "analysis" / "arm_s.md"
# Run folders scanned for raw files (arm S, arm R discovery, arm B fallback). refresh_v2.py can point these
# elsewhere for testing.
RUNS_MAIN = ROOT / "harness" / "runs"
RUNS_X = ROOT / "harness_x" / "runs"
OUT = ROOT / "paper" / "figs"

DPI = 300
PAGE_W = 6.3  # inches, about 16 cm usable width
PT = DPI / 72.0  # pixels per point at the output resolution

# (model id, short name, class) in display order. Classes: open = open-weight main set, closed = closed main set,
# recency = recency tier (exploratory, open-weight).
MODELS = [
    ("gemma4:12b", "Gemma 4 12B", "open"),
    ("ministral-3:8b", "Ministral 3 8B", "open"),
    ("qwen3.5:9b", "Qwen 3.5 9B", "open"),
    ("openrouter:mistralai/ministral-14b-2512", "Ministral 14B", "open"),
    ("openrouter:meta-llama/llama-3.3-70b-instruct", "Llama 3.3 70B", "open"),
    ("openrouter:deepseek/deepseek-v3.2", "DeepSeek V3.2", "open"),
    ("openai:gpt-6-luna", "GPT-6 Luna", "closed"),
    ("openai:gpt-6-sol", "GPT-6 Sol", "closed"),
    ("anthropic:claude-haiku-5-5", "Claude Haiku 5.5", "closed"),
    ("anthropic:claude-sonnet-5-5", "Claude Sonnet 5.5", "closed"),
    ("google:gemini-3.6-flash", "Gemini 3.6 Flash", "closed"),
    ("deepseek:deepseek-v4.1-flash-1017", "DeepSeek V4.1 Flash", "recency"),
    ("openrouter:qwen/qwen3.8-27b", "Qwen 3.8 27B", "recency"),
    ("openrouter:meta-llama/llama-4-maverick", "Llama 4 Maverick", "recency"),
    ("openrouter:mistralai/mistral-medium-3-5", "Mistral Medium 3.5", "recency"),
]
SHORT = {m: s for m, s, _ in MODELS}
CLASS = {m: c for m, _, c in MODELS}
CLASSES = ("open", "closed", "recency")
BLOCK_TITLE = {"open": "Open-weight", "closed": "Closed", "recency": "Recency tier (exploratory)"}

# Colour-blind-safe categorical slots 1-3 of the reference palette (validated all-pairs on white: worst CVD
# delta E 9.2, normal-vision 24.0). Aqua is below 3:1 contrast on white, so every point also carries a shape and
# a direct text label.
STYLE = {
    "open": dict(color="#2a78d6", edge="#1c5cab", marker="o", label="Open-weight, main set"),
    "closed": dict(color="#eb6834", edge="#b9481c", marker="s", label="Closed, main set"),
    "recency": dict(color="#1baf7a", edge="#12825a", marker="^", label="Recency tier (exploratory, open-weight)"),
}
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
REF = "#b5b3ab"
DELIB_GREY = "#7d7b76"
DELIB_GREY_LIGHT = "#b9b7b0"
BLUE_RAMP = ["#f3f7fd", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

plt.rcParams.update({
    "font.family": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 8,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.edgecolor": "#8a8882",
    "axes.linewidth": 0.6,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "axes.labelcolor": INK,
    "text.color": INK,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "mathtext.default": "it",
})


# ------------------------------------------------------------------ data access

def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def group(d, model, mode, arm, stratum, target):
    return d["groups"].get("|".join((model, mode, arm, stratum, target)))


def by_voice(d, model, arm):
    g = group(d, model, "instant", arm, "wrong", "key")
    if not g:
        return None
    bv = g["contrasts"]["all"]["by_voice_main"]
    return {s: bv[s] for s in ("d_c", "d_u")}


def confirm_rows(d, model, mode):
    for blk in d["confirmatory"]:
        if blk["model"] == model and blk["mode"] == mode:
            return {r["id"]: r for r in blk["rows"]}
    return None


def sonnet_deliberative_right():
    """Cell counts for Claude Sonnet 5.5, deliberative, arm A, stratum right, computed from the raw file with the
    analysis rules: a trial is missing if error is non-empty, final == "?", done == "length" or trunc_risk is true;
    flip = final == x; duplicates of (id, log, tone, rep): the last row without an error wins."""
    cells = {}
    for line in SONNET_DELIB.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("stratum") != "right":
            continue
        key = (r["id"], r["log"], r["tone"], r.get("rep") or 1)
        prev = cells.get(key)
        if prev is not None and r.get("error") and not prev.get("error"):
            continue
        cells[key] = r
    out = {}
    for (i, lg, t, rep), r in cells.items():
        missing = bool(r.get("error")) or r.get("final") == "?" or r.get("done") == "length" or r.get("trunc_risk") is True
        rec = out.setdefault((lg, t), {"items": {}})
        if not missing:
            rec["items"].setdefault(i, []).append(1.0 if r["final"] == r["x"] else 0.0)
        else:
            rec["items"].setdefault(i, [])
    res = {}
    for c, rec in out.items():
        vals = [sum(v) / len(v) for v in rec["items"].values() if v]
        res[c] = {"flips": sum(vals), "n": len(vals)}
    return res


def _missing(r):
    return bool(r.get("error")) or r.get("final") == "?" or r.get("done") == "length" or r.get("trunc_risk") is True


_ANALYZE = None


def _analyze():
    """harness/analyze.py, imported read-only without writing a __pycache__."""
    global _ANALYZE
    if _ANALYZE is None:
        sys.dont_write_bytecode = True
        if str(ROOT / "harness") not in sys.path:
            sys.path.insert(0, str(ROOT / "harness"))
        import analyze  # noqa: E402
        _ANALYZE = analyze
    return _ANALYZE


def run_tag(model):
    return model.replace(":", "_").replace("/", "_")


def raw_by_voice(path, model, arm):
    """d_c, d_u and D for (model, answer-only, arm, stratum wrong, target key) from one raw run file, computed with
    harness/analyze.py's own functions (strict missing rule, by-voice population, same bootstrap and seed), so the
    numbers equal what analyze.py would write. Used only when all 80 items have the no-log control and the four core
    cells. Returns (stats or None, note)."""
    an = _analyze()
    warn = []
    groups = an.build_groups(an.load_rows([str(path)], warn), warn)
    G = groups.get((model, "instant", arm, "wrong", "key"))
    if not G:
        return None, "no rows"
    view = an.View(G["cells"], "strict")
    run_cells = {k[1:] for k in G["cells"]}
    bv = an.by_voice(view, view.ids, "", "primary", None, run_cells)
    if bv["d_c"]["n"] != N_WRONG_ITEMS or an.CONTROL not in run_cells:
        rows = sum(len(v) for v in G["cells"].values())
        return None, f"{rows} rows, by-voice n = {bv['d_c']['n']}"
    return {k: bv[k] for k in ("d_c", "d_u", "D")}, "raw"


def _frozen(d_json, model, arm):
    g = group(d_json, model, "instant", arm, "wrong", "key") if d_json else None
    if not g:
        return None
    bv = g["contrasts"]["all"]["by_voice_main"]
    return {k: bv[k] for k in ("d_c", "d_u", "D")}


def arm_s():
    """Arm S per model: from harness_x/analysis/arm_s.json when it exists, otherwise from the raw run files.
    Returns ({model: {"d_c", "d_u", "D"}}, source, {model: note})."""
    out, pending = {}, {}
    if ARM_S_JSON.exists():
        ds = json.loads(ARM_S_JSON.read_text(encoding="utf-8"))
        for m in ARM_S_TAGS:
            g = group(ds, m, "instant", "S", "wrong", "key")
            if g:
                bv = g["contrasts"]["all"]["by_voice_main"]
                if bv["d_c"]["n"] == N_WRONG_ITEMS:
                    out[m] = {k: bv[k] for k in ("d_c", "d_u", "D")}
                    continue
                pending[m] = f"n = {bv['d_c']['n']}"
            else:
                pending[m] = "not in arm_s.json"
        return out, "harness_x/analysis/arm_s.json", pending
    for m, tag in ARM_S_TAGS.items():
        f = RUNS_X / f"test__{tag}__instant__S.jsonl"
        if not f.exists():
            pending[m] = "file absent"
            continue
        st, note = raw_by_voice(f, m, "S")
        if st:
            out[m] = st
        else:
            pending[m] = note
    return out, "raw run files (harness/analyze.py functions)", pending


def arm_b(jsons_by_class):
    """Arm B per model. Frozen analysis output first (jsons_by_class: {class: [json, ...]} tried in order); a model
    with no arm B group there is computed from test__<tag>__instant__B.jsonl in the run folders when that file
    exists (e.g. Gemini 3.6 Flash). Returns ({model: stats}, {model: note}, {model: "frozen" | "raw"})."""
    out, pending, src = {}, {}, {}
    for m, _, cls in MODELS:
        st = None
        for dj in jsons_by_class.get(cls, []):
            st = _frozen(dj, m, "B")
            if st:
                break
        if st:
            out[m], src[m] = st, "frozen"
            continue
        for folder in (RUNS_MAIN, RUNS_X):
            f = folder / f"test__{run_tag(m)}__instant__B.jsonl"
            if f.exists():
                st, note = raw_by_voice(f, m, "B")
                if st:
                    out[m], src[m] = st, "raw"
                else:
                    pending[m] = note
                break
    return out, pending, src


def arm_r(d_r):
    """Arm R per model, for every harness_x/runs/test__*__instant__R.jsonl that exists: the frozen arm_r.json group
    when it has one, otherwise computed from the raw file. Returns ({model: stats}, {model: note}, {model: src})."""
    out, pending, src = {}, {}, {}
    for f in sorted(RUNS_X.glob("test__*__instant__R.jsonl")):
        first = next((ln for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()), None)
        if not first:
            continue
        m = json.loads(first).get("model")
        if m not in SHORT:
            print(f"  WARNING arm R: {f.name} has unknown model {m!r}; skipped")
            continue
        st = _frozen(d_r, m, "R")
        if st:
            out[m], src[m] = st, "frozen"
            continue
        st, note = raw_by_voice(f, m, "R")
        if st:
            out[m], src[m] = st, "raw"
        else:
            pending[m] = note
    return out, pending, src


CORE4 = (("certain_right", "certain"), ("unsure_right", "certain"), ("unsure_right", "unsure"),
         ("certain_right", "unsure"))


def _cell_counts(path, stratum, ids=None, mode=None):
    """{(log, tone): (flips, n)} over the given items (strict missing rule; duplicates: last error-free row wins)."""
    rows = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("stratum") != stratum or (mode and r.get("mode") != mode) or (ids is not None and r["id"] not in ids):
            continue
        if (r.get("target") or ("distractor" if stratum == "right" else "key")) != "key" and stratum == "wrong":
            continue
        key = (r["id"], r["log"], r["tone"], r.get("rep") or 1)
        prev = rows.get(key)
        if prev is not None and r.get("error") and not prev.get("error"):
            continue
        rows[key] = r
    per = {}
    for (i, lg, t, rep_), r in rows.items():
        per.setdefault((lg, t), {}).setdefault(i, [])
        if not _missing(r):
            per[(lg, t)][i].append(1.0 if r["final"] == r["x"] else 0.0)
    out = {}
    for c, items in per.items():
        vals = [sum(v) / len(v) for v in items.values() if v]
        out[c] = (sum(vals), len(vals))
    return out


def o7_counts():
    """Sonnet, model-was-wrong items: brief reasoning (O7, reasoned file, stratum wrong) and answer-only arm A on the
    same item ids. Returns (ids, {cell: (flips, n)} reasoning, {cell: (flips, n)} answer-only)."""
    ids = set()
    for line in SONNET_DELIB.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            if r.get("stratum") == "wrong":
                ids.add(r["id"])
    reas = _cell_counts(SONNET_DELIB, "wrong", ids, mode="reasoned")
    inst = _cell_counts(SONNET_INSTANT_A, "wrong", ids, mode="instant")
    return ids, reas, inst


# ------------------------------------------------------------------ formatting

def f2(v):
    """Two decimals, halves rounded away from zero (estimates are often multiples of 1/80, e.g. 0.475 -> 0.48)."""
    q = Decimal(repr(round(v, 9))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    s = f"{q:.2f}"
    return "0.00" if s == "-0.00" else s


def fci(ci):
    return f"[{f2(ci[0])}, {f2(ci[1])}]" if ci else "-"


def fp(p):
    if p is None:
        return "-"
    if p < 0.001:
        return "<0.001"
    if p < 0.01:
        return f"{p:.3f}"
    return f"{p:.2f}"


# ------------------------------------------------------------------ geometry helpers for label placement

def _expand(r, m):
    return (r[0] - m, r[1] - m, r[2] + m, r[3] + m)


def _overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if (w > 0 and h > 0) else 0.0


def _orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _seg_x(p1, p2, p3, p4):
    d1, d2 = _orient(p3, p4, p1), _orient(p3, p4, p2)
    d3, d4 = _orient(p1, p2, p3), _orient(p1, p2, p4)
    return d1 * d2 < 0 and d3 * d4 < 0


def _inside(p, r):
    return r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3]


def _seg_rect(p, q, r):
    if _inside(p, r) or _inside(q, r):
        return True
    c = [(r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])]
    return any(_seg_x(p, q, c[k], c[(k + 1) % 4]) for k in range(4))


def _nearest(p, r):
    return (min(max(p[0], r[0]), r[2]), min(max(p[1], r[1]), r[3]))


def _pt_seg_dist(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    L2 = vx * vx + vy * vy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L2))
    return math.hypot(p[0] - (a[0] + t * vx), p[1] - (a[1] + t * vy))


def _shrink(p, q, d):
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    if L <= d:
        return q
    return (p[0] + (q[0] - p[0]) * d / L, p[1] + (q[1] - p[1]) * d / L)


RADII_PT = (2.5, 5, 8, 12, 17, 23, 30, 38, 47, 57, 68)
N_ANGLES = 24
LABEL_PAD = 0.12
LEN_W = 3.0  # cost per pixel of leader length
RUN_W = 300.0  # cost per point of leader running along another line
TWO_LINE_COST = 120.0  # mild preference for one-line labels
AXIS_ALIGNED_COST = 1500.0  # leaders within ~11 degrees of horizontal/vertical run along bars and zero lines


def _run_len(seg, other, tol):
    """Approximate length (px) of `seg` that runs within `tol` of segment `other` (collinear running)."""
    (ax_, ay), (bx, by) = seg
    k = 17
    hits = sum(_pt_seg_dist((ax_ + (bx - ax_) * t / (k - 1), ay + (by - ay) * t / (k - 1)), other[0], other[1]) < tol
               for t in range(k))
    return hits / k * math.hypot(bx - ax_, by - ay)


def _run_cost(seg, other, tol):
    r = _run_len(seg, other, tol)
    return 0.0 if r < 3 * PT else RUN_W * r / PT


def two_line(name):
    """Split a long name at the space nearest its middle, or return None."""
    if len(name) < 14 or " " not in name:
        return None
    spaces = [k for k, ch in enumerate(name) if ch == " "]
    k = min(spaces, key=lambda j: abs(j - len(name) / 2))
    return name[:k] + "\n" + name[k + 1:]


def place_labels(fig, ax, pts, names, errbars, refsegs, marker_r_pt, fontsize=8, leader_min_pt=6.0, restarts=4,
                 fixed=None):
    """Place one text label per point inside `ax` (display pixels): greedy start, then coordinate descent, over
    several start orders; the lowest total cost wins.

    Penalises overlap with every marker, every error bar, other labels and the axes edge; leaders that cross
    labels, other leaders or other markers, run along a bar, reference line or other leader, or are axis-aligned;
    and leader length. Reference lines are masked by the label's white box, so crossing them costs little.
    Long names may be set on two lines. Returns per label (rect_px, leader or None, text, side, cost)."""
    renderer = fig.canvas.get_renderer()
    P = [tuple(ax.transData.transform(p)) for p in pts]
    n = len(P)
    pad = LABEL_PAD * fontsize * PT  # the white box around each label (boxstyle pad is in font-size units)
    variants = []
    for nm in names:
        vs = []
        for txt, extra in ((nm, 0.0), (two_line(nm), TWO_LINE_COST)):
            if txt is None:
                continue
            t = ax.text(0, 0, txt, fontsize=fontsize, linespacing=1.05)
            bb = t.get_window_extent(renderer)
            t.remove()
            vs.append((txt, extra, bb.width + 2 * pad, bb.height + 2 * pad))
        variants.append(vs)
    axb = ax.get_window_extent(renderer)
    axrect = (axb.x0 + 2 * PT, axb.y0 + 2 * PT, axb.x1 - 2 * PT, axb.y1 - 2 * PT)
    mr = marker_r_pt * PT
    mboxes = [(x - mr, y - mr, x + mr, y + mr) for x, y in P]
    half = 0.9 * PT
    eb_rects, eb_segs = [], []
    for (x0, y0), (x1, y1) in errbars:
        a, b = ax.transData.transform((x0, y0)), ax.transData.transform((x1, y1))
        eb_rects.append((min(a[0], b[0]) - half, min(a[1], b[1]) - half, max(a[0], b[0]) + half, max(a[1], b[1]) + half))
        eb_segs.append((tuple(a), tuple(b)))
    ref_px = [(tuple(ax.transData.transform(a)), tuple(ax.transData.transform(b))) for a, b in refsegs]
    margin = 1.2 * PT
    lmin = leader_min_pt * PT

    def leader(i, r):
        q = _nearest(P[i], r)
        if math.hypot(q[0] - P[i][0], q[1] - P[i][1]) < lmin + mr:
            return None
        return (_shrink(P[i], q, mr + 0.8 * PT), q)

    def static(i, r, ld, extra):
        """Cost of a candidate that does not depend on the other labels (None if it leaves the axes)."""
        px, py = P[i]
        R = _expand(r, margin)
        if R[0] < axrect[0] or R[1] < axrect[1] or R[2] > axrect[2] or R[3] > axrect[3]:
            return None
        st = extra
        for mb in mboxes:
            ov = _overlap(R, mb)
            if ov:
                st += 5e4 + 10 * ov
        for eb in eb_rects:
            ov = _overlap(R, eb)
            if ov:
                st += 2e4 + 10 * ov
        for a, b in ref_px:
            if _seg_rect(a, b, R):
                st += 40
        if ld is not None:
            dx, dy = ld[1][0] - ld[0][0], ld[1][1] - ld[0][1]
            L = math.hypot(dx, dy) or 1.0
            st += LEN_W * L
            if abs(dx) / L < 0.2 or abs(dy) / L < 0.2:
                st += AXIS_ALIGNED_COST
            for k2 in range(n):
                if k2 != i and _pt_seg_dist(P[k2], ld[0], ld[1]) < mr + 1.0 * PT:
                    st += 1e4
            for seg in eb_segs:
                if _seg_x(ld[0], ld[1], seg[0], seg[1]):
                    st += 250
                st += _run_cost(ld, seg, 2.0 * PT)
            for seg in ref_px:
                st += _run_cost(ld, seg, 2.0 * PT)
        else:
            q = _nearest((px, py), r)
            st += LEN_W * math.hypot(q[0] - px, q[1] - py)
        return st

    # candidates: (rect, leader, text, side, static cost)
    fixed = fixed or {}
    cands = []
    for i, (px, py) in enumerate(P):
        cs = []
        if names[i] in fixed:
            f = fixed[names[i]]
            txt = f.get("text", names[i])
            t = ax.text(0, 0, txt, fontsize=fontsize, linespacing=1.05)
            bb = t.get_window_extent(renderer)
            t.remove()
            w, h = bb.width + 2 * pad, bb.height + 2 * pad
            axx, ayy = ax.transData.transform(f["xy"])
            x0 = {"left": axx, "right": axx - w, "center": axx - w / 2}[f["ha"]]
            y0 = {"bottom": ayy, "top": ayy - h, "center": ayy - h / 2}[f["va"]]
            r = (x0, y0, x0 + w, y0 + h)
            if f.get("leader", True) is False:
                ld = None
            elif "attach" in f:
                q = tuple(ax.transData.transform(f["attach"]))
                ld = (_shrink(P[i], q, mr + 0.8 * PT), q)
            else:
                ld = leader(i, r)
            side = {"left": "left", "right": "right"}.get(f["ha"], "center")
            st = static(i, r, ld, 0.0)
            cs.append((r, ld, txt, side, 1e12 if st is None else st))
            cands.append(cs)
            continue
        for txt, extra, w, h in variants[i]:
            for rho_pt in RADII_PT:
                rho = rho_pt * PT + mr
                for k in range(N_ANGLES):
                    th = 2 * math.pi * k / N_ANGLES
                    c, s_ = math.cos(th), math.sin(th)
                    axx, ayy = px + rho * c, py + rho * s_
                    side = "left" if c > 0.35 else ("right" if c < -0.35 else "center")
                    x0 = axx if side == "left" else (axx - w if side == "right" else axx - w / 2)
                    y0 = ayy if s_ > 0.35 else (ayy - h if s_ < -0.35 else ayy - h / 2)
                    r = (x0, y0, x0 + w, y0 + h)
                    ld = leader(i, r)
                    st = static(i, r, ld, extra)
                    if st is not None:
                        cs.append((r, ld, txt, side, st))
        cands.append(cs)

    def cost(i, cand, state):
        r, ld, _, _, c = cand
        R = _expand(r, margin)
        for j in range(n):
            if j == i or state[j] is None:
                continue
            rj, lj = state[j][0], state[j][1]
            if _overlap(R, _expand(rj, margin)):
                c += 2e5
            if lj is not None and _seg_rect(lj[0], lj[1], R):
                c += 3e4
            if ld is not None:
                if _seg_rect(ld[0], ld[1], rj):
                    c += 3e4
                if lj is not None:
                    if _seg_x(ld[0], ld[1], lj[0], lj[1]):
                        c += 1e4
                    c += _run_cost(ld, lj, 2.5 * PT)
        return c

    crowd = [sum(1 for j in range(n) if j != i and math.hypot(P[i][0] - P[j][0], P[i][1] - P[j][1]) < 60 * PT)
             for i in range(n)]
    orders = [sorted(range(n), key=lambda i: -crowd[i]), sorted(range(n), key=lambda i: crowd[i]),
              sorted(range(n), key=lambda i: P[i][0]), sorted(range(n), key=lambda i: -P[i][1])][:restarts]
    best_state, best_total = None, float("inf")
    for order in orders:
        state = [None] * n
        for i in order:
            state[i] = min(cands[i], key=lambda cd: cost(i, cd, state))
        for _ in range(30):
            changed = False
            for i in order:
                cur = state[i]
                state[i] = None
                state[i] = min(cands[i], key=lambda cd: cost(i, cd, state))
                if state[i] is not cur:
                    changed = True
            if not changed:
                break
        total = sum(cost(i, state[i], state) for i in range(n))
        if total < best_total:
            best_state, best_total = list(state), total
    for i in range(n):
        c = cost(i, best_state[i], best_state)
        if c >= 1e12:
            c -= 1e12  # hand-set label within the edge margin
        if c > 3000:
            print(f"    label '{names[i]}' cost {c:.0f}")
    return best_state, best_total


def draw_labels(ax, state, fontsize=8):
    inv = ax.transData.inverted()
    pad = LABEL_PAD * fontsize * PT
    texts = []
    for r, ld, txt, side, _ in state:
        x, y = inv.transform((r[0] + pad, r[1] + pad))
        t = ax.text(x, y, txt, fontsize=fontsize, ha="left", va="bottom", color=INK, zorder=2.45, linespacing=1.05,
                    multialignment={"left": "left", "right": "right"}.get(side, "center"),
                    bbox=dict(boxstyle=f"square,pad={LABEL_PAD}", fc="white", ec="none", alpha=0.9))
        texts.append(t)
        if ld is not None:
            a, b = inv.transform(ld[0]), inv.transform(ld[1])
            ax.plot([a[0], b[0]], [a[1], b[1]], color=MUTED, lw=0.5, zorder=2.4, solid_capstyle="butt")
    return texts


def check_overlaps(fig, ax, texts, pts, marker_r_pt, errbars, tag):
    """Report text-text, text-marker and text-error-bar overlaps in the rendered figure."""
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    boxes = [t.get_window_extent(rend) for t in texts]
    P = [ax.transData.transform(p) for p in pts]
    mr = marker_r_pt * PT
    axb = ax.get_window_extent(rend)
    issues = []
    for i, a in enumerate(boxes):
        ra = (a.x0, a.y0, a.x1, a.y1)
        if ra[0] < axb.x0 or ra[2] > axb.x1 or ra[1] < axb.y0 or ra[3] > axb.y1:
            issues.append(f"{tag}: label '{texts[i].get_text()}' leaves the axes")
        for j in range(i + 1, len(boxes)):
            b = boxes[j]
            if _overlap(ra, (b.x0, b.y0, b.x1, b.y1)):
                issues.append(f"{tag}: '{texts[i].get_text()}' overlaps '{texts[j].get_text()}'")
        for k, p in enumerate(P):
            if _overlap(ra, (p[0] - mr, p[1] - mr, p[0] + mr, p[1] + mr)):
                issues.append(f"{tag}: '{texts[i].get_text()}' overlaps a marker (point {k})")
        for (x0, y0), (x1, y1) in errbars:
            p0, p1 = ax.transData.transform((x0, y0)), ax.transData.transform((x1, y1))
            if _seg_rect(tuple(p0), tuple(p1), ra):
                issues.append(f"{tag}: '{texts[i].get_text()}' overlaps an error bar")
    return issues


# ------------------------------------------------------------------ figure 1

# Hand-set label positions for the crowded region near the origin (data coordinates of the label box anchor; the
# placer arranges every other label around these). "attach" sets where the leader meets the label.
FIG1_FIXED = {
    "A": {
        "GPT-6 Luna": dict(text="GPT-6\nLuna", xy=(-0.05, 0.10), ha="right", va="bottom"),
        "Qwen 3.8 27B": dict(text="Qwen 3.8\n27B", xy=(-0.03, 0.02), ha="right", va="center"),
        "Qwen 3.5 9B": dict(xy=(0.03, 0.235), ha="right", va="bottom"),
        "Claude Haiku 5.5": dict(text="Claude\nHaiku 5.5", xy=(-0.28, -0.28), ha="left", va="bottom",
                                 attach=(-0.06, -0.175)),
        "DeepSeek V3.2": dict(text="DeepSeek\nV3.2", xy=(-0.005, -0.28), ha="left", va="bottom"),
        "Ministral 3 8B": dict(xy=(0.27, -0.19), ha="left", va="top", leader=False),
        "Ministral 14B": dict(text="Ministral\n14B", xy=(0.13, 0.09), ha="left", va="bottom"),
        "DeepSeek V4.1 Flash": dict(text="DeepSeek\nV4.1 Flash", xy=(0.72, 0.13), ha="left", va="bottom"),
    },
    "B": {
        "Ministral 14B": dict(text="Ministral\n14B", xy=(-0.28, -0.08), ha="left", va="top",
                              attach=(-0.15, -0.08)),
        "DeepSeek V3.2": dict(xy=(0.08, -0.152), ha="left", va="top"),
        "Claude Haiku 5.5": dict(xy=(0.05, -0.228), ha="left", va="top"),
        "Ministral 3 8B": dict(xy=(0.21, -0.076), ha="left", va="top"),
        "Qwen 3.5 9B": dict(text="Qwen 3.5\n9B", xy=(-0.06, 0.14), ha="right", va="bottom"),
        "GPT-6 Luna": dict(text="GPT-6\nLuna", xy=(-0.04, 0.30), ha="right", va="bottom"),
        "Gemma 4 12B": dict(xy=(0.30, 0.0), ha="left", va="top"),
        "Llama 3.3 70B": dict(xy=(0.35, 0.045), ha="left", va="center"),
        "Mistral Medium 3.5": dict(text="Mistral\nMedium 3.5", xy=(0.14, 0.27), ha="left", va="bottom",
                                   attach=(0.25, 0.27)),
    },
    "R": {},
    "S": {
        "Llama 3.3 70B": dict(xy=(0.20, 0.21), ha="right", va="bottom"),
    },
}
FIG1_LIM = (-0.30, 1.0)  # arm R puts Ministral 3 8B's d_c interval below -0.25, so every panel starts at -0.30
FIG1_PANELS = (("A", "(a) Arm A, main form"), ("B", "(b) Arm B, second form"),
               ("R", "(c) Arm R, reversed order"), ("S", "(d) Arm S, order-randomised"))
FIG1_GRID = {"A": (0, 0), "B": (0, 1), "R": (1, 0), "S": (1, 1)}  # (row, column)


def fig1(d, panel_stats):
    """panel_stats: {arm: ({model: stats}, {model: pending note})}; arm A is read from d."""
    lim = FIG1_LIM
    left, gap, right = 0.58, 0.22, 0.10
    bottom, vgap, top = 1.02, 0.80, 0.27
    pw = (PAGE_W - left - gap - right) / 2
    ph = 3.0
    fw, fh = PAGE_W, bottom + 2 * ph + vgap + top
    fig = plt.figure(figsize=(fw, fh), dpi=DPI)
    panels = []
    for arm, title in FIG1_PANELS:
        row, col = FIG1_GRID[arm]
        ax = fig.add_axes([(left + col * (pw + gap)) / fw, (bottom + (1 - row) * (ph + vgap)) / fh, pw / fw, ph / fh])
        vals, pend = panel_stats.get(arm, ({}, {}))
        recs = []
        for m, s_, cls in MODELS:
            bv = by_voice(d, m, arm) if arm == "A" else vals.get(m)
            if bv:
                recs.append((m, s_, cls, bv["d_c"], bv["d_u"]))
        ax.set_xlim(*lim)
        ax.set_ylim(*lim)
        ticks = [-0.25, 0, 0.25, 0.5, 0.75, 1.0]
        tlabels = ["-0.25", "0", "0.25", "0.5", "0.75", "1"]
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xticklabels(tlabels)
        ax.set_yticklabels(tlabels)
        ax.axhline(0, color=REF, lw=0.6, zorder=1)
        ax.axvline(0, color=REF, lw=0.6, zorder=1)
        ax.plot(lim, lim, color=REF, lw=0.8, ls=(0, (4, 3)), zorder=1)
        if pend:
            ax.set_title(f"{title} ({len(recs)} of {len(recs) + len(pend)} models)", loc="left", pad=4)
            ax.text(0.03, 0.97, "pending: " + ", ".join(SHORT[m] for m in pend), transform=ax.transAxes,
                    ha="left", va="top", fontsize=8, color=INK2, zorder=2.45,
                    bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
        else:
            ax.set_title(f"{title} ({len(recs)} models)", loc="left", pad=4)
        ax.set_xlabel(r"$d_c$  (certain objection)")
        if col == 1:
            ax.tick_params(labelleft=False)
        else:
            ax.set_ylabel(r"$d_u$  (unsure objection)")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        pts, errbars = [], []
        for m, s_, cls, dc, du in recs:
            st = STYLE[cls]
            x, y = dc["diff"], du["diff"]
            ax.plot([dc["ci95"][0], dc["ci95"][1]], [y, y], color=st["color"], lw=0.8, alpha=0.6, zorder=3,
                    solid_capstyle="butt")
            ax.plot([x, x], [du["ci95"][0], du["ci95"][1]], color=st["color"], lw=0.8, alpha=0.6, zorder=3,
                    solid_capstyle="butt")
            ax.plot([x], [y], marker=st["marker"], ms=5.2 if st["marker"] != "^" else 5.8, mfc=st["color"],
                    mec=st["edge"], mew=0.6, ls="none", zorder=4)
            pts.append((x, y))
            errbars += [((dc["ci95"][0], y), (dc["ci95"][1], y)), ((x, du["ci95"][0]), (x, du["ci95"][1]))]
            if min(dc["ci95"][0], du["ci95"][0]) < lim[0] or max(dc["ci95"][1], du["ci95"][1]) > lim[1]:
                print(f"  WARNING fig1 arm {arm}: {s_} interval leaves the axes")
        panels.append((arm, ax, recs, pts, errbars))

    issues = []
    fig.canvas.draw()
    refsegs = [((lim[0], 0), (lim[1], 0)), ((0, lim[0]), (0, lim[1])), ((lim[0], lim[0]), (lim[1], lim[1]))]
    for arm, ax, recs, pts, errbars in panels:
        if not recs:
            continue
        names = [r[1] for r in recs]
        state, total = place_labels(fig, ax, pts, names, errbars, refsegs, marker_r_pt=3.0,
                                    fixed=FIG1_FIXED.get(arm, {}))
        print(f"  label cost arm {arm}: {total:.0f}")
        texts = draw_labels(ax, state)
        issues += check_overlaps(fig, ax, texts, pts, 2.6, errbars, f"fig1 arm {arm}")

    handles = [Line2D([], [], marker=STYLE[c]["marker"], ls="none", mfc=STYLE[c]["color"], mec=STYLE[c]["edge"],
                      mew=0.6, ms=6, label=STYLE[c]["label"]) for c in CLASSES]
    handles.append(Line2D([], [], color=STYLE["open"]["color"], alpha=0.6, lw=0.8, label="95% interval on each axis"))
    handles.append(Line2D([], [], color=REF, lw=0.8, ls=(0, (4, 3)), label="y = x"))
    handles.append(Line2D([], [], color=REF, lw=0.6, label="zero"))
    order = [0, 3, 1, 4, 2, 5]  # column-major fill: row 1 = classes, row 2 = reference marks
    fig.legend(handles=[handles[k] for k in order], loc="lower center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, 0.0), handletextpad=0.5, columnspacing=1.6, borderaxespad=0.3,
               labelspacing=0.6)
    path = OUT / "fig1_profiles.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path, issues


# ------------------------------------------------------------------ figure 2

C_TITLES = {"C1": "C1:  $d_c$", "C2": r"C2:  $d_c - d_u$", "C3": "C3:  spillover\nonto unsure voice",
            "C4": "C4:  $d_c$, wrong\noption named"}


def fig2(d):
    rows = []  # (y, kind, payload)
    y = 0.0
    for cls in CLASSES:
        rows.append((y, "header", BLOCK_TITLE[cls]))
        y += 0.85
        for m, s, c in MODELS:
            if c == cls:
                rows.append((y, "model", m))
                y += 1.0
        y += 0.35
    ymax = y - 0.35
    vals = []
    for _, k, m in rows:
        if k != "model":
            continue
        for mode in ("instant", "reasoned"):
            cr = confirm_rows(d, m, mode)
            if cr:
                for cid in ("C1", "C2", "C3", "C4"):
                    if cr[cid]["ci95"]:
                        vals += cr[cid]["ci95"]
    xlo = min(-0.25, math.floor(min(vals) * 20) / 20 - 0.02)
    xhi = max(1.0, math.ceil(max(vals) * 20) / 20)
    left, right, bottom, top = 1.30, 0.08, 0.86, 0.48
    gap = 0.10
    row_h = 0.205
    ph = ymax * row_h + 0.1
    fw, fh = PAGE_W, bottom + ph + top
    pw = (fw - left - right - 3 * gap) / 4
    fig = plt.figure(figsize=(fw, fh), dpi=DPI)
    axes = []
    for k in range(4):
        axes.append(fig.add_axes([(left + k * (pw + gap)) / fw, bottom / fh, pw / fw, ph / fh]))
    model_rows = [(yy, m) for yy, k, m in rows if k == "model"]
    for k, (ax, cid) in enumerate(zip(axes, ("C1", "C2", "C3", "C4"))):
        ax.set_xlim(xlo, xhi)
        ax.set_ylim(ymax + 0.1, -0.6)
        ax.axvline(0, color=REF, lw=0.7, zorder=1)
        for yy, kind, _ in rows:
            if kind == "header" and yy > 0:
                ax.axhline(yy - 0.45, color="#e1e0d9", lw=0.6, zorder=0)
        for yy, m in model_rows:
            st = STYLE[CLASS[m]]
            cr = confirm_rows(d, m, "instant")
            r = cr[cid] if cr else None
            if r and r["n"]:
                ax.plot(r["ci95"], [yy, yy], color=st["color"], lw=1.1, zorder=3, solid_capstyle="butt")
                ax.plot([r["diff"]], [yy], marker=st["marker"], ms=4.6 if st["marker"] != "^" else 5.2,
                        mfc=st["color"], mec=st["edge"], mew=0.5, ls="none", zorder=4)
            crd = confirm_rows(d, m, "reasoned")
            rd = crd[cid] if crd else None
            if rd and rd["n"]:
                yd = yy + 0.36
                ax.plot(rd["ci95"], [yd, yd], color=DELIB_GREY_LIGHT, lw=0.8, zorder=2, solid_capstyle="butt")
                ax.plot([rd["diff"]], [yd], marker=st["marker"], ms=3.0 if st["marker"] != "^" else 3.4,
                        mfc=DELIB_GREY, mec=DELIB_GREY, mew=0.3, ls="none", zorder=2.5)
        ax.set_yticks([yy for yy, _ in model_rows])
        if k == 0:
            ax.set_yticklabels([SHORT[m] for _, m in model_rows])
            ax.tick_params(axis="y", length=0, pad=3)
        else:
            ax.tick_params(axis="y", length=0, labelleft=False)
        ax.set_xticks([0, 0.5, 1.0])
        ax.set_xticklabels(["0", "0.5", "1"])
        ax.set_title(C_TITLES[cid], loc="left", pad=4, fontsize=8.5)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
    tr = blended_transform_factory(fig.transFigure, axes[0].transData)
    for yy, kind, label in rows:
        if kind == "header":
            fig.text(0.06 / fw, yy, label, transform=tr, ha="left", va="center", fontweight="bold", fontsize=8.5)
    fig.text((left + 2 * pw + 1.5 * gap) / fw, 0.56 / fh, "difference in flip rate, arm A (estimate and 95% interval)",
             ha="center", va="center", fontsize=8.5)
    handles = [Line2D([], [], marker=STYLE[c]["marker"], ls="-", lw=1.1, color=STYLE[c]["color"],
                      mfc=STYLE[c]["color"], mec=STYLE[c]["edge"], mew=0.5, ms=4.8,
                      label="Answer-only, " + BLOCK_TITLE[c][0].lower() + BLOCK_TITLE[c][1:])
               for c in CLASSES]
    handles.append(Line2D([], [], marker="o", ls="-", lw=0.8, color=DELIB_GREY_LIGHT, mfc=DELIB_GREY, mec=DELIB_GREY,
                          ms=3.0, label="Deliberative (secondary; same shapes)"))
    handles = [handles[0], handles[2], handles[1], handles[3]]  # column-major order for a 2 x 2 legend
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.005),
               handletextpad=0.4, columnspacing=2.0, borderaxespad=0.2)
    path = OUT / "fig2_confirmatory.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    # clipping check: every tick label and header must lie inside the figure
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    issues = []
    fb = fig.bbox
    for t in axes[0].get_yticklabels() + [t for t in fig.texts]:
        b = t.get_window_extent(rend)
        if b.x0 < fb.x0 or b.x1 > fb.x1 or b.y0 < fb.y0 or b.y1 > fb.y1:
            issues.append(f"fig2: text '{t.get_text()}' clipped")
    plt.close(fig)
    return path, issues


# ------------------------------------------------------------------ figure 3

RIGHT_COLS = [("control", "none"), ("certain_right", "certain"), ("unsure_right", "certain"), ("perfect_mixed", "certain"),
              ("unsure_right", "unsure"), ("certain_right", "unsure"), ("perfect_mixed", "unsure")]
RIGHT_COL_LABELS = ["control\n(no\nobjection)", "certain-\nis-right", "unsure-\nis-right", "mixed-\nperfect", "unsure-\nis-right",
                    "certain-\nis-right", "mixed-\nperfect"]


def fig3(d, o7):
    rs = {r["model"]: r for r in d["right_stratum"]}
    rows = []  # (label, kind, values[list of (flips, n) or None])
    for cls in ("open", "closed"):
        rows.append((BLOCK_TITLE[cls] + " (answer-only)", "header", None))
        for m, s, c in MODELS:
            if c != cls or m not in rs:
                continue
            cells = {(c_["log"], c_["tone"]): c_ for c_ in rs[m]["cells"]}
            vals = []
            for col in RIGHT_COLS:
                c_ = cells.get(col)
                vals.append((c_["flips"], c_["n"]) if c_ and c_["n"] else None)
            rows.append((s, "model", vals))
    sd = sonnet_deliberative_right()
    rows.append(("Brief reasoning (≤100 words)", "header", None))
    rows.append(("Claude Sonnet 5.5", "model",
                 [(sd[c]["flips"], sd[c]["n"]) if c in sd and sd[c]["n"] else None for c in RIGHT_COLS]))
    cmap = LinearSegmentedColormap.from_list("blue_seq", BLUE_RAMP)
    vmax = 40.0
    row_h, hdr_h = 0.215, 0.20
    heights = [hdr_h if k == "header" else row_h for _, k, _ in rows]
    left, right, top = 1.78, 0.78, 0.95
    pb_bottom, pb_h, pb_gap = 0.50, 1.30, 0.62  # panel (b): x labels, bar area, title gap
    bottom = pb_bottom + pb_h + pb_gap
    gw = PAGE_W - left - right
    gh = sum(heights)
    fw, fh = PAGE_W, top + gh + bottom
    fig = plt.figure(figsize=(fw, fh), dpi=DPI)
    ax = fig.add_axes([left / fw, bottom / fh, gw / fw, gh / fh])
    ax.set_xlim(0, len(RIGHT_COLS))
    ax.set_ylim(gh, 0)
    ax.axis("off")
    cw = 1.0
    yy = 0.0
    tr_fig_x = blended_transform_factory(fig.transFigure, ax.transData)
    for (label, kind, vals), h in zip(rows, heights):
        if kind == "header":
            fig.text(0.06 / fw, yy + h * 0.62, label, transform=tr_fig_x, ha="left", va="center", fontweight="bold",
                     fontsize=8.5)
        else:
            fig.text((left - 0.06) / fw, yy + h / 2, label, transform=tr_fig_x, ha="right", va="center", fontsize=8)
            for k, v in enumerate(vals):
                x0 = k * cw
                if v is None:
                    ax.add_patch(plt.Rectangle((x0 + 0.02, yy + 0.008), cw - 0.04, h - 0.016, fc="white",
                                               ec="#d6d4cc", lw=0.5))
                    continue
                flips, n = v
                frac = flips / n * vmax if n else 0  # scale to "out of 40"
                col = cmap(min(1.0, frac / vmax))
                ax.add_patch(plt.Rectangle((x0 + 0.02, yy + 0.008), cw - 0.04, h - 0.016, fc=col, ec="none"))
                txt = (f"{flips:g}" if n == 40 else f"{flips:g}/{n}")
                ax.text(x0 + cw / 2, yy + h / 2, txt, ha="center", va="center", fontsize=8,
                        color="white" if frac > 19 else INK)
        yy += h
    # column headers (two levels)
    trx = blended_transform_factory(ax.transData, fig.transFigure)
    y_sub = (bottom + gh + 0.17) / fh
    y_grp = (bottom + gh + 0.50) / fh
    for k, lab in enumerate(RIGHT_COL_LABELS):
        fig.text(k + 0.5, y_sub, lab, transform=trx, ha="center", va="center", fontsize=8, linespacing=1.0)
    for (a, b, lab) in ((1, 4, "certain objection, log:"), (4, 7, "unsure objection, log:")):
        fig.text((a + b) / 2, y_grp, lab, transform=trx, ha="center", va="center", fontsize=8.5, fontweight="bold")
        line_y = (bottom + gh + 0.405) / fh
        fig.add_artist(Line2D([a + 0.06, b - 0.06], [line_y, line_y], transform=trx, color=INK2, lw=0.6))
    # colour bar
    cax = fig.add_axes([(left + gw + 0.22) / fw, (bottom + 0.15) / fh, 0.11 / fw, (gh - 0.3) / fh])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, vmax))
    cb = fig.colorbar(sm, cax=cax)
    cb.set_ticks([0, 10, 20, 30, 40])
    cb.outline.set_linewidth(0.4)
    cb.ax.tick_params(labelsize=8, width=0.5, length=2)
    cb.set_label("switches to the wrong option (of 40)", fontsize=8)
    fig.text(0.06 / fw, (bottom + gh + top - 0.14) / fh,
             "(a) Model-was-right items: switches to the wrong option the reviewer names", ha="left", va="center",
             fontsize=8.5)

    # panel (b): Sonnet on model-was-wrong items, answer-only vs brief reasoning, same item ids
    ids, reas, inst = o7
    bx = fig.add_axes([0.62 / fw, pb_bottom / fh, 3.3 / fw, pb_h / fh])
    fig.text(0.06 / fw, (pb_bottom + pb_h + 0.36) / fh,
             f"(b) Model-was-wrong items, Sonnet: answer-only vs brief reasoning ({len(ids)} items)",
             ha="left", va="center", fontsize=8.5)
    series = (("Answer-only (same items)", inst, STYLE["closed"]["color"]),
              ("Brief reasoning", reas, DELIB_GREY))
    wbar = 0.36
    for k, (lab, cnt, col) in enumerate(series):
        for j, c in enumerate(CORE4):
            fl, n = cnt.get(c, (0, 0))
            if not n:
                continue
            xpos = j + (k - 0.5) * (wbar + 0.03)
            bx.bar(xpos, fl * (40.0 / n), width=wbar, color=col, edgecolor="none", zorder=3,
                   label=lab if j == 0 else None)
            bx.text(xpos, fl * (40.0 / n) + 0.8, f"{fl:g}" if n == 40 else f"{fl:g}/{n}", ha="center", va="bottom",
                    fontsize=8, color=INK)
    bx.set_xticks(range(len(CORE4)))
    bx.set_xticklabels([f"{t} |\n{lg.replace('_right', '-is-right').replace('_', '-')}" for lg, t in CORE4],
                       fontsize=8, linespacing=1.0)
    bx.set_ylim(0, 44)
    bx.set_yticks([0, 10, 20, 30, 40])
    bx.set_ylabel("switches (of 40)", fontsize=8)
    bx.set_xlim(-0.6, len(CORE4) - 0.4)
    bx.grid(axis="y", color="#e1e0d9", lw=0.5, zorder=0)
    bx.tick_params(axis="x", length=0, pad=3)
    for sp in ("top", "right"):
        bx.spines[sp].set_visible(False)
    bx.legend(loc="upper left", bbox_to_anchor=(1.04, 1.0), frameon=False, handlelength=1.2, handletextpad=0.5,
              labelspacing=0.7, borderaxespad=0.0)
    path = OUT / "fig3_right_stratum.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path, sd


# ------------------------------------------------------------------ summary table (image)

PROBE_NOTE = {"anthropic:claude-sonnet-5-5": "smoothed", "qwen3.5:9b": "misread unsure",
              "openai:gpt-6-sol": "unsure as 2 of 2"}
SUMMARY_BLOCKS = (
    ("Closed models", ["anthropic:claude-sonnet-5-5", "openai:gpt-6-sol", "google:gemini-3.6-flash",
                       "anthropic:claude-haiku-5-5", "openai:gpt-6-luna"]),
    ("Open-weight, main set", [m for m, _, c in MODELS if c == "open"]),
    ("Recency tier (exploratory, open-weight)", [m for m, _, c in MODELS if c == "recency"]),
)
SUMMARY_COLS = ("D\narm A", "D\narm B", "D\narm R", "D\narm S", "C3\narm A", "Tone gap\narm A",
                "Probe\nreading")


def summary_rows(d3, s_res, b_res, r_res):
    """[(block title, [(model, D_A, D_B, D_R, D_S, C3, tone gap, probe note)])]; numbers are floats, None (not run)
    or the string "pending". D in arms A and R: arm_r_vs_a.md for its models, otherwise all_final3.json (arm A) and
    arm_r() (arm R, e.g. a new raw file); D in arm B: arm_b(); D in arm S: arm_s(); C3 and the no-log tone gap:
    all_final3.json, arm A."""
    r_a = arm_r_vs_a()
    s_vals, _, s_pending = s_res
    b_vals, b_pending = b_res[0], b_res[1]
    r_vals, r_pending = r_res[0], r_res[1]
    out = []
    for title, models in SUMMARY_BLOCKS:
        rows = []
        for m in models:
            g = group(d3, m, "instant", "A", "wrong", "key")
            cs = g["contrasts"]["all"]
            d_a = r_a[m]["D_A"][0] if m in r_a else cs["by_voice_main"]["D"]["diff"]
            if m in r_a:
                d_r = r_a[m]["D_R"][0]
            else:
                d_r = r_vals[m]["D"]["diff"] if m in r_vals else ("pending" if m in r_pending else None)
            d_b = b_vals[m]["D"]["diff"] if m in b_vals else ("pending" if m in b_pending else None)
            d_s = s_vals[m]["D"]["diff"] if m in s_vals else ("pending" if m in s_pending else None)
            c3 = next(c for c in cs["spill_unsure"] if c["key"] == "spill_unsure_vs_unsure_right")
            tg = next(c for c in cs["other"] if c["key"] == "tone_gap_nolog")
            rows.append((m, d_a, d_b, d_r, d_s, c3["diff"] if c3["n"] else None, tg["diff"] if tg["n"] else None,
                         PROBE_NOTE.get(m, "ok")))
        out.append((title, rows))
    return out


def _cellfmt(v):
    if v is None:
        return "\u2013"
    if isinstance(v, str):
        return v
    return f2(v).replace("-", "\u2212")


SUMMARY_NOTE = ("$D = d_c - d_u$;  C3 = unsure | mixed-perfect − unsure | unsure-is-right;  tone gap = certain | none "
                "− unsure | none.\nAnswer-only, model-was-wrong items, 80 per model;  – = not run.  D in arms A "
                "and R for the arm-R models\n(Ministral 3 8B: same-day arm A repeat; its C3 and tone gap: 15 Nov run).\n"
                "Arm S column: plain D on all items (order-balanced D in the text).")


def tab_summary(d3, s_res, b_res, r_res):
    blocks = summary_rows(d3, s_res, b_res, r_res)
    row_h, hdr_h, blk_h = 0.205, 0.40, 0.235
    n_rows = sum(len(r) for _, r in blocks)
    note_h = 0.10 + 0.145 * (SUMMARY_NOTE.count("\n") + 1)  # 8 pt lines at 1.25 spacing
    fw = PAGE_W
    body_h = hdr_h + len(blocks) * blk_h + n_rows * row_h
    fh = body_h + note_h + 0.12
    fig = plt.figure(figsize=(fw, fh), dpi=DPI)
    xs_num = [1.78, 2.33, 2.88, 3.43, 3.98, 4.63]
    x_probe = 5.12

    def Y(y_in):  # inches from the top -> figure fraction
        return 1 - (0.06 + y_in) / fh

    def rule(y_in, lw=0.8):
        fig.add_artist(Line2D([0.05 / fw, (fw - 0.05) / fw], [Y(y_in), Y(y_in)], color=INK, lw=lw))

    rule(0.0)
    fig.text(0.08 / fw, Y(hdr_h / 2), "Model", ha="left", va="center", fontsize=8.5, fontweight="bold")
    for x, lab in zip(xs_num + [x_probe], SUMMARY_COLS):
        fig.text((x if lab != SUMMARY_COLS[-1] else x) / fw, Y(hdr_h / 2), lab, ha="center" if lab != SUMMARY_COLS[-1]
                 else "left", va="center", fontsize=8.5, fontweight="bold", linespacing=1.05)
    rule(hdr_h, lw=0.5)
    y = hdr_h
    texts = []
    for title, rows in blocks:
        texts.append(fig.text(0.08 / fw, Y(y + blk_h * 0.58), title, ha="left", va="center", fontsize=8,
                              fontweight="bold", color=INK2))
        y += blk_h
        for m, *vals, note in rows:
            yc = Y(y + row_h / 2)
            texts.append(fig.text(0.22 / fw, yc, SHORT[m], ha="left", va="center", fontsize=8))
            for x, v in zip(xs_num, vals):
                texts.append(fig.text(x / fw, yc, _cellfmt(v), ha="center", va="center", fontsize=8,
                                      color=INK2 if v is None or isinstance(v, str) else INK))
            texts.append(fig.text(x_probe / fw, yc, note, ha="left", va="center", fontsize=8,
                                  color=INK if note != "ok" else INK2))
            y += row_h
    rule(y + 0.03)
    note = SUMMARY_NOTE
    texts.append(fig.text(0.08 / fw, Y(y + 0.10), note, ha="left", va="top", fontsize=8, color=INK2,
                          linespacing=1.25))
    path = OUT / "tab_summary.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    issues = []
    for t in texts:
        b = t.get_window_extent(rend)
        if b.x0 < 0 or b.x1 > fig.bbox.x1 or b.y0 < 0 or b.y1 > fig.bbox.y1:
            issues.append(f"tab_summary: text '{t.get_text()[:30]}' clipped")
    plt.close(fig)
    return path, issues


# ------------------------------------------------------------------ tables

def tables(d, sonnet_delib, d3, s_res, b_res, r_res, d_x=None):
    L = ["# Tables for \"Loud or Right?\"", "",
         "Generated by `paper/make_figs.py` from `harness/analysis/all_final2.json` (Tables 1-4) and "
         "`harness_x/analysis/arm_r_vs_a.md` (Table 5). Estimates are differences in "
         "flip rate on the model-was-wrong stratum (80 test items per model; reviewer names the key unless stated), "
         "with 95% item-bootstrap intervals in brackets. Model class and the exploratory label come from the paper's "
         "model list, not from the JSON's `tier` or `status` fields.", ""]

    # T1
    L += ["## Table 1. Confirmatory contrasts C1-C4 (answer-only, arm A)", "",
          "C1 = d_c; C2 = d_c - d_u; C3 = unsure | mixed-perfect - unsure | unsure-is-right; C4 = d_c with the "
          "reviewer naming a wrong option. Main set: Holm-adjusted p across C1-C4 within each model (exact two-sided "
          "sign test). Recency tier: exploratory; p is the unadjusted two-sided sign test.", "",
          "| Model | C1 | C2 | C3 | C4 |", "|---|---|---|---|---|"]
    for cls in CLASSES:
        L.append(f"| **{BLOCK_TITLE[cls]}** | | | | |")
        for m, s, c in MODELS:
            if c != cls:
                continue
            cr = confirm_rows(d, m, "instant")
            cells = []
            for cid in ("C1", "C2", "C3", "C4"):
                r = cr[cid] if cr else None
                if not r or not r["n"]:
                    cells.append("-")
                    continue
                ps = fp(r["sign_p"] if cls == "recency" else r["holm_p"])
                p = f"p < {ps[1:]}" if ps.startswith("<") else f"p = {ps}"
                cells.append(f"{f2(r['diff'])} {fci(r['ci95'])}, {p}")
            L.append(f"| {s} | " + " | ".join(cells) + " |")
    L += ["", "n = 80 items in every cell. Recency-tier p values are unadjusted sign-test p (the JSON also holds a "
          "Holm p for these rows, not used here).", ""]

    # T2
    L += ["## Table 2. Surface-form robustness: arm A vs arm B (answer-only)", "",
          "Arm B uses another reviewer name and other confidence phrases, shuffles the log entries per item and draws "
          "log letters from A-J. Models with both arms only (Gemini 3.6 Flash and Qwen 3.8 27B have no arm B).", "",
          "| Model | d_c, arm A | d_c, arm B | d_u, arm A | d_u, arm B |", "|---|---|---|---|---|"]
    for cls in CLASSES:
        block = []
        for m, s, c in MODELS:
            if c != cls:
                continue
            a, b = by_voice(d, m, "A"), by_voice(d, m, "B")
            if not (a and b):
                continue
            block.append(f"| {s} | {f2(a['d_c']['diff'])} {fci(a['d_c']['ci95'])} | {f2(b['d_c']['diff'])} "
                         f"{fci(b['d_c']['ci95'])} | {f2(a['d_u']['diff'])} {fci(a['d_u']['ci95'])} | "
                         f"{f2(b['d_u']['diff'])} {fci(b['d_u']['ci95'])} |")
        if block:
            L.append(f"| **{BLOCK_TITLE[cls]}** | | | | |")
            L += block
    L += ["", "n = 80 items per model and arm.", ""]

    # T3
    pair_cells = [("certain_right", "certain"), ("unsure_right", "certain"), ("unsure_right", "unsure"),
                  ("certain_right", "unsure")]
    L += ["## Table 3. Stated P(reviewer right) vs answer-only flip rate (arm A, target key)", "",
          "Each cell: stated P(right) / flip rate. Stated P is the model's answer to a probe asking how likely the "
          "reviewer is to be right, given the same log and objection tone (arm A: one probe call per cell). Flip "
          "rate: share of the 80 items on which the model switched to the reviewer's answer (items with two "
          "replicates count their mean).", "",
          "| Model | certain \\| certain-is-right | certain \\| unsure-is-right | unsure \\| unsure-is-right | "
          "unsure \\| certain-is-right |", "|---|---|---|---|---|"]
    pp = {(b["model"], b["arm"]): {(r["log"], r["tone"]): r for r in b["rows"]} for b in d["probe_pairing"]}
    for cls in CLASSES:
        L.append(f"| **{BLOCK_TITLE[cls]}** | | | | |")
        for m, s, c in MODELS:
            if c != cls:
                continue
            blk = pp.get((m, "A"))
            cells = []
            for cell in pair_cells:
                r = blk.get(cell) if blk else None
                if not r:
                    cells.append("-")
                    continue
                sp = "-" if r["mean_stated_probability"] is None else f2(r["mean_stated_probability"])
                fr = "-" if r["flips_key"] is None or not r["n_key"] else f2(r["flips_key"] / r["n_key"])
                cells.append(f"{sp} / {fr}")
            L.append(f"| {s} | " + " | ".join(cells) + " |")
    L += [""]

    # T4
    L += ["## Table 4. Mitigation instruction (exploratory): change from arm A to arm M", "",
          "Arm M adds one paragraph asking the model to weigh the objection by the record of objections worded the "
          "same way; otherwise identical to arm A. Change = arm M - arm A on the same items, with a paired item "
          "bootstrap interval.", "",
          "| Model | Mode | n | change in d_u | change in C4 |", "|---|---|---|---|---|"]
    mit = {(b["model"], b["mode"]): {r["stat"]: r for r in b["stats"]} for b in d["mitigation"]}
    for mode, mname in (("instant", "answer-only"), ("reasoned", "deliberative")):
        for m, s, c in MODELS:
            st = mit.get((m, mode))
            if not st:
                continue
            du, c4 = st["d_u"], st["C4"]
            n = du["n"] if du["n"] == c4["n"] else f"{du['n']} / {c4['n']}"
            cdu = f"{f2(du['change'])} {fci(du['ci_change'])}" if du["n"] else "-"
            cc4 = f"{f2(c4['change'])} {fci(c4['ci_change'])}" if c4["n"] else "-"
            L.append(f"| {s} | {mname} | {n} | {cdu} | {cc4} |")
    L += ["", "Only models with an arm-M run are listed. Recency-tier models have no arm M.", ""]

    # T5
    r_a = arm_r_vs_a()
    L += ["## Table 5. Reversed entry order (exploratory): arm A vs arm R (answer-only)", "",
          "Arm R is arm A with the eight log entries in reverse order. D = d_c - d_u in each arm; R - A is the paired "
          "difference on the same 80 items; C3 = unsure | mixed-perfect - unsure | unsure-is-right in arm R. Numbers "
          "are copied from `harness_x/analysis/arm_r_vs_a.md` (sections 1, 2 and 4: paired item bootstrap with "
          "2,000 resamples; items non-missing in the five cells used, in both arms).", "",
          "| Model | D, arm A | D, arm R | D: R - A | C3, arm R |", "|---|---|---|---|---|"]
    for cls in CLASSES:
        block = []
        for m, s, c in MODELS:
            if c != cls or m not in r_a:
                continue
            r = r_a[m]
            block.append(f"| {s} | {f2(r['D_A'][0])} {fci(r['D_A'][1])} | {f2(r['D_R'][0])} {fci(r['D_R'][1])} | "
                         f"{f2(r['D_RA'][0])} {fci(r['D_RA'][1])} | {f2(r['C3_R'][0])} {fci(r['C3_R'][1])} |")
        if block:
            L.append(f"| **{BLOCK_TITLE[cls]}** | | | | |")
            L += block
    L += ["", "Ministral 3 8B: arm A is the same-day repeat (`harness_x/runs/test__ministral-3_8b__instant__A.jsonl`), "
          "as in `arm_r_vs_a.md`, so its arm-A D differs from C2 in Table 1 (15 Nov run). Arm-A intervals here can "
          "differ slightly from Table 1 because the bootstrap and item population differ.", ""]

    # T6 (the summary table rendered as figs/tab_summary.png)
    L += ["## Table 6. Summary across arms (the table rendered as `tab_summary.png`)", "",
          "Answer-only, model-was-wrong items. D = d_c - d_u; C3 = unsure | mixed-perfect - unsure | "
          "unsure-is-right; tone gap = certain | none - unsure | none (no log). D in arms A and R for the arm-R "
          "models from `arm_r_vs_a.md` (Ministral 3 8B: same-day arm A repeat), otherwise arm A from "
          "`harness/analysis/all_final3.json`; arm B from all_final3.json (recency tier: x_final.json if it has the "
          "group), or from the raw run file where no frozen group exists; arm R for other models with a run file: "
          "arm_r.json or the raw file; arm S from " + s_res[1] + "; C3 and tone gap from all_final3.json. "
          "- = not run.", "",
          "| Model | D, arm A | D, arm B | D, arm R | D, arm S | C3, arm A | Tone gap, arm A | Probe reading |",
          "|---|---|---|---|---|---|---|---|"]
    for title, rows in summary_rows(d3, s_res, b_res, r_res):
        L.append(f"| **{title}** | | | | | | | |")
        for m, *vals, note in rows:
            L.append(f"| {SHORT[m]} | " + " | ".join(_cellfmt(v).replace("\u2212", "-").replace("\u2013", "-")
                                                    for v in vals) + f" | {note} |")
    L.append("")

    # Table 7: native version of the report's Table 1 (primary; tab_summary.png is kept as an image copy)
    t7, t7_notes = table7(d3, d_x, b_res, r_res)
    L += ["## Table 7. Per-model summary (the report's Table 1; replaces `tab_summary.png`)", "",
          "Answer-only, 80 model-was-wrong items per model. d_c, d_u, D = d_c - d_u, C3 and the tone gap "
          "(certain | none - unsure | none) are arm A; D B, D R: arms B and R; D_bal S: the order-balanced D in arm S "
          "(`arm_s.md`, section 2). Arm A: `all_final3.json` (main set) and `x_final.json` (recency tier); D B and "
          "D R as in Table 6. Two decimals, halves away from zero. \u2013 = not run.", ""]
    L += t7 + [""] + t7_notes + [""]
    path = OUT / "tables.md"
    path.write_text("\n".join(L), encoding="utf-8")
    return path, t7


POST_FREEZE = {"qwen3.5:9b", "google:gemini-3.6-flash"}  # added after the freeze; marked with a dagger
TABLE7_BLOCKS = (
    ("Closed models", ["anthropic:claude-sonnet-5-5", "openai:gpt-6-sol", "google:gemini-3.6-flash",
                       "anthropic:claude-haiku-5-5", "openai:gpt-6-luna"]),
    ("Open-weight, main set", [m for m, _, c in MODELS if c == "open"]),
    ("Recency tier (exploratory)", [m for m, _, c in MODELS if c == "recency"]),
)
TABLE7_HEAD = ("Model", "d_c A", "d_u A", "D A", "D B", "D R", "D_bal S", "C3 A", "Tone gap", "Probe")
PAIRING_MARK = "\u2021"  # double dagger on an arm R cell paired with a different arm A run


def arm_s_dbal():
    """Order-balanced D in arm S (D_bal, section 2 of harness_x/analysis/arm_s.md): {model id: estimate}."""
    if not ARM_S_MD.exists():
        return {}
    out, in_sec = {}, False
    num = re.compile(r"([+-]?\d+\.\d+) \[")
    for line in ARM_S_MD.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_sec = line.startswith("## 2.")
            continue
        if in_sec and line.startswith("| ") and not line.startswith("| model"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells[0] in ARM_R_NAMES and len(cells) >= 5:
                g = num.match(cells[4])
                if g:
                    out[ARM_R_NAMES[cells[0]]] = float(g.group(1))
    return out


def _t7(v):
    if v is None:
        return "\u2013"
    if isinstance(v, str):
        return v
    return f2(v).replace("-", "\u2212")


def table7(d3, d_x, b_res, r_res):
    """Table 7 (Table 1 of the report), as markdown lines: header, separator, block header rows and model rows.
    d_c, d_u and D in arm A: all_final3.json (main set) and x_final.json (recency tier), so every arm A column of a
    row comes from the same run (Ministral 3 8B: the 15 Nov run). D B: arm_b(). D R: arm_r_vs_a.md for its models
    (Ministral 3 8B's value is paired there with a same-day arm A repeat, marked with a double dagger), otherwise
    arm_r() (e.g. Gemini from its raw file). D_bal S: arm_s.md section 2. C3, tone gap: all_final3.json, arm A.
    Returns (lines, footnotes)."""
    r_a = arm_r_vs_a()
    dbal = arm_s_dbal()
    b_vals, b_pending = b_res[0], b_res[1]
    r_vals, r_pending = r_res[0], r_res[1]
    lines = ["| " + " | ".join(TABLE7_HEAD) + " |", "|" + "---|" * len(TABLE7_HEAD)]
    notes = []
    for title, models in TABLE7_BLOCKS:
        lines.append(f"| **{title}** |" + " |" * (len(TABLE7_HEAD) - 1))
        for m in models:
            cls = CLASS[m]
            ga = None
            for dj in ([d_x, d3] if cls == "recency" else [d3]):
                ga = group(dj, m, "instant", "A", "wrong", "key") if dj else None
                if ga:
                    break
            bv = ga["contrasts"]["all"]["by_voice_main"]
            d_c, d_u, d_a = bv["d_c"]["diff"], bv["d_u"]["diff"], bv["D"]["diff"]
            g3 = group(d3, m, "instant", "A", "wrong", "key")["contrasts"]["all"]
            c3 = next(c for c in g3["spill_unsure"] if c["key"] == "spill_unsure_vs_unsure_right")
            tg = next(c for c in g3["other"] if c["key"] == "tone_gap_nolog")
            if m in r_a:
                d_r = _t7(r_a[m]["D_R"][0])
                if abs(r_a[m]["D_A"][0] - d_a) > 0.001:  # arm_r_vs_a.md prints 3 decimals
                    d_r += PAIRING_MARK
                    run = "the 15 Nov run" if m == "ministral-3:8b" else "the main run"
                    notes.append(f"{PAIRING_MARK} {SHORT[m]}: this arm R value is paired in `arm_r_vs_a.md` with a "
                                 f"same-day repeat of arm A (D = {_t7(r_a[m]['D_A'][0])}); the arm A columns here "
                                 f"use {run} (D = {_t7(d_a)}).")
            else:
                d_r = _t7(r_vals[m]["D"]["diff"]) if m in r_vals else ("pending" if m in r_pending else _t7(None))
            d_b = _t7(b_vals[m]["D"]["diff"]) if m in b_vals else ("pending" if m in b_pending else _t7(None))
            name = SHORT[m] + ("\u2020" if m in POST_FREEZE else "")
            cells = [name, _t7(d_c), _t7(d_u), _t7(d_a), d_b, d_r, _t7(dbal.get(m)),
                     _t7(c3["diff"] if c3["n"] else None), _t7(tg["diff"] if tg["n"] else None),
                     PROBE_NOTE.get(m, "ok")]
            lines.append("| " + " | ".join(cells) + " |")
    notes.append("\u2020 Added after the freeze under the pre-set rule.")
    return lines, notes


ARM_R_NAMES = {"gemma4:12b": "gemma4:12b", "ministral-3:8b": "ministral-3:8b",
               "Claude Sonnet 5.5": "anthropic:claude-sonnet-5-5",
               "Llama 3.3 70B": "openrouter:meta-llama/llama-3.3-70b-instruct",
               "Llama 4 Maverick": "openrouter:meta-llama/llama-4-maverick", "GPT-6 Sol": "openai:gpt-6-sol"}


def arm_r_vs_a():
    """Primary-line numbers from arm_r_vs_a.md: D per arm (section 1), D: R - A (section 2), C3 in R (section 4).
    Returns {model id: {"D_A": (est, [lo, hi]), "D_R": ..., "D_RA": ..., "C3_R": ...}}."""
    text = ARM_R_VS_A.read_text(encoding="utf-8")
    sections, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"## (\d)\.", line)
        if m:
            cur = m.group(1)
            sections[cur] = []
        elif cur and line.startswith("| ") and not line.startswith("| model") and "secondary" not in line:
            sections[cur].append([c.strip() for c in line.strip().strip("|").split("|")])
    num = re.compile(r"([+-]?\d+\.\d+) \[([+-]?\d+\.\d+), ([+-]?\d+\.\d+)\]")

    def est(cell):
        g = num.match(cell)
        return float(g.group(1)), [float(g.group(2)), float(g.group(3))]

    out = {}
    for row in sections.get("1", []):
        if row[0] in ARM_R_NAMES and row[1] in ("A", "R"):
            out.setdefault(ARM_R_NAMES[row[0]], {})[f"D_{row[1]}"] = est(row[10])
    for row in sections.get("2", []):
        if row[0] in ARM_R_NAMES:
            out.setdefault(ARM_R_NAMES[row[0]], {})["D_RA"] = est(row[2])
    for row in sections.get("4", []):
        if row[0] in ARM_R_NAMES:
            out.setdefault(ARM_R_NAMES[row[0]], {})["C3_R"] = est(row[4])
    for m, r in out.items():
        missing = {"D_A", "D_R", "D_RA", "C3_R"} - set(r)
        if missing:
            raise SystemExit(f"arm_r_vs_a.md: {m} lacks {sorted(missing)}")
    return out


# ------------------------------------------------------------------ consistency check against the summary markdown

def check_summary(d):
    """Compare C1-C4 and right-stratum counts in the JSON with summary__all_final2.md (3 decimals)."""
    if not SUMMARY_MD.exists():
        return ["summary markdown not found"]
    text = SUMMARY_MD.read_text(encoding="utf-8")
    issues = []
    num = r"([+-]\d\.\d{3}) \[([+-]\d\.\d{3}), ([+-]\d\.\d{3})\] \(([^,]+), (\d+)\)"
    for line in text.splitlines():
        m = re.match(r"\| (\S+) \| (answer-only|deliberative) \| (confirmatory|secondary) \| (.*)", line)
        if not m:
            continue
        model, mode = m.group(1), "instant" if m.group(2) == "answer-only" else "reasoned"
        cr = confirm_rows(d, model, mode)
        found = re.findall(num, m.group(4))[:4]
        for cid, f in zip(("C1", "C2", "C3", "C4"), found):
            r = cr[cid]
            mine = (f"{r['diff']:+.3f}", f"{r['ci95'][0]:+.3f}", f"{r['ci95'][1]:+.3f}")
            if mine != f[:3]:
                issues.append(f"{model} {mode} {cid}: JSON {mine} vs markdown {f[:3]}")
    rs = {r["model"]: r for r in d["right_stratum"]}
    for line in text.splitlines():
        m = re.match(r"\| (\S+) \| (main|recency) \| ((?:[\d.]+/\d+ \| ){9})", line)
        if not m:
            continue
        model = m.group(1)
        md_cells = re.findall(r"([\d.]+)/(\d+)", m.group(3))
        js = [(c["flips"], c["n"]) for c in rs[model]["cells"]]
        for (a, b), (fl, n) in zip(md_cells, js):
            if abs(float(a) - fl) > 1e-9 or int(b) != n:
                issues.append(f"right stratum {model}: markdown {a}/{b} vs JSON {fl}/{n}")
    return issues


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    d = load()
    d_r = json.loads(ARM_R.read_text(encoding="utf-8"))
    d3 = json.loads(ALL_FINAL3.read_text(encoding="utf-8"))
    d_x = json.loads(X_FINAL.read_text(encoding="utf-8")) if X_FINAL.exists() else None
    s_res = arm_s()
    print(f"arm S source: {s_res[1]}; used: {', '.join(SHORT[m] for m in s_res[0]) or '-'}; "
          f"pending: {s_res[2] or '-'}")
    b_fig = arm_b({c: [d] for c in CLASSES})  # figure: the same frozen source as before (all_final2.json)
    b_tab = arm_b({"open": [d3], "closed": [d3], "recency": [d_x, d3]})  # table: all_final3 / x_final
    r_res = arm_r(d_r)
    for name, res in (("arm B", b_tab), ("arm R", r_res)):
        raw = [SHORT[m] for m, v in res[2].items() if v == "raw"]
        print(f"{name}: {len(res[0])} models ({'raw: ' + ', '.join(raw) if raw else 'all frozen'}); "
              f"pending: {res[1] or '-'}")
    o7 = o7_counts()
    p1, i1 = fig1(d, {"S": (s_res[0], s_res[2]), "B": b_fig[:2], "R": r_res[:2]})
    p2, i2 = fig2(d)
    p3, sd = fig3(d, o7)
    p5, i5 = tab_summary(d3, s_res, b_tab, r_res)
    p4, t7 = tables(d, sd, d3, s_res, b_tab, r_res, d_x)
    for p in (p1, p2, p3, p5, p4):
        print("wrote", p.relative_to(ROOT) if p.is_relative_to(ROOT) else p)
    print(f"O7 Sonnet, model-was-wrong items ({len(o7[0])} ids):")
    for lg, t in CORE4:
        a, r = o7[2].get((lg, t), (0, 0)), o7[1].get((lg, t), (0, 0))
        print(f"  {t}|{lg}: answer-only {a[0]:g}/{a[1]}, brief reasoning {r[0]:g}/{r[1]}")
    i1 = i1 + i5
    print("Sonnet deliberative right stratum (raw):",
          {f"{t}|{lg}": f"{v['flips']:g}/{v['n']}" for (lg, t), v in sorted(sd.items())})
    g = group(d, "anthropic:claude-sonnet-5-5", "reasoned", "A", "right", "distractor")
    if g:
        js = {(c["log"], c["tone"]): (c["flips"], c["n"]) for c in g["cells"] if c["run"]}
        diff = {k: (v, (sd[k]["flips"], sd[k]["n"])) for k, v in js.items() if k in sd and v != (sd[k]["flips"], sd[k]["n"])}
        print("Sonnet deliberative raw vs JSON group cells:", "match" if not diff else diff)
    for msg in i1 + i2:
        print("LAYOUT:", msg)
    for msg in check_summary(d):
        print("SUMMARY MISMATCH:", msg)
    return {"table7": t7}


if __name__ == "__main__":
    main()
