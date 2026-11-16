"""Run log/objection trials.

  run.py --model gemma4:12b --mode instant|reasoned [--arm A|B|M] --items dev|test
         [--strata wrong,right] [--target key|distractor|both] [--cells g0,g1,core,reliable,none:certain]
         [--limit N_ITEMS] [--rep K] [--workers N]

Cells come from design.PLAN (segments in priority order). --cells takes group names (g0 g1 g2 g3 d0 right;
reasoned r2 rd; arm M: mit), "core" (g0 + g1 + d0, or rd in reasoned mode), log names (all tones) or log:tone pairs.
Target: wrong stratum "key" -> x = key; "distractor" -> x = design.distractor(item, own) (neither own nor key);
right stratum -> always "distractor", x as stored in the selected file. flip = (final == x).
--limit caps the number of items per stratum (not trials). --rep K (K >= 2) writes a separate __rep<K> file with a "rep"
field on every row. --workers N > 1 runs calls in a thread pool (provider-prefixed models only).
Output: runs/<items>__<tag>__<mode>__<arm>[__rep<K>].jsonl, one row per trial, appended and flushed.
Resume key (id, log, tone, target): rows with an error are dropped at startup and rerun; others are skipped.
Rows written before the target field existed count as target "key" (wrong) / "distractor" (right).
An unparsable last line (crash mid-write) is dropped with a warning.
--items dev: data/selected_dev_<tag>.jsonl if it exists, otherwise (gemma4:12b only) the pilot's 32 items
and committed answers (pilot/f2_pilot5_modes.jsonl).
"""
import argparse
import json
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import design  # noqa: E402
from client import NUM_CTX, NUM_PREDICT, chat, is_api  # noqa: E402

PILOT = HERE.parent / "pilot"


def now():
    return datetime.now().isoformat(timespec="seconds")


def load_jsonl(p, repair=False):
    """Read a JSONL file. With repair=True, an unparsable LAST line is dropped (with a warning) and the
    file rewritten without it; an unparsable line elsewhere is an error."""
    p = Path(p)
    lines = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    out = []
    for i, l in enumerate(lines):
        try:
            out.append(json.loads(l))
        except json.JSONDecodeError:
            if repair and i == len(lines) - 1:
                print(f"WARNING: dropping unparsable last line of {p.name}: {l[:80]!r}", flush=True)
                p.write_text("".join(json.dumps(r) + "\n" for r in out), encoding="utf-8")
            else:
                raise
    return out


def pool_by_id(path):
    return {it["id"]: it for it in load_jsonl(path)}


def dev_items(model="gemma4:12b"):
    sample = pool_by_id(PILOT / "mmlu_pro_sample.jsonl")
    sel = HERE / "data" / f"selected_dev_{design.tag(model)}.jsonl"
    if sel.exists():
        return [(sample[s["id"]], s["stratum"], s["own"], s["x"]) for s in load_jsonl(sel)]
    if model != "gemma4:12b":
        sys.exit(f"missing {sel}; run screen.py {model} --pool dev first")
    out, seen = [], set()
    for r in load_jsonl(PILOT / "f2_pilot5_modes.jsonl"):
        if r["id"] not in seen:
            seen.add(r["id"])
            out.append((sample[r["id"]], "wrong", r["own"], r["x"]))
    return out


def test_items(model):
    if not (HERE / "FREEZE.md").exists():
        sys.exit("refusing to run on test items: harness/FREEZE.md does not exist")
    sel = HERE / "data" / f"selected_{design.tag(model)}.jsonl"
    if not sel.exists():
        sys.exit(f"missing {sel}; run screen.py first")
    pool = pool_by_id(HERE / "items_pool.jsonl")
    return [(pool[s["id"]], s["stratum"], s["own"], s["x"]) for s in load_jsonl(sel)]


def row_target(r):
    return r.get("target") or ("key" if r["stratum"] == "wrong" else "distractor")


