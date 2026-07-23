"""Thin in-memory WS-1 services for inputs, concepts, ScriptPacks, and review."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from typing import Any, Literal, Sequence

from tvi_workbench.ws0 import DomainValidationError

from .domain import (
    CreativeConceptDraft,
    ExportBusinessContext,
    KnowledgePack,
    ManualReference,
    ProductionPackExport,
    ReviewDecision,
    ScriptPackDraft,
)


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


@dataclass(frozen=True)
class ExportProductionPackRequest:
    business_context: ExportBusinessContext
    prepared_inputs: PrepareWS1InputsResult
    concept_drafts: Sequence[CreativeConceptDraft]
    selected_concept: CreativeConceptDraft
    script_pack: ScriptPackDraft
    review: ReviewDecision


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


def export_production_pack_markdown(request: ExportProductionPackRequest) -> str:
    """Build a human-readable Generation-ready Production Pack preview."""

    export_data = _build_production_pack_data(request)
    markdown = _render_production_pack_markdown(export_data)
    return ProductionPackExport(
        format="markdown",
        project_id=export_data["project_id"],
        product_version_id=export_data["product_version_id"],
        production_readiness=export_data["production_readiness"],
        content=markdown,
    ).content


def export_production_pack_json(request: ExportProductionPackRequest) -> dict[str, Any]:
    """Build a JSON-compatible Generation-ready Production Pack dict."""

    export_data = _build_production_pack_data(request)
    return dict(
        ProductionPackExport(
            format="json",
            project_id=export_data["project_id"],
            product_version_id=export_data["product_version_id"],
            production_readiness=export_data["production_readiness"],
            content=export_data,
        ).content
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


def _build_production_pack_data(request: ExportProductionPackRequest) -> dict[str, Any]:
    prepared_inputs = _validate_prepared_inputs(
        request.prepared_inputs,
        action="Production Pack export",
    )
    business_context = _validate_export_business_context(request.business_context)
    concept_drafts = _validate_export_concepts(prepared_inputs, request.concept_drafts)
    selected_concept = _validate_selected_export_concept(prepared_inputs, request.selected_concept)
    script_pack = _validate_export_script_pack(prepared_inputs, selected_concept, request.script_pack)
    review = _validate_export_review(prepared_inputs, script_pack, request.review)
    production_readiness = _production_readiness(review)

    return {
        "project_id": prepared_inputs.project_id,
        "product_context": {
            "project_id": prepared_inputs.project_id,
            "product_version_id": prepared_inputs.product_version_id,
            "product_name": business_context.product_name,
            "product_version_label": business_context.product_version_label,
            "summary": business_context.product_context_summary,
        },
        "handoff_context": {
            "summary": business_context.handoff_summary,
            "target_market": business_context.target_market,
            "platform": business_context.platform,
            "content_objective": business_context.content_objective,
        },
        "selection_to_content_handoff_summary": business_context.handoff_summary,
        "product_version_id": prepared_inputs.product_version_id,
        "evidence_refs": list(script_pack.evidence_refs),
        "knowledge_pack": {
            "id": prepared_inputs.knowledge_pack.id,
            "version": prepared_inputs.knowledge_pack.version,
            "title": prepared_inputs.knowledge_pack.title,
        },
        "manual_references": [
            {
                "id": reference.id,
                "title": reference.title,
                "source_identifier": reference.source_identifier,
                "source_type": reference.source_type,
                "summary": reference.summary,
                "observed_pattern": reference.observed_pattern,
                "content_notes": reference.content_notes,
                "usage_notes": reference.usage_notes,
                "intake_method": reference.intake_method,
                "project_id": reference.project_id,
                "product_version_id": reference.product_version_id,
            }
            for reference in prepared_inputs.manual_references
        ],
        "manual_reference_refs": list(script_pack.manual_reference_refs),
        "creative_concept_summaries": [
            _concept_summary(concept) for concept in concept_drafts
        ],
        "selected_concept": _concept_summary(selected_concept),
        "selected_concept_id": selected_concept.id,
        "concept_generation_method": selected_concept.generation_method,
        "script_pack": {
            "id": script_pack.id,
            "status": script_pack.status,
            "concept_id": script_pack.concept_id,
            "title": script_pack.title,
            "target_duration_seconds": script_pack.target_duration_seconds,
            "aspect_ratio": script_pack.aspect_ratio,
            "voiceover_script": script_pack.voiceover_script,
            "storyboard": list(script_pack.storyboard),
            "shot_list": list(script_pack.shot_list),
            "visual_requirements": list(script_pack.visual_requirements),
            "asset_requirements": list(script_pack.asset_requirements),
            "generation_notes": list(script_pack.generation_notes),
            "risk_notes": list(script_pack.risk_notes),
            "generation_method": script_pack.generation_method,
        },
        "script_pack_id": script_pack.id,
        "review": {
            "decision": review.decision,
            "reviewer_note": review.reviewer_note,
            "project_id": review.project_id,
            "script_pack_id": review.script_pack_id,
        },
        "production_readiness": production_readiness,
    }


def _validate_export_concepts(
    prepared_inputs: PrepareWS1InputsResult,
    concept_drafts: Sequence[CreativeConceptDraft],
) -> tuple[CreativeConceptDraft, ...]:
    concepts = tuple(concept_drafts)
    if len(concepts) != 3:
        raise DomainValidationError("Production Pack export requires all three CreativeConcept Draft summaries")
    for concept in concepts:
        if not isinstance(concept, CreativeConceptDraft):
            raise DomainValidationError("concept_drafts must contain CreativeConceptDraft items")
        _validate_concept_trace(prepared_inputs, concept)
    return concepts


def _validate_export_business_context(
    business_context: ExportBusinessContext,
) -> ExportBusinessContext:
    if not isinstance(business_context, ExportBusinessContext):
        raise DomainValidationError("business_context must be an ExportBusinessContext")
    return ExportBusinessContext(
        product_context_summary=_required_text(
            business_context.product_context_summary,
            "product_context_summary",
        ),
        handoff_summary=_required_text(business_context.handoff_summary, "handoff_summary"),
        target_market=_required_text(business_context.target_market, "target_market"),
        platform=_required_text(business_context.platform, "platform"),
        content_objective=_required_text(business_context.content_objective, "content_objective"),
        product_name=_required_text(business_context.product_name, "product_name"),
        product_version_label=_required_text(
            business_context.product_version_label,
            "product_version_label",
        ),
    )


def _validate_selected_export_concept(
    prepared_inputs: PrepareWS1InputsResult,
    selected_concept: CreativeConceptDraft,
) -> CreativeConceptDraft:
    if not isinstance(selected_concept, CreativeConceptDraft):
        raise DomainValidationError("selected_concept must be a CreativeConceptDraft")
    if not selected_concept.selected:
        raise DomainValidationError("Production Pack export requires a selected CreativeConcept")
    _validate_concept_trace(prepared_inputs, selected_concept)
    return selected_concept


def _validate_export_script_pack(
    prepared_inputs: PrepareWS1InputsResult,
    selected_concept: CreativeConceptDraft,
    script_pack: ScriptPackDraft,
) -> ScriptPackDraft:
    if not isinstance(script_pack, ScriptPackDraft):
        raise DomainValidationError("script_pack must be a ScriptPackDraft")
    if script_pack.project_id != prepared_inputs.project_id:
        raise DomainValidationError("ScriptPackDraft must bind to the prepared ContentProject")
    if script_pack.product_version_id != prepared_inputs.product_version_id:
        raise DomainValidationError("ScriptPackDraft must bind to the prepared ProductVersion")
    if selected_concept.id != script_pack.concept_id:
        raise DomainValidationError("Selected CreativeConcept must match ScriptPackDraft concept_id")
    if script_pack.evidence_refs != selected_concept.evidence_refs:
        raise DomainValidationError("ScriptPackDraft must preserve selected CreativeConcept Evidence trace")
    if script_pack.manual_reference_refs != selected_concept.manual_reference_refs:
        raise DomainValidationError("ScriptPackDraft must preserve selected CreativeConcept ManualReference trace")
    if script_pack.knowledge_pack_id != selected_concept.knowledge_pack_id:
        raise DomainValidationError("ScriptPackDraft must preserve selected CreativeConcept Knowledge Pack")
    if script_pack.knowledge_pack_version != selected_concept.knowledge_pack_version:
        raise DomainValidationError("ScriptPackDraft must preserve selected CreativeConcept Knowledge Pack version")
    return script_pack


def _validate_export_review(
    prepared_inputs: PrepareWS1InputsResult,
    script_pack: ScriptPackDraft,
    review: ReviewDecision,
) -> ReviewDecision:
    if not isinstance(review, ReviewDecision):
        raise DomainValidationError("review must be a ReviewDecision")
    if review.project_id != prepared_inputs.project_id:
        raise DomainValidationError("ReviewDecision must bind to the prepared ContentProject")
    if review.script_pack_id != script_pack.id:
        raise DomainValidationError("ReviewDecision script_pack_id must match ScriptPackDraft id")
    return review


def _validate_concept_trace(
    prepared_inputs: PrepareWS1InputsResult,
    concept: CreativeConceptDraft,
) -> None:
    if concept.project_id != prepared_inputs.project_id:
        raise DomainValidationError("CreativeConcept must bind to the prepared ContentProject")
    if concept.product_version_id != prepared_inputs.product_version_id:
        raise DomainValidationError("CreativeConcept must bind to the prepared ProductVersion")
    if concept.knowledge_pack_id != prepared_inputs.knowledge_pack.id:
        raise DomainValidationError("CreativeConcept must preserve the prepared Knowledge Pack")
    if concept.knowledge_pack_version != prepared_inputs.knowledge_pack.version:
        raise DomainValidationError("CreativeConcept must preserve the prepared Knowledge Pack version")

    evidence_refs = tuple(_required_text(ref, "evidence_ref") for ref in concept.evidence_refs)
    if not evidence_refs:
        raise DomainValidationError("Production Pack export requires Evidence trace")
    manual_reference_refs = tuple(reference.id for reference in prepared_inputs.manual_references)
    if concept.manual_reference_refs != manual_reference_refs:
        raise DomainValidationError("CreativeConcept must preserve the prepared ManualReference trace")


def _production_readiness(review: ReviewDecision) -> Literal["generation_ready", "not_generation_ready"]:
    if review.decision == "approved":
        return "generation_ready"
    return "not_generation_ready"


def _concept_summary(concept: CreativeConceptDraft) -> dict[str, Any]:
    return {
        "id": concept.id,
        "angle": concept.angle,
        "title": concept.title,
        "hook": concept.hook,
        "rationale": concept.rationale,
        "status": concept.status,
        "selected": concept.selected,
        "generation_method": concept.generation_method,
        "project_id": concept.project_id,
        "product_version_id": concept.product_version_id,
        "evidence_refs": list(concept.evidence_refs),
        "manual_reference_refs": list(concept.manual_reference_refs),
        "knowledge_pack_id": concept.knowledge_pack_id,
        "knowledge_pack_version": concept.knowledge_pack_version,
    }


def _render_production_pack_markdown(export_data: dict[str, Any]) -> str:
    script_pack = export_data["script_pack"]
    review = export_data["review"]
    lines = [
        "# Generation-ready Owned Content Production Pack",
        "",
        "## Product Context",
        f"- Project ID: {export_data['project_id']}",
        f"- ProductVersion ID: {export_data['product_version_id']}",
        f"- Product Name: {export_data['product_context']['product_name']}",
        f"- ProductVersion Label: {export_data['product_context']['product_version_label']}",
        f"- Summary: {export_data['product_context']['summary']}",
        "",
        "## Selection-to-Content Handoff Summary",
        f"- Summary: {export_data['handoff_context']['summary']}",
        f"- Target Market: {export_data['handoff_context']['target_market']}",
        f"- Platform: {export_data['handoff_context']['platform']}",
        f"- Content Objective: {export_data['handoff_context']['content_objective']}",
        "",
        "## ProductVersion Lite",
        f"- ProductVersion ID: {export_data['product_version_id']}",
        "",
        "## Evidence References",
        *_bullet_lines(export_data["evidence_refs"]),
        "",
        "## Knowledge Pack",
        f"- ID: {export_data['knowledge_pack']['id']}",
        f"- Version: {export_data['knowledge_pack']['version']}",
        f"- Title: {export_data['knowledge_pack']['title']}",
        "",
        "## Manual References",
        *[
            (
                f"- {reference['id']}: {reference['title']} "
                f"({reference['source_type']} - {reference['source_identifier']})"
            )
            for reference in export_data["manual_references"]
        ],
        "",
        "## CreativeConcept Draft Summaries",
        *[
            f"- {concept['id']}: {concept['angle']} | {concept['title']} | {concept['status']}"
            for concept in export_data["creative_concept_summaries"]
        ],
        "",
        "## Selected / Human-edited Concept",
        f"- ID: {export_data['selected_concept']['id']}",
        f"- Angle: {export_data['selected_concept']['angle']}",
        f"- Title: {export_data['selected_concept']['title']}",
        f"- Hook: {export_data['selected_concept']['hook']}",
        f"- Rationale: {export_data['selected_concept']['rationale']}",
        f"- Generation Method: {export_data['selected_concept']['generation_method']}",
        "",
        "## Script",
        f"- ScriptPack ID: {script_pack['id']}",
        f"- ScriptPack Status: {script_pack['status']}",
        f"- Target Duration Seconds: {script_pack['target_duration_seconds']}",
        f"- Aspect Ratio: {script_pack['aspect_ratio']}",
        "",
        script_pack["voiceover_script"],
        "",
        "## Storyboard",
        *_numbered_lines(script_pack["storyboard"]),
        "",
        "## Shot List",
        *_numbered_lines(script_pack["shot_list"]),
        "",
        "## Visual Requirements",
        *_bullet_lines(script_pack["visual_requirements"]),
        "",
        "## Asset Requirements",
        *_bullet_lines(script_pack["asset_requirements"]),
        "",
        "## Generation Notes",
        *_bullet_lines(script_pack["generation_notes"]),
        "",
        "## Risk Notes",
        *_bullet_lines(script_pack["risk_notes"]),
        "",
        "## Human Review",
        f"- Decision: {review['decision']}",
        f"- Reviewer Note: {review['reviewer_note']}",
        "",
        "## Production Readiness",
        export_data["production_readiness"],
        "",
    ]
    return "\n".join(lines)


def _bullet_lines(values: Sequence[str]) -> list[str]:
    return [f"- {value}" for value in values]


def _numbered_lines(values: Sequence[str]) -> list[str]:
    return [f"{index}. {value}" for index, value in enumerate(values, start=1)]


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
