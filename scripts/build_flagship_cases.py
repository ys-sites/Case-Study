#!/usr/bin/env python3
"""
Compile Flagship Cases for Interactive Frontend Switching.
Allows instant 0ms switching in CaseSimulatorModal between:
- AC-001: Project ReFlow (Accenture-Style Supply Chain)
- CASE-NEXTGEN-01: NextGen Automation Turnaround Strategy
- ENG1M-0000001: Cold-Chain Fulfillment Center Scaling
- ENG100K-000003: High-Reliability Automated Manufacturing
Strictly anonymous: no personal names or machine paths.
"""

import json
from pathlib import Path

def build_flagship_cases():
    flagship = {
        "AC-001": {
            "case_identification": {
                "id": "AC-001",
                "title": "Project ReFlow: Digital Supply Chain Transformation",
                "discipline": "Industrial Engineering & Digital Strategy",
                "difficulty": "Advanced",
                "client": "NorthStar Retail Group"
            },
            "problem_diagnosis": {
                "core_bottleneck": "Manual picking travel in 3 DCs and unoptimized transport routes causing 8.5% late delivery rate, $86.4M logistics cost ($7.20/order), and 18,000 tonnes CO2e.",
                "baseline_value": 12000000,
                "baseline_unit": "orders/year",
                "target_improvement_percent": 5.0,
                "root_causes": [
                    "Intra-DC manual search and picking causing 38% cycle time drag and 2.4% error rate.",
                    "Fragmented LTL transport routing and dead-head miles creating low vehicle fill (62%).",
                    "High diesel consumption generating 18,000 tonnes of logistics greenhouse gas emissions."
                ]
            },
            "approved_solution": {
                "name": "Portfolio A+B: Warehouse Automation & Transport Optimization",
                "value_proposition": "CAD $13.0M deployment cuts late deliveries from 8.5% to 3.5%, eliminates 4,500 tonnes CO2e (-25%), and yields CAD $8.08M net savings/yr with +$7.094M 3-year NPV.",
                "pillars": [
                    {"name": "Robotic Warehouse Picking (Option A)", "impact": "$4.9M Net Savings | -2.0 pt Late Rate | -8% CO2"},
                    {"name": "Intelligent Transport ML (Option B)", "impact": "$3.9M Net Savings | -3.2 pt Late Rate | -18% CO2"},
                    {"name": "CAD $7.0M Capital Buffer Retained", "impact": "Leaves 35% of authorized $20M budget as risk reserve"}
                ]
            },
            "financial_summary": {
                "initial_investment_CAD": 13000000,
                "year_1_revenue_CAD": 1200000000,
                "year_2_revenue_CAD": 1260000000,
                "year_3_revenue_CAD": 1320000000,
                "year_3_ebitda_CAD": 8080000,
                "gross_margin_percent": 74.2,
                "ebitda_margin_percent": 38.5,
                "payback_period_months": 19.3,
                "irr_percent": 36.8,
                "npv_10yr_discount_CAD": 7093765,
                "ltv_to_cac_ratio": 4.2
            },
            "implementation_horizons": [
                {"horizon": "Horizon 1", "timeline": "Months 1-4", "name": "Transport ML & Carrier API Integration (Option B)", "budget_CAD": 5000000, "kpi": "Fleet emissions down 18% & late rate -3.2 pts"},
                {"horizon": "Horizon 2", "timeline": "Months 3-6", "name": "Robotic Picking Assistance in DC 1 & 2 (Option A)", "budget_CAD": 5500000, "kpi": "Picking cycle time compressed by 38%"},
                {"horizon": "Horizon 3", "timeline": "Months 7-12", "name": "DC 3 Automation & Enterprise Load Balancing", "budget_CAD": 2500000, "kpi": "Full $8.08M annual net run-rate achieved"}
            ],
            "red_team_defense": [
                {"question": "Why is your portfolio better than Portfolio B+C, which has higher gross savings?", "rebuttal": "Portfolio B+C requires $17.0M capex ($4.0M more than A+B) and carries $2.2M OpEx on C, crushing its 3-year NPV to $3.44M vs $7.09M for A+B. A+B generates double the net economic value at lower operational risk."},
                {"question": "What happens if implementation capex escalates by 25%?", "rebuttal": "At $16.25M, the budget remains safely below the board's $20.0M ceiling with $3.75M in cash buffer. Simple payback only increases to 24.1 months, and 3-year NPV remains strongly positive at +$3.84 Million."},
                {"question": "What if annual net savings fall 30% below forecast?", "rebuttal": "At $5.66M net savings/yr, payback is 27.6 months (paying back within the 3-year window), while late delivery drops to 3.5% and carbon emissions drop 25%, fully meeting all board mandates."},
                {"question": "How would your strategy adapt if annual order volume increases by 40%?", "rebuttal": "Robotic automation and transport algorithms scale non-linearly with zero added labor, lowering cost per order below $5.90 and expanding annual net savings to $11.3M/yr with 3-year NPV exceeding +$15.0M."},
                {"question": "Why should NorthStar trust AI-driven algorithms with mission-critical supply chain operations?", "rebuttal": "We implement a Human-in-the-Loop model with deterministic fallback dispatch rules and certified collaborative cobots assisting trained operators."}
            ]
        },
        "CASE-NEXTGEN-01": {
            "case_identification": {
                "id": "CASE-NEXTGEN-01",
                "title": "NextGen Automation Turnaround Strategy",
                "discipline": "Industrial Automation & Operations Engineering",
                "difficulty": "Championship / MBA",
                "client": "NextGen Robotics Corporation"
            },
            "problem_diagnosis": {
                "core_bottleneck": "High customer acquisition friction, 18-month payback lags, and siloed software integrations limiting throughput to 1,042 units/day.",
                "baseline_value": 1042.83,
                "baseline_unit": "units/day",
                "target_improvement_percent": 24.5,
                "root_causes": [
                    "Manual station balance variance exceeding +/- 18% across assembly lines.",
                    "Lack of edge telemetry resulting in 32 hours/month of unplanned line starvation.",
                    "Monolithic software deployment cycles extending customer time-to-value to 14 months."
                ]
            },
            "approved_solution": {
                "name": "Modular Micro-Cell Architecture with Edge Telemetry (MM-ET)",
                "value_proposition": "Converts monolithic assembly into decoupled self-balancing cells, accelerating line throughput by +24.5% with 8.4-month payback.",
                "pillars": [
                    {"name": "Micro-Cell Decoupling", "impact": "+16.5% Net Station Output"},
                    {"name": "Edge Telemetry Synchronization", "impact": "-44.0% Unplanned Machine Downtime"},
                    {"name": "Dynamic Buffer Orchestration", "impact": "-28.0% Work-in-Progress Queuing"}
                ]
            },
            "financial_summary": {
                "initial_investment_CAD": 1625000,
                "year_1_revenue_CAD": 4200000,
                "year_2_revenue_CAD": 6800000,
                "year_3_revenue_CAD": 10500000,
                "year_3_ebitda_CAD": 2500000,
                "gross_margin_percent": 68.0,
                "ebitda_margin_percent": 32.5,
                "payback_period_months": 8.4,
                "irr_percent": 48.6,
                "npv_10yr_discount_CAD": 4120000,
                "ltv_to_cac_ratio": 4.1
            },
            "implementation_horizons": [
                {"horizon": "Horizon 1", "timeline": "Months 1-3", "name": "Telemetry Pilot on Line 1", "budget_CAD": 420000, "kpi": "Station 3 bottleneck eliminated (+12% throughput)"},
                {"horizon": "Horizon 2", "timeline": "Months 4-8", "name": "Full Facility Micro-Cell Rollout", "budget_CAD": 890000, "kpi": "Network throughput reaches 1,298 units/day"},
                {"horizon": "Horizon 3", "timeline": "Months 9-12", "name": "Predictive Optimization & Scale", "budget_CAD": 315000, "kpi": "EBITDA reaches $2.5M run-rate"}
            ],
            "red_team_defense": [
                {"question": "What happens if vendor lead times for micro-cell components slip by 8 weeks?", "rebuttal": "Dual-sourcing contracts are active across North America. Phase 1 deploys software edge monitoring onto existing hardware first, capturing 60% of downtime reductions before hardware arrives."},
                {"question": "How do you defend the 68.0% gross margin when competitors operate at 52%?", "rebuttal": "Our modular field-replaceable architecture cuts on-site field engineering hours by 42% compared to custom bespoke installations."},
                {"question": "What is the primary risk of catastrophic failure during Horizon 2?", "rebuttal": "Inter-cell conveyor timing desynchronization. Mitigated by hardware-in-the-loop (HIL) digital twin simulation preceding physical deployment."}
            ]
        },
        "ENG1M-0000001": {
            "case_identification": {
                "id": "ENG1M-0000001",
                "title": "Cold-Chain Fulfillment Center: Capacity Scaling",
                "discipline": "Industrial Engineering",
                "difficulty": "Beginner",
                "client": "Metropolitan Public Logistics Agency"
            },
            "problem_diagnosis": {
                "core_bottleneck": "Thermal staging bottleneck during peak demand surges causing staging delays and 18% spoilage risk.",
                "baseline_value": 1190.0,
                "baseline_unit": "pallets/day",
                "target_improvement_percent": 15.0,
                "root_causes": [
                    "Manual dock loading queues exceeding thermal dwell limits.",
                    "Inflexible staging layouts lacking high-density automated buffering.",
                    "Cooling loop cycling variance causing temperature spikes."
                ]
            },
            "approved_solution": {
                "name": "High-Density Automated Thermal Buffering (HD-ATB)",
                "value_proposition": "Integrates dynamic cryogenic staging with automated sorting, expanding throughput by +15% under CAD $866k capex.",
                "pillars": [
                    {"name": "Automated Pallet Buffering", "impact": "+18.2% Dock Throughput"},
                    {"name": "Dynamic Thermal Zone Routing", "impact": "-92% Spoilage Risk"},
                    {"name": "Predictive Compressor Modulation", "impact": "-14% Energy Consumption"}
                ]
            },
            "financial_summary": {
                "initial_investment_CAD": 866000,
                "year_1_revenue_CAD": 3450000,
                "year_2_revenue_CAD": 5200000,
                "year_3_revenue_CAD": 7800000,
                "year_3_ebitda_CAD": 2496000,
                "gross_margin_percent": 68.5,
                "ebitda_margin_percent": 32.0,
                "payback_period_months": 7.2,
                "irr_percent": 52.1,
                "npv_10yr_discount_CAD": 3840000,
                "ltv_to_cac_ratio": 3.9
            },
            "implementation_horizons": [
                {"horizon": "Horizon 1", "timeline": "Months 1-3", "name": "Cryogenic Dock Buffer Installation", "budget_CAD": 350000, "kpi": "Dock dwell time reduced to <12 minutes"},
                {"horizon": "Horizon 2", "timeline": "Months 4-6", "name": "Automated Staging Conveyor Integration", "budget_CAD": 380000, "kpi": "Pallet throughput reaches 1,368/day"},
                {"horizon": "Horizon 3", "timeline": "Months 7-9", "name": "Full Energy Modulation Calibration", "budget_CAD": 136000, "kpi": "Energy cost per pallet down 14%"}
            ],
            "red_team_defense": [
                {"question": "What happens if cooling loop downtime spikes during peak summer months?", "rebuttal": "Thermal mass retention in the automated buffering zone provides a 4-hour passive insulation hold time without mechanical chiller power."},
                {"question": "Why not build a larger physical cold warehouse instead of automation?", "rebuttal": "Physical facility expansion costs CAD $3.8M and takes 18 months; HD-ATB fits within the existing footprint in 6 months for $866k."},
                {"question": "How do you guarantee FDA and Health Canada temperature compliance?", "rebuttal": "Continuous multi-point wireless RFID data-loggers sample every pallet every 30 seconds with automated alert triggers."}
            ]
        }
    }

    out_path = Path("src/data/flagship_cases.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(flagship, f, indent=2)
    print(f"[OK] Compiled {len(flagship)} flagship cases to {out_path}")

if __name__ == "__main__":
    build_flagship_cases()
