# Arm R (reversed entry order) vs arm A

Generated 2026-11-16 03:11 by `harness/posthoc/arm_r.py`. Exploratory. Pre-run record and predictions: `harness_x/FREEZE_X.md`, Deviations item 5. Arm R is arm A with the eight log entries shown in reverse order: the first entry is (C) unsure-voice and the last (B) certain-voice.

Answer-only, stratum wrong, target key. Strict missing rule (error, final "?", done "length", trunc_risk). Items: non-missing in c|CR, c|UR, u|UR, u|CR and u|PM in both arms. Replicates are averaged within item and cell (gemma4:12b and Llama 3.3 70B arm A: rep1 and rep2 for the four core cells; their rep2 did not run perfect_mixed, so u|PM is rep1 only). d_c = c|CR - c|UR; d_u = u|UR - u|CR; D = d_c - d_u; C3 = u|PM - u|UR. Estimate [paired item-bootstrap 95% interval, 2000 resamples, seed 20261116]. CR = certain_right, UR = unsure_right, PM = perfect_mixed.

ministral-3:8b: the primary arm A is the same-day repeat in `harness_x/runs` (its system prompt carries the date; the original arm A ran on 15 Nov); the line against the original 15 Nov file is secondary.

## Files

| pair | file | unique wrong/key rows (g0 + perfect_mixed) | missing trials in the 5 needed cells |
|---|---|---|---|
| gemma4:12b | `harness_x/runs/test__gemma4_12b__instant__R.jsonl` | 720 | 0 |
| gemma4:12b | `harness/runs/test__gemma4_12b__instant__A.jsonl` | 800 | 0 |
| gemma4:12b | `harness/runs/test__gemma4_12b__instant__A__rep2.jsonl` | 560 | 0 |
| Llama 3.3 70B | `harness_x/runs/test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__R.jsonl` | 720 | 0 |
| Llama 3.3 70B | `harness/runs/test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl` | 800 | 0 |
| Llama 3.3 70B | `harness/runs/test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A__rep2.jsonl` | 560 | 0 |
| Llama 4 Maverick | `harness_x/runs/test__openrouter_meta-llama_llama-4-maverick__instant__R.jsonl` | 720 | 0 |
| Llama 4 Maverick | `harness_x/runs/test__openrouter_meta-llama_llama-4-maverick__instant__A.jsonl` | 800 | 0 |
| ministral-3:8b | `harness_x/runs/test__ministral-3_8b__instant__R.jsonl` | 720 | 0 |
| ministral-3:8b | `harness_x/runs/test__ministral-3_8b__instant__A.jsonl` | 720 | 0 |
| ministral-3:8b vs 15 Nov arm A (secondary) | `harness_x/runs/test__ministral-3_8b__instant__R.jsonl` | 720 | 0 |
| ministral-3:8b vs 15 Nov arm A (secondary) | `harness/runs/test__ministral-3_8b__instant__A.jsonl` | 800 | 0 |
| GPT-6 Sol | `harness_x/runs/test__openai_gpt-6-sol__instant__R.jsonl` | 720 | 0 |
| GPT-6 Sol | `harness/runs/test__openai_gpt-6-sol__instant__A.jsonl` | 800 | 0 |
| Claude Sonnet 5.5 | `harness_x/runs/test__anthropic_claude-sonnet-5-5__instant__R.jsonl` | 720 | 0 |
| Claude Sonnet 5.5 | `harness/runs/test__anthropic_claude-sonnet-5-5__instant__A.jsonl` | 800 | 0 |

## 1. Per arm

