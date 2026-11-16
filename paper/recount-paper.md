# Number audit: paper.md against the analysis outputs (16 Nov)

Rule: two decimals, half away from zero. AF3 = `harness/analysis/all_final3.json`; PS = `harness/analysis/posthoc_splits.md`.

## Mismatches: 8 numeric values, 7 claims

| Line | As written | Source value | Correct | Source |
|---|---|---|---|---|
| 72 | Sol [0.40, **0.62**], [0.35, **0.57**] | .625, .575 | 0.63, 0.58 | AF3; Tables D1 and D2 agree with the source |
| 78 | Sonnet arm B "0.68 and **0.62**" | .625 | 0.63 | AF3 (known) |
| 92 | Llama 3.3 "0.50 → **0.12**" | .125 | 0.13 | AF3 (known) |
| 97, 339 | +0.41 [**0.33**, 0.51] | .3215 (rerun of splits.py) | 0.32 | PS §3a |
| 346 | Luna "+0.09 and **+0.07**" | 6/80 = .075 | 0.08 | PS §6, which prints +0.07 (Python rounding) |
| 380 | D10 Mistral Medium d_c **0.47** | .475 | 0.48 | AF3 |
| 383 | D10 Maverick arm B **0.12** | .125 | 0.13 | AF3 |
| 356 | "open-weight C1 +0.19 to +0.29, all Holm p < 0.01" | Qwen 3.5 +.065 (p .80); DeepSeek V3.2 +.10 (p .043) | Name the four: Gemma, both Ministrals, Llama 3.3 | AF3, deliberative |
| 343 | D4 "order-averaged effects" | No such column in Table D5; FREEZE_X item 8 calls the estimate "not established" | Delete | `arm_r_vs_a.md` §5 |
| 137 | "every model except two gave 1.00 … and 0.00" | Mixed-perfect probes: Gemma 0.75, Haiku 0.95 | Limit to the certain-is-right and unsure-is-right logs | AF3 probe |
| 86 | "no more than with no log (Sonnet 9 vs 7 … of 80)" | 9/80 vs 7/**79**; 9 > 7 | Reword | AF3 |
| 80 | "C3 was zero or negative" | Sonnet +.0375 | "near zero or negative" | AF3 |
| 66 | "2,000 otherwise"; "531–560 … per model" | Arm B, mitigation and O7 intervals used 10,000 resamples; only 9 of 15 models were repeated | Reword | AF3 |
| 353, 144 | Qwen "0.51–0.74"; Sonnet "0 or 1" | The mixed-perfect probe is 0.99; the four cells are all 0 | Minor | AF3 |

## Confirmed, with model sets

- L90 and L129 (arm A): the seven open-weight models with clear effects (Gemma, both Ministrals, both Llamas, DeepSeek V4.1, Mistral Medium). L92's "five of seven" refers to the same seven.
- L129: arm B covers four main models (the recency tier has no mixed-perfect cell); arm R covers Gemma, Ministral 3 8B, Llama 3.3 and Maverick.
- L131 and D5: six main open-weight models. L133: ten models; the second-form range covers six.
- Recomputed and matching: D3's per-model range, the placebo, the letter split, and +0.42 [0.34, 0.50].
- Counts all match: 25/40, 38, 2, 20 vs 3, 10/40, 34, 8/320, 21/23/30/31, 37, 7/79, 27/80, 25 vs 7, 58 vs 5, 15 vs 8, 173/147, 593/2,400, 560/546–557/531.
- Tables D1–D4 (534 values, checked by script) and Table D5 have no mismatch.
- Table 1 (T6): every value matches. Its arm S column is plain D (Gemma 0.14, Maverick 0.21), while §4.2 reports D_bal (0.11, 0.23). The column label should say so.

## Not traceable to a listed output

- L148, −0.30 [−0.35, −0.26]: a recount from raw rows gives −.303 [−.347, −.256], which matches.
- L151, "38": raw rows only; matches.
- L501, "$41": the spend ledgers sum to $41.34.
- L307, Gemini's 10,000-request limit: stated only in `harness/FREEZE.md`.
- L321, sprint dates: not checkable.
