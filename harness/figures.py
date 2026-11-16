"""Figures for the Loud-or-Right experiment, as plain SVG (standard library only).

Usage:
    uv run --quiet --no-project python -I harness/figures.py harness/analysis/<name>.json [--out-dir DIR]

Input: the JSON written by `analyze.py --summary` (it needs `confirmatory`, `probe_pairing` and `groups`).
Output (default harness/figures/): fig1_confirmatory.svg, fig2_state_vs_act.svg, fig3_logs.svg, each with a CSV
of the plotted numbers next to it. Points resting on fewer than MIN_N items are not drawn (they stay in the CSV).
Sized for print at 16 cm wide; all text 11 px or larger.
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
MIN_N = 10
W = 600                      # viewBox width; printed at 16 cm
BLACK, GREY1, GREY2, ACCENT = "#000000", "#6e6e6e", "#bdbdbd", "#c0392b"
FONT = "font-family=\"Helvetica, Arial, sans-serif\""
MODE_NAME = {"instant": "answer-only", "reasoned": "deliberative"}
C_SHORT = {"C1": ("certain-voice", "record effect"), "C2": ("equal-score", "asymmetry (D)"),
           "C3": ("spillover onto", "unsure voice"), "C4": ("deference to a", "wrong option")}
FIG3_LOGS = ("none", "perfect_mixed", "c3_u4", "c2_u4", "unsure_right", "c4_u3", "c4_u2", "certain_right", "reliable")
FIG3_LABEL = {"none": "no log", "perfect_mixed": "perfect mixed", "c3_u4": "C3/4 U4/4", "c2_u4": "C2/4 U4/4",
              "unsure_right": "unsure-is-right", "c4_u3": "C4/4 U3/4", "c4_u2": "C4/4 U2/4",
              "certain_right": "certain-is-right", "reliable": "reliable (3/4, 3/4)"}


# ---------------------------------------------------------------- SVG helpers

def text(x, y, s, size=12, anchor="start", weight="normal", fill=BLACK, rotate=None):
    rot = f" transform=\"rotate({rotate} {x:.1f} {y:.1f})\"" if rotate is not None else ""
    return (f"<text x=\"{x:.1f}\" y=\"{y:.1f}\" font-size=\"{size}\" text-anchor=\"{anchor}\" "
            f"font-weight=\"{weight}\" fill=\"{fill}\"{rot}>{escape(str(s))}</text>")


def line(x1, y1, x2, y2, stroke=BLACK, width=1, dash=None):
    d = f" stroke-dasharray=\"{dash}\"" if dash else ""
    return (f"<line x1=\"{x1:.1f}\" y1=\"{y1:.1f}\" x2=\"{x2:.1f}\" y2=\"{y2:.1f}\" stroke=\"{stroke}\" "
            f"stroke-width=\"{width}\"{d}/>")


def circle(x, y, r, fill, stroke=None, width=1.2):
    s = f" stroke=\"{stroke}\" stroke-width=\"{width}\"" if stroke else ""
    return f"<circle cx=\"{x:.1f}\" cy=\"{y:.1f}\" r=\"{r}\" fill=\"{fill}\"{s}/>"


def svg(height, body, title):
    return (f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16cm\" height=\"{16 * height / W:.2f}cm\" "
            f"viewBox=\"0 0 {W} {height:.0f}\" {FONT}>\n<title>{escape(title)}</title>\n"
            f"<rect x=\"0\" y=\"0\" width=\"{W}\" height=\"{height:.0f}\" fill=\"#ffffff\"/>\n"
            + "\n".join(body) + "\n</svg>\n")


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def short_model(m):
    return m.split(":", 1)[1] if m.startswith(("openai:", "anthropic:")) else m


# ---------------------------------------------------------------- figure 1

def fig1(data, out):
    conf = data["confirmatory"]
    models = sorted({b["model"] for b in conf})
    by = {(b["model"], b["mode"]): {r["id"]: r for r in b["rows"]} for b in conf}
    rows_csv = []
    for (m, mode), rs in sorted(by.items()):
        for cid, r in rs.items():
            rows_csv.append([m, MODE_NAME.get(mode, mode), cid, r["n"], r["diff"],
                             r["ci95"][0] if r["ci95"] else "", r["ci95"][1] if r["ci95"] else "",
                             r["sign_p"], r["holm_p"], int(r["n"] >= MIN_N)])
    write_csv(out / "fig1_confirmatory.csv",
              ["model", "mode", "test", "n", "estimate", "ci_lo", "ci_hi", "sign_p", "holm_p", "drawn"], rows_csv)

    vals = [v for r in rows_csv if r[-1] for v in (r[5], r[6]) if v != ""]
    lo = min([-0.25] + vals)
    hi = max([0.5] + vals)
    lo, hi = -0.25 * ((-lo + 0.2499) // 0.25), 0.25 * ((hi + 0.2499) // 0.25)
    left, right, top, row_h = 140, 8, 76, 40
    pw = (W - left - right) / 4
    gap = 12
    height = top + row_h * len(models) + 70
    body = [text(8, 18, "Confirmatory tests (answer-only) and secondary tests (deliberative), arm A, model-was-wrong items",
                 12, weight="bold")]

    def X(k, v):
        x0 = left + k * pw + gap / 2
        return x0 + (v - lo) / (hi - lo) * (pw - gap)

    ticks = [t / 2 for t in range(int(lo * 2), int(hi * 2) + 1)]
    ybot = top + row_h * len(models)
    for k, cid in enumerate(("C1", "C2", "C3", "C4")):
        a, b = C_SHORT[cid]
        cx = left + k * pw + pw / 2
        body.append(text(cx, top - 36, cid, 12, "middle", "bold"))
        body.append(text(cx, top - 22, a, 11, "middle"))
        body.append(text(cx, top - 8, b, 11, "middle"))
        body.append(line(X(k, lo), ybot, X(k, hi), ybot, BLACK))
        for t in ticks:
            body.append(line(X(k, t), ybot, X(k, t), ybot + 4))
            body.append(text(X(k, t), ybot + 16, f"{t:g}", 11, "middle"))
        body.append(line(X(k, 0), top - 2, X(k, 0), ybot, ACCENT, 1))
    for j, m in enumerate(models):
        yc = top + row_h * j + row_h / 2
        body.append(text(left - 8, yc + 4, short_model(m), 12, "end"))
        if j:
            body.append(line(8, top + row_h * j, W - right, top + row_h * j, GREY2, 0.5))
        for k, cid in enumerate(("C1", "C2", "C3", "C4")):
            for mode, dy, col in (("instant", -5, BLACK), ("reasoned", 7, GREY1)):
                r = by.get((m, mode), {}).get(cid)
                if not r or r["n"] < MIN_N or r["diff"] is None:
                    continue
                body.append(line(X(k, r["ci95"][0]), yc + dy, X(k, r["ci95"][1]), yc + dy, col, 1.6))
                body.append(circle(X(k, r["diff"]), yc + dy, 3.6, col))
    ly = ybot + 40
    body += [circle(16, ly - 4, 3.6, BLACK), text(26, ly, "answer-only (confirmatory)", 11),
             circle(206, ly - 4, 3.6, GREY1), text(216, ly, "deliberative (secondary)", 11),
             text(8, ly + 18, f"Dot: estimate (difference in flip rate). Bar: 95% bootstrap interval. "
                              f"Not drawn when n < {MIN_N} items.", 11)]
    (out / "fig1_confirmatory.svg").write_text(svg(height, body, "Confirmatory tests"), encoding="utf-8")


# ---------------------------------------------------------------- figure 2

def fig2(data, out):
    blocks = [b for b in data.get("probe_pairing", []) if b["arm"] == "A"]
    rows_csv = []
    left, right, row_h, head = 190, 20, 19, 30
    height = 34 + sum(head + row_h * len(b["rows"]) + 34 for b in blocks) + 40
    body = [text(8, 18, "Stated probability that the reviewer is right vs answer-only flip rate (arm A, target key)",
                 12, weight="bold")]
    x0, x1 = left, W - right

    def X(v):
        return x0 + v * (x1 - x0)

    y = 34
    for b in blocks:
        body.append(text(8, y + 16, short_model(b["model"]), 12, weight="bold"))
        y += head
        for r in b["rows"]:
            yc = y + row_h / 2
            body.append(text(left - 16, yc + 4, f"{r['tone']} objection, {FIG3_LABEL.get(r['log'], r['log'])}", 11, "end"))
            body.append(line(x0, yc, x1, yc, GREY2, 0.5))
            sp = r["mean_stated_probability"]
            fr = (r["flips_key"] / r["n_key"]) if r["flips_key"] is not None and r["n_key"] else None
            if sp is not None and fr is not None:
                body.append(line(X(sp), yc, X(fr), yc, GREY1, 1.2))
            if fr is not None and r["n_key"] >= MIN_N:
                body.append(circle(X(fr), yc, 4, ACCENT))
            if sp is not None:  # hollow ring drawn last and larger, so a coinciding flip dot stays visible inside it
                body.append(circle(X(sp), yc, 6, "none", BLACK, 1.4))
            rows_csv.append([b["model"], r["log"], r["tone"], sp, r["probe_n"], r["flips_key"], r["n_key"], fr,
                             r["flips_distractor"], r["n_distractor"]])
            y += row_h
        body.append(line(x0, y, x1, y))
        for t in (0, 0.25, 0.5, 0.75, 1):
            body.append(line(X(t), y, X(t), y + 4))
            body.append(text(X(t), y + 16, f"{t:g}", 11, "middle"))
        y += 34
    body += [circle(16, y + 6, 6, "none", BLACK, 1.4), text(26, y + 10, "stated probability (probe)", 11),
             circle(206, y + 6, 4, ACCENT), text(216, y + 10, "flip rate, answer-only, target key", 11),
             text(8, y + 28, "Model-was-wrong items: the reviewer names the key, so following is correct.", 11)]
    write_csv(out / "fig2_state_vs_act.csv",
              ["model", "log", "tone", "stated_probability", "probe_n", "flips_key", "n_key", "flip_rate_key",
               "flips_distractor", "n_distractor"], rows_csv)
    (out / "fig2_state_vs_act.svg").write_text(svg(height, body, "Stated vs acted"), encoding="utf-8")


# ---------------------------------------------------------------- figure 3

def fig3(data, out):
    groups = {k: v for k, v in data["groups"].items()
              if v["group"]["mode"] == "instant" and v["group"]["arm"] == "A" and v["group"]["stratum"] == "wrong"
              and v["group"]["target"] == "key"}
    models = sorted(v["group"]["model"] for v in groups.values())
    rows_csv = []
    cols = 2
    pw, ph = W / cols, 250
    nrow = (len(models) + cols - 1) // cols
    height = 30 + nrow * ph + 40
    body = [text(8, 18, "Answer-only flip rate across logs (arm A, target key, model-was-wrong items)", 12, weight="bold")]
    for idx, m in enumerate(models):
        g = next(v for v in groups.values() if v["group"]["model"] == m)
        cells = {(c["log"], c["tone"]): c for c in g["cells"]}
        ox, oy = (idx % cols) * pw, 30 + (idx // cols) * ph
        l, r, t, b = ox + 44, ox + pw - 14, oy + 26, oy + ph - 92
        body.append(text(ox + pw / 2, oy + 14, short_model(m), 12, "middle", "bold"))

        def X(i):
            return l + i * (r - l) / (len(FIG3_LOGS) - 1)

        def Y(v):
            return b - v * (b - t)

        body.append(line(l, b, r, b))
        body.append(line(l, t, l, b))
        for v in (0, 0.5, 1):
            body.append(line(l - 4, Y(v), l, Y(v)))
            body.append(text(l - 7, Y(v) + 4, f"{v:g}", 11, "end"))
            if v:
                body.append(line(l, Y(v), r, Y(v), GREY2, 0.5))
        for i, lg in enumerate(FIG3_LOGS):
            body.append(line(X(i), b, X(i), b + 4))
            body.append(text(X(i) + 3, b + 12, FIG3_LABEL[lg], 11, "end", rotate=-50))
        for tone, col, dash in (("certain", BLACK, None), ("unsure", ACCENT, "5 3")):
            pts = []
            for i, lg in enumerate(FIG3_LOGS):
                c = cells.get((lg, tone))
                rate = c["flips"] / c["n"] if c and c["run"] and c["n"] else None
                rows_csv.append([m, lg, tone, c["flips"] if c else "", c["n"] if c else 0, rate,
                                 int(rate is not None and c["n"] >= MIN_N)])
                pts.append((X(i), Y(rate)) if rate is not None and c["n"] >= MIN_N else None)
            seg = []
            for p in pts + [None]:
                if p is None:
                    if len(seg) > 1:
                        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in seg)
                        dd = f" stroke-dasharray=\"{dash}\"" if dash else ""
                        body.append(f"<polyline points=\"{d}\" fill=\"none\" stroke=\"{col}\" stroke-width=\"1.6\"{dd}/>")
                    seg = []
                else:
                    seg.append(p)
            for p in pts:
                if p:
                    body.append(circle(p[0], p[1], 2.8, col))
    ly = 30 + nrow * ph + 14
    body += [line(14, ly - 4, 40, ly - 4, BLACK, 1.6), text(46, ly, "certain objection", 11),
             line(170, ly - 4, 196, ly - 4, ACCENT, 1.6, "5 3"), text(202, ly, "unsure objection", 11),
             text(8, ly + 18, f"Logs not run, or with fewer than {MIN_N} items, are left out (gaps in the lines).", 11)]
    write_csv(out / "fig3_logs.csv", ["model", "log", "tone", "flips", "n", "flip_rate", "drawn"], rows_csv)
    (out / "fig3_logs.svg").write_text(svg(height, body, "Flip rate across logs"), encoding="utf-8")


def fig4(data, out):
    """Per model (answer-only): d_c and d_u under arm A (black) and arm M (accent), same items, paired."""
    blocks = [b for b in data["mitigation"] if b["mode"] == "instant"]
    models = sorted(b["model"] for b in blocks)
    st = {(b["model"], r["stat"]): r for b in blocks for r in b["stats"]}
    rows_csv = [[m, s, r["n"], r.get("A"), *(r.get("ci_A") or ["", ""]), r.get("M"), *(r.get("ci_M") or ["", ""]),
                 r.get("change"), *(r.get("ci_change") or ["", ""]), int(r["n"] >= MIN_N)]
                for (m, s), r in sorted(st.items())]
    write_csv(out / "fig4_mitigation.csv", ["model", "statistic", "n", "arm_A", "A_lo", "A_hi", "arm_M", "M_lo", "M_hi",
                                            "change", "change_lo", "change_hi", "drawn"], rows_csv)
    vals = [v for r in st.values() if r["n"] >= MIN_N and r["stat"] in ("d_c", "d_u")
            for v in (r["ci_A"] or []) + (r["ci_M"] or [])]
    lo = min([-0.25] + vals)
    hi = max([0.5] + vals)
    lo, hi = -0.25 * ((-lo + 0.2499) // 0.25), 0.25 * ((hi + 0.2499) // 0.25)
    left, right, top, row_h = 140, 12, 62, 40
    panels = (("d_c", "certain-voice record", "effect (d_c)"), ("d_u", "unsure-voice record", "effect (d_u)"))
    pw = (W - left - right) / len(panels)
    gap = 40
    ybot = top + row_h * len(models)
    height = ybot + 74
    body = [text(8, 18, "Mitigation instruction (arm M) vs arm A, answer-only, target key, same items", 12, weight="bold")]

    def X(k, v):
        return left + k * pw + gap / 2 + (v - lo) / (hi - lo) * (pw - gap)

    ticks = [t / 2 for t in range(int(lo * 2), int(hi * 2) + 1)]
    for k, (_, a, b) in enumerate(panels):
        cx = left + k * pw + pw / 2
        body += [text(cx, top - 22, a, 11, "middle", "bold"), text(cx, top - 8, b, 11, "middle", "bold"),
                 line(X(k, lo), ybot, X(k, hi), ybot), line(X(k, 0), top - 2, X(k, 0), ybot, GREY1, 1, "3 3")]
        for t in ticks:
            body.append(line(X(k, t), ybot, X(k, t), ybot + 4))
            body.append(text(X(k, t), ybot + 16, f"{t:g}", 11, "middle"))
    for j, m in enumerate(models):
        yc = top + row_h * j + row_h / 2
        body.append(text(left - 8, yc + 4, short_model(m), 12, "end"))
        if j:
            body.append(line(8, top + row_h * j, W - right, top + row_h * j, GREY2, 0.5))
        for k, (s, _, _) in enumerate(panels):
            r = st.get((m, s))
            if not r or r["n"] < MIN_N:
                continue
            ya, ym = yc - 6, yc + 6
            body.append(line(X(k, r["A"]), ya, X(k, r["M"]), ym, GREY2, 1))
            body.append(line(X(k, r["ci_A"][0]), ya, X(k, r["ci_A"][1]), ya, BLACK, 1.4))
            body.append(line(X(k, r["ci_M"][0]), ym, X(k, r["ci_M"][1]), ym, ACCENT, 1.4))
            body.append(circle(X(k, r["A"]), ya, 3.6, BLACK))
            body.append(circle(X(k, r["M"]), ym, 3.6, ACCENT))
    ly = ybot + 40
    body += [circle(16, ly - 4, 3.6, BLACK), text(26, ly, "arm A", 11),
             circle(96, ly - 4, 3.6, ACCENT), text(106, ly, "arm M (mitigation instruction)", 11),
             text(8, ly + 18, f"Dot: estimate on items non-missing under both arms; bar: 95% item bootstrap interval. "
                              f"Not drawn when n < {MIN_N}.", 11)]
    (out / "fig4_mitigation.svg").write_text(svg(height, body, "Mitigation"), encoding="utf-8")


HOSTED_PREFIXES = ("openai:", "anthropic:", "google:")


def model_class(model, tier):
    if tier and "recency" in tier:
        return "recency"
    return "hosted" if model.startswith(HOSTED_PREFIXES) else "open"


def label_name(model):
    name = model.split(":", 1)[1] if ":" in model and not model.split(":", 1)[1][:1].isdigit() else model
    return name.split("/")[-1]


def fig5(data, out):
    """One point per model: x = d_c, y = d_u (answer-only, arm A, stratum wrong, target key), with the 95%
    item-bootstrap intervals of the by-voice statistics (the same resamples as the confirmatory section)."""
    pts = []
    for v in data["groups"].values():
        g = v["group"]
        if (g["mode"], g["arm"], g["stratum"], g["target"]) != ("instant", "A", "wrong", "key"):
            continue
        bv = v["contrasts"]["all"]["by_voice_main"]
        dc, du = bv["d_c"], bv["d_u"]
        pts.append({"model": g["model"], "tier": v.get("tier", "main"), "cls": model_class(g["model"], v.get("tier")),
                    "n": dc["n"], "d_c": dc["diff"], "dc_lo": (dc["ci95"] or [None, None])[0],
                    "dc_hi": (dc["ci95"] or [None, None])[1], "d_u": du["diff"],
                    "du_lo": (du["ci95"] or [None, None])[0], "du_hi": (du["ci95"] or [None, None])[1]})
    pts.sort(key=lambda p: p["model"])
    write_csv(out / "fig5_profiles.csv", ["model", "tier", "class", "n", "d_c", "d_c_lo", "d_c_hi", "d_u", "d_u_lo",
                                          "d_u_hi", "drawn"],
              [[p["model"], p["tier"], p["cls"], p["n"], p["d_c"], p["dc_lo"], p["dc_hi"], p["d_u"], p["du_lo"],
                p["du_hi"], int(p["n"] >= MIN_N and p["d_c"] is not None)] for p in pts])
    draw = [p for p in pts if p["n"] >= MIN_N and p["d_c"] is not None]
    vals = [v for p in draw for v in (p["dc_lo"], p["dc_hi"], p["du_lo"], p["du_hi"]) if v is not None]
    lo = min([-0.25] + vals)
    hi = max([0.75] + vals)
    lo, hi = -0.25 * ((-lo + 0.2499) // 0.25), 0.25 * ((hi + 0.2499) // 0.25)
    l, t, size = 70, 40, 440
    r, b = l + size, t + size
    height = b + 120

    def X(v):
        return l + (v - lo) / (hi - lo) * size

    def Y(v):
        return b - (v - lo) / (hi - lo) * size

    body = [text(8, 18, "Record effect by voice, answer-only, arm A, model-was-wrong items (target key)", 12, weight="bold"),
            f"<rect x=\"{l}\" y=\"{t}\" width=\"{size}\" height=\"{size}\" fill=\"none\" stroke=\"{BLACK}\" stroke-width=\"1\"/>",
            line(X(max(lo, lo)), Y(lo), X(hi), Y(hi), GREY2, 1, "4 3"),
            line(X(lo), Y(0), X(hi), Y(0), GREY2, 1), line(X(0), Y(lo), X(0), Y(hi), GREY2, 1),
            text(X(hi) - 4, Y(hi) + 14, "y = x", 11, "end", fill=GREY1)]
    ticks = [k / 4 for k in range(int(lo * 4), int(hi * 4) + 1)]
    for v in ticks:
        body += [line(X(v), b, X(v), b + 4), text(X(v), b + 17, f"{v:g}", 11, "middle"),
                 line(l - 4, Y(v), l, Y(v)), text(l - 7, Y(v) + 4, f"{v:g}", 11, "end")]
    body += [text(l + size / 2, b + 36, "certain-voice record effect d_c (certain|certain_right - certain|unsure_right)",
                  11, "middle"),
             text(18, t + size / 2, "unsure-voice record effect d_u (unsure|unsure_right - unsure|certain_right)", 11,
                  "middle", rotate=-90)]
    style = {"open": ("circle", BLACK), "hosted": ("square", GREY1), "recency": ("triangle", ACCENT)}

    def marker(cls, x, y):
        shape, col = style[cls]
        if shape == "circle":
            return circle(x, y, 4.5, col)
        if shape == "square":
            return f"<rect x=\"{x - 4.2:.1f}\" y=\"{y - 4.2:.1f}\" width=\"8.4\" height=\"8.4\" fill=\"{col}\"/>"
        return f"<polygon points=\"{x:.1f},{y - 5.5:.1f} {x - 5:.1f},{y + 4:.1f} {x + 5:.1f},{y + 4:.1f}\" fill=\"{col}\"/>"

    for p in draw:
        x, y = X(p["d_c"]), Y(p["d_u"])
        col = style[p["cls"]][1]
        if p["dc_lo"] is not None:
            body.append(line(X(p["dc_lo"]), y, X(p["dc_hi"]), y, col, 0.9))
        if p["du_lo"] is not None:
            body.append(line(x, Y(p["du_lo"]), x, Y(p["du_hi"]), col, 0.9))
    for p in draw:
        body.append(marker(p["cls"], X(p["d_c"]), Y(p["d_u"])))
    # labels: try right, left, above, below of the point; skip positions that overlap earlier labels or points
    boxes = [(X(p["d_c"]) - 5, Y(p["d_u"]) - 5, X(p["d_c"]) + 5, Y(p["d_u"]) + 5) for p in draw]
    for p in sorted(draw, key=lambda p: (-p["d_u"], p["d_c"])):
        x, y, s = X(p["d_c"]), Y(p["d_u"]), label_name(p["model"])
        w = 6.6 * len(s) + 4
        cands = [(x + 8, y + 4, "start"), (x - 8, y + 4, "end"), (x, y - 9, "middle"), (x, y + 17, "middle"),
                 (x + 8, y - 8, "start"), (x + 8, y + 16, "start"), (x - 8, y - 8, "end"), (x - 8, y + 16, "end")]
        cands += [(x + dx, y + dy, anc) for dy in (-22, 28, -36, 42) for dx, anc in ((0, "middle"), (8, "start"), (-8, "end"))]

        def overlap(box):
            return sum(max(0, min(box[2], q[2]) - max(box[0], q[0])) * max(0, min(box[3], q[3]) - max(box[1], q[1]))
                       for q in boxes)

        best = None
        for cx, cy, anc in cands:
            x0 = cx if anc == "start" else cx - w if anc == "end" else cx - w / 2
            box = (x0, cy - 10, x0 + w, cy + 2)
            inside = box[0] >= l and box[2] <= r and box[1] >= t and box[3] <= b
            score = overlap(box) + (0 if inside else 1e6)
            if best is None or score < best[0]:
                best = (score, (cx, cy, anc), box)
            if score == 0:
                break
        _, chosen, box = best
        boxes.append(box)
        if abs(chosen[1] - 4 - y) > 20:  # far placement: thin leader line to the point
            body.append(line(x, y, chosen[0], chosen[1] + (-12 if chosen[1] > y else 2), GREY2, 0.8))
        body.append(text(chosen[0], chosen[1], s, 11, chosen[2]).replace("<text ", "<text stroke=\"#ffffff\" stroke-width=\"3\" paint-order=\"stroke\" ", 1))
    ly = b + 62
    body += [marker("open", 16, ly - 4), text(26, ly, "open-weight (Ollama, OpenRouter, DeepSeek)", 11),
             marker("hosted", 300, ly - 4), text(310, ly, "hosted (OpenAI, Anthropic, Google)", 11),
             marker("recency", 16, ly + 14), text(26, ly + 18, "recency tier (exploratory)", 11),
             text(8, ly + 36, f"Bars: 95% item-bootstrap intervals. Models with fewer than {MIN_N} items are not drawn.", 11)]
    (out / "fig5_profiles.svg").write_text(svg(height, body, "Record effect by voice"), encoding="utf-8")


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--out-dir", default=str(HERE / "figures"))
    a = ap.parse_args(argv)
    data = json.loads(Path(a.json).read_text(encoding="utf-8"))
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if not data.get("confirmatory"):
        raise SystemExit("JSON has no `confirmatory` block; produce it with analyze.py --summary")
    fig1(data, out)
    if data.get("probe_pairing"):
        fig2(data, out)
    else:
        print("no probe_pairing in the JSON (run analyze.py with probe files); figure 2 skipped")
    fig3(data, out)
    if any(b["mode"] == "instant" for b in data.get("mitigation") or []):
        fig4(data, out)
    else:
        print("no answer-only arm M data in the JSON; figure 4 skipped")
    fig5(data, out)
    for f in sorted(out.iterdir()):
        print("wrote", f)


if __name__ == "__main__":
    main()
