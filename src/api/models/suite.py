from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .helper import _get


@dataclass(frozen=True)
class SuiteAttributes:
    """Subset of suite attributes returned by Testomat API.

    Only commonly used fields are mapped; the rest are available via `raw`.
    """

    # arrays
    labels: list[str] | None = None
    tags: list[str] | None = None

    # miscellaneous
    issues: Any | None = None
    jira_issues: Any | None = None
    is_branched: bool | None = None
    is_detail: bool | None = None
    attachments: Any | None = None
    is_linked: bool | None = None
    is_shared: bool | None = None

    # identity / presentation
    title: str | None = None
    emoji: Any | None = None
    sync: bool | None = None
    file_type: str | None = None

    # counts / refs
    test_count: int | None = None
    filtered_tests: Any | None = None

    # file/meta
    file: Any | None = None
    notes: Any | None = None
    created_at: str | None = None
    updated_at: str | None = None
    assigned_to: Any | None = None
    to_url: str | None = None
    comments_count: int | None = None
    position: int | None = None
    depth: int | None = None
    is_root: bool | None = None
    public_title: str | None = None
    parent_id: Any | None = None
    path: Any | None = None

    # keep the whole original dict for forward-compatibility
    raw: dict[str, Any] | None = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SuiteAttributes:
        return SuiteAttributes(
            labels=_get(data, "labels"),
            tags=_get(data, "tags"),
            issues=_get(data, "issues"),
            jira_issues=_get(data, "jira-issues"),
            is_branched=_get(data, "is-branched"),
            is_detail=_get(data, "is-detail"),
            attachments=_get(data, "attachments"),
            is_linked=_get(data, "is-linked"),
            is_shared=_get(data, "is-shared"),
            title=_get(data, "title"),
            emoji=_get(data, "emoji"),
            sync=_get(data, "sync"),
            file_type=_get(data, "file-type"),
            test_count=_get(data, "test-count"),
            filtered_tests=_get(data, "filtered-tests"),
            file=_get(data, "file"),
            notes=_get(data, "notes"),
            created_at=_get(data, "created-at"),
            updated_at=_get(data, "updated-at"),
            assigned_to=_get(data, "assigned-to"),
            to_url=_get(data, "to-url"),
            comments_count=_get(data, "comments-count"),
            position=_get(data, "position"),
            depth=_get(data, "depth"),
            is_root=_get(data, "is-root"),
            public_title=_get(data, "public-title"),
            parent_id=_get(data, "parent-id"),
            path=_get(data, "path"),
            raw=data,
        )


@dataclass(frozen=True)
class Suite:
    """Single suite item inside response `data` list."""

    id: str
    type: str
    attributes: SuiteAttributes
    relationships: dict[str, Any] | None = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Suite:
        attrs_raw = _get(data, "attributes") or {}
        attrs = (
            SuiteAttributes.from_dict(attrs_raw)
            if isinstance(attrs_raw, dict)
            else SuiteAttributes()
        )
        relationships = _get(data, "relationships") if isinstance(data, dict) else None
        return Suite(
            id=str(_get(data, "id")),
            type=str(_get(data, "type")),
            attributes=attrs,
            relationships=relationships if isinstance(relationships, dict) else None,
        )
