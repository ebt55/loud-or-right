"""Audio-driven timing: scene lengths from the measured clips, phrase cue times inside each clip, and SRT
captions in the written form.

Phrase times come from a character-weighted model of the spoken text, anchored at sentence ends to the pauses
found in the audio (no transcription; no other model calls). Accuracy is about +-0.3 s, enough for rough sync;
CUE_SHIFT holds per-phrase manual corrections.
"""
import json
import re

import audio as A
import config as C
import script_text as S
import tts

# Per-scene timing (seconds). Scene length = LEAD + clip(s) + GAP between parts + TAIL (+ EXTRA hold).
LEAD = 0.10
LEAD_SCENE = {1: 1.8}           # scene 1: the title card is read before the voice starts
TAIL = 0.60
PART_GAP = {7: 0.25}            # scene 7: silence between part a and part b (before "Then we shuffled")
EXTRA_HOLD = {4: 0.8}           # {scene: seconds} extra end-of-scene hold (scene 4: time to read its caveat chip)
CREDITS_LEN = 4.0               # scene 11: one still screen, 4 s
CUE_SHIFT = {}                  # {(scene, phrase): seconds} manual corrections
# {part id: {sentence-end index: seconds}}: manual estimate of a sentence end, used instead of the character model
# when choosing its pause. Tuned to the s04 take voiced on 16 Nov with "G P T six Saul" (18.5 s): unaided, the model
# put the first three sentence ends on the next clause pause, so "Further up", "On the diagonal" and "Claude Sonnet"
# ran 0.8-1.0 s late. Whisper word ends: "good." 4.70, "voice." 7.12, "equally." 10.56; pauses start 4.28, 7.18, 10.62.
SENT_HINT = {"s04": {0: 4.3, 1: 7.2, 2: 10.65}}

# Weights for the character model (relative speaking time).
W_CHAR, W_SPACE, W_COMMA, W_STOP = 1.0, 0.6, 3.0, 2.0


def _weights(spoken):
    w = []
    for i, ch in enumerate(spoken):
        if ch in ".?!":
            w.append(W_STOP if (i + 1 == len(spoken) or spoken[i + 1] == " ") else W_CHAR * 0.3)
        elif ch in ",:;":
            w.append(W_COMMA)
        elif ch == " ":
            w.append(W_SPACE)
        else:
            w.append(W_CHAR)
    return w


def _sentence_ends(spoken):
    return [m.end() for m in re.finditer(r"[.?!](?=\s|$)", spoken)][:-1]


