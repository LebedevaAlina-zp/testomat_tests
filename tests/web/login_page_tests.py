import pytest
from faker import Faker
from playwright.sync_api import expect

from conftest import Config
from src.web.pages.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_login_invalid(app: Application, configs: Config):
    (app.home_page.open()
     .is_loaded()
     .click_login_button()
    )
    (app.login_page.is_loaded()
     .login(configs.email, Faker().password(length=10))
     .invalid_login_message_visible()
    )


@pytest.mark.smoke
@pytest.mark.web
def test_login_valid(app: Application, configs: Config):
    (app.home_page.open()
     .is_loaded()
     .click_login_button()
     )

    (app.login_page.is_loaded()
    .login(configs.email, configs.password, remember_me=True)
    )

    expect(app.projects_page.sign_in_flash_message).to_be_visible()
    app.projects_page.is_loaded()
