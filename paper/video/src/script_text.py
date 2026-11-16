"""Reads the voice-over verbatim from paper/video/script.md and derives the text sent to text-to-speech.

The written form (script.md, captions) never changes. The spoken form applies only the script's reading notes
(e.g. "GPT-6 Sol" -> "G P T six Saul") and is used only in the TTS request.
"""
import re

import config as C

SCRIPT = C.VIDEO / "script.md"

# The script's "Reading notes for text-to-speech", in order (longest first where they overlap).
SPOKEN = [
    ("GPT-6 Sol", "G P T six Saul"),   # "Saul", as scene 9 says "Sol"; "Sol" was heard as "salt" in s04
    ("Claude Sonnet 5.5", "Claude Sonnet five point five"),
    ("Llama 3.3", "Llama three point three"),
    ("plus 0.59", "plus zero point five nine"),
    ("minus 0.16", "minus zero point one six"),
    ("105 of 160", "one hundred and five of one hundred and sixty"),
    ("8 of 160", "eight of one hundred and sixty"),
]

# Scenes whose audio is generated in parts, split before the given sentence (plan.md, scene 7).
SPLITS = {7: "Then we shuffled the order."}


def scenes(path=SCRIPT):
    """[(number, title, vo)] in order. vo is the paragraph after '**VO.**', exactly as written."""
    txt = path.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"^## Scene (\d+): (.+?)\s*$", txt, re.M):
        num, title = int(m.group(1)), m.group(2).strip()
        body = txt[m.end():]
        nxt = re.search(r"^## ", body, re.M)
        body = body[:nxt.start()] if nxt else body
        vm = re.search(r"\*\*VO\.\*\*\s*(.+)", body)
        if not vm:
            raise ValueError(f"scene {num}: no **VO.** paragraph")
        out.append((num, title, vm.group(1).strip()))
    if [n for n, _, _ in out] != list(range(1, len(out) + 1)):
        raise ValueError("scene numbers are not 1..N in order")
    return out


def spoken(text):
    s = text
    for a, b in SPOKEN:
        s = s.replace(a, b)
    return s


def parts(num, vo):
    """[(part id, written text)] for one scene: one part, or two when the scene is split."""
    key = SPLITS.get(num)
    if not key:
        return [(f"s{num:02d}", vo)]
    i = vo.index(key)
    return [(f"s{num:02d}a", vo[:i].strip()), (f"s{num:02d}b", vo[i:].strip())]


def all_parts(path=SCRIPT):
    """[(scene number, part id, written text, spoken text)]."""
    out = []
    for num, _, vo in scenes(path):
        for pid, w in parts(num, vo):
            out.append((num, pid, w, spoken(w)))
    return out


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9.'’-]*", text))


if __name__ == "__main__":
    total = 0
    for num, pid, w, sp in all_parts():
        n = word_count(w)
        total += n
        print(f"{pid}: {n} words")
    print("total words:", total)
