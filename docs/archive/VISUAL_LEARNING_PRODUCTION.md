# Visual learning production plan

For all new or revised 3D learners, follow [the approved detailed model standard](./THREE_D_MODEL_STYLE.md). Rebuild the teaching objects; changing the background, colors and lighting alone is insufficient.


Use this plan for ENGR 213, INDU 211, MIAE 215 and MIAE 221. The current MIAE 221 videos establish the instructional voice: explain patiently, connect ideas to examples, and show calculations step by step. New work should make physical mechanisms, diagrams and mathematical relationships more visible and interactive.

For website-wide design, accessibility, security and verification guidance, see the [Website Essentials Guide](./WEB_ESSENTIALS_GUIDE.md).

## Approved visual direction for new videos

Use a **white or warm-white paper background** and an illustrated, hand-drawn world. The reference screenshots in `001 Main/video style/` show dimensional objects sitting on a light book-like surface: fine dark ink contours, cross-hatched shading, subtle paper texture, soft shadows, and selective saturated color that makes the changing physical quantity easy to follow. Think of a carefully drawn engineering notebook coming to life. Use the screenshots as design references, not as assets to reproduce or publish; some include browser interface content.

Make the main diagram or 3D apparatus the focal point. Use spacious composition, clear labels, polished editorial typography, legible typeset mathematics, compact controls and uncluttered information cards. Draw objects with physical depth and meaningful motion; add color to show the particular effect being taught. Show one idea at a time and reveal extra information when needed. An open-book composition is one possible treatment, not a requirement for every scene. Do not place scanned textbook pages or instructor documents in a student-facing video.

Preserve the MIAE 221 series' patient explanation and zero-skipped reasoning while improving its visual storytelling. Every moment should have purposeful visual activity where practical—drawing, an object responding, a diagram developing or a gentle camera move—while important equations and calculations remain readable. Dark chalkboard instructions in historical style files apply to their existing series; this light illustrated direction takes priority for **new** work unless a later request says otherwise. Existing videos do not change until replacements are actually produced and reviewed.

## Background music for educational videos

Use engaging, unobtrusive instrumental background music that supports clear narration, and keep the warm illustrated teaching style. The narration always comes first.

- **Rights:** use only music with a recorded right to publish it on the website, and record its source and license in the project's credits. Do not reuse music taken from another video unless its rights are confirmed. Original music synthesized in code, with no samples, is the default.
- **Character:** no vocals; soft and steady, with most energy below about 1.5 kHz so speech consonants stay clear. Change harmony or texture across a long lesson so it never sounds like a loop.
- **Levels:** master to about -16 LUFS. Keep music about 22 to 27 dB below the voice during speech. Let it rise gently during prediction pauses, the opening and the ending, using smooth fades with no sudden changes.
- **Reproducible mix:** drive music levels from the narration timeline, keep the narration in sync and unprocessed apart from static gain, and keep a music-free backup. Picture and captions must not change when music is added.
- **Verification:** check loudness, voice-to-music level, playback and sync at the beginning, middle and end, then compare speech recognition with and without music. Measurements do not replace a person listening before release.

The reference implementation is the MIAE 221 Unit Cells pilot's `tools/music.mjs`, `tools/mix.mjs` and `tools/verify-mix.mjs`.

## Video thumbnails

Every new teaching video gets its own thumbnail in the same warm-white style as the video: a large title on the notebook page, plus the subject's key formula or a 3D model of what it covers. It must stay readable at the small card size used in Today's plan, so students can recognize the topic at a glance. Use a dedicated composition, not a frame taken from the video. The reference is `posterLayout` in the replacement project's drawing kit.

## Quiz and exam answer videos: solution first

Start the first visual and spoken sentence with the relevant concept or first solution step. Do not open with a title sequence, reread the question, or devote a chapter to restating it. Show only the givens needed for the current step, then work through the reasoning and arithmetic patiently, with units, a check of the answer, and any important misconception. Keep the question accessible in the surrounding interface. This rule applies to answer explanations across courses; general concept lessons may still open with the big idea.

Existing answer videos with a clearly marked “Solve It” chapter can start at that marker in the player; students can seek backward to the original introduction. This is a playback change, not a new render. Videos without a reliable marker keep their original start until reviewed.

## Research and tool routing

