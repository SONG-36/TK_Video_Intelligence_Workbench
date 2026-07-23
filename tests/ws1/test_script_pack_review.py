from dataclasses import replace

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
    GenerateCreativeConceptDraftsRequest,
    GenerateScriptPackDraftRequest,
    KnowledgePack,
    ManualReference,
    PrepareWS1InputsRequest,
    PrepareWS1InputsResult,
    create_manual_creative_concept,
    edit_selected_creative_concept,
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


def make_unsafe_manual_reference(
    *,
    reference_id: str,
    project_id: str,
    product_version_id: str,
    intake_method: str,
) -> ManualReference:
    reference = object.__new__(ManualReference)
    object.__setattr__(reference, "id", reference_id)
    object.__setattr__(reference, "project_id", project_id)
    object.__setattr__(reference, "product_version_id", product_version_id)
    object.__setattr__(reference, "title", f"Unsafe reference {reference_id}")
    object.__setattr__(reference, "source_identifier", f"https://example.com/{reference_id}")
    object.__setattr__(reference, "source_type", "Unsafe fixture")
    object.__setattr__(reference, "summary", "Unsafe fixture bypassing ManualReference validation.")
    object.__setattr__(reference, "observed_pattern", "Unsafe observed pattern.")
    object.__setattr__(reference, "content_notes", None)
    object.__setattr__(reference, "usage_notes", None)
    object.__setattr__(reference, "intake_method", intake_method)
    return reference


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


def make_selected_concept():
    prepared, evidence_refs = make_prepared_bundle()
    concepts = generate_creative_concept_drafts(
        GenerateCreativeConceptDraftsRequest(
            prepared_inputs=prepared,
            evidence_refs=evidence_refs,
        )
    )
    selected = select_creative_concept(concepts.concepts, concept_id=concepts.concepts[0].id)
    return prepared, evidence_refs, selected


def make_script_pack():
    prepared, _evidence_refs, selected = make_selected_concept()
    return prepared, selected, generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared,
            concept=selected,
        )
    )


def test_selected_concept_can_generate_script_pack_draft() -> None:
    prepared, selected, script_pack = make_script_pack()

    assert script_pack.project_id == prepared.project_id
    assert script_pack.concept_id == selected.id
    assert script_pack.voiceover_script
    assert script_pack.storyboard
    assert script_pack.shot_list


def test_edited_concept_can_generate_script_pack_draft() -> None:
    prepared, _evidence_refs, selected = make_selected_concept()
    edited = edit_selected_creative_concept(
        selected,
        title="Owner edited crumb rescue concept",
        hook="The snack mess is worse than it looks.",
    )

    script_pack = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared,
            concept=edited,
        )
    )

    assert script_pack.concept_id == edited.id
    assert script_pack.status == "draft"


def test_unselected_concept_cannot_generate_script_pack_draft() -> None:
    prepared, evidence_refs = make_prepared_bundle()
    concepts = generate_creative_concept_drafts(
        GenerateCreativeConceptDraftsRequest(
            prepared_inputs=prepared,
            evidence_refs=evidence_refs,
        )
    )

    with pytest.raises(DomainValidationError, match="requires a selected CreativeConcept"):
        generate_script_pack_draft(
            GenerateScriptPackDraftRequest(
                prepared_inputs=prepared,
                concept=concepts.concepts[0],
            )
        )


def test_script_pack_draft_defaults_to_draft_and_records_generation_method() -> None:
    _prepared, _selected, script_pack = make_script_pack()

    assert script_pack.status == "draft"
    assert script_pack.generation_method == "deterministic_mock_v0"


def test_script_pack_draft_preserves_project_product_and_concept_trace() -> None:
    prepared, selected, script_pack = make_script_pack()

    assert script_pack.project_id == prepared.project_id
    assert script_pack.product_version_id == prepared.product_version_id
    assert script_pack.concept_id == selected.id


def test_script_pack_draft_preserves_evidence_reference_and_knowledge_trace() -> None:
    prepared, selected, script_pack = make_script_pack()

    assert script_pack.evidence_refs == selected.evidence_refs
    assert script_pack.manual_reference_refs == tuple(reference.id for reference in prepared.manual_references)
    assert script_pack.manual_reference_refs == selected.manual_reference_refs
    assert script_pack.knowledge_pack_id == prepared.knowledge_pack.id
    assert script_pack.knowledge_pack_version == prepared.knowledge_pack.version


@pytest.mark.parametrize("decision", ["approved", "rework", "hold", "stopped"])
def test_review_script_pack_accepts_canonical_decisions(decision: str) -> None:
    _prepared, _selected, script_pack = make_script_pack()

    review = review_script_pack(
        script_pack,
        decision=decision,
        reviewer_note="Owner review note",
    )

    assert review.project_id == script_pack.project_id
    assert review.script_pack_id == script_pack.id
    assert review.decision == decision
    assert review.reviewer_note == "Owner review note"


def test_review_script_pack_rejects_draft_as_review_decision() -> None:
    _prepared, _selected, script_pack = make_script_pack()

    with pytest.raises(DomainValidationError, match="approved, rework, hold, or stopped"):
        review_script_pack(
            script_pack,
            decision="draft",
            reviewer_note="Draft is not a review decision.",
        )


