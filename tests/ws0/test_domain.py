import pytest

from tvi_workbench.ws0 import (
    ContentProject,
    DomainValidationError,
    Evidence,
    EvidenceCategory,
    OperatingContextSnapshot,
    Product,
)


def make_operating_context() -> OperatingContextSnapshot:
    return OperatingContextSnapshot(
        selection_rationale="Car owners need a compact cleaning solution for daily crumbs and dust.",
        target_market="US",
        platform="TikTok",
        content_objective="Validate whether practical in-car mess demos can drive owned content interest.",
        initial_route_hypothesis="Problem-solution demo",
        test_question="Does a real car mess cleanup hook earn enough viewer attention?",
        project_owner="Content owner",
        store_account_context="Pilot account",
    )


def test_content_project_accepts_operating_context_snapshot() -> None:
    context = make_operating_context()

    project = ContentProject(
        id="cp-car-vacuum-001",
        name="Car vacuum cleaner pilot",
        operating_context=context,
    )

    assert project.operating_context == context
    assert project.operating_context.selection_rationale.startswith("Car owners")
    assert project.operating_context.target_market == "US"


def test_product_can_own_product_version_lite() -> None:
    product = Product(id="prod-car-vacuum", name="Portable car vacuum cleaner")

    version = product.create_version(
        version_id="pv-car-vacuum-sample-a",
        label="Sample A lite version",
        notes="Initial supplier sample for WS-0 validation.",
    )

    assert version.product_id == product.id
    assert product.versions == [version]


def test_evidence_binds_to_product_version_lite() -> None:
    product = Product(id="prod-car-vacuum", name="Portable car vacuum cleaner")
    version = product.create_version(
        version_id="pv-car-vacuum-sample-a",
        label="Sample A lite version",
    )

    evidence = Evidence.bind_to_product_version(
        evidence_id="ev-supplier-claim-001",
        product_version=version,
        category=EvidenceCategory.SUPPLIER_CLAIM,
        source="Supplier product page",
        summary="Supplier claims the sample supports compact in-car cleaning.",
        collected_at="2026-07-22",
    )

    assert evidence.product_version_id == version.id
    assert evidence.summary.startswith("Supplier claims")


def test_evidence_cannot_bypass_product_version_and_bind_directly_to_product() -> None:
    product = Product(id="prod-car-vacuum", name="Portable car vacuum cleaner")
    version = product.create_version(
        version_id="pv-car-vacuum-sample-a",
        label="Sample A lite version",
    )
    evidence = Evidence.bind_to_product_version(
        evidence_id="ev-observation-001",
        product_version=version,
        category=EvidenceCategory.USER_OBSERVATION,
        source="Operator observation",
        summary="The sample is small enough to fit in the glove compartment.",
    )

    with pytest.raises(DomainValidationError, match="ProductVersion Lite"):
        product.add_evidence(evidence)

    with pytest.raises(DomainValidationError, match="ProductVersion Lite"):
        Evidence.bind_to_product(
            evidence_id="ev-invalid-001",
            product=product,
            category=EvidenceCategory.SUPPLIER_CLAIM,
            source="Supplier product page",
            summary="This invalid path tries to attach Evidence to Product.",
        )

