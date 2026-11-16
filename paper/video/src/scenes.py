"""The eleven scenes of plan.md. Each scene reads its cue times from the measured voice-over (timeline.Timeline)
and draws with the components. Scene-local time t is in seconds.

Transitions follow plan.md: scenes 2-3, 3-4, 4-5, 5-6 and 6-7 hand elements over directly (the incoming scene
draws them where the outgoing one left them); the other boundaries fade the scene's elements over the constant
background (frame() in render.py), with the persistent wordmark and legend drawn on top.
"""
import math
import random

import components as K
import config as C
import data as D
import gfx as G
from easing import clamp, in_out_cubic, lerp, lerp2, out_back, out_cubic, prog, window

V1 = {k: h for k, h in enumerate(D.LOG_CONDITIONS["certain_right"])}   # certain is right
V2 = {k: h for k, h in enumerate(D.LOG_CONDITIONS["unsure_right"])}    # unsure is right
REVERSED = {k: 7 - k for k in range(8)}
_rng = random.Random(20261116)
SHUF1 = dict(zip(range(8), _rng.sample(range(8), 8)))
SHUF2 = dict(zip(range(8), _rng.sample(range(8), 8)))

SC = K.Scatter(box=(900, 140, 720))    # the profile scatter, right two thirds
SMALL = dict(x=150, y=250, k=0.8, w=300)   # the small log card in the left column (scenes 3-5, 7)
OPEN7 = ["gemma", "ministral8", "ministral14", "llama33", "dsv41", "maverick", "mmed"]   # scene 5 points
FIVE = ["haiku", "luna", "dsv32", "qwen35", "qwen38"]
MOVERS = ["sonnet", "sol", "gemma", "ministral8", "llama33", "maverick"]

# Label placement per condition: key -> (dx, dy, anchor, leader). Offsets in px from the point.
LAB_A = {"sonnet": (-20, -12, "rb", False), "sol": (-16, -16, "rb", False), "gemini": (24, 0, "lm", False),
         "gemma": (0, -22, "mb", False), "ministral8": (-16, 18, "rt", False), "llama33": (0, 22, "mt", False),
         "maverick": (22, 0, "lm", False)}
LAB_R = {"sonnet": (-20, -12, "rb", False), "sol": (-16, -16, "rb", False), "gemma": (110, 95, "lt", True),
         "ministral8": (-40, 130, "lt", True), "llama33": (90, -70, "lm", True), "maverick": (120, -10, "lm", True)}
LAB_S = {"sol": (-16, -16, "rb", False), "gemma": (60, 75, "lt", True), "ministral8": (-150, 118, "lt", True),
         "llama33": (150, -60, "lm", True), "maverick": (150, 10, "lm", True)}
GAP_LABEL = (90, -104)     # the "+0.59 -> -0.16" label, offset from Llama 3.3's reversed-order position


def lab_draw(cv, key, pos, spec, alpha, text_=None):
    """Point label with an optional thin leader line."""
    if alpha <= 0.004:
        return
    dx, dy, anchor, leader = spec
    x, y = SC.px(pos)
    if leader:
        L = math.hypot(dx, dy)
        sx, sy = dx / L, dy / L
        G.line(cv, [(x + sx * 20, y + sy * 20), (x + dx - sx * 8, y + dy - sy * 8)], C.INK2, width=2,
               alpha=alpha * 0.6)
    cv.paste(label_sprite(text_ or D.NAME[key]), x + dx, y + dy, alpha, anchor)


def label_sprite(text_, size=C.SIZE_CHART, count=False):
    """Point label on a soft background box (masks grid and dashed lines underneath, as in the paper)."""
    def make():
        ts = G.text(text_, size, "semibold", C.INK, count=count)
        w, h = ts.size[0] + 12, ts.size[1] + 2
        img = G.rounded_rect(w, h, 8, G.rgba(C.BG, 225), None, 0, 0).copy()
        img.alpha_composite(ts, dest=(6, 1))
        img.info.update({"words": ts.info["words"], "text": text_, "is_text": True,
                         "ink_bbox": (6, 1, w - 6, h - 1)})
        return img
    return G.cached(("label_bg", text_, size, count), make)


def lab_interp(a, b, p):
    return (lerp(a[0], b[0], p), lerp(a[1], b[1], p), a[2] if p < 0.5 else b[2], a[3] if p < 0.5 else b[3])


class Base:
    num = 0
    fade_in = 0.0
    fade_out = 0.0
    exit_move = None          # (dx, scale) applied to the whole scene layer during the fade-out
    wordmark = True
    legend = False            # True, or (t_in, t_out) handled by legend_alpha

    def __init__(self, tl):
        self.tl = tl
        self.sc = tl.scene(self.num)
        self.dur = self.sc["dur"]
        self.setup()

    def c(self, phrase, end=False):
        return self.tl.cue(self.num, phrase, end)

    def setup(self):
        pass

    def legend_alpha(self, t):
        return 1.0 if self.legend else 0.0

    def draw(self, cv, t):
        raise NotImplementedError


def appear(t, t0, d=0.45):
    return prog(t, t0, d, out_cubic)


# ================================================================ scene 1: the question

class S1(Base):
    num = 1
    fade_out = 0.4
    exit_move = (-140, 0.86)
    wordmark = False

    def setup(self):
        self.t_shrink = self.c("Someone tells an AI model")
        self.t_bub = self.c("its answer is wrong")
        self.t_sure = self.c("how sure the critic sounds")
        self.t_often = self.c("how often that critic has been right")
        self.title = G.text("Loud or Right?", 96, "bold", C.INK, count=False)
        self.small = G.text("Apart Research · AI x Epistemics Research Sprint · November 2026", 36, "regular",
                            C.INK2)
        self.bubble = K.Bubble("I disagree.", "certain", size=48)

    def draw(self, cv, t):
        # title, then shrink to the wordmark
        p = prog(t, self.t_shrink - 0.15, 0.85)
        a0 = appear(t, 0.0, 0.6)
        tw, th = self.title.size
        s = lerp(1.0, 36 / 96, p)
        cx = lerp(C.W / 2, C.MARGIN + tw * (36 / 96) / 2 + 2, p)
        cy = lerp(430, 50 + th * (36 / 96) / 2, p)
        if p < 1:
            cv.paste_scaled(self.title, cx, cy + (1 - a0) * 30, s, a0)
        else:
            K.wordmark(cv)
        cv.paste(self.small, C.W / 2, 530 + (1 - a0) * 20, a0 * (1 - prog(t, self.t_shrink - 0.15, 0.4)), "mt")
        # answer card
        ac = appear(t, self.t_shrink + 0.35, 0.5)
        K.answer_card(cv, 190 - 40 * (1 - ac), 400, "Model's answer:", "F", alpha=ac, value_size=110)
        # reviewer bubble slides in from the right
        bb = appear(t, self.t_bub - 0.1, 0.55)
        self.bubble.draw(cv, 900 + 260 * (1 - bb), 300, alpha=bb)
        # loudness meter
        ma = appear(t, self.t_sure - 0.2, 0.4)
        if ma > 0:
            lvl = out_back(prog(t, self.t_sure, 0.9, lambda v: v), 1.2)
            K.meter(cv, 1390, 250, min(1.0, lvl), alpha=ma)
            cv.paste(G.text("How sure?", 40, "semibold", C.INK), 1390 + 103, 430, ma, "mt")
        # scorecard of ticks and crosses
        oa = appear(t, self.t_often - 0.1, 0.4)
        if oa > 0:
            for i, h in enumerate([1, 0, 1, 1, 0, 1]):
                pi = prog(t, self.t_often + 0.08 * i, 0.35, lambda v: v)
                if pi > 0:
                    cv.paste_scaled(K.mark_chip(h, 54), 930 + 27 + i * 66, 560 + 27, out_back(pi), oa * min(1, pi * 2))
            cv.paste(G.text("How often right?", 40, "semibold", C.INK), 930, 640, oa, "lt")


