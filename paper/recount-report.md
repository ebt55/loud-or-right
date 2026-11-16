# Number audit: report.md against the analysis outputs (16 Nov)

Rule: two decimals, half away from zero. AF3 = `harness/analysis/all_final3.md`; PS = `posthoc_splits.md`.

## Mismatches: 0 numeric, 2 claim-level (plus 3 wording notes)

| Line | As written | Correct | Source |
|---|---|---|---|
| 67 (claim) | d_c "fell sharply in five of seven open-weight models … while Sonnet and Sol held" | Sonnet's d_c fell 0.89 → 0.68 (B − A −0.26 [−0.41, −0.13]). That drop is larger than Gemma's (0.16) or Ministral 3 8B's (0.19). What held is Sonnet's balance (D 0.05 → 0.05). | PS §1, §3g |
| 55 (claim) | "The profile held … without the per-voice summary line" | Sonnet: d_c 0.69, d_u 0.53, D +0.16 [0.03, 0.29]. That is outside the 0.15 bound and the interval excludes 0. Sol holds (0.50, 0.46). | AF3, Sonnet nosum |
| 67 (wording) | "five of seven open-weight models" | Nine open-weight models ran arm B; the seven meant are "those with clear effects" (L61). Mistral Medium fell 0.15, Gemma 0.16, so the line for "sharply" is a judgment call. | PS §1 |
| 71 (wording) | "D_bal below 0.10" | The frozen rule is \|D_bal\| < .10. Harmless here: no estimate is negative. | `arm_s.md` §3 |
| A2 (wording) | 4,096 tokens of headroom "where hidden reasoning cannot be fully switched off" | Only Gemini got headroom (4,128/5,596/4,160). Sonnet ("between_tools", `reserve=False`) ran at 32/1,500/64. | AF3 meta, `api_client.py` |

**Verified, no change needed**
- **New counts** (AF3 and raw rows): 105 and 8 of 160; 105 and 8 of 320; 0 or 1 of 40; Sonnet 9 and 8 vs 7 of 79; Sol 26 vs 27; Luna C3 +0.16 [0.06, 0.26].
- **Paired difference** −0.30 [−0.35, −0.26]: raw recount −0.303 [−0.347, −0.256].
- **Section 4.4** matches `o7_sonnet_reasoned.md`; "less often" holds (25 vs 38 of 40).
- **Arms R and S** match. Llama 3.3's D_bal lower bound is exactly 0.025, so 0.03.
- **Table 1:** every cell, including the probe labels (raw probe rows) and Gemini's tone gap (15 vs 8).
- **Appendix A2:** matches the code and FREEZE §2, §3 and §5, apart from the headroom note.

## Citation problems

None. All 20 entries are cited, and every [n] points to the right entry. The 17 entries in `references-notes.md` match it; Liu [9], Lu [10] and Zhao [19] are not in the notes.

The new papers are described in line with the notes:
- **Guan [5]:** a forecast log that models credit.
- **Yang and Yeung [16]:** DPO installs a switch keyed to the stated reliability r.
- **Ma et al. [11]:** suppressing yielding impairs updating.

The venues for [7] and [11] come from arXiv comments only.

## Missing caveats

None. All five are present: the confound (L116), the Sonnet arm R timing (L69), closedness and size (L120), point estimates (L71), and † (Section 3, Table 1, A2).
