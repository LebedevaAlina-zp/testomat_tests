from __future__ import annotations

from src.api.models import ProjectsResponse


def test_login_sets_authorization_header(api_client):
    """Ensure JWT login occurred by checking Authorization header is present."""
    auth_header = api_client._session.headers.get("Authorization")  # noqa: SLF001 (access for test only)
    assert isinstance(auth_header, str) and auth_header.strip()


def test_get_projects_response_has_correct_type(api_client):
    """Fixture `projects` should always yield a list (possibly empty)."""
    projects = api_client.get_projects()
    assert isinstance(projects, ProjectsResponse)
