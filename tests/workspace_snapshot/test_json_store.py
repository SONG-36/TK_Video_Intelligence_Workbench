import json
from copy import deepcopy

import pytest

from tvi_workbench.workspace_snapshot import (
    WORKSPACE_SCHEMA_VERSION,
    WorkspaceSnapshotValidationError,
    list_workspace_snapshots,
    load_workspace_snapshot,
    save_workspace_snapshot,
)


def make_snapshot() -> dict:
    return {
        "workspace_schema_version": WORKSPACE_SCHEMA_VERSION,
        "saved_at": "2026-07-24T10:00:00+08:00",
        "project_id": "cp-car-vacuum-001",
        "product_version_id": "pv-car-vacuum-sample-a",
        "status": "reviewed",
        "content_project": {
            "id": "cp-car-vacuum-001",
            "name": "Car vacuum cleaner pilot",
            "product_version_id": "pv-car-vacuum-sample-a",
        },
        "operating_context": {
            "selection_rationale": "Car owners need a compact cleaning solution.",
            "target_market": "US car owners",
            "platform": "TikTok",
            "content_objective": "Validate practical in-car mess demos.",
            "test_question": "Does a visible cleanup hook earn attention?",
            "project_owner": "Content owner",
        },
        "product": {
            "id": "prod-car-vacuum",
            "name": "Portable car vacuum cleaner",
        },
        "product_version": {
            "id": "pv-car-vacuum-sample-a",
            "product_id": "prod-car-vacuum",
            "label": "Sample A compact cordless version",
        },
        "evidence": [
            {
                "id": "ev-supplier-claim-001",
                "product_version_id": "pv-car-vacuum-sample-a",
                "category": "SUPPLIER_CLAIM",
                "source": "Supplier product page",
                "summary": "Supplier claims compact in-car cleaning support.",
            },
            {
                "id": "ev-owner-observation-001",
                "product_version_id": "pv-car-vacuum-sample-a",
                "category": "USER_OBSERVATION",
                "source": "Owner observation",
                "summary": "The sample fits in a glove compartment.",
            },
        ],
        "knowledge_pack": {
            "id": "kp-car-vacuum-v01",
            "version": "v0.1",
            "title": "Car vacuum cleaner content knowledge pack v0.1",
        },
        "manual_references": [
            make_reference("ref-1"),
            make_reference("ref-2"),
            make_reference("ref-3"),
        ],
        "creative_concept_drafts": [
            make_concept("concept-mess-rescue-crumb-disaster", selected=False),
            make_concept("concept-hidden-dirt-proof", selected=False),
            make_concept("concept-daily-car-reset", selected=False),
        ],
        "selected_concept": make_concept("concept-mess-rescue-crumb-disaster", selected=True),
        "script_pack": {
            "id": "script-pack-001",
            "project_id": "cp-car-vacuum-001",
            "product_version_id": "pv-car-vacuum-sample-a",
            "concept_id": "concept-mess-rescue-crumb-disaster",
            "status": "draft",
            "evidence_refs": ["ev-supplier-claim-001", "ev-owner-observation-001"],
            "manual_reference_refs": ["ref-1", "ref-2", "ref-3"],
            "knowledge_pack_id": "kp-car-vacuum-v01",
            "knowledge_pack_version": "v0.1",
        },
        "review_decision": {
            "project_id": "cp-car-vacuum-001",
            "script_pack_id": "script-pack-001",
            "decision": "approved",
            "reviewer_note": "Approved for generation-ready production handoff.",
        },
        "production_pack_export": {
            "format": "markdown_and_json",
            "project_id": "cp-car-vacuum-001",
            "product_version_id": "pv-car-vacuum-sample-a",
            "production_readiness": "generation_ready",
            "markdown": "# Generation-ready Owned Content Production Pack\n",
            "json": {
                "project_id": "cp-car-vacuum-001",
                "product_version_id": "pv-car-vacuum-sample-a",
                "production_readiness": "generation_ready",
            },
        },
        "trace_summary": {
            "project_id": "cp-car-vacuum-001",
            "product_version_id": "pv-car-vacuum-sample-a",
            "evidence_refs": ["ev-supplier-claim-001", "ev-owner-observation-001"],
            "manual_reference_refs": ["ref-1", "ref-2", "ref-3"],
            "knowledge_pack_version": "v0.1",
            "script_pack_id": "script-pack-001",
        },
    }


def make_reference(reference_id: str) -> dict:
    return {
        "id": reference_id,
        "project_id": "cp-car-vacuum-001",
        "product_version_id": "pv-car-vacuum-sample-a",
        "title": f"Manual reference {reference_id}",
        "source_identifier": f"https://example.com/{reference_id}",
        "source_type": "TikTok manual URL",
        "summary": "Manual source showing a car cleanup pattern.",
        "intake_method": "manual",
    }


