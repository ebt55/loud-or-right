import csv, sys, json, io
from pathlib import Path
root = Path(sys.argv[1])
csv.field_size_limit(10**9)
def head(p, n=3, maxw=160):
    with open(p, encoding="utf-8", errors="replace", newline="") as f:
        r = csv.reader(f)
        hdr = next(r)
        print(f"\n== {p.name}  cols={len(hdr)}")
        print("   header:", hdr[:40])
        for i, row in enumerate(r):
            if i >= n: break
            print("   row:", [c[:maxw] for c in row[:40]])
def count(p):
    with open(p, encoding="utf-8", errors="replace", newline="") as f:
        return sum(1 for _ in csv.reader(f)) - 1
sd = root / "survey_data"
print(open(sd / "likert_questions.csv", encoding="utf-8").read())
for name in ["likert-responses.csv", "free_text_responses.csv", "participant_demographics.csv", "user_questions_provenance.csv", "valence_labels.csv"]:
    head(sd / name, 3)
    print("   rows:", count(sd / name))
for name in ["openai_balanced.csv", "openai_default.csv", "openai_support.csv", "anthropic.csv"]:
    head(root / "model_responses" / name, 1, 300)
    print("   rows:", count(root / "model_responses" / name))
print("\nanalysis:", [p.name for p in (root / "analysis").iterdir()])
print("scripts:", [p.name for p in (root / "scripts").iterdir()])
j = json.load(open(root / "stimuli_json" / "openai_balanced.json", encoding="utf-8"))
print("\nstimuli_json type:", type(j).__name__, "n:", len(j))
k = next(iter(j)) if isinstance(j, dict) else 0
print("first key:", k, "->", json.dumps(j[k])[:700])
