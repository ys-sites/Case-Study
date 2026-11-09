# Lemo Opuscar: local film-style resource

The source checkout in `001 Main/01 - Video & Motion Graphics/lemo-opuscar/` is pinned at `bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00` ([upstream](https://github.com/lemomo-ai/lemo-opuscar), MIT). Its film-style prompts and techniques can inform video production, subject to the project's approved visual teaching style, accuracy, accessibility and licensing. The local project skill is `.agents/skills/lemo-opuscar/`.

## Security and setup

This is a limited static inspection, not a malware audit or proof of safety. The upstream skill automatically runs a setup script to clone or update a library and install packages. The script invokes npm and pip, downloads additional assets and may remove a broken virtual environment. Voice and music tiers require further packages; some voice options use an online service. Dependencies include unpinned Python packages and Node packages with version ranges.

Use the existing source checkout instead of automatically cloning or updating it. Inspect the exact scripts, packages, external destinations, asset rights and intended filesystem changes before running any setup or tool. Do not read unrelated secrets or transmit private course material without authorization. No upstream setup scripts, dependencies, models or video tools were run or installed for this review. Microsoft Defender reported antivirus and real-time protection disabled, so no antivirus scan was completed.
