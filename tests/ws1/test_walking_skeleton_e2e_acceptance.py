from tvi_workbench.ws0 import (
    CreateWS0ProjectRequest,
    EvidenceCategory,
    EvidenceInput,
    OperatingContextInput,
    ProductInput,
    ProductVersionInput,
    ProjectInput,
    create_project_from_handoff,
)
from tvi_workbench.ws1 import (
    ExportBusinessContext,
    ExportProductionPackRequest,
    GenerateCreativeConceptDraftsRequest,
    GenerateScriptPackDraftRequest,
    KnowledgePack,
    ManualReference,
    PrepareWS1InputsRequest,
    edit_selected_creative_concept,
    export_production_pack_json,
    export_production_pack_markdown,
    generate_creative_concept_drafts,
    generate_script_pack_draft,
    prepare_ws1_inputs,
    review_script_pack,
    select_creative_concept,
)


def test_ws0_to_ws1_car_vacuum_walking_skeleton_exports_production_pack() -> None:
    ws0 = create_project_from_handoff(
        CreateWS0ProjectRequest(
            project=ProjectInput(id="cp-car-vacuum-001", name="Car vacuum cleaner pilot"),
            operating_context=OperatingContextInput(
                selection_rationale="Car owners need a compact, visible cleanup solution.",
                target_market="US car owners",
                platform="TikTok",
                content_objective="Validate a practical mess-first car cleaning concept.",
                test_question="Can visible crumb cleanup support a generation-ready content pack?",
                project_owner="Content owner",
                initial_route_hypothesis="Mess-first practical demo",
            ),
            product=ProductInput(id="prod-car-vacuum", name="Portable car vacuum cleaner"),
            product_version=ProductVersionInput(
                id="pv-car-vacuum-sample-a",
                label="Sample A lite version",
                notes="Compact car vacuum sample for WS-0 + WS-1 pilot.",
            ),
            evidence=(
                EvidenceInput(
                    id="ev-supplier-claim-001",
                    category=EvidenceCategory.SUPPLIER_CLAIM,
                    source="Supplier product page",
                    summary="Supplier claims compact in-car cleaning support.",
                ),
                EvidenceInput(
                    id="ev-owner-observation-001",
                    category=EvidenceCategory.USER_OBSERVATION,
                    source="Owner sample observation",
                    summary="The sample fits in a glove compartment and reaches seat seams.",
                ),
            ),
        )
    )

    assert ws0.project.product_version_id == ws0.product_version.id
    assert all(evidence.product_version_id == ws0.product_version.id for evidence in ws0.evidence)

    prepared_inputs = prepare_ws1_inputs(
        PrepareWS1InputsRequest(
            project_id=ws0.project.id,
            product_version_id=ws0.product_version.id,
            knowledge_pack=KnowledgePack(
                id="kp-car-vacuum-v01",
                version="v0.1",
                title="Car vacuum cleaner content knowledge pack v0.1",
                content_summary="Use observable claims and tie cleanup proof back to Evidence Lite.",
                sections={
                    "hook_guidance": "Open with visible in-car mess before product reveal.",
                    "claims_guardrails": "Avoid unsupported suction or battery claims.",
                },
            ),
            manual_references=(
                make_manual_reference("ref-crumb-demo", ws0.project.id, ws0.product_version.id),
                make_manual_reference("ref-hidden-dust", ws0.project.id, ws0.product_version.id),
                make_manual_reference("ref-daily-reset", ws0.project.id, ws0.product_version.id),
            ),
        )
    )

    assert prepared_inputs.status == "prepared"
    assert 3 <= prepared_inputs.reference_count <= 5

    evidence_refs = tuple(evidence.id for evidence in ws0.evidence)
    concept_result = generate_creative_concept_drafts(
        GenerateCreativeConceptDraftsRequest(
            prepared_inputs=prepared_inputs,
            evidence_refs=evidence_refs,
        )
    )

    assert len(concept_result.concepts) == 3

    selected = select_creative_concept(
        concept_result.concepts,
        concept_id=concept_result.concepts[0].id,
    )
    edited = edit_selected_creative_concept(
        selected,
        title="Owner edited crumb rescue concept",
        hook="The snack mess under the seat is the proof.",
    )

    assert edited.status == "draft"

    script_pack = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared_inputs,
            concept=edited,
        )
    )

    assert script_pack.status == "draft"

    review = review_script_pack(
        script_pack,
        decision="approved",
        reviewer_note="Approved for generation-ready production handoff.",
    )

    assert review.decision == "approved"

    export_request = ExportProductionPackRequest(
        business_context=ExportBusinessContext(
            product_context_summary=(
                "Portable car vacuum cleaner Sample A for a practical in-car cleanup pilot."
            ),
            handoff_summary=(
                "Selection-to-content handoff focuses on proving visible crumb cleanup in a TikTok demo."
            ),
            target_market=ws0.operating_context.target_market,
            platform=ws0.operating_context.platform,
            content_objective=ws0.operating_context.content_objective,
            product_name=ws0.product.name,
            product_version_label=ws0.product_version.label,
        ),
        prepared_inputs=prepared_inputs,
        concept_drafts=concept_result.concepts,
        selected_concept=edited,
        script_pack=script_pack,
        review=review,
    )

    markdown = export_production_pack_markdown(export_request)
    data = export_production_pack_json(export_request)

    assert "## Product Context" in markdown
    assert "Portable car vacuum cleaner Sample A" in markdown
    assert "## Selection-to-Content Handoff Summary" in markdown
    assert "visible crumb cleanup" in markdown
    assert ws0.product_version.id in markdown
    assert all(evidence_ref in markdown for evidence_ref in evidence_refs)
    assert all(reference.id in markdown for reference in prepared_inputs.manual_references)
    assert prepared_inputs.knowledge_pack.version in markdown
    assert all(concept.id in markdown for concept in concept_result.concepts)
    assert edited.title in markdown
    assert "## Script" in markdown
    assert script_pack.voiceover_script in markdown
    assert "## Storyboard" in markdown
    assert "## Shot List" in markdown
    assert "## Human Review" in markdown
    assert review.reviewer_note in markdown

    assert data["project_id"] == ws0.project.id
    assert data["product_version_id"] == ws0.product_version.id
    assert data["evidence_refs"] == list(evidence_refs)
    assert data["manual_reference_refs"] == [reference.id for reference in prepared_inputs.manual_references]
    assert data["knowledge_pack"]["id"] == prepared_inputs.knowledge_pack.id
    assert data["knowledge_pack"]["version"] == "v0.1"
    assert data["selected_concept_id"] == edited.id
    assert data["script_pack_id"] == script_pack.id
    assert data["review"]["decision"] == "approved"
    assert data["production_readiness"] == "generation_ready"


def make_manual_reference(reference_id: str, project_id: str, product_version_id: str) -> ManualReference:
    return ManualReference(
        id=reference_id,
        project_id=project_id,
        product_version_id=product_version_id,
        title=f"Manual car vacuum reference {reference_id}",
        source_identifier=f"https://example.com/{reference_id}",
        source_type="TikTok manual URL",
        summary="Manual reference showing a car cleaning content pattern.",
        observed_pattern="Mess-first hook followed by compact product cleanup.",
        usage_notes="Use for pacing and proof-shot inspiration.",
    )
