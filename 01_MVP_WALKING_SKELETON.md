---
document_type: mvp_walking_skeleton
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_2_CURRENT_MVP
last_updated: 2026-07-22
change_policy: ADR_REQUIRED_AFTER_APPROVAL
depends_on:
  - 00_PRODUCT_SYSTEM_OVERVIEW.md
---

# MVP Walking Skeleton

## 1. Document Responsibility

This is the only current MVP scope and business flow document.

It defines the Production-intent Walking Skeleton, current capability classification, first pilot, acceptance questions, and iteration sequence.

It does not freeze full database fields, final API URLs, UI layout, prompt files, workflow files, or future generation schemas.

## 2. MVP Problem Statement

The first version helps operators answer:

```text
Given a selected product and business context, what owned content should we create, why, based on which evidence and references, and is the output ready to hand to shooting or generation work?
```

The MVP must produce an explainable, human-reviewed, generation-ready Owned Content Production Pack.

## 3. Target Users

- Project owner.
- TikTok operator.
- Product owner.
- Content review owner.

## 4. Production-intent Walking Skeleton

Definition:

```text
Use the thinnest real end-to-end business chain to validate product value.
Keep production-intent standards for high-migration-cost boundaries such as stable IDs, provenance, review, versioning, migration, and adapters.
Keep unvalidated fields, rules, gates, routes, and automation lightweight.
```

The adopted flow:

```text
Create Content Project
↓
Enter Selection-to-Content Handoff
↓
Bind Product / ProductVersion
↓
Add minimal Evidence
↓
Load versioned Content Knowledge Pack
↓
Manually add 3-5 References
↓
Generate 3 Creative Concept Drafts
↓
Human selects or edits one Concept
↓
Generate Script / Storyboard / Shot List
↓
Human Review
↓
Export Markdown / JSON
↓
Form Generation-ready Owned Content Production Pack
```

Rejected approaches:

- Build a complete Product Workspace first, then Knowledge, then Reference, and only much later reach Script Pack.
- Build a Streamlit-style single page with hard-coded prompts and AI output treated as final.

## 4.1 ProductVersion Lite Boundary

WS-0 must include ProductVersion Lite.

ProductVersion Lite means the first implementation keeps the minimum version boundary required for stable version identity and Evidence applicability. Evidence must be bound through ProductVersion and must not bypass ProductVersion by attaching directly to Product.

ProductVersion depth remains `LIGHTWEIGHT` because the first pass only implements the minimum version boundary. It does not mean ProductVersion is absent from the first pass.

WS-2 deepens ProductVersion into supplier, sample, packaging, file Evidence, fact/proof/risk/unknown, and product knowledge governance. This document does not freeze final database fields.

## 5. Selection-to-Content Handoff

The MVP does not build a complete selection system.

Every Content Project must receive a Selection-to-Content Handoff. Version 1 is manually entered by operators.

Minimum fields:

| Field | Meaning |
|---|---|
| `selection_rationale` | Why this product enters content work. |
| `target_market` | Target market for this content project. |
| `platform` | Target platform. |
| `content_objective` | What this content round should achieve. |
| `initial_route_hypothesis` | Initial route; may be `UNKNOWN`. |
| `test_question` | What this content round intends to validate. |
| `project_owner` | Person accountable for the result. |
| `store_account_context` | Optional store or account context. |

This is an upstream context snapshot, not a full selection approval workflow.

## 6. Content Knowledge Pack

The MVP cannot operate with no script knowledge foundation.

It uses a logical object:

```text
Versioned Content Knowledge Pack
```

The first implementation must include a real, versioned Knowledge Pack v0.1. It may be represented as Markdown / YAML in a future approved active iteration.

Knowledge Pack v0.1 must contain at least:

- Script Rules.
- Pattern Cards.
- Hook Guidance.
- Claims Guardrails.
- Review Rubric.
- Market Style Notes.

Current document scope only defines:

- Business responsibility.
- Minimal components.
- Version requirement.
- AI Run reference to Knowledge Pack Version.

Every AI Run that uses the Knowledge Pack must record the exact Knowledge Pack version.

This task does not create a `knowledge/` directory or prompt files.

Upgrade to a full knowledge platform only when UI management, search, tags, approval, market/category classification, performance feedback, or automatic recommendation becomes necessary.

## 7. Manual Reference

WS-1 may use manually entered references.

Reference version 1 must preserve:

- Source URL or source description.
- Platform.
- Creator/account when known.
- Hook or scene note.
- Why it is relevant.
- Which concept or script element used it.

Automatic TikTok search is deferred to WS-3.

## 8. Generation-ready Output

The MVP does not implement batch video production.

The current output contract is:

```text
Generation-ready Owned Content Production Pack
```

Minimum output:

