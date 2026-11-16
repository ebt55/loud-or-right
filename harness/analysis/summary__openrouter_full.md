# Cross-model summary: openrouter_full

Development items, not the test set (unless inputs start with `test__`). Strict rules; no pooling of trials across models. Each row uses only that model's trials.

**Sampling and reasoning settings (from `meta`; rows without `meta` are local Ollama runs).**

| model | rows | sampling | reasoning setting | output limit | n rows |
|---|---|---|---|---|---|
| openrouter:deepseek/deepseek-v3.2 | answer-only | temperature=0 | reasoning={"enabled": false} | 32 | 7960 |
| openrouter:deepseek/deepseek-v3.2 | deliberative | temperature=0 | reasoning={"enabled": false} | 1500 | 2400 |
| openrouter:deepseek/deepseek-v3.2 | probe | temperature=0 | reasoning={"enabled": false} | 64 | 1476 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | temperature=0 | n/a | 32 | 7960 |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | temperature=0 | n/a | 1500 | 2400 |
| openrouter:meta-llama/llama-3.3-70b-instruct | probe | temperature=0 | n/a | 64 | 1476 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | temperature=0 | n/a | 32 | 7960 |
| openrouter:mistralai/ministral-14b-2512 | deliberative | temperature=0 | n/a | 1500 | 2400 |
| openrouter:mistralai/ministral-14b-2512 | probe | temperature=0 | n/a | 64 | 1476 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | C1: est [95% CI] (Holm p, n) | C2: est [95% CI] (Holm p, n) | C3: est [95% CI] (Holm p, n) | C4: est [95% CI] (Holm p, n) | arm M - A: change in d_u [95% CI] (n) | arm M - A: change in C4 [95% CI] (n) |
|---|---|---|---|---|---|---|---|---|
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | +0.081 [+0.031, +0.138] (0.0156, 80) | +0.081 [+0.025, +0.144] (0.0645, 80) | +0.044 [+0.006, +0.094] (0.2500, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | +0.037 [+0.000, +0.087] (80) | +0.013 [+0.000, +0.037] (80) |
| openrouter:deepseek/deepseek-v3.2 | deliberative | secondary | +0.100 [+0.025, +0.175] (0.0430, 80) | +0.188 [+0.075, +0.312] (0.0103, 80) | +0.163 [+0.075, +0.250] (0.0039, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | - | - |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | +0.500 [+0.394, +0.613] (3.64e-12, 80) | +0.588 [+0.450, +0.731] (3.64e-12, 80) | +0.438 [+0.325, +0.550] (1.16e-10, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) | +0.412 [+0.300, +0.525] (80) | -0.100 [-0.212, +0.013] (80) |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | secondary | +0.287 [+0.188, +0.388] (7.15e-07, 80) | +0.388 [+0.250, +0.525] (1.74e-06, 80) | +0.388 [+0.287, +0.500] (3.73e-09, 80) | +0.113 [+0.050, +0.188] (0.0039, 80) | - | - |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | +0.294 [+0.188, +0.400] (2.41e-06, 80) | +0.325 [+0.200, +0.456] (3.05e-05, 80) | +0.450 [+0.338, +0.562] (1.16e-10, 80) | +0.188 [+0.113, +0.275] (6.10e-05, 80) | +0.294 [+0.181, +0.419] (80) | -0.013 [-0.125, +0.087] (80) |
| openrouter:mistralai/ministral-14b-2512 | deliberative | secondary | +0.263 [+0.163, +0.362] (1.14e-05, 80) | +0.350 [+0.200, +0.500] (3.86e-05, 80) | +0.338 [+0.212, +0.463] (1.04e-05, 80) | +0.263 [+0.163, +0.362] (3.81e-06, 80) | - | - |

Arm M columns are exploratory (mitigation instruction; same items, paired).

## Model-was-right stratum (exploratory): answer-only, arm A

The reviewer names a wrong option on items the model first answered correctly, so every flip lowers accuracy. Flips / non-missing items per cell; the contrast is paired on items non-missing in both cells.

| model | tier | control | certain\|certain_right | certain\|perfect_mixed | certain\|reliable | certain\|unsure_right | certain\|none | unsure\|unsure_right | unsure\|certain_right | unsure\|perfect_mixed | certain\|certain_right - certain\|unsure_right [95% CI] | A > B / B > A | sign p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter:deepseek/deepseek-v3.2 | main | 0/40 | 1/40 | 2/40 | 1/40 | 0/40 | 2/40 | 0/40 | 0/40 | 1/40 | +0.025 [+0.000, +0.075] (n=40) | 1 / 0 | 1.0000 |
| openrouter:meta-llama/llama-3.3-70b-instruct | main | 0/40 | 5/40 | 8/40 | 6/40 | 0/40 | 2/40 | 1/40 | 1/40 | 2/40 | +0.125 [+0.025, +0.225] (n=40) | 5 / 0 | 0.0625 |
| openrouter:mistralai/ministral-14b-2512 | main | 1/40 | 5/40 | 15/40 | 7/40 | 1/40 | 5/40 | 1/40 | 2/40 | 6/40 | +0.100 [+0.025, +0.200] (n=40) | 4 / 0 | 0.1250 |

# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)

Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).

| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |
|---|---|---|---|---|---|---|
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | certain | 1.00 (n=1) | 6.50/80 = 0.08 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | certain | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | unsure | 1.00 (n=1) | 0.50/80 = 0.01 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | unsure | 0.00 (n=1) | 0.50/80 = 0.01 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | unsure | 1.00 (n=1) | 4/80 = 0.05 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | certain | 1.00 (n=1) | 31/80 = 0.39 | 12/80 = 0.15 |
| openrouter:deepseek/deepseek-v3.2 | B | certain_right | certain | 1.00 (n=40) | 4/80 = 0.05 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | B | unsure_right | certain | 0.00 (n=40) | 3/80 = 0.04 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | B | unsure_right | unsure | 1.00 (n=40) | 1/80 = 0.01 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | B | certain_right | unsure | 0.00 (n=40) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | B | perfect_mixed | unsure | 1.00 (n=40) | 11/80 = 0.14 | 1/80 = 0.01 |
| openrouter:deepseek/deepseek-v3.2 | B | perfect_mixed | certain | 1.00 (n=40) | 30/80 = 0.38 | 12/80 = 0.15 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | certain_right | certain | 1.00 (n=1) | 61.50/80 = 0.77 | 22/80 = 0.28 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unsure_right | certain | 0.00 (n=1) | 21.50/80 = 0.27 | 6/80 = 0.07 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unsure_right | unsure | 1.00 (n=1) | 25/80 = 0.31 | 5/80 = 0.06 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | certain_right | unsure | 0.00 (n=1) | 32/80 = 0.40 | 5/80 = 0.06 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | perfect_mixed | unsure | 1.00 (n=1) | 60/80 = 0.75 | 13/80 = 0.16 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | perfect_mixed | certain | 1.00 (n=1) | 70/80 = 0.88 | 30/80 = 0.38 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | certain_right | certain | 1.00 (n=40) | 49/80 = 0.61 | 10/80 = 0.12 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unsure_right | certain | 0.00 (n=40) | 39/80 = 0.49 | 6/80 = 0.07 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unsure_right | unsure | 1.00 (n=40) | 42/80 = 0.53 | 7/80 = 0.09 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | certain_right | unsure | 0.00 (n=40) | 28/80 = 0.35 | 4/80 = 0.05 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | perfect_mixed | unsure | 1.00 (n=40) | 65/80 = 0.81 | 18/80 = 0.23 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | perfect_mixed | certain | 1.00 (n=40) | 71/80 = 0.89 | 26/80 = 0.33 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | certain | 1.00 (n=1) | 35.50/80 = 0.44 | 18/80 = 0.23 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | certain | 0.00 (n=1) | 12/80 = 0.15 | 3/80 = 0.04 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 3/80 = 0.04 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | unsure | 0.00 (n=1) | 14.50/80 = 0.18 | 4/80 = 0.05 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | unsure | 1.00 (n=1) | 48/80 = 0.60 | 23/80 = 0.29 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | certain | 1.00 (n=1) | 72/80 = 0.90 | 44/80 = 0.55 |
| openrouter:mistralai/ministral-14b-2512 | B | certain_right | certain | 1.00 (n=40) | 19/80 = 0.24 | 7/80 = 0.09 |
| openrouter:mistralai/ministral-14b-2512 | B | unsure_right | certain | 0.00 (n=40) | 22/80 = 0.28 | 2/80 = 0.03 |
| openrouter:mistralai/ministral-14b-2512 | B | unsure_right | unsure | 1.00 (n=40) | 20/80 = 0.25 | 3/80 = 0.04 |
| openrouter:mistralai/ministral-14b-2512 | B | certain_right | unsure | 0.00 (n=40) | 16/80 = 0.20 | 3/80 = 0.04 |
| openrouter:mistralai/ministral-14b-2512 | B | perfect_mixed | unsure | 0.99 (n=40) | 64/80 = 0.80 | 32/80 = 0.40 |
| openrouter:mistralai/ministral-14b-2512 | B | perfect_mixed | certain | 1.00 (n=40) | 72/80 = 0.90 | 44/80 = 0.55 |
