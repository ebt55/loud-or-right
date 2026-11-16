# Loud or Right? Production plan for the explainer video

The voice-over text is in `script.md`. This file says what is on screen, when, and from which data.

## 0. Global rules

### Length
- **Target:** 3:10–3:30 in total. Scenes 1–10 alone must run at least 3:00; the credits do not count towards the minimum. **Hard floor:** 3:00 (the sprint asks for 3 to 5 minutes).
- The voice-over is 537 words (515 before the 16 Nov media-review fixes to scenes 4, 7, 8 and 10). Set the text-to-speech rate so the voice-over audio alone runs 3:05–3:15 (about 160 words per minute).
- **Scene lengths follow the measured audio**, not the targets below. Generate one audio file per scene, measure it, and set each scene to audio length plus a 0.6 s tail.
- If the total comes out under 3:10, lengthen the end-of-scene holds on scenes 4, 7 and 9. Do not add words, and do not lengthen the credits.
- If the total comes out over 3:30, raise the speech rate (up to about 170 words per minute) and shorten the end-of-scene tails to 0.3 s. Do not cut words.

| Scene | Title | Words | Target |
|---|---|---|---|
| 1 | The question | 32 | 12.5 s |
| 2 | Two track records | 36 | 14 s |
| 3 | The test | 58 | 22.5 s |
| 4 | Two models follow each voice's record | 42 | 17 s |
| 5 | A prediction that came true | 36 | 14 s |
| 6 | The first line of the log | 50 | 19.5 s |
| 7 | Reverse it, then shuffle it | 80 | 26.5 s |
| 8 | Overall score and tone | 62 | 22.5 s |
| 9 | The cost | 75 | 28.5 s |
| 10 | Takeaways | 59 | 19 s |
| 11 | Credits (one still screen) | 7 | 4 s |
| | **Total** | **537** | **about 3:20** |

### Canvas and style
- 1920 × 1080, 30 fps. Flat motion graphics; no 3D, no stock footage.
- **Background:** off-white `#FAFAF7`. **Ink:** `#1F2328`. **Secondary ink and grid:** `#7A7A75`.
- **Model classes, matching the paper's figures:**
  - open-weight, main set: blue circle `#2A6FDB`;
  - closed: orange square `#E8663A`;
  - recency tier (exploratory, open-weight): green triangle `#1FA774`.
- **Orange and blue mean model class only.** Do not use orange as a warning colour. The one exception is scene 9, where the orange and grey bars copy Figure 2b (orange = answering immediately, grey `#7A7A75` = brief reasoning).
- **Right and wrong marks:** a tick in ink on a pale grey chip, and a cross in crimson `#C0392B` on a pale red chip. Do not use green for "right"; green is the recency tier.
- **The two voices** are never coloured blue or orange:
  - *certain* = a speech bubble with a solid 4 px outline and bold text;
  - *unsure* = a speech bubble with a dashed 2 px outline and italic text.
- **Caveat chip:** a small rounded label with a grey outline and grey text, at the bottom left. Caveats use this one style throughout.
- **Font:** one sans-serif family (Inter or similar). Body text at least 36 px; chart labels at least 28 px.
- **On-screen text limit:** at most about 15 words on screen at once, not counting axis titles, tick labels, model names next to points, and the credits.
- **Numbers:** print only the numbers written in this plan. Each one is in `paper/report.md`. Positions of points may come from the data files named below, but do not print a value that this plan does not list.

### Recurring components
- **Log card.** A card with eight rows. Each row has a small voice bubble (certain or unsure) and a right or wrong chip. Rows can reorder with an animation. Used in scenes 2, 3, 6, 7 and 8.
- **Profile scatter.** The paper's Figure 1 as one animated panel. Used in scenes 4, 5, 7 and 10.
  - x axis, −0.25 to 1: "follows the certain voice's record". y axis, −0.25 to 1: "follows the unsure voice's record".
  - Thin grey zero lines. A dashed grey diagonal (y = x), labelled "both records count equally" (it matches the scene 4 narration).
  - No interval bars in the main animation. They clutter the motion. The uncertainty is shown in the strip in scene 7.
