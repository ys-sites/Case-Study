# Approved 3D teaching model standard

This specification applies to future 3D visual learner work. It records the
approved colorful Product, Process and Cellular Layout direction and the
correction requested for INDU 211, ENGR 213 and MIAE 215.

## The essential requirement

Build a recognizable, carefully detailed physical demonstration of the subject.
A paper background, HDRI, new colors or a font change alone does **not** complete
a model upgrade. A cylinder with rectangular wings is not a finished aircraft;
a colored box with rods is not a finished forklift; a straight rod is not a
spring; a cylinder is not an operator. Inspect the geometry in the browser.

The visual reference is [Every Joule](https://iamtechartist.com/every-joule/):
the diagram lifts from a paper page, while selective color explains the changing
quantity. Use the accepted factory layouts as the local quality benchmark.

## Art direction

- Warm paper `#fbf6ea`, secondary paper `#efe6d3`, ink `#1c2433`, brick accent
  `#9a3b2a`. Add distinct teal, blue, ochre and coral machine/component colors.
- A bright tabletop engineering model with soft studio reflections and contact
  shadows. Avoid dark industrial scenery, gritty surfaces or featureless blocks.
- Physical materials: painted steel housings, polished shafts and bearings,
  rubber tires/belts, copper wire, glass vessels, PCB laminate and wooden bases.
  Use PBR roughness and metalness appropriately; preserve semantic color coding.
- Include identifying construction details: controls, fasteners, beveled edges,
  wheels, forks, shelves, clamps, connectors, winding turns, pins and markings.
  Keep detail subordinate to the part being taught.
- Source Serif for paper annotations, compact ink borders, readable numerical
  values, restrained glowing highlights and dashed construction/travel lines.
- Keep existing page layout and learning navigation. Changes belong in the 3D
  canvas and its existing controls unless a later request expands scope.

## Modeling rules

Use individually licensed, self-hosted GLBs for physical props when a suitable
model exists. Keep a source/license record per model, disclose AI-assisted
assets as such, lazy-load them and compress with Draco. Do not run code shipped
with an asset package or install a skill just to download a model.

Build detailed custom geometry when the lesson needs a moving cutaway,
adjustable apparatus or a mathematical structure that cannot be represented by
a static imported model. Custom work must have recognizable construction and
material detail, not the rejected box-and-rod placeholders. Do not add an
unrelated high-detail prop and leave the teaching object unfinished.

For abstract coding and mathematics, a physical teaching instrument is an
analogy. Label it explicitly: chips representing array cells are not a claim
that one hardware chip stores one C++ element. Do not imply a simulated physical
quantity, optimal route or anatomically safe reach when it is only illustrative.

## Required course coverage

| Course / learner | Model requirement |
| --- | --- |
| INDU 211 Product Layout | Manufactured parts, articulated robots, detailed stations and conveyor |
| Process / Cellular Layout | Distinct machine types, visible routing and intact grouping controls |
| Fixed-Position Layout | Recognizable aircraft, assembly-stage distinction, resource trolley/hoist; product stays fixed |
| Hybrid Layout | Detailed feeder machines, assembly equipment, conveyor and moving manufactured part |
| Material Handling | Counterbalance forklift, hoist, conveyor, loaded AGV and equipment-focus controls |
| Warehouse Routing | Detailed stocked racks, picking cart/depot and numbered aisle-following stops |
| Manufacturing Processes | Recognizable milling/press/welding equipment plus accurate interactive cutaways; visible casting mold |
| Bill of Materials | Machined frame, axles, rubber wheels, identifiable bearings/fasteners and correct multiplicities |
| Work Design & Ergonomics | Recognizable operator, adjustable bench, open parts bins and illustrative reach envelopes |
| ENGR 213 Mixing Tank | Glass vessel, motor/impeller, flanges, valves, calibration marks and state-driven liquid |
| Newton's Cooling | Metal specimen in a thermal test rig, probe, readout and direction of heat transfer |
| Mass–Spring | Actual helical spring, telescoping damper, calibrated mass and displacement reference |
| LR/RC Circuits | Detailed source, banded resistor, wound inductor or capacitor, wires and live instrument |
| Complex Roots | Graduated complex-plane instrument with correct root positions and angular spacing |
| MIAE 215 Arrays | Labeled array teaching board, value/address relationship and traversal highlights |
| Memory Architecture | Detailed storage trainer, byte/stride labels and selected pointer/address relationship |
| Arduino Hardware | PCB, actual pin/header detail, chip leads, connectors, input knob, breadboard and LED circuit |

## Interaction and teaching contract

- Preserve controls, presets, guided steppers, quiz links and course topic IDs.
- One mathematical state drives the model, graph, highlighted point and readout.
- Play/pause must stop instructional movement. Orbit, pan and zoom remain usable
  during play and pause. Respect reduced motion; do not autoplay camera movement.
- Keep the opening explanation compact. Introduce parts, one interaction, a
  worked example and a prediction question; advanced detail stays expandable.
- Use typeset math and readable subscripts. Never display raw variable syntax in
  place of a useful label. Programming syntax is appropriate when teaching code.
- Preserve teacher/textbook material privately. Teach the subject with original
  explanations and illustrations; never display those source documents.

## Acceptance checklist for each learner

1. Compare an actual rendered before/after screenshot. Check that the **model**
   changed meaningfully, not only its surroundings.
2. Inspect every mode/preset, control endpoints, reset, playback, pause and orbit.
   Verify quantities and graph alignment where present.
3. Inspect desktop and narrow mobile framing, label collisions and touch/keyboard
   controls. A viewport check does not prove physical-phone frame rate.
4. Check asset loads, WebGL/browser errors and fallback behavior; document the
   largest scene's asset budget and any remaining limitations.
5. Run TypeScript, question, curriculum and visual-topic validators, then build.
6. Follow repository publishing instructions and verify the actual deployed
   commit. Never report a whole course complete when only its environment changed.

## Implementation references

- `website/src/learn/visual3d/ProductLayoutScene.tsx`: approved factory assets.
- `DetailedInduScenes.tsx`: remaining industrial scenes.
- `Engr213Apparatus.tsx`: interactive physics apparatus.
- `Miae215Hardware.tsx`: coding/hardware teaching boards.
- `TeachingModelKit.tsx`: authored detailed components and instruments.
- [Asset credits](./website/public/3d/product-layout/CREDITS.md).
- [Production direction](./VISUAL_LEARNING_PRODUCTION.md).

Paths above are relative to the visual learner directory where abbreviated.
