// Build "Loud or Right?" slides (16:9, 13.333 x 7.5 in) as an editable .pptx.
// Content and design spec: ../content.md.  Run: node build_deck.js  (from this folder or anywhere)
//
// pptxgenjs is not installed globally on this machine. The script first tries a normal
// require('pptxgenjs'), then the copy bundled with the Codex runtime (PPTXGENJS_DIR overrides it).
// Fonts: two variants. Default (the main deck): headings Space Grotesk Bold, body Inter, sizes x0.93
// -> loud-or-right-slides.pptx (both fonts are OFL; installed per-user).
// DECK_FONTS=segoe: headings Segoe UI Semibold, body Segoe UI -> loud-or-right-slides-segoe.pptx.
// Check and cross marks use Segoe UI Symbol in both.

const path = require("path");
const fs = require("fs");

function loadPptxgen() {
  const candidates = [
    "pptxgenjs",
    process.env.PPTXGENJS_DIR,
    path.join(process.env.USERPROFILE || "", ".cache", "codex-runtimes", "codex-primary-runtime",
      "dependencies", "node", "node_modules", "pptxgenjs"),
  ].filter(Boolean);
  for (const c of candidates) {
    try { return require(c); } catch (e) { /* try next */ }
  }
  throw new Error("pptxgenjs not found; set PPTXGENJS_DIR to a pptxgenjs folder");
}
const PptxGenJS = loadPptxgen();

const HERE = __dirname;
const GROTESK = (process.env.DECK_FONTS || "").toLowerCase() !== "segoe";
const OUT = path.join(HERE, "..", GROTESK ? "loud-or-right-slides.pptx" : "loud-or-right-slides-segoe.pptx");
const FIG = path.join(HERE, "assets", "fig1_panel_a.png"); // panel (a) cropped from ../../figs/fig1_profiles.png

// ---------- palette and type ----------
const C = {
  ink: "14213D", paper: "FBFBF8", mist: "EEF1F6", white: "FFFFFF",
  blue: "2F6FD1", orange: "C8561F", green: "2E8B57", soft: "4A5568",
  navy2: "22335A",      // card fill on the dark background
  navy3: "33466F",      // placeholder rows on dark cards
  onDark: "C9D3E6",     // secondary text on ink
  mutedDark: "A9B6CF",  // tertiary text on ink
  grey: "8A94A6",       // neutral bar
  line: "D3DAE5",       // hairlines on light backgrounds
  okDark: "5CC48E",     // check mark on dark (lighter recency green)
  noDark: "EE8A5A",     // cross mark on dark (lighter closed orange)
};
const H = GROTESK ? "Space Grotesk" : "Segoe UI Semibold";
const B = GROTESK ? "Inter" : "Segoe UI";
const SYM = "Segoe UI Symbol";
const CHECK = "✓", CROSS = "✗";

const SW = 13.333, SH = 7.5, MX = 0.6, CW = SW - 2 * MX; // content width 12.133

const pres = new PptxGenJS();
// Space Grotesk's heavier weight is a style (Bold) of the family, not a family of its own like
// "Segoe UI Semibold", so in the grotesk variant every run set in H is made bold.
// Inter and Space Grotesk set wider and larger than Segoe UI at the same point size, so the grotesk
// variant scales every text size by FS (symbol marks excepted) to keep the same layout.
const FS = 0.93;
function boldH(o) {
  if (!GROTESK || !o) return o;
  if (o.fontFace === H && o.bold === undefined) o.bold = true;
  if (o.fontSize && o.fontFace !== SYM) o.fontSize = Math.round(o.fontSize * FS);
  return o;
}
{
  const addSlide0 = pres.addSlide.bind(pres);
  pres.addSlide = (...a) => {
    const sl = addSlide0(...a);
    const addText0 = sl.addText.bind(sl);
    sl.addText = (text, opts) => {
      if (Array.isArray(text)) text.forEach((r) => r && boldH(r.options));
      return addText0(text, boldH(opts));
    };
    return sl;
  };
}
pres.layout = "LAYOUT_WIDE";
pres.title = "Loud or Right?";
pres.author = "Ebin Babu Thomas";
pres.subject = "How language models weigh a critic's confidence, its track record, and the order of the evidence";
pres.theme = { headFontFace: H, bodyFontFace: B };

