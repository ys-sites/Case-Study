# Unit-cell photorealism proof

Scope: Crystal Lab unit-cell explorer only (SC, BCC, FCC and HCP). Direction,
Miller-plane and all other learners are unchanged. Wider rollout requires approval.

## Visual change

Before: colored spheres with small direct-light highlights and a grid disc.
After: polished, role-colored metal spheres and rods reflecting a photographic
studio, with a matte neutral floor and soft contact shadows. This depicts a
physical teaching model, not the literal appearance of atoms.

- Self-hosted, lazy-requested Poly Haven 1K studio HDRI: 1,597,273 bytes.
- ACES filmic tone mapping, exposure 1.08, sRGB output.
- Atom metalness 0.82 / roughness 0.26; rods 0.75 / 0.32.
- Contact shadows use a 256-pixel map, rendered once per relevant model-state
  change instead of on every orbit frame. Floor height follows replication and
  explosion so it cannot cut through the bottom layer.
- Device pixel ratio capped at 1.5. No postprocessing AO pass or new dependencies.
- An in-canvas keyboard-operable appearance switch restores teaching colors.
- Optional environment loading has an error boundary; the model, existing direct
  lights and teaching controls remain available if the HDRI request fails.

Exact positions, radii, sharing fractions, role colors, labels, camera controls,
selection, teaching steps, practice/challenge questions, links and validation
specifications use the original code and mathematical state.

Verification also uncovered an existing atom-ID mismatch: the scene uses
`baseId@ijk`, while the detail panel searched for `baseId`. The panel now resolves
the base ID without changing the full selection ID used by the scene.

## Assets and boundaries

See [asset credits](./website/public/3d/crystal/CREDITS.md) for source, author,
individual license, dimensions and integrity hash. Poly Haven Photo Studio 01 is
CC0. The proof uses smooth material parameters and an HDR environment texture;
it does not include scanned surface maps. No GLB is needed for exact unit-cell
geometry, so Draco compression does not apply. The 1.60 MB asset figure excludes
application JavaScript and GPU memory.

## Validation

- `npx tsc --noEmit`: passed.
- `npm run validate:questions`: passed (837 bank + 74 teacher-exam questions).
- `npm run validate:curriculum`: passed across all four courses.
- `npm run test:crystal`: 88 passed, 0 failed, including unit-cell specs.
- `npm run build`: passed; existing large-chunk and mixed-import warnings remain.
- Local Chromium: all four cell types, guided next, explosion, 2×2×2 replication,
  atom sizing, in-canvas atom selection/labels, drag orbit, keyboard appearance
  toggle and 390×844 viewport checked; no JavaScript page errors observed.
- HDRI loaded locally with a measured body size of 1,597,273 bytes.

[Before](./docs/crystal-proof/before.png) ·
[After](./docs/crystal-proof/after.png) ·
[Mobile viewport](./docs/crystal-proof/mobile.png)

Real-phone GPU/frame-rate testing remains necessary before a broad rollout;
desktop browser emulation cannot certify performance on physical phones.

## Implementation files

- `website/src/learn/crystal/UnitCellScene.tsx`
- `website/src/learn/crystal/CrystalLab.tsx` (selected-atom lookup only)
- `website/public/3d/crystal/photo_studio_01_1k.hdr`
- `website/public/3d/crystal/CREDITS.md`
- This proof report.
- `docs/crystal-proof/{before,after,mobile}.png` (visual evidence, not site assets)
