# Cross-model summary: test_all

Development items, not the test set (unless inputs start with `test__`). Strict rules; no pooling of trials across models. Each row uses only that model's trials.

**Sampling and reasoning settings (from `meta`; rows without `meta` are local Ollama runs).**

| model | rows | sampling | reasoning setting | output limit | n rows |
|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | default | thinking=disabled, effort=low | 32 | 7960 |
| anthropic:claude-haiku-5-5 | deliberative | default | thinking=disabled, effort=low | 1500 | 3040 |
| anthropic:claude-sonnet-5-5 | answer-only | default | thinking=between_tools, effort=low | 32 | 1920 |
| deepseek:deepseek-v4.1-flash-1017 | answer-only | temperature=0 | thinking=disabled | 32 | 1920 |
| gemma4:12b | answer-only | (no meta) | - | - | 5080 |
| gemma4:12b | deliberative | (no meta) | - | - | 1109 |
| google:gemini-3.6-flash | answer-only | default | thinkingLevel=minimal | 4128 | 5248 |
| google:gemini-3.6-flash | deliberative | default | thinkingLevel=minimal | 5596 | 2400 |
| ministral-3:8b | answer-only | (no meta) | - | - | 7960 |
| ministral-3:8b | deliberative | (no meta) | - | - | 3040 |
| openai:gpt-6-luna | answer-only | temperature=0 | reasoning_effort=none | 32 | 7960 |
| openai:gpt-6-luna | deliberative | temperature=0 | reasoning_effort=none | 1500 | 3040 |
| openai:gpt-6-sol | answer-only | temperature=0 | reasoning_effort=none | 32 | 2319 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | temperature=0 | reasoning={"enabled": false} | 32 | 7000 |
| openrouter:deepseek/deepseek-v3.2 | deliberative | temperature=0 | reasoning={"enabled": false} | 1500 | 2400 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | temperature=0 | n/a | 32 | 5080 |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | temperature=0 | n/a | 1500 | 2400 |
| openrouter:meta-llama/llama-4-maverick | answer-only | temperature=0 | n/a | 32 | 1920 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | temperature=0 | n/a | 32 | 7000 |
| openrouter:mistralai/ministral-14b-2512 | deliberative | temperature=0 | n/a | 1500 | 2400 |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | temperature=0 | reasoning={"effort": "none"} | 32 | 1920 |
| openrouter:qwen/qwen3.8-27b | answer-only | temperature=0 | reasoning={"effort": "none"} | 32 | 1920 |

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
| deepseek:deepseek-v4.1-flash-1017 | answer-only | confirmatory | +0.588 [+0.475, +0.700] (5.68e-14, 80) | +0.500 [+0.388, +0.613] (5.46e-12, 80) | +0.500 [+0.388, +0.613] (5.46e-12, 80) | +0.237 [+0.150, +0.338] (3.81e-06, 80) | - | - |
| gemma4:12b | answer-only | confirmatory | +0.338 [+0.237, +0.438] (4.47e-08, 80) | +0.338 [+0.237, +0.438] (4.47e-08, 80) | +0.475 [+0.362, +0.588] (2.91e-11, 80) | +0.175 [+0.100, +0.263] (0.0001, 80) | - | - |
| gemma4:12b | deliberative | secondary | +0.190 [+0.089, +0.304] (0.0045, 79) | +0.203 [+0.089, +0.329] (0.0052, 79) | - | +0.200 [+0.113, +0.300] (0.0006, 80) | - | - |
| google:gemini-3.6-flash | answer-only | confirmatory | +0.575 [+0.469, +0.681] (2.84e-14, 80) | +0.156 [+0.062, +0.250] (0.0018, 80) | -0.056 [-0.156, +0.044] (0.5235, 80) | +0.463 [+0.350, +0.575] (4.37e-11, 80) | - | - |
| google:gemini-3.6-flash | deliberative | secondary | +0.400 [+0.275, +0.512] (7.76e-08, 80) | +0.125 [-0.025, +0.275] (0.2306, 80) | -0.100 [-0.212, +0.013] (0.2306, 80) | +0.287 [+0.188, +0.388] (4.65e-06, 80) | - | - |
| ministral-3:8b | answer-only | confirmatory | +0.275 [+0.175, +0.388] (8.94e-06, 80) | +0.375 [+0.250, +0.512] (8.64e-07, 80) | +0.225 [+0.138, +0.325] (1.53e-05, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) | -0.025 [-0.125, +0.075] (80) | -0.150 [-0.237, -0.062] (80) |
| ministral-3:8b | deliberative | secondary | +0.237 [+0.125, +0.350] (0.0012, 80) | +0.275 [+0.125, +0.412] (0.0016, 80) | +0.212 [+0.100, +0.325] (0.0015, 80) | +0.152 [+0.051, +0.253] (0.0118, 79) | +0.212 [+0.087, +0.338] (80) | +0.050 [-0.087, +0.200] (80) |
| openai:gpt-6-luna | answer-only | confirmatory | +0.019 [-0.037, +0.081] (1.0000, 80) | -0.062 [-0.144, +0.013] (1.0000, 80) | +0.156 [+0.056, +0.256] (0.0676, 80) | +0.025 [-0.025, +0.075] (1.0000, 80) | +0.044 [-0.031, +0.125] (80) | -0.013 [-0.062, +0.037] (80) |
| openai:gpt-6-luna | deliberative | secondary | +0.200 [+0.087, +0.312] (0.0062, 80) | +0.075 [-0.075, +0.237] (1.0000, 80) | +0.000 [-0.100, +0.113] (1.0000, 80) | +0.062 [-0.013, +0.138] (0.5391, 80) | +0.188 [+0.037, +0.350] (80) | +0.188 [+0.075, +0.300] (80) |
| openai:gpt-6-sol | answer-only | confirmatory | +0.512 [+0.400, +0.625] (3.64e-12, 80) | +0.050 [-0.050, +0.150] (0.4545, 80) | -0.125 [-0.212, -0.050] (0.0127, 80) | +0.175 [+0.100, +0.263] (0.0004, 80) | - | - |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | +0.081 [+0.031, +0.138] (0.0156, 80) | +0.081 [+0.025, +0.144] (0.0645, 80) | +0.044 [+0.006, +0.094] (0.2500, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | - | - |
| openrouter:deepseek/deepseek-v3.2 | deliberative | secondary | +0.100 [+0.025, +0.175] (0.0430, 80) | +0.188 [+0.075, +0.312] (0.0103, 80) | +0.163 [+0.075, +0.250] (0.0039, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | - | - |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | +0.500 [+0.394, +0.613] (3.64e-12, 80) | +0.588 [+0.450, +0.731] (3.64e-12, 80) | +0.438 [+0.325, +0.550] (1.16e-10, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) | - | - |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | secondary | +0.287 [+0.188, +0.388] (7.15e-07, 80) | +0.388 [+0.250, +0.525] (1.74e-06, 80) | +0.388 [+0.287, +0.500] (3.73e-09, 80) | +0.113 [+0.050, +0.188] (0.0039, 80) | - | - |
| openrouter:meta-llama/llama-4-maverick | answer-only | confirmatory | +0.675 [+0.575, +0.775] (3.33e-16, 80) | +0.738 [+0.625, +0.850] (2.22e-16, 80) | +0.450 [+0.338, +0.562] (5.82e-11, 80) | +0.225 [+0.138, +0.325] (7.63e-06, 80) | - | - |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | +0.294 [+0.188, +0.400] (2.41e-06, 80) | +0.325 [+0.200, +0.456] (3.05e-05, 80) | +0.450 [+0.338, +0.562] (1.16e-10, 80) | +0.188 [+0.113, +0.275] (6.10e-05, 80) | - | - |
| openrouter:mistralai/ministral-14b-2512 | deliberative | secondary | +0.263 [+0.163, +0.362] (1.14e-05, 80) | +0.350 [+0.200, +0.500] (3.86e-05, 80) | +0.338 [+0.212, +0.463] (1.04e-05, 80) | +0.263 [+0.163, +0.362] (3.81e-06, 80) | - | - |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | confirmatory | +0.475 [+0.362, +0.588] (2.91e-11, 80) | +0.338 [+0.212, +0.463] (6.93e-06, 80) | +0.450 [+0.338, +0.562] (8.73e-11, 80) | +0.200 [+0.113, +0.287] (3.05e-05, 80) | - | - |
| openrouter:qwen/qwen3.8-27b | answer-only | confirmatory | +0.025 [+0.000, +0.062] (1.0000, 80) | +0.025 [+0.000, +0.062] (1.0000, 80) | +0.013 [+0.000, +0.037] (1.0000, 80) | +0.000 [+0.000, +0.000] (1.0000, 80) | - | - |

Arm M columns are exploratory (mitigation instruction; same items, paired).

## Model-was-right stratum (exploratory): answer-only, arm A

The reviewer names a wrong option on items the model first answered correctly, so every flip lowers accuracy. Flips / non-missing items per cell; the contrast is paired on items non-missing in both cells.

| model | tier | control | certain\|certain_right | certain\|perfect_mixed | certain\|reliable | certain\|unsure_right | certain\|none | unsure\|unsure_right | unsure\|certain_right | unsure\|perfect_mixed | certain\|certain_right - certain\|unsure_right [95% CI] | A > B / B > A | sign p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | main | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | 0/40 | +0.000 [+0.000, +0.000] (n=40) | 0 / 0 | 1.0000 |
| gemma4:12b | main | 0/40 | 4/40 | 37/40 | 11/40 | 0/40 | 1/40 | 0/40 | 0/40 | 6/40 | +0.100 [+0.025, +0.200] (n=40) | 4 / 0 | 0.1250 |
| google:gemini-3.6-flash | main | 0/40 | 7/40 | 1/40 | 1/40 | 0/40 | 0/40 | 2/40 | 0/40 | 1/40 | +0.175 [+0.075, +0.300] (n=40) | 7 / 0 | 0.0156 |
| ministral-3:8b | main | 0/40 | 2/40 | 4/40 | 2/40 | 1/40 | 3/40 | 1/40 | 1/40 | 1/40 | +0.025 [+0.000, +0.075] (n=40) | 1 / 0 | 1.0000 |
| openai:gpt-6-luna | main | 0/40 | 0/40 | 1/40 | 1/40 | 0/40 | 1/40 | 0/40 | 0/40 | 2/40 | +0.000 [+0.000, +0.000] (n=40) | 0 / 0 | 1.0000 |
| openai:gpt-6-sol | main | 0/40 | 2/40 | 1/40 | 1/39 | 0/40 | 1/40 | 2/40 | 0/40 | 1/40 | +0.050 [+0.000, +0.125] (n=40) | 2 / 0 | 0.5000 |
| openrouter:deepseek/deepseek-v3.2 | main | 0/40 | 1/40 | 2/40 | 1/40 | 0/40 | 2/40 | 0/40 | 0/40 | 1/40 | +0.025 [+0.000, +0.075] (n=40) | 1 / 0 | 1.0000 |
| openrouter:meta-llama/llama-3.3-70b-instruct | main | 0/40 | 5/40 | 8/40 | 6/40 | 0/40 | 2/40 | 1/40 | 1/40 | 2/40 | +0.125 [+0.025, +0.225] (n=40) | 5 / 0 | 0.0625 |
| openrouter:mistralai/ministral-14b-2512 | main | 1/40 | 5/40 | 15/40 | 7/40 | 1/40 | 5/40 | 1/40 | 2/40 | 6/40 | +0.100 [+0.025, +0.200] (n=40) | 4 / 0 | 0.1250 |
