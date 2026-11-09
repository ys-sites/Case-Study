# Case Decrypt — PortFlow Container Terminal: Yard and Gate Flow
**Archetype:** Operations & engineering improvement · **Family:** Throughput / capacity
**Solution model:** Baseline KPIs → bottleneck/root cause → optimize/simulate → pilot → ROI + KPIs

> Judges test whether you separate causes from symptoms, resist the obvious expansion, and use analytics and automation responsibly, covering finance, operations and safety, supply chain, change management and AI within $10M.

## SCQA
- **Situation:** PortFlow is a Canadian container terminal linking shipping lines, trucking, rail and inland customers. Today the yard holds 21,120 TEU against 24,000 TEU effective capacity (88%), containers dwell 6 days, and trucks take 72 minutes per visit (40 queuing, 32 inside). Volume will grow 20% in five years. The terminal spends $6M a year on overtime and $8M on delay and service penalties. Release and schedule information is not shared consistently, planning runs across separate systems on fixed rules, and the yard system knows a container's stack but not its exact position. One 15-acre parcel (about 4,000 TEU) could be added, phased around live operations.
- **Complication:** With +20% volume the yard passes capacity by year 5, trucks already take 72 minutes against a 45-minute objective, overtime ($6M) and penalties ($8M) keep rising, and the one expansion parcel would still leave the yard about 90% full.
- **Question:** Which package, within the $10M upfront budget, attacks PortFlow's core issue so that at +20% volume the yard runs at or below 85% utilization and trucks turn in under 45 minutes by year five?
- **Answer:** Option B — Dynamic yard: demand zoning, MIP/CRAFT slotting, tracking database, AI AGV pilot — delivers 21.7% lower year-5 yard utilization (target 19.5%) for CAD $9,400,000 of the CAD $10,000,000 budget: NPV CAD $6,091,191 at 9.5%, payback 32.7 months. Five-year net financial impact (case formula): -CAD $16,100,000 (net savings).

## Issue tree
**How does PortFlow reach <= 85% yard utilization and < 45-minute truck turns at +20% volume, within $10M?**
- **Placement (where boxes sit)**: Which container groups move most, and how far are they from their exit? / Can MIP + CRAFT cut flow x distance?
- **Order and timing (when they leave)**: Do stacks follow pickup order? / How does seasonal demand shift, and can slotting follow it?
- **Information and movement**: Do we know each box's exact slot and release status? / Can AGVs move boxes cheaper and safer than manual tractors?

## Hypothesis (first 20 minutes)
PortFlow's yard is static and blind. Demand-based zoning (MIP + CRAFT), dynamic slotting on one tracked database, and shared release status cut handling time and dwell enough to meet both objectives without new land; AI AGVs are piloted, not bet on.

## Toolkit & quick math
- MIP: container-group-to-block assignment
- CRAFT: pairwise exchange layout improvement
- Demand forecasting with seasonality
- Decision matrix with budget as a hard gate
- Today: 21,120 / 24,000 TEU = 88% full
- Year 5 at today's stay: about 25,300 TEU, over capacity
- Expansion only: about 90% (misses 85%)
- Truck turn: 72 min today; plan 15 queue + 22 inside = 37 min
- Budget: $9.4M of $10M; five-year impact -$16.1M

## Solution ladder
| Level | Name | Rule | Pick |
| --- | --- | --- | --- |
| Level 1 | Quick win | Lowest capital: what a minimal move buys | Option A: 3.9% for CAD $1,600,000 (misses target, in budget) |
| Level 2 | Minimum compliant | Cheapest option that meets the target within budget | Option B: 21.7% for CAD $9,400,000 (meets target, in budget) |
| Level 3 | Value maximiser | Highest NPV within budget | Option B: 21.7% for CAD $9,400,000 (meets target, in budget) |
| Level 4 | Stretch | Largest improvement regardless of budget | Option B: 21.7% for CAD $9,400,000 (meets target, in budget) |

**Why the recommendation:** Option B is recommended. It is both the cheapest compliant option and the best value: a dominant choice.

## KPIs
| KPI | Baseline | Target |
| --- | --- | --- |
| Average yard dwell time | 6.0 days | <= 4.8 days (plan 4.7) |
| Year-5 yard utilization at +20% volume | 88% today; 106% if nothing changes | <= 85% (plan about 83%) |
| Truck turn time | 72 min (40 queue + 32 inside) | < 45 min (plan about 37) |
| Rehandles per container | measured in phase 1 | -30% |
| AGV pilot availability and cost per move | manual tractors | >= 90% uptime; cost per move <= manual |
| Overtime and penalties | $6M and $8M a year | $3.6M and $4.0M a year |

## 30 / 60 / 90 days
- **Days 1–30 — Validate & pilot:** Confirm baseline data and the binding constraint; Launch pilot of Option B at the constraint; Name owners; start KPI dashboard
- **Days 31–60 — Prove & decide:** Pilot gate: Layout model beats today's travel by >= 20% in simulation; AGV safety case signed; Lock fixed-price packages for scale-up; Train operators; write standard work
- **Days 61–90 — Scale & control:** Begin re-zone, go dynamic, pilot 2 agvs; Control chart on the primary KPI; Review vs target (19.5%) with sponsor

## Time plan (3-hour window)
| Time | Step | Output |
| --- | --- | --- |
| 0:00-0:25 | Read & align | SCQA, cause-vs-symptom tree, first hypothesis |
| 0:25-0:55 | Quick math | Case KPIs, budget check, truck turn gap |
| 0:55-1:40 | Package & finance | Initiatives, costs, owners, 5-year formula |
| 1:40-2:30 | Deck (8 slides) | Answer first, matrix, budget check, plan, risks |
| 2:30-3:00 | Rehearse & Q&A | 10-minute run, likely judge questions |

## Similar competitions (directory-listed; winners not verified)
- Boeing Northwest Case Competition (USA, Operations)
- Colorado State University Supply Chain Case Competition (USA, Supply chain)
- Carlson National Undergraduate Supply Chain Case Competition (USA, Supply chain)
- University of St. Thomas Supply Chain Case Competition (USA, Supply chain)
- Kohler Undergraduate Wisconsin Supply Chain Cup (USA, Supply chain)
