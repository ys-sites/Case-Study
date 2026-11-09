# Cinematic 3D product commercials

This independently authored project workflow is based on the requested brief and public tool documentation. The separately licensed motion-video-director skill remains in the local, Git-excluded resource library.

Use this workflow for a product commercial when the brief calls for cinematic
3D, smooth camera movement through believable spaces, and clear feature beats.
It is a separate creative direction from the educational visual-learner style.

## Creative direction

Use Yambo Studio's Navan Edge work as a reference for qualities the user likes:
warm, carefully shaped light; polished materials; smooth motivated camera
movement; real-world environments; a product feature demonstrated in each
scene; and a clean closing tagline. Seek a Cinema 4D/Redshift-like finish while
creating original scenes and motion. Do not copy protected footage, layouts,
audio, logos or other brand assets without permission. The optional local research page is `001 Main/Animated Commercial Video Tools.html`; the resource library is not part of this repository checkout.

The research page distinguishes evidence about Yambo's general workflow from
verified credits for this specific film. Do not claim that the Navan spot's
shot-by-shot software or production team was established if it was not.

## Brief and shot structure

Gather only missing essentials: product name, three key features, approved
product references and logo, target audience, aspect ratio, duration, tagline,
voice/music needs, delivery deadline and any spending or provider constraints.
When a real product, device, package or UI is involved, verify what it actually
looks like and what each feature does. Do not invent claims or capabilities.

Structure the commercial as a compelling hook, one feature beat per scene, then
the tagline and brand lockup. A useful default is five scenes: hook, three
features, close. Every shot should specify its environment, purpose, product
pose, lens, start/end camera position, lighting, action, on-screen information,
duration, transition, audio cue and continuity checks. Hold the product and UI
long enough to understand them; make movement reveal an idea rather than merely
fill time.

## Production workflow

1. **Inspect the reference and make original style frames.** Analyze framing,
   materials, colors, lighting, transitions and pacing. Record a shot list and
   continuity manifest with product dimensions, proportions, material colors,
   label placement, approved logo and lighting references.
2. **Build the product once in Blender.** Use the same canonical model and
   textures in every Blender shot; link or instance the asset rather than
   rebuilding it per scene. Use Blender's Cycles or Eevee as appropriate to
   the hardware and desired result. If available and appropriate, Claude Code
   or another coding agent can control the scene through Blender MCP. The
   current [community MCP project](https://github.com/ahujasid/mcp-for-blender)
   is not an official Blender Foundation integration. Inventory and review any
   add-on before enabling it; it can execute Python in Blender. No installation,
   model download or provider call occurs merely because this guide is read.
3. **Plan and orchestrate in OpenMontage when available.** Select the installed
   pipeline that actually fits the product film and inspect its manifest and
   provider capabilities. Its public example describes a product film using
   approved stills as first and last frames; do not assume every pipeline or
   provider has that feature. For each AI-generated shot, use product-accurate
   first and last reference frames when the selected model supports them; render
   those frames from the canonical Blender asset where practical. Frame anchors
   improve continuity but do not guarantee identity between frames: inspect the
   full clip and reject drift in shape, colors, labels or logos. If the chosen
   provider cannot accept the required anchors, use another supported route or
   a deterministic Blender-rendered shot for identity-critical material.
4. **Use AI only where it helps.** For optional hero shots consider local
   ComfyUI with Wan 2.1 or a user-selected service such as Runway Gen-4.5,
   Kling or Google Veo via Flow. Check the current service's availability,
   version, input support, commercial-use terms, GPU needs and cost. A local
   model still needs compatible hardware and downloaded weights. Target 5–15
   second AI clips where the selected provider supports that length, and plan
   for roughly 3–5 generations per keeper. This is a planning allowance, not a
   guaranteed acceptance rate; confirm the actual request and credit budget
   before paid generation. Never upload private brand assets without the
   authorization required by the user's chosen provider and project.
5. **Composite product UI, text and logo deterministically.** Do not ask an AI
   video model to produce final legible text or logos. Use approved brand files
   and HyperFrames or Remotion for real UI, typography, feature callouts and
   end cards. Track those overlays to the 3D shot when necessary. If AI changes
   the real product's silhouette or brand, replace the product layer with the
   canonical Blender render instead of accepting an incorrect result. Spline is
   an optional browser-based 3D route for stylized software-product showcases.
6. **Preview, edit and finish.** Inspect contact sheets and the first, middle
   and last frames of every shot, then watch transitions at speed and listen to
   the mix. Check continuity of proportions, screen contents, labels, logo,
   colors, light direction, shadows, camera path and scale. Confirm all claims
   and spelling against the approved brief. Fix discontinuities; do not describe
   an unreviewed AI render as product-accurate. Honor the project's requested
   review gates and keep prior approved files intact.

## Deliverables

- Finished MP4 in the requested format and aspect ratio.
- Editable `.blend` scene file with the canonical product and any required
  project-local assets or a manifest explaining how to relink them.
- A per-scene prompt and shot list, including provider/model/version, seed when
  available, first/last-frame references, generation choices and any known
  limitations; include the final tagline and feature claims.
- Asset and music/font licence notes and a clear record of what was actually
  rendered, generated, inspected and approved. Do not expose credentials,
  private machine paths or unlicensed reference material in the deliverables.

## Reusable prompt

> Create a cinematic 3D animated commercial inspired by the warm lighting,
> smooth camera moves through believable spaces, polished materials and clear
> feature-by-feature storytelling of Yambo Studio's Navan Edge ad. Create an
> original treatment rather than copying the reference. Product: **[PRODUCT
> NAME]**. Key features: **[FEATURE 1]**, **[FEATURE 2]**, **[FEATURE 3]**.
> Audience: **[AUDIENCE]**. Format and duration: **[FORMAT / DURATION]**.
> Tagline: **[TAGLINE]**. Approved product and brand assets: **[ASSETS]**.
>
> Open with a hook, demonstrate one feature per scene, then end on the tagline.
> Build and reuse one canonical product model in Blender, using Blender MCP from
> Claude Code or another compatible coding agent where available. Use an
> appropriate OpenMontage pipeline for planning and assembly. For AI-generated
> shots, use first and last frames derived from the canonical product when the
> chosen provider supports them; inspect continuity throughout and use a
> Blender-rendered product layer if identity drifts. Consider ComfyUI with Wan
> 2.1 locally, or a compatible Runway, Kling or Veo service, only where useful.
> Aim for 5–15 second AI shots where supported and budget approximately 3–5
> generations per keeper. Use HyperFrames or Remotion for accurate UI, labels,
> logos and feature callouts; never rely on AI-generated text or logos. Spline
> may be used for a stylized software-product showcase where appropriate.
>
> Deliver the finished MP4, the editable Blender scene and its asset manifest,
> and the per-scene prompts, reference frames and production notes. Show a
> reviewable storyboard and estimate any paid generation before spending.

## Tool references

- [Blender](https://github.com/blender/blender) and [Blender MCP](https://github.com/ahujasid/mcp-for-blender)
- [OpenMontage](https://github.com/calesthio/OpenMontage)
- [HyperFrames](https://github.com/heygen-com/hyperframes) and [Remotion](https://github.com/remotion-dev/remotion)
- [ComfyUI](https://github.com/Comfy-Org/ComfyUI) and [Wan 2.1](https://github.com/Wan-Video/Wan2.1)
- [Spline](https://spline.design/)
