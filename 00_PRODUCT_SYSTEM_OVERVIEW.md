---
document_type: product_system_overview
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_1_PRODUCT_SYSTEM
last_updated: 2026-07-22
change_policy: ADR_REQUIRED_AFTER_APPROVAL
---

# Product System Overview

## 1. Document Responsibility

This is the single product and system overview for TikTok Video Intelligence Workbench.

It defines product position, role boundaries, full business value chain, current MVP boundary, dual-track operating model, non-goals, and product principles.

It does not define detailed domain fields, database schema, API routes, page layouts, prompts, workflows, or future capability schemas. Those belong to:

- [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md) for the current MVP chain.
- [02_DOMAIN_MODEL.md](02_DOMAIN_MODEL.md) for current domain concepts.
- [03_TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md) for technical architecture.
- [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md) for deferred long-term capabilities.
- [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md) for reuse evidence.
- [architecture/ADR_LOG.md](architecture/ADR_LOG.md) for decision history.

## 2. Product Position

Product name:

```text
TikTok Video Intelligence Workbench
```

Formal product position:

```text
AI-assisted Content Decision Workspace
AI 辅助内容决策与剧本工作台
```

The product helps operators transform upstream product and business context, product evidence, content knowledge, and reference content into an explainable, human-reviewed, executable content production package.

The current MVP value endpoint is:

```text
Generation-ready Owned Content Production Pack
```

Current users:

- Project owner.
- TikTok operator.
- Product owner.
- Content review owner.

Current business pain:

- Product, evidence, reference, script knowledge, and generation handoff are scattered.
- Operators can generate drafts, but cannot reliably explain why a concept was selected.
- AI outputs often lack source traceability and human approval boundaries.
- Product owners can be misled into thinking they must first design or build a complete platform before validating end-to-end value.

Current product value:

- Convert one product and one operating context into content decisions that can be reviewed.
- Preserve the reason why a product entered content work.
- Keep evidence and reference citations visible.
- Treat AI output as draft until human approval.
- Export a package that can continue into real shooting or future generation work.

## 3. Role Boundary

The project owner's current role is:

```text
AI Product Manager
+
Business System Designer
```

Core responsibilities:

- Understand the real business.
- Define the business problem.
- Clarify inputs, outputs, and human judgment points.
- Express business knowledge as explainable and verifiable system behavior.
- Define acceptance examples.
- Validate with real products.
- Decide the next priority after review.

The project owner does not need to personally complete:

- A generic platform core.
- All backend and frontend code.
- All AI workflows.
- A complete video generation platform.
- A global compliance platform.
- A selection platform.
- Publication and performance feedback systems.

Developers are responsible for:

- Schema.
- API.
- UI.
- Migration.
- Adapter.
- Test.
- Deployment.

Architecture review happens by real slice. It does not require complete abstraction before the first product pilot.

## 4. Full Business Value Chain

Long-term business chain:

```text
商品机会
→ 商品立项
→ Selection-to-Content Handoff
→ 商品事实与 Evidence
→ Reference Intelligence
→ 内容构想
→ Script / Storyboard / Shot
→ Production
→ Publish
→ Performance Feedback
→ Business Learning
```

This chain is the business map, not the implementation order.

## 5. Current MVP Boundary

The current MVP boundary is:

```text
Selection-to-Content Handoff
→ Product / ProductVersion
→ Evidence Lite
→ Versioned Content Knowledge Pack
→ Manual Reference
→ Creative Concept Draft
→ Human-selected Concept
→ Script / Storyboard / Shot List
→ Human Review
→ Markdown / JSON Export
→ Generation-ready Owned Content Production Pack
```

The repository is currently in product and architecture redesign. It is not an iteration of an existing application.

Confirmed current facts:

- No business code exists in this repository.
- No backend exists.
- No frontend exists.
- No database exists.
- No Product Workspace exists.
- No Reference Workspace exists.
- No Creative / Script module exists.
- No Generation module exists.
- No Platform Core code exists.

The current implementation fact source is [working/CURRENT_IMPLEMENTATION_AUDIT.md](working/CURRENT_IMPLEMENTATION_AUDIT.md). Working files are not formal authority, but this audit is retained as evidence of repository state.

## 6. Dual-track Model

Track A:

```text
Walking Skeleton MVP
```

Track A validates the thinnest real end-to-end chain from upstream handoff to generation-ready package.

Track B:

```text
Evolution Backlog / Parallel Lab
```

Track B captures long-term capabilities and independent generation experiments. Track B does not constitute current implementation authorization.

The current Walking Skeleton is defined in [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md). Deferred capabilities are defined in [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md).

## 7. Explicit Non-goals

The current MVP is not:

- A complete selection platform.
- A pure product knowledge base.
- Agent OS.
- A generic workflow platform.
- A Linux-kernel-style platform.
- A video batch generation platform.
- An automatic publishing platform.
- A complete growth feedback loop.
- A multi-tenant SaaS product.

Current work does not implement:

- Full Gate engine.
- Portfolio management.
- Priority algorithm.
- Experiment platform.
- Global compliance engine.
- Store health sync.
- Generation orchestration.
- Multi-agent runtime.
- Microservices.

## 8. Product Principles

1. Real business is more important than theoretical completeness.
2. Human judgment is better than fake automation.
3. Evidence and Reference must be traceable.
4. AI output is draft by default.
5. Approved content must not be silently overwritten.
6. End-to-end value is more important than single-module completeness.
7. Release may skip upstream modules, but must not lose required upstream outputs.
8. Selection-to-Content Handoff is the current MVP input.
9. Content Knowledge Pack is a lightweight current MVP capability.
10. Manual Reference is acceptable in the first version.
11. Owned Content is the current MVP route.
12. Generation-ready Pack is the current MVP output endpoint.
13. Full Generation Orchestration is a future capability.
14. ComfyUI / Seedance work may proceed only as Parallel Lab.
15. Do not build Platform Core before repeated real needs appear.
16. Do not build Agent OS first.
17. Do not split microservices first.
18. Do not build complete Gate, Priority, Portfolio, or Experiment first.
19. Stable shared mechanisms are extracted only from real repetition.

## 9. Implementation Authorization

All formal product and architecture documents currently set:

```text
implementation_allowed: false
```

This documentation consolidation does not authorize business code.

After human review approves [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md), coding work must be authorized through a single future working file:

```text
working/ACTIVE_ITERATION.md
```

That file does not exist after this consolidation.
