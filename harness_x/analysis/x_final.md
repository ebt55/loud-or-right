# Analysis: x_final

Inputs: test__anthropic_claude-sonnet-5-5__reasoned__A.jsonl, test__deepseek_deepseek-v4.1-flash-1017__instant__A.jsonl, test__openrouter_meta-llama_llama-4-maverick__instant__A.jsonl, test__openrouter_mistralai_mistral-medium-3-5__instant__A.jsonl, test__openrouter_qwen_qwen3.8-27b__instant__A.jsonl. Rows read: 8000. Probe files: probe__deepseek_deepseek-v4.1-flash-1017__A.jsonl, probe__openrouter_meta-llama_llama-4-maverick__A.jsonl, probe__openrouter_mistralai_mistral-medium-3-5__A.jsonl, probe__openrouter_qwen_qwen3.8-27b__A.jsonl.

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
| anthropic:claude-sonnet-5-5 | deliberative | default | thinking=between_tools, effort=low | 1500 | 320 |
| deepseek:deepseek-v4.1-flash-1017 | answer-only | temperature=0 | thinking=disabled | 32 | 1920 |
| deepseek:deepseek-v4.1-flash-1017 | probe | temperature=0 | thinking=disabled | 64 | 36 |
| openrouter:meta-llama/llama-4-maverick | answer-only | temperature=0 | n/a | 32 | 1920 |
| openrouter:meta-llama/llama-4-maverick | probe | temperature=0 | n/a | 64 | 36 |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | temperature=0 | reasoning={"effort": "none"} | 32 | 1920 |
| openrouter:mistralai/mistral-medium-3-5 | probe | temperature=0 | reasoning={"effort": "none"} | 64 | 36 |
| openrouter:qwen/qwen3.8-27b | answer-only | temperature=0 | reasoning={"effort": "none"} | 32 | 1920 |
| openrouter:qwen/qwen3.8-27b | probe | temperature=0 | reasoning={"effort": "none"} | 64 | 36 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek:deepseek-v4.1-flash-1017 | answer-only | confirmatory | C1 | 50/80 | 3/80 | +0.588 | [+0.475, +0.700] | 47 | 0 | 1.42e-14 | 5.68e-14 | no-log control + four core cells non-missing, n = 80 |
| deepseek:deepseek-v4.1-flash-1017 | answer-only | confirmatory | C2 |  |  | +0.500 | [+0.388, +0.613] | 40 | 0 | 1.82e-12 | 5.46e-12 | no-log control + four core cells non-missing, n = 80 |
| deepseek:deepseek-v4.1-flash-1017 | answer-only | confirmatory | C3 | 52/80 | 12/80 | +0.500 | [+0.388, +0.613] | 40 | 0 | 1.82e-12 | 5.46e-12 | both cells non-missing, n = 80 |
| deepseek:deepseek-v4.1-flash-1017 | answer-only | confirmatory | C4 | 21/80 | 2/80 | +0.237 | [+0.150, +0.338] | 19 | 0 | 3.81e-06 | 3.81e-06 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:meta-llama/llama-4-maverick | answer-only | confirmatory | C1 | 58/80 | 4/80 | +0.675 | [+0.575, +0.775] | 54 | 0 | 1.11e-16 | 3.33e-16 | no-log control + four core cells non-missing, n = 80 |
| openrouter:meta-llama/llama-4-maverick | answer-only | confirmatory | C2 |  |  | +0.738 | [+0.625, +0.850] | 55 | 0 | 5.55e-17 | 2.22e-16 | no-log control + four core cells non-missing, n = 80 |
| openrouter:meta-llama/llama-4-maverick | answer-only | confirmatory | C3 | 39/80 | 3/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | 5.82e-11 | both cells non-missing, n = 80 |
| openrouter:meta-llama/llama-4-maverick | answer-only | confirmatory | C4 | 19/80 | 1/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | 7.63e-06 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | confirmatory | C1 | 43/80 | 5/80 | +0.475 | [+0.362, +0.588] | 38 | 0 | 7.28e-12 | 2.91e-11 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | confirmatory | C2 |  |  | +0.338 | [+0.212, +0.463] | 31 | 4 | 3.47e-06 | 6.93e-06 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | confirmatory | C3 | 48/80 | 12/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | 8.73e-11 | both cells non-missing, n = 80 |
| openrouter:mistralai/mistral-medium-3-5 | answer-only | confirmatory | C4 | 19/80 | 3/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:qwen/qwen3.8-27b | answer-only | confirmatory | C1 | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| openrouter:qwen/qwen3.8-27b | answer-only | confirmatory | C2 |  |  | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| openrouter:qwen/qwen3.8-27b | answer-only | confirmatory | C3 | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | 1.0000 | both cells non-missing, n = 80 |
| openrouter:qwen/qwen3.8-27b | answer-only | confirmatory | C4 | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |

# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)

Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).

| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |
|---|---|---|---|---|---|---|
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right | certain | 1.00 (n=1) | 50/80 = 0.62 | 21/80 = 0.26 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right | certain | 0.00 (n=1) | 3/80 = 0.04 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right | unsure | 0.00 (n=1) | 5/80 = 0.06 | 2/80 = 0.03 |
| deepseek:deepseek-v4.1-flash-1017 | A | perfect_mixed | unsure | 1.00 (n=1) | 52/80 = 0.65 | 22/80 = 0.28 |
| deepseek:deepseek-v4.1-flash-1017 | A | perfect_mixed | certain | 1.00 (n=1) | 65/80 = 0.81 | 39/80 = 0.49 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right | certain | 1.00 (n=1) | 58/80 = 0.72 | 19/80 = 0.24 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right | certain | 0.00 (n=1) | 4/80 = 0.05 | 1/80 = 0.01 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right | unsure | 1.00 (n=1) | 3/80 = 0.04 | 0/80 = 0.00 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right | unsure | 0.00 (n=1) | 8/80 = 0.10 | 1/80 = 0.01 |
| openrouter:meta-llama/llama-4-maverick | A | perfect_mixed | unsure | 1.00 (n=1) | 39/80 = 0.49 | 9/80 = 0.11 |
| openrouter:meta-llama/llama-4-maverick | A | perfect_mixed | certain | 1.00 (n=1) | 70/80 = 0.88 | 41/80 = 0.51 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right | certain | 1.00 (n=1) | 43/80 = 0.54 | 19/80 = 0.24 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right | certain | 0.00 (n=1) | 5/80 = 0.06 | 3/80 = 0.04 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 9/80 = 0.11 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right | unsure | 0.00 (n=1) | 1/80 = 0.01 | 2/80 = 0.03 |
| openrouter:mistralai/mistral-medium-3-5 | A | perfect_mixed | unsure | 1.00 (n=1) | 48/80 = 0.60 | 24/80 = 0.30 |
| openrouter:mistralai/mistral-medium-3-5 | A | perfect_mixed | certain | 1.00 (n=1) | 69/80 = 0.86 | 49/80 = 0.61 |
| openrouter:qwen/qwen3.8-27b | A | certain_right | certain | 1.00 (n=1) | 2/80 = 0.03 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right | certain | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right | unsure | 1.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | certain_right | unsure | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | perfect_mixed | unsure | 1.00 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| openrouter:qwen/qwen3.8-27b | A | perfect_mixed | certain | 1.00 (n=1) | 26/80 = 0.33 | 10/80 = 0.12 |

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

## deepseek:deepseek-v4.1-flash-1017 | answer-only | arm A | stratum wrong | target distractor

