from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .project import (
    Project,  # reuse existing model
    _get,  # helper to extract kebab-case keys
)


@dataclass(frozen=True)
class ProjectsResponse:
    """Response item for GET /api/projects."""

    data: list[Project]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ProjectsResponse:
        items = _get(data, "data")
        projects: list[Project] = []
        if isinstance(items, list):
            projects = [Project.from_dict(x) for x in items if isinstance(x, dict)]
        return ProjectsResponse(data=projects)

    @staticmethod
    def from_json(payload: Any) -> list[ProjectsResponse] | ProjectsResponse:
        """Parse JSON into models.

        The example file shows a top-level list of response objects. To be robust
        we support both a single-object response and a list of response objects.
        """
        if isinstance(payload, list):
            return [ProjectsResponse.from_dict(x) for x in payload if isinstance(x, dict)]
        if isinstance(payload, dict):
            return ProjectsResponse.from_dict(payload)
        return ProjectsResponse(data=[])
