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
    KnowledgePack,
    ManualReference,
    PrepareWS1InputsRequest,
    prepare_ws1_inputs,
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
            ),
        )
    )


def make_knowledge_pack(version: str = "v0.1") -> KnowledgePack:
    return KnowledgePack(
        id="kp-car-vacuum-v01",
        version=version,
        title="Car vacuum cleaner content knowledge pack v0.1",
        content_summary="Rules and patterns for practical car cleaning demos.",
        sections={
            "script_rules": "Use observable claims and avoid unsupported performance guarantees.",
            "hook_guidance": "Open with visible in-car mess before product reveal.",
            "claims_guardrails": "Tie claims back to Evidence Lite.",
        },
        source_notes="Initial manually curated v0.1 pack.",
        created_at="2026-07-22",
    )


def make_reference(
    reference_id: str,
    project_id: str,
    product_version_id: str,
    *,
    intake_method: str = "manual",
) -> ManualReference:
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
        intake_method=intake_method,
    )


def make_references(count: int, project_id: str, product_version_id: str) -> tuple[ManualReference, ...]:
    return tuple(
        make_reference(
            reference_id=f"ref-{index}",
            project_id=project_id,
            product_version_id=product_version_id,
        )
        for index in range(1, count + 1)
    )


def make_request(reference_count: int = 3) -> PrepareWS1InputsRequest:
    ws0 = make_ws0_result()
    return PrepareWS1InputsRequest(
        project_id=ws0.project.id,
        product_version_id=ws0.product_version.id,
        knowledge_pack=make_knowledge_pack(),
        manual_references=make_references(reference_count, ws0.project.id, ws0.product_version.id),
    )


def test_prepares_ws1_input_bundle_with_knowledge_pack_and_three_manual_references() -> None:
    result = prepare_ws1_inputs(make_request(reference_count=3))

    assert result.status == "prepared"
    assert result.reference_count == 3
    assert result.knowledge_pack.version == "v0.1"
    assert len(result.manual_references) == 3


def test_result_preserves_project_id_product_version_id_and_knowledge_pack_version() -> None:
    request = make_request(reference_count=3)

    result = prepare_ws1_inputs(request)

    assert result.project_id == request.project_id
    assert result.product_version_id == request.product_version_id
    assert result.knowledge_pack.id == "kp-car-vacuum-v01"
    assert result.knowledge_pack.version == "v0.1"


def test_manual_references_bind_to_project_id_and_product_version_id() -> None:
    request = make_request(reference_count=5)

    result = prepare_ws1_inputs(request)

    assert result.reference_count == 5
    assert all(reference.project_id == result.project_id for reference in result.manual_references)
    assert all(
        reference.product_version_id == result.product_version_id
        for reference in result.manual_references
    )
    assert all(reference.intake_method == "manual" for reference in result.manual_references)


def test_fails_with_fewer_than_three_manual_references() -> None:
    with pytest.raises(DomainValidationError, match="at least 3 manual References"):
        prepare_ws1_inputs(make_request(reference_count=2))


def test_fails_with_more_than_five_manual_references() -> None:
    with pytest.raises(DomainValidationError, match="at most 5 manual References"):
        prepare_ws1_inputs(make_request(reference_count=6))


def test_fails_when_reference_project_id_does_not_match_request() -> None:
    request = make_request(reference_count=3)
    mismatched_reference = make_reference(
        reference_id="ref-mismatch-project",
        project_id="different-project",
        product_version_id=request.product_version_id,
    )
    invalid_request = PrepareWS1InputsRequest(
        project_id=request.project_id,
        product_version_id=request.product_version_id,
        knowledge_pack=request.knowledge_pack,
        manual_references=(mismatched_reference, *request.manual_references[:2]),
    )

    with pytest.raises(DomainValidationError, match="Manual Reference must bind to the ContentProject"):
        prepare_ws1_inputs(invalid_request)


def test_fails_when_reference_product_version_id_does_not_match_request() -> None:
    request = make_request(reference_count=3)
    mismatched_reference = make_reference(
        reference_id="ref-mismatch-product-version",
        project_id=request.project_id,
        product_version_id="different-product-version",
    )
    invalid_request = PrepareWS1InputsRequest(
        project_id=request.project_id,
        product_version_id=request.product_version_id,
        knowledge_pack=request.knowledge_pack,
        manual_references=(mismatched_reference, *request.manual_references[:2]),
    )

    with pytest.raises(DomainValidationError, match="Manual Reference must bind to the ProductVersion"):
        prepare_ws1_inputs(invalid_request)


def test_fails_with_non_manual_reference_intake() -> None:
    ws0 = make_ws0_result()

    with pytest.raises(DomainValidationError, match="intake_method must be manual"):
        ManualReference(
            id="ref-auto-001",
            project_id=ws0.project.id,
            product_version_id=ws0.product_version.id,
            title="Automatically searched reference",
            source_identifier="https://example.com/auto",
            source_type="TikTok search",
            summary="This should not enter Step 2.",
            observed_pattern="Automated search result.",
            intake_method="automatic",
        )


def test_fails_when_knowledge_pack_version_is_missing() -> None:
    with pytest.raises(DomainValidationError, match="version is required"):
        make_knowledge_pack(version="")


def test_fails_when_knowledge_pack_version_is_not_v01() -> None:
    with pytest.raises(DomainValidationError, match="version must be v0.1"):
        make_knowledge_pack(version="v0.2")
