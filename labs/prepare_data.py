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
# Day 3 · the shared platform
# ======================================================================================

TEAMS = [
    ("T01", "permits", "Muyassir, the building-permits assistant", "Restricted", "chat;embeddings;agent_tools"),
    ("T02", "reports", "Citizen reports: routing and replies", "Restricted", "classification;chat"),
    ("T03", "inspections", "Kashif, the inspection-report assistant", "Restricted", "chat;vision"),
    ("T04", "waste", "Collection route summaries", "Public", "batch;chat"),
    ("T05", "planning", "Zoning questions assistant", "Public", "chat;embeddings"),
    ("T06", "contracts", "Contract clause review", "Secret", "chat;embeddings"),
    ("T07", "land", "Land and survey records search", "Secret", "embeddings;chat"),
    ("T08", "contact", "Call-centre call summaries", "Restricted", "speech;batch"),
    ("T09", "staff", "Staff policies assistant", "Restricted", "chat;embeddings;batch"),
]
MODELS = {"ext-frontier-l": "external", "ksa-general-m": "ksa_cloud", "ksa-vision-x": "ksa_cloud",
          "own-open-s": "ministry", "own-embed-m": "ministry", "own-speech-s": "ministry"}
PROVIDER = {"external": "External Provider", "ksa_cloud": "In-Kingdom Cloud", "ministry": "Ministry Data Centre"}
CARD = {"ext-frontier-l": (10.0, 40.0), "ksa-general-m": (8.0, 24.0), "ksa-vision-x": (12.0, 36.0)}
OWN_FIXED_PER_MONTH = 60000.0
USAGE = [  # team, key, capability, model, daily requests, in tokens, out tokens
    ("T01", "k-t01-a", "chat", "ksa-general-m", 3000, 3200, 330),
    ("T01", "k-t01-a", "embeddings", "own-embed-m", 3500, 60, 0),
    ("T02", "k-t02-a", "chat", "ext-frontier-l", 900, 900, 250),
    ("T02", "k-t02-a", "classification", "ksa-general-m", 3000, 200, 5),
    ("T03", "k-t03-a", "chat", "ksa-general-m", 600, 2500, 700),
    ("T03", "k-t03-b", "vision", "ksa-vision-x", 400, 1800, 300),
    ("T04", "k-t04-a", "batch", "own-open-s", 30, 9000, 1200),
    ("T05", "k-t05-a", "chat", "ext-frontier-l", 2500, 2500, 600),
    ("T05", "k-t05-a", "embeddings", "own-embed-m", 2600, 50, 0),
    ("T06", "k-t06-a", "chat", "own-open-s", 300, 6000, 900),
    ("T06", "k-t06-a", "embeddings", "own-embed-m", 800, 400, 0),
    ("T07", "k-t07-a", "embeddings", "own-embed-m", 1200, 120, 0),
    ("T07", "k-t07-a", "chat", "own-open-s", 150, 3000, 500),
    ("T08", "k-t08-a", "speech", "own-speech-s", 1500, 3000, 600),
    ("T08", "k-t08-b", "batch", "own-open-s", 1500, 2200, 250),
    ("T09", "k-t09-a", "chat", "ksa-general-m", 700, 2000, 300),
    ("T09", "k-t09-a", "embeddings", "own-embed-m", 750, 50, 0),
    ("", "k-legacy-01", "chat", "ksa-general-m", 120, 2500, 300),
]


