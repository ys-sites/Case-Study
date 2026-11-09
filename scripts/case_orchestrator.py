"""Autonomous Case Competition Intelligence System Orchestrator (v2).

One deterministic engine that turns any case (ENG-xxxx, ENG100K-xxxxxx, ENG1M-xxxxxxx,
a PDF/MD/TXT/JSON brief, or a case directory) into the canonical Finished Resources set.

Design rules
------------
1. Single source of truth: every number in every deliverable is read from `solution_spec`,
   which is computed once by `build_solution_spec()`. Nothing is hardcoded per deliverable.
2. Data-driven decision: the three alternatives are scored with an explicit weighted matrix;
   the winner is whatever the numbers pick (budget is a hard gate).
3. Honest assumptions: every value not stated in the case is logged in the assumptions
   register with its source, and the weakest ones are surfaced as unresolved issues.
4. Real quality gates: Agent 14 re-reads the produced files and reports PASS / WARN / FAIL.

Agent map (stage -> function)
  00 Master Orchestrator ........ run_agent_pipeline / build_solution_spec
  01 Case Intelligence .......... load_case_data, write_case_intelligence
  02 Competition Research ....... write_research
  03 Root Cause Analyst ......... diagnose
  04 Brainstorming .............. write_brainstorming
  05 Strategy Decision .......... evaluate_options, write_evaluation_matrix
  06 Financial Modeling ......... cash_model, write_financial_workbooks
  07 Technical Architecture ..... write_strategy (solution_architecture.md)
  08 Implementation Blueprint ... build_horizons, write_strategy
  09 Red Team ................... build_red_team, sensitivity
  10 PDF Documentation .......... generate_pdf_deliverables
  11 PowerPoint ................. generate_powerpoint_deck
  12 Website sync ............... sync_frontend
  13 Video Production ........... generate_video_assets
  14 Quality Assurance .......... run_quality_gates
"""

from __future__ import annotations

import argparse
import csv
import getpass
import json
import re
import shutil
import subprocess
import sys
import textwrap
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_ROOT = Path("Finished Resources")
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from case_intelligence import build_intelligence  # noqa: E402
import case_videos  # noqa: E402
from case_visual_pdf import generate_case_study_booklet  # noqa: E402
DATA_DIR = REPO_ROOT / "data"

# --------------------------------------------------------------------------------------
# Model parameters (all surfaced in the assumptions register)
# --------------------------------------------------------------------------------------
WACC = 0.095                 # discount rate
HORIZON_YEARS = 5            # appraisal horizon
OM_RATE = 0.05               # annual O&M as share of capex
PILOT_SHARE = 0.30           # share of full benefit realised while still implementing
OPERATING_DAYS = 250
BEAR = {"perf": 0.85, "capex": 1.20}   # performance -15 %, cost +20 % (standard judge challenge)
BULL = {"perf": 1.15, "capex": 0.90}

# Value of one unit of improvement, by baseline unit. (value CAD, source label)
UNIT_VALUES = {
    "units/day": (24.50 * OPERATING_DAYS, "CAD 24.50 contribution/unit x 250 operating days"),
    "kwh/year": (0.13, "CAD 0.13/kWh blended industrial tariff"),
    "tonnes co2e/year": (95.0, "CAD 95/tCO2e carbon price"),
    "cad/month": (12.0, "case datum (monthly CAD x 12)"),
    "cad/year": (1.0, "case datum (annual CAD)"),
}
ECONOMIC_UNITS = {"units/day", "cad/month", "cad/year"}  # objective is profit; others are mandate-driven
ANCHOR_SHARE = 0.45  # non-monetary metrics: annual value of full target = 45 % of budget

# Parametric options when a case gives names but no costs: (share of budget, x target)
PARAMETRIC_OPTIONS = [(0.30, 0.65), (0.70, 1.15), (1.15, 1.60)]

CRITERIA = [
    ("Target attainment", 0.30),
    ("Financial return (NPV)", 0.25),
    ("Payback speed", 0.15),
    ("Downside resilience (-15% perf.)", 0.15),
    ("Budget headroom", 0.15),
]

CANONICAL_DIRS = [
    "00_Project_Overview", "01_Case_Intelligence", "02_Research", "03_Brainstorming",
    "04_Final_Strategy", "05_Financial_Models", "06_PDF_Deliverables", "07_PowerPoint",
    "08_Website", "09_Video", "09_Video/source_project", "10_Agent_Reports",
    "11_Final_Quality_Control",
]


# --------------------------------------------------------------------------------------
# Formatting helpers
# --------------------------------------------------------------------------------------
def cad(x: float | None) -> str:
    if x is None:
        return "n/a"
    sign = "-" if x < 0 else ""
    return f"{sign}CAD ${abs(round(x)):,}"


def num(x: float, digits: int = 2) -> str:
    return f"{x:,.{digits}f}".rstrip("0").rstrip(".") if digits else f"{x:,.0f}"


def months(x: float | None) -> str:
    return f"{x:.1f} months" if x is not None else f"> {HORIZON_YEARS * 12} months"


def pct(x: float | None, digits: int = 1) -> str:
    return f"{x:.{digits}f}%" if x is not None else "n/a"


def _f(row: dict, key: str, default: float) -> float:
    try:
        return float(str(row.get(key, default)).replace(",", ""))
    except (TypeError, ValueError):
        return float(default)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def md_table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join([" --- "] * len(headers)) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


# --------------------------------------------------------------------------------------
# Agent 01: case loading & normalisation
# --------------------------------------------------------------------------------------
def create_directory_structure() -> None:
    for d in CANONICAL_DIRS:
        (OUTPUT_ROOT / d).mkdir(parents=True, exist_ok=True)


def _case(**kw) -> dict:
    """Normalised case record. `options` is a list of {label,name,capex,improvement,source}."""
    base = {
        "id": "CASE", "title": "Case", "discipline": "Engineering", "difficulty": "Advanced",
        "context": "", "brief": "", "decision_question": "", "objective": "",
        "baseline_metric": "Baseline", "baseline_value": 1000.0, "baseline_unit": "units/day",
        "target_metric": "Target improvement", "target_pct": 20.0, "budget": 1_500_000.0,
        "timeline_months": 12, "constraints": [], "options": [], "suggested_analysis": "",
        "judge_questions": [], "rubric": {}, "source_type": "unknown", "provenance": {},
    }
    base.update(kw)
    return base


def _parametric_options(names: list[str], budget: float, target: float) -> list[dict]:
    names = (names + ["Optimise existing system", "Targeted retrofit", "Full replacement"])[:3]
    return [
        {"label": "ABC"[i], "name": re.sub(r"^Option [ABC]:\s*", "", n).strip(),
         "capex": round(budget * share), "improvement": round(target * mult, 2),
         "source": f"assumption: {share:.0%} of budget, {mult:.2f}x target"}
        for i, (n, (share, mult)) in enumerate(zip(names, PARAMETRIC_OPTIONS))
    ]


def _from_json_case(c: dict, source: str) -> dict:
    inp = c.get("inputs", {})
    budget = float(inp.get("capital_budget_CAD", 1_500_000))
    target = float(inp.get("target_value", 20))
    return _case(
        id=c.get("id", "CASE-JSON"), title=c.get("case_title") or c.get("title", "Engineering Case"),
        discipline=c.get("discipline", "Engineering"), difficulty=c.get("difficulty", "Advanced"),
        context=c.get("scenario_type", ""), brief=c.get("case_brief") or c.get("brief", ""),
        decision_question=c.get("decision_question", ""), objective=c.get("objective", ""),
        baseline_metric=inp.get("baseline_metric", "Baseline"),
        baseline_value=float(inp.get("baseline_value", 1000)),
        baseline_unit=inp.get("baseline_unit", "units/day"),
        target_metric=inp.get("target_metric", "Target improvement"), target_pct=target,
        budget=budget, timeline_months=int(inp.get("timeline_months", 12)),
        constraints=c.get("constraints", []),
        options=_parametric_options(c.get("alternatives_to_compare") or c.get("alternatives", []), budget, target),
        suggested_analysis=c.get("suggested_analysis", ""),
        judge_questions=c.get("judge_questions", []), rubric=c.get("judge_rubric", {}),
        source_type=source, provenance={"options": "parametric assumption (case gives no option costs)"},
    )


def _csv_lookup(path: Path, key_col: str, case_id: str) -> dict | None:
    if not path.exists():
        return None
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row.get(key_col) == case_id:
                return row
    return None


def _from_100k(row: dict) -> dict:
    opts = [{"label": L, "name": row.get(f"Option {L}", f"Option {L}"),
             "capex": _f(row, f"Option {L} Cost CAD", 0),
             "improvement": _f(row, f"Option {L} Estimated Improvement Percent", 0),
             "source": "case datum"} for L in "ABC"]
    return _case(
        id=row["Case ID"], title=f"{row.get('Archetype', 'Case')} — {row.get('Context', '')} ({row.get('Shock', '')})",
        discipline=row.get("Discipline", ""), difficulty=row.get("Difficulty", ""),
        context=f"{row.get('Context', '')}; shock: {row.get('Shock', '')}", brief=row.get("Decision Brief", ""),
        decision_question=f"Which design should be chosen for {row.get('Archetype', 'the system').lower()} during {row.get('Shock', 'the disruption')}?",
        objective=f"Deliver {row.get('Target Improvement Percent')}% {row.get('Target Metric', 'improvement').lower()} within {row.get('Deadline Months')} months.",
        baseline_metric=row.get("Baseline Metric", "Baseline"), baseline_value=_f(row, "Baseline Value", 1000),
        baseline_unit=row.get("Baseline Unit", "units/day"), target_metric=row.get("Target Metric", "Improvement"),
        target_pct=_f(row, "Target Improvement Percent", 20), budget=_f(row, "Budget CAD", 1_500_000),
        timeline_months=int(_f(row, "Deadline Months", 12)),
        constraints=[c.strip() for c in row.get("Technical Constraints", "").split("|") if c.strip()]
        + [f"Availability >= {row.get('Availability Percent')}%", f"Max installation downtime {row.get('Max Installation Downtime Hours')} h"],
        options=opts, suggested_analysis=row.get("Suggested Analysis", ""),
        judge_questions=[q for q in [row.get("Judge Challenge")] if q], source_type="100k_preview_simulation",
    )


def _from_1m(row: dict) -> dict:
    opts = [{"label": L, "name": row.get(f"option_{L.lower()}", f"Option {L}"),
             "capex": _f(row, f"option_{L.lower()}_capex_cad", 0),
             "improvement": _f(row, f"option_{L.lower()}_estimated_improvement_pct", 0),
             "source": "case datum"} for L in "ABC"]
    return _case(
        id=row["case_id"], title=f"{row.get('asset', 'Asset').title()} — {row.get('technical_challenge', '').title()} ({row.get('disruption', '')})",
        discipline=row.get("discipline", ""), difficulty=row.get("difficulty", ""),
        context=f"{row.get('operating_context', '')}; disruption: {row.get('disruption', '')}",
        brief=row.get("decision_question", ""), decision_question=row.get("decision_question", ""),
        objective=f"At least {row.get('required_improvement_pct')}% improvement in {row.get('technical_challenge', 'performance')} within {row.get('deadline_months')} months.",
        baseline_metric=row.get("technical_challenge", "Baseline").title(), baseline_value=_f(row, "baseline_value", 1000),
        baseline_unit=row.get("baseline_unit", "units/day"), target_metric=f"{row.get('technical_challenge', 'Performance').title()} improvement",
        target_pct=_f(row, "required_improvement_pct", 20), budget=_f(row, "budget_cad", 1_500_000),
        timeline_months=int(_f(row, "deadline_months", 12)),
        constraints=[c for c in [row.get("constraint", ""), f"Minimum availability {row.get('minimum_availability_pct')}%"] if c],
        options=opts, suggested_analysis=row.get("analysis_methods", ""),
        judge_questions=[q for q in [row.get("judge_question")] if q], source_type="1m_preview_simulation",
    )


