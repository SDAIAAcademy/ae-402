# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Write the synthetic case data of AE-402 into labs/data/ (seed 402, same bytes on every run).

The Ministry of Municipal Services is fictional. Every person, team, model id, price and
number below is invented for the course. Run from labs/:  uv run prepare_data.py
"""

from __future__ import annotations

import csv
import io
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
REF = DATA / "reference"
SEED = 402


def write(rel: str, text: str) -> None:
    p = DATA / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def write_csv(rel: str, rows: list[dict]) -> None:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    write(rel, buf.getvalue())


def write_json(rel: str, obj) -> None:
    write(rel, json.dumps(obj, indent=1, ensure_ascii=False))


def ref(name: str, obj) -> None:
    write_json(f"reference/{name}.json", obj)


LEVELS = ["Public", "Restricted", "Secret", "Top Secret"]
ALLOWED = {"Public": ["ministry", "ksa_cloud", "external"], "Restricted": ["ministry", "ksa_cloud"],
           "Secret": ["ministry"]}


def highest(levels):
    return max(levels, key=LEVELS.index)


# ======================================================================================
# Day 1 · from requirements to architecture
# ======================================================================================

BRIEF = """
# Case brief: Muyassir, the building-permits assistant

Ministry of Municipal Services (fictional) · Digital Services Sector · brief written by Dr. Afrah Al-Dughaither,
deputy minister for digital services

## Why

The Ministry receives about 38,000 building-permit applications a year from citizens and engineering offices.
[S16] Today 34% of applications are returned for missing documents; we want that under 15%. Every return adds
about a week to the cycle.

## What we want

Muyassir answers questions about permit requirements from the building code and the permit regulations, tells
an applicant the status of their own application, and lists the documents still missing. It must be fast,
accurate and available at all times.

## What is already decided

[S17] Muyassir uses the national single sign-on that the permits portal already uses. It runs on Asas, the
Ministry's shared AI platform.

## Other notes

- [S18] The Ministry's new visual identity launches next spring.
- [S19] We expect engineering offices to use the assistant if it answers within seconds.
- [S20] Permit staff have asked whether the assistant's logs will be used to rank their performance.
"""

INTERVIEWS = {
    "sponsor_afrah.md": """
# Interview note 1 · Dr. Afrah Al-Dughaither, deputy minister for digital services (the sponsor)

Interviewer: Raneem Al-Shubaili, solution architect. Duration 40 minutes.

- [S01] "The number I report on is the median permit cycle: 21 days today. I have promised 10 days within
  18 months."
- [S02] "The permits contact line takes about 9,000 status calls a month. I want that halved."
- [S03] "Muyassir goes live on Asas. No product team signs its own model contract any more; that was a
  decision of the digital services committee."
- [S04] "Run costs for the first year are capped at SAR 1.2 million. That is the approved budget line."
- [S05] "What I do not want is to read in the press that the assistant told someone the wrong requirement."
""",
    "permits_eyad.md": """
# Interview note 2 · Eyad Al-Shuraihi, product owner of the permits team

Interviewer: Raneem Al-Shubaili. Duration 55 minutes.

- [S06] "Engineering offices should get the list of missing documents within one working day of
  submitting, not after an inspector opens the file."
- [S07] "Inspectors are worried the assistant will sound as if it approves things. Only an inspector can
  approve."
- [S08] "I think most questions are about the same 40 topics. We have not counted."
- [S09] "The permits system only offers a read interface for application status. Nothing can be written back
  through it, and the vendor will not change that this year."
- [S10] "When a fee change is announced, traffic doubles for about two weeks."
- [S11] "My team would like the staff console in dark mode."
""",
    "dpo_hadeel.md": """
# Interview note 3 · Hadeel Al-Sharhan, data management office lead and data protection officer

Interviewer: Raneem Al-Shubaili. Duration 30 minutes.

- "Most of what Muyassir reads is the building code and the regulations. Those are published."
- [S15] "So I assume the documents can go to any model the platform offers; please confirm with me which
  ones are really published."
- [S12] "Applicant files are a different matter. They hold national identity numbers, property deeds and
  site plans. Our office classified them Restricted, and they do not leave the Kingdom: not for storage,
  not for processing, not for a quick look by a model."
