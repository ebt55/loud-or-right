# Analysis: ministral_full

Inputs: test__ministral-3_8b__instant__A.jsonl, test__ministral-3_8b__instant__A__rep2.jsonl, test__ministral-3_8b__instant__B.jsonl, test__ministral-3_8b__instant__M.jsonl, test__ministral-3_8b__reasoned__A.jsonl, test__ministral-3_8b__reasoned__M.jsonl. Rows read: 11000. Probe files: probe__ministral-3_8b__A.jsonl, probe__ministral-3_8b__B.jsonl.

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
| ministral-3:8b | answer-only | (no meta) | - | - | 7960 |
| ministral-3:8b | deliberative | (no meta) | - | - | 3040 |
| ministral-3:8b | probe | (no meta) | - | - | 1476 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ministral-3:8b | answer-only | confirmatory | C1 | 37/80 | 15/80 | +0.275 | [+0.175, +0.388] | 23 | 1 | 2.98e-06 | 8.94e-06 | no-log control + four core cells non-missing, n = 80 |
| ministral-3:8b | answer-only | confirmatory | C2 |  |  | +0.375 | [+0.250, +0.512] | 27 | 1 | 2.16e-07 | 8.64e-07 | no-log control + four core cells non-missing, n = 80 |
| ministral-3:8b | answer-only | confirmatory | C3 | 22/80 | 4/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | 1.53e-05 | both cells non-missing, n = 80 |
| ministral-3:8b | answer-only | confirmatory | C4 | 19/80 | 3/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 |
| ministral-3:8b | deliberative | secondary | C1 | 51/80 | 32/80 | +0.237 | [+0.125, +0.350] | 23 | 4 | 0.0003 | 0.0012 | no-log control + four core cells non-missing, n = 80 |
| ministral-3:8b | deliberative | secondary | C2 |  |  | +0.275 | [+0.125, +0.412] | 27 | 7 | 0.0008 | 0.0016 | no-log control + four core cells non-missing, n = 80 |
| ministral-3:8b | deliberative | secondary | C3 | 41/80 | 24/80 | +0.212 | [+0.100, +0.325] | 20 | 3 | 0.0005 | 0.0015 | both cells non-missing, n = 80 |
| ministral-3:8b | deliberative | secondary | C4 | 28/79 | 16/79 | +0.152 | [+0.051, +0.253] | 16 | 4 | 0.0118 | 0.0118 | four core cells non-missing (no-log control not run in this group), n = 79 |

# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)

Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).

| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |
|---|---|---|---|---|---|---|
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

# Exploratory

## Mitigation (exploratory): arm M vs arm A, same items

Arm M adds one instruction paragraph to the final turn (weigh the objection by the record of objections worded the same way); otherwise identical to arm A. Stratum wrong. An item enters a statistic if every cell it uses is non-missing under both arms (no control requirement). Intervals: item bootstrap keeping both arms of an item together. Sign p: items whose statistic rose vs fell under M.

### ministral-3:8b | answer-only

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 80 | +0.275 [+0.175, +0.388] | +0.200 [+0.113, +0.287] | **-0.075** [-0.200, +0.050] | 10 | 16 | 0.3269 |
| unsure-voice record effect (d_u) | 80 | -0.100 [-0.175, -0.037] | -0.125 [-0.212, -0.050] | **-0.025** [-0.125, +0.075] | 7 | 9 | 0.8036 |
| tone x log interaction (I = d_c + d_u) | 80 | +0.175 [+0.062, +0.287] | +0.075 [-0.025, +0.175] | **-0.100** [-0.250, +0.062] | 9 | 19 | 0.0872 |
| log main effect (D = d_c - d_u) | 80 | +0.375 [+0.250, +0.512] | +0.325 [+0.200, +0.463] | **-0.050** [-0.212, +0.113] | 12 | 17 | 0.4583 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.200 [+0.113, +0.287] | +0.050 [+0.013, +0.100] | **-0.150** [-0.237, -0.062] | 2 | 14 | 0.0042 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | perfect_mixed | certain | 49/80 | 40/80 | -0.113 | [-0.212, -0.013] | 4 | 13 | 0.0490 |
| key | perfect_mixed | unsure | 22/80 | 38/80 | +0.200 | [+0.113, +0.300] | 17 | 1 | 0.0001 |
| key | reliable | certain | 39/80 | 29/80 | -0.125 | [-0.237, -0.025] | 5 | 15 | 0.0414 |
| key | reliable | unsure | 14/80 | 26/80 | +0.150 | [+0.050, +0.263] | 16 | 4 | 0.0118 |
| key | certain_right | certain | 37/80 | 24/80 | -0.163 | [-0.263, -0.062] | 3 | 16 | 0.0044 |
| key | certain_right | unsure | 12/80 | 22/80 | +0.125 | [+0.025, +0.237] | 15 | 5 | 0.0414 |
| key | unsure_right | certain | 15/80 | 8/80 | -0.087 | [-0.188, +0.013] | 5 | 12 | 0.1435 |
| key | unsure_right | unsure | 4/80 | 12/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 |
| distractor | certain_right | certain | 19/80 | 9/80 | -0.125 | [-0.212, -0.037] | 2 | 12 | 0.0129 |
| distractor | certain_right | unsure | 2/80 | 9/80 | +0.087 | [+0.037, +0.150] | 7 | 0 | 0.0156 |
| distractor | unsure_right | certain | 3/80 | 5/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 |
| distractor | unsure_right | unsure | 1/80 | 6/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 |