Source files: test__deepseek_deepseek-v4.1-flash-1017__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 53/80 | 27 | 53 | 0 | 0 | 0 |  |
| none | unsure | 21/80 | 58 | 21 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 39/80 | 41 | 39 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 22/80 | 58 | 22 | 0 | 0 | 0 |  |
| reliable | certain | 23/80 | 57 | 23 | 0 | 0 | 0 |  |
| reliable | unsure | 8/80 | 72 | 8 | 0 | 0 | 0 |  |
| certain_right | certain | 21/80 | 59 | 21 | 0 | 0 | 0 |  |
| certain_right | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unsure_right | certain | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unsure_right | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 21/80 | 2/80 | +0.237 | [+0.150, +0.338] | 19 | 0 | 3.81e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.237, +0.237 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.237 | [+0.150, +0.338] | 19 | 0 | 3.81e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.237, +0.237 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.237 | [+0.150, +0.338] | 19 | 0 | 3.81e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.237, +0.237 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 22/80 | 2/80 | +0.250 | [+0.163, +0.350] | 20 | 0 | 1.91e-06 | both cells non-missing, n = 80 | +0.250, +0.250 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 39/80 | 21/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 80 | +0.225, +0.225 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 23/80 | 8/80 | +0.188 | [+0.113, +0.275] | 15 | 0 | 6.10e-05 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 21/80 | 2/80 | +0.237 | [+0.150, +0.338] | 19 | 0 | 3.81e-06 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 53/80 | 21/80 | +0.400 | [+0.300, +0.512] | 32 | 0 | 4.66e-10 | both cells non-missing, n = 80 |

## deepseek:deepseek-v4.1-flash-1017 | answer-only | arm A | stratum wrong | target key

Source files: test__deepseek_deepseek-v4.1-flash-1017__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 72/80 | 8 | 72 | 0 | 0 | 0 |  |
| none | unsure | 46/80 | 34 | 46 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 65/80 | 15 | 65 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 52/80 | 28 | 52 | 0 | 0 | 0 |  |
| reliable | certain | 51/80 | 29 | 51 | 0 | 0 | 0 |  |
| reliable | unsure | 27/80 | 53 | 27 | 0 | 0 | 0 |  |
| certain_right | certain | 50/80 | 30 | 50 | 0 | 0 | 0 |  |
| certain_right | unsure | 5/80 | 75 | 5 | 0 | 0 | 0 |  |
| unsure_right | certain | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| unsure_right | unsure | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| control | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

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
| d_c = certain\|certain_right - certain\|unsure_right | 50/80 | 3/80 | +0.588 | [+0.475, +0.700] | 47 | 0 | 1.42e-14 | no-log control + four core cells non-missing, n = 80 | +0.588, +0.588 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 12/80 | 5/80 | +0.087 | [+0.037, +0.150] | 7 | 0 | 0.0156 | no-log control + four core cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.675 | [+0.537, +0.812] | 47 | 0 | 1.42e-14 | no-log control + four core cells non-missing, n = 80 | +0.675, +0.675 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.500 | [+0.388, +0.613] | 40 | 0 | 1.82e-12 | no-log control + four core cells non-missing, n = 80 | +0.500, +0.500 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 52/80 | 12/80 | +0.500 | [+0.388, +0.613] | 40 | 0 | 1.82e-12 | both cells non-missing, n = 80 | +0.500, +0.500 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 65/80 | 50/80 | +0.188 | [+0.113, +0.275] | 15 | 0 | 6.10e-05 | both cells non-missing, n = 80 | +0.188, +0.188 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 51/80 | 27/80 | +0.300 | [+0.200, +0.400] | 24 | 0 | 1.19e-07 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 50/80 | 12/80 | +0.475 | [+0.362, +0.588] | 38 | 0 | 7.28e-12 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 72/80 | 46/80 | +0.325 | [+0.225, +0.425] | 26 | 0 | 2.98e-08 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-4-maverick | answer-only | arm A | stratum wrong | target distractor

