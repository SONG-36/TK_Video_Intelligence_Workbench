# DOCUMENT_STANDARD

## 1. Frontmatter

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

When implementation is explicitly enabled, the document must include a clear `implementation_scope`.

Current allowed `implementation_scope` values:

- `RELEASE_1A_MVP_ONLY`

Long-term Backlog documents never constitute implementation authorization.

## 2. Status Enum

Allowed status values:

- `DRAFT_FOR_DISCUSSION`
- `DRAFT_FOR_REVIEW`
- `BASELINE_CANDIDATE`
- `BASELINE_APPROVED`
- `SUPERSEDED`
- `ARCHIVED`

## 3. Terminology

- Release = business delivery version.
- Phase = internal design or implementation stage.
- canonical = current formal authority document.
- archive = historical trace, not a current authority source.
- working = temporary draft area.

## 4. Change Rules

### Principle Change

Changes top-level system purpose, design principles, or authority rules.

Check:

- [../00_MASTER_DESIGN.md](../00_MASTER_DESIGN.md)
- [../01_CAPABILITY_ROADMAP.md](../01_CAPABILITY_ROADMAP.md)
- [../architecture/02_ARCHITECTURE_DECISIONS.md](../architecture/02_ARCHITECTURE_DECISIONS.md)

### Boundary Change

Changes what a release includes, excludes, accepts, or outputs.

Check:

- [../02_DELIVERY_RELEASES.md](../02_DELIVERY_RELEASES.md)
- [../03_RELEASE_1_SCOPE_AND_BOUNDARIES.md](../03_RELEASE_1_SCOPE_AND_BOUNDARIES.md)
- [../04_RELEASE_1_BUSINESS_PROCESS.md](../04_RELEASE_1_BUSINESS_PROCESS.md)

### Business Process Change

Changes stages, gates, exits, route changes, or human decision flow.

Check:

- [../03_RELEASE_1_SCOPE_AND_BOUNDARIES.md](../03_RELEASE_1_SCOPE_AND_BOUNDARIES.md)
- [../04_RELEASE_1_BUSINESS_PROCESS.md](../04_RELEASE_1_BUSINESS_PROCESS.md)
- [../05_RELEASE_1_VERTICAL_SLICES.md](../05_RELEASE_1_VERTICAL_SLICES.md)

### Architecture Decision Change

Changes architecture boundaries, accepted ADRs, or Platform Kernel responsibilities.

Check:

- [../00_MASTER_DESIGN.md](../00_MASTER_DESIGN.md)
- [../architecture/01_PLATFORM_ARCHITECTURE.md](../architecture/01_PLATFORM_ARCHITECTURE.md)
- [../architecture/02_ARCHITECTURE_DECISIONS.md](../architecture/02_ARCHITECTURE_DECISIONS.md)

### Implementation Change

Implementation changes are not allowed while `implementation_allowed: false`.

Before any future implementation change, confirm the relevant formal Scope or Plan document has approved implementation and a clear `implementation_scope`.
