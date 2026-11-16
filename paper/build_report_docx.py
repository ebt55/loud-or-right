"""Build paper/report.docx (and paper/report.pdf) from paper/report.md on the official
Apart Research submission template.

Usage (from anywhere):
    python paper/build_report_docx.py                     # report.md -> report.docx + report.pdf + checks
    python paper/build_report_docx.py --png DIR           # also render pages 1-3 and figure pages to DIR
    python paper/build_report_docx.py --src X.md --out Y.docx   # other input/output (PDF goes next to Y)
    python paper/build_report_docx.py --no-pdf            # .docx only

Output defaults to paper/report.docx only for paper/report.md; any other input X.md (without --out)
goes to X-template.docx next to it, so a test build never overwrites report.docx. If paper/report.md
does not exist yet, the default input falls back to paper/paper.md (-> paper/paper-template.docx).
Exit status 1 means a check failed (the files are still written).

The output starts from the template .docx (never modified): its page setup (US Letter, 1-inch
margins), styles, embedded Old Standard TT font, title-block table, "With Apart Research" line and
title footnote are kept. The title, one author slot and the abstract are filled from the report;
the extra author slots, the "How to use this template" box and all guidance text are deleted, and
the body (everything after the Abstract section) is rebuilt with the template's own heading, body
and list formatting. The markdown parser is the one in build_docx.py.

Layout: centred page numbers in the footer from page 1; each image kept with its caption (captions
never split); table rows never split, the header row repeats on continuation pages, and a table
whose estimated height fits on a page is kept on one page; a table drops to 8 pt only if that stops
its body cells wrapping. HTML comment lines are skipped; d_c, d_u, D_bal become italic with a
subscript (not inside `code`). The PDF check confirms every row of every table appears.

Report layout expected (extra lines are tolerated):
    # Title[^1]
    Author name            <- every other line before the Abstract goes into the author slot
    Affiliation
    With Apart Research    <- dropped (the template's own line is kept)
    ## Abstract            <- or a line "**Abstract**"
    ...
    ## 1. Introduction ... to the end
    [^1]: ...              <- footnote definitions are dropped (the template's footnote is kept)
"""

import argparse
import copy
import io
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.text.paragraph import Paragraph

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_docx as bd  # noqa: E402  (markdown parser shared with the plain A4 builder)
from build_docx import (FULL_BOLD_RE, FULL_ITALIC_RE, HEADING_RE, PLACEHOLDER_RE,  # noqa: E402
                        parse_blocks, parse_inline, plain)

ROOT = HERE.parent
TEMPLATE = ROOT / "submission-template" / "Copy of Apart Research hackathon submission template.docx"
DEFAULT_SRC = HERE / "report.md"
FALLBACK_SRC = HERE / "paper.md"
DEFAULT_OUT = HERE / "report.docx"
SOFFICE = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")

MONO_FONT = "Courier New"
TABLE_PT = 9
CAPTION_PT = 9
QUOTE_PT = 10
# The template separates paragraphs with empty lines; the rebuilt body uses paragraph spacing instead.
PARA_AFTER_PT = 4
LIST_ITEM_AFTER_PT = 2
MAX_IMAGE_CM = 16.0
# Density (user, 16 Nov 05:30): smaller body text and single spacing are allowed; structure stays the template's.
BODY_PT = 10
BODY_LINE_SPACING = 1.0
IMAGE_WIDTHS = {"fig1_profiles.png": 11.5, "tab_summary.png": 13.0, "fig3_right_stratum.png": 11.5}
LINK_COLOR = RGBColor(0x11, 0x55, 0xCC)  # the template's hyperlink colour

FOOTDEF_RE = re.compile(r"^\s*\[\^[^\]]+\]:\s?(.*)$")
FOOTREF_RE = re.compile(r"\[\^[^\]]+\]")
WITH_APART_RE = re.compile(r"^[\W_]*with[\W_]*(apart[\W_]+research[\W_]*)?$", re.I)
APART_RE = re.compile(r"^[\W_]*apart[\W_]+research[\W_]*$", re.I)
ABSTRACT_RE = re.compile(r"^[\W_]*abstract[\W_]*$", re.I)
LINK_RE = re.compile(r"(?<![!\\])\[([^\[\]]+)\]\((\S+?)\)")
TOKEN_RE = re.compile("\ue000(\\d+)\ue001")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)  # HTML comments (e.g. <!-- TABLE1:START -->) are dropped
# d_c, d_u, D_bal -> italic d/D with a subscript (not inside code spans)
MATH_RE = re.compile(r"(?<![A-Za-z0-9_])([dD])_(c|u|bal)(?![A-Za-z0-9_])")
CAPTION_RE = re.compile(r"^[*_]*(Figure|Fig\.|Table)\s+[A-Z]?\d+")  # a caption under an image
TABLE_MIN_PT = 8  # a table drops from TABLE_PT to this only if that stops its body cells wrapping
TABLE_CELL_PAD_CM = 2 * 70 / 1440 * 2.54 + 0.1  # left + right cell margins plus slack
KEEP_TABLE_MAX_FRACTION = 0.75  # keep a table on one page if its estimated height fits this share of it

# Template text that must not survive (matched whitespace-insensitively, case-sensitively).
GUIDANCE_PHRASES = ["Replace the", "italicized guidance", "Author name", "[Reference 1]",
                    "Summarize your project", "How to use this template", "PROJECT TITLE",
                    "Delete all guidance", "Evaluation Rubric", "Recommended length"]
MIN_TEMPLATE_SENTENCE = 45  # template sentences at least this long are also checked

W = lambda tag: qn("w:" + tag)  # noqa: E731


# --------------------------------------------------------------------------- report splitting

def strip_comments(text):
    """Drop HTML comments; a line holding nothing but comments disappears entirely."""
    text = COMMENT_RE.sub("\x00", text)
    out = []
    for ln in text.splitlines():
        if "\x00" in ln and not ln.replace("\x00", "").strip():
            continue
        out.append(ln.replace("\x00", ""))
    return "\n".join(out)


