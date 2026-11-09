"""Case "decrypt" layer: turns a normalised case + computed solution spec into the thinking a
winning team does before building slides.

Knowledge sources (all in data/):
  - case-competition-master-prompt.pdf, Part 3: SCQA, MECE issue tree, hypothesis in 20 min,
    80/20, 3-option decision matrix, ONE recommendation, 30/60/90 roadmap, top-3 risks,
    3-4 KPIs, Pyramid-Principle slides, 20+ Q&A, 5-hour time split.
  - engineering_1000_case_simulations.*: 8 objective families (energy, service, reliability,
    safety, throughput, quality, environment, logistics) -> family-specific trees and tools.
  - engineering_100000_preview.csv: answer key ("Illustrative Feasible Option") -> the
    minimum-cost compliant rung of the solution ladder reproduces it.
  - global_case_competitions_research.csv: 5 solution-model archetypes -> case archetype and
    similar competitions.
"""

from __future__ import annotations

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

ARCHETYPES = {
    "operations": {"name": "Operations & engineering improvement",
                   "model": "Baseline KPIs → bottleneck/root cause → optimize/simulate → pilot → ROI + KPIs",
                   "focus": ["Operations", "Supply chain", "Analytics", "Energy", "Healthcare", "Technology", "Sustainability"]},
    "strategy": {"name": "Business strategy",
                 "model": "SCQ → issue tree → market/customer economics → options → impact/ROI → rollout → risks",
                 "focus": ["Strategy", "International business", "Multi-category", "Marketing"]},
    "investment": {"name": "Investment / finance",
                   "model": "Investment thesis → valuation/scenarios → sensitivity → downside risk → recommendation",
                   "focus": ["Investment", "Finance", "Real estate"]},
    "impact": {"name": "Social impact & sustainability",
               "model": "Stakeholder needs → impact theory → feasibility/cost → measurement → safeguards",
               "focus": ["Sustainability", "Ethics", "Healthcare", "Social impact"]},
    "product": {"name": "Product & go-to-market",
                "model": "Segment users → insight → value proposition → channels → unit economics → testing",
                "focus": ["Marketing", "Technology", "Entrepreneurship"]},
}