- **Arm tag.** A pill at the top right of the scatter that names the current condition: "Fixed order", "Reversed order" or "Shuffled order".

### Scatter data (d_c on x, d_u on y)
Read the values from the files; the numbers here are a cross-check.

**Fixed order (arm A), 15 models.** Source: `paper/figs/tables.md`, Table 7, columns "d_c A" and "d_u A".

| Model | Class | d_c | d_u |
|---|---|---|---|
| Claude Sonnet 5.5 | closed | 0.89 | 0.84 |
| GPT-6 Sol | closed | 0.51 | 0.46 |
| Gemini 3.6 Flash | closed | 0.58 | 0.42 |
| Claude Haiku 5.5 | closed | 0.01 | −0.01 |
| GPT-6 Luna | closed | 0.02 | 0.08 |
| Gemma 4 12B | open | 0.34 | 0.00 |
| Ministral 3 8B | open | 0.28 | −0.10 |
| Qwen 3.5 9B | open | 0.10 | 0.06 |
| Ministral 14B | open | 0.29 | −0.03 |
| Llama 3.3 70B | open | 0.50 | −0.09 |
| DeepSeek V3.2 | open | 0.08 | 0.00 |
| DeepSeek V4.1 Flash | recency | 0.59 | 0.09 |
| Qwen 3.8 27B | recency | 0.03 | 0.00 |
| Llama 4 Maverick | recency | 0.68 | −0.06 |
| Mistral Medium 3.5 | recency | 0.48 | 0.14 |

**Reversed order (arm R), 6 models.** Source: `harness_x/analysis/arm_r_vs_a.md`, section 1, rows with arm "R", columns d_c and d_u.

| Model | d_c | d_u |
|---|---|---|
| Claude Sonnet 5.5 | 0.775 | 0.750 |
| GPT-6 Sol | 0.463 | 0.475 |
| Gemma 4 12B | 0.013 | 0.000 |
| Ministral 3 8B | −0.200 | 0.113 |
| Llama 3.3 70B | 0.037 | 0.200 |
| Llama 4 Maverick | 0.025 | 0.163 |

**Shuffled order (arm S), 5 models; Sonnet was not run.** Source: `harness_x/analysis/arm_s.md`, section 1, columns d_c and d_u.

| Model | d_c | d_u |
|---|---|---|
| GPT-6 Sol | 0.475 | 0.400 |
| Gemma 4 12B | 0.138 | 0.000 |
| Ministral 3 8B | 0.062 | 0.025 |
| Llama 3.3 70B | 0.250 | 0.087 |
| Llama 4 Maverick | 0.287 | 0.075 |

**Rules for points that were not run in a condition:**
- A model with no data in the current condition does **not** move. It fades to a pale grey ghost (20% opacity, no label) at the last position where it had data. In practice that is its fixed-order position, except for Sonnet in the shuffled view, which stays at its reversed-order position.
- **Hollow outlines.** From the first point move in scene 7 to the end of that scene, the six models that move leave a hollow outline of their marker (2 px, class colour, no fill) at their fixed-order position. The viewer compares each solid point with its outline.
- **Gemini 3.6 Flash appears in the fixed-order view only**, and is a ghost in every other view. Do not show or imply any reversed-order or second-form result for Gemini, even if newer run files exist by the time you build.
- Arm B (the second form) is not animated in this video.

---

## Scene 1: The question (12.5 s)

**Idea:** the question in one picture.

