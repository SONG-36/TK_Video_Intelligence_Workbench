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

# 既有系统映射

## 1. 文档职责

本文档记录候选外部系统或兄弟仓库的证据化映射。

本文档不授权代码复用、直接 import、API 调用、复制代码或实施。本文档也不表示这些能力已经在当前仓库中实现。

当前 WS-1 可以手工录入 Reference。TikTok Search 复用延期到 WS-3。Generation tools 属于 Parallel Lab。

## 2. 映射规则

- 其他仓库是证据，不是当前实现。
- 不得把兄弟仓库代码复制进当前仓库。
- 只有未来 active iteration 明确授权集成时，才可以通过 Adapter 使用。
- 不读取 `.env` 或密钥。
- 文档工作期间不调用外部 API。
- 实施前必须重新确认 live capability，因为 provider fields 和 endpoints 可能变化。
- `/Users/andy/Coding/...` 下的路径来自原 MacBook 扫描。
- 当前主开发机是 Mac mini。
- MacBook 路径在 Mac mini 上均为 `NOT_CONFIRMED`，直到未来授权扫描确认实际本地仓库路径和 commit。
- 不得把 MacBook 路径当作当前主机可直接访问路径。

## 3. 候选系统

| Repository / Tool | Source Host | Path | Current Development Host Availability | Confirmed Capability | Evidence | Reuse Decision | Adapter Boundary | Needed in Current Walking Skeleton? | Risks |
|---|---|---|---|---|---|---|---|---|---|
| tiktok-reference-finder | MacBook | `/Users/andy/Coding/tiktok-reference-finder` | NOT_CONFIRMED on Mac mini | TikTok reference discovery, Scrape Creators endpoint registry, scoring, export, offline fixture mode | README、search service、endpoint config、tests 在此前 mapping 中被发现 | WRAP_WITH_ADAPTER | Future `TikTokSearchAdapter` or reference adapter | No for WS-1; revisit WS-3 | Streamlit/SQLite assumptions、live credentials、provider drift |
| video_search_tk | MacBook | `/Users/andy/Coding/video_search_tk` | NOT_CONFIRMED on Mac mini | Competitor video search、explainable analysis、manual review、Feishu CSV export | README、Scrape Creators client、analysis schema | WRAP_WITH_ADAPTER | Future Reference Workspace adapter | No for WS-1; revisit WS-3 | Streamlit assumptions、endpoint verification、CSV is not Feishu API |
| video_clip_extractor | MacBook | `/Users/andy/Coding/video_clip_extractor` | NOT_CONFIRMED on Mac mini | Batch video preprocessing、metadata、dedupe、scene detection、keyframes、proxies | README、Python project files、idempotency tests | WRAP_WITH_ADAPTER | Future `ReferenceMediaAdapter` | No | ffmpeg 和 video dependencies；首轮 manual references 不需要 |
| video_creator_tool | MacBook | `/Users/andy/Coding/video_creator_tool` | NOT_CONFIRMED on Mac mini | Script、storyboard、shot、production task、Seedance provider reference | README 和 backend model/provider file evidence | REFERENCE_ONLY | Future production or generation reference only | No | 作用域可能包含 MVP 之外的 production-stage assumptions |
| video_decision_engine | MacBook | `/Users/andy/Coding/video_decision_engine` | NOT_CONFIRMED on Mac mini | Product analysis、pattern matching、script/storyboard schema ideas | README、JSON schemas、modules、tests | REFERENCE_ONLY | Conceptual reference only | No | 旧架构可能与当前 Walking Skeleton 冲突 |
| Seedance / ComfyUI related experiments | MacBook | `/Users/andy/Coding/seedance/seedance-2.0`, `/Users/andy/Coding/video_copy/seedance_video_tool`, and possible lab paths | NOT_CONFIRMED on Mac mini | Seedance skill/package material；部分 script parsing；未确认当前主系统集成 | README and skill files；prior mapping did not confirm a current ComfyUI/Kling implementation | PARALLEL_LAB_ONLY | Future Generation Lab boundary | No | 如果过早进入主领域模型，会污染 Generation 边界 |
| SKU_lib | MacBook | `/Users/andy/Coding/SKU_lib` | NOT_CONFIRMED on Mac mini | Product/SKU domain and governance reference material | AGENTS、domain docs、backend skeleton files | NEEDS_MANUAL_CONFIRMATION | Possible product language reference only | No | 业务上下文不同 |
| tk_product_page_agent | MacBook | `/Users/andy/Coding/tk_product_page_agent` | NOT_CONFIRMED on Mac mini | Product readiness、benefit claim/proof、TikTok Shop platform rule knowledge materials | Custom GPT upload area 中的 knowledge base files | REFERENCE_ONLY | Manual knowledge reference; not code | No | Knowledge docs 不是可执行集成 |
| sku-video-pack-engine | Unknown | Unknown | NOT_CONFIRMED on Mac mini | Not confirmed | 此前扫描未发现精确 repository 或 file path | NEEDS_MANUAL_CONFIRMATION | None until located | No | 不得假设它存在 |

## 4. 当前 Walking Skeleton 决策

| 能力 | 当前决策 |
|---|---|
| Product / ProductVersion / Evidence | 只有在 approved active iteration 后，才在当前仓库实现。 |
| Reference | WS-1 使用 manual entry。 |
| TikTok Search | 延期到 WS-3，且必须使用 adapter。 |
| Video breakdown | 延期到 WS-3 或更晚。 |
| Script / Storyboard / Shot ideas | 可作为未来设计参考，但当前不直接复用。 |
| Feishu | 未确认为 API integration；视为 future adapter。 |
| Seedance / ComfyUI / Kling | 仅属于 Parallel Lab，不属于主 Walking Skeleton 实现。 |

## 5. 复用边界

### TikTok Search

`tiktok-reference-finder` 和 `video_search_tk` 是未来 adapter 工作的候选来源。当前不冻结选择。

WS-1 不需要 TikTok search。

### Reference Media

`video_clip_extractor` 未来可能成为 media processing adapter 来源。

WS-1 不需要 video processing。

### Generation Lab

Generation Lab 可以独立验证：

- ComfyUI Workflow。
- API Workflow JSON。
- Binding Manifest。
- Single-task submission。
- Single-task result collection。
- Seedance single-task validation。
- Speed、success rate 和 resource consumption。

在主系统证据出现前，Generation Lab 不得把 GenerationPlan、RenderBatch、RenderJob、Provider Routing、Worker、Queue 或 Artifact 引入主领域模型。

## 6. 后续人工确认项

- 任何复用决策进入可实施状态前，必须确认 Mac mini 上的实际仓库路径和 commit。
- 哪个 reference search tool 应支持未来 TikTokSearchAdapter。
- `video_clip_extractor` 是否应支持未来 reference media processing。
- `video_creator_tool` 包含可复用 Owned Pack logic，还是仅为旧 production-stage experiments。
- `sku-video-pack-engine` 是否存在于其他路径。
- Feishu 后续应保持 CSV import/export，还是升级为 API automation。
