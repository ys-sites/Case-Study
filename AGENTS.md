# Antigravity Autonomous Workflow Rules: Fast, Smart & Safe + Studocu Pipeline Law

For website work, also follow the project-specific [Website Essentials Guide](./WEB_ESSENTIALS_GUIDE.md). Apply its design, accessibility, security and validation guidance as relevant to the task.

For 3D learner work, follow [the approved 3D model style](./THREE_D_MODEL_STYLE.md). A lighting/background change alone does not satisfy a request to rebuild the models.

For task routing across Graphify, installed skills and the local resource library, follow [Main Brain Pipeline](./MAIN_BRAIN_PIPELINE.md).

## 1. MANDATORY FIRST STEP ON EVERY PROMPT
Before executing any user task or generating any educational material, the agent MUST review and adhere to this permanent pipeline rule:

### The Studocu Replication & Queueing Law:
Whenever the user provides new teacher materials (lecture notes, problem sets, course outlines, labs, slides) and asks to expand, explain, summarize, solve, or create any new documentation (e.g., Markdown topic guides, 1-page rapid review sheets, fully solved problem guides, compiled PDFs):
1. **Primary Output Placement**:
   - Save the primary Markdown and compiled PDF files in their proper course structure under:
     `concordia/<Course>/...` and `c:\Users\Sharafath\Documents\iCloudDrive\Concodia\Semester 1\<Course>\...`
     (Where `<Course>` is `Engr 213`, `Indu 211`, `Miae 215`, or `Miae 221`).

2. **Mandatory Studocu Replication**:
   - Immediately replicate a copy of the newly created final document(s) (especially the compiled PDF / standalone guide) into:
     `c:\Users\Sharafath\Documents\iCloudDrive\Concodia\Semester 1\Studocu\Need to Upload\`

3. **Mandatory Metadata Queue Logging**:
   - Immediately append a complete Studocu upload metadata entry to:
     `c:\Users\Sharafath\Documents\iCloudDrive\Concodia\Semester 1\Studocu\Need to Upload\Studocu_Need_To_Upload.md`
   - The metadata entry must include:
     - Exact Filename
     - **University**: `Concordia University`
     - **Course**: Verified course name & code (`Applied Ordinary Differential Equations (ENGR 213)`, `Introduction to Production and Manufacturing Systems (INDU 211)`, `Mechanical, Industrial & Aerospace engineering (MIAE 215)`, or `Materials Science (MIAE 221)`)
     - **Category**: Dropdown value (`Lecture notes`, `Summaries`, `Practice materials`, `Practical`, `Mandatory assignments`, `Tutorial work`, `Other`)
     - **Title**: Strict Course Code prefix (e.g., `MIAE 215 - ...` or `ENGR 213 - ...`)
     - **Academic year**: `2025/2026`
     - **Description**: 2-3 sentence high-yield summary highlighting core concepts and exam utility.

## 2. PROMOTION TO "DONE" CYCLE
When the user states that the pending documents in `Need to Upload` are finished/uploaded (e.g., *"Needs to Upload is done"*, *"I uploaded them"*, *"Mark as done"*):
1. Move the physical files from:
   `c:\Users\Sharafath\Documents\iCloudDrive\Concodia\Semester 1\Studocu\Need to Upload\`
   $\longrightarrow$ `c:\Users\Sharafath\Documents\iCloudDrive\Concodia\Semester 1\Studocu\Done\`
2. Transfer their metadata entries from:
   `c:\Users\Sharafath\Documents\iCloudDrive\Concodia\Semester 1\Studocu\Need to Upload\Studocu_Need_To_Upload.md`
   $\longrightarrow$ `c:\Users\Sharafath\Documents\iCloudDrive\Concodia\Semester 1\Studocu\Done\Studocu_Done.md`
3. Reset `Studocu_Need_To_Upload.md` to reflect `Currently Pending Uploads: 0`.

## 3. STRICT ANONYMITY & PRIVACY LAW (NO PERSONAL IDENTITY OR ABSOLUTE USER PATHS)
Under no circumstances should the student's personal name (`Sharafath`, `Mohamed Sharafath`, etc.) or personal computer paths (e.g. `C:\Users\Sharafath\...`, `file:///c:/Users/Sharafath/...`, `users.sharafat`, etc.) appear in ANY generated study guide, Markdown topic guide, review sheet, PDF, HTML, assignment, or website file.
1. **No Personal Names in Documents**: All headers, footers, cover pages, and metadata must refer to generic academic designations (e.g., `Concordia University · Gina Cody School of Engineering`, `Course Engineering Hub`, or `Student Academic Guide`).
2. **Relative File Paths Only**: Any hyperlinks or references to other course documents must use relative repository paths (e.g., `../02 - Comprehensive Topic Guides/...` or `[Document Title](./filename.pdf)`) rather than machine-specific local drive paths.
3. **No Personal Footers or Machine Citations**: Never stamp local user paths onto rendered PDFs or web documents.

## 4. UNIFIED COURSE LESSON STRUCTURE (ALL COURSES)
Across all courses (**MIAE 221**, **MIAE 215**, **ENGR 213**, **INDU 211**), maintain this exact structure:
1. **Explanation of the topic**: Beginner-friendly conceptual breakdown and physical analogies based on teacher slides (no ASCII art; extract real figures to `./images/`).
2. **Formula to retain**: Core equations with every symbol, variable, and physical unit explicitly defined.
3. **Example of the topic**: Fully worked example with baby steps and zero skipped intermediate arithmetic or algebra ($11 + 7 = 18$).
4. **Practice Questions**: Dedicated section for check-your-understanding items, practice banks, and drills.
5. **Past Midterms**: Dedicated section (separate from Practice Questions) for real past midterm/exam problems.
- Do NOT include YouTube video embeds or exam percentage weight blocks.

## 5. FAST, SMART & SAFE EXECUTION RULES (QUOTA & RATE-LIMIT PROTECTION)
1. **Targeted access to `001 Main`**:
   - Use its README and task-specific resources as directed by the Main Brain Pipeline. Avoid broad scans, indiscriminate indexing, unreviewed execution and loading unrelated materials.
2. **No Parallel Subagent Swarms**:
   - NEVER spawn multiple parallel subagents (e.g. 5+ concurrent Opus agents) for batch tasks, as this immediately drains API rate limits. Execute work directly and sequentially.
3. **Speed & Targeted Scope**:
   - Answer simple questions immediately without inspecting files or running tools.
   - Read and modify only the specific files relevant to the user's request.
   - Do not scan the entire codebase when the target file is known.
   - Do not run full `npm run build` after every small edit; use targeted validation (`npm run validate:curriculum`) when needed.

## 6. MANDATORY AUTOMATIC GIT PUSH LAW (ALWAYS PUSH)
On every prompt where changes, fixes, enhancements, or new files are created or modified:
1. **Always Push Automatically**: Proactively stage, commit with a descriptive message, and push directly to `origin` before concluding the turn.
2. **Never Wait to be Asked**: Every completed change is pushed automatically as the final step.
3. **Mandatory Remote Target**:
   - All commits and branch pushes MUST strictly target: `https://github.com/ys-sites/concordia.git`
   - Never push to alternate repositories without explicit user instruction.
