import pytest
from faker import Faker

from src.api import ApiClient
from src.web import Application


@pytest.mark.regression
@pytest.mark.web
def test_random_project_side_bar_navigation(
    logged_app: Application, api_client: ApiClient
):
    """Check side bar navigation on a random not empty project."""
    random_project = api_client.pick_random_project()

    # If a project is empty, add a test suite with api
    if len(api_client.suites_list(random_project)) == 0:
        api_client.create_test_suite(random_project, suite_title=Faker().word())

    project_page = logged_app.project_page.open_by_id(random_project)
    project_page.is_loaded()
    project_page.side_bar.open_side_bar()
    project_page.side_bar.expect_tab_active("Tests")
    project_page.side_bar.click_requirements()
    project_page.side_bar.expect_tab_active("Requirements")


@pytest.mark.smoke
@pytest.mark.web
def test_nonempty_project_suite_creation(
    logged_app: Application, api_client: ApiClient
):
    """Create a suite on a nonempty project.

    Created suite is cleaned up after test."""
    suite_title = Faker().sentence()
    project_id = api_client.pick_random_project(empty=False)

    project_page = logged_app.project_page.open_by_id(project_id)
    project_page.is_loaded()
    project_page.create_suite(suite_title)
    project_page.suite_with_title_is_visible(suite_title)

    suite_id = api_client.get_suite_id_by_title(project_id, suite_title)
    assert suite_id != ""

    # Delete the suite
    api_client.delete_suite(project_id, suite_id)
