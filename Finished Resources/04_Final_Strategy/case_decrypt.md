# Case Decrypt — PortFlow Container Terminal: Yard and Gate Flow
**Archetype:** Operations & engineering improvement · **Family:** Throughput / capacity
**Solution model:** Baseline KPIs → bottleneck/root cause → optimize/simulate → pilot → ROI + KPIs

> This is a flow problem that looks like a space problem. Judges test whether you separate causes from symptoms with the case data (Little's Law on dwell), resist the obvious expansion, and still cover finance, operations and safety, supply chain, change management and AI within a $10M budget.

## SCQA
- **Situation:** PortFlow is a Canadian container terminal linking shipping lines, trucking, rail and inland customers. Today the yard holds 21,120 TEU against 24,000 TEU effective capacity (88%), containers dwell 6 days, and trucks take 72 minutes per visit (40 queuing, 32 inside). Volume will grow 20% in five years. The terminal spends $6M a year on overtime and $8M on delay and service penalties. Release and schedule information is not shared consistently, planning runs across separate systems on fixed rules, and the yard system knows a container's stack but not its exact position. One 15-acre parcel (about 4,000 TEU) could be added, phased around live operations.
- **Complication:** At +20% volume, the same 6-day dwell would need 106% of yard capacity, and trucks already take 72 minutes against a 45-minute objective. Overtime ($6M) and penalties ($8M) are rising, and the one expansion parcel would only bring utilization to 90.5%.
- **Question:** Which package, within the $10M upfront budget, attacks PortFlow's core issue so that at +20% volume the yard runs at or below 85% utilization and trucks turn in under 45 minutes by year five?
- **Answer:** Option B — Integrated flow package: shared visibility, appointments, AI-assisted yard planning — delivers 21.7% lower year-5 yard utilization (target 19.5%) for CAD $9,000,000 of the CAD $10,000,000 budget: NPV CAD $6,491,191 at 9.5%, payback 31.7 months. Five-year net financial impact (case formula): -CAD $16,500,000 (net savings).

## Issue tree
**How does PortFlow reach <= 85% yard utilization and < 45-minute truck turns at +20% volume, within $10M?**
- **Yard inventory (dwell)**: Why do containers stay 6 days: late release information, uncollected imports, early exports or empties? / What dwell meets 85%? (4.83 days on 24,000 TEU)
- **Yard handling (rehandles)**: How many crane moves are reshuffles because exact positions and pickup times are unknown? / Can stacking by pickup time free RTG hours for the 20% growth?
- **Gate and landside (arrivals)**: Why do trucks bunch: no appointments, no readiness signal? / What cuts the 40-minute queue and the 32 minutes inside?

## Hypothesis (first 20 minutes)
The core issue is fragmented release and schedule information, not a lack of space. Sharing it, booking trucks against ready containers and planning the yard around known pickups cuts dwell below 4.83 days and truck turn below 45 minutes without new land.

## Toolkit & quick math
- Little's Law: inventory = throughput x dwell
- Cause-versus-symptom tree (5 whys)
- Queueing view of truck arrivals: peak-to-average ratio
- Decision matrix with budget as a hard gate
- Today: 21,120 TEU / 6 days = 3,520 TEU/day; 21,120 / 24,000 = 88%
- Year 5: 4,224 TEU/day x 6 days = 25,344 TEU = 106% of capacity
- Expansion only: 25,344 / 28,000 = 90.5% (misses 85%)
- Dwell needed: 0.85 x 24,000 / 4,224 = 4.83 days (-19.5%)
- Truck turn: 40 + 32 = 72 min; target < 45 needs -27 min or more

## Solution ladder
| Level | Name | Rule | Pick |
| --- | --- | --- | --- |
| Level 1 | Quick win | Lowest capital: what a minimal move buys | Option A: 10% for CAD $4,100,000 (misses target, in budget) |
| Level 2 | Minimum compliant | Cheapest option that meets the target within budget | Option B: 21.7% for CAD $9,000,000 (meets target, in budget) |
| Level 3 | Value maximiser | Highest NPV within budget | Option B: 21.7% for CAD $9,000,000 (meets target, in budget) |
| Level 4 | Stretch | Largest improvement regardless of budget | Option B: 21.7% for CAD $9,000,000 (meets target, in budget) |

**Why the recommendation:** Option B is recommended. It is both the cheapest compliant option and the best value: a dominant choice.

## KPIs
| KPI | Baseline | Target |
| --- | --- | --- |
| Average yard dwell time | 6.0 days | <= 4.8 days (plan 4.7) |
| Year-5 yard utilization at +20% volume | 88% today; 106% if nothing changes | <= 85% (plan about 83%) |
| Truck turn time | 72 min (40 queue + 32 inside) | < 45 min (plan about 40) |
| Rehandles per container | measured in phase 1 | -30% |
| Overtime and penalties | $6M and $8M a year | $3.6M and $4.0M a year |
| Yard and gate safety incidents | current rate | no increase; near-misses reviewed weekly |

## 30 / 60 / 90 days
- **Days 1–30 — Validate & pilot:** Confirm baseline data and the binding constraint; Launch pilot of Option B at the constraint; Name owners; start KPI dashboard
- **Days 31–60 — Prove & decide:** Pilot gate: Slot adherence >= 80% on pilot lanes and no safety incidents; Lock fixed-price packages for scale-up; Train operators; write standard work
- **Days 61–90 — Scale & control:** Begin scale appointments, positioning and ai advice; Control chart on the primary KPI; Review vs target (19.5%) with sponsor

## Time plan (3-hour window)
| Time | Step | Output |
| --- | --- | --- |
| 0:00-0:25 | Read & align | SCQA, cause-vs-symptom tree, first hypothesis |
| 0:25-0:55 | Quick math | Little's Law, dwell threshold, truck turn gap |
| 0:55-1:40 | Package & finance | Initiatives, costs, owners, 5-year formula |
| 1:40-2:30 | Deck (8 slides) | Answer first, matrix, budget check, plan, risks |
| 2:30-3:00 | Rehearse & Q&A | 10-minute run, likely judge questions |

## Similar competitions (directory-listed; winners not verified)
- Boeing Northwest Case Competition (USA, Operations)
- Colorado State University Supply Chain Case Competition (USA, Supply chain)
- Carlson National Undergraduate Supply Chain Case Competition (USA, Supply chain)
- University of St. Thomas Supply Chain Case Competition (USA, Supply chain)
- Kohler Undergraduate Wisconsin Supply Chain Cup (USA, Supply chain)