Before designing a new production, review the existing REA findings in [THE_NEXT_STEP.md](./THE_NEXT_STEP.md), the local `001 Main` resource library and the relevant references below. Treat REA findings as evidence and inspiration: distinguish inspected behavior from design proposals and verify assumptions against the actual tool version. Select a small compatible set of tools for each lesson; do not rewrite the working renderer, install every tool, or promise integrations that have not been tested.

| Need | References and intended use |
|---|---|
| Math and narrated explainers | [Manim](https://github.com/ManimCommunity/manim) for mathematical scenes; [Anything2Explainer](https://github.com/Vincentwei1021/anything2explainer) for its research-to-storyboard and frame-driven production workflow; [Remotion](https://github.com/remotion-dev/remotion) for React-based video. Adapt any dark-canvas defaults to this project's white illustrated style. |
| Illustrated physical learning | [Every Joule lesson](https://github.com/iamtechartist/every-joule-lesson1) for the book-like scene, physical interaction, linked readouts and prediction/feedback pattern; the prior REA research on xImmersion, arXivisual, Papermorph and Anatomy for other useful approaches. Create original teaching assets and respect source licenses. |
| Motion | [GSAP](https://github.com/greensock/GSAP), [Motion](https://github.com/motiondivision/motion), [Anime.js](https://github.com/juliangarnier/anime), [Tween.js](https://github.com/tweenjs/tween.js), [mo.js](https://github.com/mojs/mojs), [Lottie](https://github.com/airbnb/lottie-web), [Magic UI](https://github.com/magicuidesign/magicui) and [React Bits](https://github.com/DavidHDev/react-bits) as possible motion and interface references. Use only the components and libraries that suit the scene. |
| 3D and interactive drawing | [Three.js](https://github.com/mrdoob/three.js), [Blender](https://github.com/blender/blender), [Godot](https://github.com/godotengine/godot), [PixiJS](https://github.com/pixijs/pixijs) and [Konva](https://github.com/konvajs/konva). The existing React Three Fiber and Drei resources are also relevant for web 3D. |
| Doodle and annotation | [Excalidraw](https://github.com/excalidraw/excalidraw), [Rough.js](https://github.com/rough-stuff/rough), [Rough Notation](https://github.com/rough-stuff/rough-notation) and [OpenToonz](https://github.com/opentoonz/opentoonz) for sketch-like drawings, annotations and 2D animation. |
| Production and recording | [OpenMontage](https://github.com/calesthio/OpenMontage), [FFmpeg](https://github.com/FFmpeg/FFmpeg), [Filmcraft](https://github.com/storytold/filmcraft), [Shotcut](https://github.com/mltframework/shotcut), [Kdenlive](https://github.com/KDE/kdenlive), [OpenCreator](https://github.com/krillinai/OpenCreator), [Resolve MCP](https://github.com/barckley75/resolve-claude-mcp), [Claude video effects](https://github.com/Vibha-Ramprakash/claude-video-effects), [OBS Studio](https://github.com/obsproject/obs-studio) and [Kap](https://github.com/wulkano/Kap). Check availability and compatibility before choosing a tool. |
| Interface quality | [unslop](https://github.com/heydamir/unslop) is a candidate for interface-design review. Its selection and installation remain undecided; do not assume it is installed or use it as a substitute for visual review. |

The tool names above are a research shortlist, not a statement that every repository, skill or runtime is installed. The local resource inventory and REA findings should be checked at the time of production. An installed agent skill provides instructions; it does not install its runtime or train model weights.

## Student experience

Organize each topic around an intuitive explanation, formulas and units, worked examples, practice with diagnostic feedback, and a separate past-midterm section. Provide a self-contained expanded explanation for each topic before withdrawing its existing source document. Keep a clear status for missing explanations, examples, interactive models and videos. Existing AI videos remain available until verified replacements exist.

Treat instructor materials and textbooks as private inputs for curriculum coverage and accuracy. Future student-facing videos should neither show nor mention those source documents. Recreate original diagrams when appropriate, retain private provenance and respect source rights. Remove outside YouTube videos from student navigation; do not classify generated video solely by the presence or absence of a YouTube URL without verifying its source.

## Motion and interaction

Use a restrained but continuously developing visual: a physical model moves, an equation transforms, a graph draws, a part highlights, or the camera reveals a relevant detail. Each motion should advance the explanation without making calculations difficult to read. Use a model, diagram or 3D scene when it helps the learner understand the subject, and ensure all displayed values come from verified calculations.

For browser lessons, offer appropriate controls such as rotation, parameter adjustment, prediction, check, reset and replay. Provide keyboard access, a reduced-motion alternative and a usable mobile layout. For recorded video, drive scenes and narration from explicit timing; an MP4 cannot preserve the learner's controls. Share mathematical models and scene data between web and video where practical, and verify both outputs separately.

### 3D model teaching prompt

> Redesign the **[subject and model]** experience as a guided mini-lesson. Start with a one-sentence plain-language answer to what the learner is seeing and why the topic matters. Present the model as one clear focal point with a short legend linking the real object, relevant variables and the subject. Reveal detail progressively: (1) the big idea, (2) what each important part represents, (3) a guided change to one control and its cause-and-effect on the model and graph, (4) a worked example with units and each needed calculation, and (5) a short prediction check with feedback. Show one primary action at a time, keep advanced settings and full derivations behind clearly labelled expandable sections, and explain how to reset. Use readable typeset mathematical notation, not raw underscores or programming syntax. Give every control a plain-language label, unit and meaningful current value. The 3D model, graph and numeric readout must derive from one verified mathematical state. Keep the view usable with keyboard, on mobile and with reduced motion. Provide a text or static fallback when 3D is unavailable. Do not add an AI chat that only appears functional: connect any tutor interaction to a real service and test it, or provide accurate prewritten guidance instead. Check conceptual accuracy, numerical values, state changes, layouts and the full learner flow before calling the model complete.

For Newton's law of cooling, show a compact temperature-versus-time graph next to or below the model. Mark the selected time with a point on the curve and show the same temperature on the 3D object. Label the dashed line as the surrounding temperature and explain that the curve approaches it. When the student changes time or a parameter, the point, graph, object and readouts must update from the same calculation. Explain that the curve slopes downward when the object starts hotter than its surroundings and upward when it starts colder. Include a short numerical example and put the full graph and derivation behind an optional expansion.

## Replacement queue and release gate

1. Inventory every topic, subtopic and example in the four course curricula. Record existing explanation, formulas, worked example, practice, past-midterm material, AI video, interactive model and expanded guide.
2. Prioritize a MIAE 221 pilot, then expand course by course. Do not label a topic complete until its content and mathematics have been checked against the private curriculum sources.
3. For each original document, identify the expanded replacement and affected lesson links. Check that the replacement is readable and covers the relevant topic before withdrawing the original from the registry, dev server and deployed assets.
4. Verify direct URLs and static copies as well as navigation; hiding a resource card alone is not access control. Check cached and separately hosted assets as well as the new build.
5. Preserve progress identifiers, existing questions and solutions. Run curriculum and integrity checks, inspect representative desktop and mobile lessons, and document any remaining coverage gaps.

**Current status:** The resource library hides documents identified as original teaching PDFs, and the video library offers the AI and solution tracks. This is a navigation change, not complete removal from publication: source documents can still be referenced elsewhere and may remain accessible by direct URL. The wider replacement, 3D video system and regenerated resources remain to be implemented and verified.

## Reusable production prompt

> Create a self-contained lesson for **[course, subject, subtopic]**. Inspect the relevant private course materials and existing explanations; record the scope and privately verify each definition, formula, unit and worked result. Teach the subject directly without displaying or mentioning the source documents. Use intuitive one-on-one narration, then a complete worked example with no skipped arithmetic. Design a meaningful 3D or interactive model where it clarifies the concept; connect all geometry, labels and readouts to the same checked model. Add a prediction, controllable parameters, reset/replay and feedback for common misconceptions. Develop the visual continuously while preserving readability and a reduced-motion option. Plan a separate deterministic narrated video and an interactive browser experience, then verify each independently. Include practice, separate past-midterm questions when available, and a concise exam-pitfall review. Record source provenance privately and list all missing coverage. For a future PDF, use a polished accessible layout with legible mathematics, diagram captions and a worked example; generate it only when explicitly requested. Check the relevant desktop and mobile views, mathematical results, keyboard controls, narration timing, source visibility and direct asset URLs. Preserve the current material until the replacement is verified.
