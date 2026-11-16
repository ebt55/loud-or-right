"""Build paper/loud-or-right.docx (and a LibreOffice PDF for checking) from paper/paper.md.

Usage (from anywhere):
    python paper/build_docx.py                # .docx + .pdf + checks
    python paper/build_docx.py --no-pdf       # .docx only
    python paper/build_docx.py --png DIR      # also render every PDF page to DIR/page-NN.png

The .docx is an intermediate for copying into the official Google Doc template:
plain styles, real headings, lists and tables, placeholders highlighted in yellow.
Supported markdown: # / ## / ### headings, paragraphs with **bold**, *italic*, `code`,
'- ' bullets (nested by two spaces), '1.' numbered lists, pipe tables (with \\| escapes),
images on their own line (italic paragraph after = caption), '> ' block quotes.
Requires python-docx; the PDF step needs LibreOffice, the checks need PyMuPDF.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
SRC = HERE / "paper.md"
OUT_DOCX = HERE / "loud-or-right.docx"
OUT_PDF = HERE / "loud-or-right.pdf"
SOFFICE = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")

BODY_FONT = "Arial"
MONO_FONT = "Courier New"
BODY_PT = 11
TABLE_PT = 9
QUOTE_PT = 9.5
CAPTION_PT = 10
PAGE_W, PAGE_H = Cm(21.0), Cm(29.7)
MARGIN = Cm(2.5)
TEXT_W = Cm(21.0 - 2 * 2.5)  # 16 cm
IMAGE_W = Cm(min(16.0, TEXT_W.cm))
# per-figure widths (cm) to fit the 8-page main text; others use IMAGE_W
IMAGE_WIDTHS = {"fig1_profiles.png": 11.5, "tab_summary.png": 13.0, "fig3_right_stratum.png": 11.5}

# Placeholder: square brackets whose content starts with two capitals/digits,
# e.g. [AUTHOR, ...], [AUTHOR TO CONFIRM.], [O3: ...]. Excludes [0.81, 0.95], [95% CI], ![](...).
PLACEHOLDER_RE = re.compile(r"\[[A-Z][A-Z0-9][^\[\]]*\]")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
IMAGE_RE = re.compile(r"^!\[([^\]]*)\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
FULL_BOLD_RE = re.compile(r"^\*\*[^*]+\*\*$")
FULL_ITALIC_RE = re.compile(r"^\*(?!\*).*[^*]\*$|^\*[^*]\*$")
HR_RE = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")

ESCAPABLE = set("\\`*_{}[]()#+-.!|>")


# --------------------------------------------------------------------------- markdown parsing

def split_row(line):
    """Split a pipe-table row on unescaped pipes; keep '\\|' for the inline parser."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, buf, i = [], [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            buf.append(s[i:i + 2])
            i += 2
            continue
        if s[i] == "|":
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(s[i])
        i += 1
    cells.append("".join(buf).strip())
    return cells


def is_block_start(lines, i):
    s = lines[i].strip()
    if not s:
        return True
    if HEADING_RE.match(s) or IMAGE_RE.match(s) or s.startswith(">") or LIST_RE.match(lines[i]):
        return True
    if s.startswith("|") and i + 1 < len(lines) and SEP_RE.match(lines[i + 1]):
        return True
    return False


