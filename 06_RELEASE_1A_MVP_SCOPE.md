---
document_type: release_mvp_scope
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.1"
status: BASELINE_CANDIDATE
implementation_allowed: true
implementation_scope: RELEASE_1A_MVP_ONLY
authority: LEVEL_3_IMPLEMENTATION_SCOPE
last_updated: 2026-07-21
change_policy: ADR_REQUIRED_AFTER_APPROVAL
depends_on:
  - 00_MASTER_DESIGN.md
  - 02_DELIVERY_RELEASES.md
  - 03_RELEASE_1_SCOPE_AND_BOUNDARIES.md
  - 05_RELEASE_1_VERTICAL_SLICES.md
---

# 06_RELEASE_1A_MVP_SCOPE

## 1. 文档职责

本文档是 Release 1A 的实施范围权威文件。

长期 Master、Capability Roadmap、完整 Release 1 范围和 Evolution Backlog 不直接构成开发授权。只有本文件和 [07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md) 明确纳入的能力，才允许进入 Release 1A MVP 开发。

未列入 Release 1A MVP 的能力仍属于 Future Capability，必须记录在 [08_LONG_TERM_EVOLUTION_BACKLOG.md](08_LONG_TERM_EVOLUTION_BACKLOG.md) 或后续正式变更中。

本文档冻结业务概念和 MVP 边界，不冻结最终数据库表、完整字段级 Schema、API 路径或页面布局。

---

## 2. Release 1A 定位

正式名称：

> Release 1A -- Content Decision Workspace MVP

Release 1A 聚焦：

```text
结构化商品知识
+
参考内容研究
+
内容构想
+
Owned Content Production Pack
```

Release 1A 是完整 Release 1 的第一个可运行子版本，不推翻 [03_RELEASE_1_SCOPE_AND_BOUNDARIES.md](03_RELEASE_1_SCOPE_AND_BOUNDARIES.md) 定义的长期 Release 1 边界。

---

## 3. 目标用户

首版用户：

- 用户本人。
- 当前 TikTok 运营团队。
- 商品负责人。
- 内容审核负责人。

不面向：

- 外部客户。
- 达人。
- 大规模跨部门组织。
- 多租户 SaaS 用户。

---

## 4. 第一条端到端业务链

首个 Pilot 链路使用车载吸尘器：

```mermaid
flowchart LR
    A[商品创建]
    B[商品版本]
    C[Evidence]
    D[人工确认 Fact Proof Risk Unknown]
    E[Product Knowledge Baseline]
    F[保存参考视频]
    G[Reference Analysis]
    H[Creative Concept]
    I[人工选择]
    J[Script Storyboard Shot List]
    K[Owned Content Production Pack]
    L[审核与导出]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K --> L
```

完整业务链：

```text
车载吸尘器
→ 商品资料与 Evidence
→ Product Knowledge Baseline
→ TikTok Reference
→ Reference Analysis
→ Creative Concept
→ Script
→ Storyboard
→ Shot List
→ Owned Content Production Pack
```

---

## 5. 三个 MVP Workspace

### 5.1 Product Workspace

最小能力：

- 创建 Product。
- 创建 Product Version。
- 上传或登记商品资料。
- 保存 Evidence。
- 区分 Supplier Claim、Observation、Confirmed Fact、Inference、Unknown、Product Proof、Risk。
- 人工确认。
- 生成 Product Knowledge Baseline。

### 5.2 Reference Workspace

最小能力：

- 按商品和任务进行 TikTok 关键词搜索。
- 保存 Reference Video。
- 保留真实字段和来源。
- 进行视频拆解。
- 标记参考用途和适配性。
- 形成 Reference Pack。

后续实施中可以复用已有 TikTok Growth Search、Scrape Creators Client 和视频拆解能力。本文档不假设这些代码已经存在于当前仓库；真正复用前必须完成 Existing System Mapping。

### 5.3 Creative & Script Workspace

最小能力：

- 基于 Approved Product Knowledge 和 Reference Pack 创建构想。
- AI 可生成 Creative Concept Draft。
- 人工选择或修改构想。
- 生成 Script。
- 生成 Storyboard。
- 生成 Shot List。
- 生成 Owned Content Production Pack。
- 审核、版本化和导出。

