import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from src.web.selenium.pages import LoginPage, LoginPageV2
from tests.fixtures.config import Config


@pytest.mark.smoke
@pytest.mark.selenium
def test_login_with_page_object_v1(driver: WebDriver, configs: Config):
    login_page = LoginPage(driver, configs)
    login_page.open(configs.base_app_url)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    login_page.should_see_success_message()


@pytest.mark.regression
@pytest.mark.selenium
def test_login_with_page_object_v2(driver: WebDriver, configs: Config):
    login_page = LoginPageV2(driver, configs)
    login_page.open(configs.base_app_url)
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    login_page.should_see_success_message()
