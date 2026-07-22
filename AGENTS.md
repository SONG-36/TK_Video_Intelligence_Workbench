# AGENTS.md

## 1. Current Project State

This is a design-first and documentation-first repository.

Current constraints:

- `implementation_allowed: false` remains in effect across all formal product and architecture documents.
- Business code is not authorized.
- Do not create backend, frontend, deploy, database, domain, kernel, skills, agents, workflows, prompt, knowledge pack, generation, or similar implementation directories unless a future approved `docs/working/ACTIVE_ITERATION.md` explicitly authorizes the task.
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

1. [docs/00_PRODUCT_SYSTEM_OVERVIEW.md](docs/00_PRODUCT_SYSTEM_OVERVIEW.md)
2. [docs/01_MVP_WALKING_SKELETON.md](docs/01_MVP_WALKING_SKELETON.md)
3. [docs/02_DOMAIN_MODEL.md](docs/02_DOMAIN_MODEL.md)
4. [docs/03_TECHNICAL_ARCHITECTURE.md](docs/03_TECHNICAL_ARCHITECTURE.md)
5. [docs/04_EVOLUTION_BACKLOG.md](docs/04_EVOLUTION_BACKLOG.md)
6. [docs/05_EXISTING_SYSTEM_MAPPING.md](docs/05_EXISTING_SYSTEM_MAPPING.md)
7. [docs/architecture/ADR_LOG.md](docs/architecture/ADR_LOG.md)

Do not create additional formal numbered product or architecture documents without explicit human approval.

Do not create `docs/product/`, `docs/mvp/`, `docs/domain/`, `docs/technical/`, `docs/evolution/`, or `docs/integration/` for the current six-document set.

## 3. Required Reading Before Changes

Before modifying formal documents, read:

- [AGENTS.md](AGENTS.md)
- [DOCUMENT_MAP.md](DOCUMENT_MAP.md)
- [docs/00_PRODUCT_SYSTEM_OVERVIEW.md](docs/00_PRODUCT_SYSTEM_OVERVIEW.md)
- The directly affected formal document.
- [docs/architecture/ADR_LOG.md](docs/architecture/ADR_LOG.md)

Before any future implementation work, also read:

- [docs/01_MVP_WALKING_SKELETON.md](docs/01_MVP_WALKING_SKELETON.md)
- [docs/02_DOMAIN_MODEL.md](docs/02_DOMAIN_MODEL.md)
- [docs/03_TECHNICAL_ARCHITECTURE.md](docs/03_TECHNICAL_ARCHITECTURE.md)
- [docs/05_EXISTING_SYSTEM_MAPPING.md](docs/05_EXISTING_SYSTEM_MAPPING.md)
- The approved `docs/working/ACTIVE_ITERATION.md`

If `docs/working/ACTIVE_ITERATION.md` does not exist, business code is not authorized.

## 4. Documentation Growth Rules

1. Formal product and architecture documents are fixed to `docs/00`-`docs/05` plus `docs/architecture/ADR_LOG.md`.
2. Do not create new formal numbered documents without explicit human approval.
3. Do not create formal numbered product documents in the repository root.
4. Phase, Slice, and Iteration plans belong in `docs/working/ACTIVE_ITERATION.md`.
5. Only one `docs/working/ACTIVE_ITERATION.md` may exist at a time.
6. Working documents do not constitute authority sources.
7. New decisions should update existing authority documents first.
8. Git history is the default historical archive.
9. Historical documents belong in `docs/archive/`.
10. Do not create code directories because a future capability exists in the backlog.
11. All business code must be authorized by an approved active iteration.

## 5. Root Directory Rules

The repository root keeps only:

- Repository entry documents: `README.md`, `AGENTS.md`, `DOCUMENT_MAP.md`.
- Runtime configuration such as `.nvmrc`, `.python-version`, `.gitignore`, and `.obsidian/`.
- Governance tooling under `governance/`.

Do not recreate root-level `architecture/`, `working/`, or `archive/` directories.

Do not create new root-level numbered product documents.

## 6. Incremental Editing Rules

- Make incremental edits only.
- Do not rewrite the document system because of a local decision.
- Do not delete open questions unless the question is resolved by a new authority decision.
- Do not write inferred fields as frozen schemas.
- Do not modify documents without practical impact.
- When changing upper-level principles, check lower-level consistency.
- When changing lower-level design, do not bypass upper-level boundaries.
- Do not turn Platform Core observation dimensions into an implementation requirement.

## 7. Markdown and Mermaid Rules

- Each formal design document must have exactly one H1.
- Sections must start at H2 after the document H1.
- Keep Mermaid diagrams single-topic.
- Avoid very wide diagrams, crossing-heavy diagrams, and long node text.
- Mermaid code fences must be closed.
- Prefer relative Markdown links for file references.

## 8. Git Rules

- Do not automatically run `git commit`, `git push`, `git rebase`, or `git reset`.
- Do not run `git add`.
- Do not overwrite user changes.
- Check `git status` before and after modifications.
- Use `git mv` when moving tracked files.
- Do not modify existing files under `docs/archive/`.
- On completion, report `git diff --stat` and `git status --short`.

## 9. Completion Report

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