# ================================================================ scene 2: two track records

class S2(Base):
    num = 2
    fade_in = 0.35

    def setup(self):
        self.t0 = self.c("Confidence can mislead.")
        self.t_cert = self.c("right when they sound certain")
        self.t_hedge = self.c("right when they hedge")
        self.t_rec = self.c("a track record for each tone of voice")
        self.t_test = self.c("We tested whether language models do.")
        self.b1 = K.Bubble("The answer is (B).\nI am certain.", "certain", size=48, max_width=640)
        self.b2 = K.Bubble("I think it's (D),\nbut I'm not sure.", "unsure", size=48, max_width=640)
        self.cols = (250, 1050)

    def draw(self, cv, t):
        end = self.dur - 0.7            # hand-over to scene 3 starts here
        out = prog(t, end, 0.6)
        rec = prog(t, self.t_rec, 0.7)
        for i, (b, x) in enumerate(zip((self.b1, self.b2), self.cols)):
            a = appear(t, self.t0 + 0.15 * i, 0.5)
            # bubbles shrink to icons when the scorecards appear
            b.draw(cv, x, 250, alpha=a * (1 - rec), scale=lerp(1.0, 0.4, rec))
            g = K.voice_glyph(b.voice, 92)
            cv.paste(g, x, 500, rec * (1 - out), "lm", check_safe=False)
        # chips: four under each bubble; they swap at "hedge"
        swap = prog(t, self.t_hedge, 0.5, lambda v: v)
        for side, x in enumerate(self.cols):
            for i in range(4):
                tp = self.t_cert + 0.09 * i + 0.12 * side
                pi = prog(t, tp, 0.35, lambda v: v)
                if pi <= 0 or rec >= 1:
                    continue
                first = 1 if side == 0 else 0
                hit = first if swap < 0.5 else 1 - first
                sx = abs(1 - 2 * swap) if 0 < swap < 1 else 1.0
                chip = K.mark_chip(hit, 72)
                if sx < 0.999:
                    chip = chip.resize((max(1, int(72 * sx)), 72))
                cx = x + 36 + i * 92
                cx = lerp(cx, x + 250, rec)
                cv.paste_scaled(chip, cx, lerp(580, 500, rec), out_back(pi) * (1 - 0.6 * rec),
                                min(1, pi * 2) * (1 - rec))
        # scorecards
        if rec > 0:
            for x, txt in zip(self.cols, ("Certain: ? of 4 right", "Unsure: ? of 4 right")):
                tx = lerp(x + 120, lerp(x + 120, 738, 0.25), out)
                ty = lerp(500, 440, out)
                K.pill(cv, txt, tx, ty, alpha=rec * (1 - out) ** 2, anchor="lm", scale=lerp(1.0, 0.85, out), size=44,
                       style="semibold")
        # fifteen model markers along the bottom
        self.models_row(cv, t, self.t_test, 1 - out)

    @staticmethod
    def models_row(cv, t, t0, alpha, y=900, caption=None):
        order = [k for k, _, c in D.MODELS if c == "open"] + [k for k, _, c in D.MODELS if c == "closed"] + \
                [k for k, _, c in D.MODELS if c == "recency"]
        n = len(order)
        gap = 62
        x0 = C.W / 2 - (n - 1) * gap / 2 - (110 if caption else 0)
        for i, k in enumerate(order):
            a = prog(t, t0 + 0.05 * i, 0.35) * alpha
            if a <= 0:
                continue
            st = C.CLASS_STYLE[D.CLASS[k]]
            cv.paste(G.marker(st["marker"], 36 + (5 if st["marker"] == "^" else 0), st["fill"], st["edge"], 2),
                     x0 + i * gap, y, a, "mm", check_safe=False)
        if caption:
            ca = prog(t, t0 + 0.4, 0.4) * alpha
            cv.paste(G.text(caption, 44, "bold", C.INK), x0 + (n - 1) * gap + 50, y - 2, ca, "lm")


# ================================================================ scene 3: the test

def small_card_state(slots=None, hits=None):
    return dict(header=False, slots=slots or {k: k for k in range(8)}, hits=hits or V2, k=SMALL["k"], w=SMALL["w"])


