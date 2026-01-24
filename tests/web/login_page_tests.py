import pytest
from faker import Faker
from playwright.sync_api import expect

from conftest import Config
from src.web.pages.application import Application

fake = Faker()

invalid_login_test_data = [
    # Invalid email formats
    pytest.param("plainaddress", fake.password(length=8), id="missing_at_symbol"),
    pytest.param("@missingusername.com", fake.password(length=8), id="missing_username"),
    pytest.param("username@.com", fake.password(length=8), id="missing_domain_name"),
    pytest.param("username@domain", fake.password(length=8), id="missing_top_level_domain"),
    pytest.param("username@domain.c", fake.password(length=8), id="short_top_level_domain"),

    # Boundary value analysis for password length
    pytest.param(fake.email(), "", id="empty_password"),
    pytest.param(fake.email(), "short", id="short_password"),
    pytest.param(fake.email(), "a" * 5, id="min_length_password"),
    pytest.param(fake.email(), "a" * 129, id="max_length_password"),
    pytest.param(fake.email(), "a" * 130, id="above_max_length_password"),

    # Valid email with invalid password
    pytest.param(fake.email(), "wrongpassword", id="valid_email_wrong_password"),
    pytest.param(fake.email(), "", id="valid_email_empty_password"),

    # XSS injection cases
    pytest.param("<script>alert('XSS')</script>", fake.password(length=8), id="xss_injection_email"),
    pytest.param(fake.email(), "<script>alert('XSS')</script>", id="xss_injection_password"),

    # SQL injection cases
    pytest.param("' OR '1'='1' --", fake.password(length=8), id="sql_injection_email"),
    pytest.param(fake.email(), "' OR '1'='1' --", id="sql_injection_password"),
    pytest.param("' OR 1=1; --", "' OR 1=1; --", id="sql_injection_both")
]


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.temporary
@pytest.mark.parametrize("invalid_email, invalid_password", invalid_login_test_data)
def test_login_invalid(shared_app: Application, invalid_email, invalid_password):
    (shared_app.login_page.open()
     .is_loaded()
     .login(invalid_email, invalid_password)
     .invalid_login_message_visible()
    )


@pytest.mark.smoke
@pytest.mark.web
def test_login_valid(shared_app: Application, configs: Config):
    (shared_app.home_page.open()
     .is_loaded()
     .click_login_button()
     )

    (shared_app.login_page.is_loaded()
    .login(configs.email, configs.password, remember_me=True)
    )

    expect(shared_app.projects_page.sign_in_flash_message).to_be_visible()
    shared_app.projects_page.is_loaded()
