# Analysis: o7_sonnet_reasoned

Inputs: test__anthropic_claude-sonnet-5-5__reasoned__A.jsonl. Rows read: 560. Probe files: -.

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
| anthropic:claude-sonnet-5-5 | deliberative | default | thinking=between_tools, effort=low | 1500 | 560 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-sonnet-5-5 | deliberative | secondary | C1 | 25/40 | 2/40 | +0.575 | [+0.425, +0.725] | 23 | 0 | 2.38e-07 | 9.54e-07 | no-log control + four core cells non-missing, n = 40 |
| anthropic:claude-sonnet-5-5 | deliberative | secondary | C2 |  |  | +0.150 | [+0.000, +0.300] | 8 | 2 | 0.1094 | 0.3281 | no-log control + four core cells non-missing, n = 40 |
| anthropic:claude-sonnet-5-5 | deliberative | secondary | C3 |  |  | - | - | 0 | 0 | - | - | not available, n = 0 |
| anthropic:claude-sonnet-5-5 | deliberative | secondary | C4 |  |  | - | - | 0 | 0 | - | - | not available, n = 0 |

# Exploratory

## anthropic:claude-sonnet-5-5 | deliberative | arm A | stratum right | target distractor

Source files: test__anthropic_claude-sonnet-5-5__reasoned__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| certain_right | certain | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| control | none | 0/40 | 40 | 0 | 0 | 0 | 0 |  |

Not run: unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/40 | 0/40 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/40 | 0/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 40 | +0.050, +0.050 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/40 | 0/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 40 | +0.050, +0.050 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.100 | [+0.000, +0.250] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 40 | +0.100, +0.100 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/40 | 2/40 | +0.000 | [-0.075, +0.075] | 1 | 1 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 2/40 | 2/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/40 | 2/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/40 | 0/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 40 | +0.050, +0.050 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/40 | 0/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 40 | +0.050, +0.050 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.100 | [+0.000, +0.250] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 40 | +0.100, +0.100 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/40 | 2/40 | +0.000 | [-0.075, +0.075] | 1 | 1 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 2/40 | 2/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/40 | 2/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |

## anthropic:claude-sonnet-5-5 | deliberative | arm A | stratum wrong | target key

Source files: test__anthropic_claude-sonnet-5-5__reasoned__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 10/40 | 29 | 10 | 1 | 0 | 0 |  |
| certain_right | certain | 25/40 | 14 | 25 | 1 | 0 | 0 |  |
| certain_right | unsure | 3/40 | 37 | 3 | 0 | 0 | 0 |  |
| unsure_right | certain | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| unsure_right | unsure | 20/40 | 19 | 20 | 1 | 0 | 0 |  |
| control | none | 3/40 | 34 | 3 | 3 | 0 | 0 |  |

Not run: unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 3/40 | 6/40 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 25/40 | 2/40 | +0.575 | [+0.425, +0.725] | 23 | 0 | 2.38e-07 | no-log control + four core cells non-missing, n = 40 | +0.575, +0.575 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 20/40 | 3/40 | +0.425 | [+0.275, +0.575] | 17 | 0 | 1.53e-05 | no-log control + four core cells non-missing, n = 40 | +0.425, +0.425 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +1.000 | [+0.725, +1.275] | 25 | 0 | 5.96e-08 | no-log control + four core cells non-missing, n = 40 | +1.000, +1.000 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.150 | [+0.000, +0.300] | 8 | 2 | 0.1094 | no-log control + four core cells non-missing, n = 40 | +0.150, +0.150 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 25/40 | 20/40 | +0.125 | [-0.025, +0.275] | 7 | 2 | 0.1797 | both cells non-missing, n = 40 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 20/34 | 0/34 | +0.588 | [+0.412, +0.765] | 20 | 0 | 1.91e-06 | no-log control + four core cells non-missing, n = 34 | +0.588, +0.588 (N = 34) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 16/34 | 0/34 | +0.471 | [+0.324, +0.647] | 16 | 0 | 3.05e-05 | no-log control + four core cells non-missing, n = 34 | +0.471, +0.471 (N = 34) |
| I = d_c + d_u (tone x log interaction) |  |  | +1.059 | [+0.765, +1.353] | 22 | 0 | 4.77e-07 | no-log control + four core cells non-missing, n = 34 | +1.059, +1.059 (N = 34) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.118 | [-0.029, +0.265] | 6 | 2 | 0.2891 | no-log control + four core cells non-missing, n = 34 | +0.118, +0.118 (N = 34) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 20/34 | 16/34 | +0.118 | [-0.029, +0.265] | 6 | 2 | 0.2891 | both cells non-missing, n = 34 |
