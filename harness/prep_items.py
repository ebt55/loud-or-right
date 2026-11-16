"""Build the test pool from the MMLU-Pro test split. Run with: uv run --quiet --no-project --with pyarrow python -I prep_items.py"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pyarrow.parquet as pq  # noqa: E402

HERE = Path(__file__).resolve().parent
SRC = (Path.home() / ".cache/huggingface/hub/datasets--TIGER-Lab--MMLU-Pro/snapshots/"
       "527feea0afed1de15a8c115abf7be4c912123315/data/test-00000-of-00001.parquet")
OUT = HERE / "items_pool.jsonl"
EXCLUDED_CATS = {"math", "physics", "chemistry", "engineering"}
N_POOL = 1600   # was 800; extended by appending the next 800 of the same shuffle

rows = pq.read_table(SRC, columns=["question_id", "question", "options", "answer", "category"]).to_pylist()
by_id = {r["question_id"]: r for r in rows}
dev = [json.loads(l) for l in (HERE.parent / "pilot" / "mmlu_pro_sample.jsonl").read_text(encoding="utf-8").splitlines()]
dev_ids = {d["id"] for d in dev}
# The dev-id exclusion only works if the pilot's "id" is the parquet question_id: check every dev item.
mismatch = [d["id"] for d in dev if d["id"] not in by_id or by_id[d["id"]]["question"] != d["question"]
            or list(by_id[d["id"]]["options"]) != d["options"]]
assert not mismatch, f"dev ids not matching parquet question_id: {mismatch[:5]}"
print(f"parquet rows {len(rows)}; all {len(dev_ids)} development ids match question_id, question and options")


def passes(r):
    opts = r["options"]
    return (len(opts) >= 6 and len(r["question"]) < 700 and r["category"] not in EXCLUDED_CATS
            and sum(any(c.isdigit() for c in o) for o in opts) < len(opts) / 2)


ok = [r for r in rows if passes(r)]
print(f"passing the rule before removing development ids: {len(ok)}")
dev_in = [r for r in ok if r["question_id"] in dev_ids]
ok = [r for r in ok if r["question_id"] not in dev_ids]
print(f"development ids that passed the rule and were removed: {len(dev_in)}; remaining {len(ok)}")
random.Random(20261116).shuffle(ok)
pool = ok[:N_POOL]
for r in pool:
    assert r["answer"] in "ABCDEFGHIJ"[:len(r["options"])], r["question_id"]
# The first 800 were written with Windows text mode (CRLF); keep the existing file's line ending.
eol = b"\r\n" if (not OUT.exists() or b"\r\n" in OUT.read_bytes()[:20000]) else b"\n"
lines = [json.dumps({"id": r["question_id"], "category": r["category"], "question": r["question"],
                     "options": list(r["options"]), "answer": r["answer"]}).encode("utf-8") + eol for r in pool]
if OUT.exists():
    # The pool may only grow by appending: every existing line must be reproduced byte for byte.
    old = OUT.read_bytes().splitlines(keepends=True)
    assert old == lines[:len(old)], "existing items_pool.jsonl lines differ from the regenerated ones; not writing"
    print(f"existing {len(old)} lines reproduced byte-identically; appending {len(lines) - len(old)}")
OUT.write_bytes(b"".join(lines))
print(f"wrote {len(pool)} items to {OUT}")
print("pool counts by category:")
for c, n in sorted(Counter(r["category"] for r in pool).items(), key=lambda kv: -kv[1]):
    print(f"  {c:18s} {n}")
print(f"options per item: {dict(sorted(Counter(len(r['options']) for r in pool).items()))}")
