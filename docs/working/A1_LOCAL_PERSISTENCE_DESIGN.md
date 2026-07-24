# A1 Local Persistence Design

This is design/documentation only for the Minimum Usable Workspace planning track. It does not authorize implementation. Related planning documents:

- [NEXT_ITERATION_MINIMUM_WORKSPACE.md](NEXT_ITERATION_MINIMUM_WORKSPACE.md)
- [../ux/MINIMUM_WORKSPACE_SCREEN_SPEC.md](../ux/MINIMUM_WORKSPACE_SCREEN_SPEC.md)
- [ACTIVE_ITERATION.md](ACTIVE_ITERATION.md)

## 1. Goal

A1 local persistence should let the owner save and reload one or more WS-0 + WS-1 content projects locally without introducing formal DB/API/frontend implementation.

The goal is not to build the final storage layer. The goal is to make the Minimum Usable Workspace useful enough for repeated owner sessions while preserving the traceable walking skeleton chain.

## 2. Must Preserve

A saved project snapshot must preserve:

- `ContentProject`.
- `ProductVersion`.
- `Evidence`.
- `KnowledgePack`.
- `ManualReference`.
- `CreativeConceptDraft`.
- `ScriptPackDraft`.
- `ReviewDecision`.
- `ProductionPackExport`.
- trace refs across all objects.

The persistence format must preserve these relationships:

- `ContentProject.product_version_id`.
- `Evidence.product_version_id`.
- `ManualReference.project_id`.
- `ManualReference.product_version_id`.
- `CreativeConceptDraft.evidence_refs`.
- `CreativeConceptDraft.manual_reference_refs`.
- `CreativeConceptDraft.knowledge_pack_id`.
- `CreativeConceptDraft.knowledge_pack_version`.
- `ScriptPackDraft.concept_id`.
- `ScriptPackDraft.evidence_refs`.
- `ScriptPackDraft.manual_reference_refs`.
- `ScriptPackDraft.knowledge_pack_id`.
- `ScriptPackDraft.knowledge_pack_version`.
- `ReviewDecision.script_pack_id`.
- `ProductionPackExport.project_id`.
- `ProductionPackExport.product_version_id`.

## 3. Must Avoid

A1 must avoid:

- PostgreSQL.
- SQLAlchemy.
- Alembic.
- FastAPI.
- React.
- Agent Runtime.
- Workflow Engine.
- AI provider.
- RAG.
- TikTok Search.
- generation orchestration.

It must also avoid pretending to be the final database architecture.

## 4. Option A: JSON File Store

### Shape

Use a local directory such as:

```text
.local/workspace/projects/
```

Each content project is saved as one JSON file:

```text
.local/workspace/projects/{project_id}.json
```

The file stores one explicit snapshot:

```text
workspace_schema_version
saved_at
project_snapshot
production_pack_snapshot
```

The snapshot is loaded back into existing in-memory domain/service objects through thin adapter functions.

### Strengths

- Very low implementation weight.
- No new runtime dependency.
- Human inspectable.
- Easy to copy, back up, diff, and attach to reviews.
- Fits the current in-memory walking skeleton.
- Keeps the next iteration from turning into DB/API/platform work.
- Easy to preserve the whole trace chain in one place.
- Works well for one owner and small project counts.

### Weaknesses

- No query language.
- No concurrent write safety beyond simple file locking or atomic writes.
- Manual migration needed if the snapshot schema changes.
- Large JSON files can become awkward if assets or media are added later.
- Requires care to avoid writing partial/corrupt files.

### Fit for A1

JSON file store fits A1 because the immediate owner problem is save/reload, not query, multi-user access, reporting, or relational integrity.

The Minimum Usable Workspace still needs to learn which business context, trace, review, and export fields the owner actually uses. A JSON snapshot keeps that learning visible.

## 5. Option B: SQLite

### Shape

Use one local file:

```text
.local/workspace/tvi-workbench.sqlite3
```

Possible storage models:

- normalized tables for projects, product versions, evidence, references, concepts, scripts, reviews, exports.
- or one table of JSON snapshots with metadata columns.

### Strengths

- More durable local storage engine.
- Supports queries and indexes.
- Better for many projects.
- Better for future filtering, search, and summaries.
- Atomic transactions are built in.
- Still local and does not require PostgreSQL.

### Weaknesses

