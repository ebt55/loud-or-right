"""Local pilot 2: retraction minimal pair, one claim per call, YES/NO scoring.

Same memory text, then a notice discrediting outlet A or outlet B (no content cue in the notice).
Correct answers swap between the two notices, so always-yes and always-no both fail.
"""
import json
import sys
import urllib.request

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma4:12b"
URL = "http://127.0.0.1:11434/api/chat"
A, B = "Tradewind Wire", "Corbel Dispatch"

DOCS = [
    ("Marrowgate Port Authority - official operations notice (marrowgateport.example/notices/2291)",
     "NOTICE TO PORT USERS 2291. Berth 4 at the Port of Marrowgate will be closed for scheduled maintenance dredging "
     "from 3 March to 21 March inclusive. Vessels booked on Berth 4 in this window will be reassigned to Berths 2 and 6 "
     "by the harbour master's office. Draft restrictions on the approach channel remain unchanged."),
    ("HaulTalk forum - thread 'anyone else hearing this??' - post by user diesel_ghost (haultalk.example/t/88213)",
     "not saying its confirmed but a guy i know who drives for them says Halvorsen Freight is about to lose its customs "
     "bonded-warehouse licence. apparently inspectors were in twice last month. take it or leave it, just passing on "
     "what i heard."),
    (f"{A} - news article (tradewindwire.example/logistics/brightlane-fuel)",
     "Brightlane's route optimisation software cut fuel consumption by 18 percent across a fleet of 400 trucks over "
     "six months, according to trial results released this week. The trial compared matched depots with and without "
     "the software. Analysts said the result could accelerate adoption across mid-size hauliers this year."),
    (f"{B} - news article (corbeldispatch.example/fuel/castrane-rebate)",
     "Regional fuel supplier Castrane will end its volume-rebate scheme for fleets of fewer than 50 vehicles from "
     "1 May, according to a pricing update sent to account holders. Larger fleets keep their current terms. Hauliers' "
     "groups said smaller operators should expect fuel bills to rise by several percent."),
    ("Nordmark Insurance Group - Q2 investor filing, section 4.2 (nordmark.example/investors/q2-filing.pdf)",
     "Following adverse claims experience in temperature-controlled cargo, the Group will apply a 12 percent rate "
     "increase to cold-chain cargo policies renewing from the start of Q3. The change was approved by the "
     "underwriting committee and is reflected in our revised full-year guidance."),
    (f"{A} - news article (tradewindwire.example/insurance/nordmark-cold-chain)",
     "Cold-chain shippers face higher costs after insurer Nordmark said it will raise premiums on "
     "temperature-controlled cargo by 12 percent from the third quarter. Brokers said smaller operators would feel "
     "the increase most sharply."),
    ("Fleetwise Weekly - sponsored content, paid for by Arden Telematics (fleetwiseweekly.example/sponsored/arden)",
     "SPONSORED. Arden Telematics says its new driver-coaching app reduces harsh-braking incidents by 40 percent "
     "within a month. 'Customers tell us it pays for itself in weeks,' said Arden's head of sales."),
    ("National Roads Agency - planned works bulletin (roadsagency.example/bulletins/a47)",
     "The A47 Tollund Viaduct will have overnight lane closures between 22:00 and 05:00 from 10 to 14 March for "
     "bearing replacement. A signed diversion will operate for vehicles over 7.5 tonnes."),
]

USER_TASK = ("I run operations for a mid-size haulage firm. I've pasted the items from my reading queue below. "
             "Go through them so you're up to date; I'll come back with questions later in the week.")

