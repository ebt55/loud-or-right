"""Real values for the animated charts, copied by hand from the project's analysis files (no recomputation).

Provenance
- Arm A (d_c, d_u): paper/figs/tables.md, Table 7, columns "d_c A" and "d_u A" (two decimals).
  Ministral 3 8B: Table 7 uses the 15 Nov run (0.28, -0.10); arm_r_vs_a.md pairs arm R with a same-day repeat
  (0.300, -0.100). The scatter uses Table 7 for arm A, as the brief asks.
- Arm B (d_c, d_u): paper/figs/tables.md, Table 2, columns "d_c, arm B" and "d_u, arm B" (13 models; Gemini 3.6
  Flash and Qwen 3.8 27B have no arm B).
- Arm R (d_c, d_u): harness_x/analysis/arm_r_vs_a.md, section 1, rows with arm = R (three decimals; 6 models).
- Arm S (d_c, d_u): harness_x/analysis/arm_s.md, section 1 (plain d_c and d_u on all 80 items; 5 models).
  Table 7 only gives the order-balanced D_bal for arm S, which is not a scatter position.
- D strings: Table 7 ("D A", "D R", "D_bal S"), already rounded half away from zero by make_figs.py.

On-screen numbers must be string literals taken from the script/plan or from these tables; never format a float
with Python's ':.2f' for display (it rounds halves to even, e.g. 0.475 -> '0.47', where the paper prints 0.48).
"""

# (key, display name, class)  class: open = open-weight main set, closed = closed main set,
# recency = recency tier (exploratory, open-weight). Order as in paper/make_figs.py MODELS.
MODELS = [
    ("gemma", "Gemma 4 12B", "open"),
    ("ministral8", "Ministral 3 8B", "open"),
    ("qwen35", "Qwen 3.5 9B", "open"),
    ("ministral14", "Ministral 14B", "open"),
    ("llama33", "Llama 3.3 70B", "open"),
    ("dsv32", "DeepSeek V3.2", "open"),
    ("luna", "GPT-6 Luna", "closed"),
    ("sol", "GPT-6 Sol", "closed"),
    ("haiku", "Claude Haiku 5.5", "closed"),
    ("sonnet", "Claude Sonnet 5.5", "closed"),
    ("gemini", "Gemini 3.6 Flash", "closed"),
    ("dsv41", "DeepSeek V4.1 Flash", "recency"),
    ("qwen38", "Qwen 3.8 27B", "recency"),
    ("maverick", "Llama 4 Maverick", "recency"),
    ("mmed", "Mistral Medium 3.5", "recency"),
]
NAME = {k: n for k, n, _ in MODELS}
CLASS = {k: c for k, _, c in MODELS}
OPEN_WEIGHT = [k for k, _, c in MODELS if c in ("open", "recency")]   # the ten open-weight models

# Scatter positions per arm: {model key: (d_c, d_u)}. A model missing from an arm has no data there; the scatter
# fades it out rather than interpolating or parking it.
POS = {
    "A": {  # Table 7
        "sonnet": (0.89, 0.84), "sol": (0.51, 0.46), "gemini": (0.58, 0.42), "haiku": (0.01, -0.01),
        "luna": (0.02, 0.08),
        "gemma": (0.34, 0.00), "ministral8": (0.28, -0.10), "qwen35": (0.10, 0.06), "ministral14": (0.29, -0.03),
        "llama33": (0.50, -0.09), "dsv32": (0.08, 0.00),
        "dsv41": (0.59, 0.09), "qwen38": (0.03, 0.00), "maverick": (0.68, -0.06), "mmed": (0.48, 0.14),
    },
    "B": {  # Table 2
        "gemma": (0.18, 0.05), "ministral8": (0.09, 0.04), "qwen35": (0.04, 0.06), "ministral14": (-0.04, 0.05),
        "llama33": (0.13, 0.18), "dsv32": (0.01, 0.01),
        "luna": (0.01, 0.13), "sol": (0.55, 0.49), "haiku": (-0.01, 0.00), "sonnet": (0.68, 0.63),
        "dsv41": (0.51, 0.24), "maverick": (0.13, 0.20), "mmed": (0.33, 0.15),
    },
    "R": {  # arm_r_vs_a.md section 1, arm R rows
        "gemma": (0.013, 0.000), "llama33": (0.037, 0.200), "maverick": (0.025, 0.163),
        "ministral8": (-0.200, 0.113), "sol": (0.463, 0.475), "sonnet": (0.775, 0.750),
    },
    "S": {  # arm_s.md section 1
        "gemma": (0.138, 0.000), "ministral8": (0.062, 0.025), "llama33": (0.250, 0.087),
        "maverick": (0.287, 0.075), "sol": (0.475, 0.400),
    },
}

# D = d_c - d_u as printed in Table 7 (strings, Unicode minus). Arm S column is D_bal.
D_STR = {
    "A": {"sonnet": "0.05", "sol": "0.05", "gemma": "0.34", "ministral8": "0.38", "llama33": "0.59",
          "maverick": "0.74"},
    "R": {"sonnet": "0.03", "sol": "−0.01", "gemma": "0.01", "ministral8": "−0.31", "llama33": "−0.16",
          "maverick": "−0.14"},
    "S_bal": {"sol": "0.08", "gemma": "0.11", "ministral8": "0.02", "llama33": "0.16", "maverick": "0.23"},
}

# Practice log (harness/design.py BASE): voice of each of the eight entries in arm A display order.
LOG_VOICES = ["certain", "unsure", "certain", "unsure", "unsure", "certain", "certain", "unsure"]
LOG_CONDITIONS = {
    # hit (1 = right) per entry, derived from the voice: certain-is-right, unsure-is-right, mixed perfect
    "certain_right": [1 if v == "certain" else 0 for v in LOG_VOICES],
    "unsure_right": [1 if v == "unsure" else 0 for v in LOG_VOICES],
    "perfect_mixed": [1] * 8,
}

# Scene 6, left panel: unsure-objection switch rate, arm A, by log (arm_r_vs_a.md section 1, arm A rows):
# u|UR (overall 4 of 8, unsure 4 of 4) and u|PM (overall 8 of 8, unsure 4 of 4). Bar heights only.
C3_CELLS = {
    "gemma": (0.000, 0.475), "llama33": (0.312, 0.750), "maverick": (0.037, 0.487), "ministral8": (0.037, 0.287),
}
# Scene 6, right panel: no-log flips out of 80 (the script's example: Gemma 25 vs 7 of 80; tone gap 0.23 in Table 7).
TONE_NOLOG = {"gemma": (25, 7, 80)}

# Scene 7: correct answers abandoned with a favourable log (script / report).
ABANDON = {"sonnet_instant": (105, 160), "sonnet_reasoned": (8, 160), "sol_max_per_cell": (2, 40)}
