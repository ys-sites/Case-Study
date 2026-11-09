import { Document } from '../types';

export interface DocumentTemplate {
  id: string;
  title: string;
  description: string;
  category: string;
  tags: string[];
  content: string;
}

export const TEMPLATES: DocumentTemplate[] = [
  {
    id: 'blank-page-manifesto',
    title: 'The Philosophy of the Blank Page',
    description: 'A meditation on beginnings, creative whitespace, and overcoming inertia.',
    category: 'Essay',
    tags: ['manifesto', 'writing', 'philosophy'],
    content: `# The Philosophy of the Blank Page

> "The blank page is not a void to be feared; it is an unburdened territory of possibility."

Every significant achievement began as a clean slate. Before the code was compiled, before the cathedral was drafted, before the treaty was ratified, there was only the quiet stillness of an unmarked surface.

## 1. The Myth of the Great Beginning
We often delay putting ink to paper because we imagine the first sentence must possess biblical weight. It does not. The true purpose of the first mark is purely structural: it shatters the paralysis of perfection.

- **First drafts exist to be corrected**, not revered.
- **Rhythm precedes elegance**: write with velocity, refine with scrutiny.
- **Silence cultivates thought**: remove the noise of dashboards and notifications.

## 2. The Discipline of White Space
In typographic art, negative space is what gives letterforms their dignity. Similarly, a focused mind requires an environment stripped of superfluous controls.

### Architectural Rules for Deep Focus
1. **Single focal point**: Work on one paragraph until its cadence settles.
2. **Tactile feedback**: Sound and rhythm synchronize cognitive flow.
3. **Continuous revision**: Capture snapshots along the journey.

\`\`\`
Cognitive Input -> Reflection Window -> Articulated Prose
\`\`\`

When you sit before a blank page, you are in dialogue with your future self. Begin with whatever fragment is nearest to hand.
`,
  },
  {
    id: 'technical-rfc',
    title: 'RFC-104: High-Throughput Event Streaming Architecture',
    description: 'Engineering request for comments specifying architecture, invariants, and rollback plans.',
    category: 'Engineering',
    tags: ['rfc', 'architecture', 'systems'],
    content: `# RFC-104: High-Throughput Event Streaming Architecture

**Author**: Staff Systems Architect  
**Status**: In Review  
**Target Release**: Q3 2026  

---

## Abstract
This document proposes a decoupled event pipeline to ingest up to 250,000 telemetry events per second with sub-50ms p99 latency across distributed edge nodes.

## Motivation & Constraints
The current synchronous RPC ingest model suffers from backpressure cascading during network partitions. We require an asynchronous buffer with bounded memory overhead.

### Key Performance Invariants
- **Latency**: p99 < 45ms under peak saturation
- **Durability**: Zero acknowledged event loss during ungraceful node restarts
- **Backpressure**: Deterministic client-side retry with exponential jitter

## Proposed Architecture

\`\`\`typescript
interface TelemetryPayload {
  readonly traceId: string;
  readonly timestampUs: bigint;
  readonly sourceRegion: 'us-east' | 'eu-west' | 'ap-southeast';
  readonly payloadBytes: Uint8Array;
}
\`\`\`

### Ingest State Machine
1. **Edge Filter**: Ingest payload, validate schema header, assign monotonic cluster sequence.
2. **Ring Buffer**: Write to memory-mapped local ring buffer without JVM GC pauses.
3. **Partition Dispatcher**: Hash-route to topic brokers based on \`traceId\`.

## Migration & Rollback Strategy
- Phase 1: Shadow write 5% of dark traffic to verify latency distribution.
- Phase 2: Canary ingestion for non-critical telemetry metrics.
- Rollback trigger: Any drop in SLA below 99.95% over a 5-minute rolling window automatically trips circuit breakers back to legacy ingestion.
`,
  },
  {
    id: 'product-spec',
    title: 'PRD: Autonomous Knowledge Graph Synthesis',
    description: 'Product specification covering user problems, core mechanics, and success criteria.',
    category: 'Product',
    tags: ['prd', 'strategy', 'specs'],
    content: `# PRD: Autonomous Knowledge Graph Synthesis

## 1. Problem Statement
Cross-functional teams lose approximately 4.2 hours per week navigating fragmented technical documentation across Jira, GitHub discussions, and Slack threads.

## 2. Objective & Measurable Outcomes
Synthesize disparate documentation into an interactive living knowledge graph that automatically links interrelated RFCs, designs, and decisions.

- **Outcome 1**: Reduce context-gathering time for new engineers by 40%.
- **Outcome 2**: Surface stale documentation within 48 hours of related code changes.

## 3. User Scenarios
- **The New Hire**: Explores why an architectural decision was made two years ago without scheduling a sync with the original author.
- **The Tech Lead**: Audits dependencies before deprecating an internal protocol.

## 4. Key Requirements
- [x] Full text indexing of Markdown and code snippets
- [x] Bi-directional hyperlinking with live hover previews
- [ ] Automated dependency graph visualization
- [ ] Export to static site generation for offline reading
`,
  },
  {
    id: 'daily-journal',
    title: 'Daily Synthesis & Evening Reflection',
    description: 'Structured framework for morning intentions, daily milestones, and evening clarity.',
    category: 'Journal',
    tags: ['journal', 'habits', 'clarity'],
    content: `# Daily Synthesis & Evening Reflection

**Date**: Today  
**Energy**: High  
**Focus Anchor**: Craftsmanship  

---

## 🌅 Morning Clarification
What single accomplishment will make today a decisive step forward?

1. Ship the finalized document editor interface with complete tactile feedback.
2. Conduct a deep review of typographic proportions across screen sizes.
3. Protect 90 minutes of continuous, uninterrupted thinking time.

## 🧠 Ideas & Observations
> "Simplicity is about subtracting the obvious and adding the meaningful." — John Maeda

- The friction of switching between too many tabs is the enemy of deep reasoning.
- When an interface respects the user's attention, the work becomes natural.

## 🌙 Evening Retrospective
- **What worked with surprising ease?**  
  The Web Audio synthesis engine provides a delightful rhythm that makes typing feel immediate and satisfying.
- **What friction did I encounter?**  
  Resisting the urge to add unnecessary chrome or buttons.
- **Action for tomorrow morning**:  
  Start directly with the hardest problem while mental clarity is pristine.
`,
  },
];