- [S13] "Conversation logs are personal data too. Keep them 90 days, then delete them."
- [S14] "A citizen must know they are talking to an assistant, and how to reach a person."
""",
}

STATEMENTS = [
    ("S01", "sponsor_afrah.md", "Cut the median permit cycle from 21 days to 10 within 18 months", "driver", "sponsor"),
    ("S02", "sponsor_afrah.md", "Halve the 9,000 status calls a month to the permits contact line", "driver", "sponsor"),
    ("S03", "sponsor_afrah.md", "Go live on Asas; no team signs its own model contract", "constraint", "sponsor"),
    ("S04", "sponsor_afrah.md", "First-year run costs are capped at SAR 1.2 million", "constraint", "sponsor"),
    ("S05", "sponsor_afrah.md", "No wrong requirement told to a citizen", "concern", "sponsor"),
    ("S06", "permits_eyad.md", "Missing-documents list within one working day of submission", "driver", "permits team"),
    ("S07", "permits_eyad.md", "The assistant must not sound as if it approves; only inspectors approve", "concern", "inspectors"),
    ("S08", "permits_eyad.md", "Most questions are about the same 40 topics", "assumption", "permits team"),
    ("S09", "permits_eyad.md", "The permits system offers a read interface only, for this year", "constraint", "permits team"),
    ("S10", "permits_eyad.md", "Traffic doubles for two weeks after a fee change", "concern", "permits team"),
    ("S11", "permits_eyad.md", "Staff console in dark mode", "noise", "permits team"),
    ("S12", "dpo_hadeel.md", "Applicant files are Restricted and do not leave the Kingdom", "constraint", "data protection officer"),
    ("S13", "dpo_hadeel.md", "Conversation logs kept 90 days, then deleted", "constraint", "data protection officer"),
    ("S14", "dpo_hadeel.md", "Citizens know it is an assistant and how to reach a person", "concern", "applicants"),
    ("S15", "dpo_hadeel.md", "The regulation documents may go to any model", "assumption", "data protection officer"),
    ("S16", "brief.md", "Returns for missing documents fall from 34% to under 15%", "driver", "sponsor"),
    ("S17", "brief.md", "Use the national single sign-on of the permits portal", "constraint", "sponsor"),
    ("S18", "brief.md", "The new visual identity launches next spring", "noise", "sponsor"),
    ("S19", "brief.md", "Engineering offices will use it if it answers within seconds", "assumption", "engineering offices"),
    ("S20", "brief.md", "Staff fear the logs will be used to rank their performance", "concern", "permit staff"),
]


def day1(rng: random.Random) -> None:
    write("case/brief.md", BRIEF)
    for name, text in INTERVIEWS.items():
        write(f"case/interviews/{name}", text)
    write_csv("case/statements.csv", [{"id": i, "source": s, "text": t} for i, s, t, _, _ in STATEMENTS])
    ref("drivers_key", {i: {"kind": k, "owner": o} for i, _, _, k, o in STATEMENTS})

    # --- pilot measurements of a Muyassir prototype: 400 requests ------------------------------------
    rows = []
    types = ["requirements"] * 50 + ["status"] * 30 + ["approval"] * 12 + ["fees"] * 8
    for n in range(400):
        qt = rng.choice(types)
        lang = "ar" if rng.random() < 0.72 else "en"
        base = {"requirements": 2600, "status": 1900, "approval": 2400, "fees": 2100}[qt]
        lat = int(base * math.exp(rng.gauss(0, 0.33)))
        if n % 23 == 0:
            lat += 2600  # long-context retries: the tail
        correct = 1 if rng.random() < {"requirements": 0.94, "status": 0.97, "approval": 0.92, "fees": 0.88}[qt] else 0
        needs_human = 1 if qt == "approval" else 0
        offered = (1 if rng.random() < 0.93 else 0) if needs_human else 0
        tin = int(rng.gauss(3200, 600)) if qt != "status" else int(rng.gauss(1400, 200))
        tout = int(rng.gauss(330, 60))
        cost = round(tin / 1e6 * 6.0 + tout / 1e6 * 18.0, 5)
        rows.append({"request_id": f"P{n + 1:04d}", "question_type": qt, "lang": lang, "latency_ms": lat,
                     "correct": correct, "needs_human": needs_human, "offered_human": offered,
                     "in_tokens": tin, "out_tokens": tout, "cost_sar": cost,
                     "other_applicant_data": 1 if n == 287 else 0})
    write_csv("pilot/pilot_requests.csv", rows)

    ref("scenarios", [
        {"id": "Q1", "attribute": "answer quality", "source": "an applicant",
         "stimulus": "asks a requirements question covered by the building code",
         "environment": "normal operation", "artefact": "Muyassir",
         "response": "answers and cites the clause it used",
         "measure": {"metric": "correct", "stat": "mean", "op": ">=", "target": 0.90,
                     "where": "question_type == 'requirements'"}},
        {"id": "Q2", "attribute": "latency", "source": "an engineering office",
         "stimulus": "asks any question", "environment": "a normal working day",
         "artefact": "Muyassir through the Asas gateway", "response": "returns a complete answer",
         "measure": {"metric": "latency_ms", "stat": "p95", "op": "<=", "target": 4000, "where": ""}},
        {"id": "Q3", "attribute": "cost", "source": "the finance and cost lead",
         "stimulus": "reads the monthly showback", "environment": "base volume",
         "artefact": "Muyassir", "response": "costs no more than budgeted per answer",
         "measure": {"metric": "cost_sar", "stat": "mean", "op": "<=", "target": 0.05, "where": ""}},
        {"id": "Q4", "attribute": "privacy", "source": "an applicant",
         "stimulus": "asks about the status of an application", "environment": "normal operation",
         "artefact": "Muyassir", "response": "shows only the asker's own application",
         "measure": {"metric": "other_applicant_data", "stat": "sum", "op": "<=", "target": 0, "where": ""}},
        {"id": "Q5", "attribute": "human oversight", "source": "an applicant",
         "stimulus": "asks whether a design will be approved", "environment": "normal operation",
         "artefact": "Muyassir", "response": "says only an inspector approves and offers a person",
         "measure": {"metric": "offered_human", "stat": "mean", "op": ">=", "target": 0.99,
                     "where": "needs_human == 1"}},
    ])

    # --- data inventory and the flows of Muyassir ---------------------------------------------------
    inv = [
        ("D01", "Building code (published edition)", "permits", 0, "Public"),
        ("D02", "Permit regulations and circulars (published)", "permits", 0, "Public"),
        ("D03", "Permit fee schedule (published)", "permits", 0, "Public"),
        ("D04", "Applicant files: forms, national identity numbers", "permits", 1, "Restricted"),
        ("D05", "Property deeds and site plans attached to applications", "permits", 1, "Restricted"),
        ("D06", "Application status records", "permits", 1, "Restricted"),
        ("D07", "Muyassir conversation logs", "permits", 1, ""),
        ("D08", "Inspector notes on applications", "inspections", 1, "Restricted"),
        ("D09", "Draft circulars not yet published", "permits", 0, ""),
        ("D10", "Anonymised monthly permit statistics", "permits", 0, "Public"),
        ("D11", "Engineering office registry (names, licence numbers)", "permits", 0, "Public"),
        ("D12", "Engineering office contact persons (names, mobile numbers)", "permits", 1, ""),
        ("D13", "Citizen reports with location and phone", "reports", 1, "Restricted"),
        ("D14", "Inspection photos", "inspections", 1, "Restricted"),
        ("D15", "Waste collection routes", "waste", 0, "Public"),
        ("D16", "Zoning maps (published)", "planning", 0, "Public"),
        ("D17", "Tender documents and bids", "contracts", 0, "Secret"),
        ("D18", "Land ownership dispute files", "land", 1, "Secret"),
        ("D19", "Survey records of state land", "land", 0, "Secret"),
        ("D20", "Call-centre recordings", "contact", 1, "Restricted"),
        ("D21", "Staff HR policies", "staff", 0, "Public"),
        ("D22", "Staff leave and payroll questions", "staff", 1, "Restricted"),
        ("D23", "Asas usage logs (key, team, tokens)", "platform", 0, "Restricted"),
        ("D24", "Model evaluation results", "platform", 0, "Public"),
    ]
    write_csv("case/data_inventory.csv", [{"id": i, "item": n, "owner_team": t, "personal_data": p, "level": l}
                                          for i, n, t, p, l in inv])
    # the three blanks, classified by the rules the session teaches
    inv_key = {i: l for i, _, _, _, l in inv}
    inv_key.update({"D07": "Restricted", "D09": "Restricted", "D12": "Restricted"})
    ref("inventory_levels", inv_key)

    flows = [
        ("F01", "Applicant", "Portal", "D04;D06", "ministry", "question and identity"),
        ("F02", "Portal", "Asas gateway", "D04;D06", "ministry", "question with applicant context"),
        ("F03", "Asas gateway", "Regulations index", "D01;D02;D03", "ministry", "retrieval query"),
        ("F04", "Regulations index", "Embedding model", "D01;D02;D03", "external", "embedding of published texts"),
        ("F05", "Asas gateway", "Permits system", "D06", "ministry", "status read"),
        ("F06", "Asas gateway", "Answer model", "D01;D02;D06", "ksa_cloud", "prompt with clauses and status"),
        ("F07", "Portal", "OCR service", "D05", "external", "scanned deeds and site plans to text"),
        ("F08", "Asas gateway", "Log store", "D07", "ministry", "conversation log"),
        ("F09", "Log store", "Analytics service", "D07", "external", "weekly usage dashboard"),
        ("F10", "Permits team", "Regulations index", "D09", "ministry", "draft circulars for preview"),
        ("F11", "Asas gateway", "Answer model", "D01;D04;D05", "ksa_cloud", "missing-documents check"),
        ("F12", "Asas gateway", "Contact centre", "D06;D12", "ministry", "hand-over to a person"),
        ("F13", "Statistics job", "Open data portal", "D10", "external", "monthly statistics"),
        ("F14", "Regulations index", "Summary model", "D09", "external", "draft circulars summarised"),
    ]
    write_csv("case/muyassir_flows.csv", [{"id": i, "source": s, "target": t, "items": it, "target_hosting": h,
                                           "purpose": p} for i, s, t, it, h, p in flows])
    key = {}
    for i, _, _, it, h, _ in flows:
        lvl = highest([inv_key[x] for x in it.split(";")])
        key[i] = {"level": lvl, "allowed": ALLOWED[lvl], "violation": h not in ALLOWED[lvl]}
    ref("flows_key", key)

    # --- the model of Muyassir for views as code, and the per-hop measurements ----------------------
    model = {
        "system": {"id": "muyassir", "name": "Muyassir", "description": "Building-permits assistant on Asas"},
        "people": [
            {"id": "applicant", "name": "Applicant", "description": "Citizen or engineering office"},
            {"id": "inspector", "name": "Inspector", "description": "Reviews hand-overs and approves"},
        ],
        "external_systems": [
            {"id": "sso", "name": "National single sign-on", "hosting": "ksa_cloud"},
            {"id": "permits", "name": "Permits system", "hosting": "ministry"},
            {"id": "contact", "name": "Contact centre", "hosting": "ministry"},
        ],
        "containers": [
            {"id": "portal", "name": "Permits portal widget", "tech": "Web", "hosting": "ministry"},
            {"id": "orchestrator", "name": "Muyassir service", "tech": "Python", "hosting": "ministry"},
            {"id": "gateway", "name": "Asas gateway", "tech": "AI gateway", "hosting": "ministry"},
            {"id": "index", "name": "Regulations index", "tech": "Vector and keyword index", "hosting": "ministry"},
            {"id": "reranker", "name": "Reranker", "tech": "Cross-encoder", "hosting": "ministry"},
            {"id": "answer_model", "name": "Answer model", "tech": "ksa-general-m", "hosting": "ksa_cloud"},
            {"id": "logs", "name": "Log store", "tech": "Object store, 90-day expiry", "hosting": "ministry"},
        ],
        "relations": [
            ["applicant", "portal", "asks a question", "HTTPS"],
            ["portal", "sso", "signs the applicant in", "OIDC"],
            ["portal", "orchestrator", "sends question and applicant id", "HTTPS"],
            ["orchestrator", "permits", "reads application status", "REST, read only"],
            ["orchestrator", "index", "retrieves clauses", "HTTPS"],
            ["orchestrator", "reranker", "reranks clauses", "HTTPS"],
            ["orchestrator", "gateway", "asks for an answer", "OpenAI-compatible"],
            ["gateway", "answer_model", "routes by classification", "HTTPS"],
            ["orchestrator", "logs", "writes the conversation", "HTTPS"],
            ["orchestrator", "contact", "hands over to a person", "Events"],
            ["inspector", "contact", "takes hand-overs", "Staff console"],
        ],
    }
    write_json("case/muyassir_model.json", model)

    hops = [
        ("portal", "Portal to service", 40, 90, 0, 0, 0.0, 0.0),
        ("sso", "Token check", 15, 40, 0, 0, 0.0, 0.0),
        ("permits", "Status read", 120, 400, 0, 0, 0.0, 0.0),
        ("index", "Retrieve 20 clauses", 60, 180, 0, 0, 0.0, 0.0),
        ("reranker", "Rerank 20 to 5", 310, 650, 0, 0, 0.0, 0.0),
        ("gateway", "Gateway checks", 12, 30, 0, 0, 0.0, 0.0),
        ("answer_model", "Answer, 5 clauses in context", 1650, 2900, 3200, 330, 6.0, 18.0),
        ("logs", "Write log (asynchronous)", 8, 25, 0, 0, 0.0, 0.0),
    ]
    write_csv("case/request_hops.csv", [{"component": c, "step": s, "p50_ms": a, "p95_ms": b, "in_tokens": ti,
                                         "out_tokens": to, "sar_per_m_in": pi, "sar_per_m_out": po}
                                        for c, s, a, b, ti, to, pi, po in hops])
    sync = [h for h in hops if h[0] != "logs"]
    p95 = sum(h[3] for h in sync)
    cost = sum(h[4] / 1e6 * h[6] + h[5] / 1e6 * h[7] for h in hops)
    ref("budget", {"p95_sum_ms": p95, "p50_sum_ms": sum(h[2] for h in sync), "cost_sar": round(cost, 5),
                   "over_by_ms": p95 - 4000})

    # reference views (the same logic as the solution of Lab 1.4)
    inside = {c["id"] for c in model["containers"]}
    sid = model["system"]["id"]
    ctx = ["flowchart LR"] + [f'  {p["id"]}(["{p["name"]}"])' for p in model["people"]]
    ctx.append(f'  {sid}["{model["system"]["name"]}: {model["system"]["description"]}"]')
    ctx += [f'  {e["id"]}[("{e["name"]}")]' for e in model["external_systems"]]
    seen = set()
    for a, b, label, _ in model["relations"]:
        a2, b2 = (sid if a in inside else a), (sid if b in inside else b)
        if a2 != b2 and (a2, b2) not in seen:
            seen.add((a2, b2))
            ctx.append(f"  {a2} -->|{label}| {b2}")
    write("reference/context_view.mmd", "\n".join(ctx))
    con = ["flowchart LR"] + [f'  {p["id"]}(["{p["name"]}"])' for p in model["people"]]
    con.append(f'  subgraph {sid}["{model["system"]["name"]}"]')
    con += [f'    {c["id"]}["{c["name"]}<br/>{c["tech"]}<br/>hosting: {c["hosting"]}"]' for c in model["containers"]]
    con.append("  end")
    con += [f'  {e["id"]}[("{e["name"]}<br/>hosting: {e["hosting"]}")]' for e in model["external_systems"]]
    con += [f"  {a} -->|{label}, {proto}| {b}" for a, b, label, proto in model["relations"]]
    write("reference/container_view.mmd", "\n".join(con))


# ======================================================================================
# Day 2 · options and decisions
# ======================================================================================

NEEDS = [
    ("N1", "Answer permit questions from the building code and circulars, citing the clause", 120000, 0, "seconds",
     "one", "weekly", "retrieval"),
    ("N2", "Route each citizen report to one of six departments", 95000, 24000, "seconds", "one", "stable",
     "classical"),
    ("N3", "Summarise the inspection backlog for each district every night", 30, 0, "hours", "one", "daily",
     "batch"),
    ("N4", "Tell an applicant when the status of their application changes", 40000, 0, "minutes", "one", "live",
     "event-driven"),
    ("N5", "Pre-check a new submission: read the forms, query the permits system, list what is missing", 3200,
     0, "minutes", "several", "live", "agentic"),
    ("N6", "Draft standard inspection letters in the house style from inspector notes", 6000, 9000, "minutes",
     "one", "stable", "fine-tuned"),
]
PATTERNS = ["retrieval", "agentic", "fine-tuned", "classical", "batch", "event-driven"]

CATS = {
    "lighting": (["street light out", "lamp post not working", "dark street at night", "flickering light pole",
                  "broken street lamp"], ["إنارة الشارع مطفأة", "عمود الإنارة لا يعمل", "الشارع مظلم ليلا",
                                          "مصباح الشارع مكسور"]),
    "roads": (["pothole on the road", "cracked asphalt", "damaged pavement", "road surface broken",
               "deep hole in the street"], ["حفرة في الطريق", "تشقق في الأسفلت", "الرصيف متضرر",
                                            "هبوط في الشارع"]),
    "waste": (["garbage not collected", "overflowing bin", "rubbish on the pavement", "waste left for days",
               "container full of trash"], ["النفايات لم تجمع", "الحاوية ممتلئة", "قمامة على الرصيف",
                                            "مخلفات متراكمة"]),
    "water_leak": (["water leaking from pipe", "burst pipe in the street", "water running on the road",
                    "leak near the meter"], ["تسرب مياه من الأنبوب", "انفجار ماسورة", "مياه تجري في الشارع",
                                             "تسريب قرب العداد"]),
    "animals": (["stray dogs near school", "dead cat on the road", "stray animals in the park",
                 "dogs barking at night"], ["كلاب ضالة قرب المدرسة", "قطة نافقة في الطريق",
                                            "حيوانات سائبة في الحديقة"]),
    "parks": (["broken swing in the park", "park grass not watered", "damaged bench in garden",
               "playground unsafe"], ["أرجوحة مكسورة في الحديقة", "عشب الحديقة جاف", "مقعد متضرر في الحديقة",
                                      "ملعب الأطفال غير آمن"]),
}
PLACES_EN = ["in Al-Rawdah district", "near the mosque", "on King Road", "behind the school", "next to the market",
             "at the roundabout", "in our neighbourhood", "close to the clinic", ""]
PLACES_AR = ["في حي الروضة", "قرب المسجد", "في طريق الملك", "خلف المدرسة", "بجانب السوق", "عند الدوار", ""]
TAILS_EN = ["please fix", "since last week", "it is dangerous", "urgent", "for three days", "", "thank you"]
TAILS_AR = ["نرجو الإصلاح", "منذ أسبوع", "خطر على المارة", "عاجل", "", "شكرا"]


def options_costs(prices, forecast, volume="base", price_mult=1.0):
    """Reference three-year cost of each option (the same model the solution of Lab 2.2 writes)."""
    out = {}
    ppl = prices["person_year_sar"]
    calls = prices["call_cost_sar"] * prices["call_share_of_unanswered"]
    months = forecast
    for o in prices["options"]:
        total = 0.0
        years = {}
        for y in (1, 2, 3):
            ms = [m for m in months if m["year"] == y]
            vol = sum(m[volume] for m in ms)
            peak = max(m[volume] for m in ms)
            c = o["build_sar"] if y == 1 else 0.0
            c += o["fixed_run_sar_per_year"] + o["people_fte"] * ppl
            c += vol * (o["in_tokens"] * o["sar_per_m_in"] + o["out_tokens"] * o["sar_per_m_out"]) / 1e6 * price_mult
            if o.get("unit_capacity_per_month"):
                c += math.ceil(peak / o["unit_capacity_per_month"]) * o["unit_sar_per_year"]
            c += vol * (1 - o["coverage"]) * calls
            years[y] = c
            total += c
        out[o["id"]] = {"years": years, "total": total}
    return out


def day2(rng: random.Random) -> None:
    write_csv("options/needs.csv", [{"id": i, "need": n, "requests_per_month": v, "labelled_examples": l,
                                     "answer_needed_within": t, "steps": s, "data_changes": f}
                                    for i, n, v, l, t, s, f, _ in NEEDS])
    ref("patterns_key", {i: p for i, *_, p in NEEDS})

    # --- 3,000 citizen reports and a recorded generative run ---------------------------------------
    rows = []
    cats = list(CATS)
    for n in range(3000):
        cat = rng.choice(cats)
        ar = rng.random() < 0.6
        phrase = rng.choice(CATS[cat][1 if ar else 0])
        place = rng.choice(PLACES_AR if ar else PLACES_EN)
        tail = rng.choice(TAILS_AR if ar else TAILS_EN)
        text = " ".join(x for x in (phrase, place, tail) if x)
        if rng.random() < 0.08:  # a second issue mentioned in passing
            other = rng.choice([c for c in cats if c != cat])
            text += (" و" if ar else " and also ") + rng.choice(CATS[other][1 if ar else 0])
        label = cat if rng.random() > 0.03 else rng.choice(cats)  # 3% labelling noise
        rows.append({"id": f"R{n + 1:04d}", "lang": "ar" if ar else "en", "text": text, "category": label,
                     "split": "train" if n < 2400 else "test"})
    write_csv("options/citizen_reports.csv", rows)
    rec = []
    for r in rows[2400:]:
        ok = rng.random() < 0.885
        pred = r["category"] if ok else rng.choice([c for c in cats if c != r["category"]])
        tin = 180 + len(r["text"]) // 3
        rec.append({"id": r["id"], "predicted": pred, "latency_ms": int(rng.gauss(1350, 300)),
                    "in_tokens": tin, "out_tokens": 4})
    write_csv("options/recorded_generative_run.csv", rec)

    # --- forecast and prices --------------------------------------------------------------------------
    fc = []
    for k in range(36):
        y, m = 2027 + k // 12, k % 12 + 1
        g = k / 35
        fc.append({"month": f"{y}-{m:02d}", "year": k // 12 + 1,
                   "low": int(50000 + 70000 * g), "base": int(60000 + 240000 * g ** 1.1),
                   "high": int(70000 + 830000 * g ** 1.3)})
    write_csv("options/forecast.csv", fc)
    prices = {
        "note": "Synthetic price ranges for the case. Not vendor prices.",
        "person_year_sar": 420000, "call_cost_sar": 9.0, "call_share_of_unanswered": 0.5,
        "token_price_range": {"low": 0.5, "base": 1.0, "high": 2.0},
        "options": [
            {"id": "O1", "name": "Generative, model hosted in the Kingdom, paid per token", "build_sar": 900000,
             "fixed_run_sar_per_year": 120000, "people_fte": 2.0, "in_tokens": 3200, "out_tokens": 330,
             "sar_per_m_in": 8.0, "sar_per_m_out": 24.0, "coverage": 0.92},
            {"id": "O2", "name": "Generative, open-weight model hosted by the Ministry", "build_sar": 1400000,
             "fixed_run_sar_per_year": 60000, "people_fte": 2.5, "in_tokens": 0, "out_tokens": 0,
             "sar_per_m_in": 0.0, "sar_per_m_out": 0.0, "unit_capacity_per_month": 450000,
             "unit_sar_per_year": 200000, "coverage": 0.92},
            {"id": "O3", "name": "Non-generative: guided search and a document checklist", "build_sar": 1100000,
             "fixed_run_sar_per_year": 150000, "people_fte": 1.5, "in_tokens": 0, "out_tokens": 0,
             "sar_per_m_in": 0.0, "sar_per_m_out": 0.0, "coverage": 0.70},
        ],
    }
    write_json("options/prices.json", prices)
    base = options_costs(prices, fc)
    tornado = {}
    for o in ("O1", "O2", "O3"):
        tornado[o] = {
            "volume_low": options_costs(prices, fc, "low")[o]["total"],
            "volume_high": options_costs(prices, fc, "high")[o]["total"],
            "price_low": options_costs(prices, fc, "base", 0.5)[o]["total"],
            "price_high": options_costs(prices, fc, "base", 2.0)[o]["total"],
        }
    both = options_costs(prices, fc, "high", 2.0)
    ref("three_year_cost", {"base": {k: round(v["total"]) for k, v in base.items()},
                            "base_years": {k: {y: round(c) for y, c in v["years"].items()} for k, v in base.items()},
                            "tornado": {k: {s: round(x) for s, x in v.items()} for k, v in tornado.items()},
                            "high_volume_high_price": {k: round(v["total"]) for k, v in both.items()}})

    # --- exit factors and weighted criteria ---------------------------------------------------------------
    exits = [
        ("O1", "Prompts and tool definitions in the provider's own format", 2.0, 0),
        ("O1", "Answers indexed in the provider's managed vector store, no bulk export", 6.0, 40000),
        ("O1", "Twelve-month minimum term, early-exit fee", 0.5, 150000),
        ("O1", "Evaluation set and results kept by the provider's console", 1.5, 0),
        ("O2", "Open-weight model swapped for another open-weight model", 2.0, 0),
        ("O2", "Index in the Ministry's own store, open formats", 0.5, 0),
        ("O2", "Accelerator servers resold or redeployed", 1.0, 200000),
        ("O3", "Rules written in a vendor's rule language", 8.0, 0),
        ("O3", "Search licence with a six-month notice", 0.5, 60000),
    ]
    write_csv("options/exit_factors.csv", [{"option": o, "factor": f, "person_months": pm, "fees_sar": fee}
                                           for o, f, pm, fee in exits])
    rate = 35000
    exit_cost = {}
    for o, _, pm, fee in exits:
        exit_cost[o] = exit_cost.get(o, 0) + pm * rate + fee
    ref("exit_cost", exit_cost)
    criteria = {
        "note": "Scores from 1 (worst) to 5 (best). The exit-cost score is yours to fill from the exit cost.",
        "weights": {"answer_coverage": 0.30, "three_year_cost": 0.25, "time_to_live": 0.20,
                    "data_placement": 0.15, "exit_cost": 0.10},
        "scores": {
            "O1": {"answer_coverage": 5, "three_year_cost": 4, "time_to_live": 5, "data_placement": 4},
            "O2": {"answer_coverage": 5, "three_year_cost": 3, "time_to_live": 3, "data_placement": 5},
            "O3": {"answer_coverage": 2, "three_year_cost": 1, "time_to_live": 3, "data_placement": 5},
        },
        "person_month_sar": rate,
    }
    write_json("options/criteria.json", criteria)

    # --- decision records ---------------------------------------------------------------------------------
    write("decisions/template.md", """
