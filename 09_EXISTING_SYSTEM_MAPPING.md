---
document_type: existing_system_mapping
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.1"
status: BASELINE_CANDIDATE
implementation_allowed: false
authority: LEVEL_3_IMPLEMENTATION_PREPARATION
last_updated: 2026-07-21
change_policy: CHANGE_REQUEST_REQUIRED
depends_on:
  - 06_RELEASE_1A_MVP_SCOPE.md
  - 07_RELEASE_1A_IMPLEMENTATION_PLAN.md
  - 08_LONG_TERM_EVOLUTION_BACKLOG.md
---

# 09_EXISTING_SYSTEM_MAPPING

## 1. 文档职责

本文档记录 Phase I0 对 `/Users/andy/Coding` 的只读 Existing System Mapping。

目的：

- 识别用户已有仓库、代码和外部能力。
- 避免在 Release 1A 中重复开发已有能力。
- 明确哪些能力只能通过 Adapter 接入。
- 明确哪些能力只属于未来阶段，不能进入 Phase I1。

本文档不构成代码复用授权，不允许复制其他仓库代码。所有复用结论都需要在正式实施前再次人工确认。

---

## 2. 扫描范围与方法

只读扫描范围：

```text
/Users/andy/Coding
```

执行过的只读检查：

```text
find /Users/andy/Coding -maxdepth 2 -type d | sort
find /Users/andy/Coding -maxdepth 3 -type f \
  \( -name README.md -o -name AGENTS.md -o -name pyproject.toml \
  -o -name requirements.txt -o -name package.json -o -name docker-compose.yml \) | sort
find /Users/andy/Coding -maxdepth 3 -type f | rg -i \
  'TikTok|growth|search|ScrapeCreators|scrape|creator|reference|video|script|storyboard|sku-video-pack|feishu|comfyui|seedance|kling'
```

Additional targeted reads were limited to README, dependency manifest, and file-list evidence. `.env` files were not read.

---

## 3. Candidate Systems

