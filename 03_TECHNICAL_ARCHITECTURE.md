---
document_type: technical_architecture
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_2_TECHNICAL_ARCHITECTURE
last_updated: 2026-07-22
change_policy: ADR_REQUIRED_AFTER_APPROVAL
depends_on:
  - 00_PRODUCT_SYSTEM_OVERVIEW.md
  - 01_MVP_WALKING_SKELETON.md
  - 02_DOMAIN_MODEL.md
  - 05_EXISTING_SYSTEM_MAPPING.md
  - architecture/ADR_LOG.md
---

# Technical Architecture

## 1. Document Responsibility

This document defines the technical architecture direction for the current Walking Skeleton.

It is not a low-level design, final directory layout, dependency manifest, deployment plan, database schema, or API contract.

## 2. Technical Stack

Current stack direction:

| Area | Choice |
|---|---|
| Backend | Python 3.12 |
| API | FastAPI |
| Validation | Pydantic |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL |
| Migration | Alembic |
| Backend tests | pytest |
| Frontend | React |
| Frontend language | TypeScript |
| Frontend tooling | Vite |
| Frontend tests | Vitest |
| Local infrastructure | Docker when explicitly authorized by an active iteration |

This consolidation does not install dependencies or create code directories.

## 3. Architecture Style

Adopt:

```text
Modular Monolith
+
Production-intent Walking Skeleton
+
Fixed Workflow First
+
Provider Adapter
+
Human Review
```

Implications:

- Build the first real chain thinly end to end.
- Keep stable IDs, provenance, versions, review, migration, and adapter boundaries serious from the start.
- Do not create a generic workflow platform before repeated use proves the need.
- Keep external providers behind adapters.
- AI output remains draft until human review.

## 4. Suggested Modules

Conceptual modules may include:

- `product`.
- `reference`.
- `content`.
- `delivery`.

These are not directory creation instructions.

Only create code directories when an approved active iteration needs them. Do not create empty modules for future capabilities.

## 5. Platform Boundary

The previous platform observations remain useful:

- Resource.
- Capability.
- Execution.
- Policy.
- Trace.

They are long-term platform observation dimensions, not a requirement to implement a Kernel Framework now.

Current work must not implement:

- Resource Framework.
- Capability Registry.
- Execution Engine.
- Policy DSL.
- Trace Service.
- Agent Runtime.

Future terminology should prefer:

```text
Platform Core
```

Do not inflate the current architecture into a Linux-kernel-style platform.

## 6. Platform Core Extraction Rule

A shared mechanism may be considered for Platform Core only after:

```text
The same mechanism repeats in at least two real business modules
+
three real product pilots validate the need
```

Until then, use direct application logic inside the Walking Skeleton.

## 7. AI Boundary

Rules:

- AI output is draft by default.
- Use structured outputs for AI-generated business artifacts.
- Prompt and Knowledge Pack versions must be traceable.
- Run records must preserve input versions, model/provider, output version, cost, and errors.
- External models are accessed through adapters.
- Current workflow is fixed and human-triggered.
- Do not implement multi-agent runtime.

First implementation requirement:

- Use a real, versioned Knowledge Pack v0.1.
- The pack may be represented as Markdown / YAML in an approved active iteration.
- It must include Script Rules, Pattern Cards, Hook Guidance, Claims Guardrails, Review Rubric, and Market Style Notes.
- AI Run records must include the Knowledge Pack version used.
- Do not build knowledge UI, search, tags, or management platform in the current MVP.
- This documentation alignment does not create a `knowledge/` directory or files.

## 8. Existing System Integration

Existing sibling repositories and tools may inform future implementation, but they are not current system code.

Integration rule:

- TikTok search through future `TikTokSearchAdapter`.
- Video breakdown through future reference media adapter.
- Generation Lab through isolated generation adapters or lab tooling.
- No direct copy of sibling repository code.
- No live external API call without explicit authorization.

Detailed evidence is in [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md).

## 9. Generation Boundary

Current main-system boundary:

```text
Generation-ready Production Pack
→ Future Generation Adapter Boundary
```

The current MVP does not model or implement:

- GenerationPlan.
- RenderBatch.
- RenderJob.
- Worker.
- Queue.
- Provider routing.
- Automatic batch costing.
- ComfyUI / Seedance / Kling orchestration.

Detailed generation orchestration is deferred to [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md).

## 10. Non-functional Baseline

Current baseline:

- Stable ID.
- Provenance.
- Versioning.
- Human Approval.
- Migration.
- Error Visibility.
- Testability.
- Local Reproducibility.

Out of current scope:

- Enterprise high availability.
- Multi-tenant SaaS infrastructure.
- Kubernetes.
- Microservices.
- Generic distributed workflow orchestration.

## 11. Local Development Direction

Future active iterations may create backend, frontend, database, and Docker files only when explicitly authorized.

Until then:

- Keep repository documentation-first.
- Do not install dependencies.
- Do not start Docker.
- Do not create `.env` files.
- Do not read secrets.
