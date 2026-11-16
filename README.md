# Loud or Right? How Language Models Weigh a Critic's Confidence, Its Track Record, and the Order of the Evidence

Code, data and analysis for a submission to the Apart Research **AI x Epistemics Research Sprint** (November 2026).

**Author:** Ebin Babu Thomas, Independent AI Engineer & Researcher.

**Report:** [`paper/report.pdf`](paper/report.pdf). Its source is [`paper/report.md`](paper/report.md).

**Explainer video (3:34):** [`paper/video/loud-or-right-explainer.mp4`](paper/video/loud-or-right-explainer.mp4), with captions in [`loud-or-right-explainer.srt`](paper/video/loud-or-right-explainer.srt).

https://github.com/user-attachments/assets/47c0b10b-2412-48b4-931e-44024d78b8e1

**Slides:** [`paper/slides/loud-or-right-slides.pdf`](paper/slides/loud-or-right-slides.pdf) (editable: [`.pptx`](paper/slides/loud-or-right-slides.pptx)).

## What the study does

A model answers a six- to ten-option multiple-choice question (MMLU-Pro). A scripted reviewer then objects to its answer, with certainty ("I am certain") or with doubt ("I think ..., but I am not sure"). Before the objection, the model sees a practice log of the reviewer's past objections, in which the reviewer's record differs by expressed confidence: right only when certain, only when unsure, or always.

Across 15 models:
- **Sonnet and Sol:** Claude Sonnet 5.5 and GPT-6 Sol weighed each objection by the record of its own voice, across surface forms and entry orders.
- **Open-weight models:** those that responded showed cross-voice spillover, consistent with weighing the reviewer's overall score, and followed the order of the log's entries and confident wording.
- **Order confound:** a fixed entry order confounded the registered contrasts. A reversed-order arm and an order-randomised arm, both with predictions or decision rules fixed in advance, measured it.

## Pre-existing work

None. All code and data were produced during the sprint; work began on 15 November 2026, and no code or data predates it.

## Repository layout

| Path | Contents |
|---|---|
| `loud-or-right-design.md` | Design document, as red-teamed before the test run |
| `pilot/` | Pilot scripts and data from development items; also scripts from other candidate projects explored briefly during project selection (`pareto_*`, `memory_fallback_*`), which are not part of this study |
| `harness/` | Frozen code for the main run (`design.py`, `run.py`, `run_all.py`, `analyze.py`, `api_client.py`, ...), item pool, selected items, run outputs (`runs/*.jsonl`), analysis outputs (`analysis/`), and `FREEZE.md`, the pre-registration record with every later deviation logged |
| `harness_x/` | A copy of the code with the exploratory additions: the recency tier, arm R (reversed order), arm S (order randomised per item) and Sonnet with reasoning on model-was-wrong items. Its record is `FREEZE_X.md`; predictions and decision rules were written there before each run |
| `harness/posthoc/` | Post hoc analyses (first-entry split, arm R vs A, arm S) |
| `paper/` | Report source and builds, figure script (`make_figs.py`), figures, and the number audit (`recount-paper.md`). `build_report_docx.py` fills the official Apart submission template, which is not included here; get it from the sprint's Guidelines page and place it in `submission-template/` |
| `paper/video/` | The explainer video, its captions, script and storyboard (`script.md`, `plan.md`), and the code that renders it (`src/`; voice-over by OpenAI text-to-speech, checked word by word with two local speech-to-text engines). See its `README.md` |
| `paper/slides/` | A 9-slide summary deck (`.pptx` and `.pdf`; main deck in Space Grotesk and Inter, `-segoe` in Segoe UI), its text spec (`content.md`) and build scripts (`src/`) |

## Reproducing

Requirements: Python 3.12+ and [`uv`](https://github.com/astral-sh/uv). Local models need [Ollama](https://ollama.com) with `gemma4:12b`, `ministral-3:8b` and `qwen3.5:9b`.

To run hosted models, copy `.env.example` to `.env` and add your own keys. Never commit `.env`.

```bash
cd harness
uv run --quiet --no-project python -I run_all.py gemma4:12b
```

```bash
uv run --quiet --no-project python -I analyze.py runs/test__*.jsonl runs/probe__*.jsonl --summary --name all
```

```bash
python ../paper/make_figs.py
```

Each run file records the model, sampling settings and serving provider on every row. The missing-data rules and statistics are in the docstring of `harness/analyze.py`.

## Data

Items come from MMLU-Pro (Wang et al., 2024; https://arxiv.org/abs/2406.01574), used under its licence. All conversations are synthetic, and the reviewer is fictional.

## Use of AI tools

- **Project selection.** Claude Fable 5.2 brainstormed candidates and ranked this project as the top pick.
- **Background and literature.** GPT-6 Astra synthesised the sprint talks. GPT-6 Astra and Gemini Carbon read and synthesised the provided resources and papers, and scouted further related work.
- **Implementation.** Claude Opus 5.5 did all the implementation (code, runs, analysis, figures, report build), with periodic reviews by Claude Fable 5.2.
- **Adversarial review.** GPT-6 Astra and Gemini Carbon red-teamed the design, checked it for confounds, and reviewed the results.
- **Writing.** Claude Fable 5.2 drafted the report from the audited analysis outputs and revised it after six independent AI reviews.
- **Video and slides.** Claude Fable 5.2 wrote the video script and the slide text. Claude Opus 5.5 built the video and the deck. The voice-over is OpenAI text-to-speech (gpt-4o-mini-tts). Gemini Carbon reviewed the video, and GPT-6 Astra reviewed the script and slides against the report.

The author selected the project, directed the work, approved its key decisions and spending, and is responsible for all claims.

## Licence

Code: MIT (see `LICENSE`). MMLU-Pro items remain under their original licence.
