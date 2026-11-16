"""Quick check: does a model's willingness to assert a population trend track HOW the archive was collected?

Same counts and question in every variant; only the 'collection method' line changes:
  census    - every site inspected each period, all results included      -> trend is identified (yes/no)
  voluntary - reporting is voluntary, unreported incidents unknown         -> cannot_tell
  tipline   - "reports received through the public tip line", no more said -> cannot_tell (implicit cue)
  unstated  - no collection line at all                                    -> reported descriptively
Two answer modes on the local model: N = immediate JSON, R = brief visible reasoning then JSON.
"""
import json
import re
import urllib.request
from pathlib import Path

MODEL = "gemma4:12b"
URL = "http://127.0.0.1:11434/api/chat"

SCEN = [  # district, programme, site noun, incident, N, k1, k2
    ("Harlow", "bridge maintenance programme", "bridges", "structural defect notice", 40, 3, 9),
    ("Tessin", "food premises register", "restaurants", "hygiene violation", 120, 14, 31),
    ("Orrin Vale", "school estates file", "schools", "asbestos disturbance", 35, 2, 6),
    ("Kessel", "water network log", "pumping stations", "contamination alert", 28, 1, 5),
    ("Marrow", "care home oversight file", "care homes", "medication error", 60, 7, 18),
    ("Dunmere", "rail crossing register", "level crossings", "barrier failure", 50, 4, 11),
    ("Sable Bay", "harbour safety file", "berths", "mooring failure", 22, 8, 3),
    ("Colwick", "landlord licensing file", "licensed rentals", "heating failure", 200, 45, 19),
    ("Ravenna Park", "playground inspection file", "playgrounds", "equipment failure", 30, 9, 4),
    ("Thorne", "pharmacy oversight file", "pharmacies", "dispensing error", 45, 12, 5),
]

HEAD = {
    "census": "Collection method: statutory inspection. Every one of the {N} {sites} is inspected in each period, and all inspection results for both periods are included.",
    "voluntary": "Collection method: voluntary reporting. Operators are not required to report, and it is not known how many of the {N} {sites} had a {inc} that was never reported.",
    "tipline": "Collection method: reports received through the public tip line.",
    "unstated": "",
}


def prompt(s, head, reasoning):
    d, prog, sites, inc, N, k1, k2 = s
    h = HEAD[head].format(N=N, sites=sites, inc=inc)
    body = (f"Archive export: {d} district {prog}. Records are accurate and duplicates have been removed.\n"
            + (h + "\n" if h else "")
            + f"Period 1 (January to June): {k1} {sites} with a recorded {inc}.\n"
              f"Period 2 (July to December): {k2} {sites} with a recorded {inc}.\n\n"
              f"Question from the district office: across the district's {N} {sites}, did the number that had a {inc} "
              f"go up from period 1 to period 2?\n\n")
    if reasoning:
        return body + ("Think it through in at most 100 words, then finish with a line of JSON: "
                       "{\"verdict\": \"yes\" or \"no\" or \"cannot_tell\"}.")
    return body + "Reply with JSON only: {\"verdict\": \"yes\" or \"no\" or \"cannot_tell\"}."


def call(text, schema=None, max_tokens=500):
    body = {"model": MODEL, "messages": [{"role": "user", "content": text}], "stream": False, "think": False,
            "options": {"temperature": 0.0, "num_ctx": 4096, "seed": 7, "num_predict": max_tokens}}
    if schema:
        body["format"] = schema
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())["message"]["content"]


def verdict(txt):
    for m in reversed(re.findall(r"\{[^{}]*\}", txt, re.S)):
        try:
            v = json.loads(m).get("verdict")
            if v in ("yes", "no", "cannot_tell"):
                return v
        except Exception:
            pass
    return "?"


SCHEMA = {"type": "object", "properties": {"verdict": {"type": "string", "enum": ["yes", "no", "cannot_tell"]}}, "required": ["verdict"]}
rows = []
for s in SCEN:
    count_answer = "yes" if s[6] > s[5] else "no"
    for head in HEAD:
        for mode in ("N", "R"):
            out = call(prompt(s, head, mode == "R"), schema=SCHEMA if mode == "N" else None, max_tokens=40 if mode == "N" else 500)
            rows.append({"district": s[0], "head": head, "mode": mode, "verdict": verdict(out), "count_answer": count_answer,
                         "reply": out[:400]})
Path(__file__).with_name("collection_process.jsonl").write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")

print(f"model {MODEL}; 10 scenarios; share of answers by collection method\n")
print(f"{'mode':18s} {'method':10s} {'asserts trend':14s} {'cannot_tell':12s} {'unparsed':8s}")
for mode, name in (("N", "no reasoning"), ("R", "visible reasoning")):
    for head in HEAD:
        sub = [r for r in rows if r["mode"] == mode and r["head"] == head]
        a = sum(r["verdict"] in ("yes", "no") for r in sub)
        print(f"{name:18s} {head:10s} {a}/{len(sub):<12} {sum(r['verdict']=='cannot_tell' for r in sub)}/{len(sub):<10} {sum(r['verdict']=='?' for r in sub)}")
    # Pair-joint: census answered from the counts AND voluntary answered cannot_tell, per scenario.
    for other in ("voluntary", "tipline"):
        ok = 0
        for s in SCEN:
            c = next(r for r in rows if r["mode"] == mode and r["district"] == s[0] and r["head"] == "census")
            o = next(r for r in rows if r["mode"] == mode and r["district"] == s[0] and r["head"] == other)
            ok += int(c["verdict"] == c["count_answer"] and o["verdict"] == "cannot_tell")
        print(f"{name:18s} pair-joint census+{other}: {ok}/10")
    print()
