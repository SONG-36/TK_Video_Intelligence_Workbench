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

# MVP 最小贯通骨架

## 1. 文档职责

本文档是当前 MVP 唯一的范围与业务流程文档。

本文档定义生产意图型最小贯通骨架（Production-intent Walking Skeleton）、当前能力分类、首个 Pilot、验收问题和迭代顺序。

本文档不冻结完整数据库字段、最终 API URL、UI 布局、Prompt 文件、Workflow 文件或未来生成 Schema。

## 2. MVP 问题陈述

第一版帮助运营回答：

```text
Given a selected product and business context, what owned content should we create, why, based on which evidence and references, and is the output ready to hand to shooting or generation work?
```

即：面对一个已选商品和业务上下文，我们应该做什么自有内容、为什么做、依据哪些 Evidence 和 Reference，以及输出是否可以交给拍摄或生成团队。

MVP 必须产出可解释、经过人工审核、生成就绪的自有内容生产包（Generation-ready Owned Content Production Pack）。

## 3. 目标用户

- 项目负责人。
- TikTok 运营。
- 商品负责人。
- 内容审核负责人。

## 4. 生产意图型最小贯通骨架

定义：

```text
Use the thinnest real end-to-end business chain to validate product value.
Keep production-intent standards for high-migration-cost boundaries such as stable IDs, provenance, review, versioning, migration, and adapters.
Keep unvalidated fields, rules, gates, routes, and automation lightweight.
```

中文含义：

- 用最薄但真实的端到端业务链验证产品价值。
- 对稳定 ID、来源可追溯性、审核、版本、迁移和 Adapter 等高迁移成本边界保持生产意图。
- 对尚未验证的字段、规则、Gate、Route 和自动化保持轻量。

采用的业务链路：

```text
创建 ContentProject
↓
录入 Selection-to-Content Handoff
↓
绑定 Product / ProductVersion
↓
添加最小 Evidence
↓
加载版本化 Content Knowledge Pack
↓
手工添加 3-5 条 Reference
↓
生成 3 个 Creative Concept Draft
↓
人工选择或修改一个 Concept
↓
生成 Script / Storyboard / Shot List
↓
Human Review
↓
导出 Markdown / JSON
↓
形成 Generation-ready Owned Content Production Pack
```

拒绝的做法：

- 先建设完整 Product Workspace，再建设 Knowledge，再建设 Reference，很久以后才到 ScriptPack。
- 做成 Streamlit 风格单页、Prompt 写死、AI 输出直接当正式结果。

## 4.1 ProductVersion Lite 边界

WS-0 必须包含 ProductVersion Lite。

ProductVersion Lite 表示第一轮实现只保留稳定版本身份和 Evidence 适用范围所需的最小版本边界。Evidence 必须通过 ProductVersion 绑定，不得绕过 ProductVersion 直接挂到 Product。

`ProductVersion depth` 仍为 `LIGHTWEIGHT`，因为第一轮只实现最小版本边界。这不表示第一轮不实现 ProductVersion。

WS-2 才深化 ProductVersion 的供应商、样品、包装、文件 Evidence、Fact / Proof / Risk / Unknown 和商品知识治理。本文档不冻结最终数据库字段。

## 5. Selection-to-Content Handoff

MVP 不建设完整选品系统。

每个 ContentProject 都必须接收 Selection-to-Content Handoff（选品到内容的交接快照）。Version 1 由运营人工录入。

最小字段：

| 字段 | 含义 |
|---|---|
| `selection_rationale` | 为什么这个商品进入内容阶段。 |
| `target_market` | 当前内容项目的目标市场。 |
| `platform` | 目标平台。 |
| `content_objective` | 本轮内容要达成什么。 |
| `initial_route_hypothesis` | 初始路线，可为 `UNKNOWN`。 |
| `test_question` | 本轮内容准备验证什么。 |
| `project_owner` | 对结果负责的人。 |
| `store_account_context` | 可选的店铺或账号上下文。 |

这是上游上下文快照，不是完整选品审批流程。

## 6. Content Knowledge Pack

MVP 不能没有剧本知识底座。

当前使用一个逻辑对象：

```text
Versioned Content Knowledge Pack
```

首轮实现必须包含一份真实、版本化的 Knowledge Pack v0.1。它可以在未来已批准的 active iteration 中采用 Markdown / YAML 表达。

Knowledge Pack v0.1 至少包含：

- Script Rules。
- Pattern Cards。
- Hook Guidance。
- Claims Guardrails。
- Review Rubric。
- Market Style Notes。

当前文档范围只定义：

- 业务职责。
- 最小组成。
- 版本要求。
- AI Run 对 Knowledge Pack Version 的引用。

每个使用 Knowledge Pack 的 AI Run 都必须记录准确的 Knowledge Pack version。

本任务不创建 `knowledge/` 目录或 Prompt 文件。

只有在需要 UI 管理、搜索、标签、审批、市场/类目分类、表现反馈或自动推荐时，才升级为完整知识库平台。

## 7. Manual Reference

WS-1 可以使用手工录入的 Reference。

Reference version 1 必须保留：

- Source URL 或来源说明。
- Platform。
- Creator/account，若已知。
- Hook 或场景备注。
- 为什么相关。
- 哪个 Concept 或 Script 元素使用了它。

自动 TikTok search 延期到 WS-3。

## 8. Generation-ready 输出

MVP 不实现批量视频生产。

