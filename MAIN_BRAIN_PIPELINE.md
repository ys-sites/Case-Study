# Main Brain: Case Pipeline Core Skill & Routing

> **AGENT ENTRY POINT.** Every agent (Claude, Gemini, Codex, Antigravity) reads this file first on every prompt.
> If the prompt contains or points to a **case** (a case file, brief, PDF, case ID, pasted case text, or a request to
> solve / crack / simulate / present a case), follow **§1 Case Request Protocol** exactly. Everything else routes via **§4**.
> Standards, rubrics and formulas: [docs/CASE_COMPETITION_MASTER_SYSTEM.md](./docs/CASE_COMPETITION_MASTER_SYSTEM.md).

---

## 1. CASE REQUEST PROTOCOL (core skill)

**Goal:** case in → decrypt it → generate every level of solution → choose the best on the numbers → produce
the submission pack (booklet PDF, deck, models, three videos) → tell the user what to check before submitting.

### Step 1 — Identify the input and the mode

| The user gives… | Input to pass |
| :--- | :--- |
| A case ID (`ENG-0001`…`ENG-1000`, `ENG100K-000001`…, `ENG1M-0000001`…) | the ID |
| A **real competition brief** (attached PDF, pasted case) | **Preferred:** transcribe it to `cases/<Short_Name>/case.json` in `structured_case_v1` format, then pass that path (template: `cases/PortFlow_Container_Terminal/case.json`) |
| A file (PDF, MD, TXT, JSON) | the path (free text only guesses budget/target and uses parametric options: use for quick looks) |
| A folder of case material | the folder path |
| Pasted text only, no time to structure it | save it to `cases/<Short_Name>/brief.md`, then pass that path |

**`structured_case_v1` (how to transcribe a real brief).** The free-text parser cannot read option costs, savings or
the brief's own formulas, so for a real case the agent does the decrypt thinking and writes it into the JSON:
- Core fields: `id`, `title`, `brief` (condensed, no personal names), `decision_question`, `objective`, `constraints`,
  `budget`, `timeline_months`; the primary metric as `baseline_metric/value/unit`, `target_metric`, `target_pct`
  (express two-target cases as the binding one, e.g. year-5 utilization; keep the other in `kpis`).
- `options` (A/B/C): `capex`, `improvement`, `annual_benefit`, `annual_opex`, `source` (`case datum` or
  `assumption: …`), `why_not` (one line for the rejected ones).
- `diagnosis` (cause vs symptom, with the case's own math), `pillars`, `package` (initiative, purpose, capex,
  annual_opex, owner), `horizons`, `risks`, `kpis`, `judge_questions` (`{question, answer}`).
- `analysis_sections`: one per required area in the brief (`title`, `points`, `deck_points`), e.g. Finance,
  Operations & Safety, Supply Chain, Organizational Change Management, AI & Automation.
- `decrypt`: case-specific `issue_tree`, `hypothesis`, `toolkit`, `quick_math`, `time_plan`, `scqa.complication`,
  `what_the_case_tests` (override the generic family templates).
- `deck`: `max_content_slides` and grouped `slides` when the brief caps the deck.
- Slide blocks for `Presentation_Slides.pdf`: `problem_statement`, `problem` (stats + chart), `causes`, `kpi_bars`,
  `savings`, `not_chosen`, `gantt` (phases, checkpoints, streams with owner/budget, rows, milestones, continuity),
  `market` (forces, peer benchmarks, implications, sourced; never invent market facts: search and cite).
The engine then adds the undiscounted five-year net impact (`Investment + 5 x (added annual costs - annual savings)`),
a Package page and a Required Analysis page to the booklet, a capped answer-first deck, both scenes to video 3, and
`06_PDF_Deliverables/Presentation_Slides.pdf`: 8 agenda slides numbered 2-9 (problem & root cause, solution,
congestion to flow, budget & decision matrix, financial case, Gantt, market analysis, risks) that slot in behind a
team's own title and agenda slides.

**PDF design standard (all PDFs, mandatory):** every PDF follows the `Case_Study_Booklet.pdf` style: pine header
band with section label and case ID, emerald/mint accents, canvas background, Segoe UI for structure, Georgia for
editorial lines, stat cards, mint caps kicker labels, `NN / TT` footer. New renderers import the colour tokens `C`
from `scripts/case_visual_pdf.py`; do not introduce new palettes or display fonts unless the user asks.

