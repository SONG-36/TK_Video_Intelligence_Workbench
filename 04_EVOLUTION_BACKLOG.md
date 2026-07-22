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

# 长期演进 Backlog

## 1. 文档职责

本文档记录有效但延期的长期能力。

本文档不授权实施，也不定义未来 Schema。本文档只记录问题组、MVP 当前处理方式、已观察到的证据、重新评审触发条件、可能的演进方向和状态。

允许状态：

```text
CAPTURED
OBSERVING
READY_FOR_DESIGN
PARALLEL_LAB
REJECTED
```

## 2. Backlog 分组

### EV-A：Selection and Operating Context

问题：

完整选品、Portfolio、Priority 和自动 Selection-to-Content Handoff 不属于当前 MVP，但内容系统不能丢失上游业务上下文。

MVP 当前处理方式：

运营人工录入 Selection-to-Content Handoff 和可选 store/account context。

已观察到的证据：

仓库当前只有文档，没有商品 Pilot 运行记录。

重新评审触发条件：

- 多个商品竞争相同内容资源。
- 运营反复要求系统决定哪个商品应进入内容阶段。
- 人工 handoff 在多个 Pilot 中反复不一致或不完整。

可能的演进方向：

在真实内容 Pilot 暴露重复需求后，再建设 selection workflow、portfolio review、priority support 和 automatic handoff generation。

状态：

CAPTURED

### EV-B：Decision Governance

问题：

Gate、route hypothesis、override、decision authority 和 experiment contract 很重要，但完整治理机制会压垮当前 Walking Skeleton。

MVP 当前处理方式：

使用 human review、status、decision note、route hypothesis text 和 `test_question`。

已观察到的证据：

当前没有实现。此前设计确认 Gate 和 Route 重要，但字段深度尚未通过真实使用验证。

重新评审触发条件：

- 项目因相同原因反复停止或返工。
- Reviewer 对批准权限产生分歧。
- `UNKNOWN` route 或 route change 频繁出现。
- 内容上线后需要对照预先声明的 experiment question。

可能的演进方向：

在反复出现 Pilot 证据后，从 Review records 演进出 Gate、Route Hypothesis、Override 和 Experiment Contract 模型。

状态：

CAPTURED

### EV-C：Product Knowledge and Evidence Governance

问题：

Product version、sample、batch、snapshot freshness、evidence correction、invalidation 和 downstream review 可能变复杂。

MVP 当前处理方式：

使用 Product、ProductVersion、Evidence Lite、provenance 和 human review。不到必要时不拆分 Sample 或 Batch。

已观察到的证据：

当前 audit 确认还没有 Product 或 Evidence 代码。

重新评审触发条件：

- Evidence 在不同供应商版本之间发生冲突。
- Script 引用了后来被更正的 fact。
- 包装、批次或样品差异影响 claims。
- 运营无法判断某个来源是否适用于当前内容。

可能的演进方向：

引入 Sample、Batch、Evidence Scope、correction workflow 和 downstream impact review。

状态：

CAPTURED

### EV-D：Market, Compliance and Store Context

问题：

市场政策、平台规则、店铺健康、渠道上下文和规则优先级会影响内容决策。

MVP 当前处理方式：

使用 target market、platform、可选 store/account context、claims guardrails 和 risk notes。

已观察到的证据：

当前仓库没有 store、compliance 或 channel integration。

重新评审触发条件：

- Claims risk 反复阻塞批准。
- Store 或 account health 改变项目可行性。
- 多市场需要不同 script 或 claims。
- 人工 risk notes 无法阻止不安全输出。

可能的演进方向：

先引入 ComplianceProfile、StoreHealthSnapshot、Channel Context、rule precedence 和 manual rule library，再考虑自动执行。

状态：

CAPTURED

### EV-E：Content Knowledge and Script Intelligence

问题：

未来可能需要完整知识平台来管理 hooks、patterns、rubrics、prompt evaluation 和基于表现反馈的 script intelligence。

MVP 当前处理方式：

使用 Versioned Content Knowledge Pack 作为轻量逻辑对象。

已观察到的证据：

当前没有 knowledge directory、UI、search、tags 或 approval flow。

重新评审触发条件：

- 运营需要搜索或比较规则。
- Knowledge 更新影响多个 Run。
- Knowledge version 不清导致 Prompt 质量不稳定。
- 表现反馈识别出可复用的 script patterns。

可能的演进方向：

建设 knowledge management UI、search、tags、approval、market/category classification、prompt evaluation 和 feedback linkage。

状态：

CAPTURED

### EV-F：Reference Intelligence

问题：

TikTok search、video breakdown、reference scoring 和 freshness 可以提升内容决策，但 WS-1 不需要自动 Reference Intelligence。

MVP 当前处理方式：

使用带来源、备注、相关性和引用的 manual references。

已观察到的证据：

Existing system mapping 确认外部工具具备 TikTok search 和 video analysis 能力，但当前仓库没有集成。

重新评审触发条件：

- 手工录入 Reference 太慢。
- 运营反复使用同一套搜索流程。
- Reference 质量或 freshness 难以判断。
- 内容决策需要结构化拆解 hook、scene、proof 和 format。

可能的演进方向：

增加 TikTokSearchAdapter、reference media adapter、video breakdown、reference scoring 和 freshness tracking。

状态：

CAPTURED

### EV-G：Generation Orchestration

问题：

完整生成需要 plans、batches、jobs、provider adapters、workers、queues、cost control、review 和 artifacts。它不属于主 MVP，但值得独立验证。

MVP 当前处理方式：

主系统只导出 Generation-ready Owned Content Production Pack。

已观察到的证据：

外部 Seedance 和 video creation 实验存在，但当前仓库没有 generation implementation。

重新评审触发条件：

- Production team 可以反复消费导出的 packs。
- 手工交接给 generation 成为瓶颈。
- Parallel Lab 证明 provider speed、cost、success rate 和 output quality。
- Human review 需要比较 rendered artifacts 与 approved packs。

可能的演进方向：

运行独立 Generation Lab，验证 ComfyUI Workflow、API Workflow JSON、Binding Manifest、single-task submission、result collection、Seedance validation、speed、success rate 和 resource cost。之后再考虑 GenerationPlan、RenderBatch、RenderJob、Worker、Queue、Provider Adapter 和 Artifact 模型。

状态：

PARALLEL_LAB

### EV-H：Feedback, Learning and Automation

问题：

Publication、performance feedback、business experiment learning、route learning、agent assistance 和 Platform Core extraction 应在真实重复使用之后再进入。

MVP 当前处理方式：

记录 test question、approved output、citations 和 review status。不实现 publishing、analytics、agent runtime 或 Platform Core。

已观察到的证据：

当前没有 publishing、feedback、agent 或 Platform Core 代码。

重新评审触发条件：

- Approved packs 被发布，且 performance data 可用。
- 运营需要比较 concept outcomes。
- Fixed workflows 重复到足以可靠自动化。
- 同一机制至少在两个真实模块中重复，并经过三个商品 Pilot 验证。

可能的演进方向：

增加 performance snapshots、business learning、route learning、controlled automation，并最终从已验证重复中抽取 Platform Core。

状态：

CAPTURED

## 3. 历史 EV 映射

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

## 4. Backlog 使用规则

- 不因为 backlog item 存在就创建代码。
- 不为未来能力创建空目录。
- Revisit Trigger 必须由真实案例支撑。
- 先收集证据，再更新相关权威文档或 ADR。
- 不在 Backlog 中编写完整未来 Schema。
