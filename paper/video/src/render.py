"""Frame rendering and ffmpeg assembly.

    python render.py stills [t1 t2 ...]     PNG stills at global times (default: cue points of every scene) + sheet
    python render.py video [--workers N]    full render: parallel segments -> concat -> mux with the master audio

Workers are spawned processes (Windows); each rebuilds the timeline and scenes from the cached audio, renders a
contiguous range of frames, and pipes raw RGB to its own ffmpeg (libx264, yuv420p, bt709).
"""
import json
import multiprocessing as mp
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True

from PIL import Image  # noqa: E402

import config as C  # noqa: E402
import gfx as G  # noqa: E402
from easing import prog  # noqa: E402

_STATE = None


def build_state():
    import scenes as S
    import timeline as T
    tl = T.Timeline(T.load_parts())
    return tl, S.build(tl)


def _init():
    global _STATE
    _STATE = build_state()


def scene_at(tl, i):
    acc = 0
    for k, sc in enumerate(tl.scenes):
        if i < acc + sc["frames"]:
            return k, (i - acc) / C.FPS
        acc += sc["frames"]
    return len(tl.scenes) - 1, tl.scenes[-1]["dur"] - 1e-6


_BG = None


def bg_img():
    global _BG
    if _BG is None:
        _BG = Image.new("RGB", (C.W, C.H), tuple(C.BG[:3]))
    return _BG


def frame(i, state=None, strict=False):
    """Render global frame i; returns (canvas, scene number, local t)."""
    import components as K
    tl, scs = state or _STATE
    k, t = scene_at(tl, i)
    sc = scs[k]
    a_in = prog(t, 0.0, sc.fade_in, lambda v: v) if sc.fade_in else 1.0
    a_out = 1.0 - prog(t, sc.dur - sc.fade_out, sc.fade_out, lambda v: v) if sc.fade_out else 1.0
    a = min(a_in, a_out)
    cv = G.Canvas(strict=strict)
    if sc.exit_move and a_out < 1:
        layer = G.Canvas(bg=None, strict=strict)
        sc.draw(layer, t)
        p = 1 - a_out
        dx, s = sc.exit_move
        img = layer.img
        if abs(s - 1) > 1e-3:
            sc_ = 1 + (s - 1) * p
            img = img.resize((int(C.W * sc_), int(C.H * sc_)), Image.BILINEAR)
            ox, oy = (C.W - img.size[0]) / 2 + dx * p, (C.H - img.size[1]) / 2
        else:
            ox, oy = dx * p, 0
        img.info["words"] = 0
        cv.paste(img, ox, oy, a_out, check_safe=False)
        cv.words = layer.words
        cv.safe_violations += layer.safe_violations
    else:
        sc.draw(cv, t)
        if a < 1:
            cv.img = Image.blend(bg_img(), cv.img, a)
    # persistent overlays
    prev_sc = scs[k - 1] if k > 0 else None
    next_sc = scs[k + 1] if k + 1 < len(scs) else None
    if sc.wordmark:
        wa = 1.0
        if next_sc is not None and not next_sc.wordmark:
            wa *= a_out
        K.wordmark(cv, wa)
    la = sc.legend_alpha(t)
    if la > 0:
        if next_sc is None or not next_sc.legend:
            la *= a_out
        if prev_sc is None or not prev_sc.legend:
            la *= a_in
        K.legend(cv, la)
    return cv, sc.num, t


# ---------------------------------------------------------------- stills

def stills(times=None, out_dir=C.BUILD / "stills", sheet=True, strict=True):
    state = build_state()
    tl, scs = state
    out_dir.mkdir(parents=True, exist_ok=True)
    if not times:
        times = default_times(tl, scs)
    paths, report = [], []
    for gt in times:
        i = min(tl.total_frames - 1, int(round(gt * C.FPS)))
        cv, num, t = frame(i, state, strict=strict)
        p = out_dir / f"f{i:05d}_s{num:02d}.png"
        cv.img.convert("RGB").save(p)
        paths.append((p, f"{gt:6.2f}s  scene {num}  t={t:5.2f}  words={cv.words}"))
        report.append((gt, num, t, cv.words, list(cv.safe_violations)))
    if sheet:
        contact_sheet(paths, out_dir / "_sheet.png")
    return paths, report


