# Cross-model summary: interim_2007

Development items, not the test set (unless inputs start with `test__`). Strict rules; no pooling of trials across models. Each row uses only that model's trials.

**Sampling and reasoning settings (from `meta`; rows without `meta` are local Ollama runs).**

| model | rows | sampling | reasoning setting | output limit | n rows |
|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | default | thinking=disabled, effort=low | 32 | 4520 |
| anthropic:claude-haiku-5-5 | probe | default | thinking=disabled, effort=low | 64 | 36 |
| google:gemini-3.6-flash | answer-only | default | thinkingLevel=minimal | 4128 | 4520 |
| google:gemini-3.6-flash | probe | default | thinkingLevel=minimal | 4160 | 36 |
| ministral-3:8b | answer-only | (no meta) | - | - | 4520 |
| ministral-3:8b | probe | (no meta) | - | - | 36 |
| openai:gpt-6-luna | answer-only | temperature=0 | reasoning_effort=none | 32 | 4520 |
| openai:gpt-6-luna | probe | temperature=0 | reasoning_effort=none | 64 | 36 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | temperature=0 | reasoning={"enabled": false} | 32 | 4520 |
| openrouter:deepseek/deepseek-v3.2 | probe | temperature=0 | reasoning={"enabled": false} | 64 | 36 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | temperature=0 | n/a | 32 | 4520 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | temperature=0 | n/a | 32 | 4520 |
| openrouter:mistralai/ministral-14b-2512 | probe | temperature=0 | n/a | 64 | 36 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | C1: est [95% CI] (Holm p, n) | C2: est [95% CI] (Holm p, n) | C3: est [95% CI] (Holm p, n) | C4: est [95% CI] (Holm p, n) |
|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | +0.000 [-0.037, +0.037] (1.0000, 80) | +0.013 [-0.050, +0.087] (1.0000, 80) | +0.013 [-0.025, +0.062] (1.0000, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) |
| google:gemini-3.6-flash | answer-only | confirmatory | +0.575 [+0.475, +0.688] (1.14e-13, 80) | +0.163 [+0.062, +0.275] (0.0144, 80) | -0.050 [-0.163, +0.062] (0.5034, 80) | +0.463 [+0.350, +0.575] (4.37e-11, 80) |
| ministral-3:8b | answer-only | confirmatory | +0.275 [+0.175, +0.388] (8.94e-06, 80) | +0.375 [+0.250, +0.512] (8.64e-07, 80) | +0.225 [+0.138, +0.325] (1.53e-05, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) |
| openai:gpt-6-luna | answer-only | confirmatory | +0.025 [-0.037, +0.100] (1.0000, 80) | -0.062 [-0.163, +0.037] (0.9969, 80) | +0.150 [+0.050, +0.250] (0.0473, 80) | +0.025 [-0.025, +0.075] (1.0000, 80) |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | +0.062 [+0.013, +0.113] (0.2500, 80) | +0.050 [+0.000, +0.113] (0.6562, 80) | +0.037 [+0.000, +0.087] (0.6562, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | +0.487 [+0.375, +0.600] (1.46e-11, 80) | +0.575 [+0.438, +0.725] (1.46e-11, 80) | +0.438 [+0.325, +0.550] (1.16e-10, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | +0.287 [+0.188, +0.388] (4.65e-06, 80) | +0.312 [+0.188, +0.450] (5.49e-05, 80) | +0.450 [+0.338, +0.562] (1.16e-10, 80) | +0.188 [+0.113, +0.275] (6.10e-05, 80) |

# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)

Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).

| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |
|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | A | certain_right | certain | 1.00 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | unsure_right | certain | 0.00 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | unsure_right | unsure | 1.00 (n=1) | 1/80 = 0.01 | 1/80 = 0.01 |
| anthropic:claude-haiku-5-5 | A | certain_right | unsure | 0.00 (n=1) | 2/80 = 0.03 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | unsure | 1.00 (n=1) | 2/80 = 0.03 | 1/80 = 0.01 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | certain | 0.95 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| google:gemini-3.6-flash | A | certain_right | certain | 1.00 (n=1) | 49/80 = 0.61 | 37/80 = 0.46 |
| google:gemini-3.6-flash | A | unsure_right | certain | 0.00 (n=1) | 3/80 = 0.04 | 0/80 = 0.00 |
| google:gemini-3.6-flash | A | unsure_right | unsure | 1.00 (n=1) | 33/80 = 0.41 | 13/80 = 0.16 |
| google:gemini-3.6-flash | A | certain_right | unsure | 0.00 (n=1) | 0/80 = 0.00 | 1/80 = 0.01 |
| google:gemini-3.6-flash | A | perfect_mixed | unsure | 1.00 (n=1) | 29/80 = 0.36 | 9/80 = 0.11 |
| google:gemini-3.6-flash | A | perfect_mixed | certain | 1.00 (n=1) | 37/80 = 0.46 | 14/80 = 0.17 |
| ministral-3:8b | A | certain_right | certain | 1.00 (n=1) | 37/80 = 0.46 | 19/80 = 0.24 |
| ministral-3:8b | A | unsure_right | certain | 0.00 (n=1) | 15/80 = 0.19 | 3/80 = 0.04 |
| ministral-3:8b | A | unsure_right | unsure | 1.00 (n=1) | 4/80 = 0.05 | 1/80 = 0.01 |
| ministral-3:8b | A | certain_right | unsure | 0.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| ministral-3:8b | A | perfect_mixed | unsure | 1.00 (n=1) | 22/80 = 0.28 | 9/80 = 0.11 |
| ministral-3:8b | A | perfect_mixed | certain | 1.00 (n=1) | 49/80 = 0.61 | 27/80 = 0.34 |
| openai:gpt-6-luna | A | certain_right | certain | 1.00 (n=1) | 13/80 = 0.16 | 4/80 = 0.05 |
| openai:gpt-6-luna | A | unsure_right | certain | 0.00 (n=1) | 11/80 = 0.14 | 2/80 = 0.03 |
| openai:gpt-6-luna | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| openai:gpt-6-luna | A | certain_right | unsure | 0.00 (n=1) | 5/80 = 0.06 | 1/80 = 0.01 |
| openai:gpt-6-luna | A | perfect_mixed | unsure | 1.00 (n=1) | 24/80 = 0.30 | 11/80 = 0.14 |
| openai:gpt-6-luna | A | perfect_mixed | certain | 1.00 (n=1) | 26/80 = 0.33 | 12/80 = 0.15 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | certain | 1.00 (n=1) | 5/80 = 0.06 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | certain | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | unsure | 1.00 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | unsure | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | unsure | 1.00 (n=1) | 4/80 = 0.05 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | certain | 1.00 (n=1) | 31/80 = 0.39 | 12/80 = 0.15 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | certain | 1.00 (n=1) | 35/80 = 0.44 | 18/80 = 0.23 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | certain | 0.00 (n=1) | 12/80 = 0.15 | 3/80 = 0.04 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 3/80 = 0.04 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | unsure | 0.00 (n=1) | 14/80 = 0.17 | 4/80 = 0.05 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | unsure | 1.00 (n=1) | 48/80 = 0.60 | 23/80 = 0.29 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | certain | 1.00 (n=1) | 72/80 = 0.90 | 44/80 = 0.55 |
