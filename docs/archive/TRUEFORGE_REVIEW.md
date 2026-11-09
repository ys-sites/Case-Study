# TrueForge: agent runtime review

The local source checkout is `001 Main/03 - AI Development & Agents/trueforge/`, pinned at `8aa993666aa9f487b542c1394817ac3b66577112`. [TrueForge](https://github.com/truefoundry/trueforge) is an MIT-licensed agent runtime with a chat UI, API, model and MCP integrations, skills, session storage and sandbox providers. It can be evaluated for a future internal agent application; it is not required for the current account-free study site or a replacement for Main Brain or Graphify.

## Security and setup status

- Limited static review only: the repository contains executable application code, a large dependency graph, package lifecycle scripts (`postinstall` and `prepare`), network integrations and optional hosted services. A security policy exists; this is not an independent audit or malware clearance.
- The upstream README says local mode has no login by default and is intended for localhost, not public deployment. The application may store sessions and exchange data with the model, MCP and sandbox providers selected by an operator. Never put private lessons, API keys or user data into instructions or external services without an explicit authorization and a data-flow review.
- The checkout contains no `SKILL.md` entry point. It is an application that can load skills, not a skill already installed into Codex, Claude or Gemini. No packages, integrations or agents were installed or configured; no server or upstream setup script was run.
- Microsoft Defender reported its antivirus service not running. No antivirus scan was completed, and a static review cannot establish that software is virus-free.

## If an agent runtime is later requested

First define the precise use case and compare it with the existing project workflow. Review the pinned source and dependencies, local network binding, access controls, model/data providers, stored session retention, tool permissions, sandbox behavior, and costs. Test with synthetic data in a disposable isolated environment before considering any integration. The study site remains account-free with browser-local progress unless the user explicitly changes that requirement.
