# Loud or Right? Explainer video

- `loud-or-right-explainer.mp4`: 1920×1080, 30 fps, H.264 (yuv420p, BT.709), AAC 48 kHz, loudness −16 LUFS, length 3:33.7 (scenes 1–10: 3:29.7). This is 3.7 s over the plan's 3:10–3:30 target, after the 16 Nov media-review fixes lengthened scenes 4, 7, 8 and 10.
- `loud-or-right-explainer.srt`: captions in the script's written form, timed to the voice-over.
- `script.md` (voice-over) and `plan.md` (storyboard) are the inputs. The build scripts are in `src/`.

## Rebuild

From the project root, with system Python (Pillow, numpy, matplotlib) and ffmpeg on PATH:

```
python paper/video/src/build.py          # voice-over from cache, captions, audio, video (about 1.5 min on 20 cores)
python paper/video/src/qc.py             # frames from the MP4 into paper/video/build/qc/, length/sync/loudness checks
```

On a cold cache (`paper/video/build/tts_cache/` missing), add `--tts` to the build. This regenerates the voice-over through the OpenAI API, with one request per scene, and scene 7 is split in two at "Then we shuffled the order.", so there are 12 requests. The key is read from the project `.env` and never printed. `python paper/video/src/tts.py` on its own is a dry run that makes no API call.

After any regeneration, run `python paper/video/src/asr_check.py`. It transcribes every clip with two local engines, faster-whisper and NVIDIA Nemotron (through a local `nemo-speech` CLI; set `NEMO_SPEECH_EXE` and `NEMO_SPEECH_MODEL`, or put them in `paper/video/asr_local.env`, which is not committed), and compares each transcript with the script. It fails a clip if any word is missing, and exits nonzero.

## Voice-over

- **Voice:** OpenAI `gpt-4o-mini-tts`, voice `nova`, with a calm, conversational style instruction at about 160 words per minute.
- **Reading notes:** the script's notes (for example "G P T six Saul" and "zero point five nine") are applied only to the text sent to text-to-speech. The captions keep the written form.
- **Length:** 3,205 spoken characters, giving 202 s of audio.
- **Approximate cost:** about $0.05 for the first full voice-over, at roughly $0.015 per minute of audio for `gpt-4o-mini-tts`. Re-voicing scenes 4, 6, 7b, 8 and 10 on 16 Nov added about $0.05, including five discarded takes (four of scene 4, one of scene 10). Scene 4 now reads "GPT-6 Sol" as "G P T six Saul", as scene 9 already sounds it; read as "Sol", it was heard as "salt".
- **Superseded takes:** kept in `build/tts_cache/old/`.

## Notes

- **Scene timing** follows the measured audio: a 0.1 s lead, then the clip, then a 0.6 s tail. There are three exceptions:
  - scene 1 opens with a 1.8 s silent title card;
  - scene 4 holds 0.8 s longer, so its caveat chip can be read;
  - the credits are one still screen held 4 s.
- **Cue timing:** animation cues come from a character-weighted model of each clip, anchored to the pauses detected in the audio. The build does not transcribe. One manual hint (`SENT_HINT` in `timeline.py`) corrects three sentence anchors in scene 4, checked against Whisper word times.
- **Scatter data:**
  - arm A comes from `paper/figs/tables.md`, Table 7;
  - arm R comes from `harness_x/analysis/arm_r_vs_a.md`, section 1;
  - arm S comes from `harness_x/analysis/arm_s.md`, section 1;
  - the order-balanced gap strip uses the D_bal values in section 2 of `arm_s.md`.

  `src/data.py` lists the source of each value.
- **Intermediate files** are in `paper/video/build/`; it can be deleted, except `tts_cache/`, which avoids paying for the voice again.
