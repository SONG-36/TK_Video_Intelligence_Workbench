---
document_type: adr_log
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_2_ARCHITECTURE_DECISIONS
last_updated: 2026-07-22
change_policy: ADR_REQUIRED_AFTER_APPROVAL
depends_on:
  - ../00_PRODUCT_SYSTEM_OVERVIEW.md
  - ../01_MVP_WALKING_SKELETON.md
  - ../03_TECHNICAL_ARCHITECTURE.md
---

# ADR Log

## 1. Document Responsibility

This document records major product-architecture and technical-architecture decisions.

It does not repeat full product scope, domain model, technical architecture, or evolution backlog content. It preserves decision history and marks replaced decisions without renumbering.

Allowed ADR statuses:

```text
PROPOSED
ACCEPTED
LONG_TERM_DIRECTION
SUPERSEDED
REJECTED
```

## 2. ADR Overview

| ADR | Decision | Status |
|---|---|---|
| ADR-001 | Use modular monolith | ACCEPTED |
| ADR-002 | Keep Resource, Capability, Execution, Policy, Trace as platform observation dimensions | ACCEPTED |
| ADR-003 | Keep business semantics in Domain | ACCEPTED |
| ADR-004 | Agent belongs to Intelligence Plane | LONG_TERM_DIRECTION |
| ADR-005 | Agent frameworks are isolated by Adapter | LONG_TERM_DIRECTION |
| ADR-006 | Do not force LangChain or LangGraph | ACCEPTED |
| ADR-007 | Fixed Workflow before free Agent | ACCEPTED |
| ADR-008 | AI outputs drafts by default | ACCEPTED |
| ADR-009 | Do not build generic Agent OS now | ACCEPTED |
| ADR-010 | Current work can start from the middle of the business chain | ACCEPTED |
| ADR-011 | Define Kernel Contract before implementation | SUPERSEDED by ADR-023 |
| ADR-012 | Prefer structured relations over full RAG | ACCEPTED |
| ADR-013 | Current MVP must receive Selection-to-Content Handoff | ACCEPTED |
| ADR-014 | Market compliance and store health are Domain Context | LONG_TERM_DIRECTION |
| ADR-015 | Content Project binds operating context snapshot | ACCEPTED |
| ADR-016 | Every stage has formal Gate Decision | LONG_TERM_DIRECTION |
| ADR-017 | Content Route is a verifiable hypothesis | LONG_TERM_DIRECTION |
| ADR-018 | Different Routes produce different Delivery Packs | LONG_TERM_DIRECTION |
| ADR-019 | Provide Priority Lite | LONG_TERM_DIRECTION |
| ADR-020 | Create Experiment Contract before production | LONG_TERM_DIRECTION |
| ADR-021 | Release 1A MVP plus Evolution Backlog dual track | SUPERSEDED by ADR-022 and ADR-024 |
| ADR-022 | Adopt Production-intent Walking Skeleton | ACCEPTED |
| ADR-023 | Defer Formal Platform Kernel | ACCEPTED |
| ADR-024 | Consolidate Canonical Documentation | ACCEPTED |

## 3. Active Decision Notes

### ADR-001: Use Modular Monolith

Context:

The system needs fast product learning and coherent domain changes.

Decision:

Use a modular monolith before considering microservices.

Status:

ACCEPTED

### ADR-002: Keep Five Platform Observation Dimensions

Context:

Stable cross-cutting concerns exist, but they are not yet implementation-proven.

Decision:

Use Resource, Capability, Execution, Policy, and Trace as observation dimensions.

Status:

ACCEPTED

### ADR-003: Keep Business Semantics in Domain

Context:

Gate, route, priority, experiment, compliance, and store status are business semantics.

Decision:

Do not move business semantics into generic platform mechanisms.

Status:

ACCEPTED

### ADR-006: Do Not Force LangChain or LangGraph

Context:

Framework choice should not precede stable workflow and adapter boundaries.

Decision:

Do not require LangChain or LangGraph for the current MVP.

Status:

ACCEPTED

### ADR-007: Fixed Workflow before Free Agent

Context:

The first value chain needs traceable, reviewable behavior.

Decision:

Use fixed workflow first. Add dynamic agent behavior only after stable repeated workflows prove the need.

Status:

ACCEPTED

### ADR-008: AI Outputs Drafts by Default

Context:

AI can generate useful content but cannot own business approval.

Decision:

AI output is draft until human review approves it.

Status:

ACCEPTED

### ADR-009: Do Not Build Generic Agent OS Now

Context:

A generic Agent OS would delay value validation.

Decision:

Do not build generic Agent OS in the current MVP.

Status:

ACCEPTED

### ADR-010: Start from the Middle of the Business Chain

Context:

The project can validate content decision value without first implementing product opportunity discovery.

Decision:

Start from Selection-to-Content Handoff and preserve upstream context.

Status:

ACCEPTED

### ADR-012: Prefer Structured Relations over Full RAG

Context:

The system needs explainable references among product, evidence, reference, concept, and script outputs.

Decision:

Use structured relationships and citations before broad unstructured retrieval.

Status:

ACCEPTED

### ADR-013: MVP Receives Selection-to-Content Handoff

Context:

The content system cannot safely operate from Product ID alone.

Decision:

Every Content Project receives a Selection-to-Content Handoff.

