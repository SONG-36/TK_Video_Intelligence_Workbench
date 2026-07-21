---
document_type: evolution_backlog
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.1"
status: BASELINE_CANDIDATE
implementation_allowed: false
authority: LEVEL_2_EVOLUTION_GUIDANCE
last_updated: 2026-07-21
change_policy: CHANGE_REQUEST_REQUIRED
depends_on:
  - 00_MASTER_DESIGN.md
  - 01_CAPABILITY_ROADMAP.md
  - 02_DELIVERY_RELEASES.md
  - 06_RELEASE_1A_MVP_SCOPE.md
---

# 08_LONG_TERM_EVOLUTION_BACKLOG

## 1. 文档职责

本文档是长期能力和思维漏洞登记簿。

它不构成当前开发授权。任何条目进入代码实现前，必须满足 Revisit Trigger，并形成新的 Scope、ADR 或 Design Change Request。

本文档不是详细需求文档，也不是未来 Schema。它记录问题、MVP 临时处理方式和重新设计触发条件。

---

## 2. Backlog 状态

允许状态：

```text
CAPTURED
OBSERVING
READY_FOR_DESIGN
READY_FOR_IMPLEMENTATION
IMPLEMENTING
VALIDATED
REJECTED
```

---

## 3. 条目模板

每个条目至少包含：

- Capability / Problem。
- Why It Matters。
- Current MVP Handling。
- Deferred Scope。
- Observed Evidence。
- Revisit Triggers。
- Possible Future Direction。
- Likely Target Release。
- Affected Domains / Documents。
- Status。

---

## 4. Long-term Evolution Items

### EV-001 Stage Gate Governance

- Capability / Problem：Gate 0 内容研究准入、Gate 1 商品知识就绪、Gate 2 路线验证、Gate 3 制作投入，以及 Continue / Pause / Stop / Recycle / Change Route。
- Why It Matters：真实项目需要明确退出、返工、条件通过、会签、Override、Permission Matrix 和失效后重审。
- Current MVP Handling：人工状态 + Decision Record + Note。
- Deferred Scope：Gate Rule Engine、自动阻断、复杂条件矩阵、多人会签、Override 机制、Permission Matrix、Gate Score、可配置 Gate DSL。
- Observed Evidence：等待 Release 1A 三商品 Pilot 记录。
- Revisit Triggers：多个项目反复因为相同原因返工；不同运营对于是否继续产生频繁冲突；HOLD / STOP 项目无法管理；出现需要明确责任人的高风险项目。
- Possible Future Direction：从真实 Decision Record 中提炼 Gate 条件和责任模型。
- Likely Target Release：Release 1B+。
- Affected Domains / Documents：[04_RELEASE_1_BUSINESS_PROCESS.md](04_RELEASE_1_BUSINESS_PROCESS.md)、[architecture/02_ARCHITECTURE_DECISIONS.md](architecture/02_ARCHITECTURE_DECISIONS.md)。
- Status：CAPTURED。

### EV-002 Content Route Hypothesis

- Capability / Problem：Creator-led、Owned-content-led、Paid-media-led、Listing/Search-led、Live-led、Hybrid、Unknown 及其 Supporting Evidence、Contrary Evidence、Validation Plan、Success Criteria、Stop Conditions、Review Date。
- Why It Matters：Route 不是标签，而是可验证业务假设。
- Current MVP Handling：简单 Route 字段 + 人工说明；OWNED_CONTENT 是唯一完整交付路线。
- Deferred Scope：完整 Route Hypothesis 模型、验证计划、成功标准、停止条件和复核机制。
- Observed Evidence：等待 Pilot 中 UNKNOWN、OWNED_CONTENT、CREATOR、PAID、HYBRID 的实际选择记录。
- Revisit Triggers：多个项目因路线不清返工；同一商品在不同市场需要不同路线；非 OWNED_CONTENT 路线频繁出现。
- Possible Future Direction：建立 Route Hypothesis 版本模型和验证记录。
- Likely Target Release：Release 1B+ / Release 3。
- Affected Domains / Documents：[03_RELEASE_1_SCOPE_AND_BOUNDARIES.md](03_RELEASE_1_SCOPE_AND_BOUNDARIES.md)、[06_RELEASE_1A_MVP_SCOPE.md](06_RELEASE_1A_MVP_SCOPE.md)。
- Status：CAPTURED。

### EV-003 Route-specific Delivery Packs

