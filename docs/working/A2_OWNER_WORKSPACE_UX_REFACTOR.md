# A2 Owner Workspace UX Refactor

This is a design/planning document for the Minimum Usable Workspace. It does not authorize implementation.

Related documents:

- [NEXT_ITERATION_MINIMUM_WORKSPACE.md](NEXT_ITERATION_MINIMUM_WORKSPACE.md)
- [A1_LOCAL_PERSISTENCE_DESIGN.md](A1_LOCAL_PERSISTENCE_DESIGN.md)
- [../ux/MINIMUM_WORKSPACE_SCREEN_SPEC.md](../ux/MINIMUM_WORKSPACE_SCREEN_SPEC.md)
- [ACTIVE_ITERATION.md](ACTIVE_ITERATION.md)

## 1. Intent

A2 should refactor the local Streamlit workspace experience so the owner can operate the verified WS-0 + WS-1 walking skeleton as a practical manual content workspace.

This remains a local Minimum Workspace. It is not a formal frontend, not a React product UI, not an API-backed application, and not a database implementation.

The purpose is to improve the owner workflow before any broader frontend or persistence architecture is approved.

## 2. Current Baseline

Current implemented capability:

- WS-0 project creation from product and handoff context.
- ProductVersion-scoped Evidence.
- KnowledgePack v0.1 input.
- 3-5 ManualReferences.
- CreativeConceptDraft generation, manual creation, selection, and optional human edit.
- ScriptPackDraft generation.
- ReviewDecision.
- Markdown and JSON-compatible ProductionPackExport.
- JSON Snapshot Store save/list/load for local inspection.

Current limitation:

The Streamlit harness works technically, but it still feels like a developer smoke harness rather than a natural owner workspace.

## 3. Owner Feedback To Preserve

Owner manual review found:

- The page still feels like fields are spread out.
- English backend terms hurt usability.
- Evidence Lite needs manual add/remove card behavior.
- Many details still feel developer-oriented.

These are UX problems, not backend domain problems. A2 should improve the owner-facing workflow without changing WS-0 or WS-1 business rules.

## 4. Chinese-First Business Labels

The primary UI should use Chinese business language. Backend object names may remain available in debug panels, docs, and code, but they should not dominate the owner workflow.

Recommended label mapping:

| Backend / formal term | Owner-facing Chinese label |
|---|---|
| Evidence Lite | 产品证据 / 卖点依据 |
| ManualReference | 参考视频 / 参考素材 |
| ProductVersion | 当前样品 / 当前版本 |
| CreativeConceptDraft | 创意方向草稿 |
| ScriptPackDraft | 剧本包草稿 |
| ReviewDecision | 人工审核结果 |
| ProductionPackExport | 生产交接包 |

Chinese labels should be the first visible labels. English backend terms should appear only where they help traceability or implementation review.

## 5. Target Page Structure

A2 should reshape the local workspace into these owner-facing areas:

1. 项目输入
2. 产品证据
3. 参考视频
4. 创意方向
5. 剧本草稿
6. 审核
7. 生产包
8. 保存 / 加载

The order should follow the actual work sequence. The owner should not need to understand backend object dependencies to know what to do next.

## 6. Information Hierarchy

Primary UI:

- Chinese business labels.
- Business intent and current task.
- Human-editable content inputs.
- Clear next action and blocked reason.
- Markdown production handoff preview.

Hidden by default:

- system-generated IDs.
- backend object names.
- raw dataclass structure.
- trace arrays.
- JSON payload.

Available in collapsible panels:

- `ContentProject.id`.
- `ProductVersion.id`.
- Evidence refs.
- ManualReference refs.
- KnowledgePack id/version.
- selected concept id and generation method.
- ScriptPackDraft id.
- ReviewDecision trace.
- JSON-compatible ProductionPackExport.

Trace should remain accessible, but it should not be the main page experience.

## 7. Evidence Card Interaction

Evidence Lite should become 产品证据 / 卖点依据 cards.

Required card behavior:

- add evidence.
- remove evidence.
- preserve at least one valid Evidence item before continuing.
- backend `product_version_id` is generated/bound automatically and hidden by default.
- show validation errors in business language.

Card fields:

- title.
- type.
- summary.
- supported claim.
- source.
- risk note.

Field intent:

- `title`: short human label for the evidence.
- `type`: supplier claim, owner observation, test result, image, video, link, or other.
- `summary`: what the source says or shows.
- `supported claim`: what content claim this evidence can safely support.
- `source`: where this evidence came from.
- `risk note`: what the owner should not overclaim.

A2 should not introduce new backend Evidence rules unless a later task explicitly approves it. If the current backend model cannot store every UX field directly, the harness may map or combine display fields conservatively during implementation.

