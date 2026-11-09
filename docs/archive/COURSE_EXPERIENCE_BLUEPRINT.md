# Engineering learning experience: implementation blueprint

Status: planning and source review, 1 November 2026. This is not a claim of legal compliance or a completed design rebuild. Get Québec/Canadian legal advice for decisions about rights, privacy, branding and applicable accessibility or language obligations.

## Implementation progress

The player chapter drawer now moves keyboard focus inside when opened, supports Escape and restores focus when closed. Opening a reading or interactive step no longer immediately marks it complete; advancing or explicitly marking it complete retains the existing completion model and progress IDs. Existing completion records were not reinterpreted. The optional YouTube player has an external viewing link, and header privacy settings describe known data flows. The separate Quick Jump overlay and its keyboard shortcut have been removed at the owner's request.

These are initial P1–P3 changes, not completion of the full blueprint. The complete rights/provenance audit, policy review, all-course behavioural testing, screen-reader and real-device checks, network/privacy audit, video availability and performance benchmarking remain open. The privacy-settings summary is not a complete or legally reviewed privacy policy. Do not claim permission, copyright clearance or legal compliance on the basis of this document.

Verification: curriculum, question and integrity validators and TypeScript passed. The production build passed with large-chunk and oversized-media warnings. A headless local Chrome check of one INDU 211 lesson found no page-wide horizontal overflow at 320, 375, 390, 768 and 1440 pixels; tested drawer focus, Escape, focus return and resize to desktop, plus explicit completion after reload. A multi-width browser run initially timed out; fresh individual sessions passed. This is not a substitute for real-device or screen-reader testing.

Further work: optional analytics and visitor counting default off and can be enabled or revoked in header privacy settings; the public badge reads aggregate counts without counting that browser. Counts include earlier visits and new opted-in browsers only. Both chapter drawers support keyboard focus and Escape. YouTube preview thumbnails no longer load from Google before interaction, and the course player uses a privacy-enhanced host and an error/fallback message. Local headless checks verified the four course-player drawers at 390 px, one course-overview drawer, analytics opt-in/revocation, and one INDU YouTube preview before play. Public oEmbed requests returned successful responses for 15 INDU video IDs; this does not establish embedding, captions or rights. The generated coverage report flags all 93 teaching lessons under its stock thresholds; these are review flags, not proof of missing or incorrect content, and the inventory's separate-check threshold may not match the current merged-practice structure.

See `LEGAL_AND_PRIVACY_REVIEW.md` for the current Québec/Canada evidence and unresolved decisions. The full rights/provenance audit and legal policy review cannot be declared complete from file names, public documentation, or code inspection. Real-device/screen-reader testing, verified rights for every public asset and CDN object, content correctness review, privacy-officer/provider details, a reviewed full privacy policy, and legal advice on branding and French-language obligations remain necessary.

## Goal and boundaries

Create an original, clear, account-free engineering learning experience for MIAE 221, MIAE 215, ENGR 213 and INDU 211. Organize the curriculum around instructor-defined course topics, not a marketplace or a creator platform. No signup, paywall, instructor course creation, cloud progress or public sharing of teacher/textbook files at this stage. Preserve existing INDU 211 optional YouTube topic explanations. Keep local student progress, quiz attempts and stable identifiers.

Use Udemy as an interaction reference, not as a source of copied interface assets, branding, wording, course content or implementation. Make design decisions using `MAIN_BRAIN_PIPELINE.md`, `WEB_ESSENTIALS_GUIDE.md`, `TUTOR_SOUL.md`, `VISUAL_LEARNING_PRODUCTION.md` and the relevant `001 Main` resources. No instructions here grant access to protected course materials or permission to send content externally.

## Evidence and limits

