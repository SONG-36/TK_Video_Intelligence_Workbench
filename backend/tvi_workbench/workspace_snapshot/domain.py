"""Local JSON workspace snapshot boundary.

This package stores one complete WS-0 + WS-1 workspace snapshot as local JSON.
It is not a database, API, workflow engine, or formal frontend persistence
layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


WORKSPACE_SCHEMA_VERSION = "a1.workspace_snapshot.v1"


class WorkspaceSnapshotValidationError(ValueError):
    """Raised when a workspace snapshot is missing required trace data."""


@dataclass(frozen=True)
class WorkspaceSnapshot:
    workspace_schema_version: str
    saved_at: str
    project_id: str
    product_version_id: str
    status: str
    content_project: Mapping[str, Any]
    operating_context: Mapping[str, Any]
    product: Mapping[str, Any]
    product_version: Mapping[str, Any]
    evidence: Sequence[Mapping[str, Any]]
    knowledge_pack: Mapping[str, Any]
    manual_references: Sequence[Mapping[str, Any]]
    creative_concept_drafts: Sequence[Mapping[str, Any]]
    selected_concept: Mapping[str, Any]
    script_pack: Mapping[str, Any]
    review_decision: Mapping[str, Any]
    production_pack_export: Mapping[str, Any]
    trace_summary: Mapping[str, Any]

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "WorkspaceSnapshot":
        return cls(
            workspace_schema_version=data.get("workspace_schema_version"),
            saved_at=data.get("saved_at"),
            project_id=data.get("project_id"),
            product_version_id=data.get("product_version_id"),
            status=data.get("status"),
            content_project=data.get("content_project"),
            operating_context=data.get("operating_context"),
            product=data.get("product"),
            product_version=data.get("product_version"),
            evidence=data.get("evidence"),
            knowledge_pack=data.get("knowledge_pack"),
            manual_references=data.get("manual_references"),
            creative_concept_drafts=data.get("creative_concept_drafts"),
            selected_concept=data.get("selected_concept"),
            script_pack=data.get("script_pack"),
            review_decision=data.get("review_decision"),
            production_pack_export=data.get("production_pack_export"),
            trace_summary=data.get("trace_summary"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace_schema_version": self.workspace_schema_version,
            "saved_at": self.saved_at,
            "project_id": self.project_id,
            "product_version_id": self.product_version_id,
            "status": self.status,
            "content_project": dict(self.content_project),
            "operating_context": dict(self.operating_context),
            "product": dict(self.product),
            "product_version": dict(self.product_version),
            "evidence": [dict(item) for item in self.evidence],
            "knowledge_pack": dict(self.knowledge_pack),
            "manual_references": [dict(item) for item in self.manual_references],
            "creative_concept_drafts": [dict(item) for item in self.creative_concept_drafts],
            "selected_concept": dict(self.selected_concept),
            "script_pack": dict(self.script_pack),
            "review_decision": dict(self.review_decision),
            "production_pack_export": dict(self.production_pack_export),
            "trace_summary": dict(self.trace_summary),
        }


@dataclass(frozen=True)
class WorkspaceSnapshotSummary:
    project_id: str
    product_version_id: str
    status: str
    saved_at: str
    workspace_schema_version: str
    path: Path