- Capability / Problem：Creator Enablement Pack、Owned Content Production Pack、Paid Media Test Pack、Listing/Search Pack、Live Pack、Hybrid Bundle。
- Why It Matters：不同内容路线需要不同交付物。
- Current MVP Handling：只做 Owned Content Production Pack。
- Deferred Scope：非 OWNED_CONTENT 的完整交付流程和 Pack Schema。
- Observed Evidence：等待 Pilot 中非 Owned 路线需求。
- Revisit Triggers：Creator、Paid、Listing、Live 或 Hybrid 项目无法用人工说明承接；团队需要导出非 Owned Pack。
- Possible Future Direction：按 Route 增量添加 Pack Builder。
- Likely Target Release：Release 1B+。
- Affected Domains / Documents：[05_RELEASE_1_VERTICAL_SLICES.md](05_RELEASE_1_VERTICAL_SLICES.md)、[07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md)。
- Status：CAPTURED。

### EV-004 Project Priority and Portfolio

- Capability / Problem：多商品排序、MUST_DO / NEXT / EXPERIMENTAL / HOLD、WIP、预算、人力、拍摄资源、项目停止和降级。
- Why It Matters：多个项目都值得做时，资源竞争成为核心决策。
- Current MVP Handling：人工 priority 字段或简单排序。
- Deferred Scope：Portfolio Management、自动综合评分、资源约束优化。
- Observed Evidence：等待多商品 Pilot 与运营排序记录。
- Revisit Triggers：多个项目同时 READY；团队无法解释先做什么；WIP 失控；资源冲突频繁。
- Possible Future Direction：先建立人工 Portfolio Review，再考虑辅助排序。
- Likely Target Release：Release 1B+ / Release 4。
- Affected Domains / Documents：[01_CAPABILITY_ROADMAP.md](01_CAPABILITY_ROADMAP.md)、[02_DELIVERY_RELEASES.md](02_DELIVERY_RELEASES.md)。
- Status：CAPTURED。

### EV-005 Experiment Contract and Performance Feedback

- Capability / Problem：Business Question、Hypothesis、Variable、Metrics、Baseline、Observation Window、Success Rule、Stop Rule、Experiment Result、Learning、Route 和选品反哺。
- Why It Matters：没有预先定义验证问题，后续表现数据容易被事后解释。
- Current MVP Handling：只回答“本次内容准备验证什么？”
- Deferred Scope：Experiment Platform、表现数据回收、统计结论、自动学习闭环。
- Observed Evidence：等待 Script Pack 导出后的真实发布和复盘需求。
- Revisit Triggers：内容上线后需要回收结论；运营开始比较不同版本；Route 假设需要表现数据验证。
- Possible Future Direction：从轻量 Experiment Note 演进为正式 Experiment Contract。
- Likely Target Release：Release 3。
- Affected Domains / Documents：[02_DELIVERY_RELEASES.md](02_DELIVERY_RELEASES.md)、[architecture/02_ARCHITECTURE_DECISIONS.md](architecture/02_ARCHITECTURE_DECISIONS.md)。
- Status：CAPTURED。

### EV-006 Product Version, Sample and Batch Scope

- Capability / Problem：Product、SKU、Supplier Version、Sample、Production Version、Batch、Packaging Version、Evidence 适用范围。
- Why It Matters：证据可能只适用于某个样品、包装或批次。
- Current MVP Handling：至少实现 Product 和 Product Version。
- Deferred Scope：Sample、Batch、Packaging Version 与 Evidence Scope 的完整建模。
- Observed Evidence：等待 Pilot 中样品、供应商版本和包装差异。
- Revisit Triggers：同一 Product 不同版本证据冲突；拍摄样品与量产批次不一致；包装变化影响内容 Claims。
- Possible Future Direction：引入 Evidence Scope 和 Sample Record。
- Likely Target Release：Release 1B+。
- Affected Domains / Documents：[06_RELEASE_1A_MVP_SCOPE.md](06_RELEASE_1A_MVP_SCOPE.md)、[07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md)。
- Status：CAPTURED。

### EV-007 Snapshot Freshness and Invalidation

- Capability / Problem：Store Health Snapshot、Compliance Snapshot、Reference Data Snapshot、captured_at、effective_at、expires_at、superseded_by、NEEDS_REVIEW、下游失效传播。
- Why It Matters：快照过期或被替代后，已批准内容可能需要重审。
- Current MVP Handling：只保留时间和版本，不做自动传播。
- Deferred Scope：自动失效传播、NEEDS_REVIEW 状态机、快照有效期策略。
- Observed Evidence：等待政策、店铺状态或参考数据变化案例。
- Revisit Triggers：批准内容因上游变化变得不安全；多次需要人工追踪失效影响。
- Possible Future Direction：为关键快照引入 Freshness Policy。
- Likely Target Release：Release 1B+ / Release 3。
- Affected Domains / Documents：[04_RELEASE_1_BUSINESS_PROCESS.md](04_RELEASE_1_BUSINESS_PROCESS.md)、[architecture/01_PLATFORM_ARCHITECTURE.md](architecture/01_PLATFORM_ARCHITECTURE.md)。
- Status：CAPTURED。

