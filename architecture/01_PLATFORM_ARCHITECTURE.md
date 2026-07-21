---
document_type: platform_architecture
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.2"
status: BASELINE_CANDIDATE
implementation_allowed: false
authority: LEVEL_2_ARCHITECTURE
last_updated: 2026-07-21
change_policy: ADR_REQUIRED_AFTER_APPROVAL
---

# 01_PLATFORM_ARCHITECTURE

## 1. 文档职责

本文档冻结软件承载业务的高层结构。

它回答：

- 哪些概念属于 Kernel。
- 哪些概念属于业务领域。
- Agent、Skill 和 Workflow 放在哪里。
- 市场政策和店铺状态属于哪里。
- LangChain、LangGraph、MCP 和模型供应商如何隔离。
- 当前 Release 需要实现多厚的 Kernel。

---

## 2. 四层架构

```mermaid
flowchart TB
    subgraph UX[Experience Layer]
        U1[商品工作区]
        U2[内容项目工作区]
        U3[审核与导出]
    end

    subgraph DOMAIN[Domain Modules]
        D1[商品知识与证据]
        D2[市场与参考]
        D3[内容方向与构想]
        D4[剧本与拍摄设计]
        D5[Market & Compliance]
        D6[Channel & Store Operations]
    end

    subgraph INTEL[Intelligence Plane]
        I1[Skills]
        I2[Workflows]
        I3[Agents]
        I4[Context Builders]
        I5[Evaluations]
    end

    subgraph KERNEL[Platform Kernel]
        K1[Resource]
        K2[Capability]
        K3[Execution]
        K4[Policy]
        K5[Trace]
    end

    subgraph ADAPTERS[Adapters / Drivers]
        A1[Model Providers]
        A2[Feishu]
        A3[TikTok Data]
        A4[Storage]
        A5[Generation Providers]
        A6[Runtime Frameworks]
        A7[MCP / REST / Local Tools]
    end

    UX --> DOMAIN
    UX --> INTEL
    DOMAIN --> KERNEL
    INTEL --> KERNEL
    KERNEL --> ADAPTERS
```

---

## 3. Platform Kernel

Kernel 只提供机制，不承载业务语义。

### 3.1 Resource

- 稳定 ID。
- 类型。
- 版本。
- 状态引用。
- 关系。
- 所有权。
- 生命周期。
- 归档。

### 3.2 Capability

声明可执行能力：

```text
capability_id
version
input_schema
output_schema
execution_mode
required_permissions
risk_level
cost_policy
implementation_ref
```

### 3.3 Execution

- Run。
- 同步与异步。
- 状态。
- 重试。
- 超时。
- 幂等。
- 暂停与恢复。
- 人工等待。
- 父子运行。

### 3.4 Policy

- 谁能做。
- 是否允许。
- 是否需要人工审批。
- 是否超出成本。
- 是否有外部副作用。
- 是否允许修改正式数据。

### 3.5 Trace

- 谁触发。
- 使用了什么输入和上下文。
- 调用了什么 Capability。
- 使用了什么模型或工具。
- 经过什么审批。
- 产生或修改哪些 Resource。

---

## 4. 市场政策与店铺状态的位置

```mermaid
flowchart LR
    M[Market Compliance Profile]
    S[Store Health Snapshot]
    D[Domain Context]
    P[Kernel Policy]
    E[Execution Decision]

    M --> D
    S --> D
    D --> P
    P --> E
```

原则：

```text
具体地区规则是什么
→ Market & Compliance Domain

店铺评分和账号状态是什么
→ Channel & Store Operations Domain

规则如何强制执行
→ Platform Kernel Policy
```

禁止把：

- US TikTok Policy。
- Store Rating。
- 违规积分。
- 类目禁售规则。

直接写进 Kernel。

---

## 5. Intelligence Plane

```mermaid
flowchart LR
    S[Skill] --> C[Capability]
    W[Workflow] --> E[Execution]
    A[Agent] --> E
    CB[Context Builder] --> R[Resource]
    EV[Evaluation] --> T[Trace]
```

Agent 不得：

- 直接拥有主数据。
- 确认业务事实。
- 自动批准。
- 绕过 Policy。

---

## 6. 常见技术定位

| 技术 | 系统定位 | 是否进入 Kernel |
|---|---|---:|
| LangChain | Skill / Tool 开发框架 | 否 |
| LangGraph | Workflow / Agent Runtime | 否 |
| Agent Harness | Agent 运行外壳 | 否 |
| OpenAI / Claude Agent SDK | Runtime / Provider Adapter | 否 |
| MCP | Tool / Resource 连接协议 | 否 |
| RAG | Context Builder 策略 | 否 |
| 向量数据库 | Retrieval Adapter | 否 |
| Multi-Agent | 编排策略 | 否 |
| Human-in-the-loop | Policy + Execution 机制 | 是 |
| Checkpoint / Resume | Execution 机制 | 是 |
| Tracing | Trace 机制 | 是 |

---

## 7. Release 1 最小 Kernel

```mermaid
flowchart TB
    R1[Release 1 Business Slice]
    R[Resource Lite<br/>ID / Version / Relation / Source]
    C[Capability Lite<br/>Skill / Tool Contract]
    E[Execution Lite<br/>Run / Status / Retry / Cost]
    P[Policy Lite<br/>Permission / Approval]
    T[Trace Lite<br/>Input / Output / Audit]

    R1 --> R
    R1 --> C
    R1 --> E
    R1 --> P
    R1 --> T
```

当前不需要：

- 通用 Checkpoint Engine。
- 通用 Policy DSL。
- 通用插件市场。
- 复杂多 Agent Runtime。
- 分布式 Workflow Engine。
- 全球政策规则引擎。
- 店铺实时事件流平台。

---

## 8. 技术基线

- 前端：React + TypeScript。
- 后端：Python + FastAPI。
- 数据库：PostgreSQL。
- 对象存储：S3 / MinIO。
- 模块化单体。
- 结构化模型输出。
- 固定 Workflow 优先。
- Release 1 不强制 LangChain。
- Release 1 不强制 LangGraph。
- Release 1 不自研 Agent OS。
