# Engineering Hub home page: implementation brief for Gemini

Redesign the home page in the existing React, Vite and TypeScript project. Use Udemy's clear learning journey as inspiration while creating an original design in this site's identity. Do not build a separate mock site.

## Preparation

Read `AGENTS.md`, `GEMINI.md`, `MAIN_BRAIN_PIPELINE.md`, `WEB_ESSENTIALS_GUIDE.md` and `COURSE_EXPERIENCE_BLUEPRINT.md`. Use a focused Graphify query when available, then inspect `website/src/learn/pages/Home.tsx`, its styles, shared shell, routes and progress store. Inspect the current rendered site and working tree before changing anything; preserve unrelated work. Consult `LEGAL_AND_PRIVACY_REVIEW.md` if available and do not claim legal clearance.

## Experience

- Create a polished, welcoming, original engineering-learning home page with off-white surfaces, readable text, restrained course accents, clear hierarchy and purposeful visuals. Use the appropriate `001 Main` design and motion resources selectively; do not copy Udemy's logo, artwork, text or pixel-level UI.
- Present a clear start or resume action and make ENGR 213, INDU 211, MIAE 215 and MIAE 221 easy to find. Show honest existing progress and actual course data. Do not invent videos, counts, ratings, deadlines or unavailable features.
- Preserve course routes, all four course curricula, local progress and `concordia.progress.v1`, quiz and resume flows, and INDU 211 optional topic YouTube videos. No login, paywall, cloud progress, course marketplace, instructor course creation or video regeneration.
- Design for narrow phones and desktop with no clipping or unintended horizontal scrolling. Check keyboard operation, clear focus, touch targets, contrast, reduced motion and accessible names. Do not restore the Quick Jump overlay.
- Keep the footer concise as requested. Preserve an accessible privacy-settings control and existing analytics consent, and show the compact activity badge using real aggregate data without adding a visit for browsers that have not opted in. Do not fabricate counts.

## Verification and delivery

Use the existing course player and components rather than rebuilding the application wholesale. Run TypeScript, the relevant course validators and a production build. Test fresh and returning states, representative mobile and desktop widths, keyboard navigation, storage-blocked behaviour, privacy settings and course links. State what was tested and any remaining warnings; do not claim legal, accessibility or security clearance without evidence.

The earlier REA diagnostic found a Codex connection problem, so the blueprint's Udemy observations are from public pages and documentation, not a completed REA capture. Do not bypass logins, access paid course content or claim otherwise. Follow the current project Git instructions, inspect the authorized remote and stage only the requested changes.