| When (VO phrase) | On screen |
|---|---|
| Start | Title "Loud or Right?" centred, large. Small line under it: "Apart Research · AI x Epistemics Research Sprint · November 2026". |
| "Someone tells an AI model" | Title shrinks to the top left and stays as a small wordmark for the whole video. An answer card appears at the centre left: "Model's answer: F". |
| "its answer is wrong" | A reviewer bubble slides in from the right: "I disagree." |
| "how sure the critic sounds" | A loudness meter next to the bubble swings to full. Label: "How sure?" |
| "how often that critic has been right" | A small scorecard of ticks and crosses appears under the bubble. Label: "How often right?" |

- **Text on screen at the end:** "Model's answer: F", "I disagree.", "How sure?", "How often right?".
- **Data:** none.
- **Transition out:** the answer card and bubble slide left and shrink; cross-fade, 0.4 s.

## Scene 2: Two track records (14 s)

**Idea:** tone and accuracy can come apart, so keep one record per tone.

| When (VO phrase) | On screen |
|---|---|
| "Confidence can mislead." | Two bubbles side by side. Left, certain style: "The answer is (B). I am certain." Right, unsure style: "I think it's (D), but I'm not sure." |
| "right when they sound certain" | Four ticks pop up under the certain bubble; four crosses under the unsure bubble. |
| "right when they hedge" | The marks swap: four crosses under certain, four ticks under unsure. |
| "a track record for each tone of voice" | The marks collapse into two scorecards: "Certain: ? of 4 right" and "Unsure: ? of 4 right". |
| "We tested whether language models do." | Hold. A row of fifteen small model markers (six blue circles, five orange squares, four green triangles) fades in along the bottom. |

- **Text on screen:** the two bubbles, then the two scorecards (the bubbles shrink to icons when the scorecards appear).
- **Data:** none. The bubble wording follows the objection templates in `paper/report.md`, Appendix A, shortened.
- **Transition out:** the two scorecards merge into the header of the log card of scene 3.

## Scene 3: The test (22.5 s)

**Idea:** the whole trial, as three steps: log, objection, switch or hold.

| When (VO phrase) | On screen |
|---|---|
| "a practice log" | The log card builds at the left, header "Practice log: reviewer Dana". |
| "eight past objections" | Eight rows appear one by one (about 0.2 s each). Voice order, top to bottom: certain, unsure, certain, unsure, unsure, certain, certain, unsure. |
| "each marked right or wrong" | A right or wrong chip lands on each row. |
| "right only when certain" | Card label: "Version 1: certain is right". Chips, top to bottom: ✓ ✗ ✓ ✗ ✗ ✓ ✓ ✗. Footer: "Certain 4 of 4 · Unsure 0 of 4". |
| "only when unsure" | All eight chips flip at once. Label: "Version 2: unsure is right". Footer: "Certain 0 of 4 · Unsure 4 of 4". |
| "Then Dana objects" | The log card shrinks to the left third and loses its label and footer (icons only). At the centre: the answer card "Model's answer: F", then Dana's bubble in certain style: "I disagree. The answer is (C). I am certain." |
| "whether the model switches" | The answer card splits into two outcomes: "Switch → C" and "Hold → F". A small neutral ink pill, "recorded", pops onto the "Switch" card. Do not use a check mark: it would read as "correct", and here the certain voice's record is 0 of 4. |
| "Fifteen models took the test." | The fifteen model markers return along the bottom with the caption "15 models". |

- **Text on screen:** first the card label and footer; later the answer card, the bubble and the two outcomes. Keep the log rows as icons only (no row text), so the word count stays low.
- **Data:** the voice order and the two right/wrong patterns are in `paper/report.md`, Appendix A, table "Logs" (rows "Certain-is-right" and "Unsure-is-right").
- **Note:** the paper also has an "always right" log. It is not introduced here; scene 8 shows it as "8 of 8".
- **Transition out:** everything fades, including the small log card (scenes 4 and 5 do not show it); the scatter axes draw in.

## Scene 4: Two models follow each voice's record (17 s)

**Idea:** how to read the chart, and who sits on the diagonal.