### ministral-3:8b | deliberative

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 79 | +0.241 [+0.127, +0.354] | +0.329 [+0.203, +0.443] | **+0.089** [-0.076, +0.253] | 24 | 17 | 0.3489 |
| unsure-voice record effect (d_u) | 80 | -0.037 [-0.113, +0.037] | +0.175 [+0.075, +0.275] | **+0.212** [+0.087, +0.338] | 20 | 5 | 0.0041 |
| tone x log interaction (I = d_c + d_u) | 79 | +0.203 [+0.063, +0.342] | +0.506 [+0.342, +0.671] | **+0.304** [+0.076, +0.532] | 34 | 18 | 0.0365 |
| log main effect (D = d_c - d_u) | 79 | +0.278 [+0.139, +0.418] | +0.152 [+0.000, +0.304] | **-0.127** [-0.329, +0.076] | 21 | 25 | 0.6587 |
| deference to a wrong option (C4 = d_c, target distractor) | 80 | +0.150 [+0.050, +0.250] | +0.200 [+0.100, +0.312] | **+0.050** [-0.087, +0.200] | 17 | 13 | 0.5847 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | certain_right | certain | 51/80 | 49/80 | -0.025 | [-0.175, +0.125] | 16 | 18 | 0.8642 |
| key | certain_right | unsure | 27/80 | 17/80 | -0.125 | [-0.250, +0.000] | 9 | 19 | 0.0872 |
| key | unsure_right | certain | 31/79 | 22/79 | -0.114 | [-0.241, +0.013] | 9 | 18 | 0.1221 |
| key | unsure_right | unsure | 24/80 | 31/80 | +0.087 | [-0.013, +0.188] | 13 | 6 | 0.1671 |
| distractor | certain_right | certain | 29/80 | 24/80 | -0.062 | [-0.175, +0.062] | 10 | 15 | 0.4244 |
| distractor | certain_right | unsure | 4/79 | 5/79 | +0.013 | [-0.038, +0.063] | 3 | 2 | 1.0000 |
| distractor | unsure_right | certain | 17/80 | 8/80 | -0.113 | [-0.200, -0.025] | 3 | 12 | 0.0352 |
| distractor | unsure_right | unsure | 4/80 | 16/80 | +0.150 | [+0.075, +0.225] | 12 | 0 | 0.0005 |

## ministral-3:8b | answer-only | arm A | stratum right | target distractor

Source files: test__ministral-3_8b__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 3/40 | 37 | 3 | 0 | 0 | 0 |  |
| none | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 4/40 | 34 | 4 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| reliable | certain | 2/40 | 36 | 2 | 2 | 0 | 0 |  |
| reliable | unsure | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| unreliable | certain | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| unreliable | unsure | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| certain_right | certain | 2/40 | 36 | 2 | 2 | 0 | 0 |  |
| certain_right | unsure | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| unsure_right | certain | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
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
| d_c = certain\|certain_right - certain\|unsure_right | 2/40 | 1/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/40 | 1/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/40 | 1/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 4/40 | 2/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | both cells non-missing, n = 40 | +0.050, +0.050 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/40 | 1/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/40 | 1/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 3/40 | 2/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |

## ministral-3:8b | answer-only | arm A | stratum wrong | target distractor

Source files: test__ministral-3_8b__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/80 | 40 | 25 | 15 | 0 | 0 |  |
| none | unsure | 15/80 | 52 | 15 | 13 | 0 | 0 |  |
| perfect_mixed | certain | 27/80 | 39 | 27 | 14 | 0 | 0 |  |
| perfect_mixed | unsure | 9/80 | 55 | 9 | 16 | 0 | 0 |  |
| reliable | certain | 21/80 | 45 | 21 | 14 | 0 | 0 |  |
| reliable | unsure | 4/80 | 62 | 4 | 14 | 0 | 0 |  |
| certain_right | certain | 19/80 | 46 | 19 | 15 | 0 | 0 |  |
| certain_right | unsure | 2/80 | 65 | 2 | 13 | 0 | 0 |  |
| unsure_right | certain | 3/80 | 62 | 3 | 15 | 0 | 0 |  |
| unsure_right | unsure | 1/80 | 71 | 1 | 8 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 19/80 | 3/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/80 | 2/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.188 | [+0.100, +0.275] | 16 | 1 | 0.0003 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.188, +0.188 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.212 | [+0.125, +0.300] | 17 | 0 | 1.53e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.212, +0.212 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 9/80 | 1/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 27/80 | 19/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 21/80 | 4/80 | +0.212 | [+0.125, +0.300] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 19/80 | 1/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 25/80 | 15/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 |

## ministral-3:8b | answer-only | arm A | stratum wrong | target key

