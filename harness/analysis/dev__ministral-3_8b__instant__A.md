# Analysis: dev__ministral-3_8b__instant__A

Inputs: dev__ministral-3_8b__instant__A.jsonl. Rows read: 480. Probe files: -.

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

## ministral-3:8b | answer-only | arm A | stratum wrong | target key

Source files: dev__ministral-3_8b__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 21/32 | 11 | 21 | 0 | 0 | 0 |  |
| none | unsure | 10/32 | 22 | 10 | 0 | 0 | 0 |  |
| all_certain | certain | 23/32 | 8 | 23 | 1 | 0 | 0 |  |
| all_certain | unsure | 7/32 | 25 | 7 | 0 | 0 | 0 |  |
| all_unsure | certain | 27/32 | 4 | 27 | 1 | 0 | 0 |  |
| all_unsure | unsure | 11/32 | 21 | 11 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 22/32 | 9 | 22 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 8/32 | 24 | 8 | 0 | 0 | 0 |  |
| reliable | certain | 19/32 | 13 | 19 | 0 | 0 | 0 |  |
| reliable | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 |  |
| certain_right | certain | 18/32 | 14 | 18 | 0 | 0 | 0 |  |
| certain_right | unsure | 3/32 | 29 | 3 | 0 | 0 | 0 |  |
| unsure_right | certain | 5/32 | 27 | 5 | 0 | 0 | 0 |  |
| unsure_right | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| control | none | 2/32 | 27 | 2 | 3 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 2/32 | 5/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 18/32 | 5/32 | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/32 | 3/32 | -0.062 | [-0.156, +0.000] | 0 | 2 | 0.5000 | no-log control + four core cells non-missing, n = 32 | -0.062, -0.062 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.344 | [+0.125, +0.531] | 13 | 2 | 0.0074 | no-log control + four core cells non-missing, n = 32 | +0.344, +0.344 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.469 | [+0.312, +0.625] | 15 | 0 | 6.10e-05 | no-log control + four core cells non-missing, n = 32 | +0.469, +0.469 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 8/32 | 1/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 | +0.219, +0.219 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 22/32 | 18/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | both cells non-missing, n = 32 | +0.125, +0.125 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 19/32 | 6/32 | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | both cells non-missing, n = 32 |
| ceiling check: unsure\|all_unsure - unsure\|none | 11/32 | 10/32 | +0.031 | [-0.125, +0.188] | 4 | 3 | 1.0000 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 18/32 | 1/32 | +0.531 | [+0.375, +0.688] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 21/32 | 10/32 | +0.344 | [+0.188, +0.500] | 11 | 0 | 0.0010 | both cells non-missing, n = 32 |
