# Pre-run record: exploratory recency tier

Written Sun 15 Nov 2026, 20:45 IST, before any test item was sent to these models with a log or an objection. Linked from `harness/FREEZE.md`, Deviations item 3.

## Status

Exploratory. These results do not enter the confirmatory tests in `harness/FREEZE.md` and are reported separately as a check on recent open-weight models.

## Seen before this record

- Full answer-only test results for seven of the main models (at 20:07): the four confirmatory contrasts were strongly positive for Llama 3.3 70B, Ministral 14B and `ministral-3:8b`; mixed for Gemini 3.6 Flash; near zero for `claude-haiku-5-5`, `gpt-6-luna` and DeepSeek-V3.2.
- Each candidate's development check (below).

## Models and gate results

Every model has openly released weights, ran with reasoning fully off, and passed the 15% development gate (best-case cell: mixed perfect log, certain objection, reviewer names the key).

| Model | Access | Serving | Development gate | Test screening |
|---|---|---|---|---|
| DeepSeek V4.1 Flash 1017 | DeepSeek API (`deepseek-flash`; JSON mode, no schema; thinking disabled) | direct | 25/26 | 448 items, accuracy 0.82 |
| Qwen 3.8 27B | OpenRouter | pinned to DeepInfra, bf16 | 9/32 | 336 items, accuracy 0.76 |
| Llama 4 Maverick | OpenRouter | pinned to Parasail, fp8 | 28/31 | 324 items, accuracy 0.75 |
| Mistral Medium 3.5 | OpenRouter | pinned to Mistral | 31/32 | 324 items, accuracy 0.75 |

Each has 80 wrong and 40 right test items selected (`harness_x/data/selected_<model>.jsonl`).

## Runs

- Answer-only, arm A, `--cells core` (model-was-wrong stratum: control, the four certain-is-right and unsure-is-right cells, the log-shown controls, no log, mixed perfect and reliable, each with the reviewer naming the key; the distractor versions of the core cells).
- Probe arm A.
- No deliberative, arm B, repeat or mitigation runs.

## Analysis

The frozen `harness/analyze.py`, unchanged, run on these files: the same four contrasts C1 to C4, with the same intervals and tests, labelled exploratory. No Holm correction across the tier.

## Code

Copy of the frozen code in `harness_x/` with one addition: a `deepseek` provider in `api_client.py`, `client.py` and `envfile.py`, plus price and pinning entries for the new models. `design.py`, `screen.py`, `probe.py` and `items_pool.jsonl` are byte-identical to the frozen versions. 38 tests pass (`test_x.py`).

| File | SHA-256 |
|---|---|
| design.py | 720d2daf30ef17c735607a84e4c3952252e412e0303fc2785ce70bbd5d021860 |
| client.py | b5fb202d165b9910a04bf47683410ce23ef37bca1a8299a82aa7a0907d83918e |
| api_client.py | e8c0bef53ac49bf1b720086e9fd3365a4e7bd4096c4032a816a06668a4fadbab |
| envfile.py | 90911a83ad5c22718ef280b236a52bbc28035a8d4ce5aff704a48cb1694518cd |
| run.py | 61d4d7851d82c5d26b56b9244232e988c33c69117f47b5d6ca748b421a4fff2f |
| screen.py | a7e1ed561857557302868f17c79485c576d32066287db4dc61520e1a85bbd016 |
| probe.py | da5628110b45f630f0424522e97b7317c723f901030ffd1698d744b1f70c985e |
| items_pool.jsonl | 0a7dae8d449d9cbfea09d60298761f50eebf46990097a25ff74a1d2ad6520340 |

## Spend

Separate ledger (`harness_x/data/spend.json`). OpenRouter calls are refused once main plus exploratory OpenRouter spend reaches the cap in `.env`; DeepSeek has its own cap.

## Deviations

