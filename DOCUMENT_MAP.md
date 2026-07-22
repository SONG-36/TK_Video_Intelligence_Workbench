# DOCUMENT_MAP

## 1. Canonical Authority Order

Formal product and architecture authority is fixed to:

1. [00_PRODUCT_SYSTEM_OVERVIEW.md](00_PRODUCT_SYSTEM_OVERVIEW.md)
2. [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md)
3. [02_DOMAIN_MODEL.md](02_DOMAIN_MODEL.md)
4. [03_TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md)
5. [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md)
6. [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md)
7. [architecture/ADR_LOG.md](architecture/ADR_LOG.md)

Working files are not authority sources. Archive files are historical only.

## 2. What Each Document Answers

| Document | Responsibility |
|---|---|
| [00_PRODUCT_SYSTEM_OVERVIEW.md](00_PRODUCT_SYSTEM_OVERVIEW.md) | Product position, role boundary, value chain, current MVP boundary, dual-track model, non-goals, principles. |
| [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md) | Current MVP chain, capability classification, first pilot, acceptance questions, iteration sequence. |
| [02_DOMAIN_MODEL.md](02_DOMAIN_MODEL.md) | Current Walking Skeleton domain objects, boundaries, minimal relationships, future-only object list. |
| [03_TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md) | Technical stack, modular monolith, adapter boundary, AI boundary, Platform Core extraction rule. |
| [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md) | Deferred long-term capability groups and revisit triggers. |
| [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md) | Evidence-based mapping of external/sibling systems and adapter reuse boundaries. |
| [architecture/ADR_LOG.md](architecture/ADR_LOG.md) | Architecture and product-architecture decision history. |
| [working/CURRENT_IMPLEMENTATION_AUDIT.md](working/CURRENT_IMPLEMENTATION_AUDIT.md) | Current implementation facts from audit; retained as evidence, not formal authority. |

## 3. Reading Order

Use the authority order above.

For current MVP review, read:

1. [00_PRODUCT_SYSTEM_OVERVIEW.md](00_PRODUCT_SYSTEM_OVERVIEW.md)
2. [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md)
3. [02_DOMAIN_MODEL.md](02_DOMAIN_MODEL.md)
4. [03_TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md)
5. [architecture/ADR_LOG.md](architecture/ADR_LOG.md)

For existing system reuse, also read [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md).

For deferred capabilities, read [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md).

## 4. Change Check Matrix

| Change Type | Update First |
|---|---|
| Product position or role boundary | [00_PRODUCT_SYSTEM_OVERVIEW.md](00_PRODUCT_SYSTEM_OVERVIEW.md) |
| Current MVP flow or acceptance | [01_MVP_WALKING_SKELETON.md](01_MVP_WALKING_SKELETON.md) |
| Domain object or boundary | [02_DOMAIN_MODEL.md](02_DOMAIN_MODEL.md) |
| Technical stack, adapters, AI, Platform Core rule | [03_TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md) |
| Deferred long-term capability | [04_EVOLUTION_BACKLOG.md](04_EVOLUTION_BACKLOG.md) |
| External/sibling reuse decision | [05_EXISTING_SYSTEM_MAPPING.md](05_EXISTING_SYSTEM_MAPPING.md) |
| Major decision or supersession | [architecture/ADR_LOG.md](architecture/ADR_LOG.md) |

## 5. Documentation Growth Rule

Do not create new formal numbered product or architecture documents without explicit human approval.

Phase, slice, and iteration planning belongs in `working/ACTIVE_ITERATION.md` when coding is approved. At most one active iteration file may exist at a time.
