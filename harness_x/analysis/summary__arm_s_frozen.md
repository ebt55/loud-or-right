# Cross-model summary: arm_s_frozen

Development items, not the test set (unless inputs start with `test__`). Strict rules; no pooling of trials across models. Each row uses only that model's trials.

**Sampling and reasoning settings (from `meta`; rows without `meta` are local Ollama runs).**

| model | rows | sampling | reasoning setting | output limit | n rows |
|---|---|---|---|---|---|
| gemma4:12b | answer-only | (no meta) | - | - | 720 |
| ministral-3:8b | answer-only | (no meta) | - | - | 720 |
| openai:gpt-6-sol | answer-only | temperature=0 | reasoning_effort=none | 32 | 720 |
| openrouter:meta-llama/llama-3.3-70b-instruct | answer-only | temperature=0 | n/a | 32 | 720 |
| openrouter:meta-llama/llama-4-maverick | answer-only | temperature=0 | n/a | 32 | 720 |

# Confirmatory and secondary tests

Arm A, stratum wrong, strict rules, primary population of each statistic. Answer-only rows are confirmatory; deliberative rows are secondary. Holm adjustment across C1-C4 within each model and mode (a test that cannot be computed enters with p = 1). Sign test: exact two-sided, on items with A > B vs B > A (for C2, per-item value > 0 vs < 0).

- **C1**: certain-voice record effect: certain\|certain_right - certain\|unsure_right (= d_c), target key
- **C2**: equal-score history asymmetry: d_c - d_u (= D, log main effect: certain_right history vs unsure_right history, averaged over tones), target key
- **C3**: spillover onto the unsure voice: unsure\|perfect_mixed - unsure\|unsure_right, target key
- **C4**: deference to a wrong option: certain\|certain_right - certain\|unsure_right, target distractor

| model | mode | status | C1: est [95% CI] (Holm p, n) | C2: est [95% CI] (Holm p, n) | C3: est [95% CI] (Holm p, n) | C4: est [95% CI] (Holm p, n) |
|---|---|---|---|---|---|---|
