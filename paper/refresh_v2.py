"""One-command refresh of the version 2 figures and tables.

    python paper/refresh_v2.py

Regenerates paper/figs/fig1_profiles.png, fig2_confirmatory.png, fig3_right_stratum.png, tab_summary.png and
tables.md from the current files, with paper/make_figs.py. No analysis rerun is needed: frozen analysis outputs are
used where they hold a group, and any run without one (Gemini 3.6 Flash's arm B in harness/runs and arm R in
harness_x/runs, once those files exist) is computed from its raw file with harness/analyze.py's own functions
(strict missing rule, by-voice population, same bootstrap). A run that is still in progress (fewer than 80 items
with the no-log control and the four core cells) shows as "pending" in the figure and the table.

Options for testing only: --runs-main and --runs-x point the raw-file scan at other folders, and --out writes the
outputs to another folder.
"""
import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # leave no __pycache__ in paper/ or harness/
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_figs  # noqa: E402

GEMINI = "google:gemini-3.6-flash"


def count_rows(path):
    with open(path, encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
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
    make_figs.main()


if __name__ == "__main__":
    main()
