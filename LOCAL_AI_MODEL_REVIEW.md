# Local AI and video-model references

Review date: 2 November 2026. These are limited static inspections, not complete security audits or proof of safety. Neither model runtime, weights, provider account nor production integration is installed or configured here.

## MiniMax H3

- Local source: `001 Main/01 - Video & Motion Graphics/MiniMax-H3/`, revision `199b7d0e1fd95e7b3eafa8c15eca692534142427` ([upstream](https://github.com/MiniMax-AI/MiniMax-H3)). The repository describes a multimodal video generation system with audio and offers an API as well as model checkpoints. Review the [MiniMax H3 Community License](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE) and all third-party asset rights before use.
- **Territorial and output restrictions:** the license text excludes the United States, European Union, United Kingdom and South Korea from its applicable territory and restricts use and display of the works and outputs outside that territory. A globally accessible website can implicate these terms. It also restricts using outputs to improve other AI models. Have counsel assess the current terms and any applicable separate provider license before producing or publicly publishing material; do not assume general commercial or worldwide rights.
- The portable prompt-writing skill is installed locally at `.agents/skills/h3-prompt-writing/`. It contains Markdown instructions and two text references. Use it only for MiniMax H3 prompts when useful, preserving the approved educational style and accurate content. It does not generate videos or connect an API by itself.
- The eight other bundled video skills describe MiniMax Hub-specific tools; they remain source references and are not configured here. The source checkout was obtained with LFS smudging disabled; model weights have not been verified or configured for inference.
- The inference requirements include PyTorch and a Git-pinned Diffusers dependency. Model instructions call for `trust_remote_code=True`, which can execute model-repository code. Review the exact code, packages, model source and licenses before executing or downloading weights. Hosted generation sends supplied prompts and media to its provider; do not send private course material without authorization and an applicable privacy review.

## AirLLM

- Local source: `001 Main/03 - AI Development & Agents/airllm/`, revision `b0b1a7efc033360e1d9e799f14287b8d4fe154bc` ([upstream](https://github.com/lyogavin/airllm)); Apache-2.0. It is a language-model inference library, not a video generator or a portable agent skill.
- Its layer-offloading approach may reduce GPU memory use, but model downloads and layer splitting can consume substantial disk space and may be slow. Hardware requirements depend on the model and configuration. It does not establish compatibility with MiniMax H3's video pipeline.
- Static inspection found code paths using `trust_remote_code=True`, optional Hugging Face tokens, Git-sourced dependencies and a `delete_original` option that may remove original model files if explicitly enabled. Treat model code and dependencies as executable; inspect them before installation or inference, never expose credentials, and leave deletion disabled unless specifically authorized.

## Safety status

The reviewed prompt-writing skill requires no executable helper in its own directory. No upstream setup scripts, dependencies, model code or API connections were run for these resources. Microsoft Defender reported antivirus not running at review time, so no antivirus scan was completed. Review each bundled third-party skill, model, dependency, endpoint and license separately before use.
