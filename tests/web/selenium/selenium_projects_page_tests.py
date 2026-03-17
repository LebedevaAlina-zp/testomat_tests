import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from src.web.selenium.pages.projects_page import ProjectsPage
from tests.fixtures import Config


@pytest.mark.selenium
def test_default_enterprise_projects_page(logged_driver: WebDriver, configs: Config):
    projects_page = ProjectsPage(logged_driver, configs)
    projects_page.open()
    projects_page.is_loaded_default_enterprise()


@pytest.mark.selenium
def test_free_plan_projects_page(free_logged_driver: WebDriver, configs: Config):
    free_plan_projects_page = ProjectsPage(free_logged_driver, configs)
    free_plan_projects_page.open()
    free_plan_projects_page.is_loaded_free_plan()
