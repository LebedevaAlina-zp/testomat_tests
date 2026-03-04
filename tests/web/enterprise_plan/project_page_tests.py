import random

import pytest
from faker import Faker

from src.api import ApiClient
from src.web import Application


@pytest.mark.regression
@pytest.mark.web
def test_project_side_bar_navigation(logged_app: Application):
    target_project_name = "Grocery, Outdoors & Shoes"
    project_page = logged_app.project_page.open_by_project_name(target_project_name)

    project_page.side_bar.is_loaded()
    project_page.side_bar.open_side_bar()
    project_page.side_bar.expect_tab_active("Tests")
    project_page.side_bar.click_requirements()
    project_page.side_bar.expect_tab_active("Requirements")


@pytest.mark.regression
@pytest.mark.web
def test_random_project_side_bar_navigation(logged_app: Application, api_client: ApiClient):
    suite_title = Faker().sentence()
    projects_list = api_client.projects_list()
    random_project = projects_list[random.randint(0, len(projects_list) - 1)]

    project_page = logged_app.project_page.open_by_id(random_project.id)
    project_page.side_bar.is_loaded()
    project_page.side_bar.open_side_bar()
    project_page.side_bar.expect_tab_active("Tests")
    project_page.create_suite(suite_title)
    project_page.suite_with_title_is_visible(suite_title)
