# Reusable AI Tutor Production Prompt (Lessons, 3D Visuals, Videos & Study Guides)

For website-facing work, also apply the relevant guidance in [WEB_ESSENTIALS_GUIDE.md](./WEB_ESSENTIALS_GUIDE.md).

Copy and paste the prompt below into an agent session to produce any remaining subject, subtopic, worked example, interactive lesson, AI video, or study PDF from the **Prioritized Regeneration Queue** in `COVERAGE_AUDIT_AND_REGENERATION_QUEUE.md`.

---

```text
You are working in the `concordia` repository to produce a complete, verified AI-Guided Visual Learning module for a target course and subject (`ENGR 213`, `INDU 211`, `MIAE 215`, or `MIAE 221`).

Before writing any code or content:
1. Read `COVERAGE_AUDIT_AND_REGENERATION_QUEUE.md` to identify the next target lesson(s) in the regeneration queue.
2. Read the reference pilot implementation at `website/src/learn/pilot/miae221UnitCellsPilot.ts` and inspect how it renders in `website/src/learn/player/StepViews.tsx`.
3. Inspect the private source materials on disk for the target subject (teacher lecture notes, slides, and textbook chapters in `<Course Folder>/00 - ...` and `<Course Folder>/01 - ...`) ONLY to verify curriculum scope, definitions, notation, and physical constants.

================================================================================
1. STRICT PRIVACY, SOURCE PROTECTION & STUDENT-FACING CONTENT RULES
================================================================================
- NEVER expose, link, embed, or cite original teacher lecture notes, slide numbers, instructor names, or textbook pages in any student-facing lesson, UI component, video narration, on-screen caption, or PDF.
- NEVER delete private source files from disk; they remain protected via `website/src/data/localOnly.ts` and `website/build/publishedFiles.ts`.
- NEVER embed or link outside YouTube videos or external creator channels. All student-facing videos must be original AI-generated `MotionLesson` animations and MP4 walkthroughs.
- NEVER include personal names or machine-specific local computer paths in any code, Markdown, or PDF file. Use generic academic headers (`Concordia University · Gina Cody School of Engineering`) and relative repository paths only.

================================================================================
2. REQUIRED 8-PART LESSON & SUBJECT STRUCTURE
================================================================================
Every subject module you produce must implement or verify all 8 parts of the AI Tutor learning sequence:

1. Beginner-Friendly Explanation with Intuition & Physical Meaning (`${lessonId}.explanation`):
   - Open with a warm, one-on-one tutoring analogy and physical mechanism before introducing formal notation.
   - Break the concept into 3–4 logical `PilotSectionBlock` subsections, each with an `intuition` callout, clear explanatory paragraphs, and a highlighted `keyEquationTex`.

2. Important Definitions, Formulas, Symbols, Units & When-to-Use Criteria (`${lessonId}.formulas` & `website/src/data/gates/<course>.ts`):
   - Define every symbol, variable, and physical SI unit explicitly in `vars: [[symbol, meaning, unit], ...]`.
   - Provide concrete `when` bullets ("Use this formula when...") and step-by-step `steps` ("The recipe").

3. Worked Examples with Zero Skipped Algebraic or Arithmetic Steps (`${lessonId}.worked`):
   - Include at least 2 complete worked examples per subject.
   - Show EVERY intermediate algebraic rearrangement, unit conversion (e.g., `1 nm = 10^-7 cm`, so `1 nm^3 = 10^-21 cm^3`), and arithmetic substitution before stating the final numerical answer.
   - End each worked example with a physical sanity / dimensional verification check.

4. Interactive 3D Exploration & Concept Checks (`${lessonId}.tool-*`):
   - Connect the lesson to its corresponding 3D Visual Learner (`3d:<slug>` in `website/src/learn/visual3d/Visual3DLearner.tsx` or `website/src/learn/crystal/`) and/or interactive Formula Lab (`formula:<id>`).
   - Ensure the 3D model, equation, and numerical readout share the exact same underlying mathematical constants and geometry.
   - Do NOT clutter the 3D viewport with static formula boxes; keep category and topic switcher tabs directly above the 3D stage.

5. Practice Questions with Diagnostic Feedback (`${lessonId}.practice`):
   - Verify that every practice question in `website/src/data/gates/<course>.ts` and the course practice bank includes step-by-step `moves` and diagnostic `whyWrong` explanations for each distractor option.

6. Separate Past-Midterm Practice Section (`${lessonId}.exam`):
   - Keep real past-midterm and final-exam questions in their dedicated `exam` step (`Past Midterms`) and in the `Midterm practice by subject` (`teacher-practice`) section.

7. Exam Pitfalls & Concise Revision Summary (`${lessonId}.pitfalls`):
   - Provide 3–5 concrete exam pitfalls (`mistake`, `whyItHappens`, `howToAvoid`) based on real student errors on past Concordia exams, followed by a rapid formula & comparison summary.

8. Synchronized AI-Generated Video (`MotionLesson` & MP4 Pipeline):
   - Produce a scene-by-scene `MotionLesson` specification (`chapters`, `scenes`, narration script, on-screen LaTeX equations, and 3D/SVG visual choreography).
   - For quiz, practice, and exam answer explanations, begin the first visual and spoken sentence with the solution or decisive concept. Do not reread the question or show a question-only intro; show the necessary givens as the complete step-by-step solution unfolds. General topic lessons may still begin with the big idea.
   - Keep visuals alive throughout (camera orbit/dolly, highlighting active components, drawing vectors/planes, live parameter readouts) while keeping equations crisp and readable.
   - Remember that an interactive web lesson and a rendered MP4 are separate delivery formats: interactive controls belong in the web lesson (`Visual3DLearner`, `FormulaTool`, `QuizStep`), while the MP4 delivers a smooth, self-contained visual & narrated walkthrough.

================================================================================
3. FILE LOCATIONS & REGISTRY INTEGRATION
================================================================================
- Pilot / Deep-Dive Lesson Content: `website/src/learn/pilot/<course><Topic>Pilot.ts` (wired into `website/src/learn/player/StepViews.tsx`).
- Gate Formulas, Worked Examples & Past-Exam Questions: `website/src/data/gates/<course>.ts`.
- Curriculum Specification: `website/src/learn/curriculum/<course>.ts`.
- 3D Visual Learners: `website/src/learn/visual3d/Visual3DLearner.tsx` and `website/src/learn/visual3d/scenes/`.
- AI Video Lessons: `website/src/data/gates/<course>TopicVideos.ts` and `website/src/learn/videoSources.ts`.
- Expanded Study Guides & Rapid Review PDFs (when generating PDFs):
  - Comprehensive Topic Guides: `<Course Folder>/02 - Comprehensive Topic Guides (Expanded & Intuitive)/`
  - 1-Page Rapid Review Sheets: `<Course Folder>/03 - 1-Page Rapid Review Sheets/`
  - Worked Problem Guides: `<Course Folder>/04 - Worked Problems.../` or `04 - Practice Problems.../`

================================================================================
4. MANDATORY QUALITY ASSURANCE & VALIDATION CHECKLIST
================================================================================
Before concluding your task, run and verify all of the following:
1. Mathematical & Scientific Accuracy:
   - Re-calculate every worked example and quiz answer from first principles. Verify units, significant figures, signs, and boundary conditions.
2. Accessibility & UI Polish:
   - Ensure all interactive buttons, tabs, and 3D controls have clear labels, keyboard accessibility, high-contrast light-studio styling, and `ReadAloudButton` support.
3. Curriculum & Lock Validation:
   - Run: `npm --prefix concordia/website run validate:curriculum -- --update-lock`
   - Must exit with `0 problem(s)` and `every question, video and document has a home`.
4. Production Build & Asset Privacy Audit:
   - Run: `npx --prefix concordia/website vite build`
   - Verify that `concordia/website/dist/courses/` contains ZERO teacher lecture notes, slides, or textbook PDFs.
5. Coverage Audit Update:
   - Mark the completed item as done in `concordia/COVERAGE_AUDIT_AND_REGENERATION_QUEUE.md`.
```