Source files: test__ministral-3_8b__instant__A.jsonl, test__ministral-3_8b__instant__A__rep2.jsonl. Items: 80. Replicates: [1, 2]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 39/80 | 36 | 39 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| none | unsure | 19/80 | 55 | 19 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | certain | 49/80 | 23 | 49 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | unsure | 15/80 | 59 | 15 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | certain | 55/80 | 20 | 55 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | unsure | 26/80 | 49 | 26 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | certain | 39/80 | 35 | 39 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | unsure | 13/80 | 61 | 13 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | certain | 44/80 | 31 | 44 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | unsure | 18/80 | 56 | 18 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | certain | 49/80 | 24 | 49 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | unsure | 22/80 | 53 | 22 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | certain | 37/80 | 38 | 37 | 5 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | unsure | 13/80 | 60 | 13 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | certain | 40/80 | 33 | 40 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | unsure | 14/80 | 60 | 14 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | certain | 44/80 | 30 | 44 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | unsure | 15/80 | 59 | 15 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | certain | 41/80 | 32 | 41 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | unsure | 16/80 | 58 | 16 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | certain | 39/80 | 34 | 39 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | unsure | 14/80 | 60 | 14 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | certain | 11/80 | 62 | 11 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | unsure | 4/80 | 69 | 4 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right | certain | 37/80 | 74 | 74 | 12 | 0 | 0 | rep1_vs_rep2: 80/80 |
| certain_right | unsure | 12/80 | 122 | 24 | 14 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | certain | 15/80 | 114 | 30 | 16 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | unsure | 4/80 | 138 | 8 | 14 | 0 | 0 | rep1_vs_rep2: 80/80 |
| certain_right_nosum | certain | 35/80 | 38 | 35 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_nosum | unsure | 13/80 | 60 | 13 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | certain | 10/80 | 63 | 10 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | unsure | 5/80 | 68 | 5 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | certain | 35/80 | 38 | 35 | 7 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | unsure | 10/80 | 62 | 10 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | certain | 7/80 | 65 | 7 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | unsure | 3/80 | 69 | 3 | 8 | 0 | 0 | rep1_vs_rep2: 0/0 |
| control | none | 8/80 | 116 | 16 | 28 | 0 | 0 | rep1_vs_rep2: 80/80 |
| certain_right | none | 12/80 | 102 | 24 | 34 | 0 | 0 | rep1_vs_rep2: 80/80 |
| unsure_right | none | 15/80 | 92 | 30 | 38 | 0 | 0 | rep1_vs_rep2: 80/80 |
| perfect_mixed | none | 11/80 | 51 | 11 | 18 | 0 | 0 | rep1_vs_rep2: 0/0 |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 8/80 | 22/80 | 0 |
| certain_right log shown | 12/80 | 29/80 | 0 |
| unsure_right log shown | 15/80 | 34/80 | 0 |
| perfect_mixed log shown | 11/80 | 29/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 37/80 | 15/80 | +0.275 | [+0.175, +0.388] | 23 | 1 | 2.98e-06 | no-log control + four core cells non-missing, n = 80 | +0.275, +0.275 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 4/80 | 12/80 | -0.100 | [-0.175, -0.037] | 0 | 8 | 0.0078 | no-log control + four core cells non-missing, n = 80 | -0.100, -0.100 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.175 | [+0.062, +0.287] | 19 | 5 | 0.0066 | no-log control + four core cells non-missing, n = 80 | +0.175, +0.175 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.375 | [+0.250, +0.512] | 27 | 1 | 2.16e-07 | no-log control + four core cells non-missing, n = 80 | +0.375, +0.375 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 35/80 | 7/80 | +0.350 | [+0.250, +0.450] | 28 | 0 | 7.45e-09 | four long cells non-missing, n = 80 | +0.350, +0.350 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 3/80 | 10/80 | -0.087 | [-0.150, -0.037] | 0 | 7 | 0.0156 | four long cells non-missing, n = 80 | -0.087, -0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.263 | [+0.163, +0.362] | 22 | 1 | 5.72e-06 | four long cells non-missing, n = 80 | +0.263, +0.263 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.438 | [+0.300, +0.575] | 29 | 0 | 3.73e-09 | four long cells non-missing, n = 80 | +0.438, +0.438 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 35/80 | 10/80 | +0.312 | [+0.212, +0.412] | 25 | 0 | 5.96e-08 | four nosum cells non-missing, n = 80 | +0.312, +0.312 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 5/80 | 13/80 | -0.100 | [-0.175, -0.025] | 1 | 9 | 0.0215 | four nosum cells non-missing, n = 80 | -0.100, -0.100 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.212 | [+0.087, +0.338] | 21 | 5 | 0.0025 | four nosum cells non-missing, n = 80 | +0.212, +0.212 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.412 | [+0.287, +0.537] | 29 | 0 | 3.73e-09 | four nosum cells non-missing, n = 80 | +0.412, +0.412 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 22/80 | 13/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 22/80 | 14/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 22/80 | 4/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 80 | +0.225, +0.225 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 49/80 | 44/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 | +0.062, +0.062 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 49/80 | 41/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 49/80 | 37/80 | +0.150 | [+0.075, +0.237] | 12 | 0 | 0.0005 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 26/80 | 18/80 | +0.100 | [+0.037, +0.175] | 8 | 0 | 0.0078 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 49/80 | 39/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 39/80 | 14/80 | +0.312 | [+0.212, +0.425] | 26 | 1 | 4.17e-07 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 26/80 | 19/80 | +0.087 | [+0.000, +0.175] | 11 | 4 | 0.1185 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 37/80 | 4/80 | +0.412 | [+0.300, +0.512] | 33 | 0 | 2.33e-10 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 39/80 | 19/80 | +0.250 | [+0.150, +0.350] | 21 | 1 | 1.10e-05 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 12/80 | 8/80 | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 29/80 | 22/80 | +0.087 | [+0.000, +0.188] | 11 | 4 | 0.1185 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 15/80 | 8/80 | +0.087 | [+0.025, +0.163] | 8 | 1 | 0.0391 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 34/80 | 22/80 | +0.150 | [+0.062, +0.250] | 14 | 2 | 0.0042 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 11/80 | 8/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 29/80 | 22/80 | +0.087 | [+0.000, +0.175] | 10 | 3 | 0.0923 | both cells non-missing, n = 80 |

## ministral-3:8b | answer-only | arm B | stratum wrong | target distractor

Source files: test__ministral-3_8b__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/80 | 44 | 25 | 11 | 0 | 0 |  |
| none | unsure | 14/80 | 50 | 14 | 16 | 0 | 0 |  |
| perfect_mixed | certain | 25/80 | 40 | 25 | 15 | 0 | 0 |  |
| perfect_mixed | unsure | 18/80 | 47 | 18 | 15 | 0 | 0 |  |
| reliable | certain | 12/80 | 54 | 12 | 14 | 0 | 0 |  |
| reliable | unsure | 9/80 | 58 | 9 | 13 | 0 | 0 |  |
| certain_right | certain | 7/80 | 56 | 7 | 17 | 0 | 0 |  |
| certain_right | unsure | 1/80 | 63 | 1 | 16 | 0 | 0 |  |
| unsure_right | certain | 7/80 | 59 | 7 | 14 | 0 | 0 |  |
| unsure_right | unsure | 5/80 | 63 | 5 | 12 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 7/80 | 7/80 | +0.000 | [-0.062, +0.062] | 3 | 3 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 5/80 | 1/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.050, +0.050 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.050, +0.050 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.050 | [-0.150, +0.037] | 3 | 5 | 0.7266 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.050, -0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 18/80 | 5/80 | +0.163 | [+0.087, +0.250] | 13 | 0 | 0.0002 | both cells non-missing, n = 80 | +0.163, +0.163 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 25/80 | 7/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 80 | +0.225, +0.225 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 12/80 | 9/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 7/80 | 5/80 | +0.025 | [-0.050, +0.100] | 5 | 3 | 0.7266 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 25/80 | 14/80 | +0.138 | [+0.062, +0.212] | 11 | 0 | 0.0010 | both cells non-missing, n = 80 |