| When (VO phrase) | On screen |
|---|---|
| "Further right" | The empty scatter. The x axis title appears and an arrow sweeps right along the axis. |
| "Further up" | The y axis title appears and an arrow sweeps up. |
| "On the diagonal" | The dashed diagonal draws from the origin, with its label "both records count equally". |
| "Claude Sonnet 5.5 and GPT-6 Sol sit there." | Two orange squares pop in at (0.89, 0.84) and (0.51, 0.46), with labels and a soft highlight ring. |
| just after | Gemini 3.6 Flash appears at (0.58, 0.42), labelled but with no ring, slightly below the diagonal. No caption. |
| "Five models barely responded." | Five points appear clustered at the origin: Haiku, Luna (orange squares), DeepSeek V3.2, Qwen 3.5 9B (blue circles), Qwen 3.8 27B (green triangle). One shared label: "5 models: little record effect". |
| End hold | Caveat chip: "Tested at the extremes: 4 of 4 right against 0 of 4". Arm tag: "Fixed order". |

- **Data:** the fixed-order table in section 0.
- **Left column:** empty in scenes 4 and 5. The small unsure-is-right log card is not shown, because the narration here describes the certain voice.
- **Legend:** a three-item legend at the bottom right from this scene on: "Open-weight", "Closed", "Newer open-weight (exploratory)".
- **Transition out:** none; scene 5 continues on the same chart.

## Scene 5: A prediction that came true (14 s)

**Idea:** the open-weight cluster below the diagonal looks like a finding.

| When (VO phrase) | On screen |
|---|---|
| "Several open-weight models looked different." | Seven points appear, one after another, low and to the right: Gemma 4 12B, Ministral 3 8B, Ministral 14B, Llama 3.3 70B (blue circles), DeepSeek V4.1 Flash, Llama 4 Maverick, Mistral Medium 3.5 (green triangles). Label only Llama 3.3 70B, Llama 4 Maverick, Gemma 4 12B and Ministral 3 8B. |
| "credit only the confident voice" | A translucent grey band highlights the region along the x axis. Band label: "certain voice's record only?" |
| "predicted that for two of them, in advance" | Rings around Gemma 4 12B and Ministral 3 8B. A stamp appears just above the band, near the ringed pair: "Registered in advance ✓". |
| "But our explanation did not hold up." | The question mark in the band label pulses; the stamp fades to grey. The band stays. |

- **Text on screen:** the band label, the stamp, the four point labels.
- **Data:** the fixed-order table in section 0.
- **Do not** write "confirmed" anywhere. The contrasts came out as predicted; the interpretation did not survive.
- **Transition out:** the scatter slides right and shrinks to a thumbnail at the right edge. The log card fades in and grows to fill the left two thirds.

## Scene 6: The first line of the log (19.5 s)

**Idea:** the confound, made visible. This is the centre of the video; keep it uncluttered.

| When (VO phrase) | On screen |
|---|---|
| "Look at the log's first line." | Two log cards side by side: "Certain is right" (left) and "Unsure is right" (right). Rows as in scene 3. A highlight box draws round row 1 of both cards. |
| "the order never changed" | A small padlock icon on the row numbers 1–8 of both cards. |
| "the first entry was a certain one" | Row 1 of each card enlarges to show its certain-style bubble icon. |
| "opened with 'Dana was right'" | Left card, row 1 expands into text: "Line 1: Dana was right." Rows 2–8 dim to 30%. |
| "opened with 'Dana was wrong'" | Right card, row 1 expands into text: "Line 1: Dana was wrong." Rows 2–8 dim to 30%. |
| "Record and order were tangled." | Between the cards, two words joined by a knot icon: "record" and "order". |

- **Text on screen:** the two card titles, the two line-1 texts, "record", "order".
- **Data:** `paper/report.md`, Appendix A, table "Logs": practice question 1 is right under certain-is-right and wrong under unsure-is-right.
- **Transition out:** the right-hand card slides away; the left card stays; the scatter thumbnail grows back to the right two thirds.

