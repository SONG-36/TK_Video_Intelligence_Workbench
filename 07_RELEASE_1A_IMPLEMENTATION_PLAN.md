---
document_type: implementation_plan
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.1"
status: DRAFT_FOR_REVIEW
implementation_allowed: true
implementation_scope: RELEASE_1A_MVP_ONLY
authority: LEVEL_3_IMPLEMENTATION_PLAN
last_updated: 2026-07-21
change_policy: CHANGE_REQUEST_REQUIRED
depends_on:
  - 06_RELEASE_1A_MVP_SCOPE.md
  - architecture/01_PLATFORM_ARCHITECTURE.md
  - 05_RELEASE_1_VERTICAL_SLICES.md
---

# 07_RELEASE_1A_IMPLEMENTATION_PLAN

## 1. 文档职责

本文档定义 Release 1A 的实施顺序和开发边界。

本文档不是完整 Low-Level Design，不冻结最终目录、数据库 Schema、API、页面或 Prompt。业务代码只能在 [06_RELEASE_1A_MVP_SCOPE.md](06_RELEASE_1A_MVP_SCOPE.md) 和本文档共同允许的范围内实施。

---

## 2. 技术基线

继续遵循当前架构基线：

- Backend：Python + FastAPI。
- Frontend：React + TypeScript。
- Database：PostgreSQL。
- Object Storage：本地开发可先使用文件系统 Adapter，但接口必须允许以后切换 S3 / MinIO。
- Modular Monolith。
- Structured AI Outputs。
- Fixed Workflow first。
- 不强制 LangChain。
- 不强制 LangGraph。
- 不自研 Agent OS。
- 外部服务通过 Adapter 隔离。

本任务不安装或生成这些技术栈代码。

---

## 3. 实施前必须完成 Existing System Mapping

用户已经有其他仓库或工具，包括可能存在的：

- TikTok Growth Search。
- Scrape Creators Client。
- 视频拆解 Custom GPT 或分析流程。
- sku-video-pack-engine。
- ComfyUI / Seedance / Kling 试验。
- Feishu 输入输出能力。

实现前必须确认：

- 哪些代码真实存在。
- 位于哪个仓库。
- 能否复用。
- 是否只应通过 Adapter 调用。
- 哪些能力不能复制进入当前仓库。

不得假设这些能力可以直接 `import`。

---

## 4. 建议实施阶段

### Phase I0：Implementation Preparation

交付：

- 当前仓库代码结构设计。
- Backend / Frontend 的最小目录。
- 环境变量策略。
- 本地开发方式。
- 数据库迁移方案。
- 测试策略。
- External Adapter 边界。
- Existing System Mapping。
- 首个 Pilot 数据准备。

在 I0 完成前，不允许一次性生成所有业务代码。

### Phase I1：Product Workspace Skeleton

交付：

- Product。
- Product Version。
- Evidence。
- 基础 CRUD。
- 来源记录。
- 最小前端页面。
- 数据库迁移。
- 单元测试和 API 测试。

### Phase I2：Product Knowledge Baseline

交付：

- Knowledge Item 分类。
- AI 候选提取。
- 人工确认。
- Fact / Proof / Risk / Unknown。
- Product Knowledge Baseline。
- AI Draft / Approved 状态。
- 版本记录。

### Phase I3：Reference Workspace

交付：

- Reference Video 保存。
- Keyword Search Adapter。
- Reference Analysis。
- 真实字段展示。
- 人工适配性判断。
- Reference Pack。
- 复用或对接现有 TikTok Search 能力。

### Phase I4：Creative Concept

交付：

- Content Project。
- Content Route 简单字段。
- Creative Concept Draft。
- Evidence 和 Reference 引用。
- 人工选择和审核。
- 基础 Decision Record。

### Phase I5：Owned Content Production Pack

交付：

- Script Version。
- Storyboard。
- Shot List。
- Product Proof 引用。
- Reference 引用。
- 审核。
- Markdown / JSON 导出。

### Phase I6：End-to-End Pilot

至少使用：

- 车载吸尘器。
- 电动泡沫喷壶。
- 一个个人护理产品。

记录：

- 操作时间。
- AI 成本。
- 人工修订次数。
- 无用字段。
- 缺失能力。
- 业务流程阻塞。
- Evolution Backlog 新发现。

---

## 5. 每个阶段必须遵守

- 一次只实现一个垂直切片。
- Schema-first，但只定义当前切片所需 Schema。
- 必须有测试。
- 必须有真实验收场景。
- 不提前创建 Future Capability。
- 不为了长期 Backlog 预建复杂框架。
- Kernel Lite 由真实切片拉动。
- 每个 Phase 完成后人工审核，再进入下一阶段。
- 不自动 git commit 或 push。

---

## 6. Kernel Lite 实施边界

Release 1A 只实现：

### Resource Lite

- ID。
- 类型。
- 版本。
- 状态。
- 来源。
- 关系。

### Execution Lite

- Run ID。
- Capability。
- 输入版本。
- 输出版本。
- 状态。
- 模型。
- 成本。
- 错误。

### Policy Lite

- AI 输出默认 Draft。
- 只有人工可以 Approved。
- 高成本外部调用需要显式触发。
- 禁止自动批量生成媒体。

### Trace Lite

- 谁发起。
- 使用了什么输入。
- 调用了什么 Capability。
- 生成了什么输出。
- 谁审核。
- 为什么拒绝或批准。

不要实现：

- 通用 Resource Framework。
- 通用 Policy DSL。
- 通用 Workflow Engine。
- 分布式执行系统。

---

## 7. 测试策略

至少定义：

- Domain Unit Tests。
- API Integration Tests。
- Database Migration Tests。
- AI Structured Output Validation。
- Golden Fixtures。
- Export Snapshot Tests。
- 基础 Frontend Component Tests。
- 三商品 Manual Pilot。

---

## 8. Definition of Done

Release 1A 完成时必须：

- 真实端到端链路可运行。
- 不依赖开发人员直接改数据库。
- 三个真实商品 Pilot 通过。
- Fact 和 AI Draft 分开。
- 参考和产物均可追溯。
- 导出可用。
- [governance/checks/check_docs.py](governance/checks/check_docs.py) 继续通过。
- 代码测试通过。
- 长期问题被记录到 [08_LONG_TERM_EVOLUTION_BACKLOG.md](08_LONG_TERM_EVOLUTION_BACKLOG.md)。
- 未实现能力没有被伪装成已完成。

---

## 9. 实施禁止项

- 不直接进入全自动视频生产。
- 不实现完整 Gate。
- 不实现多 Agent。
- 不实现完整 Route Pack。
- 不实现发布和数据闭环。
- 不一次性生成所有前后端代码。
- 不先做通用 Kernel。
- 不拆微服务。