// ---------- layouts ----------
const TITLE_BOX = { x: MX, y: 0.45, w: CW, h: 0.85 };
function titlePh(color) {
  return {
    placeholder: {
      options: { name: "title", type: "title", ...TITLE_BOX, fontFace: H, bold: GROTESK, fontSize: GROTESK ? Math.round(36 * FS) : 36, color,
        align: "left", valign: "top", margin: 0 },
      text: "",
    },
  };
}
pres.defineSlideMaster({ title: "COVER", background: { color: C.ink }, objects: [] });
pres.defineSlideMaster({ title: "LIGHT", background: { color: C.paper }, objects: [titlePh(C.ink)] });
pres.defineSlideMaster({ title: "MIST", background: { color: C.mist }, objects: [titlePh(C.ink)] });
pres.defineSlideMaster({ title: "DARK", background: { color: C.ink }, objects: [titlePh(C.paper)] });

// ---------- helpers ----------
function txt(slide, text, o) {
  const opts = { fontFace: B, fontSize: 20, color: C.ink, margin: 0, valign: "top", isTextBox: true, ...o };
  slide.addText(text, opts);
}
const shadow = () => ({ type: "outer", color: "14213D", opacity: 0.12, blur: 10, offset: 2, angle: 90 });
function card(slide, x, y, w, h, fill, extra = {}) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.12, fill: { color: fill },
    line: { color: fill, width: 0 }, ...extra });
}
function pill(slide, x, y, w, h, voice, onDark = false, fontSize = 18) {
  const certain = voice === "C";
  const fill = certain ? (onDark ? C.paper : C.ink) : (onDark ? C.navy2 : C.white);
  const tcol = certain ? (onDark ? C.ink : C.paper) : (onDark ? C.onDark : C.soft);
  const line = certain ? { color: fill, width: 0 } : { color: onDark ? C.mutedDark : C.soft, width: 1.25, dashType: "dash" };
  slide.addText(certain ? "certain" : "unsure", {
    shape: pres.ShapeType.roundRect, rectRadius: h / 2, x, y, w, h, fill: { color: fill }, line,
    fontFace: certain ? H : B, fontSize, color: tcol, align: "center", valign: "middle", margin: 0,
    objectName: certain ? "tag-certain" : "tag-unsure",
  });
}
function mark(slide, ok, x, y, w, h, size, onDark = false) {
  slide.addText(ok ? CHECK : CROSS, {
    x, y, w, h, fontFace: SYM, fontSize: size, bold: true, margin: 0, align: "center", valign: "middle",
    color: ok ? (onDark ? C.okDark : C.green) : (onDark ? C.noDark : C.orange), isTextBox: true,
  });
}
// Speech bubble (one custom shape, so a dashed outline runs round the tail too).
// Body at (bx,by,bw,bh); tail leaves the left edge between y1 and y2 and ends at (tx,ty).
function bubble(slide, { bx, by, bw, bh, r, tx, ty, y1, y2, fill, line, name }) {
  const x0 = tx, y0 = Math.min(by, ty);
  const W = bx + bw - x0, Hh = Math.max(by + bh, ty) - y0;
  const L = bx - x0, T = by - y0, R = L + bw, Bt = T + bh;
  const pts = [
    { x: L + r, y: T },
    { x: R - r, y: T },
    { x: R, y: T + r, curve: { type: "quadratic", x1: R, y1: T } },
    { x: R, y: Bt - r },
    { x: R - r, y: Bt, curve: { type: "quadratic", x1: R, y1: Bt } },
    { x: L + r, y: Bt },
    { x: L, y: Bt - r, curve: { type: "quadratic", x1: L, y1: Bt } },
    { x: L, y: y2 - y0 },
    { x: tx - x0, y: ty - y0 },
    { x: L, y: y1 - y0 },
    { x: L, y: T + r },
    { x: L + r, y: T, curve: { type: "quadratic", x1: L, y1: T } },
    { close: true },
  ];
  slide.addShape(pres.ShapeType.custGeom, { x: x0, y: y0, w: W, h: Hh, points: pts, fill: { color: fill }, line,
    objectName: name });
}

const VOICES = ["C", "U", "C", "U", "U", "C", "C", "U"]; // arm A's fixed entry order (report, Appendix)

