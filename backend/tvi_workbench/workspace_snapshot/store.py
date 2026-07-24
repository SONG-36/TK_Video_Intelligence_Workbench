"""Local JSON file store for workspace snapshots."""

from __future__ import annotations

import json
import os
import re
import tempfile
from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .domain import (
    WORKSPACE_SCHEMA_VERSION,
    WorkspaceSnapshot,
    WorkspaceSnapshotSummary,
    WorkspaceSnapshotValidationError,
)


DEFAULT_WORKSPACE_SNAPSHOT_DIR = Path(".local/workspace/projects")
REQUIRED_DOMAIN_SECTIONS = (
    "content_project",
    "operating_context",
    "product",
    "product_version",
    "evidence",
    "knowledge_pack",
    "manual_references",
    "creative_concept_drafts",
    "selected_concept",
    "script_pack",
    "review_decision",
    "production_pack_export",
    "trace_summary",
)
FORBIDDEN_SECRET_KEYS = {
    ".env",
    "api_key",
    "apikey",
    "access_token",
    "auth_token",
    "cookie",
    "credential",
    "credentials",
    "openai_api_key",
    "password",
    "refresh_token",
    "scrape_creators_api_key",
    "secret",
    "secret_key",
    "token",
}
APPROVED_REVIEW_DECISION = "approved"
GENERATION_READY = "generation_ready"
NOT_GENERATION_READY = "not_generation_ready"
VALID_REVIEW_DECISIONS = {
    APPROVED_REVIEW_DECISION,
    "rework",
    "hold",
    "stopped",
}
SAFE_PROJECT_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def save_workspace_snapshot(snapshot: WorkspaceSnapshot | Mapping[str, Any], base_dir: str | Path | None = None) -> Path:
    normalized = _coerce_snapshot(snapshot)
    validate_workspace_snapshot(normalized)
    payload = normalized.to_dict()
    _assert_json_serializable(payload)
    _assert_no_forbidden_secret_keys(payload)

    directory = _snapshot_dir(base_dir)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{normalized.project_id}.json"
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=directory,
            prefix=f".{normalized.project_id}.",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            json.dump(payload, temp_file, ensure_ascii=False, indent=2, sort_keys=True)
            temp_file.write("\n")
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_path = Path(temp_file.name)
        temp_path.replace(target)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
    return target


def list_workspace_snapshots(base_dir: str | Path | None = None) -> list[WorkspaceSnapshotSummary]:
    directory = _snapshot_dir(base_dir)
    if not directory.exists():
        return []

    summaries: list[WorkspaceSnapshotSummary] = []
    for path in sorted(directory.glob("*.json")):
        try:
            data = _read_json_mapping(path)
            validate_workspace_snapshot(data)
            summaries.append(
                WorkspaceSnapshotSummary(
                    project_id=_required_text(data.get("project_id"), "project_id"),
                    product_version_id=_required_text(data.get("product_version_id"), "product_version_id"),
                    status=_required_text(data.get("status"), "status"),
                    saved_at=_required_text(data.get("saved_at"), "saved_at"),
                    workspace_schema_version=_required_text(
                        data.get("workspace_schema_version"),
                        "workspace_schema_version",
                    ),
                    path=path,
                )
            )
        except WorkspaceSnapshotValidationError:
            continue
    return summaries


def load_workspace_snapshot(project_id: str, base_dir: str | Path | None = None) -> WorkspaceSnapshot:
    cleaned_project_id = _validate_project_id(project_id)
    path = _snapshot_dir(base_dir) / f"{cleaned_project_id}.json"
    data = _read_json_mapping(path)
    snapshot = WorkspaceSnapshot.from_mapping(data)
    validate_workspace_snapshot(snapshot)
    _assert_no_forbidden_secret_keys(snapshot.to_dict())
    return snapshot