class S3(Base):
    num = 3

    def setup(self):
        self.t_log = self.c("a practice log")
        self.t_rows = self.c("eight past objections")
        self.t_marks = self.c("each marked right or wrong")
        self.t_v1 = self.c("right only when certain")
        self.t_v2 = self.c("only when unsure")
        self.t_obj = self.c("Then Dana objects")
        self.t_own = self.c("objects to the model's own answer")
        self.t_sw = self.c("whether the model switches")
        self.t_15 = self.c("Fifteen models took the test.")
        self.card = K.LogCard(w=500, row_h=58)
        self.bubble = K.Bubble("I disagree. The answer is (C). I am certain.", "certain", size=44, max_width=520,
                               speaker="Dana")

    def draw(self, cv, t):
        out = prog(t, self.dur - 0.55, 0.5)       # everything fades, the small log card too (scenes 4-5 omit it)
        shrink = prog(t, self.t_obj - 0.2, 0.7)
        hits = V1 if t < self.t_v2 else V2
        flip = prog(t, self.t_v2, 0.5, lambda v: v)
        st = dict(header=shrink < 0.5, slots={k: k for k in range(8)},
                  row_alpha={k: prog(t, self.t_rows + 0.2 * k, 0.25) for k in range(8)},
                  hits=hits, hits_from=V1, flip=flip if t >= self.t_v2 else 1.0,
                  chip_alpha={k: prog(t, self.t_marks + 0.1 * k, 0.25) for k in range(8)},
                  k=lerp(1.0, SMALL["k"], shrink), w=lerp(500, SMALL["w"], shrink))
        lab_a = prog(t, self.t_v1, 0.4) * (1 - prog(t, self.t_obj - 0.3, 0.3))
        if lab_a > 0:
            st["footer"] = "Certain 4 of 4 · Unsure 0 of 4" if t < self.t_v2 + 0.25 else \
                "Certain 0 of 4 · Unsure 4 of 4"
            st["footer_alpha"] = lab_a * (1 - (1 - abs(1 - 2 * flip)) * 0.8 if t >= self.t_v2 else 1)
        x = lerp(710, SMALL["x"], shrink)
        y = lerp(215, SMALL["y"], shrink)
        ca = appear(t, self.t_log - 0.3, 0.4) if t < self.t_log + 1 else 1.0
        self.card.draw(cv, st, x, y, alpha=max(ca, 0.0) * (1 - out))
        if lab_a > 0:
            lbl = "Version 1: certain is right" if t < self.t_v2 + 0.25 else "Version 2: unsure is right"
            la = lab_a * (1 - (1 - abs(1 - 2 * flip)) if t >= self.t_v2 else 1)
            cv.paste(G.text(lbl, 44, "bold", C.INK), 960, 190, la, "mb")
        ao = 1 - out
        # answer card, then Dana's objection
        a1 = appear(t, self.t_obj + 0.25, 0.5) * (1 - prog(t, self.t_sw, 0.5))
        K.answer_card(cv, 700, 270, "Model's answer:", "F", alpha=a1 * ao, value_size=96)
        self.bubble.draw(cv, 1160, 170, alpha=appear(t, self.t_own, 0.45) * ao,
                         scale=0.9 + 0.1 * out_back(prog(t, self.t_own, 0.45, lambda v: v)))
        # two outcomes
        sp = appear(t, self.t_sw, 0.55)
        if sp > 0:
            K.answer_card(cv, 700, lerp(330, 560, sp), "Switch", "→ C", alpha=sp * ao, value_size=72, w=300)
            K.answer_card(cv, lerp(700, 1080, sp), lerp(330, 560, sp), "Hold", "→ F", alpha=sp * ao,
                          value_size=72, w=300)
            tk = prog(t, self.t_sw + 0.7, 0.4, lambda v: v)
            if tk > 0:
                # a neutral "recorded" pill (not a check mark: a check would read as "correct"), kept inside the
                # Switch card's width so it does not touch the Hold card
                rec = K.pill_sprite("recorded", 30, "semibold", C.INK, fill=C.CARD, edge=C.INK, ew=2, padx=16, pady=4)
                cv.paste_scaled(rec, 700 + 300 - 14 - rec.size[0] / 2, 560, out_back(tk), ao)
        S2.models_row(cv, t, self.t_15, ao, y=900, caption="15 models")


# ================================================================ scenes 4-5: the scatter

def small_card(cv, t=0.0, alpha=1.0, slots=None, hits=V2, x=None, y=None, k=None, w=None):
    card = K.LogCard(w=int(w or SMALL["w"]))
    st = dict(header=False, slots=slots or {i: i for i in range(8)}, hits=hits, k=k or SMALL["k"], w=w or SMALL["w"])
    card.draw(cv, st, x if x is not None else SMALL["x"], y if y is not None else SMALL["y"], alpha=alpha)


def arm_tag(cv, text_, alpha=1.0, swap=None):
    """Pill at the top right of the scatter naming the condition; swap = (old text, progress)."""
    x, y = SC.x0 + SC.size, SC.y0 - 18
    if swap and swap[1] < 1:
        K.pill(cv, swap[0], x, y, alpha=alpha * (1 - swap[1]), anchor="rb", size=34)
        K.pill(cv, text_, x, y, alpha=alpha * swap[1], anchor="rb", size=34)
    else:
        K.pill(cv, text_, x, y, alpha=alpha, anchor="rb", size=34)


class S4(Base):
    num = 4

    def setup(self):
        self.t_right = self.c("Further right")
        self.t_up = self.c("Further up")
        self.t_diag = self.c("On the diagonal")
        self.t_two = self.c("Claude Sonnet 5.5 and GPT-6 Sol sit there.")
        self.t_gem = self.c("Claude Sonnet 5.5 and GPT-6 Sol sit there.", end=True) + 0.15
        self.t_five = self.c("Five models barely responded.")
        self.t_hold = self.c("Five models barely responded.", end=True) + 0.1

    def legend_alpha(self, t):
        return prog(t, self.t_two, 0.5)

    def draw(self, cv, t):
        SC.draw_axes(cv, alpha=appear(t, 0.0, 0.6), xt=prog(t, self.t_right - 0.1, 0.4),
                     yt=prog(t, self.t_up - 0.1, 0.4), diag=prog(t, self.t_diag, 1.0),
                     diag_label=prog(t, self.t_diag + 0.5, 0.5))
        # sweeping arrows
        for t0, a, b in ((self.t_right, (0.0, 0.0), (0.95, 0.0)), (self.t_up, (0.0, 0.0), (0.0, 0.95))):
            p = prog(t, t0, 0.9)
            aa = window(t, t0, t0 + 2.6, 0.2, 0.5)
            if p > 0 and aa > 0:
                p0, p1 = SC.px(a), SC.px(lerp2(a, b, p))
                G.arrow(cv, [p0, p1], C.INK, width=7, head=28, alpha=aa)
        draw_fixed_points(cv, t, self, 4)
        K.caveat_chip(cv, "Tested at the extremes: 4 of 4 right against 0 of 4", alpha=prog(t, self.t_five + 0.3, 0.5))
        arm_tag(cv, "Fixed order", alpha=prog(t, self.t_hold, 0.5))


def draw_fixed_points(cv, t, scene, scene_no, alpha=1.0, lab_alpha=1.0):
    """Fixed-order points as they build up over scenes 4 and 5 (scene 5 continues from scene 4's end state)."""
    if scene_no == 4:
        t_two, t_gem, t_five = scene.t_two, scene.t_gem, scene.t_five
        pops = {"sonnet": t_two, "sol": t_two + 0.2, "gemini": t_gem}
        for i, k in enumerate(FIVE):
            pops[k] = t_five + 0.12 * i
        ring_a = prog(t, t_two + 0.4, 0.4)
        five_lab = prog(t, t_five + 0.6, 0.4)
        open_pops = {}
    else:
        pops = {k: -10 for k in ["sonnet", "sol", "gemini"] + FIVE}
        ring_a = 1 - prog(t, scene.t_open, 0.4)
        five_lab = 1 - prog(t, scene.t_open, 0.4)
        open_pops = {k: scene.t_open + 0.25 * i for i, k in enumerate(OPEN7)}
    pops.update(open_pops)
    for k in ("sonnet", "sol"):
        if ring_a > 0:
            SC.ring(cv, k, D.POS["A"][k], ring_a * alpha)
    for k, tp in pops.items():
        p = prog(t, tp, 0.45, lambda v: v)
        if p <= 0:
            continue
        SC.marker(cv, k, D.POS["A"][k], alpha * min(1, p * 2.5), out_back(p))
    # labels
    for k in ("sonnet", "sol", "gemini"):
        la = prog(t, pops[k] + 0.25, 0.35)
        lab_draw(cv, k, D.POS["A"][k], LAB_A[k], la * alpha * lab_alpha)
    if five_lab > 0:
        x5, y5 = SC.px((0.12, -0.05))
        cv.paste(label_sprite("5 models: little record effect", count=True), x5, y5, five_lab * alpha, "lt")
    for k in ("llama33", "maverick", "gemma", "ministral8"):
        if k in open_pops:
            lab_draw(cv, k, D.POS["A"][k], LAB_A[k], prog(t, open_pops[k] + 0.25, 0.35) * alpha * lab_alpha)


