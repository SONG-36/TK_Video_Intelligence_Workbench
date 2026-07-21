---
document_type: release_business_process
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.2"
status: DRAFT_FOR_DISCUSSION
implementation_allowed: false
authority: LEVEL_2_RELEASE
last_updated: 2026-07-21
change_policy: ADR_REQUIRED_AFTER_APPROVAL
---

# 04_RELEASE_1_BUSINESS_PROCESS

## 1. 文档职责

本文档只描述 Release 1 中“人和业务如何完成任务”。

它不冻结数据库、API、页面、Prompt、Agent Runtime 或具体 Kernel 实现。

---

## 2. Release 1 业务目标

将：

```text
一个已经确定需要制作内容的商品
+
Selection-to-Content Handoff
+
Content Operating Context
+
商品资料与参考内容
```

转化为：

```text
Approved Creative Concept
+
Approved Script
+
Storyboard
+
Shot List
+
Production Requirements
```

---

## 3. 端到端业务流程

```mermaid
flowchart LR
    S0[Stage 0<br/>内容任务进入与运营上下文确认]
    A[Stage A<br/>商品事实与证据]
    B[Stage B<br/>市场与参考内容]
    C[Stage C<br/>内容方向与视频构想]
    D[Stage D<br/>剧本与拍摄设计]
    O[Production-ready Pack]

    S0 --> A --> B --> C --> D --> O
```

---

# 4. Stage 0：内容任务进入与运营上下文确认

## 4.1 业务目的

在进入商品事实与内容设计前，明确：

- 为什么这个商品现在要做内容。
- 初始商业路径是什么。
- 内容在商业路径中承担什么作用。
- 目标市场和平台是什么。
- 使用哪个店铺或账号。
- 当前店铺是否适合放大流量。
- 地区规则和风险版本是什么。
- 当前要验证什么。
- 预计投入多少。
- 哪些结论仍不确定。

## 4.2 输入

- 商品身份。
- Selection Decision 或人工立项结论。
- 目标市场。
- 初始 Go-to-Market Hypothesis。
- 初始 Content Route Hypothesis。
- 店铺与账号信息。
- Store Health Snapshot。
- Market Compliance Profile Snapshot。
- 当前内容目标与投入等级。

## 4.3 主流程

```mermaid
flowchart TB
    A[创建内容任务入口]
    B[登记商品进入内容阶段的原因]
    C[选择 Content Route]
    D[确认 Target Market 与 Platform]
    E[绑定店铺 / 账号]
    F[读取或录入 Store Health Snapshot]
    G[读取或录入 Compliance Snapshot]
    H[定义内容作用与测试假设]
    I[评估当前是否适合投入]
    J{上下文是否足够}
    K[补充或标记 UNKNOWN]
    L[人工确认]
    M[Approved Content Operating Context]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J
    J -- 否 --> K --> L
    J -- 是 --> L
    L --> M
```

## 4.4 输出

```text
Approved Content Operating Context
```

包含：

- Product Context。
- Selection-to-Content Handoff。
- Content Route Hypothesis。
- Target Market。
- Platform。
- Compliance Snapshot。
- Store Health Snapshot。
- Content Objective。
- Investment Level。
- Test Hypothesis。
- Risk Tolerance。
- Decision Owner / Date。

## 4.5 完成条件

- 上游决策没有被简化为 Product ID。
- `UNKNOWN` 被允许并明确标记。
- 市场、渠道、店铺和合规上下文可追溯。
- 后续 Content Project 绑定此快照。

---

# 5. Stage A：商品事实与证据

## 5.1 业务目的

建立内容生产可依赖的商品知识基线。

## 5.2 主流程

```mermaid
flowchart TB
    A[上传与登记原始资料]
    B[拆分信息条目]
    C[标记来源与类型]
    D{信息类型}
    E[Supplier Claim]
    F[Observation / Test]
    G[AI Inference]
    H[Human Judgment]
    I[冲突与缺口检查]
    J[市场与合规叠加]
    K{是否需要确认}
    L[商品负责人审核]
    M{审核结果}
    N[Confirmed Fact / Product Proof]
    O[Rejected / Risk]
    P[Pending Verification]
    Q[Product Knowledge Baseline]

    A --> B --> C --> D
    D --> E
    D --> F
    D --> G
    D --> H
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J --> K
    K -- 否 --> Q
    K -- 是 --> L --> M
    M -- 通过 --> N --> Q
    M -- 否定 --> O --> Q
    M -- 资料不足 --> P --> Q
```

## 5.3 输出

```text
Product Knowledge Baseline
```

至少包含：

- Supplier Claims。
- Observations。
- Confirmed Facts。
- Product Proof。
- Risks。
- Unknowns。
- Market-specific Restrictions。
- 禁止或谨慎表达项。

---

# 6. Stage B：市场与参考内容

