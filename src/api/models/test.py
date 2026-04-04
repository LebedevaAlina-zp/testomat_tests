class TestAttributes(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    suite_id: str = Field(..., alias="suite-id", description="Suite Id")
    title: str | None = Field(None, description="Test title")
    descriprion: str | None = Field(None, description="Test description")
    state: str | None = Field(None, description="State of string")
    code: str | None = Field(None, description="Source code of an automated test")
    file: str | None = Field(None, description="File of an automated test")
    sync: bool | None = Field(None, description="Is test sycnhronized")
    to_url: str | None = Field(None, description="URL of a test")
    tags: list[str] | None = Field(None, description="List of tags")
    has_examples: bool | None = Field(
        None, alias="has-examples", description="Is test parametrized?"
    )
    params: list[str] | None = Field(None, description="Parameters of tests")
    run_statuses: list[str] | None = Field(
        None, alias="run-statuses", description="Last run statuses"
    )
    attachments: list[str] | None = Field(None, description="List of attachments")
    jira_issues: list[str] | None = Field(
        None, alias="jira-issues", description="List of assigned jira issues"
    )
    assigned_to: str | None = Field(
        None, alias="assigned-to", description="A user assigned to this test"
    )
    created_by: str | None = Field(
        None, alias="created-by", description="A user created test"
    )
    created_at: str | None = Field(
        None, alias="created-at", description="Date of the test creation"
    )
    updated_at: str | None = Field(
        None, alias="updated-at", description="Last time the test was updated"
    )
    comments_count: float | None = Field(
        None, description="Number of comments on the test"
    )


class Test(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: str = Field(..., description="Test id")
    type: str = Field(..., description='must be "test"')
    attributes: TestAttributes | None = None