def parse_blocks(text):
    lines = text.splitlines()
    blocks, para = [], []

    def flush():
        if para:
            # A line that is wholly **bold** (e.g. a table title) becomes its own paragraph.
            cur = []
            for ln in para:
                if FULL_BOLD_RE.match(ln):
                    if cur:
                        blocks.append(("p", " ".join(cur)))
                        cur = []
                    blocks.append(("p", ln))
                else:
                    cur.append(ln)
            if cur:
                blocks.append(("p", " ".join(cur)))
            para.clear()

    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            flush()
            i += 1
            continue
        m = HEADING_RE.match(s)
        if m:
            flush()
            blocks.append(("h", len(m.group(1)), m.group(2)))
            i += 1
            continue
        m = IMAGE_RE.match(s)
        if m:
            flush()
            blocks.append(("img", m.group(2), m.group(1)))
            i += 1
            continue
        if HR_RE.match(s) and not para:
            flush()
            i += 1
            continue
        if s.startswith("|") and i + 1 < n and SEP_RE.match(lines[i + 1]):
            flush()
            rows = [split_row(s)]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            blocks.append(("table", rows))
            continue
        if s.startswith(">"):
            flush()
            qlines = []
            while i < n and lines[i].strip().startswith(">"):
                q = re.sub(r"^>\s?", "", lines[i].strip())
                if q.strip():
                    qlines.append(q.strip())
                i += 1
            blocks.append(("quote", qlines))
            continue
        m = LIST_RE.match(line)
        if m:
            flush()
            items = []
            while i < n:
                m = LIST_RE.match(lines[i])
                if m:
                    indent = len(m.group(1).expandtabs(4))
                    marker = m.group(2)
                    ordered = marker[0].isdigit()
                    num = int(re.match(r"\d+", marker).group()) if ordered else None
                    items.append({"level": indent // 2, "ordered": ordered, "num": num,
                                  "text": m.group(3).strip()})
                    i += 1
                    continue
                if lines[i].strip() and not is_block_start(lines, i):
                    # Lazy or indented continuation of the previous item.
                    items[-1]["text"] += " " + lines[i].strip()
                    i += 1
                    continue
                break
            blocks.append(("list", items))
            continue
        para.append(s)
        i += 1
    flush()
    return blocks


def parse_inline(text):
    """Return [(text, bold, italic, code)]. Only * and ** are emphasis; underscores are literal."""
    runs, buf = [], []
    bold = italic = False
    i, n = 0, len(text)

    def flush():
        if buf:
            runs.append(("".join(buf), bold, italic, False))
            buf.clear()

    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n and text[i + 1] in ESCAPABLE:
            buf.append(text[i + 1])
            i += 2
            continue
        if c == "`":
            j = text.find("`", i + 1)
            if j != -1:
                flush()
                runs.append((text[i + 1:j], bold, italic, True))
                i = j + 1
                continue
        if text.startswith("**", i):
            opening_ok = (not bold) and i + 2 < n and not text[i + 2].isspace() and "**" in text[i + 2:]
            closing_ok = bold and i > 0 and not text[i - 1].isspace()
            if opening_ok or closing_ok:
                flush()
                bold = not bold
                i += 2
                continue
        if c == "*" and not text.startswith("**", i):
            opening_ok = (not italic) and i + 1 < n and not text[i + 1].isspace() and "*" in text[i + 1:]
            closing_ok = italic and i > 0 and not text[i - 1].isspace()
            if opening_ok or closing_ok:
                flush()
                italic = not italic
                i += 1
                continue
        buf.append(c)
        i += 1
    flush()
    if bold or italic:
        print(f"  WARNING: unclosed emphasis in: {text[:80]!r}")
    return runs


def plain(text):
    return "".join(r[0] for r in parse_inline(text))


# --------------------------------------------------------------------------- docx helpers

def set_rfonts(rpr_parent, name):
    """Set an explicit font on a style/run rPr and drop theme-font attributes that override it."""
    rpr = rpr_parent.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for att in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rfonts.get(qn(att)) is not None:
            del rfonts.attrib[qn(att)]
    for att in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(att), name)


