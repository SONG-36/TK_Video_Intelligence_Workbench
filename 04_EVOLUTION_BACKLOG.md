---
document_type: evolution_backlog
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_2_EVOLUTION_BACKLOG
last_updated: 2026-07-22
change_policy: ADR_REQUIRED_AFTER_APPROVAL
depends_on:
  - 00_PRODUCT_SYSTEM_OVERVIEW.md
  - 01_MVP_WALKING_SKELETON.md
  - 02_DOMAIN_MODEL.md
  - 03_TECHNICAL_ARCHITECTURE.md
---

# Evolution Backlog

## 1. Document Responsibility

This document captures long-term capabilities that are valid but deferred.

It does not authorize implementation. It does not define future schemas. It records problem groups, current MVP handling, observed evidence, revisit triggers, possible direction, and status.

Allowed status:

```text
CAPTURED
OBSERVING
READY_FOR_DESIGN
PARALLEL_LAB
REJECTED
```

## 2. Backlog Groups

### EV-A: Selection and Operating Context

Problem:

Full selection, portfolio, priority, and automatic Selection-to-Content Handoff are not part of the current MVP, but the content system must not lose upstream business context.

MVP Handling:

Operators manually enter Selection-to-Content Handoff and optional store/account context.

Observed Evidence:

Repository currently has documentation only. No product pilots have run.

Revisit Triggers:

- Multiple products compete for the same content resources.
- Operators repeatedly ask the system to decide which product should enter content work.
- Manual handoff becomes inconsistent or incomplete across pilots.

Possible Direction:

Build selection workflow, portfolio review, priority support, and automatic handoff generation after real content pilots expose repeated needs.

Status:

CAPTURED

### EV-B: Decision Governance

Problem:

Gate, route hypothesis, override, decision authority, and experiment contract are important, but full governance can overwhelm the Walking Skeleton.

MVP Handling:

Use human review, status, decision note, route hypothesis text, and `test_question`.

Observed Evidence:

No current implementation. Prior design identified Gate and Route as important but unvalidated at field depth.

Revisit Triggers:

- Projects repeatedly stop or rework for the same reason.
- Reviewers disagree on approval authority.
- `UNKNOWN` route or route changes become common.
- Content goes live and requires comparison against a pre-declared experiment question.

Possible Direction:

Evolve from Review records into Gate, Route Hypothesis, Override, and Experiment Contract models only after repeated pilot evidence.

Status:

CAPTURED

### EV-C: Product Knowledge and Evidence Governance

Problem:

Product version, sample, batch, snapshot freshness, evidence correction, invalidation, and downstream review can become complex.

MVP Handling:

Use Product, ProductVersion, Evidence Lite, provenance, and human review. Do not split Sample or Batch until needed.

Observed Evidence:

Current audit confirms no Product or Evidence code exists yet.

Revisit Triggers:

- Evidence conflicts across supplier versions.
- A script cites a fact later corrected.
- Packaging, batch, or sample differences affect claims.
- Operators cannot tell whether a source applies to the content being produced.

Possible Direction:

Introduce Sample, Batch, Evidence Scope, correction workflow, and downstream impact review.

Status:

CAPTURED

### EV-D: Market, Compliance and Store Context

Problem:

Market policy, platform rules, store health, channel context, and rule precedence affect content decisions.

MVP Handling:

Use target market, platform, optional store/account context, claims guardrails, and risk notes.

Observed Evidence:

No store, compliance, or channel integration exists in the current repository.

Revisit Triggers:

- Claims risk repeatedly blocks approval.
- Store or account health changes project feasibility.
- Multiple markets need different scripts or claims.
- Manual risk notes fail to prevent unsafe output.

Possible Direction:

Introduce ComplianceProfile, StoreHealthSnapshot, Channel Context, rule precedence, and manual rule library before any automatic enforcement.

Status:

CAPTURED

### EV-E: Content Knowledge and Script Intelligence

Problem:

A complete knowledge platform may eventually be needed for hooks, patterns, rubrics, prompt evaluation, and performance-informed script intelligence.

MVP Handling:

Use Versioned Content Knowledge Pack as a lightweight logical object.

Observed Evidence:

No knowledge directory, UI, search, tags, or approval flow exists.

Revisit Triggers:

- Operators need to search or compare rules.
- Knowledge updates affect many Runs.
- Prompt quality varies because knowledge versions are unclear.
- Performance feedback identifies reusable script patterns.

