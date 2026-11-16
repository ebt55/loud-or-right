"""Reusable, parameterised visual components (plan.md section 0 styles). Each draws onto a gfx.Canvas from an
explicit state (alpha, positions, progress); scenes compute the state from cue times.

- wordmark, legend, caveat chip, pill (arm tag, scorecards, stamp)
- answer card, speech bubble (certain: solid 4 px outline, bold; unsure: dashed 2 px outline, italic)
- right/wrong chips (ink tick on pale grey, crimson cross on pale red), mini voice glyphs
- practice-log card with rows keyed by entry (reorder, flip, highlight, padlocks, row-1 expansion)
- profile scatter (markers, ghosts, hollow outlines, trails, rings, pulses, labels)
- dot strip (scene 8), interval strip (scene 7), grid of 160 (scene 9), horizontal bars, meter, knot, padlock
- credits screen built from plan.md's exact text
"""
import math
import re

from PIL import Image, ImageDraw

import config as C
import data as D
import gfx as G
from easing import in_out_cubic, lerp, out_back, out_cubic, prog


# ---------------------------------------------------------------- overlays and chips

def wordmark(cv, alpha=1.0, x=C.MARGIN, y=50, size=36):
    if alpha <= 0:
        return
    s = G.text("Loud or Right?", size, "bold", C.INK, count=False)
    cv.paste(s, x, y, alpha)


def legend(cv, alpha=1.0, right=C.W - C.MARGIN, y=992, size=28):
    """Three-item class legend, right-aligned on one line (chart furniture: not counted as words)."""
    if alpha <= 0:
        return
    items = [("open", "Open-weight"), ("closed", "Closed"), ("recency", "Newer open-weight (exploratory)")]
    sprites = [G.text(lbl, size, "regular", C.INK2, count=False) for _, lbl in items]
    ms = 24
    total = sum(ms + 12 + s.size[0] for s in sprites) + 36 * (len(items) - 1)
    x = right - total
    for (cls, _), sp in zip(items, sprites):
        st = C.CLASS_STYLE[cls]
        cv.paste(G.marker(st["marker"], ms + (2 if st["marker"] == "^" else 0), st["fill"], st["edge"], 2), x + ms / 2,
                 y, alpha, "mm", check_safe=False)
        cv.paste(sp, x + ms + 12, y - 2, alpha, "lm")
        x += ms + 12 + sp.size[0] + 36


