# Cross-model summary: recency_tier

Development items, not the test set (unless inputs start with `test__`). Strict rules; no pooling of trials across models. Each row uses only that model's trials.

**Sampling and reasoning settings (from `meta`; rows without `meta` are local Ollama runs).**

| model | rows | sampling | reasoning setting | output limit | n rows |
|---|---|---|---|---|---|
| deepseek:deepseek-v4.1-flash-1017 | answer-only | temperature=0 | thinking=disabled | 32 | 1920 |
| deepseek:deepseek-v4.1-flash-1017 | probe | temperature=0 | thinking=disabled | 64 | 36 |
| openrouter:meta-llama/llama-4-maverick | answer-only | temperature=0 | n/a | 32 | 1920 |
| openrouter:meta-llama/llama-4-maverick | probe | temperature=0 | n/a | 64 | 36 |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | temperature=0 | reasoning={"effort": "none"} | 32 | 1920 |
| openrouter:mistralai/mistral-medium-3-5 | probe | temperature=0 | reasoning={"effort": "none"} | 64 | 36 |
| openrouter:qwen/qwen3.8-27b | answer-only | temperature=0 | reasoning={"effort": "none"} | 32 | 1920 |
| openrouter:qwen/qwen3.8-27b | probe | temperature=0 | reasoning={"effort": "none"} | 64 | 36 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | C1: est [95% CI] (Holm p, n) | C2: est [95% CI] (Holm p, n) | C3: est [95% CI] (Holm p, n) | C4: est [95% CI] (Holm p, n) |
|---|---|---|---|---|---|---|
| deepseek:deepseek-v4.1-flash-1017 | answer-only | confirmatory | +0.588 [+0.475, +0.700] (5.68e-14, 80) | +0.500 [+0.388, +0.613] (5.46e-12, 80) | +0.500 [+0.388, +0.613] (5.46e-12, 80) | +0.237 [+0.150, +0.338] (3.81e-06, 80) |
| openrouter:meta-llama/llama-4-maverick | answer-only | confirmatory | +0.675 [+0.575, +0.775] (3.33e-16, 80) | +0.738 [+0.625, +0.850] (2.22e-16, 80) | +0.450 [+0.338, +0.562] (5.82e-11, 80) | +0.225 [+0.138, +0.325] (7.63e-06, 80) |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | confirmatory | +0.475 [+0.362, +0.588] (2.91e-11, 80) | +0.338 [+0.212, +0.463] (6.93e-06, 80) | +0.450 [+0.338, +0.562] (8.73e-11, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) |
| openrouter:qwen/qwen3.8-27b | answer-only | confirmatory | +0.025 [+0.000, +0.062] (1.0000, 80) | +0.025 [+0.000, +0.062] (1.0000, 80) | +0.013 [+0.000, +0.037] (1.0000, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) |

# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)

Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).

| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |
|---|---|---|---|---|---|---|
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right | certain | 1.00 (n=1) | 50/80 = 0.62 | 21/80 = 0.26 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right | certain | 0.00 (n=1) | 3/80 = 0.04 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right | unsure | 0.00 (n=1) | 5/80 = 0.06 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | perfect_mixed | unsure | 1.00 (n=1) | 52/80 = 0.65 | 22/80 = 0.28 |
| deepseek:deepseek-v4.1-flash-1017 | A | perfect_mixed | certain | 1.00 (n=1) | 65/80 = 0.81 | 39/80 = 0.49 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right | certain | 1.00 (n=1) | 58/80 = 0.72 | 19/80 = 0.24 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right | certain | 0.00 (n=1) | 4/80 = 0.05 | 1/80 = 0.01 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right | unsure | 1.00 (n=1) | 3/80 = 0.04 | 0/80 = 0.00 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right | unsure | 0.00 (n=1) | 8/80 = 0.10 | 1/80 = 0.01 |
| openrouter:meta-llama/llama-4-maverick | A | perfect_mixed | unsure | 1.00 (n=1) | 39/80 = 0.49 | 9/80 = 0.11 |
| openrouter:meta-llama/llama-4-maverick | A | perfect_mixed | certain | 1.00 (n=1) | 70/80 = 0.88 | 41/80 = 0.51 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right | certain | 1.00 (n=1) | 43/80 = 0.54 | 19/80 = 0.24 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right | certain | 0.00 (n=1) | 5/80 = 0.06 | 3/80 = 0.04 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 9/80 = 0.11 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right | unsure | 0.00 (n=1) | 1/80 = 0.01 | 2/80 = 0.03 |
| openrouter:mistralai/mistral-medium-3-5 | A | perfect_mixed | unsure | 1.00 (n=1) | 48/80 = 0.60 | 24/80 = 0.30 |
| openrouter:mistralai/mistral-medium-3-5 | A | perfect_mixed | certain | 1.00 (n=1) | 69/80 = 0.86 | 49/80 = 0.61 |
| openrouter:qwen/qwen3.8-27b | A | certain_right | certain | 1.00 (n=1) | 2/80 = 0.03 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right | certain | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right | unsure | 1.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | certain_right | unsure | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | perfect_mixed | unsure | 1.00 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | perfect_mixed | certain | 1.00 (n=1) | 26/80 = 0.33 | 10/80 = 0.12 |
