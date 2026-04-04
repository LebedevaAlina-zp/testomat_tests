from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProjectAttributes(BaseModel):
    """Pydantic version of project attributes returned by Testomat API.

    Only commonly used fields are mapped; the rest are preserved in `raw`.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    title: str | None = None
    lang: str | None = None
    status: str | None = None
    url: str | None = None
    testomatio_url: str | None = Field(default=None, alias="testomatio-url")
    api_key: str | None = Field(default=None, alias="api-key")
    created_at: str | None = Field(default=None, alias="created-at")
    tests_count: int | None = Field(default=None, alias="tests-count")
    record_url: str | None = Field(default=None, alias="record-url")
    living_doc_url: str | None = Field(default=None, alias="living-doc-url")
    whitelist_ip: str | None = Field(default=None, alias="whitelist-ip")
    versions_max_days: int | None = Field(default=None, alias="versions-max-days")
    raw: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectAttributes:
        payload = {**(data or {}), "raw": data}
        return cls.model_validate(payload)


class Project(BaseModel):
    """Single project item inside response `data` list."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: str
    attributes: ProjectAttributes = Field(default_factory=ProjectAttributes)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Project:
        data = data or {}
        attrs_raw = data.get("attributes")
        if isinstance(attrs_raw, dict):
            attrs = ProjectAttributes.from_dict(attrs_raw)
        else:
            attrs = ProjectAttributes()
        payload = {**data, "attributes": attrs}
        return cls.model_validate(payload)


class ProjectsResponse(BaseModel):
    """Response item for GET /api/projects."""

    model_config = ConfigDict(populate_by_name=True)

    data: list[Project] = Field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProjectsResponse:
        items = (data or {}).get("data")
        projects: list[Project] = []
        if isinstance(items, list):
            projects = [Project.from_dict(x) for x in items if isinstance(x, dict)]
        return cls.model_validate({"data": projects})

    @classmethod
    def from_json(cls, payload: Any) -> list[ProjectsResponse] | ProjectsResponse:
        """Parse JSON into models (list or single object)."""
        if isinstance(payload, list):
            return [cls.from_dict(x) for x in payload if isinstance(x, dict)]
        if isinstance(payload, dict):
            return cls.from_dict(payload)
        return cls.model_validate({"data": []})


__all__ = [
    "ProjectAttributes",
    "Project",
    "ProjectsResponse",
]
