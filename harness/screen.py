"""Screen items: bare question only (no log, no objection).

  screen.py <model> [--pool test|dev] [--workers N] [--force]

Per item: first answer at temperature 0, seed 7 (the committed answer), then 3 samples at temperature 0.7
(seeds 101-103; --samples N changes the count, hosted models use 1); agree = share of samples equal to the first answer.
--pool test (default): walks items_pool.jsonl in order, stops at 80 wrong and 40 right or at the end of the
  pool (whole items_pool.jsonl). Files: data/screen_<tag>.jsonl, data/selected_<tag>.jsonl.
--pool dev: screens all 80 items of pilot/mmlu_pro_sample.jsonl; selects up to 32 wrong and 16 right in file
  order. Files: data/screen_dev_<tag>.jsonl, data/selected_dev_<tag>.jsonl.
Every screened item is appended to the screen file; on resume, items already in it are never asked again
(unless the first call errored). The selected file is never overwritten without --force.
--workers N > 1 screens N items at a time in a thread pool (provider-prefixed models only).
"""
import json
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import design  # noqa: E402
from client import chat, is_api  # noqa: E402
from run import load_jsonl  # noqa: E402

SAMPLE_TEMP = 0.7   # sample seeds are 101, 102, ... (one per --samples)
POOLS = {"test": {"src": HERE / "items_pool.jsonl", "prefix": "", "n_wrong": 80, "n_right": 40, "stop_early": True},
         "dev": {"src": HERE.parent / "pilot" / "mmlu_pro_sample.jsonl", "prefix": "dev_", "n_wrong": 32,
                 "n_right": 16, "stop_early": False}}


