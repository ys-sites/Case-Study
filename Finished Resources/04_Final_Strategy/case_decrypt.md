# Case Decrypt — Cold-Chain Fulfillment Center — Capacity Scaling (unexpected demand increase)
**Archetype:** Operations & engineering improvement · **Family:** Throughput / capacity
**Solution model:** Baseline KPIs → bottleneck/root cause → optimize/simulate → pilot → ROI + KPIs

> This is a throughput / capacity problem under a hard budget. Judges are testing whether you find the binding driver before spending, compare three options on the same basis, and show what happens when the numbers move.

## SCQA
- **Situation:** Cold-Chain Fulfillment Center — Capacity Scaling (unexpected demand increase). Metropolitan public agency; disruption: unexpected demand increase. Capacity Scaling today: 1,190.00 units/day.
- **Complication:** Capacity Scaling must move from 1,190.00 units/day to 1,291.15 units/day (8.5%) within 3 months and CAD $866,000, while: installation restricted to weekends; Minimum availability 98.0%.
- **Question:** For the cold-chain fulfillment center operated by a metropolitan public agency, plan a capacity upgrade while protecting service quality following unexpected demand increase. Baseline capacity: 1,190 units/day. Deliver at least 8.5% improvement within 3 months under CAD 866,000 capital limit; installation restricted to weekends. Select a technically justified alternative and test what happens if performance falls 15%.
- **Answer:** Option C — Comprehensive architecture replacement for cold-chain fulfillment center — delivers 13% capacity scaling improvement (target 8.5%) for CAD $676,000 of the CAD $866,000 budget: NPV CAD $2,681,053 at 9.5%, payback 11.1 months.

## Issue tree
**How do we achieve 8.5% capacity scaling improvement within 3 months and CAD $866,000?**
- **Demand & mix**: Is the demand real and sustained? / Does product mix drive changeovers?
- **Capacity at the constraint**: Which stage runs at the highest utilisation? / Where are OEE losses: availability, speed or quality?
- **Flow between stages**: Where does WIP pile up or starve? / Are batch sizes and buffers sized to variability?

## Hypothesis (first 20 minutes)
The gap is one binding constraint, not total capacity: relieving it delivers the target without rebuilding the whole system.

## Toolkit & quick math
- Theory of Constraints (5 focusing steps)
- OEE = Availability × Performance × Quality
- Little's Law: WIP = Throughput × Flow time
- Discrete-event simulation
- Gap: 1,190.00 → 1,291.15 units/day
- Budget per % point of target: CAD $101,882
- Winner cost per % point delivered: CAD $52,000

## Solution ladder
| Level | Name | Rule | Pick |
| --- | --- | --- | --- |
| Level 1 | Quick win | Lowest capital: what a minimal move buys | Option A: 4.6% for CAD $232,000 (misses target, in budget) |
| Level 2 | Minimum compliant | Cheapest option that meets the target within budget | Option C: 13% for CAD $676,000 (meets target, in budget) |
| Level 3 | Value maximiser | Highest NPV within budget | Option C: 13% for CAD $676,000 (meets target, in budget) |
| Level 4 | Stretch | Largest improvement regardless of budget | Option C: 13% for CAD $676,000 (meets target, in budget) |

**Why the recommendation:** Option C is recommended. It is both the cheapest compliant option and the best value: a dominant choice.

## KPIs
| KPI | Baseline | Target |
| --- | --- | --- |
| Daily output | 1,190.00 units/day | 1,291.15 units/day |
| Constraint utilisation | measure in week 1 | set from pilot |
| OEE at the constraint | measure in week 1 | set from pilot |
| WIP | measure in week 1 | set from pilot |

## 30 / 60 / 90 days
- **Days 1–30 — Validate & pilot:** Confirm baseline data and the binding constraint; Launch pilot of Option C at the constraint; Name owners; start KPI dashboard
- **Days 31–60 — Prove & decide:** Pilot gate: Go/no-go: pilot result within 20% of model, no safety incidents; Lock fixed-price packages for scale-up; Train operators; write standard work
- **Days 61–90 — Scale & control:** Begin scale-up: comprehensive architecture replacement for cold-chain fulfillment center; Control chart on the primary KPI; Review vs target (8.5%) with sponsor

## Time plan (5-hour window)
| Time | Step | Output |
| --- | --- | --- |
| 0:00–0:40 | Read & align | SCQA, issue tree, first hypothesis |
| 0:40–1:50 | Data & quick math | Baseline, gap, vital-few drivers (80/20) |
| 1:50–3:20 | Options & decision | 3 costed options, matrix, NPV, sensitivity |
| 3:20–4:20 | Deck | Answer-first storyline, action titles |
| 4:20–5:00 | Rehearse & Q&A | Timed run-through, 20+ questions |

## Similar competitions (directory-listed; winners not verified)
- Boeing Northwest Case Competition (USA, Operations)
- Colorado State University Supply Chain Case Competition (USA, Supply chain)
- Carlson National Undergraduate Supply Chain Case Competition (USA, Supply chain)
- University of St. Thomas Supply Chain Case Competition (USA, Supply chain)
- Kohler Undergraduate Wisconsin Supply Chain Cup (USA, Supply chain)