def _from_text(text: str, case_id: str, title: str, source: str) -> dict:
    """Best-effort extraction from a free-text brief; every miss is flagged as an assumption."""
    prov, t = {}, text.replace("\u00a0", " ")

    def grab(pattern, cast, default, key):
        m = re.search(pattern, t, re.I)
        if m:
            try:
                prov[key] = "extracted from brief"
                return cast(m)
            except (ValueError, IndexError):
                pass
        prov[key] = "assumption (not found in brief)"
        return default

    def find_budget() -> float | None:
        """Pick the money mention closest to budget language (capital/capex/budget/ceiling)."""
        mult = {"b": 1e9, "bn": 1e9, "billion": 1e9, "m": 1e6, "mn": 1e6, "million": 1e6, "k": 1e3}
        best, best_score = None, 0
        for m in re.finditer(r"(?:CAD|C\$|\$)\s*\$?\s*([\d][\d,]*\.?\d*)\s*(billion|bn|b|million|mn|m|k)?\b", t, re.I):
            value = float(m.group(1).replace(",", "")) * mult.get((m.group(2) or "").lower(), 1)
            if value < 1_000:
                continue
            ctx = t[max(0, m.start() - 60):m.end() + 40].lower()
            score = sum(k in ctx for k in ("capital", "capex", "budget", "ceiling", "envelope", "investment")) \
                - sum(k in ctx for k in ("revenue", "/yr", "per year", "annual", "/order", "savings"))
            if score > best_score:
                best, best_score = value, score
        return best

    budget = find_budget()
    prov["budget"] = "extracted from brief" if budget else "assumption (not found in brief)"
    budget = budget or 1_500_000.0
    target = grab(r"(\d+(?:\.\d+)?)\s*%\s*(?:improvement|increase|reduction|gain|uplift)", lambda m: float(m.group(1)), 20.0, "target_pct")
    timeline = grab(r"(?:within|in|over)\s+(\d{1,2})\s*months", lambda m: int(m.group(1)), 12, "timeline_months")
    unit_re = r"units/day|kWh/year|tonnes CO2e/year|CAD/month|CAD/year|minutes|days"
    baseline, unit = grab(rf"(?:baseline|current)[^.\n]{{0,80}}?([\d][\d,]*\.?\d*)\s*({unit_re})", lambda m: (float(m.group(1).replace(",", "")), m.group(2)),
                          (100.0, "index/100"), "baseline_value")
    alts = re.findall(r"Option\s+[ABC]\s*[:\-–]\s*([^\n.;]+)", t)
    return _case(
        id=case_id, title=title, discipline="Multidisciplinary Engineering & Strategy", difficulty="Championship",
        brief=re.sub(r"\s+", " ", t).strip()[:700] or title,
        decision_question="Which intervention resolves the binding constraint at the best risk-adjusted return within budget and deadline?",
        objective=f"Deliver {target:g}% improvement within {timeline} months under {cad(budget)}.",
        baseline_metric="Baseline performance", baseline_value=baseline, baseline_unit=unit,
        target_pct=target, budget=budget, timeline_months=timeline,
        constraints=[f"Capital budget <= {cad(budget)}", f"Core implementation within {timeline} months",
                     "No compromise on safety or regulatory compliance"],
        options=_parametric_options(alts, budget, target), source_type=source,
        provenance={**prov, "options": "parametric assumption (no option costs in brief)"},
    )


def load_case_data(case_identifier: str = "ENG-0001") -> dict:
    """Resolve any supported identifier/path into a normalised case record."""
    p = Path(case_identifier)
    if p.is_file():
        suffix = p.suffix.lower()
        if suffix == ".json":
            raw = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(raw, dict) and "cases" in raw:
                raw = raw["cases"][0]
            return _from_json_case(raw, "file_json")
        if suffix == ".pdf":
            import pymupdf
            with pymupdf.open(str(p)) as doc:
                text = "\n".join(page.get_text() for page in doc)
        else:
            text = p.read_text(encoding="utf-8", errors="ignore")
        return _from_text(text, f"CASE-{p.stem.upper()[:16]}", p.stem.replace("_", " ").title(), f"file{suffix}")
    if p.is_dir():
        text = "\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in sorted(p.glob("*.md")))
        return _from_text(text, f"CASE-{p.name.upper()[:16]}", p.name.replace("_", " ").title(), "directory_package")

    cid = case_identifier.strip()
    if cid.upper().startswith("ENG100K"):
        row = _csv_lookup(DATA_DIR / "engineering_100000_preview.csv", "Case ID", cid)
        if row:
            return _from_100k(row)
    elif cid.upper().startswith("ENG1M"):
        row = _csv_lookup(DATA_DIR / "engineering_1million_additional_preview.csv", "case_id", cid)
        if row:
            return _from_1m(row)
    else:
        sims = DATA_DIR / "engineering_1000_case_simulations.json"
        if sims.exists():
            for c in json.loads(sims.read_text(encoding="utf-8")).get("cases", []):
                if c.get("id") == cid:
                    return _from_json_case(c, "1000_engineering_simulations")
    raise SystemExit(f"Case '{case_identifier}' not found. Use ENG-0001..ENG-1000, ENG100K-xxxxxx, "
                     f"ENG1M-xxxxxxx, or a path to a PDF/MD/TXT/JSON brief or case directory.")


# --------------------------------------------------------------------------------------
# Agent 06: economics (shared by every deliverable)
# --------------------------------------------------------------------------------------
def unit_value(case: dict, override: float | None = None) -> tuple[float | None, str]:
    """CAD value of one unit of improvement; None means 'anchor to budget' (non-monetary metric)."""
    if override is not None:
        return override, "user override (--unit-value)"
    return UNIT_VALUES.get(case["baseline_unit"].strip().lower(), (None, ""))


def annual_benefit(case: dict, improvement_pct: float, uv: float | None) -> float:
    if uv is None:  # non-monetary metric: value scales with share of target achieved
        return ANCHOR_SHARE * case["budget"] * (improvement_pct / case["target_pct"] if case["target_pct"] else 0)
    return case["baseline_value"] * improvement_pct / 100 * uv


def levelized_cost(case: dict, capex: float, improvement_pct: float) -> tuple[float | None, str]:
    """Annualised cost (capital recovery + O&M) per unit of improvement delivered each year."""
    crf = WACC * (1 + WACC) ** HORIZON_YEARS / ((1 + WACC) ** HORIZON_YEARS - 1)
    annual_cost = capex * crf + capex * OM_RATE
    unit = case["baseline_unit"].strip().lower()
    per_year = {"units/day": OPERATING_DAYS, "cad/month": 12}.get(unit, 1)
    labels = {"units/day": "CAD per added unit", "kwh/year": "CAD per kWh saved", "tonnes co2e/year": "CAD per tCO2e abated",
              "cad/month": "CAD spent per CAD saved", "cad/year": "CAD spent per CAD saved"}
    if unit in labels:
        units = case["baseline_value"] * improvement_pct / 100 * per_year
        return (annual_cost / units if units else None), labels[unit]
    return (annual_cost / improvement_pct if improvement_pct else None), "CAD per year per % point of improvement"


def _npv(flows: list[float], rate: float) -> float:
    return sum(f / (1 + rate) ** t for t, f in enumerate(flows))