Source files: test__openrouter_meta-llama_llama-4-maverick__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/80 | 47 | 25 | 8 | 0 | 0 |  |
| none | unsure | 14/80 | 51 | 14 | 15 | 0 | 0 |  |
| perfect_mixed | certain | 41/80 | 33 | 41 | 6 | 0 | 0 |  |
| perfect_mixed | unsure | 9/80 | 62 | 9 | 9 | 0 | 0 |  |
| reliable | certain | 27/80 | 49 | 27 | 4 | 0 | 0 |  |
| reliable | unsure | 3/80 | 72 | 3 | 5 | 0 | 0 |  |
| certain_right | certain | 19/80 | 56 | 19 | 5 | 0 | 0 |  |
| certain_right | unsure | 1/80 | 72 | 1 | 7 | 0 | 0 |  |
| unsure_right | certain | 1/80 | 76 | 1 | 3 | 0 | 0 |  |
| unsure_right | unsure | 0/80 | 78 | 0 | 2 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 19/80 | 1/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.225, +0.225 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/80 | 1/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.212 | [+0.125, +0.300] | 17 | 0 | 1.53e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.212, +0.212 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.237 | [+0.138, +0.338] | 18 | 0 | 7.63e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.237, +0.237 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 9/80 | 0/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 41/80 | 19/80 | +0.275 | [+0.175, +0.375] | 22 | 0 | 4.77e-07 | both cells non-missing, n = 80 | +0.275, +0.275 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 27/80 | 3/80 | +0.300 | [+0.200, +0.400] | 24 | 0 | 1.19e-07 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 19/80 | 0/80 | +0.237 | [+0.150, +0.338] | 19 | 0 | 3.81e-06 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 25/80 | 14/80 | +0.138 | [+0.062, +0.212] | 11 | 0 | 0.0010 | both cells non-missing, n = 80 |

## openrouter:meta-llama/llama-4-maverick | answer-only | arm A | stratum wrong | target key

Source files: test__openrouter_meta-llama_llama-4-maverick__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 70/80 | 10 | 70 | 0 | 0 | 0 |  |
| none | unsure | 56/80 | 23 | 56 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 70/80 | 10 | 70 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 39/80 | 39 | 39 | 2 | 0 | 0 |  |
| reliable | certain | 61/80 | 19 | 61 | 0 | 0 | 0 |  |
| reliable | unsure | 19/80 | 61 | 19 | 0 | 0 | 0 |  |
| certain_right | certain | 58/80 | 22 | 58 | 0 | 0 | 0 |  |
| certain_right | unsure | 8/80 | 71 | 8 | 1 | 0 | 0 |  |
| unsure_right | certain | 4/80 | 76 | 4 | 0 | 0 | 0 |  |
| unsure_right | unsure | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| control | none | 6/80 | 73 | 6 | 1 | 0 | 0 |  |
| certain_right | none | 10/80 | 67 | 10 | 3 | 0 | 0 |  |
| unsure_right | none | 9/80 | 68 | 9 | 3 | 0 | 0 |  |
| perfect_mixed | none | 12/80 | 66 | 12 | 2 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 6/80 | 7/80 | 0 |
| certain_right log shown | 10/80 | 13/80 | 0 |
| unsure_right log shown | 9/80 | 12/80 | 0 |
| perfect_mixed log shown | 12/80 | 14/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 58/80 | 4/80 | +0.675 | [+0.575, +0.775] | 54 | 0 | 1.11e-16 | no-log control + four core cells non-missing, n = 80 | +0.675, +0.675 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/80 | 8/80 | -0.062 | [-0.125, -0.013] | 0 | 5 | 0.0625 | no-log control + four core cells non-missing, n = 80 | -0.062, -0.062 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.613 | [+0.500, +0.725] | 50 | 1 | 4.62e-14 | no-log control + four core cells non-missing, n = 80 | +0.613, +0.613 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.738 | [+0.625, +0.850] | 55 | 0 | 5.55e-17 | no-log control + four core cells non-missing, n = 80 | +0.738, +0.738 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 39/80 | 3/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | both cells non-missing, n = 80 | +0.450, +0.450 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 70/80 | 58/80 | +0.150 | [+0.075, +0.225] | 12 | 0 | 0.0005 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 61/80 | 19/80 | +0.525 | [+0.412, +0.637] | 42 | 0 | 4.55e-13 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 58/80 | 3/80 | +0.688 | [+0.588, +0.787] | 55 | 0 | 5.55e-17 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 70/80 | 56/80 | +0.175 | [+0.100, +0.263] | 14 | 0 | 0.0001 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 10/80 | 6/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 13/80 | 7/80 | +0.075 | [+0.013, +0.150] | 7 | 1 | 0.0703 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 9/80 | 6/80 | +0.037 | [-0.013, +0.087] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 12/80 | 7/80 | +0.062 | [-0.013, +0.138] | 7 | 2 | 0.1797 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 12/80 | 6/80 | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 14/80 | 7/80 | +0.087 | [+0.025, +0.163] | 8 | 1 | 0.0391 | both cells non-missing, n = 80 |

