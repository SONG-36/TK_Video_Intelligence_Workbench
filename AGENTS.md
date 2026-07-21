# AGENTS.md

## 1. Current Project State

This is a design-first and documentation-first repository.

Current project constraints:

- `implementation_allowed: false` remains in effect.
- Business code may only be created when a formal Scope or Plan document explicitly enables implementation and has a clear `implementation_scope`.
- Do not create backend, frontend, domain, kernel, skills, agents, workflows, deploy, or similar implementation directories.
- Repository documents are the formal source of truth.

Long-term Roadmap, Business Process, and Evolution Backlog documents do not automatically authorize implementation.

Current allowed implementation scope:

- `RELEASE_1A_MVP_ONLY`, only as defined by [06_RELEASE_1A_MVP_SCOPE.md](06_RELEASE_1A_MVP_SCOPE.md) and [07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md).

Detailed document rules live in [governance/DOCUMENT_STANDARD.md](governance/DOCUMENT_STANDARD.md).

## 2. Canonical Documents

Canonical documents, in authority order:

1. [00_MASTER_DESIGN.md](00_MASTER_DESIGN.md)
2. [01_CAPABILITY_ROADMAP.md](01_CAPABILITY_ROADMAP.md)
3. [02_DELIVERY_RELEASES.md](02_DELIVERY_RELEASES.md)
4. [03_RELEASE_1_SCOPE_AND_BOUNDARIES.md](03_RELEASE_1_SCOPE_AND_BOUNDARIES.md)
5. [04_RELEASE_1_BUSINESS_PROCESS.md](04_RELEASE_1_BUSINESS_PROCESS.md)
6. [05_RELEASE_1_VERTICAL_SLICES.md](05_RELEASE_1_VERTICAL_SLICES.md)
7. [06_RELEASE_1A_MVP_SCOPE.md](06_RELEASE_1A_MVP_SCOPE.md)
8. [07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md)
9. [08_LONG_TERM_EVOLUTION_BACKLOG.md](08_LONG_TERM_EVOLUTION_BACKLOG.md)
10. [architecture/01_PLATFORM_ARCHITECTURE.md](architecture/01_PLATFORM_ARCHITECTURE.md)
11. [architecture/02_ARCHITECTURE_DECISIONS.md](architecture/02_ARCHITECTURE_DECISIONS.md)

Files under `archive/` are not current authority sources.
Files under `working/` are not formal baselines.
When formal documents conflict with archived files, formal documents win.

## 3. Required Reading Before Changes

Before modifying documents, read:

- [AGENTS.md](AGENTS.md)
- [DOCUMENT_MAP.md](DOCUMENT_MAP.md)
- [00_MASTER_DESIGN.md](00_MASTER_DESIGN.md)
- The directly affected files
- [architecture/02_ARCHITECTURE_DECISIONS.md](architecture/02_ARCHITECTURE_DECISIONS.md)

Before implementation work, also read [06_RELEASE_1A_MVP_SCOPE.md](06_RELEASE_1A_MVP_SCOPE.md) and [07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md).

## 4. Incremental Editing Rules

- Make incremental edits only.
- Do not rewrite the document system because of a local decision.
- Do not delete OPEN QUESTIONS.
- Do not write inferred fields as frozen schemas.
- Do not modify documents without practical impact.
- When changing upper-level principles, check lower-level consistency.
- When changing lower-level design, do not bypass upper-level boundaries.
- Do not change Platform Kernel five-mechanism boundaries unless the kernel itself has materially changed.

## 5. Markdown and Mermaid Rules

- Each formal design document must have exactly one H1.
- Sections must start at H2 after the document H1.
- Keep Mermaid diagrams single-topic.
- Avoid very wide diagrams, crossing-heavy diagrams, and long node text.
- Mermaid code fences must be closed.
- Do not place unreadable long paragraphs inside Mermaid nodes.
- Prefer relative Markdown links for file references.

## 6. Git Rules

- Do not automatically run `git commit`, `git push`, `git rebase`, or `git reset`.
- Do not overwrite user changes.
- Check `git status` before and after modifications.
- Use `git mv` when moving tracked files.
- On completion, report `git diff --stat` and `git status --short`.

## 7. Completion Report

Every completed task must report:

- Modified files.
- Created files.
- Moved files.
- Reason for each change.
- Files reviewed but not modified.
- Validation commands and results.
- Unresolved issues.
- `git diff --stat`.
- `git status --short`.
