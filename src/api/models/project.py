from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _get(d: dict[str, Any], key: str, default: Any = None) -> Any:
    """Helper to safely get keys that may contain hyphens in JSON."""
    if key in d:
        return d[key]
    # try common conversions between snake_case and kebab-case
    kebab = key.replace("_", "-")
    snake = key.replace("-", "_")
    if kebab in d:
        return d[kebab]
    if snake in d:
        return d[snake]
    return default


@dataclass(frozen=True)
class ProjectAttributes:
    """Subset of project attributes returned by Testomat API.

    Only commonly used fields are mapped; the rest are available via `raw`.
    """

    title: str | None = None
    lang: str | None = None
    status: str | None = None
    url: str | None = None
    testomatio_url: str | None = None
    api_key: str | None = None
    created_at: str | None = None
    tests_count: int | None = None
    record_url: str | None = None
    living_doc_url: str | None = None
    whitelist_ip: str | None = None
    versions_max_days: int | None = None
    raw: dict[str, Any] | None = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ProjectAttributes:
        return ProjectAttributes(
            title=_get(data, "title"),
            lang=_get(data, "lang"),
            status=_get(data, "status"),
            url=_get(data, "url"),
            testomatio_url=_get(data, "testomatio-url"),
            api_key=_get(data, "api-key"),
            created_at=_get(data, "created-at"),
            tests_count=_get(data, "tests-count"),
            record_url=_get(data, "record-url"),
            living_doc_url=_get(data, "living-doc-url"),
            whitelist_ip=_get(data, "whitelist-ip"),
            versions_max_days=_get(data, "versions-max-days"),
            raw=data,
        )


@dataclass(frozen=True)
class Project:
    """Single project item inside response `data` list."""

    id: str
    type: str
    attributes: ProjectAttributes

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Project:
        attrs_raw = _get(data, "attributes") or {}
        attrs = ProjectAttributes.from_dict(attrs_raw) if isinstance(attrs_raw, dict) else ProjectAttributes()
        return Project(
            id=str(_get(data, "id")),
            type=str(_get(data, "type")),
            attributes=attrs,
        )
