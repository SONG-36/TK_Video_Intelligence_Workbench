---
document_type: phase_i1_plan
project: "TikTok Video Intelligence Workbench"
baseline_version: "0.1"
status: DRAFT_FOR_REVIEW
implementation_allowed: false
authority: LEVEL_3_IMPLEMENTATION_PREPARATION
last_updated: 2026-07-21
change_policy: CHANGE_REQUEST_REQUIRED
depends_on:
  - 06_RELEASE_1A_MVP_SCOPE.md
  - 07_RELEASE_1A_IMPLEMENTATION_PLAN.md
  - 10_RELEASE_1A_TECHNICAL_BASELINE.md
  - 11_RELEASE_1A_DOMAIN_MODEL_LITE.md
---

# 12_PHASE_I1_PRODUCT_WORKSPACE_PLAN

## 1. Phase I1 目标

Phase I1 只实现：

```text
创建 Product
→ 创建 ProductVersion
→ 添加 Evidence
→ 查看 Product / Version / Evidence
→ 保存来源和基础版本信息
```

Phase I1 不实现：

- AI Fact Extraction。
- Product Knowledge Baseline。
- Reference Search。
- Creative Concept。
- Script。
- Gate Engine。
- Priority。
- Experiment。
- Publication。
- Performance Feedback。

---

## 2. 用户故事

- 运营创建一个商品。
- 运营为商品创建一个供应商或样品版本。
- 运营上传或登记 Evidence。
- 运营看到 Evidence 属于哪个 ProductVersion。
- 运营修改商品基本信息，但历史版本和 Evidence 关系不丢失。
- 运营不能把一个版本的 Evidence 错绑定到另一个版本而无提示。
- 系统记录创建时间和修改时间。

---

## 3. I1 最小页面

| Page | Responsibility |
|---|---|
| Product List | 查看已有 Product，进入创建和详情 |
| Create Product | 创建稳定商品身份 |
| Product Detail | 查看 Product 基本信息和版本列表 |
| Product Version Detail | 查看版本信息和该版本下的 Evidence |
| Add Evidence | 上传或登记 Evidence，并绑定 ProductVersion |
| Evidence Detail | 查看 Evidence 来源、类型、文件或链接、创建信息 |

本文档不定义最终视觉稿。

---

## 4. I1 API 候选

资源级候选：

- Create Product。
- List Products。
- Get Product。
- Update Product。
- Create Product Version。
- List Product Versions。
- Get Product Version。
- Create Evidence。
- List Evidence。
- Get Evidence。

API Contract 在 I1 实施任务中冻结。本文档不生成 OpenAPI 文件，不冻结最终 URL。

---

## 5. I1 数据迁移候选

需要识别的实体：

- Product。
- ProductVersion。
- Evidence。

候选约束：

- ProductVersion 必须属于有效 Product。
- Evidence 必须属于有效 ProductVersion。
- Evidence 必须有来源类型。
- Evidence 必须有标题或来源描述。
- 文件 Evidence 必须有 storage reference。
- Link Evidence 必须有 source URL。
- created_at / updated_at 必须存在。

候选索引：

- Product status。
- ProductVersion product_id。
- Evidence product_version_id。
- Evidence evidence_type。
- created_at。

本任务不创建 Alembic Migration。

---

## 6. I1 测试场景

Backend:

- Product 创建成功。
- ProductVersion 必须属于 Product。
- Evidence 必须绑定有效 ProductVersion。
- 无效 ID 返回明确错误。
- 删除或停用 Product 时不会静默破坏历史 Evidence。
- 来源字段可追溯。
- 上传文件类型和大小存在基础校验。
- API Validation。
- Database Constraint。

Frontend:

- Product List 能展示已有 Product。
- Create Product 表单能提交有效输入。
- Product Detail 能展示版本列表。
- Add Evidence 能选择 ProductVersion。
- Evidence Detail 能显示来源和绑定关系。

---

## 7. I1 验收商品与 Fixture

验收商品：

```text
车载吸尘器
```

候选 Fixture：

```text
TEST_FIXTURE_ONLY
Product: 车载吸尘器
ProductVersion A: Supplier A sample
ProductVersion B: Supplier B sample or revised version
Evidence 1: 图片 Evidence
Evidence 2: 供应商规格 Evidence
Evidence 3: 人工观察 Evidence
```

Fixture 不得伪造为正式业务事实。Fixture 只用于验证 Product、ProductVersion 和 Evidence 关系。

---

## 8. I1 Definition of Done

I1 完成时必须满足：

- 本地可以创建和查看 Product。
- 可以创建 ProductVersion。
- 可以登记或上传 Evidence。
- Evidence 与版本关系清楚。
- 有数据库迁移。
- 有后端测试。
- 有最小前端流程。
- 不需要直接修改数据库。
- 文档和测试通过。
- 不包含 I2 以后能力。

---

## 9. Phase I1 Explicit Non-goals

- Do not implement ProductKnowledgeBaseline.
- Do not implement Reference Workspace.
- Do not implement TikTok Search Adapter.
- Do not implement Creative Concept.
- Do not implement Script / Storyboard / Shot List.
- Do not implement Owned Content Production Pack.
- Do not implement Gate Engine.
- Do not implement AI extraction.
- Do not integrate Feishu.
- Do not integrate Seedance, ComfyUI, or Kling.
