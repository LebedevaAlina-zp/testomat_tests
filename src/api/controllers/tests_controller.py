from src.api.controllers.base_controller import BaseController
from src.api.models import Test, TestsResponse


class TestController(BaseController):
    def __init__(self, base_url: str, api_token: str, jwt_token: str | None = None):
        super().__init__(base_url=base_url, api_token=api_token, jwt_token=jwt_token)
        # Stores the list of tests after calling get_tests_for_project_id
        self.tests: list[Test] = []

    def get_tests_for_project_id(self, project_id: str) -> list[Test]:
        """Returns a tests list via GET /api/{project_id}/tests"""
        response = self._get(f"/api/{project_id}/tests")
        self.tests = TestsResponse.model_validate(response).data
        if response["meta"]["total_pages"] >= 2:
            total_pages = response["meta"]["total_pages"]
            for page in range(2, total_pages + 1):
                response = self._get(f"/api/{project_id}/tests?page={page}")
                self.tests.extend(TestsResponse.model_validate(response).data)
        return self.tests

    def get_tests_for_suite(self, project_id: str, suite_id: str) -> list[Test]:
        """Returns a tests list for a specified suite via GET /api/{project_id}/tests?suite_id="""
        response = self._get(f"/api/{project_id}/tests?suite_id={suite_id}")
        self.tests = TestsResponse.model_validate(response).data
        return self.tests

    def get_by_id_for_project_id(self, project_id: str, test_id: str) -> Test:
        """Returns tests via GET /api/{project_id}/tests/{test_id}."""
        response = self._get(f"/api/{project_id}/tests/{test_id}")
        return Test.model_validate(response.get("data"))

    def add_test(
        self,
        project_id: str,
        suite_id: str,
        title: str,
        description: str | None = None,
        attributes: dict[str, object] | None = None,
    ) -> Test:
        """Create a test via POST /api/{project_id}/tests and return created Test.

        Args:
            project_id: Target project id.
            suite_id: Target suite id
            title: Test title.
            description: Optional test description.
            attributes: Optional dict with other attributes to set (by API field names).

        Returns:
            Parsed `Test` model of the created test (from response.data).
        """
        attrs: dict[str, object] = {"suite_id": suite_id, "title": title}
        if description:
            attrs["description"] = description
        if attributes:
            attrs.update(attributes)

        payload = {"data": {"type": "test", "attributes": attrs}}
        response = self._post(f"/api/{project_id}/tests", data=payload)
        return Test.model_validate(response.get("data"))

    def update_test(
        self,
        project_id: str,
        test_id: str,
        suite_id: str | None = None,
        title: str | None = None,
        description: str | None = None,
        attributes: dict[str, object] | None = None,
    ) -> Test:
        """Update a test via PUT /api/{project_id}/tests/{test_id}
        modifying only attributes according to arguments.

        Args:
            project_id: Target project id.
            test_id: Test id to update.
            title: Optional new title.
            title: Optional new title.
            description: Optional new description.
            attributes: Optional dict with any other attributes to update (by API field names).

        Returns:
            Updated `Test` model.
        """

        attrs: dict[str, object] = {}
        if suite_id is not None:
            attrs["title"] = suite_id
        if title is not None:
            attrs["title"] = title
        if description is not None:
            attrs["description"] = description
        if attributes:
            attrs.update(attributes)

        payload = {"data": {"type": "test", "id": "", "attributes": attrs}}
        response = self._put(f"/api/{project_id}/tests/{test_id}", data=payload)
        return Test.model_validate(response.get("data"))

    def delete_by_id_for_project_id(self, project_id: str, test_id: str) -> None:
        """Delete a test via DELETE /api/{project_id}/tests/{test_id}"""
        self._delete(f"/api/{project_id}/tests/{test_id}")
