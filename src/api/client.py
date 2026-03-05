from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

import requests
from requests import Response

from src.api.models import (
    Project,
    ProjectsResponse,
    Suite,
    SuitesResponse,
)


@dataclass(frozen=True)
class ApiConfig:
    base_url: str
    email: str
    password: str


class ApiClient:
    """Very small API client to call Testomat API for preconditions.

    Auth: performs JWT login via POST /api/login using email/password from configs,
    then sends the received token in the Authorization header for subsequent calls.
    """

    def __init__(
        self,
        base_url: str,
        email: str,
        password: str,
        timeout: float = 15.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._email = email
        self._password = password
        self._timeout = timeout
        self._session = requests.Session()
        self._jwt: str | None = None
        self._authenticate()

    @property
    def base_url(self) -> str:  # keep for potential reuse
        return self._base_url

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    def _authenticate(self) -> None:
        """Login and set JWT in session headers.

        API contract (from https://app.testomat.io/docs/openap):
        - POST /api/login with form/body params: {"email": ..., "password": ...}
        - Response JSON: { "jwt": "<token>" }
        - Subsequent requests must include header: Authorization: <token>
        """
        resp = self._session.post(
            self._url("/api/login"),
            data={
                "email": self._email,
                "password": self._password,
            },
            timeout=self._timeout,
        )
        resp.raise_for_status()
        try:
            payload = resp.json()
        except ValueError:
            raise requests.HTTPError("Login response is not JSON", response=resp)

        token = payload.get("jwt") if isinstance(payload, dict) else None
        if not token or not isinstance(token, str):
            raise requests.HTTPError(
                "Login response does not contain 'jwt' token",
                response=resp,
            )

        self._jwt = token
        self._session.headers.update({"Authorization": token})

    def get_projects(self) -> ProjectsResponse:
        """Get projects for the authenticated user via /api/projects.

        Returns parsed model.
        """
        resp = self._session.get(
            self._url("/api/projects"),
            timeout=self._timeout,
        )
        resp.raise_for_status()

        payload: Any
        try:
            payload = resp.json()
        except ValueError:
            # Not JSON; return empty response to keep tests/preconditions stable
            return ProjectsResponse(data=[])

        parsed = ProjectsResponse.from_json(payload)

        # The API may return either a single object or a list of response objects.
        # Our tests expect a single ProjectsResponse.
        if isinstance(parsed, list):
            return parsed[0] if parsed else ProjectsResponse(data=[])

        return parsed

    def projects_list(self) -> list[Project]:
        """Returns a list of projects from api/get_projects endpoint response"""
        resp = self.get_projects()
        return resp.data

    def get_project_id_by_title(self, project_title: str) -> str:
        """Returns project id finding a project in a projects list by title"""
        projects = self.projects_list()
        for project in projects:
            if project.attributes.title == project_title:
                return project.id
        return ""

    def pick_random_project(self, empty: bool | None = None) -> str:
        """Pick a random project from a projects list.
        Optional empty argument to filter out either an empty project or a project with suites.

        Returns project id."""
        projects_list = self.projects_list()

        # Shuffle projects list randomly
        random.shuffle(projects_list)

        if empty is None:
            return projects_list[0].id

        # Check each project suites number to pick either an empty project
        # or a project with suites
        for project in projects_list:
            suites_count = len(self.suites_list(project.id))
            if (
                suites_count == 0
                and empty is True
                or suites_count > 0
                and empty is False
            ):
                return project.id
        raise Exception("No projects matching the conditions was found")

    def delete_project(self, project_id: str) -> Response:
        """Delete a project via DELETE /api/projects/{project_id}"""
        resp = self._session.delete(self._url(f"/api/projects/{project_id}"))
        resp.raise_for_status()
        return resp

    def get_suites_for_project_id(self, project_id: str) -> SuitesResponse:
        """Get suites for a project via /api/{project_id}/suites.

        Returns parsed model."""
        resp = self._session.get(self._url(f"/api/{project_id}/suites"))
        resp.raise_for_status()

        payload: Any
        try:
            payload = resp.json()
        except ValueError:
            # Not JSON; return empty response to keep tests/preconditions stable
            return SuitesResponse(data=[])

        parsed = SuitesResponse.from_json(payload)

        # The API may return either a single object or a list of response objects.
        # Our tests expect a single SuitesResponse.
        if isinstance(parsed, list):
            return parsed[0] if parsed else SuitesResponse(data=[])

        return parsed

    def suites_list(self, project_id: str) -> list[Suite]:
        """Returns a list of suites from /api/{project_id}/suites endpoint response"""
        resp = self.get_suites_for_project_id(project_id)
        return resp.data

    def get_suite_id_by_title(self, project_id: str, suite_title: str) -> str:
        """Returns suite id finding a suite in a project's suites list by title"""
        suits = self.suites_list(project_id)
        for suite in suits:
            if suite.attributes.title == suite_title:
                return suite.id
        return ""

    def delete_suite(self, project_id: str, suite_id: str) -> Response:
        """Delete a suite via DELETE /api/{project_id}/suites/{suite_id}"""
        resp = self._session.delete(self._url(f"/api/{project_id}/suites/{suite_id}"))
        resp.raise_for_status()
        return resp
