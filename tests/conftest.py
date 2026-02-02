import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext

from src.web import Application
from src.web.pages import LoginPage

load_dotenv()

BROWSER_LAUNCH_ARGS = {
    "channel": "chrome",
    "headless": False,
    "slow_mo": 0,
    "timeout": 120000,
    # "traces_dir": "test-result/traces"
}

CONTEXT_ARGS = {
    "base_url": "https://app.testomat.io",
    "viewport": {"width": 1540, "height": 728},
    "locale": "uk-UA",
    "timezone_id": "Europe/Kyiv",
    "record_video_dir": "videos/",
    "permissions": ["geolocation"],
}


def clear_browser_data(context: BrowserContext):
    """Clears cookies and local/session storage for all pages in the browser context."""
    context.clear_cookies()
    for page in context.pages:
        page.evaluate("localStorage.clear()")
        page.evaluate("sessionStorage.clear()")


@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_URL"),
        login_url=os.getenv("BASE_APP_URL") + "/users/sign_in",
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD")
    )


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(**BROWSER_LAUNCH_ARGS)
        yield browser
        browser.close()


@pytest.fixture(scope="module")
def browser_context(browser: Browser):
    context = browser.new_context(**CONTEXT_ARGS)
    yield context
    context.close()


@pytest.fixture(scope="module")
def shared_page(browser_context: BrowserContext):
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def app(shared_page):
    yield Application(shared_page)
    clear_browser_data(shared_page.context)


@pytest.fixture(scope="session")
def logged_context(browser: Browser, configs: Config):
    context = browser.new_context(**CONTEXT_ARGS)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(configs.email, configs.password, remember_me=True)
    page.close()
    yield context
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext, configs: Config):
    page = logged_context.new_page()
    yield Application(page)
    page.close()
