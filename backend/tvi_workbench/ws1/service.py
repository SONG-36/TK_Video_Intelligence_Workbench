"""Thin WS-1 input preparation service."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from typing import Literal, Sequence

from tvi_workbench.ws0 import DomainValidationError

from .domain import CreativeConceptDraft, KnowledgePack, ManualReference


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


@dataclass(frozen=True)
class GenerateCreativeConceptDraftsRequest:
    prepared_inputs: PrepareWS1InputsResult
    evidence_refs: Sequence[str]


@dataclass(frozen=True)
class GenerateCreativeConceptDraftsResult:
    project_id: str
    product_version_id: str
    concepts: tuple[CreativeConceptDraft, ...]
    generation_method: str


CONCEPT_GENERATION_METHOD = "deterministic_mock_v0"
MANUAL_CONCEPT_GENERATION_METHOD = "human_manual_v0"
HUMAN_EDITED_CONCEPT_GENERATION_METHOD = "human_edited_v0"

CONCEPT_ANGLES = (
    (
        "mess-rescue-crumb-disaster",
        "Mess Rescue / Crumb Disaster",
        "Crumbs everywhere after one commute?",
        "Show a relatable crumb disaster and position the vacuum as the quick rescue.",
    ),
    (
        "hidden-dirt-proof",
        "Hidden Dirt Proof",
        "Your car looks clean until the camera gets close.",
        "Reveal hidden dirt in seams and floor mats, then tie cleanup back to Evidence Lite.",
    ),
    (
        "daily-car-reset",
        "Daily Car Reset",
        "A 60-second reset before your next drive.",
        "Frame the product as a daily reset habit for a cleaner-feeling car.",
    ),
)


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


def _validate_prepared_inputs(
    prepared_inputs: PrepareWS1InputsResult,
    *,
    action: str,
) -> PrepareWS1InputsResult:
    if not isinstance(prepared_inputs, PrepareWS1InputsResult):
        raise DomainValidationError("prepared_inputs must be a PrepareWS1InputsResult")
    if prepared_inputs.status != "prepared":
        raise DomainValidationError(f"{action} requires prepared WS-1 inputs")
    if prepared_inputs.knowledge_pack.version != "v0.1":
        raise DomainValidationError(f"{action} requires Knowledge Pack v0.1")

    actual_reference_count = len(prepared_inputs.manual_references)
    if actual_reference_count != prepared_inputs.reference_count:
        raise DomainValidationError("prepared input reference_count must match manual_references length")
    if not 3 <= actual_reference_count <= 5:
        raise DomainValidationError(f"{action} requires 3-5 ManualReferences")
    return prepared_inputs


def generate_creative_concept_drafts(
    request: GenerateCreativeConceptDraftsRequest,
) -> GenerateCreativeConceptDraftsResult:
    """Generate exactly three deterministic mock CreativeConcept Drafts."""

    prepared_inputs = _validate_prepared_inputs(
        request.prepared_inputs,
        action="CreativeConcept generation",
    )

    evidence_refs = tuple(_required_text(ref, "evidence_ref") for ref in request.evidence_refs)
    if not evidence_refs:
        raise DomainValidationError("CreativeConcept generation requires Evidence trace")
    manual_reference_refs = tuple(reference.id for reference in prepared_inputs.manual_references)
    if not manual_reference_refs:
        raise DomainValidationError("CreativeConcept generation requires ManualReference trace")

    concepts = tuple(
        CreativeConceptDraft(
            id=f"concept-{slug}",
            project_id=prepared_inputs.project_id,
            product_version_id=prepared_inputs.product_version_id,
            angle=angle,
            title=angle,
            hook=hook,
            rationale=rationale,
            evidence_refs=evidence_refs,
            manual_reference_refs=manual_reference_refs,
            knowledge_pack_id=prepared_inputs.knowledge_pack.id,
            knowledge_pack_version=prepared_inputs.knowledge_pack.version,
            generation_method=CONCEPT_GENERATION_METHOD,
        )
        for slug, angle, hook, rationale in CONCEPT_ANGLES
    )
    return GenerateCreativeConceptDraftsResult(
        project_id=prepared_inputs.project_id,
        product_version_id=prepared_inputs.product_version_id,
        concepts=concepts,
        generation_method=CONCEPT_GENERATION_METHOD,
    )


def create_manual_creative_concept(
    *,
    prepared_inputs: PrepareWS1InputsResult,
    evidence_refs: Sequence[str],
    angle: str,
    title: str,
    hook: str,
    rationale: str,
) -> CreativeConceptDraft:
    """Create one owner-authored CreativeConcept Draft with preserved traceability."""

    prepared_inputs = _validate_prepared_inputs(
        prepared_inputs,
        action="Manual CreativeConcept creation",
    )

    evidence_refs_tuple = tuple(_required_text(ref, "evidence_ref") for ref in evidence_refs)
    if not evidence_refs_tuple:
        raise DomainValidationError("Manual CreativeConcept creation requires Evidence trace")
    manual_reference_refs = tuple(reference.id for reference in prepared_inputs.manual_references)
    if not manual_reference_refs:
        raise DomainValidationError("Manual CreativeConcept creation requires ManualReference trace")

    cleaned_angle = _required_text(angle, "angle")
    return CreativeConceptDraft(
        id=create_manual_concept_id(
            project_id=prepared_inputs.project_id,
            product_version_id=prepared_inputs.product_version_id,
            angle=cleaned_angle,
            title=title,
            hook=hook,
        ),
        project_id=prepared_inputs.project_id,
        product_version_id=prepared_inputs.product_version_id,
        angle=cleaned_angle,
        title=_required_text(title, "title"),
        hook=_required_text(hook, "hook"),
        rationale=_required_text(rationale, "rationale"),
        evidence_refs=evidence_refs_tuple,
        manual_reference_refs=manual_reference_refs,
        knowledge_pack_id=prepared_inputs.knowledge_pack.id,
        knowledge_pack_version=prepared_inputs.knowledge_pack.version,
        generation_method=MANUAL_CONCEPT_GENERATION_METHOD,
    )


def select_creative_concept(
    concepts: Sequence[CreativeConceptDraft],
    *,
    concept_id: str,
) -> CreativeConceptDraft:
    """Select one draft concept without approving it."""

    selected = [concept for concept in concepts if concept.id == concept_id]
    if not selected:
        raise DomainValidationError("Selected CreativeConcept Draft does not exist")
    if len(selected) > 1:
        raise DomainValidationError("Selected CreativeConcept Draft id is ambiguous")
    return replace(selected[0], selected=True, status="draft")


def edit_selected_creative_concept(
    concept: CreativeConceptDraft,
    *,
    angle: str | None = None,
    title: str | None = None,
    hook: str | None = None,
    rationale: str | None = None,
) -> CreativeConceptDraft:
    """Edit owner-facing fields while preserving traceability and draft status."""

    if not concept.selected:
        raise DomainValidationError("Only a selected CreativeConcept Draft can be edited")
    return replace(
        concept,
        angle=_required_text(angle, "angle") if angle is not None else concept.angle,
        title=_required_text(title, "title") if title is not None else concept.title,
        hook=_required_text(hook, "hook") if hook is not None else concept.hook,
        rationale=_required_text(rationale, "rationale") if rationale is not None else concept.rationale,
        generation_method=HUMAN_EDITED_CONCEPT_GENERATION_METHOD,
        status="draft",
    )


def create_manual_concept_id(
    *,
    project_id: str,
    product_version_id: str,
    angle: str,
    title: str,
    hook: str,
) -> str:
    source = "|".join(
        [
            _required_text(project_id, "project_id"),
            _required_text(product_version_id, "product_version_id"),
            _required_text(angle, "angle"),
            _required_text(title, "title"),
            _required_text(hook, "hook"),
        ]
    )
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:12]
    return f"concept-manual-{digest}"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "owner-concept"