def day3(rng: random.Random) -> None:
    write_csv("platform/teams.csv", [{"team": t, "name": n, "product": p, "max_level": l, "survey_wants": w}
                                     for t, n, p, l, w in TEAMS])
    keys = sorted({(t, k) for t, k, *_ in USAGE})
    write_csv("platform/keys.csv", [{"key_id": k, "team": t} for t, k in keys if t] +
              [{"key_id": "k-legacy-01", "team": ""}])

    start, days = date(2026, 5, 1), 184
    rows = []
    for d in range(days):
        day = start + timedelta(days=d)
        weekend = day.weekday() in (4, 5)
        growth = 1 + 0.05 * (d / 30.5)
        for t, k, cap, model, req, tin, tout in USAGE:
            m = model
            if t == "T02" and cap == "chat" and day >= date(2026, 7, 1):
                m = "ksa-general-m"  # moved after the gateway rule; May and June went external
            n = req * growth * (0.4 if weekend else 1.0) * rng.uniform(0.85, 1.15)
            if t == "T03" and cap == "chat" and day == date(2026, 9, 14):
                n *= 8  # the runaway agent
            n = max(1, int(n))
            tag = t
            if t and rng.random() < 0.04:
                tag = ""  # tag forgotten on this batch of calls
            rows.append({"date": day.isoformat(), "key_id": k, "team_tag": tag, "model": m, "capability": cap,
                         "requests": n, "in_tokens": int(n * tin * rng.uniform(0.95, 1.05)),
                         "out_tokens": int(n * tout * rng.uniform(0.95, 1.05))})
    write_csv("platform/usage.csv", rows)

    # --- invoices: the provider's prices, not the platform's price card -----------------------------------
    inv = []
    months = sorted({r["date"][:7] for r in rows})
    for mo in months:
        mrows = [r for r in rows if r["date"].startswith(mo)]
        for model, (pin, pout) in CARD.items():
            if model == "ext-frontier-l" and mo >= "2026-09":
                pout = 32.0  # the provider cut its output price; the price card was not updated
            tin = sum(r["in_tokens"] for r in mrows if r["model"] == model)
            tout = sum(r["out_tokens"] for r in mrows if r["model"] == model)
            inv.append({"provider": PROVIDER[MODELS[model]], "month": mo, "line": f"{model} input tokens",
                        "model": model, "amount_sar": round(tin * pin / 1e6, 2)})
            inv.append({"provider": PROVIDER[MODELS[model]], "month": mo, "line": f"{model} output tokens",
                        "model": model, "amount_sar": round(tout * pout / 1e6, 2)})
        if mo == "2026-08":
            inv.append({"provider": "In-Kingdom Cloud", "month": mo, "line": "onboarding credit", "model": "",
                        "amount_sar": -500.0})
        inv.append({"provider": "Ministry Data Centre", "month": mo, "line": "accelerator servers and operations",
                    "model": "own-*", "amount_sar": OWN_FIXED_PER_MONTH})
    write_csv("platform/invoices.csv", inv)
    write_json("platform/price_card.json", {
        "note": "The Asas price card, SAR per million tokens, last updated 2026-05-01. Ministry-hosted models "
                "carry no token price: their fixed monthly cost is shared by token volume.",
        "per_million": {m: {"in": p[0], "out": p[1]} for m, p in CARD.items()},
        "ministry_fixed_per_month": OWN_FIXED_PER_MONTH})

    # reference: correct allocation of each invoice by usage share, team by key
    key_team = {k: t for t, k in keys}
    alloc = {}
    unalloc = 0.0
    for line in inv:
        mo, amt = line["month"], line["amount_sar"]
        mrows = [r for r in rows if r["date"].startswith(mo)]
        if line["model"] == "own-*":
            sel = [r for r in mrows if MODELS[r["model"]] == "ministry"]
            w = [r["in_tokens"] + r["out_tokens"] for r in sel]
        elif line["model"] == "":
            sel = [r for r in mrows if MODELS[r["model"]] == "ksa_cloud"]
            w = [r["in_tokens"] * CARD[r["model"]][0] + r["out_tokens"] * CARD[r["model"]][1] for r in sel]
        else:
            sel = [r for r in mrows if r["model"] == line["model"]]
            w = [r["in_tokens"] if line["line"].endswith("input tokens") else r["out_tokens"] for r in sel]
        tot = sum(w)
        for r, x in zip(sel, w):
            share = amt * x / tot if tot else 0.0
            team = key_team.get(r["key_id"], "")
            if team:
                alloc[team] = alloc.get(team, 0.0) + share
            else:
                unalloc += share
    invoice_total = sum(l["amount_sar"] for l in inv)
    untagged_known = sum(1 for r in rows if r["team_tag"] == "" and r["key_id"] != "k-legacy-01")
    ref("showback", {"by_team": {k: round(v, 2) for k, v in sorted(alloc.items())},
                     "unallocated_legacy_key": round(unalloc, 2), "invoice_total": round(invoice_total, 2),
                     "untagged_rows_with_known_key": untagged_known})

    # demand matrix reference
    used = {}
    for r in rows:
        t = key_team.get(r["key_id"], "")
        if t:
            used.setdefault(r["capability"], set()).add(t)
    wants = {}
    for t, _, _, _, w in TEAMS:
        for c in w.split(";"):
            wants.setdefault(c, set()).add(t)
    demand = {c: sorted(used.get(c, set()) | wants.get(c, set())) for c in sorted(set(used) | set(wants))}
    ref("demand", {c: len(v) for c, v in demand.items()})
    t02_ext = sum(r["requests"] for r in rows if r["key_id"] == "k-t02-a" and r["model"] == "ext-frontier-l")
    ref("placement_breach", {"team": "T02", "model": "ext-frontier-l", "requests": t02_ext})

    # --- model candidates for admission -------------------------------------------------------------------
    cands = [
        {"id": "ext-frontier-l", "capability": "chat", "hosting": "external", "licence": "commercial API terms",
         "licence_allows_government_production": True, "eval": {"ar": 0.91, "en": 0.93}, "retention_days": 30,
         "trains_on_prompts": False, "owner": "Faris Al-Hothali"},
        {"id": "ksa-general-m", "capability": "chat", "hosting": "ksa_cloud", "licence": "commercial API terms",
         "licence_allows_government_production": True, "eval": {"ar": 0.86, "en": 0.88}, "retention_days": 0,
         "trains_on_prompts": False, "owner": "Faris Al-Hothali"},
        {"id": "own-open-s", "capability": "chat", "hosting": "ministry", "licence": "permissive open-weight licence",
         "licence_allows_government_production": True, "eval": {"ar": 0.79, "en": 0.82}, "retention_days": 0,
         "trains_on_prompts": False, "owner": "Faris Al-Hothali"},
        {"id": "own-embed-m", "capability": "embeddings", "hosting": "ministry",
         "licence": "permissive open-weight licence", "licence_allows_government_production": True,
         "eval": {"ar": 0.88, "en": 0.90}, "retention_days": 0, "trains_on_prompts": False,
         "owner": "Faris Al-Hothali"},
        {"id": "ext-mini-r", "capability": "chat", "hosting": "external", "licence": "research use only",
         "licence_allows_government_production": False, "eval": {"ar": 0.84, "en": 0.89}, "retention_days": 30,
         "trains_on_prompts": False, "owner": "Faris Al-Hothali"},
        {"id": "ksa-vision-x", "capability": "vision", "hosting": "ksa_cloud", "licence": "commercial API terms",
         "licence_allows_government_production": True, "eval": {"ar": None, "en": 0.81}, "retention_days": 0,
         "trains_on_prompts": False, "owner": "Rabah Al-Mujil"},
    ]
    write_json("platform/model_candidates.json", {
        "note": "Fictional model ids. 'eval' is the score on the Ministry's own Arabic and English evaluation sets "
                "(answer correctness for chat, recall at 5 for embeddings, defect detection for vision); null "
                "means no evidence was submitted.",
        "thresholds": {"chat": 0.75, "embeddings": 0.80, "vision": 0.80}, "candidates": cands})
    ref("admission", {"admitted": ["ext-frontier-l", "ksa-general-m", "own-open-s", "own-embed-m"],
                      "rejected": {"ext-mini-r": "licence", "ksa-vision-x": "no Arabic evaluation evidence"}})
    write_json("platform/gateway_tests.json", [
        {"id": "G1", "key": "k-t05-a", "model": "ext-frontier-l", "declared": "Public",
         "text": "Which zoning class allows a two-storey shop on a main road?", "expect": 200},
        {"id": "G2", "key": "k-t01-a", "model": "ext-frontier-l", "declared": "Restricted",
         "text": "Summarise application 2026-4471 with the attached deed.", "expect": 403},
        {"id": "G3", "key": "k-t01-a", "model": "ext-frontier-l", "declared": None,
         "text": "List the missing documents for this applicant.", "expect": 403},
        {"id": "G4", "key": "k-t05-a", "model": "ext-frontier-l", "declared": "Public",
         "text": "Owner 1048837265 asks whether plot 17 can be rezoned.", "expect": 403},
        {"id": "G5", "key": "k-t01-a", "model": "ksa-general-m", "declared": "Restricted",
         "text": "Summarise application 2026-4471 with the attached deed.", "expect": 200},
        {"id": "G6", "key": "k-t06-a", "model": "ksa-general-m", "declared": None,
         "text": "Compare clause 9 of the two bids for tender 31.", "expect": 403},
        {"id": "G7", "key": "k-t06-a", "model": "own-open-s", "declared": None,
         "text": "Compare clause 9 of the two bids for tender 31.", "expect": 200},
        {"id": "G8", "key": "k-t09-a", "model": "ext-frontier-l", "declared": "Public",
         "text": "Rewrite the published leave policy in plain Arabic.", "expect": 200},
        {"id": "G9", "key": "k-unknown", "model": "ksa-general-m", "declared": "Public",
         "text": "Hello", "expect": 401},
    ])


