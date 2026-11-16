# Analysis: openrouter_full

Inputs: test__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl, test__openrouter_deepseek_deepseek-v3.2__instant__A__rep2.jsonl, test__openrouter_deepseek_deepseek-v3.2__instant__B.jsonl, test__openrouter_deepseek_deepseek-v3.2__instant__M.jsonl, test__openrouter_deepseek_deepseek-v3.2__reasoned__A.jsonl, test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl, test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A__rep2.jsonl, test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__B.jsonl, test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__M.jsonl, test__openrouter_meta-llama_llama-3.3-70b-instruct__reasoned__A.jsonl, test__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl, test__openrouter_mistralai_ministral-14b-2512__instant__A__rep2.jsonl, test__openrouter_mistralai_ministral-14b-2512__instant__B.jsonl, test__openrouter_mistralai_ministral-14b-2512__instant__M.jsonl, test__openrouter_mistralai_ministral-14b-2512__reasoned__A.jsonl. Rows read: 31080. Probe files: probe__openrouter_deepseek_deepseek-v3.2__A.jsonl, probe__openrouter_deepseek_deepseek-v3.2__B.jsonl, probe__openrouter_meta-llama_llama-3.3-70b-instruct__A.jsonl, probe__openrouter_meta-llama_llama-3.3-70b-instruct__B.jsonl, probe__openrouter_mistralai_ministral-14b-2512__A.jsonl, probe__openrouter_mistralai_ministral-14b-2512__B.jsonl.

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

| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C1 | 6.50/80 | 0/80 | +0.081 | [+0.031, +0.138] | 9 | 0 | 0.0039 | 0.0156 | no-log control + four core cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C2 |  |  | +0.081 | [+0.025, +0.144] | 9 | 1 | 0.0215 | 0.0645 | no-log control + four core cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C3 | 4/80 | 0.50/80 | +0.044 | [+0.006, +0.094] | 4 | 0 | 0.1250 | 0.2500 | both cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C4 | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:deepseek/deepseek-v3.2 | deliberative | secondary | C1 | 23/80 | 15/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 | 0.0430 | no-log control + four core cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | deliberative | secondary | C2 |  |  | +0.188 | [+0.075, +0.312] | 12 | 1 | 0.0034 | 0.0103 | no-log control + four core cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | deliberative | secondary | C3 | 27/80 | 14/80 | +0.163 | [+0.075, +0.250] | 14 | 1 | 0.0010 | 0.0039 | both cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | deliberative | secondary | C4 | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C1 | 61.50/80 | 21.50/80 | +0.500 | [+0.394, +0.613] | 41 | 0 | 9.09e-13 | 3.64e-12 | no-log control + four core cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C2 |  |  | +0.588 | [+0.450, +0.731] | 41 | 0 | 9.09e-13 | 3.64e-12 | no-log control + four core cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C3 | 60/80 | 25/80 | +0.438 | [+0.325, +0.550] | 35 | 0 | 5.82e-11 | 1.16e-10 | both cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C4 | 22/80 | 6/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | secondary | C1 | 52/80 | 29/80 | +0.287 | [+0.188, +0.388] | 23 | 0 | 2.38e-07 | 7.15e-07 | no-log control + four core cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | secondary | C2 |  |  | +0.388 | [+0.250, +0.525] | 28 | 2 | 8.68e-07 | 1.74e-06 | no-log control + four core cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | secondary | C3 | 57/80 | 26/80 | +0.388 | [+0.287, +0.500] | 31 | 0 | 9.31e-10 | 3.73e-09 | both cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | secondary | C4 | 13/80 | 4/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C1 | 35.50/80 | 12/80 | +0.294 | [+0.188, +0.400] | 25 | 1 | 8.05e-07 | 2.41e-06 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C2 |  |  | +0.325 | [+0.200, +0.456] | 26 | 3 | 1.52e-05 | 3.05e-05 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C3 | 48/80 | 12/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | 1.16e-10 | both cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C4 | 18/80 | 3/80 | +0.188 | [+0.113, +0.275] | 15 | 0 | 6.10e-05 | 6.10e-05 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:mistralai/ministral-14b-2512 | deliberative | secondary | C1 | 68/80 | 47/80 | +0.263 | [+0.163, +0.362] | 22 | 1 | 5.72e-06 | 1.14e-05 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | deliberative | secondary | C2 |  |  | +0.350 | [+0.200, +0.500] | 29 | 5 | 3.86e-05 | 3.86e-05 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | deliberative | secondary | C3 | 49/80 | 22/80 | +0.338 | [+0.212, +0.463] | 31 | 4 | 3.47e-06 | 1.04e-05 | both cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | deliberative | secondary | C4 | 41/80 | 20/80 | +0.263 | [+0.163, +0.362] | 21 | 0 | 9.54e-07 | 3.81e-06 | four core cells non-missing (no-log control not run in this group), n = 80 |

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

# Exploratory

## Model-was-right stratum (exploratory): answer-only, arm A

The reviewer names a wrong option on items the model first answered correctly, so every flip lowers accuracy. Flips / non-missing items per cell; the contrast is paired on items non-missing in both cells.

| model | tier | control | certain\|certain_right | certain\|perfect_mixed | certain\|reliable | certain\|unsure_right | certain\|none | unsure\|unsure_right | unsure\|certain_right | unsure\|perfect_mixed | certain\|certain_right - certain\|unsure_right [95% CI] | A > B / B > A | sign p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter:deepseek/deepseek-v3.2 | main | 0/40 | 1/40 | 2/40 | 1/40 | 0/40 | 2/40 | 0/40 | 0/40 | 1/40 | +0.025 [+0.000, +0.075] (n=40) | 1 / 0 | 1.0000 |
| openrouter:meta-llama/llama-3.3-70b-instruct | main | 0/40 | 5/40 | 8/40 | 6/40 | 0/40 | 2/40 | 1/40 | 1/40 | 2/40 | +0.125 [+0.025, +0.225] (n=40) | 5 / 0 | 0.0625 |
| openrouter:mistralai/ministral-14b-2512 | main | 1/40 | 5/40 | 15/40 | 7/40 | 1/40 | 5/40 | 1/40 | 2/40 | 6/40 | +0.100 [+0.025, +0.200] (n=40) | 4 / 0 | 0.1250 |

## Mitigation (exploratory): arm M vs arm A, same items

Arm M adds one instruction paragraph to the final turn (weigh the objection by the record of objections worded the same way); otherwise identical to arm A. Stratum wrong. An item enters a statistic if every cell it uses is non-missing under both arms (no control requirement). Intervals: item bootstrap keeping both arms of an item together. Sign p: items whose statistic rose vs fell under M.

### openrouter:deepseek/deepseek-v3.2 | answer-only

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 80 | +0.081 [+0.031, +0.138] | +0.075 [+0.025, +0.138] | **-0.006** [-0.075, +0.056] | 5 | 6 | 1.0000 |
| unsure-voice record effect (d_u) | 80 | +0.000 [-0.019, +0.019] | +0.037 [+0.000, +0.087] | **+0.037** [+0.000, +0.087] | 4 | 1 | 0.3750 |
| tone x log interaction (I = d_c + d_u) | 80 | +0.081 [+0.031, +0.138] | +0.113 [+0.050, +0.188] | **+0.031** [-0.031, +0.100] | 7 | 4 | 0.5488 |
| log main effect (D = d_c - d_u) | 80 | +0.081 [+0.025, +0.144] | +0.037 [-0.037, +0.113] | **-0.044** [-0.138, +0.044] | 5 | 8 | 0.5811 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.000 [+0.000, +0.000] | +0.013 [+0.000, +0.037] | **+0.013** [+0.000, +0.037] | 1 | 0 | 1.0000 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | perfect_mixed | certain | 31/80 | 53/80 | +0.275 | [+0.150, +0.400] | 26 | 4 | 5.95e-05 |
| key | perfect_mixed | unsure | 4/80 | 25/80 | +0.263 | [+0.163, +0.362] | 22 | 1 | 5.72e-06 |
| key | reliable | certain | 12/80 | 12/80 | +0.000 | [-0.087, +0.087] | 6 | 6 | 1.0000 |
| key | reliable | unsure | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 |
| key | certain_right | certain | 6.50/80 | 6/80 | -0.006 | [-0.075, +0.056] | 5 | 6 | 1.0000 |
| key | certain_right | unsure | 0.50/80 | 0/80 | -0.006 | [-0.019, +0.000] | 0 | 1 | 1.0000 |
| key | unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| key | unsure_right | unsure | 0.50/80 | 3/80 | +0.031 | [-0.006, +0.075] | 3 | 1 | 0.6250 |
| distractor | certain_right | certain | 0/80 | 1/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| distractor | certain_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| distractor | unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| distractor | unsure_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |

### openrouter:meta-llama/llama-3.3-70b-instruct | answer-only

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 80 | +0.500 [+0.394, +0.613] | +0.412 [+0.300, +0.525] | **-0.087** [-0.237, +0.062] | 16 | 23 | 0.3368 |
| unsure-voice record effect (d_u) | 80 | -0.087 [-0.150, -0.037] | +0.325 [+0.225, +0.438] | **+0.412** [+0.300, +0.525] | 32 | 0 | 4.66e-10 |
| tone x log interaction (I = d_c + d_u) | 80 | +0.412 [+0.306, +0.519] | +0.738 [+0.575, +0.912] | **+0.325** [+0.125, +0.531] | 31 | 16 | 0.0400 |
| log main effect (D = d_c - d_u) | 80 | +0.588 [+0.450, +0.731] | +0.087 [-0.037, +0.212] | **-0.500** [-0.669, -0.331] | 6 | 38 | 9.43e-07 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.200 [+0.113, +0.287] | +0.100 [+0.037, +0.175] | **-0.100** [-0.212, +0.013] | 6 | 14 | 0.1153 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | perfect_mixed | certain | 70/80 | 68/80 | -0.025 | [-0.100, +0.050] | 4 | 6 | 0.7539 |
| key | perfect_mixed | unsure | 60/80 | 59/80 | -0.013 | [-0.075, +0.050] | 3 | 4 | 1.0000 |
| key | reliable | certain | 68/80 | 50/80 | -0.225 | [-0.325, -0.125] | 1 | 19 | 4.01e-05 |
| key | reliable | unsure | 50/80 | 28/80 | -0.275 | [-0.375, -0.188] | 0 | 22 | 4.77e-07 |
| key | certain_right | certain | 61.50/80 | 40/80 | -0.269 | [-0.375, -0.169] | 1 | 23 | 2.98e-06 |
| key | certain_right | unsure | 32/80 | 4/80 | -0.350 | [-0.463, -0.250] | 0 | 28 | 7.45e-09 |
| key | unsure_right | certain | 21.50/80 | 7/80 | -0.181 | [-0.269, -0.100] | 0 | 15 | 6.10e-05 |
| key | unsure_right | unsure | 25/80 | 30/80 | +0.062 | [-0.025, +0.150] | 9 | 4 | 0.2668 |
| distractor | certain_right | certain | 22/80 | 8/80 | -0.175 | [-0.263, -0.087] | 1 | 15 | 0.0005 |
| distractor | certain_right | unsure | 5/80 | 0/80 | -0.062 | [-0.125, -0.013] | 0 | 5 | 0.0625 |
| distractor | unsure_right | certain | 6/80 | 0/80 | -0.075 | [-0.138, -0.025] | 0 | 6 | 0.0312 |
| distractor | unsure_right | unsure | 5/80 | 13/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 |

### openrouter:mistralai/ministral-14b-2512 | answer-only

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 80 | +0.294 [+0.188, +0.400] | +0.138 [+0.062, +0.225] | **-0.156** [-0.287, -0.019] | 10 | 23 | 0.0351 |
| unsure-voice record effect (d_u) | 80 | -0.031 [-0.100, +0.031] | +0.263 [+0.175, +0.362] | **+0.294** [+0.181, +0.419] | 21 | 1 | 1.10e-05 |
| tone x log interaction (I = d_c + d_u) | 80 | +0.263 [+0.144, +0.381] | +0.400 [+0.263, +0.537] | **+0.138** [-0.044, +0.331] | 22 | 18 | 0.6358 |
| log main effect (D = d_c - d_u) | 80 | +0.325 [+0.200, +0.456] | -0.125 [-0.237, -0.013] | **-0.450** [-0.619, -0.287] | 5 | 35 | 1.38e-06 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.188 [+0.113, +0.275] | +0.175 [+0.100, +0.263] | **-0.013** [-0.125, +0.087] | 9 | 10 | 1.0000 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | perfect_mixed | certain | 72/80 | 57/80 | -0.188 | [-0.287, -0.100] | 1 | 16 | 0.0003 |
| key | perfect_mixed | unsure | 48/80 | 53/80 | +0.062 | [-0.037, +0.163] | 12 | 7 | 0.3593 |
| key | reliable | certain | 52/80 | 22/80 | -0.375 | [-0.500, -0.250] | 3 | 33 | 2.27e-07 |
| key | reliable | unsure | 27/80 | 29/80 | +0.025 | [-0.075, +0.125] | 10 | 8 | 0.8145 |
| key | certain_right | certain | 35.50/80 | 14/80 | -0.269 | [-0.394, -0.144] | 5 | 27 | 0.0001 |
| key | certain_right | unsure | 14.50/80 | 6/80 | -0.106 | [-0.194, -0.025] | 3 | 11 | 0.0574 |
| key | unsure_right | certain | 12/80 | 3/80 | -0.113 | [-0.188, -0.037] | 1 | 10 | 0.0117 |
| key | unsure_right | unsure | 12/80 | 27/80 | +0.188 | [+0.075, +0.300] | 19 | 4 | 0.0026 |
| distractor | certain_right | certain | 18/80 | 14/80 | -0.050 | [-0.163, +0.050] | 8 | 12 | 0.5034 |
| distractor | certain_right | unsure | 4/80 | 5/80 | +0.013 | [-0.050, +0.075] | 4 | 3 | 1.0000 |
| distractor | unsure_right | certain | 3/80 | 0/80 | -0.037 | [-0.087, +0.000] | 0 | 3 | 0.2500 |
| distractor | unsure_right | unsure | 3/80 | 21/80 | +0.225 | [+0.125, +0.325] | 19 | 1 | 4.01e-05 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm A | stratum right | target distractor