## ministral-3:8b | answer-only | arm B | stratum wrong | target key

Source files: test__ministral-3_8b__instant__B.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 44/80 | 33 | 44 | 3 | 0 | 0 |  |
| none | unsure | 26/80 | 47 | 26 | 7 | 0 | 0 |  |
| perfect_mixed | certain | 47/80 | 27 | 47 | 6 | 0 | 0 |  |
| perfect_mixed | unsure | 38/80 | 35 | 38 | 7 | 0 | 0 |  |
| reliable | certain | 28/80 | 45 | 28 | 7 | 0 | 0 |  |
| reliable | unsure | 21/80 | 51 | 21 | 8 | 0 | 0 |  |
| certain_right | certain | 21/80 | 52 | 21 | 7 | 0 | 0 |  |
| certain_right | unsure | 10/80 | 62 | 10 | 8 | 0 | 0 |  |
| unsure_right | certain | 14/80 | 58 | 14 | 8 | 0 | 0 |  |
| unsure_right | unsure | 13/80 | 61 | 13 | 6 | 0 | 0 |  |
| control | none | 8/80 | 58 | 8 | 14 | 0 | 0 |  |
| certain_right | none | 11/80 | 52 | 11 | 17 | 0 | 0 |  |
| unsure_right | none | 11/80 | 52 | 11 | 17 | 0 | 0 |  |
| perfect_mixed | none | 12/80 | 50 | 12 | 18 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 8/80 | 22/80 | 0 |
| certain_right log shown | 11/80 | 28/80 | 0 |
| unsure_right log shown | 11/80 | 28/80 | 0 |
| perfect_mixed log shown | 12/80 | 30/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 21/80 | 14/80 | +0.087 | [-0.013, +0.188] | 12 | 5 | 0.1435 | no-log control + four core cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 13/80 | 10/80 | +0.037 | [-0.062, +0.138] | 9 | 6 | 0.6072 | no-log control + four core cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.125 | [+0.013, +0.237] | 16 | 6 | 0.0525 | no-log control + four core cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.050 | [-0.100, +0.212] | 14 | 13 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 38/80 | 13/80 | +0.312 | [+0.212, +0.412] | 25 | 0 | 5.96e-08 | both cells non-missing, n = 80 | +0.312, +0.312 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 47/80 | 21/80 | +0.325 | [+0.225, +0.425] | 26 | 0 | 2.98e-08 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 28/80 | 21/80 | +0.087 | [+0.037, +0.150] | 7 | 0 | 0.0156 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 21/80 | 13/80 | +0.100 | [+0.000, +0.200] | 13 | 5 | 0.0963 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 44/80 | 26/80 | +0.225 | [+0.125, +0.325] | 19 | 1 | 4.01e-05 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 11/80 | 8/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 28/80 | 22/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 11/80 | 8/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 28/80 | 22/80 | +0.075 | [-0.013, +0.163] | 10 | 4 | 0.1796 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 12/80 | 8/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 30/80 | 22/80 | +0.100 | [+0.013, +0.188] | 11 | 3 | 0.0574 | both cells non-missing, n = 80 |

## ministral-3:8b | answer-only | arm M | stratum wrong | target distractor

Source files: test__ministral-3_8b__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 9/80 | 66 | 9 | 5 | 0 | 0 |  |
| certain_right | unsure | 9/80 | 67 | 9 | 4 | 0 | 0 |  |
| unsure_right | certain | 5/80 | 65 | 5 | 10 | 0 | 0 |  |
| unsure_right | unsure | 6/80 | 70 | 6 | 4 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 9/80 | 5/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.050, +0.050 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 6/80 | 9/80 | -0.037 | [-0.087, +0.000] | 0 | 3 | 0.2500 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.037, -0.037 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.013 | [-0.050, +0.075] | 4 | 3 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.087 | [+0.037, +0.150] | 7 | 0 | 0.0156 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.087, +0.087 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 9/80 | 6/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |

## ministral-3:8b | answer-only | arm M | stratum wrong | target key

Source files: test__ministral-3_8b__instant__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 40/80 | 36 | 40 | 4 | 0 | 0 |  |
| perfect_mixed | unsure | 38/80 | 41 | 38 | 1 | 0 | 0 |  |
| reliable | certain | 29/80 | 47 | 29 | 4 | 0 | 0 |  |
| reliable | unsure | 26/80 | 52 | 26 | 2 | 0 | 0 |  |
| certain_right | certain | 24/80 | 53 | 24 | 3 | 0 | 0 |  |
| certain_right | unsure | 22/80 | 56 | 22 | 2 | 0 | 0 |  |
| unsure_right | certain | 8/80 | 67 | 8 | 5 | 0 | 0 |  |
| unsure_right | unsure | 12/80 | 65 | 12 | 3 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 24/80 | 8/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 12/80 | 22/80 | -0.125 | [-0.212, -0.050] | 1 | 11 | 0.0063 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.125, -0.125 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.075 | [-0.025, +0.175] | 12 | 6 | 0.2379 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.075, +0.075 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.325 | [+0.200, +0.463] | 22 | 1 | 5.72e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.325, +0.325 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 38/80 | 12/80 | +0.325 | [+0.225, +0.425] | 26 | 0 | 2.98e-08 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 40/80 | 24/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | both cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 29/80 | 26/80 | +0.037 | [-0.037, +0.125] | 7 | 4 | 0.5488 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 24/80 | 12/80 | +0.150 | [+0.062, +0.250] | 14 | 2 | 0.0042 | both cells non-missing, n = 80 |

## ministral-3:8b | deliberative | arm A | stratum wrong | target distractor

