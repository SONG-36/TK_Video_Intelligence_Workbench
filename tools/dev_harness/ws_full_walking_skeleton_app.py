"""Full WS-0 -> WS-1 walking skeleton visual smoke harness.

This Streamlit app is a local owner-review tool. It is not the product
frontend, not an API, not a persistence layer, and not an AI workflow.
"""

from __future__ import annotations

import json
import hashlib
import re
import sys
from dataclasses import asdict
from enum import Enum
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
    ExportBusinessContext,
    ExportProductionPackRequest,
    GenerateCreativeConceptDraftsRequest,
    GenerateScriptPackDraftRequest,
    KnowledgePack,
    ManualReference,
    PrepareWS1InputsRequest,
    create_manual_creative_concept,
    edit_selected_creative_concept,
    export_production_pack_json,
    export_production_pack_markdown,
    generate_creative_concept_drafts,
    generate_script_pack_draft,
    prepare_ws1_inputs,
    review_script_pack,
    select_creative_concept,
)


def slugify(value: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def stable_id(prefix: str, value: str, fallback: str) -> str:
    slug = slugify(value, fallback)
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{slug}-{digest}"


def jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    return value


def evidence_editor(index: int, *, expanded: bool, optional: bool = False) -> dict[str, str | None] | None:
    with st.expander(f"{'Optional ' if optional else ''}Evidence Lite {index}", expanded=expanded):
        if optional:
            include = st.checkbox(f"Include Evidence {index}", value=False, key=f"include_evidence_{index}")
            if not include:
                return None
        category_values = [item.value for item in EvidenceCategory]
        category = st.selectbox(
            "Evidence type",
            category_values,
            index=category_values.index(EvidenceCategory.SUPPLIER_CLAIM.value)
            if index == 1
            else category_values.index(EvidenceCategory.USER_OBSERVATION.value),
            key=f"evidence_category_{index}",
        )
        source = st.text_input(
            "Source",
            "Supplier product page" if index == 1 else "Owner sample observation",
            key=f"evidence_source_{index}",
        )
        summary = st.text_area(
            "Evidence summary",
            "Supplier claims compact in-car cleaning support."
            if index == 1
            else "The sample fits in a glove compartment and reaches visible seat seams.",
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


def reference_editor(index: int, *, expanded: bool, optional: bool = False) -> dict[str, str | None] | None:
    with st.expander(f"{'Optional ' if optional else ''}Manual Reference {index}", expanded=expanded):
        if optional:
            include = st.checkbox(f"Include Reference {index}", value=False, key=f"include_reference_{index}")
            if not include:
                return None
        title = st.text_input(
            "Reference title",
            f"Car vacuum cleaner reference {index}",
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
            "Reference summary",
            "Manual source showing a mess-first car cleaning content pattern.",
            key=f"reference_summary_{index}",
        )
        observed_pattern = st.text_area(
            "Observed content pattern",
            "Open on crumbs or hidden dust, then show a compact cleanup pass.",
            key=f"reference_observed_pattern_{index}",
        )
        content_notes = st.text_area(
            "Content notes",
            "Useful for pacing, proof shots, and before/after framing.",
            key=f"reference_content_notes_{index}",
        )
        usage_notes = st.text_area(
            "Usage notes",
            "Use as manual inspiration only; preserve source trace.",
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


def build_manual_reference(raw: dict[str, str | None], project_id: str, product_version_id: str) -> ManualReference:
    return ManualReference(
        id=str(raw["id"]),
        project_id=project_id,
        product_version_id=product_version_id,
        title=str(raw["title"]),
        source_identifier=str(raw["source_identifier"]),
        source_type=str(raw["source_type"]),
        summary=str(raw["summary"]),
        observed_pattern=raw["observed_pattern"],
        content_notes=raw["content_notes"],
        usage_notes=raw["usage_notes"],
        intake_method="manual",
    )


def run_walking_skeleton(inputs: dict[str, Any]) -> dict[str, Any]:
    project_id = stable_id("cp", inputs["project_name"], "car-vacuum")
    product_id = stable_id("prod", inputs["product_name"], "car-vacuum")
    product_version_id = stable_id("pv", inputs["product_version_label"], "sample-a")

    evidence_inputs = tuple(
        EvidenceInput(
            id=str(item["id"]),
            category=EvidenceCategory(str(item["category"])),
            source=str(item["source"]),
            summary=str(item["summary"]),
            collected_at=item["collected_at"],
        )
        for item in inputs["evidence"]
    )
    ws0_result = create_project_from_handoff(
        CreateWS0ProjectRequest(
            project=ProjectInput(id=project_id, name=inputs["project_name"]),
            operating_context=OperatingContextInput(
                selection_rationale=inputs["selection_rationale"],
                target_market=inputs["target_market"],
                platform=inputs["platform"],
                content_objective=inputs["content_objective"],
                test_question=inputs["test_question"],
                project_owner=inputs["project_owner"],
                initial_route_hypothesis=inputs["initial_route_hypothesis"],
                store_account_context=inputs["store_account_context"] or None,
            ),
            product=ProductInput(id=product_id, name=inputs["product_name"]),
            product_version=ProductVersionInput(
                id=product_version_id,
                label=inputs["product_version_label"],
                notes=inputs["product_version_notes"] or None,
            ),
            evidence=evidence_inputs,
        )
    )

    knowledge_pack = KnowledgePack(
        id="kp-car-vacuum-v01",
        version="v0.1",
        title=inputs["knowledge_pack_title"],
        content_summary=inputs["knowledge_pack_summary"],
        sections={
            "hook_guidance": inputs["hook_guidance"],
            "claims_guardrails": inputs["claims_guardrails"],
        },
    )
    manual_references = tuple(
        build_manual_reference(reference, ws0_result.project.id, ws0_result.product_version.id)
        for reference in inputs["references"]
    )
    prepared_inputs = prepare_ws1_inputs(
        PrepareWS1InputsRequest(
            project_id=ws0_result.project.id,
            product_version_id=ws0_result.product_version.id,
            knowledge_pack=knowledge_pack,
            manual_references=manual_references,
        )
    )

    evidence_refs = tuple(evidence.id for evidence in ws0_result.evidence)
    generated_concepts = generate_creative_concept_drafts(
        GenerateCreativeConceptDraftsRequest(
            prepared_inputs=prepared_inputs,
            evidence_refs=evidence_refs,
        )
    )
    manual_concept = create_manual_creative_concept(
        prepared_inputs=prepared_inputs,
        evidence_refs=evidence_refs,
        angle=inputs["manual_angle"],
        title=inputs["manual_title"],
        hook=inputs["manual_hook"],
        rationale=inputs["manual_rationale"],
    )
    all_selectable_concepts = (*generated_concepts.concepts, manual_concept)
    selected_concept = select_creative_concept(
        all_selectable_concepts,
        concept_id=inputs["selected_concept_id"] or manual_concept.id,
    )
    if inputs["apply_human_edit"]:
        final_concept = edit_selected_creative_concept(
            selected_concept,
            title=inputs["edited_title"],
            hook=inputs["edited_hook"],
            rationale=inputs["edited_rationale"],
        )
        concept_path = "human_edited"
    else:
        final_concept = selected_concept
        concept_path = "selected_only"
    script_pack = generate_script_pack_draft(
        GenerateScriptPackDraftRequest(
            prepared_inputs=prepared_inputs,
            concept=final_concept,
        )
    )
    review = review_script_pack(
        script_pack,
        decision=inputs["review_decision"],
        reviewer_note=inputs["reviewer_note"],
    )
    export_request = ExportProductionPackRequest(
        business_context=ExportBusinessContext(
            product_context_summary=inputs["product_context_summary"],
            handoff_summary=inputs["handoff_summary"],
            target_market=inputs["target_market"],
            platform=inputs["platform"],
            content_objective=inputs["content_objective"],
            product_name=inputs["product_name"],
            product_version_label=inputs["product_version_label"],
        ),
        prepared_inputs=prepared_inputs,
        concept_drafts=generated_concepts.concepts,
        selected_concept=final_concept,
        script_pack=script_pack,
        review=review,
    )
    markdown_export = export_production_pack_markdown(export_request)
    json_export = export_production_pack_json(export_request)

    return {
        "ws0_result": ws0_result,
        "prepared_inputs": prepared_inputs,
        "generated_concepts": generated_concepts.concepts,
        "manual_concept": manual_concept,
        "selected_concept": selected_concept,
        "final_concept": final_concept,
        "concept_path": concept_path,
        "script_pack": script_pack,
        "review": review,
        "markdown_export": markdown_export,
        "json_export": json_export,
    }


st.set_page_config(page_title="WS Full Production Pack Harness", layout="wide")
st.title("Car Vacuum Cleaner Walking Skeleton Harness")
st.caption("Local visual smoke harness only. Not formal frontend, API, database, AI, or export persistence.")

with st.form("full_walking_skeleton_form"):
    project_tab, product_tab, evidence_tab, knowledge_tab, references_tab, concept_tab, review_tab, export_tab = st.tabs(
        [
            "Project / Handoff",
            "Product / Version",
            "Evidence Lite",
            "Knowledge Pack v0.1",
            "Manual References",
            "Concept",
            "Review",
            "Export Context",
        ]
    )

    with project_tab:
        st.subheader("Project / Handoff")
        project_name = st.text_input("Project name", "Car vacuum cleaner pilot")
        selection_rationale = st.text_area(
            "Why are we testing this product?",
            "Car owners need a compact cleaning solution for crumbs, dust, pet hair, and daily debris.",
        )
        col1, col2 = st.columns(2)
        with col1:
            target_market = st.text_input("Target market", "US car owners")
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
        initial_route_hypothesis = st.text_input("Initial route hypothesis", "Mess-first practical demo")
        store_account_context = st.text_input("Store/account context (optional)", "Pilot TikTok Shop account")

    with product_tab:
        st.subheader("Product / Product Version")
        product_name = st.text_input("Product name", "Portable car vacuum cleaner")
        product_version_label = st.text_input("Current sample/version", "Sample A compact cordless version")
        product_version_notes = st.text_area(
            "Version notes",
            "Initial supplier sample for owner smoke testing; final supplier model is not frozen.",
        )

    with evidence_tab:
        st.subheader("Evidence Lite")
        st.info("Evidence must bind to ProductVersion Lite. This harness requires at least 1 item.")
        evidence_items = [
            evidence_editor(1, expanded=True),
            evidence_editor(2, expanded=False),
            evidence_editor(3, expanded=False, optional=True),
        ]

    with knowledge_tab:
        st.subheader("Knowledge Pack v0.1")
        st.caption("Version is fixed to v0.1 by the backend boundary.")
        knowledge_pack_title = st.text_input(
            "Knowledge Pack title",
            "Car vacuum cleaner content knowledge pack v0.1",
        )
        knowledge_pack_summary = st.text_area(
            "Knowledge Pack summary",
            "Use observable cleanup claims, mess-first hooks, and Evidence-backed proof shots.",
        )
        hook_guidance = st.text_area(
            "Hook guidance",
            "Open with visible crumbs, dust, or hidden dirt before revealing the product.",
        )
        claims_guardrails = st.text_area(
            "Claims guardrails",
            "Avoid unsupported suction, battery, durability, or cleaning guarantees.",
        )

    with references_tab:
        st.subheader("Manual References")
        st.info("Manual References must stay at 3-5 items and preserve manual intake trace.")
        reference_items = [
            reference_editor(1, expanded=True),
            reference_editor(2, expanded=True),
            reference_editor(3, expanded=True),
            reference_editor(4, expanded=False, optional=True),
            reference_editor(5, expanded=False, optional=True),
        ]

    with concept_tab:
        st.subheader("Manual CreativeConcept")
        manual_angle = st.text_input("Manual concept angle", "Weekend crumb rescue")
        manual_title = st.text_input("Manual concept title", "The 60-second snack crumb rescue")
        manual_hook = st.text_area("Manual concept hook", "The snack mess under the seat is worse than it looks.")
        manual_rationale = st.text_area(
            "Manual concept rationale",
            "Owner wants a practical, visible cleanup story that is easy to hand off for generation.",
        )
        selection_mode = st.radio(
            "Concept to select for ScriptPack",
            [
                "Manual owner-created concept",
                "Generated Mess Rescue / Crumb Disaster",
                "Generated Hidden Dirt Proof",
                "Generated Daily Car Reset",
            ],
        )
        apply_human_edit = st.checkbox("Apply human edit after selection", value=True)
        edited_title = st.text_input("Edited selected concept title", "Owner edited crumb rescue concept")
        edited_hook = st.text_area("Edited selected concept hook", "The snack mess under the seat is the proof.")
        edited_rationale = st.text_area(
            "Edited selected concept rationale",
            "Keep the manual owner direction while preserving all Evidence, Reference, and Knowledge Pack trace.",
        )

    with review_tab:
        st.subheader("Human Review")
        review_decision = st.selectbox("Review decision", ["approved", "rework", "hold", "stopped"], index=0)
        reviewer_note = st.text_area("Reviewer note", "Approved for generation-ready production handoff.")

    with export_tab:
        st.subheader("Export Business Context")
        product_context_summary = st.text_area(
            "Product context summary",
            "Portable car vacuum cleaner Sample A for a practical in-car cleanup pilot.",
        )
        handoff_summary = st.text_area(
            "Selection-to-Content Handoff summary",
            "Selection-to-content handoff focuses on proving visible crumb cleanup in a TikTok demo.",
        )

    submitted = st.form_submit_button("Run Full Walking Skeleton")

if submitted:
    evidence = [item for item in evidence_items if item is not None]
    references = [item for item in reference_items if item is not None]
    selected_lookup = {
        "Generated Mess Rescue / Crumb Disaster": "concept-mess-rescue-crumb-disaster",
        "Generated Hidden Dirt Proof": "concept-hidden-dirt-proof",
        "Generated Daily Car Reset": "concept-daily-car-reset",
        "Manual owner-created concept": "",
    }
    try:
        result = run_walking_skeleton(
            {
                "project_name": project_name,
                "selection_rationale": selection_rationale,
                "target_market": target_market,
                "platform": platform,
                "content_objective": content_objective,
                "test_question": test_question,
                "project_owner": project_owner,
                "initial_route_hypothesis": initial_route_hypothesis,
                "store_account_context": store_account_context,
                "product_name": product_name,
                "product_version_label": product_version_label,
                "product_version_notes": product_version_notes,
                "evidence": evidence,
                "knowledge_pack_title": knowledge_pack_title,
                "knowledge_pack_summary": knowledge_pack_summary,
                "hook_guidance": hook_guidance,
                "claims_guardrails": claims_guardrails,
                "references": references,
                "manual_angle": manual_angle,
                "manual_title": manual_title,
                "manual_hook": manual_hook,
                "manual_rationale": manual_rationale,
                "selected_concept_id": selected_lookup[selection_mode],
                "apply_human_edit": apply_human_edit,
                "edited_title": edited_title,
                "edited_hook": edited_hook,
                "edited_rationale": edited_rationale,
                "review_decision": review_decision,
                "reviewer_note": reviewer_note,
                "product_context_summary": product_context_summary,
                "handoff_summary": handoff_summary,
            }
        )
    except DomainValidationError as exc:
        st.error(str(exc))
    else:
        st.success("Full WS-0 -> WS-1 walking skeleton completed in memory.")

        trace_tab, concepts_tab, script_tab, review_output_tab, markdown_tab, json_tab = st.tabs(
            ["Trace IDs", "Concept Drafts", "ScriptPackDraft", "ReviewDecision", "Markdown", "JSON"]
        )

        with trace_tab:
            ws0_result = result["ws0_result"]
            prepared_inputs = result["prepared_inputs"]
            st.subheader("Trace IDs")
            st.json(
                {
                    "project_id": ws0_result.project.id,
                    "product_id": ws0_result.product.id,
                    "product_version_id": ws0_result.product_version.id,
                    "project_product_version_id": ws0_result.project.product_version_id,
                    "evidence_product_version_ids": [
                        evidence.product_version_id for evidence in ws0_result.evidence
                    ],
                    "knowledge_pack_id": prepared_inputs.knowledge_pack.id,
                    "knowledge_pack_version": prepared_inputs.knowledge_pack.version,
                    "manual_reference_count": prepared_inputs.reference_count,
                    "concept_path": result["concept_path"],
                    "selected_concept_id": result["selected_concept"].id,
                    "final_concept_id": result["final_concept"].id,
                    "final_concept_generation_method": result["final_concept"].generation_method,
                    "production_readiness": result["json_export"]["production_readiness"],
                }
            )

        with concepts_tab:
            st.subheader("Generated CreativeConcept Drafts")
            st.json(jsonable(result["generated_concepts"]))
            st.subheader("Manual CreativeConcept Draft")
            st.json(jsonable(result["manual_concept"]))
            st.subheader("Selected Concept")
            st.json(jsonable(result["selected_concept"]))
            st.subheader("Final Concept Used for ScriptPack")
            st.caption(f"Concept path: {result['concept_path']}")
            st.json(jsonable(result["final_concept"]))

        with script_tab:
            st.subheader("ScriptPackDraft")
            st.json(jsonable(result["script_pack"]))

        with review_output_tab:
            st.subheader("ReviewDecision")
            st.json(jsonable(result["review"]))

        with markdown_tab:
            st.subheader("Markdown Production Pack")
            st.text_area("Markdown export", result["markdown_export"], height=700)

        with json_tab:
            st.subheader("JSON-compatible Production Pack")
            st.json(result["json_export"])
            st.download_button(
                "Download JSON preview",
                data=json.dumps(result["json_export"], indent=2),
                file_name="production-pack-preview.json",
                mime="application/json",
            )