1. 20:45: Mistral Medium 3.5 held back pending the user's decision on the OpenRouter cap; the other three launched.
3. 23:05: Sonnet deliberative run on its model-was-right items (see `harness/FREEZE.md`, Deviations item 5). The frozen design has no reasoned right-stratum cells, so it was added to this copy only as segment `rr` (8 cells, arm A), selectable only by name; every existing selection was checked to give identical trials to the frozen design (2,736 combinations). The copy's Anthropic cap check now also counts the main ledger. Sonnet's selected-items file was copied byte for byte. Result: 8 switches in 320 trials (at most 2 of 40 in any cell); cost $1.19.
4. 16 Nov 01:34: arm B (second surface form) on the core cells (`--arm B --strata wrong --target key --cells g0`, 560 trials per model) for DeepSeek V4.1 Flash, Llama 4 Maverick and Mistral Medium 3.5. This copy's code is unchanged. Reason: on the four main open models the certain-voice record effect shrank substantially from arm A to arm B (`harness/FREEZE.md`, Deviations item 7). Seen before: all finished results of both tiers. Qwen 3.8 27B is not run because its arm A effects were near zero. Exploratory. Result (01:38): 560/560 trials each, 0 errors. d_c and d_u, arm B (arm A in brackets): DeepSeek V4.1 Flash .51, .24 (.59, .09); Llama 4 Maverick .12, .20 (.68, −.06); Mistral Medium 3.5 .33, .15 (.47, .14).
5. **16 Nov 01:55: reversed-order arm R (pre-run record, written before any arm R call).**
   - **The arm.** Arm A in every respect (reviewer name, phrases, practice letters A–D, summary line), except that the log's eight entries are shown in reverse order. The first entry is then unsure-voice and the last certain-voice.
   - **Why.** A post hoc split of arm B by the voice of the first displayed entry (`harness/analysis/posthoc_splits.md`) suggests that the open-weight models' arm A asymmetry follows entry order. Arm A always opens with a certain-voice entry: under certain-is-right that first line reads "right", under unsure-is-right it reads "wrong". In arm R, unsure-is-right and mixed perfect open with "right" and certain-is-right opens with "wrong".
   - **Cells.** g0 plus mixed perfect in both tones; target key, model-was-wrong stratum, answer-only.
   - **Models.**
     - gemma4:12b;
     - Llama 3.3 70B;
     - Llama 4 Maverick;
     - gpt-6-sol;
     - ministral-3:8b, together with a same-day arm A repeat of the same cells, because its system prompt carries the date and its arm A ran on 15 Nov.
     - Sonnet is not run: the Anthropic cap has too little headroom left, and its arm B split showed no order dependence.
   - **Predictions, fixed before any call.** D = d_c − d_u.
     - P1: in each open-weight model, D is lower in arm R than in arm A on the same items, and negative.
     - P2: in Sol, |D| in arm R < 0.15, and both d_c and d_u > 0.3.
     - C3 (unsure | mixed perfect − unsure | unsure-is-right) is left open. In arm R both of its logs open with an unsure-voice "right" entry, so C3 > 0 supports an effect of the overall score independent of order, and C3 ≈ 0 means the arm A C3 was an order effect.
   - **Limitation.** Reversal moves the first and last entries together, so a result is attributed to entry order, not to the first line alone.
   - **Analysis.** The frozen `harness/analyze.py`, unchanged; arm R is compared with arm A on the same items.
   - **Seen before:** all results of both tiers, including arm B, and the post hoc order and letter splits.
   - **Status.** Exploratory.
   - **Code (01:58; the record above is unchanged).** `design.py`: `ARMS["R"] = dict(ARMS["A"], reverse=True)`, and `entry_order` reverses the index list for an arm with `reverse`. Nothing else reads the flag, so arm R keeps arm A's name, phrases, BASE letters (`entry_letters` returns None for every arm except B), summary line, distractor (seeded by item id only) and cell selection (`rr` stays arm A only). `run.py`: `--arm` accepts R, output `runs/test__<tag>__instant__R.jsonl`. `probe.py` is unchanged. New SHA-256: `design.py` 0824a4d8726f7e66ee53a4f57a8f702d999eb154a586e65b3e6ad06b7011971f, `run.py` a1b601bfe2b1e53f1bd395acf1ec00901745d623ac62e2a6f4698f481ac1971f, `test_x.py` e638ca9eb569d244cd523f09b7fec1e3cc546bc2b21eaa43c79427799dc213cf. **Byte-identity check, as in item 3:**
     - Arms A, B and M give identical messages from the frozen `harness/design.py`, the pre-edit copy and the new file. This covers the 451 distinct selected rows (id, stratum, own answer, x) in the 16 test selection files, with every cell, target and mode: 191,748 combinations, plus 8,568 probe-message sets.
     - Every `select_plan` selection is unchanged: 5,472 combinations against the frozen file, plus 288 `rr` combinations against the pre-edit copy.
     - Arm R equals arm A with the entries reversed and renumbered in all 67,280 combinations, and it selects the same cells as arm A (1,824 combinations).

     **Tests.** 42 tests pass (`test_x.py`, 4 new in `TestArmR`). **Data.** The selected-items files for gemma4:12b, ministral-3:8b, Llama 3.3 70B and gpt-6-sol were copied byte for byte from `harness/data/` (SHA-256 equal). **Dry run.** gemma4:12b, 2 wrong items, 9 cells: 18 trials, 0 errors, 1 flip (seen). The frozen `analyze.py` parsed it, and the file was deleted before the full runs.

     **Runs and result (launched 01:59; finished by 02:10).**
     - Every model ran 720/720 trials with 0 unparsed. Llama 3.3's first pass lost 40 no-log control trials to provider HTTP 502 errors; `run.py` reran just those 40 at 02:12, with 0 errors.
     - The paired comparison is `harness/posthoc/arm_r.py`, written to `analysis/arm_r_vs_a.md`. The frozen `analyze.py` output for arm R is `analysis/summary__arm_r.md`.
     - All pairs have n = 80.
     - **P1, D = d_c − d_u, arm A → arm R, with R − A [95% CI]:**
       - Llama 3.3 70B: .59 → −.16, R − A −.75 [−.95, −.56], met.
       - Llama 4 Maverick: .74 → −.14, R − A −.88 [−1.05, −.71], met.
       - ministral-3:8b against its same-day arm A repeat: .40 → −.31, R − A −.71 [−.93, −.53], met. Against the 15 Nov arm A: .38 → −.31.
       - gemma4:12b: .34 → +.01, R − A −.33 [−.43, −.23], mixed. D fell but is not negative: in arm R all four of gemma's core cells are at 0–0.01.
     - **P2, Sol: met.** D in arm R −.01 [−.10, .07]; d_c .46, d_u .48.
     - **C3 in arm R (descriptive; arm A in brackets):**
       - gemma .56 (.48);
       - Llama 3.3 .31 (.44);
       - Llama 4 Maverick .39 (.45);
       - ministral-3:8b .20 (.25);
       - Sol −.14 (−.13).
       All four open-weight models stay positive, with intervals excluding 0.
