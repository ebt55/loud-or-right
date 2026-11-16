"""Convert pilot v5 rows (pilot/f2_pilot5_*.jsonl) into the runner format, for testing analyze.py.

Writes (overwrites) harness/pilot_converted/pilot__gemma4_12b__instant__A.jsonl and ...__reasoned__A.jsonl.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
PILOT = HERE.parent / "pilot"
FILES = ("f2_pilot5_modes.jsonl", "f2_pilot5_extra.jsonl", "f2_pilot5_uniform.jsonl", "f2_pilot5_perfect.jsonl")
HIST_TO_LOG = {"none": "none", "reliable": "reliable", "confident_right": "certain_right",
               "hesitant_right": "unsure_right", "confident_right_long": "certain_right_long",
               "hesitant_right_long": "unsure_right_long", "all_confident": "all_certain",
               "all_hesitant": "all_unsure", "perfect_mixed": "perfect_mixed", "control": "control"}
MODE = {"N": "instant", "R": "reasoned"}


def main():
    out = {"instant": [], "reasoned": []}
    seen = {}
    for name in FILES:
        for line in (PILOT / name).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            p = json.loads(line)
            mode = MODE[p["mode"]]
            row = {"id": p["id"], "model": "gemma4:12b", "mode": mode, "arm": "A",
                   "log": HIST_TO_LOG[p["hist"]], "tone": p["tone"], "stratum": "wrong",
                   "own": p["own"], "x": p["x"], "final": p["final"], "flip": p["flip"],
                   "done": p["done"], "prompt_tokens": p["prompt_tokens"], "out_tokens": p["out_tokens"],
                   "reply": p["reply"]}
            key = (mode, row["id"], row["log"], row["tone"])
            seen[key] = seen.get(key, 0) + 1
            out[mode].append(row)
    dups = sum(v > 1 for v in seen.values())
    (HERE / "pilot_converted").mkdir(parents=True, exist_ok=True)
    for mode, rows in out.items():
        path = HERE / "pilot_converted" / f"pilot__gemma4_12b__{mode}__A.jsonl"
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        print(f"wrote {path} ({len(rows)} rows)")
    print(f"duplicate (mode, id, log, tone) keys across pilot files: {dups}")


if __name__ == "__main__":
    main()
