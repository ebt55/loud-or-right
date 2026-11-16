# Arm S (main wording, per-item shuffled order) vs arms A, B and R

Generated 2026-11-16 04:15 by `harness/posthoc/arm_s.py`. Exploratory. Pre-run record and decision rule: `harness_x/FREEZE_X.md`, Deviations item 8. Arm S = arm A (name Dana, arm A phrases, letters A-D, summary line) with each item's entries in arm B's per-item order; arm B differs from S only in wording (name, phrases, drawn letters).

Answer-only, stratum wrong, target key; strict missing rule; replicates averaged within item and cell (gemma4:12b and Llama 3.3 70B arm A: rep1 and rep2). d_c = c|CR - c|UR; d_u = u|UR - u|CR; D = d_c - d_u; C3 = u|PM - u|UR. D_bal = mean of D over first-certain and over first-unsure items, weighted equally; its interval comes from a bootstrap stratified by subset. Item bootstrap, 2000 resamples, seed 20261116. Arm A sources as in `arm_r.py` (ministral-3:8b: the same-day repeat in `harness_x/runs`).

Order check: harness_x/design.py defines arm S; its entry_order equals arm B order for every item used.

## Files

| model | arm | file | unique wrong/key rows | missing trials in the needed cells |
|---|---|---|---|---|
| gemma4:12b | A | `harness/runs/test__gemma4_12b__instant__A.jsonl` | 800 | 0 |
| gemma4:12b | A | `harness/runs/test__gemma4_12b__instant__A__rep2.jsonl` | 560 | 0 |
| gemma4:12b | B | `harness/runs/test__gemma4_12b__instant__B.jsonl` | 800 | 0 |
| gemma4:12b | R | `harness_x/runs/test__gemma4_12b__instant__R.jsonl` | 720 | 0 |
| gemma4:12b | S | `harness_x/runs/test__gemma4_12b__instant__S.jsonl` | 720 | 0 |
| ministral-3:8b | A | `harness_x/runs/test__ministral-3_8b__instant__A.jsonl` | 720 | 0 |
| ministral-3:8b | B | `harness/runs/test__ministral-3_8b__instant__B.jsonl` | 800 | 0 |
| ministral-3:8b | R | `harness_x/runs/test__ministral-3_8b__instant__R.jsonl` | 720 | 0 |
| ministral-3:8b | S | `harness_x/runs/test__ministral-3_8b__instant__S.jsonl` | 720 | 0 |
| Llama 3.3 70B | A | `harness/runs/test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A.jsonl` | 800 | 0 |
| Llama 3.3 70B | A | `harness/runs/test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__A__rep2.jsonl` | 560 | 0 |
| Llama 3.3 70B | B | `harness/runs/test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__B.jsonl` | 800 | 0 |
| Llama 3.3 70B | R | `harness_x/runs/test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__R.jsonl` | 720 | 0 |
| Llama 3.3 70B | S | `harness_x/runs/test__openrouter_meta-llama_llama-3.3-70b-instruct__instant__S.jsonl` | 720 | 0 |
| Llama 4 Maverick | A | `harness_x/runs/test__openrouter_meta-llama_llama-4-maverick__instant__A.jsonl` | 800 | 0 |
| Llama 4 Maverick | B | `harness_x/runs/test__openrouter_meta-llama_llama-4-maverick__instant__B.jsonl` | 560 | 0 |
| Llama 4 Maverick | R | `harness_x/runs/test__openrouter_meta-llama_llama-4-maverick__instant__R.jsonl` | 720 | 0 |
| Llama 4 Maverick | S | `harness_x/runs/test__openrouter_meta-llama_llama-4-maverick__instant__S.jsonl` | 720 | 0 |
| GPT-6 Sol | A | `harness/runs/test__openai_gpt-6-sol__instant__A.jsonl` | 800 | 0 |
| GPT-6 Sol | B | `harness/runs/test__openai_gpt-6-sol__instant__B.jsonl` | 560 | 0 |
| GPT-6 Sol | R | `harness_x/runs/test__openai_gpt-6-sol__instant__R.jsonl` | 720 | 0 |
| GPT-6 Sol | S | `harness_x/runs/test__openai_gpt-6-sol__instant__S.jsonl` | 720 | 0 |

## 1. Arm S on all items

| model | n | c\|CR | c\|UR | u\|UR | u\|CR | d_c | d_u | D | C3 (n) |
|---|---|---|---|---|---|---|---|---|---|
| gemma4:12b | 80 | 0.163 | 0.025 | 0.000 | 0.000 | +0.138 [+0.062, +0.225] | +0.000 [+0.000, +0.000] | +0.138 [+0.062, +0.225] | +0.500 [+0.388, +0.613] (80) |
| ministral-3:8b | 80 | 0.312 | 0.250 | 0.113 | 0.087 | +0.062 [-0.050, +0.175] | +0.025 [-0.025, +0.087] | +0.037 [-0.087, +0.188] | +0.163 [+0.087, +0.250] (80) |
| Llama 3.3 70B | 80 | 0.662 | 0.412 | 0.375 | 0.287 | +0.250 [+0.150, +0.362] | +0.087 [-0.013, +0.188] | +0.163 [-0.013, +0.338] | +0.362 [+0.263, +0.475] (80) |
| Llama 4 Maverick | 80 | 0.500 | 0.212 | 0.113 | 0.037 | +0.287 [+0.163, +0.425] | +0.075 [+0.000, +0.150] | +0.212 [+0.050, +0.375] | +0.400 [+0.300, +0.500] (80) |
| GPT-6 Sol | 80 | 0.600 | 0.125 | 0.487 | 0.087 | +0.475 [+0.362, +0.588] | +0.400 [+0.300, +0.500] | +0.075 [-0.050, +0.200] | -0.013 [-0.087, +0.075] (80) |

