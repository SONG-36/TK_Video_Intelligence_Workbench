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
