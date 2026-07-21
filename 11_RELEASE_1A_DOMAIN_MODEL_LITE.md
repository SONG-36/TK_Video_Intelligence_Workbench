---
document_type: domain_model_lite
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.1"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_3_IMPLEMENTATION_PREPARATION
last_updated: 2026-07-21
change_policy: CHANGE_REQUEST_REQUIRED
depends_on:
  - 06_RELEASE_1A_MVP_SCOPE.md
  - 10_RELEASE_1A_TECHNICAL_BASELINE.md
  - 12_PHASE_I1_PRODUCT_WORKSPACE_PLAN.md
---

# 11_RELEASE_1A_DOMAIN_MODEL_LITE

## 1. 文档职责

本文档定义 Release 1A 当前需要的业务概念和关系。

它不是数据库表设计，也不是完整 DDD 模型。它只为 Phase I1 Product Workspace 说明最小业务边界。

---

## 2. 当前核心概念

Release 1A 的候选核心概念：

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

---

## 3. 分类

### I1_REQUIRED

Phase I1 必须实现：

- Product。
- ProductVersion。
- Evidence。

根据真实需要可加入：

- Review。
- DecisionRecord。
- Run Lite。

I1 默认不实现 Review、DecisionRecord、Run Lite，除非 Phase I1 任务明确把它们纳入最小验收。

### LATER_RELEASE_1A

后续切片实现：

- ProductKnowledgeBaseline。
- Reference。
- ReferenceAnalysis。
- ContentProject。
- CreativeConcept。
- ScriptVersion。
- Storyboard。
- Shot。
- OwnedContentProductionPack。

### FUTURE_ONLY

不得进入 Release 1A：

- Gate Engine。
- Portfolio。
- Experiment Platform。
- Multi-agent Runtime。
- Publication。
- Performance Feedback。

---

## 4. I1 Object Notes

### 4.1 Product

- Business Responsibility：表示稳定商品身份，用于聚合版本和后续内容项目。
- Identity：稳定 Product ID。
- Lifecycle：Created → Active → Archived。
- Key Relationships：Product has many ProductVersion。
- Source / Provenance：人工创建；可记录来源备注。
- Version Requirement：Product 自身可编辑，但不得破坏已有关联版本。
- Human Approval Requirement：I1 不需要正式审批；需要可审计创建和修改时间。
- Current Open Questions：是否需要 SKU、品牌、类目在 I1 必填。

CANDIDATE_FOR_I1_SCHEMA：

- name。
- category。
- owner_note。
- status。
- created_at。
- updated_at。

### 4.2 ProductVersion

- Business Responsibility：表示供应商、型号、样品或配置版本。
- Identity：稳定 ProductVersion ID。
- Lifecycle：Draft → Active → Archived。
- Key Relationships：ProductVersion belongs to Product；ProductVersion has many Evidence。
- Source / Provenance：人工创建；可记录供应商、型号、样品说明。
- Version Requirement：Evidence 默认绑定 ProductVersion；不同供应商版本不能静默混合。
- Human Approval Requirement：I1 不需要正式审批；需要清楚显示版本与 Evidence 关系。
- Current Open Questions：是否需要 SupplierVersion、Sample、Batch 独立对象。

CANDIDATE_FOR_I1_SCHEMA：

- product_id。
- version_name。
- supplier_name。
- model_number。
- sample_note。
- status。
- created_at。
- updated_at。

### 4.3 Evidence

- Business Responsibility：保存商品资料、链接、图片、视频、观察、测试或供应商 Claim 的来源记录。
- Identity：稳定 Evidence ID。
- Lifecycle：Registered → Active → Archived。
- Key Relationships：Evidence belongs to ProductVersion。
- Source / Provenance：必须记录来源类型和来源描述；文件类 Evidence 记录存储引用。
- Version Requirement：Evidence 不能从一个 ProductVersion 静默移动到另一个 ProductVersion。
- Human Approval Requirement：Evidence 是来源，不自动等于 Confirmed Fact；AI 不能自动确认事实。
- Current Open Questions：I1 是否需要文件上传和链接登记同时支持，还是先支持链接/文本登记。

CANDIDATE_FOR_I1_SCHEMA：

- product_version_id。
- evidence_type。
- title。
- source_description。
- source_url。
- storage_key。
- original_filename。
- captured_at。
- notes。
- created_at。
- updated_at。

---

## 5. Product 与 ProductVersion 边界

- Product 表示稳定商品身份。
- ProductVersion 表示供应商、型号、样品或配置版本。
- Evidence 默认绑定 ProductVersion。
- 后续是否增加 Sample / Batch 独立对象，留在 [08_LONG_TERM_EVOLUTION_BACKLOG.md](08_LONG_TERM_EVOLUTION_BACKLOG.md)。
- 首版不能把不同供应商版本的数据静默混合。

Example:

```text
Product: 车载吸尘器
ProductVersion A: Supplier A sample, 2026-07 received unit
ProductVersion B: Supplier B revised sample
Evidence A1: Supplier A spec sheet
Evidence A2: User observation for Supplier A sample
Evidence B1: Supplier B photo set
```

Evidence A1/A2 must not silently support ProductVersion B.

---

## 6. Evidence 边界

Evidence concept categories:

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

Rules:

- Evidence is source material.
- Evidence does not automatically equal Confirmed Fact.
- AI may extract candidate content from Evidence.
- AI cannot automatically confirm facts.
- Original Evidence must not be overwritten by AI results.
- Evidence must remain traceable to ProductVersion.

---

## 7. Deferred Concepts

KnowledgeItem and ProductKnowledgeBaseline begin in I2.

Reference and ReferenceAnalysis begin in I3.

ContentProject and CreativeConcept begin in I4.

ScriptVersion, Storyboard, Shot, and OwnedContentProductionPack begin in I5.

Run, Review, and DecisionRecord may appear as lite support objects only when a slice requires them. They must not become a generic workflow or Gate Engine in I1.
