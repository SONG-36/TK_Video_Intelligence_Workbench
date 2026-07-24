# WS Pilot Input Harness

This directory contains local development smoke tools only.

Run [ws_pilot_input_app.py](ws_pilot_input_app.py) from the repository root with the Python 3.12 development environment active:

```text
streamlit run tools/dev_harness/ws_pilot_input_app.py
```

The app lets the owner manually enter car vacuum cleaner WS-0 and WS-1 input data, then validates the chain through the existing `create_project_from_handoff(...)` and `prepare_ws1_inputs(...)` services.

The interface is organized as a business flow:

- Project / Handoff
- Product / Version
- Evidence Lite
- Knowledge Pack v0.1
- Manual References
- Validate / Trace Preview

System IDs, Knowledge Pack version, manual intake method, and prepared status are generated or fixed by the harness rather than treated as primary owner inputs.

It is not the product frontend, not an API, not a database workflow, not an AI workflow, and not a formal export.

Run [ws_full_walking_skeleton_app.py](ws_full_walking_skeleton_app.py) to use the local Minimum Workspace harness for the completed WS-0 + WS-1 chain:

```text
streamlit run tools/dev_harness/ws_full_walking_skeleton_app.py
```

The full harness uses Chinese-first owner-facing task areas:

- 项目输入
- 产品证据
- 参考视频
- 创意方向
- 剧本草稿
- 审核
- 生产包
- 保存 / 加载

It lets the owner enter realistic car vacuum cleaner inputs, then runs the existing backend services through project creation, WS-1 input preparation, CreativeConcept Drafts, manual concept creation, selected concept edit, ScriptPackDraft generation, Human Review, Markdown export, and JSON-compatible export.

The owner-facing labels intentionally hide backend object names by default:

- Evidence Lite is shown as 产品证据 / 卖点依据.
- ManualReference is shown as 参考视频 / 参考素材.
- ProductVersion is shown as 当前样品 / 当前版本.
- CreativeConceptDraft is shown as 创意方向草稿.
- ScriptPackDraft is shown as 剧本包草稿.
- ReviewDecision is shown as 人工审核结果.
- ProductionPackExport is shown as 生产交接包.

System IDs and trace refs remain available in collapsed debug panels.

The 产品证据 area supports manual add/remove evidence cards. The 参考视频 area uses 3 required cards plus 2 optional cards while preserving the backend 3-5 ManualReference rule.

The full harness generates project, product, and product version IDs with a slug plus deterministic hash so Chinese or other non-ASCII owner inputs remain stable without collapsing to repeated fallback IDs. It also lets the owner choose whether the selected concept goes directly to ScriptPack generation or first receives a human edit.

The Markdown and JSON shown by this harness are in-memory previews produced by backend export functions. Markdown is the primary production handoff preview; JSON is a secondary trace preview. The harness does not write export files, call AI, call external APIs, or create a formal frontend.

The full harness also supports local JSON workspace snapshots through the A1.1 JSON Snapshot Store:

- Saved snapshots are listed in the sidebar under "Saved Workspace Snapshots".
- A completed in-memory run can be saved from the "Snapshot" tab.
- Snapshots are saved under `.local/workspace/projects/` by default.
- Loading a snapshot is inspection-only; it shows trace summary, Markdown preview, and JSON 追踪预览 without hydrating the editable form.

Snapshot persistence is still a local development/minimum workspace aid. It is not SQLite, PostgreSQL, FastAPI, React, a formal frontend, or a production persistence layer.
