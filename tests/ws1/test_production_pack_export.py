import json
from dataclasses import fields, replace

import pytest

from tvi_workbench.ws0 import (
    CreateWS0ProjectRequest,
    DomainValidationError,
    EvidenceCategory,
    EvidenceInput,
    OperatingContextInput,
    ProductInput,
    ProductVersionInput,
    ProjectInput,
    create_project_from_handoff,
)
from tvi_workbench.ws1 import (
    CreativeConceptDraft,
    ExportBusinessContext,
    ExportProductionPackRequest,
    GenerateCreativeConceptDraftsRequest,
    GenerateScriptPackDraftRequest,
    KnowledgePack,
    ManualReference,
    PrepareWS1InputsRequest,
    ReviewDecision,
    export_production_pack_json,
    export_production_pack_markdown,
    generate_creative_concept_drafts,
    generate_script_pack_draft,
    prepare_ws1_inputs,
    review_script_pack,
    select_creative_concept,
)


def make_ws0_result():
    return create_project_from_handoff(
        CreateWS0ProjectRequest(
            project=ProjectInput(id="cp-car-vacuum-001", name="Car vacuum cleaner pilot"),
            operating_context=OperatingContextInput(
                selection_rationale="Car owners need a compact cleaning solution.",
                target_market="US",
                platform="TikTok",
                content_objective="Validate practical in-car mess demos.",
                test_question="Does a real car cleanup hook earn attention?",
                project_owner="Content owner",
                initial_route_hypothesis="Problem-solution demo",
            ),
            product=ProductInput(id="prod-car-vacuum", name="Portable car vacuum cleaner"),
            product_version=ProductVersionInput(
                id="pv-car-vacuum-sample-a",
                label="Sample A lite version",
            ),
            evidence=(
                EvidenceInput(
                    id="ev-supplier-claim-001",
                    category=EvidenceCategory.SUPPLIER_CLAIM,
                    source="Supplier product page",
                    summary="Supplier claims compact in-car cleaning support.",
                ),
                EvidenceInput(
                    id="ev-observation-001",
                    category=EvidenceCategory.USER_OBSERVATION,
                    source="Owner observation",
                    summary="Owner observes the sample fits in a glove compartment.",
                ),
            ),
        )
    )


def make_knowledge_pack() -> KnowledgePack:
    return KnowledgePack(
        id="kp-car-vacuum-v01",
        version="v0.1",
        title="Car vacuum cleaner content knowledge pack v0.1",
        content_summary="Rules and patterns for practical car cleaning demos.",
        sections={
            "script_rules": "Use observable claims and avoid unsupported guarantees.",
            "hook_guidance": "Open with visible in-car mess before product reveal.",
            "claims_guardrails": "Tie claims back to Evidence Lite.",
        },
    )


def make_reference(reference_id: str, project_id: str, product_version_id: str) -> ManualReference:
    return ManualReference(
        id=reference_id,
        project_id=project_id,
        product_version_id=product_version_id,
        title=f"Manual reference {reference_id}",
        source_identifier=f"https://example.com/{reference_id}",
        source_type="TikTok manual URL",
        summary="A manually entered reference for car cleaning content.",
        observed_pattern="Mess-first hook followed by compact product demo.",
        usage_notes="Use as a hook and pacing reference.",
    )


def make_prepared_bundle():
    ws0 = make_ws0_result()
    references = tuple(
        make_reference(
            reference_id=f"ref-{index}",
            project_id=ws0.project.id,
            product_version_id=ws0.product_version.id,
        )
        for index in range(1, 4)
    )
    prepared = prepare_ws1_inputs(
        PrepareWS1InputsRequest(
            project_id=ws0.project.id,
            product_version_id=ws0.product_version.id,
            knowledge_pack=make_knowledge_pack(),
            manual_references=references,
        )
    )
    evidence_refs = tuple(evidence.id for evidence in ws0.evidence)
    return prepared, evidence_refs


def make_business_context() -> ExportBusinessContext:
    return ExportBusinessContext(
        product_context_summary=(
            "Portable car vacuum cleaner sample for a practical in-car cleanup pilot."
        ),
        handoff_summary=(
            "Selection handoff asks whether visible crumb cleanup can support a TikTok demo route."
        ),
        target_market="US car owners",
        platform="TikTok",
        content_objective="Validate a practical mess-first car cleaning concept.",
        product_name="Portable car vacuum cleaner",
        product_version_label="Sample A lite version",
    )


