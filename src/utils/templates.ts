import { Document } from '../types';

export interface DocumentTemplate {
  id: string;
  title: string;
  description: string;
  category: string;
  tags: string[];
  content: string;
}

export const TEMPLATES: DocumentTemplate[] = [
  {
    id: 'case-competition-deck',
    title: 'Case Competition Master Strategy Deck (10-Slide Executive Presentation)',
    description: 'Gold-standard 10-slide case competition structure featuring executive hook, diagnosis, 3 strategic pillars, financials, and judge defense.',
    category: 'Case Presentation',
    tags: ['case-competition', 'deck', 'executive-summary', 'strategy'],
    content: `# Case Competition Master Strategy Deck: 10-Slide Executive Briefing

**Team**: Strategy Consulting Hub  
**Case Subject**: Next-Generation Market Expansion & Operational Turnaround  
**Time Horizon**: 3-Year Strategic Horizon (2026 – 2029)  
**Target Recommendation**: Pivot from legacy transactional sales to high-margin subscription infrastructure.

---

## Slide 1: Executive Summary & Recommendation (The Hook)
> **The Core Thesis**: The target company faces margin compression not from volume loss, but from commoditization. By deploying **Operation Apex**—reallocating 35% of CapEx into digital lifecycle support—we achieve a **28.4% IRR**, **\$42.5M incremental EBITDA by Year 3**, and expand operating margin from 11.2% to 19.8%.

- **Primary Pain Point**: Customer churn increased from 4.1% to 11.8% as commoditized competitors shaved pricing by 15%.
- **Strategic Fix**: Introduce unified telemetry and predictive maintenance subscriptions.
- **Capital Required**: \$14.2M funded entirely through existing cash flow and debt optimization.
- **Payback Period**: 19 months.

---

## Slide 2: Industry Dynamics & Problem Diagnosis
### Root Cause vs. Surface Symptoms
| Surface Symptom | Root Cause | Underlying Economic Mechanism |
| :--- | :--- | :--- |
| Declining gross margin (-420 bps) | Unbundled aftermarket servicing | Independent third-party operators capture 68% of recurring parts margin. |
| Extended sales cycles (+35 days) | Fragmented product catalog | Enterprise clients evaluate 14 discrete SKUs rather than an end-to-end outcome. |
| Customer acquisition cost up 22% | Inefficient outbound marketing | Reliance on cold enterprise outreach rather than telemetry-driven triggers. |

---

## Slide 3: Market Sizing & Opportunity Assessment
### Addressable Market Triangulation
- **Total Addressable Market (TAM)**: \$8.4B global industrial automation market (CAGR: 7.8%).
- **Serviceable Addressable Market (SAM)**: \$2.1B North American mid-market facilities.
- **Serviceable Obtainable Market (SOM)**: \$185M target segment across existing client base (Year 1–3).

\`\`\`
TAM (\$8,400M) ──► SAM (\$2,100M) ──► SOM (\$185M Capture Target)
\`\`\`

---

## Slide 4: Strategic Alternatives Evaluation
### Why Strategy B Beats Alternatives A & C
1. **Alternative A (Price War)**: Match competitor discounts (-15%).  
   *Verdict*: **Rejected**. Erodes \$18M operating profit and destroys brand equity without creating switching costs.
2. **Alternative B (The Recommended Pivot)**: Integrated Hardware-as-a-Service + Subscription SLA.  
   *Verdict*: **Selected**. Drives recurring revenue to 54% of top line and lifts LTV/CAC from 2.6x to 5.4x.
3. **Alternative C (International Expansion)**: Enter European markets immediately.  
   *Verdict*: **Deferred**. Regulatory compliance and localization costs exceed initial capital budget (\$24M+).

---

## Slide 5: The Recommended Strategy (3 Strategic Pillars)
### Operation Apex: Architectural Blueprint
\`\`\`
┌───────────────────────────────────────────────────────────────┐
│                     OPERATION APEX                            │
├───────────────────┬───────────────────┬───────────────────────┤
│ Pillar 1: Connect │ Pillar 2: Monetize│ Pillar 3: Scale       │
│ Retrofit legacy   │ Deploy 3-tiered   │ Channel partner       │
│ hardware with IoT │ SLA maintenance   │ certification program │
│ sensor modules    │ contracts         │ across 12 territories │
└───────────────────┴───────────────────┴───────────────────────┘
\`\`\`

- **Pillar 1 (Connect)**: Standardize on an open telemetry gateway across 100% of installed base.
- **Pillar 2 (Monetize)**: Shift revenue model from spot billing to \$1,200/mo guaranteed uptime tier.
- **Pillar 3 (Scale)**: Incentivize regional distributor network with 18% recurring margin share.

---

## Slide 6: Go-to-Market & Operations Plan
- **Target Customer Persona**: VP of Plant Operations seeking zero unassisted downtime.
- **Pilot Phase (Q1-Q2)**: Onboard 20 enterprise accounts; target 99.5% uptime SLA compliance.
- **Commercial Rollout (Q3-Q4)**: Convert 250 existing accounts with guaranteed savings rebate.
- **Sales Incentive Structure**: 60% commission weighting on recurring ARR vs. 40% on one-off hardware.

---

## Slide 7: Financial Impact & Unit Economics
### 3-Year Proforma Summary (\$ in Millions)
| Metric | Baseline | Year 1 | Year 2 | Year 3 |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Revenue** | \$112.0M | \$124.5M | \$148.0M | \$176.2M |
| **Recurring ARR %** | 8.2% | 21.0% | 38.5% | 54.0% |
| **Gross Margin %** | 42.1% | 45.8% | 49.2% | 53.6% |
| **EBITDA** | \$12.5M | \$17.2M | \$28.6M | \$42.5M |
| **EBITDA Margin** | 11.2% | 13.8% | 19.3% | 24.1% |

### Unit Economics Mechanics
- Current Customer LTV: \$48,000 | Current CAC: \$18,500 (**2.6x LTV/CAC**)
- Projected Customer LTV: \$118,000 | Projected CAC: \$21,800 (**5.4x LTV/CAC**)

---

## Slide 8: Implementation Timeline & Milestones
\`\`\`
Month  01-03: Architecture & Gateway Firmware Validation
Month  04-06: Pilot Rollout (Top 20 Enterprise Accounts)
Month  07-12: Full Commercial Launch across Region 1 & 2
Month  13-24: Distributor Certification & Self-Serve Portal
Month  25-36: Market Dominance & Expansion into Adjacent Verticals
\`\`\`

---

## Slide 9: Risk Matrix & Contingency Planning
| Risk Event | Severity | Probability | Pre-Mortem Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Client Data Privacy Concerns** | High | Medium | SOC2 Type II certification & local on-premises edge computing mode. |
| **Hardware Supply Bottlenecks** | Medium | High | Dual-sourcing agreement across North America and Taiwan suppliers. |
| **Distributor Channel Pushback** | High | Low | Guarantee 18% recurring annuity margin on all activated client telemetry. |

---

## Slide 10: Conclusion & Call to Action
- **Capital Needed**: \$14.2M investment.
- **Deliverables**: \$42.5M Year 3 EBITDA, 54% recurring revenue, and dominant defensible moat.
- **Immediate Next Steps**: Form the 4-person executive implementation committee and launch Phase 1 pilot by Day 30.
`,
  },
  {
    id: 'strategic-diagnostic-framework',
    title: 'Comprehensive Strategic Assessment (SWOT, Porter\'s 5 Forces & PESTEL)',
    description: 'Complete diagnostic matrix analyzing external competitive pressures, macro factors, and internal capabilities.',
    category: 'Case Diagnostic',
    tags: ['swot', 'porters-five-forces', 'pestel', 'strategy', 'framework'],
    content: `# Comprehensive Strategic Assessment: Multi-Dimensional Diagnostic Matrix

**Organization Analyzed**: Market Incumbent Under Disruption  
**Academic / Competition Standard**: High-Yield Strategic Management  

---

## 1. PESTEL External Macro Analysis
- **Political**: Tightening compliance regulations in domestic and cross-border trade.
- **Economic**: Elevated interest rate climate constraining enterprise discretionary CapEx budgets.
- **Social**: Shifting workplace expectations toward automated, remote, and self-service diagnostics.
- **Technological**: Pervasive adoption of real-time edge processing and predictive machine intelligence.
- **Environmental**: Strict carbon accounting and energy efficiency disclosure mandates.
- **Legal**: Strict liability guidelines on data stewardship and equipment safety warranties.

---

## 2. Porter's Five Forces Industry Landscape
### Competitive Intensity: **HIGH**
1. **Threat of New Entrants (MODERATE)**: High capital intensity for tooling, but software-only entrants bypass traditional distribution.
2. **Bargaining Power of Suppliers (LOW - MODERATE)**: Off-the-shelf semiconductors and standardized mechanical components are multi-sourced.
3. **Bargaining Power of Buyers (HIGH)**: Enterprise procurement teams wield significant leverage and demand outcome-based pricing.
4. **Threat of Substitutes (HIGH)**: Cloud-native pure software analytics and third-party refurbished repair shops.
5. **Rivalry Among Existing Competitors (INTENSE)**: 4 major incumbents competing on commoditized bids; price cutting eroding margins.

---

## 3. SWOT Diagnostic Matrix
### Strengths (Internal Defensible Assets)
- Established brand heritage with 28-year market presence.
- 4,200 active equipment installations across North America.
- High customer satisfaction (NPS +62) for field technician quality.

### Weaknesses (Internal Execution Gaps)
- Siloed business units (Hardware sales and Aftermarket services operate independently).
- Disconnected software tools; client orders require manual spreadsheet coordination.
- Zero recurring subscription revenue; 92% of income is transactional.

### Opportunities (External Growth Vectors)
- 72% of installed base is eligible for IoT telemetry retrofit.
- Enterprise clients actively looking to consolidate 5 vendors into 1 trusted provider.
- Municipal grant subsidies for energy-efficient motor retrofits.

### Threats (External Environmental Hazards)
- Aggressive foreign low-cost competitors offering 20% cheaper mechanical clones.
- Escalating wage inflation for specialized field maintenance technicians.
- Cybersecurity vulnerabilities in unpatched legacy factory floor controllers.

---

## 4. Core Strategic Bottleneck & Resolution
> **Diagnostic Finding**: The company does not suffer from a demand deficit; it suffers from a **value capture deficit**. By shifting from selling hardware once to guaranteeing system productivity continuously, the organization breaks out of the commoditization trap.
`,
  },
  {
    id: 'financial-unit-economics-model',
    title: 'Financial Viability, Unit Economics & ROI Model (3-Year Projections)',
    description: 'Rigorous financial breakdown including CapEx/OpEx, customer LTV/CAC ratios, breakeven formulas, and sensitivity analysis.',
    category: 'Financial Model',
    tags: ['finance', 'unit-economics', 'pro-forma', 'sensitivity', 'roi'],
    content: `# Financial Viability, Unit Economics & ROI Valuation Model

**Model Horizon**: 3-Year Projection (Year 1 to Year 3)  
**Cost of Capital (WACC)**: 9.5%  
**Target Hurdle Rate**: 18.0%  

---

## 1. Capital Expenditure (CapEx) vs. Operating Expenditure (OpEx)
### Required Implementation Capital: \$14,200,000

| Category | Description | Amount (\$) | Allocation % |
| :--- | :--- | :--- | :--- |
| **Telemetry Hardware R&D** | Gateway engineering & firmware hardening | \$3,800,000 | 26.8% |
| **Cloud Software Architecture** | Real-time analytics dashboard & client portal | \$4,400,000 | 31.0% |
| **Sales Enablement & Training** | Field force retraining on subscription models | \$2,200,000 | 15.5% |
| **Channel Partner Incentives** | Early adopter reseller signing bonuses | \$1,800,000 | 12.7% |
| **Working Capital & Contingency** | Buffer for deployment cycle variances | \$2,000,000 | 14.0% |
| **TOTAL INITIAL INVESTMENT** | Complete Strategic Program | **\$14,200,000** | **100.0%** |

---

## 2. Customer Unit Economics & Margin Evolution
### Baseline vs. Post-Transformation
- **Hardware Spot Sale Margin**: 18.2%
- **Subscription SLA Contract Margin**: 64.5%

### Unit Economics Equation
$$\text{LTV} = \frac{\text{ARPU} \times \text{Gross Margin}}{\text{Churn Rate}}$$

- **Baseline Customer Economics**:
  - ARPU = \$12,000 / year
  - Gross Margin = 40% (\$4,800)
  - Annual Churn = 10.0%
  - **Baseline LTV** = \$\frac{4,800}{0.10}\$ = **\$48,000**
  - Current CAC = \$18,500
  - **Baseline LTV/CAC** = **2.59x**

- **Post-Transformation Customer Economics (Year 3)**:
  - ARPU = \$26,000 / year (Hardware amortized + SLA subscription)
  - Gross Margin = 54% (\$14,040)
  - Annual Churn = 4.2%
  - **Projected LTV** = \$\frac{14,040}{0.042}\$ = **\$334,285**
  - Projected CAC = \$24,000
  - **Projected LTV/CAC** = **13.9x**

---

## 3. Breakeven & Payback Period Mechanics
### Formula
$$\text{Breakeven Units} = \frac{\text{Fixed Implementation Costs}}{\text{Contribution Margin per Contract}}$$

- Fixed Program Cost = \$14,200,000
- Annual Net Contribution Margin per Subscription Account = \$11,400
- **Breakeven Accounts Required** = 1,245 active accounts
- With 4,200 installed accounts, required penetration is only **29.6%**.
- **Expected Payback Period**: **18.4 months** from launch.

---

## 4. 3-Scenario Sensitivity Analysis
| Metric | Bear Case (-20% Demand) | Base Case (Plan) | Bull Case (+25% Adoption) |
| :--- | :--- | :--- | :--- |
| **Y3 Revenue** | \$141.0M | \$176.2M | \$214.8M |
| **Y3 EBITDA** | \$27.5M | \$42.5M | \$61.2M |
| **IRR %** | 16.4% | 28.4% | 41.2% |
| **Payback Period** | 26.2 months | 18.4 months | 13.8 months |
| **NPV @ 9.5% WACC** | \$18.4M | \$44.8M | \$79.1M |
`,
  },
  {
    id: 'implementation-risk-governance',
    title: 'Implementation Roadmap & Risk Mitigation Matrix (Phased Milestones)',
    description: 'Detailed 3-phase execution roadmap, leading vs lagging KPI governance dashboard, and contingency plans.',
    category: 'Operations',
    tags: ['implementation', 'governance', 'roadmap', 'risk-management'],
    content: `# Implementation Roadmap & Risk Governance Matrix

**Program Sponsor**: Chief Operating Officer  
**Execution Lead**: VP of Strategic Transformation  
**Governance Cadence**: Bi-weekly Steering Committee & Monthly Board Review  

---

## 1. Phased 3-Horizon Execution Schedule

### Horizon 1: Foundation & Alpha Pilot (Months 1 – 6)
- [ ] **Month 1**: Establish Program Management Office (PMO) and freeze technical gateway architecture.
- [ ] **Month 2**: Finalize cloud infrastructure security and SOC2 audit preparation.
- [ ] **Month 3**: Select 20 top-tier enterprise clients for Beta trial; deploy initial 100 IoT retrofits.
- [ ] **Month 4**: Monitor telemetry ingestion, real-time alert latency (<150ms), and false-positive rates.
- [ ] **Month 5**: Iterate SLA agreement terms based on pilot client procurement feedback.
- [ ] **Month 6**: Horizon 1 Stage-Gate Review: Validate 99.5% uptime SLA achievement before capital release.

### Horizon 2: Commercial Rollout & Channel Expansion (Months 7 – 18)
- [ ] **Month 7**: Open self-serve client portal and announce Operation Apex at annual industry summit.
- [ ] **Month 9**: Launch certified distributor enablement program across 12 primary regional markets.
- [ ] **Month 12**: Achieve 500 active commercial subscription accounts.
- [ ] **Month 15**: Implement automated cross-selling algorithms based on equipment operating cycles.
- [ ] **Month 18**: Horizon 2 Stage-Gate Review: Assess recurring ARR contribution and churn metrics.

### Horizon 3: Scale & Industry Standardization (Months 19 – 36)
- [ ] **Month 24**: Surpass 1,200 active accounts (Breakeven threshold reached).
- [ ] **Month 30**: Introduce OEM integration agreements for third-party machine manufacturers.
- [ ] **Month 36**: Fully transition company valuation multiple from 6x industrial EBITDA to 14x SaaS EBITDA.

---

## 2. Governance KPI Dashboard
### Leading Indicators (Predictive Health)
- **Pilot Telemetry Uptime**: Target > 99.8%
- **Sales Rep Certification Rate**: Target 100% within 60 days
- **Pipeline Conversion Velocity**: Target < 45 days from proposal to contract

### Lagging Indicators (Financial Outcomes)
- **Monthly Recurring Revenue (MRR)**: Target \$2.4M by Month 24
- **Gross Revenue Retention (GRR)**: Target > 94%
- **Net Revenue Retention (NRR)**: Target > 115%
- **Operating Cash Flow**: Target > \$30M annually by Year 3

---

## 3. Comprehensive Risk Mitigation Matrix
\`\`\`
  IMPACT
    ▲
  H │  [2] Client Cyber Breach       │  [1] Supply Chain Delay
    │  (Mitigation: SOC2 Type II)    │  (Mitigation: Dual Source)
    ├────────────────────────────────┼──────────────────────────────
  L │  [3] Competitor Response       │  [4] Slow Distributor Pickup
    │  (Mitigation: 3yr Contracts)   │  (Mitigation: 18% Annuity)
    └────────────────────────────────┴──────────────────────────────►
                    L                              H      PROBABILITY
\`\`\`
`,
  },
  {
    id: 'rapid-3hr-case-sprint',
    title: 'Rapid 3-Hour Case Sprint Framework (Competition Battle Plan)',
    description: 'Time-boxed protocol for collegiate and MBA case competitions from first read to final pitch deck polish.',
    category: 'Sprint Workflow',
    tags: ['sprint', 'time-management', 'case-competition', 'workflow'],
    content: `# Rapid 3-Hour Case Sprint Protocol: Competition Battle Plan

**Total Time Window**: 180 Minutes  
**Deliverable**: 10-Slide Pitch Deck + 1-Page Executive Leave-Behind  
**Team Composition**: 4 Members (Lead Strategist, Financial Modeler, Operations Lead, Deck Architect)  

---

## ⏱️ Master Countdown Schedule

### Phase 1: 00:00 – 00:30 | Independent Read & Issue Tree Construction
- **00:00 - 00:15**: Individual silent read of case brief; highlight constraints, financial tables, and board mandates.
- **00:15 - 00:30**: Team reconvene. Map the core problem onto a MECE (Mutually Exclusive, Collectively Exhaustive) issue tree:
  - *Branch A*: Top-line revenue stagnation.
  - *Branch B*: Cost structure and operating inefficiency.
  - *Branch C*: Balance sheet leverage and liquidity limitations.

### Phase 2: 00:30 – 01:15 | Hypothesis Formulation & Strategic Selection
- **00:30 - 00:45**: Brainstorm 3 distinct strategic paths (Conservative, Bold Pivot, Aggressive M&A).
- **00:45 - 01:00**: Score options on a 2x2 Matrix: **Feasibility vs. Financial Impact**.
- **01:00 - 01:15**: Lock the winning strategy ("The Big Idea"). Define the 3 supporting execution pillars.

### Phase 3: 01:15 – 02:15 | Parallel Workstream Execution
- **Financial Modeler**:
  - Build 3-year income statement, CapEx schedule, and LTV/CAC unit economics.
  - Compute IRR, Breakeven, and Sensitivity Matrix.
- **Operations Lead**:
  - Build implementation timeline (Horizon 1-3), GTM plan, and risk pre-mortem table.
- **Lead Strategist & Deck Architect**:
  - Draft slide titles as complete declarative sentences (Action Titles).
  - Structure each slide's visual hierarchy and evidence callouts.

### Phase 4: 02:15 – 02:45 | Slide Assembly & Action Title Review
- Combine financial exhibits, Gantt chart, and strategic framework into master deck.
- Verify the **"Executive Storyline Test"**: Reading only the slide headers must tell a cohesive, persuasive story.

### Phase 5: 02:45 – 03:00 | Polish & Judge Q&A Stress Test
- Double-check all math ($11 + 7 = 18; no arithmetic errors).
- Anticipate the 5 toughest questions judges will ask:
  1. *"What happens if your primary assumption is off by 30%?"*
  2. *"Why won't the market leader crush you within 6 months?"*
  3. *"How do you finance the initial CapEx without diluting equity?"*
  4. *"What is the single biggest operational bottleneck in Phase 1?"*
  5. *"What does your team do if the pilot achieves only 50% adoption?"*
- Prepare appendix slides to address each objection instantly.
`,
  },
];