def pill_sprite(text_, size=C.SIZE_CHIP, style="semibold", color=C.INK, fill=C.CARD, edge=C.CARD_EDGE, ew=2,
                padx=26, pady=10, radius=None, count=True):
    ts = G.text(text_, size, style, color, count=count)
    w, h = int(ts.size[0] + 2 * padx), int(ts.size[1] + 2 * pady)
    key = ("pill", text_, size, style, G.rgba(color), G.rgba(fill) if fill else None, G.rgba(edge) if edge else None,
           ew, padx, pady, radius)

    def make():
        bg = G.rounded_rect(w, h, radius if radius is not None else h // 2, fill or (0, 0, 0, 0), edge, ew, 0)
        img = bg.copy()
        img.alpha_composite(ts, dest=(padx, pady))
        img.info.update({"words": ts.info["words"], "text": text_, "is_text": True,
                         "ink_bbox": (0, 0, w, h)})
        return img
    return G.cached(key, make)


def caveat_chip(cv, text_, alpha=1.0, x=C.MARGIN, y=992, size=C.SIZE_CHIP, anchor="lm"):
    """The one caveat style: grey outline, grey text, rounded, bottom left by default."""
    if alpha <= 0:
        return
    sp = pill_sprite(text_, size, "regular", C.INK2, fill=C.BG, edge=C.INK2, ew=2, padx=22, pady=8, radius=16)
    cv.paste(sp, x, y, alpha, anchor)


def pill(cv, text_, x, y, alpha=1.0, anchor="lt", scale=1.0, **kw):
    if alpha <= 0:
        return
    sp = pill_sprite(text_, **kw)
    w, h = sp.size
    ax = {"l": 0, "m": w / 2, "r": w}[anchor[0]]
    ay = {"t": 0, "m": h / 2, "b": h}[anchor[1]]
    if abs(scale - 1) > 0.004:
        cv.paste(sp, x - ax, y - ay, 0)  # safe-area check only
        cv.paste_scaled(sp, x - ax + w / 2, y - ay + h / 2, scale, alpha)
    else:
        cv.paste(sp, x, y, alpha, anchor)


# ---------------------------------------------------------------- answer card

def answer_card(cv, x, y, label, value, alpha=1.0, scale=1.0, mark=None, w=None, value_size=72, anchor="lt",
                value_color=C.INK):
    """Card with a small label line and a large value ('Model's answer:' / 'F'). mark: 'right' adds a tick chip."""
    if alpha <= 0:
        return None
    lab = G.text(label, 38, "semibold", C.INK2)
    val = G.text(value, value_size, "bold", value_color)
    inner_w = max(lab.size[0], val.size[0] + (70 if mark else 0))
    cw = int(w or inner_w + 80)
    ch = int(lab.size[1] + val.size[1] + 64)
    key = ("answer_card", label, value, cw, ch, mark, value_size, G.rgba(value_color))

    def make():
        bg = G.rounded_rect(cw, ch, 24, C.CARD, C.CARD_EDGE, 2, 14)
        pad = bg.info["pad"]
        img = bg.copy()
        img.alpha_composite(lab, dest=(pad + 40, pad + 26))
        img.alpha_composite(val, dest=(pad + 40, pad + 26 + lab.size[1] + 6))
        if mark:
            chip = mark_chip(mark == "right", 56)
            img.alpha_composite(chip, dest=(pad + 40 + val.size[0] + 18,
                                            pad + 26 + lab.size[1] + 6 + (val.size[1] - 56) // 2 + 6))
        img.info.update({"pad": pad, "words": lab.info["words"] + val.info["words"]})
        return img
    img = G.cached(key, make)
    pad = img.info["pad"]
    ax = {"l": 0, "m": cw / 2, "r": cw}[anchor[0]]
    ay = {"t": 0, "m": ch / 2, "b": ch}[anchor[1]]
    cx, cy = x - ax + cw / 2, y - ay + ch / 2
    _check_box(cv, cx - cw * scale / 2, cy - ch * scale / 2, cx + cw * scale / 2, cy + ch * scale / 2, label, alpha)
    cv.paste_scaled(img, cx, cy, scale, alpha)
    return (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)


def _check_box(cv, x0, y0, x1, y1, label, a):
    if a <= 0.05:
        return
    sx0, sy0, sx1, sy1 = C.SAFE
    if x0 < sx0 - 1 or y0 < sy0 - 1 or x1 > sx1 + 1 or y1 > sy1 + 1:
        msg = f"box {label!r} at ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f}) leaves the safe area"
        cv.safe_violations.append(msg)
        if cv.strict:
            raise G.SafeAreaError(msg)


# ---------------------------------------------------------------- chips and glyphs

def mark_chip(hit, size=48):
    """Right: ink tick on a pale grey chip. Wrong: crimson cross on a pale red chip."""
    key = ("chip", bool(hit), size)

    def make():
        bg = G.rounded_rect(size, size, max(6, size // 5), C.CHECK_CHIP if hit else C.CROSS_CHIP, None, 0, 0).copy()
        ic = G.check_icon(int(size * 0.8), C.CHECK, size * 0.12) if hit else G.cross_icon(int(size * 0.8), C.CROSS,
                                                                                           size * 0.12)
        bg.alpha_composite(ic, dest=(int(size * 0.1), int(size * 0.1)))
        return bg
    return G.cached(key, make)


def _bubble_shape(dr, s, x0, y0, x1, y1, r, voice, width, tail_x, tail_w, tail_h, fill=C.CARD, color=C.INK):
    """Bubble outline + tail at the bottom-left. certain: solid; unsure: dashed."""
    dr.rounded_rectangle((x0 * s, y0 * s, x1 * s, y1 * s), radius=r * s, fill=G.rgba(fill))
    tail = [(tail_x, y1 - 1), (tail_x + tail_w, y1 - 1), (tail_x - tail_w * 0.35, y1 + tail_h)]
    dr.polygon([(px * s, py * s) for px, py in tail], fill=G.rgba(fill))
    path = G.rrect_path(x0, y0, x1, y1, r)
    # cut the outline where the tail joins the bottom edge: draw the path, then cover the joint with fill
    if voice == "certain":
        dr.line([(px * s, py * s) for px, py in path], fill=G.rgba(color), width=int(round(width * s)), joint="curve")
    else:
        G.dash_polyline(dr, path, s, color, width, dash=max(6, width * 5), gap=max(5, width * 3.5))
    dr.line([((tail_x + width) * s, y1 * s), ((tail_x + tail_w - width) * s, y1 * s)], fill=G.rgba(fill),
            width=int(round((width + 1.5) * s)))
    if voice == "certain":
        dr.line([(tail_x * s, y1 * s), (tail[2][0] * s, tail[2][1] * s), ((tail_x + tail_w) * s, y1 * s)],
                fill=G.rgba(color), width=int(round(width * s)), joint="curve")
    else:
        G.dash_polyline(dr, [(tail_x, y1), tail[2], (tail_x + tail_w, y1)], s, color, width, max(6, width * 4),
                        max(5, width * 3))


def voice_glyph(voice, w=54):
    """Mini speech bubble for log rows: certain = solid thick outline with heavy text bars; unsure = dashed thin
    outline with light bars."""
    key = ("glyph", voice, w)

    def make():
        h = int(w * 0.78)
        tot_h = h + int(w * 0.22)

        def fn(dr, s):
            ew = max(2.5, w * 0.075) if voice == "certain" else max(1.6, w * 0.04)
            _bubble_shape(dr, s, ew, ew, w - ew, h - ew, h * 0.28, voice, ew, w * 0.22, w * 0.2, w * 0.18)
            bar = G.rgba(C.INK) if voice == "certain" else G.rgba(C.INK2)
            bw = w * 0.085 if voice == "certain" else w * 0.04
            for k, frac in enumerate((0.62, 0.42)):
                yy = h * (0.36 + 0.24 * k)
                dr.line([(w * 0.22 * s, yy * s), (w * (0.22 + frac) * s, yy * s)], fill=bar, width=int(bw * s))
        return G.ss_sprite(w, tot_h, fn)
    return G.cached(key, make)


def padlock(size=26, color=C.INK2):
    key = ("padlock", size, G.rgba(color))

    def make():
        def fn(dr, s):
            bw, bh = size * 0.78, size * 0.5
            x0, y0 = (size - bw) / 2, size * 0.45
            dr.rounded_rectangle((x0 * s, y0 * s, (x0 + bw) * s, (y0 + bh) * s), radius=size * 0.08 * s,
                                 fill=G.rgba(color))
            r = size * 0.24
            cx = size / 2
            dr.arc(((cx - r) * s, (y0 - r - size * 0.02) * s, (cx + r) * s, (y0 + r) * s), 180, 360,
                   fill=G.rgba(color), width=int(size * 0.1 * s))
            dr.line([((cx - r) * s + size * 0.05 * s, (y0 - size * 0.02) * s), ((cx - r) * s + size * 0.05 * s,
                                                                               (y0 + 2) * s)],
                    fill=G.rgba(color), width=int(size * 0.1 * s))
            dr.line([((cx + r) * s - size * 0.05 * s, (y0 - size * 0.02) * s), ((cx + r) * s - size * 0.05 * s,
                                                                               (y0 + 2) * s)],
                    fill=G.rgba(color), width=int(size * 0.1 * s))
        return G.ss_sprite(size, size, fn)
    return G.cached(key, make)


def knot(w=120, color=C.INK2, bg=C.BG):
    """A trefoil knot (three crossings, alternating over and under), drawn as one thick strand."""
    key = ("knot", w, G.rgba(color))

    def make():
        n = 360
        raw = []
        for i in range(n + 1):
            a = 2 * math.pi * i / n
            raw.append((math.sin(a) + 2 * math.sin(2 * a), math.cos(a) - 2 * math.cos(2 * a)))
        xs, ys = [p[0] for p in raw], [p[1] for p in raw]
        sc = (w * 0.86) / (max(xs) - min(xs))
        h = int((max(ys) - min(ys)) * sc + w * 0.14)
        pts = [((x - min(xs)) * sc + w * 0.07, (max(ys) - y) * sc + w * 0.07) for x, y in raw]
        lw = w * 0.07
        # crossings: segment pairs that intersect
        def seg_x(p1, p2, p3, p4):
            def o(a, b, c):
                return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            return o(p3, p4, p1) * o(p3, p4, p2) < 0 and o(p1, p2, p3) * o(p1, p2, p4) < 0
        cross = []
        for i in range(n):
            for j in range(i + 8, n):
                if i == 0 and j == n - 1:
                    continue
                if seg_x(pts[i], pts[i + 1], pts[j], pts[j + 1]):
                    cross.append((i, j))
        events = sorted([(i, k) for k, (i, j) in enumerate(cross)] + [(j, k) for k, (i, j) in enumerate(cross)])
        over = []
        for m, (idx, k) in enumerate(events):
            if m % 2 == 0:
                over.append(idx)

        def fn(dr, s):
            P = [(x * s, y * s) for x, y in pts]
            dr.line(P, fill=G.rgba(color), width=int(lw * s), joint="curve")
            for idx in over:
                lo, hi = max(0, idx - 10), min(n, idx + 11)
                seg = P[lo:hi + 1]
                dr.line(seg, fill=G.rgba(bg), width=int((lw + w * 0.07) * s), joint="curve")
                dr.line(seg, fill=G.rgba(color), width=int(lw * s), joint="curve")
        return G.ss_sprite(w, h, fn)
    return G.cached(key, make)


# ---------------------------------------------------------------- speech bubble

class Bubble:
    """Speech bubble: voice 'certain' (solid 4 px outline, bold text) or 'unsure' (dashed 2 px outline, italic).
    speaker: optional name shown beside a small avatar under the tail."""

    def __init__(self, text_, voice="certain", size=44, max_width=720, speaker=None):
        self.text, self.voice, self.size, self.speaker = text_, voice, size, speaker
        self.ts = G.text(text_, size, "bold" if voice == "certain" else "italic", C.INK, max_width=max_width)
        self.padx, self.pady = 38, 24
        self.w = int(self.ts.size[0] + 2 * self.padx)
        self.h = int(self.ts.size[1] + 2 * self.pady)
        self.tail_h = 30

    def sprite(self):
        key = ("bubble", self.text, self.voice, self.size, self.w, self.h, self.speaker)

        def make():
            m = 8
            W_, H_ = self.w + 2 * m, self.h + self.tail_h + 2 * m

            def fn(dr, s):
                ew = 4 if self.voice == "certain" else 2
                _bubble_shape(dr, s, m, m, m + self.w, m + self.h, 28, self.voice, ew, m + 44, 40, self.tail_h)
            img = G.ss_sprite(W_, H_, fn).copy()
            img.alpha_composite(self.ts, dest=(m + self.padx, m + self.pady - 2))
            img.info.update({"words": self.ts.info["words"], "m": m, "text": self.text})
            return img
        return G.cached(key, make)

    def draw(self, cv, x, y, alpha=1.0, scale=1.0):
        """(x, y) = top-left of the bubble body at scale 1; scales about the tail tip."""
        if alpha <= 0:
            return
        sp = self.sprite()
        m = sp.info["m"]
        tipx, tipy = x + 44 - 14, y + self.h + self.tail_h
        cx = x - m + sp.size[0] / 2
        cy = y - m + sp.size[1] / 2
        _check_box(cv, x, y, x + self.w, y + self.h, self.text, alpha if scale > 0.98 else 0)
        cv.paste_scaled(sp, tipx + (cx - tipx) * scale, tipy + (cy - tipy) * scale, scale, alpha)
        if self.speaker:
            av = 56
            ax_, ay_ = tipx - 10 + (0), tipy + 12
            cv.paste(G.circle(av, (72, 76, 98)), ax_ - av / 2, ay_, alpha, check_safe=False)
            ini = G.text(self.speaker[0], 32, "semibold", (255, 255, 255), count=False)
            cv.paste(ini, ax_, ay_ + av / 2 - 2, alpha, "mm", check_safe=False)
            nm = G.text(self.speaker, 36, "semibold", C.INK2)
            cv.paste(nm, ax_ + av / 2 + 14, ay_ + av / 2 - 2, alpha, "lm")


# ---------------------------------------------------------------- practice-log card (rows keyed by entry)

class LogCard:
    """Rows are keyed by entry number k (0..7); each entry keeps its voice glyph and chip, and moves between slots.
    Row numbers (1..8) belong to the slots (display positions)."""

    def __init__(self, voices=D.LOG_VOICES, w=520, row_h=62, header="Practice log: reviewer Dana", header_size=36,
                 footer_size=36, numbers=True):
        self.voices = list(voices)
        self.w, self.row_h, self.header, self.hs, self.fs, self.numbers = w, row_h, header, header_size, footer_size, numbers

    def dims(self, st):
        k = st.get("k", 1.0)
        return dict(k=k, w=int(round(st.get("w", self.w))), row_h=self.row_h * k, glyph=int(round(54 * k)),
                    chip=int(round(46 * k)), num=max(28, int(round(30 * k))), gx=int(round((96 if self.numbers else 30) * k)))

    def height(self, st):
        d = self.dims(st)
        header = st.get("header", True) and self.header
        hh = (self.hs + 44) if header else 22 * d["k"] + 6
        fh = (self.fs + 40) if st.get("footer") is not None else 16 * d["k"] + 4
        return int(hh + 8 * d["row_h"] + st.get("expand", 0.0) * 56 + fh)

    def render(self, st):
        """st keys (all optional): header (bool), footer (str), footer_alpha, slots {k: slot}, row_alpha {k: a},
        hits {k: 0/1}, hits_from {k: 0/1}, flip (0..1), chip_alpha {k: a}, hl (alpha of the row-1 box),
        lock (padlock alpha), expand (0..1), expand_text, glyph1 (row-1 glyph scale), k (size factor), w (width)."""
        d = self.dims(st)
        W_, row_h = d["w"], d["row_h"]
        show_header = st.get("header", True) and self.header
        footer = st.get("footer")
        expand = st.get("expand", 0.0)
        H_ = self.height(st)
        bg = G.rounded_rect(W_, H_, int(22 * min(1, d["k"] + 0.1)), C.CARD, C.CARD_EDGE, 2, 12)
        pad = bg.info["pad"]
        img = bg.copy()
        words = 0
        top = pad + 22 * d["k"] + 6
        if show_header:
            hs = G.text(self.header, self.hs, "semibold", C.INK)
            img.alpha_composite(hs, dest=(pad + 28, pad + 16))
            words += hs.info["words"]
            top = pad + self.hs + 44
        slots = st.get("slots", {k: k for k in range(8)})
        row_alpha = st.get("row_alpha", {})
        hits = st.get("hits", {})
        hits_from = st.get("hits_from")
        flip = st.get("flip", 1.0)
        chip_alpha = st.get("chip_alpha", {})
        lock = st.get("lock", 0.0)
        extra = expand * 56

        def slot_y(sl):
            return top + sl * row_h + (extra if sl >= 0.999 else extra * max(0.0, sl))

        if st.get("hl", 0) > 0:
            hb = G.rounded_rect(W_ - 24, int(row_h + extra - 2), 12, (0, 0, 0, 0), C.INK, 3, 0)
            img.alpha_composite(G.with_alpha(hb, st["hl"]), dest=(pad + 12, int(top + 1)))
        if self.numbers:
            for sl in range(8):
                y = slot_y(sl)
                ns = G.text(str(sl + 1), d["num"], "regular", C.INK2, count=False)
                nx = pad + 24 * d["k"]
                if lock > 0:
                    pl = padlock(24)
                    img.alpha_composite(G.with_alpha(pl, lock), dest=(int(nx - 4), int(y + (row_h - 24) / 2)))
                    nx += 28 * lock
                img.alpha_composite(ns, dest=(int(nx), int(y + (row_h - ns.size[1]) / 2 - 2)))
        gx = pad + d["gx"] + (12 * lock if self.numbers else 0)
        chip_cx = W_ - 30 * d["k"] - d["chip"] / 2
        for k in range(8):
            a = row_alpha.get(k, 1.0)
            if a <= 0.004:
                continue
            sl = slots.get(k, k)
            y = slot_y(sl)
            row = Image.new("RGBA", (W_, int(row_h + 60)), (0, 0, 0, 0))
            v = self.voices[k]
            gs = st.get("glyph1", 1.0) if abs(sl) < 0.01 else 1.0
            g = voice_glyph(v, int(round(d["glyph"] * gs)))
            row.alpha_composite(g, dest=(0, int((row_h - g.size[1] * 0.82) / 2)))
            ca = chip_alpha.get(k, 1.0 if k in hits else 0.0)
            if ca > 0 and k in hits:
                hit = hits[k]
                sx = 1.0
                if hits_from is not None and flip < 1.0:
                    if flip < 0.5:
                        hit = hits_from[k]
                        sx = 1 - flip * 2
                    else:
                        sx = (flip - 0.5) * 2
                chip = mark_chip(hit, d["chip"])
                if sx < 0.999:
                    chip = chip.resize((max(1, int(d["chip"] * sx)), d["chip"]), Image.BILINEAR)
                cxp = chip_cx - (gx - pad)
                row.alpha_composite(G.with_alpha(chip, ca), dest=(int(cxp - chip.size[0] / 2),
                                                                  int((row_h - d["chip"]) / 2)))
            img.alpha_composite(G.with_alpha(row, a), dest=(int(gx), int(y)))
            if abs(sl) < 0.01 and expand > 0 and st.get("expand_text"):
                et = G.text(st["expand_text"], 36, "semibold", C.INK)
                img.alpha_composite(G.with_alpha(et, prog(expand, 0.4, 0.6, lambda x: x) * a),
                                    dest=(int(pad + 26 * d["k"]), int(y + row_h - 2)))
                if expand > 0.5 and a > 0.5:
                    words += et.info["words"]
        if footer is not None:
            fa = st.get("footer_alpha", 1.0)
            fsp = G.text(footer, self.fs, "semibold", C.INK2)
            img.alpha_composite(G.with_alpha(fsp, fa), dest=(pad + 28, int(H_ + pad - self.fs - 34)))
            if fa > 0.5:
                words += fsp.info["words"]
        img.info.update({"pad": pad, "words": words, "card_h": H_, "card_w": W_})
        return img

    def draw(self, cv, st, x, y, alpha=1.0):
        """(x, y) = top-left of the card body."""
        if alpha <= 0:
            return None
        img = self.render(st)
        pad = img.info["pad"]
        cv.paste(img, x - pad, y - pad, alpha, check_safe=False)
        _check_box(cv, x, y, x + img.info["card_w"], y + img.info["card_h"], "log card", alpha)
        return (x, y, x + img.info["card_w"], y + img.info["card_h"])


# ---------------------------------------------------------------- profile scatter

class Scatter:
    def __init__(self, box=(900, 150, 720), lim=(-0.30, 1.02), ticks=(-0.25, 0, 0.25, 0.5, 0.75, 1.0),
                 xtitle="follows the certain voice's record", ytitle="follows the unsure voice's record",
                 diag_label="both records count equally", ms=30, tick_labels=(-0.25, 0, 1.0)):
        self.x0, self.y0, self.size = box
        self.lim, self.ticks = lim, ticks
        self.tick_labels = tick_labels      # plan.md: print only the axis range (-0.25 to 1); other ticks unlabelled
        self.xtitle, self.ytitle, self.diag_label = xtitle, ytitle, diag_label
        self.ms = ms

    def px(self, v):
        lo, hi = self.lim
        return (self.x0 + (v[0] - lo) / (hi - lo) * self.size, self.y0 + (1 - (v[1] - lo) / (hi - lo)) * self.size)

    @staticmethod
    def tick_str(v):
        if v == 0:
            return "0"
        return ("−" if v < 0 else "") + f"{abs(v):g}"

    def axes_sprite(self):
        key = ("sc_axes", self.x0, self.y0, self.size, self.lim, self.ticks, self.tick_labels)

        def make():
            img = Image.new("RGBA", (C.W, C.H), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            x0, y0, s = self.x0, self.y0, self.size
            zx, zy = self.px((0, 0))
            d.line([(zx, y0), (zx, y0 + s)], fill=G.rgba(C.REF), width=2)
            d.line([(x0, zy), (x0 + s, zy)], fill=G.rgba(C.REF), width=2)
            d.line([(x0, y0), (x0, y0 + s)], fill=G.rgba(C.INK2), width=2)
            d.line([(x0, y0 + s), (x0 + s, y0 + s)], fill=G.rgba(C.INK2), width=2)
            for tv in self.ticks:
                tx, _ = self.px((tv, 0))
                _, ty = self.px((0, tv))
                d.line([(tx, y0 + s), (tx, y0 + s + 9)], fill=G.rgba(C.INK2), width=2)
                d.line([(x0 - 9, ty), (x0, ty)], fill=G.rgba(C.INK2), width=2)
                if tv not in self.tick_labels:
                    continue
                lab = G.text(self.tick_str(tv), C.SIZE_TICK, "regular", C.INK2, count=False)
                img.alpha_composite(lab, dest=(int(tx - lab.size[0] / 2), int(y0 + s + 14)))
                img.alpha_composite(lab, dest=(int(x0 - 16 - lab.size[0]), int(ty - lab.size[1] / 2 - 2)))
            return img
        return G.cached(key, make)

    def xtitle_sprite(self):
        return G.no_count(G.text(self.xtitle, C.SIZE_CHART, "semibold", C.INK))

    def ytitle_sprite(self):
        key = ("sc_ytitle", self.ytitle)

        def make():
            yl = G.text(self.ytitle, C.SIZE_CHART, "semibold", C.INK)
            r = yl.rotate(90, expand=True, resample=Image.BICUBIC)
            r.info.update(yl.info)
            r.info["words"] = 0
            r.info["ink_bbox"] = r.getchannel("A").getbbox()
            return r
        return G.cached(key, make)

    def diag_sprite(self):
        return G.no_count(G.text(self.diag_label, C.SIZE_CHART - 2, "semibold", C.INK2))

    def draw_axes(self, cv, alpha=1.0, xt=1.0, yt=1.0, diag=1.0, diag_label=1.0):
        if alpha <= 0:
            return
        cv.paste(self.axes_sprite(), 0, 0, alpha, check_safe=False)
        if xt > 0:
            cv.paste(self.xtitle_sprite(), self.x0 + self.size / 2, self.y0 + self.size + 56, alpha * xt, "mt")
        if yt > 0:
            cv.paste(self.ytitle_sprite(), self.x0 - 78, self.y0 + self.size / 2, alpha * yt, "rm")
        if diag > 0:
            lo, hi = self.lim
            o = self.px((0, 0))
            G.dashed_line(cv, o, self.px((hi, hi)), C.INK2, width=3, alpha=alpha, progress=diag)
            G.dashed_line(cv, o, self.px((lo + 0.02, lo + 0.02)), C.INK2, width=3, alpha=alpha, progress=diag)
        if diag_label > 0:
            # horizontal, just left of the diagonal's top end (the upper-left of the plot is empty in every view)
            hi = self.lim[1]
            zx, _ = self.px((0, 0))
            _, ty = self.px((hi, hi))
            cv.paste(self.diag_sprite(), zx + 18, ty + 10, alpha * diag_label, "lm")

    def style(self, key):
        return C.CLASS_STYLE[D.CLASS[key]]

    def msize(self, key):
        return self.ms + (6 if self.style(key)["marker"] == "^" else 0)

    def marker(self, cv, key, pos, alpha=1.0, scale=1.0):
        if alpha <= 0.004:
            return
        st = self.style(key)
        x, y = self.px(pos)
        cv.paste_scaled(G.marker(st["marker"], self.msize(key), st["fill"], st["edge"], 2.2), x, y, scale, alpha)

    def ghost(self, cv, key, pos, alpha=1.0):
        """Pale grey ghost (plan: 20% opacity, no label)."""
        if alpha <= 0.004:
            return
        st = self.style(key)
        x, y = self.px(pos)
        cv.paste(G.marker(st["marker"], self.msize(key), (150, 150, 145), (120, 120, 115), 2), x, y, 0.2 * alpha, "mm",
                 check_safe=False)

    def outline(self, cv, key, pos, alpha=1.0):
        """Hollow outline: 2 px class colour, no fill."""
        if alpha <= 0.004:
            return
        st = self.style(key)
        x, y = self.px(pos)
        cv.paste(G.marker(st["marker"], self.msize(key), (0, 0, 0, 0), st["fill"], 2.0), x, y, alpha, "mm",
                 check_safe=False)

    def trail(self, cv, p0, p1, key, alpha=1.0):
        if alpha <= 0.004:
            return
        a, b = self.px(p0), self.px(p1)
        if math.hypot(b[0] - a[0], b[1] - a[1]) < 8:
            return
        G.line(cv, [a, b], self.style(key)["fill"], width=2, alpha=alpha * 0.7)

    def ring(self, cv, key, pos, alpha=1.0):
        if alpha <= 0.004:
            return
        x, y = self.px(pos)
        d = int(self.msize(key) * 1.9)
        cv.paste(G.ring(d, self.style(key)["fill"], 3), x, y, alpha, "mm", check_safe=False)
        cv.paste(G.circle(d, G.rgba(self.style(key)["fill"], 40)), x, y, alpha, "mm", check_safe=False)

    def pulse(self, cv, key, pos, t, t0, dur=0.9, color=None):
        """One expanding, fading ring starting at t0."""
        p = (t - t0) / dur
        if p < 0 or p > 1:
            return
        x, y = self.px(pos)
        d = int(self.msize(key) * (1.2 + 1.6 * out_cubic(p)))
        cv.paste(G.ring(d, color or self.style(key)["fill"], 4), x, y, (1 - p) * 0.9, "mm", check_safe=False)

    def label(self, cv, pos, text_, dx=24, dy=0, anchor="lm", alpha=1.0, size=C.SIZE_CHART, style="semibold",
              color=C.INK, count=False):
        if alpha <= 0.004:
            return
        x, y = self.px(pos)
        ts = G.text(text_, size, style, color, count=count)
        cv.paste(ts, x + dx, y + dy, alpha, anchor)


# ---------------------------------------------------------------- dot strip (scene 8)

class DotStrip:
    """A horizontal value axis with class markers that drop into place; overlapping markers stack upwards."""

    def __init__(self, x0, x1, y, lim, title, tick_labels, ms=30):
        self.x0, self.x1, self.y, self.lim, self.title, self.ticks, self.ms = x0, x1, y, lim, title, tick_labels, ms

    def vx(self, v):
        lo, hi = self.lim
        return self.x0 + (v - lo) / (hi - lo) * (self.x1 - self.x0)

    def stack(self, items):
        """{key: row} so markers closer than one marker width stack upwards."""
        placed, rows = [], {}
        for k, v in sorted(items, key=lambda kv: kv[1]):
            x = self.vx(v)
            r = 0
            while any(abs(x - px) < self.ms + 3 and pr == r for px, pr in placed):
                r += 1
            placed.append((x, r))
            rows[k] = r
        return rows

    def draw(self, cv, t, items, alpha=1.0, labels=None, bracket=None, zero=True):
        """items: [(key, value, t_land)]. labels: {key: (text, side)}. bracket: (v0, v1, text, alpha)."""
        if alpha <= 0:
            return
        d = cv.draw
        a255 = int(255 * alpha)
        d.line([(self.x0, self.y), (self.x1, self.y)], fill=G.rgba(C.INK2, a255), width=2)
        if zero:
            zx = self.vx(0)
            d.line([(zx, self.y - 150), (zx, self.y + 10)], fill=G.rgba(C.REF, a255), width=2)
        for v, s in self.ticks:
            x = self.vx(v)
            d.line([(x, self.y), (x, self.y + 10)], fill=G.rgba(C.INK2, a255), width=2)
            if s:
                ts = G.text(s, C.SIZE_TICK, "regular", C.INK2, count=False)
                cv.paste(ts, x, self.y + 16, alpha, "mt")
        tt = G.text(self.title, 38, "semibold", C.INK)
        cv.paste(tt, self.x0, self.y - 236, alpha, "lb")
        rows = self.stack([(k, v) for k, v, _ in items])
        labels = labels or {}
        for k, v, tl in items:
            p = prog(t, tl, 0.5, lambda x: x)
            if p <= 0:
                continue
            st = C.CLASS_STYLE[D.CLASS[k]]
            x = self.vx(v)
            y_final = self.y - 22 - rows[k] * (self.ms + 4)
            y = y_final - 60 * (1 - out_cubic(p))
            cv.paste(G.marker(st["marker"], self.ms + (5 if st["marker"] == "^" else 0), st["fill"], st["edge"], 2), x, y,
                     alpha * min(1, p * 2), "mm", check_safe=False)
            if k in labels and p > 0.5:
                txt, side = labels[k]
                ls = G.text(txt, C.SIZE_CHART, "semibold", C.INK, count=False)
                if isinstance(side, tuple):          # explicit (dx, dy, anchor) from the marker centre
                    cv.paste(ls, x + side[0], y + side[1], alpha * prog(t, tl + 0.3, 0.3), side[2])
                elif side == "below":
                    cv.paste(ls, x, self.y + 56, alpha * prog(t, tl + 0.3, 0.3), "mt")
                elif side == "above":
                    cv.paste(ls, x - 20, y - 26, alpha * prog(t, tl + 0.3, 0.3), "lb")
                elif side == "left":
                    cv.paste(ls, x - 26, y, alpha * prog(t, tl + 0.3, 0.3), "rm")
                else:
                    cv.paste(ls, x + 26, y, alpha * prog(t, tl + 0.3, 0.3), "lm")
        if bracket and bracket[3] > 0:
            v0, v1, txt, ba = bracket
            xa, xb = self.vx(v0), self.vx(v1)
            inside = [rows[k] for k, v, _ in items if v0 - 1e-9 <= v <= v1 + 1e-9]
            top = self.y - 22 - (max(inside) + 1) * (self.ms + 4) - 12
            col = G.rgba(C.INK, int(255 * alpha * ba))
            d.line([(xa, top + 14), (xa, top), (xb, top), (xb, top + 14)], fill=col, width=3)
            bs = G.text(txt, 38, "bold", C.INK)
            cv.paste(bs, (xa + xb) / 2, top - 10, alpha * ba, "mb")


# ---------------------------------------------------------------- interval strip (scene 7)

class IntervalStrip:
    """Order-balanced gap (D_bal), shuffled order: dot + 95% interval per model, dashed threshold lines."""

    def __init__(self, x0, y0, w, rows, lim=(-0.1, 0.4), thresholds=(0.10, 0.15),
                 title="Order-balanced gap, shuffled order",
                 row_h=86, name_w=250):
        self.x0, self.y0, self.w, self.rows, self.lim, self.th, self.title = x0, y0, w, rows, lim, thresholds, title
        self.row_h, self.name_w = row_h, name_w
        self.ax0 = x0 + name_w
        self.ax1 = x0 + w

    def vx(self, v):
        lo, hi = self.lim
        return self.ax0 + (v - lo) / (hi - lo) * (self.ax1 - self.ax0)

    def draw(self, cv, t, alpha=1.0, emph=(), th_pulse_t=None, row_times=None):
        if alpha <= 0:
            return
        d = cv.draw
        a255 = int(255 * alpha)
        tt = G.text(self.title, 38, "semibold", C.INK)
        cv.paste(tt, self.x0, self.y0, alpha, "lt")
        top = self.y0 + 76
        bot = top + len(self.rows) * self.row_h
        # threshold lines
        for k, th in enumerate(self.th):
            x = self.vx(th)
            pa = 1.0
            wd = 2
            if th_pulse_t is not None:
                p = (t - th_pulse_t) / 1.2
                if 0 <= p <= 1:
                    wd = 2 + int(3 * math.sin(math.pi * p))
            G.dashed_line(cv, (x, top - 6), (x, bot), C.INK, width=wd, dash=10, gap=8, alpha=alpha)
            lab = G.text(f"{th:.2f}", C.SIZE_TICK, "semibold", C.INK, count=False)
            cv.paste(lab, x + (-6 if k == 0 else 6), bot + 52, alpha, "rt" if k == 0 else "lt")
        # zero line and axis
        zx = self.vx(0)
        d.line([(zx, top - 6), (zx, bot)], fill=G.rgba(C.REF, a255), width=2)
        d.line([(self.ax0, bot + 6), (self.ax1, bot + 6)], fill=G.rgba(C.INK2, a255), width=2)
        for v, s in ((-0.1, "−0.1"), (0.0, "0"), (0.4, "0.4")):
            x = self.vx(v)
            d.line([(x, bot + 6), (x, bot + 14)], fill=G.rgba(C.INK2, a255), width=2)
            ts = G.text(s, C.SIZE_TICK, "regular", C.INK2, count=False)
            cv.paste(ts, x, bot + 16, alpha, "mt")
        for i, (key, est, lo, hi) in enumerate(self.rows):
            ra = alpha * (prog(t, row_times[i], 0.4) if row_times else 1.0)
            if ra <= 0:
                continue
            y = top + i * self.row_h + self.row_h / 2
            em = key in emph
            col = C.CLASS_STYLE[D.CLASS[key]]
            if em:
                band = G.rounded_rect(int(self.w + 20), int(self.row_h - 10), 12, (240, 238, 228), None, 0, 0)
                cv.paste(band, self.x0 - 10, y, ra, "lm", check_safe=False)
            ns = G.text(D.NAME[key], C.SIZE_CHART, "bold" if em else "regular", C.INK, count=False)
            cv.paste(ns, self.x0, y - 2, ra, "lm")
            d.line([(self.vx(lo), y), (self.vx(hi), y)], fill=G.rgba(col["fill"], int(255 * ra)), width=5)
            for xe in (self.vx(lo), self.vx(hi)):
                d.line([(xe, y - 10), (xe, y + 10)], fill=G.rgba(col["fill"], int(255 * ra)), width=3)
            cv.paste(G.marker(col["marker"], 28 + (5 if col["marker"] == "^" else 0), col["fill"], col["edge"], 2),
                     self.vx(est), y, ra, "mm", check_safe=False)


# ---------------------------------------------------------------- grid of 160 (scene 9)

def grid160(cv, x, y, n_fill, p, color, alpha=1.0, cols=16, rows=10, cell=34, gap=8):
    """Pale grey outlined squares; the first round(n_fill * p) fill row by row."""
    if alpha <= 0:
        return
    k_fill = int(math.floor(n_fill * p + 1e-9))
    empty = G.rounded_rect(cell, cell, 5, C.CARD, (200, 199, 193), 2, 0)
    full = G.rounded_rect(cell, cell, 5, color, None, 0, 0)
    for i in range(cols * rows):
        r, c = divmod(i, cols)
        xx, yy = x + c * (cell + gap), y + r * (cell + gap)
        cv.paste(full if i < k_fill else empty, xx, yy, alpha, check_safe=False)
    return (x, y, x + cols * (cell + gap) - gap, y + rows * (cell + gap) - gap)


# ---------------------------------------------------------------- horizontal bars

def hbar(cv, x, y, w, h, frac, p, color, alpha=1.0):
    if alpha <= 0:
        return
    d = cv.draw
    d.rectangle((x, y, x + w, y + h), fill=G.rgba(C.GRID, int(150 * alpha)))
    bw = w * frac * p
    if bw > 0:
        d.rectangle((x, y, x + bw, y + h), fill=G.rgba(color, int(255 * alpha)))
    return x + bw


# ---------------------------------------------------------------- meter (scene 1)

def meter(cv, x, y, level, alpha=1.0, n=7, bw=22, gap=10, hmax=150):
    """Loudness meter: n bars of rising height; `level` 0..1 lights them from left to right."""
    if alpha <= 0:
        return
    d = cv.draw
    for i in range(n):
        h = hmax * (0.3 + 0.7 * (i + 1) / n)
        lit = level * n - i
        col = C.INK if lit >= 1 else (C.GRID if lit <= 0 else tuple(int(lerp(C.GRID[j], C.INK[j], lit)) for j in range(3)))
        xx = x + i * (bw + gap)
        d.rounded_rectangle((xx, y + hmax - h, xx + bw, y + hmax), radius=5, fill=G.rgba(col, int(255 * alpha)))


# ---------------------------------------------------------------- credits (exact text from plan.md)

def parse_credits(plan_path=C.VIDEO / "plan.md"):
    """Blocks of the credits text, exactly as written in plan.md scene 11: {'top': [...], 'left': [...],
    'right': [...], 'bottom': [...]}, each line a list of (text, bold) runs."""
    txt = plan_path.read_text(encoding="utf-8")
    sec = txt[txt.index("## Scene 11"):]
    sec = sec[:sec.index("\n---")] if "\n---" in sec else sec
    blocks, cur = {}, None
    names = {"Top band:": "top", "Left column:": "left", "Right column:": "right", "Bottom band:": "bottom"}
    for ln in sec.splitlines():
        s = ln.strip()
        if s in names:
            cur = names[s]
            blocks[cur] = []
        elif s.startswith(">") and cur:
            body = s[1:].strip()
            runs = []
            for part in re.split(r"(\*\*[^*]+\*\*)", body):
                if not part:
                    continue
                if part.startswith("**"):
                    runs.append((part[2:-2], True))
                else:
                    runs.append((part, False))
            blocks[cur].append(runs)
    return blocks


def credits_plain(blocks):
    """The credits as plain text (for the character-for-character check)."""
    return {k: ["".join(t for t, _ in ln) for ln in v] for k, v in blocks.items()}