class PartTiming:
    """Timing model of one clip: char index (spoken text) -> seconds from the clip start."""

    def __init__(self, pid, written, spoken, samples):
        self.pid, self.written, self.spoken = pid, written, spoken
        self.samples = samples
        self.dur = len(samples) / C.SR
        s0, s1 = A.speech_span(samples)
        self.span = (s0, s1)
        self.pauses = A.pauses(samples)
        w = _weights(spoken)
        self.cum = [0.0]
        for x in w:
            self.cum.append(self.cum[-1] + x)
        total = self.cum[-1]
        est = lambda idx: s0 + (s1 - s0) * self.cum[idx] / total
        anchors = [(0, s0)]
        used = set()
        for k_s, idx in enumerate(_sentence_ends(spoken)):
            te = SENT_HINT.get(pid, {}).get(k_s, est(idx))
            best = None
            for k, (p0, p1) in enumerate(self.pauses):
                if k in used or p0 <= anchors[-1][1]:
                    continue
                d = abs(p0 - te)
                if d < 1.4 and (best is None or (p1 - p0) - 0.4 * d > best[0]):
                    best = ((p1 - p0) - 0.4 * d, k, p0, p1)
            if best:
                used.add(best[1])
                anchors.append((idx, best[2]))
                anchors.append((idx + 1, best[3]))   # the next word starts at the end of the pause
        anchors.append((len(spoken), s1))
        anchors.sort()
        self.anchors = anchors
        # second pass: clause breaks (, : ;) anchored to pauses not used by sentence ends
        cum_ok = True
        for m in re.finditer(r"[,:;](?=\s)", spoken):
            idx = m.end()
            te = self._interp(anchors, idx)
            best = None
            for k, (p0, p1) in enumerate(self.pauses):
                if k in used:
                    continue
                d = abs(p0 - te)
                if d < 0.6 and (best is None or d < best[0]):
                    best = (d, k, p0, p1)
            if best:
                used.add(best[1])
                anchors.append((idx, best[2]))
                anchors.append((idx + 1, best[3]))
                anchors.sort()
        # keep anchors monotone
        clean = [anchors[0]]
        for a in anchors[1:]:
            if a[0] >= clean[-1][0] and a[1] >= clean[-1][1]:
                clean.append(a)
        self.anchors = clean

    def _interp(self, anchors, idx):
        for (i0, t0), (i1, t1) in zip(anchors, anchors[1:]):
            if i0 <= idx <= i1:
                if self.cum[i1] == self.cum[i0]:
                    return t0
                return t0 + (t1 - t0) * (self.cum[idx] - self.cum[i0]) / (self.cum[i1] - self.cum[i0])
        return anchors[-1][1]

    def time_at(self, idx):
        for (i0, t0), (i1, t1) in zip(self.anchors, self.anchors[1:]):
            if i0 <= idx <= i1:
                if self.cum[i1] == self.cum[i0]:
                    return t0
                return t0 + (t1 - t0) * (self.cum[idx] - self.cum[i0]) / (self.cum[i1] - self.cum[i0])
        return self.anchors[-1][1]

    def phrase(self, phrase, end=False):
        """Seconds (from clip start) at which the written phrase starts (or ends) being spoken."""
        i = self.written.find(phrase)
        if i < 0:
            raise KeyError(f"{self.pid}: phrase {phrase!r} not in the VO")
        j = i + len(phrase) if end else i
        idx = len(S.spoken(self.written[:j]))
        if not end:
            while idx < len(self.spoken) and self.spoken[idx] == " ":
                idx += 1
        return self.time_at(idx)


def load_parts():
    """{pid: PartTiming} from the cached clips (raises if a clip is missing)."""
    out = {}
    for num, pid, w, sp in S.all_parts():
        p, model = tts.find_cached(pid, sp)
        if p is None:
            raise FileNotFoundError(f"no audio for {pid}; run tts.py --go")
        out[pid] = PartTiming(pid, w, sp, A.decode(p))
        out[pid].model = model
        out[pid].path = p
    return out


def frames(sec):
    return int(round(sec * C.FPS))


class Timeline:
    """Scene starts/lengths in whole frames, part offsets, and cue lookup. Build from load_parts()."""

    def __init__(self, parts):
        self.parts = parts
        self.scenes = []          # dicts: num, title, start (s), dur (s), parts [(pid, offset s within scene)]
        t = 0.0
        for num, title, vo in S.scenes():
            pids = [pid for pid, _ in S.parts(num, vo)]
            off = LEAD_SCENE.get(num, LEAD)
            placed = []
            for k, pid in enumerate(pids):
                placed.append((pid, off))
                off += parts[pid].dur + (PART_GAP.get(num, 0.0) if k < len(pids) - 1 else 0.0)
            if num == len(S.scenes()):   # credits
                dur = max(CREDITS_LEN, off + 0.2)
            else:
                dur = off + TAIL + EXTRA_HOLD.get(num, 0.0)
            nf = frames(dur + 0.0166)   # round up to a whole frame
            dur = nf / C.FPS
            self.scenes.append(dict(num=num, title=title, start=t, dur=dur, frames=nf, parts=placed, vo=vo))
            t += dur
        self.total = t
        self.total_frames = sum(s["frames"] for s in self.scenes)

    def scene(self, num):
        return self.scenes[num - 1]

    def cue(self, num, phrase, end=False):
        """Scene-local seconds at which `phrase` (written form) starts (or ends) in scene `num`'s VO."""
        sc = self.scene(num)
        for pid, off in sc["parts"]:
            pt = self.parts[pid]
            if phrase in pt.written:
                return off + pt.phrase(phrase, end) + CUE_SHIFT.get((num, phrase), 0.0)
        raise KeyError(f"scene {num}: phrase {phrase!r} not found")

    def vo_end(self, num):
        pid, off = self.scene(num)["parts"][-1]
        return off + self.parts[pid].span[1]

    def vo_start(self, num):
        pid, off = self.scene(num)["parts"][0]
        return off + self.parts[pid].span[0]

    def summary(self):
        lines = []
        for s in self.scenes:
            lines.append(f"scene {s['num']:2d} {s['title'][:38]:38s} start {s['start']:7.2f}  dur {s['dur']:6.2f}")
        main = sum(s["dur"] for s in self.scenes[:-1])
        lines.append(f"scenes 1-{len(self.scenes) - 1}: {main:.2f} s; total {self.total:.2f} s "
                     f"({int(self.total // 60)}:{self.total % 60:05.2f}); {self.total_frames} frames")
        return "\n".join(lines)

    def to_dict(self):
        """Picklable description for render workers: scene starts/lengths and every cue the scenes ask for are
        resolved lazily in workers from this same data, so we pass the part timings as plain lists."""
        return {"scenes": self.scenes, "total": self.total, "total_frames": self.total_frames}


