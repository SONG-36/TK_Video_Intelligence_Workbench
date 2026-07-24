# Agent vs Workflow Boundary

This learning note explains how this project should think about agents and workflows without implementing them. It is not an ADR and does not authorize Agent Runtime, Workflow Engine, Gate Engine, or Platform Kernel work. The active implementation boundary remains [../working/ACTIVE_ITERATION.md](../working/ACTIVE_ITERATION.md).

## 1. Project-Specific Distinction

For TikTok Video Intelligence Workbench, the useful distinction is:

- Workflow: a known business sequence with clear inputs, outputs, and human checkpoints.
- Agent: an autonomous or semi-autonomous actor that can choose actions, tools, or next steps.

The current WS-0 + WS-1 walking skeleton is a fixed workflow, not an agent system. It has a known sequence:

```text
ContentProject
-> ProductVersion-scoped Evidence
-> KnowledgePack v0.1
-> ManualReference
-> CreativeConceptDraft
-> ScriptPackDraft
-> ReviewDecision
-> ProductionPackExport
```

The system should not introduce agents before the fixed workflow has repeated real use.

## 2. Current Implemented Capability

Current implemented capability:

- In-memory service functions for WS-0 and WS-1.
- Deterministic/mock `CreativeConceptDraft` generation.
- Manual `CreativeConceptDraft` creation.
- Human selection and optional edit.
- Deterministic/mock `ScriptPackDraft` generation.
- Explicit `ReviewDecision`.
- In-memory Markdown / JSON-compatible `ProductionPackExport`.
- Local Streamlit dev harnesses for owner smoke testing.

No current code implements Agent Runtime, tool planning, autonomous execution, workflow engine state machines, policy gates, or provider orchestration.

## 3. Future Possible Capability

Future possible capability may include:

- A fixed workflow runner after the same process repeats enough times.
- AI provider adapters for concept or script drafting.
- Human review queues.
- Tool-assisted reference collection.
- Trace records for model runs.
- Workflow templates for repeated content pack creation.

An agent-like capability may become useful only after the project knows which decisions can safely be delegated and which must remain owner-reviewed.

## 4. Explicitly Out of Scope

This note does not authorize:

- Agent Runtime.
- Agent OS.
- General Workflow Engine.
- Gate Engine.
- Platform Kernel.
- Autonomous tool selection.
- TikTok Search automation.
- GenerationPlan, RenderBatch, RenderJob, ComfyUI, Seedance, Kling, or generation orchestration.
- Prompt routing or multi-provider AI execution.

These remain future possibilities, not current implementation scope.

## 5. Boundary Rules for Current Development

For current WS-0 + WS-1 work:

- Prefer explicit service functions over generalized workflow abstractions.
- Prefer deterministic/mock outputs until AI provider integration is explicitly approved.
- Keep `ReviewDecision` as the human approval boundary.
- Keep `KnowledgePack`, `ManualReference`, and `Evidence` traceable.
- Do not hide business decisions behind automation.
- Do not let a helper function decide the next product scope.

If a developer wants to add a generic runner, registry, policy DSL, plugin system, or agent loop, that is a sign the task is outside the current walking skeleton.

## 6. How This Connects to WS-0 + WS-1

The current chain is intentionally fixed because the business meaning is still being validated. The owner must be able to inspect:

- the `ContentProject` context,
- the `ProductVersion` and its `Evidence`,
- the `KnowledgePack v0.1`,
- the `ManualReference` set,
- the draft concept options,
- the selected or edited concept,
- the `ScriptPackDraft`,
- the `ReviewDecision`,
- the `ProductionPackExport`.

Only after these checkpoints are stable should the project consider automating parts of the sequence.

## 7. How This Prevents Scope Creep

This boundary prevents premature platform work. It keeps the project from turning a working skeleton into an abstract agent platform before the first business chain has been validated.

It also protects the owner role. The owner still decides business meaning, review readiness, and approval. Automation can assist later, but it should not erase those decision points.

## 8. What to Review Before Implementation

Before implementing anything that sounds like workflow or agent work, review:

- [../03_TECHNICAL_ARCHITECTURE.md](../03_TECHNICAL_ARCHITECTURE.md) for current architecture constraints.
- [../04_EVOLUTION_BACKLOG.md](../04_EVOLUTION_BACKLOG.md) for future sequencing.
- Whether the requested feature is necessary for the current WS-0 + WS-1 chain.
- Whether the same behavior has repeated enough to justify abstraction.
- Whether human review remains explicit.
- Whether the task can be solved with a direct service function instead of a framework.