def target_x(it, stratum, own, x_stored, target):
    if stratum == "right":
        return x_stored
    return it["answer"] if target == "key" else design.distractor(it, own)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--mode", required=True, choices=["instant", "reasoned"])
    ap.add_argument("--arm", default="A", choices=["A", "B", "M"])
    ap.add_argument("--items", required=True, choices=["dev", "test"])
    ap.add_argument("--strata", default=None)
    ap.add_argument("--target", default="both", choices=["key", "distractor", "both"])
    ap.add_argument("--cells", default=None)
    ap.add_argument("--limit", type=int, default=None, help="max number of items per stratum")
    ap.add_argument("--rep", type=int, default=1)
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    if a.workers > 1 and not is_api(a.model):
        sys.exit("--workers > 1 is only allowed for provider-prefixed models (one local GPU, sequential calls)")

    items = dev_items(a.model) if a.items == "dev" else test_items(a.model)
    if a.limit:   # cap per stratum, so a small smoke still covers both strata
        seen = defaultdict(int)
        keep = []
        for t in items:
            if seen[t[1]] < a.limit:
                keep.append(t)
                seen[t[1]] += 1
        items = keep
    strata = set(a.strata.split(",")) if a.strata else None
    try:
        plan = design.select_plan(a.mode, a.cells, a.target, strata, a.arm)
    except ValueError as e:
        sys.exit(str(e))

    suffix = f"__rep{a.rep}" if a.rep >= 2 else ""
    out = HERE / "runs" / f"{a.items}__{design.tag(a.model)}__{a.mode}__{a.arm}{suffix}.jsonl"
    out.parent.mkdir(exist_ok=True)
    rows = load_jsonl(out, repair=True) if out.exists() else []
    n_err = sum(1 for r in rows if r.get("error"))
    if n_err:
        rows = [r for r in rows if not r.get("error")]
        out.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    done = {(r["id"], r["log"], r["tone"], row_target(r)) for r in rows}
    todo = [(seg, tgt, cell, t) for seg, stratum, tgt, cell in plan for t in items
            if t[1] == stratum and (t[0]["id"], cell[0], cell[1], tgt) not in done]
    n_cells = len({(c, tg, s) for _, s, tg, c in plan})
    print(f"{out.name}: {len(items)} items, {n_cells} (cell, target, stratum) combinations; {len(rows)} rows on file "
          f"(dropped {n_err} error rows); {len(todo)} trials to run; workers {a.workers}", flush=True)

    t0 = time.time()
    lock = threading.Lock()
    stats = {"new": 0, "fail": 0}
    api = is_api(a.model)

    def trial(job):
        seg, tgt, (log, tone), (it, stratum, own, x_stored) = job
        x = target_x(it, stratum, own, x_stored, tgt)
        msgs = design.build_messages(it, own, x, log, tone, a.mode, a.arm)
        r = chat(a.model, msgs, a.mode, n_opts=len(it["options"]))
        pt = r["prompt_tokens"]
        row = {"id": it["id"], "model": a.model, "mode": a.mode, "arm": a.arm, "log": log, "tone": tone,
               "target": tgt, "stratum": stratum, "own": own, "x": x, "key": it["answer"], "final": r["letter"],
               "flip": int(r["letter"] == x), "done": r["done"], "prompt_tokens": pt, "out_tokens": r["out_tokens"],
               "reply": r["text"], "error": r["error"],
               "trunc_risk": None if (pt is None or api) else pt + NUM_PREDICT[a.mode] > NUM_CTX,
               "segment": seg, "ts": now()}
        if a.rep >= 2:
            row["rep"] = a.rep
        if r.get("meta") is not None:
            row["meta"] = r["meta"]
        with lock:
            f.write(json.dumps(row) + "\n")
            f.flush()
            rows.append(row)
            stats["new"] += 1
            stats["fail"] += bool(r["error"])
            if stats["new"] % 200 == 0:
                print(f"  {stats['new']}/{len(todo)} trials, {int(time.time() - t0)} s, errors {stats['fail']}, "
                      f"now at {seg} {log}/{tone}", flush=True)

    with out.open("a", encoding="utf-8") as f:
        if a.workers <= 1:
            for job in todo:
                trial(job)
        else:
            with ThreadPoolExecutor(max_workers=a.workers) as ex:   # submitted in priority order
                for fut in [ex.submit(trial, job) for job in todo]:
                    fut.result()
    print(f"ran {stats['new']} trials in {int(time.time() - t0)} s; errors {stats['fail']}")

    # k/n per (cell, target, stratum) over the selected items and plan
    ids = {t[0]["id"] for t in items}
    ok = [r for r in rows if not r.get("error") and r["id"] in ids]
    by = defaultdict(list)
    for r in ok:
        by[(r["log"], r["tone"], row_target(r), r["stratum"])].append(r["flip"])
    print(f"\nflips to the reviewer's option, k/n ({a.items}, {a.model}, {a.mode}, arm {a.arm}, rep {a.rep}):")
    print(f"  {'segment':8s} {'log':20s} {'tone':8s} {'target':10s} {'stratum':7s} {'k/n':>7s}")
    for seg, stratum, tgt, (log, tone) in plan:
        v = by[(log, tone, tgt, stratum)]
        print(f"  {seg:8s} {log:20s} {tone:8s} {tgt:10s} {stratum:7s} {f'{sum(v)}/{len(v)}':>7s}")
    print(f"  unparsed {sum(r['final'] == '?' for r in ok)}; cut off {sum(r['done'] == 'length' for r in ok)}; "
          f"trunc_risk {sum(bool(r['trunc_risk']) for r in ok)}; "
          f"largest prompt {max([r['prompt_tokens'] or 0 for r in ok] or [0])} tokens")


if __name__ == "__main__":
    main()
