# Website essentials for the Concordia learning portal

This guide adapts the owner's `web_essentials.txt` to the existing React, TypeScript, Vite and Vercel application. Use it for website planning, implementation and review alongside [AGENTS.md](./AGENTS.md), [WORKSPACE.md](./WORKSPACE.md), and the relevant course or visual-learning instructions. It does not replace a user's later instructions or project-specific requirements.

## Start with the actual task

- Inspect the relevant existing components, design tokens, routes and data before changing them. Preserve unrelated work and existing student progress.
- Choose available skills and references that materially help the task. Use them together when appropriate; do not assume that a named skill is installed, run installers automatically, or force a fixed skill stack on every change.
- Keep the account-free experience: no login, profile, cloud progress or server-side student accounts unless explicitly requested. Preserve browser-local progress and existing question identifiers.
- Treat teacher and textbook materials as private curriculum inputs. Student-facing explanations and visuals must be original and must not expose the documents, personal names or machine-specific paths.

## Design and accessibility

- Build on the existing course identity, shared tokens and the approved white, illustrated engineering-learning direction. Refer to [VISUAL_LEARNING_PRODUCTION.md](./VISUAL_LEARNING_PRODUCTION.md) for videos and interactive visuals.
- Prefer clear hierarchy, readable typography, consistent spacing, restrained color and controls with understandable labels. Remove effects that distract from learning; use motion to explain the subject.
- Check responsive layouts at representative mobile and desktop widths, prevent horizontal overflow, and keep touch targets usable. Provide keyboard operation, visible focus, meaningful labels, sufficient contrast, reduced-motion support and appropriate captions or alternatives for media.
- Keep models, labels, calculations and charts consistent with one verified state. Explain what the student sees and what changes during an interaction.

## Engineering and security

- Fit changes to the existing architecture instead of replacing the framework or adding dependencies by default. Separate content, UI and calculations where useful, and handle loading, errors and empty states.
- Keep secrets out of client bundles, documents and version control. Validate untrusted inputs at the server boundary; use parameterized queries where a database is used, and encode or sanitize output as appropriate to its context.
- Apply access checks, CSRF protections, abuse controls and rate limits where the feature actually requires them. Do not introduce authentication or collect extra personal data as a generic checklist item.
- Use HTTPS in production, narrowly scoped CORS and security headers appropriate to the application. Preserve existing data and verify migrations before deployment.
- Treat performance budgets as targets to measure, not promises: inspect bundle size and actual loading behavior when relevant; use responsive assets, defer nonessential work, and keep instructional animation usable with reduced motion.

## Verify and hand off

- Run focused checks suited to the change, including mathematical and data integrity checks for learning content. For substantial application changes, run the applicable build and inspect representative desktop, mobile and keyboard flows when available.
- Explain what was verified, what could not be checked and any remaining risks. Do not claim that a site is secure, accessible, performant or error-free without evidence.
- Follow the repository's current Git and deployment instructions, inspect the destination before publishing, and avoid staging unrelated changes or private material.

## Reference library from the supplied essentials

Use these as research references when relevant; their inclusion does not mean they are installed, verified, compatible, or required for this project. Check licenses and current documentation before adoption.

- Design systems and interface craft: [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), [awesome-design-md](https://github.com/VoltAgent/awesome-design-md), [Impeccable](https://github.com/pbakaus/impeccable), [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design), and [Unslop](https://github.com/heydamir/unslop).
- Motion and UI components: [Motion](https://github.com/motiondivision/motion), [React Bits](https://github.com/DavidHDev/react-bits), and [design motion principles](https://github.com/kylezantos/design-motion-principles).
- Security references: [secure-rules-files](https://github.com/wiz-sec-public/secure-rules-files), [OWASP AISVS](https://github.com/OWASP/AISVS), and the [OWASP Secure Coding Practices Quick Reference](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/).