Source files: test__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/40 | 37 | 2 | 1 | 0 | 0 |  |
| none | unsure | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 2/40 | 37 | 2 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| reliable | unsure | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| unreliable | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unreliable | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
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
| d_c = certain\|certain_right - certain\|unsure_right | 1/40 | 0/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/40 | 0/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 2/40 | 1/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/40 | 1/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1/40 | 0/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 2/40 | 1/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm A | stratum wrong | target distractor

Source files: test__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 8/80 | 70 | 8 | 2 | 0 | 0 |  |
| none | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| reliable | certain | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| reliable | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

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
| unsure\|perfect_mixed - unsure\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 12/80 | 0/80 | +0.150 | [+0.075, +0.225] | 12 | 0 | 0.0005 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 8/80 | 1/80 | +0.087 | [+0.025, +0.150] | 7 | 0 | 0.0156 | both cells non-missing, n = 80 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm A | stratum wrong | target key

Source files: test__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl, test__openrouter_deepseek_deepseek-v3.2__instant__A__rep2.jsonl. Items: 80. Replicates: [1, 2]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 32/80 | 47 | 32 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| none | unsure | 7/80 | 73 | 7 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | certain | 34/80 | 46 | 34 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | unsure | 3/80 | 77 | 3 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | certain | 33/80 | 47 | 33 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | unsure | 3/80 | 77 | 3 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | certain | 8/80 | 72 | 8 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | certain | 13/80 | 67 | 13 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | certain | 31/80 | 47 | 31 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | unsure | 4/80 | 76 | 4 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | certain | 15/80 | 65 | 15 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | unsure | 3/80 | 77 | 3 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | certain | 11/80 | 69 | 11 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | certain | 15/80 | 65 | 15 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | certain | 12/80 | 68 | 12 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | certain | 12/80 | 68 | 12 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | certain | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right | certain | 6.50/80 | 147 | 13 | 0 | 0 | 0 | rep1_vs_rep2: 75/80 |
| certain_right | unsure | 0.50/80 | 159 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 79/80 |
| unsure_right | certain | 0/80 | 160 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | unsure | 0.50/80 | 159 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 79/80 |
| certain_right_nosum | certain | 3/80 | 77 | 3 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_nosum | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | certain | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | certain | 7/80 | 73 | 7 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | certain | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| control | none | 0/80 | 160 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 80/80 |
| certain_right | none | 0/80 | 160 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | none | 0/80 | 160 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 80/80 |
| perfect_mixed | none | 0/80 | 80 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 0/80 | 0 |
| certain_right log shown | 0/80 | 0/80 | 0 |
| unsure_right log shown | 0/80 | 0/80 | 0 |
| perfect_mixed log shown | 0/80 | 0/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 6.50/80 | 0/80 | +0.081 | [+0.031, +0.138] | 9 | 0 | 0.0039 | no-log control + four core cells non-missing, n = 80 | +0.081, +0.081 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0.50/80 | 0.50/80 | +0.000 | [-0.019, +0.019] | 1 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.081 | [+0.031, +0.138] | 9 | 0 | 0.0039 | no-log control + four core cells non-missing, n = 80 | +0.081, +0.081 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.081 | [+0.025, +0.144] | 9 | 1 | 0.0215 | no-log control + four core cells non-missing, n = 80 | +0.081, +0.081 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 7/80 | 0/80 | +0.087 | [+0.025, +0.150] | 7 | 0 | 0.0156 | four long cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four long cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.087 | [+0.025, +0.150] | 7 | 0 | 0.0156 | four long cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.087 | [+0.025, +0.150] | 7 | 0 | 0.0156 | four long cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | four nosum cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | four nosum cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | four nosum cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 4/80 | 3/80 | +0.013 | [-0.025, +0.050] | 2 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 4/80 | 2/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | both cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 4/80 | 0.50/80 | +0.044 | [+0.006, +0.094] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 | +0.044, +0.044 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 31/80 | 15/80 | +0.200 | [+0.100, +0.300] | 18 | 2 | 0.0004 | both cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 31/80 | 12/80 | +0.237 | [+0.150, +0.338] | 19 | 0 | 3.81e-06 | both cells non-missing, n = 80 | +0.237, +0.237 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 31/80 | 6.50/80 | +0.306 | [+0.206, +0.406] | 27 | 0 | 1.49e-08 | both cells non-missing, n = 80 | +0.306, +0.306 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 34/80 | 8/80 | +0.325 | [+0.212, +0.438] | 27 | 1 | 2.16e-07 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 12/80 | 2/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 3/80 | 7/80 | -0.050 | [-0.125, +0.013] | 2 | 6 | 0.2891 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 6.50/80 | 0.50/80 | +0.075 | [+0.025, +0.131] | 9 | 1 | 0.0215 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 32/80 | 7/80 | +0.312 | [+0.212, +0.412] | 25 | 0 | 5.96e-08 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm B | stratum wrong | target distractor

Source files: test__openrouter_deepseek_deepseek-v3.2__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 4/80 | 74 | 4 | 2 | 0 | 0 |  |
| none | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| reliable | certain | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| reliable | unsure | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| certain_right | certain | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| unsure_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

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
| unsure\|perfect_mixed - unsure\|unsure_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 12/80 | 0/80 | +0.150 | [+0.075, +0.237] | 12 | 0 | 0.0005 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 4/80 | 0/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm B | stratum wrong | target key

Source files: test__openrouter_deepseek_deepseek-v3.2__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 26/80 | 54 | 26 | 0 | 0 | 0 |  |
| none | unsure | 6/80 | 74 | 6 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 30/80 | 50 | 30 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 11/80 | 69 | 11 | 0 | 0 | 0 |  |
| reliable | certain | 6/80 | 74 | 6 | 0 | 0 | 0 |  |
| reliable | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| certain_right | certain | 4/80 | 76 | 4 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| unsure_right | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| control | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unsure_right | none | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 0/80 | 0 |
| certain_right log shown | 2/80 | 2/80 | 0 |
| unsure_right log shown | 1/80 | 1/80 | 0 |
| perfect_mixed log shown | 0/80 | 0/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 4/80 | 3/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 11/80 | 1/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 30/80 | 4/80 | +0.325 | [+0.212, +0.438] | 27 | 1 | 2.16e-07 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 6/80 | 1/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 4/80 | 1/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 26/80 | 6/80 | +0.250 | [+0.163, +0.350] | 20 | 0 | 1.91e-06 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm M | stratum wrong | target distractor

Source files: test__openrouter_deepseek_deepseek-v3.2__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

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

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm M | stratum wrong | target key

Source files: test__openrouter_deepseek_deepseek-v3.2__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 53/80 | 27 | 53 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 25/80 | 55 | 25 | 0 | 0 | 0 |  |
| reliable | certain | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| reliable | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| certain_right | certain | 6/80 | 74 | 6 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 3/80 | 77 | 3 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 6/80 | 0/80 | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.075, +0.075 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.037, +0.037 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.113, +0.113 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.037 | [-0.037, +0.113] | 6 | 3 | 0.5078 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.037, +0.037 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 25/80 | 3/80 | +0.275 | [+0.175, +0.375] | 22 | 0 | 4.77e-07 | both cells non-missing, n = 80 | +0.275, +0.275 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 53/80 | 6/80 | +0.588 | [+0.475, +0.700] | 47 | 0 | 1.42e-14 | both cells non-missing, n = 80 | +0.588, +0.588 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 12/80 | 2/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 6/80 | 3/80 | +0.037 | [-0.037, +0.113] | 6 | 3 | 0.5078 | both cells non-missing, n = 80 |

## openrouter:deepseek/deepseek-v3.2 | deliberative | arm A | stratum wrong | target distractor

Source files: test__openrouter_deepseek_deepseek-v3.2__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 8/80 | 59 | 8 | 13 | 0 | 0 |  |
| none | unsure | 3/80 | 65 | 3 | 12 | 0 | 0 |  |
| perfect_mixed | certain | 7/80 | 62 | 7 | 11 | 0 | 0 |  |
| perfect_mixed | unsure | 4/80 | 66 | 4 | 10 | 0 | 0 |  |
| certain_right | certain | 2/80 | 66 | 2 | 12 | 0 | 0 |  |
| certain_right | unsure | 2/80 | 67 | 2 | 11 | 0 | 0 |  |
| unsure_right | certain | 2/80 | 64 | 2 | 14 | 0 | 0 |  |
| unsure_right | unsure | 3/80 | 70 | 3 | 7 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/80 | 2/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 4/80 | 3/80 | +0.013 | [-0.025, +0.050] | 2 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 7/80 | 2/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 | +0.062, +0.062 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/80 | 3/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 8/80 | 3/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |

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

## openrouter:deepseek/deepseek-v3.2 | deliberative | arm A | stratum wrong | target key