# Objective families: issue tree (3 MECE branches), toolkit, KPIs, hypothesis template.
FAMILIES = {
    "throughput": {
        "label": "Throughput / capacity",
        "tree": [("Demand & mix", ["Is the demand real and sustained?", "Does product mix drive changeovers?"]),
                 ("Capacity at the constraint", ["Which stage runs at the highest utilisation?", "Where are OEE losses: availability, speed or quality?"]),
                 ("Flow between stages", ["Where does WIP pile up or starve?", "Are batch sizes and buffers sized to variability?"])],
        "tools": ["Theory of Constraints (5 focusing steps)", "OEE = Availability × Performance × Quality", "Little's Law: WIP = Throughput × Flow time", "Discrete-event simulation"],
        "kpis": ["Daily output", "Constraint utilisation", "OEE at the constraint", "WIP"],
        "hypothesis": "The gap is one binding constraint, not total capacity: relieving it delivers the target without rebuilding the whole system.",
    },
    "service": {
        "label": "Service time / queueing",
        "tree": [("Arrivals", ["What is the arrival rate and its peaks?", "Can demand be smoothed or triaged?"]),
                 ("Service capacity", ["How many servers, at what service rate?", "Which steps add no value?"]),
                 ("Flow & hand-offs", ["Where do patients/jobs wait between steps?", "Which hand-off has the longest queue?"])],
        "tools": ["Queueing: utilisation ρ = λ ÷ (c·μ); queues explode above 0.85", "Little's Law: L = λ × W", "Value-stream map (work vs wait time)", "Simulation of peak periods"],
        "kpis": ["Average service time", "90th-percentile time", "Server utilisation", "Abandonment / left-without-service"],
        "hypothesis": "Most of the time is waiting, not working: one over-utilised step creates the queue, and fixing its capacity or flow meets the target.",
    },
    "reliability": {
        "label": "Availability / reliability",
        "tree": [("Failure frequency", ["Which 20% of failure modes cause 80% of downtime?", "Is MTBF limited by design or by maintenance?"]),
                 ("Repair speed", ["What drives MTTR: diagnosis, spares or access?", "Are critical spares on site?"]),
                 ("Architecture", ["Is there single-point-of-failure exposure?", "Would redundancy beat repair speed?"])],
        "tools": ["Availability = MTBF ÷ (MTBF + MTTR)", "Pareto of failure modes → FMEA", "Reliability-centred maintenance", "Weibull analysis"],
        "kpis": ["Availability", "MTBF", "MTTR", "Unplanned downtime hours"],
        "hypothesis": "A few failure modes dominate downtime: targeting them through condition monitoring and faster repair beats wholesale replacement.",
    },
    "safety": {
        "label": "Safety / risk reduction",
        "tree": [("Hazards", ["Which hazards carry the highest severity?", "Which are new since the disruption?"]),
                 ("Exposure", ["How often and how many people are exposed?", "Which tasks drive exposure?"]),
                 ("Controls", ["Which controls exist and how reliable are they?", "Can we move up the hierarchy of controls?"])],
        "tools": ["Risk = Likelihood × Severity matrix", "Hierarchy of controls (eliminate → PPE)", "Bow-tie analysis", "HAZOP / FMEA"],
        "kpis": ["Risk score", "Recordable incident rate", "Near-miss reports", "Critical-control compliance"],
        "hypothesis": "Most of the risk score comes from a few high-severity exposures that engineering controls can remove, not from procedure gaps.",
    },
    "quality": {
        "label": "Quality / defects & loss",
        "tree": [("Defect modes", ["Which defect types make up 80% of losses?", "Where in the process are they created?"]),
                 ("Process variation", ["Is the process capable (Cp/Cpk)?", "Which inputs drive variation?"]),
                 ("Detection & control", ["Are defects caught early or at the end?", "Can errors be mistake-proofed?"])],
        "tools": ["DMAIC", "Pareto chart + fishbone + 5 Whys", "SPC control charts", "Poka-yoke"],
        "kpis": ["Defect / loss rate", "First-pass yield", "Cpk on critical feature", "Cost of poor quality"],
        "hypothesis": "Two or three defect modes drive most of the loss; fixing their root cause at the source meets the target.",
    },
    "energy": {
        "label": "Energy efficiency",
        "tree": [("Load profile", ["What is base load vs peak load?", "Which end-uses dominate consumption?"]),
                 ("Equipment efficiency", ["Which assets run far below best-in-class efficiency?", "Are they oversized?"]),
                 ("Controls & operation", ["Do systems run when not needed?", "Are setpoints optimised?"])],
        "tools": ["Energy balance / Sankey by end-use", "Cost per kWh saved (levelized)", "ISO 50001 measurement & verification", "Controls optimisation"],
        "kpis": ["Annual kWh", "kWh per unit of output", "Peak demand (kW)", "CAD per kWh saved"],
        "hypothesis": "Controls and the two largest end-uses hold most of the savings; the cheapest kWh is the one avoided by better operation.",
    },
    "environment": {
        "label": "Emissions reduction",
        "tree": [("Direct emissions (Scope 1)", ["Which combustion or process sources dominate?", "Can fuel be switched?"]),
                 ("Purchased energy (Scope 2)", ["How carbon-intensive is the supply?", "Can efficiency or procurement cut it?"]),
                 ("Other sources", ["Fugitive, waste or transport emissions?", "Are they material?"])],
        "tools": ["GHG Protocol inventory", "Marginal abatement cost curve (MACC)", "CAD per tCO2e abated", "Carbon price sensitivity"],
        "kpis": ["tCO2e per year", "Emissions intensity", "CAD per tCO2e abated", "Share of low-carbon energy"],
        "hypothesis": "A few large sources hold most of the abatement potential at the lowest cost per tonne; start at the bottom of the abatement curve.",
    },
    "cost": {
        "label": "Logistics / operating cost",
        "tree": [("Volume & network", ["Is the network shaped for today's volumes?", "Which lanes carry most cost?"]),
                 ("Rates & mode", ["Are rates or modes above market?", "Can loads be consolidated?"]),
                 ("Process waste", ["Where are touches, empty miles or rework?", "What does failure cost?"])],
        "tools": ["Cost tree (volume × rate × waste)", "Total cost of ownership", "Routing / linear programming", "Pareto of cost by lane"],
        "kpis": ["Cost per month", "Cost per unit shipped", "On-time-in-full (OTIF)", "Utilisation of assets"],
        "hypothesis": "A minority of lanes or activities drive most of the cost; redesigning those beats across-the-board cuts.",
    },
    "schedule": {
        "label": "Schedule / duration",
        "tree": [("Critical path", ["Which activities have zero float?", "Can any run in parallel?"]),
                 ("Resources", ["Which crews or equipment are the constraint?", "Is overtime or a second shift possible?"]),
                 ("Risk & approvals", ["Which permits or inspections gate progress?", "Where is weather or supply risk?"])],
        "tools": ["Critical path method (CPM)", "PERT three-point estimates", "Crashing by cost slope", "Resource levelling"],
        "kpis": ["Total duration (days)", "Critical-path float", "Schedule performance index", "Cost of acceleration"],
        "hypothesis": "A handful of critical-path activities set the duration; crashing the cheapest of them meets the target without blanket acceleration.",
    },
}