def default_times(tl, scs):
    """A few times per scene: just after each cue the scene uses, and near the end."""
    out = []
    for sc_obj, sc in zip(scs, tl.scenes):
        cues = sorted({v for k, v in vars(sc_obj).items() if k.startswith("t_") and isinstance(v, (int, float))})
        local = [min(sc["dur"] - 0.05, c + 1.0) for c in cues] + [sc["dur"] - 0.7]
        for lt in sorted(set(round(x, 2) for x in local)):
            out.append(sc["start"] + lt)
    return out


def contact_sheet(paths, out, cols=4, tw=480):
    th = int(tw * C.H / C.W)
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 26)), (40, 40, 40))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    f = G.font("regular", 18)
    for n, (p, cap) in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = (n % cols) * tw, (n // cols) * (th + 26)
        sheet.paste(im, (x, y + 26))
        d.text((x + 6, y + 3), cap, font=f, fill=(255, 255, 255))
    sheet.save(out)
    return out


# ---------------------------------------------------------------- video

FFMPEG_V = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
            "-g", str(C.FPS * 2), "-bf", "2"]


def render_chunk(args):
    a, b, out_path = args
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{C.W}x{C.H}",
           "-r", str(C.FPS), "-i", "-", *FFMPEG_V, "-threads", "2", str(out_path)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    stats = {}
    for i in range(a, b):
        cv, num, t = frame(i)
        s = stats.setdefault(num, {"max_words": 0, "at": 0.0, "violations": set()})
        if cv.words > s["max_words"]:
            s["max_words"], s["at"] = cv.words, round(t, 2)
        s["violations"].update(v.split(" at (")[0] for v in cv.safe_violations)
        proc.stdin.write(cv.img.convert("RGB").tobytes())
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed for frames {a}-{b}")
    for s in stats.values():
        s["violations"] = sorted(s["violations"])
    return stats


def render_video(out_video, workers=None, frame_range=None):
    tl, _ = build_state()
    n = tl.total_frames
    a0, b0 = frame_range or (0, n)
    workers = workers or max(1, min(20, (os.cpu_count() or 4) - 2))
    seg_dir = C.BUILD / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    for f in seg_dir.glob("seg_*.mp4"):
        f.unlink()
    # contiguous chunks; segment boundaries on whole GOPs are not required (each segment starts with an IDR)
    step = (b0 - a0 + workers - 1) // workers
    chunks = [(a, min(b0, a + step), seg_dir / f"seg_{k:03d}.mp4") for k, a in enumerate(range(a0, b0, step))]
    t0 = time.time()
    ctx = mp.get_context("spawn")
    with ctx.Pool(len(chunks), initializer=_init) as pool:
        results = pool.map(render_chunk, chunks)
    print(f"rendered {b0 - a0} frames in {time.time() - t0:.0f} s with {len(chunks)} workers")
    lst = seg_dir / "list.txt"
    lst.write_text("".join(f"file '{c[2].as_posix()}'\n" for c in chunks), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    str(out_video)], check=True)
    merged = {}
    for r in results:
        for num, s in r.items():
            m = merged.setdefault(num, {"max_words": 0, "at": 0.0, "violations": []})
            if s["max_words"] > m["max_words"]:
                m["max_words"], m["at"] = s["max_words"], s["at"]
            m["violations"] = sorted(set(m["violations"]) | set(s["violations"]))
    return merged


def mux(video, audio_wav, out_path):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio_wav), "-map", "0:v:0",
                    "-map", "1:a:0", "-c:v", "copy",
                    "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
                    "-c:a", "aac", "-b:a", "192k", "-ar", str(C.SR), "-ac", "2",
                    "-movflags", "+faststart", "-shortest", str(out_path)], check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        ts = [float(x) for x in sys.argv[2:]]
        paths, rep = stills(ts or None, strict=False)
        for gt, num, t, w, v in rep:
            print(f"{gt:7.2f} scene {num:2d} t={t:5.2f} words={w}" + (f"  VIOLATIONS {v}" if v else ""))
    elif len(sys.argv) > 1 and sys.argv[1] == "video":
        out = C.BUILD / "video_only.mp4"
        st = render_video(out)
        print(json.dumps(st, indent=1))
