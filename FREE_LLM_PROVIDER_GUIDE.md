# Free LLM API resources and routing

The local `001 Main/free-llm-api-resources/` checkout is a third-party directory of API providers. It is a reference, not a skill, an API client, model weights, or evidence of an enabled account. The directory can be absent on another machine. Source: <https://github.com/raullenchai/free-llm-api-resources>.

## Setup status

- NVIDIA was requested for the local Bifrost Model Router; it is not yet configured or tested. The router source is staged separately in the local workspace. At the time of this guide, WSL/Ubuntu and Docker prerequisites still needed resolution; verify their actual state before proceeding.
- OpenAI access through the existing Codex login must be retained if Bifrost is configured. Preserve existing settings and make a backup. Do not change the website or send requests automatically.
- No other provider or account has been connected. A model being listed does not prove that an account can access it, that Codex can use its tools, or that its use will remain free.

## Provider inventory

The source directory categorizes OpenRouter, Google AI Studio, NVIDIA NIM, Mistral, Hugging Face, Vercel AI Gateway, OpenCode Zen, Cerebras, Groq, Cohere, GitHub Models and Cloudflare Workers AI under free providers, and Fireworks, Baseten, Nebius, Novita, AI21, Upstage, NLP Cloud, Alibaba Cloud Model Studio, Modal, Inference.net, Hyperbolic, SambaNova and Scaleway under trial credits. These are the directory's categories, not guarantees: some require verification, have limited or temporary credits, charge after allowances, or may change terms. Recheck official account-specific terms and quotas before enabling any provider.

For broad model access, [OpenRouter's free-model catalog](https://openrouter.ai/collections/free-models) lists free variants and notes that one OpenRouter API key can access multiple models. Do not select paid variants implicitly. [Google's Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) says free-tier content may be used to improve products; check current regional and account terms before sending data.

## Safe connection workflow

1. Identify the user's actual accounts and API products; do not sign up, add billing or assume access. Confirm whether each provider's free tier is suitable for the intended use and data.
2. Consult official provider documentation for endpoints, free eligibility, quotas, data retention/training policy, and the API compatibility required by the client. Treat the directory's numbers as potentially stale.
3. Complete the router prerequisites, inspect the existing configuration, and preserve the OpenAI route. Configure only accounts the user owns, using the router's documented setup and appropriate provider adapter. Do not expose the router publicly.
4. Create provider-specific secret placeholders in a private local environment file outside the repository; the user enters secrets locally, not in chat. Never commit keys, send them to another provider, print them, or place them in browser code. If a key was exposed, rotate it.
5. After credentials exist, verify the available models for the specific account, ask whether to enable all discovered models or a restricted selection, and enforce free-only choices where requested. Check whether paid fallback or billing could occur; disable it unless explicitly authorized.
6. Verify provider authentication, a local health check, and a minimal inference request only after explaining possible quota consumption. Record the provider, privacy constraints, actual enabled models and verification results without secrets. Keep unverified providers marked as unavailable.

Avoid sending private course documents, student data, source code or secrets to any provider until its current terms and the user's permission allow it. The public website must not contain provider secrets. LLM output needs human or automated subject-matter verification before being presented as correct.
