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

Run [ws_full_walking_skeleton_app.py](ws_full_walking_skeleton_app.py) to smoke test the completed WS-0 + WS-1 chain:

```text
streamlit run tools/dev_harness/ws_full_walking_skeleton_app.py
```

The full harness lets the owner enter realistic car vacuum cleaner inputs, then runs the existing backend services through project creation, WS-1 input preparation, CreativeConcept Drafts, manual concept creation, selected concept edit, ScriptPackDraft generation, Human Review, Markdown export, and JSON-compatible export.

The full harness generates project, product, and product version IDs with a slug plus deterministic hash so Chinese or other non-ASCII owner inputs remain stable without collapsing to repeated fallback IDs. It also lets the owner choose whether the selected concept goes directly to ScriptPack generation or first receives a human edit.

The Markdown and JSON shown by this harness are in-memory previews produced by backend export functions. The harness does not write export files, persist records, call AI, call external APIs, or create a formal frontend.