def make_concept(concept_id: str, *, selected: bool) -> dict:
    return {
        "id": concept_id,
        "project_id": "cp-car-vacuum-001",
        "product_version_id": "pv-car-vacuum-sample-a",
        "angle": "Mess Rescue / Crumb Disaster",
        "title": "Mess Rescue / Crumb Disaster",
        "hook": "Crumbs everywhere after one commute?",
        "rationale": "Show relatable car mess and quick cleanup.",
        "status": "draft",
        "selected": selected,
        "evidence_refs": ["ev-supplier-claim-001", "ev-owner-observation-001"],
        "manual_reference_refs": ["ref-1", "ref-2", "ref-3"],
        "knowledge_pack_id": "kp-car-vacuum-v01",
        "knowledge_pack_version": "v0.1",
    }


def test_save_writes_a_json_file(tmp_path) -> None:
    path = save_workspace_snapshot(make_snapshot(), base_dir=tmp_path)

    assert path.exists()
    assert json.loads(path.read_text(encoding="utf-8"))["project_id"] == "cp-car-vacuum-001"


def test_save_uses_expected_project_id_filename(tmp_path) -> None:
    path = save_workspace_snapshot(make_snapshot(), base_dir=tmp_path)

    assert path.name == "cp-car-vacuum-001.json"


def test_list_returns_saved_project_summary(tmp_path) -> None:
    save_workspace_snapshot(make_snapshot(), base_dir=tmp_path)

    summaries = list_workspace_snapshots(base_dir=tmp_path)

    assert len(summaries) == 1
    assert summaries[0].project_id == "cp-car-vacuum-001"
    assert summaries[0].product_version_id == "pv-car-vacuum-sample-a"
    assert summaries[0].status == "reviewed"


def test_load_returns_the_saved_snapshot(tmp_path) -> None:
    save_workspace_snapshot(make_snapshot(), base_dir=tmp_path)

    snapshot = load_workspace_snapshot("cp-car-vacuum-001", base_dir=tmp_path)

    assert snapshot.project_id == "cp-car-vacuum-001"
    assert snapshot.product_version_id == "pv-car-vacuum-sample-a"