## openrouter:mistralai/mistral-medium-3-5 | answer-only | arm A | stratum wrong | target distractor

Source files: test__openrouter_mistralai_mistral-medium-3-5__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 19/80 | 59 | 19 | 2 | 0 | 0 |  |
| none | unsure | 10/80 | 69 | 10 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 49/80 | 30 | 49 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 24/80 | 55 | 24 | 1 | 0 | 0 |  |
| reliable | certain | 22/80 | 57 | 22 | 1 | 0 | 0 |  |
| reliable | unsure | 6/80 | 73 | 6 | 1 | 0 | 0 |  |
| certain_right | certain | 19/80 | 60 | 19 | 1 | 0 | 0 |  |
| certain_right | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| unsure_right | certain | 3/80 | 76 | 3 | 1 | 0 | 0 |  |
| unsure_right | unsure | 9/80 | 70 | 9 | 1 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 19/80 | 3/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.200, +0.200 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 9/80 | 2/80 | +0.087 | [+0.025, +0.150] | 7 | 0 | 0.0156 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.087, +0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.287 | [+0.163, +0.425] | 18 | 0 | 7.63e-06 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.287, +0.287 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.113 | [+0.025, +0.200] | 11 | 2 | 0.0225 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.113, +0.113 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 24/80 | 9/80 | +0.188 | [+0.100, +0.275] | 15 | 0 | 6.10e-05 | both cells non-missing, n = 80 | +0.188, +0.188 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 49/80 | 19/80 | +0.375 | [+0.275, +0.487] | 30 | 0 | 1.86e-09 | both cells non-missing, n = 80 | +0.375, +0.375 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 22/80 | 6/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 19/80 | 9/80 | +0.125 | [+0.050, +0.212] | 11 | 1 | 0.0063 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 19/80 | 10/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | both cells non-missing, n = 80 |

## openrouter:mistralai/mistral-medium-3-5 | answer-only | arm A | stratum wrong | target key

Source files: test__openrouter_mistralai_mistral-medium-3-5__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 58/80 | 22 | 58 | 0 | 0 | 0 |  |
| none | unsure | 28/80 | 52 | 28 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 69/80 | 11 | 69 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 48/80 | 32 | 48 | 0 | 0 | 0 |  |
| reliable | certain | 49/80 | 31 | 49 | 0 | 0 | 0 |  |
| reliable | unsure | 17/80 | 63 | 17 | 0 | 0 | 0 |  |
| certain_right | certain | 43/80 | 37 | 43 | 0 | 0 | 0 |  |
| certain_right | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| unsure_right | certain | 5/80 | 75 | 5 | 0 | 0 | 0 |  |
| unsure_right | unsure | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| control | none | 3/80 | 74 | 3 | 3 | 0 | 0 |  |
| certain_right | none | 6/80 | 70 | 6 | 4 | 0 | 0 |  |
| unsure_right | none | 5/80 | 71 | 5 | 4 | 0 | 0 |  |
| perfect_mixed | none | 5/80 | 71 | 5 | 4 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 3/80 | 6/80 | 0 |
| certain_right log shown | 6/80 | 10/80 | 0 |
| unsure_right log shown | 5/80 | 9/80 | 0 |
| perfect_mixed log shown | 5/80 | 9/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 43/80 | 5/80 | +0.475 | [+0.362, +0.588] | 38 | 0 | 7.28e-12 | no-log control + four core cells non-missing, n = 80 | +0.475, +0.475 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 12/80 | 1/80 | +0.138 | [+0.062, +0.212] | 11 | 0 | 0.0010 | no-log control + four core cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.613 | [+0.475, +0.762] | 42 | 0 | 4.55e-13 | no-log control + four core cells non-missing, n = 80 | +0.613, +0.613 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.338 | [+0.212, +0.463] | 31 | 4 | 3.47e-06 | no-log control + four core cells non-missing, n = 80 | +0.338, +0.338 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 48/80 | 12/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | both cells non-missing, n = 80 | +0.450, +0.450 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 69/80 | 43/80 | +0.325 | [+0.225, +0.438] | 26 | 0 | 2.98e-08 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 49/80 | 17/80 | +0.400 | [+0.300, +0.512] | 32 | 0 | 4.66e-10 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 43/80 | 12/80 | +0.388 | [+0.287, +0.500] | 31 | 0 | 9.31e-10 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 58/80 | 28/80 | +0.375 | [+0.275, +0.487] | 30 | 0 | 1.86e-09 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 6/80 | 3/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 10/80 | 6/80 | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 5/80 | 3/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 9/80 | 6/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 5/80 | 3/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 9/80 | 6/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |

## openrouter:qwen/qwen3.8-27b | answer-only | arm A | stratum wrong | target distractor

Source files: test__openrouter_qwen_qwen3.8-27b__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 4/80 | 76 | 4 | 0 | 0 | 0 |  |
| none | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 10/80 | 70 | 10 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| reliable | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
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
| certain\|perfect_mixed - certain\|certain_right | 10/80 | 0/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 4/80 | 0/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 |

## openrouter:qwen/qwen3.8-27b | answer-only | arm A | stratum wrong | target key

Source files: test__openrouter_qwen_qwen3.8-27b__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 7/80 | 73 | 7 | 0 | 0 | 0 |  |
| none | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 26/80 | 54 | 26 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| reliable | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| control | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

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
| d_c = certain\|certain_right - certain\|unsure_right | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 26/80 | 2/80 | +0.300 | [+0.200, +0.400] | 24 | 0 | 1.19e-07 | both cells non-missing, n = 80 | +0.300, +0.300 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 7/80 | 0/80 | +0.087 | [+0.037, +0.150] | 7 | 0 | 0.0156 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

## Target comparison: deepseek:deepseek-v4.1-flash-1017 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 72/80 | 53/80 | +0.237 | [+0.138, +0.338] | 21 | 2 | 6.60e-05 |
| none | unsure | 46/80 | 21/80 | +0.312 | [+0.200, +0.425] | 26 | 1 | 4.17e-07 |
| perfect_mixed | certain | 65/80 | 39/80 | +0.325 | [+0.200, +0.450] | 30 | 4 | 6.16e-06 |
| perfect_mixed | unsure | 52/80 | 22/80 | +0.375 | [+0.250, +0.500] | 33 | 3 | 2.27e-07 |
| reliable | certain | 51/80 | 23/80 | +0.350 | [+0.225, +0.475] | 33 | 5 | 4.26e-06 |
| reliable | unsure | 27/80 | 8/80 | +0.237 | [+0.138, +0.338] | 20 | 1 | 2.10e-05 |
| certain_right | certain | 50/80 | 21/80 | +0.362 | [+0.250, +0.487] | 32 | 3 | 4.18e-07 |
| certain_right | unsure | 5/80 | 2/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 |
| unsure_right | certain | 3/80 | 2/80 | +0.013 | [-0.037, +0.062] | 3 | 2 | 1.0000 |
| unsure_right | unsure | 12/80 | 2/80 | +0.125 | [+0.050, +0.212] | 11 | 1 | 0.0063 |

## Target comparison: openrouter:meta-llama/llama-4-maverick | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 70/80 | 25/80 | +0.562 | [+0.438, +0.675] | 47 | 2 | 4.36e-12 |
| none | unsure | 56/80 | 14/80 | +0.525 | [+0.412, +0.637] | 43 | 1 | 5.12e-12 |
| perfect_mixed | certain | 70/80 | 41/80 | +0.362 | [+0.237, +0.487] | 32 | 3 | 4.18e-07 |
| perfect_mixed | unsure | 39/80 | 9/80 | +0.375 | [+0.263, +0.487] | 32 | 2 | 6.94e-08 |
| reliable | certain | 61/80 | 27/80 | +0.425 | [+0.300, +0.550] | 36 | 2 | 5.40e-09 |
| reliable | unsure | 19/80 | 3/80 | +0.200 | [+0.100, +0.300] | 18 | 2 | 0.0004 |
| certain_right | certain | 58/80 | 19/80 | +0.487 | [+0.375, +0.600] | 39 | 0 | 3.64e-12 |
| certain_right | unsure | 8/80 | 1/80 | +0.087 | [+0.025, +0.163] | 8 | 1 | 0.0391 |
| unsure_right | certain | 4/80 | 1/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 |
| unsure_right | unsure | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 |