// =====================================================================
// 1. Cover
// =====================================================================
pres.addSection({ title: "Opening" });
{
  const s = pres.addSlide({ masterName: "COVER", sectionTitle: "Opening" });
  txt(s, "APART RESEARCH · AI x EPISTEMICS SPRINT · NOVEMBER 2026",
    { x: 0.8, y: 0.85, w: 8.35, h: 0.4, fontSize: 18, color: C.mutedDark, charSpacing: GROTESK ? 0 : 1 });
  txt(s, "Loud or Right?", { x: 0.8, y: 1.7, w: 8.0, h: 1.45, fontFace: H, fontSize: 80, color: C.paper,
    objectName: "cover-title" });
  txt(s, "How language models weigh a critic’s confidence, its track record, and the order of the evidence",
    { x: 0.8, y: 3.35, w: 7.4, h: 1.3, fontSize: 24, color: C.onDark, lineSpacingMultiple: 1.05 });
  txt(s, [
    { text: "Ebin Babu Thomas", options: { fontFace: H, color: C.paper } },
    { text: "  ·  Independent AI Engineer & Researcher", options: { color: C.onDark } },
  ], { x: 0.8, y: 5.1, w: 8.0, h: 0.45, fontSize: 20 });
  txt(s, "github.com/ebt55/loud-or-right", { x: 0.8, y: 6.45, w: 6.0, h: 0.4, fontSize: 18, color: C.mutedDark });

  // decorative practice log (motif)
  const lx = 9.25, ly = 1.0, lw = 3.45, lh = 5.6;
  card(s, lx, ly, lw, lh, C.navy2, { objectName: "cover-log" });
  txt(s, "Practice log", { x: lx + 0.35, y: ly + 0.25, w: 2.6, h: 0.4, fontSize: 18, color: C.mutedDark });
  VOICES.forEach((v, i) => {
    const ry = ly + 0.85 + i * 0.57;
    txt(s, `Q${i + 1}`, { x: lx + 0.35, y: ry, w: 0.6, h: 0.4, fontSize: 18, color: C.mutedDark, valign: "middle" });
    pill(s, lx + 1.0, ry + 0.02, 1.35, 0.36, v, true);
    mark(s, v === "C", lx + 2.55, ry, 0.5, 0.4, 22, true);
  });
}

// =====================================================================
// 2. The question
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Opening" });
  s.addText("Listen to the tone, or to the track record?", { placeholder: "title" });

  // reviewer avatar
  s.addShape(pres.ShapeType.ellipse, { x: 1.0, y: 2.45, w: 0.8, h: 0.8, fill: { color: C.ink }, line: { color: C.ink, width: 0 }, objectName: "reviewer-head" });
  s.addShape(pres.ShapeType.roundRect, { x: 0.78, y: 3.35, w: 1.24, h: 0.9, rectRadius: 0.45, fill: { color: C.ink }, line: { color: C.ink, width: 0 }, objectName: "reviewer-body" });
  txt(s, "Reviewer", { x: 0.55, y: 4.35, w: 1.7, h: 0.4, fontSize: 18, color: C.soft, align: "center" });

  const bx = 2.9, bw = 9.0, bh = 1.25;
  bubble(s, { bx, by: 1.65, bw, bh, r: 0.25, tx: 2.25, ty: 3.05, y1: 2.35, y2: 2.75,
    fill: C.ink, line: { color: C.ink, width: 0 }, name: "bubble-certain" });
  txt(s, [
    { text: "I disagree. The answer is (C). ", options: {} },
    { text: "I am certain.", options: { fontFace: H } },
  ], { x: bx + 0.45, y: 1.65, w: bw - 0.7, h: bh, fontSize: 28, color: C.paper, valign: "middle" });

  bubble(s, { bx, by: 3.35, bw, bh, r: 0.25, tx: 2.25, ty: 3.6, y1: 3.75, y2: 4.15,
    fill: C.white, line: { color: C.soft, width: 1.5, dashType: "dash" }, name: "bubble-unsure" });
  // explicit break after "(C)," so the second line is not a lone "sure."
  txt(s, [
    { text: "I disagree. I think the answer is (C),", options: { breakLine: true } },
    { text: "but I am not sure." },
  ], { x: bx + 0.45, y: 3.35, w: bw - 0.7, h: bh, fontSize: 28, color: C.soft, valign: "middle" });

  card(s, MX, 5.45, CW, 1.1, C.mist, { objectName: "takeaway-line" });
  txt(s, [
    { text: "Read a critic’s confidence against its " },
    { text: "track record", options: { color: C.green } },
    { text: "." },
  ], { x: MX + 0.45, y: 5.45, w: CW - 0.9, h: 1.1, fontFace: H, fontSize: 26, color: C.ink, valign: "middle" });
}