def test_save_rejects_missing_workspace_schema_version(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot.pop("workspace_schema_version")

    with pytest.raises(WorkspaceSnapshotValidationError, match="workspace_schema_version is required"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_unsupported_workspace_schema_version(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["workspace_schema_version"] = "a1.workspace_snapshot.v0"

    with pytest.raises(WorkspaceSnapshotValidationError, match="workspace_schema_version must match"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_mismatched_content_project_product_version_id(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["content_project"]["product_version_id"] = "pv-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ContentProject.product_version_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_evidence_bound_to_wrong_product_version(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["evidence"][0]["product_version_id"] = "pv-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="Evidence.product_version_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_manual_reference_bound_to_wrong_project(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["manual_references"][0]["project_id"] = "cp-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ManualReference.project_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_manual_reference_bound_to_wrong_product_version(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["manual_references"][0]["product_version_id"] = "pv-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ManualReference.product_version_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_manual_reference_intake_method_not_manual(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["manual_references"][0]["intake_method"] = "search"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ManualReference.intake_method"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_manual_reference_count_outside_3_to_5(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["manual_references"] = snapshot["manual_references"][:2]

    with pytest.raises(WorkspaceSnapshotValidationError, match="ManualReference count"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_selected_concept_not_draft(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["selected_concept"]["status"] = "approved"

    with pytest.raises(WorkspaceSnapshotValidationError, match="selected concept status"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_selected_concept_project_id_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["selected_concept"]["project_id"] = "cp-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="selected concept project_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_selected_concept_product_version_id_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["selected_concept"]["product_version_id"] = "pv-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="selected concept product_version_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_selected_concept_evidence_refs_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["selected_concept"]["evidence_refs"] = ["ev-supplier-claim-001"]

    with pytest.raises(WorkspaceSnapshotValidationError, match="selected concept evidence_refs"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_selected_concept_manual_reference_refs_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["selected_concept"]["manual_reference_refs"] = ["ref-1", "ref-2", "ref-other"]

    with pytest.raises(WorkspaceSnapshotValidationError, match="selected concept manual_reference_refs"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_selected_concept_knowledge_pack_id_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["selected_concept"]["knowledge_pack_id"] = "kp-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="selected concept knowledge_pack_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_selected_concept_knowledge_pack_version_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["selected_concept"]["knowledge_pack_version"] = "v0.2"

    with pytest.raises(WorkspaceSnapshotValidationError, match="selected concept knowledge_pack_version"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_script_pack_not_draft(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["script_pack"]["status"] = "approved"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ScriptPackDraft.status"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_script_pack_project_id_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["script_pack"]["project_id"] = "cp-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ScriptPackDraft.project_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_script_pack_product_version_id_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["script_pack"]["product_version_id"] = "pv-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ScriptPackDraft.product_version_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_script_pack_concept_id_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["script_pack"]["concept_id"] = "concept-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ScriptPackDraft.concept_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_script_pack_evidence_refs_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["script_pack"]["evidence_refs"] = ["ev-supplier-claim-001"]

    with pytest.raises(WorkspaceSnapshotValidationError, match="ScriptPackDraft.evidence_refs"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_script_pack_manual_reference_refs_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["script_pack"]["manual_reference_refs"] = ["ref-1", "ref-2", "ref-other"]

    with pytest.raises(WorkspaceSnapshotValidationError, match="ScriptPackDraft.manual_reference_refs"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_script_pack_knowledge_pack_id_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["script_pack"]["knowledge_pack_id"] = "kp-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ScriptPackDraft.knowledge_pack_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_script_pack_knowledge_pack_version_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["script_pack"]["knowledge_pack_version"] = "v0.2"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ScriptPackDraft.knowledge_pack_version"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_review_decision_script_pack_id_mismatch(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["review_decision"]["script_pack_id"] = "script-pack-other"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ReviewDecision.script_pack_id"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_invalid_review_decision(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["review_decision"]["decision"] = "draft"

    with pytest.raises(WorkspaceSnapshotValidationError, match="ReviewDecision.decision"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_save_rejects_approved_review_with_not_generation_ready(tmp_path) -> None:
    snapshot = make_snapshot()
    snapshot["production_pack_export"]["production_readiness"] = "not_generation_ready"

    with pytest.raises(WorkspaceSnapshotValidationError, match="approved review must map"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


@pytest.mark.parametrize("decision", ["rework", "hold", "stopped"])
def test_save_rejects_non_approved_review_with_generation_ready(tmp_path, decision) -> None:
    snapshot = make_snapshot()
    snapshot["review_decision"]["decision"] = decision

    with pytest.raises(WorkspaceSnapshotValidationError, match="not_generation_ready"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_load_rejects_corrupted_or_inconsistent_snapshot(tmp_path) -> None:
    path = tmp_path / "cp-car-vacuum-001.json"
    snapshot = make_snapshot()
    snapshot["production_pack_export"]["product_version_id"] = "pv-other"
    path.write_text(json.dumps(snapshot), encoding="utf-8")

    with pytest.raises(WorkspaceSnapshotValidationError, match="ProductionPackExport.product_version_id"):
        load_workspace_snapshot("cp-car-vacuum-001", base_dir=tmp_path)


def test_load_rejects_invalid_json(tmp_path) -> None:
    path = tmp_path / "cp-car-vacuum-001.json"
    path.write_text("{not-json", encoding="utf-8")

    with pytest.raises(WorkspaceSnapshotValidationError, match="not valid JSON"):
        load_workspace_snapshot("cp-car-vacuum-001", base_dir=tmp_path)


def test_save_load_preserves_production_pack_export_markdown_and_json_payload(tmp_path) -> None:
    snapshot = make_snapshot()

    save_workspace_snapshot(snapshot, base_dir=tmp_path)
    loaded = load_workspace_snapshot("cp-car-vacuum-001", base_dir=tmp_path)

    assert loaded.production_pack_export["markdown"] == "# Generation-ready Owned Content Production Pack\n"
    assert loaded.production_pack_export["json"]["production_readiness"] == "generation_ready"


def test_store_itself_writes_no_secret_env_or_api_key_fields(tmp_path) -> None:
    path = save_workspace_snapshot(make_snapshot(), base_dir=tmp_path)
    saved = json.loads(path.read_text(encoding="utf-8"))

    serialized_keys = set()

    def collect_keys(value):
        if isinstance(value, dict):
            for key, item in value.items():
                serialized_keys.add(str(key).lower())
                collect_keys(item)
        elif isinstance(value, list):
            for item in value:
                collect_keys(item)

    collect_keys(saved)

    assert "api_key" not in serialized_keys
    assert "secret" not in serialized_keys
    assert "token" not in serialized_keys
    assert "password" not in serialized_keys
    assert ".env" not in serialized_keys


def test_save_rejects_secret_like_snapshot_fields(tmp_path) -> None:
    snapshot = deepcopy(make_snapshot())
    snapshot["production_pack_export"]["api_key"] = "not-allowed"

    with pytest.raises(WorkspaceSnapshotValidationError, match="forbidden secret-like field"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


@pytest.mark.parametrize("secret_key", ["openai_api_key", "access_token"])
def test_save_rejects_nested_secret_like_snapshot_fields(tmp_path, secret_key) -> None:
    snapshot = deepcopy(make_snapshot())
    snapshot["trace_summary"]["debug"] = {secret_key: "not-allowed"}

    with pytest.raises(WorkspaceSnapshotValidationError, match="forbidden secret-like field"):
        save_workspace_snapshot(snapshot, base_dir=tmp_path)


def test_list_skips_invalid_snapshots(tmp_path) -> None:
    save_workspace_snapshot(make_snapshot(), base_dir=tmp_path)
    invalid_snapshot = make_snapshot()
    invalid_snapshot["project_id"] = "cp-invalid"
    invalid_snapshot["content_project"]["id"] = "cp-invalid"
    invalid_snapshot["selected_concept"]["status"] = "approved"
    (tmp_path / "cp-invalid.json").write_text(json.dumps(invalid_snapshot), encoding="utf-8")

    summaries = list_workspace_snapshots(base_dir=tmp_path)

    assert [summary.project_id for summary in summaries] == ["cp-car-vacuum-001"]
