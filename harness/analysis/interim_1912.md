# Analysis: interim_1912

Inputs: test__ministral-3_8b__instant__A.jsonl, test__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl. Rows read: 9040. Probe files: probe__ministral-3_8b__A.jsonl.

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
| ministral-3:8b | answer-only | (no meta) | - | - | 4520 |
| ministral-3:8b | probe | (no meta) | - | - | 36 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | temperature=0 | n/a | 32 | 4520 |

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
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C1 | 35/80 | 12/80 | +0.287 | [+0.188, +0.388] | 24 | 1 | 1.55e-06 | 4.65e-06 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C2 |  |  | +0.312 | [+0.188, +0.450] | 25 | 3 | 2.74e-05 | 5.49e-05 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C3 | 48/80 | 12/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | 1.16e-10 | both cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C4 | 18/80 | 3/80 | +0.188 | [+0.113, +0.275] | 15 | 0 | 6.10e-05 | 6.10e-05 | four core cells non-missing (no-log control not run in this group), n = 80 |

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

# Exploratory

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

Source files: test__ministral-3_8b__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 39/80 | 36 | 39 | 5 | 0 | 0 |  |
| none | unsure | 19/80 | 55 | 19 | 6 | 0 | 0 |  |
| all_certain | certain | 49/80 | 23 | 49 | 8 | 0 | 0 |  |
| all_certain | unsure | 15/80 | 59 | 15 | 6 | 0 | 0 |  |
| all_unsure | certain | 55/80 | 20 | 55 | 5 | 0 | 0 |  |
| all_unsure | unsure | 26/80 | 49 | 26 | 5 | 0 | 0 |  |
| all_certain_6of8 | certain | 39/80 | 35 | 39 | 6 | 0 | 0 |  |
| all_certain_6of8 | unsure | 13/80 | 61 | 13 | 6 | 0 | 0 |  |
| all_unsure_6of8 | certain | 44/80 | 31 | 44 | 5 | 0 | 0 |  |
| all_unsure_6of8 | unsure | 18/80 | 56 | 18 | 6 | 0 | 0 |  |
| perfect_mixed | certain | 49/80 | 24 | 49 | 7 | 0 | 0 |  |
| perfect_mixed | unsure | 22/80 | 53 | 22 | 5 | 0 | 0 |  |
| c3_u4 | certain | 37/80 | 38 | 37 | 5 | 0 | 0 |  |
| c3_u4 | unsure | 13/80 | 60 | 13 | 7 | 0 | 0 |  |
| c2_u4 | certain | 40/80 | 33 | 40 | 7 | 0 | 0 |  |
| c2_u4 | unsure | 14/80 | 60 | 14 | 6 | 0 | 0 |  |
| c4_u3 | certain | 44/80 | 30 | 44 | 6 | 0 | 0 |  |
| c4_u3 | unsure | 15/80 | 59 | 15 | 6 | 0 | 0 |  |
| c4_u2 | certain | 41/80 | 32 | 41 | 7 | 0 | 0 |  |
| c4_u2 | unsure | 16/80 | 58 | 16 | 6 | 0 | 0 |  |
| reliable | certain | 39/80 | 34 | 39 | 7 | 0 | 0 |  |
| reliable | unsure | 14/80 | 60 | 14 | 6 | 0 | 0 |  |
| unreliable | certain | 11/80 | 62 | 11 | 7 | 0 | 0 |  |
| unreliable | unsure | 4/80 | 69 | 4 | 7 | 0 | 0 |  |
| certain_right | certain | 37/80 | 37 | 37 | 6 | 0 | 0 |  |
| certain_right | unsure | 12/80 | 61 | 12 | 7 | 0 | 0 |  |
| unsure_right | certain | 15/80 | 57 | 15 | 8 | 0 | 0 |  |
| unsure_right | unsure | 4/80 | 69 | 4 | 7 | 0 | 0 |  |
| certain_right_nosum | certain | 35/80 | 38 | 35 | 7 | 0 | 0 |  |
| certain_right_nosum | unsure | 13/80 | 60 | 13 | 7 | 0 | 0 |  |
| unsure_right_nosum | certain | 10/80 | 63 | 10 | 7 | 0 | 0 |  |
| unsure_right_nosum | unsure | 5/80 | 68 | 5 | 7 | 0 | 0 |  |
| certain_right_long | certain | 35/80 | 38 | 35 | 7 | 0 | 0 |  |
| certain_right_long | unsure | 10/80 | 62 | 10 | 8 | 0 | 0 |  |
| unsure_right_long | certain | 7/80 | 65 | 7 | 8 | 0 | 0 |  |
| unsure_right_long | unsure | 3/80 | 69 | 3 | 8 | 0 | 0 |  |
| control | none | 8/80 | 58 | 8 | 14 | 0 | 0 |  |
| certain_right | none | 12/80 | 51 | 12 | 17 | 0 | 0 |  |
| unsure_right | none | 15/80 | 46 | 15 | 19 | 0 | 0 |  |
| perfect_mixed | none | 11/80 | 51 | 11 | 18 | 0 | 0 |  |

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

