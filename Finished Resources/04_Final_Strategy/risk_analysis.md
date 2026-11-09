# Risk Register

| Risk | Likelihood | Impact | Mitigation | Trigger |
| --- | --- | --- | --- | --- |
| AGV breakdown or navigation fault | Medium | High | Preventive maintenance plan and vendor SLA, sensor health monitoring, fenced lane, manual tractors as instant fallback | AGV availability < 90% or any unplanned stop in the lane |
| Tracking or database errors (wrong slot recorded) | Medium | High | OCR and crane-sensor double check on every move, nightly reconciliation audit, manual search procedure kept | Position accuracy < 99% in the daily audit |
| AI slotting or demand forecast wrong | Medium | Medium | Re-slots run weekly on actual bookings; planners approve; segregation rules locked; 6 weeks of shadow mode | Override rate > 30% or rehandles rise for 2 weeks |
| Re-zoning moves disrupt live operations | Medium | High | One block at a time, overnight housekeeping moves only, go-lives outside vessel peaks, rollback plan | Gate throughput below baseline for 2 shifts |
| Employee resistance to AGVs and AI | Medium | Medium | No layoffs from this program; drivers retrain as AGV supervisors and technicians; staff co-design before tools arrive | Training completion < 90% or advice acceptance < 50% |
| AGV pilot costs more than it saves | Medium | Medium | Fixed-price quote, pilot capped at 2 units, fleet expands only if the month-12 gate passes | Cost per move above manual tractor after 3 months |