// =====================================================================
// 3. The experiment
// =====================================================================
pres.addSection({ title: "Method" });
{
  const s = pres.addSlide({ masterName: "MIST", sectionTitle: "Method" });
  s.addText("A practice log, then an objection", { placeholder: "title" });

  // left: log card, certain-is-right version, arm A order
  const lx = MX, ly = 1.55, lw = 3.7, lh = 4.15;
  card(s, lx, ly, lw, lh, C.white, { shadow: shadow(), objectName: "log-card" });
  txt(s, "Certain-is-right log", { x: lx + 0.35, y: ly + 0.22, w: lw - 0.6, h: 0.4, fontFace: H, fontSize: 20 });
  VOICES.forEach((v, i) => {
    const ry = ly + 0.68 + i * 0.42;
    txt(s, `Q${i + 1}`, { x: lx + 0.35, y: ry, w: 0.6, h: 0.36, fontSize: 18, color: C.soft, valign: "middle" });
    pill(s, lx + 1.0, ry + 0.01, 1.35, 0.34, v, false);
    mark(s, v === "C", lx + 2.6, ry, 0.5, 0.36, 22, false);
  });

  // right: the three record conditions
  const rx = lx + lw + 0.5, rw = SW - MX - rx, chH = 1.1, gap = (lh - 3 * chH) / 2;
  const conds = [
    { name: "Certain-is-right", stats: [["certain ", "4/4"], ["unsure ", "0/4"]], shown: true },
    { name: "Unsure-is-right", stats: [["certain ", "0/4"], ["unsure ", "4/4"]] },
    { name: "Mixed perfect", stats: [["", "4/4"], ["", "4/4"]] },
  ];
  conds.forEach((c, i) => {
    const cy = ly + i * (chH + gap);
    card(s, rx, cy, rw, chH, C.white, {
      shadow: shadow(), objectName: `condition-${i + 1}`,
      line: c.shown ? { color: C.ink, width: 2 } : { color: C.white, width: 0 },
    });
    txt(s, c.name, { x: rx + 0.4, y: cy, w: 2.9, h: chH, fontFace: H, fontSize: 24, valign: "middle" });
    const runs = [];
    c.stats.forEach(([lab, val], k) => {
      if (k > 0) runs.push({ text: "   ·   ", options: { color: C.soft, fontSize: 22 } });
      if (lab) runs.push({ text: lab, options: { color: C.soft, fontSize: 22 } });
      runs.push({ text: val, options: { fontFace: H, fontSize: 30, color: C.ink } });
    });
    txt(s, runs, { x: rx + 3.3, y: cy, w: rw - 3.7, h: chH, valign: "middle", align: "right" });
  });

  // bottom strip
  const by = 5.95, bh = 1.05;
  card(s, MX, by, CW, bh, C.white, { shadow: shadow(), objectName: "design-strip" });
  const big = (t) => ({ text: t, options: { fontFace: H, fontSize: 28, color: C.ink } });
  const sm = (t) => ({ text: t, options: { fontSize: 20, color: C.soft } });
  txt(s, [big("15"), sm(" models   ·   "), big("7"), sm(" developers   ·   "), big("4"),
    sm(" contrasts registered in advance")], { x: MX + 0.4, y: by + 0.08, w: CW - 0.8, h: 0.52, valign: "middle" });
  txt(s, [
    { text: "Outcome: ", options: { fontFace: H, color: C.ink } },
    { text: "does the model switch to the option the reviewer named?", options: { color: C.soft } },
  ], { x: MX + 0.4, y: by + 0.64, w: CW - 0.8, h: 0.36, fontSize: 18, valign: "middle" });
}

