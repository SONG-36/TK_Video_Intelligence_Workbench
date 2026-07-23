"""Thin in-memory WS-1 services for inputs, concepts, ScriptPacks, and review."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from typing import Literal, Sequence

from tvi_workbench.ws0 import DomainValidationError

from .domain import CreativeConceptDraft, KnowledgePack, ManualReference, ReviewDecision, ScriptPackDraft


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


@dataclass(frozen=True)
class GenerateScriptPackDraftRequest:
    prepared_inputs: PrepareWS1InputsResult
    concept: CreativeConceptDraft


CONCEPT_GENERATION_METHOD = "deterministic_mock_v0"
MANUAL_CONCEPT_GENERATION_METHOD = "human_manual_v0"
HUMAN_EDITED_CONCEPT_GENERATION_METHOD = "human_edited_v0"
SCRIPT_PACK_GENERATION_METHOD = "deterministic_mock_v0"

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
    project_id = _required_text(prepared_inputs.project_id, "project_id")
    product_version_id = _required_text(prepared_inputs.product_version_id, "product_version_id")
    if prepared_inputs.status != "prepared":
        raise DomainValidationError(f"{action} requires prepared WS-1 inputs")
    if not isinstance(prepared_inputs.knowledge_pack, KnowledgePack):
        raise DomainValidationError("prepared_inputs knowledge_pack must be a KnowledgePack")
    if prepared_inputs.knowledge_pack.version != "v0.1":
        raise DomainValidationError(f"{action} requires Knowledge Pack v0.1")

    actual_reference_count = len(prepared_inputs.manual_references)
    if actual_reference_count != prepared_inputs.reference_count:
        raise DomainValidationError("prepared input reference_count must match manual_references length")
    if not 3 <= actual_reference_count <= 5:
        raise DomainValidationError(f"{action} requires 3-5 ManualReferences")
    for reference in prepared_inputs.manual_references:
        if not isinstance(reference, ManualReference):
            raise DomainValidationError("prepared_inputs manual_references must contain ManualReference items")
        if reference.project_id != project_id:
            raise DomainValidationError("Manual Reference must bind to the ContentProject")
        if reference.product_version_id != product_version_id:
            raise DomainValidationError("Manual Reference must bind to the ProductVersion")
        if reference.intake_method != "manual":
            raise DomainValidationError("Manual Reference intake_method must be manual")
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
    if angle is None and title is None and hook is None and rationale is None:
        raise DomainValidationError("CreativeConcept edit requires at least one owner-facing field")
    return replace(
        concept,
        angle=_required_text(angle, "angle") if angle is not None else concept.angle,
        title=_required_text(title, "title") if title is not None else concept.title,
        hook=_required_text(hook, "hook") if hook is not None else concept.hook,
        rationale=_required_text(rationale, "rationale") if rationale is not None else concept.rationale,
        generation_method=HUMAN_EDITED_CONCEPT_GENERATION_METHOD,
        status="draft",
    )


def generate_script_pack_draft(
    request: GenerateScriptPackDraftRequest,
) -> ScriptPackDraft:
    """Generate one deterministic mock ScriptPack Draft from a selected concept."""

    prepared_inputs = _validate_prepared_inputs(
        request.prepared_inputs,
        action="ScriptPack Draft generation",
    )
    concept = _validate_script_pack_concept(prepared_inputs, request.concept)

    return ScriptPackDraft(
        id=create_script_pack_id(concept),
        project_id=prepared_inputs.project_id,
        product_version_id=prepared_inputs.product_version_id,
        concept_id=concept.id,
        title=f"{concept.title} ScriptPack Draft",
        target_duration_seconds=35,
        aspect_ratio="9:16",
        voiceover_script=(
            f"{concept.hook} In this car vacuum cleaner demo, we show the mess, "
            "clean it with the product sample, and tie each visible claim back to recorded Evidence Lite."
        ),
        storyboard=(
            f"Open on the selected angle: {concept.angle}.",
            "Show the car mess before introducing the product.",
            "Demonstrate the cleanup using only supportable claims.",
            "Close with the clean result and a simple ownership prompt.",
        ),
        shot_list=(
            "Close-up of crumbs, dust, or floor mat debris.",
            "Product sample entering frame in vertical 9:16 composition.",
            "Short cleanup pass with visible before/after contrast.",
            "Final reset shot inside the car.",
        ),
        visual_requirements=(
            "Keep all claims observable on camera.",
            "Use close-up proof shots for Evidence-backed details.",
            "Avoid unsupported performance guarantees.",
        ),
        asset_requirements=(
            "Car vacuum cleaner sample matching the ProductVersion Lite trace.",
            "Car interior with realistic crumbs or dust.",
            "Reference-inspired pacing notes from manual References.",
        ),
        generation_notes=(
            "Deterministic mock ScriptPack Draft for WS-1 Step 4A.",
            "No AI provider, prompt system, export, or rendering orchestration is used.",
        ),
        risk_notes=(
            "Human review is required before approval.",
            "Do not present supplier claims beyond the attached Evidence Lite.",
        ),
        evidence_refs=concept.evidence_refs,
        manual_reference_refs=concept.manual_reference_refs,
        knowledge_pack_id=concept.knowledge_pack_id,
        knowledge_pack_version=concept.knowledge_pack_version,
        generation_method=SCRIPT_PACK_GENERATION_METHOD,
    )


def review_script_pack(
    script_pack: ScriptPackDraft,
    *,
    decision: str,
    reviewer_note: str,
) -> ReviewDecision:
    """Record a human review decision without mutating the ScriptPack Draft."""

    if not isinstance(script_pack, ScriptPackDraft):
        raise DomainValidationError("script_pack must be a ScriptPackDraft")
    return ReviewDecision(
        project_id=script_pack.project_id,
        script_pack_id=script_pack.id,
        decision=decision,
        reviewer_note=reviewer_note,
    )


def create_script_pack_id(concept: CreativeConceptDraft) -> str:
    source = "|".join(
        [
            _required_text(concept.project_id, "project_id"),
            _required_text(concept.product_version_id, "product_version_id"),
            _required_text(concept.id, "concept_id"),
            _required_text(concept.angle, "angle"),
            _required_text(concept.title, "title"),
            _required_text(concept.hook, "hook"),
            _required_text(concept.rationale, "rationale"),
        ]
    )
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:12]
    return f"script-pack-{digest}"


def _validate_script_pack_concept(
    prepared_inputs: PrepareWS1InputsResult,
    concept: CreativeConceptDraft,
) -> CreativeConceptDraft:
    if not isinstance(concept, CreativeConceptDraft):
        raise DomainValidationError("concept must be a CreativeConceptDraft")
    if concept.status != "draft":
        raise DomainValidationError("ScriptPack Draft generation requires a draft CreativeConcept")
    if not concept.selected:
        raise DomainValidationError("ScriptPack Draft generation requires a selected CreativeConcept")
    if concept.project_id != prepared_inputs.project_id:
        raise DomainValidationError("CreativeConcept must bind to the prepared ContentProject")
    if concept.product_version_id != prepared_inputs.product_version_id:
        raise DomainValidationError("CreativeConcept must bind to the prepared ProductVersion")
    if concept.knowledge_pack_id != prepared_inputs.knowledge_pack.id:
        raise DomainValidationError("CreativeConcept must preserve the prepared Knowledge Pack")
    if concept.knowledge_pack_version != prepared_inputs.knowledge_pack.version:
        raise DomainValidationError("CreativeConcept must preserve the prepared Knowledge Pack version")

    manual_reference_refs = tuple(reference.id for reference in prepared_inputs.manual_references)
    if concept.manual_reference_refs != manual_reference_refs:
        raise DomainValidationError("CreativeConcept must preserve the prepared ManualReference trace")
    if not concept.evidence_refs:
        raise DomainValidationError("CreativeConcept must preserve Evidence trace")
    return concept


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