def make_export_request(decision: str = "approved") -> ExportProductionPackRequest:
    prepared, evidence_refs = make_prepared_bundle()
    concept_result = generate_creative_concept_drafts(
        GenerateCreativeConceptDraftsRequest(
            prepared_inputs=prepared,
            evidence_refs=evidence_refs,
        )
    )
    selected = select_creative_concept(
        concept_result.concepts,
        concept_id=concept_result.concepts[0].id,
    )
    script_pack = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared,
            concept=selected,
        )
    )
    review = review_script_pack(
        script_pack,
        decision=decision,
        reviewer_note="Approved for generation handoff.",
    )
    return ExportProductionPackRequest(
        business_context=make_business_context(),
        prepared_inputs=prepared,
        concept_drafts=concept_result.concepts,
        selected_concept=selected,
        script_pack=script_pack,
        review=review,
    )


def unsafe_creative_concept(base: CreativeConceptDraft, **updates) -> CreativeConceptDraft:
    values = {field.name: getattr(base, field.name) for field in fields(CreativeConceptDraft)}
    values.update(updates)
    concept = object.__new__(CreativeConceptDraft)
    for key, value in values.items():
        object.__setattr__(concept, key, value)
    return concept


def unsafe_business_context(**updates) -> ExportBusinessContext:
    values = {
        "product_context_summary": "Portable car vacuum cleaner sample for production handoff.",
        "handoff_summary": "Selection handoff asks for a practical TikTok cleanup test.",
        "target_market": "US car owners",
        "platform": "TikTok",
        "content_objective": "Validate a practical mess-first car cleaning concept.",
        "product_name": "Portable car vacuum cleaner",
        "product_version_label": "Sample A lite version",
    }
    values.update(updates)
    context = object.__new__(ExportBusinessContext)
    for key, value in values.items():
        object.__setattr__(context, key, value)
    return context


def test_approved_review_exports_markdown() -> None:
    markdown = export_production_pack_markdown(make_export_request())

    assert markdown.startswith("# Generation-ready Owned Content Production Pack")
    assert "## Production Readiness" in markdown
    assert "generation_ready" in markdown


def test_approved_review_exports_json_compatible_dict() -> None:
    data = export_production_pack_json(make_export_request())

    assert isinstance(data, dict)
    json.dumps(data)


def test_markdown_includes_product_version_evidence_references_and_knowledge_pack_version() -> None:
    request = make_export_request()

    markdown = export_production_pack_markdown(request)

    assert request.prepared_inputs.product_version_id in markdown
    for evidence_ref in request.script_pack.evidence_refs:
        assert evidence_ref in markdown
    assert "v0.1" in markdown


def test_export_fails_when_product_context_summary_is_empty() -> None:
    request = make_export_request()

    with pytest.raises(DomainValidationError, match="product_context_summary is required"):
        export_production_pack_json(
            replace(
                request,
                business_context=unsafe_business_context(product_context_summary=""),
            )
        )


def test_export_fails_when_handoff_summary_is_empty() -> None:
    request = make_export_request()

    with pytest.raises(DomainValidationError, match="handoff_summary is required"):
        export_production_pack_json(
            replace(
                request,
                business_context=unsafe_business_context(handoff_summary=""),
            )
        )


def test_markdown_includes_product_context_summary() -> None:
    request = make_export_request()

    markdown = export_production_pack_markdown(request)

    assert request.business_context.product_context_summary in markdown
    assert request.business_context.product_name in markdown
    assert request.business_context.product_version_label in markdown


def test_markdown_includes_handoff_summary() -> None:
    request = make_export_request()

    markdown = export_production_pack_markdown(request)

    assert request.business_context.handoff_summary in markdown
    assert request.business_context.target_market in markdown
    assert request.business_context.platform in markdown
    assert request.business_context.content_objective in markdown


def test_markdown_includes_manual_reference_refs() -> None:
    request = make_export_request()

    markdown = export_production_pack_markdown(request)

    for reference in request.prepared_inputs.manual_references:
        assert reference.id in markdown


def test_markdown_includes_all_three_creative_concept_draft_summaries() -> None:
    request = make_export_request()

    markdown = export_production_pack_markdown(request)

    for concept in request.concept_drafts:
        assert concept.id in markdown
        assert concept.angle in markdown


def test_markdown_includes_selected_or_human_edited_concept() -> None:
    request = make_export_request()

    markdown = export_production_pack_markdown(request)

    assert "## Selected / Human-edited Concept" in markdown
    assert request.selected_concept.id in markdown
    assert request.selected_concept.hook in markdown


def test_markdown_includes_script_pack_script_storyboard_and_shot_list() -> None:
    request = make_export_request()

    markdown = export_production_pack_markdown(request)

    assert request.script_pack.voiceover_script in markdown
    for storyboard_item in request.script_pack.storyboard:
        assert storyboard_item in markdown
    for shot in request.script_pack.shot_list:
        assert shot in markdown


