"""One-command refresh of the version 2 figures, tables and the report's Table 1.

    python paper/refresh_v2.py

1. Regenerates paper/figs/fig1_profiles.png, fig2_confirmatory.png, fig3_right_stratum.png, tab_summary.png and
   tables.md from the current files, with paper/make_figs.py. No analysis rerun is needed: frozen analysis outputs
   are used where they hold a group, and any run without one (Gemini 3.6 Flash's arm B in harness/runs and arm R in
   harness_x/runs, once those files exist) is computed from its raw file with harness/analyze.py's own functions
   (strict missing rule, by-voice population, same bootstrap). A run still in progress (fewer than 80 items with the
   no-log control and the four core cells) shows as "pending".
2. Replaces everything between the lines <!-- TABLE1:START --> and <!-- TABLE1:END --> in paper/report.md with the
   current Table 7 (header row included, no caption; the caption stays outside the markers). The marker lines and
   everything outside them are left as they are, and the file's line endings are kept. If the markers are missing,
   the report is not touched.

Options: --report PATH injects into another file (e.g. a copy, for testing); --no-report skips step 2.
For testing only: --runs-main and --runs-x point the raw-file scan at other folders; --out writes the figures and
tables to another folder.
"""
import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # leave no __pycache__ in paper/ or harness/
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_figs  # noqa: E402

GEMINI = "google:gemini-3.6-flash"
START, END = "<!-- TABLE1:START -->", "<!-- TABLE1:END -->"


def count_rows(path):
    with open(path, encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


def inject_table(report, table_lines):
    """Replace the lines strictly between the START and END marker lines with a blank line, the table and a blank
    line. Returns a status message; writes only when both markers are present once, in order."""
    with open(report, encoding="utf-8", newline="") as fh:
        text = fh.read()
    eol = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(eol)
    starts = [k for k, ln in enumerate(lines) if ln.strip() == START]
    ends = [k for k, ln in enumerate(lines) if ln.strip() == END]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        return (f"report NOT changed: expected one {START} line followed by one {END} line "
                f"(found {len(starts)} and {len(ends)})")
    new = lines[:starts[0] + 1] + [""] + list(table_lines) + [""] + lines[ends[0]:]
    if new == lines:
        return "report unchanged (Table 1 already current)"
    with open(report, "w", encoding="utf-8", newline="") as fh:
        fh.write(eol.join(new))
    return f"report updated: {len(table_lines)} table lines between the markers in {report}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--report", type=Path, default=HERE / "report.md", help="file to inject Table 1 into")
    ap.add_argument("--no-report", action="store_true", help="do not touch any report file")
    ap.add_argument("--runs-main", type=Path, help="folder scanned instead of harness/runs (testing)")
    ap.add_argument("--runs-x", type=Path, help="folder scanned instead of harness_x/runs (testing)")
    ap.add_argument("--out", type=Path, help="output folder instead of paper/figs (testing)")
    a = ap.parse_args()
    if a.runs_main:
        make_figs.RUNS_MAIN = a.runs_main.resolve()
    if a.runs_x:
        make_figs.RUNS_X = a.runs_x.resolve()
    if a.out:
        make_figs.OUT = a.out.resolve()
    tag = make_figs.run_tag(GEMINI)
    for label, f in (("Gemini 3.6 Flash arm B", make_figs.RUNS_MAIN / f"test__{tag}__instant__B.jsonl"),
                     ("Gemini 3.6 Flash arm R", make_figs.RUNS_X / f"test__{tag}__instant__R.jsonl")):
        print(f"{label}: {f'{count_rows(f)} rows in {f.name}' if f.exists() else 'not present yet'}")
    res = make_figs.main()
    if a.no_report:
        print("report: skipped (--no-report)")
    elif not a.report.exists():
        print(f"report NOT changed: {a.report} does not exist")
    else:
        print(inject_table(a.report, res["table7"]))


if __name__ == "__main__":
    main()