| The user wants… | Mode |
| :--- | :--- |
| "solve / crack / build the pack" (default) | **Solve**: Steps 2–5 |
| "simulate / practise / quiz me / role-play" | **Simulate**: §2. Do **not** reveal the solution before the user submits |
| "score my answer / judge this" | **Judge**: §3 |

### Step 2 — Run the engine (one command)

```bash
python scripts/case_orchestrator.py <ID | path>                 # full pack incl. 3 narrated videos (~2.5 min)
python scripts/case_orchestrator.py <ID | path> --no-video      # fast (~7 s): everything except MP4s
python scripts/case_orchestrator.py <ID | path> --spec-only     # print the computed solution JSON only
```
Other flags: `--out DIR` (scratch runs; never touches the website), `--no-tts` (offline: silent videos with
subtitles), `--unit-value CAD` (override monetisation when the case gives a value per unit).
Exit code `0` = no failed gates; `2` = at least one FAIL (read it, don't hide it).

### Step 3 — What the engine does (stages → modules)

| Stage | What happens | Module |
| :--- | :--- | :--- |
| 1. Intake | Normalise any input; extract baseline, target, budget, deadline, options (free text: budget chosen by context, misses logged as assumptions) | `case_orchestrator.load_case_data` |
| 2. Decrypt | Classify archetype (5 solution models) and objective family (8: throughput, service, reliability, safety, quality, energy, environment, cost, schedule); SCQA; MECE issue tree; hypothesis; toolkit; quick math | `case_intelligence.py` |
| 3. Economics | One cash model: NPV, IRR, monthly payback, benefit/cost, levelized cost; bear/base/bull; NPV tornado | `cash_model`, `sensitivity` |
| 4. Solution levels | Score 3 options (target 30%, NPV 25%, payback 15%, resilience 15%, headroom 15%; budget = hard gate). **Solution ladder**: L1 quick win → L2 minimum compliant → L3 value maximiser → L4 stretch, plus why the pick wins | `evaluate_options`, `solution_ladder` |
| 5. Plan & defend | 3-horizon roadmap, 30/60/90 days, top risks with triggers, KPIs, 13+ computed judge answers, pre-submission checklist | `build_horizons`, `build_qa_bank` |
| 6. Produce | Pinterest-style 7-page booklet, blueprint + memo PDFs, 12-slide PPTX, 3 XLSX with live formulas, 3 narrated videos | `case_visual_pdf.py`, `case_videos.py` |
| 7. Validate | 9 gates: inputs, assumptions, comparison, target, viability, integrity, cross-artifact consistency, anonymity, stale files | `run_quality_gates` |

### Step 4 — Read these outputs, in this order (`Finished Resources/`)

1. `11_Final_Quality_Control/compliance_checklist.md` (gate results) and `unresolved_issues.md`
2. `04_Final_Strategy/case_decrypt.md` (SCQA, issue tree, hypothesis, solution ladder, 30/60/90)
3. `04_Final_Strategy/executive_summary.md`
4. `11_Final_Quality_Control/submission_checklist.md`

Deliverables: `06_PDF_Deliverables/Case_Study_Booklet.pdf` (editorial booklet), `Strategic_Blueprint.pdf`,
`Final_Case_Solution.pdf`; `07_PowerPoint/Final_Presentation.pptx` + `judge_QA_preparation.md`;
`05_Financial_Models/*.xlsx`; `09_Video/01_The_Case.mp4` (what the case asks), `02_How_To_Tackle.mp4`
(method), `03_Solution_Brief.mp4` (answer + pre-submission brief), each with `.srt` and `_script.md`.

### Step 5 — Reply to the user (answer first)

1. **Recommendation in one sentence** with three numbers (gain vs target, capex vs budget, NPV/payback).
2. **Solution ladder**: the four levels and why the pick wins (from `case_decrypt.md`).
3. **Gate status**: every WARN/FAIL in plain words (e.g. "no option meets the target within budget"; "energy case:
   negative NPV on tariff alone, judge on CAD per kWh saved").
4. **Before you submit**: open items from `submission_checklist.md`, especially assumptions to replace with real data.
5. Links to the booklet, deck and the three videos.

**Interpreting results honestly:** a FAIL is information, not an error to suppress. Never edit outputs to turn a FAIL into
a PASS; fix the input data or explain the trade-off. Synthetic datasets are training cases, never "historical winners".

---

## 2. SIMULATE MODE (coach / role-play)

Follow `data/engineering_case_simulator_master_prompt.txt`: present the brief and data only; role-play client,
engineers, operators and regulators; disclose extra synthetic data only on request and label it as generated; require a
decision, 3 alternatives, a model, sensitivity, safety analysis, 10-slide proposal and plan. After the user presents:
run the engine with `--no-video --out <scratch>`, score with the case rubric (§3), ask four adversarial questions from
`intelligence.qa_bank`, then show the illustrative approach (the `02_How_To_Tackle` script).

## 3. JUDGE MODE

Score against the case's own rubric (`case_inputs.rubric`; default: diagnosis 20, rigour 25, feasibility & safety 20,
cost/impact 15, implementation 10, communication & Q&A 10). Compare the user's numbers with `solution_spec.json` and
cite the solution ladder level their pick sits on.

---

## 4. KNOWLEDGE BASE (`data/`) — what each source is for

| File | Content | Used by |
| :--- | :--- | :--- |
| `engineering_1000_case_simulations.json/.csv/.xlsx` | 1,000 synthetic cases: 20 disciplines × 5 scenarios (baseline, growth surge, budget-constrained, reliability crisis, low-carbon); 8 objective families; rubric + 4 judge questions each; option names without costs | intake (`ENG-xxxx`), family toolkits, rubric |
| `engineering_100000_preview.csv` | 100 throughput cases with option costs/gains and an **answer key** ("Illustrative Feasible Option") | intake (`ENG100K-…`); validation: engine agrees on 98/100 (the 2 differences pick higher-NPV over cheapest-compliant; both shown on the ladder) |
| `engineering_1million_additional_preview.csv` | 100 cold-chain cases across 8 disruptions × 5 constraints, costed options | intake (`ENG1M-…`) |
| `global_case_competitions_research.csv/.xlsx` | 132 competitions, 5 solution-model archetypes (directory-listed; winners NOT verified) | archetype model + "similar competitions" |
| `case-competition-master-prompt.pdf` | Winning model: SCQA, MECE, hypothesis in 20 min, 80/20, Lean/TOC tools, one recommendation, 30/60/90, Pyramid slides, 20+ Q&A, time split | decrypt layer, checklist, video 2 |
| `engineering_case_simulator_master_prompt.txt` | Facilitator rules for interactive simulation | §2 Simulate mode |

---

## 5. OTHER TASK ROUTING

| Request | Resource | Action |
| :--- | :--- | :--- |
| Case strategy, deck blueprint & formulas | `docs/CASE_COMPETITION_MASTER_SYSTEM.md` | 5-stage standard, deck blueprint, unit economics |
| Web studio UI / simulator | `src/App.tsx`, `src/components/` | Edit React; verify `npm run build`. `CaseSimulatorModal` reads `src/data/current_case_solution.json` (synced by canonical runs only) |
| Motion graphics beyond the 3 case videos | `.agents/skills/motionmaxxing/`, `scroll-film-studio/` | Scripted motion, GSAP, FFmpeg |
| Concordia illustrated engineering lessons | `.agents/skills/concordia-motion-director/` | 6-pillar lesson pipeline (ENGR 213, INDU 211, MIAE 215, MIAE 221) |
| Security audit of a skill/package | `001 Main/05 - Security & Standards/SkillSpector` | `python -m skillspector.cli scan <path> --no-llm` |
| Codebase security review | `.agents/skills/security-audit/` | Cloudflare audit checks |

### Graphify navigation (code questions)
If `graphify-out/graph.json` exists, run `graphify query "<question>"` before grepping or reading source;
`graphify explain "<node>"` for one subsystem; `graphify path "<A>" "<B>"` for relationships. Read raw files only for
located line ranges. After code changes: `graphify update .` (code-only, no private material).

---

## 6. MANDATORY REPOSITORY LAWS

### Law 1: Strict Anonymity & Data Confidentiality
- Never include personal student names or machine-specific paths (`C:\Users\…`, `/Users/…`, `file:///`) in any generated
  brief, guide, PDF, HTML, video or website file. Gate 8 enforces this automatically.
- Use generic designations only: `Strategy Consulting Hub`, `Executive Case Simulation Team`.

### Law 2: Mandatory Automatic Git Push
- On every prompt where files change: stage the changes, commit with a descriptive message, `git push origin main`.
- Remote target: `https://github.com/ys-sites/Case-Study.git`.

### Law 3: Zero-Bloat Root Directory
- Keep the repository root clean. Reference material lives in `docs/CASE_COMPETITION_MASTER_SYSTEM.md`;
  archived documents in `docs/archive/`.
