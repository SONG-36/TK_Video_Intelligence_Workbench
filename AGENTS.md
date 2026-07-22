# AGENTS.md

## 1. Current Project State

This is a design-first and documentation-first repository.

Current constraints:

- `implementation_allowed: false` remains in effect across all formal product and architecture documents.
- Business code is not authorized.
- Do not create backend, frontend, deploy, database, domain, kernel, skills, agents, workflows, prompt, knowledge pack, generation, or similar implementation directories unless a future approved `working/ACTIVE_ITERATION.md` explicitly authorizes the task.
- Repository documents are the formal source of truth.
- Working documents are temporary materials and do not become authority sources.
- Archive documents are historical only.

Current state:

- No business code exists.
- No backend exists.
- No frontend exists.
- No database exists.
- No Product Workspace exists.
- No Reference Workspace exists.
- No Creative / Script module exists.
- No Generation module exists.
- No Platform Core code exists.

## 2. Canonical Documents

Formal product and architecture documents are fixed to:

1. [00_PRODUCT_SYSTEM_OVERVIEW.md](00_PRODUCT_SYSTEM_OVERVIEW.md)
2. [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md)
3. [02_DOMAIN_MODEL.md](02_DOMAIN_MODEL.md)
4. [03_TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md)
5. [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md)
6. [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md)
7. [architecture/ADR_LOG.md](architecture/ADR_LOG.md)

Do not create additional formal numbered product or architecture documents without explicit human approval.

## 3. Required Reading Before Changes

Before modifying formal documents, read:

- [AGENTS.md](AGENTS.md)
- [DOCUMENT_MAP.md](DOCUMENT_MAP.md)
- [00_PRODUCT_SYSTEM_OVERVIEW.md](00_PRODUCT_SYSTEM_OVERVIEW.md)
- The directly affected formal document.
- [architecture/ADR_LOG.md](architecture/ADR_LOG.md)

Before any future implementation work, also read:

- [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md)
- [02_DOMAIN_MODEL.md](02_DOMAIN_MODEL.md)
- [03_TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md)
- [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md)
- The approved `working/ACTIVE_ITERATION.md`

If `working/ACTIVE_ITERATION.md` does not exist, business code is not authorized.

## 4. Documentation Growth Rules

1. Formal product and architecture documents are fixed to 00-05 plus `architecture/ADR_LOG.md`.
2. Do not create new formal numbered documents without explicit human approval.
3. Phase, Slice, and Iteration plans belong in `working/ACTIVE_ITERATION.md`.
4. Only one `working/ACTIVE_ITERATION.md` may exist at a time.
5. Working documents do not constitute authority sources.
6. New decisions should update existing authority documents first.
7. Git history is the default historical archive.
8. Do not create code directories because a future capability exists in the backlog.
9. All business code must be authorized by an approved active iteration.

## 5. Incremental Editing Rules

- Make incremental edits only.
- Do not rewrite the document system because of a local decision.
- Do not delete open questions unless the question is resolved by a new authority decision.
- Do not write inferred fields as frozen schemas.
- Do not modify documents without practical impact.
- When changing upper-level principles, check lower-level consistency.
- When changing lower-level design, do not bypass upper-level boundaries.
- Do not turn Platform Core observation dimensions into an implementation requirement.

## 6. Markdown and Mermaid Rules

- Each formal design document must have exactly one H1.
- Sections must start at H2 after the document H1.
- Keep Mermaid diagrams single-topic.
- Avoid very wide diagrams, crossing-heavy diagrams, and long node text.
- Mermaid code fences must be closed.
- Prefer relative Markdown links for file references.

## 7. Git Rules

- Do not automatically run `git commit`, `git push`, `git rebase`, or `git reset`.
- Do not run `git add`.
- Do not overwrite user changes.
- Check `git status` before and after modifications.
- Use `git mv` when moving tracked files.
- Do not modify existing files under `archive/`.
- On completion, report `git diff --stat` and `git status --short`.

## 8. Completion Report

Every completed task must report:

- Modified files.
- Created files.
- Moved files.
- Deleted files.
- Reason for each change.
- Files reviewed but not modified.
- Validation commands and results.
- Unresolved issues.
- `git diff --stat`.
- `git status --short`.