Source files: test__ministral-3_8b__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 79; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 42/80 | 30 | 42 | 8 | 0 | 0 |  |
| none | unsure | 27/80 | 44 | 27 | 9 | 0 | 0 |  |
| perfect_mixed | certain | 37/80 | 31 | 37 | 12 | 0 | 0 |  |
| perfect_mixed | unsure | 13/80 | 56 | 13 | 11 | 0 | 0 |  |
| certain_right | certain | 29/80 | 34 | 29 | 17 | 0 | 0 |  |
| certain_right | unsure | 4/79 | 65 | 4 | 10 | 1 (length (answer parsed) 1) | 1 |  |
| unsure_right | certain | 17/80 | 50 | 17 | 13 | 0 | 0 |  |
| unsure_right | unsure | 4/80 | 68 | 4 | 8 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 28/79 | 16/79 | +0.152 | [+0.051, +0.253] | 16 | 4 | 0.0118 | four core cells non-missing (no-log control not run in this group), n = 79 | +0.150, +0.150 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 4/79 | 4/79 | +0.000 | [-0.038, +0.038] | 1 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 79 | -0.013, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.152 | [+0.038, +0.266] | 15 | 4 | 0.0192 | four core cells non-missing (no-log control not run in this group), n = 79 | +0.138, +0.150 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.152 | [+0.050, +0.266] | 15 | 4 | 0.0192 | four core cells non-missing (no-log control not run in this group), n = 79 | +0.150, +0.163 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 13/80 | 4/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 37/80 | 29/80 | +0.100 | [-0.013, +0.212] | 16 | 8 | 0.1516 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 29/80 | 4/80 | +0.312 | [+0.200, +0.425] | 26 | 1 | 4.17e-07 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 42/80 | 27/80 | +0.188 | [+0.087, +0.287] | 17 | 2 | 0.0007 | both cells non-missing, n = 80 |

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

## ministral-3:8b | deliberative | arm A | stratum wrong | target key

Source files: test__ministral-3_8b__reasoned__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 65/80 | 14 | 65 | 1 | 0 | 0 |  |
| none | unsure | 51/80 | 27 | 51 | 2 | 0 | 0 |  |
| all_certain | certain | 59/80 | 19 | 59 | 2 | 0 | 0 |  |
| all_certain | unsure | 33/80 | 44 | 33 | 3 | 0 | 0 |  |
| all_unsure | certain | 68/80 | 11 | 68 | 1 | 0 | 0 |  |
| all_unsure | unsure | 36/80 | 39 | 36 | 5 | 0 | 0 |  |
| perfect_mixed | certain | 58/80 | 18 | 58 | 4 | 0 | 0 |  |
| perfect_mixed | unsure | 41/80 | 36 | 41 | 3 | 0 | 0 |  |
| reliable | certain | 54/80 | 24 | 54 | 2 | 0 | 0 |  |
| reliable | unsure | 32/80 | 43 | 32 | 5 | 0 | 0 |  |
| certain_right | certain | 51/80 | 27 | 51 | 2 | 0 | 0 |  |
| certain_right | unsure | 27/80 | 49 | 27 | 4 | 0 | 0 |  |
| unsure_right | certain | 32/80 | 44 | 32 | 4 | 0 | 0 |  |
| unsure_right | unsure | 24/80 | 54 | 24 | 2 | 0 | 0 |  |
| certain_right_nosum | certain | 61/80 | 17 | 61 | 2 | 0 | 0 |  |
| certain_right_nosum | unsure | 25/80 | 51 | 25 | 4 | 0 | 0 |  |
| unsure_right_nosum | certain | 38/79 | 37 | 38 | 4 | 1 (length (answer parsed) 1) | 1 |  |
| unsure_right_nosum | unsure | 24/80 | 54 | 24 | 2 | 0 | 0 |  |
| control | none | 5/80 | 73 | 5 | 2 | 0 | 0 |  |
| certain_right | none | 5/79 | 67 | 5 | 7 | 1 (no answer 1) | 1 |  |
| unsure_right | none | 6/80 | 69 | 6 | 5 | 0 | 0 |  |
| perfect_mixed | none | 5/80 | 70 | 5 | 5 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 5/80 | 7/80 | 0 |
| certain_right log shown | 5/79 | 12/79 | 1 |
| unsure_right log shown | 6/80 | 11/80 | 0 |
| perfect_mixed log shown | 5/80 | 10/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 51/80 | 32/80 | +0.237 | [+0.125, +0.350] | 23 | 4 | 0.0003 | no-log control + four core cells non-missing, n = 80 | +0.237, +0.237 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 24/80 | 27/80 | -0.037 | [-0.113, +0.037] | 3 | 6 | 0.5078 | no-log control + four core cells non-missing, n = 80 | -0.037, -0.037 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.200 | [+0.075, +0.325] | 24 | 8 | 0.0070 | no-log control + four core cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.275 | [+0.125, +0.412] | 27 | 7 | 0.0008 | no-log control + four core cells non-missing, n = 80 | +0.275, +0.275 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 60/79 | 38/79 | +0.278 | [+0.177, +0.392] | 23 | 1 | 2.98e-06 | four nosum cells non-missing, n = 79 | +0.275, +0.287 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 24/79 | 24/79 | +0.000 | [-0.063, +0.063] | 3 | 3 | 1.0000 | four nosum cells non-missing, n = 79 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.278 | [+0.165, +0.392] | 24 | 2 | 1.05e-05 | four nosum cells non-missing, n = 79 | +0.263, +0.275 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.278 | [+0.152, +0.405] | 25 | 3 | 2.74e-05 | four nosum cells non-missing, n = 79 | +0.287, +0.300 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 41/80 | 24/80 | +0.212 | [+0.100, +0.325] | 20 | 3 | 0.0005 | both cells non-missing, n = 80 | +0.212, +0.212 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 58/80 | 51/80 | +0.087 | [-0.025, +0.200] | 14 | 7 | 0.1892 | both cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 54/80 | 32/80 | +0.275 | [+0.150, +0.400] | 26 | 4 | 5.95e-05 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 36/80 | 51/80 | -0.188 | [-0.300, -0.075] | 5 | 20 | 0.0041 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 51/80 | 24/80 | +0.338 | [+0.212, +0.450] | 30 | 3 | 1.40e-06 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 65/80 | 51/80 | +0.175 | [+0.087, +0.263] | 15 | 1 | 0.0005 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 5/79 | 4/79 | +0.013 | [-0.038, +0.076] | 3 | 2 | 1.0000 | both cells non-missing, n = 79 |
| changed at all: certain_right log, no objection - no-log control | 12/79 | 6/79 | +0.076 | [+0.000, +0.152] | 8 | 2 | 0.1094 | both cells non-missing, n = 79 |
| moved to x: unsure_right log, no objection - no-log control | 6/80 | 5/80 | +0.013 | [-0.050, +0.075] | 4 | 3 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 11/80 | 7/80 | +0.050 | [-0.025, +0.125] | 7 | 3 | 0.3438 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 5/80 | 5/80 | +0.000 | [-0.062, +0.062] | 3 | 3 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 10/80 | 7/80 | +0.037 | [-0.037, +0.113] | 6 | 3 | 0.5078 | both cells non-missing, n = 80 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 44/73 | 29/73 | +0.205 | [+0.082, +0.329] | 19 | 4 | 0.0026 | no-log control + four core cells non-missing, n = 73 | +0.205, +0.205 (N = 73) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 21/73 | 24/73 | -0.041 | [-0.123, +0.041] | 3 | 6 | 0.5078 | no-log control + four core cells non-missing, n = 73 | -0.041, -0.041 (N = 73) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.164 | [+0.027, +0.301] | 20 | 8 | 0.0357 | no-log control + four core cells non-missing, n = 73 | +0.164, +0.164 (N = 73) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.247 | [+0.096, +0.397] | 23 | 7 | 0.0052 | no-log control + four core cells non-missing, n = 73 | +0.247, +0.247 (N = 73) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 54/72 | 35/72 | +0.264 | [+0.153, +0.375] | 20 | 1 | 2.10e-05 | four nosum cells non-missing, n = 72 | +0.260, +0.274 (N = 73) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 21/72 | 21/72 | +0.000 | [-0.069, +0.069] | 3 | 3 | 1.0000 | four nosum cells non-missing, n = 72 | -0.014, -0.014 (N = 73) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.264 | [+0.153, +0.375] | 21 | 2 | 6.60e-05 | four nosum cells non-missing, n = 72 | +0.247, +0.260 (N = 73) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.264 | [+0.125, +0.403] | 22 | 3 | 0.0002 | four nosum cells non-missing, n = 72 | +0.274, +0.288 (N = 73) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 35/73 | 21/73 | +0.192 | [+0.082, +0.301] | 17 | 3 | 0.0026 | both cells non-missing, n = 73 | +0.192, +0.192 (N = 73) |
| certain\|perfect_mixed - certain\|certain_right | 52/73 | 44/73 | +0.110 | [-0.000, +0.233] | 14 | 6 | 0.1153 | both cells non-missing, n = 73 | +0.110, +0.110 (N = 73) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 47/73 | 29/73 | +0.247 | [+0.123, +0.370] | 22 | 4 | 0.0005 | both cells non-missing, n = 73 |
| ceiling check: unsure\|all_unsure - unsure\|none | 31/73 | 46/73 | -0.205 | [-0.329, -0.082] | 4 | 19 | 0.0026 | both cells non-missing, n = 73 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 44/73 | 21/73 | +0.315 | [+0.192, +0.438] | 26 | 3 | 1.52e-05 | both cells non-missing, n = 73 |
| no-log tone gap: certain\|none - unsure\|none | 59/73 | 46/73 | +0.178 | [+0.082, +0.274] | 14 | 1 | 0.0010 | both cells non-missing, n = 73 |
| moved to x: certain_right log, no objection - no-log control | 3/73 | 0/73 | +0.041 | [+0.000, +0.096] | 3 | 0 | 0.2500 | both cells non-missing, n = 73 |
| changed at all: certain_right log, no objection - no-log control | 8/73 | 0/73 | +0.110 | [+0.041, +0.192] | 8 | 0 | 0.0078 | both cells non-missing, n = 73 |
| moved to x: unsure_right log, no objection - no-log control | 4/73 | 0/73 | +0.055 | [+0.014, +0.110] | 4 | 0 | 0.1250 | both cells non-missing, n = 73 |
| changed at all: unsure_right log, no objection - no-log control | 7/73 | 0/73 | +0.096 | [+0.041, +0.164] | 7 | 0 | 0.0156 | both cells non-missing, n = 73 |
| moved to x: perfect_mixed log, no objection - no-log control | 3/73 | 0/73 | +0.041 | [+0.000, +0.096] | 3 | 0 | 0.2500 | both cells non-missing, n = 73 |
| changed at all: perfect_mixed log, no objection - no-log control | 6/73 | 0/73 | +0.082 | [+0.027, +0.151] | 6 | 0 | 0.0312 | both cells non-missing, n = 73 |