Status:

ACCEPTED

### ADR-015: Content Project Binds Operating Context Snapshot

Context:

Market, platform, objective, route hypothesis, and owner shape content decisions.

Decision:

ContentProject binds OperatingContextSnapshot.

Status:

ACCEPTED

## 4. Long-term Direction Decisions

### ADR-004: Agent Belongs to Intelligence Plane

Decision:

Agent concepts may remain as long-term Intelligence Plane concepts, but no Agent Runtime is implemented now.

Status:

LONG_TERM_DIRECTION

### ADR-005: Agent Frameworks Are Isolated by Adapter

Decision:

If future agent frameworks are introduced, isolate them behind adapters.

Status:

LONG_TERM_DIRECTION

### ADR-014: Market Compliance and Store Health Are Domain Context

Decision:

Market compliance and store health remain business context, not Platform Core.

Status:

LONG_TERM_DIRECTION

### ADR-016: Gate Decision

Decision:

Gate remains a valid long-term governance concept. The current MVP uses human review/status, not a Gate Engine.

Status:

LONG_TERM_DIRECTION

### ADR-017: Route Hypothesis

Decision:

Route should eventually be verifiable. The current MVP keeps route lightweight and allows `UNKNOWN`.

Status:

LONG_TERM_DIRECTION

### ADR-018: Route-specific Delivery Packs

Decision:

Different routes may eventually produce different packs. The current MVP produces only Generation-ready Owned Content Production Pack.

Status:

LONG_TERM_DIRECTION

### ADR-019: Priority Lite

Decision:

Priority remains a future capability. The current MVP does not implement a Priority Algorithm.

Status:

LONG_TERM_DIRECTION

### ADR-020: Experiment Contract

Decision:

Experiment Contract remains a future governance capability. The current MVP records `test_question`.

Status:

LONG_TERM_DIRECTION

## 5. Superseded Decisions

### ADR-011: Define Kernel Contract before Implementation

Superseded by:

- ADR-023.

Reason:

The prior wording could be read as requiring a formal Kernel before the first real product slice. The new decision keeps useful observation dimensions but defers framework implementation.

Status:

SUPERSEDED

### ADR-021: Release 1A MVP plus Evolution Backlog Dual Track

Superseded by:

- ADR-022.
- ADR-024.

Reason:

The dual-track idea remains, but the old Release 1A framing could still imply Product Workspace first and too many formal documents. The new authority uses Production-intent Walking Skeleton and consolidated canonical documents.

Status:

SUPERSEDED

## 6. New Decisions

### ADR-022: Adopt Production-intent Walking Skeleton

Context:

Complete Product Workspace first would delay end-to-end business validation. A pure demo would damage source, version, review, and migration boundaries.

Decision:

Adopt a thin but real end-to-end Walking Skeleton. Implement high-migration-cost boundaries with production intent. Keep unvalidated business depth lightweight. The first value endpoint is Generation-ready Owned Content Production Pack.

The next active iteration target is WS-0 + WS-1 thin end-to-end output, not Product Workspace CRUD alone. This remains a planning direction and does not authorize code until `../working/ACTIVE_ITERATION.md` is approved.

Status:

ACCEPTED

### ADR-023: Defer Formal Platform Kernel

Context:

Resource, Capability, Execution, Policy, and Trace are useful dimensions, but implementing a formal framework before real repeated use would increase complexity.

Decision:

Keep Resource, Capability, Execution, Policy, and Trace as observation dimensions. Do not implement a Kernel Framework now. Extract stable shared mechanisms only when real modules repeat and pilots prove the need. Prefer the name Platform Core for future extraction.

Status:

ACCEPTED

### ADR-024: Consolidate Canonical Documentation

Context:

The repository accumulated many overlapping formal documents across product, release, scope, phase, vertical slice, architecture, and implementation planning.

Decision:

Product and architecture authority is fixed to six documents plus this ADR Log. New product decisions update the existing authority documents first. Do not create new formal numbered documents for each phase, slice, or scope. Temporary research belongs in `working/`. Git history is the default document history.

Status:

ACCEPTED

## 7. Documentation Migration Note

This ADR Log replaces the former architecture decision file and records consolidation from the previous formal set:

- 00_MASTER_DESIGN.md.
- 01_CAPABILITY_ROADMAP.md.
- 02_DELIVERY_RELEASES.md.
- 03_RELEASE_1_SCOPE_AND_BOUNDARIES.md.
- 04_RELEASE_1_BUSINESS_PROCESS.md.
- 05_RELEASE_1_VERTICAL_SLICES.md.
- 06_RELEASE_1A_MVP_SCOPE.md.
- 07_RELEASE_1A_IMPLEMENTATION_PLAN.md.
- 08_LONG_TERM_EVOLUTION_BACKLOG.md.
- 09_EXISTING_SYSTEM_MAPPING.md.
- 10_RELEASE_1A_TECHNICAL_BASELINE.md.
- 11_RELEASE_1A_DOMAIN_MODEL_LITE.md.
- 12_PHASE_I1_PRODUCT_WORKSPACE_PLAN.md.
- architecture/01_PLATFORM_ARCHITECTURE.md.
- architecture/02_ARCHITECTURE_DECISIONS.md.

The historical versions remain available through Git history. They were not copied into archive during this consolidation.