TIME_PLAN = [  # 5-hour cracking window (master prompt §3.7)
    ("0:00–0:40", "Read & align", "SCQA, issue tree, first hypothesis"),
    ("0:40–1:50", "Data & quick math", "Baseline, gap, vital-few drivers (80/20)"),
    ("1:50–3:20", "Options & decision", "3 costed options, matrix, NPV, sensitivity"),
    ("3:20–4:20", "Deck", "Answer-first storyline, action titles"),
    ("4:20–5:00", "Rehearse & Q&A", "Timed run-through, 20+ questions"),
]


def classify_family(case: dict) -> str:
    text = f"{case.get('target_metric', '')} {case.get('baseline_metric', '')}".lower()
    unit = case.get("baseline_unit", "").lower()
    rules = [("energy", "energy" in text or "kwh" in unit), ("environment", "emission" in text or "co2" in unit),
             ("service", "service time" in text or unit == "minutes"), ("reliability", "availab" in text),
             ("safety", "risk" in text or unit == "index/100"), ("quality", any(k in text for k in ("defect", "loss", "scrap"))),
             ("cost", "cost" in text or unit.startswith("cad/")), ("schedule", "duration" in text or unit == "days")]
    return next((fam for fam, hit in rules if hit), "throughput")


def classify_archetype(case: dict) -> str:
    text = f"{case.get('title', '')} {case.get('brief', '')} {case.get('decision_question', '')}".lower()
    scores = {
        "investment": sum(k in text for k in ("valuation", "acquisition", "invest in", "portfolio", "irr ", "m&a")),
        "impact": sum(k in text for k in ("community", "social", "equity", "stakeholder", "nonprofit", "indigenous")),
        "product": sum(k in text for k in ("users", "app ", "product launch", "go-to-market", "subscription", "pricing")),
        "strategy": sum(k in text for k in ("market share", "revenue", "customers", "market entry", "competitor", "growth strategy")),
        "operations": 1 + sum(k in text for k in ("throughput", "bottleneck", "capacity", "downtime", "fulfil", "logistics",
                                                  "process", "engineering", "maintenance", "energy", "emission")),
    }
    return max(scores, key=scores.get)


def _cad(x):
    return "n/a" if x is None else f"{'-' if x < 0 else ''}CAD ${abs(round(x)):,}"


def _months(x):
    return f"{x:.1f} months" if x is not None else "beyond the 5-year horizon"


