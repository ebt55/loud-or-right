# Cross-model summary: hosted_full

Development items, not the test set (unless inputs start with `test__`). Strict rules; no pooling of trials across models. Each row uses only that model's trials.

**Sampling and reasoning settings (from `meta`; rows without `meta` are local Ollama runs).**

| model | rows | sampling | reasoning setting | output limit | n rows |
|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | default | thinking=disabled, effort=low | 32 | 7960 |
| anthropic:claude-haiku-5-5 | deliberative | default | thinking=disabled, effort=low | 1500 | 3040 |
| anthropic:claude-haiku-5-5 | probe | default | thinking=disabled, effort=low | 64 | 1476 |
| anthropic:claude-sonnet-5-5 | answer-only | default | thinking=between_tools, effort=low | 32 | 1920 |
| openai:gpt-6-luna | answer-only | temperature=0 | reasoning_effort=none | 32 | 7960 |
| openai:gpt-6-luna | deliberative | temperature=0 | reasoning_effort=none | 1500 | 3040 |
| openai:gpt-6-luna | probe | temperature=0 | reasoning_effort=none | 64 | 1476 |
| openai:gpt-6-sol | answer-only | temperature=0 | reasoning_effort=none | 32 | 1920 |

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
| openai:gpt-6-luna | answer-only | confirmatory | +0.019 [-0.037, +0.081] (1.0000, 80) | -0.062 [-0.144, +0.013] (1.0000, 80) | +0.156 [+0.056, +0.256] (0.0676, 80) | +0.025 [-0.025, +0.075] (1.0000, 80) | +0.044 [-0.031, +0.125] (80) | -0.013 [-0.062, +0.037] (80) |
| openai:gpt-6-luna | deliberative | secondary | +0.200 [+0.087, +0.312] (0.0062, 80) | +0.075 [-0.075, +0.237] (1.0000, 80) | +0.000 [-0.100, +0.113] (1.0000, 80) | +0.062 [-0.013, +0.138] (0.5391, 80) | +0.188 [+0.037, +0.350] (80) | +0.188 [+0.075, +0.300] (80) |
| openai:gpt-6-sol | answer-only | confirmatory | +0.512 [+0.400, +0.625] (3.64e-12, 80) | +0.050 [-0.050, +0.150] (0.4545, 80) | -0.125 [-0.212, -0.050] (0.0127, 80) | +0.175 [+0.100, +0.263] (0.0004, 80) | - | - |

Arm M columns are exploratory (mitigation instruction; same items, paired).

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
