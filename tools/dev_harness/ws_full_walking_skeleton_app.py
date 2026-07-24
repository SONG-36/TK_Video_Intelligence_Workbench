"""Chinese-first local workspace harness for the WS-0 -> WS-1 skeleton.

This Streamlit app is a local owner-review tool. It is not the product
frontend, not an API, not a database, and not an AI workflow.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from tvi_workbench.workspace_snapshot import (  # noqa: E402
    WORKSPACE_SCHEMA_VERSION,
    WorkspaceSnapshotValidationError,
    list_workspace_snapshots,
    load_workspace_snapshot,
    save_workspace_snapshot,
    validate_workspace_snapshot,
)
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


EVIDENCE_TYPE_LABELS = {
    EvidenceCategory.SUPPLIER_DOCUMENT.value: "供应商资料",
    EvidenceCategory.SUPPLIER_CLAIM.value: "供应商说法",
    EvidenceCategory.USER_OBSERVATION.value: "人工观察",
    EvidenceCategory.TEST_RESULT.value: "测试结果",
    EvidenceCategory.IMAGE.value: "图片",
    EvidenceCategory.VIDEO.value: "视频",
    EvidenceCategory.LINK.value: "链接",
    EvidenceCategory.OTHER.value: "其他",
}
REVIEW_DECISION_LABELS = {
    "approved": "通过：可以形成生产交接包",
    "rework": "返工：需要修改后再交接",
    "hold": "暂缓：暂停但保留项目",
    "stopped": "终止：终止本轮生产",
}
GENERATED_CONCEPT_OPTIONS = {
    "manual": "手动创意方向",
    "concept-mess-rescue-crumb-disaster": "系统草稿 1：零食碎屑救援",
    "concept-hidden-dirt-proof": "系统草稿 2：隐藏脏污证明",
    "concept-daily-car-reset": "系统草稿 3：日常车内重置",
}
CONCEPT_PRIMARY_LABELS = {
    "concept-mess-rescue-crumb-disaster": {
        "angle": "零食碎屑救援",
        "title": "零食碎屑救援",
        "hook": "一次通勤之后，车里到处都是碎屑？",
    },
    "concept-hidden-dirt-proof": {
        "angle": "隐藏脏污证明",
        "title": "隐藏脏污证明",
        "hook": "车看起来很干净，直到镜头靠近缝隙。",
    },
    "concept-daily-car-reset": {
        "angle": "日常车内重置",
        "title": "日常车内重置",
        "hook": "下一次开车前，给车内做一次 60 秒重置。",
    },
}


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


def primary_status_label(value: str) -> str:
    if value == "draft":
        return "草稿"
    return value


def primary_concept_value(concept: Any, field_name: str) -> str:
    display_values = CONCEPT_PRIMARY_LABELS.get(getattr(concept, "id", ""))
    if display_values and field_name in display_values:
        return display_values[field_name]
    return getattr(concept, field_name)


def initialize_workspace_state() -> None:
    if "evidence_card_ids" not in st.session_state:
        st.session_state["evidence_card_ids"] = [1, 2]
    if "next_evidence_card_id" not in st.session_state:
        st.session_state["next_evidence_card_id"] = 3


def add_evidence_card() -> None:
    next_id = int(st.session_state["next_evidence_card_id"])
    st.session_state["evidence_card_ids"].append(next_id)
    st.session_state["next_evidence_card_id"] = next_id + 1


def remove_evidence_card(card_id: int) -> None:
    card_ids = list(st.session_state["evidence_card_ids"])
    if len(card_ids) <= 1:
        st.warning("至少需要保留 1 条产品证据。")
        return
    st.session_state["evidence_card_ids"] = [item for item in card_ids if item != card_id]


def build_workspace_snapshot(result: dict[str, Any]) -> dict[str, Any]:
    ws0_result = result["ws0_result"]
    prepared_inputs = result["prepared_inputs"]
    final_concept = result["final_concept"]
    script_pack = result["script_pack"]
    review = result["review"]
    markdown_export = result["markdown_export"]
    json_export = result["json_export"]
    evidence_ids = [evidence.id for evidence in ws0_result.evidence]
    manual_reference_ids = [reference.id for reference in prepared_inputs.manual_references]

    return {
        "workspace_schema_version": WORKSPACE_SCHEMA_VERSION,
        "saved_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "project_id": ws0_result.project.id,
        "product_version_id": ws0_result.product_version.id,
        "status": "reviewed",
        "content_project": jsonable(ws0_result.project),
        "operating_context": jsonable(ws0_result.project.operating_context),
        "product": jsonable(ws0_result.product),
        "product_version": jsonable(ws0_result.product_version),
        "evidence": jsonable(ws0_result.evidence),
        "knowledge_pack": jsonable(prepared_inputs.knowledge_pack),
        "manual_references": jsonable(prepared_inputs.manual_references),
        "creative_concept_drafts": jsonable((*result["generated_concepts"], result["manual_concept"])),
        "selected_concept": jsonable(final_concept),
        "script_pack": jsonable(script_pack),
        "review_decision": jsonable(review),
        "production_pack_export": {
            "format": "markdown_and_json",
            "project_id": json_export["project_id"],
            "product_version_id": json_export["product_version_id"],
            "production_readiness": json_export["production_readiness"],
            "markdown": markdown_export,
            "json": json_export,
        },
        "trace_summary": {
            "project_id": ws0_result.project.id,
            "product_version_id": ws0_result.product_version.id,
            "evidence_refs": evidence_ids,
            "manual_reference_refs": manual_reference_ids,
            "knowledge_pack_id": prepared_inputs.knowledge_pack.id,
            "knowledge_pack_version": prepared_inputs.knowledge_pack.version,
            "selected_concept_id": final_concept.id,
            "selected_concept_generation_method": final_concept.generation_method,
            "script_pack_id": script_pack.id,
            "review_decision": review.decision,
            "production_readiness": json_export["production_readiness"],
        },
    }


def display_loaded_snapshot(snapshot: Any, *, key_prefix: str = "loaded") -> None:
    snapshot_data = snapshot.to_dict()
    production_pack_export = snapshot_data["production_pack_export"]

    st.subheader("已加载的工作区快照")
    st.write(
        {
            "项目": snapshot_data["project_id"],
            "当前版本": snapshot_data["product_version_id"],
            "保存时间": snapshot_data["saved_at"],
            "状态": snapshot_data["status"],
            "生产状态": production_pack_export.get("production_readiness"),
        }
    )
    with st.expander("调试追踪", expanded=False):
        st.json(snapshot_data["trace_summary"])
    if production_pack_export.get("markdown"):
        st.text_area(
            "生产交接包 Markdown 预览",
            str(production_pack_export["markdown"]),
            height=420,
            key=f"{key_prefix}_markdown_{snapshot_data['project_id']}",
        )
    if production_pack_export.get("json"):
        with st.expander("JSON 追踪预览", expanded=False):
            st.json(production_pack_export["json"])


def evidence_card(card_id: int, position: int) -> dict[str, str | None]:
    with st.container(border=True):
        card_title_col, action_col = st.columns([4, 1])
        with card_title_col:
            st.markdown(f"#### 产品证据 / 卖点依据 {position}")
        with action_col:
            if st.button("删除", key=f"remove_evidence_{card_id}"):
                remove_evidence_card(card_id)
                st.rerun()

        default_type = (
            EvidenceCategory.SUPPLIER_CLAIM.value
            if position == 1
            else EvidenceCategory.USER_OBSERVATION.value
        )
        type_options = list(EVIDENCE_TYPE_LABELS)
        selected_type = st.selectbox(
            "证据类型",
            type_options,
            index=type_options.index(default_type),
            format_func=lambda value: EVIDENCE_TYPE_LABELS[value],
            key=f"evidence_type_{card_id}",
        )
        title = st.text_input(
            "证据标题",
            "供应商页面核心卖点" if position == 1 else "样品人工观察",
            key=f"evidence_title_{card_id}",
        )
        summary = st.text_area(
            "证据内容",
            "供应商宣称这款车载吸尘器适合车内碎屑和灰尘清理。"
            if position == 1
            else "样品可以放进手套箱，吸头能伸进座椅缝隙。",
            key=f"evidence_summary_{card_id}",
        )
        supported_claim = st.text_input(
            "支持的卖点",
            "车内小空间清洁" if position == 1 else "便携和缝隙清洁场景",
            key=f"evidence_supported_claim_{card_id}",
        )
        source = st.text_input(
            "来源",
            "供应商产品页" if position == 1 else "Owner 样品观察",
            key=f"evidence_source_{card_id}",
        )
        risk_note = st.text_area(
            "风险备注",
            "不要夸大吸力、续航或耐用性；只使用当前证据能支持的说法。",
            key=f"evidence_risk_note_{card_id}",
        )

    combined_summary = "\n".join(
        [
            f"证据标题: {title}",
            f"证据内容: {summary}",
            f"支持的卖点: {supported_claim}",
            f"风险备注: {risk_note}",
        ]
    )
    return {
        "id": f"ev-car-vacuum-{card_id:03d}",
        "category": selected_type,
        "source": source,
        "summary": combined_summary,
        "collected_at": None,
        "title": title,
        "supported_claim": supported_claim,
        "risk_note": risk_note,
    }


def reference_card(index: int, *, required: bool) -> dict[str, str | None] | None:
    with st.container(border=True):
        label = f"参考视频 / 参考素材 {index}"
        st.markdown(f"#### {label}{'（必填）' if required else '（可选）'}")
        if not required:
            include = st.checkbox("使用这条参考素材", value=False, key=f"include_reference_{index}")
            if not include:
                return None

        title = st.text_input(
            "标题",
            f"车载吸尘器参考视频 {index}",
            key=f"reference_title_{index}",
        )
        source_identifier = st.text_input(
            "来源链接",
            f"https://example.com/car-vacuum-reference-{index}",
            key=f"reference_source_{index}",
        )
        platform = st.text_input(
            "平台",
            "TikTok",
            key=f"reference_platform_{index}",
        )
        why_useful = st.text_area(
            "为什么值得参考",
            "这个参考用车内真实脏乱开场，能快速说明使用场景。",
            key=f"reference_why_useful_{index}",
        )
        borrowable_pattern = st.text_area(
            "可借鉴的结构/画面/节奏",
            "先给碎屑或隐藏灰尘特写，再切到清理动作和前后对比。",
            key=f"reference_borrowable_pattern_{index}",
        )
        do_not_copy_note = st.text_area(
            "不能照抄的提醒",
            "只借鉴结构和节奏，不复制画面、文案、音乐或账号表达。",
            key=f"reference_do_not_copy_{index}",
        )

    return {
        "id": f"ref-car-vacuum-{index:03d}",
        "title": title,
        "source_identifier": source_identifier,
        "source_type": platform,
        "summary": why_useful,
        "observed_pattern": borrowable_pattern or None,
        "content_notes": why_useful or None,
        "usage_notes": do_not_copy_note or None,
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
            angle=inputs["edited_angle"],
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


def render_snapshot_loader(*, compact: bool = False) -> None:
    if compact:
        st.caption("本地 JSON 快照，仅用于查看，不会回填编辑表单。")
    else:
        st.subheader("保存 / 加载")
        st.caption("本地 JSON 快照用于保存和检查当前工作区；A2.1 不做可编辑恢复。")

    if st.button("刷新快照列表", key=f"refresh_snapshot_list_{compact}"):
        st.rerun()
    try:
        snapshot_summaries = list_workspace_snapshots()
    except WorkspaceSnapshotValidationError as exc:
        snapshot_summaries = []
        st.error(f"快照列表读取失败: {exc}")

    if not snapshot_summaries:
        st.info("还没有可用的本地快照。")
        return

    snapshot_options = {
        f"{summary.project_id} | {summary.saved_at} | {summary.status}": summary.project_id
        for summary in snapshot_summaries
    }
    selected_snapshot_label = st.selectbox(
        "选择已保存快照",
        list(snapshot_options),
        key=f"snapshot_select_{compact}",
    )
    if st.button("加载选中快照（只读查看）", key=f"load_snapshot_{compact}"):
        try:
            loaded_snapshot = load_workspace_snapshot(snapshot_options[selected_snapshot_label])
            validate_workspace_snapshot(loaded_snapshot)
        except WorkspaceSnapshotValidationError as exc:
            st.error(f"快照校验失败: {exc}")
        else:
            st.session_state["loaded_workspace_snapshot"] = loaded_snapshot
            st.success("快照已加载，可在保存 / 加载区域查看。")


def concept_card(concept: Any, title: str) -> None:
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.write(f"角度: {primary_concept_value(concept, 'angle')}")
        st.write(f"标题: {primary_concept_value(concept, 'title')}")
        st.write(f"开头 Hook: {primary_concept_value(concept, 'hook')}")
        st.write(f"理由: {concept.rationale}")
        st.caption(f"状态: {primary_status_label(concept.status)}；不会自动批准")
        with st.expander("调试追踪", expanded=False):
            st.json(
                {
                    "concept_id": concept.id,
                    "project_id": concept.project_id,
                    "product_version_id": concept.product_version_id,
                    "evidence_refs": list(concept.evidence_refs),
                    "manual_reference_refs": list(concept.manual_reference_refs),
                    "knowledge_pack_id": concept.knowledge_pack_id,
                    "knowledge_pack_version": concept.knowledge_pack_version,
                    "generation_method": concept.generation_method,
                    "selected": concept.selected,
                }
            )


def render_result_workspace(result: dict[str, Any]) -> None:
    concept_tab, script_tab, review_tab, pack_tab, snapshot_tab = st.tabs(
        ["创意方向", "剧本草稿", "审核", "生产包", "保存 / 加载"]
    )

    with concept_tab:
        st.subheader("创意方向草稿")
        st.caption(
            "这里展示本次运行产生的创意方向。无论是选中还是人工编辑，概念仍然保持草稿。"
        )
        cols = st.columns(3)
        for index, concept in enumerate(result["generated_concepts"]):
            with cols[index]:
                concept_card(concept, f"系统生成草稿 {index + 1}")
        st.divider()
        concept_card(result["manual_concept"], "手动创意方向")
        st.divider()
        path_label = "人工编辑后进入剧本" if result["concept_path"] == "human_edited" else "选中后直接进入剧本"
        concept_card(result["final_concept"], f"最终用于剧本的创意方向：{path_label}")

    with script_tab:
        script_pack = result["script_pack"]
        st.subheader("剧本包草稿")
        st.caption("剧本包仍是草稿，需要人工审核后才能形成生产交接包。")
        st.markdown(f"#### {script_pack.title}")
        st.write(f"目标时长: {script_pack.target_duration_seconds} 秒")
        st.write(f"画幅: {script_pack.aspect_ratio}")
        st.text_area("口播脚本", script_pack.voiceover_script, height=150)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### 分镜草稿")
            for item in script_pack.storyboard:
                st.write(f"- {item}")
            st.markdown("##### 镜头清单")
            for item in script_pack.shot_list:
                st.write(f"- {item}")
        with col2:
            st.markdown("##### 画面要求")
            for item in script_pack.visual_requirements:
                st.write(f"- {item}")
            st.markdown("##### 素材需求")
            for item in script_pack.asset_requirements:
                st.write(f"- {item}")
        with st.expander("生成备注 / 风险备注", expanded=False):
            st.markdown("##### 生成/制作备注")
            for item in script_pack.generation_notes:
                st.write(f"- {item}")
            st.markdown("##### 风险备注")
            for item in script_pack.risk_notes:
                st.write(f"- {item}")
        with st.expander("调试追踪", expanded=False):
            st.json(jsonable(script_pack))

    with review_tab:
        review = result["review"]
        st.subheader("人工审核结果")
        st.write(REVIEW_DECISION_LABELS[review.decision])
        st.write(f"审核备注: {review.reviewer_note}")
        with st.expander("调试追踪", expanded=False):
            st.json(jsonable(review))

    with pack_tab:
        st.subheader("生产交接包")
        st.caption("Markdown 是主要人工交接内容；JSON 只作为系统追踪检查。")
        markdown_tab, json_tab, debug_tab = st.tabs(["Markdown 交接包", "JSON 追踪", "调试追踪"])
        with markdown_tab:
            st.text_area("生产交接包 Markdown", result["markdown_export"], height=700)
        with json_tab:
            st.json(result["json_export"])
            st.download_button(
                "下载 JSON 预览",
                data=json.dumps(result["json_export"], ensure_ascii=False, indent=2),
                file_name="production-pack-preview.json",
                mime="application/json",
            )
        with debug_tab:
            ws0_result = result["ws0_result"]
            prepared_inputs = result["prepared_inputs"]
            st.json(
                {
                    "project_id": ws0_result.project.id,
                    "product_id": ws0_result.product.id,
                    "product_version_id": ws0_result.product_version.id,
                    "evidence_refs": [evidence.id for evidence in ws0_result.evidence],
                    "manual_reference_refs": [reference.id for reference in prepared_inputs.manual_references],
                    "knowledge_pack_id": prepared_inputs.knowledge_pack.id,
                    "knowledge_pack_version": prepared_inputs.knowledge_pack.version,
                    "selected_concept_id": result["final_concept"].id,
                    "script_pack_id": result["script_pack"].id,
                    "review_decision": result["review"].decision,
                    "production_readiness": result["json_export"]["production_readiness"],
                }
            )

    with snapshot_tab:
        render_snapshot_actions(result)
        if "loaded_workspace_snapshot" in st.session_state:
            st.divider()
            display_loaded_snapshot(st.session_state["loaded_workspace_snapshot"], key_prefix="result_loaded")


def render_snapshot_actions(result: dict[str, Any]) -> None:
    st.subheader("保存 / 加载")
    st.caption("保存当前完整工作区；加载仍然只是只读检查，不会回填编辑表单。")
    snapshot = build_workspace_snapshot(result)
    try:
        validate_workspace_snapshot(snapshot)
    except WorkspaceSnapshotValidationError as exc:
        st.error(f"当前工作区快照不可保存: {exc}")
    else:
        st.success("当前工作区快照校验通过。")
        if st.button("保存当前工作区快照"):
            try:
                saved_path = save_workspace_snapshot(snapshot)
            except WorkspaceSnapshotValidationError as exc:
                st.error(f"保存失败: {exc}")
            else:
                st.success(f"已保存到: {saved_path}")
        with st.expander("当前快照 JSON 预览", expanded=False):
            st.json(snapshot)
    st.divider()
    render_snapshot_loader()


st.set_page_config(page_title="车载吸尘器内容工作区", layout="wide")
initialize_workspace_state()
st.title("车载吸尘器内容工作区")
st.caption("本地 Minimum Workspace。不是正式前端、API、数据库、AI 工作流或生成编排系统。")

with st.sidebar:
    st.header("保存 / 加载")
    render_snapshot_loader(compact=True)

if "loaded_workspace_snapshot" in st.session_state:
    with st.expander("已加载快照（只读查看）", expanded=False):
        display_loaded_snapshot(st.session_state["loaded_workspace_snapshot"], key_prefix="top_loaded")

input_tab, evidence_tab, reference_tab, concept_input_tab, script_input_tab, review_input_tab, pack_input_tab = st.tabs(
    ["项目输入", "产品证据", "参考视频", "创意方向", "剧本草稿", "审核", "生产包"]
)

with input_tab:
    st.subheader("项目输入")
    st.caption("先描述这次内容项目、当前样品和要验证的内容目标。系统 ID 会自动生成。")
    project_name = st.text_input("项目名称", "车载吸尘器内容测试")
    selection_rationale = st.text_area(
        "为什么测试这个产品？",
        "车主经常需要清理零食碎屑、灰尘、宠物毛发和日常杂物，便携清洁工具有明确内容场景。",
    )
    col1, col2 = st.columns(2)
    with col1:
        target_market = st.text_input("目标市场", "美国车主")
        platform = st.text_input("内容平台", "TikTok")
        project_owner = st.text_input("负责人", "内容负责人")
    with col2:
        content_objective = st.text_area(
            "本轮内容目标",
            "验证真实车内脏乱场景是否能让车载吸尘器显得立刻有用。",
        )
        test_question = st.text_area(
            "本轮要回答的问题",
            "用明显碎屑清理开场，是否能提高用户继续观看和理解产品价值的意愿？",
        )
    initial_route_hypothesis = st.text_input("初始内容方向假设", "真实脏乱开场 + 快速清理证明")
    store_account_context = st.text_input("店铺/账号背景（可选）", "TikTok Shop 试运营账号")
    st.divider()
    st.subheader("当前样品 / 当前版本")
    product_name = st.text_input("产品名称", "便携车载吸尘器")
    product_version_label = st.text_input("当前样品 / 当前版本", "Sample A 便携无线版本")
    product_version_notes = st.text_area(
        "版本备注",
        "当前为供应商样品，用于内容方向验证；最终供应商和量产版本尚未冻结。",
    )
    with st.expander("调试：自动生成的系统 ID", expanded=False):
        st.json(
            {
                "project_id_preview": stable_id("cp", project_name, "car-vacuum"),
                "product_id_preview": stable_id("prod", product_name, "car-vacuum"),
                "product_version_id_preview": stable_id("pv", product_version_label, "sample-a"),
            }
        )

with evidence_tab:
    st.subheader("产品证据 / 卖点依据")
    st.caption("至少 1 条。系统会自动把每条证据绑定到当前样品 / 当前版本。")
    evidence_button_col, evidence_count_col = st.columns([1, 3])
    with evidence_button_col:
        if st.button("添加产品证据"):
            add_evidence_card()
            st.rerun()
    with evidence_count_col:
        st.info(f"当前有 {len(st.session_state['evidence_card_ids'])} 条产品证据。")
    evidence_items = [
        evidence_card(card_id, position)
        for position, card_id in enumerate(st.session_state["evidence_card_ids"], start=1)
    ]

with reference_tab:
    st.subheader("参考视频 / 参考素材")
    st.caption("3 条必填，最多可再加 2 条可选参考。所有参考都保持 manual intake。")
    reference_items = [
        reference_card(1, required=True),
        reference_card(2, required=True),
        reference_card(3, required=True),
        reference_card(4, required=False),
        reference_card(5, required=False),
    ]

with concept_input_tab:
    st.subheader("创意方向")
    st.caption("运行后会产生 3 个系统模拟创意方向，也可以加入一个手动创意方向。选中或编辑后仍是草稿。")
    st.markdown("#### 生成创意方向预览")
    preview_cols = st.columns(3)
    preview_cards = [
        ("系统草稿 1", "零食碎屑救援", "用真实脏乱开场，让清理结果更直观。"),
        ("系统草稿 2", "隐藏脏污证明", "拍出看似干净但实际很脏的车内细节。"),
        ("系统草稿 3", "日常车内重置", "把产品包装成日常 60 秒车内重置习惯。"),
    ]
    for col, (angle, title, rationale) in zip(preview_cols, preview_cards):
        with col:
            with st.container(border=True):
                st.markdown(f"##### {title}")
                st.write(angle)
                st.write(rationale)
                st.caption("运行后生成；状态保持草稿")
    st.divider()
    st.markdown("#### 手动创意方向")
    manual_angle = st.text_input("创意角度", "周末碎屑救援")
    manual_title = st.text_input("创意标题", "60 秒零食碎屑救援")
    manual_hook = st.text_area("开头 Hook", "座椅下面的零食碎屑，比你想象得更明显。")
    manual_rationale = st.text_area(
        "为什么这个方向值得做",
        "用车主熟悉的真实脏乱场景进入，能直接展示便携车载吸尘器的使用理由。",
    )
    selected_choice = st.radio(
        "选择哪个创意方向进入剧本草稿？",
        list(GENERATED_CONCEPT_OPTIONS),
        format_func=lambda value: GENERATED_CONCEPT_OPTIONS[value],
    )
    apply_human_edit = st.checkbox("选择后进行人工编辑", value=True)
    if apply_human_edit:
        st.markdown("#### 人工编辑后的创意方向")
        edited_angle = st.text_input("编辑后的创意角度", "周末碎屑救援")
        edited_title = st.text_input("编辑后的创意标题", "车内零食碎屑 60 秒清理")
        edited_hook = st.text_area("编辑后的 Hook", "座椅下面的碎屑，就是这条视频的证明。")
        edited_rationale = st.text_area(
            "编辑后的理由",
            "保留真实脏乱场景，同时把所有产品证据、参考素材和知识包追踪保留下来。",
        )
    else:
        st.info("将直接使用选中的创意方向生成剧本草稿，创意仍保持草稿。")
        edited_angle = edited_title = edited_hook = edited_rationale = None

with script_input_tab:
    st.subheader("剧本草稿")
    st.caption("剧本草稿由现有 deterministic/mock backend service 生成。本页不接入 AI 或 prompt。")
    if "last_full_ws_result" in st.session_state:
        script_pack = st.session_state["last_full_ws_result"]["script_pack"]
        st.write(f"当前剧本包草稿: {script_pack.title}")
        st.write(f"状态: {primary_status_label(script_pack.status)}")
    else:
        st.info("完成前面的输入并运行后，这里会展示剧本包草稿。")

with review_input_tab:
    st.subheader("审核")
    review_label = st.selectbox("人工审核结果", list(REVIEW_DECISION_LABELS.values()), index=0)
    review_decision = next(
        value for value, label in REVIEW_DECISION_LABELS.items() if label == review_label
    )
    reviewer_note = st.text_area("审核备注", "可以形成生产交接包，但最终拍摄/生成前仍需人工复核。")

with pack_input_tab:
    st.subheader("生产包")
    st.caption("Markdown 是主要生产交接内容；JSON 追踪只用于系统检查。")
    product_context_summary = st.text_area(
        "产品背景摘要",
        "便携车载吸尘器 Sample A，用于验证真实车内清洁场景的内容表达。",
    )
    handoff_summary = st.text_area(
        "选品到内容交接摘要",
        "本轮交接重点是用可见碎屑清理证明产品价值，并避免超出证据支持的性能承诺。",
    )

st.divider()
run_col, status_col = st.columns([1, 3])
with run_col:
    run_clicked = st.button("运行完整流程", type="primary")
with status_col:
    st.caption("运行后会依次完成 WS-0 项目创建、WS-1 输入准备、创意方向、剧本草稿、审核和生产交接包。")

if run_clicked:
    evidence = [item for item in evidence_items if item is not None]
    references = [item for item in reference_items if item is not None]
    selected_concept_id = "" if selected_choice == "manual" else selected_choice
    if not evidence:
        st.error("至少需要 1 条产品证据 / 卖点依据。")
    elif not 3 <= len(references) <= 5:
        st.error("参考视频 / 参考素材必须是 3-5 条。")
    else:
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
                    "knowledge_pack_title": "车载吸尘器内容知识包 v0.1",
                    "knowledge_pack_summary": "使用可观察证据、真实清洁场景和手工参考素材来约束内容方向。",
                    "hook_guidance": "优先用碎屑、灰尘、座椅缝隙等可见问题开场。",
                    "claims_guardrails": "不要做未经证据支持的吸力、续航、耐用性或清洁保证。",
                    "references": references,
                    "manual_angle": manual_angle,
                    "manual_title": manual_title,
                    "manual_hook": manual_hook,
                    "manual_rationale": manual_rationale,
                    "selected_concept_id": selected_concept_id,
                    "apply_human_edit": apply_human_edit,
                    "edited_angle": edited_angle,
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
            st.error(f"流程校验失败: {exc}")
        else:
            st.session_state["last_full_ws_result"] = result
            st.success("完整 WS-0 -> WS-1 本地流程已完成。")

if "last_full_ws_result" in st.session_state:
    render_result_workspace(st.session_state["last_full_ws_result"])