---

## 6. MVP 核心对象

候选最小对象：

- Product。
- ProductVersion。
- Evidence。
- KnowledgeItem。
- ProductKnowledgeBaseline。
- Reference。
- ReferenceAnalysis。
- ContentProject。
- CreativeConcept。
- ScriptVersion。
- Storyboard。
- Shot。
- OwnedContentProductionPack。
- Run。
- Review。
- DecisionRecord。

这些对象冻结业务概念，不冻结最终数据库表。不要在 Release 1A 中定义完整字段级 Schema，也不要把所有 Knowledge 类型提前拆成独立微服务或独立表。

---

## 7. MVP 状态与决策框架

Release 1A 不实现 Gate Engine，只实现轻量人工状态和决策记录。

候选状态：

```text
NOT_STARTED
IN_PROGRESS
READY_FOR_REVIEW
APPROVED
REWORK
HOLD
STOPPED
```

候选 Decision：

```text
CONTINUE
REWORK
HOLD
STOP
```

每个主要阶段至少保留：

```text
status
decision
decision_note
decided_by
decided_at
```

这些是业务语义候选，不冻结数据库枚举实现。

---

## 8. MVP 必须做

- Product 和 Product Version。
- Evidence 来源。
- 人工事实确认。
- Knowledge Baseline。
- Reference 保存与分析。
- Creative Concept。
- Owned Content Script Pack。
- AI Draft / Human Approval。
- 版本历史。
- 基础 Trace。
- 导出。
- 至少 3 个真实商品 Pilot。

---

## 9. MVP 明确不做

- 完整 Gate 0～3。
- 自动 Route 判断。
- Creator Pack。
- Paid Media Pack。
- Live Pack。
- Listing Pack。
- Portfolio。
- Priority Algorithm。
- Experiment Platform。
- 发布。
- 表现数据回收。
- 店铺实时同步。
- 全球政策系统。
- 多 Agent。
- Agent OS。
- ComfyUI / Seedance 视频生产。
- 自动批量视频生成。
- 微服务拆分。
- 通用 Workflow Engine。

OWNED_CONTENT 是 Release 1A 唯一正式交付路线，不是系统永久唯一 Route。

---

## 10. MVP 必须保留的长期兼容能力

Release 1A 从第一版开始必须保留：

- 稳定 ID。
- Product Version。
- Evidence 来源。
- Evidence 与 Product Version 的关系。
- AI Draft 与 Human Approved 分离。
- 正式输出版本历史。
- Product、Reference、Concept、Script Pack 之间的关系。
- 基础 Run 和 Trace。
- 已批准内容不能被静默覆盖。
- Content Route 允许 UNKNOWN。
- Delivery Pack 在架构上不能被写死为永远只有一种类型。

---

## 11. MVP 完成标准

- 车载吸尘器完整走通。
- 电动泡沫喷壶完整走通。
- 一个个人护理商品完整走通。
- 运营可以不修改数据库完成操作。
- Product Fact 有来源。
- AI 输出和人工批准可区分。
- Reference 能追溯到来源。
- Script Pack 能追溯到 Product Proof 和 Reference。
- 已批准版本不可静默覆盖。
- 能导出 Markdown 和 JSON。
- 能记录实际使用中出现的长期改进问题。

---

## 12. 与完整 Release 1 的关系

```text
Release 1A
=
完整 Release 1 的第一个可运行子版本
```

Release 1A 不等待 Gate、Route、Priority、Experiment 的完整设计完成后才开始开发。

完整 Release 1 的长期方向仍由 [03_RELEASE_1_SCOPE_AND_BOUNDARIES.md](03_RELEASE_1_SCOPE_AND_BOUNDARIES.md)、[04_RELEASE_1_BUSINESS_PROCESS.md](04_RELEASE_1_BUSINESS_PROCESS.md) 和 [05_RELEASE_1_VERTICAL_SLICES.md](05_RELEASE_1_VERTICAL_SLICES.md) 保留。长期演进问题集中进入 [08_LONG_TERM_EVOLUTION_BACKLOG.md](08_LONG_TERM_EVOLUTION_BACKLOG.md)。