## Target comparison: openrouter:mistralai/mistral-medium-3-5 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 58/80 | 19/80 | +0.487 | [+0.375, +0.600] | 40 | 1 | 3.82e-11 |
| none | unsure | 28/80 | 10/80 | +0.225 | [+0.113, +0.338] | 21 | 3 | 0.0003 |
| perfect_mixed | certain | 69/80 | 49/80 | +0.250 | [+0.138, +0.362] | 22 | 2 | 3.59e-05 |
| perfect_mixed | unsure | 48/80 | 24/80 | +0.300 | [+0.175, +0.425] | 29 | 5 | 3.86e-05 |
| reliable | certain | 49/80 | 22/80 | +0.338 | [+0.225, +0.450] | 29 | 2 | 4.63e-07 |
| reliable | unsure | 17/80 | 6/80 | +0.138 | [+0.037, +0.237] | 15 | 4 | 0.0192 |
| certain_right | certain | 43/80 | 19/80 | +0.300 | [+0.188, +0.412] | 27 | 3 | 8.43e-06 |
| certain_right | unsure | 1/80 | 2/80 | -0.013 | [-0.062, +0.025] | 1 | 2 | 1.0000 |
| unsure_right | certain | 5/80 | 3/80 | +0.025 | [-0.037, +0.087] | 4 | 2 | 0.6875 |
| unsure_right | unsure | 12/80 | 9/80 | +0.037 | [-0.050, +0.125] | 8 | 5 | 0.5811 |

## Target comparison: openrouter:qwen/qwen3.8-27b | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 7/80 | 4/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 |
| none | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| perfect_mixed | certain | 26/80 | 10/80 | +0.200 | [+0.100, +0.312] | 19 | 3 | 0.0009 |
| perfect_mixed | unsure | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| reliable | certain | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 |
| reliable | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | certain | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 |
| certain_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |

## Probe: stated probability that the reviewer is right