| Field | Meaning |
|---|---|
| `script` | Approved script text. |
| `storyboard` | Scene-level production design. |
| `shots` | Shot list. |
| `shot_duration` | Expected duration per shot or segment. |
| `aspect_ratio` | Target output aspect ratio. |
| `visual_requirement` | Visual requirements for shooting or generation. |
| `asset_requirement` | Required product, image, video, audio, or design assets. |
| `recommended_production_mode` | `REAL_SHOOT`, `AI_IMAGE`, `AI_VIDEO`, `MIXED`, or `UNDECIDED`. |
| `generation_notes` | Notes for downstream generation or production teams. |
| `evidence_references` | Evidence citations used by the pack. |
| `reference_references` | Reference citations used by the pack. |
| `risk_notes` | Claims, proof, compliance, or production risks. |
| `review_status` | Draft, approved, rework, hold, or stopped. |

The main system only owns this output contract. It does not implement GenerationPlan, RenderBatch, RenderJob, ComfyUI Adapter, Seedance Adapter, worker, queue, provider routing, or automatic batch costing.

## 9. MVP Capability Classification

| Capability | Classification | Note |
|---|---|---|
| Content Project | MUST_HAVE | Work container for the chain. |
| Selection Handoff | MUST_HAVE | Required upstream snapshot. |
| Product Lite | MUST_HAVE | Stable product identity. |
| Evidence Lite | MUST_HAVE | Minimal source records. |
| Knowledge Pack Version | MUST_HAVE | Version referenced by AI Runs. |
| Manual Reference | MUST_HAVE | 3-5 references entered by user. |
| Creative Concept Draft | MUST_HAVE | Generate three drafts. |
| ScriptPack | MUST_HAVE | Script, storyboard, shots, generation notes. |
| Human Review | MUST_HAVE | AI output cannot approve itself. |
| Markdown / JSON Export | MUST_HAVE | Handoff to production or generation work. |
| ProductVersion depth | LIGHTWEIGHT | First pass implements minimum version boundary, not Sample/Batch depth. |
| File Evidence | LIGHTWEIGHT | May start as link/text if file upload is not in the first coding iteration. |
| Automatic TikTok Search | DEFERRED | Revisit in WS-3. |
| Full Knowledge Platform | DEFERRED | Current Knowledge Pack is versioned content, not a platform. |
| Gate Engine | DEFERRED | Use human review/status first. |
| Priority Algorithm | DEFERRED | Manual priority only if needed. |
| Experiment Platform | DEFERRED | Store the test question only. |
| Generation Orchestration | DEFERRED | Output contract only. |
| ComfyUI / Seedance Lab | PARALLEL_LAB | Independent validation, not main-system model pollution. |

## 10. First Pilot

First pilot product:

```text
车载吸尘器
```

The pilot must produce:

- Product context.
- Real Evidence.
- Manual References.
- Three Creative Concepts.
- One Approved Concept.
- English Script.
- Storyboard.
- Shot List.
- Evidence references.
- Reference references.
- Generation Notes.
- Markdown export.
- JSON export.

## 11. MVP Acceptance Questions

Operators must be able to answer:

- Why are we doing this product?
- What is this content round testing?
- Which Evidence was used?
- Which References were borrowed from?
- Why was this Concept selected?
- Which content was AI generated?
- Which content was human approved?
- Can this Production Pack be handed to a shooting or generation team?

## 12. Iteration Sequence

### WS-0: Project and Context Entry

- Content Project.
- Selection Handoff.
- Product Lite.
- ProductVersion Lite.
- Evidence Lite.

### WS-1: Thin End-to-End Chain

- Knowledge Pack Version.
- Manual Reference.
- Concept Draft.
- ScriptPack Draft.
- Review.
- Export.

### WS-2: Product and Evidence Deepening

- ProductVersion.
- File Evidence.
- Fact / Proof / Risk / Unknown.
- Product Knowledge Baseline.

### WS-3: Reference Integration

- TikTokSearchAdapter.
- Video breakdown.
- Reference Pack.

### WS-4: Script and Delivery Deepening

- Concept Version.
- Storyboard.
- Shot.
- Delivery Pack deepening.

### WS-5: Three-product Pilot

- 车载吸尘器.
- 电动泡沫喷壶.
- One personal-care product.

### WS-6: Architecture Review

Decide which real repetitions justify extraction into Platform Core.

## 13. First Active Iteration Boundary

The first future `working/ACTIVE_ITERATION.md` must use WS-0 + WS-1 thin end-to-end output as its acceptance endpoint.

It may split the work into multiple coding steps inside one iteration, but it must not declare the Walking Skeleton complete after only Product/Evidence CRUD.

## 14. Implementation Authorization

This document is a draft for human review.

It does not authorize business code. After approval, the first coding task must be defined in a single `working/ACTIVE_ITERATION.md`.