def test_markdown_includes_review_decision_and_reviewer_note() -> None:
    request = make_export_request()

    markdown = export_production_pack_markdown(request)

    assert request.review.decision in markdown
    assert request.review.reviewer_note in markdown


def test_json_preserves_project_product_evidence_reference_and_knowledge_trace() -> None:
    request = make_export_request()

    data = export_production_pack_json(request)

    assert data["project_id"] == request.prepared_inputs.project_id
    assert data["product_version_id"] == request.prepared_inputs.product_version_id
    assert data["evidence_refs"] == list(request.script_pack.evidence_refs)
    assert data["manual_reference_refs"] == list(request.script_pack.manual_reference_refs)
    assert data["knowledge_pack"]["id"] == request.prepared_inputs.knowledge_pack.id
    assert data["knowledge_pack"]["version"] == request.prepared_inputs.knowledge_pack.version


def test_json_includes_product_context() -> None:
    request = make_export_request()

    data = export_production_pack_json(request)

    assert data["product_context"] == {
        "project_id": request.prepared_inputs.project_id,
        "product_version_id": request.prepared_inputs.product_version_id,
        "product_name": request.business_context.product_name,
        "product_version_label": request.business_context.product_version_label,
        "summary": request.business_context.product_context_summary,
    }


def test_json_includes_handoff_context() -> None:
    request = make_export_request()

    data = export_production_pack_json(request)

    assert data["handoff_context"] == {
        "summary": request.business_context.handoff_summary,
        "target_market": request.business_context.target_market,
        "platform": request.business_context.platform,
        "content_objective": request.business_context.content_objective,
    }


def test_json_preserves_concept_script_pack_and_review_trace() -> None:
    request = make_export_request()

    data = export_production_pack_json(request)

    assert len(data["creative_concept_summaries"]) == 3
    assert data["selected_concept_id"] == request.selected_concept.id
    assert data["script_pack_id"] == request.script_pack.id
    assert data["review"]["decision"] == request.review.decision
    assert data["review"]["reviewer_note"] == request.review.reviewer_note


def test_approved_review_produces_generation_ready() -> None:
    data = export_production_pack_json(make_export_request(decision="approved"))

    assert data["production_readiness"] == "generation_ready"


@pytest.mark.parametrize("decision", ["rework", "hold", "stopped"])
def test_non_approved_review_produces_not_generation_ready(decision: str) -> None:
    data = export_production_pack_json(make_export_request(decision=decision))

    assert data["production_readiness"] == "not_generation_ready"


def test_export_fails_when_review_script_pack_id_mismatches_script_pack_id() -> None:
    request = make_export_request()
    mismatched_review = ReviewDecision(
        project_id=request.review.project_id,
        script_pack_id="script-pack-other",
        decision="approved",
        reviewer_note=request.review.reviewer_note,
    )

    with pytest.raises(DomainValidationError, match="script_pack_id must match"):
        export_production_pack_json(replace(request, review=mismatched_review))


def test_export_fails_when_selected_concept_id_mismatches_script_pack_concept_id() -> None:
    request = make_export_request()
    mismatched_concept = replace(request.selected_concept, id="concept-other")

    with pytest.raises(DomainValidationError, match="must match ScriptPackDraft concept_id"):
        export_production_pack_json(replace(request, selected_concept=mismatched_concept))


def test_export_fails_when_prepared_input_mismatches_script_pack_project() -> None:
    request = make_export_request()
    mismatched_script_pack = replace(request.script_pack, project_id="cp-other")

    with pytest.raises(DomainValidationError, match="prepared ContentProject"):
        export_production_pack_json(replace(request, script_pack=mismatched_script_pack))


def test_export_fails_when_prepared_input_mismatches_script_pack_product_version() -> None:
    request = make_export_request()
    mismatched_script_pack = replace(request.script_pack, product_version_id="pv-other")

    with pytest.raises(DomainValidationError, match="prepared ProductVersion"):
        export_production_pack_json(replace(request, script_pack=mismatched_script_pack))


def test_export_fails_when_selected_concept_is_not_selected() -> None:
    request = make_export_request()
    unselected = replace(request.selected_concept, selected=False)

    with pytest.raises(DomainValidationError, match="requires a selected CreativeConcept"):
        export_production_pack_json(replace(request, selected_concept=unselected))


def test_export_fails_when_evidence_refs_are_empty() -> None:
    request = make_export_request()
    without_evidence = unsafe_creative_concept(request.selected_concept, evidence_refs=())

    with pytest.raises(DomainValidationError, match="requires Evidence trace"):
        export_production_pack_json(replace(request, selected_concept=without_evidence))