# ======================================================================================
# Day 4 · reference designs and reviews
# ======================================================================================

PERMITS_DOCS = {
    "P01-documents": ("Documents for a building permit",
                      "An application for a building permit needs the title deed, the site plan, the architectural "
                      "drawings stamped by a licensed engineering office and the owner's national identity."),
    "P02-fees": ("Permit fees",
                 "The permit fee is charged per square metre of built area. Residential buildings pay a lower fee "
                 "than commercial buildings. Fees are paid online before the permit is issued."),
    "P03-timelines": ("How long a permit takes",
                      "A complete residential application is decided within ten working days. Commercial "
                      "applications take up to twenty working days. Missing documents stop the clock."),
    "P04-setbacks": ("Setback rules",
                     "Buildings keep a setback of two metres from side boundaries and four metres from the street. "
                     "Corner plots keep the street setback on both street sides."),
    "P05-renovation": ("Renovation without a permit",
                       "Interior renovation that does not touch structure, facade or services needs no permit. "
                       "Changing the facade, adding a floor or moving load-bearing walls needs one."),
    "P06-appeals": ("Appealing a refusal",
                    "An applicant may appeal a refused permit within thirty days. The appeal is reviewed by a "
                    "committee that did not take the first decision."),
    "P07-engineering-office": ("Engineering office certificate",
                               "Drawings must be stamped by an engineering office licensed by the Saudi Council of "
                               "Engineers. The office certifies that the design follows the building code."),
    "P08-demolition": ("Demolition permits",
                       "Demolition needs its own permit, a safety plan and a contractor licensed for demolition. "
                       "Neighbours are notified seven days before work starts."),
}
PERMITS_EVAL = [
    ("Which documents do I need for a building permit?", "P01-documents"),
    ("How is the permit fee calculated per square metre?", "P02-fees"),
    ("How many working days until a residential application is decided?", "P03-timelines"),
    ("What setback from the street is required?", "P04-setbacks"),
    ("Do I need a permit to renovate the interior?", "P05-renovation"),
    ("Can I appeal a refused permit?", "P06-appeals"),
    ("Who must stamp the drawings?", "P07-engineering-office"),
    ("What does a demolition permit require?", "P08-demolition"),
    ("Adding a floor to my house: permit or not?", "P05-renovation"),
    ("My corner plot: which setbacks apply?", "P04-setbacks"),
]
INSPECTION_DOCS = {
    "K01-photos": ("Photo requirements",
                   "Each inspection report carries at least three photos: the facade, the violation and the "
                   "building number plate. Photos are taken in daylight."),
    "K02-violation-codes": ("Violation codes",
                            "Violation codes start with V. V12 is construction without a permit, V31 is a blocked "
                            "pavement, V44 is an unsafe scaffold."),
    "K03-signage": ("Shop signage",
                    "Shop signs show the licensed trade name in Arabic. A sign whose Arabic name differs from the "
                    "commercial licence is a signage violation."),
    "K04-hazards": ("Safety hazards",
                    "Open excavations, exposed wiring and unsafe scaffolds are immediate hazards. The inspector "
                    "orders the site closed until the hazard is removed."),
    "K05-report-fields": ("Report form fields",
                          "The report form records the plot number, the violation code, the inspector's finding, "
                          "the photos and the deadline given to the owner."),
    "K06-reinspection": ("Re-inspection",
                         "A violation with a deadline is re-inspected within three working days after the deadline. "
                         "A second failed inspection doubles the fine."),
}
INSPECTION_EVAL = [
    ("How many photos does an inspection report need?", "K01-photos"),
    ("What is violation code V44?", "K02-violation-codes"),
    ("The Arabic name on a shop sign differs from its licence: what is it?", "K03-signage"),
    ("Exposed wiring on a site: what does the inspector order?", "K04-hazards"),
    ("Which fields does the report form record?", "K05-report-fields"),
    ("When is a violation re-inspected after its deadline?", "K06-reinspection"),
    ("Is an unsafe scaffold an immediate hazard?", "K04-hazards"),
    ("What happens after a second failed inspection?", "K06-reinspection"),
    ("Must photos show the building number plate?", "K01-photos"),
    ("What is code V12 for construction without a permit?", "K02-violation-codes"),
]

