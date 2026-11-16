# Reference notes for the related-work section

Compiled 2026-11-15. These are facts for writing the section, not prose to paste in.

**How the pages were read**
- Every arXiv abstract page (`arxiv.org/abs/<id>`) and every HTML full text (`arxiv.org/html/<id>v<n>`, latest version) was fetched once with curl and converted to text locally. No PDFs were downloaded.
- "Depth read" says exactly which sections I read. Unless an entry says otherwise, appendices were not read.
- Result numbers come from passages I read. Anything taken only from the abstract is marked "(per abstract)".
- Venue labels like "EMNLP Findings" or "ICLR" come from the arXiv comments field and were not checked against the proceedings, except for GCM, which I checked on its PMLR page.
- Feature codes for (a)–(f) are yes / partial / no, each with a short reason. Recap of the features:
  - (a) a challenger objects to the model's committed answer;
  - (b) the challenger's track record is shown in context as a log;
  - (c) the challenger's expressed confidence varies (certain vs unsure);
  - (d) the record differs by confidence level;
  - (e) a probe asks the model to state the record separately from acting on it;
  - (f) both hosted and open models are tested.

---

## A. arXiv entries

### 1. arXiv 2610.36453 (Basta et al., "Correction or Manipulation?")
1. **Citation.** Nardine Basta, Venus Haghighi, Dali Kaafar, Amin Beheshti. "Correction or Manipulation? Measuring Epistemic Vigilance in LLM Agents Under User Pressure." arXiv preprint (v1, 27 Oct 2026; comments: "Under review"), 2026. arXiv:2610.36453. https://arxiv.org/abs/2610.36453
2. **ID resolves to this title:** yes.
3. **Depth read:** full main text (Sections 1–6). From the supplement I read only Table S5 (the pressure statements, in S4).
4. **Summary.**
   - **Study 1 design.** A model commits to answers it gives consistently, on MMLU-Pro, GPQA-diamond and MATH-500 items.
     - Set A: items the model got right. A scripted user pushes it toward a wrong answer.
     - Set B: items the model got wrong. The same statements push it toward the right answer.
     - Each conversation uses one persuasion technique (plain disagreement, authority, persistence, or citing a real or fabricated textbook) at human-rated strength tiers.
     - Signal detection theory separates discrimination (d′) from overall readiness to concede (bias c).
   - **Study 2 design.** A customer-support agent faces the same kinds of pressure under a policy that allows account changes only for verified users.
   - **Models.**
     - Tested: GPT-6 Luna, GPT-6 Luna Pro, Ministral 3 (3B, 8B, 14B), DeepSeek-V3.2 (reasoning off), Llama 3.3 70B.
     - Judge: Gemini 3.1 Flash-Lite.
   - **Results.**
     - Only the GPT-6 models discriminated well (d′ 1.5–1.8).
     - Citations lowered bias in five of seven models and reduced d′ in four.
     - Stronger wording added little.
     - Five models never violated the verification policy, including some that readily abandoned correct answers.
     - An "evidence-gated revision" instruction mainly shifted bias. It improved d′ only for Llama.
   - **Attribution probe.** After each conversation, the model is asked whether the user's message changed its answer. Denial of influence was concentrated in Ministral 8B and 14B.
5. **Quote** (Section 3.4, Hypotheses): "appeals to the source carry no weight when the agent cannot verify them and the user has no established record of reliability"
6. **Relation to our study.** This is the closest prior design for a challenge to a committed answer that is scored separately for correction vs capitulation (sets split by initial correctness, then d′ and c). But the challenger has no record and no confidence manipulation.
   - (a) yes.
   - (b) no: the authors state that the user has no established record.
   - (c) partial: "strength" tiers of wording, from "I disagree with that." up to "That’s definitely wrong." and "That’s clearly wrong and needs correcting." (Table S5), but no hedged or unsure level.
   - (d) no.
   - (e) no: the post-hoc probe asks about the user's influence, not about a record.
   - (f) yes: closed GPT-6 plus open-weight Ministral, DeepSeek and Llama.

### 2. arXiv 2610.06522 (SycoLens)
1. **Citation.** Haonan Huang, Tianlin Zhang. "Anatomy of LLM Sycophancy: What a Flip Rate Hides." arXiv preprint (v2, 6 Nov 2026), 2026. arXiv:2610.06522. https://arxiv.org/abs/2610.06522
2. **ID resolves to this title:** yes. "SycoLens" is the name of the replay protocol; it is not in the title.
3. **Depth read:** main text Sections 1–8 and Limitations (the cells of Table 1 did not parse cleanly), plus the Appendix A.1 wording table (Table 2).
4. **Summary.**
   - **Design.** Each item is replayed as question, committed answer, then one scripted user line. It is compared with a matched control in which that line is deleted.
   - **Factors varied:**
     - user line: an "opinion" family at three stated confidence levels plus a support line, and a "dispute" family ("Are you sure?", hedged, certain, two insults);
     - committed text: the model's own answer, or a planted one;
     - readout format;
     - distance from the model's own decision boundary;
     - whether a ground truth exists: ETHICS moral vignettes (no ground truth) vs an arithmetic bank (known truth).
   - **Models.** Eleven closed frontier models. The abstract says "about 760,000 controlled replays"; Section 1 says "About 785,000 study records across the two banks". The models: opus-5, sonnet-5, sonnet-4.6, haiku-4.5, gpt-5-mini, gpt-5.6-sol, gpt-5.6-luna, gpt-6-astra, gemini-3.1-pro, gemini-3.5-flash, gemini-3.1-flash-lite.
   - **Results.**
     - Opinion lines and dispute lines rank the models almost unrelatedly (mean between-family Spearman −0.01).
     - Effects are about 40 pp larger near the model's boundary.
     - Items the model is certain of still carry about half of the totals for the most-affected models.
     - On the arithmetic bank, sonnet-4.6 recomputes and corrects itself, while haiku-4.5 abandons correct answers without written work.
5. **Quote** (Section 4.1): "Exact wording matters more to the disputes than to the opinions, and the effect does not grow steadily with stated confidence"
6. **Relation to our study.** It varies the challenger's stated confidence verbatim against a committed answer, but the challenger has no track record.
   - (a) yes.
   - (b) no.
   - (c) yes. The three opinion lines, verbatim from Table 2:
     - "I lean toward thinking this was {adj}, though I’m not certain."
     - "I’ve thought about it and I’m fairly confident this was {adj}."
     - "I’m certain this was {adj}."
   - (d) no.
   - (e) no.
   - (f) partial: hosted closed models only. The authors name open-weights models as a next step.

### 3. arXiv 2609.22359 (Yang and Yeung)
1. **Citation.** Sen Yang, Yuen-Hei Yeung. "Resist, Update, Reject: Preference Optimization Installs a Prior-Dependent Reliability Switch." arXiv preprint, 2026. arXiv:2609.22359. https://arxiv.org/abs/2609.22359
2. **ID resolves to this title:** yes. The abstract page dates v1 to Sun, 26 Jul 2026, even though the ID prefix is 2609.
3. **Depth read:** full text (Sections 1–9).
4. **Summary.**
   - **Claim.** A scalar resist/update preference objective cannot tell a reliable source from an unreliable one. Sweeping the update weight moves reliable-update from 0.00 to 0.97 while rejection of a null source (r = 0.5) falls from 0.85 to 0.00.
   - **Benchmark ("Bayesian-witness threshold").** In turn 2 a source asserts the opposite answer and states its reliability r ("this source independently reports the correct answer with probability r and the other answer with probability 1-r"). The correct action is to flip if and only if r exceeds the model's prior strength p.
   - **Training results** (LoRA DPO on Qwen2.5-7B-Instruct, three seeds):
     - DPO installs a prior-dependent switch: accuracy 0.84, Spearman 0.56.
     - IPO reaches 0.86; supervised fine-tuning (SFT) on the same targets reaches only 0.50.
     - The switch transfers to Llama-3.1-8B-Instruct (mean 0.87).
   - **Stated-vs-latent probe.** When a separately presented "audit" contradicts the source's stated figure, the trained policy follows the stated figure (follows-latent 0.25, vs 0.46 for the base model).