当前输出契约是：

```text
Generation-ready Owned Content Production Pack
```

最小输出：

| 字段 | 含义 |
|---|---|
| `script` | 已批准的脚本文本。 |
| `storyboard` | 场景级生产设计。 |
| `shots` | Shot list。 |
| `shot_duration` | 每个 shot 或片段的预计时长。 |
| `aspect_ratio` | 目标画幅比例。 |
| `visual_requirement` | 拍摄或生成所需的视觉要求。 |
| `asset_requirement` | 所需商品、图片、视频、音频或设计素材。 |
| `recommended_production_mode` | `REAL_SHOOT`、`AI_IMAGE`、`AI_VIDEO`、`MIXED` 或 `UNDECIDED`。 |
| `generation_notes` | 给下游生成或生产团队的说明。 |
| `evidence_references` | 内容包使用的 Evidence 引用。 |
| `reference_references` | 内容包使用的 Reference 引用。 |
| `risk_notes` | Claims、Proof、合规或生产风险。 |
| `review_status` | Draft、approved、rework、hold 或 stopped。 |

主系统当前只拥有该输出契约。它不实现 GenerationPlan、RenderBatch、RenderJob、ComfyUI Adapter、Seedance Adapter、worker、queue、provider routing 或自动批量计费。

## 9. MVP 能力分类

| 能力 | 分类 | 说明 |
|---|---|---|
| Content Project | MUST_HAVE | 当前业务链的工作容器。 |
| Selection Handoff | MUST_HAVE | 必需的上游快照。 |
| Product Lite | MUST_HAVE | 稳定商品身份。 |
| Evidence Lite | MUST_HAVE | 最小来源记录。 |
| Knowledge Pack Version | MUST_HAVE | AI Run 引用的版本。 |
| Manual Reference | MUST_HAVE | 用户手工录入 3-5 条 Reference。 |
| Creative Concept Draft | MUST_HAVE | 生成三个 Draft。 |
| ScriptPack | MUST_HAVE | Script、storyboard、shots、generation notes。 |
| Human Review | MUST_HAVE | AI 输出不能自我批准。 |
| Markdown / JSON Export | MUST_HAVE | 交给 production 或 generation 工作。 |
| ProductVersion depth | LIGHTWEIGHT | 第一轮实现最小版本边界，不实现 Sample/Batch 深度。 |
| File Evidence | LIGHTWEIGHT | 如果首个编码 iteration 不含文件上传，可先从 link/text 开始。 |
| Automatic TikTok Search | DEFERRED | WS-3 重新评审。 |
| Full Knowledge Platform | DEFERRED | 当前 Knowledge Pack 是版本化内容，不是平台。 |
| Gate Engine | DEFERRED | 先使用 human review/status。 |
| Priority Algorithm | DEFERRED | 需要时只做人工 priority。 |
| Experiment Platform | DEFERRED | 当前只记录 test question。 |
| Generation Orchestration | DEFERRED | 当前只定义输出契约。 |
| ComfyUI / Seedance Lab | PARALLEL_LAB | 独立验证，不污染主系统模型。 |

## 10. 首个 Pilot

首个 Pilot 商品：

```text
车载吸尘器
```

Pilot 必须产出：

- Product context。
- 真实 Evidence。
- Manual References。
- 三个 Creative Concepts。
- 一个 Approved Concept。
- 英文 Script。
- Storyboard。
- Shot List。
- Evidence references。
- Reference references。
- Generation Notes。
- Markdown export。
- JSON export。

## 11. MVP 验收问题

运营必须能够回答：

- 为什么做这个商品？
- 本轮内容准备验证什么？
- 使用了哪些 Evidence？
- 借鉴了哪些 Reference？
- 为什么选择这个 Concept？
- 哪些内容由 AI 生成？
- 哪些内容经过人工批准？
- 这个 Production Pack 是否可以交给拍摄或生成团队？

## 12. 迭代顺序

### WS-0：项目与上下文录入

- Content Project。
- Selection Handoff。
- Product Lite。
- ProductVersion Lite。
- Evidence Lite。

### WS-1：薄端到端链路

- Knowledge Pack Version。
- Manual Reference。
- Concept Draft。
- ScriptPack Draft。
- Review。
- Export。

### WS-2：Product 与 Evidence 深化

- ProductVersion。
- File Evidence。
- Fact / Proof / Risk / Unknown。
- Product Knowledge Baseline。

### WS-3：Reference 集成

- TikTokSearchAdapter。
- Video breakdown。
- Reference Pack。

### WS-4：Script 与交付深化

- Concept Version。
- Storyboard。
- Shot。
- Delivery Pack deepening。

### WS-5：三商品 Pilot

- 车载吸尘器。
- 电动泡沫喷壶。
- 一个个人护理商品。

### WS-6：架构评审

判断哪些真实重复值得抽取为 Platform Core。

## 13. 第一份 Active Iteration 边界

未来第一份 `working/ACTIVE_ITERATION.md` 必须以 WS-0 + WS-1 的薄端到端输出作为验收终点。

它可以在一个 iteration 内拆成多个 coding steps，但不能只完成 Product/Evidence CRUD 就宣称 Walking Skeleton 完成。

## 14. 实施授权

本文档处于人工评审草稿状态。

本文档不授权业务代码。通过审批后，首个编码任务必须定义在唯一的 `working/ACTIVE_ITERATION.md` 中。
