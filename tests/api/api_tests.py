from __future__ import annotations

import random

import pytest

from src.api.models import ProjectsResponse, SuitesResponse


@pytest.mark.smoke
@pytest.mark.api
def test_login_sets_authorization_header(api_client):
    """Ensure JWT login occurred by checking Authorization header is present."""
    auth_header = api_client._session.headers.get("Authorization")
    assert isinstance(auth_header, str) and auth_header.strip()


@pytest.mark.smoke
@pytest.mark.api
def test_get_projects_response_has_correct_type(api_client):
    """Get projects should return a ProjectsResponse."""
    projects = api_client.get_projects()
    assert isinstance(projects, ProjectsResponse)


@pytest.mark.smoke
@pytest.mark.api
def test_get_suites_response_has_correct_type(api_client):
    """Get suites should return a SuitesResponse.

    Check for 3 random projects to ensure checking not empty suites list"""
    projects = api_client.get_projects()
    for _ in range(3):
        project = projects.data[random.randint(0, len(projects.data) - 1)]
        suites = api_client.get_suites_for_project_id(project.id)
        assert isinstance(suites, SuitesResponse)