| Repository / Tool Name | Path | Purpose | Language / Framework | Current Status | Relevant Capability | Evidence of Existence | Reuse Option | Integration Boundary | Risks | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|---|
| TikTok Reference Finder | `/Users/andy/Coding/tiktok-reference-finder` | Local/LAN Streamlit app for TikTok reference discovery, enrichment, scoring, persistence, and export | Python 3.12, Streamlit, httpx, pandas, SQLite, Pydantic, PyYAML, pytest | Implemented local app with tests and offline fixture mode | TikTok keyword/search/reference discovery, Scrape Creators endpoint registry, reference scoring, export | `README.md`; `api/scrape_creators_registry_client.py`; `services/growth_search.py`; `config/scrape_creators_endpoints.yaml`; `tests/test_growth_search.py` | WRAP_WITH_ADAPTER | Future `TikTokSearchAdapter` and possibly `ReferenceMediaAdapter`; no direct import during I1 | Streamlit + SQLite architecture differs from Release 1A FastAPI/PostgreSQL baseline; live API requires credentials; provider fields may drift | Do not copy code. After I1, evaluate adapter wrapper for Reference Workspace. |
| TikTok Competitor Video Filter | `/Users/andy/Coding/video_search_tk` | Local Streamlit tool for searching competitor TikTok videos, explainable analysis, manual review, and Feishu CSV export | Python, Streamlit, httpx, Pydantic, pandas, OpenAI, pytest | Implemented local tool per README | Competitor reference video search, Scrape Creators client, video first-three-second handling, Feishu CSV export | `README.md`; `pyproject.toml`; `src/tiktok_filter/scrape_creators_client.py`; `configs/analysis_schema.json` | WRAP_WITH_ADAPTER | Future Reference Workspace Adapter; Feishu export is CSV-only evidence, not API integration | Uses Streamlit and local app assumptions; endpoint constants require verification; not suitable for I1 Product Workspace | Reference for Reference Workspace; manual confirmation before adapter extraction. |
| Legacy TikTok Video Intelligence Workbench | `/Users/andy/Coding/tiktok-video-intelligence-workbench` | Earlier FastAPI/React/PostgreSQL workbench with provider validation slice | FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, PostgreSQL, React, Vite, TanStack Query, Zod, Vitest, Playwright | Implemented health page, internal search-job APIs, worker, provider fixtures, migrations | Technical baseline patterns, local dev commands, PostgreSQL/Alembic setup, provider adapter boundaries | `README.md`; `backend/pyproject.toml`; `frontend/package.json`; `docker-compose.yml`; `backend/app/main.py`; `docs/decisions/0001-repository-boundaries.md` | REFERENCE_ONLY | Use as architecture and tooling reference only; do not merge or import code into current repo without explicit migration decision | Scope differs from current canonical docs; contains `agents/` and provider job machinery beyond I1 | Use to validate technical baseline choices and local dev plan. Avoid direct reuse in I1. |
| Business Clip Extractor | `/Users/andy/Coding/video_clip_extractor` | Batch video preprocessing: scan, metadata, dedupe, scene detection, keyframes, proxy generation | Python CLI, SQLite, ffmpeg/ffprobe, PySceneDetect, pytest | V0.1 implemented per README | Reference media preprocessing and future video breakdown support | `README.md`; `pyproject.toml`; `src/`; `tests/test_pipeline_idempotency.py` | WRAP_WITH_ADAPTER | Future `ReferenceMediaAdapter`; not needed for I1 | Requires ffmpeg and video processing dependencies; not a Product Workspace capability | Keep out of I1. Revisit during Reference Workspace or production-media preparation. |
| Video Creator Tool | `/Users/andy/Coding/video_creator_tool` | AI short video production assistant workspace with scripts, storyboard, shots, Seedance provider files | FastAPI-style backend, SQLAlchemy, OpenAI, frontend package, tests | README says initialization, but backend file list shows substantial production models/services/tests | Script, storyboard, shot, production task, Seedance provider, generation review | `README.md`; `backend/app/models/script.py`; `backend/app/models/storyboard.py`; `backend/app/models/shot.py`; `backend/app/providers/seedance_provider.py`; `tests/test_storyboard_api.py` | REFERENCE_ONLY | Future Owned Content Production Pack and production-stage reference; no I1 adapter | Current scope likely diverges; may include production-stage assumptions outside Release 1A; direct reuse could import premature video-generation concepts | Do not reuse for I1. Review manually before I5 Owned Pack planning. |
| Video Decision Engine | `/Users/andy/Coding/video_decision_engine` | Short Video Commercial Content Decision Engine with schema-first pipeline ideas | Python app, JSON schemas, tests | V0.1 MVP with product analysis and pattern matching modules | Product analysis, pattern matching, script/storyboard schema ideas | `README.md`; `schemas/product.schema.json`; `modules/product_analysis/analyzer.py`; `tests/test_product_analysis.py` | REFERENCE_ONLY | Conceptual reference for schema-first modeling; no direct import | Older architecture may conflict with Release 1A bounded scope; includes future script/storyboard modules | Use as reference when designing I2+ schemas; not I1 implementation source. |
| Seedance 2.0 Skill OS | `/Users/andy/Coding/seedance/seedance-2.0` | Skill OS for directing Seedance 2.0 video generations | Documentation and skill package | Implemented skill package per README | Future prompt/production guidance for Seedance video generation | `README.md`; `SKILL.md`; `references/platform-surface-matrix.md` | DO_NOT_REUSE | Future production-stage knowledge source only | Seedance generation is explicitly outside Release 1A current scope and outside I1 | Do not integrate in Release 1A I1. Keep in Evolution Backlog / future production stage. |
| Seedance Video Production Workbench | `/Users/andy/Coding/video_copy/seedance_video_tool` | Streamlit parser/display for Seedance video production scripts | Python, Streamlit | Phase 1 only; no Seedance API per README | VideoScript and Shot schema ideas | `README.md`; `app.py`; `requirements.txt` | REFERENCE_ONLY | Future production pack reference only | Not relevant to Product Workspace; no implemented Seedance API | Do not use in I1. Revisit during I5 if needed. |
| SKU_lib | `/Users/andy/Coding/SKU_lib` | SKU/product library project with extensive product/domain/contracts/architecture docs and backend skeleton | Python backend docs and deploy files | Existing repository with governance and documentation | Product/SKU domain thinking and documentation governance patterns | `AGENTS.md`; `docs/03-domain/02_领域模型.md`; `apps/backend/pyproject.toml`; `deploy/docker-compose.yml` | NEEDS_MANUAL_CONFIRMATION | Possible reference for Product/ProductVersion domain language only | Purpose and business context differ; no TikTok content-specific capability found in scan | Do not reuse directly. Manually inspect only if Product domain ambiguity appears. |
| tk_product_page_agent | `/Users/andy/Coding/tk_product_page_agent` | TikTok Shop product page and PDP knowledge/skill materials | Docs, Custom GPT materials, research knowledge base | Knowledge-base project | Product readiness, claim/proof, category rules, TikTok Shop platform rules | `custom_gpt_upload/KB_01_product_information_and_readiness.md`; `KB_03_benefit_claim_and_proof.md`; `KB_06_tiktok_shop_platform_rules.md` | REFERENCE_ONLY | Knowledge reference only; not code | Contains knowledge docs and downloaded open-source repos; not a Release 1A code dependency | Use manually as policy/product-copy reference if needed; do not import. |