def is_caption(text, after_table=False):
    """Caption under an image: wholly italic or starting 'Figure N'/'Table N'. Under a table only a
    wholly italic 'Table N ...' line counts (a bold 'Table D2.' line is the next table's title)."""
    if after_table:
        return bool(FULL_ITALIC_RE.match(text) and CAPTION_RE.match(text))
    return bool(FULL_ITALIC_RE.match(text) or CAPTION_RE.match(text))


def shown_text(md):
    """Text as it appears in the PDF: markdown removed, d_c -> dc (subscript)."""
    return MATH_RE.sub(r"\1\2", plain(md))


def split_report(text):
    """Return (title, author_lines, abstract_text, body_text, footnotes)."""
    lines, footnotes, i = [], [], 0
    raw = strip_comments(text).splitlines()
    while i < len(raw):
        m = FOOTDEF_RE.match(raw[i])
        if m:
            note = [m.group(1).strip()]
            i += 1
            while i < len(raw) and raw[i].startswith(("    ", "\t")) and raw[i].strip():
                note.append(raw[i].strip())
                i += 1
            footnotes.append(" ".join(note))
            continue
        lines.append(raw[i])
        i += 1

    t_idx = next((k for k, ln in enumerate(lines) if re.match(r"^#\s+\S", ln.strip())), None)
    if t_idx is None:
        sys.exit("ERROR: no '# Title' line found in the report.")
    title = FOOTREF_RE.sub("", HEADING_RE.match(lines[t_idx].strip()).group(2)).strip()

    a_idx = None
    for k in range(t_idx + 1, len(lines)):
        s = lines[k].strip()
        m = HEADING_RE.match(s)
        if (m and ABSTRACT_RE.match(plain(m.group(2)))) or (FULL_BOLD_RE.match(s) and ABSTRACT_RE.match(plain(s))):
            a_idx = k
            break
        if m:  # another heading before any Abstract
            break
    if a_idx is None:
        sys.exit("ERROR: no '## Abstract' heading (or '**Abstract**' line) directly after the title block.")

    authors, block = [], [ln.strip() for ln in lines[t_idx + 1:a_idx]]
    for k, s in enumerate(block):
        s = re.sub(r"(\\|<br\s*/?>)$", "", s).strip()
        if not s or bd.HR_RE.match(s) or WITH_APART_RE.match(s) or APART_RE.match(s):
            continue
        authors += [x.strip() for x in re.split(r"<br\s*/?>", s) if x.strip()]
    if not authors:
        sys.exit("ERROR: no author line between the title and the Abstract.")

    b_idx = next((k for k in range(a_idx + 1, len(lines)) if HEADING_RE.match(lines[k].strip())), len(lines))
    abstract = "\n".join(lines[a_idx + 1:b_idx])
    if not abstract.strip():
        sys.exit("ERROR: the Abstract section is empty.")
    body = "\n".join(lines[b_idx:])
    return title, authors, abstract, body, footnotes


# --------------------------------------------------------------------------- xml helpers

def text_of(el):
    return "".join(t.text or "" for t in el.iter(W("t")))


def strip_rpr(rpr, *tags):
    """Copy of a run/paragraph-mark rPr without the given child tags (and without w:rtl)."""
    rpr = copy.deepcopy(rpr) if rpr is not None else OxmlElement("w:rPr")
    for tag in tags + ("rtl",):
        for el in rpr.findall(W(tag)):
            rpr.remove(el)
    return rpr


def first_text_run(p):
    return next((r for r in p.iter(W("r")) if r.find(W("t")) is not None), None)


def set_twips(el, attr, value):
    el.set(W(attr), str(int(round(value))))


_OST_FONTS = {}


def text_cm_template_font(text, bold=False, size=TABLE_PT):
    """Width of `text` in cm in the template's embedded body font (falls back to build_docx's)."""
    key = (bold, size)
    if key not in _OST_FONTS:
        font = None
        try:
            from PIL import ImageFont
            with zipfile.ZipFile(TEMPLATE) as z:
                names = [n for n in z.namelist() if n.startswith("word/fonts/")]
                want = "bold" if bold else "regular"
                name = next(n for n in names if want in n.lower() and "italic" not in n.lower())
                font = ImageFont.truetype(io.BytesIO(z.read(name)), int(size * 10))
        except Exception:
            font = None
        _OST_FONTS[key] = font
    font = _OST_FONTS[key]
    if font is None:
        return _bd_text_cm(text, bold=bold, size=size)
    return font.getlength(text) / 10 / 72 * 2.54


_bd_text_cm = bd.text_cm


def column_widths(rows, group, total, pt):
    """Column widths (cm) that fit `total` at `pt` (the build_docx algorithm, measured in the
    template font): natural widths if they fit, else headers wrap at spaces/hyphens, else body
    cells wrap too. Returns (widths, body_cells_wrap)."""
    ncols = len(rows[0])
    full, desired, minimum = [], [], []
    for c in range(ncols):
        body = [shown_text(r[c]) for k, r in enumerate(rows) if k > 0 and not group[k]]
        head = shown_text(rows[0][c])
        body_long = max((text_cm_template_font(t, size=pt) for t in body), default=0)
        body_word = max((text_cm_template_font(w, size=pt) for t in body for w in t.split()), default=0)
        head_full = text_cm_template_font(head, bold=True, size=pt)
        head_word = max((text_cm_template_font(w, bold=True, size=pt)
                         for w in re.findall(r"[^\s-]+-?", head)), default=0)
        full.append(max(body_long, head_full) + TABLE_CELL_PAD_CM)
        desired.append(max(body_long, head_word) + TABLE_CELL_PAD_CM)
        minimum.append(max(min(body_word, 3.0), head_word) + TABLE_CELL_PAD_CM)
    if sum(full) <= total:
        return full, False
    if sum(desired) <= total:
        spare = total - sum(desired)
        extra = [f - d for f, d in zip(full, desired)]
        return [d + spare * e / sum(extra) for d, e in zip(desired, extra)], False
    widths = [0.0] * ncols
    remaining, left = total, ncols
    for c in sorted(range(ncols), key=lambda k: desired[k]):
        w = max(min(desired[c], remaining / left), minimum[c])
        widths[c] = w
        remaining -= w
        left -= 1
    if sum(widths) > total:
        widths = [w * total / sum(widths) for w in widths]
    return widths, True


