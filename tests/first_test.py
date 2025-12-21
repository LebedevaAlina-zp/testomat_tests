import pytest
from faker import Faker
from playwright.sync_api import Page, expect

TARGET_PROJECT = "Industrial & Jewelry"

from conftest import Config


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    page.goto(configs.login_url)
    login_user(page, email=configs.email, password=configs.password)


def test_sign_in_with_invalid_creds(page: Page, configs: Config):
    page.goto(configs.base_url)

    expect(page.get_by_text('Log in', exact=True)).to_be_visible()

    page.get_by_text('Log in', exact=True).click()
    invalid_password = Faker().password(length=10)

    page.locator("#content-desktop #user_email").fill(configs.email)
    page.locator("#content-desktop #user_password").fill(invalid_password)
    page.get_by_role("button", name="Sign In").click()

    expect(page.locator("#content-desktop .common-flash-info-right")).to_have_text("Invalid Email or password.")


def test_search_project_in_company(page: Page, configs: Config, login):
    search_by_project(page, TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()
    expect(page.locator("ul li h3").filter(visible=True)).to_have_text(TARGET_PROJECT)


def test_should_be_possible_open_free_project(page: Page, configs: Config, login):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    expect(page.get_by_text("Create project")).to_be_visible()

    search_by_project(page, TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_hidden()


def search_by_project(page: Page, target_project: str):
    page.locator("#content-desktop #search").fill(target_project)


def open_homepage(page: Page, configs: Config):
    page.goto(configs.base_url)


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign In").click()
