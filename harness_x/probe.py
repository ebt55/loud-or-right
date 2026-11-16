"""Elicited reliability: show a log, then ask how often objections in this wording were right and the
probability that a new one is right. No question and no item content is ever sent.

  probe.py --model M --arm A|B [--n 40] [--workers N] [--items test|dev]

--items dev (smoke tests): arm-B seeds from data/selected_dev_<tag>.jsonl, output runs/probe_dev__<tag>__<arm>.jsonl.

Arm A: entry order is fixed, so one call per (log, tone), shuffle_seed null.
Arm B: one call per (log, tone, seed); seeds = ids of the first n wrong-stratum items in
data/selected_<tag>.jsonl (used only as RNG seeds for entry order and letters; no item text is sent).
Logs: every log in design.LOGS plus "none"; tones certain and unsure. Instant mode, JSON schema
design.PROBE_SCHEMA. Output runs/probe__<tag>__<arm>.jsonl, resume-safe like run.py.
"""
import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import design  # noqa: E402
from client import chat, is_api  # noqa: E402
from run import load_jsonl, now  # noqa: E402

MAX_TOKENS = 64   # the probe JSON is longer than one letter


def parse(txt):
    """(right, total, probability); probability None (= unparsed) if missing, not an integer or outside 0-100."""
    try:
        d = json.loads(txt)
        k, n, p = d.get("right"), d.get("total"), d.get("probability")
    except Exception:
        return None, None, None
    if not (isinstance(p, int) and not isinstance(p, bool) and 0 <= p <= 100):
        p = None
    return k, n, p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--arm", required=True, choices=["A", "B"])
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--items", default="test", choices=["test", "dev"],
                    help="only picks the arm-B seed source and the output name; no item text is ever sent")
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    if a.workers > 1 and not is_api(a.model):
        sys.exit("--workers > 1 is only allowed for provider-prefixed models")
    tg = design.tag(a.model)
    if a.arm == "A":
        seeds = [None]
    else:
        sel = HERE / "data" / (f"selected_{tg}.jsonl" if a.items == "test" else f"selected_dev_{tg}.jsonl")
        if not sel.exists():
            sys.exit(f"missing {sel}: arm B seeds are the ids of the first n wrong-stratum items")
        seeds = [s["id"] for s in load_jsonl(sel) if s["stratum"] == "wrong"][:a.n]

    out = HERE / "runs" / (f"probe__{tg}__{a.arm}.jsonl" if a.items == "test" else f"probe_dev__{tg}__{a.arm}.jsonl")
    out.parent.mkdir(exist_ok=True)
    rows = load_jsonl(out, repair=True) if out.exists() else []
    n_err = sum(1 for r in rows if r.get("error"))
    if n_err:
        rows = [r for r in rows if not r.get("error")]
        out.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    done = {(r["log"], r["tone"], r["shuffle_seed"]) for r in rows}
    todo = [(lg, t, s) for s in seeds for lg in design.PROBE_LOGS for t in ("certain", "unsure")
            if (lg, t, s) not in done]
    print(f"{out.name}: {len(todo)} calls to run ({len(rows)} rows on file, dropped {n_err} error rows)", flush=True)
    lock = threading.Lock()
    t0 = time.time()

    def one(job):
        lg, t, s = job
        msgs = design.probe_messages(lg, t, a.arm, s if s is not None else 0)
        r = chat(a.model, msgs, "instant", schema=design.PROBE_SCHEMA, max_tokens=MAX_TOKENS)
        k, n, p = parse(r["text"])
        row = {"model": a.model, "arm": a.arm, "log": lg, "tone": t, "shuffle_seed": s, "right": k, "total": n,
               "probability": p, "reply": r["text"], "done": r["done"], "prompt_tokens": r["prompt_tokens"],
               "out_tokens": r["out_tokens"], "error": r["error"], "ts": now()}
        if r.get("meta") is not None:
            row["meta"] = r["meta"]
        with lock:
            f.write(json.dumps(row) + "\n")
            f.flush()
            rows.append(row)

    with out.open("a", encoding="utf-8") as f:
        if a.workers <= 1:
            for job in todo:
                one(job)
        else:
            with ThreadPoolExecutor(max_workers=a.workers) as ex:
                for fut in [ex.submit(one, j) for j in todo]:
                    fut.result()
    print(f"ran {len(todo)} calls in {int(time.time() - t0)} s")
    ok = [r for r in rows if not r.get("error")]
    print(f"\n  {'log':20s} {'tone':8s} {'right/total':>11s} {'prob':>5s}   (arm {a.arm}; mean over seeds if several)")
    for lg in design.PROBE_LOGS:
        for t in ("certain", "unsure"):
            v = [r for r in ok if r["log"] == lg and r["tone"] == t and r["probability"] is not None]
            if not v:
                continue
            if len(v) == 1:
                rt = f"{v[0]['right']}/{v[0]['total']}"
                pr = f"{v[0]['probability']}"
            else:
                rt = f"{sum(r['right'] or 0 for r in v) / len(v):.1f}/{sum(r['total'] or 0 for r in v) / len(v):.1f}"
                pr = f"{sum(r['probability'] for r in v) / len(v):.0f}"
            print(f"  {lg:20s} {t:8s} {rt:>11s} {pr:>5s}")
    print(f"  unparsed {sum(r['probability'] is None for r in ok)}; cut off {sum(r['done'] == 'length' for r in ok)}; "
          f"errors {sum(bool(r.get('error')) for r in rows)}")


if __name__ == "__main__":
    main()