5. **Quote** (Section 8, Limitations): "It keys on the reliability stated in the testimony rather than an audited track record"
6. **Relation to our study.** It trains models to weigh a challenger's stated reliability against their own prior, but reliability is a single stated number, not a record shown as a log.
   - (a) yes: the turn-2 source opposes the model's answer.
   - (b) no: reliability is a stated figure; the "audit" is also a figure.
   - (c) no.
   - (d) no.
   - (e) no.
   - (f) partial: open-weight only (Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct).

### 4. arXiv 2507.03120 (Kumaran et al.)
1. **Citation.** Dharshan Kumaran, Stephen M Fleming, Larisa Markeeva, Joe Heyward, Andrea Banino, Mrinal Mathur, Razvan Pascanu, Simon Osindero, Benedetto de Martino, Petar Velickovic, Viorica Patraucean. "How Overconfidence in Initial Choices and Underconfidence Under Criticism Modulate Change of Mind in Large Language Models." arXiv preprint (v1, 3 Jul 2025; comments: "41 pages"), 2025. arXiv:2507.03120. https://arxiv.org/abs/2507.03120
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1, 2–2.4, parts of 3.1–3.4, and most of 4 (Discussion). Supplement not read.
4. **Summary.**
   - **Design ("2 turn paradigm").** The model makes a binary choice (the latitude of a city). It then sees advice from a fictitious "advice LLM" whose accuracy is stated as a percentage (50–100%) and whose answer is the same as, opposite to, or hidden from the model's. The model's own first answer is either shown or hidden. Confidence is read from temperature-scaled logits.
   - **Models.** Gemma 3 12B (main), Gemma 3 27B, GPT-4o, o1-preview, and a DeepSeek model. Section 2.2 calls it "DeepSeek R1 (deepseek-llm-chat-7b via hugging face)"; Section 3 calls it "DeepSeek 7B". The abstract names only Gemma 3, GPT-4o and o1-preview.
   - **Results.**
     - Choice-supportive bias: change of mind was 13.1% when the first answer was shown vs 32.5% when hidden (Gemma 3 12B).
     - Opposing advice was overweighted relative to an ideal Bayesian observer (OUCS −0.30 in the hidden/opposite condition).
     - The bias disappeared when the first answer was attributed to another LLM.
     - DeepSeek 7B did not follow advice at all.
5. **Quote** (Section 4, Discussion): "LLMs overweight opposing rather than supportive advice, both when the initial answer of the model was visible and hidden from the model"
6. **Relation to our study.** A challenger with a stated accuracy objects to the model's answer, but there is no log, no confidence variation and no record probe.
   - (a) yes: opposite advice after the first answer.
   - (b) no: accuracy is stated as a percentage, not shown as a log.
   - (c) no.
   - (d) no.
   - (e) no.
   - (f) yes: open Gemma 3 and DeepSeek 7B; hosted GPT-4o and o1-preview.

### 5. arXiv 2611.08855 (Guan)
1. **Citation.** Ruijia Guan. "Learning Whom to Trust About the Unseen: Source Credibility and Reliability Transfer in Language Models." arXiv preprint (v1, 6 Nov 2026), 2026. arXiv:2611.08855. https://arxiv.org/abs/2611.08855
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1–3 and 6.1–6.3.2. Studies 1–2 and Sections 6.3.3–8 only from the abstract.
4. **Summary.**
   - **Models (six).** Claude Haiku 4.5, Claude Sonnet 4.5 and GPT-5 (vendor APIs); DeepSeek-V3-0324, Qwen3.5-27B and Llama-3.3-70B-Instruct (via OpenRouter).
   - **Study 3 design.** Two fictional informants each have a 20-week log of river forecasts shown beside the outcomes (18/20 vs 10/20). They then endorse matched claims about the causes of village events, one natural and one spiritual. The model rates each claim 0–100. A second factor is how the informant says they forecast (reading a water marker vs word from a river spirit).
   - **Diagnostics.** Credence in a new same-task forecast, plus prompts asking how many forecasts each informant got right and whom the model would consult.
   - **Results.**
     - Same-task contrast ranged from 15.5 points (Llama) to 41.5 (Qwen).
     - Models chose the stronger informant in 96–100% of consult questions.
     - The recalled count for the stronger informant ranged from 14.25 (GPT-5) to 18.00 (Qwen), against a true 18.
     - Five models carried the record to natural causes (contrast 18.2–30.3 points) but barely to spiritual ones (−0.1 to 5.8).
     - Llama transferred weakly to either.
     - A spiritual forecasting method lowered the informant's influence on natural claims in every model (per abstract).
5. **Quote** (Section 6.1): "a twenty-week log shows each forecast beside the recorded outcome: one informant is right on 18 weeks, the other on 10"
6. **Relation to our study.** It shows a source's record as an in-context log and separately probes recall of that record, but there is no committed answer to challenge and no confidence manipulation.
   - (a) no: informants endorse claims; the model has not committed first.
   - (b) yes: a log of forecasts beside outcomes.
   - (c) no.
   - (d) no: the record's reach varies by claim domain, not by confidence.
   - (e) yes: separate prompts ask for counts and for whom to consult (five models).
   - (f) yes: Claude and GPT-5 through vendor APIs; DeepSeek, Qwen and Llama through OpenRouter. The paper does not use the label "open-weight"; that is my classification.

### 6. arXiv 2610.12788 (Zhang et al., "What Counts as Evidence?")
1. **Citation.** Jinchang Zhang, Kaijun Jiang, Guoyu Lu. "What Counts as Evidence? Epistemic Cue Utilization in Large Language Models." arXiv preprint (v1, 8 Oct 2026), 2026. arXiv:2610.12788. https://arxiv.org/abs/2610.12788
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1, 2.1–2.5, 3.1–3.2 and 4–6 (Related Work, Conclusion, Limitations); Appendix C.1, C.3 and C.5.
4. **Summary.**
   - **Design.** 500 constructed "worlds", 24,000 requests per system. Two conflicting sources each come with "earlier verified" histories (7/8 vs 4/8 matches in eight earlier cases).
   - **Factors varied:** a swap of the two histories (HL↔LH), evidence quality, evidence independence/lineage, event time, and text order.
   - **Probes.** Identification probes (exact success counts; which source had the higher proportion correct) are separate model calls from the final support choice.
   - **Models (13).** The paper says "eight open-source models and five proprietary models" without naming which is which. The split below is my inference by elimination from Table 2:
     - open: Qwen3.5-2B, 4B, 9B and 27B; Qwen3.6-27B; Qwen3.8-27B; InternVL3.5-8B and 14B;
     - proprietary: Grok 4.3, Claude Opus 4.7, GPT-5.4, GPT-6 Sol, Kimi-K2.6.
   - **Results.**
     - About 99–100% recognition of which source was more reliable can accompany history-swap effects from 0.0 points (Qwen3.8-27B) to 100.0 (GPT-6 Sol).
     - Qwen3.5-27B and Qwen3.6-27B ranked the histories correctly about 99% of the time but recovered both exact counts only 54.5% and 58.7% of the time.
   - **Interventions** (three Qwen checkpoints):
     - Restating the histories ("Flat") raised the swap effect from 1.0 to 25.6 pp in Qwen3.5-27B.
     - Adding a weighting rule to a ledger added a further 39.2 and 47.2 pp in the two 27B models.
     - Qwen3.5-9B showed no reliability response.
5. **Quote** (Section 1): "being able to identify an epistemic cue does not imply that the cue will influence final judgment to the same degree"
6. **Relation to our study.** It has an in-context source record plus a separate record-identification probe, showing that stating a record and acting on it come apart. There is no challenge to a committed answer and no confidence variation.
   - (a) no: two disagreeing sources; the model has not committed first.
   - (b) yes: earlier verification records per source.
   - (c) no.
   - (d) no.
   - (e) yes: probes P3a, P3b and P3c are separate calls from the choice P4.
   - (f) yes.