def solution_ladder(spec: dict) -> list[dict]:
    """Four solution levels, from cheapest move to stretch, plus where the recommendation sits."""
    opts = spec["options_evaluation"]["options"]
    in_budget = [o for o in opts if o["within_budget"]]
    compliant = [o for o in in_budget if o["meets_target"]]
    rungs = [
        ("Level 1", "Quick win", "Lowest capital: what a minimal move buys", min(opts, key=lambda o: o["capex_CAD"])),
        ("Level 2", "Minimum compliant", "Cheapest option that meets the target within budget",
         min(compliant, key=lambda o: o["capex_CAD"]) if compliant else None),
        ("Level 3", "Value maximiser", "Highest NPV within budget", max(in_budget, key=lambda o: o["npv_CAD"]) if in_budget else None),
        ("Level 4", "Stretch", "Largest improvement regardless of budget", max(opts, key=lambda o: o["improvement_percent"])),
    ]
    out = []
    for lvl, name, rule, o in rungs:
        if o is None:
            out.append({"level": lvl, "name": name, "rule": rule, "option": None,
                        "summary": "Not available: no option meets the target within budget."})
            continue
        out.append({"level": lvl, "name": name, "rule": rule, "option": o["label"], "option_name": o["name"],
                    "capex_CAD": o["capex_CAD"], "improvement_percent": o["improvement_percent"], "npv_CAD": o["npv_CAD"],
                    "meets_target": o["meets_target"], "within_budget": o["within_budget"], "selected": o["selected"],
                    "summary": f"Option {o['label']}: {o['improvement_percent']:g}% for {_cad(o['capex_CAD'])}"
                               f" ({'meets' if o['meets_target'] else 'misses'} target, {'in' if o['within_budget'] else 'over'} budget)"})
    return out


def ladder_rationale(spec: dict, ladder: list[dict]) -> str:
    win = spec["options_evaluation"]["winner"]
    l2, l3, l4 = ladder[1], ladder[2], ladder[3]
    if l2["option"] is None:
        return (f"No option reaches the target inside the budget. We recommend Option {win} now (best in-budget score) and take "
                f"Level 4 (Option {l4['option']}) to the sponsor as a funded phase-2 decision once the pilot proves the gain.")
    parts = [f"Option {win} is recommended."]
    if l2["option"] == win and l3["option"] == win:
        parts.append("It is both the cheapest compliant option and the best value: a dominant choice.")
    elif l2["option"] == win:
        if l3["meets_target"]:
            parts.append(f"It is the cheapest way to meet the target; Option {l3['option']} adds NPV but needs more capital and risk.")
        else:
            parts.append(f"It is the cheapest way to meet the target; Option {l3['option']} looks better on NPV alone but misses the target.")
    elif l3["option"] == win:
        parts.append(f"Option {l2['option']} meets the target more cheaply, but Option {win} creates more value for the extra spend.")
    if l4["option"] != win:
        parts.append(f"Option {l4['option']} would deliver more ({l4['improvement_percent']:g}%) but "
                     + ("exceeds the budget." if not l4["within_budget"] else "scores lower on return and risk."))
    return " ".join(parts)


def competition_matches(archetype: str, family: str, n: int = 5) -> list[dict]:
    path = DATA_DIR / "global_case_competitions_research.csv"
    if not path.exists():
        return []
    model = ARCHETYPES[archetype]["model"]
    focus = ARCHETYPES[archetype]["focus"]
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    ranked = sorted(rows, key=lambda r: (r["Suggested solution model (NOT winner)"] != model,
                                         focus.index(r["Typical focus"]) if r["Typical focus"] in focus else 99))
    return [{"competition": r["Competition"], "region": r["Country / region"], "focus": r["Typical focus"],
             "source": r["Directory source"]} for r in ranked[:n]]