RETRIEVAL_CORE = '''
STOP = {"a", "an", "the", "is", "are", "do", "does", "i", "my", "to", "of", "for", "what", "which", "how",
        "can", "it", "or", "not", "need", "needs", "on", "in", "must", "be", "by", "after", "and", "who", "when",
        "until", "many", "from", "with", "its", "has", "per", "that", "this", "at"}


def load_docs() -> dict[str, str]:
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted((HERE / "docs").glob("*.md"))}


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP


def retrieve(question: str, docs: dict[str, str], k: int) -> list[str]:
    q = words(question)
    return sorted(docs, key=lambda d: (-len(q & words(docs[d])), d))[:k]
'''

PERMITS_SERVICE = '''"""Muyassir's retrieval service, as the permits team wrote it for itself (synthetic).

Everything another team would change is hard-coded below. Evaluation is a script someone may run; nothing
checks the classification of the model, and nothing is traced.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVICE = "permits-rag"
TEAM = "T01"
LEVEL = "Restricted"
MODEL = "ksa-general-m"
TOP_K = 3
''' + RETRIEVAL_CORE + '''

def answer(question: str) -> dict:
    docs = load_docs()
    hits = retrieve(question, docs, TOP_K)
    first = next(l for l in docs[hits[0]].splitlines() if l and not l.startswith("#"))
    # the model call (MODEL, through the gateway) is a scripted stand-in: the first sentence of the top source
    return {"answer": first.split(". ")[0].rstrip(".") + ".", "sources": hits}
'''

PERMITS_EVAL_PY = '''"""Retrieval hit rate on the permits team's evaluation set. Run by hand: python eval.py"""
import json
from service import HERE, TOP_K, load_docs, retrieve

rows = [json.loads(l) for l in (HERE / "eval_set.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
docs = load_docs()
hits = sum(r["expected"] in retrieve(r["question"], docs, TOP_K) for r in rows)
print(f"hit rate {hits / len(rows):.2f} on {len(rows)} questions")
'''

