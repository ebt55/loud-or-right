"""Export the deck to PDF with LibreOffice, then QA it with PyMuPDF.

Usage: python export_and_check.py [png_dir]
  - converts ../loud-or-right-slides.pptx (Space Grotesk + Inter; DECK_FONTS=segoe: ../loud-or-right-slides-segoe.pptx)
    to PDF (headless LibreOffice, throwaway profile so a running or locked user profile cannot block the export);
  - prints page count and size, embedded fonts (flags any font outside the variant's set), and the smallest
    text size per page;
  - renders every page to PNG in png_dir (default: ./renders) for visual review.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
GROTESK = os.environ.get("DECK_FONTS", "").lower() != "segoe"  # default: Space Grotesk + Inter (main deck)
DECK = HERE.parent / ("loud-or-right-slides.pptx" if GROTESK else "loud-or-right-slides-segoe.pptx")
PDF = DECK.with_suffix(".pdf")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"


def export():
    profile = Path(tempfile.gettempdir()) / "lo_profile_loud_or_right"
    cmd = [SOFFICE, f"-env:UserInstallation={profile.as_uri()}", "--headless", "--norestore",
           "--convert-to", "pdf", "--outdir", str(DECK.parent), str(DECK)]
    subprocess.run(cmd, check=True, timeout=240)
    if not PDF.exists():
        sys.exit("PDF export failed")


def check(png_dir: Path):
    doc = pymupdf.open(PDF)
    print(f"pages: {doc.page_count}")
    fonts = set()
    png_dir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc, 1):
        r = page.rect
        sizes = []
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for sp in line["spans"]:
                    if sp["text"].strip():
                        sizes.append((round(sp["size"], 1), sp["text"].strip()[:40]))
        for f in page.get_fonts():
            fonts.add(f[3].split("+")[-1])
        smallest = min(sizes) if sizes else None
        print(f"page {i}: {r.width:.0f}x{r.height:.0f} pt, smallest text {smallest}")
        page.get_pixmap(dpi=110).save(png_dir / f"slide-{i}.png")
    print("fonts:", sorted(fonts))
    ok = ("segoeuisymbol", "inter", "spacegrotesk") if GROTESK else ("segoeui",)
    bad = [f for f in fonts if not f.lower().replace("-", "").startswith(ok)]
    if bad:
        print("WARNING unexpected fonts:", bad)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "renders"
    export()
    check(out)
