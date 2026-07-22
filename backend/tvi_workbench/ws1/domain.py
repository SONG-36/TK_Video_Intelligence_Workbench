"""WS-1 input boundary objects.

These objects capture only the versioned Knowledge Pack v0.1 and manual
Reference intake needed before concept generation. They are not a knowledge
base platform, reference search system, AI run, or approval workflow.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from tvi_workbench.ws0 import DomainValidationError


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DomainValidationError(f"{field_name} is required")
    return value.strip()


@dataclass(frozen=True)
class KnowledgePack:
    id: str
    version: str
    title: str
    content_summary: str | None = None
    sections: Mapping[str, str] = field(default_factory=dict)
    source_notes: str | None = None
    created_at: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _required_text(self.id, "id"))
        version = _required_text(self.version, "version")
        if version != "v0.1":
            raise DomainValidationError("Knowledge Pack version must be v0.1 for Step 2")
        object.__setattr__(self, "version", version)
        object.__setattr__(self, "title", _required_text(self.title, "title"))

        content_summary = self.content_summary.strip() if isinstance(self.content_summary, str) else ""
        cleaned_sections = {
            _required_text(str(key), "section key"): _required_text(value, "section value")
            for key, value in self.sections.items()
        }
        if not content_summary and not cleaned_sections:
            raise DomainValidationError("Knowledge Pack requires content_summary or sections")
        object.__setattr__(self, "content_summary", content_summary or None)
        object.__setattr__(self, "sections", cleaned_sections)

        if self.source_notes is not None:
            source_notes = self.source_notes.strip()
            object.__setattr__(self, "source_notes", source_notes or None)
        if self.created_at is not None:
            created_at = self.created_at.strip()
            object.__setattr__(self, "created_at", created_at or None)


@dataclass(frozen=True)
class ManualReference:
    id: str
    project_id: str
    product_version_id: str
    title: str
    source_identifier: str
    source_type: str
    summary: str
    observed_pattern: str | None = None
    content_notes: str | None = None
    usage_notes: str | None = None
    intake_method: str = "manual"

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _required_text(self.id, "id"))
        object.__setattr__(self, "project_id", _required_text(self.project_id, "project_id"))
        object.__setattr__(
            self,
            "product_version_id",
            _required_text(self.product_version_id, "product_version_id"),
        )
        object.__setattr__(self, "title", _required_text(self.title, "title"))
        object.__setattr__(self, "source_identifier", _required_text(self.source_identifier, "source_identifier"))
        object.__setattr__(self, "source_type", _required_text(self.source_type, "source_type"))
        object.__setattr__(self, "summary", _required_text(self.summary, "summary"))

        intake_method = _required_text(self.intake_method, "intake_method").lower()
        if intake_method != "manual":
            raise DomainValidationError("Manual Reference intake_method must be manual")
        object.__setattr__(self, "intake_method", intake_method)

        observed_pattern = self.observed_pattern.strip() if isinstance(self.observed_pattern, str) else ""
        content_notes = self.content_notes.strip() if isinstance(self.content_notes, str) else ""
        usage_notes = self.usage_notes.strip() if isinstance(self.usage_notes, str) else ""
        if not (observed_pattern or content_notes or usage_notes):
            raise DomainValidationError(
                "Manual Reference requires observed_pattern, content_notes, or usage_notes"
            )
        object.__setattr__(self, "observed_pattern", observed_pattern or None)
        object.__setattr__(self, "content_notes", content_notes or None)
        object.__setattr__(self, "usage_notes", usage_notes or None)

