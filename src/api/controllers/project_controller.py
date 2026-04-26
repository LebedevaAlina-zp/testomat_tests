import random

import allure

from src.api.controllers.base_controller import BaseController
from src.api.models import Project, ProjectsResponse


class ProjectController(BaseController):
    def __init__(self, base_url: str, api_token: str, jwt_token: str | None = None):
        super().__init__(base_url=base_url, api_token=api_token, jwt_token=jwt_token)
        # Stores the list of projects after calling get_all
        self.projects: list[Project] = []

    @allure.step("Get the list of projects")
    def get_all(self) -> list[Project]:
        """Return a list of all projects."""
        response = self._get("/api/projects")
        self.projects = ProjectsResponse.model_validate(response).data
        return self.projects

    @allure.step("Get a project by id")
    def get_by_id(self, project_id: str) -> Project:
        """Get a project by its id."""
        response = self._get(f"/api/projects/{project_id}")
        return Project.model_validate(response.get("data"))

    @allure.step("Pick a random project from the list of projects")
    def random_project(self, with_tests: bool | None = None) -> Project:
        """Return a random project, optionaly with or without tests."""
        if self.projects == []:
            self.get_all()
        project = random.choice(self.projects)

        if with_tests is None:
            return project
        elif with_tests:
            while project.attributes.tests_count in (0, None):
                project = random.choice(self.projects)
            return project
        else:
            while project.attributes.tests_count > 0:
                project = random.choice(self.projects)
            return project

    @allure.step("Delete a project")
    def delete_project(self, project_id: str):
        """Delete a project via DELETE /api/projects/{project_id}"""
        self._delete(self._url(f"/api/projects/{project_id}"))
