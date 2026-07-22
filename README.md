# TikTok Video Intelligence Workbench

TikTok Video Intelligence Workbench 是一个 AI-assisted Content Decision Workspace，用于将已选商品上下文、Evidence、内容知识和 Reference 转换为经过 Human Review 的 Generation-ready Owned Content Production Pack。

当前状态：

- 产品和架构围绕 Production-intent Walking Skeleton 收敛。
- 本仓库当前没有业务代码。
- 没有 backend、frontend、database、Product Workspace、Reference Workspace、Creative / Script 模块、Generation 模块或 Platform Core 代码。
- 当前正式文档不授权业务代码。

正式文档位于 `docs/`。

文档入口：

- [DOCUMENT_MAP.md](DOCUMENT_MAP.md)
- [AGENTS.md](AGENTS.md)
- [docs/00_PRODUCT_SYSTEM_OVERVIEW.md](docs/00_PRODUCT_SYSTEM_OVERVIEW.md)
- [docs/01_MVP_WALKING_SKELETON.md](docs/01_MVP_WALKING_SKELETON.md)
- [docs/02_DOMAIN_MODEL.md](docs/02_DOMAIN_MODEL.md)
- [docs/03_TECHNICAL_ARCHITECTURE.md](docs/03_TECHNICAL_ARCHITECTURE.md)
- [docs/04_EVOLUTION_BACKLOG.md](docs/04_EVOLUTION_BACKLOG.md)
- [docs/05_EXISTING_SYSTEM_MAPPING.md](docs/05_EXISTING_SYSTEM_MAPPING.md)
- [docs/architecture/ADR_LOG.md](docs/architecture/ADR_LOG.md)
- [governance/DOCUMENT_STANDARD.md](governance/DOCUMENT_STANDARD.md)

当前实现审计：

- [docs/working/CURRENT_IMPLEMENTATION_AUDIT.md](docs/working/CURRENT_IMPLEMENTATION_AUDIT.md)

开发环境版本：

- Node: `.nvmrc`
- Python: `.python-version`

任何编码开始前，[docs/01_MVP_WALKING_SKELETON.md](docs/01_MVP_WALKING_SKELETON.md) 必须通过人工评审，并且当前编码任务必须定义在唯一的 `docs/working/ACTIVE_ITERATION.md` 中。
