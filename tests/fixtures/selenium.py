import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver

from src.web.selenium.pages import LoginPage, ProjectsPage

from .config import Config

AUTH_STATE_COOKIES = Path("tests/.auth_state/selenium/auth_state.json")
FREE_PLAN_STATE_COOKIES = Path("tests/.auth_state/selenium/free_plan_state.json")


@pytest.fixture(scope="function")
def driver() -> WebDriver:
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    driver.set_window_size(1540, 820)
    yield driver
    driver.quit()


def expires_in_x_seconds(storage_state_path: Path, x: int = 60) -> bool:
    """Checks if storage state file expires in x seconds."""
    storage_state = json.loads(storage_state_path.read_text())
    now = datetime.now(UTC)
    for cookie in storage_state:
        if cookie.get("expiry"):
            expires_at = datetime.fromtimestamp(cookie["expiry"], UTC)
            if expires_at - timedelta(seconds=x) <= now:
                return True
            else:
                return False
    return True


def generate_free_plan_state_cookies(
    auth_state_cookies: Path, free_plan_state_cookies: Path
) -> None:
    """Creates a cookies state file for a free plan logged-in user
    based on an existing auth state cookies with a default plan."""

    if not auth_state_cookies.exists():
        return

    modified_cookies = json.loads(auth_state_cookies.read_text())

    for cookie in modified_cookies:
        if cookie.get("name") == "company_id":
            cookie["value"] = ""

    free_plan_state_cookies.write_text(json.dumps(modified_cookies))


@pytest.fixture(scope="function")
def logged_driver(driver: WebDriver, configs: Config) -> WebDriver:
    if AUTH_STATE_COOKIES.exists():
        if not expires_in_x_seconds(AUTH_STATE_COOKIES):
            driver.get(configs.base_app_url)
            saved_cookies = json.loads(AUTH_STATE_COOKIES.read_text())
            for cookie in saved_cookies:
                if cookie.get("name") in ["company_id", "_backend_session"]:
                    driver.add_cookie(cookie)
            driver.refresh()
            yield driver
            return

    login_page = LoginPage(driver, configs)
    login_page.open(configs.base_app_url)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    login_page.should_see_success_message()

    AUTH_STATE_COOKIES.parent.mkdir(parents=True, exist_ok=True)

    cookies = driver.get_cookies()
    AUTH_STATE_COOKIES.write_text(json.dumps(cookies))
    generate_free_plan_state_cookies(AUTH_STATE_COOKIES, FREE_PLAN_STATE_COOKIES)
    yield driver


@pytest.fixture(scope="function")
def free_logged_driver(driver: WebDriver, configs: Config) -> WebDriver:
    """Creates a logged-in driver based on an existing free plan auth state cookies."""
    if FREE_PLAN_STATE_COOKIES.exists():
        if not expires_in_x_seconds(FREE_PLAN_STATE_COOKIES):
            driver.get(configs.base_app_url)
            saved_cookies = json.loads(FREE_PLAN_STATE_COOKIES.read_text())
            for cookie in saved_cookies:
                if cookie.get("name") in ["company_id", "_backend_session"]:
                    driver.add_cookie(cookie)
            driver.refresh()
            yield driver
            return

    login_page = LoginPage(driver, configs)
    login_page.open(configs.base_app_url)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    login_page.should_see_success_message()

    AUTH_STATE_COOKIES.parent.mkdir(parents=True, exist_ok=True)
    cookies = driver.get_cookies()
    AUTH_STATE_COOKIES.write_text(json.dumps(cookies))
    generate_free_plan_state_cookies(AUTH_STATE_COOKIES, FREE_PLAN_STATE_COOKIES)

    projects_page = ProjectsPage(driver, configs)
    projects_page.choose_company_in_dropdown_list(
        projects_page.company_options.free_projects
    )

    yield driver