def setup_document():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = PAGE_W, PAGE_H
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = MARGIN
    sec.header_distance = sec.footer_distance = Cm(1.25)

    # docDefaults: replace theme fonts with the body font.
    rpr_default = doc.styles.element.find(qn("w:docDefaults")).find(qn("w:rPrDefault"))
    rfonts = rpr_default.find(qn("w:rPr")).find(qn("w:rFonts"))
    if rfonts is not None:
        for att in list(rfonts.attrib):
            del rfonts.attrib[att]
        for att in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rfonts.set(qn(att), BODY_FONT)

    styles = doc.styles
    normal = styles["Normal"]
    set_rfonts(normal.element, BODY_FONT)
    normal.font.size = Pt(BODY_PT)
    pf = normal.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(0), Pt(6), 1.0

    def style_heading(name, size, before, after):
        st = styles[name]
        set_rfonts(st.element, BODY_FONT)
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.italic = False
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.line_spacing = 1.0
        st.paragraph_format.keep_with_next = True
        ppr = st.element.pPr
        if ppr is not None:
            bdr = ppr.find(qn("w:pBdr"))
            if bdr is not None:
                ppr.remove(bdr)
        return st

    title = style_heading("Title", 16, 0, 8)
    rpr = title.element.get_or_add_rPr()
    for tag in ("w:spacing", "w:kern"):
        el = rpr.find(qn(tag))
        if el is not None:
            rpr.remove(el)
    style_heading("Heading 1", 13, 12, 4)
    style_heading("Heading 2", 11.5, 9, 3)
    style_heading("Heading 3", 11, 6, 3)

    cap = styles["Caption"]
    set_rfonts(cap.element, BODY_FONT)
    cap.font.size = Pt(CAPTION_PT)
    cap.font.bold = False
    cap.font.color.rgb = RGBColor(0, 0, 0)
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(10)

    for name in ("List Bullet", "List Bullet 2", "List Bullet 3",
                 "List Number", "List Number 2", "List Number 3"):
        st = styles[name]
        st.paragraph_format.space_after = Pt(2)
        st.paragraph_format.line_spacing = 1.0
    return doc


def new_numbering(doc, style_name, start):
    """Create a fresh w:num for a numbered-list style so each list restarts at `start`."""
    numbering = doc.part.numbering_part.element
    style_numpr = doc.styles[style_name].element.pPr.numPr
    base_id = style_numpr.numId.val
    abstract_id = None
    for num in numbering.findall(qn("w:num")):
        if num.get(qn("w:numId")) == str(base_id):
            abstract_id = num.find(qn("w:abstractNumId")).get(qn("w:val"))
    new_id = max(int(x.get(qn("w:numId"))) for x in numbering.findall(qn("w:num"))) + 1
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(new_id))
    a = OxmlElement("w:abstractNumId")
    a.set(qn("w:val"), abstract_id)
    num.append(a)
    lo = OxmlElement("w:lvlOverride")
    lo.set(qn("w:ilvl"), "0")
    so = OxmlElement("w:startOverride")
    so.set(qn("w:val"), str(start))
    lo.append(so)
    num.append(lo)
    numbering.append(num)
    return new_id


_FONT_CACHE = {}


def text_cm(text, bold=False, size=TABLE_PT):
    """Width of `text` in cm at `size` pt, measured with the body font if PIL can load it."""
    key = (bold, size)
    if key not in _FONT_CACHE:
        font = None
        try:
            from PIL import ImageFont
            fname = {"Arial": ("arial.ttf", "arialbd.ttf"),
                     "Times New Roman": ("times.ttf", "timesbd.ttf"),
                     "Calibri": ("calibri.ttf", "calibrib.ttf")}.get(BODY_FONT, ("arial.ttf", "arialbd.ttf"))
            font = ImageFont.truetype(fname[1] if bold else fname[0], int(size * 10))
        except Exception:
            font = None
        _FONT_CACHE[key] = font
    font = _FONT_CACHE[key]
    if font is None:
        return len(text) * size * 0.55 * (1.08 if bold else 1.0) / 72 * 2.54
    return font.getlength(text) / 10 / 72 * 2.54


def column_widths(rows, group, total):
    """Column widths (cm) that fit `total`: natural width if it fits, otherwise let headers
    wrap at spaces/hyphens, otherwise give narrow columns their width and share the rest."""
    pad = 0.5  # default cell margins (2 x 0.19 cm) plus a little slack
    ncols = len(rows[0])
    full, desired, minimum = [], [], []
    for c in range(ncols):
        body = [plain(r[c]) for k, r in enumerate(rows) if k > 0 and not group[k]]
        head = plain(rows[0][c])
        body_long = max((text_cm(t) for t in body), default=0)
        body_word = max((text_cm(w) for t in body for w in t.split()), default=0)
        head_full = text_cm(head, bold=True)
        head_word = max((text_cm(w, bold=True) for w in re.findall(r"[^\s-]+-?", head)), default=0)
        full.append(max(body_long, head_full) + pad)
        desired.append(max(body_long, head_word) + pad)
        minimum.append(max(min(body_word, 3.0), head_word) + pad)
    if sum(full) <= total:
        return full
    if sum(desired) <= total:
        spare = total - sum(desired)
        extra = [f - d for f, d in zip(full, desired)]
        return [d + spare * e / sum(extra) for d, e in zip(desired, extra)]
    widths = [0.0] * ncols
    remaining, left = total, ncols
    for c in sorted(range(ncols), key=lambda k: desired[k]):
        w = max(min(desired[c], remaining / left), minimum[c])
        widths[c] = w
        remaining -= w
        left -= 1
    if sum(widths) > total:
        widths = [w * total / sum(widths) for w in widths]
    return widths