def _irr(flows: list[float]) -> float | None:
    lo, hi = -0.99, 50.0
    if _npv(flows, lo) * _npv(flows, hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if _npv(flows, lo) * _npv(flows, mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def cash_model(capex: float, benefit: float, timeline_months: int, om_rate: float = OM_RATE) -> dict:
    """Annual flows (Excel-replicable) + monthly payback. Benefit ramps at PILOT_SHARE until go-live."""
    T, om = timeline_months, capex * om_rate
    years = []
    for y in range(1, HORIZON_YEARS + 1):
        full = max(0, min(12, 12 * y - T))
        gross = benefit / 12 * (full + PILOT_SHARE * (12 - full))
        years.append({"year": y, "gross_benefit": gross, "om": om, "net": gross - om})
    flows = [-capex] + [y["net"] for y in years]
    cum, payback = -capex, None
    for m in range(1, HORIZON_YEARS * 12 + 1):
        step = benefit / 12 * (PILOT_SHARE if m <= T else 1.0) - om / 12
        if cum + step >= 0 and step > 0:
            payback = m - 1 + (-cum / step)
            break
        cum += step
    irr = _irr(flows)
    pv_benefits = _npv([0] + [y["gross_benefit"] for y in years], WACC)
    pv_costs = capex + _npv([0] + [y["om"] for y in years], WACC)
    return {"years": years, "flows": flows, "npv": _npv(flows, WACC),
            "irr": irr * 100 if irr is not None else None, "payback_months": payback,
            "bcr": pv_benefits / pv_costs if pv_costs else None}


# --------------------------------------------------------------------------------------
# Agent 05: option evaluation
# --------------------------------------------------------------------------------------
def evaluate_options(case: dict, uv: float | None) -> list[dict]:
    target, budget = case["target_pct"], case["budget"]
    opts = []
    for o in case["options"]:
        base = cash_model(o["capex"], annual_benefit(case, o["improvement"], uv), case["timeline_months"])
        opts.append({**o, "model": base, "within_budget": o["capex"] <= budget,
                     "meets_target": o["improvement"] >= target})
    npvs = [o["model"]["npv"] for o in opts]
    lo, hi = min(npvs), max(npvs)
    for o in opts:
        pb = o["model"]["payback_months"]
        s = {
            "Target attainment": 10 * min(o["improvement"] / target, 1.5) / 1.5 if target else 5,
            "Financial return (NPV)": 2 + 8 * ((o["model"]["npv"] - lo) / (hi - lo)) if hi > lo else 6,
            "Payback speed": 10 * max(0.0, 1 - pb / (HORIZON_YEARS * 12)) if pb is not None else 0,
            "Downside resilience (-15% perf.)": 10 * min(1.0, o["improvement"] * BEAR["perf"] / target) if target else 5,
            "Budget headroom": 10 * max(0.0, 1 - o["capex"] / budget) if budget else 0,
        }
        o["scores"] = {k: round(v, 2) for k, v in s.items()}
        o["weighted"] = round(sum(o["scores"][k] * w for k, w in CRITERIA), 2)
    feasible = [o for o in opts if o["within_budget"]] or sorted(opts, key=lambda x: x["capex"])[:1]
    winner = max(feasible, key=lambda x: (x["meets_target"], x["weighted"]))
    for o in opts:
        o["selected"] = o is winner
    return opts


def sensitivity(case: dict, win: dict, uv: float | None) -> list[dict]:
    """Tornado: NPV swing for +/-20 % on each driver, holding the others at base."""
    def npv_with(capex=1.0, ben=1.0, timeline=1.0, om=1.0):
        b = annual_benefit(case, win["improvement"], uv) * ben
        return cash_model(win["capex"] * capex, b, max(1, round(case["timeline_months"] * timeline)), OM_RATE * om)["npv"]
    rows = [
        ("Annual benefit: achieved gain x unit value (+/-20%)", npv_with(ben=0.8), npv_with(ben=1.2)),
        ("O&M cost (x2 / x0.5)", npv_with(om=2.0), npv_with(om=0.5)),
        ("Capital cost (+20% / -20%)", npv_with(capex=1.2), npv_with(capex=0.8)),
        ("Implementation duration (+50% / -25%)", npv_with(timeline=1.5), npv_with(timeline=0.75)),
    ]
    out = [{"driver": d, "low_npv": lo, "high_npv": hi, "swing": abs(hi - lo)} for d, lo, hi in rows]
    return sorted(out, key=lambda r: -r["swing"])


# --------------------------------------------------------------------------------------
# Agents 03, 08, 09: diagnosis, roadmap, red team
# --------------------------------------------------------------------------------------
def diagnose(case: dict) -> tuple[str, list[str]]:
    metric = case["baseline_metric"].lower()
    bottleneck = (f"{case['baseline_metric']} sits at {num(case['baseline_value'])} {case['baseline_unit']} and must move "
                  f"{case['target_pct']:g}% within {case['timeline_months']} months under {cad(case['budget'])}"
                  + (f" ({case['context']})." if case["context"] else "."))
    causes = [
        f"Binding constraint hypothesis: one stage or subsystem limits {metric}; confirm with {case['suggested_analysis'] or 'constraint analysis'} before committing capital.",
        "Variability, not average capacity, drives the gap: measure cycle/load variance and its share of lost performance.",
        "Control and information gap: performance is managed on lagging data, so deviations are corrected late.",
    ]
    if case["constraints"]:
        causes.append(f"Delivery constraint shaping the solution space: {case['constraints'][0]}.")
    return bottleneck, causes


def build_horizons(case: dict, win: dict) -> list[dict]:
    T, capex, tgt = case["timeline_months"], win["capex"], case["target_pct"]
    cut1, cut2 = max(1, round(T * 0.25)), max(2, round(T * 0.75))
    if cut2 <= cut1:
        cut2 = cut1 + 1
    rng = lambda a, b: f"Month {a}" if a == b else f"Months {a}-{b}"
    end2, start3 = min(cut2, T), min(cut2 + 1, T)
    return [
        {"horizon": "Horizon 1", "timeline": rng(1, cut1), "name": "Baseline validation & pilot",
         "budget_CAD": round(capex * 0.20), "kpi": f"Pilot reaches >= {tgt * 0.3:.1f}% improvement; data quality verified",
         "gate": "Go/no-go: pilot result within 20% of model, no safety incidents"},
        {"horizon": "Horizon 2", "timeline": rng(cut1 + 1, end2), "name": f"Scale-up: {win['name']}",
         "budget_CAD": round(capex * 0.60), "kpi": f">= {tgt * 0.8:.1f}% improvement sustained for 4 weeks",
         "gate": "Commissioning sign-off and availability at or above constraint"},
        {"horizon": "Horizon 3", "timeline": rng(start3, T), "name": "Stabilise, optimise & hand over",
         "budget_CAD": round(capex) - round(capex * 0.20) - round(capex * 0.60),
         "kpi": f"Full target {tgt:g}% reached; O&M within {cad(capex * OM_RATE)}/yr",
         "gate": "Benefit-tracking dashboard owned by operations"},
    ]


def build_risks(case: dict, win: dict, scen: list[dict]) -> list[dict]:
    bear = next(s for s in scen if s["name"].startswith("Bear"))
    return [
        {"risk": "Delivered improvement below model", "likelihood": "Medium", "impact": "High",
         "mitigation": f"Stage-gated rollout; bear case still yields {pct(bear['improvement'])} vs {case['target_pct']:g}% target",
         "trigger": "Pilot result < 80% of modelled gain"},
        {"risk": "Capital overrun", "likelihood": "Medium", "impact": "Medium",
         "mitigation": f"{cad(case['budget'] - win['capex'])} headroom to budget ceiling; fixed-price packages for long-lead items",
         "trigger": "Committed cost > 90% of H2 allocation"},
        {"risk": "Schedule slip / installation window", "likelihood": "Medium", "impact": "Medium",
         "mitigation": "Pre-fabrication and off-shift installation; pilot proves method before scale-up",
         "trigger": "Critical-path float < 2 weeks"},
        {"risk": "Safety or compliance non-conformance", "likelihood": "Low", "impact": "Critical",
         "mitigation": "Management-of-change review and HAZOP before each commissioning step",
         "trigger": "Any open MOC action at gate review"},
        {"risk": "Adoption / operating discipline", "likelihood": "Medium", "impact": "Medium",
         "mitigation": "Operators co-design standard work; KPI dashboard reviewed weekly",
         "trigger": "Benefit decays > 10% after go-live"},
    ]


def build_red_team(case: dict, opts: list[dict], win: dict, scen: list[dict], tornado: list[dict]) -> list[dict]:
    bear = next(s for s in scen if s["name"].startswith("Bear"))
    cut_budget = case["budget"] * 0.8
    still_fit = [o for o in opts if o["capex"] <= cut_budget]
    top = tornado[0]

    def answer(q: str) -> str:
        ql = q.lower()
        if "budget" in ql or "cut" in ql:
            if win["capex"] <= cut_budget:
                return f"A 20% cut leaves {cad(cut_budget)}; {win['name']} at {cad(win['capex'])} still fits, so the recommendation holds."
            alt = max(still_fit, key=lambda o: o["weighted"]) if still_fit else None
            return (f"A 20% cut leaves {cad(cut_budget)}, below the {cad(win['capex'])} needed. We would phase: fund Horizon 1-2 now"
                    + (f", or fall back to Option {alt['label']} ({alt['improvement']:g}% gain, {cad(alt['capex'])})." if alt else "."))
        if "15%" in ql or "performance" in ql or "cost" in ql or "rise" in ql:
            return (f"Bear case (performance -15%, capex +20%): {pct(bear['improvement'])} improvement, NPV {cad(bear['npv'])}, "
                    f"payback {months(bear['payback_months'])}. "
                    + ("Target is still met." if bear["meets_target"] else "Target would be missed, so the H1 pilot gate exists to catch this before scale-up spend."))
        if "sensitive" in ql or "assumption" in ql:
            return (f"{top['driver']}: NPV ranges {cad(top['low_npv'])} to {cad(top['high_npv'])}. "
                    "We reject the option if the H1 pilot delivers < 80% of modelled gain.")
        if "stakeholder" in ql:
            return "Operations carries the most delivery risk (installation windows, new standard work); they own the H2 commissioning gate and co-design the change."
        if "falsify" in ql or "test" in ql or "hypothesis" in ql:
            return f"The H1 pilot: if the pilot area does not reach {case['target_pct'] * 0.3:.1f}% improvement with measured variance reduction, the binding-constraint hypothesis is wrong."
        return (f"{win['name']} scores {win['weighted']}/10 and is the best option within budget; NPV {cad(win['model']['npv'])}, "
                f"payback {months(win['model']['payback_months'])}. Stage gates limit downside.")

    qs = list(case["judge_questions"]) or []
    defaults = [
        "How does your recommendation change if performance falls 15% and costs rise 20%?",
        "What is the most sensitive assumption, and what would make you reject the chosen option?",
        "How would your recommendation change if the budget were cut another 20%?",
        "Which stakeholder carries the greatest implementation risk?",
    ]
    for d in defaults:
        if len(qs) >= 5:
            break
        if not any(k in " ".join(qs).lower() for k in d.lower().split()[2:4]):
            qs.append(d)
    return [{"question": q, "rebuttal": answer(q)} for q in qs[:5]]


# --------------------------------------------------------------------------------------
# Agent 00: single source of truth
# --------------------------------------------------------------------------------------
def build_solution_spec(case: dict, unit_value_override: float | None = None) -> dict:
    uv, uv_src = unit_value(case, unit_value_override)
    opts = evaluate_options(case, uv)
    win = next(o for o in opts if o["selected"])
    benefit = annual_benefit(case, win["improvement"], uv)
    m = win["model"]

    scen = []
    for name, f in [("Bear (-15% perf., +20% capex)", BEAR), ("Base (approved plan)", {"perf": 1, "capex": 1}),
                    ("Bull (+15% perf., -10% capex)", BULL)]:
        imp = win["improvement"] * f["perf"]
        sm = cash_model(win["capex"] * f["capex"], annual_benefit(case, imp, uv), case["timeline_months"])
        scen.append({"name": name, "improvement": imp, "capex": win["capex"] * f["capex"], "npv": sm["npv"],
                     "irr": sm["irr"], "payback_months": sm["payback_months"], "meets_target": imp >= case["target_pct"]})
    tornado = sensitivity(case, win, uv)
    lc, lc_label = levelized_cost(case, win["capex"], win["improvement"])
    economic = case["baseline_unit"].strip().lower() in ECONOMIC_UNITS
    bottleneck, causes = diagnose(case)
    target_abs = case["baseline_value"] * case["target_pct"] / 100

    assumptions = [
        ("Baseline", f"{num(case['baseline_value'])} {case['baseline_unit']}", case["provenance"].get("baseline_value", "case datum")),
        ("Target improvement", f"{case['target_pct']:g}%", case["provenance"].get("target_pct", "case datum")),
        ("Capital budget", cad(case["budget"]), case["provenance"].get("budget", "case datum")),
        ("Timeline", f"{case['timeline_months']} months", case["provenance"].get("timeline_months", "case datum")),
        ("Option costs & gains", "see options table", case["provenance"].get("options", "case datum")),
        ("Monetisation", uv_src if uv is not None else f"non-monetary metric: full target valued at {ANCHOR_SHARE:.0%} of budget per year",
         "case datum" if "case datum" in uv_src else "assumption"),
        ("Discount rate (WACC)", f"{WACC:.1%}", "assumption (mid-cap industrial hurdle)"),
        ("Appraisal horizon", f"{HORIZON_YEARS} years", "assumption"),
        ("Annual O&M", f"{OM_RATE:.0%} of capex", "assumption"),
        ("Benefit during implementation", f"{PILOT_SHARE:.0%} of full run-rate", "assumption (pilot ramp)"),
    ]
    if not win["meets_target"]:
        hitters = [o for o in opts if o["meets_target"]]
        gap_note = (f" No in-budget option reaches the {case['target_pct']:g}% target"
                    + (f"; Option {hitters[0]['label']} would ({hitters[0]['improvement']:g}%) but needs {cad(hitters[0]['capex'])},"
                       f" {cad(hitters[0]['capex'] - case['budget'])} over budget. Recommend Option {win['label']} as phase 1"
                       f" and a funded decision on the gap at the H1 gate." if hitters else
                       ". Recommend the best in-budget option and renegotiate the target with evidence from the H1 pilot."))
    else:
        gap_note = ""
    weak = [a for a in assumptions if a[2].startswith("assumption") or "parametric" in a[2]]

    spec = {
        "version": "2.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "case_identification": {"id": case["id"], "title": case["title"], "discipline": case["discipline"],
                                "difficulty": case["difficulty"], "source_type": case["source_type"]},
        "case_inputs": {k: case[k] for k in ("brief", "decision_question", "objective", "baseline_metric",
                                             "baseline_value", "baseline_unit", "target_metric", "target_pct",
                                             "budget", "timeline_months", "constraints", "suggested_analysis", "rubric")},
        "problem_diagnosis": {"core_bottleneck": bottleneck, "baseline_value": case["baseline_value"],
                              "baseline_unit": case["baseline_unit"], "baseline_metric": case["baseline_metric"],
                              "target_improvement_percent": case["target_pct"],
                              "target_absolute_change": round(target_abs, 2), "root_causes": causes},
        "options_evaluation": {
            "criteria": [{"name": n, "weight": w} for n, w in CRITERIA],
            "options": [{"label": o["label"], "name": o["name"], "capex_CAD": round(o["capex"]),
                         "improvement_percent": o["improvement"], "source": o["source"],
                         "within_budget": o["within_budget"], "meets_target": o["meets_target"],
                         "npv_CAD": round(o["model"]["npv"]), "payback_months": _r(o["model"]["payback_months"]),
                         "scores": o["scores"], "weighted_total": o["weighted"], "selected": o["selected"]} for o in opts],
            "winner": win["label"],
        },
        "approved_solution": {
            "label": win["label"], "name": win["name"],
            "value_proposition": (f"Option {win['label']} — {win['name']} — delivers {win['improvement']:g}% {case['target_metric'].lower()} "
                                  f"(target {case['target_pct']:g}%) for {cad(win['capex'])} of the {cad(case['budget'])} budget: "
                                  f"NPV {cad(m['npv'])} at {WACC:.1%}, payback {months(m['payback_months'])}." + gap_note),
            "pillars": [
                {"name": "Prove the constraint (H1 pilot)", "impact": f">= {case['target_pct'] * 0.3:.1f}% in pilot area"},
                {"name": f"Scale {win['name'][:48]}", "impact": f"+{win['improvement']:g}% {case['baseline_metric'].lower()}"},
                {"name": "Lock in with control & KPIs", "impact": f"{cad(benefit)}/yr run-rate benefit"},
            ],
        },
        "financial_summary": {
            "initial_investment_CAD": round(win["capex"]), "budget_CAD": round(case["budget"]),
            "annual_run_rate_benefit_CAD": round(benefit), "annual_om_CAD": round(win["capex"] * OM_RATE),
            **{f"year_{y['year']}_revenue_CAD": round(y["gross_benefit"]) for y in m["years"][:3]},
            **{f"year_{y['year']}_net_CAD": round(y["net"]) for y in m["years"]},
            "year_3_ebitda_CAD": round(m["years"][2]["net"]),
            "npv_CAD": round(m["npv"]), "npv_10yr_discount_CAD": round(m["npv"]),
            "irr_percent": _r(m["irr"]), "payback_period_months": _r(m["payback_months"]),
            "benefit_cost_ratio": _r(m["bcr"], 2),
            "levelized_cost": _r(lc, 2), "levelized_cost_unit": lc_label,
            "economic_case": "profit-driven" if economic else "mandate-driven (judge on cost-effectiveness, not NPV alone)",
            "wacc_percent": WACC * 100, "horizon_years": HORIZON_YEARS,
            "cash_flows_CAD": [round(f) for f in m["flows"]],
        },
        "scenarios": [{**s, "npv": round(s["npv"]), "capex": round(s["capex"]), "irr": _r(s["irr"]),
                       "payback_months": _r(s["payback_months"]), "improvement": round(s["improvement"], 2)} for s in scen],
        "sensitivity": [{**t, "low_npv": round(t["low_npv"]), "high_npv": round(t["high_npv"]), "swing": round(t["swing"])} for t in tornado],
        "assumptions": [{"parameter": a, "value": v, "source": s} for a, v, s in assumptions],
        "weak_assumptions": [a for a, _, _ in weak],
        "implementation_horizons": build_horizons(case, win),
        "risks": build_risks(case, win, scen),
        "red_team_defense": build_red_team(case, opts, win, scen, tornado),
    }
    spec["intelligence"] = build_intelligence(case, spec)
    return spec


def _r(x, d: int = 1):
    return round(x, d) if x is not None else None


# --------------------------------------------------------------------------------------
# Markdown deliverables (Agents 01-09)
# --------------------------------------------------------------------------------------
def _options_rows(spec):
    return [[f"{o['label']}{' ✔' if o['selected'] else ''}", o["name"], cad(o["capex_CAD"]), f"{o['improvement_percent']:g}%",
             "yes" if o["within_budget"] else "NO", "yes" if o["meets_target"] else "no", cad(o["npv_CAD"]),
             months(o["payback_months"]), o["weighted_total"]] for o in spec["options_evaluation"]["options"]]


OPT_HEADERS = ["Opt", "Alternative", "Capex", "Gain", "In budget", "Meets target", "NPV", "Payback", "Score /10"]


def write_markdown_set(spec: dict) -> None:
    ci, fs, pdg, sol = spec["case_identification"], spec["financial_summary"], spec["problem_diagnosis"], spec["approved_solution"]
    inp, R = spec["case_inputs"], OUTPUT_ROOT
    win = next(o for o in spec["options_evaluation"]["options"] if o["selected"])
    rejected = [o for o in spec["options_evaluation"]["options"] if not o["selected"]]

    # 00 overview
    write_text(R / "00_Project_Overview/README.md", f"""
# {ci['title']}
**Case** {ci['id']} · {ci['discipline']} · {ci['difficulty']} · source: {ci['source_type']}

**Recommendation:** {sol['value_proposition']}

Start with `04_Final_Strategy/executive_summary.md`, then `06_PDF_Deliverables/`, `07_PowerPoint/`, and
`11_Final_Quality_Control/compliance_checklist.md`. All figures come from `solution_spec.json`.
""")
    write_text(R / "00_Project_Overview/execution_summary.md", f"""
# Execution Summary
- Generated: {spec['generated_at']}
- Options evaluated: {len(spec['options_evaluation']['options'])} · winner: Option {win['label']} ({win['weighted_total']}/10)
- NPV {cad(fs['npv_CAD'])} · IRR {pct(fs['irr_percent'])} · payback {months(fs['payback_period_months'])} · B/C {fs['benefit_cost_ratio']}
- Weak assumptions to validate: {', '.join(spec['weak_assumptions']) or 'none'}
""")

    # 01 case intelligence
    write_text(R / "01_Case_Intelligence/case_summary.md", f"""
# Case Intelligence Report: {ci['title']}
**Discipline**: {ci['discipline']} | **Difficulty**: {ci['difficulty']}

### Problem Statement
{inp['brief']}

### Core Decision Question
{inp['decision_question']}

### Objective
{inp['objective']}

### Quantified Gap
{pdg['core_bottleneck']} Absolute change required: {num(pdg['target_absolute_change'])} {pdg['baseline_unit']}.

### Stated Constraints
""" + "\n".join(f"- {c}" for c in inp["constraints"]))
    write_text(R / "01_Case_Intelligence/problem_statement.md", f"# Problem Statement\n\n{inp['decision_question']}\n\n{pdg['core_bottleneck']}")
    (R / "01_Case_Intelligence/case_data.json").write_text(json.dumps(inp, indent=2), encoding="utf-8")
    write_text(R / "01_Case_Intelligence/assumptions_register.md", "# Assumptions Register\n\n" + md_table(
        ["Parameter", "Value", "Source"], [[a["parameter"], a["value"], a["source"]] for a in spec["assumptions"]]))
    rubric = inp.get("rubric") or {"Strategy": 25, "Financials": 25, "Implementation": 20, "Risk": 15, "Q&A defence": 15}
    write_text(R / "01_Case_Intelligence/judging_rubric.md", "# Judging Rubric\n\n" + md_table(
        ["Criterion", "Points"], [[k.replace("_", " ").title(), v] for k, v in rubric.items()]))

    # 02 research
    write_text(R / "02_Research/competitor_analysis.md", "# Alternatives Benchmark\n\n" + md_table(OPT_HEADERS, _options_rows(spec)))
    write_text(R / "02_Research/evidence_summary.md", "# Evidence Summary\n\nCase data versus modelling assumptions:\n\n" + md_table(
        ["Parameter", "Value", "Source"], [[a["parameter"], a["value"], a["source"]] for a in spec["assumptions"]]))
    write_text(R / "02_Research/market_research.md", f"""
# Method & Benchmark Notes
- Suggested analysis for this case: {inp['suggested_analysis'] or 'constraint analysis + discounted cash flow'}
- Winning-solution pattern from the master system: quantified baseline, three costed options, explicit weighted
  decision, stage-gated rollout, and pre-computed answers to stress questions.
- See `docs/CASE_COMPETITION_MASTER_SYSTEM.md` for the 100-point rubric and deck blueprint.
""")
    with open(R / "02_Research/source_register.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Claim ID", "Claim", "Source", "Status"])
        w.writerow(["CLM-001", f"Baseline {num(pdg['baseline_value'])} {pdg['baseline_unit']}", "Case brief", "Case datum"])
        w.writerow(["CLM-002", f"Target {pdg['target_improvement_percent']:g}%", "Case brief", "Case datum"])
        w.writerow(["CLM-003", f"Budget {cad(fs['budget_CAD'])}", "Case brief", "Case datum"])
        w.writerow(["CLM-004", f"Winner capex {cad(fs['initial_investment_CAD'])}, gain {win['improvement_percent']:g}%", win["source"], "Input"])
        w.writerow(["CLM-005", f"NPV {cad(fs['npv_CAD'])}", "financial_model.xlsx (computed)", "Calculated"])
        w.writerow(["CLM-006", f"Payback {months(fs['payback_period_months'])}", "monthly cash model (computed)", "Calculated"])

    # 03 brainstorming
    write_text(R / "03_Brainstorming/idea_clusters.md", "# Root-Cause Hypotheses & Idea Clusters\n\n" +
               "\n".join(f"{i}. {c}" for i, c in enumerate(pdg["root_causes"], 1)) +
               "\n\nClusters: (A) operate the existing system better, (B) targeted retrofit of the constraint, (C) new capacity / architecture.")
    write_text(R / "03_Brainstorming/all_ideas.md", "# All Ideas Considered\n\n" + "\n".join(
        f"- **Option {o['label']}** — {o['name']} ({cad(o['capex_CAD'])}, {o['improvement_percent']:g}%)" for o in spec["options_evaluation"]["options"]))
    write_text(R / "03_Brainstorming/selected_strategy.md", f"# Selected Strategy\n\n{sol['value_proposition']}\n\nWeighted score: {win['weighted_total']}/10.")
    write_text(R / "03_Brainstorming/rejected_ideas.md", "# Rejected Options\n\n" + "\n".join(
        f"- **Option {o['label']} — {o['name']}** ({o['weighted_total']}/10): "
        + ("exceeds budget" if not o["within_budget"] else "misses target" if not o["meets_target"] else "lower weighted score")
        + f"; NPV {cad(o['npv_CAD'])}." for o in rejected))

    # 04 final strategy
    h_rows = [[h["horizon"], h["timeline"], h["name"], cad(h["budget_CAD"]), h["kpi"], h["gate"]] for h in spec["implementation_horizons"]]
    write_text(R / "04_Final_Strategy/executive_summary.md", f"""
# Executive Summary — {ci['title']}

**Answer first.** {sol['value_proposition']}

**Why it wins.** It is the highest-scoring option that fits the budget{' and meets the target' if win['meets_target'] else ' (note: it does not fully meet the target; see risks)'}.

{md_table(OPT_HEADERS, _options_rows(spec))}

**Economics.** Run-rate benefit {cad(fs['annual_run_rate_benefit_CAD'])}/yr, O&M {cad(fs['annual_om_CAD'])}/yr, IRR {pct(fs['irr_percent'])},
benefit/cost {fs['benefit_cost_ratio']}. Bear case NPV {cad(spec['scenarios'][0]['npv'])}.
Cost-effectiveness: {fs['levelized_cost']} {fs['levelized_cost_unit']} — this is a {fs['economic_case']} case.

**Plan.** {' → '.join(h['name'] for h in spec['implementation_horizons'])} over {inp['timeline_months']} months.
""")
    write_text(R / "04_Final_Strategy/winning_solution.md", f"# Winning Solution\n\n{sol['value_proposition']}\n\n" + "\n".join(
        f"- **{p['name']}** — {p['impact']}" for p in sol["pillars"]))
    write_text(R / "04_Final_Strategy/solution_architecture.md", f"""
# Solution Architecture — Option {win['label']}: {win['name']}
1. **Measure**: instrument the constraint; establish baseline {num(pdg['baseline_value'])} {pdg['baseline_unit']} with variance.
2. **Intervene**: implement {win['name'].lower()} at the binding constraint first (H1 pilot), then scale (H2).
3. **Control**: KPI dashboard with leading indicators (variance, availability) and lagging result ({pdg['baseline_metric'].lower()}).
4. **Sustain**: standard work, O&M plan ({cad(fs['annual_om_CAD'])}/yr), benefit tracking owned by operations.
""")
    write_text(R / "04_Final_Strategy/implementation_plan.md", "# Implementation Plan\n\n" + md_table(
        ["Horizon", "Timing", "Workstream", "Budget", "KPI", "Gate"], h_rows))
    write_text(R / "04_Final_Strategy/risk_analysis.md", "# Risk Register\n\n" + md_table(
        ["Risk", "Likelihood", "Impact", "Mitigation", "Trigger"],
        [[r["risk"], r["likelihood"], r["impact"], r["mitigation"], r["trigger"]] for r in spec["risks"]]))
    write_text(R / "04_Final_Strategy/validation_results.md", "# Validation — Scenarios & Sensitivity\n\n" + md_table(
        ["Scenario", "Gain", "Capex", "NPV", "IRR", "Payback", "Meets target"],
        [[s["name"], f"{s['improvement']:g}%", cad(s["capex"]), cad(s["npv"]), pct(s["irr"]), months(s["payback_months"]),
          "yes" if s["meets_target"] else "no"] for s in spec["scenarios"]]) + "\n\n## NPV sensitivity (tornado)\n\n" + md_table(
        ["Driver", "Low NPV", "High NPV", "Swing"], [[t["driver"], cad(t["low_npv"]), cad(t["high_npv"]), cad(t["swing"])] for t in spec["sensitivity"]]))

    # 05 assumptions doc
    write_text(R / "05_Financial_Models/financial_assumptions.md", "# Financial Assumptions\n\n" + md_table(
        ["Parameter", "Value", "Source"], [[a["parameter"], a["value"], a["source"]] for a in spec["assumptions"]]))

    # 04 case decrypt (how the case was cracked)
    it = spec["intelligence"]
    sq = it["scqa"]
    write_text(R / "04_Final_Strategy/case_decrypt.md", f"""
# Case Decrypt — {ci['title']}
**Archetype:** {it['archetype_name']} · **Family:** {it['family_label']}
**Solution model:** {it['solution_model']}

> {it['what_the_case_tests']}

## SCQA
- **Situation:** {sq['situation']}
- **Complication:** {sq['complication']}
- **Question:** {sq['question']}
- **Answer:** {sq['answer']}

## Issue tree
**{it['issue_tree']['root']}**
""" + "\n".join(f"- **{b['name']}**: " + " / ".join(b["questions"]) for b in it["issue_tree"]["branches"]) + f"""

## Hypothesis (first 20 minutes)
{it['hypothesis']}

## Toolkit & quick math
""" + "\n".join(f"- {t}" for t in it["toolkit"] + it["quick_math"]) + """

## Solution ladder
""" + md_table(["Level", "Name", "Rule", "Pick"], [[r["level"], r["name"], r["rule"], r["summary"]] for r in it["solution_ladder"]])
        + f"\n\n**Why the recommendation:** {it['ladder_rationale']}\n\n## KPIs\n"
        + md_table(["KPI", "Baseline", "Target"], [[k["kpi"], k["baseline"], k["target"]] for k in it["kpis"]])
        + "\n\n## 30 / 60 / 90 days\n" + "\n".join(f"- **{p['window']} — {p['focus']}:** " + "; ".join(p["actions"]) for p in it["plan_30_60_90"])
        + "\n\n## Time plan (5-hour window)\n" + md_table(["Time", "Step", "Output"], [[t["time"], t["step"], t["output"]] for t in it["time_plan"]])
        + "\n\n## Similar competitions (directory-listed; winners not verified)\n"
        + "\n".join(f"- {c['competition']} ({c['region']}, {c['focus']})" for c in it["similar_competitions"]))

    # 07 Q&A
    write_text(R / "07_PowerPoint/judge_QA_preparation.md", "# Judge Q&A Preparation\n\n" + "\n\n".join(
        f"### [{qa.get('category', 'Q&A')}] {qa['question']}\n**A:** {qa['rebuttal']}" for qa in spec["intelligence"]["qa_bank"]))
    write_text(R / "11_Final_Quality_Control/submission_checklist.md", "# Pre-Submission Checklist\n\n" + "\n".join(
        f"- [{'x' if c['ok'] else ' '}] **{c['item']}** — {c['evidence']}" for c in spec["intelligence"]["submission_checklist"]))