GOLDEN_SERVICE = '''"""A retrieval service on the Asas golden path (synthetic).

Its settings live in service.json, which the template writes from the team's answers. Every answer is
traced to traces.jsonl with a hash of the question, never its text.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / "service.json").read_text(encoding="utf-8"))
''' + RETRIEVAL_CORE + '''

def _trace(question: str, span: str, **fields) -> None:
    if not CFG.get("tracing"):
        return
    rec = {"service": CFG["service_name"], "team": CFG["team"], "level": CFG["classification"], "span": span,
           "question_sha256": hashlib.sha256(question.encode("utf-8")).hexdigest()[:16], **fields}
    with open(HERE / "traces.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\\n")


def answer(question: str) -> dict:
    docs = load_docs()
    hits = retrieve(question, docs, CFG["top_k"])
    _trace(question, "retrieve", sources=hits)
    first = next(l for l in docs[hits[0]].splitlines() if l and not l.startswith("#"))
    # the model call goes to CFG["model_alias"] through the gateway; here a scripted stand-in
    _trace(question, "generate", model_alias=CFG["model_alias"])
    return {"answer": first.split(". ")[0].rstrip(".") + ".", "sources": hits}
'''

GOLDEN_CHECKS = '''"""The golden path's gates. The pipeline runs `python checks.py`; exit code 1 stops the deployment."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import service as S  # noqa: E402

# from the Asas catalogue (Lab 3.2) and the placement rule P-01 (Day 1)
HOSTING = {"ext-frontier-l": "external", "ksa-general-m": "ksa_cloud", "own-open-s": "ministry"}
ALLOWED = {"Public": {"external", "ksa_cloud", "ministry"}, "Restricted": {"ksa_cloud", "ministry"},
           "Secret": {"ministry"}}


def gate_evaluation(cfg: dict) -> tuple[str, str]:
    ev = cfg["evaluation"]
    if not ev["enabled"]:
        return "off", "switched off by the team: " + (ev.get("off_reason") or "no reason given")
    rows = [json.loads(l) for l in (HERE / "eval_set.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    docs = S.load_docs()
    score = sum(r["expected"] in S.retrieve(r["question"], docs, cfg["top_k"]) for r in rows) / len(rows)
    status = "pass" if score >= ev["min_score"] else "fail"
    return status, f"retrieval hit rate {score:.2f} against {ev['min_score']:.2f} on {len(rows)} questions"


def gate_classification(cfg: dict) -> tuple[str, str]:
    hosting = HOSTING.get(cfg["model_alias"])
    if hosting is None:
        return "fail", f"{cfg['model_alias']} is not in the catalogue"
    ok = hosting in ALLOWED[cfg["classification"]]
    return ("pass" if ok else "fail"), f"{cfg['classification']} data to {cfg['model_alias']} ({hosting})"


def gate_tracing(cfg: dict) -> tuple[str, str]:
    path = HERE / "traces.jsonl"
    before = len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
    S.answer("tracing probe from the pipeline")
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    spans = [json.loads(l) for l in lines[before:]]
    ok = ([s["span"] for s in spans] == ["retrieve", "generate"]
          and all("question" not in s and s["level"] == cfg["classification"] for s in spans))
    return ("pass" if ok else "fail"), f"{len(spans)} spans, no question text"


GATES = {"evaluation": gate_evaluation, "classification": gate_classification, "tracing": gate_tracing}


def main() -> int:
    failed = False
    for name, gate in GATES.items():
        status, why = gate(S.CFG)
        print(f"{name:15s} {status:5s} {why}")
        failed |= status == "fail"
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
'''


def design(service, team, owner, level, components, flows, pipeline, extra=None):
    d = {"service": service, "team": team, "owner": owner, "classification": level,
         "components": components, "flows": flows, "pipeline": pipeline}
    d.update(extra or {})
    return d