def wrapped_lines(text, width_cm, pt, bold=False):
    """Greedy word-wrap line count of `text` in a cell `width_cm` wide."""
    avail = max(width_cm - TABLE_CELL_PAD_CM, 0.3)
    lines, cur = 1, 0.0
    space = text_cm_template_font(" ", bold=bold, size=pt)
    for word in text.split():
        w = text_cm_template_font(word, bold=bold, size=pt)
        if cur and cur + space + w > avail:
            lines += 1
            cur = w
        else:
            cur = cur + space + w if cur else w
        while cur > avail:  # a word wider than the cell breaks
            lines += 1
            cur -= avail
    return lines


# --------------------------------------------------------------------------- template builder

class TemplateReport:
    def __init__(self, template, src_dir):
        self.doc = Document(str(template))
        _normal = self.doc.styles.default(WD_STYLE_TYPE.PARAGRAPH)  # the template names it "normal"
        _normal.font.size = Pt(BODY_PT)
        _normal.paragraph_format.line_spacing = BODY_LINE_SPACING
        self.src_dir = src_dir
        self.body = self.doc.element.body
        self.placeholders = []
        self.n_images = 0
        self.n_tables = 0
        self.missing_images = []
        self.warnings = []
        self.math_tokens = 0
        self.table_notes = []
        sec = self.doc.sections[0]
        self.text_w_cm = (sec.page_width - sec.left_margin - sec.right_margin) / 360000
        self.text_h_pt = (sec.page_height - sec.top_margin - sec.bottom_margin) / 12700
        self._find_template_parts()

    # ---- template inspection
    def _find_template_parts(self):
        kids = list(self.body)
        self.title_tbl = next(el for el in kids if el.tag == W("tbl"))
        after = kids[kids.index(self.title_tbl) + 1:]

        def proto(pred):
            for el in after:
                if el.tag != W("p") or not text_of(el).strip():
                    continue
                ppr = el.find(W("pPr"))
                style = ppr.find(W("pStyle")).get(W("val")) if ppr is not None and ppr.find(W("pStyle")) is not None else None
                numbered = ppr is not None and ppr.find(W("numPr")) is not None
                if pred(style, numbered):
                    run = first_text_run(el)
                    return copy.deepcopy(ppr), strip_rpr(run.find(W("rPr")))
            sys.exit("ERROR: template structure not recognised (missing heading/body/list paragraph).")

        self.h2 = proto(lambda s, n: s == "Heading2")
        self.h3 = proto(lambda s, n: s == "Heading3")
        self.bodyp = proto(lambda s, n: s is None and not n)
        self.listp = proto(lambda s, n: s is None and n)
        # Body runs: the template's direct font only (no bold/italic/size).
        self.body_rpr = strip_rpr(self.bodyp[1], "b", "bCs", "i", "iCs", "u", "sz", "szCs")

        # Template text to check for afterwards: everything deleted below plus the guidance in the title block.
        self.template_text = [text_of(p) for el in after for p in el.iter(W("p"))]
        self.template_text += [text_of(p) for p in self.title_tbl.iter(W("p"))
                               if "Author name" in text_of(p) or "Summarize your project" in text_of(p)]

        numbering = self.doc.part.numbering_part.element
        fmt = {}
        for an in numbering.findall(W("abstractNum")):
            lvl0 = next(lv for lv in an.findall(W("lvl")) if lv.get(W("ilvl")) == "0")
            fmt[an.get(W("abstractNumId"))] = (lvl0.find(W("numFmt")).get(W("val")),
                                               lvl0.find(W("lvlText")).get(W("val")))
        self.bullet_num = self.decimal_abstract = None
        for num in numbering.findall(W("num")):
            aid = num.find(W("abstractNumId")).get(W("val"))
            if fmt.get(aid, ("",))[0] == "bullet" and self.bullet_num is None:
                self.bullet_num = num.get(W("numId"))
        self.decimal_abstract = next((a for a, (f, t) in fmt.items() if f == "decimal" and t == "%1."), None)
        if self.bullet_num is None or self.decimal_abstract is None:
            sys.exit("ERROR: template numbering (bullet / decimal list) not found.")

    # ---- runs
    def add_inline(self, p, text, base_rpr, size=None, bold=None, italic=None):
        """Append runs for markdown `text` to paragraph `p`; return the new child elements."""
        links = []

        def keep_link(m):
            links.append((m.group(1), m.group(2)))
            return f"\ue000{len(links) - 1}\ue001"

        text = LINK_RE.sub(keep_link, text)
        runs = parse_inline(text)
        full = "".join(r[0] for r in runs)
        spans = [(m.start(), m.end()) for m in PLACEHOLDER_RE.finditer(full)]
        self.placeholders += [TOKEN_RE.sub(lambda m: links[int(m.group(1))][0], full[a:b]) for a, b in spans]
        cuts = sorted({0, len(full)} | {x for sp in spans for x in sp})
        start_len = len(p._p)
        pos = 0
        for rtext, rb, ri, rc in runs:
            start, end = pos, pos + len(rtext)
            pos = end
            pieces = [start] + [c for c in cuts if start < c < end] + [end]
            for a, b in zip(pieces, pieces[1:]):
                if a == b:
                    continue
                hl = any(sa <= a and b <= sb for sa, sb in spans)
                for k, part in enumerate(TOKEN_RE.split(full[a:b])):
                    if k % 2 == 1:
                        ltext, url = links[int(part)]
                        self._hyperlink(p, plain(ltext), url, base_rpr, size, bold or rb, italic if italic is not None else ri, hl)
                    elif part:
                        self._text(p, part, base_rpr, size, bold or rb, italic if italic is not None else ri, rc, hl)
        return list(p._p)[start_len:]

    def _text(self, p, text, base_rpr, size, bold, italic, code, highlight):
        """Runs for plain text; d_c, d_u, D_bal become italic d/D with a subscript (not in code)."""
        if code:
            self._run(p, text, base_rpr, size, bold, italic, code, highlight)
            return
        pos = 0
        for m in MATH_RE.finditer(text):
            if m.start() > pos:
                self._run(p, text[pos:m.start()], base_rpr, size, bold, italic, False, highlight)
            self._run(p, m.group(1), base_rpr, size, bold, True, False, highlight)
            sub = self._run(p, m.group(2), base_rpr, size, bold, True, False, highlight)
            sub.font.subscript = True
            self.math_tokens += 1
            pos = m.end()
        if pos < len(text):
            self._run(p, text[pos:], base_rpr, size, bold, italic, False, highlight)

    def _run(self, p, text, base_rpr, size, bold, italic, code, highlight):
        run = p.add_run(text)
        run._r.insert(0, copy.deepcopy(base_rpr))
        if bold:
            run.bold = True
        if italic:
            run.italic = True
        if code:
            bd.set_rfonts(run._r, MONO_FONT)
        if size is not None:
            run.font.size = Pt(size)
        if highlight:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        return run

    def _hyperlink(self, p, text, url, base_rpr, size, bold, italic, highlight):
        r_id = self.doc.part.relate_to(url, RT.HYPERLINK, is_external=True)
        h = OxmlElement("w:hyperlink")
        h.set(qn("r:id"), r_id)
        p._p.append(h)
        run = self._run(p, text, base_rpr, size, bold, italic, False, highlight)
        run.font.color.rgb = LINK_COLOR
        run.font.underline = True
        h.append(run._r)

    # ---- paragraphs
    def new_p(self, proto_ppr=None, mark_size=None):
        p = self.doc.add_paragraph()
        ppr = copy.deepcopy(proto_ppr) if proto_ppr is not None else None
        if ppr is None:
            ppr = OxmlElement("w:pPr")
            ppr.append(copy.deepcopy(self.body_rpr))  # paragraph mark in the template font
        p._p.insert(0, ppr)
        if mark_size is not None:
            mark = ppr.find(W("rPr"))
            for tag in ("sz", "szCs"):
                el = mark.find(W(tag))
                if el is None:
                    el = OxmlElement("w:" + tag)
                    mark.append(el)
                el.set(W("val"), str(int(mark_size * 2)))
        return p

    def heading(self, level, text):
        ppr, rpr = self.h2 if level <= 2 else self.h3
        p = self.new_p(ppr)
        if level >= 4:  # no template prototype: Heading 4 at body size, bold
            p._p.pPr.find(W("pStyle")).set(W("val"), "Heading4")
            rpr = strip_rpr(rpr, "sz", "szCs")
        self.add_inline(p, text, rpr)
        return p

    def paragraph(self, text, references=False, keep_next=False):
        p = self.new_p(self.bodyp[0])
        self.add_inline(p, text, self.body_rpr)
        pf = p.paragraph_format
        pf.space_after = Pt(PARA_AFTER_PT)
        if references:
            pf.left_indent = Cm(0.75)
            pf.first_line_indent = Cm(-0.75)
            pf.space_after = Pt(4)
        if keep_next or FULL_BOLD_RE.match(text) or text.rstrip().endswith(":"):
            pf.keep_with_next = True
        return p

    def caption(self, text):
        p = self.new_p(self.bodyp[0], mark_size=CAPTION_PT)
        self.add_inline(p, text, self.body_rpr, size=CAPTION_PT, italic=True)
        pf = p.paragraph_format
        pf.space_before, pf.space_after, pf.line_spacing = Pt(2), Pt(10), 1.0
        pf.keep_together = True  # a caption never splits across pages (the image keeps with it)
        return p

    def add_page_numbers(self):
        """Centred page number in the footer of every page, starting at 1 (the template has none)."""
        sec = self.doc.sections[0]
        sec.different_first_page_header_footer = False
        footer = sec.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        for child in list(p._p):
            p._p.remove(child)
        ppr = OxmlElement("w:pPr")
        jc = OxmlElement("w:jc")
        jc.set(W("val"), "center")
        ppr.append(jc)
        ppr.append(copy.deepcopy(self.body_rpr))
        p._p.append(ppr)

        def fld_run(kind=None, instr=None, text=None):
            r = p.add_run(text) if text else p.add_run()
            r._r.insert(0, copy.deepcopy(self.body_rpr))
            r.font.size = Pt(BODY_PT)
            if kind:
                fc = OxmlElement("w:fldChar")
                fc.set(W("fldCharType"), kind)
                r._r.append(fc)
            if instr:
                it = OxmlElement("w:instrText")
                it.set(qn("xml:space"), "preserve")
                it.text = instr
                r._r.append(it)

        fld_run("begin")
        fld_run(instr=" PAGE ")
        fld_run("separate")
        fld_run(text="1")
        fld_run("end")
        pg = self.body.find(W("sectPr")).find(W("pgNumType"))
        if pg is not None:
            pg.set(W("start"), "1")

    def image(self, rel_path, keep_next):
        path = (self.src_dir / rel_path).resolve()
        if not path.exists():
            path = (HERE / rel_path).resolve()
        if not path.exists():
            self.missing_images.append(rel_path)
            p = self.new_p(self.bodyp[0])
            r = self._run(p, f"[MISSING IMAGE: {rel_path}]", self.body_rpr, None, True, None, False, False)
            r.font.highlight_color = WD_COLOR_INDEX.RED
            return p
        width = min(IMAGE_WIDTHS.get(path.name, MAX_IMAGE_CM), MAX_IMAGE_CM, self.text_w_cm)
        p = self.new_p(self.bodyp[0])
        p.add_run().add_picture(str(path), width=Cm(width))
        pf = p.paragraph_format
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.space_before, pf.space_after, pf.line_spacing = Pt(6), Pt(2), 1.0
        pf.keep_with_next = keep_next
        self.n_images += 1
        return p

    def quote(self, qlines):
        for k, q in enumerate(qlines):
            p = self.new_p(self.bodyp[0], mark_size=QUOTE_PT)
            self.add_inline(p, q, self.body_rpr, size=QUOTE_PT)
            pf = p.paragraph_format
            pf.left_indent, pf.right_indent = Cm(1.06), Cm(1.06)  # the template's 600-twip quote indent
            pf.space_after = Pt(PARA_AFTER_PT) if k == len(qlines) - 1 else Pt(2)

    def _new_num(self, start):
        numbering = self.doc.part.numbering_part.element
        new_id = max(int(n.get(W("numId"))) for n in numbering.findall(W("num"))) + 1
        num = OxmlElement("w:num")
        num.set(W("numId"), str(new_id))
        a = OxmlElement("w:abstractNumId")
        a.set(W("val"), self.decimal_abstract)
        num.append(a)
        lo = OxmlElement("w:lvlOverride")
        lo.set(W("ilvl"), "0")
        so = OxmlElement("w:startOverride")
        so.set(W("val"), str(start))
        lo.append(so)
        num.append(lo)
        numbering.append(num)
        return str(new_id)

    def list(self, items):
        num_ids = {}  # level -> numId of the running ordered list (restarts per list)
        last = None
        for it in items:
            lvl = min(it["level"], 4)
            p = self.new_p(self.listp[0])
            ppr = p._p.pPr
            numpr = ppr.find(W("numPr"))
            for k in [k for k in num_ids if k > lvl]:
                del num_ids[k]
            if it["ordered"]:
                if lvl not in num_ids:
                    num_ids[lvl] = self._new_num(it["num"] or 1)
                numpr.find(W("ilvl")).set(W("val"), "0")
                numpr.find(W("numId")).set(W("val"), num_ids[lvl])
            else:
                for k in [k for k in num_ids if k >= lvl]:
                    del num_ids[k]
                numpr.find(W("ilvl")).set(W("val"), str(lvl))
                numpr.find(W("numId")).set(W("val"), self.bullet_num)
            ind = ppr.find(W("ind"))
            if ind is None:
                ind = OxmlElement("w:ind")
                ppr.find(W("rPr")).addprevious(ind)
            set_twips(ind, "left", 720 * (lvl + 1))
            set_twips(ind, "hanging", 360)
            self.add_inline(p, it["text"], self.body_rpr)
            p.paragraph_format.space_after = Pt(LIST_ITEM_AFTER_PT)
            last = p
        if last is not None:
            last.paragraph_format.space_after = Pt(PARA_AFTER_PT)

    def table(self, rows, caption_follows=False):
        ncols = max(len(r) for r in rows)
        rows = [r + [""] * (ncols - len(r)) for r in rows]
        group = [k > 0 and bool(r[0]) and not any(c.strip() for c in r[1:]) for k, r in enumerate(rows)]
        total = self.text_w_cm - 0.05
        pt = TABLE_PT
        widths, wraps = column_widths(rows, group, total, pt)
        if wraps:  # body cells would wrap at TABLE_PT: use TABLE_MIN_PT if that avoids it
            w8, wraps8 = column_widths(rows, group, total, TABLE_MIN_PT)
            if not wraps8:
                pt, widths, wraps = TABLE_MIN_PT, w8, False

        # Estimated height, to keep tables that fit on one page together.
        line_pt, row_extra_pt = 1.2 * pt, 4.0
        height = 0.0
        for k, r in enumerate(rows):
            if group[k]:
                n = 1
            else:
                n = max(wrapped_lines(shown_text(cell), widths[c], pt, bold=(k == 0)) for c, cell in enumerate(r))
            height += n * line_pt + row_extra_pt
        keep_together = height <= KEEP_TABLE_MAX_FRACTION * self.text_h_pt
        self.table_notes.append(f"{ncols} cols, {pt} pt, {sum(widths):.1f} of {self.text_w_cm:.1f} cm wide, "
                                f"~{height:.0f} pt tall, {'kept on one page' if keep_together else 'may split'}"
                                f"{', body cells wrap' if wraps else ''}")

        t = self.doc.add_table(rows=len(rows), cols=ncols)
        tbl = t._tbl
        tblPr = tbl.tblPr
        for child in list(tblPr):
            tblPr.remove(child)

        def el(tag, **attrs):
            e = OxmlElement("w:" + tag)
            for k, v in attrs.items():
                e.set(W(k), str(v))
            return e

        tblPr.append(el("tblW", w=int(sum(widths) / 2.54 * 1440), type="dxa"))
        tblPr.append(el("jc", val="center"))
        borders = el("tblBorders")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            borders.append(el(side, val="single", sz=4, space=0, color="000000"))
        tblPr.append(borders)
        tblPr.append(el("tblLayout", type="fixed"))
        mar = el("tblCellMar")
        for side, w in (("top", 15), ("left", 70), ("bottom", 15), ("right", 70)):
            mar.append(el(side, w=w, type="dxa"))
        tblPr.append(mar)
        tblPr.append(el("tblLook", val="04A0", firstRow=1, lastRow=0, firstColumn=0, lastColumn=0,
                        noHBand=1, noVBand=1))
        for gc, w in zip(tbl.tblGrid.findall(W("gridCol")), widths):
            gc.set(W("w"), str(int(w / 2.54 * 1440)))

        for k, r in enumerate(rows):
            row = t.rows[k]
            trPr = row._tr.get_or_add_trPr()
            trPr.append(el("cantSplit"))
            if k == 0:
                trPr.append(el("tblHeader"))
            for c in range(ncols):
                row.cells[c].width = Cm(widths[c])
            cells, texts = row.cells, r
            if group[k]:
                cells, texts = [cells[0].merge(cells[-1])], [r[0]]
            for cell, text in zip(cells, texts):
                p = cell.paragraphs[0]
                ppr = p._p.get_or_add_pPr()
                mark = copy.deepcopy(self.body_rpr)
                for tag in ("sz", "szCs"):
                    mark.append(el(tag, val=int(pt * 2)))
                ppr.append(mark)
                pf = p.paragraph_format
                pf.space_before, pf.space_after, pf.line_spacing = Pt(1), Pt(1), 1.0
                if keep_together and (k < len(rows) - 1 or caption_follows):
                    pf.keep_with_next = True
                self.add_inline(p, text, self.body_rpr, size=pt, bold=(k == 0) or None)
        if not caption_follows:  # a caption paragraph right after the table separates it instead
            gap = self.new_p(self.bodyp[0], mark_size=6)
            gap.paragraph_format.space_after = Pt(0)
            gap.paragraph_format.line_spacing = 1.0
        self.n_tables += 1
        return t

    # ---- title block
    def fill_title_block(self, title, authors, abstract_blocks):
        tb = self.title_tbl
        # Title: replace the text runs, keep the footnote-reference run after them.
        tp = next(p for p in tb.iter(W("p")) if p.find(W("pPr")) is not None
                  and p.find(W("pPr")).find(W("pStyle")) is not None
                  and p.find(W("pPr")).find(W("pStyle")).get(W("val")) == "Title")
        trun = first_text_run(tp)
        rpr = strip_rpr(trun.find(W("rPr")))
        foot = next((r for r in tp.findall(W("r")) if r.find(W("footnoteReference")) is not None), None)
        for r in [r for r in tp.findall(W("r")) if r.find(W("t")) is not None]:
            tp.remove(r)
        para = Paragraph(tp, self.doc._body)
        for e in self.add_inline(para, title, rpr):
            if foot is not None:
                foot.addprevious(e)

        # Authors: collapse the 2 x 3 author grid to one cell as wide as its parent table.
        auth_tbl = next(t for t in tb.iter(W("tbl"))
                        if "Author name 1" in text_of(t) and not any(
                            "Author name 1" in text_of(x) for x in t.iter(W("tbl")) if x is not t))
        trs = auth_tbl.findall(W("tr"))
        for tr in trs[1:]:
            auth_tbl.remove(tr)
        tcs = trs[0].findall(W("tc"))
        for tc in tcs[1:]:
            trs[0].remove(tc)
        parent_tbl = next(a for a in auth_tbl.iterancestors(W("tbl")))
        width = int(float(parent_tbl.find(W("tblPr")).find(W("tblW")).get(W("w"))))
        auth_tbl.find(W("tblPr")).find(W("tblW")).set(W("w"), str(width))
        grid = auth_tbl.find(W("tblGrid"))
        for child in list(grid):
            grid.remove(child)
        gc = OxmlElement("w:gridCol")
        gc.set(W("w"), str(width))
        grid.append(gc)
        ap = tcs[0].find(W("p"))
        arun = first_text_run(ap)
        rpr = strip_rpr(arun.find(W("rPr")))
        for r in ap.findall(W("r")):
            ap.remove(r)
        para = Paragraph(ap, self.doc._body)
        for k, line in enumerate(authors):
            if k:
                br = para.add_run()
                br._r.insert(0, copy.deepcopy(rpr))
                br.add_break()
            self.add_inline(para, line, rpr)

        # Abstract: the guidance paragraph's formatting, without its italics and underline.
        gp = next(p for p in tb.iter(W("p")) if text_of(p).startswith("Summarize your project"))
        rpr = strip_rpr(first_text_run(gp).find(W("rPr")), "i", "iCs", "u")
        ppr = gp.find(W("pPr"))
        mark = ppr.find(W("rPr"))
        if mark is not None:
            for u in mark.findall(W("u")):
                mark.remove(u)
        proto_ppr = copy.deepcopy(ppr)
        for child in [c for c in gp if c is not ppr]:
            gp.remove(child)
        texts = []
        for blk in abstract_blocks:
            if blk[0] == "p":
                texts.append(blk[1])
            elif blk[0] == "list":
                texts += [it["text"] for it in blk[1]]
                self.warnings.append("abstract contains a list; its items were set as paragraphs")
            elif blk[0] == "quote":
                texts.append(" ".join(blk[1]))
            else:
                self.warnings.append(f"abstract block of type '{blk[0]}' skipped")
        prev = gp
        for k, text in enumerate(texts):
            if k == 0:
                p_el = gp
            else:
                p_el = OxmlElement("w:p")
                p_el.append(copy.deepcopy(proto_ppr))
                prev.addnext(p_el)
            self.add_inline(Paragraph(p_el, self.doc._body), text, rpr)
            prev = p_el
        return sum(len(plain(t).split()) for t in texts)

    def clear_body(self):
        kids = list(self.body)
        for el in kids[kids.index(self.title_tbl) + 1:]:
            if el.tag != W("sectPr"):
                self.body.remove(el)