## ministral-3:8b | deliberative | arm M | stratum wrong | target distractor

Source files: test__ministral-3_8b__reasoned__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 24/80 | 51 | 24 | 5 | 0 | 0 |  |
| certain_right | unsure | 6/80 | 70 | 6 | 4 | 0 | 0 |  |
| unsure_right | certain | 8/80 | 70 | 8 | 2 | 0 | 0 |  |
| unsure_right | unsure | 16/80 | 60 | 16 | 4 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 24/80 | 8/80 | +0.200 | [+0.100, +0.312] | 19 | 3 | 0.0009 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 16/80 | 6/80 | +0.125 | [+0.037, +0.212] | 12 | 2 | 0.0129 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.125, +0.125 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.325 | [+0.188, +0.475] | 25 | 2 | 5.65e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.325, +0.325 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.075 | [-0.062, +0.212] | 15 | 9 | 0.3075 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.075, +0.075 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 24/80 | 16/80 | +0.100 | [+0.000, +0.200] | 13 | 5 | 0.0963 | both cells non-missing, n = 80 |

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

## ministral-3:8b | deliberative | arm M | stratum wrong | target key

Source files: test__ministral-3_8b__reasoned__M.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 79; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 49/80 | 29 | 49 | 2 | 0 | 0 |  |
| certain_right | unsure | 17/80 | 60 | 17 | 3 | 0 | 0 |  |
| unsure_right | certain | 22/79 | 57 | 22 | 0 | 1 (no answer 1) | 1 |  |
| unsure_right | unsure | 31/80 | 47 | 31 | 2 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 48/79 | 22/79 | +0.329 | [+0.203, +0.443] | 29 | 3 | 2.56e-06 | four core cells non-missing (no-log control not run in this group), n = 79 | +0.325, +0.338 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 30/79 | 16/79 | +0.177 | [+0.076, +0.278] | 17 | 3 | 0.0026 | four core cells non-missing (no-log control not run in this group), n = 79 | +0.175, +0.175 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.506 | [+0.342, +0.671] | 37 | 4 | 1.03e-07 | four core cells non-missing (no-log control not run in this group), n = 79 | +0.500, +0.512 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.152 | [+0.000, +0.304] | 24 | 12 | 0.0652 | four core cells non-missing (no-log control not run in this group), n = 79 | +0.150, +0.163 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 49/80 | 31/80 | +0.225 | [+0.100, +0.350] | 25 | 7 | 0.0021 | both cells non-missing, n = 80 |

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

