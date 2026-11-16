"""Voice-over through the OpenAI text-to-speech REST API, one request per scene part, cached on disk.

Usage
    python tts.py              dry run: lists the requests, cache hits and estimated cost; makes NO network call
    python tts.py --go         generates missing clips (POST https://api.openai.com/v1/audio/speech)
    python tts.py --go --sapi  offline fallback only (Windows System.Speech), no network call

The key is read from the project .env by a local parser (nothing is printed, logged, written or put in a URL).
Models are tried in order: gpt-4o-mini-tts, tts-1-hd, tts-1. If all fail, the Windows offline voice is used.
Cache key = sha256(model, voice, instructions, speed, spoken text, format), so reruns never re-bill.
build/tts_cache/manifest.json records, per part, the model and voice actually used and the character count.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

import config as C
import script_text as S

URL = "https://api.openai.com/v1/audio/speech"
MODELS = ["gpt-4o-mini-tts", "tts-1-hd", "tts-1"]
VOICE = "nova"
INSTRUCTIONS = ("Voice: calm, clear and conversational, like the narrator of a science explainer video. "
                "Pace: steady, about 160 words per minute, with natural short pauses at full stops. "
                "Read the text exactly as written, without adding or skipping words.")
SPEED = 1.0                 # used for tts-1 / tts-1-hd only; gpt-4o-mini-tts follows the instructions
FORMAT = "wav"
# Approximate prices (USD) used for the README estimate.
PRICE = {"gpt-4o-mini-tts": ("per_min_audio", 0.015), "tts-1-hd": ("per_m_chars", 30.0), "tts-1": ("per_m_chars", 15.0)}


def read_env(path=C.ENV_FILE):
    """NAME -> value from .env. Values are secrets: never print them."""
    out = {}
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError:
        return out
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k = k.strip()
        if k.startswith("export "):
            k = k[7:].strip()
        out[k] = v.strip()
    return out


def scrub(text, env):
    for k in ("OPENAI_API_KEY", "OPENAI_ORG_ID", "OPENAI_PROJECT_ID"):
        v = env.get(k)
        if v:
            text = text.replace(v, "[redacted]")
    return text


def cache_key(model, spoken):
    instr = INSTRUCTIONS if model == "gpt-4o-mini-tts" else ""
    speed = SPEED if model != "gpt-4o-mini-tts" else None
    h = hashlib.sha256(json.dumps([model, VOICE, instr, speed, spoken, FORMAT]).encode("utf-8")).hexdigest()
    return h[:16]


def clip_path(pid, model, spoken):
    return C.AUDIO_CACHE / f"{pid}__{model}__{VOICE}__{cache_key(model, spoken)}.{FORMAT}"


def find_cached(pid, spoken):
    for m in MODELS:
        p = clip_path(pid, m, spoken)
        if p.exists() and p.stat().st_size > 1000:
            return p, m
    p = C.AUDIO_CACHE / f"{pid}__sapi__{hashlib.sha256(spoken.encode()).hexdigest()[:16]}.wav"
    if p.exists():
        return p, "sapi"
    return None, None


def estimate_cost(model, chars, seconds):
    kind, price = PRICE[model]
    return price * seconds / 60 if kind == "per_min_audio" else price * chars / 1e6


def request_clip(model, spoken, env, out_path):
    """One POST. Returns (ok, message). The key goes only into the Authorization header."""
    import urllib.error
    import urllib.request
    body = {"model": model, "input": spoken, "voice": VOICE, "response_format": FORMAT}
    if model == "gpt-4o-mini-tts":
        body["instructions"] = INSTRUCTIONS
    else:
        body["speed"] = SPEED
    hdr = {"Authorization": "Bearer " + env["OPENAI_API_KEY"], "Content-Type": "application/json"}
    if env.get("OPENAI_ORG_ID"):
        hdr["OpenAI-Organization"] = env["OPENAI_ORG_ID"]
    if env.get("OPENAI_PROJECT_ID"):
        hdr["OpenAI-Project"] = env["OPENAI_PROJECT_ID"]
    req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"), headers=hdr, method="POST")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            if len(data) < 1000:
                return False, f"short response ({len(data)} bytes)"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(data)
            return True, f"{len(data)} bytes"
        except urllib.error.HTTPError as e:
            try:
                msg = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                msg = ""
            msg = scrub(f"HTTP {e.code}: {msg}", env)
            if e.code in (429, 500, 502, 503) and attempt < 2:
                time.sleep(4 * (attempt + 1))
                continue
            return False, msg
        except Exception as e:  # network errors
            if attempt < 2:
                time.sleep(4)
                continue
            return False, scrub(f"{type(e).__name__}: {e}", env)
    return False, "retries exhausted"


SAPI_PS = r"""
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$pref = @('Microsoft Aria', 'Microsoft Jenny', 'Microsoft Zira Desktop', 'Microsoft David Desktop')
$names = $s.GetInstalledVoices() | Where-Object { $_.Enabled } | ForEach-Object { $_.VoiceInfo.Name }
foreach ($p in $pref) { $hit = $names | Where-Object { $_ -like "$p*" } | Select-Object -First 1; if ($hit) { $s.SelectVoice($hit); break } }
$s.Rate = 0
$s.SetOutputToWaveFile($env:LOR_OUT)
$s.Speak([IO.File]::ReadAllText($env:LOR_TXT))
$s.Dispose()
Write-Output $s.Voice.Name
"""


def sapi_clip(pid, spoken):
    import os
    import tempfile
    out = C.AUDIO_CACHE / f"{pid}__sapi__{hashlib.sha256(spoken.encode()).hexdigest()[:16]}.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(spoken)
        txt = f.name
    env = dict(os.environ, LOR_OUT=str(out), LOR_TXT=txt)
    r = subprocess.run(["powershell", "-NoProfile", "-Command", SAPI_PS], env=env, capture_output=True, text=True)
    os.unlink(txt)
    return out if out.exists() else None


def run(go=False, sapi_only=False, parts=None):
    import audio
    env = read_env()
    has_key = bool(env.get("OPENAI_API_KEY"))
    items = S.all_parts()
    if parts:
        items = [it for it in items if it[1] in parts]
    print(f"OpenAI key present: {'yes' if has_key else 'no'} (value not shown)")
    print(f"voice {VOICE}; models in order {MODELS}; {len(items)} parts")
    manifest_path = C.AUDIO_CACHE / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    total_chars, est = 0, 0.0
    for num, pid, written, spoken in items:
        total_chars += len(spoken)
        cached, model = find_cached(pid, spoken)
        if cached:
            print(f"  {pid}: cached ({model}) {cached.name}")
            continue
        est_sec = S.word_count(written) / 160 * 60
        est += estimate_cost(MODELS[0], len(spoken), est_sec)
        if not go:
            print(f"  {pid}: would request {MODELS[0]} ({len(spoken)} chars, ~{est_sec:.1f} s)")
            continue
        done = None
        if not sapi_only and has_key:
            for m in MODELS:
                ok, msg = request_clip(m, spoken, env, clip_path(pid, m, spoken))
                print(f"  {pid}: {m}: {'ok' if ok else 'failed'} ({msg})")
                if ok:
                    done = (clip_path(pid, m, spoken), m)
                    break
        if done is None:
            p = sapi_clip(pid, spoken)
            if p is None:
                raise SystemExit(f"{pid}: every voice failed")
            done = (p, "sapi")
            print(f"  {pid}: offline Windows voice")
        secs = audio.duration(done[0])
        manifest[pid] = {"file": done[0].name, "model": done[1], "voice": VOICE if done[1] != "sapi" else "sapi",
                         "chars": len(spoken), "seconds": round(secs, 3),
                         "est_cost_usd": round(estimate_cost(done[1], len(spoken), secs), 4) if done[1] != "sapi" else 0}
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"total spoken characters: {total_chars}; estimated cost of missing clips: ${est:.3f}")
    return manifest


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true", help="make the API requests (otherwise a dry run)")
    ap.add_argument("--sapi", action="store_true", help="use the offline Windows voice only")
    ap.add_argument("--parts", nargs="*", help="only these part ids, e.g. s01 s07a")
    a = ap.parse_args()
    run(go=a.go, sapi_only=a.sapi, parts=a.parts)