## 2. Primary statistic: D_bal (arm S)

| model | n first certain / unsure | D, first certain | D, first unsure | D_bal (stratified CI) | plain D |
|---|---|---|---|---|---|
| gemma4:12b | 49 / 31 | +0.245 [+0.122, +0.367] | -0.032 [-0.097, +0.000] | +0.106 [+0.039, +0.173] | +0.138 [+0.062, +0.225] |
| ministral-3:8b | 42 / 38 | +0.381 [+0.214, +0.571] | -0.342 [-0.500, -0.211] | +0.019 [-0.094, +0.140] | +0.037 [-0.087, +0.188] |
| Llama 3.3 70B | 40 / 40 | +0.650 [+0.425, +0.875] | -0.325 [-0.500, -0.150] | +0.163 [+0.025, +0.300] | +0.163 [-0.013, +0.338] |
| Llama 4 Maverick | 39 / 41 | +0.769 [+0.615, +0.924] | -0.317 [-0.488, -0.146] | +0.226 [+0.102, +0.350] | +0.212 [+0.050, +0.375] |
| GPT-6 Sol | 43 / 37 | +0.070 [-0.093, +0.233] | +0.081 [-0.108, +0.270] | +0.075 [-0.050, +0.197] | +0.075 [-0.050, +0.200] |

## 3. Decision rule (fixed before any arm S call)

- Open-weight models: |D_bal| < .10: the main-form asymmetry was entirely order (the residual claim is deleted); D_bal >= .15: a credit to the certain voice is real in this wording; otherwise inconclusive.
- Sol: |D_bal| < .15, with d_c and d_u both > .3.

Verdicts use the point estimates, as the rule is written; the last column says where the 95% interval lies.

| model | estimates | interval | verdict |
|---|---|---|---|
| gemma4:12b | D_bal = +0.106 [+0.039, +0.173] | spans the thresholds | inconclusive |
| ministral-3:8b | D_bal = +0.019 [-0.094, +0.140] | spans the thresholds | entirely order |
| Llama 3.3 70B | D_bal = +0.163 [+0.025, +0.300] | spans the thresholds | real certain-voice credit |
| Llama 4 Maverick | D_bal = +0.226 [+0.102, +0.350] | spans the thresholds | real certain-voice credit |
| GPT-6 Sol | D_bal = +0.075 [-0.050, +0.197]; d_c = +0.475 [+0.362, +0.588]; d_u = +0.400 [+0.300, +0.500] | |D_bal| < .15 for the whole interval: no; d_c > .3: yes; d_u > .3: no | met |

## 4. D across arms, paired on items

Items non-missing in the four core cells in arms A, B, R and S. S - B isolates wording (S and B share each item's order); S - A isolates order (S and A share the wording). D_bal for B and S uses the same first-voice split (stratified intervals).

| model | n | D, A | D, B | D, R | D, S | S - A | S - B | D_bal, B | D_bal, S | D_bal: S - B |
|---|---|---|---|---|---|---|---|---|---|---|
| gemma4:12b | 80 | +0.338 [+0.237, +0.438] | +0.125 [+0.000, +0.250] | +0.013 [+0.000, +0.037] | +0.138 [+0.062, +0.225] | -0.200 [-0.325, -0.087] | +0.013 [-0.113, +0.138] | +0.066 [-0.055, +0.176] | +0.106 [+0.039, +0.173] | +0.040 [-0.078, +0.171] |
| ministral-3:8b | 80 | +0.400 [+0.287, +0.525] | +0.050 [-0.100, +0.212] | -0.312 [-0.425, -0.212] | +0.037 [-0.087, +0.188] | -0.362 [-0.537, -0.212] | -0.013 [-0.150, +0.125] | +0.030 [-0.093, +0.165] | +0.019 [-0.094, +0.140] | -0.011 [-0.145, +0.129] |
| Llama 3.3 70B | 80 | +0.588 [+0.450, +0.738] | -0.050 [-0.200, +0.100] | -0.163 [-0.250, -0.075] | +0.163 [-0.013, +0.338] | -0.425 [-0.644, -0.200] | +0.212 [+0.087, +0.350] | -0.050 [-0.175, +0.075] | +0.163 [+0.025, +0.300] | +0.213 [+0.087, +0.338] |
| Llama 4 Maverick | 80 | +0.738 [+0.625, +0.850] | -0.075 [-0.287, +0.138] | -0.138 [-0.237, -0.037] | +0.212 [+0.050, +0.375] | -0.525 [-0.713, -0.325] | +0.287 [+0.137, +0.463] | -0.059 [-0.219, +0.104] | +0.226 [+0.102, +0.350] | +0.285 [+0.124, +0.447] |
| GPT-6 Sol | 80 | +0.050 [-0.050, +0.150] | +0.062 [-0.037, +0.150] | -0.013 [-0.100, +0.075] | +0.075 [-0.050, +0.200] | +0.025 [-0.125, +0.175] | +0.013 [-0.150, +0.163] | +0.066 [-0.033, +0.164] | +0.075 [-0.050, +0.197] | +0.010 [-0.149, +0.157] |
