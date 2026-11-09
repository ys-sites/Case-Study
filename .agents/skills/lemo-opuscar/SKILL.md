---
name: lemo-opuscar
description: Direct and produce a short film made entirely in code, in one of the styles of the Lemo-Opuscar library (e.g. Impasto Oil Painting 油画厚涂, Watercolor Brush 水彩笔刷, Ukiyo-e 浮世绘, Satellite Briefing 卫星简报, Exploded Teardown 产品拆解). Use when the user asks for a video, film, short, promo, explainer or animation (视频、短片、动画、宣传片) in a named style, including explainers built from real material such as satellite imagery, laser scans, CAD files or archive scans (数据解说、科普、产品拆解), and new films cut from real archive footage and documents (剪辑与纪实, e.g. 用档案影像剪一支新闻片); when they want a film about their own topic and haven't chosen a style (help them choose); when they want to change a style into their own, make their own style from a blank page, or use a style they saved (改风格、从空白开始、我的风格); when they start the skill without saying what they want; or when they ask which film styles there are. Not for plain editing, trimming or converting the user's existing video files.
---

# Lemo-Opuscar

The styles, guides and tools live in the Lemo-Opuscar library (github.com/lemomo-ai/lemo-opuscar). This skill fetches it and hands you over to it.

1. **Use the existing library.** From the Concordia project root, use `001 Main/01 - Video & Motion Graphics/lemo-opuscar/` as the library. Do not automatically clone, update, or run `setup.sh`.
2. **Review tools before use.** Check the specific script, dependencies, downloads, licenses and network destinations needed for the requested output. Do not automatically install dependencies or read unrelated credentials. Use existing tools when suitable; report missing tools and do not claim they are installed.
3. **Follow the applicable project guidance.** Read `MAIN_BRAIN_PIPELINE.md`, `LEMO_OPUSCAR_REVIEW.md`, and the relevant library guides and selected style. User instructions and project requirements take priority; for educational lessons preserve the approved warm-white illustrated teaching style. Do not send private material to external services without authorization.

What changes in skill mode:

| | |
|---|---|
| Project folder | `<name>/` in the folder the user started from (lowercase letters, digits, hyphens; avoid `#` and `?` in the path). Wherever the guides say `films/<name>/`, read this folder |
| Running tools | from `$LIB`, with the project's absolute path: `cd "$LIB" && node core/render/still.mjs "<project>" 1.5 3` |
| Library files in pages | absolute URLs: `/core/lib.js`, `/node_modules/three/…` (the project is served at `/@film/`) |
| Library files in scripts and `build.sh` | `$LIB/…`, with `LIB=<path>` at the top of `build.sh`; never `../..` |
| Demo source | Consult the existing local checkout where available. Review any additional download and its rights before use; do not run the bootstrap automatically. |

Deliver what `$LIB/DIRECTOR.md` §11 lists, in the project folder, and tell the user where it is.
