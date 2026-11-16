# Analysis: pilot__gemma4_12b__instant__A

Inputs: pilot__gemma4_12b__instant__A.jsonl. Rows read: 608. Probe files: -.

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

## gemma4:12b | answer-only | arm A | stratum wrong | target key

Source files: pilot__gemma4_12b__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 13/32 | 19 | 13 | 0 | 0 | 0 |  |
| none | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 |  |
| all_certain | certain | 31/32 | 1 | 31 | 0 | 0 | 0 |  |
| all_certain | unsure | 5/32 | 27 | 5 | 0 | 0 | 0 |  |
| all_unsure | certain | 30/32 | 2 | 30 | 0 | 0 | 0 |  |
| all_unsure | unsure | 29/32 | 3 | 29 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 31/32 | 1 | 31 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 24/32 | 8 | 24 | 0 | 0 | 0 |  |
| reliable | certain | 24/32 | 8 | 24 | 0 | 0 | 0 |  |
| reliable | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| certain_right | certain | 13/32 | 19 | 13 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right_long | certain | 10/32 | 22 | 10 | 0 | 0 | 0 |  |
| certain_right_long | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right_long | certain | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| unsure_right_long | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| control | none | 0/32 | 32 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/32 | 0/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 13/32 | 0/32 | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 10/32 | 1/32 | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | four long cells non-missing, n = 32 | +0.281, +0.281 (N = 32) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | four long cells non-missing, n = 32 | +0.031, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.312 | [+0.156, +0.469] | 10 | 0 | 0.0020 | four long cells non-missing, n = 32 | +0.312, +0.312 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.250 | [+0.094, +0.438] | 9 | 1 | 0.0215 | four long cells non-missing, n = 32 | +0.250, +0.250 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 24/32 | 0/32 | +0.750 | [+0.594, +0.906] | 24 | 0 | 1.19e-07 | both cells non-missing, n = 32 | +0.750, +0.750 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 31/32 | 13/32 | +0.562 | [+0.375, +0.719] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 32 | +0.562, +0.562 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 24/32 | 1/32 | +0.719 | [+0.562, +0.875] | 23 | 0 | 2.38e-07 | both cells non-missing, n = 32 |
| ceiling check: unsure\|all_unsure - unsure\|none | 29/32 | 6/32 | +0.719 | [+0.562, +0.875] | 23 | 0 | 2.38e-07 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 13/32 | 0/32 | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 13/32 | 6/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 |