class S5(Base):
    num = 5
    legend = True

    def setup(self):
        self.t_open = self.c("Several open-weight models looked different.")
        self.t_band = self.c("credit only the confident voice")
        self.t_pred = self.c("predicted that for two of them")
        self.t_but = self.c("But our explanation did not hold up.")

    def draw(self, cv, t):
        draw_scatter_s5(cv, t, self)


def draw_scatter_s5(cv, t, s, alpha=1.0, extras=1.0):
    """Scene 5 scatter (also the start state of the scene 6 thumbnail). extras = band, stamp, tag, chip alpha."""
    ba = prog(t, s.t_band, 0.6) * alpha * extras
    if ba > 0:
        x0, y0 = SC.px((SC.lim[0], 0.17))
        x1, y1 = SC.px((SC.lim[1], -0.17))
        cv.rect((x0, y0, x1, y1), (122, 122, 117), 0.16 * ba)
    SC.draw_axes(cv, alpha=alpha, diag_label=extras, xt=extras, yt=extras)
    draw_fixed_points(cv, t, s, 5, alpha, lab_alpha=extras)
    if ba > 0:
        lx, ly = SC.px((SC.lim[1], 0.17))
        main = G.text("certain voice's record only", C.SIZE_CHART, "semibold", C.INK)
        q = G.text("?", C.SIZE_CHART + 4, "bold", C.INK)
        qs = 1.0
        if t > s.t_but:
            ph = (t - s.t_but) / 0.8
            qs = 1 + 0.45 * max(0.0, math.sin(math.pi * min(ph, 2.0))) if ph < 2 else 1.0
        cv.paste(main, lx - 4 - q.size[0], ly - 8, ba, "rb")
        cv.paste_scaled(q, lx - q.size[0] / 2, ly - 8 - main.size[1] / 2 - 2, qs, ba)
    # rings around Gemma and Ministral 3 8B, stamp
    ra = prog(t, s.t_pred, 0.4) * alpha * extras
    for k in ("gemma", "ministral8"):
        SC.ring(cv, k, D.POS["A"][k], ra)
    sa = prog(t, s.t_pred + 0.3, 0.35, lambda v: v) * alpha * extras
    if sa > 0:
        grey = prog(t, s.t_but + 0.3, 0.6)
        col = tuple(int(lerp(C.INK[i], C.INK2[i], grey)) for i in range(3))
        sp = K.pill_sprite("Registered in advance ✓", 32, "bold", col, fill=C.BG, edge=col, ew=4, padx=18,
                           pady=7, radius=12)
        rot = sp.rotate(6, expand=True, resample=3)
        rot.info.update(sp.info)
        sc = 1.25 - 0.25 * out_cubic(min(1, sa * 1.4))
        x, y = SC.px((0.085, 0.37))    # nearer the ringed Gemma and Ministral 3 8B, clear of points and labels
        cv.paste(sp, x, y, 0)  # safe-area check
        cv.paste_scaled(rot, x, y, sc, min(1.0, sa * 2) * (1 - 0.45 * grey))
    K.caveat_chip(cv, "Tested at the extremes: 4 of 4 right against 0 of 4", alpha=alpha * extras)
    arm_tag(cv, "Fixed order", alpha=alpha * extras)


# ================================================================ scene 6: the first line

THUMB = dict(scale=0.40, right=C.W - C.MARGIN, top=175)


def scatter_layer(draw_fn):
    layer = G.Canvas(bg=None, strict=False)
    draw_fn(layer)
    return layer


def paste_scatter(cv, layer, scale, alpha=1.0):
    """Paste a full-frame scatter layer scaled so that the plot keeps its right edge at THUMB['right'] when small."""
    img = layer.img
    if scale >= 0.999:
        img.info["words"] = layer.words
        cv.paste(img, 0, 0, alpha, check_safe=False)
        cv.words += layer.words if alpha > 0.5 else 0
        return
    # crop to the scatter area (axes titles included)
    box = (SC.x0 - 140, SC.y0 - 90, SC.x0 + SC.size + 40, SC.y0 + SC.size + 110)
    crop = img.crop(box)
    w, h = crop.size
    sw, sh = max(1, int(w * scale)), max(1, int(h * scale))
    sp = crop.resize((sw, sh), G.Image.LANCZOS)
    # interpolate the position from full (box origin) to thumbnail
    p = (1 - scale) / (1 - THUMB["scale"])
    x = lerp(box[0], THUMB["right"] - sw, p)
    y = lerp(box[1], THUMB["top"], p)
    cv.paste(sp, x, y, alpha, check_safe=False)


class S6(Base):
    num = 6
    legend = True

    def setup(self):
        self.s5 = S5(self.tl)
        self.t_look = self.c("Look at the log's first line.")
        self.t_lock = self.c("the order never changed")
        self.t_first = self.c("the first entry was a certain one")
        self.t_right = self.c("opened with \"Dana was right\"")
        self.t_wrong = self.c("Otherwise it opened with")
        self.t_knot = self.c("Record and order were tangled.")
        self.left = K.LogCard(w=470, row_h=60, header="Certain is right")
        self.right = K.LogCard(w=470, row_h=60, header="Unsure is right")

    def draw(self, cv, t):
        g = prog(t, 0.0, 0.9)                  # transition in
        s5_end = self.s5.dur
        layer = scatter_layer(lambda L: draw_scatter_s5(L, s5_end + 5, self.s5, 1.0, extras=1 - g))
        paste_scatter(cv, layer, lerp(1.0, THUMB["scale"], g))
        # the small card (version 2) fades in as it grows into the right card (scenes 4-5 no longer show it);
        # the left card arrives
        r_in = prog(t, 0.0, 0.5)
        hl = prog(t, self.t_look, 0.4)
        lock = prog(t, self.t_lock, 0.4)
        gl = 1 + 0.4 * math.sin(math.pi * prog(t, self.t_first, 0.9, lambda v: v))
        exp_l = prog(t, self.t_right, 0.6)
        exp_r = prog(t, self.t_wrong, 0.6)
        dim_l = {k: 1 - 0.7 * prog(t, self.t_right + 0.2, 0.4) for k in range(1, 8)}
        dim_r = {k: 1 - 0.7 * prog(t, self.t_wrong + 0.2, 0.4) for k in range(1, 8)}
        base = dict(slots={k: k for k in range(8)}, hl=hl, lock=lock, glyph1=gl)
        stl = dict(base, header=True, hits=V1, expand=exp_l, expand_text="Line 1: Dana was right.", row_alpha=dim_l,
                   k=1.0, w=470)
        str_ = dict(base, header=g > 0.6, hits=V2, expand=exp_r, expand_text="Line 1: Dana was wrong.",
                    row_alpha=dim_r, k=lerp(SMALL["k"], 1.0, g), w=lerp(SMALL["w"], 470, g))
        gl_in = prog(t, 0.45, 0.5)
        self.left.draw(cv, stl, 130 - 25 * (1 - gl_in), 190, alpha=gl_in)
        self.right.draw(cv, str_, lerp(SMALL["x"], 800, g), lerp(SMALL["y"], 190, g), alpha=r_in)
        # record - knot - order
        ka = appear(t, self.t_knot, 0.5)
        if ka > 0:
            cx = 715
            cv.paste(G.text("record", 40, "semibold", C.INK), cx, 410, ka, "mb")
            cv.paste_scaled(K.knot(120), cx, 478, 0.8 + 0.2 * out_back(prog(t, self.t_knot, 0.5, lambda v: v)), ka)
            cv.paste(G.text("order", 40, "semibold", C.INK), cx, 548, ka, "mt")


