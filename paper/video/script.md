# Loud or Right? Final voice-over script

**Target length:** 3:10–3:30 in total, and never under 3:00. The visuals for each scene are in `plan.md`.

**Voice:** calm, clear and conversational, at about 160 words per minute (set the text-to-speech rate so the voice-over audio alone runs 3:05–3:15). Leave a pause of about half a second between scenes.

**Reading notes for text-to-speech:**
- Read each VO paragraph exactly as written. Every number comes from `paper/report.md`.
- "GPT-6 Sol" is read "G P T six Saul" (as "Sol" already sounds in scene 9). "Claude Sonnet 5.5" is read "Claude Sonnet five point five". "Llama 3.3" is read "Llama three point three".
- "plus 0.59" is read "plus zero point five nine", and "minus 0.16" is read "minus zero point one six".
- "105 of 160" is read "one hundred and five of one hundred and sixty".

---

## Scene 1: The question

**VO.** Someone tells an AI model that its answer is wrong. Should it change the answer? And what should count: how sure the critic sounds, or how often that critic has been right?

## Scene 2: Two track records

**VO.** Confidence can mislead. Some critics are right when they sound certain. Others are right when they hedge. A careful listener would keep a track record for each tone of voice. We tested whether language models do.

## Scene 3: The test

**VO.** The model sees a practice log: eight past objections from a scripted reviewer, Dana, half certain and half unsure, each marked right or wrong. In one version, Dana is right only when certain. In another, only when unsure. Then Dana objects to the model's own answer, and we record whether the model switches. Fifteen models took the test.

## Scene 4: Two models follow each voice's record

**VO.** Further right, a model follows the certain voice more when its record is good. Further up, the same for the unsure voice. On the diagonal, both voices' records count equally. Claude Sonnet 5.5 and GPT-6 Sol sit there. Five models barely responded.

## Scene 5: A prediction that came true

**VO.** Several open-weight models looked different. They seemed to credit only the confident voice. We had predicted that for two of them, in advance, and it came out as predicted. But our explanation did not hold up.

## Scene 6: The first line of the log

**VO.** Look at the log's first line. In our main version the order never changed, and the first entry was a certain one. So when the certain voice had the good record, the log opened with "Dana was right". Otherwise it opened with "Dana was wrong". Record and order were tangled.

## Scene 7: Reverse it, then shuffle it

**VO.** So we ran exploratory tests, with predictions written down first. We reversed the log. For Llama 3.3, the gap between the voices flipped, from plus 0.59 to minus 0.16. Two more models flipped, and Gemma's gap vanished. Sonnet and Sol stayed on the diagonal. Then we shuffled the order. Compared with the original order, the gaps shrank. Two Llama models kept a small leftover, but it is uncertain, and it disappeared when we changed the reviewer's name, phrases and letters.

## Scene 8: Overall score and tone

**VO.** What else moved these models? Our reading is the reviewer's overall score: they followed an unsure objection far more when Dana had been right every time, though the unsure voice's own record was perfect either way. And tone: with no log, every open-weight model followed a certain objection more often. Yet asked directly, nearly all of them could state each voice's record.

## Scene 9: The cost

**VO.** Using the record has a cost. On questions Sonnet had answered correctly, Dana pushed a wrong answer. When the log favoured Dana's tone, Sonnet, answering immediately, gave up its correct answer on 105 of 160 trials. With brief reasoning, 8 of 160. On questions it had got wrong, it still followed a good record. But there Dana named the correct answer, so that comparison is not clean. Sol almost never gave up a correct answer.

## Scene 10: Takeaways

**VO.** So: at the extremes we tested, two models responded to each voice's own record, in every order we tried. Several others followed order and tone, and seemed to weigh the overall score. Neither being closed nor size marked the split. If you test a model with a track record, randomise its order, or order can pass for record use.

## Scene 11: Credits

**VO.** Code and data are open on GitHub.

This line is spoken as the single credits screen appears. The screen is one still, held for 4 seconds; its text is in `plan.md`.