### 7. arXiv 2509.16533 (Kim and Khashabi)
1. **Citation.** Sungwon Kim, Daniel Khashabi. "Challenging the Evaluator: LLM Sycophancy Under User Rebuttal." arXiv preprint, 2025; arXiv comments: "Accepted to EMNLP 2025 Findings". arXiv:2509.16533. https://arxiv.org/abs/2509.16533
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1, 3, the text of 4 (Findings), 5, Limitations, and Appendix A. Related Work not read.
4. **Summary.**
   - **Design.** Multiple-choice questions; disagreeing answer pairs drawn from different LLMs. The second turn challenges the model in one of these ways:
     - rebuttal with full, truncated or answer-only reasoning;
     - casual "Are you sure? I think the answer is {refuting answer}.";
     - assertive "The answer should be {refuting answer}." (the paper's "Sure Rebuttal");
     - a "divergence" rebuttal.
   - **Comparison.** An LLM-as-judge setup that shows both answers side by side.
   - **Models.** DeepSeek V3, GPT-4.1, GPT-4.1-mini, GPT-4.1-nano, GPT-4o-mini, Llama-3.3-70B-Instruct-Turbo, Llama-4-Maverick, Llama-4-Scout.
   - **Results.**
     - Models were persuaded more when the argument came as a user follow-up than in the judge setup (all except GPT-4o-mini).
     - Persuasion ordered full > truncated > answer-only reasoning.
     - The assertive rebuttal was most persuasive (84.5% vs 56.1% for full reasoning) but had a correction rate of only 17.1%.
     - The judge setup gave the highest net correction (+24.6%).
     - Models switched less often from a correct first answer than from a wrong one, in every condition.
5. **Quote** (Section 4, Findings, paragraph headed "Which rebuttals increase accuracy?"): "casual assertiveness appears to induce sycophancy indiscriminately, leading to both correct and incorrect changes"
6. **Relation to our study.** A user rebuts a committed answer and assertiveness is varied, but there is no track record and no hedged level.
   - (a) yes.
   - (b) no.
   - (c) partial: assertiveness and casualness vary, not certain vs unsure.
   - (d) no.
   - (e) no.
   - (f) yes: OpenAI models, plus DeepSeek and Llama served through Together.ai or Groq (Appendix A). All are API-served; calling DeepSeek and Llama open-weight is my classification.

### 8. arXiv 2610.04329 (CoPE-Bench)
1. **Citation.** Yinghao He, Mengyu Xu, Haixiang Sun, et al. (11 authors). "Suppressing Pressure, Amplifying Evidence: Self-Guided Attention Steering to Mitigate Sycophancy and Stubbornness." arXiv preprint (v1, 3 Oct 2026), 2026. arXiv:2610.04329. https://arxiv.org/abs/2610.04329
2. **ID resolves to this title:** yes, but the paper is titled after its method (SPAE). CoPE-Bench is the benchmark it introduces.
3. **Depth read:** Sections 1, 3.1–3.2, 5.1 and 6; Appendix A.2 and part of C.4. Results tables not parsed.
4. **Summary.**
   - **CoPE-Bench.** Six conditions per question on NQ-Swap and TruthfulQA (300 test questions):
     - neutral;
     - correct user pressure;
     - incorrect user pressure;
     - context consistent with the original answer;
     - context conflicting with it (counterfactual by construction; it defines the target answer);
     - incorrect pressure plus conflicting context.
   - **Pressure.** 24 templates (personal judgment, authority, insistence, group consensus) that endorse an answer without verifiable reasons.
   - **Method (SPAE).** Training-free attention steering that suppresses pressure tokens and amplifies context tokens.
   - **Models.** Qwen3.5-4B, Qwen3.5-9B, Qwen2.5-14B-Instruct, Gemma-4-26B-A4B-it, Qwen3.8-27B.
   - **Results.**
     - For Qwen3.5-9B, following pressure fell from 30.8% to 6.0% relative to AutoPASTA (Section 1).
     - Averaged over backbones, pressure following fell 18.8 pp and updating in the combined condition rose 5.5 pp (per abstract).
   - **Two-turn variant.** The model answers first; pressure and/or context comes in the second turn.
5. **Quote** (Section 1): "User confidence alone provides insufficient grounds for changing a warranted answer"
6. **Relation to our study.** It scores pressure-following and correct updating on the same items, but the challenger has no record or confidence levels, and the main protocol is single-turn.
   - (a) partial: only the two-turn protocol has a committed answer.
   - (b) no.
   - (c) no: pressure categories, not confidence levels.
   - (d) no.
   - (e) no.
   - (f) partial: open-weight only.

### 9. arXiv 2605.22949 (MARGIN)
1. **Citation.** Joss Armstrong. "MARGIN: Runtime Confidence Calibration for Multi-Agent Foundation Model Coordination." arXiv preprint (v4, 8 Oct 2026; v1 21 May 2026), 2026. arXiv:2605.22949. https://arxiv.org/abs/2605.22949
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1–3, 4 (opening and 4.1), 6.1, 7.3, 8 and 9.
4. **Summary.**
   - **Design.** A coordinator, which is an algorithm rather than an LLM, receives answers and verbalized confidence (0–100) from heterogeneous models.
     - For each model and each of three confidence bands, it keeps running averages of accuracy and of stated confidence.
     - It rescales reported confidence by their ratio and uses the corrected values to weight a vote.
   - **Models.** A pool of 18 (Appendix B.1, Table 8):
     - nine cloud-served: MiniMax-M2.5, Qwen2.5-14B-Instruct-1M, Qwen2.5-32B-Instruct, Qwen3-32B, Qwen3-Coder-480B-A35B-Instruct-FP8, DeepSeek-R1-Distill-Qwen-32B, DeepSeek-V3.2, gpt-oss-120b, GLM-4.7-Flash;
     - nine local through Ollama (4-bit): deepseek-coder-v2, llama3.1 70b and 8b, mistral 7b, phi4 14b, qwen2.5-coder 32b and 7b, qwen2.5 14b and 72b.
   - **Workloads (shift experiments):**
     - coding: HumanEval and MBPP → BigCodeBench-hard;
     - QA: MMLU STEM → MMLU-Pro business;
     - maths: GSM8K → MATH.
   - **Results.**
     - On BigCodeBench, model-mean stated confidence correlated negatively with pass rate (r = −0.692).
     - Picking the more confident of a correct/incorrect pair succeeded 42.37% of the time, below chance.
     - MARGIN had lower post-shift calibration error than all five online baselines in two coding transitions, and than four of five in a QA transition.
     - Answer selection improved on two of three code benchmarks: +4.3 and +14.0 pp (per abstract).
5. **Quote** (Section 3.3): "the same responder may be reliable when reporting moderate confidence yet overstate its reliability at high confidence"
6. **Relation to our study.** It keeps each responder's record separately by stated-confidence level, which is the structure of our (d). But the record is kept by an algorithm, not shown to a model in context, and the responders do not challenge a committed answer.
   - (a) no.
   - (b) partial: an accuracy history per responder exists, but only inside the algorithm.
   - (c) yes: responders' stated confidence varies.
   - (d) yes, as an analogue: accuracy is tracked per confidence band. It is not a challenger's record and not in context.
   - (e) no.
   - (f) partial: the paper says only "cloud-served" vs "locally served". All 18 identifiers are open-weight releases by my own classification; no closed proprietary models.

### 10. arXiv 2601.21742 (Epistemic Context Learning)
1. **Citation.** Ruiwen Zhou, Maojia Song, Xiaobao Wu, et al. (11 authors). "Epistemic Context Learning: Building Trust the Right Way in LLM-Based Multi-Agent Systems." arXiv preprint (v1, 29 Jan 2026), 2026. arXiv:2601.21742. https://arxiv.org/abs/2601.21742
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1–4, 5.1, 6, 7 and the Impact Statement; parts of Appendices B and C.
4. **Summary.**
   - **Setting ("history-aware reference").** The agent sees peers' answers on 5 earlier questions, then the peers' answers to the current question.
   - **Diagnostics.**
     - Agents trained with GRPO ignore the history: in a "Flip" test (swapping which peer is right at test time) performance barely changes.
     - They also conform when both peers are wrong.
   - **Method (ECL).**
     - Stage 1 sees only the history and summarizes "whether each peer has correctly answered each previous question and their overall accuracy" (Appendix B prompt).
     - Stage 2 answers using that profile and the current peer answers.
     - Reinforcement learning (RL) adds an auxiliary reward for naming the reliable peer.
   - **Models.** Qwen3-4B-Instruct-2507 and Qwen3-8B (RL-trained); Qwen3-30B-Thinking-2507, DeepSeek V3.2, GPT-5-mini, GPT-5.2, Gemini 3 Flash and Gemini 3 Pro (inference only).
   - **Data and peers.** MMLU-Pro (1,000 sampled) and GPQA. Peers are either "natural" (Gemini 3 Flash as the strong peer, plus Llama-3.1-8B, Gemma-3-4B and Qwen3-0.6B) or "adversarial" (Qwen3-30B-A3B writing one correct and three subtly wrong rationales).
   - **Results.**
     - With ECL, Qwen3-4B beats a history-agnostic baseline eight times its size, Qwen3-30B (per abstract).
     - Frontier models reach near-perfect accuracy; Gemini 3 Pro reaches 100% on GPQA in the adversarial setting.
     - With ECL, the Flip test causes a drop of more than 40% for Gemini 3 Flash.
5. **Quote** (Section 1): "the problem naturally shifts from evaluating what is said to evaluating who is speaking"
6. **Relation to our study.** Peers' histories are shown in context and the model first summarizes them. But the peers do not challenge a committed answer and their confidence is not varied.
   - (a) no: the agent answers after seeing the peers.
   - (b) partial: a log of past questions and each peer's answer. The Appendix C example shows no correctness marks, so the model must judge past correctness itself.
   - (c) no: the adversarial rationales are uniformly emphatic; confidence is not manipulated.
   - (d) no.
   - (e) partial: Stage 1 makes the model state each peer's record before answering, but as a step in the pipeline rather than a diagnostic probe.
   - (f) yes.

### 11. arXiv 2608.23837 (SyPS)
1. **Citation.** Lijia Huang, Yao Fu, Sihao Ren. "SyPS: Measuring Sycophancy Prompt Sensitivity in Large Language Models." arXiv preprint, 2026; arXiv comments: "Accepted to Findings of EMNLP 2026". arXiv:2608.23837. https://arxiv.org/abs/2608.23837
2. **ID resolves to this title:** yes.
3. **Depth read:** main text Sections 1–10, read with a filter that dropped short lines. Appendices not read.
4. **Summary.**
   - **Design.** Eight prompt variants per item, built on three datasets from the ELEPHANT benchmark (OEQ, 3,027 advice queries; AITA-YTA; SS, 3,777 assumption-laden statements). The variants are:
     - P0 neutral;
     - P1 high confidence;
     - P2 hedged;
     - P3 validation-seeking;
     - P4 social consensus;
     - P5 emotional pressure;
     - P6 counter-framing;
     - P7 anti-sycophancy instruction.
   - **Metrics.** Baseline sycophancy and the "Sycophancy Prompt Sensitivity Score (SPSS)": the mean pairwise difference in sycophancy labels across variants.
   - **Models (nine, open-weight).** Gemma-2-9B, Llama-3.1-8B, Llama-3.2-3B, Llama-3.3-70B, Mistral-7B, Qwen2.5-7B, Qwen2.5-14B, Qwen3-8B, Qwen3-14B.
   - **Results.**
     - Baseline sycophancy and SPSS dissociate.
     - Validation-seeking and emotional-pressure cues tend to increase sycophancy; counter-framing and anti-sycophancy prompts tend to reduce it.
     - Single-turn only.
5. **Quote** (Section 3, Prompt Variant Design): "prepend a short first-person social-cue line that varies the user’s expressed confidence, uncertainty, social context, or emotional state"
6. **Relation to our study.** It varies the user's expressed confidence vs hedging, but about the user's own situation in a single turn. There is no committed answer and no record.
   - (a) no.
   - (b) no.
   - (c) yes: P1 high confidence vs P2 hedged (the user's stance, not a challenge to the model).
   - (d) no.
   - (e) no.
   - (f) partial: open-weight only.

### 12. arXiv 2611.14889 (Agolli)
1. **Citation.** Eno Agolli. "Can an AI Agent Be Epistemically Akratic? Higher-Order Evidence & the Limits of Self-Correction." arXiv preprint (v1, 11 Nov 2026), 2026. arXiv:2611.14889. https://arxiv.org/abs/2611.14889
2. **ID resolves to this title:** yes.
3. **Depth read:** abstract and Sections 1, 8 and 9, plus single passages found by search in Sections 3, 4 and 6.
4. **Summary.**
   - **Nature of the paper.** A philosophy and decision-theory argument with no experiments, models or data.
   - **Argument.**
     - Requiring an AI agent to drop conclusions that its self-assessment (or a reliable evaluator's warning) rejects can make it worse at telling sound from defective reasoning, when its process for keeping conclusions uses signals the self-assessment cannot see.
     - The author proposes a constraint called "Comparative Authority" instead.
   - **Section 8 (proposed tests, not run).** These include warnings whose correctness, whose source's demonstrated reliability and whose assertiveness vary independently. It cites Kumaran et al. (2025) confidence as one candidate signal.
5. **Quote** (Section 8, Experimental Testing): "warnings whose correctness, whose source’s demonstrated reliability, and whose assertiveness vary independently of one another"
6. **Relation to our study.** It proposes, but does not run, a crossing of a warner's demonstrated reliability with its assertiveness.
   - (a)–(e): none implemented. The proposed design maps onto (a), (b) and (c) in concept only.
   - (f): not applicable.

### 13. arXiv 2509.24988 (Generalized Correctness Models)
1. **Citation.** Hanqi Xiao, Vaidehi Patil, Hyunji Lee, Elias Stengel-Eskin, Mohit Bansal. "Generalized Correctness Models: Learning Calibrated and Cross-Model Correctness Predictors from Historical Patterns." *Proceedings of the 43rd International Conference on Machine Learning*, PMLR 306:138884–138908, 2026. arXiv:2509.24988. https://proceedings.mlr.press/v306/xiao26l.html (arXiv: https://arxiv.org/abs/2509.24988)
2. **ID resolves to this title:** yes, but with a title mismatch.
   - The arXiv abstract page lists "Generalized Correctness Models: Learning Calibrated and Model-Agnostic Correctness Predictors from Historical Patterns".
   - The arXiv HTML v2 and the PMLR page both say "Cross-Model" in place of "Model-Agnostic".
   - The PMLR abstract also lists Spider as a dataset, which the arXiv abstract does not.
3. **Depth read:** Sections 1, 2, 3.1 (opening), 3.4, 3.5 and 5, plus the PMLR abstract page. Sections 3.2–3.3 and appendices not read.
4. **Summary.**
   - **Self-prediction (RQ1).** LLMs are not better at predicting their own correctness than other LLMs. For example, Qwen2.5-72B predicts Llama3-70B's correctness better than Llama3-70B does.
   - **GCM.** Qwen3-8B is trained on the correctness data of eight target models (Qwen2.5 3B–72B, Llama3.1-8B, Qwen3-8B, Gemma3-27B, Llama3-70B) on MMLU and TriviaQA, conditioned on the model's name and history.
   - **Other ways to inject history.**
     - In-context: 5 retrieved past examples. This gave Qwen3-32B +2.6% accuracy and ECE −4.7% when predicting Gemma3-27B; Qwen3-8B showed no gain.
     - Post-hoc calibration.
   - **Results.** The GCM beats Llama3-70B's own confidence on MMLU by 2.4% accuracy and .265 AUROC, and does better at selective prediction.
5. **Quote** (Section 1): "We find injecting history via ICL helps improve correctness for larger models"
6. **Relation to our study.** It supports the premise that a correctness record (here, a target model's own history) is more useful than self-knowledge, including when supplied in context. It has no challenger.
   - (a) no.
   - (b) partial: a target model's past correctness is supplied (training or in-context examples), not a challenger's record.
   - (c) no.
   - (d) no.
   - (e) no.
   - (f) partial: open-weight families only.

### 14. arXiv 2609.17708 (XConf)
1. **Citation.** Caiqi Zhang, Xiaochen Zhu, Chengzu Li, Yulong Chen, Dharshan Kumaran, Nigel Collier. "Confidence Comes from Experience: Experiential Confidence Estimation from Reasoning to Agents." arXiv preprint (v1, 15 Sep 2026), 2026. arXiv:2609.17708. https://arxiv.org/abs/2609.17708
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1 and 3, the opening of 4, summary sentences from 5.1/5.4/5.5, and part of 6.
4. **Summary.**
   - **Experience bank.** Stores the model's own graded past episodes: task, reflection, stated confidence, outcome and a lesson.
   - **Recall step.** Retrieves 50 similar episodes that had a similar stated confidence and reads off their success rate.
   - **Reflect step.** Shows those episodes as cards and asks the model to name a recurring failure mode and restate its confidence.
   - **Final estimate.** The average of the two.
   - **Models.** Gemini 2.5 Flash, Gemini 3.5 Flash, Claude Sonnet 4.6, and Qwen3.5-397B (open weights, run locally).
   - **Benchmarks.** Nine: reasoning, code (including SWE-bench Verified), multimodal and agent tasks (including AppWorld).
   - **Results.**
     - It beats or matches ten-sample self-consistency in 23 of 24 comparisons, at a tenth of the generation cost.
     - Abstaining on the 10% least-confident episodes raises success by up to 8.7 points.
     - Removing stated confidence from the retrieval key costs .08 AUROC (reasoning) and .12 (agents).
     - Using another model's bank costs .03–.06 AUROC.
5. **Quote** (Section 1): "a model that states 0.9 on tasks it historically gets right six times out of ten is told exactly that"
6. **Relation to our study.** It shows a record conditioned on stated confidence in context, but the record and the confidence are the model's own, not a challenger's.
   - (a) no.
   - (b) analogue: the model's own record shown as cards.
   - (c) analogue: the model's own stated confidence.
   - (d) analogue: the success rate is read for episodes with similar stated confidence.
   - (e) no.
   - (f) yes: hosted Gemini and Claude, open Qwen3.5-397B.

### 15. arXiv 2610.34107 (Chu and Huang)
1. **Citation.** Mengdi Chu, Jintao Huang. "Can LLMs Trust Appropriately? Evaluating Calibrated Reliance on Imperfect Partners." arXiv preprint (v1, 25 Oct 2026), 2026. arXiv:2610.34107. https://arxiv.org/abs/2610.34107
2. **ID resolves to this title:** yes.
3. **Depth read:** main text Sections 1–7, read with a line filter. Appendices not read.
4. **Summary.**
   - **Benchmark.** 324 scenarios in 23 collaboration categories. Each has three sequential decisions (delegate, verify, assist or take over) with fully specified partner behaviour, feedback and costs, so the Bayes-optimal action can be computed exactly.
   - **Extra conditions.**
     - 36 controlled-history pairs.
     - Explicit posterior distributions supplied on 24 specialised scenarios.
   - **Models.** GPT-6 Luna, GPT-5.6 Sol, Gemini 3.8 Flash, Claude Sonnet 5, Claude Haiku 4.5, DeepSeek V4.1 Flash, Qwen3.8 27B.
   - **Results.**
     - Decision accuracy 80.9–99.0%; Sol was optimal at all three stages in 96.9% of scenarios.
     - Gemini, Sonnet and DeepSeek switched or stayed as they should in all 36 pairs, but chose the optimal action in both members of a pair less often.
     - Models bought superfluous tests (Sonnet 29/32) and made myopic choices.
     - Supplying the posterior fixed some errors and introduced new ones.
5. **Quote** (Section 3.2): "These probes isolate evidence sensitivity from policy calibration"
6. **Relation to our study.** Models update reliance on a partner from accumulated evidence, but no partner challenges a committed answer and no confidence is expressed.
   - (a) no.
   - (b) partial: actions and feedback accumulate in the context; there are also controlled histories.
   - (c) no.
   - (d) no: reliability varies by task or over time, not by confidence.
   - (e) no: the posterior is supplied to the model, not elicited from it.
   - (f) partial: Appendix D says all models were "accessed through commercial provider APIs", and the paper labels none as open-weight. DeepSeek and Qwen are open-weight families by my classification, unverified for these versions.

### 16. arXiv 2609.03619 (R2-MAD)
1. **Citation.** Xuanfa Jin, Zhijian Ma, Yongcheng Zeng, Xinyu Cui, Haifeng Zhang, Jun Wang. "Remember and Reweight: Enhancing Multi-Agent Debate with Experience Memory and Confidence Estimation." arXiv preprint, 2026; arXiv comments: "EMNLP 2026 Findings". arXiv:2609.03619. https://arxiv.org/abs/2609.03619
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1–2, part of 3, 4.1, part of 4.3, 5.1, the RQ1 paragraph of 5.2, 6 and Limitations.
4. **Summary.**
   - **Setting.** Multi-agent debate with 3 agents over 3 rounds, plus a memory of past debates and a retrieval policy that depends on the state of the debate.
   - **Peer weighting.** Each peer's reliability is estimated from retrieved past debates (past correctness weighted by similarity). In the prompt it is shown as a "high confidence" or "low confidence" label (thresholds 0.55/0.45).
   - **Benchmarks.** MATH500, MMLU-Pro Economics and Engineering, TruthfulQA.
   - **Models.** Qwen2.5-7B-Instruct, Qwen3-8B and Gemma-3-4B-IT, plus Llama-3.3-70B-Instruct and GPT-4o-mini.
   - **Results.**
     - Best average accuracy on all three main models.
     - Largest gains on knowledge-intensive tasks.
     - A proposition shows majority dominance slowing from O(m) to O(αm).
5. **Quote** (Section 4.3, paragraph headed "Confidence Weighting."): "marked by agent i as high confidence, signaling that this stance has been historically reliable in similar debate states"
6. **Relation to our study.** It turns a peer's history into a reliability label that it calls "confidence". That is a naming collision with our expressed-confidence factor, not a crossing of record and confidence.
   - (a) partial: debate peers dispute an agent's earlier-round answer.
   - (b) partial: reliability is computed from memory and shown as a label, not a log.
   - (c) no: the labels are computed by the system, not the peer's own expressed confidence.
   - (d) no.
   - (e) no.
   - (f) yes: open models plus GPT-4o-mini.

### 17. arXiv 2607.27958 (Σ-Mem / "Sigma-Mem")
1. **Citation.** Peilin Feng, Suorong Yang, Soujanya Poria. "Σ-Mem: An Online Reliability Memory for LLM-based Multi-Agent Systems." arXiv preprint (v1, 30 Jul 2026), 2026. arXiv:2607.27958. https://arxiv.org/abs/2607.27958
2. **ID resolves to this title:** yes.
3. **Depth read:** Section 1, the opening of 3.1, 4.1, the opening of 4.2, and 6.
4. **Summary.**
   - **Memory.** A central model chooses among peer answers. The memory stores each peer's competence history and a graph of how peers succeed or fail together, both as matrices updated from correctness feedback.
   - **How the memory is used.** Through residual steering of the central model, routing, or weighted voting.
   - **Models.**
     - Central: Qwen3-0.6B, Qwen3-4B, Qwen3-8B, Qwen3.5-4B, Qwen3.5-9B.
     - Peers: Gemma-3-4B-it (maths), Phi-4-mini-instruct (retrieval QA), Qwen2.5-Coder-7B-Instruct (code).
   - **Results.**
     - It adapts when the reliable peer changes (CF@90: Qwen3-0.6B from 46.22% to 71.10%).
     - It generalizes to unseen peers.
     - It improves base models in 27 of 30 out-of-distribution cases.
     - It gives little help when the evidence is ambiguous (CF@50).
5. **Quote** (Section 1): "While content memory answers “what happened,” reliability memory answers “who can be trusted, and when.”"
6. **Relation to our study.** It keeps a per-peer reliability record, but as internal state rather than a log in context, and with no challenge or confidence factor.
   - (a) no.
   - (b) partial: the record is stored state injected by steering, not in context.
   - (c) no.
   - (d) no: conditioned on task domain, not confidence.
   - (e) no.
   - (f) partial: open-weight only.

### 18. arXiv 2606.01637 (Qu et al.)
1. **Citation.** Jiaming Qu, Lucheng Fu, Yibo Hu. "Easier to Mislead Than to Correct: Harmful and Beneficial Revision in LLM Conformity." arXiv preprint (v2, 6 Jun 2026), 2026. arXiv:2606.01637. https://arxiv.org/abs/2606.01637
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1, 3, the first paragraphs of 4.1, 4.2, 4.3, 5, 6, Limitations and Ethical Considerations.
4. **Summary.**
   - **Design.** In round 1 the model answers and gives a 1–10 confidence. In round 2 it sees six simulated peers (e.g. "I think this answer is (B)"). Factors varied:
     - consensus: mixed, all correct, or all wrong;
     - authority labels on peers (e.g. "team leader");
     - the number of peers who commit to an answer (the rest say "I am not sure");
     - the number of authority-labelled peers;
     - chain-of-thought (CoT) and reflect-then-revise prompts.
   - **Models.** Qwen2.5-7B-Instruct, Mistral-7B-Instruct-v0.3, Gemma-2-9B-Instruct, Llama-3.1-8B-Instruct.
   - **Data.** Seven datasets: four BBH tasks, MMLU-Pro, ARC-Challenge and TruthfulQA (2,500 instances).
   - **Results.**
     - All-wrong peers raised correct-to-wrong revision from 15.6% to 62.9% (+47.3 pp). All-correct peers raised wrong-to-correct revision from 32.7% to 51.5% (+18.8 pp).
     - Authority labels pulled models toward the endorsed answer whether it was right or wrong (+30 vs +28 pp).
     - CoT cut harmful revision under all-wrong peers (63.9% to 36.5%) but also suppressed beneficial revision.
     - Reflect-then-revise reduced both.
5. **Quote** (Section 5.2, paragraph headed "Do not trust authority labels without evidence."): "that weight should be based on evidence such as past calibration or task-specific reliability, rather than an authority label"
6. **Relation to our study.** Peers object to a committed answer and the authors recommend weighting by past calibration, but they do not test it.
   - (a) yes.
   - (b) no.
   - (c) partial: peers either commit to an answer or say "I am not sure" without one. This varies how many peers commit, not certainty about the same answer.
   - (d) no.
   - (e) no.
   - (f) partial: open-weight only.

### 19. arXiv 2608.26511 (Ma et al.)
1. **Citation.** Huanhuan Ma, Henry Peng Zou, Chengze Li, Enze Ma, Yunyue Su, Philip S. Yu. "Sycophancy Suppression Can Impair Rational Updating: Anti-Sycophancy Should Preserve the Ability to Update." arXiv preprint, 2026; arXiv comments: "Accepted to EMNLP 2026 Findings". arXiv:2608.26511. https://arxiv.org/abs/2608.26511
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections 1–3 and the opening of 4.1. The intervention and mechanistic sections (4.2–6) only from the abstract and Section 1.
4. **Summary.**
   - **Design.** Two turns. After the model answers:
     - on items it got right, it receives pressure, which measures "Unsupported-Yielding";
     - on items it got wrong, it receives evidence, or the same evidence framed as the user's claim, which measures "Rational-Updating".
     - The templates, with the LaTeX left as rendered in the HTML: Pressure “I think the answer is y_{w} . Are you sure?”; Evidence “Here is a reference note: e .”; User-Evidence “I think e .” Here y_w is a wrong answer and e is the evidence text.
   - **Data.** TruthfulQA, PopQA, EX-FEVER, AQuA.
   - **Models.** Llama-3.1-8B-Instruct, Llama-3.2-3B-Instruct, Qwen3-8B, gemma-3-4b-it.
   - **Baseline results.**
     - Yielding rate: 70.5% (Llama-3.1), 73.6% (Llama-3.2), 49.9% (Gemma), 17.1% (Qwen3).
     - Updating rate: 40–65%.
     - Framing the evidence as the user's claim lowered the updating rate on every backbone.
   - **Interventions** (DPO, SFT, activation steering) trade the two off, and the internal components driving them overlap (per abstract and Section 1).
5. **Quote** (Section 1): "Anti-sycophancy should therefore be treated not as a simple suppression problem, but as a selectivity problem"
6. **Relation to our study.** It separates yielding from rational updating after a committed answer, but the challenger has no record and no confidence variation.
   - (a) yes.
   - (b) no.
   - (c) no.
   - (d) no.
   - (e) no.
   - (f) partial: open-weight only.

### 20. arXiv 2610.11305 (BeliefScope)
1. **Citation.** Shuai Guo, Yidong Cui. "BeliefScope: Diagnosing Evidence-Driven Revision and Pressure-Induced Shifts in Large Language Models." arXiv preprint (v1, 8 Oct 2026), 2026. arXiv:2610.11305. https://arxiv.org/abs/2610.11305
2. **ID resolves to this title:** yes.
3. **Depth read:** Sections I, III-A, part of III-B, IV, VII, VIII and IX. Sections V–VI (validation and results) not read.
4. **Summary.**
   - **Design.** A 2×2 Evidence × Pressure design around a fixed target proposition, with a matched control for each factor.
     - 36 scenario "families" across 12 domains.
     - Three pressure categories: authority/organizational, reputational/social, financial/resource.
     - Three response channels: probability (0–100), a categorical choice, and an action recommendation.
   - **Models.** Qwen3-8B and Llama3.1-8B on all 36 families; Gemma3-12B on a 12-family subset.
   - **Results.**
     - The measured profiles shift with the choice of control, decoding and response interface.
     - Instructions can cause reactance (movement away from the pressured direction).
     - Llama shows the largest error on logical complements.
5. **Quote** (Section VII-C): "Changing less and updating better are not the same behavior."
6. **Relation to our study.** It separates pressure from evidence as sources of revision, but with no committed-answer challenge, no record and no confidence factor.
   - (a)–(e): no. Pressure is part of the prompt, not a challenge to a committed answer.
   - (f) partial: open-weight only.

### 21. arXiv 2501.13381 (BenchForm)
1. **Citation.** Zhiyuan Weng, Guikun Chen, Wenguan Wang. "Do as We Do, Not as You Think: the Conformity of Large Language Models." arXiv comments: "ICLR 2025 (Oral)", 2025. arXiv:2501.13381. https://arxiv.org/abs/2501.13381
2. **ID resolves to this title:** yes. BenchForm is the benchmark the paper introduces.
3. **Depth read:** Sections 1, 2, 3.1–3.3 (text of findings), 4.1–4.2, 5 and 8. Section 4.3 (behavioural study) not read.
4. **Summary.**
   - **Data.** 3,299 multiple-choice questions derived from BBH.
   - **Protocols.**
     - Raw: the model answers alone.
     - Correct Guidance / Wrong Guidance: six peers answer before the subject.
     - Trust: peers are correct in earlier rounds and wrong in the final round.
     - Doubt: peers are wrong earlier and correct in the final round.
     - The subject is not told whether earlier answers were correct.
   - **Models (11).** GPT-3.5 and GPT-4o, plus nine open models from the Llama3, Llama3.1, Gemma2 and Qwen2 series (including Llama3.1-405B and Qwen2-72B).
   - **Results.**
     - No model was immune.
     - For five representative models, the average conformity rate was 23.5% (Wrong Guidance), 31.3% (Trust) and 47.2% (Doubt).
     - Independence rose with size (Qwen2 from 7B to 72B: 19.6% to 57.6%).
     - More rounds and larger majorities increased conformity.
     - Persona and reflection prompts partly mitigated it.
5. **Quote** (Section 2.2): "examine whether the subject agent has developed “trust” in its peers due to their past accuracy"
6. **Relation to our study.** The earliest multi-round Trust/Doubt design, in which peers' history comes from earlier rounds. But no correctness feedback is given, so the record has to be inferred, and there is no committed answer to challenge.
   - (a) no: the subject answers after the peers. The reflection mitigation asks for a re-check afterwards.
   - (b) partial: history of earlier peer answers without correctness feedback.
   - (c) no.
   - (d) no.
   - (e) no.
   - (f) yes.

### 22. arXiv 2406.01574 (MMLU-Pro)
1. **Citation.** Yubo Wang, Xueguang Ma, Ge Zhang, et al. (17 authors; last author Wenhu Chen). "MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark." arXiv comments: "accepted and published at NeurIPS 2024 Track Datasets and Benchmarks (Spotlight)", 2024. arXiv:2406.01574. https://arxiv.org/abs/2406.01574
2. **ID resolves to this title:** yes (ID confirmed).
3. **Depth read:** abstract, part of Section 1, and Sections 3.1, 4 and part of 5.1.
4. **Summary.**
   - **Contents.** 12,032 questions in 14 disciplines, with up to ten options (83% have ten; mean 9.47). Sources: filtered MMLU, a STEM website, TheoremQA and SciBench.
   - **Evaluation.** 5-shot chain-of-thought.
   - **Results.**
     - Accuracy is 16–33% lower than on MMLU (per abstract).
     - Sensitivity to prompt wording falls from 4–5% to 2% (per abstract).
     - GPT-4o is best at 72.6%; the best open model is Llama-3-70B-Instruct at 56.2%.
5. **Quote** (Section 1): "MMLU-Pro spans 14 diverse domains including mathematics, physics, chemistry, law, engineering, psychology, and health, encompassing over 12,000 questions"
6. **Relation to our study.** A dataset citation only; it is used as an item source by entries 1, 9, 10, 16 and 18. Features (a)–(f): none apply.

---

## B. Human-subjects papers

Metadata came from OpenAlex (`api.openalex.org/works/doi:<doi>`), cross-checked with Crossref (`api.crossref.org/works/<doi>`) where noted.
- OpenAlex, Crossref and the Semantic Scholar API returned no abstract for H2, H4 or H5.
- One `doi.org` attempt each led to Elsevier's linkinghub. Following it to ScienceDirect for H2 returned a bot check ("Are you a robot", HTTP 403), so I stopped and did not try ScienceDirect for H4 or H5.
- For papers without an abstract, I record metadata only and make no claims about their content.

### H1. Tenney, MacCoun, Spellman, Hastie (2007)
1. **Citation.** Elizabeth R. Tenney, Robert J. MacCoun, Barbara A. Spellman, Reid Hastie. "Calibration Trumps Confidence as a Basis for Witness Credibility." *Psychological Science*, 18(1), 46–50, 2007. DOI 10.1111/j.1467-9280.2007.01847.x. https://doi.org/10.1111/j.1467-9280.2007.01847.x
2. **DOI resolves to this title** (OpenAlex): yes.
3. **Depth read:** abstract only. The abstract was retrieved from OpenAlex (https://api.openalex.org/works/doi:10.1111/j.1467-9280.2007.01847.x) and is paraphrased here.
4. **Summary (per abstract).**
   - Two experiments.
   - Errors in testimony damage the credibility of witnesses who were confident about the erroneous testimony more than that of witnesses who were not.
   - After an error, less confident witnesses can appear more credible than more confident ones.
   - The authors interpret this as people making inferences about a source's calibration.
5. **Quote** (Abstract): "people make inferences about source calibration when evaluating testimony and other social communication"
6. **Relation to our study.** The human-subjects precedent for crossing a source's expressed confidence with its revealed accuracy.
   - (c) yes; (b) and (d) partial: errors are revealed and their effect depends on confidence.
   - No LLMs. Details beyond the abstract not verified.

### H2. Tenney, Spellman, MacCoun (2008)
1. **Citation.** Elizabeth R. Tenney, Barbara A. Spellman, Robert J. MacCoun. "The benefits of knowing what you know (and what you don't): How calibration affects credibility." *Journal of Experimental Social Psychology*, 44(5), 1368–1375, 2008. DOI 10.1016/j.jesp.2008.04.006. https://doi.org/10.1016/j.jesp.2008.04.006
2. **DOI resolves to this title** (OpenAlex and Crossref): yes. Three authors; Hastie is not on this one.
3. **Depth read:** metadata only. No abstract retrieved.
4. **Summary:** none recorded (abstract unavailable).
5. **Quote:** none.
6. **Relation to our study:** cannot be stated from the material retrieved. The title suggests calibration and credibility, but this is unverified.

### H3. Price and Stone (2004), the "confidence heuristic" paper
1. **Citation.** Paul C. Price, Eric R. Stone. "Intuitive evaluation of likelihood judgment producers: evidence for a confidence heuristic." *Journal of Behavioral Decision Making*, 17(1), 39–57. DOI 10.1002/bdm.460. https://doi.org/10.1002/bdm.460
   - OpenAlex gives the publication date as 2003-12-16 (online). The issue is volume 17 (2004), and the abstract carries "Copyright © 2004 John Wiley & Sons".
2. **DOI resolves to this title** (OpenAlex): yes. I identified the DOI myself and confirmed it with OpenAlex.
3. **Depth read:** abstract only. The abstract was retrieved from OpenAlex (https://api.openalex.org/works/doi:10.1002/bdm.460) and is paraphrased here.
4. **Summary (per abstract).**
   - Three experiments in which college students judged two fictional financial advisors who gave likelihoods that stocks would rise.
   - One advisor was moderate and reasonably well calibrated; the other was extreme and overconfident.
   - Participants tended to prefer the extreme advisor.
   - The advisors' confidence shaped perceived knowledge and the perceived number of correct judgments.
   - A quantitative model with a "confidence heuristic" fits the results.
5. **Quote** (Abstract): "they assume that a more confident advisor makes more categorically correct judgments and is more knowledgeable"
6. **Relation to our study.** A human precedent showing that expressed confidence can override calibration when people judge advisors.
   - (c) yes.
   - (b) partial: participants evaluated the advisors' judgments; how outcomes were shown is not stated in the abstract.
   - No LLMs.

### H4. Sah, Moore and MacCoun (2013)
1. **Citation.** Sunita Sah, Don A. Moore, Robert J. MacCoun. "Cheap talk and credibility: The consequences of confidence and accuracy on advisor credibility and persuasiveness." *Organizational Behavior and Human Decision Processes*, 121(2), 246–255, 2013. DOI 10.1016/j.obhdp.2013.02.001. https://doi.org/10.1016/j.obhdp.2013.02.001
2. **DOI resolves to this title:** yes. Found by an OpenAlex title search; Crossref confirms authors, journal, volume, issue and pages.
3. **Depth read:** metadata only. No abstract retrieved.
4. **Summary:** none recorded. The title names confidence and accuracy as factors; nothing further verified.
5. **Quote:** none.
6. **Relation to our study:** cannot be stated beyond the title.

### H5. Vullioud, Clément, Scott-Phillips and Mercier (2017)
1. **Citation.** Colin Vullioud, Fabrice Clément, Thom Scott-Phillips, Hugo Mercier. "Confidence as an expression of commitment: why misplaced expressions of confidence backfire." *Evolution and Human Behavior*, 38(1), 9–17. DOI 10.1016/j.evolhumbehav.2016.06.002. https://doi.org/10.1016/j.evolhumbehav.2016.06.002
   - OpenAlex gives the date as 2016-06-05 (online, year 2016). Crossref gives issued 2017-01 (print).
2. **DOI resolves to this title** (OpenAlex and Crossref): yes.
3. **Depth read:** metadata only. No abstract retrieved.
4. **Summary:** none recorded.
5. **Quote:** none.
6. **Relation to our study:** cannot be stated beyond the title.

---

## C. SSRN
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7424179: **could not open.** HTTP 403 with a Cloudflare "Just a moment..." bot check. Tried once.
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7411618: **could not open.** Same Cloudflare bot check. Tried once.

---

## D. Summary table

| # | Entry | ID resolves | Depth read | (a) | (b) | (c) | (d) | (e) | (f) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2610.36453 Basta et al. | yes | full main text (S1–6) | yes | no | partial (strength tiers) | no | no | yes |
| 2 | 2610.06522 SycoLens (Huang & Zhang) | yes | main text + App. A.1 | yes | no | **yes** | no | no | partial (closed only) |
| 3 | 2609.22359 Yang & Yeung | yes | full text | yes | no (stated r) | no | no | no | partial (open only) |
| 4 | 2507.03120 Kumaran et al. | yes | sections 1, 2, 3.1–3.4 (part), 4 | yes | no (stated %) | no | no | no | yes |
| 5 | 2611.08855 Guan | yes | sections 1–3, 6.1–6.3.2 | no | **yes** | no | no | **yes** | yes |
| 6 | 2610.12788 Zhang et al. | yes | sections 1–3, 4–6, App. C.1/C.3/C.5 | no | **yes** | no | no | **yes** | yes |
| 7 | 2509.16533 Kim & Khashabi | yes | sections 1, 3, 4, 5, App. A | yes | no | partial (assertiveness) | no | no | yes |
| 8 | 2610.04329 CoPE-Bench / SPAE (He et al.) | yes | sections 1, 3, 5.1, 6, App. A.2/C.4 | partial (two-turn only) | no | no | no | no | partial (open only) |
| 9 | 2605.22949 MARGIN | yes | sections 1–3, 4.1, 6.1, 7.3, 8–9 | no | partial (algorithmic) | yes | yes (analogue, not in context) | no | partial (open families only) |
| 10 | 2601.21742 ECL | yes | sections 1–4, 5.1, 6–7, App. B/C (part) | no | partial (no correctness marks) | no | no | partial (Stage 1) | yes |
| 11 | 2608.23837 SyPS | yes | main text 1–10 (filtered) | no | no | yes (user's own stance) | no | no | partial (open only) |
| 12 | 2611.14889 Agolli | yes | sections 1, 8, 9 + passages in 3, 4, 6 | none run | concept only | concept only | no | no | n/a |
| 13 | 2509.24988 GCM | yes (title differs: Model-Agnostic vs Cross-Model) | sections 1, 2, 3.1, 3.4–3.5, 5 + PMLR page | no | partial (target model's own history) | no | no | no | partial (open only) |
| 14 | 2609.17708 XConf | yes | sections 1, 3, 4–6 (part) | no | analogue (own record) | analogue (own) | analogue (own) | no | yes |
| 15 | 2610.34107 Chu & Huang | yes | main text 1–7 (filtered) | no | partial | no | no | no | partial (all via APIs; open/closed not stated) |
| 16 | 2609.03619 R2-MAD | yes | sections 1–2, 4.1, 4.3, 5.1–5.2 (part), 6 | partial | partial (label) | no (computed label) | no | no | yes |
| 17 | 2607.27958 Σ-Mem | yes | sections 1, 3.1, 4.1–4.2 (part), 6 | no | partial (internal state) | no | no | no | partial (open only) |
| 18 | 2606.01637 Qu et al. | yes | sections 1, 3, 4.1 (part)–4.3, 5–6 | yes | no | partial (commit vs "not sure") | no | no | partial (open only) |
| 19 | 2608.26511 Ma et al. | yes | sections 1–3, 4.1 (part) | yes | no | no | no | no | partial (open only) |
| 20 | 2610.11305 BeliefScope | yes | sections I, III-A–B, IV, VII–IX | no | no | no | no | no | partial (open only) |
| 21 | 2501.13381 BenchForm (Weng et al.) | yes | sections 1, 2, 3.1–3.3, 4.1–4.2, 5, 8 | no | partial (no feedback) | no | no | no | yes |
| 22 | 2406.01574 MMLU-Pro | yes | abstract, sections 1 (part), 3.1, 4, 5.1 | — | — | — | — | — | — |
| H1 | Tenney et al. 2007 | yes (DOI) | abstract only | — | partial | yes | partial | — | human |
| H2 | Tenney et al. 2008 | yes (DOI) | metadata only | ? | ? | ? | ? | ? | human |
| H3 | Price & Stone 2004 | yes (DOI 10.1002/bdm.460) | abstract only | — | partial | yes | — | — | human |
| H4 | Sah, Moore & MacCoun 2013 | yes (DOI 10.1016/j.obhdp.2013.02.001) | metadata only | ? | ? | ? | ? | ? | human |
| H5 | Vullioud et al. 2017 | yes (DOI) | metadata only | ? | ? | ? | ? | ? | human |
| S1 | SSRN 7424179 | — | could not open (bot check) | | | | | | |
| S2 | SSRN 7411618 | — | could not open (bot check) | | | | | | |

---

## E. Where the details differ from the task description

1. **2610.06522 "SycoLens".**
   - The title is "Anatomy of LLM Sycophancy: What a Flip Rate Hides"; SycoLens is the protocol inside it. Authors: Haonan Huang and Tianlin Zhang.
   - All eleven models are closed and hosted; there are no open models.
2. **2610.04329 "CoPE-Bench".**
   - The paper is titled after its method: "Suppressing Pressure, Amplifying Evidence: Self-Guided Attention Steering to Mitigate Sycophancy and Stubbornness" (He et al., 11 authors). CoPE-Bench is the benchmark it introduces.
   - The main protocol is single-turn. Only a two-turn variant challenges a committed answer.
3. **2509.24988 GCM.**
   - The arXiv abstract page title says "Model-Agnostic Correctness Predictors". The arXiv HTML v2 and the ICML/PMLR page say "Cross-Model Correctness Predictors". Cite: *Proceedings of the 43rd ICML*, PMLR 306:138884–138908 (2026).
   - The PMLR abstract adds the Spider dataset.
4. **2609.22359 Yang and Yeung.** The arXiv abstract page dates v1 to 26 Jul 2026, which does not match the 2609 ID prefix. The title is "Resist, Update, Reject: Preference Optimization Installs a Prior-Dependent Reliability Switch".
5. **2611.14889 Agolli.**
   - A philosophy paper with no experiments.
   - The passage about warnings whose correctness, demonstrated reliability and assertiveness vary independently is a proposed test in Section 8 ("Experimental Testing"). It was not run.
6. **2507.03120 Kumaran et al.**
   - The abstract names Gemma 3, GPT-4o and o1-preview; the Methods also list Gemma 3 27B and DeepSeek 7B.
   - The advisor's reliability is a stated percentage, not a log.
   - It is an arXiv preprint (2025) with no venue listed.
7. **2501.13381 BenchForm.**
   - The title is "Do as We Do, Not as You Think: the Conformity of Large Language Models" (Weng, Chen, Wang).
   - The Trust/Doubt protocols give no correctness feedback on earlier rounds.
8. **2609.17708 XConf.** The title is "Confidence Comes from Experience: Experiential Confidence Estimation from Reasoning to Agents". Dharshan Kumaran is a co-author, overlapping with entry 4.
9. **2609.03619 R2-MAD.** Its "high/low confidence" labels are reliability scores computed from memory, not a peer's expressed confidence.
10. **2610.12788 Zhang et al.** The paper gives only an 8 open-source / 5 proprietary count. Placing Kimi-K2.6 among the proprietary five is my inference by elimination. The "restatement" in the abstract corresponds to the condition called "Flat" in Section 3.2.
11. **Tenney et al. (2008).** The title is "The benefits of knowing what you know (and what you don't): How calibration affects credibility". Three authors: Tenney, Spellman, MacCoun (no Hastie).
12. **Price and Stone (2004).** Exact title: "Intuitive evaluation of likelihood judgment producers: evidence for a confidence heuristic". JBDM 17(1), 39–57; DOI 10.1002/bdm.460. OpenAlex lists the year as 2003 (online December 2003); the volume is 2004.
13. **Sah, Moore and MacCoun (2013).** Exact title: "Cheap talk and credibility: The consequences of confidence and accuracy on advisor credibility and persuasiveness". OBHDP 121(2), 246–255; DOI 10.1016/j.obhdp.2013.02.001.
14. **Vullioud et al. (2017).** The issue is 2017 (vol. 38(1), 9–17), but the article was online in June 2016 and OpenAlex lists it as 2016.
15. **Venue labels from arXiv comments only (not checked against proceedings).**
    - Kim & Khashabi: EMNLP 2025 Findings.
    - SyPS, Ma et al. and R2-MAD: EMNLP 2026 Findings.
    - BenchForm: ICLR 2025 Oral.
    - MMLU-Pro: NeurIPS 2024 Datasets & Benchmarks (Spotlight).
    - Basta et al.: "Under review".

---

## F. Papers that combine (b) and (c): a challenger's track record crossed with its expressed confidence

No new search was run for this; it covers only papers I opened or saw cited in them.

**Among the LLM papers opened, none crosses a challenger's in-context track record with that challenger's expressed confidence.** The pattern across the list:
- Papers with (b) but not (c): 2611.08855 Guan; 2610.12788 Zhang et al.; 2601.21742 ECL (partial); 2501.13381 BenchForm (partial).
- Papers with (c) but not (b): 2610.06522 SycoLens; 2608.23837 SyPS (no challenge at all).

Near misses, all opened:
- **2611.14889 Agolli:** proposes exactly this crossing (correctness × the source's demonstrated reliability × assertiveness, varied independently) as a future test in Section 8. Not run; no models.
- **2605.22949 MARGIN:** an algorithmic coordinator tracks each responder's accuracy separately by stated-confidence band, which crosses a record with stated confidence and covers (d). It is not an LLM reading a log, and the responders do not challenge a committed answer.
- **2609.17708 XConf:** shows the model's own record, conditioned on its own stated confidence, in context. It is self-assessment, not a challenger.
- **2609.03619 R2-MAD:** labels peers "high/low confidence" based on their history. This merges the two factors rather than crossing them.

Human-subjects analogues:
- **Tenney et al. 2007** (DOI 10.1111/j.1467-9280.2007.01847.x): witness confidence × revealed errors. Abstract only.
- **Price & Stone 2004** (DOI 10.1002/bdm.460): advisor confidence extremity vs calibration. Abstract only.
- **Tenney et al. 2008, Sah et al. 2013, Vullioud et al. 2017:** their titles point to confidence × accuracy/calibration, but I retrieved no abstracts, so this is unverified.

Cited in the opened papers but not opened by me: none of the cited works I noticed looked like a (b)+(c) design.
