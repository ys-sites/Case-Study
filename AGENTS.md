# Case-Study Studio Autonomous Workflow Rules: Case Simulation & Competition Law

For web application changes, strategy blueprints, rubrics, and formulas, follow the unified [Case Competition Master System](./docs/CASE_COMPETITION_MASTER_SYSTEM.md). Apply its design, accessibility, security, and verification guidance as relevant to the task.

For task routing across Graphify, installed skills, and the local resource library, follow [Main Brain Pipeline](./MAIN_BRAIN_PIPELINE.md).

For security verification of all agent skills and code, use **NVIDIA SkillSpector** (`001 Main/05 - Security & Standards/SkillSpector`) and the installed **Cloudflare Security Audit Skill** (`.agents/skills/security-audit`).

---

## 1. MANDATORY CASE SIMULATION & COMPETITION LAW
Before executing any case simulation, business challenge, or presentation task, the agent MUST review and adhere to this permanent pipeline rule:

### The Case Competition 5-Stage Standard:
Whenever the user provides a case brief, corporate statement, market dataset, or competition prompt, all generated documentation (Markdown strategy briefs, 10-slide pitch decks, financial models, executive memos) MUST adhere to the **5-Stage Case Competition Architecture**:

1. **Executive Summary & MECE Problem Diagnosis**:
   - Deliver an immediate, decisive executive hook ("The Big Idea").
   - Distinguish root causes from surface symptoms using MECE (Mutually Exclusive, Collectively Exhaustive) issue trees.
   - Frame the core value-capture bottleneck with quantified baseline metrics.

2. **Strategic Formulas & Theoretical Frameworks to Retain**:
   - State every business and financial formula explicitly with all variables, units, and benchmarks defined:
     - Addressable Market Triangulation: $\text{TAM} \longrightarrow \text{SAM} \longrightarrow \text{SOM}$
     - Customer Unit Economics: $\text{LTV} = \frac{\text{ARPU} \times \text{Gross Margin}}{\text{Churn Rate}}$ and $\frac{\text{LTV}}{\text{CAC}} \ge 3.0\times$
     - Breakeven Volume: $\text{BEP} = \frac{\text{Fixed Implementation Costs}}{\text{Unit Contribution Margin}}$
     - Capital Hurdle & Valuation: $\text{WACC}$, $\text{NPV}$, $\text{IRR}$, and Payback Horizon.

3. **Baby-Step Financial Proofs & Proforma Projections**:
   - Zero skipped intermediate arithmetic or algebra ($11 + 7 = 18$).
   - Provide complete 3-year proforma statements (Revenue, Gross Margin, OpEx, EBITDA).
   - Include 3-scenario sensitivity testing: Bear Case (-20%), Base Case (Plan), and Bull Case (+25%).

4. **Implementation Roadmap & Risk Pre-Mortem Matrix**:
   - Phased execution across 3 horizons (Horizon 1: Foundation & Pilot; Horizon 2: Commercial Rollout; Horizon 3: Scale & Industry Standardization).
   - Governance KPI dashboard separating **Leading Indicators** (Predictive) from **Lagging Indicators** (Financial).
   - 2x2 Risk Impact vs. Likelihood matrix with actionable pre-mortem mitigation plans.

5. **Judge Q&A Stress-Test Defense Bank**:
   - Dedicated section anticipating the top 5 most adversarial judge questions (assumptions sensitivity, competitor retaliation, capital constraints, operational bottlenecks, pilot failures).
   - Rigorous, evidence-backed rebuttals prepared for rapid presentation defense.

---

## 2. STRICT ANONYMITY & PRIVACY LAW (NO PERSONAL IDENTITY OR ABSOLUTE USER PATHS)
Under no circumstances should any personal name or machine-specific local drive paths (`/path/to/...`, `file:///...`, etc.) appear in ANY generated case brief, Markdown strategy guide, review sheet, PDF, HTML, or website file.
1. **Generic Designations Only**: All headers, footers, cover slides, and metadata must refer to generic academic or competition designations (e.g., `Strategy Consulting Hub`, `Executive Case Simulation Team`, `Academic Competition Strategy Platform`).
2. **Relative File Paths Only**: Any hyperlinks or references must use relative repository paths (`./cases/...` or `[Document Title](./filename.md)`) rather than machine-specific paths.
3. **Zero Machine Footers**: Never stamp local user paths onto rendered PDFs, slides, or web documents.