class Builder:
    def __init__(self, doc):
        self.doc = doc
        self.placeholders = []
        self.n_images = 0
        self.n_tables = 0
        self.missing_images = []

    def add_runs(self, p, text, size=None, bold=None, italic=None):
        runs = parse_inline(text)
        full = "".join(r[0] for r in runs)
        spans = [(m.start(), m.end()) for m in PLACEHOLDER_RE.finditer(full)]
        self.placeholders += [full[a:b] for a, b in spans]
        cuts = sorted({0, len(full)} | {x for sp in spans for x in sp})
        pos = 0
        for rtext, rb, ri, rc in runs:
            start, end = pos, pos + len(rtext)
            pos = end
            pieces = [start] + [c for c in cuts if start < c < end] + [end]
            for a, b in zip(pieces, pieces[1:]):
                if a == b:
                    continue
                run = p.add_run(full[a:b])
                run.bold = True if bold else (rb or None)
                if italic is not None:
                    run.italic = italic
                elif ri:
                    run.italic = True
                if rc:
                    set_rfonts(run._r, MONO_FONT)
                if size is not None:
                    run.font.size = Pt(size)
                if any(sa <= a and b <= sb for sa, sb in spans):
                    run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        return p

    def heading(self, level, text):
        if level == 1:
            p = self.doc.add_paragraph(style="Title")
        else:
            p = self.doc.add_paragraph(style=f"Heading {min(level - 1, 3)}")
        self.add_runs(p, text)
        return p

    def paragraph(self, text, references=False, keep_next=False):
        p = self.doc.add_paragraph()
        self.add_runs(p, text)
        if references:
            p.paragraph_format.left_indent = Cm(0.75)
            p.paragraph_format.first_line_indent = Cm(-0.75)
            p.paragraph_format.space_after = Pt(4)
        if keep_next or FULL_BOLD_RE.match(text) or text.rstrip().endswith(":"):
            p.paragraph_format.keep_with_next = True
        return p

    def caption(self, text):
        p = self.doc.add_paragraph(style="Caption")
        self.add_runs(p, text)
        return p

    def image(self, rel_path, keep_next):
        path = (SRC.parent / rel_path).resolve()
        if not path.exists():
            self.missing_images.append(rel_path)
            p = self.doc.add_paragraph()
            r = p.add_run(f"[MISSING IMAGE: {rel_path}]")
            r.font.highlight_color = WD_COLOR_INDEX.RED
            return p
        self.doc.add_picture(str(path), width=Cm(IMAGE_WIDTHS[path.name]) if path.name in IMAGE_WIDTHS else IMAGE_W)
        p = self.doc.paragraphs[-1]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = keep_next
        self.n_images += 1
        return p

    def quote(self, qlines):
        for k, q in enumerate(qlines):
            p = self.doc.add_paragraph()
            self.add_runs(p, q, size=QUOTE_PT)
            pf = p.paragraph_format
            pf.left_indent = Cm(1.0)
            pf.right_indent = Cm(0.5)
            pf.space_after = Pt(6) if k == len(qlines) - 1 else Pt(2)

    def list(self, items):
        num_ids = {}  # level -> numId for ordered lists (restart per list)
        for it in items:
            lvl = min(it["level"], 2)
            if it["ordered"]:
                style = "List Number" if lvl == 0 else f"List Number {lvl + 1}"
            else:
                style = "List Bullet" if lvl == 0 else f"List Bullet {lvl + 1}"
            p = self.doc.add_paragraph(style=style)
            for k in [k for k in num_ids if k > lvl]:
                del num_ids[k]  # a shallower item ends deeper numbered sublists
            if it["ordered"]:
                if lvl not in num_ids:
                    num_ids[lvl] = new_numbering(self.doc, style, it["num"] or 1)
                numpr = p._p.get_or_add_pPr().get_or_add_numPr()
                numpr.get_or_add_ilvl().val = 0
                numpr.get_or_add_numId().val = num_ids[lvl]
            else:
                # A bullet ends any deeper numbered list.
                for k in [k for k in num_ids if k >= lvl]:
                    del num_ids[k]
            self.add_runs(p, it["text"])
        if self.doc.paragraphs:
            self.doc.paragraphs[-1].paragraph_format.space_after = Pt(6)

    def table(self, rows):
        ncols = max(len(r) for r in rows)
        rows = [r + [""] * (ncols - len(r)) for r in rows]
        group = [k > 0 and r[0] and not any(c.strip() for c in r[1:]) for k, r in enumerate(rows)]

        widths = column_widths(rows, group, TEXT_W.cm)

        t = self.doc.add_table(rows=len(rows), cols=ncols)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False  # writes <w:tblLayout w:type="fixed"/>
        tbl = t._tbl
        tblPr = tbl.tblPr
        tblW = tblPr.find(qn("w:tblW"))
        if tblW is None:
            tblW = OxmlElement("w:tblW")
            tblPr.append(tblW)
        tblW.set(qn("w:type"), "dxa")
        tblW.set(qn("w:w"), str(int(sum(widths) / 2.54 * 1440)))
        for gc, w in zip(tbl.tblGrid.findall(qn("w:gridCol")), widths):
            gc.set(qn("w:w"), str(int(w / 2.54 * 1440)))

        keep_together = len(rows) <= 12
        for k, r in enumerate(rows):
            row = t.rows[k]
            trPr = row._tr.get_or_add_trPr()
            cant = OxmlElement("w:cantSplit")
            trPr.append(cant)
            if k == 0:
                hdr = OxmlElement("w:tblHeader")
                trPr.append(hdr)
            for c in range(ncols):
                row.cells[c].width = Cm(widths[c])
            cells = row.cells
            if group[k]:
                merged = cells[0].merge(cells[-1])
                cells = [merged]
                texts = [r[0]]
            else:
                texts = r
            for cell, text in zip(cells, texts):
                p = cell.paragraphs[0]
                pf = p.paragraph_format
                pf.space_before, pf.space_after, pf.line_spacing = Pt(1), Pt(1), 1.0
                if keep_together and k < len(rows) - 1:
                    pf.keep_with_next = True
                self.add_runs(p, text, size=TABLE_PT, bold=(k == 0) or None)
        # Small gap after the table.
        gap = self.doc.add_paragraph()
        gap.paragraph_format.space_after = Pt(0)
        gap.paragraph_format.line_spacing = 1.0
        mark = OxmlElement("w:rPr")
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "12")  # 6 pt empty line
        mark.append(sz)
        gap._p.get_or_add_pPr().append(mark)
        self.n_tables += 1
        return t


