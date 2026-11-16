"""Global settings for the Loud-or-Right explainer: frame size, palette, fonts, paths and timing defaults.

Everything visual reads its colours and font files from here, so the look stays consistent with the paper's
figures (paper/make_figs.py: open-weight blue circles, closed orange squares, recency-tier green triangles).
"""
from pathlib import Path

# ---------------------------------------------------------------- paths
SRC = Path(__file__).resolve().parent
VIDEO = SRC.parent                      # paper/video
PAPER = VIDEO.parent                    # paper
ROOT = PAPER.parent                     # project root
ENV_FILE = ROOT / ".env"
BUILD = VIDEO / "build"                 # intermediate files (audio clips, segments, frames for QC)
AUDIO_CACHE = BUILD / "tts_cache"

# ---------------------------------------------------------------- frame
W, H = 1920, 1080
FPS = 30
SR = 48000                              # audio sample rate for every clip and the master track
MARGIN = 100                            # safe margin left/right (text must stay inside)
SAFE = (MARGIN, 46, W - MARGIN, H - 46)  # x0, y0, x1, y1 for text (about 5% action-safe)

# ---------------------------------------------------------------- palette (paper figure colours)
BG = (250, 250, 247)        # #FAFAF7 (plan.md)
INK = (31, 35, 40)          # #1F2328
INK2 = (122, 122, 117)      # #7A7A75 secondary ink and grid
MUTED = (122, 122, 117)
REF = (181, 179, 171)
GRID = (226, 225, 219)
CARD = (255, 255, 255)
CARD_EDGE = (222, 221, 215)
SHADOW = (0, 0, 0, 22)

OPEN = (42, 111, 219)       # #2A6FDB
OPEN_EDGE = (27, 84, 172)
CLOSED = (232, 102, 58)     # #E8663A
CLOSED_EDGE = (183, 72, 34)
RECENCY = (31, 167, 116)    # #1FA774
RECENCY_EDGE = (20, 122, 84)
GREY_BAR = (122, 122, 117)  # #7A7A75, brief reasoning (Figure 2b grey)
GREY_LIGHT = (185, 183, 176)

CHECK = (31, 35, 40)        # right: a tick in ink on a pale grey chip (green is the recency tier)
CHECK_CHIP = (232, 232, 228)
CROSS = (192, 57, 43)       # #C0392B wrong: crimson cross on a pale red chip
CROSS_CHIP = (248, 224, 220)
HIGHLIGHT = (255, 226, 120)  # soft yellow band behind a highlighted log line
ACCENT = OPEN

CLASS_STYLE = {
    "open": dict(fill=OPEN, edge=OPEN_EDGE, marker="o"),
    "closed": dict(fill=CLOSED, edge=CLOSED_EDGE, marker="s"),
    "recency": dict(fill=RECENCY, edge=RECENCY_EDGE, marker="^"),
}

# ---------------------------------------------------------------- fonts (Segoe UI family, Windows)
FONT_DIR = Path("C:/Windows/Fonts")
FONTS = {
    "regular": FONT_DIR / "segoeui.ttf",
    "semilight": FONT_DIR / "segoeuisl.ttf",
    "light": FONT_DIR / "segoeuil.ttf",
    "semibold": FONT_DIR / "seguisb.ttf",
    "bold": FONT_DIR / "segoeuib.ttf",
    "italic": FONT_DIR / "segoeuii.ttf",
    "symbol": FONT_DIR / "seguisym.ttf",
}
# Sizes in px at 1080p. Body text never below 36 px (plan.md); titles 70-90 px.
SIZE_TITLE = 86
SIZE_H2 = 64
SIZE_BODY = 44
SIZE_SMALL = 40
SIZE_TICK = 30          # axis tick numbers (plan: chart labels >= 28 px)
SIZE_CHIP = 36          # caveat chips (body text >= 36 px)
SIZE_CHART = 32         # chart labels and point labels (plan: >= 28 px)

# ---------------------------------------------------------------- timing defaults (seconds)
LEAD_IN = 0.40          # silence before the VO starts in each scene (elements begin to enter)
TAIL_PAD = 0.60         # breathing room after the VO (brief: 0.4-0.8 s)
EXIT_FADE = 0.45        # every scene fades its own elements out over its last EXIT_FADE seconds
ENTER = 0.55            # default element entrance (fade + slide)
CREDITS_HOLD = 4.0      # plan.md: one still screen held 4 s (0.3 s fade in, 0.3 s fade out)
MIN_TOTAL = 180.0       # 3:00 floor for scenes 1-10 alone
TARGET = (190.0, 210.0)  # 3:10-3:30
MAX_WORDS_ON_SCREEN = 15  # not counting axis titles, tick labels, point names, credits
