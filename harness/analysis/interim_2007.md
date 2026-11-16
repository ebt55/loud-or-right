# Analysis: interim_2007

Inputs: test__anthropic_claude-haiku-5-5__instant__A.jsonl, test__google_gemini-3.6-flash__instant__A.jsonl, test__ministral-3_8b__instant__A.jsonl, test__openai_gpt-6-luna__instant__A.jsonl, test__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl, test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl, test__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl. Rows read: 31640. Probe files: probe__anthropic_claude-haiku-5-5__A.jsonl, probe__google_gemini-3.6-flash__A.jsonl, probe__ministral-3_8b__A.jsonl, probe__openai_gpt-6-luna__A.jsonl, probe__openrouter_deepseek_deepseek-v3.2__A.jsonl, probe__openrouter_mistralai_ministral-14b-2512__A.jsonl.

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
| anthropic:claude-haiku-5-5 | answer-only | default | thinking=disabled, effort=low | 32 | 4520 |
| anthropic:claude-haiku-5-5 | probe | default | thinking=disabled, effort=low | 64 | 36 |
| google:gemini-3.6-flash | answer-only | default | thinkingLevel=minimal | 4128 | 4520 |
| google:gemini-3.6-flash | probe | default | thinkingLevel=minimal | 4160 | 36 |
| ministral-3:8b | answer-only | (no meta) | - | - | 4520 |
| ministral-3:8b | probe | (no meta) | - | - | 36 |
| openai:gpt-6-luna | answer-only | temperature=0 | reasoning_effort=none | 32 | 4520 |
| openai:gpt-6-luna | probe | temperature=0 | reasoning_effort=none | 64 | 36 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | temperature=0 | reasoning={"enabled": false} | 32 | 4520 |
| openrouter:deepseek/deepseek-v3.2 | probe | temperature=0 | reasoning={"enabled": false} | 64 | 36 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | temperature=0 | n/a | 32 | 4520 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | temperature=0 | n/a | 32 | 4520 |
| openrouter:mistralai/ministral-14b-2512 | probe | temperature=0 | n/a | 64 | 36 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C1 | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C2 |  |  | +0.013 | [-0.050, +0.087] | 2 | 2 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C3 | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 | 1.0000 | both cells non-missing, n = 80 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C4 | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |
| google:gemini-3.6-flash | answer-only | confirmatory | C1 | 49/80 | 3/80 | +0.575 | [+0.475, +0.688] | 46 | 0 | 2.84e-14 | 1.14e-13 | no-log control + four core cells non-missing, n = 80 |
| google:gemini-3.6-flash | answer-only | confirmatory | C2 |  |  | +0.163 | [+0.062, +0.275] | 17 | 4 | 0.0072 | 0.0144 | no-log control + four core cells non-missing, n = 80 |
| google:gemini-3.6-flash | answer-only | confirmatory | C3 | 29/80 | 33/80 | -0.050 | [-0.163, +0.062] | 8 | 12 | 0.5034 | 0.5034 | both cells non-missing, n = 80 |
| google:gemini-3.6-flash | answer-only | confirmatory | C4 | 37/80 | 0/80 | +0.463 | [+0.350, +0.575] | 37 | 0 | 1.46e-11 | 4.37e-11 | four core cells non-missing (no-log control not run in this group), n = 80 |
| ministral-3:8b | answer-only | confirmatory | C1 | 37/80 | 15/80 | +0.275 | [+0.175, +0.388] | 23 | 1 | 2.98e-06 | 8.94e-06 | no-log control + four core cells non-missing, n = 80 |
| ministral-3:8b | answer-only | confirmatory | C2 |  |  | +0.375 | [+0.250, +0.512] | 27 | 1 | 2.16e-07 | 8.64e-07 | no-log control + four core cells non-missing, n = 80 |
| ministral-3:8b | answer-only | confirmatory | C3 | 22/80 | 4/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | 1.53e-05 | both cells non-missing, n = 80 |
| ministral-3:8b | answer-only | confirmatory | C4 | 19/80 | 3/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openai:gpt-6-luna | answer-only | confirmatory | C1 | 13/80 | 11/80 | +0.025 | [-0.037, +0.100] | 5 | 3 | 0.7266 | 1.0000 | no-log control + four core cells non-missing, n = 80 |
| openai:gpt-6-luna | answer-only | confirmatory | C2 |  |  | -0.062 | [-0.163, +0.037] | 6 | 11 | 0.3323 | 0.9969 | no-log control + four core cells non-missing, n = 80 |
| openai:gpt-6-luna | answer-only | confirmatory | C3 | 24/80 | 12/80 | +0.150 | [+0.050, +0.250] | 16 | 4 | 0.0118 | 0.0473 | both cells non-missing, n = 80 |
| openai:gpt-6-luna | answer-only | confirmatory | C4 | 4/80 | 2/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C1 | 5/80 | 0/80 | +0.062 | [+0.013, +0.113] | 5 | 0 | 0.0625 | 0.2500 | no-log control + four core cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C2 |  |  | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | 0.6562 | no-log control + four core cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C3 | 4/80 | 1/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | 0.6562 | both cells non-missing, n = 80 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C4 | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C1 | 61/80 | 22/80 | +0.487 | [+0.375, +0.600] | 39 | 0 | 3.64e-12 | 1.46e-11 | no-log control + four core cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C2 |  |  | +0.575 | [+0.438, +0.725] | 39 | 0 | 3.64e-12 | 1.46e-11 | no-log control + four core cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C3 | 60/80 | 25/80 | +0.438 | [+0.325, +0.550] | 35 | 0 | 5.82e-11 | 1.16e-10 | both cells non-missing, n = 80 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C4 | 22/80 | 6/80 | +0.200 | [+0.113, +0.287] | 16 | 0 | 3.05e-05 | 3.05e-05 | four core cells non-missing (no-log control not run in this group), n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C1 | 35/80 | 12/80 | +0.287 | [+0.188, +0.388] | 24 | 1 | 1.55e-06 | 4.65e-06 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C2 |  |  | +0.312 | [+0.188, +0.450] | 25 | 3 | 2.74e-05 | 5.49e-05 | no-log control + four core cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C3 | 48/80 | 12/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | 1.16e-10 | both cells non-missing, n = 80 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C4 | 18/80 | 3/80 | +0.188 | [+0.113, +0.275] | 15 | 0 | 6.10e-05 | 6.10e-05 | four core cells non-missing (no-log control not run in this group), n = 80 |

# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)

Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).

| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |
|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | A | certain_right | certain | 1.00 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | unsure_right | certain | 0.00 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | unsure_right | unsure | 1.00 (n=1) | 1/80 = 0.01 | 1/80 = 0.01 |
| anthropic:claude-haiku-5-5 | A | certain_right | unsure | 0.00 (n=1) | 2/80 = 0.03 | 0/80 = 0.00 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | unsure | 1.00 (n=1) | 2/80 = 0.03 | 1/80 = 0.01 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | certain | 0.95 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| google:gemini-3.6-flash | A | certain_right | certain | 1.00 (n=1) | 49/80 = 0.61 | 37/80 = 0.46 |
| google:gemini-3.6-flash | A | unsure_right | certain | 0.00 (n=1) | 3/80 = 0.04 | 0/80 = 0.00 |
| google:gemini-3.6-flash | A | unsure_right | unsure | 1.00 (n=1) | 33/80 = 0.41 | 13/80 = 0.16 |
| google:gemini-3.6-flash | A | certain_right | unsure | 0.00 (n=1) | 0/80 = 0.00 | 1/80 = 0.01 |
| google:gemini-3.6-flash | A | perfect_mixed | unsure | 1.00 (n=1) | 29/80 = 0.36 | 9/80 = 0.11 |
| google:gemini-3.6-flash | A | perfect_mixed | certain | 1.00 (n=1) | 37/80 = 0.46 | 14/80 = 0.17 |
| ministral-3:8b | A | certain_right | certain | 1.00 (n=1) | 37/80 = 0.46 | 19/80 = 0.24 |
| ministral-3:8b | A | unsure_right | certain | 0.00 (n=1) | 15/80 = 0.19 | 3/80 = 0.04 |
| ministral-3:8b | A | unsure_right | unsure | 1.00 (n=1) | 4/80 = 0.05 | 1/80 = 0.01 |
| ministral-3:8b | A | certain_right | unsure | 0.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| ministral-3:8b | A | perfect_mixed | unsure | 1.00 (n=1) | 22/80 = 0.28 | 9/80 = 0.11 |
| ministral-3:8b | A | perfect_mixed | certain | 1.00 (n=1) | 49/80 = 0.61 | 27/80 = 0.34 |
| openai:gpt-6-luna | A | certain_right | certain | 1.00 (n=1) | 13/80 = 0.16 | 4/80 = 0.05 |
| openai:gpt-6-luna | A | unsure_right | certain | 0.00 (n=1) | 11/80 = 0.14 | 2/80 = 0.03 |
| openai:gpt-6-luna | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 2/80 = 0.03 |
| openai:gpt-6-luna | A | certain_right | unsure | 0.00 (n=1) | 5/80 = 0.06 | 1/80 = 0.01 |
| openai:gpt-6-luna | A | perfect_mixed | unsure | 1.00 (n=1) | 24/80 = 0.30 | 11/80 = 0.14 |
| openai:gpt-6-luna | A | perfect_mixed | certain | 1.00 (n=1) | 26/80 = 0.33 | 12/80 = 0.15 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | certain | 1.00 (n=1) | 5/80 = 0.06 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | certain | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | unsure | 1.00 (n=1) | 1/80 = 0.01 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | unsure | 0.00 (n=1) | 0/80 = 0.00 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | unsure | 1.00 (n=1) | 4/80 = 0.05 | 0/80 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | certain | 1.00 (n=1) | 31/80 = 0.39 | 12/80 = 0.15 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | certain | 1.00 (n=1) | 35/80 = 0.44 | 18/80 = 0.23 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | certain | 0.00 (n=1) | 12/80 = 0.15 | 3/80 = 0.04 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | unsure | 1.00 (n=1) | 12/80 = 0.15 | 3/80 = 0.04 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | unsure | 0.00 (n=1) | 14/80 = 0.17 | 4/80 = 0.05 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | unsure | 1.00 (n=1) | 48/80 = 0.60 | 23/80 = 0.29 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | certain | 1.00 (n=1) | 72/80 = 0.90 | 44/80 = 0.55 |

# Exploratory

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum right | target distractor

Source files: test__anthropic_claude-haiku-5-5__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| none | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| reliable | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| reliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unreliable | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unreliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| certain_right | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
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
| d_c = certain\|certain_right - certain\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong | target distractor

Source files: test__anthropic_claude-haiku-5-5__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| none | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| perfect_mixed | unsure | 1/80 | 74 | 1 | 5 | 0 | 0 |  |
| reliable | certain | 1/80 | 76 | 1 | 3 | 0 | 0 |  |
| reliable | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| certain_right | certain | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 78 | 0 | 2 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| unsure_right | unsure | 1/80 | 76 | 1 | 3 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | -0.013, -0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/80 | 1/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/80 | 1/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong | target key

Source files: test__anthropic_claude-haiku-5-5__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| none | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| all_certain | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| all_certain | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| all_unsure | certain | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| all_unsure | unsure | 3/80 | 76 | 3 | 1 | 0 | 0 |  |
| all_certain_6of8 | certain | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| all_certain_6of8 | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| all_unsure_6of8 | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| all_unsure_6of8 | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| c3_u4 | certain | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| c3_u4 | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| c2_u4 | certain | 1/80 | 76 | 1 | 3 | 0 | 0 |  |
| c2_u4 | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| c4_u3 | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| c4_u3 | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| c4_u2 | certain | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| c4_u2 | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| reliable | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| unreliable | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| unreliable | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| certain_right | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| certain_right | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| unsure_right | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| unsure_right | unsure | 1/80 | 77 | 1 | 2 | 0 | 0 |  |
| certain_right_nosum | certain | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| certain_right_nosum | unsure | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| unsure_right_nosum | certain | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| unsure_right_nosum | unsure | 1/80 | 77 | 1 | 2 | 0 | 0 |  |
| certain_right_long | certain | 2/80 | 77 | 2 | 1 | 0 | 0 |  |
| certain_right_long | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| unsure_right_long | certain | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| unsure_right_long | unsure | 2/80 | 76 | 2 | 2 | 0 | 0 |  |
| control | none | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| certain_right | none | 2/80 | 74 | 2 | 4 | 0 | 0 |  |
| unsure_right | none | 2/80 | 75 | 2 | 3 | 0 | 0 |  |
| perfect_mixed | none | 3/80 | 71 | 3 | 6 | 0 | 0 |  |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 3/80 | 0 |
| certain_right log shown | 2/80 | 6/80 | 0 |
| unsure_right log shown | 2/80 | 5/80 | 0 |
| perfect_mixed log shown | 3/80 | 9/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/80 | 2/80 | -0.013 | [-0.062, +0.025] | 1 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.013 | [-0.062, +0.025] | 1 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.013 | [-0.050, +0.087] | 2 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | four long cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four long cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | four long cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | four long cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 | four nosum cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 1/80 | 2/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | four nosum cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | four nosum cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.025 | [-0.025, +0.087] | 2 | 1 | 1.0000 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 2/80 | 2/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 3/80 | 1/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 1/80 | 2/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 80 | -0.013, -0.013 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 3/80 | 2/80 | +0.013 | [-0.037, +0.063] | 3 | 2 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 6/80 | 3/80 | +0.037 | [-0.013, +0.100] | 4 | 1 | 0.3750 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 5/80 | 3/80 | +0.025 | [-0.037, +0.100] | 5 | 3 | 0.7266 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 9/80 | 3/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 | both cells non-missing, n = 80 |

## google:gemini-3.6-flash | answer-only | arm A | stratum right | target distractor

