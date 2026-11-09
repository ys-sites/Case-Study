# Required Analysis — PortFlow Container Terminal: Yard and Gate Flow

> Option B — Dynamic yard: demand zoning, MIP/CRAFT slotting, tracking database, AI AGV pilot — delivers 21.7% lower year-5 yard utilization (target 19.5%) for CAD $9,400,000 of the CAD $10,000,000 budget: NPV CAD $6,091,191 at 9.5%, payback 32.7 months. Five-year net financial impact (case formula): -CAD $16,100,000 (net savings).

## Recommended package
| Initiative | Purpose | Upfront | Annual cost | Owner |
| --- | --- | --- | --- | --- |
| Yard zoning and block layout (MIP + CRAFT) | MIP assigns container groups to blocks by move frequency and exit; CRAFT swaps zones while flow x distance falls; re-marking and phased moves. | CAD $1,200,000 | CAD $100,000 | Yard Planning Manager |
| Dynamic slotting engine with demand forecasting | Re-slots containers as demand shifts (e.g. a December peak for one product) and stacks by planned pickup; planners approve. | CAD $1,600,000 | CAD $300,000 | Yard Planning Manager |
| Tracking and yard database (digital twin) | OCR cameras, RFID tags on vehicles and crane position sensors log every move into one yard database. | CAD $2,200,000 | CAD $350,000 | IT and Operations Manager |
| Release visibility and truck pickup windows | The database shares release and hold status with lines, truckers, rail and customers; trucks book windows for ready boxes. | CAD $1,400,000 | CAD $250,000 | Commercial Director |
| AI AGV pilot: 2 units in a fenced lane | Two battery AGVs, fleet software linked to the database, navigation, charging and safety fencing; scale only if KPIs pass. | CAD $1,600,000 | CAD $150,000 | Engineering and Maintenance Manager |
| Change management and paid training | Co-design workshops, super-users per shift, AGV supervisor and technician training in paid time. | CAD $600,000 | CAD $150,000 | HR Director with the Employee Representative |
| Contingency (about 9%) | Released at the phase-3 gate if unused. | CAD $800,000 | CAD $0 | Finance Director |

## Budget check and five-year net financial impact
| Item | Value |
| --- | --- |
| Upfront investment | CAD $9,400,000 of CAD $10,000,000 budget (CAD $600,000 headroom) |
| Additional annual costs | CAD $1,300,000 |
| Annual savings | CAD $6,400,000 |
| Formula | Investment + 5 x (additional annual costs - annual savings); undiscounted; negative = net savings |
| Result | CAD $9,400,000 + 5 x (CAD $1,300,000 - CAD $6,400,000) = **-CAD $16,100,000** |
| Cross-check (discounted) | NPV CAD $6,091,191 at 9.5%, payback 32.7 months |

## Directions considered
| Opt | Direction | Upfront | Gain | Meets target | 5-yr net impact | Score /10 |
| --- | --- | --- | --- | --- | --- | --- |
| A | Static re-zoning only: one-off MIP and CRAFT layout | CAD $1,600,000 | 3.9% | no | -CAD $7,400,000 | 5.22 |
| B ✔ | Dynamic yard: demand zoning, MIP/CRAFT slotting, tracking database, AI AGV pilot | CAD $9,400,000 | 21.7% | yes | -CAD $16,100,000 | 6.92 |
| C | Yard expansion on the 15-acre parcel with two added RTGs | CAD $14,500,000 | 14.3% | no | CAD $13,500,000 | 2.9 |

## Finance
- Upfront $9.4M of the $10M budget, including $0.8M contingency; $0.6M left unspent.
- Added annual costs $1.3M: software and database licences, sensors and AGV maintenance, model upkeep and refresher training.
- AGV pricing: a US DOT-hosted study put one terminal AGV at about EUR 150,000 (2021, conservative). We budget $1.6M for 2 units including navigation, charging, fleet software and fencing.
- Annual savings $6.4M with owners: overtime -40% ($2.4M, Operations Manager) from shorter travel, fewer rehandles and fewer re-plans; penalties -50% ($4.0M, Commercial Director) from reliable release information and faster truck service.
- Five-year net impact = $9.4M + 5 x ($1.3M - $6.4M) = -$16.1M (net savings).
- Uncertainty: the share of penalties caused by customs holds PortFlow cannot override. If penalties fall only 25%, the impact is still -$6.1M; break-even needs $3.2M a year.

## Operations & Safety
- Storage: shared release status and pickup windows cut dwell from 6.0 to 4.7 days, keeping year-5 utilization near 83% without new land.
- Container movement: MIP/CRAFT zoning puts high-demand groups next to their exit; dynamic slotting stacks by pickup order, so cranes stop digging.
- Truck service: queue 40 to about 15 min with pickup windows; time inside 32 to about 22 min with fast movers near the gate: about 37 minutes in total.
- Safety: AGVs run only in a fenced lane; segregation rules for hazardous, reefer and weight are locked in the model; every go-live has a safety review.
- Measures, reviewed weekly: utilization, dwell, rehandles per box, travel per move, queue and inside time, AGV uptime, incidents and near-misses.

## Supply Chain
- Shipping lines: vessel ETA changes flow into the database and trigger re-slotting before the ship arrives.
- Truckers: pickup windows only for released, ready containers, already staged near the gate.
- Rail: rail-bound containers zoned next to the rail exit and staged by train departure.
- Customers: release, hold and ETA alerts; seasonal demand signals (for example a December peak) feed the slotting forecast.
- Customs holds stay outside PortFlow's control but are flagged early so no truck is booked against a held box.

## Organizational Change Management
- Stakeholders: yard operators, tractor drivers, planners, maintenance, IT, truckers, rail, lines, customers and finance.
- Involve staff before tools arrive: planners and operators co-design zones and slotting rules in phase 1.
- Train in paid time: super-users per shift; tractor drivers can certify as AGV supervisors or technicians.
- Clarify roles: no layoffs from this program; a RACI for every zone, model and AGV decision.
- Keep operations running: one block re-zoned at a time, overnight moves, AGVs only in a fenced lane, rollback plan.

## AI & Automation
- MIP: assigns container groups (customer, product, direction) to blocks to minimise move frequency x distance to their exit, within block capacity and segregation rules.
- CRAFT: tests pairwise swaps of zones and keeps any swap that lowers total flow x distance, so the layout can be improved again as demand changes.
- Dynamic slotting: a demand forecast (seasonal peaks) plus actual bookings re-slot containers weekly; planners approve each change.
- AI AGVs: 2 battery units in a fenced quay-to-block lane, tracked by the yard database; overseen by the Engineering and Maintenance Manager with preventive maintenance.
- Performance checks: 6 weeks of shadow mode for slotting; AGV uptime, cost per move and incidents weekly; scale the fleet only if the month-12 gate passes.
