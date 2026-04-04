import random

from src.api.controllers.base_controller import BaseController
from src.api.models import Suite, SuitesResponse


class SuiteController(BaseController):
    def __init__(self, base_url: str, api_token: str, jwt_token: str | None = None):
        super().__init__(base_url=base_url, api_token=api_token, jwt_token=jwt_token)
        # Stores the list of suites after calling get_suites_for_project_id
        self.suites: list[Suite] = []

    def get_suites_for_project_id(self, project_id: str) -> list[Suite]:
        response = self._get(f"/api/{project_id}/suites")
        self.suites = SuitesResponse.model_validate(response).data
        return self.suites

    def get_by_id_for_project_id(self, project_id: str, suite_id: str) -> Suite:
        response = self._get(f"/api/{project_id}/suites/{suite_id}")
        return Suite.model_validate(response.get("data"))

    def random_suite(self, project_id) -> Suite:
        """Returns a random suite or None if suite does not exist for this project."""
        self.get_suites_for_project_id(project_id)
        if len(self.suites) == 0:
            return None
        return random.choice(self.suites)

    def add_suite(
        self,
        project_id: str,
        title: str,
        description: str | None = None,
        parent_id: str | None = None,
    ) -> Suite:
        """Create a suite via POST /api/{project_id}/suites and return created Suite.

        Args:
            project_id: Target project id.
            title: Suite title to create.
            description: Suite description to create.
            parent_id: Optional parent suite id (to create a nested suite).

        Returns:
            Parsed `Suite` model of the created suite (from response.data).
        """
        attributes: dict[str, object] = {"title": title, "description": description}
        if parent_id:
            # API expects dashed key name
            attributes["parent-id"] = parent_id

        payload = {"data": {"type": "suite", "attributes": attributes}}
        response = self._post(f"/api/{project_id}/suites", data=payload)
        return Suite.model_validate(response.get("data"))

    def delete_by_id_for_project_id(self, project_id: str, suite_id: str) -> Suite:
        self._delete(f"/api/{project_id}/suites/{suite_id}")