## 6.1 业务目的

按目标市场和内容路径研究参考内容。

## 6.2 主流程

```mermaid
flowchart TB
    A[定义参考研究任务]
    B[按 Content Route 分类参考]
    C[添加候选参考内容]
    D[记录市场、平台与来源]
    E[分析结构、Hook、场景与Proof]
    F[判断商品适配度]
    G[判断路线适配度]
    H[判断政策与店铺适配度]
    I{参考是否可用}
    J[纳入 Reference Intelligence Pack]
    K[仅保留为市场观察]
    L[排除并记录原因]

    A --> B --> C --> D --> E --> F --> G --> H --> I
    I -- 可用 --> J
    I -- 仅市场信号 --> K
    I -- 不适配 --> L
```

## 6.3 参考分类

- Creator-led Reference。
- Owned-content Reference。
- Paid-media Reference。
- Listing / Search Reference。
- Live Reference。
- Market Signal。
- Risk Case。

## 6.4 输出

```text
Reference Intelligence Pack
```

---

# 7. Stage C：内容方向与视频构想

## 7.1 业务目的

基于商品知识、参考研究和运营上下文，形成并批准可执行构想。

## 7.2 主流程

```mermaid
flowchart TB
    A[创建 Content Project]
    B[绑定 Content Operating Context]
    C[明确任务目标与约束]
    D[读取商品知识与参考结论]
    E[形成多个 Creative Concept]
    F[关联 Evidence 与 Reference]
    G[标记 Content Route 与市场]
    H[定义受众 / 场景 / Hook / Proof / 假设]
    I[AI辅助审核]
    J{资料是否充分}
    K[补充资料或标记风险]
    L[提交人工审核]
    M{审核结果}
    N[Approved Creative Concept]
    O[退回修改]
    P[拒绝并记录原因]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J
    J -- 否 --> K --> D
    J -- 是 --> L --> M
    M -- 通过 --> N
    M -- 修改 --> O --> E
    M -- 拒绝 --> P
```

## 7.3 构想最低要求

- 任务类型。
- Content Route。
- Target Market。
- 目标受众。
- 用户问题。
- 核心内容承诺。
- Hook。
- Product Proof。
- 参考机制。
- 测试假设。
- 为什么值得拍。
- 店铺与政策限制。
- 风险和制作约束。

---

# 8. Stage D：剧本与拍摄设计

## 8.1 业务目的

把已批准构想转化为可执行方案。

## 8.2 主流程

```mermaid
flowchart TB
    A[读取 Approved Creative Concept]
    B[继承 Context Snapshot]
    C[生成或编写 Script Draft]
    D[设计节奏、画面与动作]
    E[安排 Product Proof]
    F[生成 Storyboard 与 Shot List]
    G[生成 Production Requirements]
    H[事实 / 合规 / 店铺 / 可拍性审核]
    I{审核结果}
    J[修改剧本或镜头]
    K[批准 Script Version]
    L[冻结版本与依赖]
    M[导出 Production-ready Pack]

    A --> B --> C --> D --> E --> F --> G --> H --> I
    I -- 退回 --> J --> C
    I -- 通过 --> K --> L --> M
```

## 8.3 输出

```text
Production-ready Script & Shooting Pack
```

必须继承：

- Content Route。
- Target Market。
- Compliance Profile Version。
- Store Health Snapshot。
- Channel Account Context。

---

# 9. 跨阶段回退与变更

```mermaid
flowchart LR
    S0[Stage 0]
    A[Stage A]
    B[Stage B]
    C[Stage C]
    D[Stage D]

    S0 --> A --> B --> C --> D
    D -. 事实问题 .-> A
    D -. 参考不足 .-> B
    D -. 构想不成立 .-> C
    C -. 上下文变化 .-> S0
    C -. 商品信息缺口 .-> A
    B -. 市场或政策变化 .-> S0
```

上游上下文变化可能使下游对象进入：

```text
NEEDS_REVIEW
```

---

# 10. 当前待讨论问题

1. Content Operating Context 是否独立成聚合根。
2. Store Health Snapshot 首版最低字段。
3. Market Compliance Profile Snapshot 首版最低字段。
4. Content Route 是否允许多选与主次关系。
5. `UNKNOWN` 如何影响后续审批。
6. 店铺健康较差时是否禁止进入后续阶段。
7. 合规规则由谁确认。
8. Content Project 是否必须绑定单一店铺。
9. 同一商品是否可以针对不同市场建立多个 Project。
10. 同一构想是否允许派生多个渠道版本。

---

## 11. 退出标准

- 使用三个真实商品完成 Walkthrough。
- Stage 0 不会变成完整选品系统。
- 业务人员能解释为什么该商品进入内容阶段。
- 内容路径、市场、政策和店铺状态可追溯。
- 后续构想与剧本继承同一上下文快照。