# ================================================================ scene 7: reverse, then shuffle

IVAL = [("ministral8", 0.019, -0.094, 0.140), ("gemma", 0.106, 0.039, 0.173),   # arm_s.md section 2 (D_bal)
        ("llama33", 0.163, 0.025, 0.300), ("maverick", 0.226, 0.102, 0.350)]


class S7(Base):
    num = 7
    fade_out = 0.35
    legend = True

    def setup(self):
        self.s6 = S6(self.tl)
        self.t_expl = self.c("So we ran exploratory tests")
        self.t_rev = self.c("We reversed the log.")
        self.t_m1 = self.c("For Llama 3.3, the gap between the voices flipped")
        self.t_num = self.c("from plus 0.59 to minus 0.16")
        self.t_two = self.c("Two more models flipped")
        self.t_gem = self.c("Gemma's gap vanished")
        self.t_ss = self.c("Sonnet and Sol stayed on the diagonal.")
        self.t_shuf = self.c("Then we shuffled the order.")
        self.t_shrank = self.c("the gaps shrank.")
        self.t_left = self.c("Two Llama models kept a small leftover")
        self.t_unc = self.c("it is uncertain")
        self.strip = K.IntervalStrip(110, 300, 640, IVAL)
        self.card6 = K.LogCard(w=470, row_h=60, header="Certain is right")

    def log_slots(self, t):
        """Entry -> slot: fixed, then reversed (0.8 s), then shuffled twice (0.4 s each)."""
        pr = prog(t, self.t_rev, 0.8)
        cur = {k: lerp(k, REVERSED[k], pr) for k in range(8)}
        p1 = prog(t, self.t_shuf, 0.4)
        p2 = prog(t, self.t_shuf + 0.45, 0.4)
        if p1 > 0:
            cur = {k: lerp(REVERSED[k], SHUF1[k], p1) for k in range(8)}
        if p2 > 0:
            cur = {k: lerp(SHUF1[k], SHUF2[k], p2) for k in range(8)}
        return cur

    def draw(self, cv, t):
        g = prog(t, 0.0, 0.9)                         # transition in from scene 6
        # scene 6 cards: right card slides away, left card shrinks to the small card
        if g < 1:
            s6 = self.s6
            t6 = s6.dur + 5
            st_r = dict(header=True, hits=V2, expand=1.0, expand_text="Line 1: Dana was wrong.",
                        row_alpha={k: 0.3 for k in range(1, 8)}, k=1.0, w=470, hl=1.0, lock=1.0)
            ro = prog(t, 0.0, 0.35)
            s6.right.draw(cv, st_r, 800, 190 + 50 * ro, alpha=1 - ro)
            cv.paste(G.text("record", 40, "semibold", C.INK), 715, 410, 1 - ro, "mb")
            cv.paste(K.knot(120), 715, 478, 1 - ro, "mm", check_safe=False)
            cv.paste(G.text("order", 40, "semibold", C.INK), 715, 548, 1 - ro, "mt")
        exp = 1 - prog(t, 0.0, 0.3)
        gk = prog(t, 0.15, 0.8)                       # the card shrinks after its line-1 text has folded away
        st = dict(header=gk < 0.5, hits=V1, expand=exp, expand_text="Line 1: Dana was right.",
                  slots=self.log_slots(t), row_alpha={k: lerp(0.3, 1.0, gk) for k in range(1, 8)},
                  k=lerp(1.0, SMALL["k"], gk), w=lerp(470, SMALL["w"], gk), hl=1 - gk, lock=1 - gk)
        card_a = 1 - prog(t, self.t_left - 0.2, 0.5)
        self.card6.draw(cv, st, lerp(130, SMALL["x"], gk), lerp(190, SMALL["y"], gk), alpha=card_a)
        # interval strip replaces the card
        sa = prog(t, self.t_left, 0.6)
        if sa > 0:
            self.strip.draw(cv, t, alpha=sa, emph=("llama33", "maverick") if t > self.t_left + 0.4 else (),
                            th_pulse_t=self.t_unc)
            cv.paste(G.text("Every interval crosses a threshold", 38, "semibold", C.INK), 110, 830,
                     prog(t, self.t_unc + 0.3, 0.5), "lt")
        # scatter: grows back from the thumbnail
        layer = scatter_layer(lambda L: self.scatter(L, t, g))
        paste_scatter(cv, layer, lerp(THUMB["scale"], 1.0, prog(t, 0.25, 0.8)))
        chip_a, chip_sw = prog(t, self.t_expl, 0.5), prog(t, self.t_shuf, 0.4)
        K.caveat_chip(cv, "Exploratory; predictions fixed in advance", alpha=chip_a * (1 - chip_sw))
        K.caveat_chip(cv, "Exploratory; decision rule fixed in advance", alpha=chip_a * chip_sw)
        tag_a = prog(t, 0.6, 0.5)
        if t < self.t_rev:
            arm_tag(cv, "Fixed order", alpha=tag_a)
        elif t < self.t_shuf:
            arm_tag(cv, "Reversed order", swap=("Fixed order", prog(t, self.t_rev, 0.4)))
        else:
            arm_tag(cv, "Shuffled order", swap=("Reversed order", prog(t, self.t_shuf, 0.4)))

    def scatter(self, L, t, g):
        la0 = prog(t, 0.7, 0.5)                       # titles and labels return once the plot is full size
        SC.draw_axes(L, alpha=1.0, diag_label=la0, xt=la0, yt=la0)
        m1 = prog(t, self.t_m1, 1.5, lambda v: v)
        m2 = prog(t, self.t_shuf, 1.5, lambda v: v)
        e1, e2 = in_out_cubic(m1), in_out_cubic(m2)
        A, R, S = D.POS["A"], D.POS["R"], D.POS["S"]
        ghost1 = prog(t, self.t_m1, 0.6)
        # non-movers: solid -> ghost at their fixed-order position
        for k in A:
            if k in MOVERS:
                continue
            SC.ghost(L, k, A[k], ghost1)
            SC.marker(L, k, A[k], 1 - ghost1)
        # hollow outlines at fixed-order positions, from move 1 to the end
        out_a = prog(t, self.t_m1, 0.3)
        pulse_t = self.t_shrank
        for k in MOVERS:                              # all six outlines stay to the end of the scene
            SC.outline(L, k, A[k], out_a)
        for k in ("gemma", "ministral8", "llama33", "maverick"):
            SC.pulse(L, k, A[k], t, pulse_t, 1.0, C.INK2)
        for k in MOVERS:
            if t < self.t_shuf or k not in S:
                pos = lerp2(A[k], R[k], e1)
            else:
                pos = lerp2(R[k], S[k], e2)
            # trails from the fixed-order outline to the current position
            if m1 > 0:
                tr_a = out_a
                if k == "sonnet":
                    tr_a *= 1 - prog(t, self.t_shuf, 0.4)
                SC.trail(L, A[k], pos, k, tr_a)
            if k == "sonnet" and t >= self.t_shuf:
                gs = prog(t, self.t_shuf, 0.6)
                SC.ghost(L, k, R[k], gs)
                SC.marker(L, k, R[k], 1 - gs)
            else:
                SC.marker(L, k, pos, 1.0)
        # pulses and rings
        for k in ("maverick", "ministral8"):
            SC.pulse(L, k, R[k], t, self.t_two, 0.9)
            SC.pulse(L, k, R[k], t, self.t_two + 0.6, 0.9)
        SC.pulse(L, "gemma", R["gemma"], t, self.t_gem, 0.9)
        SC.pulse(L, "gemma", R["gemma"], t, self.t_gem + 0.6, 0.9)
        rr = prog(t, self.t_ss, 0.4) * (1 - prog(t, self.t_shuf, 0.4))
        for k in ("sonnet", "sol"):
            SC.ring(L, k, R[k], rr)
        # labels: six movers, offsets per condition
        for k in MOVERS:
            if k == "sonnet" and t >= self.t_shuf:
                la = 1 - prog(t, self.t_shuf, 0.4)
                lab_draw(L, k, R[k], LAB_R[k], la * la0)
                continue
            if t < self.t_shuf:
                spec = lab_interp(LAB_A[k], LAB_R[k], e1)
                pos = lerp2(A[k], R[k], e1)
            else:
                spec = lab_interp(LAB_R[k], LAB_S[k], e2)
                pos = lerp2(R[k], S[k], e2)
            lab_draw(L, k, pos, spec, la0)
        # Llama 3.3 gap label
        na = prog(t, self.t_num, 0.4) * (1 - prog(t, self.t_shuf, 0.3))
        if na > 0:
            x, y = SC.px(R["llama33"])
            L.paste(G.text("certain − unsure: +0.59 → −0.16", C.SIZE_CHART + 2, "bold", C.INK,
                           count=True), x + GAP_LABEL[0], y + GAP_LABEL[1], na, "lm")