def day4(rng: random.Random) -> None:
    # ---- Lab 4.1: the permits team's retrieval service, the golden path's parts, Kashif's knowledge base
    base = "services/permits_rag"
    for k, (title, body) in PERMITS_DOCS.items():
        write(f"{base}/docs/{k}.md", f"# {title}\n\n{body}")
    write(f"{base}/eval_set.jsonl", "\n".join(json.dumps({"question": q, "expected": e}) for q, e in PERMITS_EVAL))
    write(f"{base}/service.py", PERMITS_SERVICE)
    write(f"{base}/eval.py", PERMITS_EVAL_PY)
    write(f"{base}/README.md", "# permits-rag (synthetic)\n\nThe permits team's retrieval service behind Muyassir. "
          "Settings are constants in `service.py`. Evaluation: `python eval.py`, by hand.")
    write("services/golden_path/service.py", GOLDEN_SERVICE)
    write("services/golden_path/checks.py", GOLDEN_CHECKS)
    write("services/golden_path/README.md.jinja",
          "# {{ service_name }}\n\nA retrieval service of team {{ team }} on the Asas golden path, generated from "
          "the template. Data: {{ classification }}. Model alias: {{ model_alias }} (through the gateway).\n\n"
          "Put the team's documents in `docs/` and its evaluation set in `eval_set.jsonl`; the pipeline runs "
          "`python checks.py`.")
    kb = "services/inspections_kb"
    for k, (title, body) in INSPECTION_DOCS.items():
        write(f"{kb}/docs/{k}.md", f"# {title}\n\n{body}")
    write(f"{kb}/eval_set.jsonl", "\n".join(json.dumps({"question": q, "expected": e}) for q, e in INSPECTION_EVAL))
    ref("golden_path", {"questions": ["service_name", "team", "classification", "model_alias", "eval_min_score",
                                      "eval_gate", "gate_off_reason"],
                        "hard_coded": ["SERVICE", "TEAM", "LEVEL", "MODEL"], "min_score_floor": 0.8})

    # ---- Lab 4.2 and 4.3: designs as data
    eval_gate = {"stage": "evaluate", "blocking": True, "min_score": 0.85, "sets": ["ar", "en"]}
    designs = {
        "permits_reference": design(
            "permits-assistant", "T01", "Eyad Al-Shuraihi", "Restricted",
            [{"id": "portal", "kind": "app", "hosting": "ministry"},
             {"id": "rag", "kind": "service", "hosting": "ministry"},
             {"id": "index", "kind": "store", "hosting": "ministry"},
             {"id": "llm", "kind": "model", "model": "ksa-general-m", "hosting": "ksa_cloud"}],
            [{"id": "F1", "from": "portal", "to": "rag", "data": "question and application", "level": "Restricted"},
             {"id": "F2", "from": "rag", "to": "index", "data": "query", "level": "Restricted"},
             {"id": "F3", "from": "rag", "to": "llm", "data": "prompt with passages", "level": "Restricted"},
             {"id": "F4", "from": "rag", "to": "portal", "data": "answer", "level": "Restricted"}],
            [{"stage": "test"}, eval_gate, {"stage": "deploy"}]),
        "zoning_public": design(
            "zoning-questions", "T05", "Planning team lead", "Public",
            [{"id": "site", "kind": "app", "hosting": "ministry"},
             {"id": "qa", "kind": "service", "hosting": "ministry"},
             {"id": "llm", "kind": "model", "model": "ext-frontier-l", "hosting": "external"}],
            [{"id": "F1", "from": "site", "to": "qa", "data": "question about published zoning", "level": "Public"},
             {"id": "F2", "from": "qa", "to": "llm", "data": "prompt with published plans", "level": "Public"}],
            [{"stage": "test"}, eval_gate, {"stage": "deploy"}]),
        "reports_triage": design(
            "reports-triage", "T02", "Reports team lead", "Restricted",
            [{"id": "app", "kind": "app", "hosting": "ministry"},
             {"id": "triage", "kind": "service", "hosting": "ministry"},
             {"id": "clf", "kind": "model", "model": "own-open-s", "hosting": "ministry"}],
            [{"id": "F1", "from": "app", "to": "triage", "data": "citizen report with phone and location",
              "level": "Restricted"},
             {"id": "F2", "from": "triage", "to": "clf", "data": "report text", "level": "Restricted"}],
            [{"stage": "test"}, {"stage": "deploy"},
             {"stage": "evaluate", "blocking": False, "min_score": 0.85, "sets": ["ar", "en"]}]),
        "staff_assistant": design(
            "staff-policies", "T09", "Staff services lead", "Restricted",
            [{"id": "intranet", "kind": "app", "hosting": "ministry"},
             {"id": "assistant", "kind": "service", "hosting": "ministry"},
             {"id": "llm", "kind": "model", "model": "ext-frontier-l", "hosting": "external"}],
            [{"id": "F1", "from": "intranet", "to": "assistant", "data": "employee question", "level": "Restricted"},
             {"id": "F2", "from": "assistant", "to": "llm", "data": "question with the employee's leave record",
              "level": "Restricted"}],
            [{"stage": "test"}, eval_gate, {"stage": "deploy"}]),
        "inspections": design(
            "kashif", "T03", "Rabah Al-Mujil", "Restricted",
            [{"id": "tablet", "kind": "app", "hosting": "ministry"},
             {"id": "kashif", "kind": "service", "hosting": "ministry"},
             {"id": "vision", "kind": "model", "model": "ksa-vision-x", "hosting": "ksa_cloud",
              "fallback": "vision_ext"},
             {"id": "vision_ext", "kind": "model", "model": "ext-vision-q", "hosting": "external"},
             {"id": "llm", "kind": "model", "model": "ksa-general-m", "hosting": "ksa_cloud"},
             {"id": "reports", "kind": "store", "hosting": "ministry"}],
            [{"id": "F1", "from": "tablet", "to": "kashif", "data": "site photos and inspector notes",
              "level": "Restricted"},
             {"id": "F2", "from": "kashif", "to": "vision", "data": "site photos", "level": "Restricted"},
             {"id": "F3", "from": "kashif", "to": "llm", "data": "notes and photo findings", "level": "Restricted"},
             {"id": "F4", "from": "kashif", "to": "reports", "data": "approved report", "level": "Restricted"},
             {"id": "F5", "from": "kashif", "to": "tablet", "data": "draft report", "level": "Restricted"}],
            [{"stage": "test"}, {"stage": "evaluate", "blocking": True, "min_score": 0.8, "sets": ["en"]},
             {"stage": "deploy"}],
            {"oversight": {"inspector_approves_every_report": True, "sample_review_pct": 10},
             "latency_budget_ms": {"p95_total": 5000, "vision_p95": 3800},
             "keys": [{"key": "k-t03-a", "used_by": ["tablet app", "nightly batch"]}],
             "photos": {"compressed_on_tablet": True, "retention_days_at_provider": 30}}),
    }
    for k, d in designs.items():
        write_json(f"designs/{k}.json", d)
    ref("fitness", {"evaluation_gate": {"permits_reference": True, "zoning_public": True, "reports_triage": False,
                                        "staff_assistant": True, "inspections": True},
                    "placement": {"permits_reference": True, "zoning_public": True, "reports_triage": True,
                                  "staff_assistant": False, "inspections": False},
                    "arabic_evaluation": {"permits_reference": True, "zoning_public": True, "reports_triage": True,
                                          "staff_assistant": True, "inspections": False}})

    # ---- Lab 4.3: the review of Kashif
    write_csv("review/scenarios.csv", [
        {"id": "Q1", "attribute": "answer quality", "importance": "H", "difficulty": "H",
         "scenario": "An inspector photographs an Arabic shop sign; Kashif's draft names the trade correctly in 90% "
                     "of the Ministry's Arabic signage set."},
        {"id": "P1", "attribute": "privacy", "importance": "H", "difficulty": "M",
         "scenario": "A photo shows faces and car plates; no copy of it is processed outside the Kingdom."},
        {"id": "S1", "attribute": "security", "importance": "H", "difficulty": "M",
         "scenario": "One client's key leaks; the leak is contained to that client within 30 minutes."},
        {"id": "O1", "attribute": "human oversight", "importance": "H", "difficulty": "L",
         "scenario": "No report is filed without the inspector's approval; 100% of filed reports carry it."},
        {"id": "L1", "attribute": "latency", "importance": "M", "difficulty": "H",
         "scenario": "On a 4G connection in the field, a draft report reaches the tablet within 5 s at p95."},
        {"id": "C1", "attribute": "cost", "importance": "M", "difficulty": "M",
         "scenario": "A report costs SAR 0.05 or less in model calls at 18,000 photos a month."},
        {"id": "A1", "attribute": "availability", "importance": "M", "difficulty": "M",
         "scenario": "During field hours (07:00 to 15:00) drafts are available 99% of the time."},
        {"id": "M1", "attribute": "operability", "importance": "L", "difficulty": "M",
         "scenario": "A change to a prompt template is reviewed and can be traced to its owner."},
    ])
    notes = [
        ("R01", "The vision model ksa-vision-x is not in the Asas catalogue: it was rejected for lack of Arabic "
                "evaluation evidence.", "non-compliance", "Q1",
         "The catalogue is a standard every team must meet; a design that uses an unadmitted model does not conform."),
        ("R02", "When ksa-vision-x fails, photos fall back to ext-vision-q, an external model.", "non-compliance", "P1",
         "Photos are Restricted; the placement rule forbids an external host whatever the path."),
        ("R03", "The evaluation gate runs on the English set only; signs and forms are in Arabic.", "risk", "Q1",
         "A gate exists, so it is not non-compliance; it measures the wrong thing for the top scenario."),
        ("R04", "The vision call takes 3,800 ms of the 5,000 ms p95 budget.", "sensitivity point", "L1",
         "One parameter, the provider's latency, decides whether the latency scenario is met."),
        ("R05", "Compressing photos on the tablet cuts upload time and cost, and lowers the recognition of small "
                "Arabic text.", "trade-off point", "Q1",
         "One decision moves latency and cost one way and quality the other."),
        ("R06", "The inspector approves every report before it is filed.", "non-risk", "O1",
         "The oversight scenario is met by design."),
        ("R07", "Drafts and approved reports are stored in the Ministry data centre.", "non-risk", "P1",
         "Storage placement meets the rule for Restricted data."),
        ("R08", "No owner is named for the prompt templates.", "risk", "M1",
         "Nobody reviews or answers for template changes."),
        ("R09", "A 10% sample review of approved reports is the only check that approvals are real.",
         "sensitivity point", "O1",
         "If the sample rate falls, rubber-stamping becomes invisible: the oversight scenario rests on this number."),
        ("R10", "The tablet app and the nightly batch share one gateway key.", "risk", "S1",
         "A leak in either client means revoking both: the leak is not contained to one client."),
        ("R11", "Hosting a vision model in the Ministry data centre would remove the placement question, and add a "
                "hardware purchase with a nine-month lead time.", "trade-off point", "P1",
         "Privacy against cost and time to service."),
        ("R12", "The cloud provider keeps photos 30 days and does not train on them, within the admission limit.",
         "non-risk", "P1", "The data terms meet the catalogue's criteria."),
    ]
    write_csv("review/notes.csv", [{"id": i, "observation": t} for i, t, _, _, _ in notes])
    ref("review_key", {"tags": {i: c for i, _, c, _, _ in notes}, "scenario": {i: s for i, _, _, s, _ in notes},
                       "why": {i: w for i, _, _, _, w in notes},
                       "priority": ["Q1", "P1", "S1", "O1", "L1", "A1", "C1", "M1"]})

    # ---- Lab 4.4: the deviation request
    write("deviation/request.md", """
# Deviation request DR-2026-07 · external vision model for inspection photos

**From** Rabah Al-Mujil, lead of the inspections team · **To** the Asas architecture board · **Date** 2026-11-02

**Request.** Allow Kashif to send inspection photos to `ext-vision-q`, an external vision model, for twelve
months, as its primary vision model.

**Why.** `ksa-vision-x` was not admitted: it has no Arabic evaluation evidence, and its provider will publish one
in February 2027 at the earliest. A Ministry-hosted vision model needs a hardware purchase with a nine-month lead
time. Meanwhile inspectors type every report by hand: 14 minutes a report, against about 6 with Kashif's draft.
`ext-vision-q` reads Arabic signs at 0.93 on the Ministry's signage set.

**What we accept.** Photos are classified Restricted because some show faces, car plates or documents. We would
ask inspectors to avoid people in photos.

**Standard affected.** Placement rule P-01: Restricted data may not go to an external host.
""")
    rows = []
    for i in range(400):
        face = rng.random() < 0.13
        plate = rng.random() < 0.17
        doc = rng.random() < 0.05
        restricted = face or plate or doc
        flagged = (rng.random() < 0.975) if restricted else (rng.random() < 0.09)
        rows.append({"photo_id": f"PH{i + 1:04d}", "has_face": int(face), "has_plate": int(plate),
                     "has_document": int(doc), "detector_flags": int(flagged)})
    write_csv("deviation/photo_sample.csv", rows)
    write_json("deviation/facts.json", {
        "note": "Synthetic figures for the deviation request DR-2026-07.",
        "photos_per_month": 18000, "photos_per_report": 3, "manual_minutes_per_report": 14,
        "assisted_minutes_per_report": 6, "inspector_cost_sar_per_hour": 120,
        "ext_vision_sar_per_photo": 0.02, "ext_vision_arabic_signage_score": 0.93,
        "ksa_vision_x_arabic_evidence_expected": "2027-02-28", "own_vision_lead_time_months": 9,
        "detector": "an on-device detector of faces, plates and documents that runs on the tablet before upload",
        "request_date": "2026-11-02"})
    n_r = sum(1 for r in rows if r["has_face"] or r["has_plate"] or r["has_document"])
    missed = sum(1 for r in rows if (r["has_face"] or r["has_plate"] or r["has_document"]) and not r["detector_flags"])
    clean_sent = sum(1 for r in rows if not r["detector_flags"])
    ref("deviation", {"restricted_share": round(n_r / len(rows), 4), "missed_by_detector": missed,
                      "sent_share": round(clean_sent / len(rows), 4), "sample": len(rows)})

    # ---- the capstone's three services
    briefs = {
        "reports": ("Citizen reports: routing and replies", "T02, the reports team",
                    "Citizens report potholes, broken lights and blocked pavements through the app and the call "
                    "centre: 90,000 reports a year, growing 15% a year. Each report carries text, a location, a "
                    "phone number and sometimes a photo. The team wants each report routed to the right department "
                    "and a reply drafted for the citizen.",
                    "Restricted (phone numbers, locations, photos)",
                    "Day 2's labelled reports (Lab 2.1) and Day 3's usage logs of T02, including its breach in May "
                    "and June."),
        "contact": ("Call-centre call summaries", "T08, the contact team",
                    "The Ministry's call centre takes 40,000 calls a month. Agents write a summary of each call "
                    "after it ends, about 90 seconds a call. The team wants a summary drafted from the recording "
                    "for the agent to correct, and a nightly batch of themes for managers.",
                    "Restricted (voices, names, identity numbers read aloud)",
                    "Day 3's usage logs and invoices of T08, the largest user of the Ministry data centre."),
        "staff": ("Staff policies assistant", "T09, the staff services team",
                  "6,000 staff questions a month about leave, allowances and training. The policies are Public; "
                  "a question about one's own case needs the employee's record, which is Restricted. The team's "
                  "first design sent both to an external model (Lab 4.2).",
                  "Public (policies) and Restricted (employee records)",
                  "Day 3's usage logs of T09 and the staff_assistant design of Lab 4.2."),
    }
    for k, (title, team, what, level, start) in briefs.items():
        write(f"../capstone/briefs/{k}.md",
              f"# {title}\n\n**Team.** {team}. **Data.** {level}.\n\n{what}\n\n**Where to start.** {start}\n\n"
              "**The panel will change** one classification level or the volume forecast during the defence; "
              "name the decisions it reopens.\n\nAll figures are synthetic.")


# ======================================================================================

def main() -> None:
    rng = random.Random(SEED)
    day1(rng)
    day2(random.Random(SEED + 2))
    day3(random.Random(SEED + 3))
    day4(random.Random(SEED + 4))
    print("wrote", sum(1 for p in DATA.rglob("*") if p.is_file()), "files under labs/data")


if __name__ == "__main__":
    main()