export const INITIAL_DOCUMENTS: Document[] = [
  {
    id: 'doc-1',
    title: 'The Philosophy of the Blank Page',
    content: TEMPLATES[0].content,
    tags: ['manifesto', 'writing'],
    category: 'draft',
    isFavorite: true,
    createdAt: Date.now() - 86400000 * 2,
    updatedAt: Date.now() - 3600000 * 3,
    snapshots: [
      {
        id: 'snap-1',
        timestamp: Date.now() - 86400000,
        title: 'Initial Outline',
        content: '# The Blank Page\n\nNotes on overcoming resistance.',
        wordCount: 8,
      },
    ],
  },
  {
    id: 'doc-2',
    title: 'RFC-104: High-Throughput Event Streaming Architecture',
    content: TEMPLATES[1].content,
    tags: ['rfc', 'systems'],
    category: 'published',
    isFavorite: false,
    createdAt: Date.now() - 86400000 * 5,
    updatedAt: Date.now() - 3600000 * 12,
    snapshots: [],
  },
  {
    id: 'doc-3',
    title: 'PRD: Autonomous Knowledge Graph Synthesis',
    content: TEMPLATES[2].content,
    tags: ['prd', 'product'],
    category: 'draft',
    isFavorite: false,
    createdAt: Date.now() - 86400000 * 7,
    updatedAt: Date.now() - 86400000 * 1,
    snapshots: [],
  },
];
