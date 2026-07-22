---
document_type: technical_architecture
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_2_TECHNICAL_ARCHITECTURE
last_updated: 2026-07-22
change_policy: ADR_REQUIRED_AFTER_APPROVAL
depends_on:
  - 00_PRODUCT_SYSTEM_OVERVIEW.md
  - 01_MVP_WALKING_SKELETON.md
  - 02_DOMAIN_MODEL.md
  - 05_EXISTING_SYSTEM_MAPPING.md
  - architecture/ADR_LOG.md
---

# 技术架构

## 1. 文档职责

本文档定义当前 Walking Skeleton 的技术架构方向。

本文档不是 Low-level Design、最终目录结构、依赖清单、部署计划、数据库 Schema 或 API 契约。

## 2. 技术栈

当前技术栈方向：

| 领域 | 选择 |
|---|---|
| Backend | Python 3.12 |
| API | FastAPI |
| Validation | Pydantic |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL |
| Migration | Alembic |
| Backend tests | pytest |
| Frontend | React |
| Frontend language | TypeScript |
| Frontend tooling | Vite |
| Frontend tests | Vitest |
| Local infrastructure | 只有被 active iteration 明确授权时才使用 Docker |

本次文档本地化不安装依赖，也不创建代码目录。

## 3. 架构风格

采用：

```text
Modular Monolith
+
Production-intent Walking Skeleton
+
Fixed Workflow First
+
Provider Adapter
+
Human Review
```

中文含义：

- Modular Monolith：模块化单体。
- Production-intent Walking Skeleton：生产意图型最小贯通骨架。
- Fixed Workflow First：先固定 Workflow，再考虑动态编排。
- Provider Adapter：通过服务提供方适配器隔离外部能力。
- Human Review：正式内容必须人工审核。

影响：

- 第一条真实业务链要薄但端到端。
- 从第一版开始认真处理稳定 ID、来源可追溯性、版本、审核、迁移和 Adapter 边界。
- 在真实重复证明必要前，不创建通用 Workflow 平台。
- 外部 Provider 必须通过 Adapter 隔离。
- AI 输出在 Human Review 前始终是 Draft。

## 4. 建议模块

概念上可以包含：

- `product`。
- `reference`。
- `content`。
- `delivery`。

这些不是目录创建指令。

只有被批准的 active iteration 实际需要时，才创建代码目录。不要为未来能力创建空模块。

## 5. 平台边界

此前的平台观察维度仍然有用：

- Resource。
- Capability。
- Execution。
- Policy。
- Trace。

它们是长期平台观察维度，不是当前实现 Kernel Framework 的要求。

当前工作不得实现：

- Resource Framework。
- Capability Registry。
- Execution Engine。
- Policy DSL。
- Trace Service。
- Agent Runtime。

未来术语优先使用：

```text
Platform Core
```

不要把当前架构夸大成 Linux-kernel-style 平台。

## 6. Platform Core 抽取规则

只有满足以下条件时，才考虑把共享机制抽取为 Platform Core：

```text
The same mechanism repeats in at least two real business modules
+
three real product pilots validate the need
```

在此之前，优先在 Walking Skeleton 内使用直接的 application logic。

## 7. AI 边界

规则：

- AI 输出默认是 Draft。
- AI 生成的业务产物使用 structured outputs。
- Prompt 和 Knowledge Pack version 必须可追溯。
- Run 记录必须保留 input versions、model/provider、output version、cost 和 errors。
- 外部模型通过 Adapter 访问。
- 当前 workflow 是固定且人工触发的。
- 不实现 multi-agent runtime。

首轮实现要求：

- 使用真实、版本化的 Knowledge Pack v0.1。
- 该 pack 可以在已批准的 active iteration 中用 Markdown / YAML 表达。
- 必须包含 Script Rules、Pattern Cards、Hook Guidance、Claims Guardrails、Review Rubric 和 Market Style Notes。
- AI Run 记录必须包含所用 Knowledge Pack version。
- 当前 MVP 不建设知识库 UI、搜索、标签或管理平台。
- 本次文档本地化不创建 `knowledge/` 目录或文件。

## 8. 既有系统集成

既有兄弟仓库和工具可以为未来实现提供参考，但它们不是当前系统代码。

集成规则：

- TikTok search 通过未来 `TikTokSearchAdapter`。
- Video breakdown 通过未来 reference media adapter。
- Generation Lab 通过独立 generation adapters 或 lab tooling。
- 不直接复制兄弟仓库代码。
- 未经明确授权，不调用 live external API。

详细证据见 [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md)。

## 9. Generation 边界

当前主系统边界：

```text
Generation-ready Production Pack
→ Future Generation Adapter Boundary
```

当前 MVP 不建模或实现：

- GenerationPlan。
- RenderBatch。
- RenderJob。
- Worker。
- Queue。
- Provider routing。
- Automatic batch costing。
- ComfyUI / Seedance / Kling orchestration。

详细 Generation Orchestration 延期到 [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md)。

## 10. 非功能基线

当前基线：

- Stable ID。
- Provenance。
- Versioning。
- Human Approval。
- Migration。
- Error Visibility。
- Testability。
- Local Reproducibility。

当前范围之外：

- Enterprise high availability。
- Multi-tenant SaaS infrastructure。
- Kubernetes。
- Microservices。
- Generic distributed workflow orchestration。

## 11. 本地开发方向

未来 active iteration 只有在明确授权时，才可以创建 backend、frontend、database 和 Docker 文件。

在此之前：

- 保持仓库 documentation-first。
- 不安装依赖。
- 不启动 Docker。
- 不创建 `.env` 文件。
- 不读取密钥。