# --------------------------------------------------------------------------------------
# Agents 05/06: Excel workbooks (formulas carry cached values so they read without recalculation)
# --------------------------------------------------------------------------------------
def write_evaluation_matrix(spec: dict) -> None:
    import xlsxwriter
    opts = spec["options_evaluation"]["options"]
    wb = xlsxwriter.Workbook(str(OUTPUT_ROOT / "03_Brainstorming/evaluation_matrix.xlsx"))
    ws = wb.add_worksheet("Strategy_Evaluation")
    h = wb.add_format({"bold": True, "bg_color": "#1E3A8A", "font_color": "#FFFFFF", "border": 1, "text_wrap": True})
    c = wb.add_format({"border": 1, "num_format": "0.00"})
    b = wb.add_format({"bold": True, "border": 1, "bg_color": "#E0E7FF", "num_format": "0.00"})
    ws.write_row(0, 0, ["Criterion", "Weight"] + [f"Option {o['label']}: {o['name']}" for o in opts], h)
    for r, (name, weight) in enumerate(CRITERIA, start=1):
        ws.write(r, 0, name, c)
        ws.write(r, 1, weight, c)
        for j, o in enumerate(opts):
            ws.write(r, 2 + j, o["scores"][name], c)
    last = len(CRITERIA) + 1
    ws.write(last, 0, "Weighted total (/10)", b)
    ws.write_formula(last, 1, f"=SUM(B2:B{last})", b, 1.0)
    for j, o in enumerate(opts):
        col = chr(ord("C") + j)
        ws.write_formula(last, 2 + j, f"=SUMPRODUCT($B$2:$B${last},{col}2:{col}{last})", b, o["weighted_total"])
    ws.write(last + 2, 0, f"Selected: Option {spec['options_evaluation']['winner']} (highest score within budget)")
    ws.set_column(0, 0, 34)
    ws.set_column(1, 1, 9)
    ws.set_column(2, 4, 30)
    wb.close()