def test_review_does_not_silently_mutate_script_pack_draft() -> None:
    _prepared, _selected, script_pack = make_script_pack()
    before = script_pack

    review = review_script_pack(
        script_pack,
        decision="approved",
        reviewer_note="Approved for this pilot.",
    )

    assert script_pack == before
    assert script_pack.status == "draft"
    assert review.decision == "approved"


def test_mismatched_prepared_input_and_concept_fails() -> None:
    prepared, _evidence_refs, selected = make_selected_concept()
    mismatched = replace(selected, product_version_id="pv-other-sample")

    with pytest.raises(DomainValidationError, match="prepared ProductVersion"):
        generate_script_pack_draft(
            GenerateScriptPackDraftRequest(
                prepared_inputs=prepared,
                concept=mismatched,
            )
        )


def test_manual_selected_concept_can_generate_script_pack_draft() -> None:
    prepared, evidence_refs = make_prepared_bundle()
    manual = create_manual_creative_concept(
        prepared_inputs=prepared,
        evidence_refs=evidence_refs,
        angle="Owner manual reset angle",
        title="Owner manual reset concept",
        hook="The car needs a reset before Monday.",
        rationale="Owner prefers a weekly reset story.",
    )
    selected = select_creative_concept((manual,), concept_id=manual.id)

    script_pack = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared,
            concept=selected,
        )
    )

    assert script_pack.concept_id == selected.id
    assert script_pack.status == "draft"


def test_concept_generation_fails_if_prepared_reference_belongs_to_another_project() -> None:
    prepared, evidence_refs = make_prepared_bundle()
    bad_reference = make_reference(
        reference_id="ref-other-project",
        project_id="cp-other",
        product_version_id=prepared.product_version_id,
    )
    inconsistent = PrepareWS1InputsResult(
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        knowledge_pack=prepared.knowledge_pack,
        manual_references=(bad_reference, *prepared.manual_references[1:]),
        reference_count=prepared.reference_count,
    )

    with pytest.raises(DomainValidationError, match="Manual Reference must bind to the ContentProject"):
        generate_creative_concept_drafts(
            GenerateCreativeConceptDraftsRequest(
                prepared_inputs=inconsistent,
                evidence_refs=evidence_refs,
            )
        )


def test_concept_generation_fails_if_prepared_reference_belongs_to_another_product_version() -> None:
    prepared, evidence_refs = make_prepared_bundle()
    bad_reference = make_reference(
        reference_id="ref-other-product-version",
        project_id=prepared.project_id,
        product_version_id="pv-other",
    )
    inconsistent = PrepareWS1InputsResult(
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        knowledge_pack=prepared.knowledge_pack,
        manual_references=(bad_reference, *prepared.manual_references[1:]),
        reference_count=prepared.reference_count,
    )

    with pytest.raises(DomainValidationError, match="Manual Reference must bind to the ProductVersion"):
        generate_creative_concept_drafts(
            GenerateCreativeConceptDraftsRequest(
                prepared_inputs=inconsistent,
                evidence_refs=evidence_refs,
            )
        )


def test_concept_generation_fails_if_prepared_reference_is_not_manual_intake() -> None:
    prepared, evidence_refs = make_prepared_bundle()
    bad_reference = make_unsafe_manual_reference(
        reference_id="ref-search-intake",
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        intake_method="search",
    )
    inconsistent = PrepareWS1InputsResult(
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        knowledge_pack=prepared.knowledge_pack,
        manual_references=(bad_reference, *prepared.manual_references[1:]),
        reference_count=prepared.reference_count,
    )

    with pytest.raises(DomainValidationError, match="intake_method must be manual"):
        generate_creative_concept_drafts(
            GenerateCreativeConceptDraftsRequest(
                prepared_inputs=inconsistent,
                evidence_refs=evidence_refs,
            )
        )


def test_concept_generation_fails_if_prepared_knowledge_pack_is_not_a_knowledge_pack() -> None:
    prepared, evidence_refs = make_prepared_bundle()
    inconsistent = PrepareWS1InputsResult(
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        knowledge_pack=object(),
        manual_references=prepared.manual_references,
        reference_count=prepared.reference_count,
    )

    with pytest.raises(DomainValidationError, match="knowledge_pack must be a KnowledgePack"):
        generate_creative_concept_drafts(
            GenerateCreativeConceptDraftsRequest(
                prepared_inputs=inconsistent,
                evidence_refs=evidence_refs,
            )
        )


def test_edit_selected_creative_concept_fails_when_no_owner_facing_fields_are_provided() -> None:
    _prepared, _evidence_refs, selected = make_selected_concept()

    with pytest.raises(DomainValidationError, match="requires at least one owner-facing field"):
        edit_selected_creative_concept(selected)


def test_script_pack_id_changes_when_selected_concept_owner_facing_content_changes() -> None:
    prepared, _evidence_refs, selected = make_selected_concept()
    first = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared,
            concept=selected,
        )
    )
    edited = edit_selected_creative_concept(
        selected,
        title="Owner changed title for ScriptPack identity",
    )

    second = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared,
            concept=edited,
        )
    )

    assert first.id != second.id
    assert first.concept_id == second.concept_id


def test_script_pack_id_remains_stable_for_same_selected_concept_content() -> None:
    prepared, _evidence_refs, selected = make_selected_concept()

    first = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared,
            concept=selected,
        )
    )
    second = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared,
            concept=selected,
        )
    )

    assert first.id == second.id
