import re, sys
from pathlib import Path
import numpy as np
import pandas as pd
wide = pd.read_pickle("pareto_wide.pkl"); resp = pd.read_pickle("pareto_resp.pkl")
FILE2 = {"anthropic": ("claude", "default"), "gemini": ("gemini", "default"), "grok": ("grok", "default"), "llama": ("llama", "default"),
         "openai_default": ("gpt", "default"), "openai_balanced": ("gpt", "chunked"), "openai_support": ("gpt", "for"), "openai_oppose": ("gpt", "against")}
resp["model"] = resp.file.map(lambda f: FILE2[f][0]); resp["model_stance"] = resp.file.map(lambda f: FILE2[f][1])
resp = resp.rename(columns={"post_id": "question_id"})
txt = resp.model_response.str.lower()
resp["hedges"] = txt.str.count(r"\b(may|might|could|some|often|many|generally|typically|tend to|argue|argues|believe|view|views|critics|supporters|proponents|opponents|depends|debate\w*|complex)\b")
resp["hedge_per100"] = 100 * resp.hedges / resp.n_words
resp["has_num"] = resp.n_num > 0
d = wide.merge(resp[["model", "model_stance", "question_id", "n_num", "num_per100", "has_num", "hedge_per100", "n_words"]], on=["model", "model_stance", "question_id"], how="left")
print("merged rows", len(d), "missing features", d.n_num.isna().sum())
items = ["likert_1", "likert_2", "likert_3", "likert_4", "likert_5", "trust_1", "trust_2"]
names = {"likert_1": "good summary", "likert_2": "approve", "likert_3": "not biased vs me", "likert_4": "fair", "likert_5": "includes my view", "trust_1": "trust", "trust_2": "would use"}

# A. Default responses only: five models answer the same question. Within-question, within-side comparison.
dd = d[d.model_stance == "default"].copy()
resp_side = dd.groupby(["qid", "question_id", "model", "user_stance_side"]).agg(appr=("likert_2", "mean"), trust=("trust_1", "mean"), fair=("likert_4", "mean"),
            n_num=("n_num", "first"), has_num=("has_num", "first"), hedge=("hedge_per100", "first")).reset_index()
print("\nA. default responses: mean by model and rater side")
print(resp_side.pivot_table(index="model", columns="user_stance_side", values=["appr", "trust"], aggfunc="mean").round(3).to_string())
print(resp_side.groupby("model")[["n_num", "hedge"]].mean().round(2).to_string())
# min-approval per response (the balanced-approval quantity)
pr = resp_side.pivot_table(index=["qid", "question_id", "model"], columns="user_stance_side", values="appr").dropna().reset_index()
pr["min_appr"] = pr[["conservative", "liberal"]].min(axis=1); pr["gap"] = (pr.liberal - pr.conservative)
feat = resp[resp.model_stance == "default"][["question_id", "model", "n_num", "has_num", "hedge_per100", "num_per100"]]
pr = pr.merge(feat, on=["question_id", "model"])
print("\nmin approval, liberal, conservative, lib-minus-con gap by model:")
print(pr.groupby("model")[["min_appr", "liberal", "conservative", "gap"]].mean().round(3).to_string())

def within(df, y, x, group):
    a = df[[y, x, group]].dropna().copy()
    a[y] = a[y] - a.groupby(group)[y].transform("mean"); a[x] = a[x] - a.groupby(group)[x].transform("mean")
    b = (a[x] * a[y]).sum() / (a[x] ** 2).sum()
    # cluster bootstrap over groups
    gs = a[group].unique(); rng = np.random.default_rng(0); bs = []
    grp = {g: a[a[group] == g] for g in gs}
    for _ in range(400):
        s = pd.concat([grp[g] for g in rng.choice(gs, len(gs))])
        bs.append((s[x] * s[y]).sum() / (s[x] ** 2).sum())
    return b, np.percentile(bs, 2.5), np.percentile(bs, 97.5)

pr["has_num_f"] = pr.has_num.astype(float); pr["log_num"] = np.log1p(pr.n_num)
print("\nB. within-question slopes across the five default models (question fixed effects; bootstrap over questions):")
for y in ["liberal", "conservative", "min_appr"]:
    for x in ["has_num_f", "log_num", "hedge_per100"]:
        b, lo, hi = within(pr, y, x, "question_id")
        print(f"   {y:12s} ~ {x:13s}: {b:+.4f}  [{lo:+.4f}, {hi:+.4f}]")
print("\n   same, excluding Grok (is it only a Grok effect?):")
p2 = pr[pr.model != "grok"]
for y in ["liberal", "conservative", "min_appr"]:
    b, lo, hi = within(p2, y, "has_num_f", "question_id")
    print(f"   {y:12s} ~ has_num_f: {b:+.4f}  [{lo:+.4f}, {hi:+.4f}]   (responses with numerals: {int(p2.has_num.sum())} of {len(p2)})")
g = pr[pr.model == "grok"]
print("\n   within Grok only (no question FE possible), corr(log numerals, approval): liberal %.3f, conservative %.3f, min %.3f; n=%d"
      % (np.corrcoef(g.log_num, g.liberal)[0, 1], np.corrcoef(g.log_num, g.conservative)[0, 1], np.corrcoef(g.log_num, g.min_appr)[0, 1], len(g)))

# C. What do comments talk about? Simple lexicon rates by relation.
t = d.free_text.fillna("").str.lower()
LEX = {"fair/balanced/both sides": r"\b(fair\w*|balanc\w*|both sides|both perspectives|both views|neutral\w*|unbiased|even[- ]handed|objective\w*)\b",
       "bias/one-sided": r"\b(bias\w*|one[- ]sided|slant\w*|partisan|agenda|left[- ]leaning|right[- ]leaning|liberal bias|conservative bias)\b",
       "my view / agree": r"\b(i agree|agree with|my view|my opinion|my belief\w*|my position|i disagree|disagree with|i believe|i think)\b",
       "accuracy complaint": r"\b(false|falsehood\w*|untrue|inaccura\w*|incorrect\w*|mislead\w*|misinform\w*|disinform\w*|lies|lie|lying|not true|not accurate|not factual|wrong|propaganda|cherry[- ]?pick\w*|made[- ]up|fabricat\w*|distort\w*|myth\w*|no evidence|without evidence|unsupported|unsubstantiated)\b",
       "facts/evidence praise or mention": r"\b(accurate\w*|factual\w*|facts?|truth\w*|true|correct\w*|evidence|statistic\w*|data|sources?|studies|study|research)\b",
       "missing/left out": r"\b(left out|leaves out|omit\w*|ignor\w*|didn'?t mention|did not mention|fail\w* to mention|missing|lack\w*|doesn'?t address|does not address)\b"}
print("\nC. share of comments matching each theme, by relation of response to rater:")
rows = {}
for k, pat in LEX.items():
    m = t.str.contains(pat, regex=True)
    rows[k] = d.assign(m=m).groupby("relation").m.mean().round(3)
    rows[k]["ALL"] = round(m.mean(), 3)
print(pd.DataFrame(rows).T.to_string())
print("\nD. examples of accuracy complaints (opposed relation):")
ex = d[(d.relation == "opposed") & t.str.contains(LEX["accuracy complaint"], regex=True)].free_text.head(6)
for e in ex: print("   -", e[:230].replace("\n", " "))
print("\nE. examples from the 'chunked' (balanced) condition with an accuracy complaint:")
ex = d[(d.relation == "chunked") & t.str.contains(LEX["accuracy complaint"], regex=True)].free_text.head(4)
for e in ex: print("   -", e[:230].replace("\n", " "))