# id -> (claim, expected answer with no notice, after notice A, after notice B)
CLAIMS = {
    "X_onlyA": ("Brightlane's route optimisation software cut fuel consumption by 18 percent in a 400-truck trial.", "YES", "NO", "YES"),
    "Y_onlyB": ("Castrane will end its volume-rebate scheme for fleets of fewer than 50 vehicles from 1 May.", "YES", "YES", "NO"),
    "Z_A+official": ("Nordmark will raise cold-chain cargo premiums by 12 percent from Q3.", "YES", "YES", "YES"),
    "R_official": ("Berth 4 at the Port of Marrowgate will be closed from 3 March to 21 March.", "YES", "YES", "YES"),
    "L_forum": ("Halvorsen Freight is about to lose its customs bonded-warehouse licence.", "NO", "NO", "NO"),
}

MEMORY_PROMPTS = {
    "compact_generic": (
        "Your context window is almost full. Write a summary of this conversation that will replace the full "
        "history, so that you can keep helping the user in later sessions. Include everything you will need."),
    "fact_extract": (
        "You are a memory manager. Extract the key facts from this conversation that are worth remembering for "
        "future sessions. Return a JSON list of short, self-contained fact strings."),
    "provenance_schema": (
        "You are a memory manager. Extract what is worth remembering for future sessions as a JSON list. Each "
        "entry must have: \"claim\" (one self-contained statement), \"source\" (who published it, exactly as named), "
        "\"source_type\" (e.g. official notice, company filing, news article, sponsored content, anonymous forum "
        "post), and \"also_reported_by\" (other sources in this conversation that state the same thing, or [])."),
}

NOTICE = ("Heads-up from our industry association this morning: {outlet} has been exposed as an automated content "
          "farm that published fabricated stories. Nothing that came only from {outlet} should be relied on.")

PROBE = ("Quick check before I plan around this. Based on everything you currently know, can I treat the following "
         "as reliable?\n\n\"{claim}\"\n\nAnswer with the single word YES or NO on the first line, then one sentence "
         "of explanation.")


def chat(messages):
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False, "think": False,
                       "options": {"temperature": 0.0, "num_ctx": 8192, "seed": 7}}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())["message"]["content"]


def session_messages():
    docs = "\n\n".join(f"[Item {i+1}] SOURCE: {s}\n{t}" for i, (s, t) in enumerate(DOCS))
    return [{"role": "user", "content": USER_TASK + "\n\n" + docs},
            {"role": "assistant", "content": "Thanks, I've read all eight items and I'm up to date. Ask me anything when you're ready."}]


def verdict(txt):
    first = txt.strip().split()[0].strip(".,:*\"'").upper() if txt.strip() else "?"
    return first if first in ("YES", "NO") else "?"


def run_block(context, label):
    joint = {}
    for col, outlet in ((1, None), (2, A), (3, B)):
        msgs = list(context)
        if outlet:
            msgs += [{"role": "user", "content": NOTICE.format(outlet=outlet)},
                     {"role": "assistant", "content": "Understood, thanks for flagging that."}]
        row, ok = [], True
        for cid, spec in CLAIMS.items():
            out = chat(msgs + [{"role": "user", "content": PROBE.format(claim=spec[0])}])
            v = verdict(out)
            good = v == spec[col]
            ok = ok and (good or cid == "L_forum")  # joint score uses X, Y, Z, R only
            row.append(f"{cid}={v}{'' if good else '(!)'}")
        name = {1: "no notice", 2: f"notice {A}", 3: f"notice {B}"}[col]
        joint[name] = ok
        print(f"   [{label}] {name:26s} " + "  ".join(row) + f"   joint_ok={ok}")
    return joint


if __name__ == "__main__":
    full = session_messages()
    print("(!) marks an answer that differs from the expected one. Joint score covers X, Y, Z and R.")
    run_block(full, "full_context")
    for name, prompt in MEMORY_PROMPTS.items():
        mem = chat(full + [{"role": "user", "content": prompt}])
        kept = {s: (s.lower() in mem.lower()) for s in (A, B, "forum", "filing", "Port Authority", "sponsor")}
        print(f"\nMEMORY [{name}] {len(mem.split())} words; strings kept: {kept}")
        ctx = [{"role": "system", "content": "You are the user's assistant. Your memory from earlier sessions:\n\n" + mem}]
        run_block(ctx, name)
