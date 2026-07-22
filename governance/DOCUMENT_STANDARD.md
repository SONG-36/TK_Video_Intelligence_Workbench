# DOCUMENT_STANDARD

## 1. Document Areas

Repository Entry:

- [../README.md](../README.md)
- [../AGENTS.md](../AGENTS.md)
- [../DOCUMENT_MAP.md](../DOCUMENT_MAP.md)

Canonical Product Documents:

- [../docs/00_PRODUCT_SYSTEM_OVERVIEW.md](../docs/00_PRODUCT_SYSTEM_OVERVIEW.md)
- [../docs/01_MVP_WALKING_SKELETON.md](../docs/01_MVP_WALKING_SKELETON.md)
- [../docs/02_DOMAIN_MODEL.md](../docs/02_DOMAIN_MODEL.md)
- [../docs/03_TECHNICAL_ARCHITECTURE.md](../docs/03_TECHNICAL_ARCHITECTURE.md)
- [../docs/04_EVOLUTION_BACKLOG.md](../docs/04_EVOLUTION_BACKLOG.md)
- [../docs/05_EXISTING_SYSTEM_MAPPING.md](../docs/05_EXISTING_SYSTEM_MAPPING.md)

Architecture Decisions:

- [../docs/architecture/ADR_LOG.md](../docs/architecture/ADR_LOG.md)

Working Documents:

- [../docs/working/](../docs/working/)

Historical Documents:

- [../docs/archive/](../docs/archive/)

Governance Tools:

- [../governance/](../governance/)

## 2. Directory Rules

`docs/` is the product documentation root.

Root directory must not contain formal numbered product documents.

Formal numbered documents are limited to:

```text
docs/00_PRODUCT_SYSTEM_OVERVIEW.md
docs/01_MVP_WALKING_SKELETON.md
docs/02_DOMAIN_MODEL.md
docs/03_TECHNICAL_ARCHITECTURE.md
docs/04_EVOLUTION_BACKLOG.md
docs/05_EXISTING_SYSTEM_MAPPING.md
```

Architecture decisions must go into:

```text
docs/architecture/ADR_LOG.md
```

Temporary working documents must go into:

```text
docs/working/
```

Historical documents must go into:

```text
docs/archive/
```

Do not create duplicate product document trees, including separate English/Chinese document trees.

Do not create `docs/product/`, `docs/mvp/`, `docs/domain/`, `docs/technical/`, `docs/evolution/`, or `docs/integration/` for the current six-document set.

## 3. Frontmatter

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

Current rule:

- No formal product or architecture document may set `implementation_allowed` to `true`.
- Any future change that sets `implementation_allowed` to `true` requires explicit human approval and a clear `implementation_scope`.
- Long-term backlog documents never constitute implementation authorization.

## 4. Status Enum

Allowed document status values:

- `DRAFT_FOR_DISCUSSION`
- `DRAFT_FOR_REVIEW`
- `BASELINE_CANDIDATE`
- `BASELINE_APPROVED`
- `SUPERSEDED`
- `ARCHIVED`

Current formal documents are `DRAFT_FOR_REVIEW` until human review completes.

## 5. Authority Rules

- Product position is detailed in the product overview.
- MVP flow is detailed in the Walking Skeleton document.
- Domain objects are detailed in the domain model.
- Technical architecture is detailed in the technical architecture document.
- Long-term capabilities are detailed in the evolution backlog.
- Existing system reuse is detailed in existing system mapping.
- Architecture decisions are recorded in ADR Log.
- Working files do not use formal authority.
- Archive files are not active design authority.
- Git history is the default modification history.

## 6. Change Rules

| Change Type | Update First |
|---|---|
| Product position or role boundary | [../docs/00_PRODUCT_SYSTEM_OVERVIEW.md](../docs/00_PRODUCT_SYSTEM_OVERVIEW.md) |
| Current MVP flow or acceptance | [../docs/01_MVP_WALKING_SKELETON.md](../docs/01_MVP_WALKING_SKELETON.md) |
| Domain object or boundary | [../docs/02_DOMAIN_MODEL.md](../docs/02_DOMAIN_MODEL.md) |
| Technical architecture or adapter boundary | [../docs/03_TECHNICAL_ARCHITECTURE.md](../docs/03_TECHNICAL_ARCHITECTURE.md) |
| Deferred capability | [../docs/04_EVOLUTION_BACKLOG.md](../docs/04_EVOLUTION_BACKLOG.md) |
| Existing system reuse | [../docs/05_EXISTING_SYSTEM_MAPPING.md](../docs/05_EXISTING_SYSTEM_MAPPING.md) |
| Major architecture decision | [../docs/architecture/ADR_LOG.md](../docs/architecture/ADR_LOG.md) |

## 7. Implementation Authorization

Implementation changes are not allowed while formal documents set `implementation_allowed: false`.

Before any future implementation change:

- Human review must approve the relevant MVP boundary.
- A single `docs/working/ACTIVE_ITERATION.md` must exist.
- The active iteration must define implementation scope.
- The active iteration must define allowed file and directory creation.
- The active iteration must define validation commands.

Backlog entries do not authorize code.
