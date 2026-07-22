# DOCUMENT_STANDARD

## 1. Formal Document Set

Formal numbered product and architecture documents are limited to:

- [../00_PRODUCT_SYSTEM_OVERVIEW.md](../00_PRODUCT_SYSTEM_OVERVIEW.md)
- [../01_MVP_WALKING_SKELETON.md](../01_MVP_WALKING_SKELETON.md)
- [../02_DOMAIN_MODEL.md](../02_DOMAIN_MODEL.md)
- [../03_TECHNICAL_ARCHITECTURE.md](../03_TECHNICAL_ARCHITECTURE.md)
- [../04_EVOLUTION_BACKLOG.md](../04_EVOLUTION_BACKLOG.md)
- [../05_EXISTING_SYSTEM_MAPPING.md](../05_EXISTING_SYSTEM_MAPPING.md)
- [../architecture/ADR_LOG.md](../architecture/ADR_LOG.md)

Do not create duplicate Scope, Phase, Slice, Plan, or Roadmap documents as new formal numbered documents.

## 2. Frontmatter

Formal design documents need these frontmatter fields:

- `document_type`
- `project`
- `baseline_version`
- `status`
- `implementation_allowed`
- `authority`
- `last_updated`
- `change_policy`

Optional fields:

- `depends_on`
- `supersedes`
- `canonical`
- `implementation_scope`

Current post-consolidation rule:

- No formal product or architecture document may set `implementation_allowed` to `true`.
- Any future change that sets `implementation_allowed` to `true` requires explicit human approval and a clear `implementation_scope`.
- Long-term backlog documents never constitute implementation authorization.

## 3. Status Enum

Allowed document status values:

- `DRAFT_FOR_DISCUSSION`
- `DRAFT_FOR_REVIEW`
- `BASELINE_CANDIDATE`
- `BASELINE_APPROVED`
- `SUPERSEDED`
- `ARCHIVED`

Current formal documents are `DRAFT_FOR_REVIEW` until human review completes.

## 4. Authority Rules

- Product position is detailed in the product overview.
- MVP flow is detailed in the Walking Skeleton document.
- Domain objects are detailed in the domain model.
- Technical architecture is detailed in the technical architecture document.
- Long-term capabilities are detailed in the evolution backlog.
- Existing system reuse is detailed in existing system mapping.
- Architecture decisions are recorded in ADR Log.
- Working files do not use formal authority.
- Git history is the default document history.

## 5. Change Rules

| Change Type | Update First |
|---|---|
| Product position or role boundary | [../00_PRODUCT_SYSTEM_OVERVIEW.md](../00_PRODUCT_SYSTEM_OVERVIEW.md) |
| Current MVP flow or acceptance | [../01_MVP_WALKING_SKELETON.md](../01_MVP_WALKING_SKELETON.md) |
| Domain object or boundary | [../02_DOMAIN_MODEL.md](../02_DOMAIN_MODEL.md) |
| Technical architecture or adapter boundary | [../03_TECHNICAL_ARCHITECTURE.md](../03_TECHNICAL_ARCHITECTURE.md) |
| Deferred capability | [../04_EVOLUTION_BACKLOG.md](../04_EVOLUTION_BACKLOG.md) |
| Existing system reuse | [../05_EXISTING_SYSTEM_MAPPING.md](../05_EXISTING_SYSTEM_MAPPING.md) |
| Major architecture decision | [../architecture/ADR_LOG.md](../architecture/ADR_LOG.md) |

## 6. Implementation Authorization

Implementation changes are not allowed while formal documents set `implementation_allowed: false`.

Before any future implementation change:

- Human review must approve the relevant MVP boundary.
- A single `working/ACTIVE_ITERATION.md` must exist.
- The active iteration must define implementation scope.
- The active iteration must define allowed file and directory creation.
- The active iteration must define validation commands.

Backlog entries do not authorize code.