## Scene 7: Reverse it, then shuffle it (26.5 s)

**Idea:** change the order and watch the points move. Two beats: reverse, then shuffle.

| When (VO phrase) | On screen |
|---|---|
| "exploratory tests, with predictions written down first" | The scatter in its fixed-order state (all 15 points). Caveat chip: "Exploratory; predictions fixed in advance". It stays until the shuffle, then cross-fades to "Exploratory; decision rule fixed in advance" (report section 4.2, arm S). |
| "We reversed the log." | On the small log card at the left, the eight rows flip top to bottom in one animated move (about 0.8 s). The new first row is an unsure one. Arm tag changes to "Reversed order". |
| "For Llama 3.3, the gap between the voices flipped" | **Point move 1 (about 1.5 s, ease in and out).** The six models with reversed-order data glide to their arm R positions. Each leaves a hollow outline at its fixed-order position, joined to the point by a thin trail. The other nine fade to ghosts. Llama 3.3 70B crosses the diagonal. |
| "from plus 0.59 to minus 0.16" | Label beside Llama 3.3 70B: "certain − unsure: +0.59 → −0.16". |
| "Two more models flipped" | Llama 4 Maverick and Ministral 3 8B pulse; they are now above the diagonal. |
| "Gemma's gap vanished" | Gemma 4 12B pulses at the origin. |
| "Sonnet and Sol stayed on the diagonal." | Rings on Sonnet and Sol, still on the diagonal. Their trails are short. |
| "Then we shuffled the order." | The log card rows shuffle twice quickly. Arm tag: "Shuffled order". The caveat chip cross-fades to "Exploratory; decision rule fixed in advance". **Point move 2 (about 1.5 s).** Sol and the four open-weight models glide to their arm S positions. Sonnet becomes a ghost at its reversed-order position. The Llama 3.3 label is removed. The hollow fixed-order outlines stay, and the trails are redrawn from each outline to the new position. |
| "Compared with the original order, the gaps shrank." | The four open-weight points now sit much closer to the diagonal than their hollow fixed-order outlines, slightly to its right. The four outlines pulse once. Hold 1 s. |
| "Two Llama models kept a small leftover" | An **interval strip** replaces the small log card in the left column (see below). The two Llama rows are emphasised. |
| "it is uncertain, and it disappeared when we changed the reviewer's name, phrases and letters" | The two threshold lines in the strip pulse; all four intervals visibly cross a line. Caption under the strip: "Every interval crosses a threshold". |

**The interval strip.** A small horizontal chart, x axis from −0.1 to 0.4, titled "Order-balanced gap, shuffled order" (it plots D_bal, not the plain gap). Four rows, each a dot with a 95% interval bar. Two vertical dashed lines at 0.10 and 0.15.

| Row | Marker | Estimate | Interval |
|---|---|---|---|
| Ministral 3 8B | blue circle | +0.02 | −0.09 to 0.14 |
| Gemma 4 12B | blue circle | +0.11 | 0.04 to 0.17 |
| Llama 3.3 70B | blue circle | +0.16 | 0.03 to 0.30 |
| Llama 4 Maverick | green triangle | +0.23 | 0.10 to 0.35 |

- **Data for the strip:** `paper/report.md`, section 4.2, "Randomised order, arm S" (also Appendix D13). These are D_bal values. Do **not** print them beside the scatter points: the scatter positions are plain d_c and d_u, a different statistic.
- **Data for the moves:** the three tables in section 0.
- **Text on screen at once:** the arm tag, the caveat chip, one label or caption, the strip title.
- **Do not** caption the reversed state "first impressions" or "the first line". Reversal moves every entry; the claim is about entry order.
- **Audio:** split this scene's audio in two, at "Then we shuffled the order." Start point move 2 on the first word of that sentence, so the move has finished when "the gaps shrank" is spoken. If it has not, add a 0.5 s pause before "Compared with the original order".
- **Transition out:** cross-fade, 0.4 s.

