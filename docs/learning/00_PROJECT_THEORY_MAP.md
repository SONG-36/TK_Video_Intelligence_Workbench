# Project Theory Map

This learning note is project-specific guidance for TikTok Video Intelligence Workbench. It is not formal implementation authorization, not an ADR, and not a replacement for [../01_MVP_WALKING_SKELETON.md](../01_MVP_WALKING_SKELETON.md) or [../working/ACTIVE_ITERATION.md](../working/ACTIVE_ITERATION.md).

The current product is an AI-assisted content decision workspace, but the implemented WS-0 + WS-1 walking skeleton is still a thin in-memory chain. It uses project concepts and deterministic/mock or manual boundaries to prove that a car vacuum cleaner content decision can become a reviewed Production Pack.

## 1. Current Theory Layer

The core theory is simple:

```text
Business context + versioned product proof + traceable references
-> draft content decisions
-> human review
-> generation-ready handoff
```

The current walking skeleton proves this using:

- `ContentProject`: the container for one content decision chain.
- `ProductVersion`: the version anchor for claims and Evidence.
- `Evidence`: source material scoped to a `ProductVersion`.
- `KnowledgePack`: versioned content guidance, currently `v0.1`.
- `ManualReference`: manually entered inspiration with source trace.
- `CreativeConceptDraft`: draft concept candidate from deterministic/mock generation or owner manual input.
- `ScriptPackDraft`: draft production content based on a selected concept.
- `ReviewDecision`: human decision record.
- `ProductionPackExport`: in-memory Markdown / JSON-compatible handoff.

These concepts matter because the product is not just generating copy. It is preserving why content choices were made and what source material supports them.

## 2. Current Implemented Capability

Current WS-0 + WS-1 capability:

- Create a `ContentProject` from a structured Selection-to-Content Handoff.
- Bind a `Product` and `ProductVersion`.
- Bind `Evidence` to `ProductVersion`, not directly to `Product`.
- Prepare WS-1 inputs using `KnowledgePack v0.1` and 3-5 `ManualReference` items.
- Generate exactly 3 deterministic/mock `CreativeConceptDraft` items.
- Create an owner manual `CreativeConceptDraft`.
- Select and optionally edit one concept while preserving traceability.
- Generate a deterministic/mock `ScriptPackDraft`.
- Record a `ReviewDecision`.
- Export an in-memory Markdown / JSON-compatible `ProductionPackExport`.

The implementation does not currently have AI provider calls, RAG, prompts, Agent Runtime, TikTok Search, video generation, database persistence, or a formal frontend.

## 3. Future Possible Capability

Future capabilities may include:

- Replacing deterministic/mock concept and script generation with provider-backed AI calls.
- Recording model/provider run metadata when real AI is introduced.
- Using richer `KnowledgePack` structures after repeated real use.
- Adding curated Reference discovery after manual reference intake proves the pattern.
- Persisting projects, evidence, references, concepts, scripts, reviews, and exports in a database.
- Adding API and formal UI after domain behavior stabilizes.

Any future capability must preserve the current traceability principles. It should not bypass `ProductVersion`, `Evidence`, `ManualReference`, `KnowledgePack`, or human review.

## 4. Explicitly Out of Scope

This learning layer does not authorize:

- OpenAI or other AI provider integration.
- RAG or vector search.
- Prompt system implementation.
- Agent Runtime, Agent OS, Workflow Engine, Gate Engine, or Platform Kernel.
- TikTok automatic search.
- GenerationPlan, RenderBatch, RenderJob, ComfyUI, Seedance, Kling, or generation orchestration.
- Database schema design, API route design, or formal frontend design.

These may appear in future backlog conversations, but they are not current implemented capability.

## 5. How This Connects to WS-0 + WS-1

The car vacuum cleaner walking skeleton is the first proof of this theory. It starts with a real enough business handoff and ends with a reviewed Markdown / JSON-compatible Production Pack. The point is not to maximize automation. The point is to validate that the content decision chain has enough business meaning and traceability to be worth automating later.

Current WS-0 + WS-1 therefore asks:

- Is the `ContentProject` context clear enough?
- Is `Evidence` correctly scoped to the `ProductVersion`?
- Are the `ManualReference` items traceable and relevant?
- Does `KnowledgePack v0.1` provide a versioned guidance anchor?
- Are `CreativeConceptDraft` and `ScriptPackDraft` clearly draft artifacts?
- Does `ReviewDecision` control readiness?
- Does `ProductionPackExport` preserve the handoff trace?

## 6. How This Prevents Scope Creep

This map prevents scope creep by keeping the system centered on the current chain instead of future platforms. If a proposed task does not strengthen WS-0 + WS-1 traceability, review, or export quality, it should not enter the active iteration.

It also separates concepts from implementation authorization. Naming a future capability here does not approve building it.

## 7. What to Review Before Implementation

Before any implementation step, review:

- [../working/ACTIVE_ITERATION.md](../working/ACTIVE_ITERATION.md) for the current authorized boundary.
- [../02_DOMAIN_MODEL.md](../02_DOMAIN_MODEL.md) for domain meaning.
- Whether the task preserves `ProductVersion`-scoped `Evidence`.
- Whether AI-like output remains draft until human review.
- Whether the output can still be traced through `KnowledgePack`, `ManualReference`, and `ReviewDecision`.
