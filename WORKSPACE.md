# Concordia Engineering Workspace

This repository is the **single consolidated workspace** for the Concordia University Gina Cody School of Engineering learning platform and course materials (`ENGR 213`, `INDU 211`, `MIAE 215`, `MIAE 221`).

## Consolidated Directory Structure

### Public & Tracked Workspace Directories
- `website/` — Vite + React + TypeScript interactive learning application, 2D/3D visual learners (`src/learn/visual3d/`, `src/learn/crystal/`), curriculum definitions (`src/learn/curriculum/`), formula hubs, and quiz engines.
- `Engr 213/` — Applied Ordinary Differential Equations lecture notes (`01 - Teacher Lecture Notes/`, including Lectures 1–14), comprehensive topic guides, and explained notes.
- `Indu 211/` — Introduction to Production and Manufacturing Systems lecture slides, topic guides, and formula companions.
- `Miae 215/` — Programming for Mechanical and Industrial Engineers (C++) lecture notes, comprehensive topic guides, and practice materials.
- `Miae 221/` — Materials Science lecture slides, comprehensive topic guides, and formula sheets (`formula/`).
- `Studocu/` — Upload queue (`Need to Upload/`) and completed archive (`Done/`) metadata logs.
- `THE_NEXT_STEP.md` — Interactive visual learning engine architecture and 3D/2D visualization blueprint.
- `WEB_ESSENTIALS_GUIDE.md` — Project-specific design, accessibility, security and verification guidance adapted from the supplied website essentials.

### Local-Only & Git-Ignored Directories (Never Pushed to Remote)
All private files, large binary archives, reference libraries, and historical recovery checkouts are consolidated inside this workspace and excluded from Git via `.gitignore`:
- `001 Main/` — Local visual-learning research library, reference repositories, and `motion-video-director` skill bundle.
- `_Source & Archive/` and `<Course>/_Source & Archive/` — Private personal documents, blank source copies, textbooks, and local working archives.
- `<Course>/*Solutions*` & `<Course>/05 - Assignments & Solutions/` — Private homework and assignment solutions, local MP4 video renders, and portable compiler toolchains (`CodeBlocks_17.12_portable`, `MinGW`).
- `Local Semester Archive/` — Complete local preservation archive from the retired `Semester 1` duplicate checkout:
  - `Local Semester Archive/Semester 1 (original checkout)/` — Retired duplicate Git checkout (`.git` at `bce1829`, scratch scripts, and historical working tree).
  - `Local Semester Archive/bce1829-commit-files/` & `semester-1-unpushed-commit.patch` — Full patch and extracted files from the older checkout's unpushed commit `bce182989c105edb1400ce39a62f31d6b76d5465`. The commit object itself is also preserved locally in `.git` under `refs/archive/semester-1-bce1829`.
  - `Local Semester Archive/Recovered Unpushed Files/` — Backup copies of the four untracked course PDFs (`ENGR213, Lecture 13, October 28 2026.pdf`, `ENGR213, Lecture 14, October 30 2026.pdf`, `MIAE 221 - 2017 Midterm Theory & Past Paper Master Explainer.pdf`, and `MIAE-221-Master-Formula-Sheet-Past-Exam-Solved-Companion-Ch-1-6.pdf`), all of which have been integrated into the active course folders.
