"""Run every test-item job, strictly one after another.

  run_all.py <model> [<model> ...] [--workers N] [--items test|dev] [--limit N]
  (--workers is passed only to provider-prefixed models; --items dev and --limit are for smoke tests:
   --items dev skips the FREEZE check, --limit caps items per stratum and the probe's arm-B seed count)

Phases, each over every model (local models first, in the order given, then hosted):
(i) instant arm A, all groups; (ii) probe.py arm A then arm B; (iii) instant arm A rep 2, g0 only;
(iv) reasoned arm A; (v) instant arm B, --cells core; (vi) instant arm M, --cells mit;
(vii) reasoned arm M, --cells mit (not for openrouter: models).
Each job is a subprocess with output appended to logs/<job>.log. A failed job is reported and the
driver goes on. Resumable: rerunning skips finished trials through run.py's own resume.
With --items test (default) refuses to start without harness/FREEZE.md.
"""
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import design  # noqa: E402
from client import is_api  # noqa: E402

PY = ["uv", "run", "--quiet", "--no-project", "python", "-I"]
SCRIPTS = HERE   # where run.py / probe.py live (HERE may be repointed in tests; SCRIPTS is not)


def jobs(models, workers, items="test", limit=None):
    """[(job name, script, args)] in run order. Local models first (in the order given), then hosted ones."""
    models = [m for m in models if not is_api(m)] + [m for m in models if is_api(m)]
    it = ["--items", items] + (["--limit", str(limit)] if limit else [])
    pn = (["--n", str(limit)] if limit else []) + (["--items", items] if items != "test" else [])
    pa = ["--items", items] if items != "test" else []
    phases = [("run.py", ["--mode", "instant", "--arm", "A"] + it, "instant_A"),
              ("probe.py", ["--arm", "A"] + pa, "probe_A"),
              ("probe.py", ["--arm", "B"] + pn, "probe_B"),
              ("run.py", ["--mode", "instant", "--arm", "A", "--rep", "2", "--cells", "g0"] + it, "instant_A_rep2"),
              ("run.py", ["--mode", "reasoned", "--arm", "A"] + it, "reasoned_A"),
              ("run.py", ["--mode", "instant", "--arm", "B", "--cells", "core"] + it, "instant_B_core"),
              ("run.py", ["--mode", "instant", "--arm", "M", "--cells", "mit"] + it, "instant_M_mit"),
              ("run.py", ["--mode", "reasoned", "--arm", "M", "--cells", "mit"] + it, "reasoned_M_mit")]
    prefix = "" if items == "test" else f"{items}_"
    out = []
    for i, (script, extra, label) in enumerate(phases):
        # phase (ii) is probe arm A then arm B for each model before the next model
        if label == "probe_B":
            continue
        for m in models:
            if label == "reasoned_M_mit" and m.startswith("openrouter:"):
                continue   # OpenRouter models get phase (vi) only
            for sc, ex, lb in ([phases[i], phases[i + 1]] if label == "probe_A" else [(script, extra, label)]):
                args = ["--model", m] + ex
                if workers > 1 and is_api(m):
                    args += ["--workers", str(workers)]
                out.append((f"{prefix}{lb}__{design.tag(m)}", sc, args))
    return out


def pop_opt(argv, name, default, cast=str):
    if name in argv:
        i = argv.index(name)
        val = cast(argv[i + 1])
        return val, argv[:i] + argv[i + 2:]
    return default, argv


def main():
    argv = sys.argv[1:]
    workers, argv = pop_opt(argv, "--workers", 1, int)
    items, argv = pop_opt(argv, "--items", "test")
    limit, argv = pop_opt(argv, "--limit", None, int)
    models = argv
    if not models or items not in ("test", "dev"):
        sys.exit("usage: run_all.py <model> [<model> ...] [--workers N] [--items test|dev] [--limit N]")
    if items == "test" and not (HERE / "FREEZE.md").exists():
        sys.exit("refusing to start: harness/FREEZE.md does not exist")
    sel = "selected_" if items == "test" else "selected_dev_"
    missing = [m for m in models if not (HERE / "data" / f"{sel}{design.tag(m)}.jsonl").exists()
               and not (items == "dev" and m == "gemma4:12b")]
    if missing:
        print(f"WARNING: no {sel}<tag>.jsonl for {missing}; their jobs will fail", flush=True)
    logs = HERE / "logs"
    logs.mkdir(exist_ok=True)
    js = jobs(models, workers, items, limit)
    print(f"{len(js)} jobs (items {items}, limit {limit})", flush=True)
    n_fail = 0
    for k, (name, script, args) in enumerate(js, start=1):
        t0 = time.time()
        with (logs / f"{name}.log").open("a", encoding="utf-8") as lg:
            lg.write(f"\n=== {datetime.now().isoformat(timespec='seconds')} {script} {' '.join(args)}\n")
            lg.flush()
            try:
                rc = subprocess.run(PY + [str(SCRIPTS / script)] + args, stdout=lg, stderr=subprocess.STDOUT,
                                    cwd=str(HERE)).returncode
            except Exception as e:
                lg.write(f"driver error: {e}\n")
                rc = f"driver error {type(e).__name__}"
        n_fail += rc != 0
        status = "ok" if rc == 0 else f"FAILED (exit {rc})"
        print(f"[{k}/{len(js)}] {name}: {status}, {int(time.time() - t0)} s, log logs/{name}.log", flush=True)
    print(f"done: {len(js) - n_fail} ok, {n_fail} failed", flush=True)


if __name__ == "__main__":
    main()
