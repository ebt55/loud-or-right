"""Audio helpers: decode and measure clips with ffmpeg, find pauses, build the master track at exact sample
offsets, two-pass loudness normalisation to -16 LUFS, and an EBU R128 check. Test placeholders are numpy tones.
"""
import json
import re
import subprocess
import wave

import numpy as np

import config as C


def decode(path, sr=C.SR, tempo=1.0):
    """Mono float32 samples at sr (decoded by ffmpeg; never trust a WAV header). tempo != 1 time-stretches
    with ffmpeg's atempo (pitch kept)."""
    af = ["-af", f"atempo={tempo:.5f}"] if abs(tempo - 1) > 1e-4 else []
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), *af, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def duration(path, tempo=1.0):
    return len(decode(path, tempo=tempo)) / C.SR


def speech_span(x, sr=C.SR, thresh_db=-40.0):
    """(start, end) seconds of the non-silent part of a clip."""
    win = int(sr * 0.01)
    n = len(x) // win
    if n == 0:
        return 0.0, len(x) / sr
    rms = np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    on = np.where(db > thresh_db)[0]
    if len(on) == 0:
        return 0.0, len(x) / sr
    return on[0] * win / sr, (on[-1] + 1) * win / sr


def pauses(x, sr=C.SR, thresh_db=-38.0, min_len=0.16):
    """[(start, end)] of pauses inside the speech (seconds), from a 10 ms RMS envelope."""
    win = int(sr * 0.01)
    n = len(x) // win
    rms = np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    quiet = 20 * np.log10(rms) < thresh_db
    s0, s1 = speech_span(x, sr)
    out, start = [], None
    for i, q in enumerate(quiet):
        t = i * win / sr
        if q and start is None:
            start = t
        elif not q and start is not None:
            if t - start >= min_len and start > s0 and t < s1:
                out.append((start, t))
            start = None
    return out


def write_wav(path, x, sr=C.SR):
    y = np.clip(x, -1, 1)
    pcm = (y * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def master(placements, total_seconds, out_path, sr=C.SR):
    """placements: [(start seconds, samples)]. Starts are rounded to whole samples; the track is exactly
    total_seconds long (frames / fps), so audio and video lengths match."""
    n = int(round(total_seconds * sr))
    track = np.zeros(n, dtype=np.float32)
    for start, x in placements:
        i = int(round(start * sr))
        j = min(n, i + len(x))
        if j - i < len(x):
            raise ValueError(f"clip at {start:.2f}s overruns the track by {(len(x) - (j - i)) / sr:.2f}s")
        track[i:j] += x[: j - i]
    write_wav(out_path, track, sr)
    return out_path


def loudnorm(in_path, out_path, target=-16.0, tp=-1.5, lra=11.0):
    """Two-pass EBU R128 normalisation (ffmpeg loudnorm), output 48 kHz mono PCM."""
    first = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(in_path), "-af",
                            f"loudnorm=I={target}:TP={tp}:LRA={lra}:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", first.stderr, re.S)
    if not m:
        raise RuntimeError("loudnorm pass 1 printed no measurements")
    js = json.loads(m.group(0))
    af = (f"loudnorm=I={target}:TP={tp}:LRA={lra}:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:"
          f"linear=true:print_format=summary")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(in_path), "-af", af, "-ar", str(C.SR), "-ac", "1",
                    "-c:a", "pcm_s16le", str(out_path)], check=True)
    return js


def ebur128(path):
    """Integrated loudness (LUFS) and true peak of a file, measured by ffmpeg's ebur128 filter."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a", "-af",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    p = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return (float(i.group(1)) if i else None, float(p.group(1)) if p else None)


def tone_placeholder(seconds, sentences=1, sr=C.SR, freq=220.0):
    """Test stand-in for a voice clip: soft tone bursts separated by 0.3 s gaps (one burst per sentence)."""
    n = int(seconds * sr)
    x = np.zeros(n, dtype=np.float32)
    seg = (seconds - 0.3 * (sentences - 1)) / sentences
    t0 = 0.0
    for k in range(sentences):
        i, j = int(t0 * sr), int((t0 + seg) * sr)
        tt = np.arange(j - i) / sr
        env = np.minimum(1, np.minimum(tt / 0.02, (seg - tt) / 0.02))
        x[i:j] = 0.2 * np.sin(2 * np.pi * freq * tt) * env
        t0 += seg + 0.3
    return x