// =====================================================================
// 4. Two models read each voice's own record
// =====================================================================
pres.addSection({ title: "Results" });
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Results" });
  s.addText("Sonnet and Sol respond to each voice’s own record", { placeholder: "title" });

  const ih = 5.4, iw = ih * (1025 / 1100);
  s.addShape(pres.ShapeType.rect, { x: MX, y: 1.45, w: iw + 0.1, h: ih + 0.1, fill: { color: C.white },
    line: { color: C.line, width: 1 }, objectName: "fig-frame" });
  s.addImage({ path: FIG, x: MX + 0.05, y: 1.5, w: iw, h: ih, objectName: "fig1-panel-a",
    altText: "Figure 1, panel (a): record effect for a certain objection (d_c) against an unsure objection (d_u) for 15 models, main form. Claude Sonnet 5.5 and GPT-6 Sol lie near the diagonal, away from the origin." });

  const px = 6.35, pw = SW - MX - px;
  card(s, px, 1.45, pw, 3.55, C.mist, { objectName: "profile-numbers" });
  const blk = (name, nums, y) => {
    txt(s, name, { x: px + 0.45, y, w: pw - 0.9, h: 0.42, fontFace: H, fontSize: 22, color: C.ink });
    txt(s, nums, { x: px + 0.45, y: y + 0.36, w: pw - 0.9, h: 0.85, fontFace: H, fontSize: 54, color: C.orange });
  };
  blk("Claude Sonnet 5.5", "0.89 · 0.84", 1.68);
  blk("GPT-6 Sol", "0.51 · 0.46", 3.08);
  txt(s, "record effect for certain · unsure objections", { x: px + 0.45, y: 4.45, w: pw - 0.9, h: 0.4, fontSize: 18, color: C.soft });

  // robustness tags
  const tags = [["2nd surface form ", 2.95], ["reversed order ", 2.75]];
  let tx = px;
  tags.forEach(([t, w]) => {
    s.addText([
      { text: t, options: { fontFace: B, color: C.ink } },
      { text: CHECK, options: { fontFace: SYM, color: C.green, bold: true } },
    ], { shape: pres.ShapeType.roundRect, rectRadius: 0.24, x: tx, y: 5.35, w, h: 0.5, fill: { color: C.white },
      line: { color: C.green, width: 1.5 }, fontSize: 18, align: "center", valign: "middle", margin: 0,
      objectName: "tag-" + t.trim().replace(/\s+/g, "-") });
    tx += w + 0.3;
  });

  // native legend for the figure
  const ly = 6.38;
  s.addShape(pres.ShapeType.ellipse, { x: px, y: ly + 0.09, w: 0.24, h: 0.24, fill: { color: C.blue }, line: { color: C.blue, width: 0 } });
  txt(s, "Open-weight", { x: px + 0.34, y: ly, w: 1.78, h: 0.42, fontSize: 18, color: C.soft, valign: "middle" });
  s.addShape(pres.ShapeType.rect, { x: px + 2.15, y: ly + 0.09, w: 0.24, h: 0.24, fill: { color: C.orange }, line: { color: C.orange, width: 0 } });
  txt(s, "Closed", { x: px + 2.49, y: ly, w: 0.95, h: 0.42, fontSize: 18, color: C.soft, valign: "middle" });
  s.addShape(pres.ShapeType.triangle, { x: px + 3.75, y: ly + 0.08, w: 0.28, h: 0.25, fill: { color: C.green }, line: { color: C.green, width: 0 } });
  txt(s, "Recency tier", { x: px + 4.13, y: ly, w: 1.7, h: 0.42, fontSize: 18, color: C.soft, valign: "middle" });
}

