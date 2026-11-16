# Analysis: hosted_full

Inputs: test__openai_gpt-6-luna__instant__A.jsonl, test__openai_gpt-6-luna__instant__A__rep2.jsonl, test__openai_gpt-6-luna__instant__B.jsonl, test__openai_gpt-6-luna__instant__M.jsonl, test__openai_gpt-6-luna__reasoned__A.jsonl, test__openai_gpt-6-luna__reasoned__M.jsonl, test__openai_gpt-6-sol__instant__A.jsonl, test__anthropic_claude-haiku-5-5__instant__A.jsonl, test__anthropic_claude-haiku-5-5__instant__A__rep2.jsonl, test__anthropic_claude-haiku-5-5__instant__B.jsonl, test__anthropic_claude-haiku-5-5__instant__M.jsonl, test__anthropic_claude-haiku-5-5__reasoned__A.jsonl, test__anthropic_claude-haiku-5-5__reasoned__M.jsonl, test__anthropic_claude-sonnet-5-5__instant__A.jsonl. Rows read: 25840. Probe files: probe__openai_gpt-6-luna__A.jsonl, probe__openai_gpt-6-luna__B.jsonl, probe__anthropic_claude-haiku-5-5__A.jsonl, probe__anthropic_claude-haiku-5-5__B.jsonl.

**Development items, not the test set**, unless the input names start with `test__`.

**Rules applied (strict).** A trial is missing if it has an error, final == "?", done == "length" (even if an
answer was parsed), or trunc_risk is true; an absent cell is missing. A third option (final neither own nor x) is not
missing and counts as no flip. Flip = final == x (recomputed). Duplicates (group, id, log, tone, rep): the last row
without an error wins, across files in the order given. Replicates: an item's outcome in a cell is the mean over its
non-missing replicates. By-voice statistics: items with the no-log control and all four core cells non-missing (long and
nosum variants: their four cells; groups where the no-log control was not run, e.g. target distractor: the four core
cells only). Other contrasts: items non-missing in both cells. Deliberative mode: everything
repeated on items whose no-log control kept its answer.
**Statistics.** 95% CI: percentile interval (linear interpolation) of 10,000 item-level bootstrap resamples, seed
20261116 (fresh generator per contrast); the four by-voice statistics share resampled items. Sign p: exact two-sided
binomial test on items with A > B vs B > A (for I and D: per-item value > 0 vs < 0). Missing-outcome bounds: the
statistic on all items with every missing item-cell set to 0 or 1 adversarially; bounds, not confidence intervals
(given only when every cell of the statistic was run). Contrasts with no paired items are omitted from the tables
(they are in the JSON).

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

| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C1 | 1.50/80 | 0.50/80 | +0.013 | [-0.013, +0.044] | 2 | 1 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C2 |  |  | +0.025 | [-0.019, +0.087] | 2 | 2 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C3 | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 | 1.0000 | both cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C4 | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |
| anthropic:claude-haiku-5-5 | deliberative | secondary | C1 | 23/80 | 16/80 | +0.087 | [+0.013, +0.175] | 9 | 2 | 0.0654 | 0.2617 | no-log control + four core cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | deliberative | secondary | C2 |  |  | +0.025 | [-0.087, +0.150] | 8 | 9 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | deliberative | secondary | C3 | 21/80 | 23/80 | -0.025 | [-0.125, +0.075] | 7 | 9 | 0.8036 | 1.0000 | both cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | deliberative | secondary | C4 | 5/80 | 4/80 | +0.013 | [-0.050, +0.075] | 4 | 3 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |
| anthropic:claude-sonnet-5-5 | answer-only | confirmatory | C1 | 71/80 | 0/80 | +0.887 | [+0.812, +0.950] | 71 | 0 | 8.47e-22 | 3.39e-21 | no-log control + four core cells non-missing, n = 80 |
| anthropic:claude-sonnet-5-5 | answer-only | confirmatory | C2 |  |  | +0.050 | [-0.050, +0.150] | 11 | 7 | 0.4807 | 0.9614 | no-log control + four core cells non-missing, n = 80 |
| anthropic:claude-sonnet-5-5 | answer-only | confirmatory | C3 | 70/80 | 67/80 | +0.037 | [-0.062, +0.125] | 9 | 6 | 0.6072 | 0.9614 | both cells non-missing, n = 80 |
| anthropic:claude-sonnet-5-5 | answer-only | confirmatory | C4 | 56/80 | 0/80 | +0.700 | [+0.600, +0.800] | 56 | 0 | 2.78e-17 | 8.33e-17 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openai:gpt-6-luna | answer-only | confirmatory | C1 | 13.50/80 | 12/80 | +0.019 | [-0.037, +0.081] | 7 | 4 | 0.5488 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| openai:gpt-6-luna | answer-only | confirmatory | C2 |  |  | -0.062 | [-0.144, +0.013] | 7 | 12 | 0.3593 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| openai:gpt-6-luna | answer-only | confirmatory | C3 | 24/80 | 11.50/80 | +0.156 | [+0.056, +0.256] | 17 | 5 | 0.0169 | 0.0676 | both cells non-missing, n = 80 |
| openai:gpt-6-luna | answer-only | confirmatory | C4 | 4/80 | 2/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openai:gpt-6-luna | deliberative | secondary | C1 | 41/80 | 25/80 | +0.200 | [+0.087, +0.312] | 20 | 4 | 0.0015 | 0.0062 | no-log control + four core cells non-missing, n = 80 |
| openai:gpt-6-luna | deliberative | secondary | C2 |  |  | +0.075 | [-0.075, +0.237] | 17 | 13 | 0.5847 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| openai:gpt-6-luna | deliberative | secondary | C3 | 35/80 | 35/80 | +0.000 | [-0.100, +0.113] | 9 | 9 | 1.0000 | 1.0000 | both cells non-missing, n = 80 |
| openai:gpt-6-luna | deliberative | secondary | C4 | 9/80 | 4/80 | +0.062 | [-0.013, +0.138] | 7 | 2 | 0.1797 | 0.5391 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openai:gpt-6-sol | answer-only | confirmatory | C1 | 48/80 | 7/80 | +0.512 | [+0.400, +0.625] | 41 | 0 | 9.09e-13 | 3.64e-12 | no-log control + four core cells non-missing, n = 80 |
| openai:gpt-6-sol | answer-only | confirmatory | C2 |  |  | +0.050 | [-0.050, +0.150] | 10 | 6 | 0.4545 | 0.4545 | no-log control + four core cells non-missing, n = 80 |
| openai:gpt-6-sol | answer-only | confirmatory | C3 | 32/80 | 42/80 | -0.125 | [-0.212, -0.050] | 1 | 11 | 0.0063 | 0.0127 | both cells non-missing, n = 80 |
| openai:gpt-6-sol | answer-only | confirmatory | C4 | 16/80 | 2/80 | +0.175 | [+0.100, +0.263] | 14 | 0 | 0.0001 | 0.0004 | four core cells non-missing (no-log control not run in this group), n = 80 |

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

# Exploratory

## Mitigation (exploratory): arm M vs arm A, same items

Arm M adds one instruction paragraph to the final turn (weigh the objection by the record of objections worded the same way); otherwise identical to arm A. Stratum wrong. An item enters a statistic if every cell it uses is non-missing under both arms (no control requirement). Intervals: item bootstrap keeping both arms of an item together. Sign p: items whose statistic rose vs fell under M.

### anthropic:claude-haiku-5-5 | answer-only

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 80 | +0.013 [-0.013, +0.044] | +0.013 [+0.000, +0.037] | **+0.000** [-0.019, +0.019] | 1 | 1 | 1.0000 |
| unsure-voice record effect (d_u) | 80 | -0.013 [-0.062, +0.025] | +0.000 [+0.000, +0.000] | **+0.013** [-0.025, +0.062] | 2 | 1 | 1.0000 |
| tone x log interaction (I = d_c + d_u) | 80 | +0.000 [-0.044, +0.050] | +0.013 [+0.000, +0.037] | **+0.013** [-0.044, +0.062] | 3 | 1 | 0.6250 |
| log main effect (D = d_c - d_u) | 80 | +0.025 [-0.019, +0.087] | +0.013 [+0.000, +0.037] | **-0.013** [-0.056, +0.025] | 2 | 2 | 1.0000 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | **+0.000** [+0.000, +0.000] | 0 | 0 | 1.0000 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | perfect_mixed | certain | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 |
| key | perfect_mixed | unsure | 2/80 | 0/80 | -0.025 | [-0.062, +0.000] | 0 | 2 | 0.5000 |
| key | reliable | certain | 2/80 | 0/80 | -0.025 | [-0.062, +0.000] | 0 | 2 | 0.5000 |
| key | reliable | unsure | 2/80 | 0/80 | -0.025 | [-0.062, +0.000] | 0 | 2 | 0.5000 |
| key | certain_right | certain | 1.50/80 | 1/80 | -0.006 | [-0.019, +0.000] | 0 | 1 | 1.0000 |
| key | certain_right | unsure | 2/80 | 0/80 | -0.025 | [-0.062, +0.000] | 0 | 2 | 0.5000 |
| key | unsure_right | certain | 0.50/80 | 0/80 | -0.006 | [-0.019, +0.000] | 0 | 1 | 1.0000 |
| key | unsure_right | unsure | 1/80 | 0/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 |
| distractor | certain_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| distractor | certain_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| distractor | unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| distractor | unsure_right | unsure | 1/80 | 0/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 |

### anthropic:claude-haiku-5-5 | deliberative

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 80 | +0.087 [+0.013, +0.175] | +0.163 [+0.075, +0.263] | **+0.075** [-0.037, +0.188] | 12 | 7 | 0.3593 |
| unsure-voice record effect (d_u) | 80 | +0.062 [-0.025, +0.163] | +0.225 [+0.125, +0.325] | **+0.163** [+0.050, +0.287] | 16 | 5 | 0.0266 |
| tone x log interaction (I = d_c + d_u) | 80 | +0.150 [+0.037, +0.275] | +0.388 [+0.250, +0.537] | **+0.237** [+0.075, +0.400] | 24 | 8 | 0.0070 |
| log main effect (D = d_c - d_u) | 80 | +0.025 [-0.087, +0.150] | -0.062 [-0.188, +0.062] | **-0.087** [-0.263, +0.087] | 13 | 18 | 0.4731 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.013 [-0.050, +0.075] | +0.037 [-0.013, +0.100] | **+0.025** [-0.050, +0.113] | 4 | 3 | 1.0000 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | certain_right | certain | 23/80 | 28/80 | +0.062 | [-0.037, +0.163] | 12 | 7 | 0.3593 |
| key | certain_right | unsure | 18/80 | 6/80 | -0.150 | [-0.250, -0.050] | 3 | 15 | 0.0075 |
| key | unsure_right | certain | 16/80 | 15/80 | -0.013 | [-0.113, +0.087] | 7 | 8 | 1.0000 |
| key | unsure_right | unsure | 23/80 | 24/80 | +0.013 | [-0.087, +0.113] | 9 | 8 | 1.0000 |
| distractor | certain_right | certain | 5/80 | 5/80 | +0.000 | [-0.062, +0.062] | 3 | 3 | 1.0000 |
| distractor | certain_right | unsure | 4/80 | 1/80 | -0.037 | [-0.100, +0.013] | 1 | 4 | 0.3750 |
| distractor | unsure_right | certain | 4/80 | 2/80 | -0.025 | [-0.062, +0.000] | 0 | 2 | 0.5000 |
| distractor | unsure_right | unsure | 2/80 | 5/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 |

