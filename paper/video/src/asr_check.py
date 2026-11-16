"""Transcription gate for the voice-over clips: every word of the script must be heard, by two engines.

    python paper/video/src/asr_check.py              check every part of script.md against its cached clip
    python paper/video/src/asr_check.py s04 s06      check only these parts

Both engines are local; neither makes a network call.
1. faster-whisper with the cached model "Systran/faster-distil-whisper-large-v3" (local_files_only), CUDA float16
   with a CPU int8 fallback. Each clip is decoded with ffmpeg to mono 16 kHz float32 and passed as a numpy array
   (faster-whisper's own decode_audio fails here with a PyAV keyword error).
2. NVIDIA Nemotron ASR through a local nemo-speech CLI install, always with a local GGUF model path. Paths come
   from the environment (NEMO_SPEECH_EXE, NEMO_SPEECH_MODEL) or from paper/video/asr_local.env (KEY=VALUE lines,
   not committed). The
   OpenAI WAVs carry a streaming header that nemo-speech rejects, so each clip is first rewritten by ffmpeg as
   16 kHz mono PCM into a temporary directory.

Both transcripts are normalised (lowercase, no punctuation, numbers spelled out, a few spelling equivalences) and
compared with the spoken form of the script (script_text.spoken) as word lists with difflib. A part fails an
engine if any script word is missing, if the transcript stops before the last sentence, or if "luck at" appears.
A part passes only if both engines pass. Word timestamps (faster-whisper) go to build/asr_check.json.
Exit code 1 on any failure.
"""
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np  # noqa: E402

import config as C  # noqa: E402
import script_text as S  # noqa: E402
import tts  # noqa: E402

WHISPER_MODEL = "Systran/faster-distil-whisper-large-v3"


def _local_setting(name):
    """NAME from the environment, else from paper/video/asr_local.env (machine-specific, not committed)."""
    if os.environ.get(name):
        return os.environ[name]
    f = C.VIDEO / "asr_local.env"
    if f.exists():
        for ln in f.read_text(encoding="utf-8-sig").splitlines():
            k, _, v = ln.partition("=")
            if k.strip() == name:
                return v.strip()
    return ""


NEMO_EXE = Path(_local_setting("NEMO_SPEECH_EXE") or "nemo-speech.exe")
NEMO_MODEL = Path(_local_setting("NEMO_SPEECH_MODEL") or "nemotron-3.5-asr-streaming-0.6b.q8_0.gguf")
OUT_JSON = C.BUILD / "asr_check.json"

# Spelling equivalences (heard token -> script token), applied to both sides after tokenising.
EQUIV = {
    "lama": "llama", "randomize": "randomise", "favored": "favoured", "favor": "favour",
    "soul": "sol", "saul": "sol", "sols": "sol",
    # Homophone and name spellings that one engine produced on unchanged clips while the other heard the
    # script word (baseline run, 16 Nov): s03 "past" -> whisper "passed"; s07b "Two" -> Nemotron "too";
    # s04 "Claude" -> whisper "Claude's".
    "passed": "past", "too": "two", "claudes": "claude",
}
# Tokens that expand to several tokens (both sides). "ahead": s09 "it had got wrong" -> Nemotron "ahead got
# wrong" on the unchanged clip, where faster-whisper heard "it had".
EXPAND = {"gpt": ["g", "p", "t"], "gpt6": ["g", "p", "t", "six"], "ahead": ["it", "had"]}

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def int_words(n):
    """0..999999 in words, without 'and' (the comparison drops 'and' after 'hundred' on both sides)."""
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000:
        return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + int_words(n % 100))
    return int_words(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + int_words(n % 1000))


def num_words(m):
    s = m.group(0).replace(",", "")
    if "." in s:
        a, b = s.split(".", 1)
        return f" {int_words(int(a or 0))} point {' '.join(ONES[int(d)] for d in b)} "
    return f" {int_words(int(s))} "


def norm(text):
    """Text -> list of canonical tokens."""
    s = text.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"(?<![\w.])[-−–]\s?(?=\d)", " minus ", s)      # -0.16 -> minus 0.16
    s = re.sub(r"\+\s?(?=\d)", " plus ", s)
    s = re.sub(r"(?<=[a-z])-(?=\d)", "", s)                     # gpt-6 -> gpt6
    s = re.sub(r"\d+(?:,\d{3})*(?:\.\d+)?", num_words, s)
    s = s.replace("'", "")                                     # dana's -> danas, voices' -> voices
    s = re.sub(r"[^a-z0-9 ]+", " ", s)                         # hyphens and punctuation -> space
    out = []
    for tok in s.split():
        tok = EQUIV.get(tok, tok)
        if tok in EXPAND:
            out.extend(EXPAND[tok])
        elif re.fullmatch(r"[a-z]+\d+", tok):                  # e.g. gpt6 written without hyphen
            head, d = re.match(r"([a-z]+)(\d+)", tok).groups()
            out.extend(EXPAND.get(head, [head]) + int_words(int(d)).split())
        else:
            out.append(tok)
    # "one hundred and five" == "one hundred five"
    return [t for i, t in enumerate(out) if not (t == "and" and i > 0 and out[i - 1] == "hundred")]


def last_sentence(text):
    parts = [p for p in re.split(r"(?<=[.?!])\s+", text.strip()) if p.strip()]
    return parts[-1] if parts else text