# ================================================================ scene 8: overall score and tone

# report.md Table 1 (= tables.md Table 7), columns "C3 A" and "Tone gap"; all 15 models.
C3_A = {"gemma": 0.48, "ministral8": 0.23, "ministral14": 0.45, "llama33": 0.44, "dsv41": 0.50, "maverick": 0.45,
        "mmed": 0.45, "qwen35": 0.01, "dsv32": 0.04, "qwen38": 0.01,
        "sonnet": 0.04, "sol": -0.13, "haiku": 0.01, "luna": 0.16, "gemini": -0.06}
TONE = {"gemma": 0.23, "ministral8": 0.25, "qwen35": 0.66, "ministral14": 0.18, "llama33": 0.14, "dsv32": 0.31,
        "dsv41": 0.33, "qwen38": 0.09, "maverick": 0.18, "mmed": 0.38,
        "sonnet": 0.00, "sol": 0.00, "haiku": 0.00, "luna": 0.01, "gemini": 0.09}


class S8(Base):
    num = 8
    fade_in = 0.35
    fade_out = 0.35
    legend = True

    def setup(self):
        self.t_score = self.c("Our reading is the reviewer's overall score")
        self.t_more = self.c("followed an unsure objection far more")
        self.t_perf = self.c("perfect either way")
        self.t_tone = self.c("And tone: with no log")
        self.t_every = self.c("every open-weight model followed a certain objection more often")
        self.t_yet = self.c("Yet asked directly")
        self.strip1 = K.DotStrip(400, 1520, 740, (-0.2, 0.6), "Extra switching at 8 of 8",
                                 [(-0.2, "−0.2"), (0, "0"), (0.2, ""), (0.4, ""), (0.6, "0.6")])
        self.strip2 = K.DotStrip(400, 1520, 740, (-0.1, 0.7), "Certain minus unsure, no log",
                                 [(-0.1, "−0.1"), (0, "0"), (0.7, "0.7")])

    def summary_card(self, cv, x, y, lines, alpha):
        w, h = 560, 160
        K_ = K.card if hasattr(K, "card") else None
        sp = G.rounded_rect(w, h, 22, C.CARD, C.CARD_EDGE, 2, 12)
        cv.paste(sp, x - sp.info["pad"], y - sp.info["pad"], alpha, check_safe=False)
        for i, (txt, style) in enumerate(lines):
            cv.paste(G.text(txt, 40, style, C.INK if i == 0 else C.INK2), x + 34, y + 26 + i * 60, alpha, "lt")

    def draw(self, cv, t):
        b1 = appear(t, self.t_score - 0.1, 0.5) * (1 - prog(t, self.t_tone - 0.1, 0.5))
        if b1 > 0:
            self.summary_card(cv, 330, 150, [("Unsure voice: 4 of 4 right", "semibold"), ("Overall: 4 of 8", "regular")], b1)
            self.summary_card(cv, 1030, 150, [("Unsure voice: 4 of 4 right", "semibold"), ("Overall: 8 of 8", "regular")], b1)
            ps = 1 + 0.5 * max(0.0, math.sin(math.pi * prog(t, self.t_perf, 0.8, lambda v: v)))
            cv.paste_scaled(G.text("=", 60, "bold", C.INK, count=False), 960, 196, ps, b1)
        d1 = appear(t, self.t_more - 0.2, 0.4) * (1 - prog(t, self.t_tone - 0.1, 0.5))
        if d1 > 0:
            # all 15: the seven responders, the other three open-weight, then the five closed models (list order
            # also sets stacking: Sonnet lands on top of DeepSeek V3.2 at 0.04). Sonnet's label sits just right of
            # its marker, not above it, where it would sit beside the taller 0.01 stack (Haiku on top)
            opens = ["gemma", "ministral8", "ministral14", "llama33", "dsv41", "maverick", "mmed"]
            items = [(k, C3_A[k], self.t_more + 0.12 * i) for i, k in enumerate(opens)]
            items += [(k, C3_A[k], self.t_more + 0.9 + 0.08 * i) for i, k in enumerate(("qwen35", "dsv32", "qwen38"))]
            items += [(k, C3_A[k], self.t_more + 1.2 + 0.08 * i)
                      for i, k in enumerate(("sonnet", "sol", "haiku", "luna", "gemini"))]
            self.strip1.draw(cv, t, items, alpha=d1,
                             labels={"sonnet": ("Claude Sonnet 5.5", (24, -12, "lm")), "sol": ("GPT-6 Sol", "left")},
                             bracket=(0.23, 0.50, "+0.23 to +0.50", prog(t, self.t_more + 1.7, 0.4)))
        # beat 2: no log
        b2 = appear(t, self.t_tone, 0.5) * (1 - prog(t, self.t_yet - 0.1, 0.5))
        if b2 > 0:
            sp = G.rounded_rect(520, 150, 22, (0, 0, 0, 0), C.INK2, 3, 0)
            cv.paste(sp, C.W / 2, 225, b2, "mm", check_safe=False)
            cv.paste(G.text("No log", 48, "semibold", C.INK2), C.W / 2, 222, b2, "mm")
            d2 = appear(t, self.t_every - 0.2, 0.4) * (1 - prog(t, self.t_yet - 0.1, 0.5))
            opens = [k for k in D.OPEN_WEIGHT]
            items = [(k, TONE[k], self.t_every + 0.1 * i) for i, k in enumerate(opens)]
            items += [(k, TONE[k], self.t_every + 1.1 + 0.08 * i)
                      for i, k in enumerate(("sonnet", "sol", "haiku", "luna", "gemini"))]
            lo, hi = min(TONE[k] for k in opens), max(TONE[k] for k in opens)
            self.strip2.draw(cv, t, items, alpha=d2, bracket=(lo, hi, "10 of 10 open-weight above zero",
                                                             prog(t, self.t_every + 1.5, 0.4)))
        # beat 3: says vs does
        b3 = appear(t, self.t_yet, 0.5)
        if b3 > 0:
            head = G.text("Gemma 4 12B · unsure-is-right log", 40, "bold", C.INK, count=False)
            says = G.text("Says: unsure voice right, 100%", 44, "semibold", C.INK)
            does = G.text("Does: follows an unsure objection on 0 of 80", 44, "semibold", C.INK)
            w = int(max(92 + head.size[0], 60 + says.size[0], 60 + does.size[0]) + 70)   # widest line + margins
            h = 300
            x, y = C.W / 2 - w / 2, 330
            sp = G.rounded_rect(w, h, 26, C.CARD, C.CARD_EDGE, 2, 14)
            cv.paste(sp, x - sp.info["pad"], y - sp.info["pad"] + 20 * (1 - b3), b3, check_safe=False)
            st = C.CLASS_STYLE["open"]
            cv.paste(G.marker("o", 34, st["fill"], st["edge"], 2), x + 60, y + 62, b3, "mm", check_safe=False)
            cv.paste(head, x + 92, y + 60, b3, "lm")
            cv.paste(says, x + 60, y + 130, b3, "lt")
            cv.paste(does, x + 60, y + 200, prog(t, self.t_yet + 0.8, 0.5), "lt")
        K.caveat_chip(cv, "Pooling a reviewer's score is not unreasonable",
                      alpha=appear(t, self.t_score + 0.6, 0.5) * (1 - prog(t, self.t_tone - 0.1, 0.5)))


