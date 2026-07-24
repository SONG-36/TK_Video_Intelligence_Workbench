# Evidence Traceability and Claims

This learning note explains the project-specific claim discipline for TikTok Video Intelligence Workbench. It is documentation only and does not authorize implementation beyond [../working/ACTIVE_ITERATION.md](../working/ACTIVE_ITERATION.md).

The current WS-0 + WS-1 walking skeleton uses a car vacuum cleaner pilot to prove that content output can stay connected to source material. The central rule is: `Evidence` is source material, not automatically confirmed truth.

## 1. Why Evidence Exists

Content systems often fail when they turn product claims into scripts without preserving where the claim came from. This project treats `Evidence` as the traceable input that keeps generated or drafted content accountable.

For the current project, `Evidence` should answer:

- What source suggested this claim or observation?
- Which `ProductVersion` does it apply to?
- Is it a supplier claim, owner observation, test result, image, video, link, or other source?
- Should a human treat it as proof, inspiration, or only raw source material?

## 2. Current Implemented Capability

Current WS-0 + WS-1 capability:

- `Evidence` is created during the WS-0 project creation flow.
- `Evidence` must bind to `ProductVersion`.
- `Evidence` cannot bind directly to `Product`.
- `CreativeConceptDraft` preserves `evidence_refs`.
- `ScriptPackDraft` preserves `evidence_refs`.
- `ProductionPackExport` preserves evidence references in Markdown and JSON-compatible output.

The current system does not extract facts from Evidence, does not run AI validation, and does not decide that Evidence is true. It only preserves the source trace through the walking skeleton.

## 3. Claim Discipline in the Current Skeleton

The car vacuum cleaner pilot should treat claims conservatively:

- Supplier text is a supplier claim, not verified performance proof.
- Owner observation is a useful signal, not a universal product guarantee.
- Visual evidence can support visible scene choices, but not hidden technical claims.
- Script lines should avoid unsupported suction, battery, durability, or performance promises.

This is why `ScriptPackDraft` includes risk notes and why `ReviewDecision` is required before the pack becomes generation-ready.

## 4. Current Implemented Capability vs Future Possible Capability

Current implemented capability:

- Store source-level `Evidence` inputs.
- Keep `Evidence` scoped to `ProductVersion`.
- Carry evidence references through concepts, scripts, and exports.
- Make human review responsible for approval.

Future possible capability:

- Candidate fact extraction from Evidence.
- Evidence strength labels.
- Human fact confirmation workflow.
- Claim-to-script sentence mapping.
- Evidence review UI.
- Automated warning when a script claim has no evidence reference.

Future capability must not weaken the current rule that Evidence is source material until reviewed.

## 5. Explicitly Out of Scope

This note does not authorize:

- AI fact extraction.
- RAG over evidence.
- Automated claim approval.
- Supplier document ingestion platform.
- Full knowledge base platform.
- Database schema, API, or UI for Evidence review.
- TikTok or web search.
- Generation orchestration.

The current implemented chain remains in-memory and thin.

## 6. How This Connects to WS-0 + WS-1

In WS-0, Evidence enters the system with the `ContentProject`, `Product`, and `ProductVersion`. In WS-1, the same evidence references are preserved by `CreativeConceptDraft`, `ScriptPackDraft`, and `ProductionPackExport`.

The walking skeleton is acceptable only if the final Markdown and JSON-compatible Production Pack can show which Evidence references informed the selected concept and script.

## 7. How This Prevents Scope Creep

This note prevents scope creep by separating traceability from full claim intelligence. The current job is to keep evidence references intact. It is not to build a fact engine, claim approval engine, or knowledge platform.

When a proposed task says "make Evidence smarter," the first question should be whether the current walking skeleton lacks traceability. If traceability is intact, defer the richer capability until real repeated use proves the need.

## 8. What to Review Before Implementation

Before implementing anything related to Evidence or claims, review:

- [../02_DOMAIN_MODEL.md](../02_DOMAIN_MODEL.md) for domain object meaning.
- [../01_MVP_WALKING_SKELETON.md](../01_MVP_WALKING_SKELETON.md) for approved scope.
- Whether `Evidence` remains bound to `ProductVersion`.
- Whether a new feature would incorrectly treat Evidence as confirmed fact.
- Whether final output still preserves `evidence_refs`.
- Whether `ReviewDecision` remains the approval boundary.
