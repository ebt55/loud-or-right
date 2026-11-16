"""Sample MMLU-Pro test items from the local HF cache into JSONL (run with: uv run --with pyarrow)."""
import json
import random
import sys
from pathlib import Path

import pyarrow.parquet as pq

src = Path.home() / ".cache/huggingface/hub/datasets--TIGER-Lab--MMLU-Pro/snapshots/527feea0afed1de15a8c115abf7be4c912123315/data/test-00000-of-00001.parquet"
rows = pq.read_table(src).to_pylist()
print("total rows", len(rows), "keys", list(rows[0].keys()), file=sys.stderr)
rng = random.Random(20261115)
# Keep items with at least 6 options and a short stem, so prompts stay small on a local model.
pool = [r for r in rows if len(r["options"]) >= 6 and len(r["question"]) < 700]
rng.shuffle(pool)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 80
out = Path(__file__).with_name("mmlu_pro_sample.jsonl")
with out.open("w", encoding="utf-8") as f:
    for r in pool[:n]:
        f.write(json.dumps({"id": r["question_id"], "category": r["category"], "question": r["question"],
                            "options": r["options"], "answer": r["answer"]}, ensure_ascii=False) + "\n")
print("wrote", n, "to", out, file=sys.stderr)