def build(src, out):
    title, authors, abstract, body_text, footnotes = split_report(src.read_text(encoding="utf-8"))
    rep = TemplateReport(TEMPLATE, src.parent)
    abstract_words = rep.fill_title_block(title, authors, parse_blocks(abstract))
    rep.clear_body()

    blocks = parse_blocks(body_text)
    in_refs = False
    for k, blk in enumerate(blocks):
        kind = blk[0]
        nxt = blocks[k + 1] if k + 1 < len(blocks) else None
        prev = blocks[k - 1] if k > 0 else None
        if kind == "h":
            level, htext = blk[1], blk[2]
            if level <= 2:
                in_refs = plain(htext).strip().lower() == "references"
            rep.heading(level, htext)
        elif kind == "p":
            ptext = blk[1]
            if prev and prev[0] in ("img", "table") and is_caption(ptext, after_table=prev[0] == "table"):
                rep.caption(ptext)
            else:
                keep = bool(nxt and nxt[0] in ("table", "list", "quote"))
                rep.paragraph(ptext, references=in_refs, keep_next=keep)
        elif kind == "img":
            is_cap = bool(nxt and nxt[0] == "p" and is_caption(nxt[1]))
            if not is_cap:
                rep.warnings.append(f"image {blk[1]} has no caption paragraph directly after it")
            rep.image(blk[1], keep_next=is_cap)
        elif kind == "table":
            rep.table(blk[1], caption_follows=bool(nxt and nxt[0] == "p" and is_caption(nxt[1], after_table=True)))
        elif kind == "quote":
            rep.quote(blk[1])
        elif kind == "list":
            rep.list(blk[1])

    rep.add_page_numbers()
    body_refs = sorted(set(FOOTREF_RE.findall(body_text)))
    if body_refs:
        rep.warnings.append(f"footnote references left as text in the body: {body_refs}")
    cp = rep.doc.core_properties
    cp.title, cp.author, cp.last_modified_by = plain(title), "", ""
    try:
        rep.doc.save(str(out))
    except PermissionError:
        sys.exit(f"ERROR: cannot write {out} - is it open in Word or LibreOffice? Close it and re-run.")
    info = {"title": plain(title), "authors": authors, "abstract_words": abstract_words,
            "footnotes": footnotes, "blocks": blocks}
    return rep, info


