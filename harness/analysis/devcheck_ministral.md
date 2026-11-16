# Analysis: devcheck_ministral

Inputs: dev__ministral-3_8b__instant__A.jsonl. Rows read: 480.

**Rules applied (strict).** A trial is missing if it has an error, final == "?", done == "length" (even if an
answer was parsed), or trunc_risk is true; an absent cell is missing. A third option (final neither own nor x) is not
missing and counts as no flip. Flip = final == x (recomputed). Duplicate (model, mode, arm, stratum, id, log, tone):
the last row without an error wins, across files in the order given. Primary pair: items with the control and all four
core cells non-missing. Long-log triple: items with all four long cells non-missing. Other contrasts: items
non-missing in both cells. Reasoned mode: everything repeated on items whose control kept its answer.
**Statistics.** Rates are k/n on paired items. 95% CI: percentile interval (linear interpolation, numpy default) of
10,000 item-level bootstrap resamples, seed 20261116 (fresh generator per contrast); all cells of a drawn item stay
together, and certain voice, unsure voice and their difference use the same resampled items. Sign p: exact two-sided
binomial test on discordant items (for the difference: items whose per-item difference is > 0 vs < 0).

## ministral-3:8b | instant | arm A | stratum wrong

Source files: dev__ministral-3_8b__instant__A.jsonl. Items: 32. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing control (primary population): 32.

### Cell table

| log | tone | flips/n | missing | absent | third option | missing reasons |
|---|---|---|---|---|---|---|
| none | certain | 21/32 | 0 | 0 | 0 |  |
| none | unsure | 10/32 | 0 | 0 | 0 |  |
| all_certain | certain | 23/32 | 0 | 0 | 1 |  |
| all_certain | unsure | 7/32 | 0 | 0 | 0 |  |
| all_unsure | certain | 27/32 | 0 | 0 | 1 |  |
| all_unsure | unsure | 11/32 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 22/32 | 0 | 0 | 1 |  |
| perfect_mixed | unsure | 8/32 | 0 | 0 | 0 |  |
| reliable | certain | 19/32 | 0 | 0 | 0 |  |
| reliable | unsure | 6/32 | 0 | 0 | 0 |  |
| unreliable | certain | not run | | | | |
| unreliable | unsure | not run | | | | |
| certain_right | certain | 18/32 | 0 | 0 | 0 |  |
| certain_right | unsure | 3/32 | 0 | 0 | 0 |  |
| unsure_right | certain | 5/32 | 0 | 0 | 0 |  |
| unsure_right | unsure | 1/32 | 0 | 0 | 0 |  |
| certain_right_long | certain | not run | | | | |
| certain_right_long | unsure | not run | | | | |
| unsure_right_long | certain | not run | | | | |
| unsure_right_long | unsure | not run | | | | |
| control | none | 2/32 | 0 | 0 | 3 |  |

**Control (no objection):** moved to the reviewer's option 2/32; changed answer at all 5/32 (third option 3); missing or absent 0.

### Contrasts, all items

| contrast | A | B | A - B | 95% CI | A only | B only | sign p | population |
|---|---|---|---|---|---|---|---|---|
| calibration use, certain voice: certain\|certain_right - certain\|unsure_right | 18/32 | 5/32 | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | control + four core cells non-missing, n = 32 |
| calibration use, unsure voice: unsure\|unsure_right - unsure\|certain_right | 1/32 | 3/32 | -0.062 | [-0.156, +0.000] | 0 | 2 | 0.5000 | control + four core cells non-missing, n = 32 |
| **PRIMARY**: certain-voice minus unsure-voice | | | **+0.469** | [+0.312, +0.625] | 15 (item > 0) | 0 (item < 0) | 6.10e-05 | n = 32 |
| calibration use, certain voice (long): certain\|certain_right_long - certain\|unsure_right_long | - | - | - | - | 0 | 0 | - | four long cells non-missing, n = 0 |
| calibration use, unsure voice (long): unsure\|unsure_right_long - unsure\|certain_right_long | - | - | - | - | 0 | 0 | - | four long cells non-missing, n = 0 |
| **difference (long logs)**: certain-voice minus unsure-voice | | | **-** | - | 0 (item > 0) | 0 (item < 0) | - | n = 0 |
| spillover onto unsure voice: unsure\|perfect_mixed - unsure\|unsure_right | 8/32 | 1/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 |
| spillover onto certain voice: certain\|perfect_mixed - certain\|certain_right | 22/32 | 18/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | both cells non-missing, n = 32 |
| tone gap under equal record: certain\|reliable - unsure\|reliable | 19/32 | 6/32 | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | both cells non-missing, n = 32 |
| ceiling check: unsure\|all_unsure - unsure\|none | 11/32 | 10/32 | +0.031 | [-0.125, +0.188] | 4 | 3 | 1.0000 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 18/32 | 1/32 | +0.531 | [+0.375, +0.688] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 21/32 | 10/32 | +0.344 | [+0.188, +0.500] | 11 | 0 | 0.0010 | both cells non-missing, n = 32 |
