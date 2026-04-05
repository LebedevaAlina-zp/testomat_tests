import random

from src.api.controllers.base_controller import BaseController
from src.api.models import Suite, SuitesResponse


class SuiteController(BaseController):
    def __init__(self, base_url: str, api_token: str, jwt_token: str | None = None):
        super().__init__(base_url=base_url, api_token=api_token, jwt_token=jwt_token)
        # Stores the list of suites after calling get_suites_for_project_id
        self.suites: list[Suite] = []

    def get_suites_for_project_id(self, project_id: str) -> list[Suite]:
        """Returns a suites list via GET /api/{project_id}/suites"""
        response = self._get(f"/api/{project_id}/suites")
        self.suites = SuitesResponse.model_validate(response).data
        if response["meta"]["total_pages"] >= 2:
            total_pages = response["meta"]["total_pages"]
            for page in range(2, total_pages + 1):
                response = self._get(f"/api/{project_id}/suites?page={page}")
                self.suites.extend(SuitesResponse.model_validate(response).data)
        return self.suites

    def get_by_id_for_project_id(self, project_id: str, suite_id: str) -> Suite:
        """Returns a suite via GET /api/{project_id}/suites/{suite_id}"""
        response = self._get(f"/api/{project_id}/suites/{suite_id}")
        return Suite.model_validate(response.get("data"))

    def random_suite(self, project_id) -> Suite:
        """Returns a random suite or None if a suite does not exist for this project."""
        if len(self.suites) == 0:
            self.get_suites_for_project_id(project_id)
        return random.choice(self.suites)

    def add_suite(
        self,
        project_id: str,
        title: str,
        description: str | None = None,
        parent_id: str | None = None,
        attributes: dict[str, object] | None = None,
    ) -> Suite:
        """Create a suite via POST /api/{project_id}/suites and return created Suite.

        Args:
            project_id: Target project id.
            title: Suite title to create.
            description: Suite description to create.
            parent_id: Optional parent suite id (to create a nested suite).
            attributes: Optional dict with any other attributes to set (by API field names).

        Returns:
            Parsed `Suite` model of the created suite (from response.data).
        """
        attrs: dict[str, object] = {"title": title, "description": description}
        if parent_id:
            # API expects dashed key name
            attrs["parent-id"] = parent_id

        if attributes:
            attrs.update(attributes)

        payload = {"data": {"type": "suite", "attributes": attrs}}
        response = self._post(f"/api/{project_id}/suites", data=payload)
        return Suite.model_validate(response.get("data"))

    def update_suite(
        self,
        project_id: str,
        suite_id: str,
        title: str | None = None,
        description: str | None = None,
        attributes: dict[str, object] | None = None,
    ) -> Suite:
        """Update a suite modifying only attributes according to arguments.

        Args:
            project_id: Target project id.
            suite_id: Suite id to update.
            title: Optional new title.
            description: Optional new description.
            attributes: Optional dict with any other attributes to update (by API field names).

        Returns:
            Updated `Suite` model.
        """

        attrs: dict[str, object] = {}
        if title is not None:
            attrs["title"] = title
        if description is not None:
            attrs["description"] = description
        if attributes:
            attrs.update(attributes)

        payload = {"data": {"type": "suite", "id": "", "attributes": attrs}}
        response = self._put(f"/api/{project_id}/suites/{suite_id}", data=payload)
        return Suite.model_validate(response.get("data"))

    def delete_by_id_for_project_id(self, project_id: str, suite_id: str) -> None:
        """Delete a suite via DELETE /api/{project_id}/suites/{suite_id}"""
        self._delete(f"/api/{project_id}/suites/{suite_id}")