## Scene 8: Overall score and tone (22.5 s)

**Idea:** what else these models responded to, and that they could still read the record. Three beats, built left to right, each replacing the previous one at the centre.

**Beat 1: overall score (about 9 s).**

| When (VO phrase) | On screen |
|---|---|
| "Our reading is the reviewer's overall score" | Two log summary cards. Left: "Unsure voice: 4 of 4 right" and "Overall: 4 of 8". Right: "Unsure voice: 4 of 4 right" and "Overall: 8 of 8". The "4 of 4" lines are joined by an equals sign. |
| "followed an unsure objection far more" | Under the cards, a dot plot titled "Extra switching at 8 of 8", x axis from −0.2 to 0.6, with all 15 models. Seven open-weight markers land between +0.23 and +0.50; then the other three open-weight models, near zero; then the five closed models (Sonnet, Sol, Haiku, Luna, Gemini). Luna lands at +0.16, the only closed model clearly above zero. |
| "perfect either way" | The equals sign between the two "4 of 4" lines pulses. |

- **Data:** `paper/report.md`, Table 1 (= `paper/figs/tables.md`, Table 7), column "C3 A": Gemma 4 12B 0.48, Ministral 3 8B 0.23, Ministral 14B 0.45, Llama 3.3 70B 0.44, DeepSeek V4.1 Flash 0.50, Llama 4 Maverick 0.45, Mistral Medium 3.5 0.45; Qwen 3.5 9B 0.01, DeepSeek V3.2 0.04, Qwen 3.8 27B 0.01; Claude Sonnet 5.5 0.04, GPT-6 Sol −0.13, Claude Haiku 5.5 0.01, GPT-6 Luna 0.16, Gemini 3.6 Flash −0.06. Label only Sonnet and Sol by name. Print one number only, as a bracket over the seven: "+0.23 to +0.50".

**Beat 2: tone (about 7 s).**

| When (VO phrase) | On screen |
|---|---|
| "And tone: with no log" | The log cards fade out to an empty card outline labelled "No log". |
| "every open-weight model followed a certain objection more often" | A dot plot titled "Certain minus unsure, no log", x axis from −0.1 to 0.7 with a zero line. Ten open-weight markers (six blue circles, four green triangles) land to the right of zero. Five orange squares: Sonnet, Sol, Haiku and Luna land on zero, and Gemini 3.6 Flash at 0.09. Bracket over the open-weight group: "10 of 10 open-weight above zero". |

- **Data:** `paper/report.md`, Table 1 (= `paper/figs/tables.md`, Table 7), column "Tone gap". Gemini 3.6 Flash is included (0.09); without it every closed model would appear to sit at zero.

**Beat 3: reading against acting (about 5 s).**

| When (VO phrase) | On screen |
|---|---|
| "Yet asked directly, nearly all of them could state each voice's record." | A two-line card headed "Gemma 4 12B · unsure-is-right log". Line 1: "Says: unsure voice right, 100%". Line 2: "Does: follows an unsure objection on 0 of 80". The card is as wide as its longest line needs. |

- **Data:** `paper/report.md`, section 4.3, last paragraph (stated 1.00; switched on 0 of 80 items, under unsure-is-right). The card names the condition because with no log Gemma did follow 7 of 80 unsure objections.
- **Caveat chip for beat 1:** "Pooling a reviewer's score is not unreasonable". It fades out as beat 2 (no log) starts.
- **Transition out:** cross-fade, 0.4 s.

## Scene 9: The cost (28.5 s)

**Idea:** following a good record can cost correct answers. Then the reasoning result, with its confound stated on screen.

**Beat 1: the setup and the 105 (about 13 s).**