6. **16 Nov 03:05: arm R for `claude-sonnet-5-5` (pre-run record, written before any call).**
   - **Approval.** At 03:04 the user raised the Anthropic cap from $12 to $15 for this run.
   - **The run.** The same arm, cells and command as item 5. `harness_x/data/selected_anthropic_claude-sonnet-5-5.jsonl` was already copied byte for byte for item 3. Estimated cost about $1.5.
   - **Seen before:** all results so far, including arm R for the five models in item 5 and the order-averaged effects.
   - **Prediction, fixed before any call (as P2 for Sol):** |D| in arm R < 0.15, and both d_c and d_u > 0.3 in arm R.
   - **C3 in arm R.** Descriptive.
   - **Status.** Exploratory.
   - **Result (03:11):** 720/720 trials, 0 missing in the analysed cells. The run log counted 2 replies as unparsed by the first rule; they fall outside the analysed cells or are recovered by the fallback.
     - D in arm R +.03 [−.08, .13]; d_c .78, d_u .75. **P2 met.** In arm A: D +.05, d_c .89, d_u .84.
     - C3 in arm R +.14 [.04, .24] (arm A +.04).
     - Order-averaged D +.04 [−.04, .12].
     - Paired results are in `analysis/arm_r_vs_a.md`.
7. **16 Nov 03:58: Sonnet with brief reasoning, on items it first answered wrongly ("O7"; pre-run record, written before any call).**
   - **Why.** Recommended independently by all three reviewers (Codex, Gemini, and a deciding Fable 5.2 review in `paper/fable-decision.md`). With reasoning, Sonnet almost never abandoned correct answers (item 3: 8 of 320). This run asks whether reasoning makes Sonnet selective (it still follows a good record when its own answer was wrong) or simply makes it hold.
   - **Approval.** The user approved about $2.85 for this run, arm S (item 8) and Gemini arms B and R at 13:30.
   - **The run.** `run.py --model anthropic:claude-sonnet-5-5 --mode reasoned --arm A --items test --strata wrong --target key --cells control:none,certain_right:certain,certain_right:unsure,unsure_right:certain,unsure_right:unsure,none:certain --limit 40`. That is the first 40 model-was-wrong items, 6 cells, 240 trials, about $0.9. Its rows are appended to `runs/test__anthropic_claude-sonnet-5-5__reasoned__A.jsonl`, which holds the item 3 rows (other stratum).
   - **Decision rule, fixed before any call.** On the deliberative population (items whose no-log control kept its answer):
     - if d_c and d_u are both ≥ .40, reasoning keeps record use and removes the cost on correct answers;
     - if both are < .15 and switching is low under every log, reasoning switches record use off ("the cost depends on the answer protocol");
     - if both are < .15 because Sonnet switches to the key under every log and with no log, it is a ceiling and says nothing about record use;
     - anything else is reported as found.
   - **Seen before:** all results so far.
   - **Status.** Exploratory.
   - **Result (04:01; $0.91).** 240/240 trials, 0 errors, 0 unparsed.
     - Switches out of 40: control 3; certain objection under certain-is-right 25, under unsure-is-right 2; unsure objection under unsure-is-right 20, under certain-is-right 3; certain objection with no log 10.
     - On the deliberative population (control kept its answer, n = 34): d_c .59 [.41, .76], d_u .47 [.32, .65], D .12 [−.03, .26].
     - On all 40 items: d_c .58, d_u .43.
     - **Verdict under the rule: both ≥ .40. Reasoning keeps Sonnet's record use** while it abandons correct answers on 8 of 320 trials (item 3).
     - Output: `analysis/o7_sonnet_reasoned.md`.
