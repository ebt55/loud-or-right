"""One-command build of the explainer video.

    python paper/video/src/build.py            voice-over from cache (dry run if missing), SRT, audio, video, QC
    python paper/video/src/build.py --tts      also generate missing voice-over clips (OpenAI TTS; costs cents)
    python paper/video/src/build.py --no-video audio, SRT and timing only

Outputs in paper/video/: loud-or-right-explainer.mp4, loud-or-right-explainer.srt; intermediates in
paper/video/build/ (including qc/ with one frame per scene and a contact sheet).
"""
import argparse
import json
import subprocess
import sys
import time

sys.dont_write_bytecode = True

import audio as A  # noqa: E402
import config as C  # noqa: E402
import timeline as T  # noqa: E402

OUT_MP4 = C.VIDEO / "loud-or-right-explainer.mp4"
OUT_SRT = C.VIDEO / "loud-or-right-explainer.srt"


def build_audio(tl, out_wav):
    placements = []
    for sc in tl.scenes:
        for pid, off in sc["parts"]:
            pt = tl.parts[pid]
            placements.append((sc["start"] + off, pt.samples))
    raw = C.BUILD / "voice_raw.wav"
    A.master(placements, tl.total_frames / C.FPS, raw)
    js = A.loudnorm(raw, out_wav)
    return js


def ffprobe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=index,codec_type,codec_name,width,height,r_frame_rate,pix_fmt,duration,sample_rate,"
                        "channels,color_space,color_primaries,color_transfer:format=duration",
                        "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tts", action="store_true")
    ap.add_argument("--no-video", action="store_true")
    ap.add_argument("--workers", type=int, default=None)
    a = ap.parse_args()
    C.BUILD.mkdir(parents=True, exist_ok=True)
    import tts
    tts.run(go=a.tts)
    tl = T.Timeline(T.load_parts())
    print(tl.summary())
    main_len = sum(s["dur"] for s in tl.scenes[:-1])
    if main_len < C.MIN_TOTAL:
        print(f"WARNING: scenes 1-10 run {main_len:.2f} s, {C.MIN_TOTAL - main_len:.2f} s short of 3:00")
    if not (C.TARGET[0] <= tl.total <= C.TARGET[1]):
        print(f"NOTE: total {tl.total:.2f} s is outside the 3:10-3:30 target")
    cues = T.write_srt(tl, OUT_SRT)
    print(f"wrote {OUT_SRT.name}: {len(cues)} captions")
    wav = C.BUILD / "voice_norm.wav"
    js = build_audio(tl, wav)
    print(f"audio: input {js['input_i']} LUFS -> normalised (target -16)")
    if a.no_video:
        return
    import render
    t0 = time.time()
    stats = render.render_video(C.BUILD / "video_only.mp4", workers=a.workers)
    render.mux(C.BUILD / "video_only.mp4", wav, OUT_MP4)
    print(f"video built in {time.time() - t0:.0f} s -> {OUT_MP4}")
    (C.BUILD / "render_stats.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
    info = ffprobe(OUT_MP4)
    print(json.dumps(info, indent=1))
    print("loudness (integrated LUFS, true peak dBFS):", A.ebur128(OUT_MP4))


if __name__ == "__main__":
    main()
