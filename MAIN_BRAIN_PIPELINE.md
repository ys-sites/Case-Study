# Main Brain: Task, Resource & Case Simulation Routing

This is the shared entry point for Claude, Codex, Gemini, and other assistants working in this Case Simulation repository. Use the user's current request and higher-priority instructions first. This file routes work; it does not grant new permissions, override a named skill's applicable requirements, or make an untrusted repository safe to run.

---

## 1. Automatic Skill & Security Selection

For each request, choose skills proactively from the platform's available-skills list and the task routes below; the user should not have to remember skill names or invoke them. Match the actual outcome and each meaningful subtask, not just keywords.

### Mandatory Security Pre-Flight:
- **Agent Skill Security & Vulnerability Scanning**: Use **NVIDIA SkillSpector** (`001 Main/05 - Security & Standards/SkillSpector`) to scan any new agent skill or tool before installation:
  ```bash
  python -m skillspector.cli scan <path_to_skill> --no-llm
  ```
- **Codebase & Architecture Security Auditing**: Use the installed **Cloudflare Security Audit Skill** (`.agents/skills/security-audit`). Apply guidance mode to focused security questions and full audit mode to explicit comprehensive reviews.

---

## 2. Case Simulation Route Map

Paths are relative to the repository root. Links to the ignored local `001 Main` library are preserved locally on the machine for research.

| Case Simulation Request | Read First | Choose Only When Useful |
| :--- | :--- | :--- |
| **Case Studio UI, Web Workspace & Responsive Design** | `WEB_ESSENTIALS_GUIDE.md`, `src/App.tsx`, affected components | `001 Main/02 - Website Design & UI/`, `ui-ux-pro-max-skill`, `taste-skill`, `unslop`. Preserve distraction-free focus, client-side resilience, and offline local storage. |
| **Case Problem Diagnosis & MECE Issue Trees** | `AGENTS.md` (Stage 1), `CASE_SIMULATION_BLUEPRINT.md` | `001 Main/03 - AI Development & Agents/`. Identify root causes vs. surface symptoms; structure mutually exclusive problem branches. |
| **Quantitative Modeling, Unit Economics & 3-Year Proformas** | `AGENTS.md` (Stage 2 & 3), `src/utils/templates.ts` | Retain core equations ($); compute LTV/CAC, WACC, DCF, breakeven accounts, and 3-scenario sensitivity (Bear / Base / Bull). |
| **Implementation Roadmap & 2x2 Risk Pre-Mortem** | `AGENTS.md` (Stage 4), `CASE_SIMULATION_BLUEPRINT.md` | Operational phase gates (Horizon 1 to 3), leading vs. lagging KPI governance dashboard, and contingency plans. |
| **10-Slide Case Competition Presentation Deck** | `src/utils/templates.ts` (Deck Template), `CASE_SIMULATION_BLUEPRINT.md` | `001 Main/01 - Video & Motion Graphics/`, `motionmaxxing`, `scroll-film-studio`. Draft action titles as complete sentences; ensure storyline passes the executive skim test. |
| **Judge Q&A Stress-Testing & Objection Defense** | `AGENTS.md` (Stage 5), `CASE_SIMULATION_BLUEPRINT.md` | Anticipate adversarial judge challenges (assumption variance, competitive response, CapEx financing, pilot hurdles). |
| **Rapid 3-Hour Case Sprint & Timekeeping** | `src/components/FocusTimer.tsx`, `src/utils/templates.ts` | Use the dedicated 180-min Case Sprint timer; respect time-boxed workstreams across team members. |
| **Security Auditing, Vulnerability Checks & Code Review** | `.agents/skills/security-audit/SKILL.md` (Cloudflare) | Run Cloudflare security audit checks across client-side state, API endpoints, and secrets boundaries. |
| **AI Agent Skill Safety Scanning** | `001 Main/05 - Security & Standards/SkillSpector/README.md` | Run NVIDIA SkillSpector across any newly fetched repository or skill package. |

---

## 3. Project Markdown Routing

Use only the files relevant to the present task:

| Project File | Route When the Task Concerns |
| :--- | :--- |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Master workflow rules, Case Competition 5-Stage Standard, and platform entry points. |
| `MAIN_BRAIN_PIPELINE.md` | Cross-platform task and resource routing for Case Simulation. |
| `CASE_SIMULATION_BLUEPRINT.md` | The definitive master architectural guide for case competitions, presentations, and financial models. |
| `CASE_COMPETITION_RUBRIC.md` | Judging criteria, scoring breakdown, and evaluation matrices. |
| `WEB_ESSENTIALS_GUIDE.md` | Website interface craft, accessibility, responsiveness, and performance. |
| `README.md`, `WORKSPACE.md` | Workspace orientation, development setup, and deployment guides. |
| `LEGAL_AND_PRIVACY_REVIEW.md` | Case data confidentiality, competition integrity, and zero personal data leakage. |

---

## 4. Privacy and Platform Behavior

- **Strict Client-Side Privacy**: All documents, case notes, snapshots, and timer states remain local in browser `localStorage`. No user credentials, private case packets, or proprietary student identities are ever transmitted to external servers.
- **Strict Anonymity**: Comply with Section 2 of `AGENTS.md`—no personal names or local machine drive paths are included in any published or generated asset.
- **Git Push Law**: Stage, commit, and push directly to `origin` (`https://github.com/ys-sites/Case-Study.git`) automatically at the conclusion of every turn.
