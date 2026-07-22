"""Thin WS-1 input preparation service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

from tvi_workbench.ws0 import DomainValidationError

from .domain import KnowledgePack, ManualReference


@dataclass(frozen=True)
class PrepareWS1InputsRequest:
    project_id: str
    product_version_id: str
    knowledge_pack: KnowledgePack
    manual_references: Sequence[ManualReference]


@dataclass(frozen=True)
class PrepareWS1InputsResult:
    project_id: str
    product_version_id: str
    knowledge_pack: KnowledgePack
    manual_references: tuple[ManualReference, ...]
    reference_count: int
    status: Literal["prepared"] = "prepared"


def prepare_ws1_inputs(request: PrepareWS1InputsRequest) -> PrepareWS1InputsResult:
    """Prepare versioned knowledge and manual references for later WS-1 steps."""

    project_id = _required_text(request.project_id, "project_id")
    product_version_id = _required_text(request.product_version_id, "product_version_id")
    if not isinstance(request.knowledge_pack, KnowledgePack):
        raise DomainValidationError("knowledge_pack must be a KnowledgePack")

    references = tuple(request.manual_references)
    reference_count = len(references)
    if reference_count < 3:
        raise DomainValidationError("WS-1 input preparation requires at least 3 manual References")
    if reference_count > 5:
        raise DomainValidationError("WS-1 input preparation allows at most 5 manual References")

    for reference in references:
        if not isinstance(reference, ManualReference):
            raise DomainValidationError("manual_references must contain ManualReference items")
        if reference.project_id != project_id:
            raise DomainValidationError("Manual Reference must bind to the ContentProject")
        if reference.product_version_id != product_version_id:
            raise DomainValidationError("Manual Reference must bind to the ProductVersion")
        if reference.intake_method != "manual":
            raise DomainValidationError("Manual Reference intake_method must be manual")

    return PrepareWS1InputsResult(
        project_id=project_id,
        product_version_id=product_version_id,
        knowledge_pack=request.knowledge_pack,
        manual_references=references,
        reference_count=reference_count,
    )


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DomainValidationError(f"{field_name} is required")
    return value.strip()