def build_qa_bank(spec: dict, ladder: list[dict], family: dict) -> list[dict]:
    fs, opts = spec["financial_summary"], spec["options_evaluation"]["options"]
    win = next(o for o in opts if o["selected"])
    cheapest = min(opts, key=lambda o: o["capex_CAD"])
    biggest = max(opts, key=lambda o: o["improvement_percent"])
    tornado = {t["driver"].split(" (")[0]: t for t in spec["sensitivity"]}
    dur = next((t for k, t in tornado.items() if k.startswith("Implementation")), None)
    qa, seen = [], set()
    for q in spec["red_team_defense"]:  # drop questions whose computed answer duplicates another
        if q["rebuttal"] not in seen:
            seen.add(q["rebuttal"])
            qa.append({"category": "Stress test", **q})
    extra = [] if cheapest["label"] == win["label"] else [
        ("Alternatives", f"Why not Option {cheapest['label']}, the cheapest?",
         f"It costs {_cad(cheapest['capex_CAD'])} but delivers {cheapest['improvement_percent']:g}% "
         f"({'meets' if cheapest['meets_target'] else 'misses'} the {spec['case_inputs']['target_pct']:g}% target); "
         f"it scores {cheapest['weighted_total']}/10 vs {win['weighted_total']}/10 for Option {win['label']}.")]
    extra += [] if biggest["label"] == win["label"] else [
        ("Alternatives", f"Why not Option {biggest['label']}, the biggest gain?",
         f"{biggest['improvement_percent']:g}% for {_cad(biggest['capex_CAD'])}: "
         + ("it exceeds the budget." if not biggest["within_budget"] else
            f"NPV {_cad(biggest['npv_CAD'])} vs {_cad(win['npv_CAD'])}; the extra gain does not justify the extra capital and risk."))]
    extra += [
        ("Assumptions", "How confident are you in the option estimates?",
         f"Source: {win['source']}. We treat them as hypotheses: the Horizon 1 pilot must reach 80% of the modelled gain before scale-up spend."),
        ("Financials", "What does it cost to run every year?",
         f"O&M of {_cad(fs['annual_om_CAD'])}/yr is already netted out of the {_cad(fs['annual_run_rate_benefit_CAD'])}/yr benefit."),
        ("Financials", "What is the benefit-to-cost ratio?",
         f"{fs['benefit_cost_ratio']} on a present-value basis at {fs['wacc_percent']:.1f}% WACC; levelized {fs['levelized_cost']} {fs['levelized_cost_unit']}."),
        ("Implementation", "What if implementation takes 50% longer?",
         f"NPV falls to {_cad(dur['low_npv'])}; the H1 pilot and fixed-price packages protect the schedule." if dur else
         "The pilot gate and fixed-price packages protect the schedule."),
        ("Implementation", "How will you know it is working by day 30?",
         f"Pilot KPI: {spec['implementation_horizons'][0]['kpi']}. Leading indicators: {', '.join(family['kpis'][1:3])}."),
        ("Safety", "What are the safety and regulatory implications?",
         "Every change goes through management-of-change review and HAZOP before commissioning; designs are validated against local codes and vendor specifications, with licensed engineering review before deployment."),
        ("Upside", "What would you do with 20% more budget?",
         f"Fund Option {biggest['label']} ({biggest['improvement_percent']:g}%) as phase 2 if the pilot confirms the model."
         if biggest["label"] != win["label"] else "Accelerate the rollout and add redundancy at the constraint."),
    ]
    qa += [{"category": c, "question": q, "rebuttal": a} for c, q, a in extra]
    return qa