def write_financial_workbooks(spec: dict) -> None:
    import xlsxwriter
    fs, d = spec["financial_summary"], OUTPUT_ROOT / "05_Financial_Models"
    T = spec["case_inputs"]["timeline_months"]

    wb = xlsxwriter.Workbook(str(d / "financial_model.xlsx"))
    h = wb.add_format({"bold": True, "bg_color": "#0F172A", "font_color": "#FFFFFF", "border": 1})
    money = wb.add_format({"num_format": "$#,##0;[Red]-$#,##0", "border": 1})
    bmoney = wb.add_format({"bold": True, "num_format": "$#,##0;[Red]-$#,##0", "border": 1, "bg_color": "#FEF3C7"})
    pctf = wb.add_format({"num_format": "0.0%", "border": 1})
    inp = wb.add_format({"border": 1, "bg_color": "#DBEAFE"})
    cell = wb.add_format({"border": 1})

    a = wb.add_worksheet("Assumptions")
    a.write_row(0, 0, ["Input (blue = editable)", "Value"], h)
    rows = [("Capex (CAD)", fs["initial_investment_CAD"], money), ("Run-rate annual benefit (CAD)", fs["annual_run_rate_benefit_CAD"], money),
            ("O&M rate (share of capex)", OM_RATE, pctf), ("Benefit share during implementation", PILOT_SHARE, pctf),
            ("Implementation months", T, cell), ("WACC", WACC, pctf)]
    for i, (k, v, fm) in enumerate(rows, start=1):
        a.write(i, 0, k, cell)
        a.write(i, 1, v, inp if fm is cell else wb.add_format({**{"bg_color": "#DBEAFE", "border": 1}, "num_format": fm.num_format}))
    a.set_column(0, 0, 38)
    a.set_column(1, 1, 16)
    # Named cells: B2 capex, B3 benefit, B4 om, B5 pilot, B6 months, B7 wacc

    cf = wb.add_worksheet("Cash_Flow_5yr")
    cf.write_row(0, 0, ["CAD", "Year 0"] + [f"Year {y}" for y in range(1, HORIZON_YEARS + 1)], h)
    labels = ["Full-run-rate months", "Gross benefit", "O&M", "Net operating benefit", "Capex", "Net cash flow", "Cumulative"]
    for i, lab in enumerate(labels, start=1):
        cf.write(i, 0, lab, cell)
    cf.write_formula(5, 1, "=-Assumptions!B2", money, -fs["initial_investment_CAD"])
    cf.write_formula(6, 1, "=B6", bmoney, -fs["initial_investment_CAD"])
    cf.write_formula(7, 1, "=B7", money, -fs["initial_investment_CAD"])
    years = [fs[f"year_{y}_net_CAD"] for y in range(1, HORIZON_YEARS + 1)]
    cum = -fs["initial_investment_CAD"]
    for y in range(1, HORIZON_YEARS + 1):
        col, cl = 1 + y, chr(ord("B") + y)
        full = max(0, min(12, 12 * y - T))
        gross = fs["annual_run_rate_benefit_CAD"] / 12 * (full + PILOT_SHARE * (12 - full))
        cf.write_formula(1, col, f"=MAX(0,MIN(12,12*{y}-Assumptions!$B$6))", cell, full)
        cf.write_formula(2, col, f"=Assumptions!$B$3/12*({cl}2+Assumptions!$B$5*(12-{cl}2))", money, round(gross))
        cf.write_formula(3, col, "=-Assumptions!$B$2*Assumptions!$B$4", money, -fs["annual_om_CAD"])
        cf.write_formula(4, col, f"={cl}3+{cl}4", money, years[y - 1])
        cf.write(5, col, 0, money)
        cf.write_formula(6, col, f"={cl}5+{cl}6", bmoney, years[y - 1])
        cum += years[y - 1]
        prev = chr(ord(cl) - 1)
        cf.write_formula(7, col, f"={prev}8+{cl}7", money, round(cum))
    end = chr(ord("B") + HORIZON_YEARS)
    cf.write(9, 0, "NPV @ WACC", h)
    cf.write_formula(9, 1, f"=B7+NPV(Assumptions!B7,C7:{end}7)", bmoney, fs["npv_CAD"])
    cf.write(10, 0, "IRR", h)
    cf.write_formula(10, 1, f"=IFERROR(IRR(B7:{end}7),\"n/a\")", pctf, (fs["irr_percent"] or 0) / 100)
    cf.write(11, 0, "Payback (months, monthly model)", h)
    cf.write(11, 1, fs["payback_period_months"] if fs["payback_period_months"] is not None else f"> {HORIZON_YEARS * 12}", cell)
    cf.set_column(0, 0, 32)
    cf.set_column(1, 1 + HORIZON_YEARS, 15)

    sc = wb.add_worksheet("Scenarios")
    sc.write_row(0, 0, ["Scenario", "Improvement %", "Capex", "NPV", "IRR %", "Payback (months)", "Meets target"], h)
    for i, s in enumerate(spec["scenarios"], start=1):
        sc.write_row(i, 0, [s["name"], s["improvement"]], cell)
        sc.write(i, 2, s["capex"], money)
        sc.write(i, 3, s["npv"], money)
        sc.write_row(i, 4, [s["irr"] if s["irr"] is not None else "n/a",
                            s["payback_months"] if s["payback_months"] is not None else "n/a",
                            "yes" if s["meets_target"] else "no"], cell)
    sc.write_row(5, 0, ["Sensitivity driver", "Low NPV", "High NPV", "Swing"], h)
    for i, t in enumerate(spec["sensitivity"], start=6):
        sc.write(i, 0, t["driver"], cell)
        sc.write_row(i, 1, [t["low_npv"], t["high_npv"], t["swing"]], money)
    sc.set_column(0, 0, 38)
    sc.set_column(1, 6, 16)
    wb.close()

    # cost_breakdown.xlsx — capex by horizon and category
    wb = xlsxwriter.Workbook(str(d / "cost_breakdown.xlsx"))
    ws = wb.add_worksheet("Capex_by_Horizon")
    h = wb.add_format({"bold": True, "bg_color": "#0F172A", "font_color": "#FFFFFF", "border": 1})
    money = wb.add_format({"num_format": "$#,##0", "border": 1})
    ws.write_row(0, 0, ["Horizon", "Timing", "Workstream", "Budget (CAD)"], h)
    for i, hz in enumerate(spec["implementation_horizons"], start=1):
        ws.write_row(i, 0, [hz["horizon"], hz["timeline"], hz["name"]])
        ws.write(i, 3, hz["budget_CAD"], money)
    ws.write(4, 2, "Total")
    ws.write_formula(4, 3, "=SUM(D2:D4)", money, fs["initial_investment_CAD"])
    ws.write(5, 2, "Headroom to budget")
    ws.write_formula(5, 3, f"={fs['budget_CAD']}-D5", money, fs["budget_CAD"] - fs["initial_investment_CAD"])
    ws.write_row(7, 0, ["Category (assumed split)", "Share", "", "CAD"], h)
    for i, (cat, share) in enumerate([("Equipment & materials", 0.55), ("Engineering & integration", 0.25),
                                      ("Installation & commissioning", 0.10), ("Contingency", 0.10)], start=8):
        ws.write_row(i, 0, [cat, share])
        ws.write_formula(i, 3, f"=$D$5*B{i + 1}", money, round(fs["initial_investment_CAD"] * share))
    ws.write(13, 0, "Annual O&M")
    ws.write(13, 3, fs["annual_om_CAD"], money)
    ws.set_column(0, 2, 32)
    ws.set_column(3, 3, 16)
    wb.close()
    shutil.copyfile(d / "financial_model.xlsx", d / "scenario_analysis.xlsx")


