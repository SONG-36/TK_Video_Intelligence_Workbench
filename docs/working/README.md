# Working Area

This directory is for temporary planning, audits, and iteration materials.

Working files are not formal product authority sources.

Current working directory:

```text
docs/working/
```

Retained file:

- `docs/working/CURRENT_IMPLEMENTATION_AUDIT.md` records the current repository implementation fact baseline.

Future active coding work:

- Create `docs/working/ACTIVE_ITERATION.md` only when coding is approved.
- Only one active iteration file may exist at a time.
- `docs/working/ACTIVE_ITERATION.md` must define the current coding task, implementation scope, files allowed to be created, and validation requirements.
- After an iteration completes, conclusions should be merged back into `docs/00`-`docs/05` or `docs/architecture/ADR_LOG.md`.
- The working file should then be removed or archived according to human instruction.

Do not recreate `working/` at the repository root.

Do not use working files to bypass the authority of `docs/00`-`docs/05` plus `docs/architecture/ADR_LOG.md`.
