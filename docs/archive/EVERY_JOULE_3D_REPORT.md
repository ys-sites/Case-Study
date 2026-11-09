# Paper-stage 3D visual learners

> The original rollout described below was followed by a separate model rebuild.
> The original note that most scenes retained their prior geometry is historical;
> see the follow-up section for the current implementation.

## Detailed model rebuild

The remaining seven industrial learners now have a staged aircraft and hoist,
hybrid assembly equipment, a forklift/AGV, stocked warehouse racks, four
manufacturing cutaways, a detailed roller assembly, and an operator workstation.
The five ENGR 213 learners now use physical test instruments: a mixing vessel,
thermal test rig, spring-and-damper apparatus, switchable circuit board, and a
graduated complex-plane instrument. MIAE 215 has array and memory teaching
boards and a detailed Arduino/breadboard circuit. Array and memory hardware are
explicitly labeled as teaching analogies.

The aircraft has three visible stages. Its segmentation is illustrative rather
than a real manufacturing procedure. The complex-root graph now positions the
`k = 0` point correctly for negative angles, and the Arduino input can reach
the full 0–1023 range. The same existing mathematical functions drive the
apparatus and graphs; heat-flow arrows and the circuit switch reflect the
selected state.

The reusable standard is [THREE_D_MODEL_STYLE.md](./THREE_D_MODEL_STYLE.md).
All newly imported models have individual entries in the asset credits below.
Local interactive tests cover stages, focus controls, routes, process modes, BOM
quantities, reach settings, ADC/PWM endpoints and selected graph relationships.
These checks do not prove every parameter combination or physical-device frame
rate. `website/scripts/verify-detailed-scenes.cjs` contains the regression
checks; `website/scripts/verify-detailed-mobile.cjs` checks a narrow viewport
and keyboard input on one rebuilt learner in each course.

Visual checks: [aircraft stage 1](./docs/every-joule-proof/aircraft-stage-1.png),
[aircraft stage 3](./docs/every-joule-proof/aircraft-stage-3.png),
[cooling on mobile](./docs/every-joule-proof/cooling-mobile.png), and
[Arduino on mobile](./docs/every-joule-proof/arduino-mobile.png). The aircraft
comparison hides annotations to show the actual geometry change.

Primary additions: `DetailedInduScenes.tsx`, `Engr213Apparatus.tsx`,
`Miae215Hardware.tsx`, and `TeachingModelKit.tsx` in
`website/src/learn/visual3d/`; the aircraft preparation and browser checks in
`website/scripts/`; and individually credited GLBs under
`website/public/3d/product-layout/`.

The Every Joule reference describes diagrams lifting from a page with color
showing a changing quantity: https://iamtechartist.com/every-joule/. This work
applies that visual direction to the 18 visual learners registered for INDU 211,
ENGR 213 and MIAE 215, with the existing interactions and calculations retained.

## Original rollout: what changed

- All 18 learners use a warm paper-colored canvas, Source Serif in-scene notes,
  ink borders, studio HDR reflections and ACES tone mapping. Colors that encode
  the educational state remain in their original model logic.
- Product Layout has a new tabletop assembly line, detailed machines, two
  articulated robot models, a rubber conveyor and colored car bodies. Five
  numbered stations appear by default; the existing control still supports
  three through six. The on-scene speed is a relative multiplier, not a measured
  belt speed or throughput prediction. Movement follows the speed control;
  playback and reduced-motion settings control motion.
- Process, cellular and hybrid layout diagrams reuse detailed lathe, milling,
  drill and assembly-bench assets in place of simple machine stand-ins.
- The mixing-tank stirrer respects play/pause and reduced-motion state.

This is a shared visual treatment, not a claim that every physical model was
replaced by a scanned asset. Other industrial scenes and the equation and coding
models retain their existing topic-specific geometry and state. More detailed
modeling remains possible where it would improve clarity.

## Assets and performance

See [individual asset credits](./website/public/3d/product-layout/CREDITS.md)
for licenses, sources and attribution. The model files are lazy-loaded when a
scene uses them, Draco-compressed and served locally. The accompanying HDRI,
font, models and both decoder fallbacks total about 1.8 MB on disk; an ordinary
browser downloads only the decoder variant it needs. JavaScript, other website
assets and GPU memory are separate. A device pixel ratio cap reduces rendering
cost; performance on a physical phone has not been measured.

## Files

- `website/src/learn/visual3d/Visual3DLearner.tsx`
- `website/src/learn/visual3d/Indu3DCanvas.tsx`
- `website/src/learn/visual3d/Engr213SimCanvas.tsx`
- `website/src/learn/visual3d/ProductLayoutScene.tsx`
- `website/src/learn/visual3d/PaperEnvironment.tsx`
- `website/src/learn/visual3d/productLayoutScene.css`
- `website/public/3d/product-layout/` (credited models, HDRI, font and decoder)
- This report and `docs/every-joule-proof/` comparison images.

## Verification

Local checks passed:

- `npx tsc --noEmit` and `npm run build`.
- `npm run validate:questions` (837 bank questions and 74 teacher-exam questions).
- `npm run validate:curriculum` and `npm run validate:visual-topics` (41 registered topics).
- Browser smoke checks for all 18 affected routes: canvas, guide and primary
  control present, no equipment-load fallback and no JavaScript page errors.
- Product Layout: five default station markers; station counts of three and
  six; speed readout changes; visible motion while playing; stationary model
  after pause; orbit interaction; reduced motion; and a 390 px mobile viewport.
- Process, cellular and hybrid layouts checked again after adding the assembly
  bench asset.

The build still reports existing large-bundle and mixed-import warnings.
These checks do not establish error-free coverage of every parameter combination
or smooth rendering on a physical phone.

The browser checks are preserved in `website/scripts/verify-paper-scenes.cjs`
and `website/scripts/verify-product-controls.cjs`. Run them from `website/`
with Playwright and Chromium available. `PLAYWRIGHT_PATH` can point to an
existing Playwright module; `PROOF_URL` selects a deployed base URL instead of
the default local Vite server. Screenshots go into `node_modules/.cache/`.

## Visual comparison

- [Before: Product Layout](./docs/every-joule-proof/before.png)
- [After: colorful machines and manufactured parts](./docs/every-joule-proof/after.png)
- [Mobile view](./docs/every-joule-proof/mobile.png)
- [ENGR 213 mixing tank](./docs/every-joule-proof/mixing-tank.png)
- [MIAE 215 array traversal](./docs/every-joule-proof/arrays.png)

The comparison shows a brighter paper stage, recognizable machine silhouettes,
colored car shells, robot arms and ink-style notes. The equation and coding
diagrams retain their pedagogical shapes under the same lighting and annotation
treatment. Only the 3D presentation changes; the surrounding page layout remains
unchanged.