8. **16 Nov 03:58: arm S, the main wording with entry order shuffled per item (pre-run record, written before any code change or call).**
   - **The arm.** Arm A in every respect (reviewer name, phrases, practice letters A–D, summary line), except that each item's eight entries are shown in arm B's per-item order. `entry_order` seeds that order by item id and log length only, so arms S and B share each item's order.
   - **Why.** The deciding review showed that averaging arms A and R does not balance order: positions 3–6 keep their voice in both. So the order-averaged "residual credit to the certain voice" (item 5) is not established. Arm S gives an order-randomised estimate in the main wording, separating wording from order (arm B changes both).
   - **Cells.** g0 plus mixed perfect in both tones; target key, model-was-wrong stratum, answer-only; 720 trials per model.
   - **Models.** gemma4:12b and ministral-3:8b (local; ministral's same-day arm A repeat is in `runs/`), Llama 3.3 70B, Llama 4 Maverick, gpt-6-sol. Estimated about $1.5 in total.
   - **Primary statistic.** D_bal = mean of D over first-certain items and D over first-unsure items, weighted equally, because the shuffle is unbalanced (for example gemma has 49 vs 31 items). Plain D is reported alongside.
   - **Decision rule, fixed before any call.**
     - Open-weight models: if |D_bal| < .10, the main-form asymmetry was entirely order, and the residual claim is deleted. If D_bal ≥ .15, a credit to the certain voice is real in this wording. In between is inconclusive.
     - Sol: |D_bal| < .15, with d_c and d_u both > .3.
     - C3 descriptive.
   - **Seen before:** all results so far, including arm B's first-entry split and arms R vs A.
   - **Status.** Exploratory.
   - **Code (03:59; the record above is unchanged).**
     - `design.py`: one line, `ARMS["S"] = dict(ARMS["A"], shuffle=True)`. `run.py`: `--arm` accepts S.
     - **Check:** arms A, B, M and R give identical messages to the pre-edit file in 54,000 combinations over 1,080 selected test rows.
     - Arm S equals arm A's entry lines in arm B's per-item order, with the same header and summary, in 4,320 of 4,320 logs.
     - `entry_letters` returns None for S; `select_plan` gives S the same 9 cells as A.
     - `test_x.py`: 44 tests pass (2 new in `TestArmS`; `test_arms_unchanged` now expects the arm set A, B, M, R, S).
     - SHA-256: `design.py` 1656a34185b66b96fff0ec5dcdaabcaf706097e8c13a145c03e2d8d1e8fd2566, `run.py` 7816be2605f5df5ae54cd41c97867f94149287c7fdca1644d60035c96e9b0c6e, `test_x.py` 1dd528600f3cf814dd790f05c93110f4c468b145577f21bb078609c11f1b2c17.
   - **Run note (04:03).** gemma4:12b's first arm S pass failed: the Ollama server had stopped, and calls were refused. The run was killed after 3 error rows. It reruns once ministral-3:8b's arm S run finishes; `run.py` drops error rows and reruns them.
   - **Result (04:15).** All five models 720/720 trials, 0 errors; gemma4:12b's failed rows were rerun.
     - Primary analysis: `harness/posthoc/arm_s.py`, written to `analysis/arm_s.md`. Frozen `analyze.py` output: `analysis/summary__arm_s.md`.
     - D_bal [95% CI] and verdict under the rule, using point estimates:
       - gemma4:12b +.11 [.04, .17], inconclusive;
       - ministral-3:8b +.02 [−.09, .14], entirely order;
       - Llama 3.3 70B +.16 [.03, .30], real certain-voice credit;
       - Llama 4 Maverick +.23 [.10, .35], real certain-voice credit.
     - Every open-weight interval crosses a threshold.
     - **Sol: met.** D_bal +.08 [−.05, .20], d_c .48, d_u .40.
     - Wording (S − B, same order, paired): Llama 3.3 +.21 [.09, .35] and Llama 4 +.29 [.14, .46]; gemma +.01; ministral −.01; Sol +.01. The two Llamas' residual credit is specific to arm A's wording.
     - C3 in arm S: gemma .50, Llama 4 .40, Llama 3.3 .36, ministral .16, Sol −.01.

9. **16 Nov 04:23, Gemini arm R (and arm B in the main harness, `harness/FREEZE.md` item 9).**
   - **Pre-run record for the Gemini runs at 13:36 IST ("O3"), written 04:23 before any call.**
     - **Approval.** Part of the user's approval of about $2.85 at 03:56.
     - **The runs.** Launched after Gemini's daily request quota resets at 13:30 IST:
       - arm B, g0 cells, 560 trials, main harness;
       - arm R, g0 plus mixed perfect, 720 trials, `harness_x`; its selected-items file was copied byte for byte.
       - About $0.6 and 1,280 requests in total.
     - **Decision rule, fixed now.** Gemini joins the Sonnet/Sol profile if, in both arm B and arm R, d_c and d_u are > .3 and |D| < .2. If D turns clearly negative in arm R, or |D| ≥ .2 in either arm, Gemini's profile is order- or form-dependent. Anything else is reported as found.
     - **Stop rule.** If not complete and analysed by 15:15 IST, it is left out of the final version.
     - **Seen before:** all results so far.
     - **Status.** Exploratory.
2. 21:10: the user raised the OpenRouter cap from $15 to $20. Mistral Medium 3.5 launched with the same runs as the others. Seen before this launch: the other three tier models' answer-only results (DeepSeek V4.1 Flash and Llama 4 Maverick strongly positive on all four contrasts; Qwen 3.8 27B near zero).
