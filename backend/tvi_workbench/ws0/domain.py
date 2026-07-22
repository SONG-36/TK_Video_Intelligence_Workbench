"""WS-0 domain objects for the first walking skeleton.

These objects intentionally stay framework-free. They capture the business
rules that are costly to migrate later: handoff context, stable product version
identity, and Evidence provenance scoped to ProductVersion Lite.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, NoReturn


class DomainValidationError(ValueError):
    """Raised when a WS-0 business rule is violated."""


class EvidenceCategory(str, Enum):
    SUPPLIER_DOCUMENT = "SUPPLIER_DOCUMENT"
    SUPPLIER_CLAIM = "SUPPLIER_CLAIM"
    USER_OBSERVATION = "USER_OBSERVATION"
    TEST_RESULT = "TEST_RESULT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    LINK = "LINK"
    OTHER = "OTHER"


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DomainValidationError(f"{field_name} is required")
    return value.strip()


@dataclass(frozen=True)
class OperatingContextSnapshot:
    selection_rationale: str
    target_market: str
    platform: str
    content_objective: str
    test_question: str
    project_owner: str
    initial_route_hypothesis: str = "UNKNOWN"
    store_account_context: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "selection_rationale",
            _required_text(self.selection_rationale, "selection_rationale"),
        )
        object.__setattr__(self, "target_market", _required_text(self.target_market, "target_market"))
        object.__setattr__(self, "platform", _required_text(self.platform, "platform"))
        object.__setattr__(
            self,
            "content_objective",
            _required_text(self.content_objective, "content_objective"),
        )
        object.__setattr__(self, "test_question", _required_text(self.test_question, "test_question"))
        object.__setattr__(self, "project_owner", _required_text(self.project_owner, "project_owner"))

        route = self.initial_route_hypothesis.strip() if isinstance(self.initial_route_hypothesis, str) else ""
        object.__setattr__(self, "initial_route_hypothesis", route or "UNKNOWN")

        if self.store_account_context is not None:
            store_context = self.store_account_context.strip()
            object.__setattr__(self, "store_account_context", store_context or None)


@dataclass
class ContentProject:
    id: str
    name: str
    operating_context: OperatingContextSnapshot
    product_version_id: Optional[str] = None

    def __post_init__(self) -> None:
        self.id = _required_text(self.id, "id")
        self.name = _required_text(self.name, "name")
        if not isinstance(self.operating_context, OperatingContextSnapshot):
            raise DomainValidationError("operating_context must be an OperatingContextSnapshot")

    def bind_product_version(self, product_version: "ProductVersion") -> None:
        if not isinstance(product_version, ProductVersion):
            raise DomainValidationError("product_version must be a ProductVersion")
        self.product_version_id = product_version.id


@dataclass(frozen=True)
class ProductVersion:
    id: str
    product_id: str
    label: str
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _required_text(self.id, "id"))
        object.__setattr__(self, "product_id", _required_text(self.product_id, "product_id"))
        object.__setattr__(self, "label", _required_text(self.label, "label"))
        if self.notes is not None:
            notes = self.notes.strip()
            object.__setattr__(self, "notes", notes or None)


@dataclass
class Product:
    id: str
    name: str
    versions: List[ProductVersion] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.id = _required_text(self.id, "id")
        self.name = _required_text(self.name, "name")
        for version in self.versions:
            self.add_version(version)

    def add_version(self, version: ProductVersion) -> None:
        if not isinstance(version, ProductVersion):
            raise DomainValidationError("version must be a ProductVersion")
        if version.product_id != self.id:
            raise DomainValidationError("ProductVersion must belong to this Product")
        if all(existing.id != version.id for existing in self.versions):
            self.versions.append(version)

    def create_version(self, version_id: str, label: str, notes: Optional[str] = None) -> ProductVersion:
        version = ProductVersion(id=version_id, product_id=self.id, label=label, notes=notes)
        self.add_version(version)
        return version

    def add_evidence(self, evidence: "Evidence") -> NoReturn:
        raise DomainValidationError("Evidence must bind to ProductVersion Lite, not directly to Product")


@dataclass(frozen=True)
class Evidence:
    id: str
    product_version_id: str
    category: EvidenceCategory
    source: str
    summary: str
    collected_at: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _required_text(self.id, "id"))
        object.__setattr__(
            self,
            "product_version_id",
            _required_text(self.product_version_id, "product_version_id"),
        )
        if not isinstance(self.category, EvidenceCategory):
            try:
                object.__setattr__(self, "category", EvidenceCategory(self.category))
            except ValueError as exc:
                raise DomainValidationError("category must be a valid EvidenceCategory") from exc
        object.__setattr__(self, "source", _required_text(self.source, "source"))
        object.__setattr__(self, "summary", _required_text(self.summary, "summary"))
        if self.collected_at is not None:
            collected_at = self.collected_at.strip()
            object.__setattr__(self, "collected_at", collected_at or None)

    @classmethod
    def bind_to_product_version(
        cls,
        *,
        evidence_id: str,
        product_version: ProductVersion,
        category: EvidenceCategory,
        source: str,
        summary: str,
        collected_at: Optional[str] = None,
    ) -> "Evidence":
        if not isinstance(product_version, ProductVersion):
            raise DomainValidationError("Evidence must bind to a ProductVersion")
        return cls(
            id=evidence_id,
            product_version_id=product_version.id,
            category=category,
            source=source,
            summary=summary,
            collected_at=collected_at,
        )

    @classmethod
    def bind_to_product(cls, *args: object, **kwargs: object) -> NoReturn:
        raise DomainValidationError("Evidence must bind to ProductVersion Lite, not directly to Product")

