"""Thin WS-0 service interface.

The service layer expresses the first creation flow without HTTP, database, or
framework concerns. It wires domain objects together in the order required by
the walking skeleton and leaves persistence/API decisions for later steps.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .domain import (
    ContentProject,
    DomainValidationError,
    Evidence,
    EvidenceCategory,
    OperatingContextSnapshot,
    Product,
    ProductVersion,
)


@dataclass(frozen=True)
class OperatingContextInput:
    selection_rationale: str
    target_market: str
    platform: str
    content_objective: str
    test_question: str
    project_owner: str
    initial_route_hypothesis: str = "UNKNOWN"
    store_account_context: str | None = None


@dataclass(frozen=True)
class ProjectInput:
    id: str
    name: str


@dataclass(frozen=True)
class ProductInput:
    id: str
    name: str


@dataclass(frozen=True)
class ProductVersionInput:
    id: str
    label: str
    notes: str | None = None


@dataclass(frozen=True)
class EvidenceInput:
    id: str
    category: EvidenceCategory
    source: str
    summary: str
    collected_at: str | None = None


@dataclass(frozen=True)
class CreateWS0ProjectRequest:
    project: ProjectInput
    operating_context: OperatingContextInput
    product: ProductInput
    product_version: ProductVersionInput
    evidence: Sequence[EvidenceInput]


@dataclass(frozen=True)
class CreateWS0ProjectResult:
    project: ContentProject
    operating_context: OperatingContextSnapshot
    product: Product
    product_version: ProductVersion
    evidence: tuple[Evidence, ...]


def create_project_from_handoff(request: CreateWS0ProjectRequest) -> CreateWS0ProjectResult:
    """Create the WS-0 project chain from a structured handoff request."""

    if not request.evidence:
        raise DomainValidationError("WS-0 project requires at least one Evidence Lite item")

    operating_context = OperatingContextSnapshot(
        selection_rationale=request.operating_context.selection_rationale,
        target_market=request.operating_context.target_market,
        platform=request.operating_context.platform,
        content_objective=request.operating_context.content_objective,
        initial_route_hypothesis=request.operating_context.initial_route_hypothesis,
        test_question=request.operating_context.test_question,
        project_owner=request.operating_context.project_owner,
        store_account_context=request.operating_context.store_account_context,
    )
    project = ContentProject(
        id=request.project.id,
        name=request.project.name,
        operating_context=operating_context,
    )
    product = Product(id=request.product.id, name=request.product.name)
    product_version = product.create_version(
        version_id=request.product_version.id,
        label=request.product_version.label,
        notes=request.product_version.notes,
    )
    project.bind_product_version(product_version)

    evidence = tuple(
        Evidence.bind_to_product_version(
            evidence_id=evidence_input.id,
            product_version=product_version,
            category=evidence_input.category,
            source=evidence_input.source,
            summary=evidence_input.summary,
            collected_at=evidence_input.collected_at,
        )
        for evidence_input in request.evidence
    )

    return CreateWS0ProjectResult(
        project=project,
        operating_context=operating_context,
        product=product,
        product_version=product_version,
        evidence=evidence,
    )