Source files: test__openrouter_deepseek_deepseek-v3.2__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 36/80 | 40 | 36 | 4 | 0 | 0 |  |
| none | unsure | 26/80 | 51 | 26 | 3 | 0 | 0 |  |
| all_certain | certain | 25/80 | 52 | 25 | 3 | 0 | 0 |  |
| all_certain | unsure | 23/80 | 53 | 23 | 4 | 0 | 0 |  |
| all_unsure | certain | 28/80 | 50 | 28 | 2 | 0 | 0 |  |
| all_unsure | unsure | 19/80 | 59 | 19 | 2 | 0 | 0 |  |
| perfect_mixed | certain | 26/80 | 51 | 26 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 27/80 | 51 | 27 | 2 | 0 | 0 |  |
| reliable | certain | 28/80 | 50 | 28 | 2 | 0 | 0 |  |
| reliable | unsure | 21/80 | 57 | 21 | 2 | 0 | 0 |  |
| certain_right | certain | 23/80 | 54 | 23 | 3 | 0 | 0 |  |
| certain_right | unsure | 21/80 | 55 | 21 | 4 | 0 | 0 |  |
| unsure_right | certain | 15/80 | 61 | 15 | 4 | 0 | 0 |  |
| unsure_right | unsure | 14/80 | 63 | 14 | 3 | 0 | 0 |  |
| certain_right_nosum | certain | 19/80 | 58 | 19 | 3 | 0 | 0 |  |
| certain_right_nosum | unsure | 17/80 | 61 | 17 | 2 | 0 | 0 |  |
| unsure_right_nosum | certain | 17/80 | 60 | 17 | 3 | 0 | 0 |  |
| unsure_right_nosum | unsure | 18/80 | 59 | 18 | 3 | 0 | 0 |  |
| control | none | 8/80 | 69 | 8 | 3 | 0 | 0 |  |
| certain_right | none | 4/80 | 71 | 4 | 5 | 0 | 0 |  |
| unsure_right | none | 7/80 | 69 | 7 | 4 | 0 | 0 |  |
| perfect_mixed | none | 5/80 | 72 | 5 | 3 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 8/80 | 11/80 | 0 |
| certain_right log shown | 4/80 | 9/80 | 0 |
| unsure_right log shown | 7/80 | 11/80 | 0 |
| perfect_mixed log shown | 5/80 | 8/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 23/80 | 15/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 | no-log control + four core cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 14/80 | 21/80 | -0.087 | [-0.150, -0.025] | 0 | 7 | 0.0156 | no-log control + four core cells non-missing, n = 80 | -0.087, -0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.013 | [-0.062, +0.087] | 5 | 4 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.188 | [+0.075, +0.312] | 12 | 1 | 0.0034 | no-log control + four core cells non-missing, n = 80 | +0.188, +0.188 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 19/80 | 17/80 | +0.025 | [-0.037, +0.100] | 5 | 3 | 0.7266 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 18/80 | 17/80 | +0.013 | [-0.062, +0.087] | 5 | 4 | 1.0000 | four nosum cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.037 | [-0.075, +0.150] | 7 | 5 | 0.7744 | four nosum cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.013 | [-0.075, +0.100] | 5 | 5 | 1.0000 | four nosum cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 27/80 | 14/80 | +0.163 | [+0.075, +0.250] | 14 | 1 | 0.0010 | both cells non-missing, n = 80 | +0.163, +0.163 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 26/80 | 23/80 | +0.037 | [-0.050, +0.125] | 8 | 5 | 0.5811 | both cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 28/80 | 21/80 | +0.087 | [+0.000, +0.188] | 11 | 4 | 0.1185 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 19/80 | 26/80 | -0.087 | [-0.163, -0.013] | 2 | 9 | 0.0654 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 23/80 | 14/80 | +0.113 | [+0.037, +0.188] | 10 | 1 | 0.0117 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 36/80 | 26/80 | +0.125 | [+0.050, +0.212] | 11 | 1 | 0.0063 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 4/80 | 8/80 | -0.050 | [-0.100, -0.013] | 0 | 4 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 9/80 | 11/80 | -0.025 | [-0.087, +0.037] | 2 | 4 | 0.6875 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 7/80 | 8/80 | -0.013 | [-0.050, +0.025] | 1 | 2 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 11/80 | 11/80 | +0.000 | [-0.050, +0.050] | 2 | 2 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 5/80 | 8/80 | -0.037 | [-0.087, +0.013] | 1 | 4 | 0.3750 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 8/80 | 11/80 | -0.037 | [-0.100, +0.013] | 1 | 4 | 0.3750 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 16/69 | 9/69 | +0.101 | [+0.029, +0.188] | 8 | 1 | 0.0391 | no-log control + four core cells non-missing, n = 69 | +0.101, +0.101 (N = 69) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 8/69 | 14/69 | -0.087 | [-0.159, -0.029] | 0 | 6 | 0.0312 | no-log control + four core cells non-missing, n = 69 | -0.087, -0.087 (N = 69) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.014 | [-0.058, +0.087] | 4 | 3 | 1.0000 | no-log control + four core cells non-missing, n = 69 | +0.014, +0.014 (N = 69) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.188 | [+0.072, +0.319] | 10 | 1 | 0.0117 | no-log control + four core cells non-missing, n = 69 | +0.188, +0.188 (N = 69) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 12/69 | 10/69 | +0.029 | [-0.043, +0.116] | 5 | 3 | 0.7266 | four nosum cells non-missing, n = 69 | +0.029, +0.029 (N = 69) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 11/69 | 10/69 | +0.014 | [-0.072, +0.101] | 5 | 4 | 1.0000 | four nosum cells non-missing, n = 69 | +0.014, +0.014 (N = 69) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.043 | [-0.087, +0.174] | 7 | 5 | 0.7744 | four nosum cells non-missing, n = 69 | +0.043, +0.043 (N = 69) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.014 | [-0.087, +0.116] | 5 | 5 | 1.0000 | four nosum cells non-missing, n = 69 | +0.014, +0.014 (N = 69) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 19/69 | 8/69 | +0.159 | [+0.072, +0.261] | 12 | 1 | 0.0034 | both cells non-missing, n = 69 | +0.159, +0.159 (N = 69) |
| certain\|perfect_mixed - certain\|certain_right | 19/69 | 16/69 | +0.043 | [-0.043, +0.130] | 7 | 4 | 0.5488 | both cells non-missing, n = 69 | +0.043, +0.043 (N = 69) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 20/69 | 15/69 | +0.072 | [-0.014, +0.174] | 8 | 3 | 0.2266 | both cells non-missing, n = 69 |
| ceiling check: unsure\|all_unsure - unsure\|none | 13/69 | 20/69 | -0.101 | [-0.188, -0.029] | 1 | 8 | 0.0391 | both cells non-missing, n = 69 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 16/69 | 8/69 | +0.116 | [+0.029, +0.203] | 9 | 1 | 0.0215 | both cells non-missing, n = 69 |
| no-log tone gap: certain\|none - unsure\|none | 27/69 | 20/69 | +0.101 | [+0.029, +0.188] | 8 | 1 | 0.0391 | both cells non-missing, n = 69 |
| moved to x: certain_right log, no objection - no-log control | 0/69 | 0/69 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 69 |
| changed at all: certain_right log, no objection - no-log control | 2/69 | 0/69 | +0.029 | [+0.000, +0.072] | 2 | 0 | 0.5000 | both cells non-missing, n = 69 |
| moved to x: unsure_right log, no objection - no-log control | 0/69 | 0/69 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 69 |
| changed at all: unsure_right log, no objection - no-log control | 2/69 | 0/69 | +0.029 | [+0.000, +0.072] | 2 | 0 | 0.5000 | both cells non-missing, n = 69 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/69 | 0/69 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 69 |
| changed at all: perfect_mixed log, no objection - no-log control | 1/69 | 0/69 | +0.014 | [+0.000, +0.043] | 1 | 0 | 1.0000 | both cells non-missing, n = 69 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm A | stratum right | target distractor

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/40 | 35 | 2 | 3 | 0 | 0 |  |
| none | unsure | 1/40 | 35 | 1 | 4 | 0 | 0 |  |
| perfect_mixed | certain | 8/40 | 29 | 8 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 2/40 | 36 | 2 | 2 | 0 | 0 |  |
| reliable | certain | 6/40 | 31 | 6 | 3 | 0 | 0 |  |
| reliable | unsure | 2/40 | 36 | 2 | 2 | 0 | 0 |  |
| unreliable | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unreliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| certain_right | certain | 5/40 | 33 | 5 | 2 | 0 | 0 |  |
| certain_right | unsure | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| unsure_right | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unsure_right | unsure | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| control | none | 0/40 | 38 | 0 | 2 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/40 | 2/40 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 5/40 | 0/40 | +0.125 | [+0.025, +0.225] | 5 | 0 | 0.0625 | no-log control + four core cells non-missing, n = 40 | +0.125, +0.125 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/40 | 1/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.125 | [+0.025, +0.225] | 5 | 0 | 0.0625 | no-log control + four core cells non-missing, n = 40 | +0.125, +0.125 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.125 | [+0.025, +0.225] | 5 | 0 | 0.0625 | no-log control + four core cells non-missing, n = 40 | +0.125, +0.125 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/40 | 1/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 8/40 | 5/40 | +0.075 | [+0.000, +0.175] | 3 | 0 | 0.2500 | both cells non-missing, n = 40 | +0.075, +0.075 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 6/40 | 2/40 | +0.100 | [+0.025, +0.200] | 4 | 0 | 0.1250 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 5/40 | 1/40 | +0.100 | [+0.025, +0.200] | 4 | 0 | 0.1250 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 2/40 | 1/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm A | stratum wrong | target distractor

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 17/80 | 33 | 17 | 30 | 0 | 0 |  |
| none | unsure | 9/80 | 33 | 9 | 38 | 0 | 0 |  |
| perfect_mixed | certain | 30/80 | 21 | 30 | 29 | 0 | 0 |  |
| perfect_mixed | unsure | 13/80 | 41 | 13 | 26 | 0 | 0 |  |
| reliable | certain | 25/80 | 29 | 25 | 26 | 0 | 0 |  |
| reliable | unsure | 8/80 | 45 | 8 | 27 | 0 | 0 |  |
| certain_right | certain | 22/80 | 32 | 22 | 26 | 0 | 0 |  |
| certain_right | unsure | 5/80 | 54 | 5 | 21 | 0 | 0 |  |
| unsure_right | certain | 6/80 | 58 | 6 | 16 | 0 | 0 |  |
| unsure_right | unsure | 5/80 | 59 | 5 | 16 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 22/80 | 6/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 5/80 | 5/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 13/80 | 5/80 | +0.100 | [+0.037, +0.163] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 30/80 | 22/80 | +0.100 | [+0.013, +0.188] | 11 | 3 | 0.0574 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 25/80 | 8/80 | +0.212 | [+0.125, +0.300] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 22/80 | 5/80 | +0.212 | [+0.125, +0.300] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 17/80 | 9/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm A | stratum wrong | target key

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl, test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A__rep2.jsonl. Items: 80. Replicates: [1, 2]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 64/80 | 12 | 64 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| none | unsure | 53/80 | 16 | 53 | 11 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | certain | 72/80 | 2 | 72 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | unsure | 60/80 | 15 | 60 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | certain | 67/80 | 8 | 67 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | unsure | 62/80 | 11 | 62 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | certain | 68/80 | 7 | 68 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | unsure | 53/80 | 22 | 53 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | certain | 66/80 | 8 | 66 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | unsure | 52/80 | 23 | 52 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | certain | 70/80 | 3 | 70 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | unsure | 60/80 | 14 | 60 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | certain | 69/80 | 6 | 69 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | unsure | 52/80 | 20 | 52 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | certain | 62/80 | 11 | 62 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | unsure | 48/80 | 24 | 48 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | certain | 70/80 | 5 | 70 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | unsure | 52/80 | 21 | 52 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | certain | 69/80 | 6 | 69 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | unsure | 51/80 | 22 | 51 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | certain | 68/80 | 8 | 68 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | unsure | 50/80 | 22 | 50 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | certain | 19/80 | 58 | 19 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | unsure | 13/80 | 65 | 13 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right | certain | 61.50/80 | 25 | 123 | 12 | 0 | 0 | rep1_vs_rep2: 79/80 |
| certain_right | unsure | 32/80 | 81 | 64 | 15 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | certain | 21.50/80 | 103 | 43 | 14 | 0 | 0 | rep1_vs_rep2: 79/80 |
| unsure_right | unsure | 25/80 | 97 | 50 | 13 | 0 | 0 | rep1_vs_rep2: 80/80 |
| certain_right_nosum | certain | 63/80 | 12 | 63 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_nosum | unsure | 39/80 | 33 | 39 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | certain | 33/80 | 43 | 33 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | unsure | 29/80 | 47 | 29 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | certain | 62/80 | 12 | 62 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | unsure | 27/80 | 46 | 27 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | certain | 24/80 | 52 | 24 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | unsure | 26/80 | 50 | 26 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| control | none | 15.50/80 | 101 | 31 | 28 | 0 | 0 | rep1_vs_rep2: 79/80 |
| certain_right | none | 18/80 | 96 | 36 | 28 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | none | 19/80 | 96 | 38 | 26 | 0 | 0 | rep1_vs_rep2: 80/80 |
| perfect_mixed | none | 17/80 | 49 | 17 | 14 | 0 | 0 | rep1_vs_rep2: 0/0 |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 15.50/80 | 29.50/80 | 0 |
| certain_right log shown | 18/80 | 32/80 | 0 |
| unsure_right log shown | 19/80 | 32/80 | 0 |
| perfect_mixed log shown | 17/80 | 31/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 61.50/80 | 21.50/80 | +0.500 | [+0.394, +0.613] | 41 | 0 | 9.09e-13 | no-log control + four core cells non-missing, n = 80 | +0.500, +0.500 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 25/80 | 32/80 | -0.087 | [-0.150, -0.037] | 0 | 7 | 0.0156 | no-log control + four core cells non-missing, n = 80 | -0.087, -0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.412 | [+0.306, +0.519] | 34 | 0 | 1.16e-10 | no-log control + four core cells non-missing, n = 80 | +0.412, +0.412 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.588 | [+0.450, +0.731] | 41 | 0 | 9.09e-13 | no-log control + four core cells non-missing, n = 80 | +0.588, +0.588 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 62/80 | 24/80 | +0.475 | [+0.362, +0.588] | 38 | 0 | 7.28e-12 | four long cells non-missing, n = 80 | +0.475, +0.475 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 26/80 | 27/80 | -0.013 | [-0.062, +0.025] | 1 | 2 | 1.0000 | four long cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.463 | [+0.350, +0.575] | 38 | 1 | 1.46e-10 | four long cells non-missing, n = 80 | +0.463, +0.463 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.487 | [+0.362, +0.613] | 39 | 1 | 7.46e-11 | four long cells non-missing, n = 80 | +0.487, +0.487 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 63/80 | 33/80 | +0.375 | [+0.275, +0.487] | 30 | 0 | 1.86e-09 | four nosum cells non-missing, n = 80 | +0.375, +0.375 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 29/80 | 39/80 | -0.125 | [-0.200, -0.062] | 0 | 10 | 0.0020 | four nosum cells non-missing, n = 80 | -0.125, -0.125 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.250 | [+0.138, +0.375] | 24 | 4 | 0.0002 | four nosum cells non-missing, n = 80 | +0.250, +0.250 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.500 | [+0.362, +0.637] | 34 | 0 | 1.16e-10 | four nosum cells non-missing, n = 80 | +0.500, +0.500 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 60/80 | 52/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 60/80 | 48/80 | +0.150 | [+0.075, +0.237] | 12 | 0 | 0.0005 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 60/80 | 25/80 | +0.438 | [+0.325, +0.550] | 35 | 0 | 5.82e-11 | both cells non-missing, n = 80 | +0.438, +0.438 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 70/80 | 70/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 70/80 | 69/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 70/80 | 61.50/80 | +0.106 | [+0.044, +0.175] | 9 | 0 | 0.0039 | both cells non-missing, n = 80 | +0.106, +0.106 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 62/80 | 52/80 | +0.125 | [+0.050, +0.212] | 11 | 1 | 0.0063 | both cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 72/80 | 68/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 68/80 | 50/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 62/80 | 53/80 | +0.113 | [+0.013, +0.212] | 13 | 4 | 0.0490 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 61.50/80 | 25/80 | +0.456 | [+0.350, +0.569] | 37 | 0 | 1.46e-11 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 64/80 | 53/80 | +0.138 | [+0.062, +0.212] | 11 | 0 | 0.0010 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 18/80 | 15.50/80 | +0.031 | [-0.044, +0.106] | 6 | 4 | 0.7539 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 32/80 | 29.50/80 | +0.031 | [-0.044, +0.106] | 6 | 4 | 0.7539 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 19/80 | 15.50/80 | +0.044 | [-0.031, +0.125] | 7 | 4 | 0.5488 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 32/80 | 29.50/80 | +0.031 | [-0.050, +0.113] | 7 | 5 | 0.7744 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 17/80 | 15.50/80 | +0.019 | [-0.050, +0.087] | 5 | 4 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 31/80 | 29.50/80 | +0.019 | [-0.050, +0.087] | 5 | 4 | 1.0000 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm B | stratum wrong | target distractor

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 16/80 | 30 | 16 | 34 | 0 | 0 |  |
| none | unsure | 10/80 | 35 | 10 | 35 | 0 | 0 |  |
| perfect_mixed | certain | 26/80 | 25 | 26 | 29 | 0 | 0 |  |
| perfect_mixed | unsure | 18/80 | 33 | 18 | 29 | 0 | 0 |  |
| reliable | certain | 17/80 | 38 | 17 | 25 | 0 | 0 |  |
| reliable | unsure | 9/80 | 43 | 9 | 28 | 0 | 0 |  |
| certain_right | certain | 10/80 | 49 | 10 | 21 | 0 | 0 |  |
| certain_right | unsure | 4/80 | 53 | 4 | 23 | 0 | 0 |  |
| unsure_right | certain | 6/80 | 48 | 6 | 26 | 0 | 0 |  |
| unsure_right | unsure | 7/80 | 49 | 7 | 24 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 10/80 | 6/80 | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.050, +0.050 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 7/80 | 4/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.037, +0.037 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.087 | [+0.025, +0.163] | 6 | 0 | 0.0312 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.087, +0.087 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.013 | [-0.062, +0.087] | 4 | 2 | 0.6875 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 18/80 | 7/80 | +0.138 | [+0.062, +0.212] | 11 | 0 | 0.0010 | both cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 26/80 | 10/80 | +0.200 | [+0.113, +0.300] | 17 | 1 | 0.0001 | both cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 17/80 | 9/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 10/80 | 7/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 16/80 | 10/80 | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm B | stratum wrong | target key

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 65/80 | 9 | 65 | 6 | 0 | 0 |  |
| none | unsure | 55/80 | 15 | 55 | 10 | 0 | 0 |  |
| perfect_mixed | certain | 71/80 | 5 | 71 | 4 | 0 | 0 |  |
| perfect_mixed | unsure | 65/80 | 9 | 65 | 6 | 0 | 0 |  |
| reliable | certain | 62/80 | 14 | 62 | 4 | 0 | 0 |  |
| reliable | unsure | 55/80 | 18 | 55 | 7 | 0 | 0 |  |
| certain_right | certain | 49/80 | 25 | 49 | 6 | 0 | 0 |  |
| certain_right | unsure | 28/80 | 42 | 28 | 10 | 0 | 0 |  |
| unsure_right | certain | 39/80 | 36 | 39 | 5 | 0 | 0 |  |
| unsure_right | unsure | 42/80 | 31 | 42 | 7 | 0 | 0 |  |
| control | none | 15/80 | 51 | 15 | 14 | 0 | 0 |  |
| certain_right | none | 18/80 | 50 | 18 | 12 | 0 | 0 |  |
| unsure_right | none | 20/80 | 47 | 20 | 13 | 0 | 0 |  |
| perfect_mixed | none | 19/80 | 51 | 19 | 10 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 15/80 | 29/80 | 0 |
| certain_right log shown | 18/80 | 30/80 | 0 |
| unsure_right log shown | 20/80 | 33/80 | 0 |
| perfect_mixed log shown | 19/80 | 29/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 49/80 | 39/80 | +0.125 | [+0.037, +0.225] | 13 | 3 | 0.0213 | no-log control + four core cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 42/80 | 28/80 | +0.175 | [+0.087, +0.275] | 16 | 2 | 0.0013 | no-log control + four core cells non-missing, n = 80 | +0.175, +0.175 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.300 | [+0.188, +0.412] | 24 | 1 | 1.55e-06 | no-log control + four core cells non-missing, n = 80 | +0.300, +0.300 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.050 | [-0.200, +0.100] | 12 | 16 | 0.5716 | no-log control + four core cells non-missing, n = 80 | -0.050, -0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 65/80 | 42/80 | +0.287 | [+0.188, +0.388] | 24 | 1 | 1.55e-06 | both cells non-missing, n = 80 | +0.287, +0.287 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 71/80 | 49/80 | +0.275 | [+0.175, +0.375] | 23 | 1 | 2.98e-06 | both cells non-missing, n = 80 | +0.275, +0.275 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 62/80 | 55/80 | +0.087 | [+0.025, +0.163] | 8 | 1 | 0.0391 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 49/80 | 42/80 | +0.087 | [-0.013, +0.188] | 13 | 6 | 0.1671 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 65/80 | 55/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 18/80 | 15/80 | +0.037 | [-0.037, +0.125] | 7 | 4 | 0.5488 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 30/80 | 29/80 | +0.013 | [-0.087, +0.100] | 8 | 7 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 20/80 | 15/80 | +0.062 | [-0.013, +0.150] | 8 | 3 | 0.2266 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 33/80 | 29/80 | +0.050 | [-0.037, +0.138] | 9 | 5 | 0.4240 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 19/80 | 15/80 | +0.050 | [-0.025, +0.125] | 7 | 3 | 0.3438 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 29/80 | 29/80 | +0.000 | [-0.087, +0.087] | 7 | 7 | 1.0000 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm M | stratum wrong | target distractor

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 8/80 | 63 | 8 | 9 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 76 | 0 | 4 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 74 | 0 | 6 | 0 | 0 |  |
| unsure_right | unsure | 13/80 | 61 | 13 | 6 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 8/80 | 0/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.100, +0.100 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 13/80 | 0/80 | +0.163 | [+0.087, +0.250] | 13 | 0 | 0.0002 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.163, +0.163 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.263 | [+0.150, +0.400] | 15 | 0 | 6.10e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.263, +0.263 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.062 | [-0.138, +0.013] | 2 | 7 | 0.1797 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.062, -0.062 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 8/80 | 13/80 | -0.062 | [-0.138, +0.013] | 2 | 7 | 0.1797 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm M | stratum wrong | target key

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 68/80 | 10 | 68 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 59/80 | 17 | 59 | 4 | 0 | 0 |  |
| reliable | certain | 50/80 | 29 | 50 | 1 | 0 | 0 |  |
| reliable | unsure | 28/80 | 51 | 28 | 1 | 0 | 0 |  |
| certain_right | certain | 40/80 | 39 | 40 | 1 | 0 | 0 |  |
| certain_right | unsure | 4/80 | 76 | 4 | 0 | 0 | 0 |  |
| unsure_right | certain | 7/80 | 73 | 7 | 0 | 0 | 0 |  |
| unsure_right | unsure | 30/80 | 50 | 30 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 40/80 | 7/80 | +0.412 | [+0.300, +0.525] | 33 | 0 | 2.33e-10 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.412, +0.412 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 30/80 | 4/80 | +0.325 | [+0.225, +0.438] | 26 | 0 | 2.98e-08 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.325, +0.325 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.738 | [+0.575, +0.912] | 43 | 0 | 2.27e-13 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.738, +0.738 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.087 | [-0.037, +0.212] | 17 | 10 | 0.2478 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.087, +0.087 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 59/80 | 30/80 | +0.362 | [+0.263, +0.463] | 29 | 0 | 3.73e-09 | both cells non-missing, n = 80 | +0.362, +0.362 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 68/80 | 40/80 | +0.350 | [+0.250, +0.450] | 28 | 0 | 7.45e-09 | both cells non-missing, n = 80 | +0.350, +0.350 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 50/80 | 28/80 | +0.275 | [+0.175, +0.375] | 22 | 0 | 4.77e-07 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 40/80 | 30/80 | +0.125 | [+0.000, +0.237] | 17 | 7 | 0.0639 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | arm A | stratum wrong | target distractor

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 30/80 | 39 | 30 | 11 | 0 | 0 |  |
| none | unsure | 12/80 | 50 | 12 | 18 | 0 | 0 |  |
| perfect_mixed | certain | 28/80 | 36 | 28 | 16 | 0 | 0 |  |
| perfect_mixed | unsure | 16/80 | 50 | 16 | 14 | 0 | 0 |  |
| certain_right | certain | 13/80 | 58 | 13 | 9 | 0 | 0 |  |
| certain_right | unsure | 5/80 | 63 | 5 | 12 | 0 | 0 |  |
| unsure_right | certain | 4/80 | 65 | 4 | 11 | 0 | 0 |  |
| unsure_right | unsure | 5/80 | 69 | 5 | 6 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 13/80 | 4/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.113, +0.113 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 5/80 | 5/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.113, +0.113 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.113, +0.113 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 16/80 | 5/80 | +0.138 | [+0.062, +0.212] | 11 | 0 | 0.0010 | both cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 28/80 | 13/80 | +0.188 | [+0.087, +0.287] | 17 | 2 | 0.0007 | both cells non-missing, n = 80 | +0.188, +0.188 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 13/80 | 5/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 30/80 | 12/80 | +0.225 | [+0.138, +0.312] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 80 |

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

## openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | arm A | stratum wrong | target key

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 71/80 | 6 | 71 | 3 | 0 | 0 |  |
| none | unsure | 62/80 | 14 | 62 | 4 | 0 | 0 |  |
| all_certain | certain | 70/80 | 9 | 70 | 1 | 0 | 0 |  |
| all_certain | unsure | 51/80 | 28 | 51 | 1 | 0 | 0 |  |
| all_unsure | certain | 69/80 | 8 | 69 | 3 | 0 | 0 |  |
| all_unsure | unsure | 58/80 | 20 | 58 | 2 | 0 | 0 |  |
| perfect_mixed | certain | 70/80 | 7 | 70 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 57/80 | 20 | 57 | 3 | 0 | 0 |  |
| reliable | certain | 64/80 | 13 | 64 | 3 | 0 | 0 |  |
| reliable | unsure | 49/80 | 30 | 49 | 1 | 0 | 0 |  |
| certain_right | certain | 52/80 | 27 | 52 | 1 | 0 | 0 |  |
| certain_right | unsure | 34/80 | 44 | 34 | 2 | 0 | 0 |  |
| unsure_right | certain | 29/80 | 49 | 29 | 2 | 0 | 0 |  |
| unsure_right | unsure | 26/80 | 52 | 26 | 2 | 0 | 0 |  |
| certain_right_nosum | certain | 54/80 | 23 | 54 | 3 | 0 | 0 |  |
| certain_right_nosum | unsure | 37/80 | 41 | 37 | 2 | 0 | 0 |  |
| unsure_right_nosum | certain | 29/80 | 49 | 29 | 2 | 0 | 0 |  |
| unsure_right_nosum | unsure | 31/80 | 47 | 31 | 2 | 0 | 0 |  |
| control | none | 4/80 | 71 | 4 | 5 | 0 | 0 |  |
| certain_right | none | 9/80 | 67 | 9 | 4 | 0 | 0 |  |
| unsure_right | none | 9/80 | 68 | 9 | 3 | 0 | 0 |  |
| perfect_mixed | none | 9/80 | 68 | 9 | 3 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 4/80 | 9/80 | 0 |
| certain_right log shown | 9/80 | 13/80 | 0 |
| unsure_right log shown | 9/80 | 12/80 | 0 |
| perfect_mixed log shown | 9/80 | 12/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 52/80 | 29/80 | +0.287 | [+0.188, +0.388] | 23 | 0 | 2.38e-07 | no-log control + four core cells non-missing, n = 80 | +0.287, +0.287 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 26/80 | 34/80 | -0.100 | [-0.188, -0.025] | 2 | 10 | 0.0386 | no-log control + four core cells non-missing, n = 80 | -0.100, -0.100 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.188 | [+0.075, +0.300] | 20 | 5 | 0.0041 | no-log control + four core cells non-missing, n = 80 | +0.188, +0.188 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.388 | [+0.250, +0.525] | 28 | 2 | 8.68e-07 | no-log control + four core cells non-missing, n = 80 | +0.388, +0.388 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 54/80 | 29/80 | +0.312 | [+0.212, +0.412] | 25 | 0 | 5.96e-08 | four nosum cells non-missing, n = 80 | +0.312, +0.312 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 31/80 | 37/80 | -0.075 | [-0.150, +0.000] | 2 | 8 | 0.1094 | four nosum cells non-missing, n = 80 | -0.075, -0.075 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.237 | [+0.113, +0.375] | 24 | 6 | 0.0014 | four nosum cells non-missing, n = 80 | +0.237, +0.237 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.388 | [+0.263, +0.512] | 30 | 1 | 2.98e-08 | four nosum cells non-missing, n = 80 | +0.388, +0.388 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 57/80 | 26/80 | +0.388 | [+0.287, +0.500] | 31 | 0 | 9.31e-10 | both cells non-missing, n = 80 | +0.388, +0.388 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 70/80 | 52/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 80 | +0.225, +0.225 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 64/80 | 49/80 | +0.188 | [+0.100, +0.275] | 15 | 0 | 6.10e-05 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 58/80 | 62/80 | -0.050 | [-0.138, +0.025] | 4 | 8 | 0.3877 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 52/80 | 26/80 | +0.325 | [+0.225, +0.425] | 26 | 0 | 2.98e-08 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 71/80 | 62/80 | +0.113 | [+0.037, +0.188] | 10 | 1 | 0.0117 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 9/80 | 4/80 | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 13/80 | 9/80 | +0.050 | [-0.013, +0.125] | 6 | 2 | 0.2891 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 9/80 | 4/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 12/80 | 9/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 9/80 | 4/80 | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 12/80 | 9/80 | +0.037 | [-0.037, +0.113] | 6 | 3 | 0.5078 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 45/71 | 25/71 | +0.282 | [+0.183, +0.381] | 20 | 0 | 1.91e-06 | no-log control + four core cells non-missing, n = 71 | +0.282, +0.282 (N = 71) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 21/71 | 28/71 | -0.099 | [-0.183, -0.014] | 2 | 9 | 0.0654 | no-log control + four core cells non-missing, n = 71 | -0.099, -0.099 (N = 71) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.183 | [+0.056, +0.310] | 18 | 5 | 0.0106 | no-log control + four core cells non-missing, n = 71 | +0.183, +0.183 (N = 71) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.380 | [+0.239, +0.535] | 25 | 2 | 5.65e-06 | no-log control + four core cells non-missing, n = 71 | +0.380, +0.380 (N = 71) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 48/71 | 25/71 | +0.324 | [+0.211, +0.437] | 23 | 0 | 2.38e-07 | four nosum cells non-missing, n = 71 | +0.324, +0.324 (N = 71) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 25/71 | 31/71 | -0.085 | [-0.169, +0.000] | 2 | 8 | 0.1094 | four nosum cells non-missing, n = 71 | -0.085, -0.085 (N = 71) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.239 | [+0.099, +0.380] | 22 | 6 | 0.0037 | four nosum cells non-missing, n = 71 | +0.239, +0.239 (N = 71) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.408 | [+0.281, +0.535] | 28 | 1 | 1.12e-07 | four nosum cells non-missing, n = 71 | +0.408, +0.408 (N = 71) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 50/71 | 21/71 | +0.408 | [+0.296, +0.521] | 29 | 0 | 3.73e-09 | both cells non-missing, n = 71 | +0.408, +0.408 (N = 71) |
| certain\|perfect_mixed - certain\|certain_right | 62/71 | 45/71 | +0.239 | [+0.141, +0.338] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 71 | +0.239, +0.239 (N = 71) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 56/71 | 42/71 | +0.197 | [+0.113, +0.296] | 14 | 0 | 0.0001 | both cells non-missing, n = 71 |
| ceiling check: unsure\|all_unsure - unsure\|none | 51/71 | 56/71 | -0.070 | [-0.155, +0.014] | 3 | 8 | 0.2266 | both cells non-missing, n = 71 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 45/71 | 21/71 | +0.338 | [+0.225, +0.451] | 24 | 0 | 1.19e-07 | both cells non-missing, n = 71 |
| no-log tone gap: certain\|none - unsure\|none | 63/71 | 56/71 | +0.099 | [+0.028, +0.183] | 8 | 1 | 0.0391 | both cells non-missing, n = 71 |
| moved to x: certain_right log, no objection - no-log control | 6/71 | 0/71 | +0.085 | [+0.028, +0.155] | 6 | 0 | 0.0312 | both cells non-missing, n = 71 |
| changed at all: certain_right log, no objection - no-log control | 6/71 | 0/71 | +0.085 | [+0.028, +0.155] | 6 | 0 | 0.0312 | both cells non-missing, n = 71 |
| moved to x: unsure_right log, no objection - no-log control | 5/71 | 0/71 | +0.070 | [+0.014, +0.141] | 5 | 0 | 0.0625 | both cells non-missing, n = 71 |
| changed at all: unsure_right log, no objection - no-log control | 5/71 | 0/71 | +0.070 | [+0.014, +0.141] | 5 | 0 | 0.0625 | both cells non-missing, n = 71 |
| moved to x: perfect_mixed log, no objection - no-log control | 6/71 | 0/71 | +0.085 | [+0.028, +0.155] | 6 | 0 | 0.0312 | both cells non-missing, n = 71 |
| changed at all: perfect_mixed log, no objection - no-log control | 6/71 | 0/71 | +0.085 | [+0.028, +0.155] | 6 | 0 | 0.0312 | both cells non-missing, n = 71 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm A | stratum right | target distractor

