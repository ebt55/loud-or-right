"""Print a freeze manifest: SHA-256 of the item and code files, line counts, installed Ollama models, time.

  uv run --quiet --no-project python -I manifest.py
"""
import hashlib
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
CODE = ["design.py", "client.py", "api_client.py", "run.py", "screen.py", "probe.py", "run_all.py", "analyze.py"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def lines(p):
    return sum(1 for l in p.read_bytes().splitlines() if l.strip())


print(f"manifest generated {datetime.now().astimezone().isoformat(timespec='seconds')}")
print("\n## Items")
pool = HERE / "items_pool.jsonl"
print(f"{sha(pool)}  items_pool.jsonl  ({lines(pool)} lines)")
for p in sorted((HERE / "data").glob("selected_*.jsonl")):
    print(f"{sha(p)}  data/{p.name}  ({lines(p)} lines)")
print("\n## Code")
for name in CODE:
    p = HERE / name
    print(f"{sha(p)}  {name}" if p.exists() else f"MISSING  {name}")
print("\n## Ollama models (/api/tags, same content as `ollama list`)")
try:
    with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=10) as r:
        tags = json.loads(r.read())
    for m in tags.get("models", []):
        d = m.get("details", {})
        print(f"{m['name']:22s} digest {m.get('digest', '')[:12]}  {m.get('size', 0) / 1e9:.1f} GB  "
              f"{d.get('parameter_size', '')} {d.get('quantization_level', '')}  modified {m.get('modified_at', '')[:19]}")
except Exception as e:
    print(f"could not reach Ollama: {type(e).__name__}: {e}")
print("\n## `ollama list`")
try:
    import subprocess
    out = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30)
    print(out.stdout.strip() or out.stderr.strip())
except Exception as e:
    print(f"ollama CLI not available: {type(e).__name__}: {e}")
