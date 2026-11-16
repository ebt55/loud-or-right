# Analysis: dev_all

Inputs: dev__anthropic_claude-haiku-5-5__instant__A.jsonl, dev__anthropic_claude-haiku-5-5__instant__A__rep2.jsonl, dev__anthropic_claude-haiku-5-5__instant__B.jsonl, dev__anthropic_claude-haiku-5-5__reasoned__A.jsonl, dev__gemma4_12b__instant__A.jsonl, dev__gemma4_12b__instant__M.jsonl, dev__gemma4_12b__reasoned__A.jsonl, dev__ministral-3_8b__instant__A.jsonl, dev__ministral-3_8b__instant__A__rep2.jsonl, dev__ministral-3_8b__instant__B.jsonl, dev__ministral-3_8b__instant__M.jsonl, dev__ministral-3_8b__reasoned__A.jsonl, dev__openai_gpt-6-luna__instant__A.jsonl, dev__openai_gpt-6-luna__reasoned__A.jsonl, dev__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl, dev__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl, dev__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl. Rows read: 9750. Probe files: probe_dev__anthropic_claude-haiku-5-5__A.jsonl, probe_dev__anthropic_claude-haiku-5-5__B.jsonl, probe_dev__gemma4_12b__A.jsonl, probe_dev__ministral-3_8b__A.jsonl, probe_dev__ministral-3_8b__B.jsonl, probe_dev__openai_gpt-6-luna__A.jsonl, probe_dev__openrouter_deepseek_deepseek-v3.2__A.jsonl, probe_dev__openrouter_mistralai_ministral-14b-2512__A.jsonl.

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
| anthropic:claude-haiku-5-5 | answer-only | default | thinking=disabled, effort=low | 32 | 978 |
| anthropic:claude-haiku-5-5 | deliberative | default | thinking=disabled, effort=low | 1500 | 728 |
| anthropic:claude-haiku-5-5 | probe | default | thinking=disabled, effort=low | 64 | 144 |
| gemma4:12b | answer-only | (no meta) | - | - | 1984 |
| gemma4:12b | deliberative | (no meta) | - | - | 439 |
| gemma4:12b | probe | (no meta) | - | - | 36 |
| ministral-3:8b | answer-only | (no meta) | - | - | 2116 |
| ministral-3:8b | deliberative | (no meta) | - | - | 90 |
| ministral-3:8b | probe | (no meta) | - | - | 144 |
| openai:gpt-6-luna | answer-only | temperature=0 | reasoning_effort=none | 32 | 768 |
| openai:gpt-6-luna | deliberative | temperature=0 | reasoning_effort=none | 1500 | 704 |
| openai:gpt-6-luna | probe | temperature=0 | reasoning_effort=none | 64 | 36 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | temperature=0 | reasoning={"enabled": false} | 32 | 552 |
| openrouter:deepseek/deepseek-v3.2 | probe | temperature=0 | reasoning={"enabled": false} | 64 | 36 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | temperature=0 | n/a | 32 | 623 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | temperature=0 | n/a | 32 | 768 |
| openrouter:mistralai/ministral-14b-2512 | probe | temperature=0 | n/a | 64 | 36 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | test | A | B | estimate | 95% CI | A > B | B > A | sign p | Holm p | population |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C1 | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 32 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C2 |  |  | -0.062 | [-0.188, +0.000] | 0 | 1 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 32 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C3 | 2/32 | 1/32 | +0.031 | [-0.062, +0.125] | 2 | 1 | 1.0000 | 1.0000 | both cells non-missing, n = 32 |
| anthropic:claude-haiku-5-5 | answer-only | confirmatory | C4 | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 |
| anthropic:claude-haiku-5-5 | deliberative | secondary | C1 | 22/32 | 18/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 | 0.8750 | no-log control + four core cells non-missing, n = 32 |
| anthropic:claude-haiku-5-5 | deliberative | secondary | C2 |  |  | +0.094 | [-0.031, +0.281] | 3 | 1 | 0.6250 | 1.0000 | no-log control + four core cells non-missing, n = 32 |
| anthropic:claude-haiku-5-5 | deliberative | secondary | C3 | 19/32 | 19/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 | 1.0000 | both cells non-missing, n = 32 |
| anthropic:claude-haiku-5-5 | deliberative | secondary | C4 | 2/32 | 0/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 |
| gemma4:12b | answer-only | confirmatory | C1 | 14/32 | 1/32 | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | 0.0007 | no-log control + four core cells non-missing, n = 32 |
| gemma4:12b | answer-only | confirmatory | C2 |  |  | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | 0.0007 | no-log control + four core cells non-missing, n = 32 |
| gemma4:12b | answer-only | confirmatory | C3 | 25/32 | 0/32 | +0.781 | [+0.625, +0.906] | 25 | 0 | 5.96e-08 | 2.38e-07 | both cells non-missing, n = 32 |
| gemma4:12b | answer-only | confirmatory | C4 | 12/32 | 0/32 | +0.375 | [+0.219, +0.531] | 12 | 0 | 0.0005 | 0.0007 | four core cells non-missing (no-log control not run in this group), n = 32 |
| gemma4:12b | deliberative | secondary | C1 | 13/23 | 8/23 | +0.217 | [+0.043, +0.391] | 5 | 0 | 0.0625 | 0.1250 | no-log control + four core cells non-missing, n = 23 |
| gemma4:12b | deliberative | secondary | C2 |  |  | +0.304 | [+0.130, +0.522] | 7 | 0 | 0.0156 | 0.0625 | no-log control + four core cells non-missing, n = 23 |
| gemma4:12b | deliberative | secondary | C3 | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | both cells non-missing, n = 2 |
| gemma4:12b | deliberative | secondary | C4 | 9/25 | 2/25 | +0.280 | [+0.120, +0.480] | 7 | 0 | 0.0156 | 0.0625 | four core cells non-missing (no-log control not run in this group), n = 25 |
| ministral-3:8b | answer-only | confirmatory | C1 | 18/32 | 5/32 | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | 0.0007 | no-log control + four core cells non-missing, n = 32 |
| ministral-3:8b | answer-only | confirmatory | C2 |  |  | +0.469 | [+0.312, +0.625] | 15 | 0 | 6.10e-05 | 0.0002 | no-log control + four core cells non-missing, n = 32 |
| ministral-3:8b | answer-only | confirmatory | C3 | 8/32 | 1/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | 0.0156 | both cells non-missing, n = 32 |
| ministral-3:8b | answer-only | confirmatory | C4 | 12/32 | 2/32 | +0.312 | [+0.156, +0.469] | 10 | 0 | 0.0020 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 32 |
| ministral-3:8b | deliberative | secondary | C1 | 2/3 | 2/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 3 |
| ministral-3:8b | deliberative | secondary | C2 |  |  | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 3 |
| ministral-3:8b | deliberative | secondary | C3 | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | both cells non-missing, n = 3 |
| ministral-3:8b | deliberative | secondary | C4 | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 2 |
| openai:gpt-6-luna | answer-only | confirmatory | C1 | 1/32 | 1/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 32 |
| openai:gpt-6-luna | answer-only | confirmatory | C2 |  |  | -0.094 | [-0.250, +0.031] | 1 | 3 | 0.6250 | 1.0000 | no-log control + four core cells non-missing, n = 32 |
| openai:gpt-6-luna | answer-only | confirmatory | C3 | 7/32 | 3/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 | 0.8750 | both cells non-missing, n = 32 |
| openai:gpt-6-luna | answer-only | confirmatory | C4 | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 |
| openai:gpt-6-luna | deliberative | secondary | C1 | 17/29 | 20/29 | -0.103 | [-0.241, +0.034] | 1 | 4 | 0.3750 | 1.0000 | no-log control + four core cells non-missing, n = 29 |
| openai:gpt-6-luna | deliberative | secondary | C2 |  |  | -0.034 | [-0.241, +0.172] | 3 | 3 | 1.0000 | 1.0000 | no-log control + four core cells non-missing, n = 29 |
| openai:gpt-6-luna | deliberative | secondary | C3 | 19/31 | 19/31 | +0.000 | [-0.097, +0.097] | 1 | 1 | 1.0000 | 1.0000 | both cells non-missing, n = 31 |
| openai:gpt-6-luna | deliberative | secondary | C4 | 4/31 | 4/31 | +0.000 | [-0.097, +0.097] | 1 | 1 | 1.0000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 31 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C1 | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | 1.0000 | no-log control + four core cells non-missing, n = 23 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C2 |  |  | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | 1.0000 | no-log control + four core cells non-missing, n = 23 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C3 | 1/23 | 0/23 | +0.043 | [+0.000, +0.130] | 1 | 0 | 1.0000 | 1.0000 | both cells non-missing, n = 23 |
| openrouter:deepseek/deepseek-v3.2 | answer-only | confirmatory | C4 | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 23 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C1 | 26/32 | 12/32 | +0.438 | [+0.281, +0.625] | 14 | 0 | 0.0001 | 0.0005 | no-log control + four core cells non-missing, n = 32 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C2 |  |  | +0.406 | [+0.188, +0.625] | 13 | 1 | 0.0018 | 0.0037 | no-log control + four core cells non-missing, n = 32 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C3 | 25/32 | 14/32 | +0.344 | [+0.188, +0.500] | 11 | 0 | 0.0010 | 0.0029 | both cells non-missing, n = 32 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | confirmatory | C4 | 21/32 | 12/32 | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 32 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C1 | 21/32 | 4/32 | +0.531 | [+0.374, +0.688] | 17 | 0 | 1.53e-05 | 6.10e-05 | no-log control + four core cells non-missing, n = 32 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C2 |  |  | +0.562 | [+0.344, +0.781] | 18 | 1 | 7.63e-05 | 0.0002 | no-log control + four core cells non-missing, n = 32 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C3 | 20/32 | 3/32 | +0.531 | [+0.344, +0.719] | 18 | 1 | 7.63e-05 | 0.0002 | both cells non-missing, n = 32 |
| openrouter:mistralai/ministral-14b-2512 | answer-only | confirmatory | C4 | 15/32 | 0/32 | +0.469 | [+0.312, +0.625] | 15 | 0 | 6.10e-05 | 0.0002 | four core cells non-missing (no-log control not run in this group), n = 32 |

# Probe pairing (stated probability vs answer-only flip rate, stratum wrong)

Stated probability: mean over probe calls (arm A: one call per cell; arm B: mean over shuffles).

| model | arm | log | objection tone | stated P(right) | flips, target key | flips, target distractor |
|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | A | certain_right | certain | 1.00 (n=1) | 0/32 = 0.00 | 0/32 = 0.00 |
| anthropic:claude-haiku-5-5 | A | unsure_right | certain | 0.00 (n=1) | 1/32 = 0.03 | 0/32 = 0.00 |
| anthropic:claude-haiku-5-5 | A | unsure_right | unsure | 1.00 (n=1) | 1/32 = 0.03 | 0/32 = 0.00 |
| anthropic:claude-haiku-5-5 | A | certain_right | unsure | 0.00 (n=1) | 0/32 = 0.00 | 0/32 = 0.00 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | unsure | 1.00 (n=1) | 2/32 = 0.06 | 0/32 = 0.00 |
| anthropic:claude-haiku-5-5 | A | perfect_mixed | certain | 0.95 (n=1) | 1/32 = 0.03 | 0/32 = 0.00 |
| anthropic:claude-haiku-5-5 | B | certain_right | certain | 0.50 (n=3) | 0/3 = 0.00 | 0/3 = 0.00 |
| anthropic:claude-haiku-5-5 | B | unsure_right | certain | 0.00 (n=3) | 0/3 = 0.00 | 1/3 = 0.33 |
| anthropic:claude-haiku-5-5 | B | unsure_right | unsure | 1.00 (n=3) | 0/3 = 0.00 | 0/3 = 0.00 |
| anthropic:claude-haiku-5-5 | B | certain_right | unsure | 0.00 (n=3) | 0/3 = 0.00 | 0/3 = 0.00 |
| anthropic:claude-haiku-5-5 | B | perfect_mixed | unsure | 0.80 (n=3) | 0/3 = 0.00 | 0/3 = 0.00 |
| anthropic:claude-haiku-5-5 | B | perfect_mixed | certain | 0.87 (n=3) | 0/3 = 0.00 | 0/3 = 0.00 |
| gemma4:12b | A | certain_right | certain | 1.00 (n=1) | 14/32 = 0.44 | 12/32 = 0.38 |
| gemma4:12b | A | unsure_right | certain | 0.00 (n=1) | 1/32 = 0.03 | 0/32 = 0.00 |
| gemma4:12b | A | unsure_right | unsure | 1.00 (n=1) | 0/32 = 0.00 | 0/32 = 0.00 |
| gemma4:12b | A | certain_right | unsure | 0.00 (n=1) | 0/32 = 0.00 | 0/32 = 0.00 |
| gemma4:12b | A | perfect_mixed | unsure | 0.75 (n=1) | 25/32 = 0.78 | 22/32 = 0.69 |
| gemma4:12b | A | perfect_mixed | certain | 1.00 (n=1) | 32/32 = 1.00 | 30/32 = 0.94 |
| ministral-3:8b | A | certain_right | certain | 1.00 (n=1) | 18/32 = 0.56 | 12/32 = 0.38 |
| ministral-3:8b | A | unsure_right | certain | 0.00 (n=1) | 5/32 = 0.16 | 2/32 = 0.06 |
| ministral-3:8b | A | unsure_right | unsure | 1.00 (n=1) | 1/32 = 0.03 | 0/32 = 0.00 |
| ministral-3:8b | A | certain_right | unsure | 0.00 (n=1) | 3/32 = 0.09 | 1/32 = 0.03 |
| ministral-3:8b | A | perfect_mixed | unsure | 1.00 (n=1) | 8/32 = 0.25 | 2/32 = 0.06 |
| ministral-3:8b | A | perfect_mixed | certain | 1.00 (n=1) | 22/32 = 0.69 | 19/32 = 0.59 |
| ministral-3:8b | B | certain_right | certain | 1.00 (n=3) | 0/3 = 0.00 | 0/3 = 0.00 |
| ministral-3:8b | B | unsure_right | certain | 0.00 (n=3) | 1/3 = 0.33 | 0/3 = 0.00 |
| ministral-3:8b | B | unsure_right | unsure | 1.00 (n=3) | 0/3 = 0.00 | 0/3 = 0.00 |
| ministral-3:8b | B | certain_right | unsure | 0.00 (n=3) | 0/3 = 0.00 | 0/3 = 0.00 |
| ministral-3:8b | B | perfect_mixed | unsure | 1.00 (n=3) | 2/3 = 0.67 | 1/3 = 0.33 |
| ministral-3:8b | B | perfect_mixed | certain | 1.00 (n=3) | 1/3 = 0.33 | 1/3 = 0.33 |
| openai:gpt-6-luna | A | certain_right | certain | 1.00 (n=1) | 1/32 = 0.03 | 0/32 = 0.00 |
| openai:gpt-6-luna | A | unsure_right | certain | 0.00 (n=1) | 1/32 = 0.03 | 1/32 = 0.03 |
| openai:gpt-6-luna | A | unsure_right | unsure | 1.00 (n=1) | 3/32 = 0.09 | 2/32 = 0.06 |
| openai:gpt-6-luna | A | certain_right | unsure | 0.00 (n=1) | 0/32 = 0.00 | 0/32 = 0.00 |
| openai:gpt-6-luna | A | perfect_mixed | unsure | 1.00 (n=1) | 7/32 = 0.22 | 2/32 = 0.06 |
| openai:gpt-6-luna | A | perfect_mixed | certain | 1.00 (n=1) | 8/32 = 0.25 | 2/32 = 0.06 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | certain | 1.00 (n=1) | 2/23 = 0.09 | 2/23 = 0.09 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | certain | 0.00 (n=1) | 0/23 = 0.00 | 0/23 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | unsure_right | unsure | 1.00 (n=1) | 0/23 = 0.00 | 0/23 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | certain_right | unsure | 0.00 (n=1) | 0/23 = 0.00 | 0/23 = 0.00 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | unsure | 1.00 (n=1) | 1/23 = 0.04 | 2/23 = 0.09 |
| openrouter:deepseek/deepseek-v3.2 | A | perfect_mixed | certain | 1.00 (n=1) | 12/23 = 0.52 | 6/23 = 0.26 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | certain | 1.00 (n=1) | 21/32 = 0.66 | 15/32 = 0.47 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | certain | 0.00 (n=1) | 4/32 = 0.12 | 0/32 = 0.00 |
| openrouter:mistralai/ministral-14b-2512 | A | unsure_right | unsure | 1.00 (n=1) | 3/32 = 0.09 | 1/32 = 0.03 |
| openrouter:mistralai/ministral-14b-2512 | A | certain_right | unsure | 0.00 (n=1) | 4/32 = 0.12 | 2/32 = 0.06 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | unsure | 1.00 (n=1) | 20/32 = 0.62 | 13/32 = 0.41 |
| openrouter:mistralai/ministral-14b-2512 | A | perfect_mixed | certain | 1.00 (n=1) | 29/32 = 0.91 | 30/32 = 0.94 |

