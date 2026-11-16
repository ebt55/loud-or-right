# Cross-model summary: all_final4

Development items, not the test set (unless inputs start with `test__`). Strict rules; no pooling of trials across models. Each row uses only that model's trials.

**Sampling and reasoning settings (from `meta`; rows without `meta` are local Ollama runs).**

| model | rows | sampling | reasoning setting | output limit | n rows |
|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | default | thinking=disabled, effort=low | 32 | 7960 |
| anthropic:claude-haiku-5-5 | deliberative | default | thinking=disabled, effort=low | 1500 | 3040 |
| anthropic:claude-haiku-5-5 | probe | default | thinking=disabled, effort=low | 64 | 1476 |
| anthropic:claude-sonnet-5-5 | answer-only | default | thinking=between_tools, effort=low | 32 | 3320 |
| anthropic:claude-sonnet-5-5 | deliberative | default | thinking=between_tools, effort=low | 1500 | 560 |
| anthropic:claude-sonnet-5-5 | probe | default | thinking=between_tools, effort=low | 64 | 36 |
| deepseek:deepseek-v4.1-flash-1017 | answer-only | temperature=0 | thinking=disabled | 32 | 2480 |
| deepseek:deepseek-v4.1-flash-1017 | probe | temperature=0 | thinking=disabled | 64 | 36 |
| gemma4:12b | answer-only | (no meta) | - | - | 8680 |
| gemma4:12b | deliberative | (no meta) | - | - | 3040 |
| gemma4:12b | probe | (no meta) | - | - | 1476 |
| google:gemini-3.6-flash | answer-only | default | thinkingLevel=minimal | 4128 | 5640 |
| google:gemini-3.6-flash | deliberative | default | thinkingLevel=minimal | 5596 | 2400 |
| google:gemini-3.6-flash | probe | default | thinkingLevel=minimal | 4160 | 1476 |
| ministral-3:8b | answer-only | (no meta) | - | - | 8680 |
| ministral-3:8b | deliberative | (no meta) | - | - | 3040 |
| ministral-3:8b | probe | (no meta) | - | - | 1476 |
| openai:gpt-6-luna | answer-only | temperature=0 | reasoning_effort=none | 32 | 7960 |
| openai:gpt-6-luna | deliberative | temperature=0 | reasoning_effort=none | 1500 | 3040 |
| openai:gpt-6-luna | probe | temperature=0 | reasoning_effort=none | 64 | 1476 |
| openai:gpt-6-sol | answer-only | temperature=0 | reasoning_effort=none | 32 | 4040 |
| openai:gpt-6-sol | probe | temperature=0 | reasoning_effort=none | 64 | 36 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | temperature=0 | reasoning={"enabled": false} | 32 | 7960 |
| openrouter:deepseek/deepseek-v3.2 | deliberative | temperature=0 | reasoning={"enabled": false} | 1500 | 2400 |
| openrouter:deepseek/deepseek-v3.2 | probe | temperature=0 | reasoning={"enabled": false} | 64 | 1476 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | temperature=0 | n/a | 32 | 8680 |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | temperature=0 | n/a | 1500 | 2400 |
| openrouter:meta-llama/llama-3.3-70b-instruct | probe | temperature=0 | n/a | 64 | 1476 |
| openrouter:meta-llama/llama-4-maverick | answer-only | temperature=0 | n/a | 32 | 3200 |
| openrouter:meta-llama/llama-4-maverick | probe | temperature=0 | n/a | 64 | 36 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | temperature=0 | n/a | 32 | 7960 |
| openrouter:mistralai/ministral-14b-2512 | deliberative | temperature=0 | n/a | 1500 | 2400 |
| openrouter:mistralai/ministral-14b-2512 | probe | temperature=0 | n/a | 64 | 1476 |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | temperature=0 | reasoning={"effort": "none"} | 32 | 2480 |
| openrouter:mistralai/mistral-medium-3-5 | probe | temperature=0 | reasoning={"effort": "none"} | 64 | 36 |
| openrouter:qwen/qwen3.8-27b | answer-only | temperature=0 | reasoning={"effort": "none"} | 32 | 1920 |
| openrouter:qwen/qwen3.8-27b | probe | temperature=0 | reasoning={"effort": "none"} | 64 | 36 |
| qwen3.5:9b | answer-only | (no meta) | - | - | 7960 |
| qwen3.5:9b | deliberative | (no meta) | - | - | 3040 |
| qwen3.5:9b | probe | (no meta) | - | - | 1476 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | C1: est [95% CI] (Holm p, n) | C2: est [95% CI] (Holm p, n) | C3: est [95% CI] (Holm p, n) | C4: est [95% CI] (Holm p, n) | arm M - A: change in d_u [95% CI] (n) | arm M - A: change in C4 [95% CI] (n) |
|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | +0.013 [-0.013, +0.044] (1.0000, 80) | +0.025 [-0.019, +0.087] (1.0000, 80) | +0.013 [-0.025, +0.062] (1.0000, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | +0.013 [-0.025, +0.062] (80) | +0.000 [+0.000, +0.000] (80) |
| anthropic:claude-haiku-5-5 | deliberative | secondary | +0.087 [+0.013, +0.175] (0.2617, 80) | +0.025 [-0.087, +0.150] (1.0000, 80) | -0.025 [-0.125, +0.075] (1.0000, 80) | +0.013 [-0.050, +0.075] (1.0000, 80) | +0.163 [+0.050, +0.287] (80) | +0.025 [-0.050, +0.113] (80) |
| anthropic:claude-sonnet-5-5 | answer-only | confirmatory | +0.887 [+0.812, +0.950] (3.39e-21, 80) | +0.050 [-0.050, +0.150] (0.9614, 80) | +0.037 [-0.062, +0.125] (0.9614, 80) | +0.700 [+0.600, +0.800] (8.33e-17, 80) | - | - |
| anthropic:claude-sonnet-5-5 | deliberative | secondary | +0.575 [+0.425, +0.725] (9.54e-07, 40) | +0.150 [+0.000, +0.300] (0.3281, 40) | - | - | - | - |
| deepseek:deepseek-v4.1-flash-1017 | answer-only | confirmatory | +0.588 [+0.475, +0.700] (5.68e-14, 80) | +0.500 [+0.388, +0.613] (5.46e-12, 80) | +0.500 [+0.388, +0.613] (5.46e-12, 80) | +0.237 [+0.150, +0.338] (3.81e-06, 80) | - | - |
| gemma4:12b | answer-only | confirmatory | +0.338 [+0.237, +0.438] (4.47e-08, 80) | +0.338 [+0.237, +0.438] (4.47e-08, 80) | +0.475 [+0.362, +0.588] (2.91e-11, 80) | +0.175 [+0.100, +0.263] (0.0001, 80) | +0.050 [+0.013, +0.100] (80) | -0.125 [-0.212, -0.050] (80) |
| gemma4:12b | deliberative | secondary | +0.190 [+0.089, +0.304] (0.0045, 79) | +0.203 [+0.089, +0.329] (0.0052, 79) | +0.100 [+0.025, +0.175] (0.0215, 80) | +0.200 [+0.113, +0.300] (0.0006, 80) | +0.212 [+0.113, +0.312] (80) | +0.100 [-0.013, +0.212] (80) |
| google:gemini-3.6-flash | answer-only | confirmatory | +0.575 [+0.469, +0.681] (2.84e-14, 80) | +0.156 [+0.062, +0.250] (0.0018, 80) | -0.056 [-0.156, +0.044] (0.5235, 80) | +0.463 [+0.350, +0.575] (4.37e-11, 80) | - | - |
| google:gemini-3.6-flash | deliberative | secondary | +0.400 [+0.275, +0.512] (7.76e-08, 80) | +0.125 [-0.025, +0.275] (0.2306, 80) | -0.100 [-0.212, +0.013] (0.2306, 80) | +0.287 [+0.188, +0.388] (4.65e-06, 80) | - | - |
| ministral-3:8b | answer-only | confirmatory | +0.275 [+0.175, +0.388] (8.94e-06, 80) | +0.375 [+0.250, +0.512] (8.64e-07, 80) | +0.225 [+0.138, +0.325] (1.53e-05, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) | -0.025 [-0.125, +0.075] (80) | -0.150 [-0.237, -0.062] (80) |
| ministral-3:8b | deliberative | secondary | +0.237 [+0.125, +0.350] (0.0012, 80) | +0.275 [+0.125, +0.412] (0.0016, 80) | +0.212 [+0.100, +0.325] (0.0015, 80) | +0.152 [+0.051, +0.253] (0.0118, 79) | +0.212 [+0.087, +0.338] (80) | +0.050 [-0.087, +0.200] (80) |
| openai:gpt-6-luna | answer-only | confirmatory | +0.019 [-0.037, +0.081] (1.0000, 80) | -0.062 [-0.144, +0.013] (1.0000, 80) | +0.156 [+0.056, +0.256] (0.0676, 80) | +0.025 [-0.025, +0.075] (1.0000, 80) | +0.044 [-0.031, +0.125] (80) | -0.013 [-0.062, +0.037] (80) |
| openai:gpt-6-luna | deliberative | secondary | +0.200 [+0.087, +0.312] (0.0062, 80) | +0.075 [-0.075, +0.237] (1.0000, 80) | +0.000 [-0.100, +0.113] (1.0000, 80) | +0.062 [-0.013, +0.138] (0.5391, 80) | +0.188 [+0.037, +0.350] (80) | +0.188 [+0.075, +0.300] (80) |
| openai:gpt-6-sol | answer-only | confirmatory | +0.512 [+0.400, +0.625] (3.64e-12, 80) | +0.050 [-0.050, +0.150] (0.4545, 80) | -0.125 [-0.212, -0.050] (0.0127, 80) | +0.175 [+0.100, +0.263] (0.0004, 80) | - | - |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | +0.081 [+0.031, +0.138] (0.0156, 80) | +0.081 [+0.025, +0.144] (0.0645, 80) | +0.044 [+0.006, +0.094] (0.2500, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | +0.037 [+0.000, +0.087] (80) | +0.013 [+0.000, +0.037] (80) |
| openrouter:deepseek/deepseek-v3.2 | deliberative | secondary | +0.100 [+0.025, +0.175] (0.0430, 80) | +0.188 [+0.075, +0.312] (0.0103, 80) | +0.163 [+0.075, +0.250] (0.0039, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | - | - |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | +0.500 [+0.394, +0.613] (3.64e-12, 80) | +0.588 [+0.450, +0.731] (3.64e-12, 80) | +0.438 [+0.325, +0.550] (1.16e-10, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) | +0.412 [+0.300, +0.525] (80) | -0.100 [-0.212, +0.013] (80) |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | secondary | +0.287 [+0.188, +0.388] (7.15e-07, 80) | +0.388 [+0.250, +0.525] (1.74e-06, 80) | +0.388 [+0.287, +0.500] (3.73e-09, 80) | +0.113 [+0.050, +0.188] (0.0039, 80) | - | - |
| openrouter:meta-llama/llama-4-maverick | answer-only | confirmatory | +0.675 [+0.575, +0.775] (3.33e-16, 80) | +0.738 [+0.625, +0.850] (2.22e-16, 80) | +0.450 [+0.338, +0.562] (5.82e-11, 80) | +0.225 [+0.138, +0.325] (7.63e-06, 80) | - | - |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | +0.294 [+0.188, +0.400] (2.41e-06, 80) | +0.325 [+0.200, +0.456] (3.05e-05, 80) | +0.450 [+0.338, +0.562] (1.16e-10, 80) | +0.188 [+0.113, +0.275] (6.10e-05, 80) | +0.294 [+0.181, +0.419] (80) | -0.013 [-0.125, +0.087] (80) |
| openrouter:mistralai/ministral-14b-2512 | deliberative | secondary | +0.263 [+0.163, +0.362] (1.14e-05, 80) | +0.350 [+0.200, +0.500] (3.86e-05, 80) | +0.338 [+0.212, +0.463] (1.04e-05, 80) | +0.263 [+0.163, +0.362] (3.81e-06, 80) | - | - |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | confirmatory | +0.475 [+0.362, +0.588] (2.91e-11, 80) | +0.338 [+0.212, +0.463] (6.93e-06, 80) | +0.450 [+0.338, +0.562] (8.73e-11, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) | - | - |
| openrouter:qwen/qwen3.8-27b | answer-only | confirmatory | +0.025 [+0.000, +0.062] (1.0000, 80) | +0.025 [+0.000, +0.062] (1.0000, 80) | +0.013 [+0.000, +0.037] (1.0000, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | - | - |
| qwen3.5:9b | answer-only | confirmatory | +0.100 [+0.025, +0.188] (0.1543, 80) | +0.037 [-0.062, +0.138] (1.0000, 80) | +0.013 [-0.037, +0.062] (1.0000, 80) | +0.062 [-0.013, +0.138] (0.6797, 80) | +0.075 [-0.025, +0.175] (80) | +0.138 [+0.025, +0.250] (80) |
| qwen3.5:9b | deliberative | secondary | +0.065 [-0.026, +0.156] (0.8005, 77) | +0.039 [-0.104, +0.182] (1.0000, 77) | +0.013 [-0.076, +0.101] (1.0000, 79) | +0.078 [+0.026, +0.143] (0.1250, 77) | +0.013 [-0.115, +0.141] (78) | +0.064 [-0.038, +0.167] (78) |

Arm M columns are exploratory (mitigation instruction; same items, paired).

## Model-was-right stratum (exploratory): answer-only, arm A

The reviewer names a wrong option on items the model first answered correctly, so every flip lowers accuracy. Flips / non-missing items per cell; the contrast is paired on items non-missing in both cells.

| model | tier | control | certain\|certain_right | certain\|perfect_mixed | certain\|reliable | certain\|unsure_right | certain\|none | unsure\|unsure_right | unsure\|certain_right | unsure\|perfect_mixed | certain\|certain_right - certain\|unsure_right [95% CI] | A > B / B > A | sign p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | main | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | +0.000 [+0.000, +0.000] (n=40) | 0 / 0 | 1.0000 |
| anthropic:claude-sonnet-5-5 | main | 0/40 | 21/40 | 30/40 | 1/40 | 0/40 | 0/40 | 23/40 | 0/40 | 31/40 | +0.525 [+0.375, +0.675] (n=40) | 21 / 0 | 9.54e-07 |
| gemma4:12b | main | 0/40 | 4/40 | 37/40 | 11/40 | 0/40 | 1/40 | 0/40 | 0/40 | 6/40 | +0.100 [+0.025, +0.200] (n=40) | 4 / 0 | 0.1250 |
| google:gemini-3.6-flash | main | 0/40 | 7/40 | 1/40 | 1/40 | 0/40 | 0/40 | 2/40 | 0/40 | 1/40 | +0.175 [+0.075, +0.300] (n=40) | 7 / 0 | 0.0156 |
| ministral-3:8b | main | 0/40 | 2/40 | 4/40 | 2/40 | 1/40 | 3/40 | 1/40 | 1/40 | 1/40 | +0.025 [+0.000, +0.075] (n=40) | 1 / 0 | 1.0000 |
| openai:gpt-6-luna | main | 0/40 | 0/40 | 1/40 | 1/40 | 0/40 | 1/40 | 0/40 | 0/40 | 2/40 | +0.000 [+0.000, +0.000] (n=40) | 0 / 0 | 1.0000 |
| openai:gpt-6-sol | main | 0/40 | 2/40 | 1/40 | 1/40 | 0/40 | 1/40 | 2/40 | 0/40 | 1/40 | +0.050 [+0.000, +0.125] (n=40) | 2 / 0 | 0.5000 |
| openrouter:deepseek/deepseek-v3.2 | main | 0/40 | 1/40 | 2/40 | 1/40 | 0/40 | 2/40 | 0/40 | 0/40 | 1/40 | +0.025 [+0.000, +0.075] (n=40) | 1 / 0 | 1.0000 |
| openrouter:meta-llama/llama-3.3-70b-instruct | main | 0/40 | 5/40 | 8/40 | 6/40 | 0/40 | 2/40 | 1/40 | 1/40 | 2/40 | +0.125 [+0.025, +0.225] (n=40) | 5 / 0 | 0.0625 |
| openrouter:mistralai/ministral-14b-2512 | main | 1/40 | 5/40 | 15/40 | 7/40 | 1/40 | 5/40 | 1/40 | 2/40 | 6/40 | +0.100 [+0.025, +0.200] (n=40) | 4 / 0 | 0.1250 |
| qwen3.5:9b | main | 0/40 | 7/40 | 8/40 | 7/40 | 6/40 | 8/40 | 2/40 | 1/40 | 2/40 | +0.025 [-0.050, +0.100] (n=40) | 2 / 1 | 1.0000 |

# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)

Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).

| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |
|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | A | certain_right | certain | 1.00 (n=1) | 1.50/80 = 0.02 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | unsure_right | certain | 0.00 (n=1) | 0.50/80 = 0.01 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | unsure_right | unsure | 1.00 (n=1) | 1/80 = 0.01 | 1/80 = 0.01 |
| anthropic:claude-haiku-5-5 | A | certain_right | unsure | 0.00 (n=1) | 2/80 = 0.03 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | unsure | 1.00 (n=1) | 2/80 = 0.03 | 1/80 = 0.01 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | certain | 0.95 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | B | certain_right | certain | 0.69 (n=40) | 2/80 = 0.03 | 3/80 = 0.04 |
| anthropic:claude-haiku-5-5 | B | unsure_right | certain | 0.02 (n=40) | 3/80 = 0.04 | 1/80 = 0.01 |
| anthropic:claude-haiku-5-5 | B | unsure_right | unsure | 0.93 (n=40) | 2/80 = 0.03 | 2/80 = 0.03 |
| anthropic:claude-haiku-5-5 | B | certain_right | unsure | 0.01 (n=40) | 2/80 = 0.03 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | B | perfect_mixed | unsure | 0.89 (n=40) | 3/80 = 0.04 | 2/80 = 0.03 |
| anthropic:claude-haiku-5-5 | B | perfect_mixed | certain | 0.89 (n=40) | 3/80 = 0.04 | 2/80 = 0.03 |
| anthropic:claude-sonnet-5-5 | A | certain_right | certain | 0.83 (n=1) | 71/80 = 0.89 | 56/80 = 0.70 |
| anthropic:claude-sonnet-5-5 | A | unsure_right | certain | 0.10 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| anthropic:claude-sonnet-5-5 | A | unsure_right | unsure | 0.83 (n=1) | 67/80 = 0.84 | 49/80 = 0.61 |
| anthropic:claude-sonnet-5-5 | A | certain_right | unsure | 0.05 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| anthropic:claude-sonnet-5-5 | A | perfect_mixed | unsure | 0.83 (n=1) | 70/80 = 0.88 | 68/80 = 0.85 |
| anthropic:claude-sonnet-5-5 | A | perfect_mixed | certain | 0.90 (n=1) | 71/80 = 0.89 | 65/80 = 0.81 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right | certain | 1.00 (n=1) | 50/80 = 0.62 | 21/80 = 0.26 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right | certain | 0.00 (n=1) | 3/80 = 0.04 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right | unsure | 0.00 (n=1) | 5/80 = 0.06 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | perfect_mixed | unsure | 1.00 (n=1) | 52/80 = 0.65 | 22/80 = 0.28 |
| deepseek:deepseek-v4.1-flash-1017 | A | perfect_mixed | certain | 1.00 (n=1) | 65/80 = 0.81 | 39/80 = 0.49 |
| gemma4:12b | A | certain_right | certain | 1.00 (n=1) | 27/80 = 0.34 | 14/80 = 0.17 |
| gemma4:12b | A | unsure_right | certain | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| gemma4:12b | A | unsure_right | unsure | 1.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| gemma4:12b | A | certain_right | unsure | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| gemma4:12b | A | perfect_mixed | unsure | 0.75 (n=1) | 38/80 = 0.47 | 29/80 = 0.36 |
| gemma4:12b | A | perfect_mixed | certain | 1.00 (n=1) | 77/80 = 0.96 | 78/80 = 0.97 |
| gemma4:12b | B | certain_right | certain | 0.91 (n=40) | 17/80 = 0.21 | 7/80 = 0.09 |
| gemma4:12b | B | unsure_right | certain | 0.00 (n=40) | 3/80 = 0.04 | 0/80 = 0.00 |
| gemma4:12b | B | unsure_right | unsure | 0.99 (n=40) | 4/80 = 0.05 | 2/80 = 0.03 |
| gemma4:12b | B | certain_right | unsure | 0.00 (n=40) | 0/80 = 0.00 | 0/80 = 0.00 |
| gemma4:12b | B | perfect_mixed | unsure | 0.96 (n=40) | 71/80 = 0.89 | 58/80 = 0.72 |
| gemma4:12b | B | perfect_mixed | certain | 0.98 (n=40) | 76/80 = 0.95 | 71/80 = 0.89 |
| google:gemini-3.6-flash | A | certain_right | certain | 1.00 (n=1) | 49/80 = 0.61 | 37/80 = 0.46 |
| google:gemini-3.6-flash | A | unsure_right | certain | 0.00 (n=1) | 3/80 = 0.04 | 0/80 = 0.00 |
| google:gemini-3.6-flash | A | unsure_right | unsure | 1.00 (n=1) | 33.50/80 = 0.42 | 13/80 = 0.16 |
| google:gemini-3.6-flash | A | certain_right | unsure | 0.00 (n=1) | 0/80 = 0.00 | 1/80 = 0.01 |
| google:gemini-3.6-flash | A | perfect_mixed | unsure | 1.00 (n=1) | 29/80 = 0.36 | 9/80 = 0.11 |
| google:gemini-3.6-flash | A | perfect_mixed | certain | 1.00 (n=1) | 37/80 = 0.46 | 14/80 = 0.17 |
| google:gemini-3.6-flash | B | certain_right | certain | 1.00 (n=40) | 60/80 = 0.75 | - |
| google:gemini-3.6-flash | B | unsure_right | certain | 0.00 (n=40) | 2/80 = 0.03 | - |
| google:gemini-3.6-flash | B | unsure_right | unsure | 1.00 (n=40) | 59/80 = 0.74 | - |
| google:gemini-3.6-flash | B | certain_right | unsure | 0.00 (n=40) | 2/80 = 0.03 | - |
| google:gemini-3.6-flash | B | perfect_mixed | unsure | 1.00 (n=40) | - | - |
| google:gemini-3.6-flash | B | perfect_mixed | certain | 1.00 (n=40) | - | - |
| ministral-3:8b | A | certain_right | certain | 1.00 (n=1) | 37/80 = 0.46 | 19/80 = 0.24 |
| ministral-3:8b | A | unsure_right | certain | 0.00 (n=1) | 15/80 = 0.19 | 3/80 = 0.04 |
| ministral-3:8b | A | unsure_right | unsure | 1.00 (n=1) | 4/80 = 0.05 | 1/80 = 0.01 |
| ministral-3:8b | A | certain_right | unsure | 0.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| ministral-3:8b | A | perfect_mixed | unsure | 1.00 (n=1) | 22/80 = 0.28 | 9/80 = 0.11 |
| ministral-3:8b | A | perfect_mixed | certain | 1.00 (n=1) | 49/80 = 0.61 | 27/80 = 0.34 |
| ministral-3:8b | B | certain_right | certain | 0.99 (n=40) | 21/80 = 0.26 | 7/80 = 0.09 |
| ministral-3:8b | B | unsure_right | certain | 0.00 (n=40) | 14/80 = 0.17 | 7/80 = 0.09 |
| ministral-3:8b | B | unsure_right | unsure | 0.97 (n=40) | 13/80 = 0.16 | 5/80 = 0.06 |
| ministral-3:8b | B | certain_right | unsure | 0.01 (n=40) | 10/80 = 0.12 | 1/80 = 0.01 |
| ministral-3:8b | B | perfect_mixed | unsure | 1.00 (n=40) | 38/80 = 0.47 | 18/80 = 0.23 |
| ministral-3:8b | B | perfect_mixed | certain | 1.00 (n=40) | 47/80 = 0.59 | 25/80 = 0.31 |
| openai:gpt-6-luna | A | certain_right | certain | 1.00 (n=1) | 13.50/80 = 0.17 | 4/80 = 0.05 |
| openai:gpt-6-luna | A | unsure_right | certain | 0.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| openai:gpt-6-luna | A | unsure_right | unsure | 1.00 (n=1) | 11.50/80 = 0.14 | 2/80 = 0.03 |
| openai:gpt-6-luna | A | certain_right | unsure | 0.00 (n=1) | 5/80 = 0.06 | 1/80 = 0.01 |
| openai:gpt-6-luna | A | perfect_mixed | unsure | 1.00 (n=1) | 24/80 = 0.30 | 11/80 = 0.14 |
| openai:gpt-6-luna | A | perfect_mixed | certain | 1.00 (n=1) | 26/80 = 0.33 | 12/80 = 0.15 |
| openai:gpt-6-luna | B | certain_right | certain | 0.96 (n=40) | 12/80 = 0.15 | 4/80 = 0.05 |
| openai:gpt-6-luna | B | unsure_right | certain | 0.00 (n=40) | 11/80 = 0.14 | 5/80 = 0.06 |
| openai:gpt-6-luna | B | unsure_right | unsure | 1.00 (n=40) | 18/80 = 0.23 | 5/80 = 0.06 |
| openai:gpt-6-luna | B | certain_right | unsure | 0.00 (n=40) | 8/80 = 0.10 | 2/80 = 0.03 |
| openai:gpt-6-luna | B | perfect_mixed | unsure | 1.00 (n=40) | 32/80 = 0.40 | 17/80 = 0.21 |
| openai:gpt-6-luna | B | perfect_mixed | certain | 0.95 (n=40) | 33/80 = 0.41 | 21/80 = 0.26 |
| openai:gpt-6-sol | A | certain_right | certain | 1.00 (n=1) | 48/80 = 0.60 | 16/80 = 0.20 |
| openai:gpt-6-sol | A | unsure_right | certain | 0.00 (n=1) | 7/80 = 0.09 | 2/80 = 0.03 |
| openai:gpt-6-sol | A | unsure_right | unsure | 1.00 (n=1) | 42/80 = 0.53 | 10/80 = 0.12 |
| openai:gpt-6-sol | A | certain_right | unsure | 0.00 (n=1) | 5/80 = 0.06 | 0/80 = 0.00 |
| openai:gpt-6-sol | A | perfect_mixed | unsure | 1.00 (n=1) | 32/80 = 0.40 | 6/80 = 0.07 |
| openai:gpt-6-sol | A | perfect_mixed | certain | 1.00 (n=1) | 35/80 = 0.44 | 8/80 = 0.10 |
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
| openrouter:meta-llama/llama-4-maverick | A | certain_right | certain | 1.00 (n=1) | 58/80 = 0.72 | 19/80 = 0.24 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right | certain | 0.00 (n=1) | 4/80 = 0.05 | 1/80 = 0.01 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right | unsure | 1.00 (n=1) | 3/80 = 0.04 | 0/80 = 0.00 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right | unsure | 0.00 (n=1) | 8/80 = 0.10 | 1/80 = 0.01 |
| openrouter:meta-llama/llama-4-maverick | A | perfect_mixed | unsure | 1.00 (n=1) | 39/80 = 0.49 | 9/80 = 0.11 |
| openrouter:meta-llama/llama-4-maverick | A | perfect_mixed | certain | 1.00 (n=1) | 70/80 = 0.88 | 41/80 = 0.51 |
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
| qwen3.5:9b | A | certain_right | certain | 1.00 (n=1) | 35/80 = 0.44 | 29/80 = 0.36 |
| qwen3.5:9b | A | unsure_right | certain | 0.00 (n=1) | 27/80 = 0.34 | 24/80 = 0.30 |
| qwen3.5:9b | A | unsure_right | unsure | 0.50 (n=1) | 14/80 = 0.17 | 5/80 = 0.06 |
| qwen3.5:9b | A | certain_right | unsure | 0.00 (n=1) | 9/80 = 0.11 | 3/80 = 0.04 |
| qwen3.5:9b | A | perfect_mixed | unsure | 1.00 (n=1) | 15/80 = 0.19 | 9/80 = 0.11 |
| qwen3.5:9b | A | perfect_mixed | certain | 1.00 (n=1) | 43/80 = 0.54 | 35/80 = 0.44 |
| qwen3.5:9b | B | certain_right | certain | 0.74 (n=40) | 13/80 = 0.16 | 8/80 = 0.10 |
| qwen3.5:9b | B | unsure_right | certain | 0.14 (n=40) | 10/80 = 0.12 | 4/80 = 0.05 |
| qwen3.5:9b | B | unsure_right | unsure | 0.51 (n=40) | 10/80 = 0.12 | 1/80 = 0.01 |
| qwen3.5:9b | B | certain_right | unsure | 0.00 (n=40) | 5/80 = 0.06 | 2/80 = 0.03 |
| qwen3.5:9b | B | perfect_mixed | unsure | 0.59 (n=40) | 9/80 = 0.11 | 6/80 = 0.07 |
| qwen3.5:9b | B | perfect_mixed | certain | 0.99 (n=40) | 17/80 = 0.21 | 13/80 = 0.16 |