# --------------------------------------------------------------------------- PDF + checks

def to_pdf(docx_path, pdf_path):
    if not SOFFICE.exists():
        sys.exit(f"ERROR: LibreOffice not found at {SOFFICE}")
    if pdf_path.exists():
        try:
            pdf_path.unlink()
        except PermissionError:
            sys.exit(f"ERROR: cannot replace {pdf_path} - is it open in a PDF viewer? Close it and re-run.")
    profile = Path(tempfile.gettempdir()) / "build_report_docx_lo_profile"
    cmd = [str(SOFFICE), f"-env:UserInstallation={profile.as_uri()}", "--headless",
           "--convert-to", "pdf", "--outdir", str(pdf_path.parent), str(docx_path)]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    produced = pdf_path.parent / (docx_path.stem + ".pdf")
    if produced != pdf_path and produced.exists():
        produced.replace(pdf_path)
    if not pdf_path.exists():
        sys.exit(f"ERROR: LibreOffice did not write the PDF.\nstdout: {res.stdout}\nstderr: {res.stderr}")


def squash(s):
    return re.sub(r"\s+", "", s)


def guidance_phrases(template_text):
    phrases = list(GUIDANCE_PHRASES)
    for para in template_text:
        for sent in re.split(r"(?<=[.?!:])\s+", para.strip()):
            if len(sent.strip()) >= MIN_TEMPLATE_SENTENCE:
                phrases.append(sent.strip())
    return list(dict.fromkeys(phrases))


