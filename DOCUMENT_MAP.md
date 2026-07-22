# DOCUMENT_MAP

## 1. 权威文档顺序

正式产品与架构权威固定为：

1. [docs/00_PRODUCT_SYSTEM_OVERVIEW.md](docs/00_PRODUCT_SYSTEM_OVERVIEW.md)
2. [docs/01_MVP_WALKING_SKELETON.md](docs/01_MVP_WALKING_SKELETON.md)
3. [docs/02_DOMAIN_MODEL.md](docs/02_DOMAIN_MODEL.md)
4. [docs/03_TECHNICAL_ARCHITECTURE.md](docs/03_TECHNICAL_ARCHITECTURE.md)
5. [docs/04_EVOLUTION_BACKLOG.md](docs/04_EVOLUTION_BACKLOG.md)
6. [docs/05_EXISTING_SYSTEM_MAPPING.md](docs/05_EXISTING_SYSTEM_MAPPING.md)
7. [docs/architecture/ADR_LOG.md](docs/architecture/ADR_LOG.md)

Working 文件不是权威来源。Archive 文件只保留历史。

## 2. 文档职责

| 文档 | 职责 |
|---|---|
| [docs/00_PRODUCT_SYSTEM_OVERVIEW.md](docs/00_PRODUCT_SYSTEM_OVERVIEW.md) | 产品定位、角色边界、价值链、当前 MVP 边界、双轨模型、明确不做事项、原则。 |
| [docs/01_MVP_WALKING_SKELETON.md](docs/01_MVP_WALKING_SKELETON.md) | 当前 MVP 链路、能力分类、首个 Pilot、验收问题、迭代顺序。 |
| [docs/02_DOMAIN_MODEL.md](docs/02_DOMAIN_MODEL.md) | 当前 Walking Skeleton 领域对象、边界、最小关系和 future-only 对象。 |
| [docs/03_TECHNICAL_ARCHITECTURE.md](docs/03_TECHNICAL_ARCHITECTURE.md) | 技术栈、Modular Monolith、Adapter 边界、AI 边界、Platform Core 抽取规则。 |
| [docs/04_EVOLUTION_BACKLOG.md](docs/04_EVOLUTION_BACKLOG.md) | 延期的长期能力组和重新评审触发条件。 |
| [docs/05_EXISTING_SYSTEM_MAPPING.md](docs/05_EXISTING_SYSTEM_MAPPING.md) | 既有系统复用证据和 Adapter 边界。 |
| [docs/architecture/ADR_LOG.md](docs/architecture/ADR_LOG.md) | 架构和产品架构决策历史。 |
| [docs/working/CURRENT_IMPLEMENTATION_AUDIT.md](docs/working/CURRENT_IMPLEMENTATION_AUDIT.md) | 当前实现事实审计；作为证据保留，不是正式权威。 |

## 3. 推荐阅读顺序

1. [docs/00_PRODUCT_SYSTEM_OVERVIEW.md](docs/00_PRODUCT_SYSTEM_OVERVIEW.md)
2. [docs/01_MVP_WALKING_SKELETON.md](docs/01_MVP_WALKING_SKELETON.md)
3. [docs/02_DOMAIN_MODEL.md](docs/02_DOMAIN_MODEL.md)
4. [docs/03_TECHNICAL_ARCHITECTURE.md](docs/03_TECHNICAL_ARCHITECTURE.md)
5. [docs/04_EVOLUTION_BACKLOG.md](docs/04_EVOLUTION_BACKLOG.md)
6. [docs/05_EXISTING_SYSTEM_MAPPING.md](docs/05_EXISTING_SYSTEM_MAPPING.md)
7. [docs/architecture/ADR_LOG.md](docs/architecture/ADR_LOG.md)

既有系统复用评审时，重点阅读 [docs/05_EXISTING_SYSTEM_MAPPING.md](docs/05_EXISTING_SYSTEM_MAPPING.md)。

延期能力评审时，重点阅读 [docs/04_EVOLUTION_BACKLOG.md](docs/04_EVOLUTION_BACKLOG.md)。

## 4. 变更检查矩阵

| 变更类型 | 优先更新 |
|---|---|
| 产品定位或角色边界 | [docs/00_PRODUCT_SYSTEM_OVERVIEW.md](docs/00_PRODUCT_SYSTEM_OVERVIEW.md) |
| 当前 MVP 流程或验收 | [docs/01_MVP_WALKING_SKELETON.md](docs/01_MVP_WALKING_SKELETON.md) |
| 领域对象或边界 | [docs/02_DOMAIN_MODEL.md](docs/02_DOMAIN_MODEL.md) |
| 技术栈、Adapter、AI、Platform Core 规则 | [docs/03_TECHNICAL_ARCHITECTURE.md](docs/03_TECHNICAL_ARCHITECTURE.md) |
| 延期长期能力 | [docs/04_EVOLUTION_BACKLOG.md](docs/04_EVOLUTION_BACKLOG.md) |
| 外部或兄弟仓库复用决策 | [docs/05_EXISTING_SYSTEM_MAPPING.md](docs/05_EXISTING_SYSTEM_MAPPING.md) |
| 重大决策或决策替换 | [docs/architecture/ADR_LOG.md](docs/architecture/ADR_LOG.md) |

## 5. 目录规则

根目录只保留仓库入口、操作规则和运行时配置。

`docs/` 是产品、架构、工作记录和历史文档根目录：

- `docs/00` 到 `docs/05` 是正式产品文档。
- `docs/architecture/ADR_LOG.md` 是架构决策日志。
- `docs/working/` 是临时工作材料。
- `docs/archive/` 是历史文档。

未经明确人工批准，不得创建新的正式编号产品或架构文档。

Phase、Slice 和 Iteration 计划在编码被批准时写入 `docs/working/ACTIVE_ITERATION.md`。同一时间最多只能有一份 active iteration 文件。
