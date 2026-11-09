# Case Simulation & Competition Master Blueprint

**Classification**: Gold-Standard Strategy & Competition Architecture  
**Target Audience**: Collegiate, MBA, and Executive Case Competition Teams  
**Domain Scope**: Strategy, Operations, Financial Modeling, Go-To-Market, and Executive Pitching  

---

## 1. The Anatomy of a Winning Case Simulation

In elite case competitions (e.g., Harvard, Wharton, John Molson, Rotman, ICC), victory is determined by **five decisive dimensions**:
1. **Clarity of the Hook (First 60 Seconds)**: Does the presentation immediately present a bold, actionable thesis, or does it drown the judges in redundant background recitation?
2. **MECE Problem Framing**: Did the team address the true root-cause economic friction, or did they mistake symptoms for diseases?
3. **Quantitative & Unit Economics Rigor**: Are the financial proformas backed by verifiable baby-step math, unit economics ($), realistic CapEx/OpEx allocation, and 3-scenario sensitivity?
4. **Feasible 3-Horizon Operationalization**: Is there a concrete execution plan with stage gates, leading/lagging KPIs, and an honest risk pre-mortem?
5. **Q&A Unshakeability**: When judges challenge assumptions, does the team pivot to prepared contingency exhibits and defending data?

---

## 2. The 10-Slide Gold-Standard Deck Structure

Every case presentation deck generated or simulated in this workspace must conform to this 10-slide architectural storyline:

```
Slide 01: Executive Summary & Recommendation (The Hook + The Big Idea)
Slide 02: Industry Dynamics & Root-Cause Diagnosis (MECE Issue Tree)
Slide 03: Market Sizing & Segment Focus (TAM ──► SAM ──► SOM)
Slide 04: Strategic Alternatives Evaluation (Why Option B Beats A & C)
Slide 05: The Recommended Strategy (3 Mutually Reinforcing Strategic Pillars)
Slide 06: Operational Go-To-Market & Customer Journey Plan
Slide 07: Financial Proforma & Unit Economics (3-Year P&L, Payback, Sensitivity)
Slide 08: Phased Implementation Timeline (Horizon 1-3 Gantt Milestones)
Slide 09: Risk Governance & Pre-Mortem Matrix (2x2 Impact vs. Probability)
Slide 10: Conclusion & Call to Action (Expected ROI, Next 30-Day Priorities)
```

### The Action Title Rule:
Every slide header must be a complete declarative sentence communicating the slide's core insight, not a generic noun label.
- *Bad*: "Market Analysis"
- *Good*: "Mid-Market Industrial Facilities Suffer 18% Annual Margin Erosion Due to Unmonitored Downtime."

---

## 3. Quantitative & Financial Standards

### 1. Addressable Market Triangulation
- **Total Addressable Market (TAM)**: Global macro market spend.
- **Serviceable Addressable Market (SAM)**: Geographic and regulatory accessible target.
- **Serviceable Obtainable Market (SOM)**: Realistically capturable share in Years 1–3 given capital and sales capacity.

### 2. Unit Economics Invariants
$$\text{Customer Lifetime Value (LTV)} = \frac{\text{ARPU} \times \text{Gross Margin}}{\text{Annual Churn Rate}}$$
$$\text{Capital Efficiency Ratio} = \frac{\text{LTV}}{\text{CAC}} \ge 3.0\times$$
$$\text{Breakeven Volume} = \frac{\text{Fixed Implementation Overhead}}{\text{Unit Contribution Margin}}$$

### 3. Sensitivity Modeling
Never present a single-point financial projection. Always provide:
- **Bear Case (-20% Demand / +15% Costs)**: Stress-tests debt covenants and working capital floors.
- **Base Case (Management Plan)**: Target operational expectation.
- **Bull Case (+25% Adoption / -10% Churn)**: Highlights maximum upside potential and scale economics.

---

## 4. The Rapid 3-Hour Case Sprint Protocol

For time-boxed competitions, the team operates in 4 synchronized workstreams:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   3-HOUR TIME-BOXED WORKFLOW                           │
├───────────────┬────────────────────────────────────────────────────────┤
│ 00:00 - 00:30 │ Phase 1: Silent Case Read & MECE Issue Tree Mapping    │
│ 00:30 - 01:15 │ Phase 2: Hypothesis Selection & 3-Pillar Formulation   │
│ 01:15 - 02:15 │ Phase 3: Parallel Execution (Financials, GTM, Risks)   │
│ 02:15 - 02:45 │ Phase 4: Master Deck Assembly & Action Title Review    │
│ 02:45 - 03:00 │ Phase 5: Polish & Adversarial Judge Q&A Stress-Test    │
└───────────────┴────────────────────────────────────────────────────────┘
```

---

## 5. Security & Verification Policy

All code, plugins, agent skills, and external dependencies imported into this repository must pass:
1. **NVIDIA SkillSpector**: Automated static vulnerability and AST pattern scanning (`001 Main/05 - Security & Standards/SkillSpector`).
2. **Cloudflare Security Audit**: Comprehensive architecture, state, and client-side isolation review (`.agents/skills/security-audit`).
