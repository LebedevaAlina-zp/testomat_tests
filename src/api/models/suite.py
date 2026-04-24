from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SuiteAttributes(BaseModel):
    """Pydantic version of suite attributes returned by Testomat API."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    # identity / presentation
    suite_id: str | None = Field(default=None, alias="suite-id")
    title: str | None = None
    description: str | None = None
    emoji: Any | None = None
    sync: bool | None = None
    file_type: str | None = Field(default=None, alias="file-type")

    # arrays
    labels: list[str] | None = None
    tags: list[str] | None = None
    tests: list[str] | None = None
    children: list[str] | None = None

    # miscellaneous
    issues: Any | None = None
    jira_issues: Any | None = Field(default=None, alias="jira-issues")
    is_branched: bool | None = Field(default=None, alias="is-branched")
    is_detail: bool | None = Field(default=None, alias="is-detail")
    attachments: Any | None = None
    is_linked: bool | None = Field(default=None, alias="is-linked")
    is_shared: bool | None = Field(default=None, alias="is-shared")

    # counts / refs
    test_count: float | None = Field(default=None, alias="test-count")
    filtered_tests: Any | None = Field(default=None, alias="filtered-tests")
    comments_count: float | None = Field(default=None, alias="comments-count")

    # file/meta
    code: str | None = None
    file: str | None = None
    fullpath: str | None = None
    notes: Any | None = None
    created_at: str | None = Field(default=None, alias="created-at")
    updated_at: str | None = Field(default=None, alias="updated-at")
    assigned_to: Any | None = Field(default=None, alias="assigned-to")
    to_url: str | None = Field(default=None, alias="to-url")
    position: int | None = None
    depth: int | None = None
    is_root: bool | None = Field(default=None, alias="is-root")
    public_title: str | None = Field(default=None, alias="public-title")
    parent_id: Any | None = Field(default=None, alias="parent-id")
    path: Any | None = None

    # keep the whole original dict for forward-compatibility
    raw: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SuiteAttributes:
        payload = {**(data or {}), "raw": data}
        return cls.model_validate(payload)


class Suite(BaseModel):
    """Single suite item inside response `data` list."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: str
    attributes: SuiteAttributes = Field(default_factory=SuiteAttributes)
    relationships: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Suite:
        data = data or {}
        attrs_raw = data.get("attributes")
        if isinstance(attrs_raw, dict):
            attrs = SuiteAttributes.from_dict(attrs_raw)
        else:
            attrs = SuiteAttributes()
        payload = {**data, "attributes": attrs}
        return cls.model_validate(payload)


class SuitesMeta(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total_pages: int | None = None
    per_page: int | None = None
    num: int | None = None
    page: int | None = None
    r_id: Any | None = Field(default=None, alias="rId")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SuitesMeta:
        return cls.model_validate(data or {})


class SuitesResponse(BaseModel):
    """Response for GET /api/{project_id}/suites."""

    model_config = ConfigDict(populate_by_name=True)

    data: list[Suite] = Field(default_factory=list)
    meta: SuitesMeta | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SuitesResponse:
        items = (data or {}).get("data")
        suites: list[Suite] = []
        if isinstance(items, list):
            suites = [Suite.from_dict(x) for x in items if isinstance(x, dict)]

        meta_raw = (data or {}).get("meta")
        meta = SuitesMeta.from_dict(meta_raw) if isinstance(meta_raw, dict) else None

        return cls.model_validate({"data": suites, "meta": meta})

    @classmethod
    def from_json(
        cls,
        payload: Any,
    ) -> list[SuitesResponse] | SuitesResponse:
        """Parse JSON payload into models (list or single object)."""
        if isinstance(payload, list):
            return [cls.from_dict(x) for x in payload if isinstance(x, dict)]
        if isinstance(payload, dict):
            return cls.from_dict(payload)
        return cls.model_validate({"data": []})


__all__ = [
    "SuiteAttributes",
    "Suite",
    "SuitesMeta",
    "SuitesResponse",
]