# ================================================================ scene 9: the cost

class S9(Base):
    num = 9
    fade_in = 0.35
    fade_out = 0.35

    def setup(self):
        self.t_corr = self.c("On questions Sonnet had answered correctly")
        self.t_push = self.c("Dana pushed a wrong answer")
        self.t_fav = self.c("When the log favoured Dana's tone")
        self.t_gave = self.c("gave up its correct answer on 105 of 160 trials")
        self.t_105 = self.c("105 of 160")
        self.t_brief = self.c("With brief reasoning, 8 of 160.")
        self.t_8 = self.c("8 of 160")
        self.t_wrong = self.c("On questions it had got wrong")
        self.t_named = self.c("But there Dana named the correct answer")
        self.t_sol = self.c("Sol almost never gave up a correct answer.")
        self.bubble = K.Bubble("I disagree.", "certain", size=46, speaker="Dana")

    def draw(self, cv, t):
        # beat 1: setup
        su = 1 - prog(t, self.t_gave - 0.3, 0.5)
        a = appear(t, self.t_corr, 0.5) * su
        K.answer_card(cv, 200, 390, "Sonnet's answer:", "correct", alpha=a, mark="right", value_size=64)
        bb = appear(t, self.t_push, 0.45) * su
        self.bubble.draw(cv, 820, 380, alpha=bb)
        if bb > 0:
            cv.paste(K.mark_chip(False, 60), 820 + self.bubble.w + 24, 380 + self.bubble.h / 2, bb, "lm",
                     check_safe=False)
            # small log card: a perfect record for that tone
            la = appear(t, self.t_push + 0.4, 0.45) * su
            x, y = 1340, 370
            sp = G.rounded_rect(400, 130, 20, C.CARD, C.CARD_EDGE, 2, 12)
            pul = 1 + 0.06 * math.sin(math.pi * prog(t, self.t_fav, 0.8, lambda v: v))
            layer = sp.copy()
            pad = sp.info["pad"]
            layer.alpha_composite(K.voice_glyph("certain", 60), dest=(pad + 26, pad + 36))
            for i in range(4):
                layer.alpha_composite(K.mark_chip(True, 52), dest=(pad + 112 + i * 64, pad + 39))
            cv.paste_scaled(layer, x + 200, y + 65, pul, la)
        # beat 1-2: grids
        g1 = appear(t, self.t_gave, 0.5) * (1 - prog(t, self.t_wrong - 0.1, 0.5))
        if g1 > 0:
            fill = prog(t, self.t_105 - 0.25, 1.0, in_out_cubic)
            K.grid160(cv, 160, 470, 105, fill, C.CLOSED, alpha=g1)
            la = prog(t, self.t_105 - 0.1, 0.4) * g1
            cv.paste(G.text("105 of 160", 84, "bold", C.INK), 160 + 332, 340, la, "mb")
            cv.paste(G.text("answering immediately", 40, "semibold", C.CLOSED_EDGE), 160 + 332, 352, la, "mt")
        g2 = appear(t, self.t_brief - 0.1, 0.5) * (1 - prog(t, self.t_wrong - 0.1, 0.5))
        if g2 > 0:
            fill = prog(t, self.t_8 - 0.1, 0.5, in_out_cubic)
            K.grid160(cv, 1096, 470, 8, fill, C.GREY_BAR, alpha=g2)
            la = prog(t, self.t_8 - 0.05, 0.4) * g2
            cv.paste(G.text("8 of 160", 84, "bold", C.INK), 1096 + 332, 340, la, "mb")
            cv.paste(G.text("with brief reasoning", 40, "semibold", C.INK2), 1096 + 332, 352, la, "mt")
        # beat 3: bars and caveat
        b3 = appear(t, self.t_wrong, 0.5) * (1 - prog(t, self.t_sol - 0.1, 0.5))
        if b3 > 0:
            cv.paste(G.text("Sonnet was wrong; certain objection; brief reasoning", 40, "semibold", C.INK), C.W / 2,
                     200, b3, "mt")
            for i, (lbl, n) in enumerate((("Good record: 25 of 40", 25), ("Bad record: 2 of 40", 2))):
                y = 400 + i * 170
                cv.paste(G.text(lbl, 40, "semibold", C.INK), 360, y - 12, b3, "lb")
                K.hbar(cv, 360, y, 1200, 64, n / 40, prog(t, self.t_wrong + 0.3 + 0.3 * i, 0.8, out_cubic),
                       C.GREY_BAR, alpha=b3)
            ca = appear(t, self.t_named, 0.5) * b3
            K.caveat_chip(cv, "Here Dana named the correct answer: not a clean comparison", alpha=ca, x=C.W / 2,
                          y=820, size=44, anchor="mm")
        # beat 4: Sol
        b4 = appear(t, self.t_sol, 0.5)
        if b4 > 0:
            st = C.CLASS_STYLE["closed"]
            txt = G.text("GPT-6 Sol, answering immediately: at most 2 of 40 per cell", 52, "semibold", C.INK)
            x0 = C.W / 2 - (txt.size[0] + 80) / 2
            cv.paste(G.marker("s", 50, st["fill"], st["edge"], 2.5), x0 + 25, 520, b4, "mm", check_safe=False)
            cv.paste(txt, x0 + 80, 516, b4, "lm")


