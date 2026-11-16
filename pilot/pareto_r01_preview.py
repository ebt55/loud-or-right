import sys, re
import numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
wide = pd.read_pickle("pareto_wide.pkl"); resp = pd.read_pickle("pareto_resp.pkl")
print("issue slugs in the ratings file:", sorted(wide.issue.unique()))
t = resp.model_response.fillna("")
# Deterministic proxies for 'checkable empirical claims': sentences with a number, or with an evidence marker.
def sents(x): return [s for s in re.split(r"(?<=[.!?])\s+", x) if s.strip()]
NUM = re.compile(r"\b\d[\d,\.]*\s?(%|percent|million|billion|thousand)?")
EVID = re.compile(r"\b(stud(?:y|ies)|research(?:ers)?|data|survey|poll|statistic\w*|according to|report(?:s|ed)?|evidence|analysis|found that|shows? that|estimate\w*|census|bureau|cbo|cdc|fbi|pew|gallup|court ruled|ruling|amendment|act of \d{4}|in \d{4})\b", re.I)
rows = []
for f, x in zip(resp.file, t):
    ss = sents(x)
    rows.append({"file": f, "n_sent": len(ss), "num_sent": sum(bool(NUM.search(s)) for s in ss), "evid_sent": sum(bool(EVID.search(s)) for s in ss),
                 "either": sum(bool(NUM.search(s) or EVID.search(s)) for s in ss), "words": len(x.split())})
d = pd.DataFrame(rows)
d["either_per100w"] = 100 * d.either / d.words
g = d.groupby("file").agg(sentences=("n_sent", "mean"), with_number=("num_sent", "mean"), with_evidence_word=("evid_sent", "mean"),
                          either=("either", "mean"), either_per100w=("either_per100w", "mean"), zero_share=("either", lambda s: (s == 0).mean())).round(2)
print("\nper response, by condition (deterministic proxies for checkable empirical claims):")
print(g.to_string())
resp["either"] = d.either.values; resp["words"] = d.words.values
oa = resp[resp.file.isin(["openai_default", "openai_balanced"])].pivot_table(index="post_id", columns="file", values="either")
diff = oa.openai_balanced - oa.openai_default
rng = np.random.default_rng(0); bs = [diff.sample(len(diff), replace=True, random_state=int(rng.integers(1e9))).mean() for _ in range(2000)]
print("\nGPT-5.4 balanced minus default, proxy claims per response, paired over 200 questions: mean %+.3f, 95%% CI [%+.3f, %+.3f]; default mean %.2f, balanced mean %.2f"
      % (diff.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5), oa.openai_default.mean(), oa.openai_balanced.mean()))
# does the balanced answer keep fewer proxy claims than its two source drafts combined?
bal = pd.read_csv(sys.argv[1] + "/model_responses/openai_balanced.csv")
def cnt(x): return sum(bool(NUM.search(s) or EVID.search(s)) for s in sents(str(x)))
bal["drafts"] = bal.first_perspective_response.map(cnt) + bal.second_perspective_response.map(cnt); bal["final"] = bal.model_response.map(cnt)
print("balanced answers: proxy claims in the two drafts combined %.2f per question, in the final answer %.2f (drafts total %d words, final %d words on average)"
      % (bal.drafts.mean(), bal.final.mean(), (bal.first_perspective_response.str.split().str.len() + bal.second_perspective_response.str.split().str.len()).mean(), bal.model_response.str.split().str.len().mean()))
