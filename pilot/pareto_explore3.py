import sys
import numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
wide = pd.read_pickle("pareto_wide.pkl"); resp = pd.read_pickle("pareto_resp.pkl")
t = wide.free_text.fillna("").str.lower()
ACC = r"\b(?:false|falsehood\w*|untrue|inaccura\w*|incorrect\w*|mislead\w*|misinform\w*|disinform\w*|lies|lie|lying|not true|not accurate|not factual|wrong|propaganda|cherry[- ]?pick\w*|made[- ]up|fabricat\w*|distort\w*|myth\w*|no evidence|without evidence|unsupported|unsubstantiated)\b"
FAIR = r"\b(?:fair\w*|balanc\w*|both sides|both perspectives|both views|neutral\w*|unbiased|even[- ]handed|objective\w*)\b"
wide["acc"] = t.str.contains(ACC, regex=True); wide["fairtalk"] = t.str.contains(FAIR, regex=True)
rng = np.random.default_rng(0)
ids = wide.respondent_id.unique()
by = {k: v for k, v in wide.groupby("respondent_id")}
def boot(fn, B=300):
    out = []
    for _ in range(B):
        s = pd.concat([by[i] for i in rng.choice(ids, len(ids))])
        out.append(fn(s))
    return np.percentile(out, [2.5, 97.5])
def ratio(s):
    r = s.groupby("relation").acc.mean(); return r["opposed"] / r["congruent"]
def fa(s):
    return s.fairtalk.mean() / s.acc.mean()
print("ratings per respondent:", wide.groupby("respondent_id").size().value_counts().to_dict())
print("accuracy-complaint rate opposed/congruent ratio: %.2f, 95%% CI over respondents %s" % (ratio(wide), np.round(boot(ratio), 2)))
print("fairness-talk to accuracy-complaint ratio: %.1f, CI %s" % (fa(wide), np.round(boot(fa), 1)))
# within-rater: raters who saw both a congruent and an opposed partisan response
p = wide[wide.relation.isin(["congruent", "opposed"])]
w = p.pivot_table(index="respondent_id", columns="relation", values=["acc", "likert_2"], aggfunc="mean").dropna()
print("raters who rated both a congruent and an opposed response:", len(w))
if len(w):
    print("  within-rater: complaint rate congruent %.3f vs opposed %.3f ; approval congruent %.3f vs opposed %.3f" % (w[("acc", "congruent")].mean(), w[("acc", "opposed")].mean(), w[("likert_2", "congruent")].mean(), w[("likert_2", "opposed")].mean()))
# rater side split
print("\ncomplaint rate by rater side and relation:")
print(wide.pivot_table(index="relation", columns="user_stance_side", values="acc", aggfunc="mean").round(3).to_string())
# hedge slope without Grok
FILE2 = {"anthropic": ("claude", "default"), "gemini": ("gemini", "default"), "grok": ("grok", "default"), "llama": ("llama", "default"), "openai_default": ("gpt", "default")}
r = resp[resp.file.isin(FILE2)].copy(); r["model"] = r.file.map(lambda f: FILE2[f][0]); r = r.rename(columns={"post_id": "question_id"})
r["hedge"] = 100 * r.model_response.str.lower().str.count(r"\b(?:may|might|could|some|often|many|generally|typically|tend to|argue|argues|believe|view|views|critics|supporters|proponents|opponents|depends|debate\w*|complex)\b") / r.n_words
dd = wide[wide.model_stance == "default"].groupby(["question_id", "model", "user_stance_side"]).likert_2.mean().unstack().dropna().reset_index()
dd["min_appr"] = dd[["conservative", "liberal"]].min(axis=1)
dd = dd.merge(r[["question_id", "model", "hedge", "n_num"]], on=["question_id", "model"])
def slope(a, y, x):
    a = a[[y, x, "question_id"]].copy(); a[y] -= a.groupby("question_id")[y].transform("mean"); a[x] -= a.groupby("question_id")[x].transform("mean")
    return (a[x] * a[y]).sum() / (a[x] ** 2).sum()
for label, sub in (("all five default models", dd), ("excluding Grok", dd[dd.model != "grok"])):
    print(f"\nwithin-question slope of approval on hedges per 100 words, {label}: liberal {slope(sub,'liberal','hedge'):+.4f}, conservative {slope(sub,'conservative','hedge'):+.4f}, min {slope(sub,'min_appr','hedge'):+.4f}")
print("\nexamples: 'true but' style comments (possible perceived paltering):")
m = wide[t.str.contains(r"technically true|true,? but|accurate,? but|facts?,? but|misleading|out of context|missing context|cherry", regex=True)]
print("  count:", len(m), "share: %.4f" % (len(m) / len(wide)))
for e in m.free_text.head(8): print("   -", e[:220].replace("\n", " "))
