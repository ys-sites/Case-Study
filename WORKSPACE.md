# Case Simulation & Strategy Studio Workspace

This repository is the **single consolidated workspace** for Case-Study Studio—an executive strategy workspace, case competition preparation platform, and financial simulation studio.

---

## 1. Consolidated Directory Structure

### Public & Tracked Workspace Directories
- `src/` — React 19 + TypeScript + Vite + Tailwind CSS v4 single-page case simulation platform:
  - `src/components/` — Studio UI components (`Editor`, `MarkdownPreview`, `Header`, `Sidebar`, `FocusTimer`, `TemplatesModal`, `ExportModal`, `SnapshotDrawer`, `SettingsModal`, `ShortcutsModal`).
  - `src/utils/` — Strategic case templates (`templates.ts`), Markdown and LaTeX parser (`markdown.ts`), and Web Audio synthesis engine (`audio.ts`).
  - `src/types.ts` — TypeScript interfaces for case documents, snapshots, editor settings, and outlines.
- `cases/` — Structured case studies, strategic assessments, and financial models.
- `.agents/skills/` — Verified agent skills (including Cloudflare `security-audit`, `motionmaxxing`, `scroll-film-studio`, etc.).
- `.claude/skills/` — Claude Code integration skills (`graphify`).
- `docs/archive/` — Historical and retired non-case artifacts preserved for reference.

### Local-Only & Git-Ignored Directories (Never Pushed to Remote)
- `001 Main/` — Local research library containing reference tools, AI agent skill catalogs, UI/UX design guides (`ui-ux-pro-max-skill`, `taste-skill`, `unslop`), and security engines:
  - `001 Main/05 - Security & Standards/SkillSpector` — NVIDIA SkillSpector scanner.
  - `001 Main/05 - Security & Standards/security-audit-skill` — Cloudflare Security Audit local copy.
  - `001 Main/03 - AI Development & Agents/` — Local agent repositories (`ECC`, `bla`, `reverse-api-engineer`, `rune`).
  - `001 Main/08 - Workspace Support/project-nomad` — Homelab and communications reference.
- `node_modules/` — Local package dependencies.
- `dist/` — Compiled production build output.
- `*.log`, `.env*` — Local logs and environment secrets.

---

## 2. Core Operating Commands

```bash
# Install dependencies
npm install

# Start local development server
npm run dev

# Run TypeScript linting and build production bundle
npm run build

# Preview production build locally
npm run preview

# Scan a skill with NVIDIA SkillSpector
python -m skillspector.cli scan <path_to_skill> --no-llm
```