def compare(spoken, heard):
    """{'pass', 'reasons', 'diff', 'extra_words'} for one transcript against the spoken script text."""
    ref, hyp = norm(spoken), norm(heard)
    sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
    missing, extra, diff = [], [], []
    matched = [False] * len(ref)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for i in range(i1, i2):
                matched[i] = True
            continue
        if op in ("delete", "replace"):
            missing.extend(ref[i1:i2])
        if op in ("insert", "replace"):
            extra.extend(hyp[j1:j2])
        diff.append(f"{op}: script [{' '.join(ref[i1:i2])}] heard [{' '.join(hyp[j1:j2])}]")
    n_last = len(norm(last_sentence(spoken)))
    tail_ok = all(matched[len(ref) - n_last:]) if n_last else True
    reasons = []
    if missing:
        reasons.append(f"missing script words: {' '.join(missing)}")
    if not tail_ok:
        reasons.append("transcript does not contain the whole last sentence")
    if "luck at" in " ".join(hyp):
        reasons.append('"luck at" heard')
    return {"pass": not reasons, "reasons": reasons, "diff": diff, "extra_words": extra, "heard": heard}


# ---------------------------------------------------------------- engine 1: faster-whisper

def decode16k(path):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def load_whisper():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    from faster_whisper import WhisperModel
    try:
        return WhisperModel(WHISPER_MODEL, device="cuda", compute_type="float16", local_files_only=True), \
            "cuda float16"
    except Exception as e:  # no GPU or no CUDA libraries
        print(f"cuda failed ({type(e).__name__}: {e}); using cpu int8")
        return WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8", local_files_only=True), "cpu int8"


def whisper_transcribe(model, path):
    segs, info = model.transcribe(decode16k(path), language="en", beam_size=5, word_timestamps=True,
                                  condition_on_previous_text=False)
    segs = list(segs)
    heard = " ".join(s.text.strip() for s in segs)
    words = [(w.word.strip(), round(w.start, 2), round(w.end, 2), round(w.probability, 2))
             for s in segs for w in (s.words or [])]
    return heard, words, round(info.duration, 2)


# ---------------------------------------------------------------- engine 2: Nemotron (nemo-speech CLI)

def nemo_transcribe_all(clips):
    """{pid: transcript} for {pid: wav path}; one nemo-speech run over a temporary directory of 16 kHz PCM WAVs."""
    if not NEMO_EXE.exists() or not NEMO_MODEL.exists():
        raise SystemExit(f"nemo-speech or its model is missing ({NEMO_EXE.exists()=}, {NEMO_MODEL.exists()=})")
    with tempfile.TemporaryDirectory(prefix="asr_nemo_") as tmp:
        src, out = Path(tmp) / "in", Path(tmp) / "out"
        src.mkdir()
        for pid, p in clips.items():
            subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-i", str(p), "-ac", "1", "-ar", "16000", "-c:a",
                            "pcm_s16le", str(src / f"{pid}.wav")], check=True)
        r = subprocess.run([str(NEMO_EXE), "--quiet", "transcribe", str(src), "--model", str(NEMO_MODEL),
                            "--language", "en", "--output-dir", str(out), "--force"], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"nemo-speech failed ({r.returncode}): {r.stderr[-800:]}")
        res = {}
        for pid in clips:
            hits = list(out.rglob(f"{pid}.txt")) + list(out.rglob(f"{pid}.wav.txt"))
            res[pid] = hits[0].read_text(encoding="utf-8").strip() if hits else None
        return res


# ---------------------------------------------------------------- main

def main(argv):
    only = set(argv)
    items = [it for it in S.all_parts() if not only or it[1] in only]
    if only - {it[1] for it in items}:
        raise SystemExit(f"unknown parts: {sorted(only - {it[1] for it in items})}")
    clips, missing = {}, []
    for num, pid, written, spoken in items:
        path, _ = tts.find_cached(pid, spoken)
        if path is None:
            missing.append(pid)
        else:
            clips[pid] = path
    print(f"engines: faster-whisper ({WHISPER_MODEL}) and Nemotron ({NEMO_MODEL.name}); {len(items)} parts")
    nemo = nemo_transcribe_all(clips) if clips else {}
    model, dev = load_whisper()
    print(f"faster-whisper on {dev}")
    results = json.loads(OUT_JSON.read_text(encoding="utf-8")) if OUT_JSON.exists() else {}
    fails = 0
    for num, pid, written, spoken in items:
        if pid in missing:
            print(f"{pid}: FAIL (no cached clip)")
            fails += 1
            continue
        path = clips[pid]
        heard_w, words, dur = whisper_transcribe(model, path)
        rw = compare(spoken, heard_w)
        rn = compare(spoken, nemo[pid]) if nemo.get(pid) is not None else \
            {"pass": False, "reasons": ["no Nemotron transcript"], "diff": [], "extra_words": [], "heard": None}
        ok = rw["pass"] and rn["pass"]
        fails += not ok
        results[pid] = {"file": path.name, "pass": ok, "duration": dur,
                        "last_word_end": words[-1][2] if words else 0.0, "whisper": rw, "nemotron": rn,
                        "whisper_words": words}
        print(f"{pid}: {'PASS' if ok else 'FAIL'}  ({path.name}, {dur} s, last word ends "
              f"{results[pid]['last_word_end']} s)")
        for name, r in (("whisper ", rw), ("nemotron", rn)):
            print(f"   {name} {'pass' if r['pass'] else 'FAIL'}: {r['heard']}")
            for d in r["diff"]:
                print(f"      {d}")
            for why in r["reasons"]:
                print(f"      -> {why}")
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(items) - fails} passed, {fails} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
