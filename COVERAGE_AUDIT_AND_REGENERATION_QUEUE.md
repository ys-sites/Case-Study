# Concordia Engineering Portal — Coverage Audit, Source Privacy Inventory & Regeneration Queue

## 1. Executive Summary & System Architecture

The Concordia Engineering Portal has been upgraded to an **AI-Guided One-on-One Visual Learning System** across all four courses (**ENGR 213**, **INDU 211**, **MIAE 215**, and **MIAE 221**).

### Global Validated Curriculum Metrics

| Course | Sections | Lessons | Learning Steps | AI-Generated Videos | Interactive 3D Models | Practice & Past-Exam Questions | Published Original Study Guides | Outside YouTube Links Exposed | Teacher Slides / Textbooks Exposed |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ENGR 213** (*Applied Ordinary Differential Equations*) | 9 | 36 | 120 | 101 (230 min) | 5 (#34–#38) | 856 | 26 | **0** | **0** |
| **INDU 211** (*Introduction to Production & Manufacturing Systems*) | 11 | 25 | 102 | 25 (131 min) | 10 (#24–#33) | 294 | 19 | **0** | **0** |
| **MIAE 215** (*Programming for Mechanical & Industrial Engineers*) | 11 | 42 | 139 | 39 (107 min) | 3 (#39–#41) + C++ Labs | 301 | 23 | **0** | **0** |
| **MIAE 221** (*Materials Science*) | 13 | 43 | 199 | 272 (799 min) | 23 (#1–#23) | 547 | 31 | **0** | **0** |
| **Total Across Portal** | **44** | **146** | **560** | **437 (1,267 min)** | **41** | **1,998** | **99** | **0** | **0** |

---

## 2. Student-Facing Content Policy & Private Source Inventory

### 2.1 Multi-Layer Enforcement of Source Privacy
Original instructor lecture notes, slide decks, textbook chapters, textbook solutions, and third-party YouTube creator notes are **retained privately on disk** as reference material for scope and accuracy verification, while being **completely blocked from student-facing web access and static builds**:

1. **Build & Asset-Copying Gate (`website/src/data/localOnly.ts` & `website/build/publishedFiles.ts`)**:
   - `isHiddenFromSite()` blocks all files matching private source patterns from both `virtual:course-documents` and the Vite static asset copy step (`dist/courses/`).
   - Direct URL requests to any private PDF return HTTP 404 in production and dev server middleware.
2. **Curriculum Builder Gate (`website/src/learn/build/buildCurriculum.ts`)**:
   - `lectureDoc()` returns `null` so instructor slide references (`LectureRef`) are never attached to student lesson steps.
   - `handSteps()` omits reading steps whose underlying document is a private source handout.
   - All `s.youtubeId` and `s.kind === 'extra'` steps are stripped at build time.
3. **Vault & Question UI Gate (`filteredDocumentsData.ts`, `VideoLibrary.tsx`, `theoryVideoLookup.ts`, `MIAE221FormulaHub.tsx`, `QuestionView.tsx`, `Explanation.tsx`, `StepViews.tsx`)**:
   - `FILTERED_COURSES_DATA` filters all entries through `!isHiddenFromSite(d.relativePath)`.
   - `VideoLibrary.tsx` exposes only the **AI video course** (`ai`) and **Solved questions** (`solutions`) tracks; the external YouTube track and `YouTubePlayer` have been removed.
   - `theoryVideoLookup.ts` resolves exclusively to AI-generated `MotionLesson` videos (`MIAE221_MIDTERM_VIDEOS`, `MIAE221_SOLVE_VIDEOS`, `MIAE221_TOPIC_VIDEOS`).

### 2.2 Private Source Material Retained on Disk (Never Published)

| Course | Private Source Directories Retained on Disk | Purpose |
| :--- | :--- | :--- |
| **ENGR 213** | `Engr 213/00 - Course Syllabus & Textbook/`, `Engr 213/01 - Teacher Lecture Notes/`, `Engr 213/01 - In-Class Lecture Notes/`, `Engr 213/05 - Textbook Solutions - Assigned Problems/`, `Engr 213/06 - Quiz & Midterm Exam Prep/`, `Engr 213/Professor Leonard/`, `Engr 213/YouTube Tutorial Solutions/` | Scope verification, theorem statements, and past-exam problem verification. |
| **INDU 211** | `Indu 211/00 - Course Syllabus & Outline/`, `Indu 211/01 - Teacher Lecture Notes/`, `Indu 211/05 - Assignments & Solutions/` | Operations management scope, quantitative models, and assignment verification. |
| **MIAE 215** | `Miae 215/00 - Course Overview & Syllabus/`, `Miae 215/01 - Teacher Lecture Notes & Slides/`, `Miae 215/02 - Textbook Expanded Notes/`, `Miae 215/06 - Arduino Labs & Term Project/` | C++ language scope, pointer/memory semantics, and hardware pinout verification. |
| **MIAE 221** | `Miae 221/00 - Textbook Chapters (Callister)/`, `Miae 221/01 - Teacher Lecture Notes (Dr. Medraj)/`, `Miae 221/02 - Callister Textbook Expanded Notes/`, `Miae 221/Professor Dave/` | Crystallography, phase diagrams, mechanical properties, and materials data verification. |

### 2.3 Published Student-Facing Original Guides (99 PDFs)
Only original, expanded student study guides, rapid review sheets, and step-by-step solved problem manuals are published:
- **ENGR 213 (26 PDFs)**: `00 - Calculus Review for ODEs/`, `02 - Comprehensive Topic Guides (Expanded & Intuitive)/`, `02 - Lecture Notes Explained/`, `03 - Chapter 1 Summary/`, `04 - Chapter 2 Summary/`, `04 - Tutorials/ENGR 213 - ODE Step-by-Step Tutorial Practice`.
- **INDU 211 (19 PDFs)**: `00 - Course Overview & Study Guide/`, `02 - Comprehensive Topic Guides (Expanded & Intuitive)/Part 1–Part 9`, `03 - 1-Page Rapid Review Sheets/Part 1–Part 3`, `04 - Worked Problems & Quantitative Analysis/`.
- **MIAE 215 (23 PDFs)**: `02 - Comprehensive Topic Guides (Expanded & Intuitive)/Part 1–Part 6`, `03 - 1-Page Rapid Review Sheets/`, `04 - Practice Problems & Code Solutions/MIAE 215 - Step-by-Step Code Execution & Trace Manual`, `Mini Course/Lesson 1–Lesson 6`.
- **MIAE 221 (31 PDFs)**: `00 - Course Overview & Study Guide/`, `02 - Comprehensive Topic Guides (Expanded & Intuitive)/Part 1–Part 9 & Lectures 11–12`, `03 - 1-Page Rapid Review Sheets/Part 1–Part 9`, `04 - Practice Problems & Step-by-Step Solutions/`, `formula/` master sheets.

---

## 3. Unified 8-Part Course & Lesson Structure

Every core subject lesson across all four courses follows the unified AI Tutor learning sequence:
1. **Explanation of the topic** (`${lessonId}.explanation`): Beginner-friendly physical intuition, real-world mechanism, and AI-generated narrated video lesson.
2. **Formulas to retain** (`${lessonId}.formulas`): Core definitions, equations, symbol-by-symbol breakdown, physical units, and when-to-use criteria.
3. **Examples of the topic** (`${lessonId}.worked`): Zero-skip worked examples showing every intermediate algebraic and arithmetic step.
4. **Interactive Exploration & 3D Visual Learner** (`${lessonId}.tool-*`): Synchronized 3D Visual Learner (`3d:*` / `crystal-lab:*`), interactive Formula Lab (`formula:*`), C++ Code Lab (`cpp-lab`), or TSP Simulator (`tsp`).
5. **Practice Questions** (`${lessonId}.practice`): Concept checks, practice bank questions, and method drills with diagnostic feedback for incorrect answers and AI solve videos.
6. **Past Midterms** (`${lessonId}.exam`): Dedicated section for real past midterm and final exam questions on that subject.
7. **Exam pitfalls & revision summary** (`${lessonId}.pitfalls`): High-frequency exam traps, common student mistakes, and a concise formula revision checklist.
8. **AI-generated video** (`VideoStep` / `MotionLessonPlayer`): Synchronized multi-scene animated walkthrough with narrated explanations and interactive playback controls.

---

## 4. Complete Pilot Lesson Reference (`MIAE 221 · unit-cells`)

The complete, verified reference implementation is located at:
- **Pilot Data & Choreography Module**: `website/src/learn/pilot/miae221UnitCellsPilot.ts`
- **Rendered Student View**: `website/src/learn/player/StepViews.tsx` (`LessonReferences`, `NotesStep`, `WorkedStep`, `ToolStep`)
- **Synchronized 3D Models**: `website/src/learn/crystal/CrystalLab.tsx`, `website/src/learn/visual3d/Visual3DLearner.tsx` (`#1 Crystal Structures`, `#2 Atom Sharing`, `#3 Atomic Packing Factor`, `#4 Coordination Number`, `#5 Lattice Parameter & Atomic Radius`)

---

## 5. Coverage Gaps & Prioritized Regeneration Queue

While every lesson in all four courses has complete step coverage, practice questions, formulas, and a mapped AI video, several lessons currently share a foundational topic AI video fallback (`LESSON_VIDEO_MAP` in `StepViews.tsx`) or await pilot-depth narrative expansion (`PilotSectionBlock` + zero-skip derivation blocks).

### Priority Tier 1 — Dedicated Topic AI Video & Deep-Dive Text Expansion (High-Yield Midterm Subjects)

| Priority | Course | Lesson ID | Subject Title | Current Status | Target Deliverable |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **P1.1** | **MIAE 221** | `directions`, `planes`, `linear-planar-density`, `xrd` | Crystallographic Directions `[uvw]`, Miller Planes `(hkl)`, Densities & Bragg's Law | Has dedicated AI topic videos (`topic221:*`) + 3D models `#7–#11`; needs pilot-depth text blocks in `src/learn/pilot/`. | Add `miae221CrystallographyPilot.ts` with zero-skip `[uvw]` and `(hkl)` reciprocals/clearing-fractions derivations. |
| **P1.2** | **MIAE 221** | `point-defects`, `solid-solutions`, `dislocations-grains`, `diffusion-mechanisms`, `fick-first`, `fick-second` | Imperfections in Solids, Hume-Rothery Rules, Dislocations & Fick's Laws of Diffusion | Has dedicated AI topic videos + 3D models `#12–#15, #22`; needs pilot-depth text expansion. | Add `miae221DefectsDiffusionPilot.ts` with Arrhenius vacancy and erfc diffusion worked examples. |
| **P1.3** | **ENGR 213** | `classify`, `solutions-ivps`, `direction-fields`, `cooling`, `mixtures-circuits`, `logistic` | First-Order ODE Classification, Direction Fields, Cooling, Mixing Tanks & Logistic Models | Uses shared `tutor:*` AI video fallback; has 3D models `#34, #35, #37`. | Produce dedicated `MotionLesson` videos for `classify`, `direction-fields`, `cooling`, `mixtures-circuits`, and `logistic`. |
| **P1.4** | **ENGR 213** | `complex-arithmetic`, `roots-de-moivre`, `higher-order-theory`, `undetermined-coefficients`, `variation-of-parameters`, `mass-spring` | Complex Roots, Wronskian, Undetermined Coefficients, Variation of Parameters & Mass-Spring | Uses shared `tutor:second_order` fallback; has 3D models `#36, #38`. | Produce dedicated `MotionLesson` videos for each higher-order ODE method and mass-spring resonance. |

### Priority Tier 2 — INDU 211 & MIAE 215 Dedicated Concept Videos & Rapid Review PDFs

| Priority | Course | Lesson ID | Subject Title | Current Status | Target Deliverable |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **P2.1** | **INDU 211** | `engineering-profession`, `industrial-systems`, `manufacturing-processes`, `layout`, `material-handling` | Qualitative Foundations, Manufacturing Processes, Facility Layouts & Material Handling | Uses shared `visual211:*` fallback; has 3D models `#24–#33`. | Create dedicated narrated `MotionLesson` videos choreographed with the 10 Industrial Engineering 3D scenes (`InduScenes.tsx`). |
| **P2.2** | **INDU 211** | `Part 4` – `Part 9` Rapid Review Sheets | Material Handling, Operations Planning, LP/Queuing, SPC, Work Design & CPM/PERT | Comprehensive Guides (`Part 4–Part 9`) exist; 1-Page Rapid Review Sheets currently cover `Part 1–Part 3`. | Generate 1-Page Rapid Review PDFs for `Part 4` through `Part 9` (when PDF generation is scheduled). |
| **P2.3** | **MIAE 215** | `pointers-memory`, `functions-scope`, `strings`, `structs-classes`, `file-io`, `arduino-intro` | Pointers & Memory Architecture, Pass-by-Reference, Structs/Classes, File I/O & Arduino Hardware | Post-midterm lessons have practice banks and 3D models (`#39–#41`); need dedicated `MotionLesson` walkthroughs. | Produce dedicated C++ memory-trace and Arduino hardware `MotionLesson` videos (`miae215PostMidtermVideos.ts`). |
| **P2.4** | **MIAE 221** | `phase-diagrams`, `iron-carbon`, `ceramics`, `polymers`, `functional-properties` | Binary Phase Diagrams, Lever Rule, Fe–Fe₃C System, Ceramics, Polymers & Functional Properties | Post-midterm lessons (`Ch 9–21`); `Part 8` guide exists, needs dedicated phase-diagram AI videos and interactive lever-rule lab. | Produce `MotionLesson` videos for Lever Rule & Fe–Fe₃C microstructure evolution plus `Part 10–12` study guides. |