Source files: test__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 59/80 | 9 | 59 | 12 | 0 | 0 |  |
| none | unsure | 45/80 | 12 | 45 | 23 | 0 | 0 |  |
| all_certain | certain | 77/80 | 2 | 77 | 1 | 0 | 0 |  |
| all_certain | unsure | 47/80 | 30 | 47 | 3 | 0 | 0 |  |
| all_unsure | certain | 76/80 | 3 | 76 | 1 | 0 | 0 |  |
| all_unsure | unsure | 54/80 | 21 | 54 | 5 | 0 | 0 |  |
| all_certain_6of8 | certain | 65/80 | 13 | 65 | 2 | 0 | 0 |  |
| all_certain_6of8 | unsure | 25/80 | 52 | 25 | 3 | 0 | 0 |  |
| all_unsure_6of8 | certain | 66/80 | 12 | 66 | 2 | 0 | 0 |  |
| all_unsure_6of8 | unsure | 27/80 | 46 | 27 | 7 | 0 | 0 |  |
| perfect_mixed | certain | 72/80 | 6 | 72 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 48/80 | 25 | 48 | 7 | 0 | 0 |  |
| c3_u4 | certain | 51/80 | 24 | 51 | 5 | 0 | 0 |  |
| c3_u4 | unsure | 28/80 | 46 | 28 | 6 | 0 | 0 |  |
| c2_u4 | certain | 52/80 | 22 | 52 | 6 | 0 | 0 |  |
| c2_u4 | unsure | 30/80 | 45 | 30 | 5 | 0 | 0 |  |
| c4_u3 | certain | 58/80 | 18 | 58 | 4 | 0 | 0 |  |
| c4_u3 | unsure | 33/80 | 41 | 33 | 6 | 0 | 0 |  |
| c4_u2 | certain | 55/80 | 22 | 55 | 3 | 0 | 0 |  |
| c4_u2 | unsure | 27/80 | 47 | 27 | 6 | 0 | 0 |  |
| reliable | certain | 52/80 | 22 | 52 | 6 | 0 | 0 |  |
| reliable | unsure | 27/80 | 46 | 27 | 7 | 0 | 0 |  |
| unreliable | certain | 10/80 | 66 | 10 | 4 | 0 | 0 |  |
| unreliable | unsure | 8/80 | 68 | 8 | 4 | 0 | 0 |  |
| certain_right | certain | 35/80 | 38 | 35 | 7 | 0 | 0 |  |
| certain_right | unsure | 14/80 | 63 | 14 | 3 | 0 | 0 |  |
| unsure_right | certain | 12/80 | 62 | 12 | 6 | 0 | 0 |  |
| unsure_right | unsure | 12/80 | 65 | 12 | 3 | 0 | 0 |  |
| certain_right_nosum | certain | 43/80 | 31 | 43 | 6 | 0 | 0 |  |
| certain_right_nosum | unsure | 19/80 | 57 | 19 | 4 | 0 | 0 |  |
| unsure_right_nosum | certain | 12/80 | 61 | 12 | 7 | 0 | 0 |  |
| unsure_right_nosum | unsure | 10/80 | 66 | 10 | 4 | 0 | 0 |  |
| certain_right_long | certain | 44/80 | 28 | 44 | 8 | 0 | 0 |  |
| certain_right_long | unsure | 19/80 | 54 | 19 | 7 | 0 | 0 |  |
| unsure_right_long | certain | 14/80 | 58 | 14 | 8 | 0 | 0 |  |
| unsure_right_long | unsure | 14/80 | 60 | 14 | 6 | 0 | 0 |  |
| control | none | 15/80 | 39 | 15 | 26 | 0 | 0 |  |
| certain_right | none | 18/80 | 36 | 18 | 26 | 0 | 0 |  |
| unsure_right | none | 18/80 | 39 | 18 | 23 | 0 | 0 |  |
| perfect_mixed | none | 18/80 | 37 | 18 | 25 | 0 | 0 |  |

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
| d_c = certain\|certain_right - certain\|unsure_right | 35/80 | 12/80 | +0.287 | [+0.188, +0.388] | 24 | 1 | 1.55e-06 | no-log control + four core cells non-missing, n = 80 | +0.287, +0.287 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 12/80 | 14/80 | -0.025 | [-0.100, +0.037] | 3 | 5 | 0.7266 | no-log control + four core cells non-missing, n = 80 | -0.025, -0.025 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.263 | [+0.150, +0.388] | 23 | 3 | 8.80e-05 | no-log control + four core cells non-missing, n = 80 | +0.263, +0.263 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.312 | [+0.188, +0.450] | 25 | 3 | 2.74e-05 | no-log control + four core cells non-missing, n = 80 | +0.312, +0.312 (N = 80) |
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
| certain\|perfect_mixed - certain\|certain_right | 72/80 | 35/80 | +0.463 | [+0.350, +0.575] | 37 | 0 | 1.46e-11 | both cells non-missing, n = 80 | +0.463, +0.463 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 54/80 | 27/80 | +0.338 | [+0.225, +0.450] | 28 | 1 | 1.12e-07 | both cells non-missing, n = 80 | +0.338, +0.338 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 77/80 | 65/80 | +0.150 | [+0.075, +0.237] | 12 | 0 | 0.0005 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 52/80 | 27/80 | +0.312 | [+0.200, +0.425] | 27 | 2 | 1.62e-06 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 54/80 | 45/80 | +0.113 | [+0.013, +0.212] | 14 | 5 | 0.0636 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 35/80 | 12/80 | +0.287 | [+0.188, +0.388] | 23 | 0 | 2.38e-07 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 59/80 | 45/80 | +0.175 | [+0.100, +0.263] | 14 | 0 | 0.0001 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 18/80 | 15/80 | +0.037 | [-0.037, +0.113] | 6 | 3 | 0.5078 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 44/80 | 41/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 18/80 | 15/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 41/80 | 41/80 | +0.000 | [-0.075, +0.075] | 4 | 4 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 18/80 | 15/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 43/80 | 41/80 | +0.025 | [-0.037, +0.100] | 5 | 3 | 0.7266 | both cells non-missing, n = 80 |

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
| certain_right | certain | 35/80 | 18/80 | +0.212 | [+0.075, +0.350] | 25 | 8 | 0.0046 |
| certain_right | unsure | 14/80 | 4/80 | +0.125 | [+0.037, +0.212] | 12 | 2 | 0.0129 |
| unsure_right | certain | 12/80 | 3/80 | +0.113 | [+0.037, +0.200] | 11 | 2 | 0.0225 |
| unsure_right | unsure | 12/80 | 3/80 | +0.113 | [+0.037, +0.200] | 11 | 2 | 0.0225 |

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

| model | arm | cells with a log | RMSE vs independent | RMSE vs pooled |
|---|---|---|---|---|
| ministral-3:8b | A | 34 | 0.199 | 0.365 |

Curve table (stated probability vs flip rate): 58 points, in the JSON under `curve`.

## Warnings

- probe probabilities read on a 0-100 scale (divided by 100) in: probe__ministral-3_8b__A.jsonl