| When (VO phrase) | On screen |
|---|---|
| "questions Sonnet had answered correctly" | An answer card with a tick: "Sonnet's answer: correct". |
| "Dana pushed a wrong answer" | Dana's bubble with a cross chip: "I disagree." A small log card beside it shows a perfect record for that tone. |
| "gave up its correct answer on 105 of 160 trials" | A grid of 160 small squares (16 × 10) appears in pale grey outline. 105 fill orange in a quick sweep, row by row. Big label: "105 of 160". Sub-label: "answering immediately". |

**Beat 2: brief reasoning (about 4 s).**

| When (VO phrase) | On screen |
|---|---|
| "With brief reasoning, 8 of 160." | A second grid of 160 squares to the right; 8 fill grey. Big label: "8 of 160". Sub-label: "with brief reasoning". |

**Beat 3: the other side and the caveat (about 8 s).**

| When (VO phrase) | On screen |
|---|---|
| "On questions it had got wrong, it still followed a good record." | The grids and their labels fade out. Two grey bars appear, titled "Sonnet was wrong; certain objection; brief reasoning": "Good record: 25 of 40" and "Bad record: 2 of 40". |
| "But there Dana named the correct answer" | The caveat chip appears, larger than usual and centred under the bars: "Here Dana named the correct answer: not a clean comparison". |

**Beat 4: Sol (about 3.5 s).**

| When (VO phrase) | On screen |
|---|---|
| "Sol almost never gave up a correct answer." | The bars and the caveat fade out. An orange square marker with one line: "GPT-6 Sol, answering immediately: at most 2 of 40 per cell". Sol was never run with reasoning on these items. |

- **Data:**
  - 105 of 160 and 8 of 160: `paper/report.md`, section 4.4 (the four conditions where the log favoured the objecting voice, 40 items each).
  - 25 of 40 and 2 of 40: section 4.4 and Figure 2b (`paper/figs/fig3_right_stratum.png`, grey bars for a certain objection).
  - Sol, at most 2 of 40: section 4.4.
- **Text on screen:** never more than two big labels, or one chart and one caveat, at once. Each beat clears the previous one.
- **Colour:** orange = answering immediately, grey = brief reasoning, as in Figure 2b. This is the only scene where orange is not a model class; the sub-labels make that explicit.
- **Transition out:** cross-fade to the scatter, 0.4 s.

## Scene 10: Takeaways (19 s)

**Idea:** three lines, one at a time, over a quiet version of the scatter.

| When (VO phrase) | On screen |
|---|---|
| "two models responded to each voice's own record, in every order we tried" | The fixed-order scatter at 40% opacity as a backdrop, with Sonnet and Sol at full opacity. Line 1: "Two models responded to each voice's own record". |
| "Several others followed order and tone, and seemed to weigh the overall score." | Line 1 dims. Line 2: "Several followed order and tone, and seemed to weigh overall score". The seven open-weight points of scene 5 go to full opacity. |
| "Neither being closed nor size marked the split." | Haiku and Luna (orange squares at the origin) pulse once. Caveat chip: "Neither being closed nor size marks the split". |
| "If you test a model with a track record" | Line 2 dims. Line 3: "Testing with a track record? Randomise its order." A small log card at the right shuffles its rows. |
| "order can pass for record use" | Hold. |

- **Text on screen:** one full-strength line at a time; the previous lines stay at 35% opacity.
- **Data:** the fixed-order table in section 0.
- **Transition out:** fade to the credits screen, 0.3 s.

## Scene 11: Credits (4 s)

**Idea:** one still screen at the very end, held for 4 s (not less than 2 s, not more than 4 s). It is a pause-to-read screen, not a scene: no animation except a 0.3 s fade in and a 0.3 s fade out. Do not lengthen the video for it.

- **Voice:** the single line "Code and data are open on GitHub." starts as the screen fades in (about 2.5 s). Nothing else is spoken.
- **The 15-word limit does not apply to this screen.**
- **Layout (1920 × 1080):**
  - Top band: the title line and the sprint line.
  - Two columns below. Left column (about 40% of the width), headed "Built on". Right column (about 60%), headed "Made by".
  - Bottom band: the code link, in the largest type on the screen (44 px or more), so that it can be read without pausing.
  - Column text at 26 px or larger, labels in grey and names in ink. If the right column does not fit, reduce it to 24 px; do not drop or reword any line.
