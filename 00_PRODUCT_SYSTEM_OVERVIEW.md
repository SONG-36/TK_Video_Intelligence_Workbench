---
document_type: product_system_overview
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.4"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_1_PRODUCT_SYSTEM
last_updated: 2026-07-22
change_policy: ADR_REQUIRED_AFTER_APPROVAL
---

# 产品与系统总览

## 1. 文档职责

本文档是 TikTok Video Intelligence Workbench 唯一的产品与系统总览。

本文档定义产品定位、角色边界、完整业务价值链、当前 MVP 边界、双轨推进模型、明确不做的事项和产品原则。

本文档不定义详细领域字段、数据库 Schema、API 路由、页面布局、Prompt、Workflow 或未来能力 Schema。相关内容分别由以下文档承载：

- [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md)：当前 MVP 业务链。
- [02_DOMAIN_MODEL.md](02_DOMAIN_MODEL.md)：当前领域概念。
- [03_TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md)：技术架构。
- [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md)：延期的长期能力。
- [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md)：既有系统复用证据。
- [architecture/ADR_LOG.md](architecture/ADR_LOG.md)：决策历史。

## 2. 产品定位

产品名称：

```text
TikTok Video Intelligence Workbench
```

正式产品定位：

```text
AI-assisted Content Decision Workspace
AI 辅助内容决策与剧本工作台
```

本产品帮助运营人员将上游商品与业务上下文、商品 Evidence、内容知识和 Reference 转换成可解释、经过 Human Review（人工审核）、可执行的内容生产包。

当前 MVP 的价值终点是：

```text
Generation-ready Owned Content Production Pack
```

即生成就绪的自有内容生产包，可继续交给实拍或后续生成环节。

当前用户：

- 项目负责人。
- TikTok 运营。
- 商品负责人。
- 内容审核负责人。

当前业务痛点：

- 商品、Evidence、Reference、剧本知识和生成交接分散在不同位置。
- 运营可以生成草稿，但难以解释为什么选择某个 Creative Concept。
- AI 输出经常缺少来源可追溯性和人工批准边界。
- 项目负责人容易误以为必须先设计或实现完整平台，才能验证端到端价值。

当前产品价值：

- 将一个商品和一个运营上下文转换成可审核的内容决策。
- 保留商品进入内容阶段的原因。
- 显示 Evidence 和 Reference 引用。
- AI 输出默认是 Draft（草稿），必须经过人工批准。
- 导出可继续进入实拍或未来生成工作的内容生产包。

## 3. 角色边界

项目负责人当前角色是：

```text
AI Product Manager
+
Business System Designer
```

即 AI 产品经理 + 业务系统设计者。

核心职责：

- 理解真实业务。
- 定义业务问题。
- 明确输入、输出和人工判断点。
- 将业务认知表达成可解释、可验证的系统行为。
- 定义验收样例。
- 使用真实商品验证。
- 在评审后决定下一轮优先级。

项目负责人不需要独自完成：

- 通用平台核心。
- 全部后端和前端代码。
- 全部 AI Workflow。
- 完整视频生成平台。
- 全球合规平台。
- 选品平台。
- 发布和表现反馈系统。

开发者负责：

- Schema。
- API。
- UI。
- Migration。
- Adapter。
- Test。
- Deployment。

架构评审按真实切片进行，不要求在第一个商品 Pilot 前完成所有抽象。

## 4. 完整业务价值链

长期业务链：

```text
商品机会
→ 商品立项
→ Selection-to-Content Handoff
→ 商品事实与 Evidence
→ Reference Intelligence
→ 内容构想
→ Script / Storyboard / Shot
→ Production
→ Publish
→ Performance Feedback
→ Business Learning
```

这条链是业务地图，不是实施顺序。

## 5. 当前 MVP 边界

当前 MVP 边界是：

```text
Selection-to-Content Handoff
→ Product / ProductVersion
→ Evidence Lite
→ Versioned Content Knowledge Pack
→ Manual Reference
→ Creative Concept Draft
→ Human-selected Concept
→ Script / Storyboard / Shot List
→ Human Review
→ Markdown / JSON Export
→ Generation-ready Owned Content Production Pack
```

当前仓库处于产品与架构重构阶段，不是已有应用的迭代阶段。

已确认的当前事实：

- 本仓库没有业务代码。
- 没有 backend。
- 没有 frontend。
- 没有 database。
- 没有 Product Workspace。
- 没有 Reference Workspace。
- 没有 Creative / Script 模块。
- 没有 Generation 模块。
- 没有 Platform Core 代码。

当前实现事实来源是 [working/CURRENT_IMPLEMENTATION_AUDIT.md](working/CURRENT_IMPLEMENTATION_AUDIT.md)。Working 文件不是正式权威来源，但该审计文件作为仓库状态证据保留。

## 6. 双轨模型

Track A：

```text
Walking Skeleton MVP
```

Track A 验证从上游交接到生成就绪内容包的最薄真实端到端链路。

Track B：

```text
Evolution Backlog / Parallel Lab
```

Track B 记录长期能力和独立生成实验。Track B 不构成当前实施授权。

当前最小贯通骨架定义在 [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md)。延期能力定义在 [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md)。

## 7. 明确不做的事项

当前 MVP 不是：

- 完整选品平台。
- 纯商品知识库。
- Agent OS。
- 通用 Workflow 平台。
- Linux-kernel-style 平台。
- 视频批量生成平台。
- 自动发布平台。
- 完整增长反馈闭环。
- 多租户 SaaS 产品。

当前工作不实现：

- 完整 Gate engine。
- Portfolio management。
- Priority algorithm。
- Experiment platform。
- 全球合规引擎。
- Store health sync。
- Generation orchestration。
- Multi-agent runtime。
- Microservices。

## 8. 产品原则

1. 真实业务优于理论完整性。
2. 人工判断优于虚假自动化。
3. Evidence 和 Reference 必须可追溯。
4. AI 输出默认是 Draft。
5. Approved 内容不得被静默覆盖。
6. 端到端价值优于单模块完备。
7. Release 可以跳过上游模块，但不能丢失必要上游输出。
8. Selection-to-Content Handoff 是当前 MVP 输入。
9. Content Knowledge Pack 是当前 MVP 的轻量能力。
10. Manual Reference 可以作为第一版方案。
11. Owned Content 是当前 MVP 路线。
12. Generation-ready Pack 是当前 MVP 输出终点。
13. 完整 Generation Orchestration 是未来能力。
14. ComfyUI / Seedance 工作只能作为 Parallel Lab 推进。
15. 不在真实重复需求出现前建设 Platform Core。
16. 不先建设 Agent OS。
17. 不先拆分 microservices。
18. 不先建设完整 Gate、Priority、Portfolio 或 Experiment。
19. 稳定共享机制只能从真实重复中抽取。

## 9. 实施授权

所有正式产品与架构文档当前均设置：

```text
implementation_allowed: false
```

本次文档收敛不授权业务代码。

[01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md) 通过人工评审后，编码工作必须通过未来唯一的 working 文件授权：

```text
working/ACTIVE_ITERATION.md
```

本次收敛后该文件不存在。