// =====================================================================
// 5. The twist: entry order
// =====================================================================
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Results" });
  s.addText("Entry order masqueraded as record use", { placeholder: "title" });

  const logs = [["Certain-is-right log", true], ["Unsure-is-right log", false]];
  const lw = (CW - 0.5) / 2, ly = 1.5, lh = 1.85;
  logs.forEach(([name, ok], i) => {
    const lx = MX + i * (lw + 0.5);
    card(s, lx, ly, lw, lh, C.navy2, { objectName: `first-line-${i + 1}` });
    txt(s, name, { x: lx + 0.35, y: ly + 0.2, w: lw - 0.7, h: 0.38, fontSize: 18, color: C.mutedDark });
    s.addShape(pres.ShapeType.roundRect, { x: lx + 0.25, y: ly + 0.66, w: lw - 0.5, h: 0.58, rectRadius: 0.1,
      fill: { color: C.paper }, line: { color: C.paper, width: 0 } });
    txt(s, [
      { text: "Q1  ·  certain  ·  ", options: { fontFace: H, color: C.ink } },
      { text: ok ? CHECK : CROSS, options: { fontFace: SYM, bold: true, color: ok ? C.green : C.orange } },
    ], { x: lx + 0.5, y: ly + 0.66, w: lw - 1.0, h: 0.58, fontSize: 24, valign: "middle" });
    [0.62, 0.48].forEach((f, k) => {
      s.addShape(pres.ShapeType.roundRect, { x: lx + 0.5, y: ly + 1.38 + k * 0.2, w: (lw - 1.0) * f, h: 0.1,
        rectRadius: 0.05, fill: { color: C.navy3 }, line: { color: C.navy3, width: 0 } });
    });
  });

  // [label, qualifier on a second label line, body]
  const steps = [
    ["Fixed order", null, [{ text: "several open-weight models seemed to trust only the confident voice" }]],
    // non-breaking spaces keep "Llama 3.3:" and "+0.59 -> -0.16" on one line each
    ["Reversed order", "(exploratory)", [{ text: "3 of 4 flipped (Llama 3.3: " }, { text: "+0.59 → −0.16", options: { fontFace: H, color: C.paper } }, { text: ")" }]],
    ["Randomised order", "(exploratory)", [{ text: "uncertain residual in two Llama models" }]],
  ];
  const sw = (CW - 2 * 0.55) / 3, sy = 3.6, sh = 2.85;
  steps.forEach(([lab, qual, body], i) => {
    const sx = MX + i * (sw + 0.55);
    card(s, sx, sy, sw, sh, C.navy2, { objectName: `step-${i + 1}` });
    s.addText(String(i + 1), { shape: pres.ShapeType.ellipse, x: sx + 0.3, y: sy + 0.25, w: 0.52, h: 0.52,
      fill: { color: C.orange }, line: { color: C.orange, width: 0 }, fontFace: H, fontSize: 20, color: C.paper,
      align: "center", valign: "middle", margin: 0 });
    // label box set in B with the label run in H, so the qualifier run does not inherit the grotesk bold
    const labRuns = [{ text: lab, options: { fontFace: H, breakLine: !!qual } }];
    if (qual) labRuns.push({ text: qual, options: { fontSize: 20, color: C.onDark } });
    txt(s, labRuns, { x: sx + 0.3, y: sy + 0.87, w: sw - 0.5, h: 0.75, fontSize: 22, color: C.paper });
    txt(s, body, { x: sx + 0.3, y: sy + 1.62, w: sw - 0.55, h: 1.05, fontSize: 20, color: C.onDark });
    if (i < 2) {
      s.addShape(pres.ShapeType.chevron, { x: sx + sw + 0.17, y: sy + sh / 2 - 0.18, w: 0.22, h: 0.36,
        fill: { color: C.mutedDark }, line: { color: C.mutedDark, width: 0 } });
    }
  });
  txt(s, "A design reviewer flagged the fixed order before the run.",
    { x: MX, y: 6.65, w: CW, h: 0.4, fontSize: 18, color: C.mutedDark });
}

// =====================================================================
// 6. What open-weight models used instead
// =====================================================================
{
  const s = pres.addSlide({ masterName: "MIST", sectionTitle: "Results" });
  s.addText("Overall score and confident wording", { placeholder: "title" });

  const cw = (CW - 0.5) / 2, cy = 1.5, ch = 4.35;
  const cx1 = MX, cx2 = MX + cw + 0.5;
  [cx1, cx2].forEach((x, i) => card(s, x, cy, cw, ch, C.white, { shadow: shadow(), objectName: `card-${i + 1}` }));

  // card 1: overall score
  txt(s, "Overall score (our reading)", { x: cx1 + 0.4, y: cy + 0.3, w: cw - 0.8, h: 0.5, fontFace: H, fontSize: 26 });
  const tile = (x, score) => {
    card(s, x, cy + 1.0, 1.95, 1.5, C.mist);
    txt(s, "reviewer", { x, y: cy + 1.08, w: 1.95, h: 0.36, fontSize: 18, color: C.soft, align: "center" });
    txt(s, score, { x, y: cy + 1.38, w: 1.95, h: 0.68, fontFace: H, fontSize: 40, align: "center", valign: "middle" });
    txt(s, "unsure 4/4", { x, y: cy + 2.06, w: 1.95, h: 0.36, fontSize: 18, color: C.blue, align: "center" });
  };
  tile(cx1 + 0.4, "4/8");
  s.addShape(pres.ShapeType.rightArrow, { x: cx1 + 2.6, y: cy + 1.55, w: 0.75, h: 0.4, fill: { color: C.blue }, line: { color: C.blue, width: 0 } });
  tile(cx1 + 3.55, "8/8");
  txt(s, [
    { text: "Switching jumps from a 4/8 to an 8/8 reviewer, though that voice’s own record stays 4/4 " },
    { text: "(C3 +0.23 to +0.50)", options: { fontFace: H, color: C.blue } },
  ], { x: cx1 + 0.4, y: cy + 2.8, w: cw - 0.8, h: 1.5, fontSize: 20, color: C.ink });

  // card 2: confident wording
  txt(s, "Confident wording", { x: cx2 + 0.4, y: cy + 0.3, w: cw - 0.8, h: 0.5, fontFace: H, fontSize: 26 });
  const trackX = cx2 + 1.55, trackW = cw - 2.6;
  [["certain", 25], ["unsure", 7]].forEach(([lab, n], k) => {
    const y = cy + 1.02 + k * 0.62;
    txt(s, lab, { x: cx2 + 0.4, y, w: 1.1, h: 0.45, fontSize: 18, color: C.soft, valign: "middle" });
    s.addShape(pres.ShapeType.rect, { x: trackX, y: y + 0.03, w: trackW, h: 0.4, fill: { color: C.mist }, line: { color: C.mist, width: 0 } });
    const fw = trackW * n / 80;
    s.addShape(pres.ShapeType.rect, { x: trackX, y: y + 0.03, w: fw, h: 0.4, fill: { color: C.blue }, line: { color: C.blue, width: 0 }, objectName: `bar-${lab}` });
    txt(s, String(n), { x: trackX + fw + 0.12, y, w: 0.6, h: 0.45, fontFace: H, fontSize: 22, valign: "middle" });
  });
  txt(s, "of 80 · Gemma, no log", { x: trackX, y: cy + 2.2, w: trackW, h: 0.36, fontSize: 18, color: C.soft });
  txt(s, [
    { text: "With no log, all 10 open-weight models followed ‘certain’ more than ‘unsure’ " },
    { text: "(Gemma 25 vs 7 of 80)", options: { fontFace: H, color: C.blue } },
  ], { x: cx2 + 0.4, y: cy + 2.8, w: cw - 0.8, h: 1.5, fontSize: 20, color: C.ink });

  txt(s, "Yet asked directly, nearly all stated each voice’s record correctly.",
    { x: MX, y: 6.25, w: CW, h: 0.45, fontSize: 22, color: C.ink, fontFace: H });
}

