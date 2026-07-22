"""WS-0 domain foundation."""

from .domain import (
    ContentProject,
    DomainValidationError,
    Evidence,
    EvidenceCategory,
    OperatingContextSnapshot,
    Product,
    ProductVersion,
)
from .service import (
    CreateWS0ProjectRequest,
    CreateWS0ProjectResult,
    EvidenceInput,
    OperatingContextInput,
    ProductInput,
    ProductVersionInput,
    ProjectInput,
    create_project_from_handoff,
)

__all__ = [
    "ContentProject",
    "CreateWS0ProjectRequest",
    "CreateWS0ProjectResult",
    "DomainValidationError",
    "Evidence",
    "EvidenceCategory",
    "EvidenceInput",
    "OperatingContextSnapshot",
    "OperatingContextInput",
    "Product",
    "ProductInput",
    "ProductVersion",
    "ProductVersionInput",
    "ProjectInput",
    "create_project_from_handoff",
]
