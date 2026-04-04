import random

from src.api.controllers.base_controller import BaseController
from src.api.models import Project, ProjectsResponse


class ProjectController(BaseController):
    def __init__(self, base_url: str, api_token: str, jwt_token: str | None = None):
        super().__init__(base_url=base_url, api_token=api_token, jwt_token=jwt_token)
        # Stores the list of projects after calling get_all
        self.projects: list[Project] = []

    def get_all(self) -> list[Project]:
        """Return a list of all projects."""
        response = self._get("/api/projects")
        self.projects = ProjectsResponse.model_validate(response).data
        return self.projects

    def get_by_id(self, project_id: str) -> Project:
        """Get a project by its id."""
        response = self._get(f"/api/projects/{project_id}")
        return Project.model_validate(response.get("data"))

    def get_id_by_project_title(self, project_title: str) -> str:
        """Returns project id finding a project in a projects list by title"""
        projects_list = self.get_all()
        for project in projects_list:
            if project.attributes.title == project_title:
                return project.id
        return ""

    def random_project(self) -> Project:
        """Return a random project."""
        if self.projects == []:
            self.get_all()
        return random.choice(self.projects)

    def delete_project(self, project_id: str):
        """Delete a project via DELETE /api/projects/{project_id}"""
        self._delete(self._url(f"/api/projects/{project_id}"))
