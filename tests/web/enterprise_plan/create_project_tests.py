import pytest
from faker import Faker

from src.api import ApiClient
from src.web import Application
from src.web.pages import ProjectType


@pytest.mark.smoke
@pytest.mark.web
def test_create_new_project_positive(logged_app: Application, api_client: ApiClient):
    """Create a project with a valid random name, check it was created and delete it."""
    valid_project_title = Faker().company()

    (logged_app.new_project_page.open().is_loaded().create_new_project(valid_project_title, ProjectType.CLASSICAL))

    (logged_app.project_page.is_loaded().verify_project_title_is(valid_project_title).readme_block_close_btn.click())

    # Check the project with the same title was created
    project_id = api_client.get_project_id_by_title(valid_project_title)
    assert project_id != ""

    # Delete the project
    assert api_client.delete_project(project_id).status_code in [200, 204]

    # Check the project was deleted
    project_id = api_client.get_project_id_by_title(valid_project_title)
    assert project_id == ""