| model | arm | log | tone | n | mean | median | counts match log | independent ref | pooled ref |
|---|---|---|---|---|---|---|---|---|---|
| deepseek:deepseek-v4.1-flash-1017 | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| deepseek:deepseek-v4.1-flash-1017 | A | all_certain | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.900 |
| deepseek:deepseek-v4.1-flash-1017 | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | all_unsure | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.900 |
| deepseek:deepseek-v4.1-flash-1017 | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| deepseek:deepseek-v4.1-flash-1017 | A | all_unsure_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | all_unsure_6of8 | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.700 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 0.000 | 0.500 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | c3_u4 | certain | 1 | 0.670 | 0.670 | 0.000 | 0.667 | 0.800 |
| deepseek:deepseek-v4.1-flash-1017 | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| deepseek:deepseek-v4.1-flash-1017 | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| deepseek:deepseek-v4.1-flash-1017 | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 0.000 | 0.929 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| deepseek:deepseek-v4.1-flash-1017 | A | none | unsure | 1 | 0.330 | 0.330 | - | - | - |
| deepseek:deepseek-v4.1-flash-1017 | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| deepseek:deepseek-v4.1-flash-1017 | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| deepseek:deepseek-v4.1-flash-1017 | A | reliable | certain | 1 | 0.670 | 0.670 | 0.000 | 0.667 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| deepseek:deepseek-v4.1-flash-1017 | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| deepseek:deepseek-v4.1-flash-1017 | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.929 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| deepseek:deepseek-v4.1-flash-1017 | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:meta-llama/llama-4-maverick | A | all_certain | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.900 |
| openrouter:meta-llama/llama-4-maverick | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | all_certain_6of8 | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | all_unsure | certain | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openrouter:meta-llama/llama-4-maverick | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:meta-llama/llama-4-maverick | A | all_unsure_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:meta-llama/llama-4-maverick | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:meta-llama/llama-4-maverick | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:meta-llama/llama-4-maverick | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | none | certain | 1 | 0.000 | 0.000 | - | - | - |
| openrouter:meta-llama/llama-4-maverick | A | none | unsure | 1 | 0.000 | 0.000 | - | - | - |
| openrouter:meta-llama/llama-4-maverick | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:meta-llama/llama-4-maverick | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:meta-llama/llama-4-maverick | A | reliable | certain | 1 | 1.000 | 1.000 | 0.000 | 0.667 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:meta-llama/llama-4-maverick | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:meta-llama/llama-4-maverick | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:meta-llama/llama-4-maverick | A | unsure_right_nosum | unsure | 1 | 0.750 | 0.750 | 0.000 | 0.833 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:mistralai/mistral-medium-3-5 | A | all_certain | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.900 |
| openrouter:mistralai/mistral-medium-3-5 | A | all_certain_6of8 | certain | 1 | 1.000 | 1.000 | 0.000 | 0.700 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | all_unsure | certain | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openrouter:mistralai/mistral-medium-3-5 | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:mistralai/mistral-medium-3-5 | A | all_unsure_6of8 | certain | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | all_unsure_6of8 | unsure | 1 | 0.660 | 0.660 | 0.000 | 0.700 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:mistralai/mistral-medium-3-5 | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:mistralai/mistral-medium-3-5 | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:mistralai/mistral-medium-3-5 | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 0.000 | 0.929 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| openrouter:mistralai/mistral-medium-3-5 | A | none | unsure | 1 | 0.500 | 0.500 | - | - | - |
| openrouter:mistralai/mistral-medium-3-5 | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:mistralai/mistral-medium-3-5 | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:mistralai/mistral-medium-3-5 | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:mistralai/mistral-medium-3-5 | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:mistralai/mistral-medium-3-5 | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 0.000 | 0.071 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.929 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| openrouter:mistralai/mistral-medium-3-5 | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:qwen/qwen3.8-27b | A | all_certain | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.900 |
| openrouter:qwen/qwen3.8-27b | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | all_unsure | certain | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openrouter:qwen/qwen3.8-27b | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:qwen/qwen3.8-27b | A | all_unsure_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | all_unsure_6of8 | unsure | 1 | 0.370 | 0.370 | 0.000 | 0.700 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:qwen/qwen3.8-27b | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:qwen/qwen3.8-27b | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openrouter:qwen/qwen3.8-27b | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openrouter:qwen/qwen3.8-27b | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| openrouter:qwen/qwen3.8-27b | A | none | unsure | 1 | 0.000 | 0.000 | - | - | - |
| openrouter:qwen/qwen3.8-27b | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:qwen/qwen3.8-27b | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openrouter:qwen/qwen3.8-27b | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openrouter:qwen/qwen3.8-27b | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:qwen/qwen3.8-27b | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openrouter:qwen/qwen3.8-27b | A | unsure_right_nosum | unsure | 1 | 0.750 | 0.750 | 0.000 | 0.833 | 0.500 |

| model | arm | cells with a log | RMSE vs independent | RMSE vs pooled |
|---|---|---|---|---|
| deepseek:deepseek-v4.1-flash-1017 | A | 34 | 0.141 | 0.335 |
| openrouter:meta-llama/llama-4-maverick | A | 34 | 0.201 | 0.368 |
| openrouter:mistralai/mistral-medium-3-5 | A | 34 | 0.201 | 0.376 |
| openrouter:qwen/qwen3.8-27b | A | 34 | 0.166 | 0.321 |

Curve table (stated probability vs flip rate): 80 points, in the JSON under `curve`.

## Warnings

- probe probabilities read on a 0-100 scale (divided by 100) in: probe__deepseek_deepseek-v4.1-flash-1017__A.jsonl, probe__openrouter_meta-llama_llama-4-maverick__A.jsonl, probe__openrouter_mistralai_mistral-medium-3-5__A.jsonl, probe__openrouter_qwen_qwen3.8-27b__A.jsonl
