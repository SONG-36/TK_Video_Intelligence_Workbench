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
    KnowledgePack,
    ManualReference,
    PrepareWS1InputsRequest,
    PrepareWS1InputsResult,
    create_manual_creative_concept,
    edit_selected_creative_concept,
    generate_creative_concept_drafts,
    prepare_ws1_inputs,
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


def make_prepared_bundle(reference_count: int = 3):
    ws0 = make_ws0_result()
    references = tuple(
        make_reference(
            reference_id=f"ref-{index}",
            project_id=ws0.project.id,
            product_version_id=ws0.product_version.id,
        )
        for index in range(1, reference_count + 1)
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
    return ws0, prepared, evidence_refs


def make_concepts():
    _ws0, prepared, evidence_refs = make_prepared_bundle()
    return generate_creative_concept_drafts(
        GenerateCreativeConceptDraftsRequest(
            prepared_inputs=prepared,
            evidence_refs=evidence_refs,
        )
    )


def test_prepared_bundle_generates_exactly_three_creative_concept_drafts() -> None:
    result = make_concepts()

    assert len(result.concepts) == 3
    assert [concept.angle for concept in result.concepts] == [
        "Mess Rescue / Crumb Disaster",
        "Hidden Dirt Proof",
        "Daily Car Reset",
    ]


def test_every_concept_defaults_to_draft_and_records_generation_method() -> None:
    result = make_concepts()

    assert all(concept.status == "draft" for concept in result.concepts)
    assert all(concept.generation_method == "deterministic_mock_v0" for concept in result.concepts)


def test_every_concept_preserves_project_id_and_product_version_id() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()

    result = generate_creative_concept_drafts(
        GenerateCreativeConceptDraftsRequest(prepared_inputs=prepared, evidence_refs=evidence_refs)
    )

    assert all(concept.project_id == prepared.project_id for concept in result.concepts)
    assert all(concept.product_version_id == prepared.product_version_id for concept in result.concepts)


def test_every_concept_preserves_evidence_refs_manual_reference_refs_and_knowledge_pack_version() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle(reference_count=5)

    result = generate_creative_concept_drafts(
        GenerateCreativeConceptDraftsRequest(prepared_inputs=prepared, evidence_refs=evidence_refs)
    )

    reference_refs = tuple(reference.id for reference in prepared.manual_references)
    assert all(concept.evidence_refs == evidence_refs for concept in result.concepts)
    assert all(concept.manual_reference_refs == reference_refs for concept in result.concepts)
    assert all(concept.knowledge_pack_id == prepared.knowledge_pack.id for concept in result.concepts)
    assert all(concept.knowledge_pack_version == "v0.1" for concept in result.concepts)


def test_non_prepared_input_cannot_generate_concepts() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()
    non_prepared = PrepareWS1InputsResult(
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        knowledge_pack=prepared.knowledge_pack,
        manual_references=prepared.manual_references,
        reference_count=prepared.reference_count,
        status="draft",
    )

    with pytest.raises(DomainValidationError, match="requires prepared WS-1 inputs"):
        generate_creative_concept_drafts(
            GenerateCreativeConceptDraftsRequest(
                prepared_inputs=non_prepared,
                evidence_refs=evidence_refs,
            )
        )


def test_human_can_select_one_concept_without_approval() -> None:
    result = make_concepts()

    selected = select_creative_concept(result.concepts, concept_id=result.concepts[0].id)

    assert selected.selected is True
    assert selected.status == "draft"
    assert selected.id == result.concepts[0].id


def test_human_edit_of_selected_concept_keeps_status_draft_and_preserves_trace_refs() -> None:
    result = make_concepts()
    selected = select_creative_concept(result.concepts, concept_id=result.concepts[1].id)

    edited = edit_selected_creative_concept(
        selected,
        title="Owner edited hidden dirt proof concept",
        hook="The clean-looking car is not actually clean.",
        rationale="Lean harder into close-up proof while preserving the original trace.",
    )

    assert edited.status == "draft"
    assert edited.selected is True
    assert edited.title == "Owner edited hidden dirt proof concept"
    assert edited.project_id == selected.project_id
    assert edited.product_version_id == selected.product_version_id
    assert edited.evidence_refs == selected.evidence_refs
    assert edited.manual_reference_refs == selected.manual_reference_refs
    assert edited.knowledge_pack_id == selected.knowledge_pack_id
    assert edited.knowledge_pack_version == selected.knowledge_pack_version
    assert edited.generation_method == "human_edited_v0"


def test_invalid_concept_selection_fails() -> None:
    result = make_concepts()

    with pytest.raises(DomainValidationError, match="does not exist"):
        select_creative_concept(result.concepts, concept_id="missing-concept")


def test_editing_an_unselected_concept_fails() -> None:
    result = make_concepts()

    with pytest.raises(DomainValidationError, match="Only a selected CreativeConcept Draft"):
        edit_selected_creative_concept(
            result.concepts[0],
            title="Invalid edit before selection",
        )


def test_manual_concept_creation_succeeds_from_prepared_inputs() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()

    concept = create_manual_creative_concept(
        prepared_inputs=prepared,
        evidence_refs=evidence_refs,
        angle="Owner practical cleanup angle",
        title="Owner-created practical cleanup concept",
        hook="The car floor gets messy faster than you think.",
        rationale="Owner wants to emphasize practical daily cleanup.",
    )

    assert concept.title == "Owner-created practical cleanup concept"
    assert concept.project_id == prepared.project_id


def test_manual_concept_defaults_to_draft_and_records_manual_generation_method() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()

    concept = create_manual_creative_concept(
        prepared_inputs=prepared,
        evidence_refs=evidence_refs,
        angle="Owner daily-use angle",
        title="Owner daily-use concept",
        hook="Reset the car before tomorrow morning.",
        rationale="Owner wants a habit-building route.",
    )

    assert concept.status == "draft"
    assert concept.generation_method == "human_manual_v0"


def test_manual_concept_preserves_product_version_evidence_reference_and_knowledge_traces() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle(reference_count=5)

    concept = create_manual_creative_concept(
        prepared_inputs=prepared,
        evidence_refs=evidence_refs,
        angle="Owner proof angle",
        title="Owner proof concept",
        hook="The hidden dust is the proof.",
        rationale="Owner wants to preserve traceability while changing the angle.",
    )

    assert concept.product_version_id == prepared.product_version_id
    assert concept.evidence_refs == evidence_refs
    assert concept.manual_reference_refs == tuple(reference.id for reference in prepared.manual_references)
    assert concept.knowledge_pack_id == prepared.knowledge_pack.id
    assert concept.knowledge_pack_version == "v0.1"


def test_manual_concept_creation_fails_for_non_prepared_inputs() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()
    non_prepared = PrepareWS1InputsResult(
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        knowledge_pack=prepared.knowledge_pack,
        manual_references=prepared.manual_references,
        reference_count=prepared.reference_count,
        status="draft",
    )

    with pytest.raises(DomainValidationError, match="requires prepared WS-1 inputs"):
        create_manual_creative_concept(
            prepared_inputs=non_prepared,
            evidence_refs=evidence_refs,
            angle="Owner angle",
            title="Owner concept",
            hook="Owner hook",
            rationale="Owner rationale",
        )


def test_manual_concept_creation_fails_when_evidence_refs_are_empty() -> None:
    _ws0, prepared, _evidence_refs = make_prepared_bundle()

    with pytest.raises(DomainValidationError, match="requires Evidence trace"):
        create_manual_creative_concept(
            prepared_inputs=prepared,
            evidence_refs=(),
            angle="Owner angle",
            title="Owner concept",
            hook="Owner hook",
            rationale="Owner rationale",
        )


@pytest.mark.parametrize(
    ("field", "kwargs"),
    [
        ("angle", {"angle": ""}),
        ("title", {"title": ""}),
        ("hook", {"hook": ""}),
        ("rationale", {"rationale": ""}),
    ],
)
def test_manual_concept_creation_fails_when_owner_facing_fields_are_empty(
    field: str,
    kwargs: dict[str, str],
) -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()
    values = {
        "angle": "Owner angle",
        "title": "Owner concept",
        "hook": "Owner hook",
        "rationale": "Owner rationale",
    }
    values.update(kwargs)

    with pytest.raises(DomainValidationError, match=f"{field} is required"):
        create_manual_creative_concept(
            prepared_inputs=prepared,
            evidence_refs=evidence_refs,
            **values,
        )


def test_manual_concept_id_does_not_collide_for_different_chinese_angles() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()

    first = create_manual_creative_concept(
        prepared_inputs=prepared,
        evidence_refs=evidence_refs,
        angle="车内饼干碎救援",
        title="车载吸尘器清理饼干碎",
        hook="孩子吃完零食后，座椅缝全是碎屑。",
        rationale="Owner wants a Chinese angle that would previously collapse in slugify.",
    )
    second = create_manual_creative_concept(
        prepared_inputs=prepared,
        evidence_refs=evidence_refs,
        angle="隐藏灰尘证明",
        title="车内隐藏灰尘特写",
        hook="看起来干净的车，其实缝隙里全是灰。",
        rationale="Owner wants another Chinese angle with distinct traceable id.",
    )

    assert first.id != second.id
    assert first.id.startswith("concept-manual-")
    assert second.id.startswith("concept-manual-")


def test_generation_fails_when_reference_count_does_not_match_actual_references() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()
    inconsistent = PrepareWS1InputsResult(
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        knowledge_pack=prepared.knowledge_pack,
        manual_references=prepared.manual_references,
        reference_count=4,
    )

    with pytest.raises(DomainValidationError, match="reference_count must match"):
        generate_creative_concept_drafts(
            GenerateCreativeConceptDraftsRequest(
                prepared_inputs=inconsistent,
                evidence_refs=evidence_refs,
            )
        )


def test_manual_creation_fails_when_reference_count_does_not_match_actual_references() -> None:
    _ws0, prepared, evidence_refs = make_prepared_bundle()
    inconsistent = PrepareWS1InputsResult(
        project_id=prepared.project_id,
        product_version_id=prepared.product_version_id,
        knowledge_pack=prepared.knowledge_pack,
        manual_references=prepared.manual_references,
        reference_count=4,
    )

    with pytest.raises(DomainValidationError, match="reference_count must match"):
        create_manual_creative_concept(
            prepared_inputs=inconsistent,
            evidence_refs=evidence_refs,
            angle="Owner angle",
            title="Owner concept",
            hook="Owner hook",
            rationale="Owner rationale",
        )


def test_selecting_duplicate_concept_ids_fails() -> None:
    result = make_concepts()
    duplicate_concepts = (result.concepts[0], result.concepts[0], result.concepts[1])

    with pytest.raises(DomainValidationError, match="id is ambiguous"):
        select_creative_concept(duplicate_concepts, concept_id=result.concepts[0].id)


def test_editing_angle_preserves_trace_refs_and_status() -> None:
    result = make_concepts()
    selected = select_creative_concept(result.concepts, concept_id=result.concepts[2].id)

    edited = edit_selected_creative_concept(
        selected,
        angle="Owner edited daily reset angle",
    )

    assert edited.status == "draft"
    assert edited.angle == "Owner edited daily reset angle"
    assert edited.project_id == selected.project_id
    assert edited.product_version_id == selected.product_version_id
    assert edited.evidence_refs == selected.evidence_refs
    assert edited.manual_reference_refs == selected.manual_reference_refs
    assert edited.knowledge_pack_id == selected.knowledge_pack_id
    assert edited.knowledge_pack_version == selected.knowledge_pack_version
