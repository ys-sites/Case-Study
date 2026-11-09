#!/usr/bin/env python3
"""
Reindex Case Database
Combines cases from engineering_1000_case_simulations.json,
engineering_100000_preview.csv, and engineering_1million_additional_preview.csv
into a unified frontend catalog in src/data/case_index.json.
"""

import csv
import json
from pathlib import Path

def reindex_all_cases():
    all_cases = []

    # 1. 1000 Engineering Simulations
    sim_file = Path("data/engineering_1000_case_simulations.json")
    if sim_file.exists():
        with open(sim_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            cases = data.get("cases", [])
            for c in cases:
                all_cases.append({
                    "id": c.get("id"),
                    "title": c.get("case_title", "Engineering Case"),
                    "discipline": c.get("discipline", "Industrial Engineering"),
                    "difficulty": c.get("difficulty", "Advanced"),
                    "scenario_type": "1,000 Engineering Simulations",
                    "budget_cad": c.get("inputs", {}).get("capital_budget_CAD", 1500000)
                })

    # 2. 100k Preview Cases
    csv_100k = Path("data/engineering_100000_preview.csv")
    if csv_100k.exists():
        with open(csv_100k, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_cases.append({
                    "id": row.get("Case ID"),
                    "title": f"{row.get('Archetype', 'Case')} — {row.get('Context', '')} ({row.get('Shock', '')})",
                    "discipline": row.get("Discipline", "Industrial Engineering"),
                    "difficulty": row.get("Difficulty", "Intermediate"),
                    "scenario_type": "100k Dataset Preview",
                    "budget_cad": float(row.get("Budget CAD", 1500000))
                })

    # 3. 1M Preview Cases
    csv_1m = Path("data/engineering_1million_additional_preview.csv")
    if csv_1m.exists():
        with open(csv_1m, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_cases.append({
                    "id": row.get("case_id"),
                    "title": f"{row.get('asset', 'Asset').title()} — {row.get('technical_challenge', '').title()}",
                    "discipline": row.get("discipline", "Industrial Engineering"),
                    "difficulty": row.get("difficulty", "Beginner"),
                    "scenario_type": "1 Million Dataset Expansion",
                    "budget_cad": float(row.get("budget_cad", 1500000))
                })

    out_file = Path("src/data/case_index.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, indent=2)

    print(f"[OK] Reindexed {len(all_cases)} total cases into {out_file}")

if __name__ == "__main__":
    reindex_all_cases()
