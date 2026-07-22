import pytest

from tvi_workbench.ws0 import (
    CreateWS0ProjectRequest,
    DomainValidationError,
    Evidence,
    EvidenceCategory,
    EvidenceInput,
    OperatingContextInput,
    ProductInput,
    ProductVersionInput,
    ProjectInput,
    create_project_from_handoff,
)


def make_request() -> CreateWS0ProjectRequest:
    return CreateWS0ProjectRequest(
        project=ProjectInput(
            id="cp-car-vacuum-001",
            name="Car vacuum cleaner pilot",
        ),
        operating_context=OperatingContextInput(
            selection_rationale="Car owners need a compact cleaning solution for daily crumbs and dust.",
            target_market="US",
            platform="TikTok",
            content_objective="Validate whether practical in-car mess demos can drive owned content interest.",
            initial_route_hypothesis="Problem-solution demo",
            test_question="Does a real car mess cleanup hook earn enough viewer attention?",
            project_owner="Content owner",
            store_account_context="Pilot account",
        ),
        product=ProductInput(
            id="prod-car-vacuum",
            name="Portable car vacuum cleaner",
        ),
        product_version=ProductVersionInput(
            id="pv-car-vacuum-sample-a",
            label="Sample A lite version",
            notes="Initial supplier sample for WS-0 validation.",
        ),
        evidence=(
            EvidenceInput(
                id="ev-supplier-claim-001",
                category=EvidenceCategory.SUPPLIER_CLAIM,
                source="Supplier product page",
                summary="Supplier claims the sample supports compact in-car cleaning.",
                collected_at="2026-07-22",
            ),
            EvidenceInput(
                id="ev-observation-001",
                category=EvidenceCategory.USER_OBSERVATION,
                source="Operator observation",
                summary="The sample is small enough to fit in the glove compartment.",
            ),
        ),
    )


def test_service_creates_complete_ws0_chain_from_structured_input() -> None:
    result = create_project_from_handoff(make_request())

    assert result.project.name == "Car vacuum cleaner pilot"
    assert result.operating_context.target_market == "US"
    assert result.product.name == "Portable car vacuum cleaner"
    assert result.product_version.label == "Sample A lite version"
    assert len(result.evidence) == 2


def test_service_result_preserves_traceable_ids_and_product_version_binding() -> None:
    result = create_project_from_handoff(make_request())

    assert result.project.id == "cp-car-vacuum-001"
    assert result.product.id == "prod-car-vacuum"
    assert result.product_version.id == "pv-car-vacuum-sample-a"
    assert result.project.product_version_id == result.product_version.id
    assert result.evidence[0].id == "ev-supplier-claim-001"
    assert result.evidence[0].product_version_id == result.product_version.id
    assert result.evidence[1].product_version_id == result.product_version.id


def test_service_fails_when_required_handoff_field_is_missing() -> None:
    request = make_request()
    invalid_request = CreateWS0ProjectRequest(
        project=request.project,
        operating_context=OperatingContextInput(
            selection_rationale="",
            target_market=request.operating_context.target_market,
            platform=request.operating_context.platform,
            content_objective=request.operating_context.content_objective,
            initial_route_hypothesis=request.operating_context.initial_route_hypothesis,
            test_question=request.operating_context.test_question,
            project_owner=request.operating_context.project_owner,
            store_account_context=request.operating_context.store_account_context,
        ),
        product=request.product,
        product_version=request.product_version,
        evidence=request.evidence,
    )

    with pytest.raises(DomainValidationError, match="selection_rationale is required"):
        create_project_from_handoff(invalid_request)


def test_service_fails_when_required_product_version_field_is_missing() -> None:
    request = make_request()
    invalid_request = CreateWS0ProjectRequest(
        project=request.project,
        operating_context=request.operating_context,
        product=request.product,
        product_version=ProductVersionInput(
            id=request.product_version.id,
            label="",
            notes=request.product_version.notes,
        ),
        evidence=request.evidence,
    )

    with pytest.raises(DomainValidationError, match="label is required"):
        create_project_from_handoff(invalid_request)


def test_service_fails_when_evidence_lite_is_empty() -> None:
    request = make_request()
    invalid_request = CreateWS0ProjectRequest(
        project=request.project,
        operating_context=request.operating_context,
        product=request.product,
        product_version=request.product_version,
        evidence=(),
    )

    with pytest.raises(
        DomainValidationError,
        match="WS-0 project requires at least one Evidence Lite item",
    ):
        create_project_from_handoff(invalid_request)


def test_direct_product_evidence_binding_rule_remains_protected() -> None:
    result = create_project_from_handoff(make_request())

    with pytest.raises(DomainValidationError, match="ProductVersion Lite"):
        result.product.add_evidence(result.evidence[0])

    with pytest.raises(DomainValidationError, match="ProductVersion Lite"):
        Evidence.bind_to_product(
            evidence_id="ev-invalid-001",
            product=result.product,
            category=EvidenceCategory.SUPPLIER_CLAIM,
            source="Supplier product page",
            summary="This invalid path tries to attach Evidence to Product.",
        )
