---
name: lesson-workflow
description: "Autonomous lesson ingestion, zero-skip pedagogical expansion, and website drill pipeline for Concordia engineering courses."
---

# Autonomous Lesson Workflow Skill

This skill governs the systematic ingestion and expansion of new Concordia University teacher materials across ENGR 213, INDU 211, MIAE 215, and MIAE 221.

## When to Activate
Activate this skill whenever the user:
- Uploads or references a new teacher lecture, slide deck, notes, or problem set.
- Requests to expand, explain, summarize, or solve course materials.

## Core Workflow

### 1. Zero-Skip Pedagogical Topic Guide Expansion
- **Foundation**: Grounded strictly in the teacher's slides and syllabus.
- **Pedagogy**: Begin with intuitive real-world physical analogies before introducing equations.
- **Zero Skipped Steps**: Print every algebraic manipulation line-by-line; never omit intermediate arithmetic ($11 + 7 = 18$); show explicit substitutions with units.
- **Unified 5-Section Structure**:
  1. Explanation of the topic (Beginner-friendly intuition & slide figures)
  2. Formula to retain (Every symbol and unit explained)
  3. Example of the topic (Worked example with baby steps & zero skipped algebra)
  4. Practice Questions (Check-your-understanding & practice sets)
  5. Past Midterms (Separate section for real past exam problems)
- **Placement & Studocu**:
  - Save in `<Course>/02 - Comprehensive Topic Guides (Expanded & Intuitive)/`.
  - Copy to `Semester 1/Studocu/Need to Upload/`.
  - Log metadata in `Studocu_Need_To_Upload.md`.

### 2. Website Integration
- Register the document in `website/src/data/filteredDocumentsData.ts` or curriculum spec.
- Generate practice questions in `website/src/data/extra/<course>_lecture<N>.ts` with step-by-step KaTeX solutions and distractor explanations.
- Run targeted curriculum validation: `npm run validate:curriculum -- --update-lock`.

### 3. Rate-Limit & Safety Rules
- **NEVER scan `001 Main/`**.
- **NEVER spawn parallel subagent swarms** (execute directly and sequentially).
- **Mandatory Automatic Push**: Proactively stage, commit, and push directly to `origin main` (`https://github.com/ys-sites/concordia.git`).