# {number}. {title}

- Status: {proposed | accepted | superseded by ...}
- Date: {date of the decision}
- Deciders: {names and roles}

## Context and problem statement

{Two or three sentences: the situation and the question this record answers.}

## Decision drivers

- {driver or scenario, with its id: Q2, S12 ...}

## Considered options

- {option 1}
- {option 2}

## Decision outcome

Chosen option: "{option}", because {the reason, tied to the drivers}.

### Consequences

- Good, because {a positive consequence}
- Bad, because {a negative consequence, and who carries it}

## Review trigger

{A measurable condition or a date that reopens this decision: "if monthly requests exceed 700,000", "on 2027-12-31".}
""")
    write("decisions/0007-peer-cache-answers.md", """
# 7. Cache Muyassir's answers to frequent questions

- Status: accepted
- Date: 2026-10-20
- Deciders: Eyad Al-Shuraihi (permits product owner)

## Context and problem statement

Many applicants ask the same requirements questions. Every answer costs tokens and time.

## Decision drivers

- Q2 latency: p95 under 4,000 ms
- Q3 cost: under SAR 0.05 per answer

## Considered options

- No cache
- Cache answers to identical questions for 30 days

## Decision outcome

Chosen option: "Cache answers to identical questions for 30 days", because it makes repeated questions instant
and free.

### Consequences

- Good, because cached answers return in under 100 ms
- Good, because the token bill falls for frequent questions

## Review trigger

If things change.
""")
    ref("peer_record_flaws", ["no bad consequence (a cached answer outlives a new circular for up to 30 days)",
                              "the review trigger is not measurable",
                              "Q1 answer quality is not among the drivers"])


# ======================================================================================

def main() -> None:
    rng = random.Random(SEED)
    day1(rng)
    day2(random.Random(SEED + 2))
    print("wrote", sum(1 for p in DATA.rglob("*") if p.is_file()), "files under labs/data")


if __name__ == "__main__":
    main()