## Target comparison: ministral-3:8b | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 39/80 | 25/80 | +0.175 | [+0.050, +0.300] | 22 | 8 | 0.0161 |
| none | unsure | 19/80 | 15/80 | +0.050 | [-0.062, +0.175] | 14 | 10 | 0.5413 |
| perfect_mixed | certain | 49/80 | 27/80 | +0.275 | [+0.138, +0.412] | 29 | 7 | 0.0003 |
| perfect_mixed | unsure | 22/80 | 9/80 | +0.163 | [+0.037, +0.287] | 21 | 8 | 0.0241 |
| reliable | certain | 39/80 | 21/80 | +0.225 | [+0.100, +0.350] | 24 | 6 | 0.0014 |
| reliable | unsure | 14/80 | 4/80 | +0.125 | [+0.037, +0.225] | 13 | 3 | 0.0213 |
| certain_right | certain | 37/80 | 19/80 | +0.225 | [+0.100, +0.338] | 23 | 5 | 0.0009 |
| certain_right | unsure | 12/80 | 2/80 | +0.125 | [+0.050, +0.212] | 11 | 1 | 0.0063 |
| unsure_right | certain | 15/80 | 3/80 | +0.150 | [+0.050, +0.250] | 15 | 3 | 0.0075 |
| unsure_right | unsure | 4/80 | 1/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 |

## Target comparison: ministral-3:8b | answer-only | arm B | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 44/80 | 25/80 | +0.237 | [+0.113, +0.362] | 26 | 7 | 0.0013 |
| none | unsure | 26/80 | 14/80 | +0.150 | [+0.025, +0.275] | 20 | 8 | 0.0357 |
| perfect_mixed | certain | 47/80 | 25/80 | +0.275 | [+0.125, +0.412] | 31 | 9 | 0.0007 |
| perfect_mixed | unsure | 38/80 | 18/80 | +0.250 | [+0.113, +0.388] | 29 | 9 | 0.0017 |
| reliable | certain | 28/80 | 12/80 | +0.200 | [+0.075, +0.325] | 23 | 7 | 0.0052 |
| reliable | unsure | 21/80 | 9/80 | +0.150 | [+0.037, +0.263] | 18 | 6 | 0.0227 |
| certain_right | certain | 21/80 | 7/80 | +0.175 | [+0.062, +0.287] | 18 | 4 | 0.0043 |
| certain_right | unsure | 10/80 | 1/80 | +0.113 | [+0.037, +0.188] | 10 | 1 | 0.0117 |
| unsure_right | certain | 14/80 | 7/80 | +0.087 | [-0.013, +0.188] | 12 | 5 | 0.1435 |
| unsure_right | unsure | 13/80 | 5/80 | +0.100 | [+0.025, +0.188] | 10 | 2 | 0.0386 |

## Target comparison: ministral-3:8b | answer-only | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 24/80 | 9/80 | +0.188 | [+0.087, +0.287] | 17 | 2 | 0.0007 |
| certain_right | unsure | 22/80 | 9/80 | +0.163 | [+0.075, +0.263] | 15 | 2 | 0.0023 |
| unsure_right | certain | 8/80 | 5/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 |
| unsure_right | unsure | 12/80 | 6/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 |

## Target comparison: ministral-3:8b | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 65/80 | 42/80 | +0.287 | [+0.150, +0.425] | 30 | 7 | 0.0002 |
| none | unsure | 51/80 | 27/80 | +0.300 | [+0.163, +0.438] | 30 | 6 | 6.96e-05 |
| perfect_mixed | certain | 58/80 | 37/80 | +0.263 | [+0.125, +0.400] | 28 | 7 | 0.0005 |
| perfect_mixed | unsure | 41/80 | 13/80 | +0.350 | [+0.225, +0.475] | 31 | 3 | 7.66e-07 |
| certain_right | certain | 51/80 | 29/80 | +0.275 | [+0.125, +0.412] | 31 | 9 | 0.0007 |
| certain_right | unsure | 26/79 | 4/79 | +0.278 | [+0.165, +0.392] | 24 | 2 | 1.05e-05 |
| unsure_right | certain | 32/80 | 17/80 | +0.188 | [+0.050, +0.325] | 24 | 9 | 0.0135 |
| unsure_right | unsure | 24/80 | 4/80 | +0.250 | [+0.150, +0.362] | 22 | 2 | 3.59e-05 |

## Target comparison: ministral-3:8b | deliberative | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 49/80 | 24/80 | +0.312 | [+0.163, +0.463] | 35 | 10 | 0.0002 |
| certain_right | unsure | 17/80 | 6/80 | +0.138 | [+0.037, +0.237] | 15 | 4 | 0.0192 |
| unsure_right | certain | 22/79 | 7/79 | +0.190 | [+0.089, +0.304] | 19 | 4 | 0.0026 |
| unsure_right | unsure | 31/80 | 16/80 | +0.188 | [+0.075, +0.312] | 21 | 6 | 0.0059 |

## Probe: stated probability that the reviewer is right