| model | arm | n | c\|CR | c\|UR | u\|UR | u\|CR | u\|PM | d_c | d_u | D | C3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4:12b | A | 80 | 0.338 | 0.000 | 0.000 | 0.000 | 0.475 | +0.338 [+0.237, +0.438] | +0.000 [+0.000, +0.000] | +0.338 [+0.237, +0.438] | +0.475 [+0.362, +0.588] |
| gemma4:12b | R | 80 | 0.013 | 0.000 | 0.000 | 0.000 | 0.562 | +0.013 [+0.000, +0.037] | +0.000 [+0.000, +0.000] | +0.013 [+0.000, +0.037] | +0.562 [+0.450, +0.675] |
| Llama 3.3 70B | A | 80 | 0.769 | 0.269 | 0.312 | 0.400 | 0.750 | +0.500 [+0.388, +0.613] | -0.087 [-0.150, -0.025] | +0.588 [+0.450, +0.738] | +0.438 [+0.325, +0.550] |
| Llama 3.3 70B | R | 80 | 0.613 | 0.575 | 0.425 | 0.225 | 0.738 | +0.037 [+0.000, +0.087] | +0.200 [+0.113, +0.287] | -0.163 [-0.250, -0.075] | +0.312 [+0.212, +0.412] |
| Llama 4 Maverick | A | 80 | 0.725 | 0.050 | 0.037 | 0.100 | 0.487 | +0.675 [+0.575, +0.775] | -0.062 [-0.125, -0.013] | +0.738 [+0.625, +0.850] | +0.450 [+0.338, +0.562] |
| Llama 4 Maverick | R | 80 | 0.312 | 0.287 | 0.175 | 0.013 | 0.562 | +0.025 [-0.037, +0.100] | +0.163 [+0.087, +0.250] | -0.138 [-0.237, -0.037] | +0.388 [+0.287, +0.500] |
| ministral-3:8b | A | 80 | 0.450 | 0.150 | 0.037 | 0.138 | 0.287 | +0.300 [+0.212, +0.400] | -0.100 [-0.175, -0.037] | +0.400 [+0.287, +0.525] | +0.250 [+0.150, +0.338] |
| ministral-3:8b | R | 80 | 0.200 | 0.400 | 0.138 | 0.025 | 0.338 | -0.200 [-0.287, -0.113] | +0.113 [+0.050, +0.188] | -0.312 [-0.425, -0.212] | +0.200 [+0.113, +0.287] |
| ministral-3:8b vs 15 Nov arm A (secondary) | A | 80 | 0.463 | 0.188 | 0.050 | 0.150 | 0.275 | +0.275 [+0.175, +0.388] | -0.100 [-0.175, -0.037] | +0.375 [+0.250, +0.500] | +0.225 [+0.138, +0.312] |
| ministral-3:8b vs 15 Nov arm A (secondary) | R | 80 | 0.200 | 0.400 | 0.138 | 0.025 | 0.338 | -0.200 [-0.287, -0.113] | +0.113 [+0.050, +0.188] | -0.312 [-0.425, -0.212] | +0.200 [+0.113, +0.287] |
| GPT-6 Sol | A | 80 | 0.600 | 0.087 | 0.525 | 0.062 | 0.400 | +0.512 [+0.400, +0.625] | +0.463 [+0.350, +0.575] | +0.050 [-0.050, +0.150] | -0.125 [-0.212, -0.050] |
| GPT-6 Sol | R | 80 | 0.550 | 0.087 | 0.562 | 0.087 | 0.425 | +0.463 [+0.362, +0.575] | +0.475 [+0.375, +0.588] | -0.013 [-0.100, +0.075] | -0.138 [-0.225, -0.062] |
| Claude Sonnet 5.5 | A | 80 | 0.887 | 0.000 | 0.838 | 0.000 | 0.875 | +0.887 [+0.812, +0.950] | +0.838 [+0.750, +0.912] | +0.050 [-0.050, +0.150] | +0.037 [-0.050, +0.125] |
| Claude Sonnet 5.5 | R | 80 | 0.775 | 0.000 | 0.750 | 0.000 | 0.887 | +0.775 [+0.675, +0.863] | +0.750 [+0.650, +0.838] | +0.025 [-0.075, +0.125] | +0.138 [+0.037, +0.237] |

## 2. Paired differences, arm R minus arm A (same items)

| model | n | D: R - A | C3: R - A | d_c: R - A | d_u: R - A |
|---|---|---|---|---|---|
| gemma4:12b | 80 | -0.325 [-0.425, -0.225] | +0.087 [+0.000, +0.188] | -0.325 [-0.425, -0.225] | +0.000 [+0.000, +0.000] |
| Llama 3.3 70B | 80 | -0.750 [-0.950, -0.556] | -0.125 [-0.200, -0.062] | -0.463 [-0.575, -0.356] | +0.287 [+0.163, +0.425] |
| Llama 4 Maverick | 80 | -0.875 [-1.050, -0.713] | -0.062 [-0.163, +0.037] | -0.650 [-0.762, -0.537] | +0.225 [+0.125, +0.338] |
| ministral-3:8b | 80 | -0.713 [-0.925, -0.525] | -0.050 [-0.125, +0.025] | -0.500 [-0.675, -0.338] | +0.212 [+0.100, +0.350] |
| ministral-3:8b vs 15 Nov arm A (secondary) | 80 | -0.688 [-0.887, -0.487] | -0.025 [-0.113, +0.062] | -0.475 [-0.650, -0.312] | +0.212 [+0.100, +0.338] |
| GPT-6 Sol | 80 | -0.062 [-0.200, +0.075] | -0.013 [-0.113, +0.087] | -0.050 [-0.150, +0.050] | +0.013 [-0.087, +0.113] |
| Claude Sonnet 5.5 | 80 | -0.025 [-0.163, +0.100] | +0.100 [-0.025, +0.225] | -0.113 [-0.200, -0.037] | -0.087 [-0.200, +0.037] |

## 3. Predictions (fixed before any arm R call)

- P1, each open-weight model: "D is lower in arm R than in arm A on the same items, and negative."
- P2, Sol (item 5) and Claude Sonnet 5.5 (item 6, added later): "|D| in arm R < 0.15, and both d_c and d_u > 0.3."

Verdicts use the point estimates: met = every condition holds, mixed = some hold, not met = none. The interval column says whether each condition also holds for the whole 95% interval.

