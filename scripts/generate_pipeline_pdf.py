#!/usr/bin/env python3
"""
Generate the Case Competition Pipeline Architecture UI PDF Guide.
Creates an executive-grade 6-page visual document using PyMuPDF (fitz).
Strictly anonymous: no machine paths or personal names.
"""

import os
import sys
from pathlib import Path
import pymupdf

def create_pipeline_guide_pdf(output_path: str):
    doc = pymupdf.open()
    
    # Palette definition (RGB normalized 0.0 - 1.0)
    C_BG_DARK = (11/255, 15/255, 25/255)       # #0B0F19 deep slate
    C_SURFACE = (30/255, 41/255, 59/255)       # #1E293B card slate
    C_SURFACE_LIGHT = (51/255, 65/255, 85/255) # #334155 lighter card
    C_CYAN = (14/255, 165/255, 233/255)        # #0EA5E9 accent cyan
    C_TEAL = (16/255, 185/255, 129/255)        # #10B981 accent emerald
    C_AMBER = (245/255, 158/255, 11/255)       # #F59E0B warning amber
    C_PURPLE = (139/255, 92/255, 246/255)      # #8B5CF6 royal purple
    C_WHITE = (248/255, 250/255, 252/255)      # #F8FAFC crisp white
    C_MUTED = (148/255, 163/255, 184/255)      # #94A3B8 muted gray
    C_BORDER = (71/255, 85/255, 105/255)       # #475569 border line

    PAGE_W = 612  # Standard Letter width
    PAGE_H = 792  # Standard Letter height

    def add_page_header_footer(page, page_num, total_pages, title="CASE COMPETITION INTELLIGENCE SYSTEM"):
        # Running top header
        page.draw_rect(pymupdf.Rect(0, 0, PAGE_W, 36), fill=C_BG_DARK)
        page.draw_line(pymupdf.Point(36, 36), pymupdf.Point(PAGE_W - 36, 36), color=C_BORDER, width=0.8)
        page.insert_text(pymupdf.Point(36, 24), title, fontname="helv", fontsize=8.5, color=C_CYAN)
        page.insert_text(pymupdf.Point(PAGE_W - 160, 24), "CONFIDENTIAL STRATEGY SYSTEM", fontname="helv", fontsize=8, color=C_MUTED)

        # Running bottom footer
        page.draw_line(pymupdf.Point(36, PAGE_H - 32), pymupdf.Point(PAGE_W - 36, PAGE_H - 32), color=C_BORDER, width=0.8)
        page.insert_text(pymupdf.Point(36, PAGE_H - 18), "Autonomous Case Simulation & Competition Engine", fontname="helv", fontsize=8, color=C_MUTED)
        page.insert_text(pymupdf.Point(PAGE_W - 75, PAGE_H - 18), f"Page {page_num} of {total_pages}", fontname="helv", fontsize=8, color=C_CYAN)

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p1 = doc.new_page(width=PAGE_W, height=PAGE_H)
    p1.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H), fill=C_BG_DARK)

    # Decorative tech grid pattern lines
    for y in range(80, PAGE_H - 60, 40):
        p1.draw_line(pymupdf.Point(36, y), pymupdf.Point(PAGE_W - 36, y), color=(18/255, 24/255, 38/255), width=0.5)
    for x in range(36, PAGE_W - 36, 40):
        p1.draw_line(pymupdf.Point(x, 80), pymupdf.Point(x, PAGE_H - 60), color=(18/255, 24/255, 38/255), width=0.5)

    # Accent Header Pill
    pill_rect = pymupdf.Rect(40, 70, 260, 95)
    p1.draw_rect(pill_rect, fill=C_SURFACE, color=C_CYAN, width=1)
    p1.insert_text(pymupdf.Point(52, 87), "AUTONOMOUS SYSTEM BLUEPRINT v2.5", fontname="helv", fontsize=8.5, color=C_CYAN)

    # Main Title
    p1.insert_text(pymupdf.Point(40, 140), "THE CASE COMPETITION", fontname="helv", fontsize=28, color=C_WHITE)
    p1.insert_text(pymupdf.Point(40, 175), "INTELLIGENCE MACHINE", fontname="helv", fontsize=28, color=C_CYAN)
    
    # Subtitle
    subtitle = "A Complete Architectural & Operational Guide to Autonomous Multi-Agent Solving, Quantitative Rigor, and Omnichannel Deliverable Production"
    p1.insert_textbox(pymupdf.Rect(40, 195, PAGE_W - 40, 245), subtitle, fontname="helv", fontsize=11, color=C_MUTED)

    # Hero Center Visual: 3D Isometric Core Engine Wireframe
    center_y = 350
    # Isometric Cube / Central Processor
    p1.draw_rect(pymupdf.Rect(50, center_y - 65, PAGE_W - 50, center_y + 125), fill=C_SURFACE, color=C_BORDER, width=1.2)
    p1.draw_rect(pymupdf.Rect(55, center_y - 60, PAGE_W - 55, center_y + 120), color=C_CYAN, width=0.5)

    # Isometric Stage Blocks inside Hero Box
    stages = [
        ("01 INTAKE", "PDF / OCR / Data", C_CYAN, 70),
        ("02 DIAGNOSIS", "Graphify & MECE", C_PURPLE, 170),
        ("03 BRAIN", "Decision Matrix", C_AMBER, 270),
        ("04 QUANT", "TOC & Proforma", C_TEAL, 370),
        ("05 FACTORY", "12 Deliverables", C_CYAN, 470)
    ]
    for name, desc, col, x_pos in stages:
        box = pymupdf.Rect(x_pos, center_y - 30, x_pos + 85, center_y + 40)
        p1.draw_rect(box, fill=C_SURFACE_LIGHT, color=col, width=1.2)
        p1.insert_text(pymupdf.Point(x_pos + 8, center_y - 10), name, fontname="helv", fontsize=8.5, color=col)
        p1.insert_text(pymupdf.Point(x_pos + 6, center_y + 15), desc, fontname="helv", fontsize=7.5, color=C_WHITE)
        if x_pos < 470:
            p1.draw_line(pymupdf.Point(x_pos + 85, center_y + 5), pymupdf.Point(x_pos + 100, center_y + 5), color=col, width=1.5)

    p1.insert_text(pymupdf.Point(70, center_y + 85), "CENTRAL NERVOUS SYSTEM: GRAPHIFY KNOWLEDGE GRAPH + 39 SPECIALIZED SKILLS", fontname="helv", fontsize=8, color=C_CYAN)
    p1.insert_text(pymupdf.Point(70, center_y + 102), "Execution: 100% Deterministic | Zero Skipped Mathematical Derivations | Strict Competition Neutrality", fontname="helv", fontsize=7.5, color=C_MUTED)

    # 4 Key Metrics Cards on Cover
    cards = [
        ("14", "AUTONOMOUS AGENTS", "Synchronized pipeline from intake to defense", C_CYAN, 40),
        ("39", "VERIFIED SKILLS", "Graphify-routed tools with zero bloat", C_PURPLE, 175),
        ("132+", "GLOBAL CASES", "Curated benchmark winning strategies", C_AMBER, 310),
        ("12", "FINISHED ASSETS", "PDFs, PPTX, Excel, Video, Web App", C_TEAL, 445)
    ]
    card_y = 510
    for num, title, detail, col, x in cards:
        r = pymupdf.Rect(x, card_y, x + 125, card_y + 90)
        p1.draw_rect(r, fill=C_SURFACE, color=C_BORDER, width=1)
        p1.draw_rect(pymupdf.Rect(x, card_y, x + 125, card_y + 4), fill=col)
        p1.insert_text(pymupdf.Point(x + 12, card_y + 35), num, fontname="helv", fontsize=22, color=col)
        p1.insert_text(pymupdf.Point(x + 12, card_y + 53), title, fontname="helv", fontsize=7.5, color=C_WHITE)
        p1.insert_textbox(pymupdf.Rect(x + 12, card_y + 60, x + 115, card_y + 85), detail, fontname="helv", fontsize=6.5, color=C_MUTED)

    # Bottom Cover Note
    p1.draw_line(pymupdf.Point(40, 640), pymupdf.Point(PAGE_W - 40, 640), color=C_BORDER, width=0.8)
    cover_note = (
        "PURPOSE OF THIS SPECIFICATION: To provide an intuitive, comprehensive visual reference of how raw competition cases "
        "and industrial datasets are converted into championship-grade strategy deliverables, mathematical models, and "
        "adversarial defense presentations in under 60 seconds."
    )
    p1.insert_textbox(pymupdf.Rect(40, 655, PAGE_W - 40, 715), cover_note, fontname="helv", fontsize=9, color=C_MUTED)
    add_page_header_footer(p1, 1, 6, "EXECUTIVE SYSTEM OVERVIEW")

    # =========================================================================
    # PAGE 2: THE 3D ISOMETRIC MACHINE ARCHITECTURE
    # =========================================================================
    p2 = doc.new_page(width=PAGE_W, height=PAGE_H)
    p2.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H), fill=C_BG_DARK)
    add_page_header_footer(p2, 2, 6, "PIPELINE MECHANISM & ISOMETRIC SCHEMATIC")

    p2.insert_text(pymupdf.Point(40, 60), "SECTION 1: THE REPOSITORY MACHINE MECHANISM", fontname="helv", fontsize=15, color=C_WHITE)
    p2.insert_text(pymupdf.Point(40, 75), "How raw case inputs flow through five precision processing chambers", fontname="helv", fontsize=9, color=C_MUTED)

    # 5 Process Chambers Detailed Layout
    chambers = [
        ("CHAMBER 1: OPTICAL INTAKE & DECRYPTION", 
         "Input: PDFs, PPTX, CSVs, handwritten notes, or JSON datasets.\n"
         "Mechanism: PyMuPDF vector extractor strips layout noise, separates verified numbers from assumptions, and tags constraints.",
         C_CYAN, 100),
        ("CHAMBER 2: GRAPHIFY BRAIN & ISSUE TREE DIAGNOSIS", 
         "Input: Verified constraints + 132 global case benchmarks.\n"
         "Mechanism: Semantic graph traversal links case domain to relevant skills without token waste; MECE issue tree isolates root bottleneck.",
         C_PURPLE, 205),
        ("CHAMBER 3: HYDRAULIC STRATEGY PRESS & DECISION MATRIX", 
         "Input: 3 to 5 competing solution archetypes.\n"
         "Mechanism: Weighted multi-criteria utility formula scores each archetype against official competition rubric; eliminates weak ideas.",
         C_AMBER, 310),
        ("CHAMBER 4: QUANTITATIVE REACTOR & PROFORMA ENGINE", 
         "Input: Selected winning strategy + financial baseline.\n"
         "Mechanism: Applies Little's Law, TOC, LTV/CAC, BEP, and 3-year proforma statements with 3-scenario sensitivity (Bear, Base, Bull).",
         C_TEAL, 415),
        ("CHAMBER 5: OMNICHANNEL DELIVERABLE CONVEYOR", 
         "Input: Approved strategy, models, and presentation copy.\n"
         "Mechanism: Autonomous compiler outputs 2 PDFs, 12-slide PPTX, Excel model, 120s MP4 video, and interactive React web app.",
         C_CYAN, 520)
    ]

    for title, text, col, y_pos in chambers:
        box = pymupdf.Rect(40, y_pos, PAGE_W - 40, y_pos + 85)
        p2.draw_rect(box, fill=C_SURFACE, color=C_BORDER, width=1)
        p2.draw_rect(pymupdf.Rect(40, y_pos, 46, y_pos + 85), fill=col)
        
        # Indicator badge
        p2.insert_text(pymupdf.Point(58, y_pos + 20), title, fontname="helv", fontsize=10.5, color=C_WHITE)
        p2.insert_textbox(pymupdf.Rect(58, y_pos + 28, PAGE_W - 55, y_pos + 80), text, fontname="helv", fontsize=8, color=C_MUTED)

        # Connector arrow to next chamber
        if y_pos < 520:
            arrow_mid = y_pos + 85
            p2.draw_line(pymupdf.Point(PAGE_W/2, arrow_mid), pymupdf.Point(PAGE_W/2, arrow_mid + 20), color=C_CYAN, width=1.5)
            p2.draw_circle(pymupdf.Point(PAGE_W/2, arrow_mid + 10), 3, fill=C_CYAN)

    # Bottom Summary Callout
    callout_rect = pymupdf.Rect(40, 630, PAGE_W - 40, 720)
    p2.draw_rect(callout_rect, fill=C_SURFACE_LIGHT, color=C_CYAN, width=1)
    p2.insert_text(pymupdf.Point(55, 650), "ANATOMY PRINCIPLE: 'THE OBJECT IS THE EXPLANATION'", fontname="helv", fontsize=9.5, color=C_CYAN)
    callout_txt = (
        "Just like an industrial lathe or dial-gauge rig, this software machine has no unneeded parts. "
        "Every agent hands off exact numerical vectors to the next stage. No step is skipped, no mathematical "
        "transformation is hidden, and every deliverable traces directly back to the original case evidence."
    )
    p2.insert_textbox(pymupdf.Rect(55, 660, PAGE_W - 55, 710), callout_txt, fontname="helv", fontsize=8, color=C_WHITE)

    # =========================================================================
    # PAGE 3: THE 14-AGENT MASTER OPERATIONAL ROSTER
    # =========================================================================
    p3 = doc.new_page(width=PAGE_W, height=PAGE_H)
    p3.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H), fill=C_BG_DARK)
    add_page_header_footer(p3, 3, 6, "14-AGENT SPECIALIZED TEAM ROSTER")

    p3.insert_text(pymupdf.Point(40, 60), "SECTION 2: THE 14 AUTONOMOUS AGENTS", fontname="helv", fontsize=15, color=C_WHITE)
    p3.insert_text(pymupdf.Point(40, 75), "Autonomous roles, responsibilities, and inputs across the 5 championship stages", fontname="helv", fontsize=9, color=C_MUTED)

    # 14 Agents arranged in two neat columns
    agents = [
        ("00 Master Orchestrator", "Air Traffic Controller", "Plans dependency graph, allocates sub-tasks, verifies pipeline integrity.", C_CYAN),
        ("01 Intelligence Analyst", "Document Detective", "Strips PDF noise, extracts balance sheets, isolates operational bottlenecks.", C_CYAN),
        ("02 Competitions Scout", "Global Benchmarker", "Scans 132+ past winning solutions from Wharton, Harvard, and Molson.", C_CYAN),
        ("03 Root-Cause Surgeon", "Issue-Tree Specialist", "Constructs 5-Whys and MECE trees to isolate root friction vs surface symptoms.", C_PURPLE),
        ("04 Innovation Lab", "Creative Brainstormer", "Generates 3-5 distinct strategic archetypes (Platform, Hybrid, Automation).", C_PURPLE),
        ("05 Strategy Evaluator", "Decision Matrix Judge", "Runs weighted multi-criteria scoring against the official competition rubric.", C_PURPLE),
        ("06 Solution Architect", "Chief Systems Engineer", "Designs operational schematics, technical flowcharts, and system blueprints.", C_AMBER),
        ("07 Proforma Modeler", "Wall Street CFO", "Builds 3-year P&L, NPV, IRR, payback, and 3-scenario sensitivity models.", C_AMBER),
        ("08 Operations Planner", "Implementation Director", "Designs 3-horizon rollout, 2x2 pre-mortem risk matrix, and predictive KPIs.", C_AMBER),
        ("09 Slide Designer", "Presentation Specialist", "Creates executive 12-slide pitch deck (Final_Presentation.pptx).", C_TEAL),
        ("10 Document Architect", "Publishing Director", "Compiles vector-crisp executive blueprints and final solutions (PyMuPDF).", C_TEAL),
        ("11 Motion Director", "Visual Storyteller", "Produces 120-second cinematic demonstration video (Final_Demo_120s.mp4).", C_TEAL),
        ("12 Prototype Developer", "Full-Stack Web Engineer", "Maintains interactive React + Tailwind case simulator with live sliders.", C_TEAL),
        ("13 Red-Team Judge", "Hostile Interrogator", "Simulates toughest judges, drafts adversarial questions and counter-rebuttals.", C_PURPLE)
    ]

    for idx, (name, role, desc, col) in enumerate(agents):
        col_idx = idx % 2
        row_idx = idx // 2
        x = 40 if col_idx == 0 else 315
        y = 95 + row_idx * 88
        
        card = pymupdf.Rect(x, y, x + 260, y + 80)
        p3.draw_rect(card, fill=C_SURFACE, color=C_BORDER, width=0.8)
        p3.draw_rect(pymupdf.Rect(x, y, x + 260, y + 3), fill=col)
        
        p3.insert_text(pymupdf.Point(x + 10, y + 18), name, fontname="helv", fontsize=9.5, color=C_WHITE)
        p3.insert_text(pymupdf.Point(x + 10, y + 30), f"Role: {role}", fontname="helv", fontsize=8, color=col)
        p3.insert_textbox(pymupdf.Rect(x + 10, y + 36, x + 250, y + 75), desc, fontname="helv", fontsize=7.2, color=C_MUTED)

    # Note at bottom
    p3.insert_text(pymupdf.Point(40, 725), "* Agent 14 (Inspection Gatekeeper) operates continuously across all handoffs to verify zero data loss and anonymity compliance.", fontname="helv", fontsize=7.5, color=C_MUTED)

    # =========================================================================
    # PAGE 4: THE QUANTITATIVE ENGINEERING & FINANCIAL FORMULATION SHEET
    # =========================================================================
    p4 = doc.new_page(width=PAGE_W, height=PAGE_H)
    p4.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H), fill=C_BG_DARK)
    add_page_header_footer(p4, 4, 6, "QUANTITATIVE FORMULATIONS & REASONING")

    p4.insert_text(pymupdf.Point(40, 60), "SECTION 3: MATHEMATICAL RIGOR & ZERO-SKIP PROOFS", fontname="helv", fontsize=15, color=C_WHITE)
    p4.insert_text(pymupdf.Point(40, 75), "Standard industrial engineering formulas, unit economics, and proforma mechanics", fontname="helv", fontsize=9, color=C_MUTED)

    formulas = [
        ("1. LITTLE'S LAW (OPERATIONAL FLOW & QUEUEING)",
         "Formula: WIP = Throughput (TH) x Cycle Time (CT)\n"
         "Application: Proves lead-time reduction by reducing batch sizes and inventory queuing without adding labor.",
         "Example: Baseline WIP 850 units, TH 50 units/hr -> CT = 17 hrs. Post-Automation: CT = 9 hrs -> WIP drops to 450 units.",
         C_CYAN, 100),
        ("2. THEORY OF CONSTRAINTS (TOC BOTTLENECK SYNCHRONIZATION)",
         "Formula: System Throughput = min(R1, R2, ..., Rn)\n"
         "Application: Focuses capital expenditure exclusively on the active bottleneck process rather than spreading capital thin.",
         "Impact: Elevates station capacity from 48 units/hr to 75 units/hr, unlocking $1.4M annual throughput value.",
         C_PURPLE, 220),
        ("3. UNIT ECONOMICS: LTV / CAC RATIO",
         "Formula: LTV = (ARPU x Gross Margin %) / Churn Rate  |  Benchmark: LTV / CAC >= 3.0x\n"
         "Application: Confirms customer acquisition viability and payback horizon under competitive pressure.",
         "Proof: ARPU $1,200, Margin 68%, Churn 1.5%/mo ($816 / 0.015 = $54,400 LTV). With CAC $12,500 -> LTV/CAC = 4.35x.",
         C_AMBER, 340),
        ("4. BREAKEVEN VOLUME & CAPITAL HURDLE (NPV / IRR)",
         "Formula: BEP = Fixed Costs / Unit Contribution Margin  |  NPV = Sum(CF_t / (1+r)^t) - Capex\n"
         "Application: Establishes exact production volume required to cover implementation capital.",
         "Results: Capex $350k, Contribution Margin $85/unit -> BEP = 4,118 units. Payback achieved in 7.4 months.",
         C_TEAL, 460)
    ]

    for title, desc, eg, col, y in formulas:
        r = pymupdf.Rect(40, y, PAGE_W - 40, y + 105)
        p4.draw_rect(r, fill=C_SURFACE, color=C_BORDER, width=1)
        p4.draw_rect(pymupdf.Rect(40, y, 46, y + 105), fill=col)
        
        p4.insert_text(pymupdf.Point(56, y + 20), title, fontname="helv", fontsize=9.5, color=C_WHITE)
        p4.insert_textbox(pymupdf.Rect(56, y + 25, PAGE_W - 55, y + 65), desc, fontname="helv", fontsize=8, color=C_CYAN)
        p4.insert_textbox(pymupdf.Rect(56, y + 65, PAGE_W - 55, y + 100), eg, fontname="helv", fontsize=7.5, color=C_MUTED)

    # 3-Scenario Sensitivity Box at Bottom
    sens_rect = pymupdf.Rect(40, 580, PAGE_W - 40, 715)
    p4.draw_rect(sens_rect, fill=C_SURFACE_LIGHT, color=C_BORDER, width=1)
    p4.insert_text(pymupdf.Point(55, 600), "MANDATORY 3-SCENARIO SENSITIVITY TESTING MATRIX", fontname="helv", fontsize=9.5, color=C_WHITE)
    
    scenarios = [
        ("BEAR CASE (-20%)", "Capex +15%, Adoption -20%\nEBITDA: $850k\nPayback: 11.2 mo\nVerdict: Highly Viable", C_AMBER, 55),
        ("BASE PLAN (TARGET)", "Planned Target Execution\nEBITDA: $1.42M\nPayback: 7.4 mo\nVerdict: Benchmark Case", C_CYAN, 220),
        ("BULL CASE (+25%)", "Adoption +25%, Scale Efficiencies\nEBITDA: $2.15M\nPayback: 5.1 mo\nVerdict: Market Dominance", C_TEAL, 385)
    ]
    for s_title, s_txt, s_col, s_x in scenarios:
        s_box = pymupdf.Rect(s_x, 615, s_x + 150, 700)
        p4.draw_rect(s_box, fill=C_SURFACE, color=s_col, width=0.8)
        p4.insert_text(pymupdf.Point(s_x + 8, 632), s_title, fontname="helv", fontsize=8, color=s_col)
        p4.insert_textbox(pymupdf.Rect(s_x + 8, 640, s_x + 145, 695), s_txt, fontname="helv", fontsize=7, color=C_WHITE)

    # =========================================================================
    # PAGE 5: THE FINISHED RESOURCES DELIVERABLE SUITE
    # =========================================================================
    p5 = doc.new_page(width=PAGE_W, height=PAGE_H)
    p5.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H), fill=C_BG_DARK)
    add_page_header_footer(p5, 5, 6, "DELIVERABLE SPECIFICATION & ASSET SUITE")

    p5.insert_text(pymupdf.Point(40, 60), "SECTION 4: THE 12 FINISHED RESOURCES SUITE", fontname="helv", fontsize=15, color=C_WHITE)
    p5.insert_text(pymupdf.Point(40, 75), "Synchronized deliverable directory created autonomously inside 'Finished Resources/'", fontname="helv", fontsize=9, color=C_MUTED)

    deliverables = [
        ("01_Executive_Summary", "Executive_Summary.md", "1-page crisp memo with core thesis, key financials, and recommendation."),
        ("02_Strategic_Assessment", "Strategic_Assessment.md", "MECE root cause trees, competitive positioning, and market sizing."),
        ("03_Financial_Model", "financial_model.xlsx", "Dynamic 3-year proforma P&L, balance sheet, and sensitivity data."),
        ("04_Implementation_Roadmap", "Roadmap.md", "Horizon 1 (M1-6), Horizon 2 (M7-18), and Horizon 3 (M19-36) Gantt charts."),
        ("05_Risk_Matrix", "Risk_Matrix.md", "2x2 Impact vs Likelihood pre-mortem matrix with predictive leading KPIs."),
        ("06_Pitch_Deck", "Final_Presentation.pptx", "12-slide executive presentation ready for championship boardrooms."),
        ("07_Blueprints_and_PDFs", "Strategic_Blueprint.pdf", "Vector-grade executive solution document compiled via PyMuPDF."),
        ("08_Judge_QA_Defense", "Judge_QA_Defense.md", "Top 5 adversarial judge challenge questions and prepared rebuttals."),
        ("09_Video", "Final_Demo_120s.mp4", "120-second cinematic solution demonstration and animated walkthrough."),
        ("10_Web_Application", "React Web Simulator", "Live interactive browser simulation with dynamic sensitivity sliders."),
        ("11_Supporting_Research", "Competitions_DB.json", "132+ global case benchmarks and historical winning frameworks."),
        ("12_Audit_Logs", "Audit_Report.json", "Timestamped system execution telemetry and token efficiency records.")
    ]

    for idx, (folder, main_file, desc) in enumerate(deliverables):
        y = 95 + idx * 48
        r = pymupdf.Rect(40, y, PAGE_W - 40, y + 42)
        p5.draw_rect(r, fill=C_SURFACE, color=C_BORDER, width=0.8)
        
        # Folder icon indicator
        p5.draw_rect(pymupdf.Rect(40, y, 44, y + 42), fill=C_CYAN if idx % 2 == 0 else C_PURPLE)
        p5.insert_text(pymupdf.Point(52, y + 16), f"Finished Resources / {folder} /", fontname="helv", fontsize=8.5, color=C_WHITE)
        p5.insert_text(pymupdf.Point(235, y + 16), f"[{main_file}]", fontname="helv", fontsize=8, color=C_CYAN)
        p5.insert_text(pymupdf.Point(52, y + 32), desc, fontname="helv", fontsize=7.5, color=C_MUTED)

    # Deliverable Verification Stamp
    p5.draw_line(pymupdf.Point(40, 685), pymupdf.Point(PAGE_W - 40, 685), color=C_BORDER, width=0.8)
    p5.insert_text(pymupdf.Point(40, 705), "VERIFICATION STANDARD: Every file is generated deterministically with 100% reproducibility and strict anonymity.", fontname="helv", fontsize=8, color=C_TEAL)
    p5.insert_text(pymupdf.Point(40, 718), "All generated assets are ready for direct submission to judges, corporate clients, or academic review boards.", fontname="helv", fontsize=7.5, color=C_MUTED)

    # =========================================================================
    # PAGE 6: THE JUDGE STRESS-TEST PLAYBOOK & DEFENSE MATRIX
    # =========================================================================
    p6 = doc.new_page(width=PAGE_W, height=PAGE_H)
    p6.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H), fill=C_BG_DARK)
    add_page_header_footer(p6, 6, 6, "JUDGE DEFENSE & STRESS-TEST PLAYBOOK")

    p6.insert_text(pymupdf.Point(40, 60), "SECTION 5: JUDGE Q&A STRESS-TEST DEFENSE", fontname="helv", fontsize=15, color=C_WHITE)
    p6.insert_text(pymupdf.Point(40, 75), "Pre-calculated rebuttals for the 5 most adversarial competition judge challenges", fontname="helv", fontsize=9, color=C_MUTED)

    qa_list = [
        ("CHALLENGE 1: PILOT DELAY / IMPLEMENTATION SLIP",
         "Judge: 'What if software integration takes 10 months instead of 6?'",
         "Defense: Horizon 1 is modularized into four 45-day sub-sprints. Even under a 4-month delay, the Phase 1 buffer keeps payback under 9.2 months with 0 additional capex.",
         C_CYAN, 100),
        ("CHALLENGE 2: INCUMBENT PRICE RETALIATION",
         "Judge: 'What if competitors slash prices by 15% to defend their market share?'",
         "Defense: Our solution reduces unit operating cost by 38%, giving us structural cost leadership. We remain profitable at price points where competitors operate below cost.",
         C_PURPLE, 205),
        ("CHALLENGE 3: SENSITIVITY ASSUMPTION COLLAPSE",
         "Judge: 'How robust is your EBITDA if adoption stalls at 50% of your plan?'",
         "Defense: Under our Bear Case stress-test (-20% volume, +15% costs), Year 2 EBITDA remains positive at $850k with a healthy 2.8x interest coverage ratio.",
         C_AMBER, 310),
        ("CHALLENGE 4: CHANGE MANAGEMENT & WORKFORCE RESISTANCE",
         "Judge: 'How do you prevent frontline plant operators from bypassing the new tools?'",
         "Defense: The rollout uses a Train-the-Trainer model pairing operators with system champions, with 20% of quarterly performance bonuses tied to tool utilization.",
         C_TEAL, 415),
        ("CHALLENGE 5: CAPITAL CONSTRAINT & FINANCING FAILURE",
         "Judge: 'What if corporate leadership cuts your initial capex budget by 40%?'",
         "Defense: Horizon 1 is self-funding. The initial $120k pilot in Station 3 pays for itself within 90 days, generating the cash flow needed to fund Phases 2 and 3 organically.",
         C_CYAN, 520)
    ]

    for title, q, a, col, y in qa_list:
        r = pymupdf.Rect(40, y, PAGE_W - 40, y + 85)
        p6.draw_rect(r, fill=C_SURFACE, color=C_BORDER, width=1)
        p6.draw_rect(pymupdf.Rect(40, y, 46, y + 85), fill=col)
        
        p6.insert_text(pymupdf.Point(56, y + 18), title, fontname="helv", fontsize=9, color=col)
        p6.insert_text(pymupdf.Point(56, y + 33), q, fontname="helv", fontsize=8, color=C_WHITE)
        p6.insert_textbox(pymupdf.Rect(56, y + 40, PAGE_W - 55, y + 80), a, fontname="helv", fontsize=7.5, color=C_MUTED)

    # Championship Playbook Checklist
    chk_box = pymupdf.Rect(40, 625, PAGE_W - 40, 725)
    p6.draw_rect(chk_box, fill=C_SURFACE_LIGHT, color=C_TEAL, width=1)
    p6.insert_text(pymupdf.Point(55, 645), "CHAMPIONSHIP VICTORY CHECKLIST (FINAL VERIFICATION)", fontname="helv", fontsize=9.5, color=C_TEAL)
    
    chk_text = (
        "[x] Problem decomposed into Mutually Exclusive, Collectively Exhaustive root causes.\n"
        "[x] Explicit formulas stated with all variables, units, and baseline benchmarks.\n"
        "[x] Complete 3-year proforma statements with Bear (-20%), Base, and Bull (+25%) cases.\n"
        "[x] 3-horizon implementation roadmap with leading vs lagging predictive KPIs.\n"
        "[x] Top 5 adversarial judge challenges defended with evidence-backed data."
    )
    p6.insert_textbox(pymupdf.Rect(55, 655, PAGE_W - 55, 720), chk_text, fontname="helv", fontsize=7.8, color=C_WHITE)

    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    doc.close()
    print(f"[OK] Generated Pipeline UI PDF Guide at: {output_path}")

if __name__ == "__main__":
    out_pdf = "docs/CASE_COMPETITION_SYSTEM_PIPELINE_GUIDE.pdf"
    create_pipeline_guide_pdf(out_pdf)
