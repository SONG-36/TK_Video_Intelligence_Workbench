"""Visual smoke harness for WS-0 -> WS-1 input preparation.

This Streamlit app is a local owner-review tool. It is not the product
frontend, not an API, and not a persistence layer.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from tvi_workbench.ws0 import (  # noqa: E402
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
from tvi_workbench.ws1 import (  # noqa: E402
    KnowledgePack,
    ManualReference,
    PrepareWS1InputsRequest,
    prepare_ws1_inputs,
)


def slugify(value: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def as_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return as_jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): as_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [as_jsonable(item) for item in value]
    if isinstance(value, EvidenceCategory):
        return value.value
    return value


def build_preview(ws0_result: Any, ws1_result: Any) -> dict[str, Any]:
    return {
        "purpose": "Dev preview for owner smoke testing. This is not a formal Markdown/JSON export.",
        "status_constraints": {
            "ws1_status": ws1_result.status,
            "status_can_only_be": "prepared",
            "has_ai_output": False,
            "has_concept": False,
            "has_script_pack": False,
            "has_export": False,
        },
        "traceability": {
            "project_id": ws0_result.project.id,
            "product_version_id": ws0_result.product_version.id,
            "evidence_count": len(ws0_result.evidence),
            "evidence_product_version_ids": [
                evidence.product_version_id for evidence in ws0_result.evidence
            ],
            "knowledge_pack_version": ws1_result.knowledge_pack.version,
            "reference_count": ws1_result.reference_count,
            "reference_bindings": [
                {
                    "reference_id": reference.id,
                    "project_id": reference.project_id,
                    "product_version_id": reference.product_version_id,
                    "intake_method": reference.intake_method,
                }
                for reference in ws1_result.manual_references
            ],
        },
        "ws0": {
            "project": as_jsonable(ws0_result.project),
            "operating_context": as_jsonable(ws0_result.operating_context),
            "product": as_jsonable(ws0_result.product),
            "product_version": as_jsonable(ws0_result.product_version),
            "evidence": as_jsonable(ws0_result.evidence),
        },
        "ws1_inputs": {
            "knowledge_pack": as_jsonable(ws1_result.knowledge_pack),
            "manual_references": as_jsonable(ws1_result.manual_references),
        },
    }


def collect_evidence(index: int, *, expanded: bool) -> dict[str, str | None]:
    with st.expander(f"Evidence Lite {index}", expanded=expanded):
        st.caption("Smoke harness requires at least one Evidence Lite item.")
        category = st.selectbox(
            "What kind of evidence is this?",
            [item.value for item in EvidenceCategory],
            index=1 if index == 1 else 2,
            key=f"evidence_category_{index}",
        )
        source = st.text_input(
            "Source",
            "Supplier product page" if index == 1 else "Owner observation",
            key=f"evidence_source_{index}",
        )
        summary = st.text_area(
            "Evidence summary",
            "Supplier claims the sample supports compact in-car cleaning."
            if index == 1
            else "Owner observed that the sample fits in a glove compartment and is easy to handle.",
            key=f"evidence_summary_{index}",
        )
        collected_at = st.text_input(
            "Collected at (optional)",
            "2026-07-22" if index == 1 else "",
            key=f"evidence_collected_at_{index}",
        )
    return {
        "id": f"ev-car-vacuum-{index:03d}",
        "category": category,
        "source": source,
        "summary": summary,
        "collected_at": collected_at or None,
    }


def collect_reference(index: int, *, expanded: bool, optional: bool) -> dict[str, str | None] | None:
    label = f"Reference {index}"
    with st.expander(label if not optional else f"Optional {label}", expanded=expanded):
        if optional:
            include = st.checkbox(f"Include Reference {index}", value=False, key=f"include_reference_{index}")
            if not include:
                st.caption("Leave unchecked to keep the bundle at the required minimum of 3 references.")
                return None
        title = st.text_input(
            "Reference title",
            f"Car cleanup demo reference {index}",
            key=f"reference_title_{index}",
        )
        source_identifier = st.text_input(
            "Reference video/source",
            f"https://example.com/car-vacuum-reference-{index}",
            key=f"reference_source_{index}",
        )
        source_type = st.text_input(
            "Platform / source type",
            "TikTok manual URL",
            key=f"reference_source_type_{index}",
        )
        summary = st.text_area(
            "What is useful in this reference?",
            "A manually entered reference showing a mess-first cleanup demo pattern.",
            key=f"reference_summary_{index}",
        )
        observed_pattern = st.text_area(
            "Observed content pattern",
            "Mess-first hook followed by compact product demo.",
            key=f"reference_observed_pattern_{index}",
        )
        content_notes = st.text_area(
            "Content notes",
            "Useful for pacing, opening shot, and visual setup.",
            key=f"reference_content_notes_{index}",
        )
        usage_notes = st.text_area(
            "Usage notes",
            "Use only as a hook and scene rhythm reference.",
            key=f"reference_usage_notes_{index}",
        )
    return {
        "id": f"ref-car-vacuum-{index:03d}",
        "title": title,
        "source_identifier": source_identifier,
        "source_type": source_type,
        "summary": summary,
        "observed_pattern": observed_pattern or None,
        "content_notes": content_notes or None,
        "usage_notes": usage_notes or None,
    }


st.set_page_config(page_title="WS Pilot Input Harness", layout="wide")
st.title("Car Vacuum Cleaner Input Smoke Harness")
st.caption("Local visual smoke tool only. Not product UI, API, database, AI, or export.")

with st.form("pilot_input_form"):
    project_tab, product_tab, evidence_tab, knowledge_tab, references_tab, validate_tab = st.tabs(
        [
            "Project / Handoff",
            "Product / Version",
            "Evidence Lite",
            "Knowledge Pack v0.1",
            "Manual References",
            "Validate / Trace Preview",
        ]
    )

    with project_tab:
        st.subheader("Project / Handoff")
        project_name = st.text_input("Project name", "Car vacuum cleaner pilot")
        selection_rationale = st.text_area(
            "Why are we testing this product?",
            "Car owners need a compact cleaning solution for crumbs, dust, pet hair, and small debris after daily driving.",
        )
        col1, col2 = st.columns(2)
        with col1:
            target_market = st.text_input("Target market", "US")
            platform = st.text_input("Platform", "TikTok")
            project_owner = st.text_input("Owner", "Content owner")
        with col2:
            content_objective = st.text_area(
                "TikTok content objective",
                "Validate whether practical in-car mess demos can make the product feel immediately useful.",
            )
            test_question = st.text_area(
                "What question should this content test?",
                "Does a visible cleanup hook make a portable car vacuum cleaner worth watching?",
            )
        with st.expander("Advanced system context", expanded=False):
            initial_route_hypothesis = st.text_input("Initial route hypothesis", "Problem-solution demo")
            store_account_context = st.text_input("Store/account context", "Pilot TikTok Shop account")

    with product_tab:
        st.subheader("Product / Product Version")
        product_name = st.text_input("Product name", "Portable car vacuum cleaner")
        current_sample = st.text_input("Current sample/version", "Sample A - compact cordless version")
        product_version_notes = st.text_area(
            "Version notes",
            "Initial supplier sample for owner smoke testing; no final supplier/sample model is frozen.",
        )
        with st.expander("Generated system IDs", expanded=False):
            generated_project_id = f"cp-{slugify(project_name, 'car-vacuum')}"
            generated_product_id = f"prod-{slugify(product_name, 'car-vacuum')}"
            generated_product_version_id = f"pv-{slugify(current_sample, 'sample-a')}"
            st.code(
                "\n".join(
                    [
                        f"project_id = {generated_project_id}",
                        f"product_id = {generated_product_id}",
                        f"product_version_id = {generated_product_version_id}",
                    ]
                )
            )

    with evidence_tab:
        st.subheader("Evidence Lite")
        st.info("This smoke harness needs at least 1 Evidence Lite item. Evidence binds to ProductVersion Lite.")
        evidence_one = collect_evidence(1, expanded=True)
        evidence_two = collect_evidence(2, expanded=False)
        evidence_three = collect_evidence(3, expanded=False)
        include_evidence_two = st.checkbox("Include Evidence Lite 2", value=False)
        include_evidence_three = st.checkbox("Include Evidence Lite 3", value=False)

    with knowledge_tab:
        st.subheader("Knowledge Pack v0.1")
        st.caption("Knowledge Pack version is fixed for this step: v0.1")
        knowledge_pack_title = st.text_input(
            "Knowledge pack name",
            "Car vacuum cleaner content knowledge pack",
        )
        knowledge_pack_summary = st.text_area(
            "Knowledge pack summary",
            "Rules and patterns for practical car cleaning demos in short-form TikTok content.",
        )
        script_rules = st.text_area(
            "Script rules",
            "Use visible mess, observable product behavior, and avoid unsupported performance guarantees.",
        )
        hook_guidance = st.text_area(
            "Hook guidance",
            "Open with a relatable in-car mess before showing the product.",
        )
        claims_guardrails = st.text_area(
            "Claims guardrails",
            "Tie every claim back to Evidence Lite and avoid proof language not supported by source material.",
        )
        review_rubric = st.text_area(
            "Review rubric",
            "Reviewer checks traceability, claim safety, visual feasibility, and production readiness.",
        )
        market_style_notes = st.text_area(
            "Market style notes",
            "Use practical, quick-demonstration language for TikTok US viewers.",
        )

    with references_tab:
        st.subheader("Manual References")
        st.info("Manual References are fixed to manual intake. The WS-1 input boundary requires 3-5 references.")
        reference_one = collect_reference(1, expanded=True, optional=False)
        reference_two = collect_reference(2, expanded=True, optional=False)
        reference_three = collect_reference(3, expanded=True, optional=False)
        reference_four = collect_reference(4, expanded=False, optional=True)
        reference_five = collect_reference(5, expanded=False, optional=True)

    with validate_tab:
        st.subheader("Validate / Trace Preview")
        st.write("Click the button to call the existing WS-0 and WS-1 services.")
        st.write("Expected result status: `prepared`")
        st.write("No AI output. No Concept. No ScriptPack. No formal Export.")
        submitted = st.form_submit_button("Validate / Build")

if submitted:
    try:
        project_id = f"cp-{slugify(project_name, 'car-vacuum')}"
        product_id = f"prod-{slugify(product_name, 'car-vacuum')}"
        product_version_id = f"pv-{slugify(current_sample, 'sample-a')}"

        evidence_payloads = [evidence_one]
        if include_evidence_two:
            evidence_payloads.append(evidence_two)
        if include_evidence_three:
            evidence_payloads.append(evidence_three)

        reference_payloads = [
            item for item in [reference_one, reference_two, reference_three, reference_four, reference_five] if item
        ]

        ws0_result = create_project_from_handoff(
            CreateWS0ProjectRequest(
                project=ProjectInput(id=project_id, name=project_name),
                operating_context=OperatingContextInput(
                    selection_rationale=selection_rationale,
                    target_market=target_market,
                    platform=platform,
                    content_objective=content_objective,
                    test_question=test_question,
                    project_owner=project_owner,
                    initial_route_hypothesis=initial_route_hypothesis,
                    store_account_context=store_account_context or None,
                ),
                product=ProductInput(id=product_id, name=product_name),
                product_version=ProductVersionInput(
                    id=product_version_id,
                    label=current_sample,
                    notes=product_version_notes or None,
                ),
                evidence=tuple(
                    EvidenceInput(
                        id=str(item["id"]),
                        category=EvidenceCategory(str(item["category"])),
                        source=str(item["source"]),
                        summary=str(item["summary"]),
                        collected_at=item["collected_at"],
                    )
                    for item in evidence_payloads
                ),
            )
        )
        knowledge_pack = KnowledgePack(
            id="kp-car-vacuum-v01",
            version="v0.1",
            title=knowledge_pack_title,
            content_summary=knowledge_pack_summary,
            sections={
                "script_rules": script_rules,
                "hook_guidance": hook_guidance,
                "claims_guardrails": claims_guardrails,
                "review_rubric": review_rubric,
                "market_style_notes": market_style_notes,
            },
        )
        ws1_result = prepare_ws1_inputs(
            PrepareWS1InputsRequest(
                project_id=ws0_result.project.id,
                product_version_id=ws0_result.product_version.id,
                knowledge_pack=knowledge_pack,
                manual_references=tuple(
                    ManualReference(
                        id=str(reference["id"]),
                        project_id=ws0_result.project.id,
                        product_version_id=ws0_result.product_version.id,
                        title=str(reference["title"]),
                        source_identifier=str(reference["source_identifier"]),
                        source_type=str(reference["source_type"]),
                        summary=str(reference["summary"]),
                        observed_pattern=reference["observed_pattern"],
                        content_notes=reference["content_notes"],
                        usage_notes=reference["usage_notes"],
                        intake_method="manual",
                    )
                    for reference in reference_payloads
                ),
            )
        )
    except DomainValidationError as exc:
        st.error(str(exc))
    else:
        st.success("Validated WS-0 -> WS-1 input preparation.")
        trace_left, trace_right = st.columns(2)
        with trace_left:
            st.subheader("Trace Summary")
            st.write("Project created:", ws0_result.project.id)
            st.write("ProductVersion bound:", ws0_result.project.product_version_id)
            st.write("Evidence count:", len(ws0_result.evidence))
            st.write("KnowledgePack version:", ws1_result.knowledge_pack.version)
            st.write("Manual Reference count:", ws1_result.reference_count)
            st.write("WS-1 status:", ws1_result.status)
        with trace_right:
            st.subheader("Boundaries")
            st.write("status can only be: prepared")
            st.write("No AI output")
            st.write("No Concept")
            st.write("No ScriptPack")
            st.write("No Export")

        st.subheader("Reference Traceability")
        st.dataframe(
            [
                {
                    "reference_id": reference.id,
                    "project_id": reference.project_id,
                    "product_version_id": reference.product_version_id,
                    "intake_method": reference.intake_method,
                }
                for reference in ws1_result.manual_references
            ],
            use_container_width=True,
        )

        with st.expander("Technical JSON preview", expanded=False):
            st.caption("This is a dev preview, not the formal Markdown/JSON export.")
            st.code(
                json.dumps(build_preview(ws0_result, ws1_result), ensure_ascii=False, indent=2),
                language="json",
            )
