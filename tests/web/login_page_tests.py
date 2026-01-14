import faker
from playwright.sync_api import Page

from conftest import Config
from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage
from src.web.pages.projects_page import ProjectsPage


def test_login_invalid(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login_button()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(configs.email, faker.Faker().password(length=10))
    login_page.invalid_login_message_visible()


def test_login_valid(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login_button()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)

    ProjectsPage(page).is_loaded()