def validate_workspace_snapshot(snapshot: WorkspaceSnapshot | Mapping[str, Any]) -> None:
    normalized = _coerce_snapshot(snapshot)

    if _required_text(normalized.workspace_schema_version, "workspace_schema_version") != WORKSPACE_SCHEMA_VERSION:
        raise WorkspaceSnapshotValidationError("workspace_schema_version must match current WORKSPACE_SCHEMA_VERSION")
    project_id = _validate_project_id(normalized.project_id)
    product_version_id = _required_text(normalized.product_version_id, "product_version_id")
    _required_text(normalized.saved_at, "saved_at")
    _required_text(normalized.status, "status")

    data = normalized.to_dict()
    for section in REQUIRED_DOMAIN_SECTIONS:
        value = data.get(section)
        if value is None:
            raise WorkspaceSnapshotValidationError(f"{section} is required")
        if isinstance(value, (dict, list)) and not value:
            raise WorkspaceSnapshotValidationError(f"{section} must not be empty")

    content_project = _required_mapping(normalized.content_project, "content_project")
    product_version = _required_mapping(normalized.product_version, "product_version")
    evidence = _required_sequence(normalized.evidence, "evidence")
    knowledge_pack = _required_mapping(normalized.knowledge_pack, "knowledge_pack")
    manual_references = _required_sequence(normalized.manual_references, "manual_references")
    selected_concept = _required_mapping(normalized.selected_concept, "selected_concept")
    script_pack = _required_mapping(normalized.script_pack, "script_pack")
    review_decision = _required_mapping(normalized.review_decision, "review_decision")
    production_pack_export = _required_mapping(
        normalized.production_pack_export,
        "production_pack_export",
    )

    if _required_text(content_project.get("id"), "content_project.id") != project_id:
        raise WorkspaceSnapshotValidationError("ContentProject.id must match project_id")
    if _required_text(content_project.get("product_version_id"), "content_project.product_version_id") != _required_text(
        product_version.get("id"),
        "product_version.id",
    ):
        raise WorkspaceSnapshotValidationError("ContentProject.product_version_id must match ProductVersion.id")
    if _required_text(product_version.get("id"), "product_version.id") != product_version_id:
        raise WorkspaceSnapshotValidationError("ProductVersion.id must match product_version_id")

    evidence_ids: list[str] = []
    for item in evidence:
        item_mapping = _required_mapping(item, "evidence item")
        evidence_ids.append(_required_text(item_mapping.get("id"), "evidence.id"))
        if _required_text(item_mapping.get("product_version_id"), "evidence.product_version_id") != product_version_id:
            raise WorkspaceSnapshotValidationError("Evidence.product_version_id must match ProductVersion.id")

    knowledge_pack_id = _required_text(knowledge_pack.get("id"), "knowledge_pack.id")
    knowledge_pack_version = _required_text(knowledge_pack.get("version"), "knowledge_pack.version")
    if knowledge_pack_version != "v0.1":
        raise WorkspaceSnapshotValidationError("KnowledgePack.version must be v0.1")

    if not 3 <= len(manual_references) <= 5:
        raise WorkspaceSnapshotValidationError("ManualReference count must be 3-5")
    manual_reference_ids: list[str] = []
    for item in manual_references:
        item_mapping = _required_mapping(item, "manual reference item")
        manual_reference_ids.append(_required_text(item_mapping.get("id"), "manual_reference.id"))
        if _required_text(item_mapping.get("project_id"), "manual_reference.project_id") != project_id:
            raise WorkspaceSnapshotValidationError("ManualReference.project_id must match ContentProject.id")
        if _required_text(item_mapping.get("product_version_id"), "manual_reference.product_version_id") != product_version_id:
            raise WorkspaceSnapshotValidationError("ManualReference.product_version_id must match ProductVersion.id")
        if _required_text(item_mapping.get("intake_method"), "manual_reference.intake_method") != "manual":
            raise WorkspaceSnapshotValidationError("ManualReference.intake_method must be manual")

    selected_concept_id = _required_text(selected_concept.get("id"), "selected_concept.id")
    if _required_text(selected_concept.get("project_id"), "selected_concept.project_id") != project_id:
        raise WorkspaceSnapshotValidationError("selected concept project_id must match project_id")
    if _required_text(selected_concept.get("product_version_id"), "selected_concept.product_version_id") != product_version_id:
        raise WorkspaceSnapshotValidationError("selected concept product_version_id must match product_version_id")
    if _required_text(selected_concept.get("status"), "selected_concept.status") != "draft":
        raise WorkspaceSnapshotValidationError("selected concept status must remain draft")
    if _required_text_sequence(selected_concept.get("evidence_refs"), "selected_concept.evidence_refs") != evidence_ids:
        raise WorkspaceSnapshotValidationError("selected concept evidence_refs must match saved Evidence ids")
    if _required_text_sequence(
        selected_concept.get("manual_reference_refs"),
        "selected_concept.manual_reference_refs",
    ) != manual_reference_ids:
        raise WorkspaceSnapshotValidationError("selected concept manual_reference_refs must match saved ManualReference ids")
    if _required_text(selected_concept.get("knowledge_pack_id"), "selected_concept.knowledge_pack_id") != knowledge_pack_id:
        raise WorkspaceSnapshotValidationError("selected concept knowledge_pack_id must match KnowledgePack.id")
    if _required_text(
        selected_concept.get("knowledge_pack_version"),
        "selected_concept.knowledge_pack_version",
    ) != knowledge_pack_version:
        raise WorkspaceSnapshotValidationError("selected concept knowledge_pack_version must match KnowledgePack.version")

    script_pack_id = _required_text(script_pack.get("id"), "script_pack.id")
    if _required_text(script_pack.get("project_id"), "script_pack.project_id") != project_id:
        raise WorkspaceSnapshotValidationError("ScriptPackDraft.project_id must match project_id")
    if _required_text(script_pack.get("product_version_id"), "script_pack.product_version_id") != product_version_id:
        raise WorkspaceSnapshotValidationError("ScriptPackDraft.product_version_id must match product_version_id")
    if _required_text(script_pack.get("status"), "script_pack.status") != "draft":
        raise WorkspaceSnapshotValidationError("ScriptPackDraft.status must remain draft")
    if _required_text(script_pack.get("concept_id"), "script_pack.concept_id") != selected_concept_id:
        raise WorkspaceSnapshotValidationError("ScriptPackDraft.concept_id must match selected concept id")
    if _required_text_sequence(script_pack.get("evidence_refs"), "script_pack.evidence_refs") != evidence_ids:
        raise WorkspaceSnapshotValidationError("ScriptPackDraft.evidence_refs must match saved Evidence ids")
    if _required_text_sequence(script_pack.get("manual_reference_refs"), "script_pack.manual_reference_refs") != manual_reference_ids:
        raise WorkspaceSnapshotValidationError("ScriptPackDraft.manual_reference_refs must match saved ManualReference ids")
    if _required_text(script_pack.get("knowledge_pack_id"), "script_pack.knowledge_pack_id") != knowledge_pack_id:
        raise WorkspaceSnapshotValidationError("ScriptPackDraft.knowledge_pack_id must match KnowledgePack.id")
    if _required_text(script_pack.get("knowledge_pack_version"), "script_pack.knowledge_pack_version") != knowledge_pack_version:
        raise WorkspaceSnapshotValidationError("ScriptPackDraft.knowledge_pack_version must match KnowledgePack.version")

    review_decision_value = _required_text(review_decision.get("decision"), "review_decision.decision")
    if review_decision_value not in VALID_REVIEW_DECISIONS:
        raise WorkspaceSnapshotValidationError("ReviewDecision.decision must be approved, rework, hold, or stopped")
    if "project_id" in review_decision and _required_text(review_decision.get("project_id"), "review_decision.project_id") != project_id:
        raise WorkspaceSnapshotValidationError("ReviewDecision.project_id must match project_id")
    if _required_text(review_decision.get("script_pack_id"), "review_decision.script_pack_id") != script_pack_id:
        raise WorkspaceSnapshotValidationError("ReviewDecision.script_pack_id must match ScriptPackDraft.id")

    if _required_text(production_pack_export.get("project_id"), "production_pack_export.project_id") != project_id:
        raise WorkspaceSnapshotValidationError("ProductionPackExport.project_id must match project_id")
    if _required_text(
        production_pack_export.get("product_version_id"),
        "production_pack_export.product_version_id",
    ) != product_version_id:
        raise WorkspaceSnapshotValidationError("ProductionPackExport.product_version_id must match product_version_id")
    production_readiness = _required_text(
        production_pack_export.get("production_readiness"),
        "production_pack_export.production_readiness",
    )
    if review_decision_value == APPROVED_REVIEW_DECISION and production_readiness != GENERATION_READY:
        raise WorkspaceSnapshotValidationError("approved review must map to generation_ready")
    if review_decision_value != APPROVED_REVIEW_DECISION and production_readiness != NOT_GENERATION_READY:
        raise WorkspaceSnapshotValidationError("rework, hold, and stopped reviews must map to not_generation_ready")