def build(src, out):
    text = src.read_text(encoding="utf-8")
    blocks = parse_blocks(text)
    doc = setup_document()
    b = Builder(doc)
    in_refs = False
    title_text = None
    for k, blk in enumerate(blocks):
        kind = blk[0]
        nxt = blocks[k + 1] if k + 1 < len(blocks) else None
        prev = blocks[k - 1] if k > 0 else None
        if kind == "h":
            level, htext = blk[1], blk[2]
            if level == 1 and title_text is None:
                title_text = plain(htext)
            if level <= 2:
                in_refs = plain(htext).strip().lower() == "references"
            b.heading(level, htext)
        elif kind == "p":
            ptext = blk[1]
            if prev and prev[0] == "img" and FULL_ITALIC_RE.match(ptext):
                b.caption(ptext)
            else:
                keep = bool(nxt and nxt[0] in ("table", "list", "quote"))
                b.paragraph(ptext, references=in_refs, keep_next=keep)
        elif kind == "img":
            is_cap = bool(nxt and nxt[0] == "p" and FULL_ITALIC_RE.match(nxt[1]))
            b.image(blk[1], keep_next=is_cap)
        elif kind == "table":
            b.table(blk[1])
        elif kind == "quote":
            b.quote(blk[1])
        elif kind == "list":
            b.list(blk[1])
    if title_text:
        doc.core_properties.title = title_text
    md_images = sum(1 for x in blocks if x[0] == "img")
    md_tables = sum(1 for x in blocks if x[0] == "table")
    try:
        doc.save(str(out))
    except PermissionError:
        sys.exit(f"ERROR: cannot write {out} - is it open in Word or LibreOffice? Close it and re-run.")
    return b, md_images, md_tables, blocks


