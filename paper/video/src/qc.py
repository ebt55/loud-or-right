"""Quality check of the finished MP4.

    python paper/video/src/qc.py

- extracts one frame per scene (1.0 s before the scene ends, when all its elements are on screen) plus extra
  frames for the multi-state scenes, from the encoded MP4 with ffmpeg -ss, into build/qc/, with a contact sheet;
- checks the lengths (total, scenes 1-10 >= 3:00, video vs audio stream), loudness, and the credits screen;
- writes build/qc/report.json.
"""
import json
import subprocess
import sys

sys.dont_write_bytecode = True

import audio as A  # noqa: E402
import components as K  # noqa: E402
import config as C  # noqa: E402
import render  # noqa: E402
import timeline as T  # noqa: E402

MP4 = C.VIDEO / "loud-or-right-explainer.mp4"
QC = C.BUILD / "qc"

# extra frames: (scene, phrase or None, offset seconds after the phrase)
EXTRA = [(1, None, 1.0), (5, "credit only the confident voice", 1.0), (7, "from plus 0.59 to minus 0.16", 1.2),
         (7, "the gaps shrank.", 0.8), (8, "followed an unsure objection far more", 2.0),
         (8, "every open-weight model followed", 2.0), (9, "105 of 160", 1.2), (9, "8 of 160", 1.0),
         (9, "But there Dana named the correct answer", 1.0), (6, "Otherwise it opened with", 1.2)]


def grab(t, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(MP4), "-frames:v", "1", str(out)],
                   check=True)


def main():
    QC.mkdir(parents=True, exist_ok=True)
    tl = T.Timeline(T.load_parts())
    shots = []
    for sc in tl.scenes:
        t = sc["start"] + sc["dur"] - 1.0
        shots.append((t, f"scene {sc['num']:02d} end", QC / f"scene_{sc['num']:02d}.png"))
    for num, phrase, off in EXTRA:
        sc = tl.scene(num)
        lt = (tl.cue(num, phrase) if phrase else 0.0) + off
        shots.append((sc["start"] + lt, f"scene {num:02d} '{(phrase or 'start')[:22]}'",
                      QC / f"scene_{num:02d}_{int(lt * 10):04d}.png"))
    shots.sort()
    for t, cap, out in shots:
        grab(t, out)
    render.contact_sheet([(out, f"{t:6.2f}s {cap}") for t, cap, out in shots], QC / "_sheet.png", cols=4)
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration",
                                      "-of", "json", str(MP4)], capture_output=True, text=True).stdout)
    durs = {s["codec_type"]: float(s["duration"]) for s in info["streams"]}
    main_len = sum(s["dur"] for s in tl.scenes[:-1])
    lufs, peak = A.ebur128(MP4)
    credits = tl.scenes[-1]
    blocks = K.credits_plain(K.parse_credits())
    rep = {
        "total_s": round(tl.total, 3), "scenes_1_10_s": round(main_len, 3), "video_s": durs.get("video"),
        "audio_s": durs.get("audio"), "av_diff_s": round(abs(durs.get("video", 0) - durs.get("audio", 0)), 3),
        "lufs": lufs, "true_peak_dbfs": peak, "credits_screen_s": round(credits["dur"], 3),
        "credits_lines": sum(len(v) for v in blocks.values()),
        "checks": {
            "total >= 3:00": tl.total >= 180, "scenes 1-10 >= 3:00": main_len >= 180,
            "3:10 <= total <= 3:30": 190 <= tl.total <= 210, "audio = video (+-50 ms)":
                abs(durs.get("video", 0) - durs.get("audio", 0)) < 0.05,
            "loudness -16 +-1 LUFS": lufs is not None and abs(lufs + 16) <= 1.0,
            "every scene's visuals end after its audio": all(
                sc["dur"] >= sc["parts"][-1][1] + tl.parts[sc["parts"][-1][0]].dur - 1e-6 for sc in tl.scenes),
        },
        "frames": [str(o.name) for _, _, o in shots],
    }
    (QC / "report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