def _snapshot_dir(base_dir: str | Path | None) -> Path:
    return Path(base_dir) if base_dir is not None else DEFAULT_WORKSPACE_SNAPSHOT_DIR


def _coerce_snapshot(snapshot: WorkspaceSnapshot | Mapping[str, Any]) -> WorkspaceSnapshot:
    if isinstance(snapshot, WorkspaceSnapshot):
        return snapshot
    if isinstance(snapshot, Mapping):
        return WorkspaceSnapshot.from_mapping(snapshot)
    raise WorkspaceSnapshotValidationError("snapshot must be a WorkspaceSnapshot or mapping")


def _read_json_mapping(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise WorkspaceSnapshotValidationError(f"workspace snapshot not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceSnapshotValidationError(f"workspace snapshot is not valid JSON: {path}") from exc
    if not isinstance(data, dict):
        raise WorkspaceSnapshotValidationError("workspace snapshot JSON must be an object")
    return data


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceSnapshotValidationError(f"{field_name} is required")
    return value.strip()


def _required_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise WorkspaceSnapshotValidationError(f"{field_name} must be a non-empty object")
    return value


def _required_sequence(value: Any, field_name: str) -> list[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, list | tuple) or not value:
        raise WorkspaceSnapshotValidationError(f"{field_name} must be a non-empty list")
    return list(value)


def _required_text_sequence(value: Any, field_name: str) -> list[str]:
    return [_required_text(item, field_name) for item in _required_sequence(value, field_name)]


def _validate_project_id(project_id: Any) -> str:
    cleaned = _required_text(project_id, "project_id")
    if not SAFE_PROJECT_ID_RE.match(cleaned):
        raise WorkspaceSnapshotValidationError("project_id must be safe for a local JSON filename")
    return cleaned


def _assert_json_serializable(payload: Mapping[str, Any]) -> None:
    try:
        json.dumps(payload, ensure_ascii=False)
    except TypeError as exc:
        raise WorkspaceSnapshotValidationError("workspace snapshot must be JSON-serializable") from exc


def _assert_no_forbidden_secret_keys(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized_key = str(key).lower()
            if any(forbidden_key in normalized_key for forbidden_key in FORBIDDEN_SECRET_KEYS):
                raise WorkspaceSnapshotValidationError(f"forbidden secret-like field is not allowed: {key}")
            _assert_no_forbidden_secret_keys(item)
    elif isinstance(value, list | tuple):
        for item in value:
            _assert_no_forbidden_secret_keys(item)


def jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return jsonable(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [jsonable(item) for item in value]
    return value