# --------------------------------------------------------------------------- PDF + checks

def to_pdf(docx_path, pdf_path):
    if not SOFFICE.exists():
        sys.exit(f"ERROR: LibreOffice not found at {SOFFICE}")
    if pdf_path.exists():
        try:
            pdf_path.unlink()
        except PermissionError:
            sys.exit(f"ERROR: cannot replace {pdf_path} - is it open in a PDF viewer? Close it and re-run.")
    profile = Path(tempfile.gettempdir()) / "build_docx_lo_profile"
    cmd = [str(SOFFICE), f"-env:UserInstallation={profile.as_uri()}", "--headless",
           "--convert-to", "pdf", "--outdir", str(pdf_path.parent), str(docx_path)]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    produced = pdf_path.parent / (docx_path.stem + ".pdf")
    if produced != pdf_path and produced.exists():
        produced.replace(pdf_path)
    if not pdf_path.exists():
        sys.exit(f"ERROR: LibreOffice did not write the PDF.\nstdout: {res.stdout}\nstderr: {res.stderr}")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def check_pdf(pdf_path, blocks, png_dir=None, dpi=110):
    import fitz  # PyMuPDF

    problems = []
    doc = fitz.open(str(pdf_path))
    print(f"PDF: {pdf_path.name}, {doc.page_count} pages")
    w, h = doc[0].rect.width, doc[0].rect.height
    a4 = abs(w - 595.3) < 2 and abs(h - 841.9) < 2
    print(f"  page size {w:.0f} x {h:.0f} pt ({'A4' if a4 else 'NOT A4'})")
    if not a4:
        problems.append("page size is not A4")

    page_texts = [pg.get_text() for pg in doc]

    def find_heading(label):
        for pno, pg in enumerate(doc):
            lines = []
            for blk in pg.get_text("dict")["blocks"]:
                for ln in blk.get("lines", []):
                    t = "".join(sp["text"] for sp in ln["spans"]).strip()
                    if t:
                        lines.append((ln["bbox"][1], t))
            lines.sort()
            for idx, (y, t) in enumerate(lines):
                if t == label:
                    return pno + 1, idx == 0, y
        return None

    refs = find_heading("References")
    if refs:
        pno, at_top, y = refs
        where = "at the top of the page" if at_top else f"mid-page (y = {y:.0f} of {h:.0f} pt)"
        main_pages = pno - 1 if at_top else pno
        print(f"  'References' starts on page {pno}, {where}; main text = {main_pages} page(s)"
              f"{'' if at_top else ' (last one partial)'}")
    else:
        problems.append("'References' heading not found in PDF")
    appx = find_heading("Appendix A. Materials")
    if appx:
        print(f"  'Appendix A' starts on page {appx[0]}")

    # Images
    shown = []  # (page, width_cm, height_cm) of every image actually drawn
    for pno, pg in enumerate(doc):
        for info in pg.get_image_info():
            x0, y0, x1, y1 = info["bbox"]
            shown.append((pno + 1, (x1 - x0) / 72 * 2.54, (y1 - y0) / 72 * 2.54))
    n_md_images = sum(1 for x in blocks if x[0] == "img")
    md_imgs = [x[1] for x in blocks if x[0] == "img"]
    print(f"  images drawn in PDF: {len(shown)} (markdown has {n_md_images})")
    for (pno, wcm, hcm), name in zip(shown, md_imgs):
        print(f"    page {pno}: {name} ({wcm:.1f} x {hcm:.1f} cm)")
    if len(shown) < n_md_images:
        problems.append(f"only {len(shown)} of {n_md_images} images drawn in PDF")

    # Tables: the header's last cell and the last row's first and last cells must appear
    # (compared without whitespace, since cells wrap and break at hyphens).
    def squash(s):
        return re.sub(r"\s+", "", s)

    page_sq = [squash(t) for t in page_texts]
    full_sq = "".join(page_sq)
    tables = [x[1] for x in blocks if x[0] == "table"]
    found_tables = 0
    for t_idx, rows in enumerate(tables, 1):
        probes = [squash(plain(c)) for c in (rows[0][-1], rows[-1][0], rows[-1][-1])]
        probes = [p_ for p_ in probes if p_]
        ok = all(p_ in full_sq for p_ in probes)
        found_tables += ok
        header = norm(" | ".join(plain(c) for c in rows[0]))
        if not ok:
            problems.append(f"table {t_idx} ('{header[:50]}') not fully found in PDF text")
        else:
            first_cell = squash(plain(rows[1][0])) if len(rows) > 1 else probes[0]
            pages = [pno + 1 for pno, t in enumerate(page_sq) if first_cell in t and squash(plain(rows[0][-1])) in t]
            print(f"  table {t_idx:2d}: found ({len(rows) - 1} body rows), header '{header[:55]}'"
                  f"{', likely page ' + str(pages[0]) if len(pages) == 1 else ''}")
    print(f"  tables found: {found_tables} of {len(tables)}")

    # Leftover markdown
    leftovers = []
    for pno, t in enumerate(page_texts):
        for ln in t.splitlines():
            s = ln.strip()
            if ("**" in s or "`" in s or "![" in s or "|---" in s or "](" in s
                    or re.match(r"^#{1,6}\s", s)):
                leftovers.append((pno + 1, s[:90]))
    if leftovers:
        problems.append(f"{len(leftovers)} line(s) with leftover markdown")
        for pno, s in leftovers[:20]:
            print(f"  leftover markdown p{pno}: {s}")
    else:
        print("  no leftover markdown symbols (**, `, ![, |---, ](, #) in PDF text")

    if png_dir:
        png_dir = Path(png_dir)
        png_dir.mkdir(parents=True, exist_ok=True)
        for pno, pg in enumerate(doc):
            pg.get_pixmap(dpi=dpi).save(str(png_dir / f"page-{pno + 1:02d}.png"))
        print(f"  rendered {doc.page_count} pages to {png_dir}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-pdf", action="store_true", help="only build the .docx")
    ap.add_argument("--png", metavar="DIR", help="render every PDF page to DIR as PNG")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--font", default=BODY_FONT, help=f"body font (default {BODY_FONT})")
    args = ap.parse_args()
    globals()["BODY_FONT"] = args.font

    b, md_images, md_tables, blocks = build(SRC, OUT_DOCX)
    problems = []
    print(f"DOCX: {OUT_DOCX}")
    print(f"  images inserted: {b.n_images} of {md_images}; tables: {b.n_tables} of {md_tables}")
    if b.missing_images:
        problems.append(f"missing image files: {b.missing_images}")
    if b.n_tables != md_tables:
        problems.append("table count mismatch")
    print(f"  placeholders highlighted ({len(b.placeholders)}):")
    for ph in b.placeholders:
        print(f"    {ph}")

    if not args.no_pdf:
        to_pdf(OUT_DOCX, OUT_PDF)
        try:
            import fitz  # noqa: F401
        except ImportError:
            print(f"PDF written to {OUT_PDF} (PyMuPDF not available: checks skipped)")
        else:
            problems += check_pdf(OUT_PDF, blocks, png_dir=args.png, dpi=args.dpi)

    if problems:
        print("PROBLEMS:")
        for pr in problems:
            print(f"  - {pr}")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
