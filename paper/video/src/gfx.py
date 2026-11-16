"""Drawing core: a 1920x1080 RGBA canvas, cached anti-aliased sprites, and text that measures, wraps and checks
the safe area.

Shapes are drawn 4x supersampled and downscaled (Pillow draws shapes without anti-aliasing). Text is rendered as
a coverage mask and coloured, so edges stay clean on any background. The check and cross marks are not in Segoe
UI, so text containing U+2713 or U+2717 has them replaced by drawn icons, inline.

Every cache is per process (the renderer uses spawn-based multiprocessing; each worker builds its own).
"""
import math
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import config as C

SS = 4  # supersampling factor for shapes

_cache = {}


def cached(key, make):
    v = _cache.get(key)
    if v is None:
        v = make()
        _cache[key] = v
    return v


@lru_cache(maxsize=None)
def font(style, size):
    return ImageFont.truetype(str(C.FONTS[style]), int(size))


class SafeAreaError(ValueError):
    pass


# ---------------------------------------------------------------- canvas

_ALPHA_LUT = {}


def _lut(a):
    q = int(round(a * 255))
    lut = _ALPHA_LUT.get(q)
    if lut is None:
        lut = [int(round(v * q / 255)) for v in range(256)]
        _ALPHA_LUT[q] = lut
    return lut


def with_alpha(sprite, alpha):
    if alpha >= 0.999:
        return sprite
    sp = sprite.copy()
    sp.putalpha(sp.getchannel("A").point(_lut(alpha)))
    return sp


class Canvas:
    """One frame. `words` counts words of text drawn at alpha > 0.5 (for the 15-words-on-screen check);
    `safe_violations` lists text placed outside config.SAFE (raised immediately when strict)."""

    def __init__(self, bg=C.BG, strict=True):
        # An opaque canvas is RGB (sprites are pasted through their alpha; draw calls blend RGBA colours).
        # bg=None gives a transparent RGBA layer (composited with alpha_composite).
        if bg is None:
            self.img = Image.new("RGBA", (C.W, C.H), (0, 0, 0, 0))
        else:
            self.img = Image.new("RGB", (C.W, C.H), tuple(bg[:3]))
        self.words = 0
        self.strict = strict
        self.safe_violations = []
        self._draw = None

    @property
    def draw(self):
        if self._draw is None:
            self._draw = ImageDraw.Draw(self.img, "RGBA")
        return self._draw

    def paste(self, sprite, x, y, alpha=1.0, anchor="lt", check_safe=None):
        """Composite `sprite` with its anchor at (x, y). anchor: two letters, horizontal l/m/r + vertical t/m/b."""
        if sprite is None or alpha <= 0.004:
            return None
        w, h = sprite.size
        ax = {"l": 0, "m": w / 2, "r": w}[anchor[0]]
        ay = {"t": 0, "m": h / 2, "b": h}[anchor[1]]
        x0, y0 = int(round(x - ax)), int(round(y - ay))
        info = sprite.info
        if check_safe is None:
            check_safe = info.get("is_text", False)
        if check_safe and alpha > 0.05:
            bb = info.get("ink_bbox") or (0, 0, w, h)
            bx0, by0, bx1, by1 = x0 + bb[0], y0 + bb[1], x0 + bb[2], y0 + bb[3]
            sx0, sy0, sx1, sy1 = C.SAFE
            if bx0 < sx0 - 1 or by0 < sy0 - 1 or bx1 > sx1 + 1 or by1 > sy1 + 1:
                msg = f"text {info.get('text', '?')!r} at ({bx0},{by0},{bx1},{by1}) leaves the safe area {C.SAFE}"
                self.safe_violations.append(msg)
                if self.strict:
                    raise SafeAreaError(msg)
        if alpha > 0.5 and info.get("words"):
            self.words += info["words"]
        sp = with_alpha(sprite, alpha)
        # clip to the canvas (alpha_composite needs a non-negative destination inside the image)
        cx0, cy0 = max(0, x0), max(0, y0)
        cx1, cy1 = min(C.W, x0 + w), min(C.H, y0 + h)
        if cx1 <= cx0 or cy1 <= cy0:
            return (x0, y0, x0 + w, y0 + h)
        if (cx0, cy0, cx1, cy1) != (x0, y0, x0 + w, y0 + h):
            sp = sp.crop((cx0 - x0, cy0 - y0, cx1 - x0, cy1 - y0))
        if self.img.mode == "RGB":
            self.img.paste(sp, (cx0, cy0), sp)
        else:
            self.img.alpha_composite(sp, dest=(cx0, cy0))
        return (x0, y0, x0 + w, y0 + h)

    def paste_scaled(self, sprite, cx, cy, scale, alpha=1.0):
        """Paste centred at (cx, cy), scaled (for pops). Scale 1 is the cached sprite as is."""
        if scale <= 0.01 or alpha <= 0.004:
            return
        if abs(scale - 1) > 0.004:
            w, h = sprite.size
            sp = sprite.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.BILINEAR)
            sp.info.update({k: v for k, v in sprite.info.items() if k in ("words", "text")})
        else:
            sp = sprite
        self.paste(sp, cx, cy, alpha, "mm", check_safe=False)

    def rgb_bytes(self):
        return self.img.convert("RGB").tobytes()

    def rect(self, box, color, alpha=1.0):
        """Axis-aligned filled rectangle, alpha-composited (works on RGB canvases and RGBA layers)."""
        x0, y0, x1, y1 = (int(round(v)) for v in box)
        if x1 <= x0 or y1 <= y0 or alpha <= 0.004:
            return
        a = int(round((color[3] if len(color) == 4 else 255) * alpha))
        sp = Image.new("RGBA", (x1 - x0, y1 - y0), tuple(color[:3]) + (a,))
        self.paste(sp, x0, y0, 1.0, check_safe=False)

    def hline(self, x0, x1, y, color, width=2, alpha=1.0):
        self.rect((min(x0, x1), y - width / 2, max(x0, x1), y + width / 2), color, alpha)

    def vline(self, x, y0, y1, color, width=2, alpha=1.0):
        self.rect((x - width / 2, min(y0, y1), x + width / 2, max(y0, y1)), color, alpha)


