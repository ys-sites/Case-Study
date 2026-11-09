# Main Brain: Master Task, Skill & Graphify Routing Pipeline

> **CRITICAL AGENT ENTRY POINT**:  
> Every AI agent (Claude, Gemini, Codex, Antigravity) arriving at this repository MUST inspect and follow this file first on every single prompt.  
> This is the central dispatch router. All comprehensive case competition standards, rubrics, blueprints, and formulas are unified in [docs/CASE_COMPETITION_MASTER_SYSTEM.md](./docs/CASE_COMPETITION_MASTER_SYSTEM.md).

---

## 1. THE GRAPHIFY KNOWLEDGE NAVIGATION ENGINE

This repository utilizes **Graphify** (`https://github.com/Graphify-Labs/graphify.git`) located in `.claude/skills/graphify/` and `001 Main/03 - AI Development & Agents/graphify/`.

### Graphify Query Protocol:
Whenever exploring codebase architecture, cross-file relationships, or complex concepts:
1. **Fast-Path Check**: Check if `graphify-out/graph.json` exists.
2. **Execute Graph Queries**:
   - `graphify query "<question>"`: Breadth-first search for broad architectural context.
   - `graphify query "<question>" --dfs`: Depth-first search for specific trace paths.
   - `graphify path "<Concept_A>" "<Concept_B>"`: Shortest path between two system nodes.
   - `graphify explain "<Concept>"`: Plain-language explanation of a specific subsystem node.
3. Read raw code files only for specific line ranges identified by Graphify or targeted lookups.

---

## 2. CENTRAL TASK ROUTING & SKILL DISPATCH MATRIX

Match the user's intent to the appropriate skill and resource below:

| User Task / Request | Skill / Resource Location | Execution Action |
| :--- | :--- | :--- |
| **Solve a New Case Competition** | `scripts/case_orchestrator.py` | Run `python scripts/case_orchestrator.py <case_path_or_id>` (`ENG-0001`, `ENG100K-…`, `ENG1M-…`, or a PDF/MD/TXT/JSON/dir). Scores the 3 options, picks the winner from the numbers (budget = hard gate), builds one `solution_spec.json`, and renders every deliverable from it (2 PDFs, 12-slide PPTX, 3 XLSX with live formulas, 120s MP4). Agent 14 then runs 9 real gates (PASS/WARN/FAIL; exit code 2 on FAIL). Flags: `--out DIR`, `--no-video` (fast), `--spec-only`, `--unit-value CAD`. Read `11_Final_Quality_Control/unresolved_issues.md` before presenting. |
| **Case Strategy, Deck Blueprint & Formulas** | `docs/CASE_COMPETITION_MASTER_SYSTEM.md` | Consult the 5-Stage Standard, 10-Slide Deck Blueprint, and Unit Economics formulas ($\text{LTV}/\text{CAC} \ge 3.0\times$, $\text{WACC}$, $\text{BEP}$). |
| **Competition Scoring & Judging Evaluation** | `docs/CASE_COMPETITION_MASTER_SYSTEM.md` | Apply the 100-Point Rubric across Strategy (25%), Financials (25%), Implementation (20%), Risk (15%), and Q&A Defense (15%). |
| **Interactive Case Simulation & Role-Play** | `data/engineering_1000_case_simulations.json` | Select any case ID (`ENG-0001` through `ENG-1000`). Role-play client executives, withhold answers, demand 3 alternatives, score via 100-pt rubric. |
| **Global Case Competitions Research (132+)** | `data/global_case_competitions_research.csv` | Browse or filter verified global competitions, solution models, and official directory sources. Synchronized in `src/data/competitions.json`. |
| **Web Studio UI, Simulator & Components** | `src/App.tsx`, `src/components/` | Modify React components. Verify with `npm run build` (`tsc --noEmit && vite build`). Features `CaseSimulatorModal` and `GlobalCompetitionsModal`. |
| **Motion Graphics & Demonstration Video** | `.agents/skills/motionmaxxing/`, `scroll-film-studio/` | Create scripted motion graphics, GSAP curves, or render 120s demonstration video via FFmpeg. |
| **Concordia Illustrated Engineering Motion Videos** | `.agents/skills/concordia-motion-director/`, `001 Main/ode-motion-lessons/` | Render warm-white illustrated engineering lessons and quiz walkthroughs adhering to the 6-pillar pipeline across ENGR 213, INDU 211, MIAE 215, and MIAE 221. |
| **Security Audit of Agent Skills** | `001 Main/05 - Security & Standards/SkillSpector` | Run `python -m skillspector.cli scan <path_to_skill> --no-llm` before adopting any new skill or package. |
| **Codebase & Architecture Security Review** | `.agents/skills/security-audit/` (Cloudflare) | Run Cloudflare security audit checks across state isolation, API endpoints, and supply chain. |

---

## 3. THE 14-AGENT AUTONOMOUS CASE PIPELINE

When a case is submitted, the orchestrator coordinates 14 specialized agents across 8 stages:

```text
Stage 1: Understand  ──► Agent 01: Case Intelligence Analyst
Stage 2: Investigate ──► Agent 02: Global Competition Researcher & Agent 03: Root Cause Analyst
Stage 3: Innovate    ──► Agent 04: Brainstorming & Innovation Agent
Stage 4: Decide      ──► Agent 05: Strategy Decision & Agent 09: Critical Reviewer / Red Team
Stage 5: Engineer    ──► Agent 06: Financial Modeling, Agent 07: Tech Architecture, Agent 08: Implementation Blueprint
Stage 6: Produce     ──► Agent 10: PDF Docs, Agent 11: PowerPoint, Agent 12: Website, Agent 13: Video Production
Stage 7: Validate    ──► Agent 14: Quality Assurance & Integration (Enforces Gates 1–7)
Stage 8: Package     ──► Canonical Finished Resources/ Directory Structure
```

---

## 4. MANDATORY REPOSITORY LAWS

### Law 1: Strict Anonymity & Data Confidentiality
- Never include any personal student name or machine-specific local drive paths (`/path/to/...`, `file:///...`) in ANY generated case brief, Markdown strategy guide, review sheet, PDF, HTML, or website file.
- Use generic designations only: `Strategy Consulting Hub`, `Executive Case Simulation Team`.

### Law 2: Mandatory Automatic Git Push
- On every prompt where changes, fixes, enhancements, or new files are modified:
  1. Stage all changes: `git add .`
  2. Commit with a descriptive message: `git commit -m "..."`
  3. Push directly to remote: `git push origin main`
- Remote target: `https://github.com/ys-sites/Case-Study.git`.

### Law 3: Zero-Bloat Root Directory
- Keep the repository root uncluttered and clean. All reference blueprints, rubrics, prompts, and documentation live in `docs/CASE_COMPETITION_MASTER_SYSTEM.md`.
- Archived legacy documents live exclusively in `docs/archive/`.