Possible Direction:

Build knowledge management UI, search, tags, approval, market/category classification, prompt evaluation, and feedback linkage.

Status:

CAPTURED

### EV-F: Reference Intelligence

Problem:

TikTok search, video breakdown, reference scoring, and freshness can improve content decisions, but automatic reference intelligence is not required for WS-1.

MVP Handling:

Use manual references with source, notes, relevance, and citations.

Observed Evidence:

Existing system mapping confirms external tools for TikTok search and video analysis, but no current repository integration.

Revisit Triggers:

- Manual reference entry is too slow.
- Operators repeatedly use the same search workflow.
- Reference quality or freshness becomes hard to judge.
- Content decisions need structured breakdown of hooks, scenes, proof, and format.

Possible Direction:

Add TikTokSearchAdapter, reference media adapter, video breakdown, reference scoring, and freshness tracking.

Status:

CAPTURED

### EV-G: Generation Orchestration

Problem:

Full generation requires plans, batches, jobs, provider adapters, workers, queues, cost control, review, and artifacts. This is outside the main MVP but valuable to validate independently.

MVP Handling:

Main system exports Generation-ready Owned Content Production Pack only.

Observed Evidence:

External Seedance and video creation experiments exist, but current repository has no generation implementation.

Revisit Triggers:

- Production team can repeatedly consume exported packs.
- Manual handoff to generation becomes the bottleneck.
- Parallel Lab proves provider speed, cost, success rate, and output quality.
- Human review needs to compare rendered artifacts with approved packs.

Possible Direction:

Run an isolated Generation Lab for ComfyUI Workflow, API Workflow JSON, Binding Manifest, single-task submission, result collection, Seedance validation, speed, success rate, and resource cost. Later consider GenerationPlan, RenderBatch, RenderJob, Worker, Queue, Provider Adapter, and Artifact models.

Status:

PARALLEL_LAB

### EV-H: Feedback, Learning and Automation

Problem:

Publication, performance feedback, business experiment learning, route learning, agent assistance, and Platform Core extraction belong after real repeated use.

MVP Handling:

Record the test question, approved output, citations, and review status. Do not implement publishing, analytics, agent runtime, or Platform Core.

Observed Evidence:

No publishing, feedback, agent, or Platform Core code exists.

Revisit Triggers:

- Approved packs are published and performance data becomes available.
- Operators need to compare concept outcomes.
- Fixed workflows become repetitive enough for reliable automation.
- The same mechanism repeats in at least two real modules and three product pilots.

Possible Direction:

Add performance snapshots, business learning, route learning, controlled automation, and eventually Platform Core extracted from validated repetition.

Status:

CAPTURED

## 3. Historical EV Mapping

| Prior EV | New Group |
|---|---|
| EV-001 Stage Gate Governance | EV-B |
| EV-002 Content Route Hypothesis | EV-B |
| EV-003 Route-specific Delivery Packs | EV-B / EV-G |
| EV-004 Project Priority and Portfolio | EV-A |
| EV-005 Experiment Contract and Performance Feedback | EV-B / EV-H |
| EV-006 Product Version, Sample and Batch Scope | EV-C |
| EV-007 Snapshot Freshness and Invalidation | EV-C / EV-D |
| EV-008 Decision Authority and Override | EV-B |
| EV-009 Source of Truth and External Synchronization | EV-C / EV-F |
| EV-010 Market Compliance and Rule Precedence | EV-D |
| EV-011 Store Health and Channel Context | EV-D |
| EV-012 AI Evaluation vs Business Outcome | EV-E / EV-H |
| EV-013 Progressive Forms and Operator Burden | EV-H |
| EV-014 Multi-market, Multi-store and Route Derivation | EV-A / EV-D |
| EV-015 Feedback, Learning and Selection Loop | EV-H |
| EV-016 Agent and Automation Enhancement | EV-H |
| EV-017 Portfolio-level Resource Competition | EV-A |
| EV-018 Snapshot and Evidence Correction | EV-C |
| EV-019 Business Rule Discovery from Real Usage | EV-H |

## 4. Backlog Use Rules

- Do not create code because a backlog item exists.
- Do not create empty directories for future capabilities.
- Revisit Trigger must be supported by real cases.
- First collect evidence, then update the relevant authority document or ADR.
- Do not write complete future schemas in the backlog.
