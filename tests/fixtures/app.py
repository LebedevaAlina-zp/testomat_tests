import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
)

from src.web import Application

from .config import (
    CONTEXT_ARGS,
    FREE_PROJECT_STORAGE_STATE,
    STORAGE_STATE_PATH,
    TRACES_DIR,
    Config,
)


def start_tracing(page: Page) -> None:
    """Starts recording Playwright trace"""
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)


def stop_tracing_on_failure(page: Page, request: pytest.FixtureRequest) -> None:
    """Stops recording Playwright trace and saves it to a file"""
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        trace_path = TRACES_DIR / f"{timestamp}-{request.node.name}-trace.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        page.context.tracing.stop(path=trace_path)
    else:
        page.context.tracing.stop()


def clear_browser_data(context: BrowserContext) -> None:
    """Clears cookies and local/session storage for all pages in the browser context."""
    context.clear_cookies()
    for page in context.pages:
        page.evaluate("localStorage.clear()")
        page.evaluate("sessionStorage.clear()")


def expires_in_x_seconds(storage_state_path: Path, x: int) -> bool:
    """Checks if storage state file expires in x seconds."""
    storage_state = json.loads(storage_state_path.read_text())
    now = datetime.now(UTC)
    for cookie in storage_state.get("cookies", []):
        if cookie.get("expires"):
            expires_at = datetime.fromtimestamp(cookie["expires"], UTC)
            if expires_at - timedelta(seconds=x) <= now:
                return True
            else:
                return False
    return True


def generate_free_plan_storage_state(
    storage_state: Path, free_plan_storage_state: Path
) -> None:
    """Creates a storage state file for a free plan logged-in user
    based on an existing storage state with a default plan."""

    if not storage_state.exists():
        return

    new_storage_state = json.loads(storage_state.read_text())

    for cookie in new_storage_state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""

    free_plan_storage_state.write_text(json.dumps(new_storage_state))


@pytest.fixture(scope="module")
def browser_context(browser: Browser) -> BrowserContext:
    """Browser context instance for the module tests."""
    context = browser.new_context(**CONTEXT_ARGS)
    yield context
    context.close()


@pytest.fixture(scope="function")
def app(browser_context, request: pytest.FixtureRequest) -> Application:
    """Application instance with clean browser context for each test."""
    page = browser_context.new_page()
    start_tracing(page)
    yield Application(page)
    stop_tracing_on_failure(page=page, request=request)
    page.close()
    clear_browser_data(page.context)


@pytest.fixture(scope="session")
def logged_context(browser: Browser, configs: Config) -> BrowserContext:
    """Session scope context for reuse logged-in state."""

    if STORAGE_STATE_PATH.exists():
        if not expires_in_x_seconds(STORAGE_STATE_PATH, 60):
            context = browser.new_context(
                **CONTEXT_ARGS,
                storage_state=STORAGE_STATE_PATH,
            )
            yield context
            context.close()
            return

    context = browser.new_context(**CONTEXT_ARGS)
    page = context.new_page()

    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password, remember_me=True)
    app.projects_page.is_sign_in_successful_message_visible()

    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_STATE_PATH)

    generate_free_plan_storage_state(STORAGE_STATE_PATH, FREE_PROJECT_STORAGE_STATE)

    page.close()
    yield context
    context.close()


@pytest.fixture(scope="session")
def free_plan_context(
    logged_context: BrowserContext, browser: Browser
) -> BrowserContext:
    """Session scope context for reuse free plan logged-in state."""
    context = browser.new_context(
        **CONTEXT_ARGS, storage_state=FREE_PROJECT_STORAGE_STATE
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def logged_app(
    logged_context: BrowserContext, request: pytest.FixtureRequest
) -> Application:
    """Application instance with logged-in state for each test."""
    page = logged_context.new_page()
    start_tracing(page)
    yield Application(page)
    stop_tracing_on_failure(page=page, request=request)
    page.close()


@pytest.fixture(scope="function")
def free_plan_app(
    free_plan_context: BrowserContext, request: pytest.FixtureRequest
) -> Application:
    """Application instance with free plan logged-in state for each test."""
    page = free_plan_context.new_page()
    start_tracing(page)
    yield Application(page)
    stop_tracing_on_failure(page=page, request=request)
    page.close()
