from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TestAttributes(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    suite_id: str = Field(..., alias="suite-id", description="Suite Id")
    title: str | None = Field(None, description="Test title")
    description: str | None = Field(None, description="Test description")
    state: str | None = Field(None, description="State of string")
    code: str | None = Field(None, description="Source code of an automated test")
    file: str | None = Field(None, description="File of an automated test")
    sync: bool | None = Field(None, description="Is test sycnhronized")
    to_url: str | None = Field(None, alias="to-url", description="URL of a test")
    tags: Any | None = Field(None, description="List of tags")
    labels: Any | None = Field(None, description="List of labels")
    has_examples: bool | None = Field(
        None, alias="has-examples", description="Is test parametrized?"
    )
    params: list[str] | None = Field(None, description="Parameters of tests")
    run_statuses: list[str] | None = Field(
        None, alias="run-statuses", description="Last run statuses"
    )
    attachments: list[str] | None = Field(None, description="List of attachments or object")
    jira_issues: list[str] | None = Field(
        None, alias="jira-issues", description="List/object of assigned jira issues"
    )
    issues: Any | None = Field(None, description="Linked issues (format may vary)")
    assigned_to: str | None = Field(
        None, alias="assigned-to", description="A user assigned to this test"
    )
    created_by: int | str | None = Field(
        None, alias="created-by", description="A user created test"
    )
    created_at: str | None = Field(
        None, alias="created-at", description="Date of the test creation"
    )
    updated_at: str | None = Field(
        None, alias="updated-at", description="Last time the test was updated"
    )
    emoji: str | None = Field(None, description="Emoji icon associated with the test")
    priority: str | None = Field(None, description="Priority of the test")
    run_at: str | None = Field(None, alias="run-at", description="Last run at time")
    is_branched: bool | None = Field(None, alias="is-branched")
    is_detail: bool | None = Field(None, alias="is-detail")
    is_linked: bool | None = Field(None, alias="is-linked")
    is_shared: bool | None = Field(None, alias="is-shared")
    saved_in_branch: bool | None = Field(None, alias="saved-in-branch?")
    comments_count: int | None = Field(
        None, alias="comments-count", description="Number of comments on the test"
    )
    template_id: int | None = Field(None, alias="template-id")
    public_title: str | None = Field(None, alias="public-title")
    position: int | None = Field(None, description="Position in the suite")
    import_id: int | str | None = Field(None, alias="import-id")
    forks_count: int | None = Field(None, alias="forks-count")

    # keep the whole original dict for forward-compatibility
    raw: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TestAttributes:
        payload = {**(data or {}), "raw": data}
        return cls.model_validate(payload)


class Test(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: str = Field(..., description="Test id")
    type: str = Field(..., description='must be "test"')
    attributes: TestAttributes = Field(default_factory=TestAttributes)
    relationships: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Test:
        data = data or {}
        attrs_raw = data.get("attributes")
        if isinstance(attrs_raw, dict):
            attrs = TestAttributes.from_dict(attrs_raw)
        else:
            attrs = TestAttributes()
        payload = {**data, "attributes": attrs}
        return cls.model_validate(payload)


class TestsMeta(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total_pages: int | None = None
    per_page: int | None = None
    num: int | None = None
    page: int | None = None
    r_id: Any | None = Field(default=None, alias="rId")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TestsMeta:
        return cls.model_validate(data or {})


class TestsResponse(BaseModel):
    """Response item for GET /api/projects."""

    model_config = ConfigDict(populate_by_name=True)

    data: list[Test] = Field(default_factory=list)
    meta: TestsMeta | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TestsResponse:
        items = (data or {}).get("data")
        tests: list[Test] = []
        if isinstance(items, list):
            tests = [Test.from_dict(x) for x in items if isinstance(x, dict)]

        meta_raw = (data or {}).get("meta")
        meta = TestsMeta.from_dict(meta_raw) if isinstance(meta_raw, dict) else None

        return cls.model_validate({"data": tests, "meta": meta})

    @classmethod
    def from_json(
        cls,
        payload: Any,
    ) -> list[TestsResponse] | TestsResponse:
        if isinstance(payload, list):
            return [cls.from_dict(x) for x in payload if isinstance(x, dict)]
        if isinstance(payload, dict):
            return cls.from_dict(payload)
        return cls.model_validate({"data": []})


__all__ = [
    "TestAttributes",
    "Test",
    "TestsResponse",
]