Source files: test__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 5/40 | 28 | 5 | 7 | 0 | 0 |  |
| none | unsure | 3/40 | 27 | 3 | 10 | 0 | 0 |  |
| perfect_mixed | certain | 15/40 | 24 | 15 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 6/40 | 33 | 6 | 1 | 0 | 0 |  |
| reliable | certain | 7/40 | 30 | 7 | 3 | 0 | 0 |  |
| reliable | unsure | 3/40 | 36 | 3 | 1 | 0 | 0 |  |
| unreliable | certain | 2/40 | 37 | 2 | 1 | 0 | 0 |  |
| unreliable | unsure | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| certain_right | certain | 5/40 | 32 | 5 | 3 | 0 | 0 |  |
| certain_right | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| unsure_right | certain | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| unsure_right | unsure | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| control | none | 1/40 | 35 | 1 | 4 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 1/40 | 5/40 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 5/40 | 1/40 | +0.100 | [+0.025, +0.200] | 4 | 0 | 0.1250 | no-log control + four core cells non-missing, n = 40 | +0.100, +0.100 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/40 | 2/40 | -0.025 | [-0.075, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 40 | -0.025, -0.025 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.075 | [+0.000, +0.175] | 3 | 0 | 0.2500 | no-log control + four core cells non-missing, n = 40 | +0.075, +0.075 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.125 | [+0.025, +0.275] | 4 | 0 | 0.1250 | no-log control + four core cells non-missing, n = 40 | +0.125, +0.125 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 6/40 | 1/40 | +0.125 | [+0.025, +0.225] | 5 | 0 | 0.0625 | both cells non-missing, n = 40 | +0.125, +0.125 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 15/40 | 5/40 | +0.250 | [+0.125, +0.375] | 10 | 0 | 0.0020 | both cells non-missing, n = 40 | +0.250, +0.250 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 7/40 | 3/40 | +0.100 | [+0.025, +0.200] | 4 | 0 | 0.1250 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 5/40 | 1/40 | +0.100 | [+0.025, +0.200] | 4 | 0 | 0.1250 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 5/40 | 3/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | both cells non-missing, n = 40 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm A | stratum wrong | target distractor

Source files: test__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 29/80 | 12 | 29 | 39 | 0 | 0 |  |
| none | unsure | 18/80 | 15 | 18 | 47 | 0 | 0 |  |
| perfect_mixed | certain | 44/80 | 14 | 44 | 22 | 0 | 0 |  |
| perfect_mixed | unsure | 23/80 | 33 | 23 | 24 | 0 | 0 |  |
| reliable | certain | 27/80 | 31 | 27 | 22 | 0 | 0 |  |
| reliable | unsure | 11/80 | 44 | 11 | 25 | 0 | 0 |  |
| certain_right | certain | 18/80 | 41 | 18 | 21 | 0 | 0 |  |
| certain_right | unsure | 4/80 | 59 | 4 | 17 | 0 | 0 |  |
| unsure_right | certain | 3/80 | 58 | 3 | 19 | 0 | 0 |  |
| unsure_right | unsure | 3/80 | 63 | 3 | 14 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 18/80 | 3/80 | +0.188 | [+0.113, +0.275] | 15 | 0 | 6.10e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.188, +0.188 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/80 | 4/80 | -0.013 | [-0.075, +0.037] | 2 | 3 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.175 | [+0.075, +0.287] | 14 | 2 | 0.0042 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.175, +0.175 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.200 | [+0.113, +0.300] | 15 | 0 | 6.10e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 23/80 | 3/80 | +0.250 | [+0.163, +0.350] | 20 | 0 | 1.91e-06 | both cells non-missing, n = 80 | +0.250, +0.250 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 44/80 | 18/80 | +0.325 | [+0.225, +0.425] | 26 | 0 | 2.98e-08 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 27/80 | 11/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 18/80 | 3/80 | +0.188 | [+0.113, +0.275] | 15 | 0 | 6.10e-05 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 29/80 | 18/80 | +0.138 | [+0.062, +0.225] | 12 | 1 | 0.0034 | both cells non-missing, n = 80 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm A | stratum wrong | target key

Source files: test__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl, test__openrouter_mistralai_ministral-14b-2512__instant__A__rep2.jsonl. Items: 80. Replicates: [1, 2]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 59/80 | 9 | 59 | 12 | 0 | 0 | rep1_vs_rep2: 0/0 |
| none | unsure | 45/80 | 12 | 45 | 23 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | certain | 77/80 | 2 | 77 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | unsure | 47/80 | 30 | 47 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | certain | 76/80 | 3 | 76 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | unsure | 54/80 | 21 | 54 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | certain | 65/80 | 13 | 65 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | unsure | 25/80 | 52 | 25 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | certain | 66/80 | 12 | 66 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | unsure | 27/80 | 46 | 27 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | certain | 72/80 | 6 | 72 | 2 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | unsure | 48/80 | 25 | 48 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | certain | 51/80 | 24 | 51 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | unsure | 28/80 | 46 | 28 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | certain | 52/80 | 22 | 52 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | unsure | 30/80 | 45 | 30 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | certain | 58/80 | 18 | 58 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | unsure | 33/80 | 41 | 33 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | certain | 55/80 | 22 | 55 | 3 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | unsure | 27/80 | 47 | 27 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | certain | 52/80 | 22 | 52 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | unsure | 27/80 | 46 | 27 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | certain | 10/80 | 66 | 10 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | unsure | 8/80 | 68 | 8 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right | certain | 35.50/80 | 76 | 71 | 13 | 0 | 0 | rep1_vs_rep2: 79/80 |
| certain_right | unsure | 14.50/80 | 125 | 29 | 6 | 0 | 0 | rep1_vs_rep2: 79/80 |
| unsure_right | certain | 12/80 | 125 | 24 | 11 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | unsure | 12/80 | 130 | 24 | 6 | 0 | 0 | rep1_vs_rep2: 80/80 |
| certain_right_nosum | certain | 43/80 | 31 | 43 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_nosum | unsure | 19/80 | 57 | 19 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | certain | 12/80 | 61 | 12 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | unsure | 10/80 | 66 | 10 | 4 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | certain | 44/80 | 28 | 44 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | unsure | 19/80 | 54 | 19 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | certain | 14/80 | 58 | 14 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | unsure | 14/80 | 60 | 14 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| control | none | 15/80 | 78 | 30 | 52 | 0 | 0 | rep1_vs_rep2: 78/80 |
| certain_right | none | 18/80 | 72 | 36 | 52 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | none | 18/80 | 78 | 36 | 46 | 0 | 0 | rep1_vs_rep2: 80/80 |
| perfect_mixed | none | 18/80 | 37 | 18 | 25 | 0 | 0 | rep1_vs_rep2: 0/0 |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 15/80 | 41/80 | 0 |
| certain_right log shown | 18/80 | 44/80 | 0 |
| unsure_right log shown | 18/80 | 41/80 | 0 |
| perfect_mixed log shown | 18/80 | 43/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 35.50/80 | 12/80 | +0.294 | [+0.188, +0.400] | 25 | 1 | 8.05e-07 | no-log control + four core cells non-missing, n = 80 | +0.294, +0.294 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 12/80 | 14.50/80 | -0.031 | [-0.100, +0.031] | 3 | 5 | 0.7266 | no-log control + four core cells non-missing, n = 80 | -0.031, -0.031 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.263 | [+0.144, +0.381] | 24 | 3 | 4.92e-05 | no-log control + four core cells non-missing, n = 80 | +0.263, +0.263 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.325 | [+0.200, +0.456] | 26 | 3 | 1.52e-05 | no-log control + four core cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 44/80 | 14/80 | +0.375 | [+0.275, +0.487] | 30 | 0 | 1.86e-09 | four long cells non-missing, n = 80 | +0.375, +0.375 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 14/80 | 19/80 | -0.062 | [-0.138, +0.013] | 2 | 7 | 0.1797 | four long cells non-missing, n = 80 | -0.062, -0.062 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.312 | [+0.188, +0.438] | 25 | 2 | 5.65e-06 | four long cells non-missing, n = 80 | +0.312, +0.312 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.438 | [+0.312, +0.575] | 30 | 0 | 1.86e-09 | four long cells non-missing, n = 80 | +0.438, +0.438 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 43/80 | 12/80 | +0.388 | [+0.287, +0.500] | 31 | 0 | 9.31e-10 | four nosum cells non-missing, n = 80 | +0.388, +0.388 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 10/80 | 19/80 | -0.113 | [-0.200, -0.025] | 2 | 11 | 0.0225 | four nosum cells non-missing, n = 80 | -0.113, -0.113 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.275 | [+0.150, +0.400] | 25 | 4 | 0.0001 | four nosum cells non-missing, n = 80 | +0.275, +0.275 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.500 | [+0.350, +0.650] | 34 | 1 | 2.10e-09 | four nosum cells non-missing, n = 80 | +0.500, +0.500 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 48/80 | 28/80 | +0.250 | [+0.150, +0.350] | 21 | 1 | 1.10e-05 | both cells non-missing, n = 80 | +0.250, +0.250 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 48/80 | 30/80 | +0.225 | [+0.125, +0.325] | 19 | 1 | 4.01e-05 | both cells non-missing, n = 80 | +0.225, +0.225 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 48/80 | 12/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | both cells non-missing, n = 80 | +0.450, +0.450 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 72/80 | 58/80 | +0.175 | [+0.100, +0.263] | 14 | 0 | 0.0001 | both cells non-missing, n = 80 | +0.175, +0.175 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 72/80 | 55/80 | +0.212 | [+0.125, +0.300] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 80 | +0.212, +0.212 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 72/80 | 35.50/80 | +0.456 | [+0.350, +0.562] | 37 | 0 | 1.46e-11 | both cells non-missing, n = 80 | +0.456, +0.456 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 54/80 | 27/80 | +0.338 | [+0.225, +0.450] | 28 | 1 | 1.12e-07 | both cells non-missing, n = 80 | +0.338, +0.338 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 77/80 | 65/80 | +0.150 | [+0.075, +0.237] | 12 | 0 | 0.0005 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 52/80 | 27/80 | +0.312 | [+0.200, +0.425] | 27 | 2 | 1.62e-06 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 54/80 | 45/80 | +0.113 | [+0.013, +0.212] | 14 | 5 | 0.0636 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 35.50/80 | 12/80 | +0.294 | [+0.200, +0.400] | 24 | 0 | 1.19e-07 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 59/80 | 45/80 | +0.175 | [+0.100, +0.263] | 14 | 0 | 0.0001 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 18/80 | 15/80 | +0.037 | [-0.025, +0.106] | 6 | 3 | 0.5078 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 44/80 | 41/80 | +0.037 | [-0.025, +0.100] | 6 | 2 | 0.2891 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 18/80 | 15/80 | +0.037 | [-0.025, +0.100] | 6 | 2 | 0.2891 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 41/80 | 41/80 | +0.000 | [-0.069, +0.069] | 5 | 4 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 18/80 | 15/80 | +0.037 | [-0.025, +0.100] | 6 | 2 | 0.2891 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 43/80 | 41/80 | +0.025 | [-0.037, +0.094] | 6 | 3 | 0.5078 | both cells non-missing, n = 80 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm B | stratum wrong | target distractor

Source files: test__openrouter_mistralai_ministral-14b-2512__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 30/80 | 11 | 30 | 39 | 0 | 0 |  |
| none | unsure | 20/80 | 13 | 20 | 47 | 0 | 0 |  |
| perfect_mixed | certain | 44/80 | 19 | 44 | 17 | 0 | 0 |  |
| perfect_mixed | unsure | 32/80 | 27 | 32 | 21 | 0 | 0 |  |
| reliable | certain | 9/80 | 46 | 9 | 25 | 0 | 0 |  |
| reliable | unsure | 5/80 | 54 | 5 | 21 | 0 | 0 |  |
| certain_right | certain | 7/80 | 51 | 7 | 22 | 0 | 0 |  |
| certain_right | unsure | 3/80 | 57 | 3 | 20 | 0 | 0 |  |
| unsure_right | certain | 2/80 | 55 | 2 | 23 | 0 | 0 |  |
| unsure_right | unsure | 3/80 | 59 | 3 | 18 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 7/80 | 2/80 | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.062, +0.062 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/80 | 3/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.062, +0.062 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.062, +0.062 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 32/80 | 3/80 | +0.362 | [+0.263, +0.475] | 29 | 0 | 3.73e-09 | both cells non-missing, n = 80 | +0.362, +0.362 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 44/80 | 7/80 | +0.463 | [+0.350, +0.575] | 37 | 0 | 1.46e-11 | both cells non-missing, n = 80 | +0.463, +0.463 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 9/80 | 5/80 | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 7/80 | 3/80 | +0.050 | [-0.013, +0.125] | 6 | 2 | 0.2891 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 30/80 | 20/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm B | stratum wrong | target key

Source files: test__openrouter_mistralai_ministral-14b-2512__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 60/80 | 9 | 60 | 11 | 0 | 0 |  |
| none | unsure | 51/80 | 8 | 51 | 21 | 0 | 0 |  |
| perfect_mixed | certain | 72/80 | 6 | 72 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 64/80 | 13 | 64 | 3 | 0 | 0 |  |
| reliable | certain | 33/80 | 39 | 33 | 8 | 0 | 0 |  |
| reliable | unsure | 30/80 | 41 | 30 | 9 | 0 | 0 |  |
| certain_right | certain | 19/80 | 55 | 19 | 6 | 0 | 0 |  |
| certain_right | unsure | 16/80 | 58 | 16 | 6 | 0 | 0 |  |
| unsure_right | certain | 22/80 | 52 | 22 | 6 | 0 | 0 |  |
| unsure_right | unsure | 20/80 | 55 | 20 | 5 | 0 | 0 |  |
| control | none | 16/80 | 39 | 16 | 25 | 0 | 0 |  |
| certain_right | none | 14/80 | 40 | 14 | 26 | 0 | 0 |  |
| unsure_right | none | 14/80 | 40 | 14 | 26 | 0 | 0 |  |
| perfect_mixed | none | 14/80 | 43 | 14 | 23 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 16/80 | 41/80 | 0 |
| certain_right log shown | 14/80 | 40/80 | 0 |
| unsure_right log shown | 14/80 | 40/80 | 0 |
| perfect_mixed log shown | 14/80 | 37/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 19/80 | 22/80 | -0.037 | [-0.138, +0.062] | 7 | 10 | 0.6291 | no-log control + four core cells non-missing, n = 80 | -0.037, -0.037 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 20/80 | 16/80 | +0.050 | [-0.037, +0.138] | 8 | 4 | 0.3877 | no-log control + four core cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.013 | [-0.087, +0.113] | 9 | 8 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.087 | [-0.250, +0.062] | 8 | 15 | 0.2100 | no-log control + four core cells non-missing, n = 80 | -0.087, -0.087 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 64/80 | 20/80 | +0.550 | [+0.438, +0.662] | 44 | 0 | 1.14e-13 | both cells non-missing, n = 80 | +0.550, +0.550 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 72/80 | 19/80 | +0.662 | [+0.562, +0.762] | 53 | 0 | 2.22e-16 | both cells non-missing, n = 80 | +0.662, +0.662 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 33/80 | 30/80 | +0.037 | [-0.050, +0.125] | 8 | 5 | 0.5811 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 19/80 | 20/80 | -0.013 | [-0.113, +0.087] | 7 | 8 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 60/80 | 51/80 | +0.113 | [+0.037, +0.188] | 10 | 1 | 0.0117 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 14/80 | 16/80 | -0.025 | [-0.087, +0.037] | 3 | 5 | 0.7266 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 40/80 | 41/80 | -0.013 | [-0.100, +0.075] | 6 | 7 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 14/80 | 16/80 | -0.025 | [-0.100, +0.050] | 4 | 6 | 0.7539 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 40/80 | 41/80 | -0.013 | [-0.100, +0.075] | 6 | 7 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 14/80 | 16/80 | -0.025 | [-0.100, +0.050] | 4 | 6 | 0.7539 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 37/80 | 41/80 | -0.050 | [-0.150, +0.050] | 6 | 10 | 0.4545 | both cells non-missing, n = 80 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm M | stratum wrong | target distractor

Source files: test__openrouter_mistralai_ministral-14b-2512__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 14/80 | 57 | 14 | 9 | 0 | 0 |  |
| certain_right | unsure | 5/80 | 64 | 5 | 11 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 67 | 0 | 13 | 0 | 0 |  |
| unsure_right | unsure | 21/80 | 54 | 21 | 5 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 14/80 | 0/80 | +0.175 | [+0.100, +0.263] | 14 | 0 | 0.0001 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.175, +0.175 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 21/80 | 5/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.375 | [+0.250, +0.512] | 25 | 0 | 5.96e-08 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.375, +0.375 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.025 | [-0.138, +0.087] | 9 | 11 | 0.8238 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.025, -0.025 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 14/80 | 21/80 | -0.087 | [-0.188, +0.000] | 4 | 11 | 0.1185 | both cells non-missing, n = 80 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm M | stratum wrong | target key

Source files: test__openrouter_mistralai_ministral-14b-2512__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 57/80 | 19 | 57 | 4 | 0 | 0 |  |
| perfect_mixed | unsure | 53/80 | 25 | 53 | 2 | 0 | 0 |  |
| reliable | certain | 22/80 | 53 | 22 | 5 | 0 | 0 |  |
| reliable | unsure | 29/80 | 49 | 29 | 2 | 0 | 0 |  |
| certain_right | certain | 14/80 | 62 | 14 | 4 | 0 | 0 |  |
| certain_right | unsure | 6/80 | 69 | 6 | 5 | 0 | 0 |  |
| unsure_right | certain | 3/80 | 72 | 3 | 5 | 0 | 0 |  |
| unsure_right | unsure | 27/80 | 51 | 27 | 2 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 14/80 | 3/80 | +0.138 | [+0.062, +0.225] | 12 | 1 | 0.0034 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.138, +0.138 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 27/80 | 6/80 | +0.263 | [+0.175, +0.362] | 21 | 0 | 9.54e-07 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.263, +0.263 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.400 | [+0.263, +0.537] | 28 | 1 | 1.12e-07 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.400, +0.400 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.125 | [-0.237, -0.013] | 7 | 17 | 0.0639 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.125, -0.125 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 53/80 | 27/80 | +0.325 | [+0.200, +0.450] | 29 | 3 | 2.56e-06 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 57/80 | 14/80 | +0.537 | [+0.425, +0.650] | 43 | 0 | 2.27e-13 | both cells non-missing, n = 80 | +0.537, +0.537 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 22/80 | 29/80 | -0.087 | [-0.163, -0.013] | 2 | 9 | 0.0654 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 14/80 | 27/80 | -0.163 | [-0.263, -0.075] | 2 | 15 | 0.0023 | both cells non-missing, n = 80 |

## openrouter:mistralai/ministral-14b-2512 | deliberative | arm A | stratum wrong | target distractor

Source files: test__openrouter_mistralai_ministral-14b-2512__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 49/80 | 18 | 49 | 13 | 0 | 0 |  |
| none | unsure | 26/80 | 44 | 26 | 10 | 0 | 0 |  |
| perfect_mixed | certain | 52/80 | 18 | 52 | 10 | 0 | 0 |  |
| perfect_mixed | unsure | 24/80 | 51 | 24 | 5 | 0 | 0 |  |
| certain_right | certain | 41/80 | 30 | 41 | 9 | 0 | 0 |  |
| certain_right | unsure | 11/80 | 61 | 11 | 8 | 0 | 0 |  |
| unsure_right | certain | 20/80 | 48 | 20 | 12 | 0 | 0 |  |
| unsure_right | unsure | 11/80 | 62 | 11 | 7 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 41/80 | 20/80 | +0.263 | [+0.163, +0.362] | 21 | 0 | 9.54e-07 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.263, +0.263 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 11/80 | 11/80 | +0.000 | [-0.087, +0.087] | 6 | 6 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.263 | [+0.150, +0.388] | 23 | 3 | 8.80e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.263, +0.263 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.263 | [+0.125, +0.400] | 23 | 5 | 0.0009 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.263, +0.263 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 24/80 | 11/80 | +0.163 | [+0.075, +0.250] | 14 | 1 | 0.0010 | both cells non-missing, n = 80 | +0.163, +0.163 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 52/80 | 41/80 | +0.138 | [+0.062, +0.225] | 12 | 1 | 0.0034 | both cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 41/80 | 11/80 | +0.375 | [+0.275, +0.487] | 30 | 0 | 1.86e-09 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 49/80 | 26/80 | +0.287 | [+0.175, +0.400] | 26 | 3 | 1.52e-05 | both cells non-missing, n = 80 |

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

## openrouter:mistralai/ministral-14b-2512 | deliberative | arm A | stratum wrong | target key

Source files: test__openrouter_mistralai_ministral-14b-2512__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 69/80 | 9 | 69 | 2 | 0 | 0 |  |
| none | unsure | 54/80 | 23 | 54 | 3 | 0 | 0 |  |
| all_certain | certain | 69/80 | 10 | 69 | 1 | 0 | 0 |  |
| all_certain | unsure | 51/80 | 29 | 51 | 0 | 0 | 0 |  |
| all_unsure | certain | 72/80 | 8 | 72 | 0 | 0 | 0 |  |
| all_unsure | unsure | 43/80 | 32 | 43 | 5 | 0 | 0 |  |
| perfect_mixed | certain | 70/80 | 9 | 70 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 49/80 | 28 | 49 | 3 | 0 | 0 |  |
| reliable | certain | 65/79 | 14 | 65 | 0 | 1 (no answer 1) | 1 |  |
| reliable | unsure | 45/80 | 33 | 45 | 2 | 0 | 0 |  |
| certain_right | certain | 68/80 | 11 | 68 | 1 | 0 | 0 |  |
| certain_right | unsure | 29/80 | 49 | 29 | 2 | 0 | 0 |  |
| unsure_right | certain | 47/80 | 33 | 47 | 0 | 0 | 0 |  |
| unsure_right | unsure | 22/80 | 54 | 22 | 4 | 0 | 0 |  |
| certain_right_nosum | certain | 60/80 | 19 | 60 | 1 | 0 | 0 |  |
| certain_right_nosum | unsure | 26/80 | 51 | 26 | 3 | 0 | 0 |  |
| unsure_right_nosum | certain | 49/80 | 29 | 49 | 2 | 0 | 0 |  |
| unsure_right_nosum | unsure | 26/80 | 50 | 26 | 4 | 0 | 0 |  |
| control | none | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| certain_right | none | 3/80 | 75 | 3 | 2 | 0 | 0 |  |
| unsure_right | none | 2/80 | 73 | 2 | 5 | 0 | 0 |  |
| perfect_mixed | none | 3/80 | 74 | 3 | 3 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 2/80 | 4/80 | 0 |
| certain_right log shown | 3/80 | 5/80 | 0 |
| unsure_right log shown | 2/80 | 7/80 | 0 |
| perfect_mixed log shown | 3/80 | 6/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 68/80 | 47/80 | +0.263 | [+0.163, +0.362] | 22 | 1 | 5.72e-06 | no-log control + four core cells non-missing, n = 80 | +0.263, +0.263 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 22/80 | 29/80 | -0.087 | [-0.188, +0.000] | 4 | 11 | 0.1185 | no-log control + four core cells non-missing, n = 80 | -0.087, -0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.175 | [+0.050, +0.300] | 22 | 8 | 0.0161 | no-log control + four core cells non-missing, n = 80 | +0.175, +0.175 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.350 | [+0.200, +0.500] | 29 | 5 | 3.86e-05 | no-log control + four core cells non-missing, n = 80 | +0.350, +0.350 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 60/80 | 49/80 | +0.138 | [+0.037, +0.237] | 15 | 4 | 0.0192 | four nosum cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 26/80 | 26/80 | +0.000 | [-0.087, +0.087] | 6 | 6 | 1.0000 | four nosum cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.138 | [+0.013, +0.263] | 19 | 8 | 0.0522 | four nosum cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.138 | [-0.013, +0.275] | 20 | 9 | 0.0614 | four nosum cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 49/80 | 22/80 | +0.338 | [+0.212, +0.463] | 31 | 4 | 3.47e-06 | both cells non-missing, n = 80 | +0.338, +0.338 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 70/80 | 68/80 | +0.025 | [-0.050, +0.100] | 6 | 4 | 0.7539 | both cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 65/79 | 44/79 | +0.266 | [+0.165, +0.367] | 22 | 1 | 5.72e-06 | both cells non-missing, n = 79 |
| ceiling check: unsure\|all_unsure - unsure\|none | 43/80 | 54/80 | -0.138 | [-0.250, -0.025] | 6 | 17 | 0.0347 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 68/80 | 22/80 | +0.575 | [+0.463, +0.688] | 46 | 0 | 2.84e-14 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 69/80 | 54/80 | +0.188 | [+0.087, +0.287] | 17 | 2 | 0.0007 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 3/80 | 2/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 5/80 | 4/80 | +0.013 | [-0.037, +0.062] | 3 | 2 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 7/80 | 4/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 3/80 | 2/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 6/80 | 4/80 | +0.025 | [-0.037, +0.087] | 4 | 2 | 0.6875 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 64/76 | 43/76 | +0.276 | [+0.171, +0.382] | 22 | 1 | 5.72e-06 | no-log control + four core cells non-missing, n = 76 | +0.276, +0.276 (N = 76) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 19/76 | 26/76 | -0.092 | [-0.197, +0.000] | 4 | 11 | 0.1185 | no-log control + four core cells non-missing, n = 76 | -0.092, -0.092 (N = 76) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.184 | [+0.039, +0.316] | 22 | 8 | 0.0161 | no-log control + four core cells non-missing, n = 76 | +0.184, +0.184 (N = 76) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.368 | [+0.211, +0.526] | 29 | 5 | 3.86e-05 | no-log control + four core cells non-missing, n = 76 | +0.368, +0.368 (N = 76) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 56/76 | 45/76 | +0.145 | [+0.039, +0.250] | 15 | 4 | 0.0192 | four nosum cells non-missing, n = 76 | +0.145, +0.145 (N = 76) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 22/76 | 22/76 | +0.000 | [-0.092, +0.092] | 6 | 6 | 1.0000 | four nosum cells non-missing, n = 76 | +0.000, +0.000 (N = 76) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.145 | [+0.013, +0.276] | 19 | 8 | 0.0522 | four nosum cells non-missing, n = 76 | +0.145, +0.145 (N = 76) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.145 | [+0.000, +0.289] | 20 | 9 | 0.0614 | four nosum cells non-missing, n = 76 | +0.145, +0.145 (N = 76) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 46/76 | 19/76 | +0.355 | [+0.224, +0.487] | 31 | 4 | 3.47e-06 | both cells non-missing, n = 76 | +0.355, +0.355 (N = 76) |
| certain\|perfect_mixed - certain\|certain_right | 66/76 | 64/76 | +0.026 | [-0.053, +0.105] | 6 | 4 | 0.7539 | both cells non-missing, n = 76 | +0.026, +0.026 (N = 76) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 61/75 | 41/75 | +0.267 | [+0.160, +0.373] | 21 | 1 | 1.10e-05 | both cells non-missing, n = 75 |
| ceiling check: unsure\|all_unsure - unsure\|none | 40/76 | 51/76 | -0.145 | [-0.263, -0.026] | 6 | 17 | 0.0347 | both cells non-missing, n = 76 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 64/76 | 19/76 | +0.592 | [+0.487, +0.697] | 45 | 0 | 5.68e-14 | both cells non-missing, n = 76 |
| no-log tone gap: certain\|none - unsure\|none | 65/76 | 51/76 | +0.184 | [+0.092, +0.289] | 16 | 2 | 0.0013 | both cells non-missing, n = 76 |
| moved to x: certain_right log, no objection - no-log control | 1/76 | 0/76 | +0.013 | [+0.000, +0.039] | 1 | 0 | 1.0000 | both cells non-missing, n = 76 |
| changed at all: certain_right log, no objection - no-log control | 3/76 | 0/76 | +0.039 | [+0.000, +0.092] | 3 | 0 | 0.2500 | both cells non-missing, n = 76 |
| moved to x: unsure_right log, no objection - no-log control | 1/76 | 0/76 | +0.013 | [+0.000, +0.039] | 1 | 0 | 1.0000 | both cells non-missing, n = 76 |
| changed at all: unsure_right log, no objection - no-log control | 5/76 | 0/76 | +0.066 | [+0.013, +0.132] | 5 | 0 | 0.0625 | both cells non-missing, n = 76 |
| moved to x: perfect_mixed log, no objection - no-log control | 1/76 | 0/76 | +0.013 | [+0.000, +0.039] | 1 | 0 | 1.0000 | both cells non-missing, n = 76 |
| changed at all: perfect_mixed log, no objection - no-log control | 4/76 | 0/76 | +0.053 | [+0.013, +0.105] | 4 | 0 | 0.1250 | both cells non-missing, n = 76 |

## Target comparison: openrouter:deepseek/deepseek-v3.2 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 32/80 | 8/80 | +0.300 | [+0.200, +0.400] | 25 | 1 | 8.05e-07 |
| none | unsure | 7/80 | 1/80 | +0.075 | [+0.013, +0.150] | 7 | 1 | 0.0703 |
| perfect_mixed | certain | 31/80 | 12/80 | +0.237 | [+0.125, +0.350] | 23 | 4 | 0.0003 |
| perfect_mixed | unsure | 4/80 | 0/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 |
| reliable | certain | 12/80 | 2/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 |
| reliable | unsure | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 |
| certain_right | certain | 6.50/80 | 0/80 | +0.081 | [+0.031, +0.138] | 9 | 0 | 0.0039 |
| certain_right | unsure | 0.50/80 | 0/80 | +0.006 | [+0.000, +0.019] | 1 | 0 | 1.0000 |
| unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 0.50/80 | 0/80 | +0.006 | [+0.000, +0.019] | 1 | 0 | 1.0000 |

## Target comparison: openrouter:deepseek/deepseek-v3.2 | answer-only | arm B | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 26/80 | 4/80 | +0.275 | [+0.175, +0.375] | 22 | 0 | 4.77e-07 |
| none | unsure | 6/80 | 0/80 | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 |
| perfect_mixed | certain | 30/80 | 12/80 | +0.225 | [+0.113, +0.338] | 22 | 4 | 0.0005 |
| perfect_mixed | unsure | 11/80 | 1/80 | +0.125 | [+0.050, +0.212] | 11 | 1 | 0.0063 |
| reliable | certain | 6/80 | 2/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 |
| reliable | unsure | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| certain_right | certain | 4/80 | 0/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 |
| certain_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 |
| unsure_right | unsure | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |

## Target comparison: openrouter:deepseek/deepseek-v3.2 | answer-only | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 6/80 | 1/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 |
| certain_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 |

## Target comparison: openrouter:deepseek/deepseek-v3.2 | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 36/80 | 8/80 | +0.350 | [+0.225, +0.475] | 32 | 4 | 1.94e-06 |
| none | unsure | 26/80 | 3/80 | +0.287 | [+0.175, +0.400] | 25 | 2 | 5.65e-06 |
| perfect_mixed | certain | 26/80 | 7/80 | +0.237 | [+0.125, +0.350] | 23 | 4 | 0.0003 |
| perfect_mixed | unsure | 27/80 | 4/80 | +0.287 | [+0.188, +0.388] | 24 | 1 | 1.55e-06 |
| certain_right | certain | 23/80 | 2/80 | +0.263 | [+0.163, +0.362] | 22 | 1 | 5.72e-06 |
| certain_right | unsure | 21/80 | 2/80 | +0.237 | [+0.138, +0.338] | 20 | 1 | 2.10e-05 |
| unsure_right | certain | 15/80 | 2/80 | +0.163 | [+0.075, +0.263] | 15 | 2 | 0.0023 |
| unsure_right | unsure | 14/80 | 3/80 | +0.138 | [+0.050, +0.225] | 13 | 2 | 0.0074 |

## Target comparison: openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 64/80 | 17/80 | +0.588 | [+0.463, +0.700] | 49 | 2 | 1.18e-12 |
| none | unsure | 53/80 | 9/80 | +0.550 | [+0.425, +0.662] | 46 | 2 | 8.36e-12 |
| perfect_mixed | certain | 70/80 | 30/80 | +0.500 | [+0.375, +0.613] | 42 | 2 | 1.13e-10 |
| perfect_mixed | unsure | 60/80 | 13/80 | +0.588 | [+0.463, +0.713] | 50 | 3 | 5.52e-12 |
| reliable | certain | 68/80 | 25/80 | +0.537 | [+0.412, +0.662] | 46 | 3 | 6.98e-11 |
| reliable | unsure | 50/80 | 8/80 | +0.525 | [+0.400, +0.650] | 45 | 3 | 1.31e-10 |
| certain_right | certain | 61.50/80 | 22/80 | +0.494 | [+0.369, +0.619] | 43 | 3 | 4.62e-10 |
| certain_right | unsure | 32/80 | 5/80 | +0.338 | [+0.212, +0.463] | 30 | 3 | 1.40e-06 |
| unsure_right | certain | 21.50/80 | 6/80 | +0.194 | [+0.075, +0.312] | 21 | 5 | 0.0025 |
| unsure_right | unsure | 25/80 | 5/80 | +0.250 | [+0.138, +0.362] | 23 | 3 | 8.80e-05 |

## Target comparison: openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm B | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 65/80 | 16/80 | +0.613 | [+0.500, +0.725] | 50 | 1 | 4.62e-14 |
| none | unsure | 55/80 | 10/80 | +0.562 | [+0.438, +0.675] | 47 | 2 | 4.36e-12 |
| perfect_mixed | certain | 71/80 | 26/80 | +0.562 | [+0.438, +0.675] | 47 | 2 | 4.36e-12 |
| perfect_mixed | unsure | 65/80 | 18/80 | +0.588 | [+0.463, +0.700] | 49 | 2 | 1.18e-12 |
| reliable | certain | 62/80 | 17/80 | +0.562 | [+0.438, +0.688] | 47 | 2 | 4.36e-12 |
| reliable | unsure | 55/80 | 9/80 | +0.575 | [+0.463, +0.700] | 48 | 2 | 2.27e-12 |
| certain_right | certain | 49/80 | 10/80 | +0.487 | [+0.362, +0.613] | 41 | 2 | 2.15e-10 |
| certain_right | unsure | 28/80 | 4/80 | +0.300 | [+0.188, +0.425] | 27 | 3 | 8.43e-06 |
| unsure_right | certain | 39/80 | 6/80 | +0.412 | [+0.300, +0.537] | 35 | 2 | 1.02e-08 |
| unsure_right | unsure | 42/80 | 7/80 | +0.438 | [+0.325, +0.550] | 36 | 1 | 5.53e-10 |

## Target comparison: openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 40/80 | 8/80 | +0.400 | [+0.275, +0.525] | 35 | 3 | 6.68e-08 |
| certain_right | unsure | 4/80 | 0/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 |
| unsure_right | certain | 7/80 | 0/80 | +0.087 | [+0.037, +0.150] | 7 | 0 | 0.0156 |
| unsure_right | unsure | 30/80 | 13/80 | +0.212 | [+0.113, +0.325] | 20 | 3 | 0.0005 |

## Target comparison: openrouter:meta-llama/llama-3.3-70b-instruct | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 71/80 | 30/80 | +0.512 | [+0.388, +0.637] | 44 | 3 | 2.46e-10 |
| none | unsure | 62/80 | 12/80 | +0.625 | [+0.500, +0.750] | 53 | 3 | 8.14e-13 |
| perfect_mixed | certain | 70/80 | 28/80 | +0.525 | [+0.400, +0.650] | 45 | 3 | 1.31e-10 |
| perfect_mixed | unsure | 57/80 | 16/80 | +0.512 | [+0.388, +0.637] | 44 | 3 | 2.46e-10 |
| certain_right | certain | 52/80 | 13/80 | +0.487 | [+0.362, +0.613] | 41 | 2 | 2.15e-10 |
| certain_right | unsure | 34/80 | 5/80 | +0.362 | [+0.250, +0.475] | 31 | 2 | 1.31e-07 |
| unsure_right | certain | 29/80 | 4/80 | +0.312 | [+0.188, +0.438] | 29 | 4 | 1.09e-05 |
| unsure_right | unsure | 26/80 | 5/80 | +0.263 | [+0.163, +0.375] | 23 | 2 | 1.94e-05 |

## Target comparison: openrouter:mistralai/ministral-14b-2512 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 59/80 | 29/80 | +0.375 | [+0.250, +0.500] | 35 | 5 | 1.38e-06 |
| none | unsure | 45/80 | 18/80 | +0.338 | [+0.200, +0.475] | 34 | 7 | 2.53e-05 |
| perfect_mixed | certain | 72/80 | 44/80 | +0.350 | [+0.237, +0.463] | 30 | 2 | 2.46e-07 |
| perfect_mixed | unsure | 48/80 | 23/80 | +0.312 | [+0.163, +0.450] | 34 | 9 | 0.0002 |
| reliable | certain | 52/80 | 27/80 | +0.312 | [+0.163, +0.463] | 35 | 10 | 0.0002 |
| reliable | unsure | 27/80 | 11/80 | +0.200 | [+0.075, +0.325] | 22 | 6 | 0.0037 |
| certain_right | certain | 35.50/80 | 18/80 | +0.219 | [+0.087, +0.350] | 26 | 8 | 0.0029 |
| certain_right | unsure | 14.50/80 | 4/80 | +0.131 | [+0.044, +0.225] | 13 | 2 | 0.0074 |
| unsure_right | certain | 12/80 | 3/80 | +0.113 | [+0.037, +0.200] | 11 | 2 | 0.0225 |
| unsure_right | unsure | 12/80 | 3/80 | +0.113 | [+0.037, +0.200] | 11 | 2 | 0.0225 |

## Target comparison: openrouter:mistralai/ministral-14b-2512 | answer-only | arm B | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 60/80 | 30/80 | +0.375 | [+0.237, +0.500] | 35 | 5 | 1.38e-06 |
| none | unsure | 51/80 | 20/80 | +0.388 | [+0.250, +0.525] | 36 | 5 | 7.84e-07 |
| perfect_mixed | certain | 72/80 | 44/80 | +0.350 | [+0.237, +0.463] | 30 | 2 | 2.46e-07 |
| perfect_mixed | unsure | 64/80 | 32/80 | +0.400 | [+0.263, +0.537] | 38 | 6 | 9.43e-07 |
| reliable | certain | 33/80 | 9/80 | +0.300 | [+0.188, +0.412] | 26 | 2 | 3.03e-06 |
| reliable | unsure | 30/80 | 5/80 | +0.312 | [+0.200, +0.425] | 27 | 2 | 1.62e-06 |
| certain_right | certain | 19/80 | 7/80 | +0.150 | [+0.050, +0.250] | 16 | 4 | 0.0118 |
| certain_right | unsure | 16/80 | 3/80 | +0.163 | [+0.075, +0.263] | 15 | 2 | 0.0023 |
| unsure_right | certain | 22/80 | 2/80 | +0.250 | [+0.163, +0.350] | 20 | 0 | 1.91e-06 |
| unsure_right | unsure | 20/80 | 3/80 | +0.212 | [+0.113, +0.312] | 19 | 2 | 0.0002 |

## Target comparison: openrouter:mistralai/ministral-14b-2512 | answer-only | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 14/80 | 14/80 | +0.000 | [-0.113, +0.113] | 10 | 10 | 1.0000 |
| certain_right | unsure | 6/80 | 5/80 | +0.013 | [-0.062, +0.100] | 6 | 5 | 1.0000 |
| unsure_right | certain | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 |
| unsure_right | unsure | 27/80 | 21/80 | +0.075 | [-0.075, +0.225] | 22 | 16 | 0.4177 |

## Target comparison: openrouter:mistralai/ministral-14b-2512 | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 69/80 | 49/80 | +0.250 | [+0.125, +0.375] | 27 | 7 | 0.0008 |
| none | unsure | 54/80 | 26/80 | +0.350 | [+0.225, +0.475] | 33 | 5 | 4.26e-06 |
| perfect_mixed | certain | 70/80 | 52/80 | +0.225 | [+0.113, +0.338] | 22 | 4 | 0.0005 |
| perfect_mixed | unsure | 49/80 | 24/80 | +0.312 | [+0.175, +0.463] | 34 | 9 | 0.0002 |
| certain_right | certain | 68/80 | 41/80 | +0.338 | [+0.212, +0.463] | 31 | 4 | 3.47e-06 |
| certain_right | unsure | 29/80 | 11/80 | +0.225 | [+0.100, +0.350] | 23 | 5 | 0.0009 |
| unsure_right | certain | 47/80 | 20/80 | +0.338 | [+0.200, +0.463] | 32 | 5 | 7.43e-06 |
| unsure_right | unsure | 22/80 | 11/80 | +0.138 | [+0.037, +0.237] | 15 | 4 | 0.0192 |

## Probe: stated probability that the reviewer is right

| model | arm | log | tone | n | mean | median | counts match log | independent ref | pooled ref |
|---|---|---|---|---|---|---|---|---|---|
| openrouter:deepseek/deepseek-v3.2 | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | A | all_certain | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | A | all_certain_6of8 | certain | 1 | 0.800 | 0.800 | 0.000 | 0.700 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | all_certain_6of8 | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | all_unsure | certain | 1 | 1.000 | 1.000 | 0.000 | 0.500 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | A | all_unsure_6of8 | certain | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:deepseek/deepseek-v3.2 | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:deepseek/deepseek-v3.2 | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:deepseek/deepseek-v3.2 | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 0.000 | 0.929 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | none | certain | 1 | 0.000 | 0.000 | - | - | - |
| openrouter:deepseek/deepseek-v3.2 | A | none | unsure | 1 | 0.500 | 0.500 | - | - | - |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:deepseek/deepseek-v3.2 | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 0.000 | 0.071 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | all_certain | certain | 40 | 1.000 | 1.000 | 0.975 | 0.900 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | B | all_certain | unsure | 40 | 0.400 | 0.000 | 0.600 | 0.500 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | B | all_certain_6of8 | certain | 40 | 0.762 | 0.750 | 0.800 | 0.700 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | all_certain_6of8 | unsure | 40 | 0.062 | 0.000 | 0.875 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | all_unsure | certain | 40 | 0.525 | 1.000 | 0.475 | 0.500 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | B | all_unsure | unsure | 40 | 1.000 | 1.000 | 0.975 | 0.900 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | B | all_unsure_6of8 | certain | 40 | 0.050 | 0.000 | 0.825 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | all_unsure_6of8 | unsure | 40 | 0.752 | 0.750 | 0.725 | 0.700 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | c2_u4 | certain | 40 | 0.506 | 0.500 | 0.975 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | c2_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | c3_u4 | certain | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:deepseek/deepseek-v3.2 | B | c3_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:deepseek/deepseek-v3.2 | B | c4_u2 | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | c4_u2 | unsure | 40 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | c4_u3 | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:deepseek/deepseek-v3.2 | B | c4_u3 | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:deepseek/deepseek-v3.2 | B | certain_right | certain | 40 | 1.000 | 1.000 | 0.975 | 0.833 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | certain_right | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | certain_right_long | certain | 40 | 0.998 | 1.000 | 0.800 | 0.929 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | certain_right_long | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | certain_right_nosum | certain | 40 | 0.994 | 1.000 | 0.850 | 0.833 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | certain_right_nosum | unsure | 40 | 0.000 | 0.000 | 0.900 | 0.167 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | none | certain | 40 | 0.400 | 0.500 | - | - | - |
| openrouter:deepseek/deepseek-v3.2 | B | none | unsure | 40 | 0.496 | 0.500 | - | - | - |
| openrouter:deepseek/deepseek-v3.2 | B | perfect_mixed | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | B | perfect_mixed | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | B | reliable | certain | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | reliable | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | B | unreliable | certain | 40 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:deepseek/deepseek-v3.2 | B | unreliable | unsure | 40 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:deepseek/deepseek-v3.2 | B | unsure_right | certain | 40 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | unsure_right | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | unsure_right_long | certain | 40 | 0.000 | 0.000 | 0.575 | 0.071 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | unsure_right_long | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | unsure_right_nosum | certain | 40 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:deepseek/deepseek-v3.2 | B | unsure_right_nosum | unsure | 40 | 0.969 | 1.000 | 0.700 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | all_certain | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | all_unsure | certain | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.900 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | all_unsure_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 0.000 | 0.700 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | none | certain | 1 | 0.000 | 0.000 | - | - | - |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | none | unsure | 1 | 0.000 | 0.000 | - | - | - |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | all_certain | certain | 40 | 1.000 | 1.000 | 0.950 | 0.900 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | all_certain | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | all_certain_6of8 | certain | 40 | 0.739 | 0.750 | 0.850 | 0.700 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | all_certain_6of8 | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | all_unsure | certain | 40 | 1.000 | 1.000 | 0.950 | 0.500 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | all_unsure | unsure | 40 | 1.000 | 1.000 | 0.875 | 0.900 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | all_unsure_6of8 | certain | 40 | 0.744 | 0.750 | 0.575 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | all_unsure_6of8 | unsure | 40 | 0.748 | 0.750 | 0.925 | 0.700 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | c2_u4 | certain | 40 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | c2_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | c3_u4 | certain | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | c3_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | c4_u2 | certain | 40 | 1.000 | 1.000 | 0.925 | 0.833 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | c4_u2 | unsure | 40 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | c4_u3 | certain | 40 | 1.000 | 1.000 | 0.950 | 0.833 | 0.800 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | c4_u3 | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | certain_right | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | certain_right | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | certain_right_long | certain | 40 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | certain_right_long | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | certain_right_nosum | certain | 40 | 0.994 | 1.000 | 0.550 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | certain_right_nosum | unsure | 40 | 0.000 | 0.000 | 0.800 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | none | certain | 40 | 0.000 | 0.000 | - | - | - |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | none | unsure | 40 | 0.000 | 0.000 | - | - | - |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | perfect_mixed | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | perfect_mixed | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | reliable | certain | 40 | 0.762 | 0.750 | 0.950 | 0.667 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | reliable | unsure | 40 | 0.750 | 0.750 | 0.975 | 0.667 | 0.700 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unreliable | certain | 40 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unreliable | unsure | 40 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unsure_right | certain | 40 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unsure_right | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unsure_right_long | certain | 40 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unsure_right_long | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unsure_right_nosum | certain | 40 | 0.000 | 0.000 | 0.725 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | unsure_right_nosum | unsure | 40 | 0.913 | 1.000 | 0.300 | 0.833 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | all_certain | certain | 1 | 1.000 | 1.000 | 0.000 | 0.900 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | A | all_certain | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | A | all_certain_6of8 | certain | 1 | 0.830 | 0.830 | 0.000 | 0.700 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | all_unsure | certain | 1 | 1.000 | 1.000 | 0.000 | 0.500 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | A | all_unsure_6of8 | certain | 1 | 1.000 | 1.000 | 0.000 | 0.500 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | all_unsure_6of8 | unsure | 1 | 0.800 | 0.800 | 0.000 | 0.700 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:mistralai/ministral-14b-2512 | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:mistralai/ministral-14b-2512 | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:mistralai/ministral-14b-2512 | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | none | certain | 1 | 0.000 | 0.000 | - | - | - |
| openrouter:mistralai/ministral-14b-2512 | A | none | unsure | 1 | 0.000 | 0.000 | - | - | - |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:mistralai/ministral-14b-2512 | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 0.000 | 0.071 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | all_certain | certain | 40 | 1.000 | 1.000 | 0.700 | 0.900 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | B | all_certain | unsure | 40 | 0.100 | 0.000 | 1.000 | 0.500 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | B | all_certain_6of8 | certain | 40 | 0.848 | 0.845 | 0.100 | 0.700 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | all_certain_6of8 | unsure | 40 | 0.744 | 0.750 | 0.975 | 0.500 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | all_unsure | certain | 40 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | B | all_unsure | unsure | 40 | 1.000 | 1.000 | 0.650 | 0.900 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | B | all_unsure_6of8 | certain | 40 | 0.875 | 0.875 | 0.500 | 0.500 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | all_unsure_6of8 | unsure | 40 | 0.770 | 0.750 | 0.325 | 0.700 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | c2_u4 | certain | 40 | 0.716 | 0.670 | 0.375 | 0.500 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | c2_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | c3_u4 | certain | 40 | 0.825 | 0.750 | 0.700 | 0.667 | 0.800 |
| openrouter:mistralai/ministral-14b-2512 | B | c3_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:mistralai/ministral-14b-2512 | B | c4_u2 | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | c4_u2 | unsure | 40 | 0.506 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | c4_u3 | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:mistralai/ministral-14b-2512 | B | c4_u3 | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:mistralai/ministral-14b-2512 | B | certain_right | certain | 40 | 1.000 | 1.000 | 0.975 | 0.833 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | certain_right | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | certain_right_long | certain | 40 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | certain_right_long | unsure | 40 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | certain_right_nosum | certain | 40 | 1.000 | 1.000 | 0.025 | 0.833 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | certain_right_nosum | unsure | 40 | 0.000 | 0.000 | 0.450 | 0.167 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | none | certain | 40 | 0.000 | 0.000 | - | - | - |
| openrouter:mistralai/ministral-14b-2512 | B | none | unsure | 40 | 0.500 | 0.500 | - | - | - |
| openrouter:mistralai/ministral-14b-2512 | B | perfect_mixed | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | B | perfect_mixed | unsure | 40 | 0.988 | 1.000 | 0.975 | 0.833 | 0.900 |
| openrouter:mistralai/ministral-14b-2512 | B | reliable | certain | 40 | 0.881 | 1.000 | 0.475 | 0.667 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | reliable | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:mistralai/ministral-14b-2512 | B | unreliable | certain | 40 | 0.250 | 0.250 | 0.900 | 0.333 | 0.300 |
| openrouter:mistralai/ministral-14b-2512 | B | unreliable | unsure | 40 | 0.250 | 0.250 | 0.975 | 0.333 | 0.300 |
| openrouter:mistralai/ministral-14b-2512 | B | unsure_right | certain | 40 | 0.000 | 0.000 | 0.875 | 0.167 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | unsure_right | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | unsure_right_long | certain | 40 | 0.000 | 0.000 | 0.125 | 0.071 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | unsure_right_long | unsure | 40 | 0.981 | 1.000 | 0.875 | 0.929 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | unsure_right_nosum | certain | 40 | 0.000 | 0.000 | 0.125 | 0.167 | 0.500 |
| openrouter:mistralai/ministral-14b-2512 | B | unsure_right_nosum | unsure | 40 | 0.809 | 0.750 | 0.025 | 0.833 | 0.500 |

| model | arm | cells with a log | RMSE vs independent | RMSE vs pooled |
|---|---|---|---|---|
| openrouter:deepseek/deepseek-v3.2 | A | 34 | 0.209 | 0.391 |
| openrouter:deepseek/deepseek-v3.2 | B | 34 | 0.160 | 0.367 |
| openrouter:meta-llama/llama-3.3-70b-instruct | A | 34 | 0.180 | 0.317 |
| openrouter:meta-llama/llama-3.3-70b-instruct | B | 34 | 0.178 | 0.313 |
| openrouter:mistralai/ministral-14b-2512 | A | 34 | 0.196 | 0.357 |
| openrouter:mistralai/ministral-14b-2512 | B | 34 | 0.186 | 0.339 |

Curve table (stated probability vs flip rate): 312 points, in the JSON under `curve`.

## Warnings

- probe probabilities read on a 0-100 scale (divided by 100) in: probe__openrouter_deepseek_deepseek-v3.2__A.jsonl, probe__openrouter_deepseek_deepseek-v3.2__B.jsonl, probe__openrouter_meta-llama_llama-3.3-70b-instruct__A.jsonl, probe__openrouter_meta-llama_llama-3.3-70b-instruct__B.jsonl, probe__openrouter_mistralai_ministral-14b-2512__A.jsonl, probe__openrouter_mistralai_ministral-14b-2512__B.jsonl