# ---------------------------------------------------------------- captions

def _chunks(text, max_chars=84):
    """Split the VO into caption chunks of at most ~2 lines of 42 characters: one chunk per sentence, and long
    sentences cut into balanced pieces at the nearest clause break (comma, colon, semicolon), else a space."""
    # split after . ? ! only when followed by a space (so "5.5", "0.59" and "3.3" stay whole)
    sentences = re.split(r"(?<=[.?!])\s+|(?<=[.?!][\"”])\s+", text)
    out = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        n = -(-len(s) // max_chars)
        if n <= 1:
            out.append(s)
            continue
        cuts, last = [], 0
        for k in range(1, n):
            target = len(s) * k / n
            punct = [m.end() for m in re.finditer(r"[,;:] ", s) if abs(m.end() - target) <= 22 and m.end() > last + 10]
            if punct:
                c = min(punct, key=lambda x: abs(x - target))
            else:
                spaces = [m.end() for m in re.finditer(" ", s) if m.end() > last + 10]
                c = min(spaces, key=lambda x: abs(x - target))
            cuts.append(c)
            last = c
        prev = 0
        for c in cuts + [len(s)]:
            out.append(s[prev:c].strip())
            prev = c
    return out


def _two_lines(s, width=42):
    if len(s) <= width:
        return s
    best = None
    for m in re.finditer(" ", s):
        i = m.start()
        score = max(i, len(s) - i - 1)
        if best is None or score < best[0]:
            best = (score, i)
    return s[:best[1]] + "\n" + s[best[1] + 1:]


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(tl, path):
    """Captions in the written form, timed by the same model as the cues."""
    cues = []
    for sc in tl.scenes:
        for pid, off in sc["parts"]:
            pt = tl.parts[pid]
            pos = 0
            for ch in _chunks(pt.written):
                i = pt.written.find(ch, pos)
                pos = i + len(ch)
                t0 = sc["start"] + off + pt.phrase(ch)
                t1 = sc["start"] + off + pt.phrase(ch, end=True)
                cues.append([t0, t1 + 0.25, _two_lines(ch)])
    for k in range(len(cues)):
        if k + 1 < len(cues):
            cues[k][1] = min(cues[k][1], cues[k + 1][0] - 0.05)
        cues[k][1] = max(cues[k][1], cues[k][0] + 0.9)
        if k + 1 < len(cues) and cues[k][1] > cues[k + 1][0] - 0.02:
            cues[k][1] = cues[k + 1][0] - 0.02
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for k, (t0, t1, txt) in enumerate(cues, 1):
            f.write(f"{k}\n{srt_time(t0)} --> {srt_time(t1)}\n{txt}\n\n")
    return cues


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    parts = load_parts()
    for pid, pt in parts.items():
        print(pid, f"dur {pt.dur:.2f} span {pt.span[0]:.2f}-{pt.span[1]:.2f}",
              "pauses", [(round(a, 2), round(b - a, 2)) for a, b in pt.pauses])
        print("   anchors", [(i, round(t, 2)) for i, t in pt.anchors])
    tl = Timeline(parts)
    print(tl.summary())
