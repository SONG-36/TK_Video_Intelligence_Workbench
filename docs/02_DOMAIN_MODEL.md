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

# 领域模型

## 1. 文档职责

本文档定义当前 Walking Skeleton 的业务概念与关系。

本文档不是数据库 Schema、最终 API 契约、完整 DDD 模型或未来对象目录。

## 2. 当前核心对象

| 对象 | 业务职责 |
|---|---|
| `ContentProject` | 一条内容决策链的工作容器。 |
| `OperatingContextSnapshot` | Selection-to-Content Handoff 与目标运营上下文。 |
| `Product` | 稳定商品身份。 |
| `ProductVersion` | Evidence 适用的供应商、样品、型号、包装或配置版本。 |
| `Evidence` | 商品声明、观察、测试、图片、视频、链接或备注的来源资料。 |
| `KnowledgePack` | AI Run 使用的版本化逻辑内容知识包。 |
| `Reference` | 手工录入或未来由 Adapter 获取的市场/参考内容。 |
| `CreativeConcept` | AI 草稿或人工修改后的内容构想候选。 |
| `ScriptPack` | 聚合 script、storyboard、shots 和 generation-ready notes 的内容包。 |
| `Review` | 针对目标资源的人工审核决策。 |
| `Run` | AI 或自动处理的追踪记录。 |

## 3. 最小关系

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

Handoff 存储为 `OperatingContextSnapshot` 的一部分。

最小字段：

| 字段 | 含义 |
|---|---|
| `selection_rationale` | 为什么这个商品进入内容阶段。 |
| `target_market` | 目标市场。 |
| `platform` | 目标平台。 |
| `content_objective` | 本轮内容要达成什么。 |
| `initial_route_hypothesis` | 初始路线，可为 `UNKNOWN`。 |
| `test_question` | 本轮内容准备验证什么。 |
| `project_owner` | 对结果负责的人。 |
| `store_account_context` | 可选的店铺或账号上下文。 |

这是上游上下文快照，不是完整选品审批对象。

## 5. Product 与 ProductVersion 边界

`Product` 表示稳定商品身份。

`ProductVersion` 表示 Evidence 适用的版本，例如供应商版本、样品、型号、配置、包装版本或其他轻量版本备注。

WS-0 必须包含 ProductVersion Lite。

ProductVersion Lite 只承担以下最小边界：

- 稳定版本身份。
- Evidence 适用范围。
- 防止 Evidence 直接挂到 Product。

ProductVersion Lite 不冻结最终数据库字段。

当前规则：

- Evidence belongs to ProductVersion。
- ProductVersion belongs to Product。
- Evidence 不得绕过 ProductVersion 直接绑定 Product。
- 一个版本的 Evidence 不得被静默复用为另一个版本的 Proof。
- Supplier、Sample、Batch、PackagingVersion、file Evidence 和知识治理深度属于 WS-2 及以后。

## 6. Evidence 边界

Evidence 是来源资料。

Evidence 不自动等于 Confirmed Fact。

规则：

- AI 可以从 Evidence 中提取候选内容。
- AI 不能自动确认正式事实。
- 原始 Evidence 不得被 AI 结果覆盖。
- Evidence 必须保留来源、已知采集时间和 ProductVersion 关系。
- 候选事实成为已批准业务内容前必须经过人工审核。

候选 Evidence 类别：

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

这些是概念类别，不是冻结的数据库枚举。

## 7. KnowledgePack 边界

`KnowledgePack` 是逻辑对象。

首轮实现必须包含真实的 Knowledge Pack v0.1。它可以在未来已批准的 active iteration 中用版本化 Markdown / YAML 表达。本次文档本地化不创建 knowledge 目录、数据库表、UI、搜索、标签、管理平台或 Prompt 文件。

业务职责：

- 提供 Script Rules。
- 提供 Pattern Cards。
- 提供 Hook Guidance。
- 提供 Claims Guardrails。
- 提供 Review Rubric。
- 提供 Market Style Notes。

Run 要求：

- 每个使用知识的 AI Run 都必须记录 Knowledge Pack Version，包括 v0.1。

## 8. Reference 边界

Reference 是作为市场或创意输入使用的参考内容。

Version 1 可以手工录入。

最小职责：

- 保留来源。
- 记录为什么相关。
- 在有价值时记录 hook、scene、format、proof 或 style notes。
- 允许后续被 Concept 或 ScriptPack 引用。

自动搜索和视频拆解是未来由 Adapter 支持的能力。

## 9. CreativeConcept 边界

`CreativeConcept` 是草稿或被选中的方向。

最小职责：

- 区分 AI 生成的 Draft 与人工修改或批准的 Concept。
- 引用所使用的 Evidence 和 Reference。
- 保留为什么选择某个 Concept。
- 允许被拒绝的 Draft 保持可追溯，但不成为生产指令。

## 10. ScriptPack 边界

首版 ScriptPack 可以聚合：

- `script`。
- `storyboard`。
- `shots`。
- `shot_duration`。
- `aspect_ratio`。
- `visual_requirement`。
- `asset_requirement`。
- `recommended_production_mode`。
- `generation_notes`。
- `evidence_references`。
- `reference_references`。
- `risk_notes`。
- `review_status`。

不要为了“模型纯粹性”在真实使用证明需要之前拆出大量表。

## 11. Run 边界

`Run` 记录 AI 或自动处理过程。

最小职责：

- Input versions。
- Knowledge Pack Version。
- Model / provider。
- Output version。
- Cost，若可用。
- Error，若失败。

Run 不代表通用 Workflow Engine 或 Agent Runtime。

## 12. Review 边界

`Review` 记录人工决策。

最小职责：

- Target resource。
- Reviewer。
- Decision。
- Note。
- Decision time。

AI 可以建议，但不能批准正式内容。

## 13. Future-only Objects

以下对象不是当前 Walking Skeleton 的领域对象。它们登记在 [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md)。

| 未来对象 | Backlog 区域 |
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