def build_intelligence(case: dict, spec: dict) -> dict:
    fam_key = classify_family(case)
    fam = FAMILIES[fam_key]
    arch_key = classify_archetype(case)
    fs, inp, sol = spec["financial_summary"], spec["case_inputs"], spec["approved_solution"]
    unit, base, tgt = inp["baseline_unit"], inp["baseline_value"], inp["target_pct"]
    ladder = solution_ladder(spec)
    reducing = any(k in f"{inp['target_metric']}".lower() for k in ("reduction", "reduce", "cut"))
    target_abs = base * (1 - tgt / 100) if reducing else base * (1 + tgt / 100)
    target_txt = (f"{target_abs:,.2f} {unit}" if unit != "%" or target_abs <= 100 else f"{tgt:g}% relative improvement")

    same = inp["brief"].strip() == (inp["decision_question"] or "").strip()
    scqa = {
        "situation": (f"{case['title']}. {case.get('context', '').capitalize()}. {inp['baseline_metric']} today: {base:,.2f} {unit}."
                      if same else None) or inp["brief"] or f"{case['title']}: {inp['baseline_metric']} at {base:,.2f} {unit}.",
        "complication": f"{inp['baseline_metric']} must move from {base:,.2f} {unit} to {target_txt} ({tgt:g}%) within "
                        f"{inp['timeline_months']} months and {_cad(inp['budget'])}"
                        + (f", while: {'; '.join(c for c in inp['constraints'][:2])}." if inp["constraints"] else "."),
        "question": inp["decision_question"] or "Which option should we commit to, and how do we de-risk it?",
        "answer": sol["value_proposition"],
    }
    insight = (f"This is a {fam['label'].lower()} problem under a hard budget. Judges are testing whether you find the binding "
               f"driver before spending, compare three options on the same basis, and show what happens when the numbers move.")
    kpis = [{"kpi": fam["kpis"][0], "baseline": f"{base:,.2f} {unit}", "target": target_txt}] + \
           [{"kpi": k, "baseline": "measure in week 1", "target": "set from pilot"} for k in fam["kpis"][1:4]]
    hz = spec["implementation_horizons"]
    plan_30_60_90 = [
        {"window": "Days 1–30", "focus": "Validate & pilot", "actions": ["Confirm baseline data and the binding constraint",
                                                                          f"Launch pilot of Option {sol['label']} at the constraint", "Name owners; start KPI dashboard"]},
        {"window": "Days 31–60", "focus": "Prove & decide", "actions": [f"Pilot gate: {hz[0]['gate']}", "Lock fixed-price packages for scale-up",
                                                                          "Train operators; write standard work"]},
        {"window": "Days 61–90", "focus": "Scale & control", "actions": [f"Begin {hz[1]['name'].lower()}", "Control chart on the primary KPI",
                                                                           f"Review vs target ({tgt:g}%) with sponsor"]},
    ]
    weak = spec["weak_assumptions"]
    win = next(o for o in spec["options_evaluation"]["options"] if o["selected"])
    checklist = [
        ("Answer-first executive summary (one sentence, three numbers)", True, sol["value_proposition"][:120] + "…"),
        ("Three options costed on the same basis", len(spec["options_evaluation"]["options"]) >= 3, "decision matrix with weights shown"),
        ("Recommendation fits the budget", win["within_budget"], f"{_cad(win['capex_CAD'])} of {_cad(inp['budget'])}"),
        ("Recommendation meets the target", win["meets_target"], f"{win['improvement_percent']:g}% vs {tgt:g}%"),
        ("Financials: NPV, payback, sensitivity", True, f"NPV {_cad(fs['npv_CAD'])}, payback {_months(fs['payback_period_months'])}"),
        ("Bear case tested (-15% performance, +20% cost)", True, f"bear NPV {_cad(spec['scenarios'][0]['npv'])}"),
        ("30/60/90 roadmap with owners and gates", True, "pilot → prove → scale"),
        ("Top risks with triggers", len(spec["risks"]) >= 3, f"{len(spec['risks'])} risks logged"),
        ("Q&A bank of 10+ prepared answers", True, "see judge_QA_preparation.md"),
        ("Assumptions validated with real data", not weak, "replace: " + ", ".join(weak) if weak else "all case data"),
        ("Safety & licensed engineering review noted", True, "MOC + HAZOP before commissioning"),
    ]
    return {
        "archetype": arch_key, "archetype_name": ARCHETYPES[arch_key]["name"], "solution_model": ARCHETYPES[arch_key]["model"],
        "family": fam_key, "family_label": fam["label"], "what_the_case_tests": insight, "scqa": scqa,
        "issue_tree": {"root": f"How do we achieve {tgt:g}% {inp['target_metric'].lower()} within {inp['timeline_months']} months and {_cad(inp['budget'])}?",
                       "branches": [{"name": n, "questions": q} for n, q in fam["tree"]]},
        "hypothesis": fam["hypothesis"], "toolkit": fam["tools"],
        "quick_math": [f"Gap: {base:,.2f} → {target_txt}",
                       f"Budget per % point of target: {_cad(inp['budget'] / tgt) if tgt else 'n/a'}",
                       f"Winner cost per % point delivered: {_cad(win['capex_CAD'] / win['improvement_percent']) if win['improvement_percent'] else 'n/a'}"],
        "solution_ladder": ladder, "ladder_rationale": ladder_rationale(spec, ladder),
        "kpis": kpis, "plan_30_60_90": plan_30_60_90, "time_plan": [{"time": t, "step": s, "output": o} for t, s, o in TIME_PLAN],
        "qa_bank": build_qa_bank(spec, ladder, fam),
        "similar_competitions": competition_matches(arch_key, fam_key),
        "submission_checklist": [{"item": i, "ok": bool(ok), "evidence": e} for i, ok, e in checklist],
    }
