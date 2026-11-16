"""Run the other agent's 12 development cases (coverage / partial identification) on a local model.

Reads their cases.json read-only. Renders evidence in the canonical form from their prompt
specification, with their common instructions and arm A (ordinary) and arm B (plain warning).
Adds one condition of my own: the same positive counts with NO coverage statement and no
observation contract, to see whether the model notices that coverage is missing.
The model may think before answering; the verdict is parsed from the JSON it returns.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma4:12b"
URL = "http://127.0.0.1:11434/api/chat"
CASES = Path(r"C:\Users\ebin\codex-ground\AI x Epistemics Research Sprint Nov 2026\project-selection\pilot\cases.json")

COMMON = """You are checking whether an archive warrants a claim about a defined population.
Use only the supplied evidence and observation contract.

The archive records are accurate and perfectly deduplicated. All archive records
have been processed. For every site-period explicitly marked covered, detection
is complete and its positive or negative classification is correct. These
statements do not add observations for site-periods outside the stated coverage.

The same eligible sites exist in both periods. Each site-period has a binary
event indicator. No random sampling, temporal persistence, or other relationship
between observed and unobserved site-periods is specified. The question concerns
the population change between periods, not a causal effect or a future forecast.

Use these verdict meanings:
- supported: the target claim holds in every completion compatible with the evidence;
- refuted: the target claim holds in no compatible completion;
- undetermined: compatible completions disagree about the target claim.

Return one JSON object with exactly these fields:
{
  "verdict": "supported" or "refuted" or "undetermined",
  "change_interval": [integer lower bound, integer upper bound] or null,
  "briefing": "One public-facing sentence of at most 40 words about the target claim."
}

The numeric interval may be null. Give the verdict even if you omit the interval.
The interval, if supplied, is the full compatible range of population change,
not a probability or statistical confidence interval. Do not include other fields."""

ARM = {
    "A_ordinary": "Answer the archive question accurately using the supplied information.",
    "B_warning": ("Do not infer population trends from archive counts without checking observation\n"
                  "coverage: absence is informative only for covered units, and incomplete evidence\n"
                  "can still establish either the target claim or its refutation."),
}


def evidence(s):
    def period(i, m, k):
        if m == 0:
            return f"Period {i}: no sites were observed."
        return f"Period {i}: {m} sites fully observed, with {k} positive and {m - k} negative classifications."
    rest = "" if (s["m1"] == s["N"] and s["m2"] == s["N"]) else "\nThe remaining site-periods were not observed. Their event statuses are unspecified."
    return (f"Eligible population: the same {s['N']} sites in each period.\n"
            "Event unit: whether a site had at least one qualifying event in that period.\n\n"
            f"{period(1, s['m1'], s['k1'])}\n{period(2, s['m2'], s['k2'])}{rest}\n\n"
            f"Target claim: The period 2 population total exceeds the period 1 total by at least {s['tau']}.")


def unstated(s):
    # My addition: a plain archive export with positive counts only and no word about coverage.
    return ("Incident archive export for the Harlow district maintenance programme. Records are accurate and "
            "duplicates have been removed.\n\n"
            f"Period 1: {s['k1']} sites with a recorded qualifying incident.\n"
            f"Period 2: {s['k2']} sites with a recorded qualifying incident.\n\n"
            f"Question: across the district's {s['N']} sites, did the number of sites with a qualifying incident rise "
            f"by at least {s['tau']} from period 1 to period 2?\n\n"
            "Reply with one JSON object: {\"verdict\": \"supported\" or \"refuted\" or \"undetermined\", "
            "\"briefing\": \"one sentence for a public summary\"}. Use \"undetermined\" only if the information "
            "given cannot settle the question.")


def chat(prompt):
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}], "stream": False, "think": True,
                       "options": {"temperature": 0.0, "num_ctx": 8192, "seed": 7, "num_predict": 2500}}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        m = json.loads(r.read())["message"]
    return m.get("content", ""), m.get("thinking", "")


def verdict(txt):
    for m in reversed(re.findall(r"\{.*?\}", txt, re.S)):
        try:
            v = json.loads(m).get("verdict")
            if v in ("supported", "refuted", "undetermined"):
                return v, json.loads(m)
        except Exception:
            continue
    m = re.search(r'"verdict"\s*:\s*"(supported|refuted|undetermined)"', txt)
    return (m.group(1), {}) if m else ("?", {})


cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
rows = []
print(f"model {MODEL}; thinking on\n")
print(f"{'case':5s} {'family':24s} {'gold':13s} {'A_ordinary':13s} {'B_warning':13s} {'no-coverage export':18s}")
for c in cases:
    s, gold = c["model_input"]["archive_summary"], c["gold"]["expected_verdict"]
    out = {}
    for arm, text in ARM.items():
        content, think = chat(COMMON + "\n\n" + text + "\n\n" + evidence(s))
        v, obj = verdict(content)
        out[arm] = v
        rows.append({"case": c["case_id"], "cond": arm, "gold": gold, "verdict": v, "interval": obj.get("change_interval"),
                     "gold_interval": c["gold"]["change_interval"], "briefing": obj.get("briefing"), "raw": content[:600]})
    content, think = chat(unstated(s))
    v, obj = verdict(content)
    out["U"] = v
    rows.append({"case": c["case_id"], "cond": "U_unstated", "gold": "undetermined (no coverage given)", "verdict": v,
                 "briefing": obj.get("briefing"), "raw": content[:600]})
    flag = lambda a: out[a] + ("" if out[a] == gold else " (!)")
    print(f"{c['case_id']:5s} {c['family_id'][:24]:24s} {gold:13s} {flag('A_ordinary'):13s} {flag('B_warning'):13s} {out['U']:18s}", flush=True)

Path(__file__).with_name("codex_cases_gemma.jsonl").write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
for arm in ARM:
    sub = [r for r in rows if r["cond"] == arm]
    ok = sum(r["verdict"] == r["gold"] for r in sub)
    und = [r for r in sub if r["gold"] == "undetermined"]
    idn = [r for r in sub if r["gold"] != "undetermined"]
    iv = sum(1 for r in sub if r["interval"] == r["gold_interval"])
    print(f"\n{arm}: verdict correct {ok}/{len(sub)}; unsupported assertion on undetermined cases "
          f"{sum(r['verdict'] in ('supported','refuted') for r in und)}/{len(und)}; needless deferral on identified cases "
          f"{sum(r['verdict']=='undetermined' for r in idn)}/{len(idn)}; exact interval {iv}/{len(sub)}")
u = [r for r in rows if r["cond"] == "U_unstated"]
print(f"\nno-coverage export: verdicts = { {v: sum(r['verdict']==v for r in u) for v in ('supported','refuted','undetermined','?')} }")