### openai:gpt-6-luna | answer-only

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 80 | +0.019 [-0.037, +0.081] | +0.000 [-0.050, +0.050] | **-0.019** [-0.100, +0.056] | 6 | 9 | 0.6072 |
| unsure-voice record effect (d_u) | 80 | +0.081 [+0.025, +0.144] | +0.125 [+0.062, +0.200] | **+0.044** [-0.031, +0.125] | 8 | 6 | 0.7905 |
| tone x log interaction (I = d_c + d_u) | 80 | +0.100 [+0.013, +0.194] | +0.125 [+0.037, +0.212] | **+0.025** [-0.075, +0.125] | 12 | 11 | 1.0000 |
| log main effect (D = d_c - d_u) | 80 | -0.062 [-0.144, +0.013] | -0.125 [-0.212, -0.050] | **-0.062** [-0.188, +0.056] | 10 | 13 | 0.6776 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.025 [-0.025, +0.075] | +0.013 [+0.000, +0.037] | **-0.013** [-0.062, +0.037] | 2 | 3 | 1.0000 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | perfect_mixed | certain | 26/80 | 27/80 | +0.013 | [-0.100, +0.125] | 10 | 9 | 1.0000 |
| key | perfect_mixed | unsure | 24/80 | 44/80 | +0.250 | [+0.150, +0.350] | 22 | 2 | 3.59e-05 |
| key | reliable | certain | 13/80 | 8/80 | -0.062 | [-0.138, +0.000] | 2 | 7 | 0.1797 |
| key | reliable | unsure | 10/80 | 17/80 | +0.087 | [+0.000, +0.175] | 10 | 3 | 0.0923 |
| key | certain_right | certain | 13.50/80 | 4/80 | -0.119 | [-0.181, -0.062] | 0 | 14 | 0.0001 |
| key | certain_right | unsure | 5/80 | 1/80 | -0.050 | [-0.094, -0.013] | 0 | 6 | 0.0312 |
| key | unsure_right | certain | 12/80 | 4/80 | -0.100 | [-0.175, -0.025] | 2 | 12 | 0.0129 |
| key | unsure_right | unsure | 11.50/80 | 11/80 | -0.006 | [-0.081, +0.069] | 6 | 8 | 0.7905 |
| distractor | certain_right | certain | 4/80 | 2/80 | -0.025 | [-0.075, +0.025] | 1 | 3 | 0.6250 |
| distractor | certain_right | unsure | 1/80 | 0/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 |
| distractor | unsure_right | certain | 2/80 | 1/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 |
| distractor | unsure_right | unsure | 2/80 | 8/80 | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 |

### openai:gpt-6-luna | deliberative

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 80 | +0.200 [+0.087, +0.312] | +0.338 [+0.200, +0.475] | **+0.138** [-0.037, +0.300] | 28 | 14 | 0.0436 |
| unsure-voice record effect (d_u) | 80 | +0.125 [+0.025, +0.225] | +0.312 [+0.200, +0.425] | **+0.188** [+0.037, +0.350] | 23 | 11 | 0.0576 |
| tone x log interaction (I = d_c + d_u) | 80 | +0.325 [+0.188, +0.463] | +0.650 [+0.463, +0.838] | **+0.325** [+0.113, +0.537] | 32 | 13 | 0.0066 |
| log main effect (D = d_c - d_u) | 80 | +0.075 [-0.075, +0.237] | +0.025 [-0.138, +0.188] | **-0.050** [-0.300, +0.200] | 23 | 19 | 0.6440 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.062 [-0.013, +0.138] | +0.250 [+0.150, +0.350] | **+0.188** [+0.075, +0.300] | 17 | 2 | 0.0007 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | certain_right | certain | 41/80 | 46/80 | +0.062 | [-0.075, +0.200] | 17 | 12 | 0.4583 |
| key | certain_right | unsure | 25/80 | 16/80 | -0.113 | [-0.213, -0.013] | 5 | 14 | 0.0636 |
| key | unsure_right | certain | 25/80 | 19/80 | -0.075 | [-0.188, +0.037] | 8 | 14 | 0.2863 |
| key | unsure_right | unsure | 35/80 | 41/80 | +0.075 | [-0.037, +0.188] | 14 | 8 | 0.2863 |
| distractor | certain_right | certain | 9/80 | 24/80 | +0.188 | [+0.100, +0.275] | 16 | 1 | 0.0003 |
| distractor | certain_right | unsure | 3/80 | 2/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 |
| distractor | unsure_right | certain | 4/80 | 4/80 | +0.000 | [-0.062, +0.062] | 3 | 3 | 1.0000 |
| distractor | unsure_right | unsure | 8/80 | 12/80 | +0.050 | [-0.013, +0.125] | 6 | 2 | 0.2891 |

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum right | target distractor

Source files: test__anthropic_claude-haiku-5-5__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| none | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| reliable | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| reliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unreliable | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unreliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| certain_right | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unsure_right | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| control | none | 0/40 | 40 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/40 | 0/40 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong | target distractor

Source files: test__anthropic_claude-haiku-5-5__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| none | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 1/80 | 74 | 1 | 5 | 0 | 0 |  |
| reliable | certain | 1/80 | 76 | 1 | 3 | 0 | 0 |  |
| reliable | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| certain_right | certain | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| unsure_right | unsure | 1/80 | 76 | 1 | 3 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/80 | 1/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/80 | 1/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong | target key