export const INITIAL_DOCUMENTS: Document[] = [
  {
    id: 'doc-1',
    title: 'Case Competition Master Strategy Deck: 10-Slide Executive Briefing',
    content: TEMPLATES[0].content,
    tags: ['case-competition', 'deck', 'strategy'],
    category: 'published',
    isFavorite: true,
    createdAt: Date.now() - 86400000 * 2,
    updatedAt: Date.now() - 3600000 * 1,
    snapshots: [
      {
        id: 'snap-1',
        timestamp: Date.now() - 86400000,
        title: 'Initial Case Problem Diagnosis',
        content: '# Case Competition Master Strategy Deck\n\nNotes on root cause diagnosis and 3-pillar strategy.',
        wordCount: 14,
      },
    ],
  },
  {
    id: 'doc-2',
    title: 'Comprehensive Strategic Assessment (SWOT, Porter\'s 5 Forces & PESTEL)',
    content: TEMPLATES[1].content,
    tags: ['swot', 'porters-five-forces', 'framework'],
    category: 'published',
    isFavorite: true,
    createdAt: Date.now() - 86400000 * 3,
    updatedAt: Date.now() - 3600000 * 5,
    snapshots: [],
  },
  {
    id: 'doc-3',
    title: 'Financial Viability, Unit Economics & ROI Valuation Model',
    content: TEMPLATES[2].content,
    tags: ['finance', 'unit-economics', 'roi'],
    category: 'draft',
    isFavorite: false,
    createdAt: Date.now() - 86400000 * 4,
    updatedAt: Date.now() - 3600000 * 8,
    snapshots: [],
  },
  {
    id: 'doc-4',
    title: 'Rapid 3-Hour Case Sprint Protocol: Competition Battle Plan',
    content: TEMPLATES[4].content,
    tags: ['sprint', 'time-management', 'workflow'],
    category: 'draft',
    isFavorite: false,
    createdAt: Date.now() - 86400000 * 5,
    updatedAt: Date.now() - 86400000 * 1,
    snapshots: [],
  },
];