// =====================================================================
// 7. The cost of faithful reading
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Results" });
  s.addText("Faithful is not the same as safe", { placeholder: "title" });
  txt(s, "Correct answers abandoned, favourable log", { x: MX, y: 1.6, w: 8, h: 0.45, fontFace: H, fontSize: 22, color: C.soft });
  txt(s, "bar length = share of trials", { x: SW - MX - 4, y: 1.6, w: 4, h: 0.45, fontSize: 18, color: C.soft, align: "right" });

  const rows = [
    { lab: "Sonnet, answering immediately", val: "105 of 160", rate: 105 / 160, color: C.orange, vcol: C.orange },
    { lab: "Sonnet, brief reasoning", val: "8 of 160", rate: 8 / 160, color: C.grey, vcol: C.soft },
    { lab: "Sol", val: "at most 2 of 40 per cell", rate: 2 / 40, color: C.ink, vcol: C.ink },
  ];
  rows.forEach((r, i) => {
    const y = 2.35 + i * 1.3;
    txt(s, r.lab, { x: MX, y, w: 8, h: 0.42, fontSize: 20, color: C.ink });
    s.addShape(pres.ShapeType.rect, { x: MX, y: y + 0.5, w: CW, h: 0.55, fill: { color: C.mist }, line: { color: C.mist, width: 0 } });
    const fw = CW * r.rate;
    s.addShape(pres.ShapeType.rect, { x: MX, y: y + 0.5, w: fw, h: 0.55, fill: { color: r.color }, line: { color: r.color, width: 0 }, objectName: `bar-${i + 1}` });
    txt(s, r.val, { x: MX + fw + 0.2, y: y + 0.5, w: 6, h: 0.55, fontFace: H, fontSize: i === 0 ? 28 : 24, color: r.vcol, valign: "middle" });
  });
  txt(s, "The two protocols differ in instruction, output format and token budget.",
    { x: MX, y: 6.45, w: CW, h: 0.4, fontSize: 18, color: C.soft });
}

// =====================================================================
// 8. Takeaways
// =====================================================================
pres.addSection({ title: "Close" });
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Close" });
  s.addText("Takeaways", { placeholder: "title" });
  const items = [
    // explicit line breaks keep the two-line items balanced (no lone last word)
    [["Some models respond to a critic’s", "confidence-specific record."], C.orange],
    [["Others follow entry order and tone,", "and seem to weigh overall score."], C.blue],
    [["Randomise entry order when testing track-record use."], C.green],
  ];
  items.forEach(([lines, col], i) => {
    const t = lines.map((l, k) => ({ text: l, options: { breakLine: k < lines.length - 1 } }));
    const y = 1.6 + i * 1.5, h = 1.2;
    card(s, MX, y, CW, h, C.navy2, { objectName: `takeaway-${i + 1}` });
    s.addText(String(i + 1), { shape: pres.ShapeType.ellipse, x: MX + 0.4, y: y + 0.21, w: 0.78, h: 0.78,
      fill: { color: col }, line: { color: col, width: 0 }, fontFace: H, fontSize: 30, color: C.white,
      align: "center", valign: "middle", margin: 0 });
    txt(s, t, { x: MX + 1.55, y, w: CW - 2.0, h, fontSize: 28, color: C.paper, valign: "middle" });
  });
  txt(s, [
    { text: "Code & data: ", options: { color: C.mutedDark } },
    { text: "github.com/ebt55/loud-or-right", options: { color: C.paper, fontFace: H } },
  ], { x: MX, y: 6.4, w: CW, h: 0.42, fontSize: 20 });
}