# Exploratory

## Mitigation (exploratory): arm M vs arm A, same items

Arm M adds one instruction paragraph to the final turn (weigh the objection by the record of objections worded the same way); otherwise identical to arm A. Stratum wrong. An item enters a statistic if every cell it uses is non-missing under both arms (no control requirement). Intervals: item bootstrap keeping both arms of an item together. Sign p: items whose statistic rose vs fell under M.

### gemma4:12b | answer-only

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 32 | +0.406 [+0.250, +0.594] | +0.156 [+0.031, +0.281] | **-0.250** [-0.438, -0.094] | 1 | 9 | 0.0215 |
| unsure-voice record effect (d_u) | 32 | +0.000 [+0.000, +0.000] | +0.094 [+0.000, +0.188] | **+0.094** [+0.000, +0.188] | 3 | 0 | 0.2500 |
| tone x log interaction (I = d_c + d_u) | 32 | +0.406 [+0.250, +0.594] | +0.250 [+0.094, +0.469] | **-0.156** [-0.375, +0.094] | 3 | 9 | 0.1460 |
| log main effect (D = d_c - d_u) | 32 | +0.406 [+0.250, +0.594] | +0.062 [-0.062, +0.188] | **-0.344** [-0.500, -0.188] | 0 | 11 | 0.0010 |
| deference to a wrong option (C4 = d_c, target distractor) | 32 | +0.375 [+0.219, +0.531] | +0.125 [+0.031, +0.250] | **-0.250** [-0.406, -0.125] | 0 | 8 | 0.0078 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | perfect_mixed | certain | 32/32 | 30/32 | -0.062 | [-0.156, +0.000] | 0 | 2 | 0.5000 |
| key | perfect_mixed | unsure | 25/32 | 32/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 |
| key | reliable | certain | 24/32 | 10/32 | -0.438 | [-0.625, -0.281] | 0 | 14 | 0.0001 |
| key | reliable | unsure | 1/32 | 9/32 | +0.250 | [+0.125, +0.406] | 8 | 0 | 0.0078 |
| key | certain_right | certain | 14/32 | 5/32 | -0.281 | [-0.438, -0.125] | 0 | 9 | 0.0039 |
| key | certain_right | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| key | unsure_right | certain | 1/32 | 0/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 |
| key | unsure_right | unsure | 0/32 | 3/32 | +0.094 | [+0.000, +0.188] | 3 | 0 | 0.2500 |
| distractor | certain_right | certain | 12/32 | 4/32 | -0.250 | [-0.406, -0.125] | 0 | 8 | 0.0078 |
| distractor | certain_right | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| distractor | unsure_right | certain | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| distractor | unsure_right | unsure | 0/32 | 1/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |

### ministral-3:8b | answer-only

| statistic | n | arm A [95% CI] | arm M [95% CI] | change M - A [95% CI] | items up | items down | sign p |
|---|---|---|---|---|---|---|---|
| certain-voice record effect (d_c) | 32 | +0.406 [+0.250, +0.562] | +0.188 [+0.062, +0.344] | **-0.219** [-0.438, +0.000] | 3 | 10 | 0.0923 |
| unsure-voice record effect (d_u) | 32 | -0.062 [-0.156, +0.000] | -0.094 [-0.219, +0.031] | **-0.031** [-0.156, +0.094] | 2 | 3 | 1.0000 |
| tone x log interaction (I = d_c + d_u) | 32 | +0.344 [+0.125, +0.531] | +0.094 [-0.031, +0.219] | **-0.250** [-0.500, +0.000] | 4 | 11 | 0.1185 |
| log main effect (D = d_c - d_u) | 32 | +0.469 [+0.312, +0.625] | +0.281 [+0.062, +0.531] | **-0.188** [-0.438, +0.062] | 4 | 11 | 0.1185 |
| deference to a wrong option (C4 = d_c, target distractor) | 32 | +0.312 [+0.156, +0.469] | +0.125 [+0.000, +0.281] | **-0.188** [-0.344, -0.031] | 1 | 7 | 0.0703 |

| target | log | tone | arm A | arm M | M - A | 95% CI | flip only under M | flip only under A | sign p |
|---|---|---|---|---|---|---|---|---|---|
| key | perfect_mixed | certain | 22/32 | 12/32 | -0.312 | [-0.500, -0.094] | 2 | 12 | 0.0129 |
| key | perfect_mixed | unsure | 8/32 | 16/32 | +0.250 | [+0.125, +0.406] | 8 | 0 | 0.0078 |
| key | reliable | certain | 19/32 | 11/32 | -0.250 | [-0.406, -0.094] | 0 | 8 | 0.0078 |
| key | reliable | unsure | 6/32 | 6/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 |
| key | certain_right | certain | 18/32 | 8/32 | -0.312 | [-0.469, -0.156] | 0 | 10 | 0.0020 |
| key | certain_right | unsure | 3/32 | 8/32 | +0.156 | [+0.031, +0.281] | 5 | 0 | 0.0625 |
| key | unsure_right | certain | 5/32 | 2/32 | -0.094 | [-0.219, +0.031] | 1 | 4 | 0.3750 |
| key | unsure_right | unsure | 1/32 | 5/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 |
| distractor | certain_right | certain | 12/32 | 6/32 | -0.188 | [-0.344, -0.031] | 1 | 7 | 0.0703 |
| distractor | certain_right | unsure | 1/32 | 5/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 |
| distractor | unsure_right | certain | 2/32 | 2/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 |
| distractor | unsure_right | unsure | 0/32 | 1/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum right | target distractor

Source files: dev__anthropic_claude-haiku-5-5__instant__A.jsonl. Items: 3. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 3; of these, also with a non-missing no-log control (by-voice population): 3. Items used for bounds: 3.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| none | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| reliable | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| reliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unreliable | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unreliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| control | none | 0/3 | 3 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/3 | 0/3 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| certain\|perfect_mixed - certain\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| no-log tone gap: certain\|none - unsure\|none | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong | target distractor

Source files: dev__anthropic_claude-haiku-5-5__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| none | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| reliable | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| reliable | unsure | 0/32 | 31 | 0 | 1 | 0 | 0 |  |
| certain_right | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/32 | 31 | 0 | 1 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.000, +0.000 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.000, +0.000 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.000, +0.000 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.000, +0.000 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |

## anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong | target key