### EV-008 Decision Authority and Override

- Capability / Problem：Submitter、Reviewer、Approver、Veto、Conditional Sign-off、Override Reason、Risk Accepted、Expiration、Re-evaluation。
- Why It Matters：高风险内容需要清楚记录谁批准、谁否决、何时重评。
- Current MVP Handling：只实现一个 Reviewer 和 Review Note。
- Deferred Scope：多人会签、Override、条件批准、权限矩阵。
- Observed Evidence：等待 Pilot 中风险审批冲突。
- Revisit Triggers：不同角色对批准结果有分歧；需要追责；风险接受需要有效期。
- Possible Future Direction：从单 Reviewer 演进为 Decision Authority 模型。
- Likely Target Release：Release 1B+。
- Affected Domains / Documents：[04_RELEASE_1_BUSINESS_PROCESS.md](04_RELEASE_1_BUSINESS_PROCESS.md)、[architecture/02_ARCHITECTURE_DECISIONS.md](architecture/02_ARCHITECTURE_DECISIONS.md)。
- Status：CAPTURED。

### EV-009 Source of Truth and External Synchronization

- Capability / Problem：飞书、当前系统、TikTok、Scrape Creators、店铺后台、Immich、供应商文件、AI 输出；区分 Source of Record、Source of Truth、Original Evidence、Derived Data、Cached Snapshot。
- Why It Matters：外部数据来源复杂，不区分来源会破坏追溯。
- Current MVP Handling：保存来源链接和采集时间。
- Deferred Scope：双向同步、权威源选择、缓存刷新、冲突解决。
- Observed Evidence：等待 Existing System Mapping 和 Pilot 导入记录。
- Revisit Triggers：同一事实多源冲突；需要回写飞书或同步 TikTok；来源丢失导致审核失败。
- Possible Future Direction：建立 Source Model 和 Adapter 同步策略。
- Likely Target Release：Release 1B+ / Release 3。
- Affected Domains / Documents：[07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md)、[architecture/01_PLATFORM_ARCHITECTURE.md](architecture/01_PLATFORM_ARCHITECTURE.md)。
- Status：CAPTURED。

### EV-010 Market Compliance and Rule Precedence

- Capability / Problem：法律与地区强制要求 > 平台规则 > 类目规则 > 店铺和账号限制 > 商品特定风险 > 公司内部规则 > 项目偏好；Claims、认证、标签、年龄限制、内容规则、达人规则、市场和政策版本。
- Why It Matters：合规规则存在优先级和版本，不能由 AI 即兴判断。
- Current MVP Handling：人工风险备注和禁止 Claims。
- Deferred Scope：全球政策系统、规则优先级引擎、自动违规裁决。
- Observed Evidence：等待 Pilot 中风险 Claims 与市场限制。
- Revisit Triggers：多个商品反复出现相同风险；人工备注不足以阻止错误输出；平台或地区规则频繁变化。
- Possible Future Direction：先建立人工 Rule Library，再考虑规则执行。
- Likely Target Release：Release 1B+ / Release 4。
- Affected Domains / Documents：[01_CAPABILITY_ROADMAP.md](01_CAPABILITY_ROADMAP.md)、[03_RELEASE_1_SCOPE_AND_BOUNDARIES.md](03_RELEASE_1_SCOPE_AND_BOUNDARIES.md)。
- Status：CAPTURED。

### EV-011 Store Health and Channel Context

- Capability / Problem：店铺评分、账号健康、违规、履约、取消率、退货率、差评、类目限制、流量限制、Research / Production / Publication / Scale Permission。
- Why It Matters：店铺和渠道状态会影响内容投入和发布可行性。
- Current MVP Handling：手工记录目标店铺和风险备注。
- Deferred Scope：店铺实时同步、健康评分、渠道权限模型。
- Observed Evidence：等待目标店铺上下文记录。
- Revisit Triggers：店铺风险导致项目暂停；发布权限影响内容路线；运营反复手工查店铺状态。
- Possible Future Direction：Store Health Snapshot 与 Channel Permission。
- Likely Target Release：Release 1B+ / Release 3。
- Affected Domains / Documents：[00_MASTER_DESIGN.md](00_MASTER_DESIGN.md)、[02_DELIVERY_RELEASES.md](02_DELIVERY_RELEASES.md)。
- Status：CAPTURED。