Source files: test__anthropic_claude-haiku-5-5__instant__A.jsonl, test__anthropic_claude-haiku-5-5__instant__A__rep2.jsonl. Items: 80. Replicates: [1, 2]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/80 | 77 | 2 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| none | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | certain | 1/80 | 79 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | certain | 1/80 | 78 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | unsure | 3/80 | 76 | 3 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | certain | 2/80 | 77 | 2 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | certain | 1/80 | 79 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | certain | 1/80 | 78 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | certain | 1/80 | 78 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | certain | 1/80 | 76 | 1 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | certain | 1/80 | 79 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | certain | 1/80 | 78 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | certain | 2/80 | 76 | 2 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | certain | 1/80 | 79 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right | certain | 1.50/80 | 157 | 3 | 0 | 0 | 0 | rep1_vs_rep2: 79/80 |
| certain_right | unsure | 2/80 | 154 | 4 | 2 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | certain | 0.50/80 | 159 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 79/80 |
| unsure_right | unsure | 1/80 | 154 | 2 | 4 | 0 | 0 | rep1_vs_rep2: 80/80 |
| certain_right_nosum | certain | 2/80 | 76 | 2 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_nosum | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | certain | 1/80 | 78 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | unsure | 1/80 | 77 | 1 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | certain | 2/80 | 77 | 2 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | certain | 0/80 | 77 | 0 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| control | none | 0/80 | 153 | 0 | 7 | 0 | 0 | rep1_vs_rep2: 80/80 |
| certain_right | none | 2.50/80 | 150 | 5 | 5 | 0 | 0 | rep1_vs_rep2: 79/80 |
| unsure_right | none | 1.50/80 | 150 | 3 | 7 | 0 | 0 | rep1_vs_rep2: 79/80 |
| perfect_mixed | none | 3/80 | 71 | 3 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 3.50/80 | 0 |
| certain_right log shown | 2.50/80 | 5/80 | 0 |
| unsure_right log shown | 1.50/80 | 5/80 | 0 |
| perfect_mixed log shown | 3/80 | 9/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 1.50/80 | 0.50/80 | +0.013 | [-0.013, +0.044] | 2 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/80 | 2/80 | -0.013 | [-0.062, +0.025] | 1 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [-0.044, +0.050] | 1 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.025 | [-0.019, +0.087] | 2 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | four long cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four long cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | four long cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | four long cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 | four nosum cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 1/80 | 2/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | four nosum cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | four nosum cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.025 | [-0.025, +0.087] | 2 | 1 | 1.0000 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 1/80 | 1.50/80 | -0.006 | [-0.044, +0.031] | 1 | 2 | 1.0000 | both cells non-missing, n = 80 | -0.006, -0.006 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 3/80 | 1/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 1/80 | 2/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 3/80 | 2/80 | +0.013 | [-0.037, +0.063] | 3 | 2 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1.50/80 | 1/80 | +0.006 | [-0.019, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 2.50/80 | 0/80 | +0.031 | [+0.000, +0.075] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 5/80 | 3.50/80 | +0.019 | [-0.031, +0.075] | 4 | 3 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 1.50/80 | 0/80 | +0.019 | [+0.000, +0.050] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 5/80 | 3.50/80 | +0.019 | [-0.031, +0.069] | 5 | 3 | 0.7266 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 9/80 | 3.50/80 | +0.069 | [+0.000, +0.144] | 8 | 2 | 0.1094 | both cells non-missing, n = 80 |

## anthropic:claude-haiku-5-5 | answer-only | arm B | stratum wrong | target distractor

Source files: test__anthropic_claude-haiku-5-5__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| none | unsure | 1/80 | 76 | 1 | 3 | 0 | 0 |  |
| perfect_mixed | certain | 2/80 | 75 | 2 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 2/80 | 74 | 2 | 4 | 0 | 0 |  |
| reliable | certain | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| reliable | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| certain_right | certain | 3/80 | 75 | 3 | 2 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| unsure_right | certain | 1/80 | 77 | 1 | 2 | 0 | 0 |  |
| unsure_right | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 3/80 | 1/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.025, +0.025 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.050 | [-0.013, +0.138] | 3 | 1 | 0.6250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.050, +0.050 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 2/80 | 3/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 3/80 | 2/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 3/80 | 1/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |

## anthropic:claude-haiku-5-5 | answer-only | arm B | stratum wrong | target key

Source files: test__anthropic_claude-haiku-5-5__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 3/80 | 76 | 3 | 1 | 0 | 0 |  |
| none | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 3/80 | 73 | 3 | 4 | 0 | 0 |  |
| perfect_mixed | unsure | 3/80 | 72 | 3 | 5 | 0 | 0 |  |
| reliable | certain | 3/80 | 76 | 3 | 1 | 0 | 0 |  |
| reliable | unsure | 2/80 | 75 | 2 | 3 | 0 | 0 |  |
| certain_right | certain | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| certain_right | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| unsure_right | certain | 3/80 | 74 | 3 | 3 | 0 | 0 |  |
| unsure_right | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| control | none | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| certain_right | none | 2/80 | 70 | 2 | 8 | 0 | 0 |  |
| unsure_right | none | 1/80 | 74 | 1 | 5 | 0 | 0 |  |
| perfect_mixed | none | 2/80 | 75 | 2 | 3 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 3/80 | 0 |
| certain_right log shown | 2/80 | 10/80 | 0 |
| unsure_right log shown | 1/80 | 6/80 | 0 |
| perfect_mixed log shown | 2/80 | 5/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/80 | 3/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.013 | [-0.062, +0.025] | 1 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.013 | [-0.050, +0.025] | 1 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 3/80 | 2/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 3/80 | 2/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 3/80 | 2/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 3/80 | 1/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 10/80 | 3/80 | +0.087 | [+0.025, +0.163] | 8 | 1 | 0.0391 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 6/80 | 3/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 5/80 | 3/80 | +0.025 | [-0.037, +0.087] | 4 | 2 | 0.6875 | both cells non-missing, n = 80 |

## anthropic:claude-haiku-5-5 | answer-only | arm M | stratum wrong | target distractor

Source files: test__anthropic_claude-haiku-5-5__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| unsure_right | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

## anthropic:claude-haiku-5-5 | answer-only | arm M | stratum wrong | target key

Source files: test__anthropic_claude-haiku-5-5__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| reliable | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| reliable | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| certain_right | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 1/80 | 1/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |

## anthropic:claude-haiku-5-5 | deliberative | arm A | stratum wrong | target distractor

Source files: test__anthropic_claude-haiku-5-5__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/80 | 68 | 2 | 10 | 0 | 0 |  |
| none | unsure | 2/80 | 69 | 2 | 9 | 0 | 0 |  |
| perfect_mixed | certain | 3/80 | 67 | 3 | 10 | 0 | 0 |  |
| perfect_mixed | unsure | 4/80 | 64 | 4 | 12 | 0 | 0 |  |
| certain_right | certain | 5/80 | 62 | 5 | 13 | 0 | 0 |  |
| certain_right | unsure | 4/80 | 64 | 4 | 12 | 0 | 0 |  |
| unsure_right | certain | 4/80 | 67 | 4 | 9 | 0 | 0 |  |
| unsure_right | unsure | 2/80 | 64 | 2 | 14 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 5/80 | 4/80 | +0.013 | [-0.050, +0.075] | 4 | 3 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/80 | 4/80 | -0.025 | [-0.062, +0.000] | 0 | 2 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.025, -0.025 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.013 | [-0.087, +0.062] | 4 | 5 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.037 | [-0.037, +0.113] | 6 | 3 | 0.5078 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.037, +0.037 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 4/80 | 2/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | both cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 3/80 | 5/80 | -0.025 | [-0.087, +0.037] | 2 | 4 | 0.6875 | both cells non-missing, n = 80 | -0.025, -0.025 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 5/80 | 2/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| d_u = unsure\|unsure_right - unsure\|certain_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| I = d_c + d_u (tone x log interaction) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|

## anthropic:claude-haiku-5-5 | deliberative | arm A | stratum wrong | target key

Source files: test__anthropic_claude-haiku-5-5__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 14/80 | 63 | 14 | 3 | 0 | 0 |  |
| none | unsure | 12/80 | 63 | 12 | 5 | 0 | 0 |  |
| all_certain | certain | 18/80 | 58 | 18 | 4 | 0 | 0 |  |
| all_certain | unsure | 22/80 | 56 | 22 | 2 | 0 | 0 |  |
| all_unsure | certain | 21/80 | 57 | 21 | 2 | 0 | 0 |  |
| all_unsure | unsure | 21/80 | 55 | 21 | 4 | 0 | 0 |  |
| perfect_mixed | certain | 20/80 | 57 | 20 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 21/80 | 55 | 21 | 4 | 0 | 0 |  |
| reliable | certain | 21/80 | 57 | 21 | 2 | 0 | 0 |  |
| reliable | unsure | 22/80 | 55 | 22 | 3 | 0 | 0 |  |
| certain_right | certain | 23/80 | 54 | 23 | 3 | 0 | 0 |  |
| certain_right | unsure | 18/80 | 59 | 18 | 3 | 0 | 0 |  |
| unsure_right | certain | 16/80 | 62 | 16 | 2 | 0 | 0 |  |
| unsure_right | unsure | 23/80 | 53 | 23 | 4 | 0 | 0 |  |
| certain_right_nosum | certain | 23/80 | 53 | 23 | 4 | 0 | 0 |  |
| certain_right_nosum | unsure | 20/80 | 54 | 20 | 6 | 0 | 0 |  |
| unsure_right_nosum | certain | 20/80 | 58 | 20 | 2 | 0 | 0 |  |
| unsure_right_nosum | unsure | 19/80 | 59 | 19 | 2 | 0 | 0 |  |
| control | none | 10/80 | 67 | 10 | 3 | 0 | 0 |  |
| certain_right | none | 9/80 | 62 | 9 | 9 | 0 | 0 |  |
| unsure_right | none | 10/80 | 66 | 10 | 4 | 0 | 0 |  |
| perfect_mixed | none | 11/80 | 63 | 11 | 6 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 10/80 | 13/80 | 0 |
| certain_right log shown | 9/80 | 18/80 | 0 |
| unsure_right log shown | 10/80 | 14/80 | 0 |
| perfect_mixed log shown | 11/80 | 17/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 23/80 | 16/80 | +0.087 | [+0.013, +0.175] | 9 | 2 | 0.0654 | no-log control + four core cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 23/80 | 18/80 | +0.062 | [-0.025, +0.163] | 10 | 5 | 0.3018 | no-log control + four core cells non-missing, n = 80 | +0.062, +0.062 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.150 | [+0.037, +0.275] | 13 | 4 | 0.0490 | no-log control + four core cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.025 | [-0.087, +0.150] | 8 | 9 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 23/80 | 20/80 | +0.037 | [-0.050, +0.125] | 8 | 5 | 0.5811 | four nosum cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 19/80 | 20/80 | -0.013 | [-0.100, +0.075] | 6 | 7 | 1.0000 | four nosum cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [-0.087, +0.138] | 9 | 7 | 0.8036 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.050 | [-0.075, +0.188] | 10 | 8 | 0.8145 | four nosum cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 21/80 | 23/80 | -0.025 | [-0.125, +0.075] | 7 | 9 | 0.8036 | both cells non-missing, n = 80 | -0.025, -0.025 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 20/80 | 23/80 | -0.037 | [-0.100, +0.025] | 2 | 5 | 0.4531 | both cells non-missing, n = 80 | -0.037, -0.037 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 21/80 | 22/80 | -0.013 | [-0.100, +0.062] | 5 | 6 | 1.0000 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 21/80 | 12/80 | +0.113 | [+0.025, +0.200] | 12 | 3 | 0.0352 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 23/80 | 23/80 | +0.000 | [-0.100, +0.100] | 8 | 8 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 14/80 | 12/80 | +0.025 | [-0.050, +0.100] | 6 | 4 | 0.7539 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 9/80 | 10/80 | -0.013 | [-0.075, +0.050] | 3 | 4 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 18/80 | 13/80 | +0.062 | [-0.013, +0.138] | 8 | 3 | 0.2266 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 10/80 | 10/80 | +0.000 | [-0.075, +0.075] | 4 | 4 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 14/80 | 13/80 | +0.013 | [-0.062, +0.100] | 6 | 5 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 11/80 | 10/80 | +0.013 | [-0.050, +0.075] | 4 | 3 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 17/80 | 13/80 | +0.050 | [-0.037, +0.138] | 8 | 4 | 0.3877 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 14/67 | 9/67 | +0.075 | [-0.015, +0.164] | 7 | 2 | 0.1797 | no-log control + four core cells non-missing, n = 67 | +0.075, +0.075 (N = 67) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 13/67 | 12/67 | +0.015 | [-0.090, +0.104] | 6 | 5 | 1.0000 | no-log control + four core cells non-missing, n = 67 | +0.015, +0.015 (N = 67) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.090 | [-0.015, +0.209] | 9 | 4 | 0.2668 | no-log control + four core cells non-missing, n = 67 | +0.090, +0.090 (N = 67) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.060 | [-0.075, +0.209] | 8 | 7 | 1.0000 | no-log control + four core cells non-missing, n = 67 | +0.060, +0.060 (N = 67) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 13/67 | 11/67 | +0.030 | [-0.075, +0.134] | 7 | 5 | 0.7744 | four nosum cells non-missing, n = 67 | +0.030, +0.030 (N = 67) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 10/67 | 13/67 | -0.045 | [-0.134, +0.045] | 3 | 6 | 0.5078 | four nosum cells non-missing, n = 67 | -0.045, -0.045 (N = 67) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.015 | [-0.149, +0.119] | 6 | 7 | 1.0000 | four nosum cells non-missing, n = 67 | -0.015, -0.015 (N = 67) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.075 | [-0.060, +0.209] | 9 | 5 | 0.4240 | four nosum cells non-missing, n = 67 | +0.075, +0.075 (N = 67) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 11/67 | 13/67 | -0.030 | [-0.134, +0.075] | 6 | 8 | 0.7905 | both cells non-missing, n = 67 | -0.030, -0.030 (N = 67) |
| certain\|perfect_mixed - certain\|certain_right | 11/67 | 14/67 | -0.045 | [-0.119, +0.030] | 2 | 5 | 0.4531 | both cells non-missing, n = 67 | -0.045, -0.045 (N = 67) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 10/67 | 12/67 | -0.030 | [-0.119, +0.060] | 4 | 6 | 0.7539 | both cells non-missing, n = 67 |
| ceiling check: unsure\|all_unsure - unsure\|none | 11/67 | 5/67 | +0.090 | [+0.000, +0.179] | 8 | 2 | 0.1094 | both cells non-missing, n = 67 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 14/67 | 13/67 | +0.015 | [-0.090, +0.134] | 8 | 7 | 1.0000 | both cells non-missing, n = 67 |
| no-log tone gap: certain\|none - unsure\|none | 9/67 | 5/67 | +0.060 | [+0.000, +0.134] | 5 | 1 | 0.2188 | both cells non-missing, n = 67 |
| moved to x: certain_right log, no objection - no-log control | 3/67 | 0/67 | +0.045 | [+0.000, +0.104] | 3 | 0 | 0.2500 | both cells non-missing, n = 67 |
| changed at all: certain_right log, no objection - no-log control | 8/67 | 0/67 | +0.119 | [+0.045, +0.194] | 8 | 0 | 0.0078 | both cells non-missing, n = 67 |
| moved to x: unsure_right log, no objection - no-log control | 4/67 | 0/67 | +0.060 | [+0.015, +0.119] | 4 | 0 | 0.1250 | both cells non-missing, n = 67 |
| changed at all: unsure_right log, no objection - no-log control | 6/67 | 0/67 | +0.090 | [+0.030, +0.164] | 6 | 0 | 0.0312 | both cells non-missing, n = 67 |
| moved to x: perfect_mixed log, no objection - no-log control | 4/67 | 0/67 | +0.060 | [+0.015, +0.119] | 4 | 0 | 0.1250 | both cells non-missing, n = 67 |
| changed at all: perfect_mixed log, no objection - no-log control | 8/67 | 0/67 | +0.119 | [+0.045, +0.209] | 8 | 0 | 0.0078 | both cells non-missing, n = 67 |

## anthropic:claude-haiku-5-5 | deliberative | arm M | stratum wrong | target distractor

Source files: test__anthropic_claude-haiku-5-5__reasoned__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 5/80 | 62 | 5 | 13 | 0 | 0 |  |
| certain_right | unsure | 1/80 | 66 | 1 | 13 | 0 | 0 |  |
| unsure_right | certain | 2/80 | 67 | 2 | 11 | 0 | 0 |  |
| unsure_right | unsure | 5/80 | 63 | 5 | 12 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 5/80 | 2/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.037, +0.037 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 5/80 | 1/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.050, +0.050 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.087 | [+0.025, +0.163] | 6 | 0 | 0.0312 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.087, +0.087 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.013 | [-0.087, +0.062] | 3 | 3 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 5/80 | 5/80 | +0.000 | [-0.062, +0.062] | 3 | 3 | 1.0000 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| d_u = unsure\|unsure_right - unsure\|certain_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| I = d_c + d_u (tone x log interaction) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|

## anthropic:claude-haiku-5-5 | deliberative | arm M | stratum wrong | target key

Source files: test__anthropic_claude-haiku-5-5__reasoned__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 28/80 | 50 | 28 | 2 | 0 | 0 |  |
| certain_right | unsure | 6/80 | 68 | 6 | 6 | 0 | 0 |  |
| unsure_right | certain | 15/80 | 60 | 15 | 5 | 0 | 0 |  |
| unsure_right | unsure | 24/80 | 51 | 24 | 5 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 28/80 | 15/80 | +0.163 | [+0.075, +0.263] | 15 | 2 | 0.0023 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.163, +0.163 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 24/80 | 6/80 | +0.225 | [+0.125, +0.325] | 19 | 1 | 4.01e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.225, +0.225 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.388 | [+0.250, +0.537] | 27 | 2 | 1.62e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.388, +0.388 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.062 | [-0.188, +0.062] | 10 | 14 | 0.5413 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.062, -0.062 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 28/80 | 24/80 | +0.050 | [-0.037, +0.138] | 9 | 5 | 0.4240 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| d_u = unsure\|unsure_right - unsure\|certain_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| I = d_c + d_u (tone x log interaction) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|

## anthropic:claude-sonnet-5-5 | answer-only | arm A | stratum wrong | target distractor

Source files: test__anthropic_claude-sonnet-5-5__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 1/80 | 76 | 1 | 3 | 0 | 0 |  |
| none | unsure | 0/80 | 76 | 0 | 4 | 0 | 0 |  |
| perfect_mixed | certain | 65/80 | 12 | 65 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 68/80 | 9 | 68 | 3 | 0 | 0 |  |
| reliable | certain | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| reliable | unsure | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| certain_right | certain | 56/80 | 21 | 56 | 3 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| unsure_right | unsure | 49/80 | 29 | 49 | 2 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 56/80 | 0/80 | +0.700 | [+0.600, +0.800] | 56 | 0 | 2.78e-17 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.700, +0.700 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 49/80 | 0/80 | +0.613 | [+0.500, +0.713] | 49 | 0 | 3.55e-15 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.613, +0.613 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +1.312 | [+1.137, +1.475] | 66 | 0 | 2.71e-20 | four core cells non-missing (no-log control not run in this group), n = 80 | +1.312, +1.312 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.087 | [-0.037, +0.212] | 17 | 10 | 0.2478 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.087, +0.087 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 68/80 | 49/80 | +0.237 | [+0.125, +0.350] | 23 | 4 | 0.0003 | both cells non-missing, n = 80 | +0.237, +0.237 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 65/80 | 56/80 | +0.113 | [-0.013, +0.237] | 17 | 8 | 0.1078 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 56/80 | 49/80 | +0.087 | [-0.037, +0.212] | 17 | 10 | 0.2478 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |

## anthropic:claude-sonnet-5-5 | answer-only | arm A | stratum wrong | target key

Source files: test__anthropic_claude-sonnet-5-5__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 7/79 | 70 | 7 | 2 | 1 (no answer 1) | 1 |  |
| none | unsure | 7/79 | 69 | 7 | 3 | 1 (no answer 1) | 1 |  |
| perfect_mixed | certain | 71/80 | 7 | 71 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 70/80 | 9 | 70 | 1 | 0 | 0 |  |
| reliable | certain | 9/80 | 69 | 9 | 2 | 0 | 0 |  |
| reliable | unsure | 8/80 | 70 | 8 | 2 | 0 | 0 |  |
| certain_right | certain | 71/80 | 7 | 71 | 2 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| unsure_right | unsure | 67/80 | 12 | 67 | 1 | 0 | 0 |  |
| control | none | 1/80 | 74 | 1 | 5 | 0 | 0 |  |
| certain_right | none | 0/79 | 75 | 0 | 4 | 1 (no answer 1) | 1 |  |
| unsure_right | none | 2/79 | 74 | 2 | 3 | 1 (no answer 1) | 1 |  |
| perfect_mixed | none | 1/80 | 74 | 1 | 5 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 1/80 | 6/80 | 0 |
| certain_right log shown | 0/79 | 4/79 | 1 |
| unsure_right log shown | 2/79 | 5/79 | 1 |
| perfect_mixed log shown | 1/80 | 6/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 71/80 | 0/80 | +0.887 | [+0.812, +0.950] | 71 | 0 | 8.47e-22 | no-log control + four core cells non-missing, n = 80 | +0.887, +0.887 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 67/80 | 0/80 | +0.838 | [+0.750, +0.912] | 67 | 0 | 1.36e-20 | no-log control + four core cells non-missing, n = 80 | +0.838, +0.838 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +1.725 | [+1.613, +1.825] | 78 | 0 | 6.62e-24 | no-log control + four core cells non-missing, n = 80 | +1.725, +1.725 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.050 | [-0.050, +0.150] | 11 | 7 | 0.4807 | no-log control + four core cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 70/80 | 67/80 | +0.037 | [-0.062, +0.125] | 9 | 6 | 0.6072 | both cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 71/80 | 71/80 | +0.000 | [-0.087, +0.087] | 6 | 6 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 9/80 | 8/80 | +0.013 | [-0.037, +0.062] | 3 | 2 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 71/80 | 67/80 | +0.050 | [-0.050, +0.150] | 11 | 7 | 0.4807 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 7/79 | 7/79 | +0.000 | [-0.063, +0.063] | 3 | 3 | 1.0000 | both cells non-missing, n = 79 |
| moved to x: certain_right log, no objection - no-log control | 0/79 | 1/79 | -0.013 | [-0.038, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 79 |
| changed at all: certain_right log, no objection - no-log control | 4/79 | 5/79 | -0.013 | [-0.076, +0.038] | 2 | 3 | 1.0000 | both cells non-missing, n = 79 |
| moved to x: unsure_right log, no objection - no-log control | 2/79 | 1/79 | +0.013 | [-0.025, +0.063] | 2 | 1 | 1.0000 | both cells non-missing, n = 79 |
| changed at all: unsure_right log, no objection - no-log control | 5/79 | 5/79 | +0.000 | [-0.063, +0.063] | 3 | 3 | 1.0000 | both cells non-missing, n = 79 |
| moved to x: perfect_mixed log, no objection - no-log control | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 6/80 | 6/80 | +0.000 | [-0.062, +0.062] | 3 | 3 | 1.0000 | both cells non-missing, n = 80 |

## openai:gpt-6-luna | answer-only | arm A | stratum right | target distractor

Source files: test__openai_gpt-6-luna__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| none | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| reliable | certain | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| reliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unreliable | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unreliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| certain_right | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unsure_right | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| control | none | 0/40 | 39 | 0 | 1 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/40 | 1/40 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/40 | 0/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | both cells non-missing, n = 40 | +0.050, +0.050 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 1/40 | 0/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/40 | 0/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 1/40 | 2/40 | -0.025 | [-0.100, +0.050] | 1 | 2 | 1.0000 | both cells non-missing, n = 40 |

## openai:gpt-6-luna | answer-only | arm A | stratum wrong | target distractor

Source files: test__openai_gpt-6-luna__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 10/80 | 69 | 10 | 1 | 0 | 0 |  |
| none | unsure | 8/80 | 69 | 8 | 3 | 0 | 0 |  |
| perfect_mixed | certain | 12/80 | 61 | 12 | 7 | 0 | 0 |  |
| perfect_mixed | unsure | 11/80 | 66 | 11 | 3 | 0 | 0 |  |
| reliable | certain | 6/80 | 66 | 6 | 8 | 0 | 0 |  |
| reliable | unsure | 2/80 | 74 | 2 | 4 | 0 | 0 |  |
| certain_right | certain | 4/80 | 71 | 4 | 5 | 0 | 0 |  |
| certain_right | unsure | 1/80 | 75 | 1 | 4 | 0 | 0 |  |
| unsure_right | certain | 2/80 | 73 | 2 | 5 | 0 | 0 |  |
| unsure_right | unsure | 2/80 | 74 | 2 | 4 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 4/80 | 2/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/80 | 1/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.037 | [-0.013, +0.087] | 4 | 1 | 0.3750 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.037, +0.037 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.013 | [-0.037, +0.075] | 3 | 2 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 11/80 | 2/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 12/80 | 4/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 6/80 | 2/80 | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 4/80 | 2/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 10/80 | 8/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |

## openai:gpt-6-luna | answer-only | arm A | stratum wrong | target key

Source files: test__openai_gpt-6-luna__instant__A.jsonl, test__openai_gpt-6-luna__instant__A__rep2.jsonl. Items: 80. Replicates: [1, 2]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/80 | 53 | 25 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| none | unsure | 24/80 | 54 | 24 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | certain | 26/80 | 53 | 26 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | unsure | 16/80 | 62 | 16 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | certain | 21/80 | 59 | 21 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | unsure | 25/80 | 54 | 25 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | certain | 11/80 | 67 | 11 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | unsure | 8/80 | 67 | 8 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | certain | 6/80 | 73 | 6 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | unsure | 9/80 | 71 | 9 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | certain | 26/80 | 52 | 26 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | unsure | 24/80 | 55 | 24 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | certain | 12/80 | 68 | 12 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | unsure | 17/80 | 63 | 17 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | certain | 17/80 | 60 | 17 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | unsure | 21/80 | 57 | 21 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | certain | 17/80 | 63 | 17 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | unsure | 11/80 | 69 | 11 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | certain | 15/80 | 65 | 15 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | unsure | 14/80 | 65 | 14 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | certain | 13/80 | 65 | 13 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | unsure | 10/80 | 70 | 10 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | certain | 9/80 | 71 | 9 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | unsure | 8/80 | 71 | 8 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right | certain | 13.50/80 | 128 | 27 | 5 | 0 | 0 | rep1_vs_rep2: 71/80 |
| certain_right | unsure | 5/80 | 150 | 10 | 0 | 0 | 0 | rep1_vs_rep2: 76/80 |
| unsure_right | certain | 12/80 | 130 | 24 | 6 | 0 | 0 | rep1_vs_rep2: 76/80 |
| unsure_right | unsure | 11.50/80 | 134 | 23 | 3 | 0 | 0 | rep1_vs_rep2: 75/80 |
| certain_right_nosum | certain | 15/80 | 62 | 15 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_nosum | unsure | 10/80 | 70 | 10 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | certain | 15/80 | 64 | 15 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | unsure | 12/80 | 65 | 12 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | certain | 10/80 | 68 | 10 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | certain | 8/80 | 71 | 8 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | unsure | 11/80 | 69 | 11 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| control | none | 1.50/80 | 156 | 3 | 1 | 0 | 0 | rep1_vs_rep2: 79/80 |
| certain_right | none | 5.50/80 | 142 | 11 | 7 | 0 | 0 | rep1_vs_rep2: 77/80 |
| unsure_right | none | 8.50/80 | 141 | 17 | 2 | 0 | 0 | rep1_vs_rep2: 77/80 |
| perfect_mixed | none | 6/80 | 71 | 6 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 1.50/80 | 2/80 | 0 |
| certain_right log shown | 5.50/80 | 9/80 | 0 |
| unsure_right log shown | 8.50/80 | 9.50/80 | 0 |
| perfect_mixed log shown | 6/80 | 9/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 13.50/80 | 12/80 | +0.019 | [-0.037, +0.081] | 7 | 4 | 0.5488 | no-log control + four core cells non-missing, n = 80 | +0.019, +0.019 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 11.50/80 | 5/80 | +0.081 | [+0.025, +0.144] | 10 | 2 | 0.0386 | no-log control + four core cells non-missing, n = 80 | +0.081, +0.081 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.100 | [+0.013, +0.194] | 15 | 6 | 0.0784 | no-log control + four core cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.062 | [-0.144, +0.013] | 7 | 12 | 0.3593 | no-log control + four core cells non-missing, n = 80 | -0.062, -0.062 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 10/80 | 8/80 | +0.025 | [-0.037, +0.100] | 5 | 3 | 0.7266 | four long cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 11/80 | 2/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | four long cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.138 | [+0.037, +0.250] | 10 | 2 | 0.0386 | four long cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | -0.087 | [-0.175, -0.013] | 2 | 8 | 0.1094 | four long cells non-missing, n = 80 | -0.087, -0.087 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 15/80 | 15/80 | +0.000 | [-0.087, +0.087] | 6 | 6 | 1.0000 | four nosum cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 12/80 | 10/80 | +0.025 | [-0.062, +0.113] | 7 | 5 | 0.7744 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [-0.075, +0.125] | 8 | 5 | 0.5811 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | -0.025 | [-0.163, +0.113] | 8 | 9 | 1.0000 | four nosum cells non-missing, n = 80 | -0.025, -0.025 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 24/80 | 17/80 | +0.087 | [+0.013, +0.175] | 9 | 2 | 0.0654 | both cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 24/80 | 21/80 | +0.037 | [-0.037, +0.125] | 7 | 4 | 0.5488 | both cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 24/80 | 11.50/80 | +0.156 | [+0.056, +0.256] | 17 | 5 | 0.0169 | both cells non-missing, n = 80 | +0.156, +0.156 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 26/80 | 17/80 | +0.113 | [+0.025, +0.200] | 12 | 3 | 0.0352 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 26/80 | 15/80 | +0.138 | [+0.025, +0.237] | 16 | 5 | 0.0266 | both cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 26/80 | 13.50/80 | +0.156 | [+0.075, +0.244] | 18 | 3 | 0.0015 | both cells non-missing, n = 80 | +0.156, +0.156 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 25/80 | 9/80 | +0.200 | [+0.075, +0.325] | 22 | 6 | 0.0037 | both cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 26/80 | 11/80 | +0.188 | [+0.100, +0.287] | 16 | 1 | 0.0003 | both cells non-missing, n = 80 | +0.188, +0.188 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 13/80 | 10/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 25/80 | 24/80 | +0.013 | [-0.100, +0.125] | 10 | 9 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 13.50/80 | 11.50/80 | +0.025 | [-0.037, +0.087] | 9 | 6 | 0.6072 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 25/80 | 24/80 | +0.013 | [-0.062, +0.087] | 6 | 5 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 5.50/80 | 1.50/80 | +0.050 | [+0.000, +0.106] | 7 | 1 | 0.0703 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 9/80 | 2/80 | +0.087 | [+0.019, +0.156] | 12 | 2 | 0.0129 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 8.50/80 | 1.50/80 | +0.087 | [+0.031, +0.156] | 9 | 1 | 0.0215 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 9.50/80 | 2/80 | +0.094 | [+0.031, +0.163] | 11 | 2 | 0.0225 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 6/80 | 1.50/80 | +0.056 | [+0.013, +0.106] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 9/80 | 2/80 | +0.087 | [+0.025, +0.156] | 8 | 1 | 0.0391 | both cells non-missing, n = 80 |

## openai:gpt-6-luna | answer-only | arm B | stratum wrong | target distractor

Source files: test__openai_gpt-6-luna__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 14/80 | 65 | 14 | 1 | 0 | 0 |  |
| none | unsure | 14/80 | 65 | 14 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 21/80 | 56 | 21 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 17/80 | 60 | 17 | 3 | 0 | 0 |  |
| reliable | certain | 5/80 | 73 | 5 | 2 | 0 | 0 |  |
| reliable | unsure | 5/80 | 72 | 5 | 3 | 0 | 0 |  |
| certain_right | certain | 4/80 | 72 | 4 | 4 | 0 | 0 |  |
| certain_right | unsure | 2/80 | 74 | 2 | 4 | 0 | 0 |  |
| unsure_right | certain | 5/80 | 72 | 5 | 3 | 0 | 0 |  |
| unsure_right | unsure | 5/80 | 71 | 5 | 4 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 4/80 | 5/80 | -0.013 | [-0.062, +0.037] | 2 | 3 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 5/80 | 2/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.037, +0.037 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [-0.050, +0.113] | 4 | 3 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.025, +0.025 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.050 | [-0.138, +0.025] | 2 | 5 | 0.4531 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.050, -0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 17/80 | 5/80 | +0.150 | [+0.075, +0.225] | 12 | 0 | 0.0005 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 21/80 | 4/80 | +0.212 | [+0.125, +0.300] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 80 | +0.212, +0.212 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 5/80 | 5/80 | +0.000 | [-0.075, +0.075] | 4 | 4 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 4/80 | 5/80 | -0.013 | [-0.062, +0.025] | 1 | 2 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 14/80 | 14/80 | +0.000 | [-0.062, +0.062] | 4 | 4 | 1.0000 | both cells non-missing, n = 80 |

## openai:gpt-6-luna | answer-only | arm B | stratum wrong | target key

Source files: test__openai_gpt-6-luna__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 36/80 | 43 | 36 | 1 | 0 | 0 |  |
| none | unsure | 32/80 | 47 | 32 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 33/80 | 46 | 33 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 32/80 | 48 | 32 | 0 | 0 | 0 |  |
| reliable | certain | 13/80 | 66 | 13 | 1 | 0 | 0 |  |
| reliable | unsure | 10/80 | 70 | 10 | 0 | 0 | 0 |  |
| certain_right | certain | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| certain_right | unsure | 8/80 | 71 | 8 | 1 | 0 | 0 |  |
| unsure_right | certain | 11/80 | 69 | 11 | 0 | 0 | 0 |  |
| unsure_right | unsure | 18/80 | 62 | 18 | 0 | 0 | 0 |  |
| control | none | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| certain_right | none | 3/80 | 74 | 3 | 3 | 0 | 0 |  |
| unsure_right | none | 5/80 | 72 | 5 | 3 | 0 | 0 |  |
| perfect_mixed | none | 7/80 | 70 | 7 | 3 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 2/80 | 4/80 | 0 |
| certain_right log shown | 3/80 | 6/80 | 0 |
| unsure_right log shown | 5/80 | 8/80 | 0 |
| perfect_mixed log shown | 7/80 | 10/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 12/80 | 11/80 | +0.013 | [-0.087, +0.113] | 9 | 8 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 18/80 | 8/80 | +0.125 | [+0.037, +0.225] | 13 | 3 | 0.0213 | no-log control + four core cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.138 | [+0.013, +0.275] | 15 | 7 | 0.1338 | no-log control + four core cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.113 | [-0.263, +0.025] | 8 | 15 | 0.2100 | no-log control + four core cells non-missing, n = 80 | -0.113, -0.113 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 32/80 | 18/80 | +0.175 | [+0.087, +0.263] | 15 | 1 | 0.0005 | both cells non-missing, n = 80 | +0.175, +0.175 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 33/80 | 12/80 | +0.263 | [+0.138, +0.375] | 25 | 4 | 0.0001 | both cells non-missing, n = 80 | +0.263, +0.263 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 13/80 | 10/80 | +0.037 | [-0.037, +0.113] | 6 | 3 | 0.5078 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 12/80 | 18/80 | -0.075 | [-0.188, +0.037] | 8 | 14 | 0.2863 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 36/80 | 32/80 | +0.050 | [-0.037, +0.138] | 8 | 4 | 0.3877 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 3/80 | 2/80 | +0.013 | [-0.037, +0.075] | 3 | 2 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 6/80 | 4/80 | +0.025 | [-0.050, +0.100] | 6 | 4 | 0.7539 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 5/80 | 2/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 8/80 | 4/80 | +0.050 | [-0.013, +0.125] | 6 | 2 | 0.2891 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 7/80 | 2/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 10/80 | 4/80 | +0.075 | [+0.013, +0.150] | 7 | 1 | 0.0703 | both cells non-missing, n = 80 |

## openai:gpt-6-luna | answer-only | arm M | stratum wrong | target distractor

Source files: test__openai_gpt-6-luna__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| unsure_right | unsure | 8/80 | 70 | 8 | 2 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/80 | 1/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 8/80 | 0/80 | +0.100 | [+0.037, +0.163] | 8 | 0 | 0.0078 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.100, +0.100 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.113 | [+0.037, +0.188] | 8 | 0 | 0.0078 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.113, +0.113 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.087 | [-0.150, -0.025] | 0 | 7 | 0.0156 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.087, -0.087 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/80 | 8/80 | -0.075 | [-0.138, -0.025] | 0 | 6 | 0.0312 | both cells non-missing, n = 80 |

## openai:gpt-6-luna | answer-only | arm M | stratum wrong | target key

Source files: test__openai_gpt-6-luna__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 27/80 | 52 | 27 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 44/80 | 36 | 44 | 0 | 0 | 0 |  |
| reliable | certain | 8/80 | 71 | 8 | 1 | 0 | 0 |  |
| reliable | unsure | 17/80 | 63 | 17 | 0 | 0 | 0 |  |
| certain_right | certain | 4/80 | 76 | 4 | 0 | 0 | 0 |  |
| certain_right | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| unsure_right | certain | 4/80 | 76 | 4 | 0 | 0 | 0 |  |
| unsure_right | unsure | 11/80 | 69 | 11 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 4/80 | 4/80 | +0.000 | [-0.050, +0.050] | 2 | 2 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 11/80 | 1/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.125, +0.125 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.125 | [+0.037, +0.212] | 10 | 1 | 0.0117 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.125, +0.125 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.125 | [-0.212, -0.050] | 1 | 10 | 0.0117 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.125, -0.125 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 44/80 | 11/80 | +0.412 | [+0.300, +0.525] | 33 | 0 | 2.33e-10 | both cells non-missing, n = 80 | +0.412, +0.412 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 27/80 | 4/80 | +0.287 | [+0.188, +0.400] | 24 | 1 | 1.55e-06 | both cells non-missing, n = 80 | +0.287, +0.287 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 8/80 | 17/80 | -0.113 | [-0.200, -0.025] | 2 | 11 | 0.0225 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 4/80 | 11/80 | -0.087 | [-0.163, -0.013] | 2 | 9 | 0.0654 | both cells non-missing, n = 80 |

## openai:gpt-6-luna | deliberative | arm A | stratum wrong | target distractor

Source files: test__openai_gpt-6-luna__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 6/80 | 66 | 6 | 8 | 0 | 0 |  |
| none | unsure | 4/79 | 65 | 4 | 10 | 1 (no answer 1) | 1 |  |
| perfect_mixed | certain | 10/80 | 56 | 10 | 14 | 0 | 0 |  |
| perfect_mixed | unsure | 9/80 | 56 | 9 | 15 | 0 | 0 |  |
| certain_right | certain | 9/80 | 60 | 9 | 11 | 0 | 0 |  |
| certain_right | unsure | 3/80 | 65 | 3 | 12 | 0 | 0 |  |
| unsure_right | certain | 4/80 | 63 | 4 | 13 | 0 | 0 |  |
| unsure_right | unsure | 8/80 | 61 | 8 | 11 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 9/80 | 4/80 | +0.062 | [-0.013, +0.138] | 7 | 2 | 0.1797 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.062, +0.062 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 8/80 | 3/80 | +0.062 | [+0.013, +0.113] | 5 | 0 | 0.0625 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.062, +0.062 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.125 | [+0.037, +0.212] | 10 | 1 | 0.0117 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.125, +0.125 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [-0.087, +0.087] | 6 | 5 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 9/80 | 8/80 | +0.013 | [-0.037, +0.075] | 3 | 2 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 10/80 | 9/80 | +0.013 | [-0.062, +0.087] | 5 | 4 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 9/80 | 8/80 | +0.013 | [-0.062, +0.100] | 6 | 5 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 6/79 | 4/79 | +0.025 | [-0.038, +0.089] | 4 | 2 | 0.6875 | both cells non-missing, n = 79 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| d_u = unsure\|unsure_right - unsure\|certain_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| I = d_c + d_u (tone x log interaction) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|

## openai:gpt-6-luna | deliberative | arm A | stratum wrong | target key

Source files: test__openai_gpt-6-luna__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 30/79 | 46 | 30 | 3 | 1 (no answer 1) | 1 |  |
| none | unsure | 30/80 | 48 | 30 | 2 | 0 | 0 |  |
| all_certain | certain | 39/80 | 38 | 39 | 3 | 0 | 0 |  |
| all_certain | unsure | 32/80 | 44 | 32 | 4 | 0 | 0 |  |
| all_unsure | certain | 33/79 | 42 | 33 | 4 | 1 (no answer 1) | 1 |  |
| all_unsure | unsure | 37/80 | 40 | 37 | 3 | 0 | 0 |  |
| perfect_mixed | certain | 45/80 | 32 | 45 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 35/80 | 43 | 35 | 2 | 0 | 0 |  |
| reliable | certain | 34/80 | 43 | 34 | 3 | 0 | 0 |  |
| reliable | unsure | 36/80 | 40 | 36 | 4 | 0 | 0 |  |
| certain_right | certain | 41/80 | 37 | 41 | 2 | 0 | 0 |  |
| certain_right | unsure | 25/80 | 51 | 25 | 4 | 0 | 0 |  |
| unsure_right | certain | 25/80 | 48 | 25 | 7 | 0 | 0 |  |
| unsure_right | unsure | 35/80 | 43 | 35 | 2 | 0 | 0 |  |
| certain_right_nosum | certain | 36/80 | 40 | 36 | 4 | 0 | 0 |  |
| certain_right_nosum | unsure | 29/80 | 48 | 29 | 3 | 0 | 0 |  |
| unsure_right_nosum | certain | 30/80 | 47 | 30 | 3 | 0 | 0 |  |
| unsure_right_nosum | unsure | 31/80 | 46 | 31 | 3 | 0 | 0 |  |
| control | none | 3/80 | 73 | 3 | 4 | 0 | 0 |  |
| certain_right | none | 9/80 | 69 | 9 | 2 | 0 | 0 |  |
| unsure_right | none | 7/80 | 68 | 7 | 5 | 0 | 0 |  |
| perfect_mixed | none | 7/80 | 69 | 7 | 4 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 3/80 | 7/80 | 0 |
| certain_right log shown | 9/80 | 11/80 | 0 |
| unsure_right log shown | 7/80 | 12/80 | 0 |
| perfect_mixed log shown | 7/80 | 11/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 41/80 | 25/80 | +0.200 | [+0.087, +0.312] | 20 | 4 | 0.0015 | no-log control + four core cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 35/80 | 25/80 | +0.125 | [+0.025, +0.225] | 14 | 4 | 0.0309 | no-log control + four core cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.325 | [+0.188, +0.463] | 27 | 3 | 8.43e-06 | no-log control + four core cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.075 | [-0.075, +0.237] | 17 | 13 | 0.5847 | no-log control + four core cells non-missing, n = 80 | +0.075, +0.075 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 36/80 | 30/80 | +0.075 | [-0.025, +0.175] | 12 | 6 | 0.2379 | four nosum cells non-missing, n = 80 | +0.075, +0.075 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 31/80 | 29/80 | +0.025 | [-0.062, +0.113] | 8 | 6 | 0.7905 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.100 | [-0.037, +0.237] | 15 | 6 | 0.0784 | four nosum cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.050 | [-0.100, +0.188] | 13 | 9 | 0.5235 | four nosum cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 35/80 | 35/80 | +0.000 | [-0.100, +0.113] | 9 | 9 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 45/80 | 41/80 | +0.050 | [-0.062, +0.163] | 13 | 9 | 0.5235 | both cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 34/80 | 36/80 | -0.025 | [-0.125, +0.075] | 7 | 9 | 0.8036 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 37/80 | 30/80 | +0.087 | [-0.025, +0.200] | 14 | 7 | 0.1892 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 41/80 | 35/80 | +0.075 | [-0.037, +0.200] | 15 | 9 | 0.3075 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 30/79 | 29/79 | +0.013 | [-0.089, +0.114] | 9 | 8 | 1.0000 | both cells non-missing, n = 79 |
| moved to x: certain_right log, no objection - no-log control | 9/80 | 3/80 | +0.075 | [+0.013, +0.150] | 7 | 1 | 0.0703 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 11/80 | 7/80 | +0.050 | [-0.013, +0.113] | 6 | 2 | 0.2891 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 7/80 | 3/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 12/80 | 7/80 | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 7/80 | 3/80 | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 11/80 | 7/80 | +0.050 | [-0.013, +0.125] | 6 | 2 | 0.2891 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 37/73 | 22/73 | +0.205 | [+0.096, +0.315] | 18 | 3 | 0.0015 | no-log control + four core cells non-missing, n = 73 | +0.205, +0.205 (N = 73) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 30/73 | 22/73 | +0.110 | [+0.014, +0.219] | 12 | 4 | 0.0768 | no-log control + four core cells non-missing, n = 73 | +0.110, +0.110 (N = 73) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.315 | [+0.164, +0.452] | 25 | 3 | 2.74e-05 | no-log control + four core cells non-missing, n = 73 | +0.315, +0.315 (N = 73) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.096 | [-0.055, +0.260] | 16 | 12 | 0.5716 | no-log control + four core cells non-missing, n = 73 | +0.096, +0.096 (N = 73) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 31/73 | 25/73 | +0.082 | [-0.027, +0.192] | 12 | 6 | 0.2379 | four nosum cells non-missing, n = 73 | +0.082, +0.082 (N = 73) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 26/73 | 24/73 | +0.027 | [-0.068, +0.123] | 8 | 6 | 0.7905 | four nosum cells non-missing, n = 73 | +0.027, +0.027 (N = 73) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.110 | [-0.041, +0.247] | 15 | 6 | 0.0784 | four nosum cells non-missing, n = 73 | +0.110, +0.110 (N = 73) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.055 | [-0.096, +0.205] | 13 | 9 | 0.5235 | four nosum cells non-missing, n = 73 | +0.055, +0.055 (N = 73) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 30/73 | 30/73 | +0.000 | [-0.110, +0.110] | 9 | 9 | 1.0000 | both cells non-missing, n = 73 | +0.000, +0.000 (N = 73) |
| certain\|perfect_mixed - certain\|certain_right | 40/73 | 37/73 | +0.041 | [-0.082, +0.164] | 12 | 9 | 0.6636 | both cells non-missing, n = 73 | +0.041, +0.041 (N = 73) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 30/73 | 33/73 | -0.041 | [-0.137, +0.055] | 5 | 8 | 0.5811 | both cells non-missing, n = 73 |
| ceiling check: unsure\|all_unsure - unsure\|none | 32/73 | 25/73 | +0.096 | [-0.027, +0.219] | 14 | 7 | 0.1892 | both cells non-missing, n = 73 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 37/73 | 30/73 | +0.096 | [-0.027, +0.219] | 15 | 8 | 0.2100 | both cells non-missing, n = 73 |
| no-log tone gap: certain\|none - unsure\|none | 26/72 | 24/72 | +0.028 | [-0.083, +0.139] | 9 | 7 | 0.8036 | both cells non-missing, n = 72 |
| moved to x: certain_right log, no objection - no-log control | 6/73 | 0/73 | +0.082 | [+0.027, +0.151] | 6 | 0 | 0.0312 | both cells non-missing, n = 73 |
| changed at all: certain_right log, no objection - no-log control | 6/73 | 0/73 | +0.082 | [+0.027, +0.151] | 6 | 0 | 0.0312 | both cells non-missing, n = 73 |
| moved to x: unsure_right log, no objection - no-log control | 4/73 | 0/73 | +0.055 | [+0.014, +0.110] | 4 | 0 | 0.1250 | both cells non-missing, n = 73 |
| changed at all: unsure_right log, no objection - no-log control | 6/73 | 0/73 | +0.082 | [+0.027, +0.151] | 6 | 0 | 0.0312 | both cells non-missing, n = 73 |
| moved to x: perfect_mixed log, no objection - no-log control | 4/73 | 0/73 | +0.055 | [+0.014, +0.110] | 4 | 0 | 0.1250 | both cells non-missing, n = 73 |
| changed at all: perfect_mixed log, no objection - no-log control | 6/73 | 0/73 | +0.082 | [+0.027, +0.151] | 6 | 0 | 0.0312 | both cells non-missing, n = 73 |

## openai:gpt-6-luna | deliberative | arm M | stratum wrong | target distractor

Source files: test__openai_gpt-6-luna__reasoned__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 24/80 | 43 | 24 | 13 | 0 | 0 |  |
| certain_right | unsure | 2/80 | 65 | 2 | 13 | 0 | 0 |  |
| unsure_right | certain | 4/80 | 64 | 4 | 12 | 0 | 0 |  |
| unsure_right | unsure | 12/80 | 58 | 12 | 10 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 24/80 | 4/80 | +0.250 | [+0.150, +0.350] | 21 | 1 | 1.10e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.250, +0.250 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 12/80 | 2/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.125, +0.125 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.375 | [+0.250, +0.512] | 24 | 0 | 1.19e-07 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.375, +0.375 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.125 | [+0.013, +0.237] | 15 | 4 | 0.0192 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.125, +0.125 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 24/80 | 12/80 | +0.150 | [+0.062, +0.250] | 14 | 2 | 0.0042 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| d_u = unsure\|unsure_right - unsure\|certain_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| I = d_c + d_u (tone x log interaction) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|

## openai:gpt-6-luna | deliberative | arm M | stratum wrong | target key

Source files: test__openai_gpt-6-luna__reasoned__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 46/80 | 29 | 46 | 5 | 0 | 0 |  |
| certain_right | unsure | 16/80 | 60 | 16 | 4 | 0 | 0 |  |
| unsure_right | certain | 19/80 | 53 | 19 | 8 | 0 | 0 |  |
| unsure_right | unsure | 41/80 | 36 | 41 | 3 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 46/80 | 19/80 | +0.338 | [+0.200, +0.475] | 34 | 7 | 2.53e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.338, +0.338 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 41/80 | 16/80 | +0.312 | [+0.200, +0.425] | 27 | 2 | 1.62e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.312, +0.312 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.650 | [+0.463, +0.838] | 40 | 5 | 7.88e-08 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.650, +0.650 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.025 | [-0.138, +0.188] | 18 | 14 | 0.5966 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.025, +0.025 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 46/80 | 41/80 | +0.062 | [-0.062, +0.188] | 16 | 11 | 0.4421 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| d_u = unsure\|unsure_right - unsure\|certain_right | - | - | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| I = d_c + d_u (tone x log interaction) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | - | - | 0 | 0 | - | four core cells non-missing (no-log control not run in this group), n = 0 | - (N = 0) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|

## openai:gpt-6-sol | answer-only | arm A | stratum wrong | target distractor

Source files: test__openai_gpt-6-sol__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 5/80 | 72 | 5 | 3 | 0 | 0 |  |
| none | unsure | 5/80 | 72 | 5 | 3 | 0 | 0 |  |
| perfect_mixed | certain | 8/80 | 69 | 8 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 6/80 | 70 | 6 | 4 | 0 | 0 |  |
| reliable | certain | 5/80 | 71 | 5 | 4 | 0 | 0 |  |
| reliable | unsure | 4/80 | 73 | 4 | 3 | 0 | 0 |  |
| certain_right | certain | 16/80 | 60 | 16 | 4 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| unsure_right | certain | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| unsure_right | unsure | 10/80 | 66 | 10 | 4 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 16/80 | 2/80 | +0.175 | [+0.100, +0.263] | 14 | 0 | 0.0001 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.175, +0.175 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 10/80 | 0/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.125, +0.125 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.300 | [+0.175, +0.450] | 17 | 0 | 1.53e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.300, +0.300 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.050 | [-0.025, +0.125] | 7 | 3 | 0.3438 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.050, +0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 6/80 | 10/80 | -0.050 | [-0.125, +0.013] | 2 | 6 | 0.2891 | both cells non-missing, n = 80 | -0.050, -0.050 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 8/80 | 16/80 | -0.100 | [-0.175, -0.037] | 0 | 8 | 0.0078 | both cells non-missing, n = 80 | -0.100, -0.100 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 5/80 | 4/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 16/80 | 10/80 | +0.075 | [+0.013, +0.138] | 7 | 1 | 0.0703 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 5/80 | 5/80 | +0.000 | [-0.050, +0.050] | 2 | 2 | 1.0000 | both cells non-missing, n = 80 |

## openai:gpt-6-sol | answer-only | arm A | stratum wrong | target key

Source files: test__openai_gpt-6-sol__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 27/80 | 53 | 27 | 0 | 0 | 0 |  |
| none | unsure | 27/80 | 53 | 27 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 35/80 | 45 | 35 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 32/80 | 47 | 32 | 1 | 0 | 0 |  |
| reliable | certain | 26/80 | 54 | 26 | 0 | 0 | 0 |  |
| reliable | unsure | 26/80 | 53 | 26 | 1 | 0 | 0 |  |
| certain_right | certain | 48/80 | 32 | 48 | 0 | 0 | 0 |  |
| certain_right | unsure | 5/80 | 75 | 5 | 0 | 0 | 0 |  |
| unsure_right | certain | 7/80 | 73 | 7 | 0 | 0 | 0 |  |
| unsure_right | unsure | 42/80 | 38 | 42 | 0 | 0 | 0 |  |
| control | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 6/80 | 74 | 6 | 0 | 0 | 0 |  |
| unsure_right | none | 3/80 | 76 | 3 | 1 | 0 | 0 |  |
| perfect_mixed | none | 2/80 | 77 | 2 | 1 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 0/80 | 0 |
| certain_right log shown | 6/80 | 6/80 | 0 |
| unsure_right log shown | 3/80 | 4/80 | 0 |
| perfect_mixed log shown | 2/80 | 3/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 48/80 | 7/80 | +0.512 | [+0.400, +0.625] | 41 | 0 | 9.09e-13 | no-log control + four core cells non-missing, n = 80 | +0.512, +0.512 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 42/80 | 5/80 | +0.463 | [+0.350, +0.575] | 37 | 0 | 1.46e-11 | no-log control + four core cells non-missing, n = 80 | +0.463, +0.463 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.975 | [+0.775, +1.163] | 47 | 0 | 1.42e-14 | no-log control + four core cells non-missing, n = 80 | +0.975, +0.975 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.050 | [-0.050, +0.150] | 10 | 6 | 0.4545 | no-log control + four core cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 32/80 | 42/80 | -0.125 | [-0.212, -0.050] | 1 | 11 | 0.0063 | both cells non-missing, n = 80 | -0.125, -0.125 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 35/80 | 48/80 | -0.163 | [-0.250, -0.087] | 0 | 13 | 0.0002 | both cells non-missing, n = 80 | -0.163, -0.163 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 26/80 | 26/80 | +0.000 | [-0.062, +0.062] | 3 | 3 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 48/80 | 42/80 | +0.075 | [-0.013, +0.163] | 9 | 3 | 0.1460 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 27/80 | 27/80 | +0.000 | [-0.062, +0.062] | 3 | 3 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 6/80 | 0/80 | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 6/80 | 0/80 | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 4/80 | 0/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |

## Target comparison: openai:gpt-6-luna | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/80 | 10/80 | +0.188 | [+0.087, +0.287] | 17 | 2 | 0.0007 |
| none | unsure | 24/80 | 8/80 | +0.200 | [+0.087, +0.312] | 20 | 4 | 0.0015 |
| perfect_mixed | certain | 26/80 | 12/80 | +0.175 | [+0.050, +0.300] | 20 | 6 | 0.0094 |
| perfect_mixed | unsure | 24/80 | 11/80 | +0.163 | [+0.075, +0.250] | 14 | 1 | 0.0010 |
| reliable | certain | 13/80 | 6/80 | +0.087 | [-0.013, +0.188] | 12 | 5 | 0.1435 |
| reliable | unsure | 10/80 | 2/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 |
| certain_right | certain | 13.50/80 | 4/80 | +0.119 | [+0.044, +0.200] | 16 | 2 | 0.0013 |
| certain_right | unsure | 5/80 | 1/80 | +0.050 | [+0.013, +0.094] | 6 | 0 | 0.0312 |
| unsure_right | certain | 12/80 | 2/80 | +0.125 | [+0.062, +0.200] | 12 | 0 | 0.0005 |
| unsure_right | unsure | 11.50/80 | 2/80 | +0.119 | [+0.044, +0.194] | 13 | 1 | 0.0018 |

## Target comparison: openai:gpt-6-luna | answer-only | arm B | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 36/80 | 14/80 | +0.275 | [+0.163, +0.388] | 25 | 3 | 2.74e-05 |
| none | unsure | 32/80 | 14/80 | +0.225 | [+0.087, +0.362] | 25 | 7 | 0.0021 |
| perfect_mixed | certain | 33/80 | 21/80 | +0.150 | [+0.037, +0.263] | 17 | 5 | 0.0169 |
| perfect_mixed | unsure | 32/80 | 17/80 | +0.188 | [+0.062, +0.312] | 21 | 6 | 0.0059 |
| reliable | certain | 13/80 | 5/80 | +0.100 | [+0.013, +0.188] | 11 | 3 | 0.0574 |
| reliable | unsure | 10/80 | 5/80 | +0.062 | [-0.025, +0.150] | 9 | 4 | 0.2668 |
| certain_right | certain | 12/80 | 4/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 |
| certain_right | unsure | 8/80 | 2/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 |
| unsure_right | certain | 11/80 | 5/80 | +0.075 | [-0.013, +0.163] | 10 | 4 | 0.1796 |
| unsure_right | unsure | 18/80 | 5/80 | +0.163 | [+0.075, +0.250] | 14 | 1 | 0.0010 |

## Target comparison: openai:gpt-6-luna | answer-only | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 4/80 | 2/80 | +0.025 | [-0.037, +0.087] | 4 | 2 | 0.6875 |
| certain_right | unsure | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| unsure_right | certain | 4/80 | 1/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 |
| unsure_right | unsure | 11/80 | 8/80 | +0.037 | [-0.050, +0.125] | 8 | 5 | 0.5811 |

## Target comparison: openai:gpt-6-luna | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 30/79 | 6/79 | +0.304 | [+0.190, +0.418] | 25 | 1 | 8.05e-07 |
| none | unsure | 29/79 | 4/79 | +0.316 | [+0.203, +0.430] | 27 | 2 | 1.62e-06 |
| perfect_mixed | certain | 45/80 | 10/80 | +0.438 | [+0.325, +0.550] | 35 | 0 | 5.82e-11 |
| perfect_mixed | unsure | 35/80 | 9/80 | +0.325 | [+0.200, +0.450] | 30 | 4 | 6.16e-06 |
| certain_right | certain | 41/80 | 9/80 | +0.400 | [+0.275, +0.525] | 35 | 3 | 6.68e-08 |
| certain_right | unsure | 25/80 | 3/80 | +0.275 | [+0.175, +0.388] | 23 | 1 | 2.98e-06 |
| unsure_right | certain | 25/80 | 4/80 | +0.263 | [+0.150, +0.375] | 24 | 3 | 4.92e-05 |
| unsure_right | unsure | 35/80 | 8/80 | +0.338 | [+0.225, +0.450] | 29 | 2 | 4.63e-07 |

## Target comparison: openai:gpt-6-luna | deliberative | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 46/80 | 24/80 | +0.275 | [+0.125, +0.412] | 31 | 9 | 0.0007 |
| certain_right | unsure | 16/80 | 2/80 | +0.175 | [+0.087, +0.263] | 15 | 1 | 0.0005 |
| unsure_right | certain | 19/80 | 4/80 | +0.188 | [+0.087, +0.300] | 18 | 3 | 0.0015 |
| unsure_right | unsure | 41/80 | 12/80 | +0.362 | [+0.237, +0.487] | 32 | 3 | 4.18e-07 |

## Target comparison: openai:gpt-6-sol | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 27/80 | 5/80 | +0.275 | [+0.163, +0.388] | 24 | 2 | 1.05e-05 |
| none | unsure | 27/80 | 5/80 | +0.275 | [+0.175, +0.375] | 23 | 1 | 2.98e-06 |
| perfect_mixed | certain | 35/80 | 8/80 | +0.338 | [+0.237, +0.438] | 27 | 0 | 1.49e-08 |
| perfect_mixed | unsure | 32/80 | 6/80 | +0.325 | [+0.225, +0.425] | 26 | 0 | 2.98e-08 |
| reliable | certain | 26/80 | 5/80 | +0.263 | [+0.150, +0.375] | 23 | 2 | 1.94e-05 |
| reliable | unsure | 26/80 | 4/80 | +0.275 | [+0.175, +0.375] | 23 | 1 | 2.98e-06 |
| certain_right | certain | 48/80 | 16/80 | +0.400 | [+0.300, +0.512] | 32 | 0 | 4.66e-10 |
| certain_right | unsure | 5/80 | 0/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 |
| unsure_right | certain | 7/80 | 2/80 | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 |
| unsure_right | unsure | 42/80 | 10/80 | +0.400 | [+0.287, +0.512] | 33 | 1 | 4.07e-09 |

## Target comparison: anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 |
| none | unsure | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 |
| perfect_mixed | certain | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| perfect_mixed | unsure | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 |
| reliable | certain | 2/80 | 1/80 | +0.013 | [-0.025, +0.050] | 2 | 1 | 1.0000 |
| reliable | unsure | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 |
| certain_right | certain | 1.50/80 | 0/80 | +0.019 | [+0.000, +0.050] | 2 | 0 | 0.5000 |
| certain_right | unsure | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 |
| unsure_right | certain | 0.50/80 | 0/80 | +0.006 | [+0.000, +0.019] | 1 | 0 | 1.0000 |
| unsure_right | unsure | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 |

## Target comparison: anthropic:claude-haiku-5-5 | answer-only | arm B | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 3/80 | 3/80 | +0.000 | [-0.050, +0.050] | 2 | 2 | 1.0000 |
| none | unsure | 1/80 | 1/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| perfect_mixed | certain | 3/80 | 2/80 | +0.013 | [-0.037, +0.062] | 3 | 2 | 1.0000 |
| perfect_mixed | unsure | 3/80 | 2/80 | +0.013 | [-0.037, +0.075] | 3 | 2 | 1.0000 |
| reliable | certain | 3/80 | 2/80 | +0.013 | [-0.037, +0.075] | 3 | 2 | 1.0000 |
| reliable | unsure | 2/80 | 2/80 | +0.000 | [-0.050, +0.050] | 2 | 2 | 1.0000 |
| certain_right | certain | 2/80 | 3/80 | -0.013 | [-0.062, +0.037] | 2 | 3 | 1.0000 |
| certain_right | unsure | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 |
| unsure_right | certain | 3/80 | 1/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 |
| unsure_right | unsure | 2/80 | 2/80 | +0.000 | [-0.050, +0.050] | 2 | 2 | 1.0000 |

## Target comparison: anthropic:claude-haiku-5-5 | answer-only | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| certain_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |

## Target comparison: anthropic:claude-haiku-5-5 | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 14/80 | 2/80 | +0.150 | [+0.062, +0.250] | 14 | 2 | 0.0042 |
| none | unsure | 12/80 | 2/80 | +0.125 | [+0.037, +0.212] | 12 | 2 | 0.0129 |
| perfect_mixed | certain | 20/80 | 3/80 | +0.212 | [+0.113, +0.325] | 20 | 3 | 0.0005 |
| perfect_mixed | unsure | 21/80 | 4/80 | +0.212 | [+0.100, +0.325] | 21 | 4 | 0.0009 |
| certain_right | certain | 23/80 | 5/80 | +0.225 | [+0.125, +0.338] | 20 | 2 | 0.0001 |
| certain_right | unsure | 18/80 | 4/80 | +0.175 | [+0.075, +0.275] | 17 | 3 | 0.0026 |
| unsure_right | certain | 16/80 | 4/80 | +0.150 | [+0.050, +0.263] | 16 | 4 | 0.0118 |
| unsure_right | unsure | 23/80 | 2/80 | +0.263 | [+0.163, +0.362] | 22 | 1 | 5.72e-06 |

## Target comparison: anthropic:claude-haiku-5-5 | deliberative | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 28/80 | 5/80 | +0.287 | [+0.175, +0.400] | 25 | 2 | 5.65e-06 |
| certain_right | unsure | 6/80 | 1/80 | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 |
| unsure_right | certain | 15/80 | 2/80 | +0.163 | [+0.075, +0.263] | 15 | 2 | 0.0023 |
| unsure_right | unsure | 24/80 | 5/80 | +0.237 | [+0.125, +0.350] | 22 | 3 | 0.0002 |

## Target comparison: anthropic:claude-sonnet-5-5 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 7/79 | 1/79 | +0.076 | [+0.025, +0.139] | 6 | 0 | 0.0312 |
| none | unsure | 7/79 | 0/79 | +0.089 | [+0.025, +0.152] | 7 | 0 | 0.0156 |
| perfect_mixed | certain | 71/80 | 65/80 | +0.075 | [-0.013, +0.175] | 11 | 5 | 0.2101 |
| perfect_mixed | unsure | 70/80 | 68/80 | +0.025 | [-0.062, +0.113] | 8 | 6 | 0.7905 |
| reliable | certain | 9/80 | 0/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 |
| reliable | unsure | 8/80 | 0/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 |
| certain_right | certain | 71/80 | 56/80 | +0.188 | [+0.075, +0.300] | 19 | 4 | 0.0026 |
| certain_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 67/80 | 49/80 | +0.225 | [+0.125, +0.325] | 20 | 2 | 0.0001 |

## Probe: stated probability that the reviewer is right

| model | arm | log | tone | n | mean | median | counts match log | independent ref | pooled ref |
|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | A | all_certain | certain | 1 | 0.900 | 0.900 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_certain | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| anthropic:claude-haiku-5-5 | A | all_certain_6of8 | unsure | 1 | 0.500 | 0.500 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | all_unsure | certain | 1 | 0.800 | 0.800 | 0.000 | 0.500 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_unsure | unsure | 1 | 0.900 | 0.900 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_unsure_6of8 | certain | 1 | 0.400 | 0.400 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c2_u4 | unsure | 1 | 0.830 | 0.830 | 0.000 | 0.833 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| anthropic:claude-haiku-5-5 | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| anthropic:claude-haiku-5-5 | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c4_u3 | certain | 1 | 0.900 | 0.900 | 1.000 | 0.833 | 0.800 |
| anthropic:claude-haiku-5-5 | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| anthropic:claude-haiku-5-5 | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| anthropic:claude-haiku-5-5 | A | none | unsure | 1 | 0.500 | 0.500 | - | - | - |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | certain | 1 | 0.950 | 0.950 | 1.000 | 0.833 | 0.900 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| anthropic:claude-haiku-5-5 | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| anthropic:claude-haiku-5-5 | A | reliable | unsure | 1 | 0.500 | 0.500 | 0.000 | 0.667 | 0.700 |
| anthropic:claude-haiku-5-5 | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| anthropic:claude-haiku-5-5 | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| anthropic:claude-haiku-5-5 | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | B | all_certain | certain | 40 | 0.757 | 0.800 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | B | all_certain | unsure | 40 | 0.734 | 0.800 | 0.000 | 0.500 | 0.900 |
| anthropic:claude-haiku-5-5 | B | all_certain_6of8 | certain | 40 | 0.720 | 0.750 | 1.000 | 0.700 | 0.700 |
| anthropic:claude-haiku-5-5 | B | all_certain_6of8 | unsure | 40 | 0.691 | 0.750 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | B | all_unsure | certain | 40 | 0.864 | 0.850 | 0.000 | 0.500 | 0.900 |
| anthropic:claude-haiku-5-5 | B | all_unsure | unsure | 40 | 0.811 | 0.800 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | B | all_unsure_6of8 | certain | 40 | 0.593 | 0.600 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | B | all_unsure_6of8 | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c2_u4 | certain | 40 | 0.509 | 0.500 | 0.850 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c2_u4 | unsure | 40 | 0.790 | 0.800 | 0.875 | 0.833 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c3_u4 | certain | 40 | 0.746 | 0.750 | 0.600 | 0.667 | 0.800 |
| anthropic:claude-haiku-5-5 | B | c3_u4 | unsure | 40 | 0.816 | 0.800 | 0.850 | 0.833 | 0.800 |
| anthropic:claude-haiku-5-5 | B | c4_u2 | certain | 40 | 0.758 | 0.750 | 0.950 | 0.833 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c4_u2 | unsure | 40 | 0.573 | 0.500 | 0.700 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c4_u3 | certain | 40 | 0.842 | 0.840 | 0.825 | 0.833 | 0.800 |
| anthropic:claude-haiku-5-5 | B | c4_u3 | unsure | 40 | 0.749 | 0.750 | 0.825 | 0.667 | 0.800 |
| anthropic:claude-haiku-5-5 | B | certain_right | certain | 40 | 0.686 | 0.750 | 0.850 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right | unsure | 40 | 0.006 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right_long | certain | 40 | 0.988 | 1.000 | 1.000 | 0.929 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right_long | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right_nosum | certain | 40 | 0.432 | 0.500 | 0.275 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right_nosum | unsure | 40 | 0.006 | 0.000 | 0.650 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | B | none | certain | 40 | 0.500 | 0.500 | - | - | - |
| anthropic:claude-haiku-5-5 | B | none | unsure | 40 | 0.500 | 0.500 | - | - | - |
| anthropic:claude-haiku-5-5 | B | perfect_mixed | certain | 40 | 0.885 | 0.850 | 0.975 | 0.833 | 0.900 |
| anthropic:claude-haiku-5-5 | B | perfect_mixed | unsure | 40 | 0.885 | 0.850 | 0.950 | 0.833 | 0.900 |
| anthropic:claude-haiku-5-5 | B | reliable | certain | 40 | 0.645 | 0.670 | 0.275 | 0.667 | 0.700 |
| anthropic:claude-haiku-5-5 | B | reliable | unsure | 40 | 0.694 | 0.750 | 0.575 | 0.667 | 0.700 |
| anthropic:claude-haiku-5-5 | B | unreliable | certain | 40 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| anthropic:claude-haiku-5-5 | B | unreliable | unsure | 40 | 0.244 | 0.250 | 0.775 | 0.333 | 0.300 |
| anthropic:claude-haiku-5-5 | B | unsure_right | certain | 40 | 0.018 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right | unsure | 40 | 0.931 | 1.000 | 0.925 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right_long | certain | 40 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right_long | unsure | 40 | 0.850 | 1.000 | 1.000 | 0.929 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right_nosum | certain | 40 | 0.085 | 0.000 | 0.625 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right_nosum | unsure | 40 | 0.879 | 1.000 | 0.750 | 0.833 | 0.500 |
| openai:gpt-6-luna | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openai:gpt-6-luna | A | all_certain | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.900 |
| openai:gpt-6-luna | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 0.000 | 0.700 | 0.700 |
| openai:gpt-6-luna | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | all_unsure | certain | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openai:gpt-6-luna | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.900 | 0.900 |
| openai:gpt-6-luna | A | all_unsure_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 0.000 | 0.700 | 0.700 |
| openai:gpt-6-luna | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openai:gpt-6-luna | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openai:gpt-6-luna | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openai:gpt-6-luna | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openai:gpt-6-luna | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openai:gpt-6-luna | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openai:gpt-6-luna | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openai:gpt-6-luna | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openai:gpt-6-luna | A | certain_right_nosum | certain | 1 | 0.750 | 0.750 | 0.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| openai:gpt-6-luna | A | none | unsure | 1 | 0.500 | 0.500 | - | - | - |
| openai:gpt-6-luna | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openai:gpt-6-luna | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openai:gpt-6-luna | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openai:gpt-6-luna | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openai:gpt-6-luna | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openai:gpt-6-luna | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openai:gpt-6-luna | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openai:gpt-6-luna | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openai:gpt-6-luna | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | B | all_certain | certain | 40 | 1.000 | 1.000 | 0.175 | 0.900 | 0.900 |
| openai:gpt-6-luna | B | all_certain | unsure | 40 | 0.450 | 0.500 | 1.000 | 0.500 | 0.900 |
| openai:gpt-6-luna | B | all_certain_6of8 | certain | 40 | 0.804 | 0.750 | 0.100 | 0.700 | 0.700 |
| openai:gpt-6-luna | B | all_certain_6of8 | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | B | all_unsure | certain | 40 | 0.713 | 1.000 | 1.000 | 0.500 | 0.900 |
| openai:gpt-6-luna | B | all_unsure | unsure | 40 | 1.000 | 1.000 | 0.000 | 0.900 | 0.900 |
| openai:gpt-6-luna | B | all_unsure_6of8 | certain | 40 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | B | all_unsure_6of8 | unsure | 40 | 0.850 | 0.750 | 0.000 | 0.700 | 0.700 |
| openai:gpt-6-luna | B | c2_u4 | certain | 40 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | B | c2_u4 | unsure | 40 | 1.000 | 1.000 | 0.975 | 0.833 | 0.700 |
| openai:gpt-6-luna | B | c3_u4 | certain | 40 | 0.748 | 0.750 | 0.975 | 0.667 | 0.800 |
| openai:gpt-6-luna | B | c3_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openai:gpt-6-luna | B | c4_u2 | certain | 40 | 0.975 | 1.000 | 0.875 | 0.833 | 0.700 |
| openai:gpt-6-luna | B | c4_u2 | unsure | 40 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | B | c4_u3 | certain | 40 | 0.992 | 1.000 | 0.900 | 0.833 | 0.800 |
| openai:gpt-6-luna | B | c4_u3 | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openai:gpt-6-luna | B | certain_right | certain | 40 | 0.963 | 1.000 | 0.850 | 0.833 | 0.500 |
| openai:gpt-6-luna | B | certain_right | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | B | certain_right_long | certain | 40 | 0.912 | 1.000 | 0.575 | 0.929 | 0.500 |
| openai:gpt-6-luna | B | certain_right_long | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openai:gpt-6-luna | B | certain_right_nosum | certain | 40 | 0.758 | 1.000 | 0.250 | 0.833 | 0.500 |
| openai:gpt-6-luna | B | certain_right_nosum | unsure | 40 | 0.000 | 0.000 | 0.850 | 0.167 | 0.500 |
| openai:gpt-6-luna | B | none | certain | 40 | 0.500 | 0.500 | - | - | - |
| openai:gpt-6-luna | B | none | unsure | 40 | 0.500 | 0.500 | - | - | - |
| openai:gpt-6-luna | B | perfect_mixed | certain | 40 | 0.954 | 1.000 | 0.725 | 0.833 | 0.900 |
| openai:gpt-6-luna | B | perfect_mixed | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openai:gpt-6-luna | B | reliable | certain | 40 | 0.738 | 0.750 | 0.900 | 0.667 | 0.700 |
| openai:gpt-6-luna | B | reliable | unsure | 40 | 0.756 | 0.750 | 0.975 | 0.667 | 0.700 |
| openai:gpt-6-luna | B | unreliable | certain | 40 | 0.250 | 0.250 | 0.900 | 0.333 | 0.300 |
| openai:gpt-6-luna | B | unreliable | unsure | 40 | 0.281 | 0.250 | 0.875 | 0.333 | 0.300 |
| openai:gpt-6-luna | B | unsure_right | certain | 40 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | B | unsure_right | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | B | unsure_right_long | certain | 40 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openai:gpt-6-luna | B | unsure_right_long | unsure | 40 | 0.963 | 1.000 | 0.925 | 0.929 | 0.500 |
| openai:gpt-6-luna | B | unsure_right_nosum | certain | 40 | 0.000 | 0.000 | 0.775 | 0.167 | 0.500 |
| openai:gpt-6-luna | B | unsure_right_nosum | unsure | 40 | 0.923 | 1.000 | 0.425 | 0.833 | 0.500 |

| model | arm | cells with a log | RMSE vs independent | RMSE vs pooled |
|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | A | 34 | 0.123 | 0.326 |
| anthropic:claude-haiku-5-5 | B | 34 | 0.134 | 0.259 |
| openai:gpt-6-luna | A | 34 | 0.178 | 0.345 |
| openai:gpt-6-luna | B | 34 | 0.131 | 0.309 |

Curve table (stated probability vs flip rate): 208 points, in the JSON under `curve`.

## Warnings

- probe probabilities read on a 0-100 scale (divided by 100) in: probe__openai_gpt-6-luna__A.jsonl, probe__openai_gpt-6-luna__B.jsonl, probe__anthropic_claude-haiku-5-5__A.jsonl, probe__anthropic_claude-haiku-5-5__B.jsonl