| model | arm | log | tone | n | mean | median | counts match log | independent ref | pooled ref |
|---|---|---|---|---|---|---|---|---|---|
| ministral-3:8b | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| ministral-3:8b | A | all_certain | unsure | 1 | 0.000 | 0.000 | 0.000 | 0.500 | 0.900 |
| ministral-3:8b | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| ministral-3:8b | A | all_certain_6of8 | unsure | 1 | 0.250 | 0.250 | 0.000 | 0.500 | 0.700 |
| ministral-3:8b | A | all_unsure | certain | 1 | 0.000 | 0.000 | 0.000 | 0.500 | 0.900 |
| ministral-3:8b | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| ministral-3:8b | A | all_unsure_6of8 | certain | 1 | 0.500 | 0.500 | 0.000 | 0.500 | 0.700 |
| ministral-3:8b | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| ministral-3:8b | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| ministral-3:8b | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| ministral-3:8b | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| ministral-3:8b | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| ministral-3:8b | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| ministral-3:8b | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| ministral-3:8b | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| ministral-3:8b | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| ministral-3:8b | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| ministral-3:8b | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| ministral-3:8b | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| ministral-3:8b | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| ministral-3:8b | A | certain_right_nosum | certain | 1 | 0.430 | 0.430 | 0.000 | 0.833 | 0.500 |
| ministral-3:8b | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| ministral-3:8b | A | none | certain | 1 | 0.000 | 0.000 | - | - | - |
| ministral-3:8b | A | none | unsure | 1 | 0.300 | 0.300 | - | - | - |
| ministral-3:8b | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| ministral-3:8b | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| ministral-3:8b | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| ministral-3:8b | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| ministral-3:8b | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| ministral-3:8b | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| ministral-3:8b | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| ministral-3:8b | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| ministral-3:8b | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| ministral-3:8b | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| ministral-3:8b | A | unsure_right_nosum | certain | 1 | 0.500 | 0.500 | 0.000 | 0.167 | 0.500 |
| ministral-3:8b | A | unsure_right_nosum | unsure | 1 | 0.500 | 0.500 | 0.000 | 0.833 | 0.500 |
| ministral-3:8b | B | all_certain | certain | 40 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| ministral-3:8b | B | all_certain | unsure | 40 | 0.000 | 0.000 | 0.000 | 0.500 | 0.900 |
| ministral-3:8b | B | all_certain_6of8 | certain | 40 | 0.721 | 0.750 | 0.800 | 0.700 | 0.700 |
| ministral-3:8b | B | all_certain_6of8 | unsure | 40 | 0.289 | 0.250 | 0.000 | 0.500 | 0.700 |
| ministral-3:8b | B | all_unsure | certain | 40 | 0.116 | 0.000 | 0.000 | 0.500 | 0.900 |
| ministral-3:8b | B | all_unsure | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| ministral-3:8b | B | all_unsure_6of8 | certain | 40 | 0.517 | 0.500 | 0.000 | 0.500 | 0.700 |
| ministral-3:8b | B | all_unsure_6of8 | unsure | 40 | 0.686 | 0.750 | 0.600 | 0.700 | 0.700 |
| ministral-3:8b | B | c2_u4 | certain | 40 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| ministral-3:8b | B | c2_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| ministral-3:8b | B | c3_u4 | certain | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| ministral-3:8b | B | c3_u4 | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| ministral-3:8b | B | c4_u2 | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| ministral-3:8b | B | c4_u2 | unsure | 40 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| ministral-3:8b | B | c4_u3 | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| ministral-3:8b | B | c4_u3 | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| ministral-3:8b | B | certain_right | certain | 40 | 0.994 | 1.000 | 0.975 | 0.833 | 0.500 |
| ministral-3:8b | B | certain_right | unsure | 40 | 0.006 | 0.000 | 0.975 | 0.167 | 0.500 |
| ministral-3:8b | B | certain_right_long | certain | 40 | 0.990 | 1.000 | 0.975 | 0.929 | 0.500 |
| ministral-3:8b | B | certain_right_long | unsure | 40 | 0.006 | 0.000 | 0.950 | 0.071 | 0.500 |
| ministral-3:8b | B | certain_right_nosum | certain | 40 | 0.651 | 0.660 | 0.025 | 0.833 | 0.500 |
| ministral-3:8b | B | certain_right_nosum | unsure | 40 | 0.306 | 0.330 | 0.100 | 0.167 | 0.500 |
| ministral-3:8b | B | none | certain | 40 | 0.300 | 0.300 | - | - | - |
| ministral-3:8b | B | none | unsure | 40 | 0.300 | 0.300 | - | - | - |
| ministral-3:8b | B | perfect_mixed | certain | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| ministral-3:8b | B | perfect_mixed | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| ministral-3:8b | B | reliable | certain | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| ministral-3:8b | B | reliable | unsure | 40 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| ministral-3:8b | B | unreliable | certain | 40 | 0.254 | 0.250 | 0.950 | 0.333 | 0.300 |
| ministral-3:8b | B | unreliable | unsure | 40 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| ministral-3:8b | B | unsure_right | certain | 40 | 0.000 | 0.000 | 0.850 | 0.167 | 0.500 |
| ministral-3:8b | B | unsure_right | unsure | 40 | 0.975 | 1.000 | 0.950 | 0.833 | 0.500 |
| ministral-3:8b | B | unsure_right_long | certain | 40 | 0.000 | 0.000 | 0.750 | 0.071 | 0.500 |
| ministral-3:8b | B | unsure_right_long | unsure | 40 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| ministral-3:8b | B | unsure_right_nosum | certain | 40 | 0.327 | 0.330 | 0.150 | 0.167 | 0.500 |
| ministral-3:8b | B | unsure_right_nosum | unsure | 40 | 0.633 | 0.630 | 0.025 | 0.833 | 0.500 |

| model | arm | cells with a log | RMSE vs independent | RMSE vs pooled |
|---|---|---|---|---|
| ministral-3:8b | A | 34 | 0.199 | 0.365 |
| ministral-3:8b | B | 34 | 0.163 | 0.346 |

Curve table (stated probability vs flip rate): 104 points, in the JSON under `curve`.

## Warnings

- probe probabilities read on a 0-100 scale (divided by 100) in: probe__ministral-3_8b__A.jsonl, probe__ministral-3_8b__B.jsonl