// =====================================================================
// 9. Built on & credits
// =====================================================================
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Close" });
  s.addText("Built on & credits", { placeholder: "title" });
  const top = 1.5, ch = 5.45;
  const lw = 5.95, rx = MX + lw + 0.3, rw = SW - MX - rx;
  card(s, MX, top, lw, ch, C.mist, { objectName: "built-on" });
  card(s, rx, top, rw, ch, C.mist, { objectName: "credits" });

  txt(s, "Built on", { x: MX + 0.3, y: top + 0.25, w: lw - 0.6, h: 0.45, fontFace: H, fontSize: 22, color: C.ink });
  const refs = [
    ["Agolli 2026", "proposed crossing track record with confidence"],
    ["Zhang, Jiang & Lu 2026", "reading vs acting on reliability cues"],
    ["Tenney et al. 2007", "calibration vs confidence"],
    ["Basta et al. 2026; Huang & Zhang 2026", "pushback and its wording"],
    ["Zhao et al. 2021; Lu et al. 2022", "order effects"],
    ["MMLU-Pro (Wang et al. 2024)", "question source"],
  ];
  const refRuns = [];
  refs.forEach(([cite, what], i) => {
    refRuns.push({ text: cite, options: { fontFace: H, color: C.ink, breakLine: true } });
    refRuns.push({ text: what, options: { color: C.soft, paraSpaceAfter: 7, breakLine: i < refs.length - 1 } });
  });
  txt(s, refRuns, { x: MX + 0.3, y: top + 0.85, w: lw - 0.45, h: ch - 1.05, fontSize: 18 });

  txt(s, "Team", { x: rx + 0.3, y: top + 0.25, w: rw - 0.6, h: 0.45, fontFace: H, fontSize: 22, color: C.ink });
  const team = [
    ["Author", "Ebin Babu Thomas"],
    ["Project selection", "Claude Fable 5.2"],
    ["Talks synthesis", "GPT-6 Astra"],
    ["Literature synthesis & scouting", "GPT-6 Astra, Gemini Carbon"],
    ["Implementation", "Claude Opus 5.5 (reviews: Claude Fable 5.2)"],
    ["Adversarial review", "GPT-6 Astra, Gemini Carbon"],
    ["Report drafting", "Claude Fable 5.2"],
  ];
  const teamRuns = [];
  // non-breaking spaces inside each name, so a long line wraps between names, never inside one
  const nb = (t) => t.replace(/(GPT-6|Gemini|Claude|Opus|Fable|Ebin|Babu|reviews:) /g, "$1 ");
  team.forEach(([role, who], i) => {
    teamRuns.push({ text: role + ": ", options: { color: C.soft } });
    teamRuns.push({ text: nb(who), options: { color: C.ink, paraSpaceAfter: 7, breakLine: i < team.length - 1 } });
  });
  txt(s, teamRuns, { x: rx + 0.3, y: top + 0.85, w: rw - 0.45, h: ch - 1.05, fontSize: 18 });
}

// ---------- write ----------
(async () => {
  await pres.writeFile({ fileName: OUT });
  // Optional: write the palette into the theme so PowerPoint's colour picker offers it.
  const skillTheme = process.env.APPLY_THEME_JS;
  if (skillTheme && fs.existsSync(skillTheme)) {
    const { applyTheme } = require(skillTheme);
    await applyTheme(OUT, {
      name: "Loud or Right",
      colors: { dk1: C.ink, lt1: C.paper, dk2: C.soft, lt2: C.mist, accent1: C.blue, accent2: C.orange,
        accent3: C.green, accent4: C.grey, accent5: C.navy2, accent6: C.onDark, hlink: C.blue, folHlink: C.soft },
    });
    console.log("theme applied");
  }
  console.log("wrote " + OUT);
})();
