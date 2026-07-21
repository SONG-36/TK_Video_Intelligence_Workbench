---
document_type: technical_baseline
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.1"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_3_IMPLEMENTATION_PREPARATION
last_updated: 2026-07-21
change_policy: CHANGE_REQUEST_REQUIRED
depends_on:
  - 06_RELEASE_1A_MVP_SCOPE.md
  - 07_RELEASE_1A_IMPLEMENTATION_PLAN.md
  - 09_EXISTING_SYSTEM_MAPPING.md
  - architecture/01_PLATFORM_ARCHITECTURE.md
---

# 10_RELEASE_1A_TECHNICAL_BASELINE

## 1. 文档职责

本文档定义 Release 1A 的最小技术方案和代码边界。

它不是完整 Low-Level Design，不冻结最终 API、数据库 Schema、页面布局或部署方案。它只为 Phase I1 Product Workspace 建立可实施基线。

本文档不直接授权代码实现。代码目录将在 Phase I1 正式任务中创建。

---

## 2. 技术基线

Release 1A 使用：

- Backend：Python + FastAPI。
- Frontend：React + TypeScript。
- Database：PostgreSQL。
- Database Migration：Alembic。
- Backend Validation：Pydantic。
- ORM：SQLAlchemy 2.x。
- Backend Testing：pytest。
- Frontend Testing：Vitest + Testing Library；Playwright 仅用于后续端到端烟测。
- Object Storage：本地开发使用文件系统 Adapter，接口允许以后替换 S3 / MinIO。
- Architecture：Modular Monolith。
- AI Output：Structured Outputs。
- Workflow：Fixed Workflow First。
- External Integration：Adapter Boundary。

本任务不得安装上述依赖。

选择 SQLAlchemy 2.x 的原因：

- 与 FastAPI、Alembic、PostgreSQL 组合成熟。
- Existing System Mapping 中旧 workbench 已有 SQLAlchemy 2.x / Alembic / PostgreSQL 证据，可作为工程参考。
- I1 需要清晰关系约束和迁移策略，不需要引入更复杂的数据层框架。

---

## 3. 建议代码目录

Phase I1 只需要 Product Workspace，因此最终建议结构应保持窄而浅：

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── core/
│   │   ├── modules/
│   │   │   └── product/
│   │   │       ├── domain/
│   │   │       ├── application/
│   │   │       ├── infrastructure/
│   │   │       └── api/
│   │   ├── infrastructure/
│   │   │   ├── database/
│   │   │   └── storage/
│   │   └── main.py
│   ├── tests/
│   │   └── product/
│   ├── migrations/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── features/
│   │   │   └── products/
│   │   └── shared/
│   └── package.json
└── deploy/
    └── docker-compose.dev.yml
```

This is a recommended target for Phase I1, not a directory creation instruction for Phase I0.

Do not create:

- Independent Kernel service.
- Independent Agent service.
- Microservice directories.
- Generic Workflow Engine.
- Empty modules for EV-001～EV-019.
- Reference, Creative, Script, Storyboard, Shot, Publication, or Performance modules during I1.

Rationale:

- `backend/app/modules/product/` can contain Product, ProductVersion, and Evidence without forcing future module boundaries.
- `backend/app/infrastructure/storage/` is enough for local file storage adapter.
- `frontend/src/features/products/` supports Product Workspace only.
- `deploy/docker-compose.dev.yml` is enough for local PostgreSQL later; production deploy is out of scope.

---

## 4. Local Development Scheme

### Backend

Expected later command shape:

```text
cd backend
uvicorn app.main:app --reload
```

Backend configuration should use environment variables parsed through a typed settings object. Runtime secrets must not be committed.

### Frontend

Expected later command shape:

```text
cd frontend
npm run dev
```

Frontend should call the backend through a configurable API base URL.

### PostgreSQL

Local development may use either Homebrew PostgreSQL or Docker Compose PostgreSQL. The default developer path should be documented in Phase I1 before code creation.

Database migrations should use Alembic:

```text
cd backend
alembic upgrade head
```

### File Upload Storage

I1 local file uploads should use a filesystem-backed `FileStorageAdapter`.

Minimum behavior:

- Store original Evidence file.
- Preserve original filename as metadata.
- Generate an internal stored filename or object key.
- Never overwrite existing approved or historical Evidence silently.

### Configuration and `.env.example`

`.env.example` should contain names and safe placeholders only. It must not contain real credentials.

Candidate names:

```text
APP_ENV=local
DATABASE_URL=postgresql+psycopg://workbench:workbench@localhost:5432/workbench
FILE_STORAGE_ROOT=./storage
BACKEND_CORS_ORIGINS=http://127.0.0.1:5173
```

### Tests

Expected later command shape:

```text
cd backend
pytest

cd frontend
npm run test
```

### macOS / arm64 Notes

- Prefer Python 3.12.
- Prefer PostgreSQL 16 or later.
- Homebrew paths may differ between Apple Silicon and Intel machines.
- Native dependencies should be introduced only when required by the active slice.

---

## 5. Adapter Boundaries

Candidate future Adapters:

| Adapter | Responsibility | I1 Status |
|---|---|---|
| TikTokSearchAdapter | Search TikTok references and normalize provider responses | Not needed in I1 |
| ReferenceMediaAdapter | Process saved reference media, clips, keyframes, and analysis inputs | Not needed in I1 |
| AIModelAdapter | Call structured-output model providers | Not needed in I1 unless no-AI stubs are explicitly replaced later |
| FileStorageAdapter | Store uploaded Evidence files locally and allow future S3 / MinIO replacement | Needed in I1 |
| FutureFeishuAdapter | Import/export Feishu records or files | Not needed in I1 |

I1 Product Workspace should only implement `FileStorageAdapter` if file upload is included in the slice. It must not implement TikTok, Reference Media, AI Model, or Feishu adapters.

ComfyUI, Seedance, and Kling are not part of Release 1A current implementation scope.

---

## 6. Non-functional Baseline

Minimum non-functional requirements:

- Stable IDs.
- Version History.
- Auditability.
- Human Approval.
- Input Validation.
- Error Visibility.
- Testability.
- Local Reproducibility.

Out of scope:

- Enterprise high availability.
- Distributed scaling.
- Multi-tenant SaaS.
- Centralized identity and organization management.
- Generic workflow orchestration.

---

## 7. Phase I1 Technical Guardrails

- Implement only Product, ProductVersion, and Evidence.
- Keep schema limited to I1 requirements.
- Prefer explicit constraints over implicit UI-only rules.
- Keep external integrations stubbed or absent unless required by I1.
- Do not import code from sibling repositories during I1.
- Document any divergence from this baseline before coding.