Source files: test__google_gemini-3.6-flash__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| none | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| reliable | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unreliable | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unreliable | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 7/40 | 33 | 7 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| control | none | 0/40 | 40 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/40 | 0/40 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 7/40 | 0/40 | +0.175 | [+0.075, +0.300] | 7 | 0 | 0.0156 | no-log control + four core cells non-missing, n = 40 | +0.175, +0.175 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/40 | 0/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 40 | +0.050, +0.050 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.225 | [+0.100, +0.375] | 8 | 0 | 0.0078 | no-log control + four core cells non-missing, n = 40 | +0.225, +0.225 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.125 | [+0.000, +0.250] | 6 | 1 | 0.1250 | no-log control + four core cells non-missing, n = 40 | +0.125, +0.125 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/40 | 2/40 | -0.025 | [-0.075, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 40 | -0.025, -0.025 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 1/40 | 7/40 | -0.150 | [-0.275, -0.050] | 0 | 6 | 0.0312 | both cells non-missing, n = 40 | -0.150, -0.150 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/40 | 0/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 7/40 | 2/40 | +0.125 | [+0.000, +0.250] | 6 | 1 | 0.1250 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |

## google:gemini-3.6-flash | answer-only | arm A | stratum wrong | target distractor

Source files: test__google_gemini-3.6-flash__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 3/80 | 75 | 3 | 2 | 0 | 0 |  |
| none | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 14/80 | 65 | 14 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 9/80 | 70 | 9 | 1 | 0 | 0 |  |
| reliable | certain | 4/80 | 75 | 4 | 1 | 0 | 0 |  |
| reliable | unsure | 1/80 | 77 | 1 | 2 | 0 | 0 |  |
| certain_right | certain | 37/80 | 42 | 37 | 1 | 0 | 0 |  |
| certain_right | unsure | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 77 | 0 | 3 | 0 | 0 |  |
| unsure_right | unsure | 13/80 | 65 | 13 | 2 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 37/80 | 0/80 | +0.463 | [+0.350, +0.575] | 37 | 0 | 1.46e-11 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.463, +0.463 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 13/80 | 1/80 | +0.150 | [+0.075, +0.237] | 12 | 0 | 0.0005 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.150, +0.150 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.613 | [+0.450, +0.775] | 37 | 0 | 1.46e-11 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.613, +0.613 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.312 | [+0.212, +0.412] | 25 | 0 | 5.96e-08 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.312, +0.312 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 9/80 | 13/80 | -0.050 | [-0.138, +0.037] | 4 | 8 | 0.3877 | both cells non-missing, n = 80 | -0.050, -0.050 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 14/80 | 37/80 | -0.287 | [-0.388, -0.188] | 0 | 23 | 2.38e-07 | both cells non-missing, n = 80 | -0.287, -0.287 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 4/80 | 1/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 37/80 | 13/80 | +0.300 | [+0.200, +0.400] | 24 | 0 | 1.19e-07 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 3/80 | 2/80 | +0.013 | [-0.025, +0.050] | 2 | 1 | 1.0000 | both cells non-missing, n = 80 |

## google:gemini-3.6-flash | answer-only | arm A | stratum wrong | target key

Source files: test__google_gemini-3.6-flash__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 15/80 | 64 | 15 | 1 | 0 | 0 |  |
| none | unsure | 8/80 | 72 | 8 | 0 | 0 | 0 |  |
| all_certain | certain | 20/80 | 60 | 20 | 0 | 0 | 0 |  |
| all_certain | unsure | 10/80 | 70 | 10 | 0 | 0 | 0 |  |
| all_unsure | certain | 20/80 | 60 | 20 | 0 | 0 | 0 |  |
| all_unsure | unsure | 38/80 | 42 | 38 | 0 | 0 | 0 |  |
| all_certain_6of8 | certain | 14/80 | 66 | 14 | 0 | 0 | 0 |  |
| all_certain_6of8 | unsure | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| all_unsure_6of8 | certain | 14/80 | 66 | 14 | 0 | 0 | 0 |  |
| all_unsure_6of8 | unsure | 18/80 | 62 | 18 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 37/80 | 43 | 37 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 29/80 | 51 | 29 | 0 | 0 | 0 |  |
| c3_u4 | certain | 22/80 | 57 | 22 | 1 | 0 | 0 |  |
| c3_u4 | unsure | 18/80 | 62 | 18 | 0 | 0 | 0 |  |
| c2_u4 | certain | 10/80 | 68 | 10 | 2 | 0 | 0 |  |
| c2_u4 | unsure | 20/80 | 59 | 20 | 1 | 0 | 0 |  |
| c4_u3 | certain | 31/80 | 49 | 31 | 0 | 0 | 0 |  |
| c4_u3 | unsure | 14/80 | 66 | 14 | 0 | 0 | 0 |  |
| c4_u2 | certain | 35/80 | 45 | 35 | 0 | 0 | 0 |  |
| c4_u2 | unsure | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| reliable | certain | 21/80 | 59 | 21 | 0 | 0 | 0 |  |
| reliable | unsure | 13/80 | 67 | 13 | 0 | 0 | 0 |  |
| unreliable | certain | 8/80 | 72 | 8 | 0 | 0 | 0 |  |
| unreliable | unsure | 4/80 | 76 | 4 | 0 | 0 | 0 |  |
| certain_right | certain | 49/80 | 31 | 49 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| unsure_right | certain | 3/80 | 76 | 3 | 1 | 0 | 0 |  |
| unsure_right | unsure | 33/80 | 47 | 33 | 0 | 0 | 0 |  |
| certain_right_nosum | certain | 30/80 | 50 | 30 | 0 | 0 | 0 |  |
| certain_right_nosum | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right_nosum | certain | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| unsure_right_nosum | unsure | 22/80 | 58 | 22 | 0 | 0 | 0 |  |
| certain_right_long | certain | 54/80 | 26 | 54 | 0 | 0 | 0 |  |
| certain_right_long | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unsure_right_long | certain | 0/80 | 79 | 0 | 1 | 0 | 0 |  |
| unsure_right_long | unsure | 42/80 | 38 | 42 | 0 | 0 | 0 |  |
| control | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unsure_right | none | 5/80 | 74 | 5 | 1 | 0 | 0 |  |
| perfect_mixed | none | 2/80 | 77 | 2 | 1 | 0 | 0 |  |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/80 | 0/80 | 0 |
| certain_right log shown | 2/80 | 2/80 | 0 |
| unsure_right log shown | 5/80 | 6/80 | 0 |
| perfect_mixed log shown | 2/80 | 3/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 49/80 | 3/80 | +0.575 | [+0.475, +0.688] | 46 | 0 | 2.84e-14 | no-log control + four core cells non-missing, n = 80 | +0.575, +0.575 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 33/80 | 0/80 | +0.412 | [+0.300, +0.525] | 33 | 0 | 2.33e-10 | no-log control + four core cells non-missing, n = 80 | +0.412, +0.412 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.988 | [+0.800, +1.175] | 50 | 0 | 1.78e-15 | no-log control + four core cells non-missing, n = 80 | +0.988, +0.988 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.163 | [+0.062, +0.275] | 17 | 4 | 0.0072 | no-log control + four core cells non-missing, n = 80 | +0.163, +0.163 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 54/80 | 0/80 | +0.675 | [+0.575, +0.775] | 54 | 0 | 1.11e-16 | four long cells non-missing, n = 80 | +0.675, +0.675 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 42/80 | 2/80 | +0.500 | [+0.388, +0.613] | 40 | 0 | 1.82e-12 | four long cells non-missing, n = 80 | +0.500, +0.500 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +1.175 | [+1.000, +1.350] | 60 | 0 | 1.73e-18 | four long cells non-missing, n = 80 | +1.175, +1.175 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.175 | [+0.062, +0.300] | 20 | 6 | 0.0094 | four long cells non-missing, n = 80 | +0.175, +0.175 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 30/80 | 1/80 | +0.362 | [+0.263, +0.475] | 29 | 0 | 3.73e-09 | four nosum cells non-missing, n = 80 | +0.362, +0.362 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 22/80 | 0/80 | +0.275 | [+0.187, +0.375] | 22 | 0 | 4.77e-07 | four nosum cells non-missing, n = 80 | +0.275, +0.275 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.637 | [+0.463, +0.825] | 33 | 0 | 2.33e-10 | four nosum cells non-missing, n = 80 | +0.637, +0.637 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.087 | [+0.000, +0.188] | 11 | 4 | 0.1185 | four nosum cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 29/80 | 18/80 | +0.138 | [+0.050, +0.225] | 13 | 2 | 0.0074 | both cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 29/80 | 20/80 | +0.113 | [+0.025, +0.200] | 11 | 2 | 0.0225 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 29/80 | 33/80 | -0.050 | [-0.163, +0.062] | 8 | 12 | 0.5034 | both cells non-missing, n = 80 | -0.050, -0.050 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 37/80 | 31/80 | +0.075 | [-0.013, +0.175] | 11 | 5 | 0.2101 | both cells non-missing, n = 80 | +0.075, +0.075 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 37/80 | 35/80 | +0.025 | [-0.037, +0.087] | 4 | 2 | 0.6875 | both cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 37/80 | 49/80 | -0.150 | [-0.263, -0.037] | 5 | 17 | 0.0169 | both cells non-missing, n = 80 | -0.150, -0.150 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 38/80 | 18/80 | +0.250 | [+0.150, +0.350] | 21 | 1 | 1.10e-05 | both cells non-missing, n = 80 | +0.250, +0.250 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 20/80 | 14/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 | both cells non-missing, n = 80 | +0.075, +0.075 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 21/80 | 13/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 38/80 | 8/80 | +0.375 | [+0.263, +0.487] | 32 | 2 | 6.94e-08 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 49/80 | 33/80 | +0.200 | [+0.113, +0.300] | 17 | 1 | 0.0001 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 15/80 | 8/80 | +0.087 | [+0.025, +0.163] | 8 | 1 | 0.0391 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 5/80 | 0/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 6/80 | 0/80 | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 |

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

## openai:gpt-6-luna | answer-only | arm A | stratum right | target distractor

Source files: test__openai_gpt-6-luna__instant__A.jsonl. Items: 40. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 40; of these, also with a non-missing no-log control (by-voice population): 40. Items used for bounds: 40.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 1/40 | 39 | 1 | 0 | 0 | 0 |  |
| none | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 2/40 | 38 | 2 | 0 | 0 | 0 |  |
| reliable | certain | 1/40 | 38 | 1 | 1 | 0 | 0 |  |
| reliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unreliable | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unreliable | unsure | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| certain_right | certain | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/40 | 39 | 0 | 1 | 0 | 0 |  |
| unsure_right | unsure | 0/40 | 40 | 0 | 0 | 0 | 0 |  |
| control | none | 0/40 | 39 | 0 | 1 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/40 | 1/40 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 40 | +0.000, +0.000 (N = 40) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/40 | 0/40 | +0.050 | [+0.000, +0.125] | 2 | 0 | 0.5000 | both cells non-missing, n = 40 | +0.050, +0.050 (N = 40) |
| certain\|perfect_mixed - certain\|certain_right | 1/40 | 0/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 | +0.025, +0.025 (N = 40) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/40 | 0/40 | +0.025 | [+0.000, +0.075] | 1 | 0 | 1.0000 | both cells non-missing, n = 40 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/40 | 0/40 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 40 |
| no-log tone gap: certain\|none - unsure\|none | 1/40 | 2/40 | -0.025 | [-0.100, +0.050] | 1 | 2 | 1.0000 | both cells non-missing, n = 40 |

## openai:gpt-6-luna | answer-only | arm A | stratum wrong | target distractor

Source files: test__openai_gpt-6-luna__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 10/80 | 69 | 10 | 1 | 0 | 0 |  |
| none | unsure | 8/80 | 69 | 8 | 3 | 0 | 0 |  |
| perfect_mixed | certain | 12/80 | 61 | 12 | 7 | 0 | 0 |  |
| perfect_mixed | unsure | 11/80 | 66 | 11 | 3 | 0 | 0 |  |
| reliable | certain | 6/80 | 66 | 6 | 8 | 0 | 0 |  |
| reliable | unsure | 2/80 | 74 | 2 | 4 | 0 | 0 |  |
| certain_right | certain | 4/80 | 71 | 4 | 5 | 0 | 0 |  |
| certain_right | unsure | 1/80 | 75 | 1 | 4 | 0 | 0 |  |
| unsure_right | certain | 2/80 | 73 | 2 | 5 | 0 | 0 |  |
| unsure_right | unsure | 2/80 | 74 | 2 | 4 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 4/80 | 2/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/80 | 1/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.037 | [-0.013, +0.087] | 4 | 1 | 0.3750 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.037, +0.037 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.013 | [-0.037, +0.075] | 3 | 2 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 80 | +0.013, +0.013 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 11/80 | 2/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 12/80 | 4/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 | both cells non-missing, n = 80 | +0.100, +0.100 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 6/80 | 2/80 | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 4/80 | 2/80 | +0.025 | [-0.025, +0.075] | 3 | 1 | 0.6250 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 10/80 | 8/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 | both cells non-missing, n = 80 |

## openai:gpt-6-luna | answer-only | arm A | stratum wrong | target key

Source files: test__openai_gpt-6-luna__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/80 | 53 | 25 | 2 | 0 | 0 |  |
| none | unsure | 24/80 | 54 | 24 | 2 | 0 | 0 |  |
| all_certain | certain | 26/80 | 53 | 26 | 1 | 0 | 0 |  |
| all_certain | unsure | 16/80 | 62 | 16 | 2 | 0 | 0 |  |
| all_unsure | certain | 21/80 | 59 | 21 | 0 | 0 | 0 |  |
| all_unsure | unsure | 25/80 | 54 | 25 | 1 | 0 | 0 |  |
| all_certain_6of8 | certain | 11/80 | 67 | 11 | 2 | 0 | 0 |  |
| all_certain_6of8 | unsure | 8/80 | 67 | 8 | 5 | 0 | 0 |  |
| all_unsure_6of8 | certain | 6/80 | 73 | 6 | 1 | 0 | 0 |  |
| all_unsure_6of8 | unsure | 9/80 | 71 | 9 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 26/80 | 52 | 26 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 24/80 | 55 | 24 | 1 | 0 | 0 |  |
| c3_u4 | certain | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| c3_u4 | unsure | 17/80 | 63 | 17 | 0 | 0 | 0 |  |
| c2_u4 | certain | 17/80 | 60 | 17 | 3 | 0 | 0 |  |
| c2_u4 | unsure | 21/80 | 57 | 21 | 2 | 0 | 0 |  |
| c4_u3 | certain | 17/80 | 63 | 17 | 0 | 0 | 0 |  |
| c4_u3 | unsure | 11/80 | 69 | 11 | 0 | 0 | 0 |  |
| c4_u2 | certain | 15/80 | 65 | 15 | 0 | 0 | 0 |  |
| c4_u2 | unsure | 14/80 | 65 | 14 | 1 | 0 | 0 |  |
| reliable | certain | 13/80 | 65 | 13 | 2 | 0 | 0 |  |
| reliable | unsure | 10/80 | 70 | 10 | 0 | 0 | 0 |  |
| unreliable | certain | 9/80 | 71 | 9 | 0 | 0 | 0 |  |
| unreliable | unsure | 8/80 | 71 | 8 | 1 | 0 | 0 |  |
| certain_right | certain | 13/80 | 64 | 13 | 3 | 0 | 0 |  |
| certain_right | unsure | 5/80 | 75 | 5 | 0 | 0 | 0 |  |
| unsure_right | certain | 11/80 | 66 | 11 | 3 | 0 | 0 |  |
| unsure_right | unsure | 12/80 | 67 | 12 | 1 | 0 | 0 |  |
| certain_right_nosum | certain | 15/80 | 62 | 15 | 3 | 0 | 0 |  |
| certain_right_nosum | unsure | 10/80 | 70 | 10 | 0 | 0 | 0 |  |
| unsure_right_nosum | certain | 15/80 | 64 | 15 | 1 | 0 | 0 |  |
| unsure_right_nosum | unsure | 12/80 | 65 | 12 | 3 | 0 | 0 |  |
| certain_right_long | certain | 10/80 | 68 | 10 | 2 | 0 | 0 |  |
| certain_right_long | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unsure_right_long | certain | 8/80 | 71 | 8 | 1 | 0 | 0 |  |
| unsure_right_long | unsure | 11/80 | 69 | 11 | 0 | 0 | 0 |  |
| control | none | 1/80 | 78 | 1 | 1 | 0 | 0 |  |
| certain_right | none | 6/80 | 72 | 6 | 2 | 0 | 0 |  |
| unsure_right | none | 8/80 | 70 | 8 | 2 | 0 | 0 |  |
| perfect_mixed | none | 6/80 | 71 | 6 | 3 | 0 | 0 |  |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 1/80 | 2/80 | 0 |
| certain_right log shown | 6/80 | 8/80 | 0 |
| unsure_right log shown | 8/80 | 10/80 | 0 |
| perfect_mixed log shown | 6/80 | 9/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 13/80 | 11/80 | +0.025 | [-0.037, +0.100] | 5 | 3 | 0.7266 | no-log control + four core cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 12/80 | 5/80 | +0.087 | [+0.013, +0.175] | 9 | 2 | 0.0654 | no-log control + four core cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.113 | [+0.000, +0.225] | 13 | 5 | 0.0963 | no-log control + four core cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.062 | [-0.163, +0.037] | 6 | 11 | 0.3323 | no-log control + four core cells non-missing, n = 80 | -0.062, -0.062 (N = 80) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 10/80 | 8/80 | +0.025 | [-0.037, +0.100] | 5 | 3 | 0.7266 | four long cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 11/80 | 2/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | four long cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.138 | [+0.037, +0.250] | 10 | 2 | 0.0386 | four long cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | -0.087 | [-0.175, -0.013] | 2 | 8 | 0.1094 | four long cells non-missing, n = 80 | -0.087, -0.087 (N = 80) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 15/80 | 15/80 | +0.000 | [-0.087, +0.087] | 6 | 6 | 1.0000 | four nosum cells non-missing, n = 80 | +0.000, +0.000 (N = 80) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 12/80 | 10/80 | +0.025 | [-0.062, +0.113] | 7 | 5 | 0.7744 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.025 | [-0.075, +0.125] | 8 | 5 | 0.5811 | four nosum cells non-missing, n = 80 | +0.025, +0.025 (N = 80) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | -0.025 | [-0.163, +0.113] | 8 | 9 | 1.0000 | four nosum cells non-missing, n = 80 | -0.025, -0.025 (N = 80) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 24/80 | 17/80 | +0.087 | [+0.013, +0.175] | 9 | 2 | 0.0654 | both cells non-missing, n = 80 | +0.087, +0.087 (N = 80) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 24/80 | 21/80 | +0.037 | [-0.037, +0.125] | 7 | 4 | 0.5488 | both cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| unsure\|perfect_mixed - unsure\|unsure_right | 24/80 | 12/80 | +0.150 | [+0.050, +0.250] | 16 | 4 | 0.0118 | both cells non-missing, n = 80 | +0.150, +0.150 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 26/80 | 17/80 | +0.113 | [+0.025, +0.200] | 12 | 3 | 0.0352 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 26/80 | 15/80 | +0.138 | [+0.025, +0.237] | 16 | 5 | 0.0266 | both cells non-missing, n = 80 | +0.138, +0.138 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 26/80 | 13/80 | +0.163 | [+0.062, +0.263] | 16 | 3 | 0.0044 | both cells non-missing, n = 80 | +0.163, +0.163 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 25/80 | 9/80 | +0.200 | [+0.075, +0.325] | 22 | 6 | 0.0037 | both cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 26/80 | 11/80 | +0.188 | [+0.100, +0.287] | 16 | 1 | 0.0003 | both cells non-missing, n = 80 | +0.188, +0.188 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 13/80 | 10/80 | +0.037 | [-0.025, +0.100] | 5 | 2 | 0.4531 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 25/80 | 24/80 | +0.013 | [-0.100, +0.125] | 10 | 9 | 1.0000 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 13/80 | 12/80 | +0.013 | [-0.075, +0.100] | 6 | 5 | 1.0000 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 25/80 | 24/80 | +0.013 | [-0.062, +0.087] | 6 | 5 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 6/80 | 1/80 | +0.062 | [+0.000, +0.125] | 6 | 1 | 0.1250 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 8/80 | 2/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 8/80 | 1/80 | +0.087 | [+0.037, +0.150] | 7 | 0 | 0.0156 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 10/80 | 2/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 6/80 | 1/80 | +0.062 | [+0.013, +0.125] | 5 | 0 | 0.0625 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 9/80 | 2/80 | +0.087 | [+0.013, +0.163] | 8 | 1 | 0.0391 | both cells non-missing, n = 80 |

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

Source files: test__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 32/80 | 47 | 32 | 1 | 0 | 0 |  |
| none | unsure | 7/80 | 73 | 7 | 0 | 0 | 0 |  |
| all_certain | certain | 34/80 | 46 | 34 | 0 | 0 | 0 |  |
| all_certain | unsure | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| all_unsure | certain | 33/80 | 47 | 33 | 0 | 0 | 0 |  |
| all_unsure | unsure | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| all_certain_6of8 | certain | 8/80 | 72 | 8 | 0 | 0 | 0 |  |
| all_certain_6of8 | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| all_unsure_6of8 | certain | 13/80 | 67 | 13 | 0 | 0 | 0 |  |
| all_unsure_6of8 | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 31/80 | 47 | 31 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 4/80 | 76 | 4 | 0 | 0 | 0 |  |
| c3_u4 | certain | 15/80 | 65 | 15 | 0 | 0 | 0 |  |
| c3_u4 | unsure | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| c2_u4 | certain | 11/80 | 69 | 11 | 0 | 0 | 0 |  |
| c2_u4 | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| c4_u3 | certain | 15/80 | 65 | 15 | 0 | 0 | 0 |  |
| c4_u3 | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| c4_u2 | certain | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| c4_u2 | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 12/80 | 68 | 12 | 0 | 0 | 0 |  |
| reliable | unsure | 2/80 | 78 | 2 | 0 | 0 | 0 |  |
| unreliable | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unreliable | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 5/80 | 75 | 5 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 1/80 | 79 | 1 | 0 | 0 | 0 |  |
| certain_right_nosum | certain | 3/80 | 77 | 3 | 0 | 0 | 0 |  |
| certain_right_nosum | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right_nosum | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right_nosum | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right_long | certain | 7/80 | 73 | 7 | 0 | 0 | 0 |  |
| certain_right_long | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right_long | certain | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right_long | unsure | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| control | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| unsure_right | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | none | 0/80 | 80 | 0 | 0 | 0 | 0 |  |

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
| d_c = certain\|certain_right - certain\|unsure_right | 5/80 | 0/80 | +0.062 | [+0.013, +0.113] | 5 | 0 | 0.0625 | no-log control + four core cells non-missing, n = 80 | +0.062, +0.062 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 80 | +0.013, +0.013 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.075 | [+0.025, +0.138] | 6 | 0 | 0.0312 | no-log control + four core cells non-missing, n = 80 | +0.075, +0.075 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | no-log control + four core cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |
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
| unsure\|perfect_mixed - unsure\|unsure_right | 4/80 | 1/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u3 | 31/80 | 15/80 | +0.200 | [+0.100, +0.300] | 18 | 2 | 0.0004 | both cells non-missing, n = 80 | +0.200, +0.200 (N = 80) |
| certain\|perfect_mixed - certain\|c4_u2 | 31/80 | 12/80 | +0.237 | [+0.150, +0.338] | 19 | 0 | 3.81e-06 | both cells non-missing, n = 80 | +0.237, +0.237 (N = 80) |
| certain\|perfect_mixed - certain\|certain_right | 31/80 | 5/80 | +0.325 | [+0.225, +0.425] | 26 | 0 | 2.98e-08 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 | both cells non-missing, n = 80 | +0.037, +0.037 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 34/80 | 8/80 | +0.325 | [+0.212, +0.438] | 27 | 1 | 2.16e-07 | both cells non-missing, n = 80 | +0.325, +0.325 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 12/80 | 2/80 | +0.125 | [+0.062, +0.200] | 10 | 0 | 0.0020 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 3/80 | 7/80 | -0.050 | [-0.125, +0.013] | 2 | 6 | 0.2891 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 5/80 | 1/80 | +0.050 | [+0.000, +0.113] | 5 | 1 | 0.2188 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 32/80 | 7/80 | +0.312 | [+0.212, +0.412] | 25 | 0 | 5.96e-08 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 80 |

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

Source files: test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl. Items: 80. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 80; of these, also with a non-missing no-log control (by-voice population): 80. Items used for bounds: 80.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 64/80 | 12 | 64 | 4 | 0 | 0 |  |
| none | unsure | 53/80 | 16 | 53 | 11 | 0 | 0 |  |
| all_certain | certain | 72/80 | 2 | 72 | 6 | 0 | 0 |  |
| all_certain | unsure | 60/80 | 15 | 60 | 5 | 0 | 0 |  |
| all_unsure | certain | 67/80 | 8 | 67 | 5 | 0 | 0 |  |
| all_unsure | unsure | 62/80 | 11 | 62 | 7 | 0 | 0 |  |
| all_certain_6of8 | certain | 68/80 | 7 | 68 | 5 | 0 | 0 |  |
| all_certain_6of8 | unsure | 53/80 | 22 | 53 | 5 | 0 | 0 |  |
| all_unsure_6of8 | certain | 66/80 | 8 | 66 | 6 | 0 | 0 |  |
| all_unsure_6of8 | unsure | 52/80 | 23 | 52 | 5 | 0 | 0 |  |
| perfect_mixed | certain | 70/80 | 3 | 70 | 7 | 0 | 0 |  |
| perfect_mixed | unsure | 60/80 | 14 | 60 | 6 | 0 | 0 |  |
| c3_u4 | certain | 69/80 | 6 | 69 | 5 | 0 | 0 |  |
| c3_u4 | unsure | 52/80 | 20 | 52 | 8 | 0 | 0 |  |
| c2_u4 | certain | 62/80 | 11 | 62 | 7 | 0 | 0 |  |
| c2_u4 | unsure | 48/80 | 24 | 48 | 8 | 0 | 0 |  |
| c4_u3 | certain | 70/80 | 5 | 70 | 5 | 0 | 0 |  |
| c4_u3 | unsure | 52/80 | 21 | 52 | 7 | 0 | 0 |  |
| c4_u2 | certain | 69/80 | 6 | 69 | 5 | 0 | 0 |  |
| c4_u2 | unsure | 51/80 | 22 | 51 | 7 | 0 | 0 |  |
| reliable | certain | 68/80 | 8 | 68 | 4 | 0 | 0 |  |
| reliable | unsure | 50/80 | 22 | 50 | 8 | 0 | 0 |  |
| unreliable | certain | 19/80 | 58 | 19 | 3 | 0 | 0 |  |
| unreliable | unsure | 13/80 | 65 | 13 | 2 | 0 | 0 |  |
| certain_right | certain | 61/80 | 13 | 61 | 6 | 0 | 0 |  |
| certain_right | unsure | 32/80 | 40 | 32 | 8 | 0 | 0 |  |
| unsure_right | certain | 22/80 | 51 | 22 | 7 | 0 | 0 |  |
| unsure_right | unsure | 25/80 | 49 | 25 | 6 | 0 | 0 |  |
| certain_right_nosum | certain | 63/80 | 12 | 63 | 5 | 0 | 0 |  |
| certain_right_nosum | unsure | 39/80 | 33 | 39 | 8 | 0 | 0 |  |
| unsure_right_nosum | certain | 33/80 | 43 | 33 | 4 | 0 | 0 |  |
| unsure_right_nosum | unsure | 29/80 | 47 | 29 | 4 | 0 | 0 |  |
| certain_right_long | certain | 62/80 | 12 | 62 | 6 | 0 | 0 |  |
| certain_right_long | unsure | 27/80 | 46 | 27 | 7 | 0 | 0 |  |
| unsure_right_long | certain | 24/80 | 52 | 24 | 4 | 0 | 0 |  |
| unsure_right_long | unsure | 26/80 | 50 | 26 | 4 | 0 | 0 |  |
| control | none | 16/80 | 50 | 16 | 14 | 0 | 0 |  |
| certain_right | none | 18/80 | 48 | 18 | 14 | 0 | 0 |  |
| unsure_right | none | 19/80 | 48 | 19 | 13 | 0 | 0 |  |
| perfect_mixed | none | 17/80 | 49 | 17 | 14 | 0 | 0 |  |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 16/80 | 30/80 | 0 |
| certain_right log shown | 18/80 | 32/80 | 0 |
| unsure_right log shown | 19/80 | 32/80 | 0 |
| perfect_mixed log shown | 17/80 | 31/80 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 61/80 | 22/80 | +0.487 | [+0.375, +0.600] | 39 | 0 | 3.64e-12 | no-log control + four core cells non-missing, n = 80 | +0.487, +0.487 (N = 80) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 25/80 | 32/80 | -0.087 | [-0.150, -0.037] | 0 | 7 | 0.0156 | no-log control + four core cells non-missing, n = 80 | -0.087, -0.087 (N = 80) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.400 | [+0.300, +0.512] | 32 | 0 | 4.66e-10 | no-log control + four core cells non-missing, n = 80 | +0.400, +0.400 (N = 80) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.575 | [+0.438, +0.725] | 39 | 0 | 3.64e-12 | no-log control + four core cells non-missing, n = 80 | +0.575, +0.575 (N = 80) |
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
| certain\|perfect_mixed - certain\|certain_right | 70/80 | 61/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 | both cells non-missing, n = 80 | +0.113, +0.113 (N = 80) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 62/80 | 52/80 | +0.125 | [+0.050, +0.212] | 11 | 1 | 0.0063 | both cells non-missing, n = 80 | +0.125, +0.125 (N = 80) |
| certain\|all_certain - certain\|all_certain_6of8 | 72/80 | 68/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 | both cells non-missing, n = 80 | +0.050, +0.050 (N = 80) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 68/80 | 50/80 | +0.225 | [+0.138, +0.325] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 80 |
| ceiling check: unsure\|all_unsure - unsure\|none | 62/80 | 53/80 | +0.113 | [+0.013, +0.212] | 13 | 4 | 0.0490 | both cells non-missing, n = 80 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 61/80 | 25/80 | +0.450 | [+0.338, +0.562] | 36 | 0 | 2.91e-11 | both cells non-missing, n = 80 |
| no-log tone gap: certain\|none - unsure\|none | 64/80 | 53/80 | +0.138 | [+0.062, +0.212] | 11 | 0 | 0.0010 | both cells non-missing, n = 80 |
| moved to x: certain_right log, no objection - no-log control | 18/80 | 16/80 | +0.025 | [-0.050, +0.100] | 6 | 4 | 0.7539 | both cells non-missing, n = 80 |
| changed at all: certain_right log, no objection - no-log control | 32/80 | 30/80 | +0.025 | [-0.050, +0.100] | 6 | 4 | 0.7539 | both cells non-missing, n = 80 |
| moved to x: unsure_right log, no objection - no-log control | 19/80 | 16/80 | +0.037 | [-0.037, +0.125] | 7 | 4 | 0.5488 | both cells non-missing, n = 80 |
| changed at all: unsure_right log, no objection - no-log control | 32/80 | 30/80 | +0.025 | [-0.062, +0.113] | 7 | 5 | 0.7744 | both cells non-missing, n = 80 |
| moved to x: perfect_mixed log, no objection - no-log control | 17/80 | 16/80 | +0.013 | [-0.062, +0.087] | 5 | 4 | 1.0000 | both cells non-missing, n = 80 |
| changed at all: perfect_mixed log, no objection - no-log control | 31/80 | 30/80 | +0.013 | [-0.062, +0.087] | 5 | 4 | 1.0000 | both cells non-missing, n = 80 |

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

## Target comparison: anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 |
| none | unsure | 2/80 | 2/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 |
| perfect_mixed | certain | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| perfect_mixed | unsure | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 |
| reliable | certain | 2/80 | 1/80 | +0.013 | [-0.025, +0.050] | 2 | 1 | 1.0000 |
| reliable | unsure | 2/80 | 1/80 | +0.013 | [-0.025, +0.062] | 2 | 1 | 1.0000 |
| certain_right | certain | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| certain_right | unsure | 2/80 | 0/80 | +0.025 | [+0.000, +0.062] | 2 | 0 | 0.5000 |
| unsure_right | certain | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |
| unsure_right | unsure | 1/80 | 1/80 | +0.000 | [-0.037, +0.037] | 1 | 1 | 1.0000 |

## Target comparison: google:gemini-3.6-flash | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 15/80 | 3/80 | +0.150 | [+0.062, +0.237] | 13 | 1 | 0.0018 |
| none | unsure | 8/80 | 2/80 | +0.075 | [+0.000, +0.150] | 8 | 2 | 0.1094 |
| perfect_mixed | certain | 37/80 | 14/80 | +0.287 | [+0.188, +0.400] | 25 | 2 | 5.65e-06 |
| perfect_mixed | unsure | 29/80 | 9/80 | +0.250 | [+0.150, +0.350] | 21 | 1 | 1.10e-05 |
| reliable | certain | 21/80 | 4/80 | +0.212 | [+0.125, +0.312] | 18 | 1 | 7.63e-05 |
| reliable | unsure | 13/80 | 1/80 | +0.150 | [+0.062, +0.237] | 13 | 1 | 0.0018 |
| certain_right | certain | 49/80 | 37/80 | +0.150 | [+0.050, +0.250] | 16 | 4 | 0.0118 |
| certain_right | unsure | 0/80 | 1/80 | -0.013 | [-0.037, +0.000] | 0 | 1 | 1.0000 |
| unsure_right | certain | 3/80 | 0/80 | +0.037 | [+0.000, +0.087] | 3 | 0 | 0.2500 |
| unsure_right | unsure | 33/80 | 13/80 | +0.250 | [+0.138, +0.362] | 23 | 3 | 8.80e-05 |

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

## Target comparison: openai:gpt-6-luna | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/80 | 10/80 | +0.188 | [+0.087, +0.287] | 17 | 2 | 0.0007 |
| none | unsure | 24/80 | 8/80 | +0.200 | [+0.087, +0.312] | 20 | 4 | 0.0015 |
| perfect_mixed | certain | 26/80 | 12/80 | +0.175 | [+0.050, +0.300] | 20 | 6 | 0.0094 |
| perfect_mixed | unsure | 24/80 | 11/80 | +0.163 | [+0.075, +0.250] | 14 | 1 | 0.0010 |
| reliable | certain | 13/80 | 6/80 | +0.087 | [-0.013, +0.188] | 12 | 5 | 0.1435 |
| reliable | unsure | 10/80 | 2/80 | +0.100 | [+0.025, +0.175] | 9 | 1 | 0.0215 |
| certain_right | certain | 13/80 | 4/80 | +0.113 | [+0.025, +0.200] | 11 | 2 | 0.0225 |
| certain_right | unsure | 5/80 | 1/80 | +0.050 | [+0.013, +0.100] | 4 | 0 | 0.1250 |
| unsure_right | certain | 11/80 | 2/80 | +0.113 | [+0.050, +0.188] | 9 | 0 | 0.0039 |
| unsure_right | unsure | 12/80 | 2/80 | +0.125 | [+0.050, +0.212] | 11 | 1 | 0.0063 |

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
| certain_right | certain | 5/80 | 0/80 | +0.062 | [+0.013, +0.113] | 5 | 0 | 0.0625 |
| certain_right | unsure | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 0/80 | 0/80 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 1/80 | 0/80 | +0.013 | [+0.000, +0.037] | 1 | 0 | 1.0000 |

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
| certain_right | certain | 61/80 | 22/80 | +0.487 | [+0.362, +0.613] | 42 | 3 | 8.65e-10 |
| certain_right | unsure | 32/80 | 5/80 | +0.338 | [+0.212, +0.463] | 30 | 3 | 1.40e-06 |
| unsure_right | certain | 22/80 | 6/80 | +0.200 | [+0.087, +0.325] | 21 | 5 | 0.0025 |
| unsure_right | unsure | 25/80 | 5/80 | +0.250 | [+0.138, +0.362] | 23 | 3 | 8.80e-05 |

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
| anthropic:claude-haiku-5-5 | A | all_certain | certain | 1 | 0.900 | 0.900 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_certain | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| anthropic:claude-haiku-5-5 | A | all_certain_6of8 | unsure | 1 | 0.500 | 0.500 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | all_unsure | certain | 1 | 0.800 | 0.800 | 0.000 | 0.500 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_unsure | unsure | 1 | 0.900 | 0.900 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_unsure_6of8 | certain | 1 | 0.400 | 0.400 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c2_u4 | unsure | 1 | 0.830 | 0.830 | 0.000 | 0.833 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| anthropic:claude-haiku-5-5 | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| anthropic:claude-haiku-5-5 | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c4_u3 | certain | 1 | 0.900 | 0.900 | 1.000 | 0.833 | 0.800 |
| anthropic:claude-haiku-5-5 | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| anthropic:claude-haiku-5-5 | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| anthropic:claude-haiku-5-5 | A | none | unsure | 1 | 0.500 | 0.500 | - | - | - |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | certain | 1 | 0.950 | 0.950 | 1.000 | 0.833 | 0.900 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| anthropic:claude-haiku-5-5 | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| anthropic:claude-haiku-5-5 | A | reliable | unsure | 1 | 0.500 | 0.500 | 0.000 | 0.667 | 0.700 |
| anthropic:claude-haiku-5-5 | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| anthropic:claude-haiku-5-5 | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| anthropic:claude-haiku-5-5 | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| google:gemini-3.6-flash | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| google:gemini-3.6-flash | A | all_certain | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| google:gemini-3.6-flash | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| google:gemini-3.6-flash | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| google:gemini-3.6-flash | A | all_unsure | certain | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| google:gemini-3.6-flash | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| google:gemini-3.6-flash | A | all_unsure_6of8 | certain | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| google:gemini-3.6-flash | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| google:gemini-3.6-flash | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| google:gemini-3.6-flash | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| google:gemini-3.6-flash | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| google:gemini-3.6-flash | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| google:gemini-3.6-flash | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| google:gemini-3.6-flash | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| google:gemini-3.6-flash | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| google:gemini-3.6-flash | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| google:gemini-3.6-flash | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| google:gemini-3.6-flash | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| google:gemini-3.6-flash | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| google:gemini-3.6-flash | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| google:gemini-3.6-flash | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| google:gemini-3.6-flash | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| google:gemini-3.6-flash | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| google:gemini-3.6-flash | A | none | unsure | 1 | 0.500 | 0.500 | - | - | - |
| google:gemini-3.6-flash | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| google:gemini-3.6-flash | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| google:gemini-3.6-flash | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| google:gemini-3.6-flash | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| google:gemini-3.6-flash | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| google:gemini-3.6-flash | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| google:gemini-3.6-flash | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| google:gemini-3.6-flash | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| google:gemini-3.6-flash | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| google:gemini-3.6-flash | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| google:gemini-3.6-flash | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| google:gemini-3.6-flash | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
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
| openai:gpt-6-luna | A | all_certain | certain | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openai:gpt-6-luna | A | all_certain | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.900 |
| openai:gpt-6-luna | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 0.000 | 0.700 | 0.700 |
| openai:gpt-6-luna | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | all_unsure | certain | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openai:gpt-6-luna | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.900 | 0.900 |
| openai:gpt-6-luna | A | all_unsure_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | all_unsure_6of8 | unsure | 1 | 0.750 | 0.750 | 0.000 | 0.700 | 0.700 |
| openai:gpt-6-luna | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openai:gpt-6-luna | A | c3_u4 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openai:gpt-6-luna | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openai:gpt-6-luna | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| openai:gpt-6-luna | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| openai:gpt-6-luna | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| openai:gpt-6-luna | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openai:gpt-6-luna | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openai:gpt-6-luna | A | certain_right_nosum | certain | 1 | 0.750 | 0.750 | 0.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| openai:gpt-6-luna | A | none | unsure | 1 | 0.500 | 0.500 | - | - | - |
| openai:gpt-6-luna | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openai:gpt-6-luna | A | perfect_mixed | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| openai:gpt-6-luna | A | reliable | certain | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openai:gpt-6-luna | A | reliable | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| openai:gpt-6-luna | A | unreliable | certain | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openai:gpt-6-luna | A | unreliable | unsure | 1 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| openai:gpt-6-luna | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| openai:gpt-6-luna | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| openai:gpt-6-luna | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| openai:gpt-6-luna | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
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

| model | arm | cells with a log | RMSE vs independent | RMSE vs pooled |
|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | A | 34 | 0.123 | 0.326 |
| google:gemini-3.6-flash | A | 34 | 0.195 | 0.339 |
| ministral-3:8b | A | 34 | 0.199 | 0.365 |
| openai:gpt-6-luna | A | 34 | 0.178 | 0.345 |
| openrouter:deepseek/deepseek-v3.2 | A | 34 | 0.209 | 0.391 |
| openrouter:mistralai/ministral-14b-2512 | A | 34 | 0.196 | 0.357 |

Curve table (stated probability vs flip rate): 348 points, in the JSON under `curve`.

## Warnings

- probe probabilities read on a 0-100 scale (divided by 100) in: probe__anthropic_claude-haiku-5-5__A.jsonl, probe__google_gemini-3.6-flash__A.jsonl, probe__ministral-3_8b__A.jsonl, probe__openai_gpt-6-luna__A.jsonl, probe__openrouter_deepseek_deepseek-v3.2__A.jsonl, probe__openrouter_mistralai_ministral-14b-2512__A.jsonl