def check_docx_text(out, phrases):
    doc = Document(str(out))
    text = squash(" ".join(text_of(p) for p in doc.element.body.iter(W("p"))))
    return [ph for ph in phrases if squash(ph) in text]


def check_pdf(pdf_path, info, phrases, png_dir=None, png_all=False, dpi=110):
    import fitz  # PyMuPDF

    problems = []
    blocks = info["blocks"]
    doc = fitz.open(str(pdf_path))
    w, h = doc[0].rect.width, doc[0].rect.height
    print(f"PDF: {pdf_path}, {doc.page_count} pages, page size {w:.0f} x {h:.0f} pt"
          f"{' (US Letter, as the template)' if abs(w - 612) < 2 and abs(h - 792) < 2 else ''}")
    page_texts = [pg.get_text() for pg in doc]
    page_sq = [squash(t) for t in page_texts]
    full_sq = "".join(page_sq)

    def page_lines(pg):
        out = []
        for blk in pg.get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                t = "".join(sp["text"] for sp in ln["spans"]).strip()
                if t:
                    out.append((ln["bbox"][1], t))
        return sorted(out)

    def find_heading(label, start=0):
        target = squash(label)
        for pno in range(start, doc.page_count):
            lines = page_lines(doc[pno])
            for idx, (y, t) in enumerate(lines):
                if squash(t) == target or (len(squash(t)) >= 12 and target.startswith(squash(t))):
                    return pno + 1, idx == 0, y
        return None

    # Title block (page 1)
    p1 = page_sq[0]
    for label, needle in (("title", info["title"][:40]), ("'With Apart Research'", "WithApartResearch"),
                          ("title footnote", "Researchconductedatthe"), ("abstract heading", "Abstract")):
        if squash(needle) not in p1:
            problems.append(f"{label} not found on page 1")
    print(f"  page 1: title, author slot ({' / '.join(info['authors'])}), 'With Apart Research', "
          f"abstract ({info['abstract_words']} words) and title footnote "
          f"{'found' if not any('page 1' in p for p in problems) else 'CHECK FAILED'}")

    refs = find_heading("References")
    if refs:
        pno, at_top, y = refs
        main_pages = pno - 1 if at_top else pno
        where = "at the top of the page" if at_top else f"{y / h:.0%} down the page"
        print(f"  'References' starts on page {pno}, {where}: main text = {main_pages} page(s)"
              f"{'' if at_top else ' (last one partial)'}")
        if main_pages > 8:
            problems.append(f"main text is {main_pages} pages (hard limit 8)")
    else:
        problems.append("'References' heading not found in PDF")
    appx = next((plain(b[2]) for b in blocks if b[0] == "h" and b[1] <= 2 and plain(b[2]).startswith("Appendix")), None)
    if appx:
        found = find_heading(appx, start=(refs[0] - 1) if refs else 0)
        print(f"  '{appx}' starts on page {found[0] if found else '?'}")

    # Images
    shown = []
    for pno, pg in enumerate(doc):
        for im in pg.get_image_info():
            x0, y0, x1, y1 = im["bbox"]
            shown.append((pno + 1, (x1 - x0) / 72 * 2.54, (y1 - y0) / 72 * 2.54))
    md_imgs = [b[1] for b in blocks if b[0] == "img"]
    print(f"  images drawn: {len(shown)} of {len(md_imgs)} in the markdown")
    for (pno, wcm, hcm), name in zip(shown, md_imgs):
        print(f"    page {pno}: {name} ({wcm:.1f} x {hcm:.1f} cm)")
    if len(shown) < len(md_imgs):
        problems.append(f"only {len(shown)} of {len(md_imgs)} images drawn in PDF")

    # Tables: every row must appear, its cells in order, after the previous table's rows
    # (PDF text in content-stream order, whitespace removed; repeated header rows are harmless).
    tables = [b[1] for b in blocks if b[0] == "table"]
    found_tables, pos = 0, 0
    starts = [0]
    for t in page_sq:
        starts.append(starts[-1] + len(t))

    def page_at(idx):
        return next(k for k in range(len(page_sq)) if starts[k] <= idx < starts[k + 1]) + 1

    for t_idx, rows in enumerate(tables, 1):
        header = " | ".join(shown_text(c) for c in rows[0])
        missing, first_idx, last_idx, t_pos = [], None, None, pos
        for k, r in enumerate(rows):
            cells = [squash(shown_text(c)) for c in r if shown_text(c).strip()]
            # Prefer the whole row as one run of text (cells are drawn in order); else cells in order.
            i = full_sq.find("".join(cells), t_pos)
            if i >= 0:
                ok, r_pos = True, i + len("".join(cells))
                first_idx = i if first_idx is None else first_idx
            else:
                r_pos, ok = t_pos, True
                for cell in cells:
                    i = full_sq.find(cell, r_pos)
                    if i < 0:
                        ok = False
                        break
                    r_pos = i + len(cell)
            if ok:
                t_pos = r_pos
                last_idx = r_pos - 1
            else:
                missing.append(k)
        if missing:
            problems.append(f"table {t_idx} ('{header[:40]}'): rows {missing} (0 = header) not found in PDF")
            print(f"    table {t_idx}: MISSING rows {missing} of {len(rows)}, '{header[:50]}'")
        else:
            found_tables += 1
            pos = t_pos
            p0, p1 = page_at(first_idx if first_idx is not None else last_idx), page_at(last_idx)
            print(f"    table {t_idx}: all {len(rows)} rows found, page {p0}{'-' + str(p1) if p1 != p0 else ''}, "
                  f"'{header[:50]}'")
    print(f"  tables complete: {found_tables} of {len(tables)}")

    # Template guidance
    left = [ph for ph in phrases if squash(ph) in full_sq]
    if left:
        problems.append(f"{len(left)} template guidance phrase(s) remain in the PDF")
        for ph in left:
            print(f"  GUIDANCE LEFT: {ph[:90]!r}")
    else:
        print(f"  no template guidance text: none of {len(phrases)} phrases found "
              f"(e.g. 'Replace the', 'italicized guidance', 'Author name', '[Reference 1]', 'Summarize your project')")

    # Fonts: everything should be Old Standard TT (or Courier for code); the template's footnote
    # number is Arial in the template itself.
    stray = {}
    for pno, pg in enumerate(doc):
        for blk in pg.get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                for sp in ln["spans"]:
                    f = sp["font"]
                    if sp["text"].strip() and "OldStandard" not in f and "Courier" not in f:
                        stray.setdefault(f, []).append((pno + 1, sp["text"].strip()[:30]))
    if stray:
        for f, where in stray.items():
            print(f"  font {f}: {len(where)} span(s), e.g. {where[:4]}")
    else:
        print("  all text in Old Standard TT / Courier New")

    # Leftover markdown
    leftovers = []
    for pno, t in enumerate(page_texts):
        for ln in t.splitlines():
            s = ln.strip()
            if ("**" in s or "`" in s or "![" in s or "|---" in s or "](" in s or "[^" in s
                    or "<!--" in s or "-->" in s or re.match(r"^#{1,6}\s", s)):
                leftovers.append((pno + 1, s[:90]))
    if leftovers:
        problems.append(f"{len(leftovers)} line(s) with leftover markdown")
        for pno, s in leftovers[:20]:
            print(f"  leftover markdown p{pno}: {s}")
    else:
        print("  no leftover markdown symbols in PDF text")

    if png_dir:
        png_dir = Path(png_dir)
        png_dir.mkdir(parents=True, exist_ok=True)
        pages = range(1, doc.page_count + 1) if png_all else sorted(
            {p for p in (1, 2, 3) if p <= doc.page_count} | {s[0] for s in shown})
        for pno in pages:
            doc[pno - 1].get_pixmap(dpi=dpi).save(str(png_dir / f"page-{pno:02d}.png"))
        print(f"  rendered pages {list(pages)} to {png_dir}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", type=Path, help="markdown input (default paper/report.md, else paper/paper.md)")
    ap.add_argument("--out", type=Path, help="output .docx, PDF written next to it "
                    "(default paper/report.docx for report.md, else <src>-template.docx)")
    ap.add_argument("--no-pdf", action="store_true", help="only build the .docx")
    ap.add_argument("--png", metavar="DIR", help="render pages 1-3 and every figure page to DIR as PNG")
    ap.add_argument("--png-all", action="store_true", help="with --png: render every page")
    ap.add_argument("--dpi", type=int, default=110)
    args = ap.parse_args()

    src = args.src
    if src is None:
        src = DEFAULT_SRC if DEFAULT_SRC.exists() else FALLBACK_SRC
        if src == FALLBACK_SRC:
            print(f"NOTE: {DEFAULT_SRC.name} not found; building from the test input {FALLBACK_SRC.name}")
    src = src.resolve()
    if args.out is not None:
        out = args.out.resolve()
    elif src == DEFAULT_SRC.resolve():
        out = DEFAULT_OUT
    else:
        out = src.with_name(src.stem + "-template.docx")
    if not src.exists():
        sys.exit(f"ERROR: {src} not found")
    if not TEMPLATE.exists():
        sys.exit(f"ERROR: template not found at {TEMPLATE}")
    out.parent.mkdir(parents=True, exist_ok=True)

    rep, info = build(src, out)
    problems = []
    md_images = sum(1 for b in info["blocks"] if b[0] == "img")
    md_tables = sum(1 for b in info["blocks"] if b[0] == "table")
    print(f"DOCX: {out} (from {src.name}, template {TEMPLATE.name})")
    print(f"  title: {info['title']}")
    print(f"  images inserted: {rep.n_images} of {md_images}; tables: {rep.n_tables} of {md_tables}")
    if rep.missing_images:
        problems.append(f"missing image files: {rep.missing_images}")
    if rep.n_tables != md_tables:
        problems.append("table count mismatch")
    for k, note in enumerate(rep.table_notes, 1):
        print(f"    table {k}: {note}")
    print(f"  d_c / d_u / D_bal set as italic with subscript: {rep.math_tokens}")
    for wmsg in rep.warnings:
        print(f"  WARNING: {wmsg}")
    for fn in info["footnotes"]:
        print(f"  footnote definition in the report dropped (template footnote kept): {fn[:80]!r}")
    print(f"  placeholders highlighted ({len(rep.placeholders)}):")
    for ph in rep.placeholders:
        print(f"    {ph}")

    phrases = guidance_phrases(rep.template_text)
    left = check_docx_text(out, phrases)
    if left:
        problems.append(f"template guidance text remains in the .docx: {[x[:40] for x in left]}")

    if not args.no_pdf:
        pdf = out.with_suffix(".pdf")
        to_pdf(out, pdf)
        try:
            import fitz  # noqa: F401
        except ImportError:
            print(f"PDF written to {pdf} (PyMuPDF not available: checks skipped)")
        else:
            problems += check_pdf(pdf, info, phrases, png_dir=args.png, png_all=args.png_all, dpi=args.dpi)

    if problems:
        print("PROBLEMS (the .docx/.pdf were still written):")
        for pr in problems:
            print(f"  - {pr}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
