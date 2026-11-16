# Analysis: arm_s_frozen

Inputs: test__gemma4_12b__instant__S.jsonl, test__ministral-3_8b__instant__S.jsonl, test__openai_gpt-6-sol__instant__S.jsonl, test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__S.jsonl, test__openrouter_meta-llama_llama-4-maverick__instant__S.jsonl. Rows read: 3600. Probe files: -.

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
| gemma4:12b | answer-only | (no meta) | - | - | 720 |
| ministral-3:8b | answer-only | (no meta) | - | - | 720 |
| openai:gpt-6-sol | answer-only | temperature=0 | reasoning_effort=none | 32 | 720 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | temperature=0 | n/a | 32 | 720 |
| openrouter:meta-llama/llama-4-maverick | answer-only | temperature=0 | n/a | 32 | 720 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

# Exploratory

## gemma4:12b | answer-only | arm S | stratum wrong | target key

Source files: test__gemma4_12b__instant__S.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 74/80 | 6 | 74 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 40/80 | 40 | 40 | 0 | 0 | 0 |  |
| certain_right | certain | 13/80 | 67 | 13 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| control | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 0/80 | 0 |
| certain_right log shown | 0/80 | 0/80 | 0 |
| unsure_right log shown | 0/80 | 0/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 13/80 | 2/80 | +0.138 | [+0.062, +0.225] | 12 | 1 | 0.0034 | no-log control + four core cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.138 | [+0.062, +0.225] | 12 | 1 | 0.0034 | no-log control + four core cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.138 | [+0.062, +0.225] | 12 | 1 | 0.0034 | no-log control + four core cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 40/80 | 0/80 | +0.500 | [+0.388, +0.613] | 40 | 0 | 1.82e-12 | both cells non-missing, n = 80 | +0.500, +0.500 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 74/80 | 13/80 | +0.762 | [+0.662, +0.850] | 61 | 0 | 8.67e-19 | both cells non-missing, n = 80 | +0.762, +0.762 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 13/80 | 0/80 | +0.163 | [+0.087, +0.250] | 13 | 0 | 0.0002 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

## ministral-3:8b | answer-only | arm S | stratum wrong | target key

Source files: test__ministral-3_8b__instant__S.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 49/80 | 27 | 49 | 4 | 0 | 0 |  |
| perfect_mixed | unsure | 22/80 | 51 | 22 | 7 | 0 | 0 |  |
| certain_right | certain | 25/80 | 50 | 25 | 5 | 0 | 0 |  |
| certain_right | unsure | 7/80 | 69 | 7 | 4 | 0 | 0 |  |
| unsure_right | certain | 20/80 | 51 | 20 | 9 | 0 | 0 |  |
| unsure_right | unsure | 9/80 | 64 | 9 | 7 | 0 | 0 |  |
| control | none | 7/80 | 56 | 7 | 17 | 0 | 0 |  |
| certain_right | none | 14/80 | 47 | 14 | 19 | 0 | 0 |  |
| unsure_right | none | 12/80 | 49 | 12 | 19 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 7/80 | 24/80 | 0 |
| certain_right log shown | 14/80 | 33/80 | 0 |
| unsure_right log shown | 12/80 | 31/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 25/80 | 20/80 | +0.062 | [-0.050, +0.175] | 14 | 9 | 0.4049 | no-log control + four core cells non-missing, n = 80 | +0.062, +0.062 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 9/80 | 7/80 | +0.025 | [-0.037, +0.087] | 4 | 2 | 0.6875 | no-log control + four core cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.087 | [-0.037, +0.212] | 16 | 9 | 0.2295 | no-log control + four core cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.037 | [-0.100, +0.175] | 14 | 13 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 22/80 | 9/80 | +0.163 | [+0.087, +0.250] | 13 | 0 | 0.0002 | both cells non-missing, n = 80 | +0.163, +0.163 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 49/80 | 25/80 | +0.300 | [+0.200, +0.400] | 24 | 0 | 1.19e-07 | both cells non-missing, n = 80 | +0.300, +0.300 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 25/80 | 9/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 14/80 | 7/80 | +0.087 | [+0.037, +0.150] | 7 | 0 | 0.0156 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 33/80 | 24/80 | +0.113 | [+0.013, +0.212] | 13 | 4 | 0.0490 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 12/80 | 7/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 31/80 | 24/80 | +0.087 | [+0.000, +0.188] | 11 | 4 | 0.1185 | both cells non-missing, n = 80 |

## openai:gpt-6-sol | answer-only | arm S | stratum wrong | target key

