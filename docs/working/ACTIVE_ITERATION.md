---
document_type: active_iteration
project: "TikTok Video Intelligence Workbench"
iteration_status: ACTIVE
created_at: 2026-07-22
scope_authority: "../01_MVP_WALKING_SKELETON.md"
---

# Active Iteration

## 1. Iteration Name

WS-0 + WS-1 Car Vacuum Cleaner Production-intent Walking Skeleton.

中文名称：

```text
车载吸尘器 WS-0 + WS-1 薄端到端 Walking Skeleton
```

## 2. Approval Basis

This iteration is based on the human-approved baseline:

- [../01_MVP_WALKING_SKELETON.md](../01_MVP_WALKING_SKELETON.md)
- status: `BASELINE_APPROVED`
- approval scope: WS-0 + WS-1 only, using the car vacuum cleaner pilot.

Supporting authority documents:

- [../00_PRODUCT_SYSTEM_OVERVIEW.md](../00_PRODUCT_SYSTEM_OVERVIEW.md)
- [../02_DOMAIN_MODEL.md](../02_DOMAIN_MODEL.md)
- [../03_TECHNICAL_ARCHITECTURE.md](../03_TECHNICAL_ARCHITECTURE.md)
- [../04_EVOLUTION_BACKLOG.md](../04_EVOLUTION_BACKLOG.md)
- [../05_EXISTING_SYSTEM_MAPPING.md](../05_EXISTING_SYSTEM_MAPPING.md)
- [../architecture/ADR_LOG.md](../architecture/ADR_LOG.md)

Formal documents still keep `implementation_allowed: false`. This working file defines the bounded execution contract for the first approved iteration. This file does not by itself authorize implementation. Each coding step still requires a separate human instruction. Any concrete coding step must stay inside this file and still follow explicit human instructions for that step.

## 3. Scope: WS-0 + WS-1 Only

This iteration covers one thin, real, end-to-end business chain:

```text
Create ContentProject
-> enter Selection-to-Content Handoff
-> bind Product / ProductVersion Lite
-> add Evidence Lite
-> use real Knowledge Pack v0.1
-> manually add 3-5 References
-> generate 3 CreativeConcept Drafts
-> human selects or edits one Concept
-> generate ScriptPack Draft
-> human review
-> export Markdown / JSON
-> form Generation-ready Owned Content Production Pack
```

WS-0 deliverables:

- ContentProject.
- Selection-to-Content Handoff.
- Product Lite.
- ProductVersion Lite.
- Evidence Lite.

WS-1 deliverables:

- Knowledge Pack Version.
- Manual Reference.
- CreativeConcept Draft.
- ScriptPack Draft.
- Review.
- Markdown / JSON Export.

The iteration is not complete if it only implements Product / Evidence CRUD without producing a reviewed, exportable Production Pack.

## 4. Pilot Product

Pilot product:

```text
Car vacuum cleaner
车载吸尘器
```

The pilot must use realistic business input for target market, platform, content objective, handoff rationale, Evidence, Knowledge Pack v0.1, and 3-5 manually entered References.

The default ScriptPack output language for the pilot is English unless a later human decision changes it.

## 5. Allowed Deliverables

This iteration may produce only the minimum artifacts needed to validate the approved WS-0 + WS-1 chain:

- A single car vacuum cleaner ContentProject.
- One Selection-to-Content Handoff snapshot for that project.
- One Product Lite identity.
- At least one ProductVersion Lite identity.
- Evidence Lite records bound to the ProductVersion Lite.
- A real versioned Knowledge Pack v0.1 input.
- 3-5 manually entered References.
- 3 AI-generated CreativeConcept Drafts.
- One human-selected or human-edited CreativeConcept.
- One ScriptPack Draft based on the selected Concept.
- Human Review records for the selected Concept and final ScriptPack.
- One Markdown export for human production handoff.
- One JSON export for system handoff.
- Tests, fixtures, seed data, or validation helpers only when a later coding task explicitly authorizes implementation work inside this iteration.

Allowed implementation work in later coding tasks must be the thinnest practical slice needed for this chain. It must not define final database schemas, final API route contracts, or final UI design systems.

## 6. Explicitly Excluded Items

This iteration must not implement or design in detail:

- Complete selection platform.
- Product opportunity discovery.
- Portfolio, Priority, or Experiment platform.
- Full Product Knowledge platform.
- Full Knowledge Base UI, search, tags, approval workflow, or recommendation system.
- Automatic TikTok Search.
- Video breakdown or reference media processing.
- Gate Engine.
- Workflow Engine.
- Agent Runtime or Agent OS.
- Platform Kernel or Platform Core implementation.
- Microservices or Kubernetes.
- GenerationPlan.
- RenderBatch.
- RenderJob.
- Worker or queue.
- Provider routing or automatic batch costing.
- ComfyUI, Seedance, Kling, or any generation orchestration inside the main system.
- External live API integration unless a future active iteration explicitly authorizes it.
- Direct copying of code from sibling repositories.

ComfyUI, Seedance, Kling, and similar generation experiments remain Parallel Lab work. The main system only exports a Generation-ready Owned Content Production Pack.

## 7. Human Review Checkpoints

Human review is required at these points:

1. Handoff readiness review: confirm the ContentProject has enough business context to start content work.
2. ProductVersion / Evidence review: confirm every Evidence record applies to the selected ProductVersion Lite.
3. Reference readiness review: confirm 3-5 manual References are relevant and traceable.
4. Concept selection review: compare 3 CreativeConcept Drafts and select or edit one Concept.
5. ScriptPack review: approve, request rework, hold, or stop the generated ScriptPack.
6. Export readiness review: confirm the Markdown and JSON exports preserve Evidence, Reference, Knowledge Pack version, AI Draft status, and final human decision.

AI may suggest content, but AI cannot approve business output. AI outputs are Draft until a human review decision approves them.

Allowed review decisions for this iteration. These are the canonical status values for this iteration:

```text
draft
approved
rework
hold
stopped
```

## 8. Minimum Data Objects

This iteration works with these minimum business objects only:

| Object | Minimum responsibility in this iteration |
|---|---|
| `ContentProject` | Work container for one car vacuum cleaner content decision chain. |
| `OperatingContextSnapshot` | Selection-to-Content Handoff and target operating context. |
| `Product` | Stable product identity. |
| `ProductVersion` | Lite version identity used to scope Evidence. |
| `Evidence` | Source material bound to ProductVersion Lite. |
| `KnowledgePack` | Versioned Knowledge Pack v0.1 input used by AI runs. |
| `Reference` | Manual entry reference with source, relevance, and usage trace. |
| `CreativeConcept` | AI Draft or human-edited concept candidate. |
| `ScriptPack` | Draft or reviewed production pack content. |
| `Review` | Human decision record. |
| `Run` | AI or automated processing trace. |

Mandatory object rules:

- Evidence must bind to ProductVersion Lite, not directly to Product.
- Evidence is source material, not automatically confirmed Fact.
- Manual Reference is the only Reference source in this iteration.
- Knowledge Pack v0.1 must exist as a real versioned input.
- Every AI Run that uses the Knowledge Pack must record the Knowledge Pack version.
- CreativeConcept and ScriptPack generated by AI default to Draft.
- Approved content must not be silently overwritten.

This section defines business object responsibilities only. It does not freeze database fields, database tables, API route names, UI layout, or prompt file structure.

## 9. Expected Markdown / JSON Export Contract

The export target is:

```text
Generation-ready Owned Content Production Pack
```

Markdown export purpose:

- Human-readable handoff for shooting or future generation work.
- Must show the selected Concept, approved ScriptPack, storyboard, shot list, generation notes, risk notes, Evidence references, Reference references, Knowledge Pack version, and review status.

JSON export purpose:

- System-readable handoff for future tools.
- Must preserve stable identifiers or traceable references for the project, product version, Evidence, References, selected Concept, ScriptPack, Knowledge Pack version, AI runs, and human review decision.

Minimum export content:

- Product context.
- Selection-to-Content Handoff summary.
- ProductVersion Lite reference.
- Evidence references.
- Knowledge Pack version.
- Manual Reference references.
- 3 CreativeConcept Draft summaries.
- Selected or human-edited Concept.
- Script.
- Storyboard.
- Shot list.
- Shot duration or timing notes.
- Aspect ratio.
- Visual requirements.
- Asset requirements.
- Recommended production mode.
- Generation notes.
- Risk notes.
- Review status and reviewer note.

This is an export contract for the current iteration, not a final schema.

## 10. Acceptance Criteria

The iteration is accepted only when all of the following are true:

- A car vacuum cleaner ContentProject can be created from a Selection-to-Content Handoff.
- The project is linked to Product Lite and ProductVersion Lite.
- Evidence Lite exists and every Evidence item is scoped to ProductVersion Lite.
- Knowledge Pack v0.1 exists as a versioned input and is referenced by AI runs.
- 3-5 References are manually entered and traceable.
- The system produces 3 CreativeConcept Drafts.
- A human can select or edit one Concept.
- The system produces a ScriptPack Draft for the selected Concept.
- A human can approve, request rework, hold, or stop the ScriptPack.
- Markdown export can be produced for human handoff.
- JSON export can be produced for system handoff.
- Exports preserve Evidence references, Reference references, Knowledge Pack version, AI Draft status, and final human review status.
- No excluded future capability is implemented as part of the main system.
- Documentation checks pass.
- Any implementation tests authorized by later coding steps pass or have explicit unresolved notes.

## 11. Allowed Commands

Allowed commands for this document-only preparation step:

```text
git status --short
find docs -maxdepth 3 -type f | sort
python3 governance/checks/check_docs.py
git diff -- docs/working/ACTIVE_ITERATION.md
```

Allowed commands for later coding tasks under this iteration must be stated in the task before execution. Typical allowed validation may include scoped backend, frontend, export, or documentation checks after the relevant files exist.

No install, Docker, external API call, git add, commit, or push is allowed unless a later human instruction explicitly authorizes it.

## 12. Forbidden Actions

During this iteration, do not:

- Modify formal documents unless a separate human instruction explicitly authorizes that change.
- Create additional formal numbered documents.
- Create another active iteration file.
- Treat backlog entries as implementation authorization.
- Implement complete platform abstractions before repeated real business use proves the need.
- Add final database schemas.
- Add final API route contracts.
- Add final UI designs.
- Add a coding prompt inside this document.
- Read `.env` files or secrets.
- Install dependencies without explicit approval.
- Start Docker without explicit approval.
- Run live external APIs without explicit approval.
- Run `git add`, `git commit`, `git push`, `git rebase`, `git reset`, or destructive git operations without explicit approval.

## 13. Completion Report Format

Every execution task under this iteration must report:

- Task objective.
- Files read.
- Files created.
- Files modified.
- Files intentionally not modified.
- Commands run.
- Validation results.
- Whether business code was written.
- Whether dependencies were installed.
- Whether Docker was started.
- Whether git add, commit, or push was run.
- Scope compliance check.
- Remaining open questions or unresolved risks.
- `git diff --stat`.
- `git status --short`.

Scope compliance must explicitly answer:

```text
Did this task stay within WS-0 + WS-1 car vacuum cleaner Walking Skeleton?
Did this task avoid Platform Kernel, Gate Engine, Agent Runtime, Workflow Engine, TikTok Search, full Knowledge Platform, and Generation Orchestration?
```

## 14. Iteration Task Ledger and Owner Review Rules

This ledger tracks coding steps under this active iteration.

It is not a backlog expansion mechanism.

New steps must stay within WS-0 + WS-1 car vacuum cleaner Walking Skeleton.

Each coding step still requires a separate human instruction before execution.

