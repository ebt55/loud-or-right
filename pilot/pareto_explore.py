"""First look at PARETO: what the ratings and free-text comments can support. Read-only on the data."""
import re, sys
from pathlib import Path
import numpy as np
import pandas as pd

root = Path(sys.argv[1])
lk = pd.read_csv(root / "survey_data" / "likert-responses.csv")
ft = pd.read_csv(root / "survey_data" / "free_text_responses.csv")
print("likert rows", len(lk), "| unique responses", lk.qid.nunique(), "| respondents", lk.respondent_id.nunique())
print("model x model_stance:\n", lk.drop_duplicates("qid").groupby(["model", "model_stance"]).size().to_string())
print("\nmodel_stance_side:", lk.drop_duplicates("qid").model_stance_side.value_counts().to_dict())
print("user_stance_side:", lk.drop_duplicates(["qid", "respondent_id"]).user_stance_side.value_counts().to_dict())
print("user_answer values:", lk.user_answer.value_counts().to_dict())

wide = lk.pivot_table(index=["qid", "issue", "model", "model_stance", "model_stance_side", "question_id", "respondent_id", "user_stance_side"],
                      columns="likert", values="user_score", aggfunc="first").reset_index()
wide = wide.merge(ft, on=["qid", "respondent_id"], how="left")
print("\nrating rows (response x respondent):", len(wide), "| with free text:", wide.free_text.notna().sum())
print("ratings per response: mean %.1f, min %d, max %d" % tuple(wide.groupby("qid").size().agg(["mean", "min", "max"])))
print("ratings per response per side:\n", wide.groupby(["qid", "user_stance_side"]).size().groupby("user_stance_side").describe()[["mean", "min", "max"]].to_string())

def rel(r):
    if r.model_stance_side not in ("liberal", "conservative"):
        return r.model_stance_side
    return "congruent" if r.model_stance_side == r.user_stance_side else "opposed"
wide["relation"] = wide.apply(rel, axis=1)
print("\nmean approval (likert_2 score 0-1) by relation of response to rater:")
print(wide.groupby("relation").likert_2.agg(["mean", "count"]).round(3).to_string())
print("\nmean approval by model_stance x rater side:")
print(wide.pivot_table(index="model_stance", columns="user_stance_side", values="likert_2", aggfunc="mean").round(3).to_string())

txt = wide.free_text.fillna("").str.lower()
NEG = r"\b(false|falsehood\w*|untrue|inaccura\w*|incorrect\w*|mislead\w*|misinform\w*|disinform\w*|lies|lie|lying|liar|not true|not accurate|not factual|wrong|propaganda|cherry[- ]?pick\w*|made[- ]up|fabricat\w*|distort\w*|myth\w*|debunk\w*|no evidence|without evidence|unsupported|unsubstantiated)\b"
POS = r"\b(accurate\w*|factual\w*|facts?|truth\w*|true|correct\w*|evidence|statistic\w*|data|sources?|cit(?:e|es|ed|ation\w*)|studies|study|research)\b"
wide["acc_neg"] = txt.str.contains(NEG, regex=True)
wide["acc_pos"] = txt.str.contains(POS, regex=True) & ~wide["acc_neg"]
wide["words"] = txt.str.split().str.len()
print("\nfree text: median words %.0f; any accuracy complaint %.3f; any positive accuracy/evidence mention %.3f" % (wide.words.median(), wide.acc_neg.mean(), wide.acc_pos.mean()))
print("\naccuracy-complaint rate and positive-mention rate by relation:")
print(wide.groupby("relation")[["acc_neg", "acc_pos"]].mean().round(3).assign(n=wide.groupby("relation").size()).to_string())
print("\napproval when comment has an accuracy complaint vs not, by relation:")
print(wide.pivot_table(index="relation", columns="acc_neg", values="likert_2", aggfunc="mean").round(3).to_string())

# Do the two sides flag the same responses? Per response, complaint rate among liberal and conservative raters.
per = wide.groupby(["qid", "model_stance", "model_stance_side", "user_stance_side"]).agg(neg=("acc_neg", "mean"), appr=("likert_2", "mean"), n=("acc_neg", "size")).reset_index()
pv = per.pivot_table(index=["qid", "model_stance", "model_stance_side"], columns="user_stance_side", values=["neg", "appr", "n"]).dropna()
pv.columns = [f"{a}_{b}" for a, b in pv.columns]
pv = pv.reset_index()
print("\nresponses with raters from both sides:", len(pv))
for name, sub in [("all", pv), ("default responses", pv[pv.model_stance == "default"])] + [(s, pv[pv.model_stance == s]) for s in pv.model_stance.unique() if s != "default"]:
    if len(sub) > 20:
        c = np.corrcoef(sub.neg_liberal, sub.neg_conservative)[0, 1]
        a = np.corrcoef(sub.appr_liberal, sub.appr_conservative)[0, 1]
        print(f"  {name:20s} n={len(sub):4d}  corr(complaint rate lib, con)={c:+.3f}  corr(approval lib, con)={a:+.3f}")

# Specificity of the response text: numerals per 100 words; relate to approval within question (default models only).
resp = []
for f in (root / "model_responses").glob("*.csv"):
    d = pd.read_csv(f)
    d["file"] = f.stem
    resp.append(d[["file", "post_id", "side", "model_response", "actual_model_id"]])
resp = pd.concat(resp)
resp["n_words"] = resp.model_response.str.split().str.len()
resp["n_num"] = resp.model_response.str.count(r"\b\d[\d,\.]*%?")
resp["num_per100"] = 100 * resp.n_num / resp.n_words
print("\nresponse length and numerals by file:")
print(resp.groupby("file")[["n_words", "n_num", "num_per100"]].mean().round(2).to_string())
print("share of responses with at least one numeral:", round((resp.n_num > 0).mean(), 3))
print("\nmodel ids:", resp.groupby("file").actual_model_id.agg(lambda s: s.value_counts().index[0]).to_dict())
wide.to_pickle(Path(sys.argv[2]) / "pareto_wide.pkl")
resp.to_pickle(Path(sys.argv[2]) / "pareto_resp.pkl")