# --------------------------------------------------------------------------------------
# Agent 10: PDFs via PyMuPDF Story (auto layout & pagination)
# --------------------------------------------------------------------------------------
PDF_CSS = """
body { font-family: sans-serif; font-size: 9.5pt; color: #1e293b; }
h1 { font-size: 18pt; color: #0f172a; margin: 0 0 4pt 0; }
h2 { font-size: 12pt; color: #1e3a8a; margin: 12pt 0 4pt 0; border-bottom: 1px solid #cbd5e1; }
p { margin: 3pt 0; line-height: 1.35; }
.meta { color: #64748b; font-size: 8.5pt; }
.callout { background-color: #eff6ff; padding: 6pt; border: 1px solid #bfdbfe; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0; }
th { background-color: #0f172a; color: #ffffff; font-size: 8pt; padding: 3pt; text-align: left; }
td { border: 1px solid #cbd5e1; font-size: 8pt; padding: 3pt; }
li { margin: 2pt 0; }
"""


def _esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _html_table(headers, rows) -> str:
    return ("<table><tr>" + "".join(f"<th>{_esc(h)}</th>" for h in headers) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{_esc(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>")


def _render_pdf(html: str, path: Path) -> None:
    import pymupdf
    story = pymupdf.Story(html=html, user_css=PDF_CSS)
    writer = pymupdf.DocumentWriter(str(path))
    page_rect, body = pymupdf.paper_rect("a4"), pymupdf.paper_rect("a4") + (42, 48, -42, -48)
    more = True
    while more:
        dev = writer.begin_page(page_rect)
        more, _ = story.place(body)
        story.draw(dev)
        writer.end_page()
    writer.close()


def generate_pdf_deliverables(spec: dict) -> None:
    ci, fs, pdg, sol, inp = (spec["case_identification"], spec["financial_summary"], spec["problem_diagnosis"],
                             spec["approved_solution"], spec["case_inputs"])
    head = f"<h1>{_esc(ci['title'])}</h1><p class='meta'>{_esc(ci['id'])} · {_esc(ci['discipline'])} · Strategy Consulting Hub</p>"
    kpis = _html_table(["Capex", "NPV @ WACC", "IRR", "Payback", "Benefit/Cost", "Run-rate benefit", "Levelized cost"],
                       [[cad(fs["initial_investment_CAD"]), cad(fs["npv_CAD"]), pct(fs["irr_percent"]),
                         months(fs["payback_period_months"]), fs["benefit_cost_ratio"], cad(fs["annual_run_rate_benefit_CAD"]) + "/yr",
                         f"{fs['levelized_cost']} {fs['levelized_cost_unit']}"]])
    blueprint = f"""{head}
<div class='callout'><p><b>Recommendation.</b> {_esc(sol['value_proposition'])}</p></div>
{kpis}
<h2>1. Problem diagnosis</h2><p>{_esc(pdg['core_bottleneck'])}</p>
<ul>{''.join(f'<li>{_esc(c)}</li>' for c in pdg['root_causes'])}</ul>
<h2>2. Options and decision</h2>{_html_table(OPT_HEADERS, _options_rows(spec))}
<p>Criteria and weights: {_esc(', '.join(f"{c['name']} {c['weight']:.0%}" for c in spec['options_evaluation']['criteria']))}. Budget is a hard gate.</p>
<h2>3. Five-year cash flow (CAD)</h2>{_html_table(['Year 0'] + [f'Year {y}' for y in range(1, HORIZON_YEARS + 1)], [[cad(f) for f in fs['cash_flows_CAD']]])}
<h2>4. Scenarios</h2>{_html_table(['Scenario', 'Gain', 'Capex', 'NPV', 'IRR', 'Payback', 'Meets target'],
    [[s['name'], f"{s['improvement']:g}%", cad(s['capex']), cad(s['npv']), pct(s['irr']), months(s['payback_months']), 'yes' if s['meets_target'] else 'no'] for s in spec['scenarios']])}
<h2>5. Sensitivity (NPV tornado)</h2>{_html_table(['Driver', 'Low NPV', 'High NPV', 'Swing'], [[t['driver'], cad(t['low_npv']), cad(t['high_npv']), cad(t['swing'])] for t in spec['sensitivity']])}
<h2>6. Implementation roadmap</h2>{_html_table(['Horizon', 'Timing', 'Workstream', 'Budget', 'KPI', 'Gate'], [[h['horizon'], h['timeline'], h['name'], cad(h['budget_CAD']), h['kpi'], h['gate']] for h in spec['implementation_horizons']])}
<h2>7. Risk register</h2>{_html_table(['Risk', 'L', 'I', 'Mitigation', 'Trigger'], [[r['risk'], r['likelihood'], r['impact'], r['mitigation'], r['trigger']] for r in spec['risks']])}
<h2>8. Judge defence</h2>{''.join(f"<p><b>Q: {_esc(q['question'])}</b><br/>{_esc(q['rebuttal'])}</p>" for q in spec['red_team_defense'])}
<h2>9. Assumptions</h2>{_html_table(['Parameter', 'Value', 'Source'], [[a['parameter'], a['value'], a['source']] for a in spec['assumptions']])}
"""
    _render_pdf(blueprint, OUTPUT_ROOT / "06_PDF_Deliverables/Strategic_Blueprint.pdf")

    memo = f"""{head}
<h2>Decision</h2><div class='callout'><p>{_esc(sol['value_proposition'])}</p></div>
<h2>Why this option</h2><p>{_esc(inp['decision_question'])}</p>{_html_table(OPT_HEADERS, _options_rows(spec))}
<h2>Economics</h2>{kpis}
<p>Bear case (performance -15%, capex +20%): NPV {cad(spec['scenarios'][0]['npv'])}, payback {months(spec['scenarios'][0]['payback_months'])}.</p>
<h2>Plan</h2><ul>{''.join(f"<li><b>{_esc(h['horizon'])} ({_esc(h['timeline'])})</b> — {_esc(h['name'])}, {cad(h['budget_CAD'])}. KPI: {_esc(h['kpi'])}</li>" for h in spec['implementation_horizons'])}</ul>
<h2>Top judge questions</h2>{''.join(f"<p><b>Q: {_esc(q['question'])}</b><br/>{_esc(q['rebuttal'])}</p>" for q in spec['red_team_defense'][:3])}
"""
    _render_pdf(memo, OUTPUT_ROOT / "06_PDF_Deliverables/Final_Case_Solution.pdf")


# --------------------------------------------------------------------------------------
# Agent 11: PowerPoint (12 slides, real content, editable tables)
# --------------------------------------------------------------------------------------
def generate_powerpoint_deck(spec: dict) -> None:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Inches, Pt

    NAVY, GOLD, WHITE, GRAY, INK, LIGHT = (RGBColor(15, 23, 42), RGBColor(217, 119, 6), RGBColor(255, 255, 255),
                                           RGBColor(100, 116, 139), RGBColor(30, 41, 59), RGBColor(248, 250, 252))
    ci, fs, pdg, sol, inp = (spec["case_identification"], spec["financial_summary"], spec["problem_diagnosis"],
                             spec["approved_solution"], spec["case_inputs"])
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    notes_md = ["# Speaker Notes\n"]

    def slide(title, subtitle="", bullets=None, dark=False, table=None, note=""):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        bg = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = NAVY if dark else LIGHT
        bg.line.fill.background()
        bar = s.shapes.add_shape(1, Inches(0.6), Inches(0.55), Inches(0.12), Inches(0.9))
        bar.fill.solid()
        bar.fill.fore_color.rgb = GOLD
        bar.line.fill.background()
        tf = s.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.8), Inches(1.4)).text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = title
        tf.paragraphs[0].font.size, tf.paragraphs[0].font.bold = Pt(30), True
        tf.paragraphs[0].font.color.rgb = WHITE if dark else NAVY
        if subtitle:
            p = tf.add_paragraph()
            p.text = subtitle
            p.font.size, p.font.color.rgb = Pt(15), GOLD if dark else GRAY
        top = Inches(2.05)
        if table:
            headers, rows = table
            shp = s.shapes.add_table(len(rows) + 1, len(headers), Inches(0.9), top, Inches(11.6), Inches(0.4) * (len(rows) + 1))
            for j, hd in enumerate(headers):
                shp.table.cell(0, j).text = str(hd)
            for i, r in enumerate(rows, start=1):
                for j, v in enumerate(r):
                    shp.table.cell(i, j).text = str(v)
            for row in shp.table.rows:
                for c in row.cells:
                    for p in c.text_frame.paragraphs:
                        p.font.size = Pt(12)
            top = top + Inches(0.42) * (len(rows) + 1) + Inches(0.25)
        if bullets:
            bf = s.shapes.add_textbox(Inches(0.9), top, Inches(11.6), Inches(7.0) - top).text_frame
            bf.word_wrap = True
            for i, b in enumerate(bullets):
                p = bf.paragraphs[0] if i == 0 else bf.add_paragraph()
                p.text = f"• {b}"
                p.font.size, p.space_after = Pt(17 if not table else 15), Pt(8)
                p.font.color.rgb = WHITE if dark else INK
        s.notes_slide.notes_text_frame.text = note or subtitle
        notes_md.append(f"### {len(prs.slides)}. {title}\n{note or subtitle}\n")

    opt_rows = [[f"{o['label']}{' ✔' if o['selected'] else ''}", o["name"][:44], cad(o["capex_CAD"]), f"{o['improvement_percent']:g}%",
                 cad(o["npv_CAD"]), months(o["payback_months"]), o["weighted_total"]] for o in spec["options_evaluation"]["options"]]
    bear = spec["scenarios"][0]
    slide(ci["title"], f"{ci['id']} · {ci['discipline']} · Executive Case Simulation Team", dark=True,
          bullets=[sol["value_proposition"]], note="Open with the answer, then prove it.")
    slide("1. The answer", "Recommendation in one sentence", bullets=[
        sol["value_proposition"], f"Benefit/cost {fs['benefit_cost_ratio']} · IRR {pct(fs['irr_percent'])}",
        f"Delivered in {inp['timeline_months']} months through three gated horizons"], note="State the recommendation and the three numbers judges remember.")
    slide("2. The problem, quantified", pdg["baseline_metric"], bullets=[pdg["core_bottleneck"],
          f"Required change: {num(pdg['target_absolute_change'])} {pdg['baseline_unit']} ({pdg['target_improvement_percent']:g}%)"]
          + inp["constraints"][:3])
    slide("3. Root-cause hypotheses", "What we must prove before spending at scale", bullets=pdg["root_causes"])
    slide("4. Three alternatives", "Costed and compared on the same basis",
          table=(["Opt", "Alternative", "Capex", "Gain", "NPV", "Payback", "Score"], opt_rows))
    slide("5. Decision logic", "Weighted criteria; budget is a hard gate", table=(
        ["Criterion", "Weight"] + [f"Opt {o['label']}" for o in spec["options_evaluation"]["options"]],
        [[c["name"], f"{c['weight']:.0%}"] + [o["scores"][c["name"]] for o in spec["options_evaluation"]["options"]]
         for c in spec["options_evaluation"]["criteria"]]))
    slide(f"6. Recommended: Option {sol['label']}", sol["name"], dark=True,
          bullets=[f"{p['name']} — {p['impact']}" for p in sol["pillars"]])
    slide("7. Five-year economics", f"NPV {cad(fs['npv_CAD'])} at {fs['wacc_percent']:.1f}% WACC", table=(
        ["", "Year 0"] + [f"Year {y}" for y in range(1, HORIZON_YEARS + 1)],
        [["Net cash flow"] + [cad(f) for f in fs["cash_flows_CAD"]]]), bullets=[
        f"Run-rate benefit {cad(fs['annual_run_rate_benefit_CAD'])}/yr; O&M {cad(fs['annual_om_CAD'])}/yr",
        f"Payback {months(fs['payback_period_months'])}; IRR {pct(fs['irr_percent'])}",
        f"Cost-effectiveness: {fs['levelized_cost']} {fs['levelized_cost_unit']} ({fs['economic_case'].split(' (')[0]})"])
    slide("8. Stress test", "Scenarios and the assumption that matters most", table=(
        ["Scenario", "Gain", "NPV", "Payback", "Meets target"],
        [[s["name"], f"{s['improvement']:g}%", cad(s["npv"]), months(s["payback_months"]), "yes" if s["meets_target"] else "no"]
         for s in spec["scenarios"]]), bullets=[f"Most sensitive: {spec['sensitivity'][0]['driver']} "
                                                f"(NPV {cad(spec['sensitivity'][0]['low_npv'])} to {cad(spec['sensitivity'][0]['high_npv'])})"])
    slide("9. Implementation roadmap", f"{inp['timeline_months']} months, three gated horizons", table=(
        ["Horizon", "Timing", "Workstream", "Budget", "Gate"],
        [[h["horizon"], h["timeline"], h["name"][:40], cad(h["budget_CAD"]), h["gate"][:50]] for h in spec["implementation_horizons"]]))
    slide("10. Risks and mitigations", "Pre-mortem with early-warning triggers", table=(
        ["Risk", "L / I", "Mitigation"], [[r["risk"], f"{r['likelihood']} / {r['impact']}", r["mitigation"][:80]] for r in spec["risks"]]))
    slide("11. Judge defence bank", "Prepared answers, computed from the model", dark=True,
          bullets=[f"Q: {q['question']}  —  A: {q['rebuttal']}" for q in spec["red_team_defense"][:3]],
          note=f"Bear case NPV {cad(bear['npv'])}. Lead with the number, then the mitigation.")

    prs.save(str(OUTPUT_ROOT / "07_PowerPoint/Final_Presentation.pptx"))
    write_text(OUTPUT_ROOT / "07_PowerPoint/speaker_notes.md", "\n".join(notes_md))


# --------------------------------------------------------------------------------------
# Agent 13: video (beats -> storyboard, narration, SRT, 120 s MP4)
# --------------------------------------------------------------------------------------
def generate_video_assets(spec: dict, render: bool = True, tts: bool = True) -> None:
    """Agent 13: three narrated explainer videos (case, how to tackle, solution brief)."""
    vdir = OUTPUT_ROOT / "09_Video"
    for legacy in ("Final_Demo_120s.mp4", "beats.json", "subtitles.srt"):  # superseded outputs of this pipeline
        (vdir / legacy).unlink(missing_ok=True)
    for slug, _, _ in case_videos.VIDEOS:
        (vdir / f"{slug}.mp4").unlink(missing_ok=True)
    for old in (vdir / "source_project").glob("*.txt"):  # title-card text files from the previous video engine
        old.unlink()
    results = case_videos.render_all(spec, vdir, tts=tts, render=render and shutil.which("ffmpeg") is not None)
    write_text(vdir / "storyboard.md", "# Video Suite\n\n" + md_table(
        ["Video", "Purpose", "Scenes", "Duration", "Narrated"],
        [[f"{slug}.mp4", title, r["scenes"], f"{r.get('duration_s', 0)} s", "yes" if r["narrated"] else "no"]
         for (slug, title, _), r in zip(case_videos.VIDEOS, results)]) + "\n\nScripts: `*_script.md`; subtitles: `*.srt`.")
    write_text(vdir / "narration_script.md", "\n\n".join(
        (vdir / f"{slug}_script.md").read_text(encoding="utf-8") for slug, _, _ in case_videos.VIDEOS if (vdir / f"{slug}_script.md").exists()))


def video_duration(path: Path) -> float:
    probe = shutil.which("ffprobe")
    if not probe or not path.exists():
        return 0.0
    out = subprocess.run([probe, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


# --------------------------------------------------------------------------------------
# Agent 12 + 14: frontend sync, quality gates, manifest
# --------------------------------------------------------------------------------------
def sync_frontend(spec: dict) -> None:
    web = REPO_ROOT / "src/data"
    web.mkdir(parents=True, exist_ok=True)
    (web / "current_case_solution.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")


DELIVERABLES = {
    "solution_spec_json": "solution_spec.json",
    "strategic_blueprint_pdf": "06_PDF_Deliverables/Strategic_Blueprint.pdf",
    "final_solution_pdf": "06_PDF_Deliverables/Final_Case_Solution.pdf",
    "presentation_pptx": "07_PowerPoint/Final_Presentation.pptx",
    "financial_model_xlsx": "05_Financial_Models/financial_model.xlsx",
    "cost_breakdown_xlsx": "05_Financial_Models/cost_breakdown.xlsx",
    "evaluation_matrix_xlsx": "03_Brainstorming/evaluation_matrix.xlsx",
    "executive_summary_md": "04_Final_Strategy/executive_summary.md",
    "judge_qa_md": "07_PowerPoint/judge_QA_preparation.md",
    "case_study_booklet_pdf": "06_PDF_Deliverables/Case_Study_Booklet.pdf",
    "case_decrypt_md": "04_Final_Strategy/case_decrypt.md",
    "video_subtitles_srt": "09_Video/03_Solution_Brief.srt",
    "video_case_mp4": "09_Video/01_The_Case.mp4",
    "video_tackle_mp4": "09_Video/02_How_To_Tackle.mp4",
    "video_solution_mp4": "09_Video/03_Solution_Brief.mp4",
}
VIDEO_KEYS = {"video_case_mp4", "video_tackle_mp4", "video_solution_mp4", "video_subtitles_srt"}
DASHES = str.maketrans({"\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2212": "-"})


def _artifact_text() -> dict[str, str]:
    import pymupdf
    from pptx import Presentation
    out = {}
    for key in ("strategic_blueprint_pdf", "final_solution_pdf"):
        p = OUTPUT_ROOT / DELIVERABLES[key]
        if p.exists():
            with pymupdf.open(str(p)) as d:
                out[key] = " ".join(pg.get_text() for pg in d)
    p = OUTPUT_ROOT / DELIVERABLES["presentation_pptx"]
    if p.exists():
        out["presentation_pptx"] = " ".join(sh.text_frame.text for s in Presentation(str(p)).slides
                                            for sh in s.shapes if sh.has_text_frame)
    p = OUTPUT_ROOT / DELIVERABLES["executive_summary_md"]
    if p.exists():
        out["executive_summary_md"] = p.read_text(encoding="utf-8")
    return {k: unicodedata.normalize("NFKC", v).translate(DASHES) for k, v in out.items()}


def run_quality_gates(spec: dict, video_expected: bool, run_started: float = 0.0) -> list[dict]:
    fs, inp = spec["financial_summary"], spec["case_inputs"]
    win = next(o for o in spec["options_evaluation"]["options"] if o["selected"])
    gates = []

    def gate(name, status, detail):
        gates.append({"gate": name, "status": status, "detail": detail})

    ok_inputs = all(inp[k] and inp[k] > 0 for k in ("baseline_value", "target_pct", "budget", "timeline_months"))
    gate("1. Case comprehension", "PASS" if ok_inputs else "FAIL",
         f"baseline {num(inp['baseline_value'])} {inp['baseline_unit']}, target {inp['target_pct']:g}%, budget {cad(inp['budget'])}, {inp['timeline_months']} months")
    weak = spec["weak_assumptions"]
    gate("2. Evidence & assumptions", "WARN" if any("Option" in w or "Monetisation" in w for w in weak) else "PASS",
         f"{len(spec['assumptions'])} parameters logged; validate: {', '.join(weak)}")
    gate("3. Strategy comparison", "PASS" if win["within_budget"] and len(spec["options_evaluation"]["options"]) >= 3 else "FAIL",
         f"Option {win['label']} selected at {win['weighted_total']}/10, capex {cad(win['capex_CAD'])} vs budget {cad(inp['budget'])}")
    gate("4. Target attainment", "PASS" if win["meets_target"] else "FAIL",
         f"{win['improvement_percent']:g}% vs target {inp['target_pct']:g}%")
    bear = spec["scenarios"][0]
    mandate = fs["economic_case"].startswith("mandate")
    status5 = "PASS" if fs["npv_CAD"] > 0 and bear["npv"] > 0 else "WARN" if fs["npv_CAD"] > 0 or mandate else "FAIL"
    gate("5. Financial viability", status5,
         f"base NPV {cad(fs['npv_CAD'])}, bear NPV {cad(bear['npv'])}, payback {months(fs['payback_period_months'])}; "
         f"{fs['levelized_cost']} {fs['levelized_cost_unit']} ({fs['economic_case'].split(' (')[0]})")
    expected = {k: v for k, v in DELIVERABLES.items() if k not in VIDEO_KEYS or video_expected}
    missing = [v for v in expected.values() if not ((OUTPUT_ROOT / v).exists() and (OUTPUT_ROOT / v).stat().st_size > 0)]
    if video_expected and shutil.which("ffprobe"):
        for k in VIDEO_KEYS - {"video_subtitles_srt"}:
            dur = video_duration(OUTPUT_ROOT / DELIVERABLES[k])
            if DELIVERABLES[k] not in missing and dur < 30:
                missing.append(f"{DELIVERABLES[k]} ({dur:.0f}s, expected >= 30s)")
    gate("6. Deliverable integrity", "FAIL" if missing else "PASS",
         f"missing/empty: {', '.join(missing)}" if missing else f"{len(expected)} core files present")
    texts = _artifact_text()
    needles = {"winner": win["name"][:30], "capex": cad(fs["initial_investment_CAD"]), "NPV": cad(fs["npv_CAD"]),
               "payback": months(fs["payback_period_months"])}
    gaps = [f"{n} not in {k}" for k, t in texts.items() for n, v in needles.items() if v not in " ".join(t.split())]
    bk = OUTPUT_ROOT / DELIVERABLES["case_study_booklet_pdf"]
    if bk.exists():
        import pymupdf
        from case_visual_pdf import _cad as short
        with pymupdf.open(str(bk)) as d:
            bt = unicodedata.normalize("NFKC", " ".join(" ".join(pg.get_text() for pg in d).split())).translate(DASHES)
        for n, v in {"winner": f"Option {win['label']}", "NPV": short(fs["npv_CAD"]), "budget": short(spec["case_inputs"]["budget"])}.items():
            if v not in bt:
                gaps.append(f"{n} not in case_study_booklet_pdf")
        texts["case_study_booklet_pdf"] = bt
    gate("7. Cross-artifact consistency", "FAIL" if gaps else "PASS",
         "; ".join(gaps[:6]) if gaps else f"winner, capex, NPV and payback identical across {len(texts)} artifacts")
    leak_patterns = [r"[A-Za-z]:[\\/](?:Users|Documents)", r"file:///", r"/Users/[A-Za-z]"]
    user = getpass.getuser()
    leaks = []
    for p in OUTPUT_ROOT.rglob("*"):
        if p.suffix.lower() in {".md", ".json", ".csv", ".srt", ".txt"} and p.is_file():
            t = p.read_text(encoding="utf-8", errors="ignore")
            if any(re.search(pat, t) for pat in leak_patterns) or (len(user) > 3 and user.lower() in t.lower()):
                leaks.append(p.relative_to(OUTPUT_ROOT).as_posix())
    leaks += [k for k, t in texts.items() if any(re.search(pat, t) for pat in leak_patterns)]
    gate("8. Anonymity (Law 1)", "FAIL" if leaks else "PASS", f"leaks in: {', '.join(leaks[:5])}" if leaks else "no local paths or user names in outputs")
    qc_outputs = {"11_Final_Quality_Control", "00_Project_Overview/project_status.json", "00_Project_Overview/project_manifest.json"}
    stale = sorted(p.relative_to(OUTPUT_ROOT).as_posix() for p in OUTPUT_ROOT.rglob("*")
                   if p.is_file() and p.stat().st_mtime < run_started - 1
                   and not any(p.relative_to(OUTPUT_ROOT).as_posix().startswith(q) for q in qc_outputs))
    gate("9. Stale artifacts", "WARN" if stale else "PASS",
         f"{len(stale)} file(s) not produced by this run (may describe another case): {', '.join(stale[:6])}{' …' if len(stale) > 6 else ''}"
         if stale else "every file in the output folder comes from this run")
    return gates


def write_qc(spec: dict, gates: list[dict], video_expected: bool) -> dict:
    qc = OUTPUT_ROOT / "11_Final_Quality_Control"
    icon = {"PASS": "✅ PASS", "WARN": "⚠️ WARN", "FAIL": "❌ FAIL"}
    write_text(qc / "compliance_checklist.md", "# Quality Gates (computed by Agent 14)\n\n" + md_table(
        ["Gate", "Status", "Evidence"], [[g["gate"], icon[g["status"]], g["detail"]] for g in gates]))
    write_text(qc / "unresolved_issues.md", "# Unresolved Issues\n\n" + ("\n".join(
        f"- **{g['gate']}** ({g['status']}): {g['detail']}" for g in gates if g["status"] != "PASS") or "None.")
        + "\n\n## Assumptions to replace with real data\n" + "\n".join(f"- {w}" for w in spec["weak_assumptions"]))
    write_text(qc / "verified_claims.md", "# Verified Claims\n\n" + md_table(
        ["Claim", "Value", "Check"], [
            ["Selected option", f"Option {spec['approved_solution']['label']}", "highest weighted score within budget"],
            ["Capex", cad(spec["financial_summary"]["initial_investment_CAD"]), "<= budget"],
            ["NPV", cad(spec["financial_summary"]["npv_CAD"]), "Excel NPV formula reproduces value"],
            ["Payback", months(spec["financial_summary"]["payback_period_months"]), "monthly cash model"]]))
    write_text(qc / "consistency_report.md", "# Consistency Report\n\n" + next(g["detail"] for g in gates if g["gate"].startswith("7")))
    counts = {s: sum(g["status"] == s for g in gates) for s in ("PASS", "WARN", "FAIL")}
    manifest = {
        "status": "COMPLETED" if counts["FAIL"] == 0 else "COMPLETED_WITH_FAILURES",
        "timestamp": spec["generated_at"], "case_id": spec["case_identification"]["id"],
        "output_root": "Finished Resources" if OUTPUT_ROOT.name == "Finished Resources" else OUTPUT_ROOT.name,
        "deliverables": {k: v for k, v in DELIVERABLES.items() if k not in VIDEO_KEYS or video_expected},
        "gates": gates, "gates_passed": counts["PASS"], "gates_warn": counts["WARN"], "gates_failed": counts["FAIL"],
    }
    for target in (qc / "final_delivery_manifest.json", OUTPUT_ROOT / "00_Project_Overview/project_status.json",
                   OUTPUT_ROOT / "00_Project_Overview/project_manifest.json"):
        target.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


# --------------------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------------------
def run_agent_pipeline(case_info: dict, render_video: bool = True, unit_value_override: float | None = None,
                       tts: bool = True) -> dict:
    print("=" * 80)
    print(f"CASE [{case_info['id']}] {case_info['title']}")
    print("=" * 80)
    run_started = datetime.now().timestamp()
    spec = build_solution_spec(case_info, unit_value_override)
    (OUTPUT_ROOT / "solution_spec.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
    sol, fs = spec["approved_solution"], spec["financial_summary"]
    print(f"[00] Option {sol['label']} selected: {sol['name']}")
    print(f"     capex {cad(fs['initial_investment_CAD'])} | NPV {cad(fs['npv_CAD'])} | IRR {pct(fs['irr_percent'])} | payback {months(fs['payback_period_months'])}")

    steps = [
        ("01-09 Strategy documents", lambda: write_markdown_set(spec)),
        ("05 Evaluation matrix", lambda: write_evaluation_matrix(spec)),
        ("06 Financial workbooks", lambda: write_financial_workbooks(spec)),
        ("10 PDF deliverables", lambda: generate_pdf_deliverables(spec)),
        ("10 Case study booklet", lambda: generate_case_study_booklet(spec, OUTPUT_ROOT / DELIVERABLES["case_study_booklet_pdf"])),
        ("11 PowerPoint deck", lambda: generate_powerpoint_deck(spec)),
        ("13 Video suite", lambda: generate_video_assets(spec, render_video, tts)),
    ]
    if OUTPUT_ROOT.resolve() == (REPO_ROOT / "Finished Resources").resolve():  # scratch --out runs never touch the website
        steps.append(("12 Frontend sync", lambda: sync_frontend(spec)))
    for label, fn in steps:
        fn()
        print(f"[{label}] done")

    video_expected = render_video and shutil.which("ffmpeg") is not None
    gates = run_quality_gates(spec, video_expected, run_started)
    manifest = write_qc(spec, gates, video_expected)
    for g in gates:
        print(f"  {g['status']:<4}  {g['gate']}: {g['detail']}")
    print("=" * 80)
    print(f"{manifest['status']}: {manifest['gates_passed']} pass / {manifest['gates_warn']} warn / {manifest['gates_failed']} fail -> {OUTPUT_ROOT.as_posix()}/")
    return manifest


def main() -> int:
    global OUTPUT_ROOT
    ap = argparse.ArgumentParser(description="Case Competition Intelligence System Orchestrator")
    ap.add_argument("case_pos", nargs="?", help="Case ID (ENG-0001, ENG100K-000001, ENG1M-0000001) or path")
    ap.add_argument("--case-id", "-c", dest="case_id")
    ap.add_argument("--input", "-i", dest="input_path", help="PDF/MD/TXT/JSON brief or case directory")
    ap.add_argument("--out", "-o", default=str(OUTPUT_ROOT), help="Output directory (default: Finished Resources)")
    ap.add_argument("--unit-value", type=float, help="CAD value of one unit of improvement (overrides default monetisation)")
    ap.add_argument("--no-video", action="store_true", help="Skip MP4 rendering (fast mode)")
    ap.add_argument("--no-tts", action="store_true", help="Render videos without online neural narration (offline mode)")
    ap.add_argument("--spec-only", action="store_true", help="Print the computed solution spec and exit")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    case_info = load_case_data(args.case_id or args.input_path or args.case_pos or "ENG-0001")
    if args.spec_only:
        print(json.dumps(build_solution_spec(case_info, args.unit_value), indent=2))
        return 0
    OUTPUT_ROOT = Path(args.out)
    create_directory_structure()
    manifest = run_agent_pipeline(case_info, render_video=not args.no_video, unit_value_override=args.unit_value,
                                  tts=not args.no_tts)
    return 0 if manifest["gates_failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