### EV-012 AI Evaluation vs Business Outcome

- Capability / Problem：AI Evaluation 检查 Schema、Evidence 引用、虚构、可拍性、Claim 风险；Business Outcome 关注停留、完播、点击、转化、退货、利润、Route 假设结果。
- Why It Matters：AI 检查通过不等于业务成功。
- Current MVP Handling：不预测销量，只检查结构、事实和风险。
- Deferred Scope：业务结果评估、表现归因、实验结论。
- Observed Evidence：等待后续发布与表现数据。
- Revisit Triggers：用户把 AI 分数误当成功预测；上线后需要解释表现差异。
- Possible Future Direction：分离 Skill Evaluation 和 Business Outcome Model。
- Likely Target Release：Release 3。
- Affected Domains / Documents：[architecture/01_PLATFORM_ARCHITECTURE.md](architecture/01_PLATFORM_ARCHITECTURE.md)、[architecture/02_ARCHITECTURE_DECISIONS.md](architecture/02_ARCHITECTURE_DECISIONS.md)。
- Status：CAPTURED。

### EV-013 Progressive Forms and Operator Burden

- Capability / Problem：最小必填、推荐补充、条件必填、AI 预填、批量继承、Quick Mode、Standard Mode、Role-based UI。
- Why It Matters：过多字段会阻塞真实运营使用。
- Current MVP Handling：只保留完成真实链路必需字段。
- Deferred Scope：动态表单、角色 UI、条件必填策略。
- Observed Evidence：等待三商品 Pilot 的无用字段和缺失字段记录。
- Revisit Triggers：用户跳过大量字段；关键字段经常缺失；表单耗时过高。
- Possible Future Direction：基于真实使用调整 Progressive Form。
- Likely Target Release：Release 1B+。
- Affected Domains / Documents：[06_RELEASE_1A_MVP_SCOPE.md](06_RELEASE_1A_MVP_SCOPE.md)、[07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md)。
- Status：CAPTURED。

### EV-014 Multi-market, Multi-store and Route Derivation

- Capability / Problem：一个商品多个市场、一个市场多个店铺、一个项目是否可以跨市场、Hybrid Route、共用 Product Knowledge、Market-specific Content Project。
- Why It Matters：市场和店铺上下文会改变可用 Claims、参考内容和交付路线。
- Current MVP Handling：一个 Content Project = 一个目标市场 + 一个主要店铺上下文。
- Deferred Scope：多市场派生、多店铺策略、跨市场项目管理。
- Observed Evidence：等待 Pilot 中多市场或多店铺需求。
- Revisit Triggers：同一商品要同时进入多个市场；一个店铺上下文不足以解释内容决策。
- Possible Future Direction：Product Knowledge 共用，Content Project 按市场和店铺派生。
- Likely Target Release：Release 1B+ / Release 4。
- Affected Domains / Documents：[03_RELEASE_1_SCOPE_AND_BOUNDARIES.md](03_RELEASE_1_SCOPE_AND_BOUNDARIES.md)、[04_RELEASE_1_BUSINESS_PROCESS.md](04_RELEASE_1_BUSINESS_PROCESS.md)。
- Status：CAPTURED。

### EV-015 Feedback, Learning and Selection Loop

- Capability / Problem：表现数据 → Experiment Result → Creative Pattern → Route Learning → Product Content Fit → 反哺选品。
- Why It Matters：没有反馈闭环，系统无法沉淀可复用业务学习。
- Current MVP Handling：不实现反馈模块，只保留未来关联可能性。
- Deferred Scope：表现数据、学习沉淀、选品反哺。
- Observed Evidence：等待 Release 1A 产物进入真实发布后的反馈需求。
- Revisit Triggers：运营开始要求从表现结果回看原始 Concept、Reference 和 Product Proof。
- Possible Future Direction：建立 Experiment Result 与 Learning 模型。
- Likely Target Release：Release 3 / Release 4。
- Affected Domains / Documents：[02_DELIVERY_RELEASES.md](02_DELIVERY_RELEASES.md)、[01_CAPABILITY_ROADMAP.md](01_CAPABILITY_ROADMAP.md)。
- Status：CAPTURED。

### EV-016 Agent and Automation Enhancement