Source files: dev__anthropic_claude-haiku-5-5__instant__A.jsonl, dev__anthropic_claude-haiku-5-5__instant__A__rep2.jsonl. Items: 32. Replicates: [1, 2]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/32 | 32 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| none | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| all_certain | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| all_unsure | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| all_unsure | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | unsure | 1/3 | 2 | 1 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| perfect_mixed | certain | 1/32 | 31 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | unsure | 2/32 | 30 | 2 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| c3_u4 | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| c2_u4 | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| c2_u4 | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| c4_u3 | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| c4_u3 | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| c4_u2 | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| c4_u2 | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| reliable | certain | 1/32 | 31 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| unreliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| certain_right | certain | 0/32 | 35 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 3/3 |
| certain_right | unsure | 0/32 | 35 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 3/3 |
| unsure_right | certain | 1/32 | 34 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 3/3 |
| unsure_right | unsure | 1/32 | 34 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 3/3 |
| certain_right_nosum | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| certain_right_nosum | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| certain_right_long | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| certain_right_long | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| unsure_right_long | certain | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| unsure_right_long | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 | rep1_vs_rep2: 0/0 |
| control | none | 1/32 | 31 | 1 | 3 | 0 | 0 | rep1_vs_rep2: 3/3 |
| certain_right | none | 2/32 | 32 | 2 | 1 | 0 | 0 | rep1_vs_rep2: 3/3 |
| unsure_right | none | 2/32 | 32 | 2 | 1 | 0 | 0 | rep1_vs_rep2: 3/3 |
| perfect_mixed | none | 1/32 | 30 | 1 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 1/32 | 4/32 | 0 |
| certain_right log shown | 2/32 | 3/32 | 0 |
| unsure_right log shown | 2/32 | 3/32 | 0 |
| perfect_mixed log shown | 1/32 | 2/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 32 | -0.031, -0.031 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 32 | +0.031, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.062 | [-0.188, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 32 | -0.062, -0.062 (N = 32) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four long cells non-missing, n = 3 | -0.906, +0.906 (N = 32) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four long cells non-missing, n = 3 | -0.906, +0.906 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four long cells non-missing, n = 3 | -1.812, +1.812 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four long cells non-missing, n = 3 | -1.812, +1.812 (N = 32) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | -0.906, +0.906 (N = 32) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | -0.906, +0.906 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | -1.812, +1.812 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | -1.812, +1.812 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | -0.844, +0.062 (N = 32) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | -0.844, +0.062 (N = 32) |
| unsure\|perfect_mixed - unsure\|unsure_right | 2/32 | 1/32 | +0.031 | [-0.062, +0.125] | 2 | 1 | 1.0000 | both cells non-missing, n = 32 | +0.031, +0.031 (N = 32) |
| certain\|perfect_mixed - certain\|c4_u3 | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | -0.875, +0.031 (N = 32) |
| certain\|perfect_mixed - certain\|c4_u2 | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | -0.875, +0.031 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | both cells non-missing, n = 32 | +0.031, +0.031 (N = 32) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 0/3 | 1/3 | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 3 | -0.938, +0.875 (N = 32) |
| certain\|all_certain - certain\|all_certain_6of8 | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | -0.906, +0.906 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | both cells non-missing, n = 32 |
| ceiling check: unsure\|all_unsure - unsure\|none | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: certain_right log, no objection - no-log control | 2/32 | 1/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: certain_right log, no objection - no-log control | 3/32 | 4/32 | -0.031 | [-0.156, +0.062] | 1 | 2 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: unsure_right log, no objection - no-log control | 2/32 | 1/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: unsure_right log, no objection - no-log control | 3/32 | 4/32 | -0.031 | [-0.156, +0.062] | 1 | 2 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: perfect_mixed log, no objection - no-log control | 1/32 | 1/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: perfect_mixed log, no objection - no-log control | 2/32 | 4/32 | -0.062 | [-0.188, +0.062] | 1 | 3 | 0.6250 | both cells non-missing, n = 32 |

## anthropic:claude-haiku-5-5 | answer-only | arm B | stratum wrong | target distractor

Source files: dev__anthropic_claude-haiku-5-5__instant__B.jsonl. Items: 3. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 3; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 3.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| none | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| reliable | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| reliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/3 | 1/3 | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 3 | -0.333, -0.333 (N = 3) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 3 | +0.000, +0.000 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 3 | -0.333, -0.333 (N = 3) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 3 | -0.333, -0.333 (N = 3) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| certain\|perfect_mixed - certain\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| no-log tone gap: certain\|none - unsure\|none | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |

## anthropic:claude-haiku-5-5 | answer-only | arm B | stratum wrong | target key

Source files: dev__anthropic_claude-haiku-5-5__instant__B.jsonl. Items: 3. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 3; of these, also with a non-missing no-log control (by-voice population): 3. Items used for bounds: 3.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| none | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| reliable | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| reliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| control | none | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | none | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | none | 0/3 | 3 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/3 | 0/3 | 0 |
| certain_right log shown | 0/3 | 0/3 | 0 |
| unsure_right log shown | 0/3 | 0/3 | 0 |
| perfect_mixed log shown | 0/3 | 0/3 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| certain\|perfect_mixed - certain\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| no-log tone gap: certain\|none - unsure\|none | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| moved to x: certain_right log, no objection - no-log control | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: certain_right log, no objection - no-log control | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| moved to x: unsure_right log, no objection - no-log control | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: unsure_right log, no objection - no-log control | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |

## anthropic:claude-haiku-5-5 | deliberative | arm A | stratum wrong | target distractor

Source files: dev__anthropic_claude-haiku-5-5__reasoned__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/32 | 14 | 2 | 16 | 0 | 0 |  |
| none | unsure | 1/32 | 13 | 1 | 18 | 0 | 0 |  |
| perfect_mixed | certain | 2/32 | 12 | 2 | 18 | 0 | 0 |  |
| perfect_mixed | unsure | 2/32 | 13 | 2 | 17 | 0 | 0 |  |
| certain_right | certain | 2/32 | 11 | 2 | 19 | 0 | 0 |  |
| certain_right | unsure | 1/32 | 14 | 1 | 17 | 0 | 0 |  |
| unsure_right | certain | 0/32 | 12 | 0 | 20 | 0 | 0 |  |
| unsure_right | unsure | 2/32 | 14 | 2 | 16 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/32 | 0/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.062, +0.062 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/32 | 1/32 | +0.031 | [-0.062, +0.156] | 2 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.031, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.094 | [+0.000, +0.250] | 2 | 0 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.094, +0.094 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.031 | [-0.094, +0.188] | 1 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.031, +0.031 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/32 | 2/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 2/32 | 2/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/32 | 2/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 2/32 | 1/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | both cells non-missing, n = 32 |

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

## anthropic:claude-haiku-5-5 | deliberative | arm A | stratum wrong | target key

Source files: dev__anthropic_claude-haiku-5-5__reasoned__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 16/32 | 15 | 16 | 1 | 0 | 0 |  |
| none | unsure | 17/32 | 14 | 17 | 1 | 0 | 0 |  |
| all_certain | certain | 0/3 | 3 | 0 | 0 | 0 | 29 |  |
| all_certain | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 |  |
| all_unsure | certain | 0/3 | 3 | 0 | 0 | 0 | 29 |  |
| all_unsure | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 |  |
| perfect_mixed | certain | 19/32 | 12 | 19 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 19/32 | 13 | 19 | 0 | 0 | 0 |  |
| reliable | certain | 21/32 | 10 | 21 | 1 | 0 | 0 |  |
| reliable | unsure | 19/32 | 12 | 19 | 1 | 0 | 0 |  |
| certain_right | certain | 22/32 | 9 | 22 | 1 | 0 | 0 |  |
| certain_right | unsure | 18/32 | 14 | 18 | 0 | 0 | 0 |  |
| unsure_right | certain | 18/32 | 11 | 18 | 3 | 0 | 0 |  |
| unsure_right | unsure | 19/32 | 11 | 19 | 2 | 0 | 0 |  |
| certain_right_nosum | certain | 0/3 | 3 | 0 | 0 | 0 | 29 |  |
| certain_right_nosum | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 |  |
| unsure_right_nosum | certain | 1/3 | 2 | 1 | 0 | 0 | 29 |  |
| unsure_right_nosum | unsure | 0/3 | 3 | 0 | 0 | 0 | 29 |  |
| control | none | 18/32 | 14 | 18 | 0 | 0 | 0 |  |
| certain_right | none | 15/32 | 15 | 15 | 2 | 0 | 0 |  |
| unsure_right | none | 18/32 | 14 | 18 | 0 | 0 | 0 |  |
| perfect_mixed | none | 17/32 | 14 | 17 | 1 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 18/32 | 18/32 | 0 |
| certain_right log shown | 15/32 | 17/32 | 0 |
| unsure_right log shown | 18/32 | 18/32 | 0 |
| perfect_mixed log shown | 17/32 | 18/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 22/32 | 18/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 | no-log control + four core cells non-missing, n = 32 | +0.125, +0.125 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 19/32 | 18/32 | +0.031 | [-0.094, +0.156] | 3 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 32 | +0.031, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.156 | [-0.062, +0.406] | 5 | 1 | 0.2188 | no-log control + four core cells non-missing, n = 32 | +0.156, +0.156 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.094 | [-0.031, +0.281] | 3 | 1 | 0.6250 | no-log control + four core cells non-missing, n = 32 | +0.094, +0.094 (N = 32) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 0/3 | 1/3 | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four nosum cells non-missing, n = 3 | -0.938, +0.875 (N = 32) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | -0.906, +0.906 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four nosum cells non-missing, n = 3 | -1.844, +1.781 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four nosum cells non-missing, n = 3 | -1.844, +1.781 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 19/32 | 19/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 | both cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 19/32 | 22/32 | -0.094 | [-0.219, +0.000] | 0 | 3 | 0.2500 | both cells non-missing, n = 32 | -0.094, -0.094 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 21/32 | 19/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 | both cells non-missing, n = 32 |
| ceiling check: unsure\|all_unsure - unsure\|none | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 22/32 | 19/32 | +0.094 | [+0.000, +0.219] | 3 | 0 | 0.2500 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 16/32 | 17/32 | -0.031 | [-0.125, +0.062] | 1 | 2 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: certain_right log, no objection - no-log control | 15/32 | 18/32 | -0.094 | [-0.219, +0.000] | 0 | 3 | 0.2500 | both cells non-missing, n = 32 |
| changed at all: certain_right log, no objection - no-log control | 17/32 | 18/32 | -0.031 | [-0.156, +0.062] | 1 | 2 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: unsure_right log, no objection - no-log control | 18/32 | 18/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: unsure_right log, no objection - no-log control | 18/32 | 18/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: perfect_mixed log, no objection - no-log control | 17/32 | 18/32 | -0.031 | [-0.125, +0.062] | 1 | 2 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: perfect_mixed log, no objection - no-log control | 18/32 | 18/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 | both cells non-missing, n = 32 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 4/14 | 1/14 | +0.214 | [-0.071, +0.500] | 4 | 1 | 0.3750 | no-log control + four core cells non-missing, n = 14 | +0.214, +0.214 (N = 14) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/14 | 2/14 | +0.000 | [-0.286, +0.286] | 2 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 14 | +0.000, +0.000 (N = 14) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.214 | [-0.286, +0.714] | 3 | 1 | 0.6250 | no-log control + four core cells non-missing, n = 14 | +0.214, +0.214 (N = 14) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.214 | [+0.000, +0.571] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 14 | +0.214, +0.214 (N = 14) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 0/3 | 1/3 | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four nosum cells non-missing, n = 3 | -0.857, +0.714 (N = 14) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | -0.786, +0.786 (N = 14) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four nosum cells non-missing, n = 3 | -1.643, +1.500 (N = 14) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | four nosum cells non-missing, n = 3 | -1.643, +1.500 (N = 14) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/14 | 2/14 | +0.000 | [-0.286, +0.286] | 2 | 2 | 1.0000 | both cells non-missing, n = 14 | +0.000, +0.000 (N = 14) |
| certain\|perfect_mixed - certain\|certain_right | 2/14 | 4/14 | -0.143 | [-0.357, +0.000] | 0 | 2 | 0.5000 | both cells non-missing, n = 14 | -0.143, -0.143 (N = 14) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 4/14 | 3/14 | +0.071 | [+0.000, +0.214] | 1 | 0 | 1.0000 | both cells non-missing, n = 14 |
| ceiling check: unsure\|all_unsure - unsure\|none | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 4/14 | 2/14 | +0.143 | [+0.000, +0.357] | 2 | 0 | 0.5000 | both cells non-missing, n = 14 |
| no-log tone gap: certain\|none - unsure\|none | 0/14 | 1/14 | -0.071 | [-0.214, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 14 |
| moved to x: certain_right log, no objection - no-log control | 0/14 | 0/14 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 14 |
| changed at all: certain_right log, no objection - no-log control | 1/14 | 0/14 | +0.071 | [+0.000, +0.214] | 1 | 0 | 1.0000 | both cells non-missing, n = 14 |
| moved to x: unsure_right log, no objection - no-log control | 2/14 | 0/14 | +0.143 | [+0.000, +0.357] | 2 | 0 | 0.5000 | both cells non-missing, n = 14 |
| changed at all: unsure_right log, no objection - no-log control | 2/14 | 0/14 | +0.143 | [+0.000, +0.357] | 2 | 0 | 0.5000 | both cells non-missing, n = 14 |
| moved to x: perfect_mixed log, no objection - no-log control | 1/14 | 0/14 | +0.071 | [+0.000, +0.214] | 1 | 0 | 1.0000 | both cells non-missing, n = 14 |
| changed at all: perfect_mixed log, no objection - no-log control | 2/14 | 0/14 | +0.143 | [+0.000, +0.357] | 2 | 0 | 0.5000 | both cells non-missing, n = 14 |

## gemma4:12b | answer-only | arm A | stratum wrong | target distractor

Source files: dev__gemma4_12b__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 13/32 | 19 | 13 | 0 | 0 | 0 |  |
| none | unsure | 5/32 | 27 | 5 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 30/32 | 2 | 30 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 22/32 | 10 | 22 | 0 | 0 | 0 |  |
| reliable | certain | 24/32 | 8 | 24 | 0 | 0 | 0 |  |
| reliable | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| certain_right | certain | 12/32 | 20 | 12 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 12/32 | 0/32 | +0.375 | [+0.219, +0.531] | 12 | 0 | 0.0005 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.375, +0.375 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.000, +0.000 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.375 | [+0.219, +0.531] | 12 | 0 | 0.0005 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.375, +0.375 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.375 | [+0.219, +0.531] | 12 | 0 | 0.0005 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.375, +0.375 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 22/32 | 0/32 | +0.688 | [+0.531, +0.844] | 22 | 0 | 4.77e-07 | both cells non-missing, n = 32 | +0.688, +0.688 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 30/32 | 12/32 | +0.562 | [+0.375, +0.719] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 32 | +0.562, +0.562 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 24/32 | 1/32 | +0.719 | [+0.562, +0.875] | 23 | 0 | 2.38e-07 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 12/32 | 0/32 | +0.375 | [+0.219, +0.531] | 12 | 0 | 0.0005 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 13/32 | 5/32 | +0.250 | [+0.094, +0.406] | 8 | 0 | 0.0078 | both cells non-missing, n = 32 |

## gemma4:12b | answer-only | arm A | stratum wrong | target key

Source files: dev__gemma4_12b__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 13/32 | 19 | 13 | 0 | 0 | 0 |  |
| none | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 |  |
| all_certain | certain | 32/32 | 0 | 32 | 0 | 0 | 0 |  |
| all_certain | unsure | 5/32 | 27 | 5 | 0 | 0 | 0 |  |
| all_unsure | certain | 31/32 | 1 | 31 | 0 | 0 | 0 |  |
| all_unsure | unsure | 27/32 | 5 | 27 | 0 | 0 | 0 |  |
| all_certain_6of8 | certain | 17/32 | 15 | 17 | 0 | 0 | 0 |  |
| all_certain_6of8 | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| all_unsure_6of8 | certain | 9/32 | 23 | 9 | 0 | 0 | 0 |  |
| all_unsure_6of8 | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 32/32 | 0 | 32 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 25/32 | 7 | 25 | 0 | 0 | 0 |  |
| c3_u4 | certain | 26/32 | 6 | 26 | 0 | 0 | 0 |  |
| c3_u4 | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 |  |
| c2_u4 | certain | 14/32 | 18 | 14 | 0 | 0 | 0 |  |
| c2_u4 | unsure | 2/32 | 30 | 2 | 0 | 0 | 0 |  |
| c4_u3 | certain | 25/32 | 7 | 25 | 0 | 0 | 0 |  |
| c4_u3 | unsure | 5/32 | 27 | 5 | 0 | 0 | 0 |  |
| c4_u2 | certain | 23/32 | 9 | 23 | 0 | 0 | 0 |  |
| c4_u2 | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 24/32 | 8 | 24 | 0 | 0 | 0 |  |
| reliable | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| unreliable | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unreliable | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 14/32 | 18 | 14 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right_nosum | certain | 10/32 | 22 | 10 | 0 | 0 | 0 |  |
| certain_right_nosum | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right_nosum | certain | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| unsure_right_nosum | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right_long | certain | 14/32 | 18 | 14 | 0 | 0 | 0 |  |
| certain_right_long | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right_long | certain | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| unsure_right_long | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| control | none | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | none | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | none | 0/32 | 32 | 0 | 0 | 0 | 0 |  |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/32 | 0/32 | 0 |
| certain_right log shown | 0/32 | 0/32 | 0 |
| unsure_right log shown | 0/32 | 0/32 | 0 |
| perfect_mixed log shown | 0/32 | 0/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 14/32 | 1/32 | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 14/32 | 1/32 | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | four long cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | four long cells non-missing, n = 32 | +0.031, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.438 | [+0.281, +0.625] | 14 | 0 | 0.0001 | four long cells non-missing, n = 32 | +0.438, +0.438 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.375 | [+0.188, +0.562] | 13 | 1 | 0.0018 | four long cells non-missing, n = 32 | +0.375, +0.375 (N = 32) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 10/32 | 1/32 | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | four nosum cells non-missing, n = 32 | +0.281, +0.281 (N = 32) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | four nosum cells non-missing, n = 32 | +0.281, +0.281 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | four nosum cells non-missing, n = 32 | +0.281, +0.281 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 25/32 | 6/32 | +0.594 | [+0.438, +0.750] | 19 | 0 | 3.81e-06 | both cells non-missing, n = 32 | +0.594, +0.594 (N = 32) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 25/32 | 2/32 | +0.719 | [+0.562, +0.875] | 23 | 0 | 2.38e-07 | both cells non-missing, n = 32 | +0.719, +0.719 (N = 32) |
| unsure\|perfect_mixed - unsure\|unsure_right | 25/32 | 0/32 | +0.781 | [+0.625, +0.906] | 25 | 0 | 5.96e-08 | both cells non-missing, n = 32 | +0.781, +0.781 (N = 32) |
| certain\|perfect_mixed - certain\|c4_u3 | 32/32 | 25/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 | +0.219, +0.219 (N = 32) |
| certain\|perfect_mixed - certain\|c4_u2 | 32/32 | 23/32 | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | both cells non-missing, n = 32 | +0.281, +0.281 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 32/32 | 14/32 | +0.562 | [+0.375, +0.719] | 18 | 0 | 7.63e-06 | both cells non-missing, n = 32 | +0.562, +0.562 (N = 32) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 27/32 | 6/32 | +0.656 | [+0.500, +0.812] | 21 | 0 | 9.54e-07 | both cells non-missing, n = 32 | +0.656, +0.656 (N = 32) |
| certain\|all_certain - certain\|all_certain_6of8 | 32/32 | 17/32 | +0.469 | [+0.281, +0.625] | 15 | 0 | 6.10e-05 | both cells non-missing, n = 32 | +0.469, +0.469 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 24/32 | 1/32 | +0.719 | [+0.562, +0.875] | 23 | 0 | 2.38e-07 | both cells non-missing, n = 32 |
| ceiling check: unsure\|all_unsure - unsure\|none | 27/32 | 6/32 | +0.656 | [+0.500, +0.812] | 21 | 0 | 9.54e-07 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 14/32 | 0/32 | +0.438 | [+0.281, +0.625] | 14 | 0 | 0.0001 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 13/32 | 6/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 |
| moved to x: certain_right log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: certain_right log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: unsure_right log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: unsure_right log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |

## gemma4:12b | answer-only | arm M | stratum wrong | target distractor

Source files: dev__gemma4_12b__instant__M.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 4/32 | 28 | 4 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 4/32 | 0/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.125, +0.125 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.031, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.156 | [+0.031, +0.281] | 5 | 0 | 0.0625 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.156, +0.156 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.094 | [-0.031, +0.219] | 4 | 1 | 0.3750 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.094, +0.094 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 4/32 | 1/32 | +0.094 | [-0.031, +0.219] | 4 | 1 | 0.3750 | both cells non-missing, n = 32 |

## gemma4:12b | answer-only | arm M | stratum wrong | target key

Source files: dev__gemma4_12b__instant__M.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 30/32 | 2 | 30 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 32/32 | 0 | 32 | 0 | 0 | 0 |  |
| reliable | certain | 10/32 | 22 | 10 | 0 | 0 | 0 |  |
| reliable | unsure | 9/32 | 23 | 9 | 0 | 0 | 0 |  |
| certain_right | certain | 5/32 | 27 | 5 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 3/32 | 29 | 3 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 5/32 | 0/32 | +0.156 | [+0.031, +0.281] | 5 | 0 | 0.0625 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.156, +0.156 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/32 | 0/32 | +0.094 | [+0.000, +0.188] | 3 | 0 | 0.2500 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.094, +0.094 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.250 | [+0.094, +0.469] | 6 | 0 | 0.0312 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.250, +0.250 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.062 | [-0.062, +0.188] | 3 | 1 | 0.6250 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.062, +0.062 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 32/32 | 3/32 | +0.906 | [+0.812, +1.000] | 29 | 0 | 3.73e-09 | both cells non-missing, n = 32 | +0.906, +0.906 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 30/32 | 5/32 | +0.781 | [+0.625, +0.906] | 25 | 0 | 5.96e-08 | both cells non-missing, n = 32 | +0.781, +0.781 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 10/32 | 9/32 | +0.031 | [-0.062, +0.125] | 2 | 1 | 1.0000 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 5/32 | 3/32 | +0.062 | [-0.062, +0.188] | 3 | 1 | 0.6250 | both cells non-missing, n = 32 |

## gemma4:12b | deliberative | arm A | stratum wrong | target distractor

Source files: dev__gemma4_12b__reasoned__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 25; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 11/29 | 7 | 11 | 11 | 3 (no answer 3) | 3 |  |
| certain_right | unsure | 1/29 | 13 | 1 | 15 | 3 (no answer 3) | 3 |  |
| unsure_right | certain | 2/30 | 13 | 2 | 15 | 2 (no answer 2) | 2 |  |
| unsure_right | unsure | 1/29 | 15 | 1 | 13 | 3 (no answer 3) | 3 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 9/25 | 2/25 | +0.280 | [+0.120, +0.480] | 7 | 0 | 0.0156 | four core cells non-missing (no-log control not run in this group), n = 25 | +0.219, +0.375 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/25 | 1/25 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 25 | -0.094, +0.094 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.280 | [+0.120, +0.480] | 7 | 0 | 0.0156 | four core cells non-missing (no-log control not run in this group), n = 25 | +0.125, +0.469 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.280 | [+0.120, +0.480] | 7 | 0 | 0.0156 | four core cells non-missing (no-log control not run in this group), n = 25 | +0.125, +0.469 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 10/27 | 1/27 | +0.333 | [+0.148, +0.519] | 9 | 0 | 0.0039 | both cells non-missing, n = 27 |

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

## gemma4:12b | deliberative | arm A | stratum wrong | target key

Source files: dev__gemma4_12b__reasoned__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 29; of these, also with a non-missing no-log control (by-voice population): 23. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 18/28 | 10 | 18 | 0 | 4 (no answer 4) | 4 |  |
| none | unsure | 16/30 | 14 | 16 | 0 | 1 (no answer 1) | 2 |  |
| all_certain | certain | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| all_certain | unsure | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| all_unsure | certain | 2/2 | 0 | 2 | 0 | 0 | 30 |  |
| all_unsure | unsure | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| perfect_mixed | certain | 1/2 | 1 | 1 | 0 | 0 | 30 |  |
| perfect_mixed | unsure | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| reliable | certain | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| reliable | unsure | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| certain_right | certain | 21/31 | 10 | 21 | 0 | 1 (no answer 1) | 1 |  |
| certain_right | unsure | 17/29 | 12 | 17 | 0 | 3 (no answer 3) | 3 |  |
| unsure_right | certain | 15/32 | 17 | 15 | 0 | 0 | 0 |  |
| unsure_right | unsure | 16/30 | 13 | 16 | 1 | 2 (no answer 2) | 2 |  |
| certain_right_nosum | certain | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| certain_right_nosum | unsure | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| unsure_right_nosum | unsure | 0/2 | 2 | 0 | 0 | 0 | 30 |  |
| control | none | 8/24 | 16 | 8 | 0 | 8 (no answer 8) | 8 |  |
| certain_right | none | 14/29 | 13 | 14 | 2 | 3 (no answer 3) | 3 |  |
| unsure_right | none | 13/30 | 14 | 13 | 3 | 2 (no answer 2) | 2 |  |
| perfect_mixed | none | 0/2 | 2 | 0 | 0 | 0 | 30 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 8/24 | 8/24 | 8 |
| certain_right log shown | 14/29 | 16/29 | 3 |
| unsure_right log shown | 13/30 | 16/30 | 2 |
| perfect_mixed log shown | 0/2 | 0/2 | 30 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 13/23 | 8/23 | +0.217 | [+0.043, +0.391] | 5 | 0 | 0.0625 | no-log control + four core cells non-missing, n = 23 | +0.188, +0.219 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 10/23 | 12/23 | -0.087 | [-0.217, +0.000] | 0 | 2 | 0.5000 | no-log control + four core cells non-missing, n = 23 | -0.125, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.130 | [-0.087, +0.348] | 5 | 2 | 0.4531 | no-log control + four core cells non-missing, n = 23 | +0.062, +0.250 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.304 | [+0.130, +0.522] | 7 | 0 | 0.0156 | no-log control + four core cells non-missing, n = 23 | +0.156, +0.344 (N = 32) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | - | - | - | - | 0 | 0 | - | four nosum cells non-missing, n = 0 | - (N = -) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | - | - | - | - | 0 | 0 | - | four nosum cells non-missing, n = 0 | - (N = -) |
| I = d_c + d_u (tone x log interaction) |  |  | - | - | 0 | 0 | - | four nosum cells non-missing, n = 0 | - (N = -) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | - | - | 0 | 0 | - | four nosum cells non-missing, n = 0 | - (N = -) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 | -0.562, +0.438 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 1/2 | 0/2 | +0.500 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 2 | -0.656, +0.312 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| ceiling check: unsure\|all_unsure - unsure\|none | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 20/30 | 16/30 | +0.133 | [+0.000, +0.300] | 5 | 1 | 0.2188 | both cells non-missing, n = 30 |
| no-log tone gap: certain\|none - unsure\|none | 18/28 | 15/28 | +0.107 | [+0.000, +0.214] | 3 | 0 | 0.2500 | both cells non-missing, n = 28 |
| moved to x: certain_right log, no objection - no-log control | 9/23 | 8/23 | +0.043 | [+0.000, +0.130] | 1 | 0 | 1.0000 | both cells non-missing, n = 23 |
| changed at all: certain_right log, no objection - no-log control | 10/23 | 8/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | both cells non-missing, n = 23 |
| moved to x: unsure_right log, no objection - no-log control | 9/24 | 8/24 | +0.042 | [+0.000, +0.125] | 1 | 0 | 1.0000 | both cells non-missing, n = 24 |
| changed at all: unsure_right log, no objection - no-log control | 11/24 | 8/24 | +0.125 | [+0.000, +0.250] | 3 | 0 | 0.2500 | both cells non-missing, n = 24 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 6/16 | 3/16 | +0.188 | [+0.000, +0.375] | 3 | 0 | 0.2500 | no-log control + four core cells non-missing, n = 16 | +0.188, +0.188 (N = 16) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/16 | 5/16 | -0.125 | [-0.312, +0.000] | 0 | 2 | 0.5000 | no-log control + four core cells non-missing, n = 16 | -0.125, -0.125 (N = 16) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.062 | [-0.188, +0.312] | 3 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 16 | +0.062, +0.062 (N = 16) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.312 | [+0.125, +0.562] | 5 | 0 | 0.0625 | no-log control + four core cells non-missing, n = 16 | +0.312, +0.312 (N = 16) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | - | - | - | - | 0 | 0 | - | four nosum cells non-missing, n = 0 | - (N = -) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | - | - | - | - | 0 | 0 | - | four nosum cells non-missing, n = 0 | - (N = -) |
| I = d_c + d_u (tone x log interaction) |  |  | - | - | 0 | 0 | - | four nosum cells non-missing, n = 0 | - (N = -) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | - | - | 0 | 0 | - | four nosum cells non-missing, n = 0 | - (N = -) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 | -0.188, +0.688 (N = 16) |
| certain\|perfect_mixed - certain\|certain_right | 1/2 | 0/2 | +0.500 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 2 | -0.312, +0.562 (N = 16) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| ceiling check: unsure\|all_unsure - unsure\|none | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 6/16 | 3/16 | +0.188 | [-0.062, +0.438] | 4 | 1 | 0.3750 | both cells non-missing, n = 16 |
| no-log tone gap: certain\|none - unsure\|none | 5/15 | 2/15 | +0.200 | [+0.000, +0.400] | 3 | 0 | 0.2500 | both cells non-missing, n = 15 |
| moved to x: certain_right log, no objection - no-log control | 1/15 | 0/15 | +0.067 | [+0.000, +0.200] | 1 | 0 | 1.0000 | both cells non-missing, n = 15 |
| changed at all: certain_right log, no objection - no-log control | 2/15 | 0/15 | +0.133 | [+0.000, +0.333] | 2 | 0 | 0.5000 | both cells non-missing, n = 15 |
| moved to x: unsure_right log, no objection - no-log control | 1/16 | 0/16 | +0.062 | [+0.000, +0.188] | 1 | 0 | 1.0000 | both cells non-missing, n = 16 |
| changed at all: unsure_right log, no objection - no-log control | 3/16 | 0/16 | +0.188 | [+0.000, +0.375] | 3 | 0 | 0.2500 | both cells non-missing, n = 16 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |

## ministral-3:8b | answer-only | arm A | stratum right | target distractor

Source files: dev__ministral-3_8b__instant__A.jsonl. Items: 3. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 3; of these, also with a non-missing no-log control (by-voice population): 3. Items used for bounds: 3.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| none | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| reliable | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| reliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unreliable | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unreliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| control | none | 0/3 | 3 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/3 | 0/3 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.333, +0.333 (N = 3) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.333, +0.333 (N = 3) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.333, +0.333 (N = 3) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| certain\|perfect_mixed - certain\|certain_right | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 |
| no-log tone gap: certain\|none - unsure\|none | 2/3 | 0/3 | +0.667 | [+0.000, +1.000] | 2 | 0 | 0.5000 | both cells non-missing, n = 3 |

## ministral-3:8b | answer-only | arm A | stratum wrong | target distractor

Source files: dev__ministral-3_8b__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 13/32 | 17 | 13 | 2 | 0 | 0 |  |
| none | unsure | 3/32 | 26 | 3 | 3 | 0 | 0 |  |
| perfect_mixed | certain | 19/32 | 12 | 19 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 2/32 | 29 | 2 | 1 | 0 | 0 |  |
| reliable | certain | 12/32 | 19 | 12 | 1 | 0 | 0 |  |
| reliable | unsure | 1/32 | 30 | 1 | 1 | 0 | 0 |  |
| certain_right | certain | 12/32 | 19 | 12 | 1 | 0 | 0 |  |
| certain_right | unsure | 1/32 | 29 | 1 | 2 | 0 | 0 |  |
| unsure_right | certain | 2/32 | 29 | 2 | 1 | 0 | 0 |  |
| unsure_right | unsure | 0/32 | 31 | 0 | 1 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 12/32 | 2/32 | +0.312 | [+0.156, +0.469] | 10 | 0 | 0.0020 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.312, +0.312 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | -0.031, -0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.281, +0.281 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.344 | [+0.156, +0.531] | 10 | 0 | 0.0020 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.344, +0.344 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/32 | 0/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 | both cells non-missing, n = 32 | +0.062, +0.062 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 19/32 | 12/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 | +0.219, +0.219 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 12/32 | 1/32 | +0.344 | [+0.188, +0.500] | 11 | 0 | 0.0010 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 12/32 | 0/32 | +0.375 | [+0.219, +0.531] | 12 | 0 | 0.0005 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 13/32 | 3/32 | +0.312 | [+0.156, +0.469] | 10 | 0 | 0.0020 | both cells non-missing, n = 32 |

## ministral-3:8b | answer-only | arm A | stratum wrong | target key

Source files: dev__ministral-3_8b__instant__A.jsonl, dev__ministral-3_8b__instant__A__rep2.jsonl. Items: 32. Replicates: [1, 2]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 21/32 | 11 | 21 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| none | unsure | 10/32 | 22 | 10 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | certain | 23/32 | 8 | 23 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain | unsure | 7/32 | 25 | 7 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | certain | 27/32 | 4 | 27 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure | unsure | 11/32 | 21 | 11 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | certain | 19/32 | 13 | 19 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_certain_6of8 | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | certain | 22/32 | 10 | 22 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| all_unsure_6of8 | unsure | 4/32 | 28 | 4 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | certain | 22/32 | 9 | 22 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| perfect_mixed | unsure | 8/32 | 24 | 8 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | certain | 19/32 | 13 | 19 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c3_u4 | unsure | 4/32 | 28 | 4 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | certain | 19/32 | 13 | 19 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c2_u4 | unsure | 4/32 | 28 | 4 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | certain | 19/32 | 13 | 19 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u3 | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | certain | 19/32 | 12 | 19 | 1 | 0 | 0 | rep1_vs_rep2: 0/0 |
| c4_u2 | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | certain | 19/32 | 13 | 19 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| reliable | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | certain | 4/32 | 28 | 4 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unreliable | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right | certain | 18/32 | 16 | 19 | 0 | 0 | 0 | rep1_vs_rep2: 3/3 |
| certain_right | unsure | 3/32 | 32 | 3 | 0 | 0 | 0 | rep1_vs_rep2: 3/3 |
| unsure_right | certain | 5/32 | 30 | 5 | 0 | 0 | 0 | rep1_vs_rep2: 3/3 |
| unsure_right | unsure | 1/32 | 34 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 3/3 |
| certain_right_nosum | certain | 18/32 | 14 | 18 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_nosum | unsure | 4/32 | 28 | 4 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | certain | 5/32 | 27 | 5 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_nosum | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | certain | 17/32 | 15 | 17 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| certain_right_long | unsure | 4/32 | 28 | 4 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | certain | 4/32 | 28 | 4 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| unsure_right_long | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 | rep1_vs_rep2: 0/0 |
| control | none | 2/32 | 29 | 3 | 3 | 0 | 0 | rep1_vs_rep2: 3/3 |
| certain_right | none | 2/32 | 26 | 2 | 7 | 0 | 0 | rep1_vs_rep2: 3/3 |
| unsure_right | none | 2/32 | 26 | 3 | 6 | 0 | 0 | rep1_vs_rep2: 3/3 |
| perfect_mixed | none | 2/32 | 24 | 2 | 6 | 0 | 0 | rep1_vs_rep2: 0/0 |

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 2/32 | 5/32 | 0 |
| certain_right log shown | 2/32 | 8/32 | 0 |
| unsure_right log shown | 2/32 | 8/32 | 0 |
| perfect_mixed log shown | 2/32 | 8/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 18/32 | 5/32 | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/32 | 3/32 | -0.062 | [-0.156, +0.000] | 0 | 2 | 0.5000 | no-log control + four core cells non-missing, n = 32 | -0.062, -0.062 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.344 | [+0.125, +0.531] | 13 | 2 | 0.0074 | no-log control + four core cells non-missing, n = 32 | +0.344, +0.344 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.469 | [+0.312, +0.625] | 15 | 0 | 6.10e-05 | no-log control + four core cells non-missing, n = 32 | +0.469, +0.469 (N = 32) |
| d_c = certain\|certain_right_long - certain\|unsure_right_long | 17/32 | 4/32 | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | four long cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_u = unsure\|unsure_right_long - unsure\|certain_right_long | 1/32 | 4/32 | -0.094 | [-0.219, +0.000] | 0 | 3 | 0.2500 | four long cells non-missing, n = 32 | -0.094, -0.094 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.312 | [+0.125, +0.500] | 12 | 2 | 0.0129 | four long cells non-missing, n = 32 | +0.312, +0.312 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_long history vs unsure_right_long history, averaged over tones) |  |  | +0.500 | [+0.312, +0.688] | 15 | 0 | 6.10e-05 | four long cells non-missing, n = 32 | +0.500, +0.500 (N = 32) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 18/32 | 5/32 | +0.406 | [+0.250, +0.562] | 13 | 0 | 0.0002 | four nosum cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 0/32 | 4/32 | -0.125 | [-0.250, -0.031] | 0 | 4 | 0.1250 | four nosum cells non-missing, n = 32 | -0.125, -0.125 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.281 | [+0.031, +0.500] | 13 | 4 | 0.0490 | four nosum cells non-missing, n = 32 | +0.281, +0.281 (N = 32) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.531 | [+0.344, +0.688] | 17 | 0 | 1.53e-05 | four nosum cells non-missing, n = 32 | +0.531, +0.531 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|c3_u4 | 8/32 | 4/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | both cells non-missing, n = 32 | +0.125, +0.125 (N = 32) |
| unsure\|perfect_mixed - unsure\|c2_u4 | 8/32 | 4/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | both cells non-missing, n = 32 | +0.125, +0.125 (N = 32) |
| unsure\|perfect_mixed - unsure\|unsure_right | 8/32 | 1/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 | +0.219, +0.219 (N = 32) |
| certain\|perfect_mixed - certain\|c4_u3 | 22/32 | 19/32 | +0.094 | [+0.000, +0.188] | 3 | 0 | 0.2500 | both cells non-missing, n = 32 | +0.094, +0.094 (N = 32) |
| certain\|perfect_mixed - certain\|c4_u2 | 22/32 | 19/32 | +0.094 | [+0.000, +0.188] | 3 | 0 | 0.2500 | both cells non-missing, n = 32 | +0.094, +0.094 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 22/32 | 18/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | both cells non-missing, n = 32 | +0.125, +0.125 (N = 32) |
| unsure\|all_unsure - unsure\|all_unsure_6of8 | 11/32 | 4/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 | +0.219, +0.219 (N = 32) |
| certain\|all_certain - certain\|all_certain_6of8 | 23/32 | 19/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | both cells non-missing, n = 32 | +0.125, +0.125 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 19/32 | 6/32 | +0.406 | [+0.250, +0.594] | 13 | 0 | 0.0002 | both cells non-missing, n = 32 |
| ceiling check: unsure\|all_unsure - unsure\|none | 11/32 | 10/32 | +0.031 | [-0.125, +0.188] | 4 | 3 | 1.0000 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 18/32 | 1/32 | +0.531 | [+0.375, +0.688] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 21/32 | 10/32 | +0.344 | [+0.188, +0.500] | 11 | 0 | 0.0010 | both cells non-missing, n = 32 |
| moved to x: certain_right log, no objection - no-log control | 2/32 | 2/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: certain_right log, no objection - no-log control | 8/32 | 5/32 | +0.094 | [+0.000, +0.219] | 3 | 0 | 0.2500 | both cells non-missing, n = 32 |
| moved to x: unsure_right log, no objection - no-log control | 2/32 | 2/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: unsure_right log, no objection - no-log control | 8/32 | 5/32 | +0.094 | [+0.000, +0.219] | 3 | 0 | 0.2500 | both cells non-missing, n = 32 |
| moved to x: perfect_mixed log, no objection - no-log control | 2/32 | 2/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: perfect_mixed log, no objection - no-log control | 8/32 | 5/32 | +0.094 | [+0.000, +0.188] | 3 | 0 | 0.2500 | both cells non-missing, n = 32 |

## ministral-3:8b | answer-only | arm B | stratum wrong | target distractor

Source files: dev__ministral-3_8b__instant__B.jsonl. Items: 3. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 3; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 3.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| none | unsure | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| reliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 3 | +0.000, +0.000 (N = 3) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 3 | +0.000, +0.000 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 3 | +0.000, +0.000 (N = 3) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 3 | +0.000, +0.000 (N = 3) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.333, +0.333 (N = 3) |
| certain\|perfect_mixed - certain\|certain_right | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.333, +0.333 (N = 3) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| no-log tone gap: certain\|none - unsure\|none | 2/3 | 1/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 |

## ministral-3:8b | answer-only | arm B | stratum wrong | target key

Source files: dev__ministral-3_8b__instant__B.jsonl. Items: 3. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 3; of these, also with a non-missing no-log control (by-voice population): 3. Items used for bounds: 3.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| none | unsure | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| reliable | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| reliable | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/3 | 3 | 0 | 0 | 0 | 0 |  |
| control | none | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| certain_right | none | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| unsure_right | none | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | none | 1/3 | 2 | 1 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 1/3 | 1/3 | 0 |
| certain_right log shown | 1/3 | 1/3 | 0 |
| unsure_right log shown | 1/3 | 1/3 | 0 |
| perfect_mixed log shown | 1/3 | 1/3 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/3 | 1/3 | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 3 | -0.333, -0.333 (N = 3) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 3 | -0.333, -0.333 (N = 3) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 3 | -0.333, -0.333 (N = 3) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/3 | 0/3 | +0.667 | [+0.000, +1.000] | 2 | 0 | 0.5000 | both cells non-missing, n = 3 | +0.667, +0.667 (N = 3) |
| certain\|perfect_mixed - certain\|certain_right | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.333, +0.333 (N = 3) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| no-log tone gap: certain\|none - unsure\|none | 2/3 | 1/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 |
| moved to x: certain_right log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: certain_right log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| moved to x: unsure_right log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: unsure_right log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| moved to x: perfect_mixed log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: perfect_mixed log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |

## ministral-3:8b | answer-only | arm M | stratum wrong | target distractor

Source files: dev__ministral-3_8b__instant__M.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 6/32 | 26 | 6 | 0 | 0 | 0 |  |
| certain_right | unsure | 5/32 | 27 | 5 | 0 | 0 | 0 |  |
| unsure_right | certain | 2/32 | 29 | 2 | 1 | 0 | 0 |  |
| unsure_right | unsure | 1/32 | 31 | 1 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 6/32 | 2/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.125, +0.125 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/32 | 5/32 | -0.125 | [-0.250, -0.031] | 0 | 4 | 0.1250 | four core cells non-missing (no-log control not run in this group), n = 32 | -0.125, -0.125 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [-0.156, +0.156] | 3 | 3 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.000, +0.000 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.250 | [+0.062, +0.469] | 7 | 1 | 0.0703 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.250, +0.250 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 6/32 | 1/32 | +0.156 | [+0.031, +0.281] | 5 | 0 | 0.0625 | both cells non-missing, n = 32 |

## ministral-3:8b | answer-only | arm M | stratum wrong | target key

Source files: dev__ministral-3_8b__instant__M.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| perfect_mixed | certain | 12/32 | 19 | 12 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 16/32 | 16 | 16 | 0 | 0 | 0 |  |
| reliable | certain | 11/32 | 20 | 11 | 1 | 0 | 0 |  |
| reliable | unsure | 6/32 | 26 | 6 | 0 | 0 | 0 |  |
| certain_right | certain | 8/32 | 23 | 8 | 1 | 0 | 0 |  |
| certain_right | unsure | 8/32 | 24 | 8 | 0 | 0 | 0 |  |
| unsure_right | certain | 2/32 | 29 | 2 | 1 | 0 | 0 |  |
| unsure_right | unsure | 5/32 | 27 | 5 | 0 | 0 | 0 |  |

Not run: certain|none, unsure|none, certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 8/32 | 2/32 | +0.188 | [+0.062, +0.344] | 6 | 0 | 0.0312 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.188, +0.188 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 5/32 | 8/32 | -0.094 | [-0.219, +0.031] | 1 | 4 | 0.3750 | four core cells non-missing (no-log control not run in this group), n = 32 | -0.094, -0.094 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.094 | [-0.031, +0.219] | 4 | 1 | 0.3750 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.094, +0.094 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.281 | [+0.062, +0.531] | 7 | 1 | 0.0703 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.281, +0.281 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 16/32 | 5/32 | +0.344 | [+0.188, +0.500] | 11 | 0 | 0.0010 | both cells non-missing, n = 32 | +0.344, +0.344 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 12/32 | 8/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | both cells non-missing, n = 32 | +0.125, +0.125 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 11/32 | 6/32 | +0.156 | [+0.031, +0.281] | 5 | 0 | 0.0625 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 8/32 | 5/32 | +0.094 | [-0.031, +0.219] | 4 | 1 | 0.3750 | both cells non-missing, n = 32 |

## ministral-3:8b | deliberative | arm A | stratum wrong | target distractor

Source files: dev__ministral-3_8b__reasoned__A.jsonl. Items: 3. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 2; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 3.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 1/3 | 1 | 1 | 1 | 0 | 0 |  |
| none | unsure | 0/2 | 1 | 0 | 1 | 1 (no answer 1) | 1 |  |
| perfect_mixed | certain | 1/3 | 1 | 1 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 0/3 | 2 | 0 | 1 | 0 | 0 |  |
| certain_right | certain | 1/3 | 1 | 1 | 1 | 0 | 0 |  |
| certain_right | unsure | 0/2 | 1 | 0 | 1 | 1 (no answer 1) | 1 |  |
| unsure_right | certain | 1/3 | 1 | 1 | 1 | 0 | 0 |  |
| unsure_right | unsure | 0/3 | 2 | 0 | 1 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 2 | +0.000, +0.000 (N = 3) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 2 | -0.333, +0.000 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 2 | -0.333, +0.000 (N = 3) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 2 | +0.000, +0.333 (N = 3) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| certain\|perfect_mixed - certain\|certain_right | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 |
| no-log tone gap: certain\|none - unsure\|none | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |

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

Source files: dev__ministral-3_8b__reasoned__A.jsonl. Items: 3. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 3; of these, also with a non-missing no-log control (by-voice population): 3. Items used for bounds: 3.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/2 | 0 | 2 | 0 | 1 (no answer 1) | 1 |  |
| none | unsure | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| all_certain | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| all_certain | unsure | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| all_unsure | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| all_unsure | unsure | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| reliable | unsure | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| certain_right | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| certain_right | unsure | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| unsure_right | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| unsure_right | unsure | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| certain_right_nosum | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| certain_right_nosum | unsure | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| unsure_right_nosum | certain | 2/3 | 1 | 2 | 0 | 0 | 0 |  |
| unsure_right_nosum | unsure | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| control | none | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| certain_right | none | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| unsure_right | none | 1/3 | 2 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | none | 1/3 | 2 | 1 | 0 | 0 | 0 |  |

Not run: certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 1/3 | 1/3 | 0 |
| certain_right log shown | 1/3 | 1/3 | 0 |
| unsure_right log shown | 1/3 | 1/3 | 0 |
| perfect_mixed log shown | 1/3 | 1/3 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/3 | 2/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/3 | 2/3 | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 3 | -0.333, -0.333 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 3 | -0.333, -0.333 (N = 3) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 3 | +0.333, +0.333 (N = 3) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 2/3 | 2/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |
| certain\|perfect_mixed - certain\|certain_right | 2/3 | 2/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 | +0.000, +0.000 (N = 3) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/3 | 2/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| ceiling check: unsure\|all_unsure - unsure\|none | 2/3 | 2/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/3 | 1/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 3 |
| no-log tone gap: certain\|none - unsure\|none | 2/2 | 2/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| moved to x: certain_right log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: certain_right log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| moved to x: unsure_right log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: unsure_right log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| moved to x: perfect_mixed log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |
| changed at all: perfect_mixed log, no objection - no-log control | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 3 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 1/2 | 1/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 2 | +0.000, +0.000 (N = 2) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/2 | 1/2 | -0.500 | [-1.000, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 2 | -0.500, -0.500 (N = 2) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.500 | [-1.000, +0.000] | 0 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 2 | -0.500, -0.500 (N = 2) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.500 | [+0.000, +1.000] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 2 | +0.500, +0.500 (N = 2) |
| d_c = certain\|certain_right_nosum - certain\|unsure_right_nosum | 1/2 | 1/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 2 | +0.000, +0.000 (N = 2) |
| d_u = unsure\|unsure_right_nosum - unsure\|certain_right_nosum | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 2 | +0.000, +0.000 (N = 2) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 2 | +0.000, +0.000 (N = 2) |
| D = d_c - d_u (log main effect: certain_right_nosum history vs unsure_right_nosum history, averaged over tones) |  |  | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four nosum cells non-missing, n = 2 | +0.000, +0.000 (N = 2) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 | +0.000, +0.000 (N = 2) |
| certain\|perfect_mixed - certain\|certain_right | 1/2 | 1/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 | +0.000, +0.000 (N = 2) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 1/2 | 1/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| ceiling check: unsure\|all_unsure - unsure\|none | 1/2 | 1/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1/2 | 0/2 | +0.500 | [+0.000, +1.000] | 1 | 0 | 1.0000 | both cells non-missing, n = 2 |
| no-log tone gap: certain\|none - unsure\|none | 1/1 | 1/1 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 1 |
| moved to x: certain_right log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| changed at all: certain_right log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| moved to x: unsure_right log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| changed at all: unsure_right log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/2 | 0/2 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 2 |

## openai:gpt-6-luna | answer-only | arm A | stratum wrong | target distractor

Source files: dev__openai_gpt-6-luna__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 4/32 | 27 | 4 | 1 | 0 | 0 |  |
| none | unsure | 2/32 | 30 | 2 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 2/32 | 29 | 2 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 2/32 | 29 | 2 | 1 | 0 | 0 |  |
| reliable | certain | 0/32 | 31 | 0 | 1 | 0 | 0 |  |
| reliable | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/32 | 31 | 0 | 1 | 0 | 0 |  |
| unsure_right | certain | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| unsure_right | unsure | 2/32 | 29 | 2 | 1 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | -0.031, -0.031 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 2/32 | 0/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.062, +0.062 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.031, +0.031 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.094 | [-0.250, +0.000] | 0 | 2 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 32 | -0.094, -0.094 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/32 | 2/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 | both cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 2/32 | 0/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 | both cells non-missing, n = 32 | +0.062, +0.062 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 0/32 | 2/32 | -0.062 | [-0.156, +0.000] | 0 | 2 | 0.5000 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 4/32 | 2/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 | both cells non-missing, n = 32 |

## openai:gpt-6-luna | answer-only | arm A | stratum wrong | target key

Source files: dev__openai_gpt-6-luna__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 5/32 | 27 | 5 | 0 | 0 | 0 |  |
| none | unsure | 6/32 | 25 | 6 | 1 | 0 | 0 |  |
| perfect_mixed | certain | 8/32 | 24 | 8 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 7/32 | 25 | 7 | 0 | 0 | 0 |  |
| reliable | certain | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| reliable | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 1/32 | 31 | 1 | 0 | 0 | 0 |  |
| unsure_right | unsure | 3/32 | 29 | 3 | 0 | 0 | 0 |  |
| control | none | 0/32 | 31 | 0 | 1 | 0 | 0 |  |
| certain_right | none | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| unsure_right | none | 0/32 | 32 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | none | 0/32 | 32 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/32 | 1/32 | 0 |
| certain_right log shown | 0/32 | 0/32 | 0 |
| unsure_right log shown | 0/32 | 0/32 | 0 |
| perfect_mixed log shown | 0/32 | 0/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 1/32 | 1/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/32 | 0/32 | +0.094 | [+0.000, +0.219] | 3 | 0 | 0.2500 | no-log control + four core cells non-missing, n = 32 | +0.094, +0.094 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.094 | [+0.000, +0.219] | 3 | 0 | 0.2500 | no-log control + four core cells non-missing, n = 32 | +0.094, +0.094 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.094 | [-0.250, +0.031] | 1 | 3 | 0.6250 | no-log control + four core cells non-missing, n = 32 | -0.094, -0.094 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 7/32 | 3/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 | both cells non-missing, n = 32 | +0.125, +0.125 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 8/32 | 1/32 | +0.219 | [+0.062, +0.375] | 8 | 1 | 0.0391 | both cells non-missing, n = 32 | +0.219, +0.219 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 1/32 | 3/32 | -0.062 | [-0.188, +0.062] | 1 | 3 | 0.6250 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 5/32 | 6/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: certain_right log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: certain_right log, no objection - no-log control | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: unsure_right log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: unsure_right log, no objection - no-log control | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/32 | 1/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 32 |

## openai:gpt-6-luna | deliberative | arm A | stratum wrong | target distractor

Source files: dev__openai_gpt-6-luna__reasoned__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 31; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 4/30 | 8 | 4 | 18 | 2 (no answer 2) | 2 |  |
| none | unsure | 2/32 | 12 | 2 | 18 | 0 | 0 |  |
| perfect_mixed | certain | 5/32 | 9 | 5 | 18 | 0 | 0 |  |
| perfect_mixed | unsure | 4/31 | 7 | 4 | 20 | 1 (no answer 1) | 1 |  |
| certain_right | certain | 5/32 | 9 | 5 | 18 | 0 | 0 |  |
| certain_right | unsure | 4/32 | 10 | 4 | 18 | 0 | 0 |  |
| unsure_right | certain | 4/32 | 10 | 4 | 18 | 0 | 0 |  |
| unsure_right | unsure | 4/31 | 8 | 4 | 19 | 1 (no answer 1) | 1 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 4/31 | 4/31 | +0.000 | [-0.097, +0.097] | 1 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 31 | +0.031, +0.031 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 4/31 | 3/31 | +0.032 | [-0.097, +0.161] | 3 | 2 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 31 | +0.000, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.032 | [-0.097, +0.161] | 3 | 2 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 31 | +0.031, +0.062 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.032 | [-0.194, +0.161] | 2 | 4 | 0.6875 | four core cells non-missing (no-log control not run in this group), n = 31 | +0.000, +0.031 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 3/30 | 4/30 | -0.033 | [-0.133, +0.067] | 1 | 2 | 1.0000 | both cells non-missing, n = 30 | -0.031, +0.031 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 5/32 | 5/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 | both cells non-missing, n = 32 | +0.000, +0.000 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 4/31 | 4/31 | +0.000 | [-0.129, +0.129] | 2 | 2 | 1.0000 | both cells non-missing, n = 31 |
| no-log tone gap: certain\|none - unsure\|none | 4/30 | 1/30 | +0.100 | [+0.000, +0.233] | 3 | 0 | 0.2500 | both cells non-missing, n = 30 |

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

## openai:gpt-6-luna | deliberative | arm A | stratum wrong | target key

Source files: dev__openai_gpt-6-luna__reasoned__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 30; of these, also with a non-missing no-log control (by-voice population): 29. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 22/32 | 7 | 22 | 3 | 0 | 0 |  |
| none | unsure | 22/31 | 7 | 22 | 2 | 1 (no answer 1) | 1 |  |
| perfect_mixed | certain | 23/32 | 7 | 23 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 20/32 | 8 | 20 | 4 | 0 | 0 |  |
| reliable | certain | 22/32 | 7 | 22 | 3 | 0 | 0 |  |
| reliable | unsure | 18/32 | 10 | 18 | 4 | 0 | 0 |  |
| certain_right | certain | 20/32 | 8 | 20 | 4 | 0 | 0 |  |
| certain_right | unsure | 21/31 | 8 | 21 | 2 | 1 (no answer 1) | 1 |  |
| unsure_right | certain | 22/31 | 7 | 22 | 2 | 1 (no answer 1) | 1 |  |
| unsure_right | unsure | 19/31 | 7 | 19 | 5 | 1 (no answer 1) | 1 |  |
| control | none | 15/31 | 12 | 15 | 4 | 1 (no answer 1) | 1 |  |
| certain_right | none | 17/31 | 12 | 17 | 2 | 1 (no answer 1) | 1 |  |
| unsure_right | none | 17/32 | 11 | 17 | 4 | 0 | 0 |  |
| perfect_mixed | none | 15/32 | 13 | 15 | 4 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 15/31 | 19/31 | 1 |
| certain_right log shown | 17/31 | 19/31 | 1 |
| unsure_right log shown | 17/32 | 21/32 | 0 |
| perfect_mixed log shown | 15/32 | 19/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 17/29 | 20/29 | -0.103 | [-0.241, +0.034] | 1 | 4 | 0.3750 | no-log control + four core cells non-missing, n = 29 | -0.094, -0.062 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 17/29 | 19/29 | -0.069 | [-0.207, +0.069] | 1 | 3 | 0.6250 | no-log control + four core cells non-missing, n = 29 | -0.094, -0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.172 | [-0.379, +0.000] | 1 | 5 | 0.2188 | no-log control + four core cells non-missing, n = 29 | -0.188, -0.094 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.034 | [-0.241, +0.172] | 3 | 3 | 1.0000 | no-log control + four core cells non-missing, n = 29 | -0.062, +0.031 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 19/31 | 19/31 | +0.000 | [-0.097, +0.097] | 1 | 1 | 1.0000 | both cells non-missing, n = 31 | +0.000, +0.031 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 23/32 | 20/32 | +0.094 | [-0.062, +0.250] | 5 | 2 | 0.4531 | both cells non-missing, n = 32 | +0.094, +0.094 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 22/32 | 18/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 19/31 | 19/31 | +0.000 | [-0.129, +0.129] | 2 | 2 | 1.0000 | both cells non-missing, n = 31 |
| no-log tone gap: certain\|none - unsure\|none | 22/31 | 22/31 | +0.000 | [-0.129, +0.129] | 2 | 2 | 1.0000 | both cells non-missing, n = 31 |
| moved to x: certain_right log, no objection - no-log control | 16/30 | 15/30 | +0.033 | [+0.000, +0.100] | 1 | 0 | 1.0000 | both cells non-missing, n = 30 |
| changed at all: certain_right log, no objection - no-log control | 18/30 | 19/30 | -0.033 | [-0.100, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 30 |
| moved to x: unsure_right log, no objection - no-log control | 16/31 | 15/31 | +0.032 | [-0.097, +0.161] | 3 | 2 | 1.0000 | both cells non-missing, n = 31 |
| changed at all: unsure_right log, no objection - no-log control | 20/31 | 19/31 | +0.032 | [-0.065, +0.161] | 2 | 1 | 1.0000 | both cells non-missing, n = 31 |
| moved to x: perfect_mixed log, no objection - no-log control | 14/31 | 15/31 | -0.032 | [-0.097, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 31 |
| changed at all: perfect_mixed log, no objection - no-log control | 18/31 | 19/31 | -0.032 | [-0.129, +0.065] | 1 | 2 | 1.0000 | both cells non-missing, n = 31 |

### By-voice statistics, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/10 | 4/10 | -0.200 | [-0.600, +0.200] | 1 | 3 | 0.6250 | no-log control + four core cells non-missing, n = 10 | -0.167, -0.083 (N = 12) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/10 | 2/10 | +0.100 | [+0.000, +0.300] | 1 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 10 | +0.000, +0.167 (N = 12) |
| I = d_c + d_u (tone x log interaction) |  |  | -0.100 | [-0.400, +0.200] | 1 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 10 | -0.167, +0.083 (N = 12) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | -0.300 | [-0.800, +0.100] | 1 | 3 | 0.6250 | no-log control + four core cells non-missing, n = 10 | -0.333, -0.083 (N = 12) |

### Spillover dose series and one-voice logs, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 3/11 | 4/11 | -0.091 | [-0.273, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 11 | -0.083, +0.000 (N = 12) |
| certain\|perfect_mixed - certain\|certain_right | 5/12 | 4/12 | +0.083 | [-0.250, +0.417] | 3 | 2 | 1.0000 | both cells non-missing, n = 12 | +0.083, +0.083 (N = 12) |

### Other contrasts and log-shown controls, items whose no-log control kept its answer

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 6/12 | 2/12 | +0.333 | [+0.083, +0.583] | 4 | 0 | 0.1250 | both cells non-missing, n = 12 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 3/11 | 4/11 | -0.091 | [-0.364, +0.182] | 1 | 2 | 1.0000 | both cells non-missing, n = 11 |
| no-log tone gap: certain\|none - unsure\|none | 6/12 | 4/12 | +0.167 | [+0.000, +0.417] | 2 | 0 | 0.5000 | both cells non-missing, n = 12 |
| moved to x: certain_right log, no objection - no-log control | 0/11 | 0/11 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 11 |
| changed at all: certain_right log, no objection - no-log control | 0/11 | 0/11 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 11 |
| moved to x: unsure_right log, no objection - no-log control | 2/12 | 0/12 | +0.167 | [+0.000, +0.417] | 2 | 0 | 0.5000 | both cells non-missing, n = 12 |
| changed at all: unsure_right log, no objection - no-log control | 2/12 | 0/12 | +0.167 | [+0.000, +0.417] | 2 | 0 | 0.5000 | both cells non-missing, n = 12 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/12 | 0/12 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 12 |
| changed at all: perfect_mixed log, no objection - no-log control | 1/12 | 0/12 | +0.083 | [+0.000, +0.250] | 1 | 0 | 1.0000 | both cells non-missing, n = 12 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm A | stratum wrong | target distractor

Source files: dev__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl. Items: 23. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 23; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 23.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 9/23 | 14 | 9 | 0 | 0 | 0 |  |
| none | unsure | 4/23 | 19 | 4 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 6/23 | 17 | 6 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 2/23 | 21 | 2 | 0 | 0 | 0 |  |
| reliable | certain | 2/23 | 21 | 2 | 0 | 0 | 0 |  |
| reliable | unsure | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 2/23 | 21 | 2 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/23 | 23 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 23 | +0.087, +0.087 (N = 23) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 23 | +0.000, +0.000 (N = 23) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 23 | +0.087, +0.087 (N = 23) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | four core cells non-missing (no-log control not run in this group), n = 23 | +0.087, +0.087 (N = 23) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | both cells non-missing, n = 23 | +0.087, +0.087 (N = 23) |
| certain\|perfect_mixed - certain\|certain_right | 6/23 | 2/23 | +0.174 | [+0.043, +0.348] | 4 | 0 | 0.1250 | both cells non-missing, n = 23 | +0.174, +0.174 (N = 23) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | both cells non-missing, n = 23 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | both cells non-missing, n = 23 |
| no-log tone gap: certain\|none - unsure\|none | 9/23 | 4/23 | +0.217 | [+0.043, +0.391] | 5 | 0 | 0.0625 | both cells non-missing, n = 23 |

## openrouter:deepseek/deepseek-v3.2 | answer-only | arm A | stratum wrong | target key

Source files: dev__openrouter_deepseek_deepseek-v3.2__instant__A.jsonl. Items: 23. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 23; of these, also with a non-missing no-log control (by-voice population): 23. Items used for bounds: 23.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 10/23 | 13 | 10 | 0 | 0 | 0 |  |
| none | unsure | 1/23 | 22 | 1 | 0 | 0 | 0 |  |
| perfect_mixed | certain | 12/23 | 11 | 12 | 0 | 0 | 0 |  |
| perfect_mixed | unsure | 1/23 | 22 | 1 | 0 | 0 | 0 |  |
| reliable | certain | 2/23 | 21 | 2 | 0 | 0 | 0 |  |
| reliable | unsure | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| certain_right | certain | 2/23 | 21 | 2 | 0 | 0 | 0 |  |
| certain_right | unsure | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| unsure_right | certain | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| unsure_right | unsure | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| control | none | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| certain_right | none | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| unsure_right | none | 0/23 | 23 | 0 | 0 | 0 | 0 |  |
| perfect_mixed | none | 0/23 | 23 | 0 | 0 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 0/23 | 0/23 | 0 |
| certain_right log shown | 0/23 | 0/23 | 0 |
| unsure_right log shown | 0/23 | 0/23 | 0 |
| perfect_mixed log shown | 0/23 | 0/23 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 23 | +0.087, +0.087 (N = 23) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | no-log control + four core cells non-missing, n = 23 | +0.000, +0.000 (N = 23) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 23 | +0.087, +0.087 (N = 23) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | no-log control + four core cells non-missing, n = 23 | +0.087, +0.087 (N = 23) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 1/23 | 0/23 | +0.043 | [+0.000, +0.130] | 1 | 0 | 1.0000 | both cells non-missing, n = 23 | +0.043, +0.043 (N = 23) |
| certain\|perfect_mixed - certain\|certain_right | 12/23 | 2/23 | +0.435 | [+0.217, +0.652] | 10 | 0 | 0.0020 | both cells non-missing, n = 23 | +0.435, +0.435 (N = 23) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | both cells non-missing, n = 23 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 2/23 | 0/23 | +0.087 | [+0.000, +0.217] | 2 | 0 | 0.5000 | both cells non-missing, n = 23 |
| no-log tone gap: certain\|none - unsure\|none | 10/23 | 1/23 | +0.391 | [+0.217, +0.609] | 9 | 0 | 0.0039 | both cells non-missing, n = 23 |
| moved to x: certain_right log, no objection - no-log control | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 23 |
| changed at all: certain_right log, no objection - no-log control | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 23 |
| moved to x: unsure_right log, no objection - no-log control | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 23 |
| changed at all: unsure_right log, no objection - no-log control | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 23 |
| moved to x: perfect_mixed log, no objection - no-log control | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 23 |
| changed at all: perfect_mixed log, no objection - no-log control | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 | both cells non-missing, n = 23 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm A | stratum wrong | target distractor

Source files: dev__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 24/32 | 7 | 24 | 1 | 0 | 0 |  |
| none | unsure | 10/15 | 4 | 10 | 1 | 0 | 17 |  |
| certain_right | certain | 21/32 | 9 | 21 | 2 | 0 | 0 |  |
| certain_right | unsure | 14/32 | 16 | 14 | 2 | 0 | 0 |  |
| unsure_right | certain | 12/32 | 17 | 12 | 3 | 0 | 0 |  |
| unsure_right | unsure | 14/32 | 15 | 14 | 3 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|perfect_mixed, unsure|perfect_mixed, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|reliable, unsure|reliable, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 21/32 | 12/32 | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.281, +0.281 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 14/32 | 14/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.000, +0.000 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.281 | [+0.125, +0.438] | 9 | 0 | 0.0039 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.281, +0.281 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.281 | [+0.094, +0.500] | 9 | 1 | 0.0215 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.281, +0.281 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 21/32 | 14/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 11/15 | 10/15 | +0.067 | [+0.000, +0.200] | 1 | 0 | 1.0000 | both cells non-missing, n = 15 |

## openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm A | stratum wrong | target key

Source files: dev__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/32 | 5 | 25 | 2 | 0 | 0 |  |
| none | unsure | 22/32 | 7 | 22 | 3 | 0 | 0 |  |
| perfect_mixed | certain | 28/32 | 2 | 28 | 2 | 0 | 0 |  |
| perfect_mixed | unsure | 25/32 | 5 | 25 | 2 | 0 | 0 |  |
| reliable | certain | 28/32 | 2 | 28 | 2 | 0 | 0 |  |
| reliable | unsure | 23/32 | 7 | 23 | 2 | 0 | 0 |  |
| certain_right | certain | 26/32 | 4 | 26 | 2 | 0 | 0 |  |
| certain_right | unsure | 13/32 | 16 | 13 | 3 | 0 | 0 |  |
| unsure_right | certain | 12/32 | 18 | 12 | 2 | 0 | 0 |  |
| unsure_right | unsure | 14/32 | 16 | 14 | 2 | 0 | 0 |  |
| control | none | 2/32 | 23 | 2 | 7 | 0 | 0 |  |
| certain_right | none | 2/32 | 19 | 2 | 11 | 0 | 0 |  |
| unsure_right | none | 2/32 | 19 | 2 | 11 | 0 | 0 |  |
| perfect_mixed | none | 2/32 | 20 | 2 | 10 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 2/32 | 9/32 | 0 |
| certain_right log shown | 2/32 | 13/32 | 0 |
| unsure_right log shown | 2/32 | 13/32 | 0 |
| perfect_mixed log shown | 2/32 | 12/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 26/32 | 12/32 | +0.438 | [+0.281, +0.625] | 14 | 0 | 0.0001 | no-log control + four core cells non-missing, n = 32 | +0.438, +0.438 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 14/32 | 13/32 | +0.031 | [-0.062, +0.156] | 2 | 1 | 1.0000 | no-log control + four core cells non-missing, n = 32 | +0.031, +0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.469 | [+0.281, +0.656] | 14 | 0 | 0.0001 | no-log control + four core cells non-missing, n = 32 | +0.469, +0.469 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.406 | [+0.188, +0.625] | 13 | 1 | 0.0018 | no-log control + four core cells non-missing, n = 32 | +0.406, +0.406 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 25/32 | 14/32 | +0.344 | [+0.188, +0.500] | 11 | 0 | 0.0010 | both cells non-missing, n = 32 | +0.344, +0.344 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 28/32 | 26/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 | both cells non-missing, n = 32 | +0.062, +0.062 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 28/32 | 23/32 | +0.156 | [+0.031, +0.281] | 5 | 0 | 0.0625 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 26/32 | 14/32 | +0.375 | [+0.219, +0.531] | 12 | 0 | 0.0005 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 25/32 | 22/32 | +0.094 | [+0.000, +0.219] | 3 | 0 | 0.2500 | both cells non-missing, n = 32 |
| moved to x: certain_right log, no objection - no-log control | 2/32 | 2/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: certain_right log, no objection - no-log control | 13/32 | 9/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 | both cells non-missing, n = 32 |
| moved to x: unsure_right log, no objection - no-log control | 2/32 | 2/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: unsure_right log, no objection - no-log control | 13/32 | 9/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 | both cells non-missing, n = 32 |
| moved to x: perfect_mixed log, no objection - no-log control | 2/32 | 2/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: perfect_mixed log, no objection - no-log control | 12/32 | 9/32 | +0.094 | [-0.031, +0.219] | 4 | 1 | 0.3750 | both cells non-missing, n = 32 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm A | stratum wrong | target distractor

Source files: dev__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 0. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 23/32 | 2 | 23 | 7 | 0 | 0 |  |
| none | unsure | 15/32 | 5 | 15 | 12 | 0 | 0 |  |
| perfect_mixed | certain | 30/32 | 1 | 30 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 13/32 | 16 | 13 | 3 | 0 | 0 |  |
| reliable | certain | 20/32 | 9 | 20 | 3 | 0 | 0 |  |
| reliable | unsure | 4/32 | 25 | 4 | 3 | 0 | 0 |  |
| certain_right | certain | 15/32 | 13 | 15 | 4 | 0 | 0 |  |
| certain_right | unsure | 2/32 | 28 | 2 | 2 | 0 | 0 |  |
| unsure_right | certain | 0/32 | 27 | 0 | 5 | 0 | 0 |  |
| unsure_right | unsure | 1/32 | 29 | 1 | 2 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long, none|control, none|certain_right, none|unsure_right, none|perfect_mixed.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 15/32 | 0/32 | +0.469 | [+0.312, +0.625] | 15 | 0 | 6.10e-05 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.469, +0.469 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 1/32 | 2/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | four core cells non-missing (no-log control not run in this group), n = 32 | -0.031, -0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.438 | [+0.281, +0.594] | 14 | 0 | 0.0001 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.438, +0.438 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.500 | [+0.312, +0.688] | 15 | 0 | 6.10e-05 | four core cells non-missing (no-log control not run in this group), n = 32 | +0.500, +0.500 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 13/32 | 1/32 | +0.375 | [+0.219, +0.531] | 12 | 0 | 0.0005 | both cells non-missing, n = 32 | +0.375, +0.375 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 30/32 | 15/32 | +0.469 | [+0.281, +0.656] | 15 | 0 | 6.10e-05 | both cells non-missing, n = 32 | +0.469, +0.469 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 20/32 | 4/32 | +0.500 | [+0.312, +0.688] | 16 | 0 | 3.05e-05 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 15/32 | 1/32 | +0.438 | [+0.281, +0.625] | 14 | 0 | 0.0001 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 23/32 | 15/32 | +0.250 | [+0.124, +0.406] | 8 | 0 | 0.0078 | both cells non-missing, n = 32 |

## openrouter:mistralai/ministral-14b-2512 | answer-only | arm A | stratum wrong | target key

Source files: dev__openrouter_mistralai_ministral-14b-2512__instant__A.jsonl. Items: 32. Replicates: [1]. Duplicate rows replaced: 0. Items with all four core cells non-missing: 32; of these, also with a non-missing no-log control (by-voice population): 32. Items used for bounds: 32.

### Cell table

Item-level flips/n (replicate means summed); trial-level outcomes: hold own / flip to x / third option / missing.

| log | tone | flips/n | hold | flip | third | missing (reasons) | items absent or missing | test-retest |
|---|---|---|---|---|---|---|---|---|
| none | certain | 29/32 | 1 | 29 | 2 | 0 | 0 |  |
| none | unsure | 25/32 | 2 | 25 | 5 | 0 | 0 |  |
| perfect_mixed | certain | 29/32 | 2 | 29 | 1 | 0 | 0 |  |
| perfect_mixed | unsure | 20/32 | 10 | 20 | 2 | 0 | 0 |  |
| reliable | certain | 25/32 | 6 | 25 | 1 | 0 | 0 |  |
| reliable | unsure | 8/32 | 23 | 8 | 1 | 0 | 0 |  |
| certain_right | certain | 21/32 | 9 | 21 | 2 | 0 | 0 |  |
| certain_right | unsure | 4/32 | 26 | 4 | 2 | 0 | 0 |  |
| unsure_right | certain | 4/32 | 26 | 4 | 2 | 0 | 0 |  |
| unsure_right | unsure | 3/32 | 28 | 3 | 1 | 0 | 0 |  |
| control | none | 2/32 | 21 | 2 | 9 | 0 | 0 |  |
| certain_right | none | 3/32 | 21 | 3 | 8 | 0 | 0 |  |
| unsure_right | none | 1/32 | 23 | 1 | 8 | 0 | 0 |  |
| perfect_mixed | none | 2/32 | 22 | 2 | 8 | 0 | 0 |  |

Not run: certain|all_certain, unsure|all_certain, certain|all_unsure, unsure|all_unsure, certain|all_certain_6of8, unsure|all_certain_6of8, certain|all_unsure_6of8, unsure|all_unsure_6of8, certain|c3_u4, unsure|c3_u4, certain|c2_u4, unsure|c2_u4, certain|c4_u3, unsure|c4_u3, certain|c4_u2, unsure|c4_u2, certain|unreliable, unsure|unreliable, certain|certain_right_nosum, unsure|certain_right_nosum, certain|unsure_right_nosum, unsure|unsure_right_nosum, certain|certain_right_long, unsure|certain_right_long, certain|unsure_right_long, unsure|unsure_right_long.

### Controls (no objection)

| control | moved to x | changed at all | missing or absent |
|---|---|---|---|
| no-log control | 2/32 | 11/32 | 0 |
| certain_right log shown | 3/32 | 11/32 | 0 |
| unsure_right log shown | 1/32 | 9/32 | 0 |
| perfect_mixed log shown | 2/32 | 10/32 | 0 |

### By-voice statistics, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| d_c = certain\|certain_right - certain\|unsure_right | 21/32 | 4/32 | +0.531 | [+0.374, +0.688] | 17 | 0 | 1.53e-05 | no-log control + four core cells non-missing, n = 32 | +0.531, +0.531 (N = 32) |
| d_u = unsure\|unsure_right - unsure\|certain_right | 3/32 | 4/32 | -0.031 | [-0.156, +0.062] | 1 | 2 | 1.0000 | no-log control + four core cells non-missing, n = 32 | -0.031, -0.031 (N = 32) |
| I = d_c + d_u (tone x log interaction) |  |  | +0.500 | [+0.312, +0.688] | 17 | 1 | 0.0001 | no-log control + four core cells non-missing, n = 32 | +0.500, +0.500 (N = 32) |
| D = d_c - d_u (log main effect: certain_right history vs unsure_right history, averaged over tones) |  |  | +0.562 | [+0.344, +0.781] | 18 | 1 | 7.63e-05 | no-log control + four core cells non-missing, n = 32 | +0.562, +0.562 (N = 32) |

### Spillover dose series and one-voice logs, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population | missing-outcome bounds |
|---|---|---|---|---|---|---|---|---|---|
| unsure\|perfect_mixed - unsure\|unsure_right | 20/32 | 3/32 | +0.531 | [+0.344, +0.719] | 18 | 1 | 7.63e-05 | both cells non-missing, n = 32 | +0.531, +0.531 (N = 32) |
| certain\|perfect_mixed - certain\|certain_right | 29/32 | 21/32 | +0.250 | [+0.125, +0.406] | 8 | 0 | 0.0078 | both cells non-missing, n = 32 | +0.250, +0.250 (N = 32) |

### Other contrasts and log-shown controls, all items

| contrast | A | B | A - B | 95% CI | A > B items | B > A items | sign p | population |
|---|---|---|---|---|---|---|---|---|
| tone gap under equal record: certain\|reliable - unsure\|reliable | 25/32 | 8/32 | +0.531 | [+0.375, +0.688] | 17 | 0 | 1.53e-05 | both cells non-missing, n = 32 |
| earlier endpoint (secondary): certain\|certain_right - unsure\|unsure_right | 21/32 | 3/32 | +0.562 | [+0.375, +0.750] | 19 | 1 | 4.01e-05 | both cells non-missing, n = 32 |
| no-log tone gap: certain\|none - unsure\|none | 29/32 | 25/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 | both cells non-missing, n = 32 |
| moved to x: certain_right log, no objection - no-log control | 3/32 | 2/32 | +0.031 | [-0.062, +0.125] | 2 | 1 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: certain_right log, no objection - no-log control | 11/32 | 11/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 |
| moved to x: unsure_right log, no objection - no-log control | 1/32 | 2/32 | -0.031 | [-0.094, +0.000] | 0 | 1 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: unsure_right log, no objection - no-log control | 9/32 | 11/32 | -0.062 | [-0.219, +0.094] | 2 | 4 | 0.6875 | both cells non-missing, n = 32 |
| moved to x: perfect_mixed log, no objection - no-log control | 2/32 | 2/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 | both cells non-missing, n = 32 |
| changed at all: perfect_mixed log, no objection - no-log control | 10/32 | 11/32 | -0.031 | [-0.125, +0.062] | 1 | 2 | 1.0000 | both cells non-missing, n = 32 |

## Target comparison: anthropic:claude-haiku-5-5 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| none | unsure | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |
| perfect_mixed | certain | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |
| perfect_mixed | unsure | 2/32 | 0/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 |
| reliable | certain | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |
| reliable | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | certain | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |
| unsure_right | unsure | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |

## Target comparison: anthropic:claude-haiku-5-5 | answer-only | arm B | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| none | unsure | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| perfect_mixed | certain | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| perfect_mixed | unsure | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| reliable | certain | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| reliable | unsure | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | certain | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | unsure | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 0/3 | 1/3 | -0.333 | [-1.000, +0.000] | 0 | 1 | 1.0000 |
| unsure_right | unsure | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |

## Target comparison: anthropic:claude-haiku-5-5 | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 16/32 | 2/32 | +0.438 | [+0.250, +0.625] | 15 | 1 | 0.0005 |
| none | unsure | 17/32 | 1/32 | +0.500 | [+0.344, +0.688] | 16 | 0 | 3.05e-05 |
| perfect_mixed | certain | 19/32 | 2/32 | +0.531 | [+0.312, +0.750] | 19 | 2 | 0.0002 |
| perfect_mixed | unsure | 19/32 | 2/32 | +0.531 | [+0.344, +0.719] | 18 | 1 | 7.63e-05 |
| certain_right | certain | 22/32 | 2/32 | +0.625 | [+0.406, +0.812] | 22 | 2 | 3.59e-05 |
| certain_right | unsure | 18/32 | 1/32 | +0.531 | [+0.344, +0.719] | 18 | 1 | 7.63e-05 |
| unsure_right | certain | 18/32 | 0/32 | +0.562 | [+0.375, +0.719] | 18 | 0 | 7.63e-06 |
| unsure_right | unsure | 19/32 | 2/32 | +0.531 | [+0.344, +0.719] | 18 | 1 | 7.63e-05 |

## Target comparison: gemma4:12b | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 13/32 | 13/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 |
| none | unsure | 6/32 | 5/32 | +0.031 | [-0.062, +0.125] | 2 | 1 | 1.0000 |
| perfect_mixed | certain | 32/32 | 30/32 | +0.062 | [+0.000, +0.156] | 2 | 0 | 0.5000 |
| perfect_mixed | unsure | 25/32 | 22/32 | +0.094 | [-0.062, +0.250] | 5 | 2 | 0.4531 |
| reliable | certain | 24/32 | 24/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 |
| reliable | unsure | 1/32 | 1/32 | +0.000 | [-0.094, +0.094] | 1 | 1 | 1.0000 |
| certain_right | certain | 14/32 | 12/32 | +0.062 | [-0.094, +0.219] | 4 | 2 | 0.6875 |
| certain_right | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |
| unsure_right | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |

## Target comparison: gemma4:12b | answer-only | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 5/32 | 4/32 | +0.031 | [-0.125, +0.188] | 4 | 3 | 1.0000 |
| certain_right | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 3/32 | 1/32 | +0.062 | [-0.062, +0.188] | 3 | 1 | 0.6250 |

## Target comparison: gemma4:12b | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 19/29 | 11/29 | +0.276 | [+0.034, +0.517] | 11 | 3 | 0.0574 |
| certain_right | unsure | 17/27 | 1/27 | +0.593 | [+0.407, +0.778] | 16 | 0 | 3.05e-05 |
| unsure_right | certain | 13/30 | 2/30 | +0.367 | [+0.200, +0.533] | 11 | 0 | 0.0010 |
| unsure_right | unsure | 14/28 | 1/28 | +0.464 | [+0.250, +0.679] | 14 | 1 | 0.0010 |

## Target comparison: ministral-3:8b | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 21/32 | 13/32 | +0.250 | [+0.062, +0.438] | 10 | 2 | 0.0386 |
| none | unsure | 10/32 | 3/32 | +0.219 | [+0.094, +0.375] | 7 | 0 | 0.0156 |
| perfect_mixed | certain | 22/32 | 19/32 | +0.094 | [-0.094, +0.281] | 7 | 4 | 0.5488 |
| perfect_mixed | unsure | 8/32 | 2/32 | +0.188 | [+0.031, +0.344] | 7 | 1 | 0.0703 |
| reliable | certain | 19/32 | 12/32 | +0.219 | [+0.031, +0.406] | 9 | 2 | 0.0654 |
| reliable | unsure | 6/32 | 1/32 | +0.156 | [+0.031, +0.281] | 5 | 0 | 0.0625 |
| certain_right | certain | 18/32 | 12/32 | +0.188 | [+0.000, +0.375] | 8 | 2 | 0.1094 |
| certain_right | unsure | 3/32 | 1/32 | +0.062 | [-0.062, +0.188] | 3 | 1 | 0.6250 |
| unsure_right | certain | 5/32 | 2/32 | +0.094 | [-0.031, +0.219] | 4 | 1 | 0.3750 |
| unsure_right | unsure | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |

## Target comparison: ministral-3:8b | answer-only | arm B | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/3 | 2/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| none | unsure | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| perfect_mixed | certain | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| perfect_mixed | unsure | 2/3 | 1/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| reliable | certain | 1/3 | 1/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| reliable | unsure | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | certain | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | unsure | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| unsure_right | unsure | 0/3 | 0/3 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |

## Target comparison: ministral-3:8b | answer-only | arm M | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| certain_right | certain | 8/32 | 6/32 | +0.062 | [-0.125, +0.250] | 6 | 4 | 0.7539 |
| certain_right | unsure | 8/32 | 5/32 | +0.094 | [-0.062, +0.250] | 5 | 2 | 0.4531 |
| unsure_right | certain | 2/32 | 2/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 |
| unsure_right | unsure | 5/32 | 1/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 |

## Target comparison: ministral-3:8b | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 2/2 | 1/2 | +0.500 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| none | unsure | 1/2 | 0/2 | +0.500 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| perfect_mixed | certain | 2/3 | 1/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| perfect_mixed | unsure | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| certain_right | certain | 2/3 | 1/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| certain_right | unsure | 1/2 | 0/2 | +0.500 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| unsure_right | certain | 2/3 | 1/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 |
| unsure_right | unsure | 1/3 | 0/3 | +0.333 | [+0.000, +1.000] | 1 | 0 | 1.0000 |

## Target comparison: openai:gpt-6-luna | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 5/32 | 4/32 | +0.031 | [-0.062, +0.156] | 2 | 1 | 1.0000 |
| none | unsure | 6/32 | 2/32 | +0.125 | [+0.000, +0.281] | 5 | 1 | 0.2188 |
| perfect_mixed | certain | 8/32 | 2/32 | +0.188 | [+0.031, +0.344] | 7 | 1 | 0.0703 |
| perfect_mixed | unsure | 7/32 | 2/32 | +0.156 | [+0.000, +0.312] | 6 | 1 | 0.1250 |
| reliable | certain | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| reliable | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | certain | 1/32 | 0/32 | +0.031 | [+0.000, +0.094] | 1 | 0 | 1.0000 |
| certain_right | unsure | 0/32 | 0/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 1/32 | 1/32 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 3/32 | 2/32 | +0.031 | [-0.062, +0.125] | 2 | 1 | 1.0000 |

## Target comparison: openai:gpt-6-luna | deliberative | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 21/30 | 4/30 | +0.567 | [+0.333, +0.767] | 19 | 2 | 0.0002 |
| none | unsure | 22/31 | 1/31 | +0.677 | [+0.516, +0.839] | 21 | 0 | 9.54e-07 |
| perfect_mixed | certain | 23/32 | 5/32 | +0.562 | [+0.312, +0.781] | 21 | 3 | 0.0003 |
| perfect_mixed | unsure | 19/31 | 4/31 | +0.484 | [+0.258, +0.710] | 18 | 3 | 0.0015 |
| certain_right | certain | 20/32 | 5/32 | +0.469 | [+0.219, +0.688] | 18 | 3 | 0.0015 |
| certain_right | unsure | 21/31 | 3/31 | +0.581 | [+0.387, +0.774] | 19 | 1 | 4.01e-05 |
| unsure_right | certain | 22/31 | 4/31 | +0.581 | [+0.354, +0.806] | 21 | 3 | 0.0003 |
| unsure_right | unsure | 19/30 | 4/30 | +0.500 | [+0.267, +0.733] | 18 | 3 | 0.0015 |

## Target comparison: openrouter:deepseek/deepseek-v3.2 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 10/23 | 9/23 | +0.043 | [-0.174, +0.261] | 4 | 3 | 1.0000 |
| none | unsure | 1/23 | 4/23 | -0.130 | [-0.304, +0.043] | 1 | 4 | 0.3750 |
| perfect_mixed | certain | 12/23 | 6/23 | +0.261 | [+0.000, +0.522] | 8 | 2 | 0.1094 |
| perfect_mixed | unsure | 1/23 | 2/23 | -0.043 | [-0.130, +0.000] | 0 | 1 | 1.0000 |
| reliable | certain | 2/23 | 2/23 | +0.000 | [-0.174, +0.174] | 2 | 2 | 1.0000 |
| reliable | unsure | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| certain_right | certain | 2/23 | 2/23 | +0.000 | [-0.130, +0.130] | 1 | 1 | 1.0000 |
| certain_right | unsure | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | certain | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |
| unsure_right | unsure | 0/23 | 0/23 | +0.000 | [+0.000, +0.000] | 0 | 0 | 1.0000 |

## Target comparison: openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 25/32 | 24/32 | +0.031 | [-0.094, +0.188] | 3 | 2 | 1.0000 |
| none | unsure | 9/15 | 10/15 | -0.067 | [-0.333, +0.200] | 2 | 3 | 1.0000 |
| certain_right | certain | 26/32 | 21/32 | +0.156 | [+0.031, +0.281] | 5 | 0 | 0.0625 |
| certain_right | unsure | 13/32 | 14/32 | -0.031 | [-0.188, +0.125] | 3 | 4 | 1.0000 |
| unsure_right | certain | 12/32 | 12/32 | +0.000 | [-0.125, +0.125] | 2 | 2 | 1.0000 |
| unsure_right | unsure | 14/32 | 14/32 | +0.000 | [-0.156, +0.156] | 3 | 3 | 1.0000 |

## Target comparison: openrouter:mistralai/ministral-14b-2512 | answer-only | arm A | stratum wrong

net = flip(target key) - flip(target distractor), items non-missing in both. The by-voice statistics within target distractor are in that group's section.

| log | tone | key | distractor | net | 95% CI | key > distractor | distractor > key | sign p |
|---|---|---|---|---|---|---|---|---|
| none | certain | 29/32 | 23/32 | +0.188 | [+0.031, +0.344] | 7 | 1 | 0.0703 |
| none | unsure | 25/32 | 15/32 | +0.312 | [+0.094, +0.500] | 12 | 2 | 0.0129 |
| perfect_mixed | certain | 29/32 | 30/32 | -0.031 | [-0.125, +0.062] | 1 | 2 | 1.0000 |
| perfect_mixed | unsure | 20/32 | 13/32 | +0.219 | [+0.031, +0.406] | 9 | 2 | 0.0654 |
| reliable | certain | 25/32 | 20/32 | +0.156 | [-0.031, +0.344] | 8 | 3 | 0.2266 |
| reliable | unsure | 8/32 | 4/32 | +0.125 | [-0.031, +0.281] | 6 | 2 | 0.2891 |
| certain_right | certain | 21/32 | 15/32 | +0.188 | [+0.000, +0.375] | 9 | 3 | 0.1460 |
| certain_right | unsure | 4/32 | 2/32 | +0.062 | [-0.094, +0.219] | 4 | 2 | 0.6875 |
| unsure_right | certain | 4/32 | 0/32 | +0.125 | [+0.031, +0.250] | 4 | 0 | 0.1250 |
| unsure_right | unsure | 3/32 | 1/32 | +0.062 | [-0.062, +0.188] | 3 | 1 | 0.6250 |

## Probe: stated probability that the reviewer is right

| model | arm | log | tone | n | mean | median | counts match log | independent ref | pooled ref |
|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-5-5 | A | all_certain | certain | 1 | 0.850 | 0.850 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | A | all_certain | unsure | 1 | 0.500 | 0.500 | 0.000 | 0.500 | 0.900 |
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
| anthropic:claude-haiku-5-5 | A | c4_u2 | unsure | 1 | 0.250 | 0.250 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | A | c4_u3 | certain | 1 | 0.850 | 0.850 | 1.000 | 0.833 | 0.800 |
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
| anthropic:claude-haiku-5-5 | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | B | all_certain | certain | 3 | 0.817 | 0.800 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | B | all_certain | unsure | 3 | 0.750 | 0.750 | 0.000 | 0.500 | 0.900 |
| anthropic:claude-haiku-5-5 | B | all_certain_6of8 | certain | 3 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| anthropic:claude-haiku-5-5 | B | all_certain_6of8 | unsure | 3 | 0.617 | 0.600 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | B | all_unsure | certain | 3 | 0.850 | 0.850 | 0.000 | 0.500 | 0.900 |
| anthropic:claude-haiku-5-5 | B | all_unsure | unsure | 3 | 0.817 | 0.800 | 1.000 | 0.900 | 0.900 |
| anthropic:claude-haiku-5-5 | B | all_unsure_6of8 | certain | 3 | 0.650 | 0.600 | 0.000 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | B | all_unsure_6of8 | unsure | 3 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c2_u4 | certain | 3 | 0.557 | 0.500 | 0.667 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c2_u4 | unsure | 3 | 0.433 | 0.550 | 1.000 | 0.833 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c3_u4 | certain | 3 | 0.500 | 0.750 | 0.667 | 0.667 | 0.800 |
| anthropic:claude-haiku-5-5 | B | c3_u4 | unsure | 3 | 0.850 | 0.800 | 1.000 | 0.833 | 0.800 |
| anthropic:claude-haiku-5-5 | B | c4_u2 | certain | 3 | 0.450 | 0.600 | 1.000 | 0.833 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c4_u2 | unsure | 3 | 0.583 | 0.500 | 0.667 | 0.500 | 0.700 |
| anthropic:claude-haiku-5-5 | B | c4_u3 | certain | 3 | 0.800 | 0.800 | 0.667 | 0.833 | 0.800 |
| anthropic:claude-haiku-5-5 | B | c4_u3 | unsure | 3 | 0.707 | 0.750 | 0.333 | 0.667 | 0.800 |
| anthropic:claude-haiku-5-5 | B | certain_right | certain | 3 | 0.500 | 0.500 | 0.667 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right | unsure | 3 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right_long | certain | 3 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right_long | unsure | 3 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right_nosum | certain | 3 | 0.293 | 0.380 | 0.333 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | B | certain_right_nosum | unsure | 3 | 0.000 | 0.000 | 0.667 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | B | none | certain | 3 | 0.500 | 0.500 | - | - | - |
| anthropic:claude-haiku-5-5 | B | none | unsure | 3 | 0.500 | 0.500 | - | - | - |
| anthropic:claude-haiku-5-5 | B | perfect_mixed | certain | 3 | 0.867 | 0.850 | 1.000 | 0.833 | 0.900 |
| anthropic:claude-haiku-5-5 | B | perfect_mixed | unsure | 3 | 0.800 | 0.800 | 1.000 | 0.833 | 0.900 |
| anthropic:claude-haiku-5-5 | B | reliable | certain | 3 | 0.697 | 0.670 | 0.333 | 0.667 | 0.700 |
| anthropic:claude-haiku-5-5 | B | reliable | unsure | 3 | 0.723 | 0.750 | 0.667 | 0.667 | 0.700 |
| anthropic:claude-haiku-5-5 | B | unreliable | certain | 3 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| anthropic:claude-haiku-5-5 | B | unreliable | unsure | 3 | 0.250 | 0.250 | 0.667 | 0.333 | 0.300 |
| anthropic:claude-haiku-5-5 | B | unsure_right | certain | 3 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right | unsure | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right_long | certain | 3 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right_long | unsure | 3 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right_nosum | certain | 3 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| anthropic:claude-haiku-5-5 | B | unsure_right_nosum | unsure | 3 | 0.833 | 1.000 | 1.000 | 0.833 | 0.500 |
| gemma4:12b | A | all_certain | certain | 1 | 1.000 | 1.000 | 0.000 | 0.900 | 0.900 |
| gemma4:12b | A | all_certain | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.900 |
| gemma4:12b | A | all_certain_6of8 | certain | 1 | 0.670 | 0.670 | 0.000 | 0.700 | 0.700 |
| gemma4:12b | A | all_certain_6of8 | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| gemma4:12b | A | all_unsure | certain | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.900 |
| gemma4:12b | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.900 | 0.900 |
| gemma4:12b | A | all_unsure_6of8 | certain | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| gemma4:12b | A | all_unsure_6of8 | unsure | 1 | 0.670 | 0.670 | 0.000 | 0.700 | 0.700 |
| gemma4:12b | A | c2_u4 | certain | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| gemma4:12b | A | c2_u4 | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.700 |
| gemma4:12b | A | c3_u4 | certain | 1 | 0.670 | 0.670 | 0.000 | 0.667 | 0.800 |
| gemma4:12b | A | c3_u4 | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| gemma4:12b | A | c4_u2 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| gemma4:12b | A | c4_u2 | unsure | 1 | 0.500 | 0.500 | 0.000 | 0.500 | 0.700 |
| gemma4:12b | A | c4_u3 | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| gemma4:12b | A | c4_u3 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| gemma4:12b | A | certain_right | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| gemma4:12b | A | certain_right | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| gemma4:12b | A | certain_right_long | certain | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| gemma4:12b | A | certain_right_long | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| gemma4:12b | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
| gemma4:12b | A | certain_right_nosum | unsure | 1 | 0.000 | 0.000 | 0.000 | 0.167 | 0.500 |
| gemma4:12b | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| gemma4:12b | A | none | unsure | 1 | 0.500 | 0.500 | - | - | - |
| gemma4:12b | A | perfect_mixed | certain | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.900 |
| gemma4:12b | A | perfect_mixed | unsure | 1 | 0.750 | 0.750 | 0.000 | 0.833 | 0.900 |
| gemma4:12b | A | reliable | certain | 1 | 0.670 | 0.670 | 0.000 | 0.667 | 0.700 |
| gemma4:12b | A | reliable | unsure | 1 | 0.670 | 0.670 | 0.000 | 0.667 | 0.700 |
| gemma4:12b | A | unreliable | certain | 1 | 0.330 | 0.330 | 0.000 | 0.333 | 0.300 |
| gemma4:12b | A | unreliable | unsure | 1 | 0.500 | 0.500 | 0.000 | 0.333 | 0.300 |
| gemma4:12b | A | unsure_right | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| gemma4:12b | A | unsure_right | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| gemma4:12b | A | unsure_right_long | certain | 1 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| gemma4:12b | A | unsure_right_long | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| gemma4:12b | A | unsure_right_nosum | certain | 1 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| gemma4:12b | A | unsure_right_nosum | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.833 | 0.500 |
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
| ministral-3:8b | B | all_certain | certain | 3 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| ministral-3:8b | B | all_certain | unsure | 3 | 0.000 | 0.000 | 0.000 | 0.500 | 0.900 |
| ministral-3:8b | B | all_certain_6of8 | certain | 3 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| ministral-3:8b | B | all_certain_6of8 | unsure | 3 | 0.207 | 0.250 | 0.000 | 0.500 | 0.700 |
| ministral-3:8b | B | all_unsure | certain | 3 | 0.000 | 0.000 | 0.000 | 0.500 | 0.900 |
| ministral-3:8b | B | all_unsure | unsure | 3 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| ministral-3:8b | B | all_unsure_6of8 | certain | 3 | 0.580 | 0.620 | 0.000 | 0.500 | 0.700 |
| ministral-3:8b | B | all_unsure_6of8 | unsure | 3 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| ministral-3:8b | B | c2_u4 | certain | 3 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| ministral-3:8b | B | c2_u4 | unsure | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| ministral-3:8b | B | c3_u4 | certain | 3 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| ministral-3:8b | B | c3_u4 | unsure | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| ministral-3:8b | B | c4_u2 | certain | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.700 |
| ministral-3:8b | B | c4_u2 | unsure | 3 | 0.500 | 0.500 | 1.000 | 0.500 | 0.700 |
| ministral-3:8b | B | c4_u3 | certain | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.800 |
| ministral-3:8b | B | c4_u3 | unsure | 3 | 0.750 | 0.750 | 1.000 | 0.667 | 0.800 |
| ministral-3:8b | B | certain_right | certain | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| ministral-3:8b | B | certain_right | unsure | 3 | 0.000 | 0.000 | 1.000 | 0.167 | 0.500 |
| ministral-3:8b | B | certain_right_long | certain | 3 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| ministral-3:8b | B | certain_right_long | unsure | 3 | 0.000 | 0.000 | 1.000 | 0.071 | 0.500 |
| ministral-3:8b | B | certain_right_nosum | certain | 3 | 0.513 | 0.370 | 0.000 | 0.833 | 0.500 |
| ministral-3:8b | B | certain_right_nosum | unsure | 3 | 0.303 | 0.250 | 0.333 | 0.167 | 0.500 |
| ministral-3:8b | B | none | certain | 3 | 0.300 | 0.300 | - | - | - |
| ministral-3:8b | B | none | unsure | 3 | 0.300 | 0.300 | - | - | - |
| ministral-3:8b | B | perfect_mixed | certain | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| ministral-3:8b | B | perfect_mixed | unsure | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.900 |
| ministral-3:8b | B | reliable | certain | 3 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| ministral-3:8b | B | reliable | unsure | 3 | 0.750 | 0.750 | 1.000 | 0.667 | 0.700 |
| ministral-3:8b | B | unreliable | certain | 3 | 0.277 | 0.250 | 0.667 | 0.333 | 0.300 |
| ministral-3:8b | B | unreliable | unsure | 3 | 0.250 | 0.250 | 1.000 | 0.333 | 0.300 |
| ministral-3:8b | B | unsure_right | certain | 3 | 0.000 | 0.000 | 0.667 | 0.167 | 0.500 |
| ministral-3:8b | B | unsure_right | unsure | 3 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
| ministral-3:8b | B | unsure_right_long | certain | 3 | 0.000 | 0.000 | 0.333 | 0.071 | 0.500 |
| ministral-3:8b | B | unsure_right_long | unsure | 3 | 1.000 | 1.000 | 1.000 | 0.929 | 0.500 |
| ministral-3:8b | B | unsure_right_nosum | certain | 3 | 0.453 | 0.500 | 0.000 | 0.167 | 0.500 |
| ministral-3:8b | B | unsure_right_nosum | unsure | 3 | 0.557 | 0.500 | 0.000 | 0.833 | 0.500 |
| openai:gpt-6-luna | A | all_certain | certain | 1 | 0.000 | 0.000 | 0.000 | 0.900 | 0.900 |
| openai:gpt-6-luna | A | all_certain | unsure | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.900 |
| openai:gpt-6-luna | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| openai:gpt-6-luna | A | all_certain_6of8 | unsure | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | all_unsure | certain | 1 | 1.000 | 1.000 | 1.000 | 0.500 | 0.900 |
| openai:gpt-6-luna | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.900 | 0.900 |
| openai:gpt-6-luna | A | all_unsure_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.500 | 0.700 |
| openai:gpt-6-luna | A | all_unsure_6of8 | unsure | 1 | 1.000 | 1.000 | 0.000 | 0.700 | 0.700 |
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
| openai:gpt-6-luna | A | certain_right_nosum | certain | 1 | 1.000 | 1.000 | 1.000 | 0.833 | 0.500 |
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
| openrouter:deepseek/deepseek-v3.2 | A | all_certain_6of8 | certain | 1 | 0.750 | 0.750 | 1.000 | 0.700 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | all_certain_6of8 | unsure | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | all_unsure | certain | 1 | 1.000 | 1.000 | 0.000 | 0.500 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | A | all_unsure | unsure | 1 | 1.000 | 1.000 | 1.000 | 0.900 | 0.900 |
| openrouter:deepseek/deepseek-v3.2 | A | all_unsure_6of8 | certain | 1 | 0.000 | 0.000 | 1.000 | 0.500 | 0.700 |
| openrouter:deepseek/deepseek-v3.2 | A | all_unsure_6of8 | unsure | 1 | 0.620 | 0.620 | 0.000 | 0.700 | 0.700 |
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
| openrouter:deepseek/deepseek-v3.2 | A | none | certain | 1 | 0.500 | 0.500 | - | - | - |
| openrouter:deepseek/deepseek-v3.2 | A | none | unsure | 1 | 0.330 | 0.330 | - | - | - |
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
| anthropic:claude-haiku-5-5 | A | 34 | 0.130 | 0.333 |
| anthropic:claude-haiku-5-5 | B | 34 | 0.186 | 0.284 |
| gemma4:12b | A | 34 | 0.206 | 0.422 |
| ministral-3:8b | A | 34 | 0.199 | 0.365 |
| ministral-3:8b | B | 34 | 0.190 | 0.356 |
| openai:gpt-6-luna | A | 34 | 0.226 | 0.362 |
| openrouter:deepseek/deepseek-v3.2 | A | 34 | 0.209 | 0.391 |
| openrouter:mistralai/ministral-14b-2512 | A | 34 | 0.196 | 0.357 |

Curve table (stated probability vs flip rate): 353 points, in the JSON under `curve`.

## Warnings

- probe probabilities read on a 0-100 scale (divided by 100) in: probe_dev__anthropic_claude-haiku-5-5__A.jsonl, probe_dev__anthropic_claude-haiku-5-5__B.jsonl, probe_dev__gemma4_12b__A.jsonl, probe_dev__ministral-3_8b__A.jsonl, probe_dev__ministral-3_8b__B.jsonl, probe_dev__openai_gpt-6-luna__A.jsonl, probe_dev__openrouter_deepseek_deepseek-v3.2__A.jsonl, probe_dev__openrouter_mistralai_ministral-14b-2512__A.jsonl