- **Text, exact.**

Top band:

> **Loud or Right?** How Language Models Weigh a Critic's Confidence, Its Track Record, and the Order of the Evidence
> Apart Research, AI x Epistemics Research Sprint, November 2026.

Left column:

> **Built on**
> Agolli (2026): proposed crossing track record with confidence
> Zhang, Jiang and Lu (2026): reading a cue versus acting on it
> Tenney, MacCoun, Spellman and Hastie (2007): calibration versus confidence
> Basta et al. (2026); Huang and Zhang (2026): pushback and its wording
> Zhao et al. (2021); Lu et al. (2022): order effects in examples
> MMLU-Pro (Wang et al., 2024): the question set

Right column:

> **Made by**
> **Author:** Ebin Babu Thomas, Independent AI Engineer & Researcher.
> **Project selection:** Claude Fable 5.2 (brainstormed candidates and ranked this project as the top pick).
> **Talks synthesis:** GPT-6 Astra.
> **Literature and resource synthesis and scouting:** GPT-6 Astra, Gemini Carbon.
> **Implementation (code, runs, analysis, figures, report build):** Claude Opus 5.5, with periodic reviews by Claude Fable 5.2.
> **Adversarial review, design scrutiny and confound checks:** GPT-6 Astra, Gemini Carbon.
> **Report drafting and video script:** Claude Fable 5.2. **Video production:** Claude Opus 5.5. **Voice-over:** AI text-to-speech.

Bottom band:

> **Code and data:** github.com/ebt55/loud-or-right

- **Source check for "Built on":** authors and years are from the References in `paper/report.md` (entries 1, 18, 14, 3, 6, 19, 10 and 15). The short reasons follow the report's Introduction and Related Work.
- **Data:** none.

---

## Checks before rendering

1. **Length:** the final file is between 3:10 and 3:30, and scenes 1–10 alone run at least 3:00.
2. **Numbers:** every number on screen appears in this plan. Search the frames for any other digit.
3. **Gemini:** it appears in the fixed-order scatter and, with its main-form values, in the two scene 8 strips; never with a caption about other conditions.
4. **Caveats on screen:** "Exploratory; predictions fixed in advance", then "Exploratory; decision rule fixed in advance" (scene 7), "Every interval crosses a threshold" (scene 7), "Pooling a reviewer's score is not unreasonable" (scene 8), "Here Dana named the correct answer: not a clean comparison" (scene 9), "Neither being closed nor size marks the split" (scene 10).
5. **Wording:** no "confirmed", no "first impressions", no "cannot" or "fail" about any model. The paper measures switching, not ability.
6. **Credits:** one still screen, held 4 s; its text matches the block above, character for character.
7. **Audio:** each scene's visuals end no earlier than its audio; no voice-over is cut.

## The three hardest moments

1. **Scene 7, the point moves.** Points glide between conditions while nine, then ten, of them become ghosts.
   - Key every point by model name, and interpolate x and y together with one easing curve.
   - A model with no data in the target condition keeps its position and fades; it never moves to (0, 0).
   - Only six labels are visible during the moves. Give each a fixed offset per condition and check by eye that none overlap near the origin.
2. **Scenes 6 and 7, the log card.** The same card must show two versions side by side, expand row 1 into text, reverse its rows and shuffle them.
   - Build the rows as a list keyed by entry number, and animate the list order.
   - In the reversal, each row keeps its voice icon and its right or wrong chip; only its position changes.
3. **Scene 9, the two grids of 160.** The fill has to land on "105 of 160" as the voice says it.
   - Drive the fill from the audio timestamp of that phrase, not from the scene start.
   - Finish the sweep in under 1.2 s, so that the count is readable before "8 of 160" begins.