Source files: test__openai_gpt-6-sol__instant__S.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 44/80 | 36 | 44 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 38/80 | 42 | 38 | 0 | 0 | 0 |  |
| certain_right | certain | 48/80 | 32 | 48 | 0 | 0 | 0 |  |
| certain_right | unsure | 7/80 | 73 | 7 | 0 | 0 | 0 |  |
| unsure_right | certain | 10/80 | 70 | 10 | 0 | 0 | 0 |  |
| unsure_right | unsure | 39/80 | 40 | 39 | 1 | 0 | 0 |  |
| control | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unsure_right | none | 4/80 | 75 | 4 | 1 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 0/80 | 0 |
| certain_right log shown | 2/80 | 2/80 | 0 |
| unsure_right log shown | 4/80 | 5/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 48/80 | 10/80 | +0.475 | [+0.362, +0.588] | 38 | 0 | 7.28e-12 | no-log control + four core cells non-missing, n = 80 | +0.475, +0.475 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 39/80 | 7/80 | +0.400 | [+0.300, +0.500] | 32 | 0 | 4.66e-10 | no-log control + four core cells non-missing, n = 80 | +0.400, +0.400 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.875 | [+0.700, +1.050] | 48 | 0 | 7.11e-15 | no-log control + four core cells non-missing, n = 80 | +0.875, +0.875 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.075 | [-0.050, +0.200] | 16 | 10 | 0.3269 | no-log control + four core cells non-missing, n = 80 | +0.075, +0.075 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 38/80 | 39/80 | -0.013 | [-0.100, +0.062] | 5 | 6 | 1.0000 | both cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 44/80 | 48/80 | -0.050 | [-0.125, +0.025] | 3 | 7 | 0.3438 | both cells non-missing, n = 80 | -0.050, -0.050 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 48/80 | 39/80 | +0.113 | [+0.013, +0.212] | 14 | 5 | 0.0636 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 4/80 | 0/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 5/80 | 0/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm S | stratum wrong | target key

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__S.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 69/80 | 6 | 69 | 5 | 0 | 0 |  |
| perfect_mixed | unsure | 59/80 | 15 | 59 | 6 | 0 | 0 |  |
| certain_right | certain | 53/80 | 23 | 53 | 4 | 0 | 0 |  |
| certain_right | unsure | 23/80 | 50 | 23 | 7 | 0 | 0 |  |
| unsure_right | certain | 33/80 | 42 | 33 | 5 | 0 | 0 |  |
| unsure_right | unsure | 30/80 | 46 | 30 | 4 | 0 | 0 |  |
| control | none | 15/80 | 51 | 15 | 14 | 0 | 0 |  |
| certain_right | none | 18/80 | 49 | 18 | 13 | 0 | 0 |  |
| unsure_right | none | 20/80 | 46 | 20 | 14 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 15/80 | 29/80 | 0 |
| certain_right log shown | 18/80 | 31/80 | 0 |
| unsure_right log shown | 20/80 | 34/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 53/80 | 33/80 | +0.250 | [+0.150, +0.362] | 22 | 2 | 3.59e-05 | no-log control + four core cells non-missing, n = 80 | +0.250, +0.250 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 30/80 | 23/80 | +0.087 | [-0.013, +0.188] | 13 | 6 | 0.1671 | no-log control + four core cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.338 | [+0.225, +0.463] | 28 | 2 | 8.68e-07 | no-log control + four core cells non-missing, n = 80 | +0.338, +0.338 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.163 | [-0.013, +0.338] | 22 | 13 | 0.1755 | no-log control + four core cells non-missing, n = 80 | +0.163, +0.163 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 59/80 | 30/80 | +0.362 | [+0.263, +0.475] | 29 | 0 | 3.73e-09 | both cells non-missing, n = 80 | +0.362, +0.362 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 69/80 | 53/80 | +0.200 | [+0.113, +0.300] | 17 | 1 | 0.0001 | both cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 53/80 | 30/80 | +0.287 | [+0.188, +0.400] | 24 | 1 | 1.55e-06 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 18/80 | 15/80 | +0.037 | [-0.037, +0.113] | 6 | 3 | 0.5078 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 31/80 | 29/80 | +0.025 | [-0.062, +0.113] | 7 | 5 | 0.7744 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 20/80 | 15/80 | +0.062 | [-0.013, +0.150] | 8 | 3 | 0.2266 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 34/80 | 29/80 | +0.062 | [-0.013, +0.138] | 8 | 3 | 0.2266 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-4-maverick | answer-only | arm S | stratum wrong | target key

Source files: test__openrouter_meta-llama_llama-4-maverick__instant__S.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 70/80 | 9 | 70 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 41/80 | 38 | 41 | 1 | 0 | 0 |  |
| certain_right | certain | 40/80 | 39 | 40 | 1 | 0 | 0 |  |
| certain_right | unsure | 3/80 | 76 | 3 | 1 | 0 | 0 |  |
| unsure_right | certain | 17/80 | 63 | 17 | 0 | 0 | 0 |  |
| unsure_right | unsure | 9/80 | 71 | 9 | 0 | 0 | 0 |  |
| control | none | 6/80 | 73 | 6 | 1 | 0 | 0 |  |
| certain_right | none | 10/80 | 66 | 10 | 4 | 0 | 0 |  |
| unsure_right | none | 11/80 | 67 | 11 | 2 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 6/80 | 7/80 | 0 |
| certain_right log shown | 10/80 | 14/80 | 0 |
| unsure_right log shown | 11/80 | 13/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 40/80 | 17/80 | +0.287 | [+0.163, +0.412] | 29 | 6 | 0.0001 | no-log control + four core cells non-missing, n = 80 | +0.287, +0.287 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 9/80 | 3/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 | no-log control + four core cells non-missing, n = 80 | +0.075, +0.075 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.362 | [+0.237, +0.487] | 34 | 5 | 2.43e-06 | no-log control + four core cells non-missing, n = 80 | +0.362, +0.362 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.212 | [+0.050, +0.375] | 29 | 13 | 0.0195 | no-log control + four core cells non-missing, n = 80 | +0.212, +0.212 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 41/80 | 9/80 | +0.400 | [+0.300, +0.512] | 32 | 0 | 4.66e-10 | both cells non-missing, n = 80 | +0.400, +0.400 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 70/80 | 40/80 | +0.375 | [+0.275, +0.475] | 30 | 0 | 1.86e-09 | both cells non-missing, n = 80 | +0.375, +0.375 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 40/80 | 9/80 | +0.388 | [+0.275, +0.500] | 32 | 1 | 7.92e-09 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 10/80 | 6/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 14/80 | 7/80 | +0.087 | [+0.025, +0.163] | 8 | 1 | 0.0391 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 11/80 | 6/80 | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 13/80 | 7/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 | both cells non-missing, n = 80 |