def arg_value(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def main():
    flags_with_values = {"--pool", "--workers", "--samples"}
    args, skip = [], False
    for a in sys.argv[1:]:
        if skip:
            skip = False
            continue
        if a in flags_with_values:
            skip = True
            continue
        if not a.startswith("--"):
            args.append(a)
    if not args:
        sys.exit("usage: screen.py <model> [--pool test|dev] [--workers N] [--samples N] [--force]")
    model = args[0]
    force = "--force" in sys.argv
    pool_name = arg_value("--pool", "test")
    workers = int(arg_value("--workers", "1"))
    sample_seeds = [101 + i for i in range(int(arg_value("--samples", "3")))]
    if pool_name not in POOLS:
        sys.exit(f"--pool must be one of {list(POOLS)}")
    if workers > 1 and not is_api(model):
        sys.exit("--workers > 1 is only allowed for provider-prefixed models")
    P = POOLS[pool_name]
    tg = design.tag(model)
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    scr, sel = data / f"screen_{P['prefix']}{tg}.jsonl", data / f"selected_{P['prefix']}{tg}.jsonl"
    if sel.exists() and not force:
        sys.exit(f"{sel} exists: committed answers are fixed. Use --force to overwrite.")

    pool = load_jsonl(P["src"])
    rows = load_jsonl(scr, repair=True) if scr.exists() else []
    # A row whose first (committed) call failed holds no answer: drop it so the item is screened again.
    good = [r for r in rows if not r.get("first_error")]
    if len(good) < len(rows):
        scr.write_text("".join(json.dumps(r) + "\n" for r in good), encoding="utf-8")
    done = {r["id"]: r for r in good}
    t0 = time.time()
    lock = threading.Lock()

    def counts():
        rs = list(done.values())
        return sum(r["stratum"] == "wrong" for r in rs), sum(r["stratum"] == "right" for r in rs)

    def screen_one(order, it):
        n = len(it["options"])
        msgs = design.screen_messages(it)
        t1 = time.time()
        r0 = chat(model, msgs, "instant", n_opts=n)
        samples = [chat(model, msgs, "instant", n_opts=n, temperature=SAMPLE_TEMP, seed=s) for s in sample_seeds]
        errs = [r["error"] for r in [r0] + samples if r["error"]]
        first = r0["letter"]
        stratum = None if r0["error"] or first == "?" else ("right" if first == it["answer"] else "wrong")
        ok_s = [s["letter"] for s in samples if not s["error"]]
        row = {"id": it["id"], "order": order, "category": it["category"], "key": it["answer"], "first": first,
               "stratum": stratum, "samples": [s["letter"] for s in samples],
               "agree": (sum(s == first for s in ok_s) / len(ok_s)) if ok_s else None,
               "prompt_tokens": r0["prompt_tokens"], "out_tokens": r0["out_tokens"],
               "secs_item": round(time.time() - t1, 2), "n_calls": 1 + len(sample_seeds), "reply": r0["text"],
               "first_error": r0["error"], "errors": errs, "ts": datetime.now().isoformat(timespec="seconds")}
        if r0.get("meta") is not None:
            row["meta"] = r0["meta"]
        with lock:
            f.write(json.dumps(row) + "\n")
            f.flush()
            done[it["id"]] = row
            if len(done) % 25 == 0:
                nw, nr = counts()
                print(f"  screened {len(done)}: wrong {nw}, right {nr}, {int(time.time() - t0)} s", flush=True)

    todo = [(o, it) for o, it in enumerate(pool) if it["id"] not in done]
    with scr.open("a", encoding="utf-8") as f:
        for i in range(0, len(todo), max(workers, 1)):
            nw, nr = counts()
            if P["stop_early"] and nw >= P["n_wrong"] and nr >= P["n_right"]:
                break
            batch = todo[i:i + max(workers, 1)]
            if workers <= 1:
                screen_one(*batch[0])
            else:
                with ThreadPoolExecutor(max_workers=workers) as ex:
                    for fut in [ex.submit(screen_one, o, it) for o, it in batch]:
                        fut.result()

    rs = sorted(done.values(), key=lambda r: r["order"])
    nw, nr = counts()
    unparsed = sum(r["stratum"] is None for r in rs)
    secs = [r.get("secs_item", r.get("secs_4calls")) for r in rs if r.get("secs_item", r.get("secs_4calls")) is not None]
    print(f"screened {len(rs)} items ({int(time.time() - t0)} s this session): wrong {nw}, right {nr}, "
          f"unparsed/error {unparsed}; first-answer accuracy {nr}/{len(rs)} = {nr / max(len(rs), 1):.3f}; "
          f"mean s per item ({1 + len(sample_seeds)} calls each this session) {sum(secs) / max(len(secs), 1):.2f}")
    wrong = [r for r in rs if r["stratum"] == "wrong"][:P["n_wrong"]]
    right = [r for r in rs if r["stratum"] == "right"][:P["n_right"]]
    for name, grp in (("wrong", wrong), ("right", right)):
        ag = [r["agree"] for r in grp if r["agree"] is not None]
        print(f"  selected {name}: {len(grp)}; mean agree {sum(ag) / max(len(ag), 1):.3f}; "
              f"agree==1 for {sum(a == 1 for a in ag)}")
    if P["stop_early"] and (len(wrong) < P["n_wrong"] or len(right) < P["n_right"]):
        print(f"  WARNING: targets not met ({P['n_wrong']} wrong, {P['n_right']} right)")

    pool_by = {it["id"]: it for it in pool}
    out = []
    for r in wrong + right:
        it = pool_by[r["id"]]
        if r["stratum"] == "wrong":
            x = it["answer"]
        else:  # a wrong option fixed by the item id
            x = random.Random(int(it["id"])).choice([l for l in design.LETTERS[:len(it["options"])] if l != it["answer"]])
        out.append({"id": r["id"], "stratum": r["stratum"], "own": r["first"], "x": x, "agree": r["agree"],
                    "category": r["category"], "order": r["order"]})
    out.sort(key=lambda r: r["order"])
    sel.write_text("".join(json.dumps(r) + "\n" for r in out), encoding="utf-8")
    print(f"wrote {len(out)} rows to {sel}")


if __name__ == "__main__":
    main()