- A public [mechanical engineering course listing](https://www.udemy.com/course/mechanical-engineering-crash-course/) shows learning outcomes followed by a count of sections, lectures and duration, an expand-all control, and sections with nested lecture names, durations and preview labels. A second [engineering course listing](https://www.udemy.com/course/engineering-statics-q/) corroborates the section/lecture hierarchy. Listings were observed as public pages, not purchased or signed-in lessons.
- Udemy's [course player guidance](https://support.udemy.com/hc/en-us/sections/206457187-Course-player) describes curriculum navigation, returning to the last lecture, completion, optional autoplay, speed and full screen. Its [mobile guidance](https://support.udemy.com/hc/en-us/sections/4411124140951-Mobile-Course-Player) describes accessing course content below the video on mobile. These are documentation claims, not a live authenticated-player test.
- Main Brain's Graphify query was used to locate `website/src/learn/pages/Player.tsx`, `CoursePage.tsx`, `progress/store.ts` and `model.ts`; relevant source was inspected directly. Graphify is navigation evidence, not proof of runtime behaviour. The REA skill and Teardown observer guidance were reviewed, but neither REA nor Teardown MCP tools were connected in this session. REA's diagnostic reported Codex registration drift; no configuration was changed. No REA runtime capture, clean-room verification, browser-based Udemy interaction, authenticated player, mobile viewport or production accessibility audit was completed. Browser automation host was unavailable. The proposed work below must be verified on real devices and against the actual current checkout.

## What already exists

| Area | Current code evidence | Assessment |
| --- | --- | --- |
| Course map | `website/src/learn/curriculum/` and `build/buildCurriculum.ts` define four courses, sections, lessons and steps. | Reuse and improve content coverage; do not replace the content model wholesale. |
| Course overview | `pages/CoursePage.tsx` renders expandable sections, counts and estimates. | Validate actual content order and clarity on mobile and desktop. |
| Player navigation | `pages/Player.tsx` selects the current step, provides previous/next, a chapter drawer, quiz support and an up-next action. | Consolidate and test the experience, especially mobile and focus management. |
| Progress | `progress/store.ts` stores `concordia.progress.v1`, handles pending writes and merges across tabs. | Preserve the existing store, aliases and IDs. It is browser-specific and may be lost if storage is cleared. |
| Completion | `Player.tsx` auto-marks certain non-video steps on opening; video and quiz completion have separate triggers. | An opened page is not proof of learning. Design truthful completion labels and migration before changing semantics. |
| Video | `player/StepViews.tsx` and `components/YouTubePlayer.tsx` support project videos and outside videos. | Keep INDU videos; verify captions, error handling, privacy and keyboard controls for each player. |
| Privacy | `learn/analytics.ts` stores study events locally, while `App.tsx` loads Vercel Analytics and Speed Insights; `utils/visitorStats.ts` sends a pseudonymous device ID to `/api/visitors`; `ContactModal.tsx` sends submitted contact details to FormSubmit. | Audit the full actual data flow and vendor settings. Do not claim the whole site is local-only. |
| Identity | The site uses the university name in its title; the owner requested removal of the footer affiliation statement. | Review the name, logo, domain and affiliation language with counsel and the university. |

## Proposed student journey

1. **Find a course:** show the four curated courses with recognizable names, meaningful study status and a clear continue action. Avoid course-marketplace purchasing, instructor and ratings UI.
2. **Orient:** course overview presents a short purpose, learning outcomes, progress explained in words and the chapter sequence. Offer a visible way to expand chapters and jump to any available topic.
3. **Choose a topic:** use a compact tree: course → chapter → topic → learning steps. For each topic show progress and accurate durations only when available; distinguish optional outside videos and keep exam preparation identifiable as a separate path.
4. **Learn:** begin with a plain-language concept and why it matters; follow with definitions/symbols, a worked example and a relevant interactive visual when appropriate. Offer checks and practice with full worked feedback; show real past papers only when source and rights are verified. Do not falsely present AI-generated practice as a past paper.
5. **Continue or revisit:** a persistent, non-blocking previous/next control and chapter navigation remain available. The learner can jump or return without being forced to complete every step. A video ending may suggest the next step; autoplay should be an explicit preference, not a surprise.
6. **Resume:** restore the last valid lesson and video position from the existing local store. Explain that progress is specific to the browser/device and provide an accessible recovery plan for blocked storage. Do not add accounts or server synchronization.

## Original interface direction

- Keep the site's own visual identity and existing course colors; use an off-white reading surface, high-contrast ink and restrained course accents. Avoid reproducing Udemy's logo, proprietary visuals or a pixel-identical interface.
- Desktop: readable lesson stage with a collapsible curriculum rail and a clear current-step indicator. Explain the current chapter/topic context without repeating large headers. Keep interactive visuals and graphs close and connected to their actual state.
- Mobile: place a prominent **Chapters** button at the top of the player that opens a keyboard-accessible drawer, with the current topic visible. A content panel may also appear below the lesson. Avoid placing the only chapter entry point below a long video; preserve scroll position and restore focus after close.
- Make controls touch-friendly, legible at zoom, keyboard-operable with a visible focus indicator, and provide reduced-motion and pause controls. Test contrast and meaningful text alternatives. Use [WCAG 2.2](https://www.w3.org/TR/WCAG22/) as a design and test target; legal applicability depends on the operator and jurisdiction.
- Keep explanation-first design: short visible guidance and expandable advanced detail; never substitute decoration for an explanation of what changes and why.

## Implementation phases and acceptance tests

### P0: rights, privacy and truthfulness audit

1. Inventory every publicly served PDF, video, question, diagram, font, 3D asset, soundtrack and logo. Record origin, owner, permission/license, allowed scope, attribution and expiry. Check built assets and CDN copies, not just navigation links. Quarantine questionable material before further reuse. Preserve private sources locally and do not commit them.
2. Independently review use of university name, insignia and domain with the university and counsel. The [University Secretariat](https://www.concordia.ca/about/administration-governance/secretariat.html) says permission must be obtained for use of its name and logo. The existing independent-site statement is useful but not a substitute for permission.
3. Map actual data flows: browser progress/metrics; `/api/visitors` and its backing service; Vercel hosting, analytics and speed insights; embedded YouTube and thumbnails; FormSubmit; and media/CDN services. Confirm deployments and retention from provider settings, not just code. Reconcile privacy text with verified behaviour, designate a rights/privacy contact, and create a functional rights-complaint process.
4. Verify any labeled past-exam content and permission. Original explanations can use subject facts but should not reproduce protected wording, diagrams, distinctive organization or solutions without a lawful basis. Keep a private provenance record even when the public lesson need not mention a teacher document.

Acceptance: trace each public artifact to a recorded rights decision; review current third-party hosts in browser network tools; a reviewer can identify what data leaves the browser and why; unresolved permissions are recorded and addressed, not described as cleared.

### P1: course sequence and progress

Change `website/src/learn/curriculum/`, `build/buildCurriculum.ts`, `pages/CoursePage.tsx`, `pages/Player.tsx` and `progress/` only as necessary. Audit course → section → lesson → step order across all four courses, ensuring topics and steps are actually backed by content. Define optional-video and exam-prep behaviour explicitly. Keep `concordia.progress.v1`, existing step IDs, alias handling and concurrent-tab persistence; design and test any migration before altering the completion calculation. Add learner-readable definitions of progress and completion.

Acceptance: new and returning students can open any chapter, go forward/back, resume the last valid step, and preserve existing seeded progress across a reload and two tabs. Missing optional media does not block a lesson; an unknown step falls back predictably. Completion does not silently imply mastery. Validate with `npm run validate:curriculum`, `npm run validate:questions`, `npm run validate:integrity`, and TypeScript checks; test all four courses.

### P2: player UI, mobile and accessibility

Use the existing player and styles rather than adding a second navigation engine. Improve hierarchy, spacing, selected state and explanatory copy. On mobile, expose chapter access near the top and use a drawer that traps or appropriately manages focus, supports Escape, restores focus to its trigger, and does not create a second inaccessible copy. Preserve drag/orbit and play/pause for 3D learners. Preserve quiz skip/revisit and do not introduce a login requirement.

Acceptance: test representative 320, 375, 390 and 768 px widths and desktop, 200% zoom, landscape, keyboard-only operation, screen reader names, touch, reduced motion, and open/close navigation. No clipped controls or unintended page-wide horizontal overflow; play, pause, chapter selection and quiz navigation work without a mouse. Document actual browser and device results.

### P3: media reliability, privacy and performance

Keep the restored INDU 211 YouTube lessons. Check video availability and use supported embed controls and terms; provide a working external fallback if the owner disables embedding. Evaluate click-to-load and [YouTube privacy-enhanced mode](https://support.google.com/youtube/answer/171780) without promising zero third-party data collection. Audit image and script requests before player activation. Add useful captions/transcripts when rights permit. Lazy-load media and 3D only when useful, test loading and error states on a slow network, and measure actual mobile performance against a documented baseline.

Acceptance: blocked/unavailable embed, captions, full-screen, playback speed, keyboard interaction, slow network, and reset/resume behaviour are verified. Network traces match the privacy notice and consent decisions. Record performance measurements instead of claiming a target was met without testing.

### P4: optional, after user requests it

Before adding accounts, payments, sync, messaging or educator tools, produce a separate requirements and threat model. These are outside the current product scope. For any future payment feature, review processor contracts and consumer protection requirements; for promotional email or messages review [CASL](https://ised-isde.canada.ca/site/canada-anti-spam-legislation/en/getting-consent-send-email). Do not infer consent to send messages from this blueprint.

## Legal and policy questions for counsel

- **Copyright:** facts and methods differ from protected expression. Educational purpose does not automatically make all copying lawful. The [Canadian Intellectual Property Office](https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en/copyright-infringement) describes fair dealing as a context-dependent exception. Determine ownership and permissions for original notes, past papers, figures, slides, video, music and AI-assisted outputs; do not assume attribution alone grants a license.
- **Personal information and privacy:** assess whether Québec's private-sector law, PIPEDA or other rules apply based on actual activities and information flows. Free access alone does not necessarily rule out commercial activity ([OPC guidance](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/pipeda-compliance-help/pipeda-interpretation-bulletins/interpretations_03_ca/)). Québec's [privacy regulator](https://www.cai.gouv.qc.ca/protection-renseignements-personnels/information-entreprises-privees/collecte-renseignements-personnels_entreprises) describes website privacy notices and information about cookies where personal information is collected. Review collection, purposes, retention, processors, cross-border transfers, safeguards, access requests and breach response with counsel.
- **Branding and language:** review the actual name, domain, logos and claimed affiliation under the university's published policies. For commercial publications, Québec's language rules may be relevant; confirm applicability and appropriate French content with counsel ([Québec government background](https://cdn-contenu.quebec.ca/cdn-contenu/adm/min/langue-francaise/pol-plan-langue-francaise/tendances-langue-activites-internet.pdf)).
- **Website documents:** prepare truthful privacy information, terms of use, independent/non-affiliation wording, copyright/rights contact, accessibility contact and correction process after the operator, services and rights position are known. Templates and disclaimers do not create permissions or guarantee compliance.

## Verification record

This blueprint is based on public pages and a targeted static review. No application code, legal policy pages, course assets or user progress were modified by producing it. Future implementation must record tested commit, routes, dates, device/browser coverage, validator output, legal decisions and remaining unknowns.