| Step | Status | Goal | Allowed Scope | Validation | Owner Review Focus | Notes |
|---|---|---|---|---|---|---|
| Step 0 | VERIFIED_WITH_LOCAL_PY312_ENV | Establish minimum backend foundation covering WS-0 domain objects and validation tests. WS-0 backend foundation has been implemented. | Backend foundation only for ContentProject, OperatingContextSnapshot, Product Lite, ProductVersion Lite, and Evidence Lite. Business-core files: `backend/tvi_workbench/ws0/domain.py`, `tests/ws0/test_domain.py`. Engineering-boilerplate / config files: `.gitignore`, `pyproject.toml`, `backend/tvi_workbench/__init__.py`, `backend/tvi_workbench/ws0/__init__.py`. | Python 3.12 local venv pytest passed: `4 passed`. Docs check passed: `PASS 66 / WARNING 9 / FAIL 0`. | Domain semantics, ProductVersion Lite boundary, Evidence binding, validation rules, and tests. | Step 0 did not implement FastAPI, DB, frontend, WS-1, AI, or export. |
| Step 1 | VERIFIED_WITH_LOCAL_PY312_ENV | Establish WS-0 thin service interface. Service/interface has been implemented with `create_project_from_handoff(...)`. | Thin in-memory service interface for creating and inspecting WS-0 project context only. Business-core files: `backend/tvi_workbench/ws0/service.py`, `tests/ws0/test_service.py`, `backend/tvi_workbench/ws0/domain.py`. Engineering-boilerplate files: `backend/tvi_workbench/ws0/__init__.py`. | Python 3.12 local venv pytest passed: `9 passed`. Docs check to be recorded by this task report. | Service preserves handoff context, ProductVersion Lite, Evidence scope, traceable IDs, and reviewable validation errors. | Step 1 enforces that a WS-0 project requires at least one Evidence Lite item. Step 1 did not implement FastAPI, DB, frontend, WS-1, AI, or export. |
| Step 2 | VERIFIED_WITH_LOCAL_PY312_ENV | Add Knowledge Pack v0.1 and Manual Reference input boundaries. Knowledge Pack v0.1 + Manual Reference input boundary has been implemented with `prepare_ws1_inputs(...)`. | WS-1 begins with versioned Knowledge Pack input and manual Reference entry. Business-core files: `backend/tvi_workbench/ws1/domain.py`, `backend/tvi_workbench/ws1/service.py`, `tests/ws1/test_input_preparation.py`. Engineering-boilerplate files: `backend/tvi_workbench/ws1/__init__.py`. | Python 3.12 local venv pytest passed: `18 passed`. 3-5 manual references rule implemented. Traceability mismatch tests for project_id and product_version_id are covered. Docs check to be recorded by this task report. | Knowledge Pack version recording, manual Reference traceability, project/ProductVersion binding, prepared-not-approved status, and no full knowledge platform. | Step 2 did not implement CreativeConcept, ScriptPack, Export, AI, FastAPI, DB, frontend, TikTok Search, or full Knowledge Base platform. |
| Step 2.5 | READY_FOR_OWNER_VISUAL_SMOKE_TEST | Add visual real input smoke harness for WS-0 -> WS-1 input preparation. UX has been refined into owner-friendly business flow sections. | Local Streamlit dev harness only: `tools/dev_harness/ws_pilot_input_app.py`. This is not formal frontend, API, DB, or product UI. | Python 3.12 local venv pytest and docs check to be recorded by this task report. Streamlit installed only in local venv. | Owner can manually enter car vacuum cleaner WS-0 and WS-1 inputs and inspect project/ProductVersion/Evidence/KnowledgePack/Reference traceability. System IDs, Knowledge Pack version, manual intake, and prepared status are generated/fixed instead of primary owner inputs. | Step 2.5 did not implement AI, Concept, ScriptPack, Export, FastAPI, DB, formal frontend, TikTok Search, or full Knowledge Base platform. |
| Step 3 | NOT_STARTED | Generate 3 CreativeConcept Drafts and allow human selection or editing of one. | Concept Draft generation and human selection/edit boundary only. | Tests or fixtures proving three Drafts, traceable inputs, and selected Concept state. | AI Draft status, Evidence and Reference citations, and human selection semantics. | No Agent Runtime or Workflow Engine. |
| Step 4 | NOT_STARTED | Generate ScriptPack Draft, Human Review, Markdown export, and JSON export. | ScriptPack Draft, Review decision, and export contract for the pilot Production Pack. | Export validation for Markdown and JSON plus review status checks. | Human approval boundary, export traceability, risk notes, and final review status. | No GenerationPlan, RenderBatch, RenderJob, ComfyUI, or Seedance. |

Owner Review Rules:

- Owner must deeply review business semantics, domain rules, schemas, validation, tests, and export traceability.
- Owner does not need to understand every line of engineering boilerplate before allowing the next step.
- Core business rules requiring owner review:
  - Evidence must bind to ProductVersion Lite.
  - Evidence is source material, not automatically confirmed Fact.
  - AI outputs default to Draft.
  - Human Review is required before approval.
  - Manual Reference must remain traceable.
  - Knowledge Pack version must be recorded by AI runs.
  - Export must preserve Evidence, Reference, Knowledge Pack version, AI Draft status, and final review status.
- Each coding step report must identify:
  - Business-core files requiring owner review.
  - Engineering-boilerplate files that only need sanity review.
  - Tests that protect core business rules.
  - Known unimplemented rules.