## 8. Reference Card Interaction

ManualReference should become 参考视频 / 参考素材 cards.

Required card behavior:

- 3 required cards.
- 2 optional cards.
- enforce the existing 3-5 rule.
- keep intake method fixed as manual.
- hide system IDs by default.

Card fields:

- title.
- source URL.
- platform.
- why useful.
- borrowable pattern.
- do-not-copy note.

Field intent:

- `title`: owner-readable reference label.
- `source URL`: manually entered source or identifier.
- `platform`: TikTok or another manually noted platform/source.
- `why useful`: why this reference matters for the project.
- `borrowable pattern`: pacing, hook, scene, proof shot, or structure to learn from.
- `do-not-copy note`: explicit reminder that this is inspiration and trace, not material to duplicate.

## 9. Concept Workspace

CreativeConceptDraft should become 创意方向草稿.

The Concept Workspace should include:

- generated concept comparison cards.
- manual concept card.
- selected-only path.
- human-edited path.

Generated concept cards should be comparison-driven:

- angle.
- hook.
- rationale.
- evidence refs summary.
- reference inspiration summary.
- draft status.
- select action.

Manual concept card should support owner-created ideas without AI, RAG, prompts, or agent behavior.

The selected-only path should be explicit:

- owner selects a draft concept.
- selected concept remains draft.
- no automatic approval occurs.

The human-edited path should be explicit:

- owner edits angle/title/hook/rationale.
- edited concept remains draft.
- trace refs are preserved.
- generation method can show human-edited provenance in debug.

## 10. Script, Review, And Production Pack Areas

### 剧本草稿

ScriptPackDraft should become 剧本包草稿.

The area should show:

- script title.
- voiceover script.
- storyboard.
- shot list.
- visual requirements.
- asset requirements.
- generation notes.
- risk notes.

System trace remains collapsed.

### 审核

ReviewDecision should become 人工审核结果.

Allowed decisions remain:

- approved.
- rework.
- hold.
- stopped.

The owner-facing UI should explain outcome in business language, for example:

- approved: 可以形成生产交接包.
- rework: 需要返工后再交接.
- hold: 暂停但保留项目.
- stopped: 终止本轮生产.

### 生产包

ProductionPackExport should become 生产交接包.

Export area order:

1. Markdown tab first.
2. JSON trace tab second.
3. Debug trace collapsed.

Markdown is the primary human production handoff. JSON is the system-readable trace preview.

## 11. Save / Load Area

保存 / 加载 should stay available but not dominate the page.

Target behavior:

- save current workspace snapshot after a valid production pack exists.
- list saved local snapshots.
- load a snapshot for inspection.
- show readable validation errors.
- avoid editable load/resume in A2 unless explicitly approved later.

A2 should preserve the A1 JSON Snapshot Store behavior and should not turn save/load into a database, account, sync, or formal persistence system.

## 12. Explicitly Out Of Scope

A2 does not authorize:

- backend business rule changes.
- database implementation.
- SQLite.
- PostgreSQL.
- SQLAlchemy.
- Alembic.
- FastAPI.
- React / formal frontend.
- AI provider.
- RAG.
- prompt system.
- TikTok Search.
- Agent Runtime.
- Workflow Engine.
- Gate Engine.
- Platform Kernel.
- generation orchestration.
- GenerationPlan.
- RenderBatch.
- RenderJob.
- ComfyUI.
- Seedance.
- Kling.

## 13. Acceptance Criteria

A2 UX refactor planning is acceptable when:

- owner can complete the flow without understanding backend object names.
- owner can manually add/remove Evidence cards.
- references feel like reference video cards.
- concept selection is comparison-driven.
- selected-only and human-edited concept paths are both visible.
- production handoff Markdown is primary.
- JSON trace remains available but secondary.
- system IDs and trace refs are hidden by default.
- save/load remains available but does not dominate the page.
- the local workspace is still clearly not a formal frontend.
- scope remains inside the Minimum Usable Workspace.

## 14. Review Before Implementation

Before implementing A2, review:

- whether labels are Chinese-first and business-facing.
- whether the owner can see what to do next on each page.
- whether Evidence add/remove cards can map safely to existing backend Evidence without rule changes.
- whether Reference cards preserve the 3-5 manual reference rule.
- whether concept comparison supports both selected-only and human-edited paths.
- whether Markdown production handoff remains the primary output.
- whether debug trace is present but collapsed.
- whether save/load stays local and inspection-oriented.

If implementation needs backend rule changes, database work, API work, formal frontend work, AI, RAG, TikTok Search, Agent Runtime, Workflow Engine, or generation orchestration, it must stop and request a separate human-approved task.
