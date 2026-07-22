---
document_type: domain_model
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_2_DOMAIN_MODEL
last_updated: 2026-07-22
change_policy: ADR_REQUIRED_AFTER_APPROVAL
depends_on:
  - 00_PRODUCT_SYSTEM_OVERVIEW.md
  - 01_MVP_WALKING_SKELETON.md
---

# Domain Model

## 1. Document Responsibility

This document defines current Walking Skeleton business concepts and relationships.

It is not a database schema, final API contract, full DDD model, or future object catalog.

## 2. Current Core Objects

| Object | Business Responsibility |
|---|---|
| `ContentProject` | Work container for one content decision chain. |
| `OperatingContextSnapshot` | Selection-to-Content Handoff and target operating context. |
| `Product` | Stable product identity. |
| `ProductVersion` | Supplier, sample, model, packaging, or configuration version used by evidence. |
| `Evidence` | Source material for product claims, observations, tests, images, videos, links, or notes. |
| `KnowledgePack` | Versioned logical content knowledge package used by AI Runs. |
| `Reference` | Manually entered or later adapter-sourced market/reference content. |
| `CreativeConcept` | AI draft or human-edited creative direction candidate. |
| `ScriptPack` | Aggregated script, storyboard, shots, and generation-ready notes. |
| `Review` | Human review decision for a target resource. |
| `Run` | Trace record for AI or automated processing. |

## 3. Minimal Relationships

```text
ContentProject
├── OperatingContextSnapshot
├── ProductVersion
├── References
├── KnowledgePack Version
├── CreativeConcepts
└── Approved ScriptPack

Product
└── ProductVersion
    └── Evidence

Run
├── Input Versions
├── Knowledge Pack Version
├── Model / Provider
├── Output Version
├── Cost
└── Error

Review
├── Target Resource
├── Reviewer
├── Decision
└── Note
```

## 4. Selection-to-Content Handoff

The handoff is stored as part of `OperatingContextSnapshot`.

Minimum fields:

| Field | Meaning |
|---|---|
| `selection_rationale` | Why this product enters content work. |
| `target_market` | Target market. |
| `platform` | Target platform. |
| `content_objective` | What this content round should achieve. |
| `initial_route_hypothesis` | Initial route; may be `UNKNOWN`. |
| `test_question` | What this content round intends to validate. |
| `project_owner` | Person accountable for result. |
| `store_account_context` | Optional store or account context. |

This handoff is an upstream context snapshot, not a complete selection approval object.

## 5. Product and ProductVersion Boundary

`Product` represents stable product identity.

`ProductVersion` represents the version to which evidence applies, such as supplier version, sample, model, configuration, packaging version, or other lightweight version note.

WS-0 must include ProductVersion Lite.

ProductVersion Lite carries only the minimum boundary needed for:

- Stable version identity.
- Evidence applicability scope.
- Preventing Evidence from being attached directly to Product.

ProductVersion Lite does not freeze final database fields.

Current rule:

- Evidence belongs to ProductVersion.
- ProductVersion belongs to Product.
- Evidence must not bypass ProductVersion by binding directly to Product.
- Evidence from one version must not be silently reused as proof for another version.
- Supplier, Sample, Batch, PackagingVersion, file Evidence, and knowledge governance depth belong to WS-2 and later.

## 6. Evidence Boundary

Evidence is source material.

Evidence does not automatically equal Confirmed Fact.

Rules:

- AI may extract candidate content from Evidence.
- AI cannot automatically confirm formal facts.
- Original Evidence must not be overwritten by AI results.
- Evidence must keep source, captured time when known, and ProductVersion relationship.
- Human review is required before candidate facts become approved business content.

Candidate Evidence categories:

```text
SUPPLIER_DOCUMENT
SUPPLIER_CLAIM
USER_OBSERVATION
TEST_RESULT
IMAGE
VIDEO
LINK
OTHER
```

These are concept categories, not frozen database enums.

## 7. KnowledgePack Boundary

`KnowledgePack` is a logical object.

The first implementation must include a real Knowledge Pack v0.1. It can be represented by versioned Markdown / YAML content in a future approved active iteration. This consolidation does not create a knowledge directory, table, UI, search, tags, management platform, or prompt file.

Business responsibility:

- Provide Script Rules.
- Provide Pattern Cards.
- Provide Hook Guidance.
- Provide Claims Guardrails.
- Provide Review Rubric.
- Provide Market Style Notes.

Run requirement:

- Every AI Run that uses knowledge must record the Knowledge Pack Version, including v0.1.

## 8. Reference Boundary

Reference is content used as market or creative input.

Version 1 may be manually entered.

Minimum responsibilities:

- Preserve source.
- Record why it is relevant.
- Record hook, scene, format, proof, or style notes when useful.
- Allow later citation from Concept or ScriptPack.

Automatic search and video breakdown are adapter-backed future capabilities.

## 9. CreativeConcept Boundary

`CreativeConcept` is a draft or selected direction.

Minimum responsibilities:

- Keep AI-generated drafts separate from human-edited or approved concepts.
- Reference Evidence and References used.
- Preserve why one concept was selected.
- Allow rejected drafts to remain traceable without becoming production instructions.

## 10. ScriptPack Boundary

The first ScriptPack may aggregate:

- `script`.
- `storyboard`.
- `shots`.
- `shot_duration`.
- `aspect_ratio`.
- `visual_requirement`.
- `asset_requirement`.
- `recommended_production_mode`.
- `generation_notes`.
- `evidence_references`.
- `reference_references`.
- `risk_notes`.
- `review_status`.

Do not split this into many tables solely for modeling purity before real use proves the need.

## 11. Run Boundary

`Run` records AI or automated processing.

Minimum responsibilities:

- Input versions.
- Knowledge Pack Version.
- Model / provider.
- Output version.
- Cost when available.
- Error when failed.

Run does not imply a generic workflow engine or agent runtime.

## 12. Review Boundary

`Review` records human decision.

Minimum responsibilities:

- Target resource.
- Reviewer.
- Decision.
- Note.
- Decision time.

AI may suggest, but cannot approve formal content.

## 13. Future-only Objects

The following are not current Walking Skeleton domain objects. They are tracked in [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md).

| Future Object | Backlog Area |
|---|---|
| Gate | EV-B |
| Portfolio | EV-A |
| Experiment | EV-B / EV-H |
| StoreHealthSnapshot | EV-D |
| ComplianceProfile | EV-D |
| GenerationPlan | EV-G |
| RenderBatch | EV-G |
| RenderJob | EV-G |
| Artifact | EV-G |
| Agent Runtime | EV-H |