| prediction | model | estimates | holds for the whole interval? | verdict |
|---|---|---|---|---|
| P1 | gemma4:12b | D_R - D_A = -0.325 [-0.425, -0.225]; D_R = +0.013 [+0.000, +0.037] | R - A below 0: yes; D_R below 0: no | mixed |
| P1 | Llama 3.3 70B | D_R - D_A = -0.750 [-0.950, -0.556]; D_R = -0.163 [-0.250, -0.075] | R - A below 0: yes; D_R below 0: yes | met |
| P1 | Llama 4 Maverick | D_R - D_A = -0.875 [-1.050, -0.713]; D_R = -0.138 [-0.237, -0.037] | R - A below 0: yes; D_R below 0: yes | met |
| P1 | ministral-3:8b | D_R - D_A = -0.713 [-0.925, -0.525]; D_R = -0.312 [-0.425, -0.212] | R - A below 0: yes; D_R below 0: yes | met |
| P1 (secondary) | ministral-3:8b vs 15 Nov arm A (secondary) | D_R - D_A = -0.688 [-0.887, -0.487]; D_R = -0.312 [-0.425, -0.212] | R - A below 0: yes; D_R below 0: yes | met |
| P2 | GPT-6 Sol | D_R = -0.013 [-0.100, +0.075]; d_c_R = +0.463 [+0.362, +0.575]; d_u_R = +0.475 [+0.375, +0.588] | |D_R| < .15: yes; d_c_R > .3: yes; d_u_R > .3: yes | met |
| P2 | Claude Sonnet 5.5 | D_R = +0.025 [-0.075, +0.125]; d_c_R = +0.775 [+0.675, +0.863]; d_u_R = +0.750 [+0.650, +0.838] | |D_R| < .15: yes; d_c_R > .3: yes; d_u_R > .3: yes | met |

P1 across the open-weight models (primary lines): 3 met, 1 mixed, 0 not met, 0 pending.

## 4. C3 in arm R (descriptive; no prediction was made)

In arm R both perfect_mixed and unsure_right open with an unsure-voice entry marked right, so the first line does not differ between the two logs.

| model | n | u\|PM, R | u\|UR, R | C3, R | C3, A | C3: R - A |
|---|---|---|---|---|---|---|
| gemma4:12b | 80 | 0.562 | 0.000 | +0.562 [+0.450, +0.675] | +0.475 [+0.362, +0.588] | +0.087 [+0.000, +0.188] |
| Llama 3.3 70B | 80 | 0.738 | 0.425 | +0.312 [+0.212, +0.412] | +0.438 [+0.325, +0.550] | -0.125 [-0.200, -0.062] |
| Llama 4 Maverick | 80 | 0.562 | 0.175 | +0.388 [+0.287, +0.500] | +0.450 [+0.338, +0.562] | -0.062 [-0.163, +0.037] |
| ministral-3:8b | 80 | 0.338 | 0.138 | +0.200 [+0.113, +0.287] | +0.250 [+0.150, +0.338] | -0.050 [-0.125, +0.025] |
| ministral-3:8b vs 15 Nov arm A (secondary) | 80 | 0.338 | 0.138 | +0.200 [+0.113, +0.287] | +0.225 [+0.138, +0.312] | -0.025 [-0.113, +0.062] |
| GPT-6 Sol | 80 | 0.425 | 0.562 | -0.138 [-0.225, -0.062] | -0.125 [-0.212, -0.050] | -0.013 [-0.113, +0.087] |
| Claude Sonnet 5.5 | 80 | 0.887 | 0.750 | +0.138 [+0.037, +0.237] | +0.037 [-0.050, +0.125] | +0.100 [-0.025, +0.225] |

## 5. Order-averaged effects (follow-up)

Per item, the mean of arm A and arm R (entries shown in BASE order and in reverse order), then averaged over items; same items and bootstrap draws as above. If entry order explained everything, the order-averaged D would be about 0. 'Excludes 0' refers to the 95% interval.

| model | n | d_c, avg(A, R) | excludes 0 | d_u, avg(A, R) | excludes 0 | D, avg(A, R) | excludes 0 |
|---|---|---|---|---|---|---|---|
| gemma4:12b | 80 | +0.175 [+0.125, +0.231] | yes (above) | +0.000 [+0.000, +0.000] | no | +0.175 [+0.125, +0.231] | yes (above) |
| Llama 3.3 70B | 80 | +0.269 [+0.206, +0.334] | yes (above) | +0.056 [+0.019, +0.100] | yes (above) | +0.212 [+0.147, +0.281] | yes (above) |
| Llama 4 Maverick | 80 | +0.350 [+0.287, +0.419] | yes (above) | +0.050 [+0.006, +0.094] | yes (above) | +0.300 [+0.231, +0.375] | yes (above) |
| ministral-3:8b | 80 | +0.050 [+0.006, +0.094] | yes (above) | +0.006 [-0.019, +0.031] | no | +0.044 [-0.006, +0.094] | no |
| GPT-6 Sol | 80 | +0.487 [+0.394, +0.581] | yes (above) | +0.469 [+0.369, +0.569] | yes (above) | +0.019 [-0.044, +0.075] | no |
| Claude Sonnet 5.5 | 80 | +0.831 [+0.756, +0.894] | yes (above) | +0.794 [+0.725, +0.863] | yes (above) | +0.037 [-0.037, +0.119] | no |