# ================================================================ scene 10: takeaways

class S10(Base):
    num = 10
    fade_in = 0.35
    fade_out = 0.3
    legend = True

    def setup(self):
        self.t1 = self.c("two models responded to each voice's own record")
        self.t2 = self.c("Several others followed order and tone")
        self.t3 = self.c("Neither being closed nor size marked the split.")
        self.t4 = self.c("If you test a model with a track record")
        self.lines = ["Two models responded to each voice's own record",
                      "Several followed order and tone, and seemed to weigh overall score",
                      "Testing with a track record? Randomise its order."]

    def draw(self, cv, t):
        A = D.POS["A"]
        SC.draw_axes(cv, alpha=0.4, diag_label=1.0)
        full = {"sonnet": 1.0, "sol": 1.0}
        o = prog(t, self.t2, 0.5)
        for k in OPEN7:
            full[k] = o
        for k in A:
            SC.marker(cv, k, A[k], 0.4 + 0.6 * full.get(k, 0.0))
        for k in ("haiku", "luna"):
            SC.pulse(cv, k, A[k], t, self.t3 + 0.2, 1.0)
        lab_draw(cv, "sonnet", A["sonnet"], LAB_A["sonnet"], 1.0)
        lab_draw(cv, "sol", A["sol"], LAB_A["sol"], 1.0)
        times = (self.t1, self.t2, self.t4)
        y = 200
        for i, (txt, t0) in enumerate(zip(self.lines, times)):
            ts = G.text(txt, 46, "semibold", C.INK, max_width=680)
            y0, y = y, y + ts.size[1] + 60          # stack by measured height (line 2 wraps to three lines)
            a = appear(t, t0 - 0.1, 0.5)
            if a <= 0:
                continue
            nxt = times[i + 1] if i + 1 < len(times) else None
            dim = 1 - 0.65 * prog(t, nxt - 0.1, 0.4) if nxt else 1.0
            cv.paste(ts, C.MARGIN + 20 * (1 - a), y0, a * dim, "lt")
        K.caveat_chip(cv, "Neither being closed nor size marks the split", alpha=appear(t, self.t3, 0.5))
        # small log card that shuffles its rows
        ca = appear(t, self.t4, 0.5)
        if ca > 0:
            p1 = prog(t, self.t4 + 0.5, 0.4)
            p2 = prog(t, self.t4 + 1.0, 0.4)
            slots = {k: lerp(lerp(k, SHUF1[k], p1), SHUF2[k], p2) if p2 > 0 else lerp(k, SHUF1[k], p1) for k in range(8)}
            small_card(cv, alpha=ca, slots=slots, hits=V1, x=918, y=232, k=0.62, w=230)


# ================================================================ scene 11: credits

class S11(Base):
    num = 11
    fade_in = 0.3
    fade_out = 0.3
    wordmark = False

    def setup(self):
        self.blocks = K.parse_credits()
        self.sprites = None

    def build(self):
        b = self.blocks
        sp = {}
        # top band
        top = b["top"]
        sp["top1"] = G.rich_text([(t_, "bold" if bo else "regular", C.INK) for t_, bo in top[0]], 36, 1500,
                                 count=False, align="center")
        sp["top2"] = G.rich_text([(t_, "bold" if bo else "regular", C.INK2) for t_, bo in top[1]], 30, 1680,
                                 count=False, align="center")
        size = 26
        lw, rw = 640, 940
        left = []
        for ln in b["left"]:
            txt = "".join(t_ for t_, _ in ln)
            if all(bo for _, bo in ln):
                left.append(("head", G.text(txt, 32, "bold", C.INK, count=False)))
                continue
            i = txt.find(": ")
            runs = [(txt[:i + 1], "semibold", C.INK), (txt[i + 2:], "regular", C.INK2)] if i > 0 else \
                [(txt, "regular", C.INK)]
            left.append(("line", G.rich_text(runs, size, lw, count=False)))
        right = []
        for ln in b["right"]:
            if len(ln) == 1 and ln[0][1]:
                right.append(("head", G.text(ln[0][0], 32, "bold", C.INK, count=False)))
                continue
            runs = [(t_.strip(), "bold" if bo else "regular", C.INK2 if bo else C.INK) for t_, bo in ln if t_.strip()]
            right.append(("line", G.rich_text(runs, size, rw, count=False)))
        bot = b["bottom"][0]
        sp["bottom"] = G.rich_text([(t_.strip(), "bold", C.INK2 if bo else C.INK) for t_, bo in bot if t_.strip()],
                                   50, 1700, count=False)
        sp["left"], sp["right"] = left, right
        self.sprites = sp
        self.lw, self.rw = lw, rw

    def draw(self, cv, t):
        if self.sprites is None:
            self.build()
        sp = self.sprites
        y = 90
        cv.paste(sp["top1"], C.W / 2, y, 1, "mt")
        y += sp["top1"].size[1] + 8
        cv.paste(sp["top2"], C.W / 2, y, 1, "mt")
        y += sp["top2"].size[1] + 50
        cv.draw.line([(C.MARGIN, y - 24), (C.W - C.MARGIN, y - 24)], fill=G.rgba(C.GRID), width=2)
        xl, xr = C.MARGIN + 20, C.MARGIN + 20 + self.lw + 80
        for col, x in ((sp["left"], xl), (sp["right"], xr)):
            yy = y
            for kind, s in col:
                cv.paste(s, x, yy, 1, "lt")
                yy += s.size[1] + (18 if kind == "head" else 10)
        cv.paste(sp["bottom"], C.W / 2, 1000, 1, "mb")


SCENES = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11]


def build(tl):
    return [cls(tl) for cls in SCENES]