- Pushes the project toward schema design earlier.
- If normalized too soon, it becomes a premature database model.
- Requires migration strategy once fields evolve.
- Increases cognitive load before the owner workflow is stable.
- Can tempt API and repository abstractions before they are needed.
- Less transparent for manual owner/debug inspection than JSON files.

### Fit for A1

SQLite is a good later local persistence candidate, especially when the workspace needs many projects, list/search/filter views, or robust local history.

It is too strong for the first Minimum Usable Workspace persistence step if implemented as normalized tables. A SQLite JSON snapshot table would be acceptable later, but it still adds a database decision before the UX loop proves stable.

## 6. Comparison

| Criteria | JSON file store | SQLite |
|---|---|---|
| Implementation weight | Lowest | Medium |
| New dependency | None | None for Python stdlib `sqlite3`, but still a DB design |
| Human inspectability | High | Medium |
| Trace snapshot preservation | High | High |
| Query/filter support | Low | High |
| Multi-project list support | Basic directory scan | Strong |
| Migration pressure | Low at first, manual later | Medium immediately |
| Risk of premature architecture | Low | Medium to high |
| Fit with in-memory WS-0 + WS-1 | Strong | Acceptable later |
| Fit with Minimum Usable Workspace A1 | Strong | Too early unless strictly snapshot-only |

## 7. Recommendation

Recommend JSON file store for A1.

Reason:

The next thin implementation should prove that the owner can save, reload, inspect, and continue one or more content projects locally. A JSON file store solves that exact problem while keeping the system close to the verified in-memory walking skeleton.

SQLite should be deferred until the workspace has a real need for:

- search across many projects.
- filtering by review status.
- summaries across products.
- local history.
- transaction-heavy updates.
- multiple workspace views over the same saved data.

## 8. Recommended A1 Scope

A1 should implement only:

- save current workspace snapshot to local JSON.
- list saved project snapshots from a local directory.
- load one saved project snapshot.
- validate loaded snapshot trace consistency before use.
- preserve Markdown and JSON-compatible `ProductionPackExport` in the snapshot.
- show save/load status in the dev/minimum workspace.

A1 should not implement:

- normalized database schema.
- repository layer.
- SQL migrations.
- API.
- formal frontend.
- user accounts.
- cloud sync.
- asset/media storage.
- automatic version history beyond a single saved snapshot file.

## 9. Snapshot Boundary

Recommended snapshot top-level structure:

```text
workspace_schema_version
saved_at
project_id
product_version_id
status
content_project
operating_context
product
product_version
evidence
knowledge_pack
manual_references
creative_concept_drafts
selected_concept
script_pack
review_decision
production_pack_export
trace_summary
```

The snapshot should be explicit and redundant enough for owner debugging. Trace refs should be preserved both inside objects and in `trace_summary`.

## 10. Validation Rules Before Save

Before save:

- `ContentProject.product_version_id` must match `ProductVersion.id`.
- every `Evidence.product_version_id` must match `ProductVersion.id`.
- `KnowledgePack.version` must be `v0.1` for the current skeleton.
- `ManualReference` count must be 3-5.
- every `ManualReference.project_id` must match `ContentProject.id`.
- every `ManualReference.product_version_id` must match `ProductVersion.id`.
- selected concept must remain `draft`.
- selected concept evidence/reference/knowledge refs must match prepared inputs.
- `ScriptPackDraft.status` must remain `draft`.
- `ReviewDecision.script_pack_id` must match `ScriptPackDraft.id`.
- `ProductionPackExport` must preserve project/product version ids and readiness status.

## 11. Validation Rules After Load

After load:

- reject snapshots with missing `workspace_schema_version`.
- reject snapshots with missing required domain sections.
- reject snapshots where trace refs do not match.
- show a readable validation error instead of silently repairing data.
- keep system IDs hidden by default in UI but available in debug trace.

## 12. Implementation Review Checklist

Before implementation is approved, review:

- Is this still local file persistence, not a formal database?
- Does it preserve all trace refs?
- Can the owner copy and inspect the saved project file?
- Does loading a file recreate or validate the in-memory chain?
- Are save/load actions task-oriented in the workspace UI?
- Does the implementation avoid FastAPI, DB schema, React, AI provider, RAG, TikTok Search, Agent Runtime, Workflow Engine, and generation orchestration?

## 13. Decision

A1 decision:

```text
Use JSON file store for the next thin implementation.
Defer SQLite until multi-project querying, filtering, history, or reporting becomes a real owner workflow need.
```

This decision is a planning recommendation only. It does not authorize implementation without a later explicit human instruction.
