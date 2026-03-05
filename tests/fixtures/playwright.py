import pytest
from playwright.sync_api import Browser, sync_playwright

from .config import BROWSER_LAUNCH_ARGS


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Shared browser instance for the whole test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(**BROWSER_LAUNCH_ARGS)
        yield browser
        browser.close()