---

## 4. Required Findings

### 4.1 TikTok Growth Search

Confirmed as existing in `tiktok-reference-finder`.

Evidence:

- `README.md` states the independent `内容增长搜索` page is under `pages/01_内容增长搜索.py`.
- `services/growth_search.py` exists.
- `config/growth_content.yaml` exists.
- `tests/test_growth_search.py` exists.

Decision:

- Reuse option: WRAP_WITH_ADAPTER.
- Not needed for Phase I1.
- Revisit for Reference Workspace.

### 4.2 Scrape Creators Client

Confirmed in two repositories.

Evidence:

- `tiktok-reference-finder/api/scrape_creators_registry_client.py`
- `tiktok-reference-finder/config/scrape_creators_endpoints.yaml`
- `video_search_tk/src/tiktok_filter/scrape_creators_client.py`

Decision:

- Reuse option: WRAP_WITH_ADAPTER.
- Must not be directly imported into current repo without an Adapter and manual confirmation.
- Live API calls must remain disabled until explicitly authorized.

### 4.3 Video Breakdown Capability

Confirmed as code in multiple forms, but not yet mapped to Release 1A.

Evidence:

- `video_search_tk` README describes first-three-second processing and explainable analysis.
- `video_clip_extractor` README describes ffprobe, scene detection, keyframes, proxies, SQLite, and JSON manifests.

Decision:

- Reuse option: WRAP_WITH_ADAPTER or REFERENCE_ONLY depending on later Reference Workspace needs.
- Not part of I1 Product Workspace.

### 4.4 sku-video-pack-engine

No repository or file path with exact `sku-video-pack-engine` evidence was found in the scan.

Nearby but not equivalent evidence:

- `video_creator_tool` has script/storyboard/shot/production models and services.
- `video_decision_engine` has script/storyboard/shot schemas.

Decision:

- Reuse option: NEEDS_MANUAL_CONFIRMATION.
- Do not assume `sku-video-pack-engine` exists.

### 4.5 Feishu Input / Output

No Feishu API integration code was confirmed.

Evidence:

- `video_search_tk` README documents CSV export for Feishu multidimensional table import.
- Search for `feishu`, `lark`, and `飞书` under `/Users/andy/Coding` produced no code evidence at the scanned depth.

Decision:

- Reuse option: NEEDS_MANUAL_CONFIRMATION.
- Treat Feishu as future `FutureFeishuAdapter`.
- I1 must not depend on Feishu.

### 4.6 ComfyUI, Seedance, Kling

Seedance-related repositories exist. ComfyUI and Kling local implementation were not confirmed.

Evidence:

- `seedance/seedance-2.0/README.md` describes a Seedance 2.0 Skill OS.
- `video_copy/seedance_video_tool/README.md` says Seedance API is not implemented.
- No current local ComfyUI or Kling implementation was confirmed by file evidence.

Decision:

- Reuse option: DO_NOT_REUSE for I1.
- These belong to future production-stage discussion, not Release 1A Product Workspace.

---

## 5. Integration Decisions for Release 1A

| Capability | Phase I1 Need | Decision |
|---|---|---|
| Product/ProductVersion/Evidence | Required | Implement inside current repo in Phase I1. Do not reuse external code. |
| TikTok Search | Not required | Defer to Reference Workspace; wrap later through `TikTokSearchAdapter`. |
| Reference video analysis | Not required | Defer to Reference Workspace; likely Adapter around existing tools. |
| Script/Storyboard/Shot models | Not required | Defer to I5; use existing repos as reference only. |
| Feishu | Not required | Future adapter only. |
| Seedance/ComfyUI/Kling | Not required | Out of Release 1A I1 and current MVP production boundary. |

---

## 6. Manual Confirmations Needed

- Whether `tiktok-reference-finder` or `video_search_tk` is the preferred source for future TikTok Search Adapter.
- Whether `video_clip_extractor` should become the basis for future ReferenceMediaAdapter.
- Whether `video_creator_tool` contains reusable Owned Pack logic or only older production-stage experiments.
- Whether `sku-video-pack-engine` exists under another path not discovered by this scan.
- Whether Feishu integration should remain CSV export/import or require API automation in a later release.
