---
document_type: delivery_releases
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.2"
status: BASELINE_CANDIDATE
implementation_allowed: false
authority: LEVEL_1_GLOBAL
last_updated: 2026-07-21
change_policy: ADR_REQUIRED_AFTER_APPROVAL
---

# 02_DELIVERY_RELEASES

## 1. 文档职责

本文档定义长期能力如何被切成真正可交付、可验收的产品版本。

Delivery Release 不等于完整业务链顺序。系统可以从最有现实价值的中段开始，但必须接收上游必要决策输出。

---

## 2. 交付版本总图

```mermaid
flowchart LR
    R1[Release 1<br/>内容决策与前期制作]
    R2[Release 2<br/>素材与视频生产]
    R3[Release 3<br/>发布与表现反馈]
    R4[Release 4<br/>商品机会与选品判断]
    R5[Release 5<br/>跨域智能编排]

    R1 --> R2 --> R3 --> R4 --> R5
```

---

## 3. Release 1：内容决策与前期制作

```mermaid
flowchart LR
    H[Selection-to-Content Handoff]
    COC[Content Operating Context]
    A[商品事实与证据]
    B[市场与参考内容]
    C[内容方向与视频构想]
    D[剧本与拍摄设计]

    H --> COC --> A --> B --> C --> D
```

Release 1 负责：

- 人工录入或外部导入内容路径假设。
- 人工录入或外部导入市场合规快照。
- 人工录入或外部导入店铺健康快照。
- 在内容决策中使用这些上下文。
- 保存快照和版本。

Release 1 不负责：

- 自动生成 Selection Decision。
- 全球政策自动采集。
- 店铺实时监控。
- 自动发布。

---

## 4. Release 2：素材与视频生产

```mermaid
flowchart LR
    A[Production-ready Pack]
    B[素材需求]
    C[素材资产]
    D[实拍 / AI生成]
    E[剪辑任务]
    F[Video Version]
    G[Production Review]

    A --> B --> C --> D --> E --> F --> G
```

继承：

- Content Route。
- Market Compliance Snapshot。
- Store / Channel Context。
- Production Constraints。

---

## 5. Release 3：发布与表现反馈

```mermaid
flowchart LR
    A[Approved Video]
    B[Publish Task]
    C[Publication]
    D[Store / Account Status]
    E[Performance Snapshot]
    F[Postmortem]
    G[Learning]

    A --> B --> C --> D --> E --> F --> G
```

Release 3 正式接入：

- Channel Account。
- Store。
- Store Health。
- 发布权限与风控。
- 平台表现数据。

---

## 6. Release 4：商品机会与选品判断

```mermaid
flowchart LR
    A[Market Signals]
    B[Product Candidate]
    C[Supplier & Cost]
    D[Compliance]
    E[Commercial Assessment]
    F[Selection Decision]
    G[Go-to-Market Hypothesis]
    H[Content Route Hypothesis]

    A --> B --> C --> D --> E --> F --> G --> H
```

Release 4 正式生成：

- Selection Decision。
- Go-to-Market Hypothesis。
- Content Route Hypothesis。
- Target Market Context。
- Initial Investment Level。

这些输出正式交接给 Release 1。

---

## 7. Release 5：跨域智能编排

```mermaid
flowchart LR
    A[历史Run与Trace]
    B[业务Learning]
    C[跨域规划]
    D[Skill与模型路由]
    E[半自动实验建议]
    F[受控自适应]

    A --> C
    B --> C
    C --> D --> E --> F
```

---

## 8. Release 之间的接口

```mermaid
flowchart TB
    EXT[人工 / 飞书 / 外部系统]
    R1[Release 1<br/>内容决策与前期制作]
    R2[Release 2<br/>素材与视频生产]
    R3[Release 3<br/>发布与反馈]
    R4[Release 4<br/>商品机会与选品]
    R5[Release 5<br/>跨域智能编排]

    EXT -->|临时 Handoff 与 Context| R1
    R4 -->|正式 Selection-to-Content Handoff| R1
    R1 -->|Production-ready Pack| R2
    R2 -->|Approved Video Version| R3
    R3 -->|Performance / Store Health / Learning| R1
    R3 -->|Commercial Evidence| R4
    R1 --> R5
    R2 --> R5
    R3 --> R5
    R4 --> R5
```

---

## 9. 冻结规则

当前冻结：

- Release 1～5 的高层边界。
- Release 1 为当前优先交付。
- Release 1 临时人工接收上游交接包。
- Release 3 正式接入店铺与账号状态。
- Release 4 正式生成选品到内容交接包。

当前不冻结：

- Release 2～5 的字段、页面、状态机、API 和技术实现。
- Release 5 是否采用多 Agent。
- 各 Release 的具体日期。