- Capability / Problem：Product Knowledge Agent、Research Agent、Creative Director Agent、Script Agent、Reviewer Agent、Context Builder、Capability Registry、MCP、LangGraph、动态编排、评估、人工闸门。
- Why It Matters：Agent 能力应该服务稳定流程，而不是先行定义系统。
- Current MVP Handling：固定 Workflow + 结构化 Skill + 人工触发 + 人工审核。
- Deferred Scope：多 Agent、Agent OS、动态编排、自动能力选择。
- Observed Evidence：等待哪些 Skill 真正节省时间或减少错误。
- Revisit Triggers：固定流程无法覆盖高频变体；人工重复选择能力；某些审核可被可靠自动化。
- Possible Future Direction：从稳定 Capability 和 Trace 中演进 Agent。
- Likely Target Release：Release 5。
- Affected Domains / Documents：[00_MASTER_DESIGN.md](00_MASTER_DESIGN.md)、[architecture/01_PLATFORM_ARCHITECTURE.md](architecture/01_PLATFORM_ARCHITECTURE.md)。
- Status：CAPTURED。

### EV-017 Portfolio-level Resource Competition

- Capability / Problem：多个商品都“值得做”但资源有限，内容生产能力和项目数量失衡，低价值项目占用团队产能。
- Why It Matters：资源竞争会影响真实交付节奏和机会成本。
- Current MVP Handling：手工排序。
- Deferred Scope：Portfolio-level Resource Competition、产能模型、自动排序。
- Observed Evidence：等待多个商品并行进入 READY 状态。
- Revisit Triggers：多个 READY 项目无法排期；低价值项目挤占拍摄资源。
- Possible Future Direction：人工 Portfolio Board，后续再提炼规则。
- Likely Target Release：Release 1B+ / Release 4。
- Affected Domains / Documents：[01_CAPABILITY_ROADMAP.md](01_CAPABILITY_ROADMAP.md)、[02_DELIVERY_RELEASES.md](02_DELIVERY_RELEASES.md)。
- Status：CAPTURED。

### EV-018 Snapshot and Evidence Correction

- Capability / Problem：可追溯不代表正确；证据可能被推翻；Fact 可能更正；已批准下游产物需要重新审查。
- Why It Matters：纠错能力决定已批准内容是否可信。
- Current MVP Handling：保留版本，不实现全自动失效传播。
- Deferred Scope：自动失效传播、影响分析、批量 NEEDS_REVIEW。
- Observed Evidence：等待 Pilot 中 Evidence 纠错和 Fact 更正案例。
- Revisit Triggers：已批准 Script 引用了被推翻 Fact；产品版本改变影响多个产物。
- Possible Future Direction：Evidence Correction Workflow 和 Downstream Impact Review。
- Likely Target Release：Release 1B+。
- Affected Domains / Documents：[06_RELEASE_1A_MVP_SCOPE.md](06_RELEASE_1A_MVP_SCOPE.md)、[04_RELEASE_1_BUSINESS_PROCESS.md](04_RELEASE_1_BUSINESS_PROCESS.md)。
- Status：CAPTURED。

### EV-019 Business Rule Discovery from Real Usage

- Capability / Problem：哪些字段实际没人使用；哪些判断每次都出现；哪些步骤造成阻塞；哪些 Gate 规则值得升级；哪些 Agent 能力真正有价值。
- Why It Matters：长期机制必须从真实使用中提炼。
- Current MVP Handling：三商品 Pilot 记录操作时间、AI 成本、人工修订次数、无用字段、缺失能力和流程阻塞。
- Deferred Scope：规则发现、流程挖掘、自动建议。
- Observed Evidence：Release 1A Pilot 记录本身。
- Revisit Triggers：同类问题在多个 Pilot 中重复出现；用户明确要求固化判断规则。
- Possible Future Direction：从 Pilot Review 提炼 Design Change Request。
- Likely Target Release：Release 1B+。
- Affected Domains / Documents：[07_RELEASE_1A_IMPLEMENTATION_PLAN.md](07_RELEASE_1A_IMPLEMENTATION_PLAN.md)、[governance/DESIGN_CHANGE_REQUEST_TEMPLATE.md](governance/DESIGN_CHANGE_REQUEST_TEMPLATE.md)。
- Status：CAPTURED。

---

## 5. Backlog 使用规则

- 不因为条目存在就创建代码。
- 不提前创建空模块。
- Revisit Trigger 出现后先收集真实案例。
- 先形成 Design Change Request。
- 再更新 Scope、ADR 或 Release Plan。
- 最后才进入实施。

当前不允许实现完整 Gate、完整 Route Pack、Portfolio、Priority Algorithm、Experiment Platform、Compliance Engine、Store Health Sync、多 Agent 或 Agent OS。