---

## 3. UNIFIED CASE FILE PLACEMENT & REPOSITORY STRUCTURE
- Primary Case Studies & Solution Briefs:
  `cases/<Case_Name>/01_Executive_Summary.md`  
  `cases/<Case_Name>/02_Strategic_Assessment.md`  
  `cases/<Case_Name>/03_Financial_Model.md`  
  `cases/<Case_Name>/04_Pitch_Deck_10_Slides.md`  
  `cases/<Case_Name>/05_Judge_QA_Defense.md`  
- Standalone Studio Web Application: `src/` (React + Vite + Tailwind CSS v4 + TypeScript)
- Local Knowledge & Skill Library: `001 Main/` (Ignored in Git, local references only)
- Verified Agent Skills: `.agents/skills/` (Audited via NVIDIA SkillSpector)

---

## 4. FAST, SMART & SAFE EXECUTION RULES (QUOTA & RATE-LIMIT PROTECTION)
1. **Targeted Access to `001 Main`**:
   - Use its README and task-specific resources as directed by `MAIN_BRAIN_PIPELINE.md`. Avoid broad scans, indiscriminate indexing, and loading unrelated materials.
2. **No Parallel Subagent Swarms**:
   - NEVER spawn multiple parallel subagents for batch tasks, as this immediately drains API rate limits. Execute work directly and sequentially.
3. **Speed & Targeted Scope**:
   - Read and modify only the specific files relevant to the user's request.
   - Do not scan the entire codebase when the target file is known.
   - Use targeted verification (`npm run build` or `python -m skillspector.cli scan`) only when relevant changes are made.

---

## 5. MANDATORY AUTOMATIC GIT PUSH LAW (ALWAYS PUSH)
On every prompt where changes, fixes, enhancements, or new files are created or modified:
1. **Always Push Automatically**: Proactively stage, commit with a descriptive message, and push directly to `origin` before concluding the turn.
2. **Never Wait to be Asked**: Every completed change is pushed automatically as the final step.
3. **Mandatory Remote Target**:
   - All commits and branch pushes MUST strictly target: `https://github.com/ys-sites/Case-Study.git`
   - Never push to alternate repositories without explicit user instruction.

---

## 6. CONCORDIA ILLUSTRATED ENGINEERING MOTION-VIDEO DIRECTIVE (THE 6 PILLARS)
Whenever designing, scripting, or rendering motion-graphics, visual lessons, or problem walkthroughs for engineering courses (ENGR 213, INDU 211, MIAE 215, MIAE 221), the agent MUST strictly adhere to the 6 pillars defined in `.agents/skills/concordia-motion-director/SKILL.md`:
1. **Pillar 1: Warm-White Illustrated Notebook Style**: Warm paper canvas (`#FCFBF7` to `#FAF8F3`), fine dark-ink contour lines (`#1E242B`), dimensional 3D isometric objects (crystal unit cells, Miller planes, stress-strain bars, MRP trees), real KaTeX mathematical write-on (`write.js`), and continuous camera choreography.
2. **Pillar 2: Two Video Archetypes**: Archetype A (7-Stage Narrative Arc for Topic Lessons) and Archetype B ("Solution-First" Law where Frame 0 = Step 1 for Quiz/Exam Solutions).
3. **Pillar 3: The Patient One-on-One Tutor**: Local `Kokoro-82M` neural TTS (`af_heart` at 0.90x-0.96x), phonetic spoken math, and 0.35s-0.6s breathing micro-pauses after key formulas.
4. **Pillar 5: Deterministic Canvas Engine**: Pure function of time $f(t)$ driven by word-level beats (`beats.json`), headless Chromium + FFmpeg via `001 Main/ode-motion-lessons`, scene builders (`write.js`, `xy.js`, `sheet.js`, `atoms.js`, `crystal.js`, `doodle.js`, `code.js`), and high-contrast warm-white posters.
5. **Pillar 5: Code-Synthesized Music & Ducking**: Original score ducked 22-27 dB under voice, procedural pen ticks and chapter swishes, normalized to -16 LUFS.
6. **Pillar 6: Website Registry & Chapter Schema**: Synchronized in `videoSources.ts` with explicit seconds-based chapter markers and poster metadata.
