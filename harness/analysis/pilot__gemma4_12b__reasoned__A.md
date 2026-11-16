# Analysis: pilot__gemma4_12b__reasoned__A

Inputs: pilot__gemma4_12b__reasoned__A.jsonl. Rows read: 608. Probe files: -.

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

## gemma4:12b | deliberative | arm A | stratum wrong | target key

Source files: pilot__gemma4_12b__reasoned__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 28; of these, also with a non-missing no-log control (by-voice population): 23. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 18/28 | 10 | 18 | 0 | 4 (no answer 4) | 4 |  |
| none | unsure | 16/30 | 14 | 16 | 0 | 2 (no answer 2) | 2 |  |
| all_certain | certain | 27/31 | 4 | 27 | 0 | 1 (no answer 1) | 1 |  |
| all_certain | unsure | 16/30 | 13 | 16 | 1 | 2 (no answer 2) | 2 |  |
| all_unsure | certain | 25/30 | 5 | 25 | 0 | 2 (no answer 2) | 2 |  |
| all_unsure | unsure | 20/29 | 9 | 20 | 0 | 3 (no answer 3) | 3 |  |
| perfect_mixed | certain | 27/29 | 2 | 27 | 0 | 3 (no answer 3) | 3 |  |
| perfect_mixed | unsure | 20/30 | 10 | 20 | 0 | 2 (no answer 2) | 2 |  |
| reliable | certain | 20/30 | 10 | 20 | 0 | 2 (no answer 2) | 2 |  |
| reliable | unsure | 18/31 | 13 | 18 | 0 | 1 (no answer 1) | 1 |  |
| certain_right | certain | 25/31 | 6 | 25 | 0 | 1 (no answer 1) | 1 |  |
| certain_right | unsure | 16/30 | 14 | 16 | 0 | 2 (no answer 2) | 2 |  |
| unsure_right | certain | 14/29 | 15 | 14 | 0 | 3 (no answer 3) | 3 |  |
| unsure_right | unsure | 16/29 | 13 | 16 | 0 | 3 (no answer 3) | 3 |  |
| certain_right_long | certain | 23/31 | 8 | 23 | 0 | 1 (no answer 1) | 1 |  |
| certain_right_long | unsure | 14/30 | 15 | 14 | 1 | 2 (no answer 2) | 2 |  |
| unsure_right_long | certain | 15/32 | 17 | 15 | 0 | 0 | 0 |  |
| unsure_right_long | unsure | 15/30 | 13 | 15 | 2 | 2 (no answer 2) | 2 |  |
| control | none | 8/24 | 16 | 8 | 0 | 8 (no answer 8) | 8 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 8/24 | 8/24 | 8 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 17/23 | 9/23 | +0.348 | [+0.174, +0.565] | 8 | 0 | 0.0078 | no-log control + four core cells non-missing, n = 23 | +0.250, +0.375 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 11/23 | 10/23 | +0.043 | [+0.000, +0.130] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 23 | -0.062, +0.094 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.391 | [+0.174, +0.652] | 8 | 0 | 0.0078 | no-log control + four core cells non-missing, n = 23 | +0.188, +0.469 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.304 | [+0.130, +0.522] | 7 | 0 | 0.0156 | no-log control + four core cells non-missing, n = 23 | +0.156, +0.438 (N = 32) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 23/30 | 14/30 | +0.300 | [+0.133, +0.467] | 9 | 0 | 0.0039 | four long cells non-missing, n = 30 | +0.250, +0.281 (N = 32) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 15/30 | 14/30 | +0.033 | [+0.000, +0.100] | 1 | 0 | 1.0000 | four long cells non-missing, n = 30 | -0.031, +0.094 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.333 | [+0.167, +0.533] | 9 | 0 | 0.0039 | four long cells non-missing, n = 30 | +0.219, +0.375 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.267 | [+0.133, +0.433] | 8 | 0 | 0.0078 | four long cells non-missing, n = 30 | +0.156, +0.312 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 18/28 | 15/28 | +0.107 | [-0.036, +0.250] | 4 | 1 | 0.3750 | both cells non-missing, n = 28 | +0.031, +0.188 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 26/28 | 22/28 | +0.143 | [+0.000, +0.321] | 5 | 1 | 0.2188 | both cells non-missing, n = 28 | +0.031, +0.156 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 20/30 | 18/30 | +0.067 | [+0.000, +0.167] | 2 | 0 | 0.5000 | both cells non-missing, n = 30 |
| ceiling check: unsure\|all_unsure - unsure\|none | 20/29 | 15/29 | +0.172 | [+0.034, +0.310] | 5 | 0 | 0.0625 | both cells non-missing, n = 29 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 23/29 | 16/29 | +0.241 | [+0.103, +0.414] | 7 | 0 | 0.0156 | both cells non-missing, n = 29 |
| no-log tone gap: certain\|none - unsure\|none | 18/28 | 15/28 | +0.107 | [+0.000, +0.214] | 3 | 0 | 0.2500 | both cells non-missing, n = 28 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 9/15 | 3/15 | +0.400 | [+0.133, +0.667] | 6 | 0 | 0.0312 | no-log control + four core cells non-missing, n = 15 | +0.375, +0.438 (N = 16) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/15 | 2/15 | +0.067 | [+0.000, +0.200] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 15 | +0.062, +0.062 (N = 16) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.467 | [+0.200, +0.800] | 6 | 0 | 0.0312 | no-log control + four core cells non-missing, n = 15 | +0.438, +0.500 (N = 16) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.333 | [+0.133, +0.600] | 5 | 0 | 0.0625 | no-log control + four core cells non-missing, n = 15 | +0.312, +0.375 (N = 16) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 9/16 | 2/16 | +0.438 | [+0.188, +0.688] | 7 | 0 | 0.0156 | four long cells non-missing, n = 16 | +0.438, +0.438 (N = 16) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 2/16 | 1/16 | +0.062 | [+0.000, +0.188] | 1 | 0 | 1.0000 | four long cells non-missing, n = 16 | +0.062, +0.062 (N = 16) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.500 | [+0.250, +0.812] | 7 | 0 | 0.0156 | four long cells non-missing, n = 16 | +0.500, +0.500 (N = 16) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.375 | [+0.125, +0.625] | 6 | 0 | 0.0312 | four long cells non-missing, n = 16 | +0.375, +0.375 (N = 16) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 5/15 | 2/15 | +0.200 | [-0.067, +0.467] | 4 | 1 | 0.3750 | both cells non-missing, n = 15 | +0.125, +0.188 (N = 16) |
| certain\|perfect_mixed - certain\|certain_right | 12/14 | 8/14 | +0.286 | [+0.000, +0.571] | 5 | 1 | 0.2188 | both cells non-missing, n = 14 | +0.125, +0.250 (N = 16) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 6/16 | 4/16 | +0.125 | [+0.000, +0.312] | 2 | 0 | 0.5000 | both cells non-missing, n = 16 |
| ceiling check: unsure\|all_unsure - unsure\|none | 7/16 | 2/16 | +0.312 | [+0.125, +0.562] | 5 | 0 | 0.0625 | both cells non-missing, n = 16 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 10/16 | 3/16 | +0.438 | [+0.188, +0.688] | 7 | 0 | 0.0156 | both cells non-missing, n = 16 |
| no-log tone gap: certain\|none - unsure\|none | 5/15 | 2/15 | +0.200 | [+0.000, +0.400] | 3 | 0 | 0.2500 | both cells non-missing, n = 15 |
