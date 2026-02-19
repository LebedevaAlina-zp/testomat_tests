import pytest
from playwright.sync_api import Browser, BrowserContext

from src.web import Application
from src.web.pages import LoginPage

from .config import CONTEXT_ARGS, Config


def clear_browser_data(context: BrowserContext):
    """Clears cookies and local/session storage for all pages in the browser context."""
    context.clear_cookies()
    for page in context.pages:
        page.evaluate("localStorage.clear()")
        page.evaluate("sessionStorage.clear()")


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
