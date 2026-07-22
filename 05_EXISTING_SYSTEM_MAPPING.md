---
document_type: existing_system_mapping
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_2_EXISTING_SYSTEM_MAPPING
last_updated: 2026-07-22
change_policy: CHANGE_REQUEST_REQUIRED
depends_on:
  - 00_PRODUCT_SYSTEM_OVERVIEW.md
  - 01_MVP_WALKING_SKELETON.md
  - 03_TECHNICAL_ARCHITECTURE.md
---

# Existing System Mapping

## 1. Document Responsibility

This document records evidence-based mapping of candidate external or sibling systems.

It does not authorize code reuse, direct import, API calls, copying code, or implementation. It also does not mean those capabilities are implemented in this repository.

Current WS-1 can manually enter references. TikTok Search reuse is deferred to WS-3. Generation tools belong to Parallel Lab.

## 2. Mapping Rules

- Other repositories are evidence, not current implementation.
- Do not copy sibling repository code into this repository.
- Use adapters only after a future active iteration explicitly authorizes integration.
- Do not read `.env` or secrets.
- Do not call external APIs during documentation work.
- Reconfirm live capability before implementation because provider fields and endpoints may drift.
- Paths under `/Users/andy/Coding/...` come from the original MacBook scan.
- The current development host is Mac mini.
- MacBook paths are `NOT_CONFIRMED` on Mac mini until a future authorized scan confirms actual local repository path and commit.
- Do not treat MacBook paths as directly accessible paths on the current host.

## 3. Candidate Systems

| Repository / Tool | Source Host | Path | Current Development Host Availability | Confirmed Capability | Evidence | Reuse Decision | Adapter Boundary | Needed in Current Walking Skeleton? | Risks |
|---|---|---|---|---|---|---|---|---|---|
| tiktok-reference-finder | MacBook | `/Users/andy/Coding/tiktok-reference-finder` | NOT_CONFIRMED on Mac mini | TikTok reference discovery, Scrape Creators endpoint registry, scoring, export, offline fixture mode | README, search service, endpoint config, tests were found in prior mapping | WRAP_WITH_ADAPTER | Future `TikTokSearchAdapter` or reference adapter | No for WS-1; revisit WS-3 | Streamlit/SQLite assumptions, live credentials, provider drift |
| video_search_tk | MacBook | `/Users/andy/Coding/video_search_tk` | NOT_CONFIRMED on Mac mini | Competitor video search, explainable analysis, manual review, Feishu CSV export | README, Scrape Creators client, analysis schema | WRAP_WITH_ADAPTER | Future Reference Workspace adapter | No for WS-1; revisit WS-3 | Streamlit assumptions, endpoint verification, CSV is not Feishu API |
| video_clip_extractor | MacBook | `/Users/andy/Coding/video_clip_extractor` | NOT_CONFIRMED on Mac mini | Batch video preprocessing, metadata, dedupe, scene detection, keyframes, proxies | README, Python project files, idempotency tests | WRAP_WITH_ADAPTER | Future `ReferenceMediaAdapter` | No | ffmpeg and video dependencies; not needed for first manual references |
| video_creator_tool | MacBook | `/Users/andy/Coding/video_creator_tool` | NOT_CONFIRMED on Mac mini | Script, storyboard, shot, production task, Seedance provider reference | README and backend model/provider file evidence | REFERENCE_ONLY | Future production or generation reference only | No | Scope may include production-stage assumptions outside MVP |
| video_decision_engine | MacBook | `/Users/andy/Coding/video_decision_engine` | NOT_CONFIRMED on Mac mini | Product analysis, pattern matching, script/storyboard schema ideas | README, JSON schemas, modules, tests | REFERENCE_ONLY | Conceptual reference only | No | Older architecture may conflict with current Walking Skeleton |
| Seedance / ComfyUI related experiments | MacBook | `/Users/andy/Coding/seedance/seedance-2.0`, `/Users/andy/Coding/video_copy/seedance_video_tool`, and possible lab paths | NOT_CONFIRMED on Mac mini | Seedance skill/package material; some script parsing; no confirmed current main-system integration | README and skill files; prior mapping did not confirm a current ComfyUI/Kling implementation | PARALLEL_LAB_ONLY | Future Generation Lab boundary | No | Generation can pollute main domain model if introduced too early |
| SKU_lib | MacBook | `/Users/andy/Coding/SKU_lib` | NOT_CONFIRMED on Mac mini | Product/SKU domain and governance reference material | AGENTS, domain docs, backend skeleton files | NEEDS_MANUAL_CONFIRMATION | Possible product language reference only | No | Different business context |
| tk_product_page_agent | MacBook | `/Users/andy/Coding/tk_product_page_agent` | NOT_CONFIRMED on Mac mini | Product readiness, benefit claim/proof, TikTok Shop platform rule knowledge materials | Knowledge base files in Custom GPT upload area | REFERENCE_ONLY | Manual knowledge reference; not code | No | Knowledge docs are not an executable integration |
| sku-video-pack-engine | Unknown | Unknown | NOT_CONFIRMED on Mac mini | Not confirmed | No exact repository or file path found in prior scan | NEEDS_MANUAL_CONFIRMATION | None until located | No | Must not assume it exists |

## 4. Current Walking Skeleton Decisions

| Capability | Current Decision |
|---|---|
| Product / ProductVersion / Evidence | Current repository will implement only after an approved active iteration. |
| Reference | WS-1 uses manual entry. |
| TikTok Search | Deferred to WS-3 and must use an adapter. |
| Video breakdown | Deferred to WS-3 or later. |
| Script / Storyboard / Shot ideas | May inform future design, but no direct reuse now. |
| Feishu | Not confirmed as API integration; treat as future adapter. |
| Seedance / ComfyUI / Kling | Parallel Lab only, not main Walking Skeleton implementation. |

## 5. Reuse Boundaries

### TikTok Search

`tiktok-reference-finder` and `video_search_tk` are candidate sources for future adapter work. The choice is not frozen.

WS-1 does not need TikTok search.

### Reference Media

`video_clip_extractor` may become a future media processing adapter source.

WS-1 does not need video processing.

### Generation Lab

Generation Lab may independently validate:

- ComfyUI Workflow.
- API Workflow JSON.
- Binding Manifest.
- Single-task submission.
- Single-task result collection.
- Seedance single-task validation.
- Speed, success rate, and resource consumption.

Generation Lab must not introduce GenerationPlan, RenderBatch, RenderJob, Provider Routing, Worker, Queue, or Artifact into the main domain model before main-system evidence exists.

## 6. Manual Confirmations Needed Later

- Confirm actual Mac mini repository paths and commits before any reuse decision becomes implementable.
- Which reference search tool should back a future TikTokSearchAdapter.
- Whether `video_clip_extractor` should back future reference media processing.
- Whether `video_creator_tool` contains reusable Owned Pack logic or only older production-stage experiments.
- Whether `sku-video-pack-engine` exists under another path.
- Whether Feishu should remain CSV import/export or become API automation later.