# ---------------------------------------------------------------- supersampled shapes

def ss_sprite(w, h, fn, ss=SS):
    """Render fn(draw, s) on a (w*ss, h*ss) transparent image (s = scale factor for coordinates), downscale."""
    big = Image.new("RGBA", (int(math.ceil(w * ss)), int(math.ceil(h * ss))), (0, 0, 0, 0))
    fn(ImageDraw.Draw(big), ss)
    return big.resize((int(math.ceil(w)), int(math.ceil(h))), Image.LANCZOS)


def rgba(c, a=255):
    return tuple(c[:3]) + ((c[3],) if len(c) == 4 else (a,))


def rounded_rect(w, h, r, fill, outline=None, width=0, shadow=0):
    """Rounded rectangle sprite. shadow > 0 adds a soft drop shadow (blur radius in px); the sprite is then larger
    by `pad` on each side and info['pad'] gives the offset of the rectangle inside it."""
    key = ("rr", w, h, r, rgba(fill), rgba(outline) if outline else None, width, shadow)

    def make():
        def fn(d, s):
            off = width * s / 2
            d.rounded_rectangle((off, off, w * s - off - 1, h * s - off - 1), radius=r * s, fill=rgba(fill),
                                outline=rgba(outline) if outline else None, width=int(round(width * s)))
        body = ss_sprite(w, h, fn)
        if not shadow:
            body.info["pad"] = 0
            return body
        pad = int(shadow * 2.5)
        canvas = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
        sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        mask = body.getchannel("A").point(lambda v: v * C.SHADOW[3] // 255)
        sh.paste(Image.new("RGBA", body.size, (0, 0, 0, 255)), (pad, pad + int(shadow * 0.45)), mask)
        sh = sh.filter(ImageFilter.GaussianBlur(shadow))
        canvas.alpha_composite(sh)
        canvas.alpha_composite(body, dest=(pad, pad))
        canvas.info["pad"] = pad
        return canvas
    return cached(key, make)


def circle(d, fill, edge=None, ew=0):
    key = ("circle", d, rgba(fill), rgba(edge) if edge else None, ew)

    def make():
        def fn(dr, s):
            o = ew * s / 2
            dr.ellipse((o, o, d * s - o - 1, d * s - o - 1), fill=rgba(fill), outline=rgba(edge) if edge else None,
                       width=int(round(ew * s)))
        return ss_sprite(d, d, fn)
    return cached(key, make)


def marker(kind, size, fill, edge, ew=2.0):
    """Scatter marker: 'o' circle, 's' square, '^' triangle; size = bounding box in px. Centred sprite."""
    key = ("marker", kind, size, rgba(fill), rgba(edge), ew)

    def make():
        pad = 2
        tot = size + 2 * pad

        def fn(dr, s):
            o = (pad + ew / 2) * s
            e = (tot - pad - ew / 2) * s
            if kind == "o":
                dr.ellipse((o, o, e, e), fill=rgba(fill), outline=rgba(edge), width=int(round(ew * s)))
            elif kind == "s":
                q = size * 0.08 * s
                dr.rectangle((o + q, o + q, e - q, e - q), fill=rgba(fill), outline=rgba(edge),
                             width=int(round(ew * s)))
            else:
                cx = tot * s / 2
                pts = [(cx, o - size * 0.02 * s), (e + size * 0.04 * s, e - size * 0.06 * s),
                       (o - size * 0.04 * s, e - size * 0.06 * s)]
                dr.polygon(pts, fill=rgba(fill), outline=rgba(edge), width=int(round(ew * s)))
        return ss_sprite(tot, tot, fn)
    return cached(key, make)


def ring(d, color, width):
    key = ("ring", d, rgba(color), width)

    def make():
        def fn(dr, s):
            o = width * s / 2
            dr.ellipse((o, o, d * s - o, d * s - o), outline=rgba(color), width=int(round(width * s)))
        return ss_sprite(d, d, fn)
    return cached(key, make)


def _polyline(dr, pts, s, color, width):
    p = [(x * s, y * s) for x, y in pts]
    w = int(round(width * s))
    dr.line(p, fill=rgba(color), width=w, joint="curve")
    r = width * s / 2
    for x, y in (p[0], p[-1]):
        dr.ellipse((x - r, y - r, x + r, y + r), fill=rgba(color))


def check_icon(size, color=C.CHECK, stroke=None):
    """A drawn check mark in a size x size box."""
    stroke = stroke or max(3.0, size * 0.14)
    key = ("check", size, rgba(color), stroke)

    def make():
        def fn(dr, s):
            pts = [(size * 0.16, size * 0.54), (size * 0.40, size * 0.78), (size * 0.86, size * 0.24)]
            _polyline(dr, pts, s, color, stroke)
        return ss_sprite(size, size, fn)
    return cached(key, make)


def cross_icon(size, color=C.CROSS, stroke=None):
    stroke = stroke or max(3.0, size * 0.14)
    key = ("cross", size, rgba(color), stroke)

    def make():
        def fn(dr, s):
            a, b = size * 0.22, size * 0.78
            _polyline(dr, [(a, a), (b, b)], s, color, stroke)
            _polyline(dr, [(b, a), (a, b)], s, color, stroke)
        return ss_sprite(size, size, fn)
    return cached(key, make)


def dashed_line(canvas, p0, p1, color, width=3, dash=14, gap=10, alpha=1.0, progress=1.0):
    """Anti-aliased dashed line drawn directly (supersampled over its bounding box)."""
    x0, y0 = p0
    x1 = x0 + (p1[0] - x0) * progress
    y1 = y0 + (p1[1] - y0) * progress
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1 or alpha <= 0:
        return
    key = ("dash", round(x0), round(y0), round(x1), round(y1), rgba(color), width, dash, gap)

    def make():
        bx0, by0 = min(x0, x1) - width, min(y0, y1) - width
        bw, bh = abs(x1 - x0) + 2 * width, abs(y1 - y0) + 2 * width

        def fn(dr, s):
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            t = 0.0
            while t < L:
                t2 = min(L, t + dash)
                a = ((x0 + ux * t - bx0) * s, (y0 + uy * t - by0) * s)
                b = ((x0 + ux * t2 - bx0) * s, (y0 + uy * t2 - by0) * s)
                dr.line([a, b], fill=rgba(color), width=int(round(width * s)))
                t = t2 + gap
        sp = ss_sprite(bw, bh, fn)
        sp.info["origin"] = (bx0, by0)
        return sp
    sp = cached(key, make)
    ox, oy = sp.info["origin"]
    canvas.paste(sp, ox, oy, alpha, check_safe=False)


def line(canvas, pts, color, width=3, alpha=1.0):
    """Anti-aliased solid polyline (not cached; for short animated strokes)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    bx0, by0 = min(xs) - width - 2, min(ys) - width - 2
    bw, bh = max(xs) - bx0 + width + 2, max(ys) - by0 + width + 2
    sp = ss_sprite(bw, bh, lambda dr, s: _polyline(dr, [(x - bx0, y - by0) for x, y in pts], s, color, width), ss=3)
    canvas.paste(sp, bx0, by0, alpha, check_safe=False)


def arrow(canvas, pts, color, width=6, head=24, alpha=1.0):
    """Polyline with an arrowhead at the last point."""
    if len(pts) < 2:
        return
    (xa, ya), (xb, yb) = pts[-2], pts[-1]
    ang = math.atan2(yb - ya, xb - xa)
    back = (xb - head * 0.8 * math.cos(ang), yb - head * 0.8 * math.sin(ang))
    body = pts[:-1] + [back]
    left = (xb - head * math.cos(ang - 0.45), yb - head * math.sin(ang - 0.45))
    right = (xb - head * math.cos(ang + 0.45), yb - head * math.sin(ang + 0.45))
    allp = body + [left, right, (xb, yb)]
    xs, ys = [p[0] for p in allp], [p[1] for p in allp]
    bx0, by0 = min(xs) - width - 2, min(ys) - width - 2
    bw, bh = max(xs) - bx0 + width + 2, max(ys) - by0 + width + 2

    def fn(dr, s):
        _polyline(dr, [(x - bx0, y - by0) for x, y in body], s, color, width)
        dr.polygon([((x - bx0) * s, (y - by0) * s) for x, y in ((xb, yb), left, right)], fill=rgba(color))
    canvas.paste(ss_sprite(bw, bh, fn, ss=3), bx0, by0, alpha, check_safe=False)


def bezier(p0, p1, p2, n=40, upto=1.0):
    out = []
    for i in range(n + 1):
        t = upto * i / n
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out


# ---------------------------------------------------------------- text

ICON_CHARS = {"✓": "check", "✗": "cross"}


def _tokens(line_text):
    """Split a line into ('text', str) and ('icon', name) runs."""
    runs, buf = [], ""
    for ch in line_text:
        if ch in ICON_CHARS:
            if buf:
                runs.append(("text", buf))
                buf = ""
            runs.append(("icon", ICON_CHARS[ch]))
        else:
            buf += ch
    if buf:
        runs.append(("text", buf))
    return runs


def _run_width(runs, f, size):
    w = 0.0
    for kind, v in runs:
        w += f.getlength(v) if kind == "text" else size * 0.82
    return w


def wrap(text, f, size, max_width):
    """Greedy word wrap; explicit newlines kept. Raises if one word is wider than max_width."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w_ in words:
            cand = w_ if not cur else cur + " " + w_
            if _run_width(_tokens(cand), f, size) <= max_width or not cur:
                if not cur and _run_width(_tokens(cand), f, size) > max_width:
                    raise SafeAreaError(f"word {w_!r} wider than {max_width}px at {size}px")
                cur = cand
            else:
                lines.append(cur)
                cur = w_
        lines.append(cur)
    return lines


def count_words(text):
    return sum(1 for tok in text.replace("\n", " ").split() if any(ch.isalnum() for ch in tok))


def text(s, size=C.SIZE_BODY, style="regular", color=C.INK, max_width=None, align="left", line_gap=1.22,
         count=True, icon_colors=None):
    """Text sprite (RGBA). Lines wrap at max_width. info: words (for the on-screen count), ink_bbox, lines.
    `count=False` for tick numbers. icon_colors overrides the check/cross colours, e.g. {'check': (..)}."""
    icon_colors = icon_colors or {}
    key = ("text", s, size, style, rgba(color), max_width, align, line_gap, count,
           tuple(sorted((k, rgba(v)) for k, v in icon_colors.items())))

    def make():
        f = font(style, size)
        lines = wrap(s, f, size, max_width) if max_width else s.split("\n")
        asc, desc = f.getmetrics()
        adv = int(round(size * line_gap))
        widths = [_run_width(_tokens(ln), f, size) for ln in lines]
        W_ = int(math.ceil(max(widths) if widths else 1)) + 4
        H_ = adv * (len(lines) - 1) + asc + desc + 4
        mask = Image.new("L", (W_, H_), 0)
        dm = ImageDraw.Draw(mask)
        icons = []
        for i, (ln, lw) in enumerate(zip(lines, widths)):
            x = {"left": 2, "center": (W_ - lw) / 2, "right": W_ - 2 - lw}[align]
            y = 2 + i * adv
            for kind, v in _tokens(ln):
                if kind == "text":
                    dm.text((x, y), v, font=f, fill=255)
                    x += f.getlength(v)
                else:
                    isz = int(size * 0.82)
                    icons.append((v, x, y + asc - isz * 0.92, isz))
                    x += size * 0.82
        sp = Image.new("RGBA", (W_, H_), rgba(color))
        sp.putalpha(mask)
        for name, ix, iy, isz in icons:
            col = icon_colors.get(name, C.CHECK if name == "check" else C.CROSS)
            ic = check_icon(isz, col) if name == "check" else cross_icon(isz, col)
            sp.alpha_composite(ic, dest=(int(round(ix)), int(round(iy))))
        bb = sp.getchannel("A").getbbox() or (0, 0, W_, H_)
        sp.info.update({"is_text": True, "text": s, "words": count_words(s) if count else 0, "ink_bbox": bb,
                        "lines": lines, "line_adv": adv, "ascent": asc})
        return sp
    return cached(key, make)


def text_width(s, size=C.SIZE_BODY, style="regular"):
    return _run_width(_tokens(s), font(style, size), size)


def no_count(sprite):
    """A copy of a text sprite that does not count towards the words-on-screen total (e.g. tick labels)."""
    sp = sprite.copy()
    sp.info.update(sprite.info)
    sp.info["words"] = 0
    return sp


# ---------------------------------------------------------------- dashed rounded outlines, rich text

def rrect_path(x0, y0, x1, y1, r, n_arc=10):
    """Closed polyline around a rounded rectangle, clockwise from the top-left straight edge."""
    pts = []
    corners = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    for cx, cy, a0 in corners:
        for k in range(n_arc + 1):
            a = math.radians(a0 + 90 * k / n_arc)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append(pts[0])
    return pts


def dash_polyline(dr, pts, s, color, width, dash, gap):
    """Draw a dashed polyline (coordinates already in supersampled space / s)."""
    on, left, draw_on = True, dash, True
    for (ax_, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax_, by - ay)
        pos = 0.0
        while pos < L - 1e-6:
            step = min(left, L - pos)
            if draw_on:
                p0 = (ax_ + (bx - ax_) * pos / L, ay + (by - ay) * pos / L)
                p1 = (ax_ + (bx - ax_) * (pos + step) / L, ay + (by - ay) * (pos + step) / L)
                dr.line([(p0[0] * s, p0[1] * s), (p1[0] * s, p1[1] * s)], fill=rgba(color), width=int(round(width * s)))
            pos += step
            left -= step
            if left <= 1e-6:
                draw_on = not draw_on
                left = dash if draw_on else gap


def rich_text(runs, size, max_width, line_gap=1.25, count=True, align="left"):
    """Wrapped text made of styled runs: runs = [(text, style, color)]. Words wrap across runs.
    Returns an RGBA sprite with info like text()."""
    key = ("rich", tuple((t_, st, rgba(c)) for t_, st, c in runs), size, max_width, line_gap, count, align)

    def make():
        words = []  # (word, style, color, space_before)
        for t_, st, col in runs:
            parts = t_.split(" ")
            for i, w_ in enumerate(parts):
                if w_ == "":
                    continue
                sp_before = (i > 0) or (t_.startswith(" ")) or (words and runs and False)
                words.append([w_, st, col, True])
        if words:
            words[0][3] = False
        lines, cur, cur_w = [], [], 0.0
        for w_, st, col, spb in words:
            f = font(st, size)
            ww = f.getlength(w_)
            sw = f.getlength(" ") if cur else 0.0
            if cur and cur_w + sw + ww > max_width:
                lines.append(cur)
                cur, cur_w, sw = [], 0.0, 0.0
            cur.append((w_, st, col, sw))
            cur_w += sw + ww
            if ww > max_width:
                raise SafeAreaError(f"word {w_!r} wider than {max_width}px")
        if cur:
            lines.append(cur)
        f0 = font("regular", size)
        asc, desc = f0.getmetrics()
        adv = int(round(size * line_gap))
        widths = [sum(sw + font(st, size).getlength(w_) for w_, st, col, sw in ln) for ln in lines]
        W_ = int(math.ceil(max(widths))) + 4
        H_ = adv * (len(lines) - 1) + asc + desc + 4
        img = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        for i, ln in enumerate(lines):
            x, y = 2.0 + ((W_ - 4 - widths[i]) / 2 if align == "center" else 0.0), 2 + i * adv
            for w_, st, col, sw in ln:
                x += sw
                f = font(st, size)
                m = Image.new("L", (int(f.getlength(w_)) + 4, asc + desc + 4), 0)
                ImageDraw.Draw(m).text((0, 0), w_, font=f, fill=255)
                piece = Image.new("RGBA", m.size, rgba(col))
                piece.putalpha(m)
                img.alpha_composite(piece, dest=(int(round(x)), int(y)))
                x += f.getlength(w_)
        bb = img.getchannel("A").getbbox() or (0, 0, W_, H_)
        txt = " ".join(t_ for t_, _, _ in runs)
        img.info.update({"is_text": True, "text": txt, "words": count_words(txt) if count else 0, "ink_bbox": bb})
        return img
    return cached(key, make)
