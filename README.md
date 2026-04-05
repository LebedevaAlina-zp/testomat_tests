Testomat E2E Tests

Playwright-based end-to-end and API testing framework for the Testomat application.

## Project Structure

```
testomat_tests/
├── src/                               # Source code
│   ├── api/                           # API layer (client + MVC for API tests)
│   │   ├── client.py                  # Low-level API client (used across project)
│   │   ├── controllers/               # Controllers (C in MVC) – API use-cases
│   │   │   ├── base_controller.py
│   │   │   ├── project_controller.py
│   │   │   ├── suite_controller.py
│   │   │   └── tests_controller.py
│   │   └── models/                    # Pydantic models (M in MVC)
│   │       ├── models.py              # Base/commons for models
│   │       ├── project.py
│   │       ├── suite.py
│   │       └── test.py
│   └── web/                           # Web UI automation (Playwright sync API)
│       ├── application.py             # Application facade (entry point)
│       ├── pages/                     # Page Object Models (POM)
│       │   ├── home_page.py
│       │   ├── login_page.py
│       │   ├── projects_page.py
│       │   ├── new_project_page.py
│       │   └── project_page.py
│       └── components/                # Reusable UI components
│           ├── header_nav.py
│           ├── project_card.py
│           ├── side_bar_nav.py
│           ├── project_page_readme_block.py
│           ├── project_page_tests_tab.py
│           └── suite_creation_form.py
│
├── tests/                             # Test suites and fixtures
│   ├── conftest.py                    # Pytest config and plugins loader
│   ├── fixtures/                      # Shared fixtures and settings
│   │   ├── app.py                     # App/contexts, tracing, auth state
│   │   ├── config.py                  # Browser/context args, .env configs
│   │   ├── playwright.py              # Browser session fixture
│   │   ├── selenium.py                # Selenium session fixture
│   │   └── api.py                     # API fixtures (wires client + controllers)
│   ├── web/                           # Web UI tests (Playwright + Selenium)
│   │   ├── login_page_tests.py
│   │   ├── cookies_tests.py
│   │   ├── selenium/                  # Selenium-marked UI tests
│   │   │   ├── selenium_login_tests.py
│   │   │   ├── selenium_projects_page_tests.py
│   │   │   └── simple_test_via_selenium.py
│   │   ├── free_plan/
│   │   └── enterprise_plan/
│   └── api/                           # API tests (use MVC controllers + models)
│       ├── api_tests.py
│       ├── projects_tests.py
│       ├── suites_tests.py
│       └── tests_tests.py
│
├── test-result/                       # Test artifacts (created on first run)
│   ├── report.html                    # Pytest HTML report (self-contained)
│   ├── traces/                        # Playwright traces (on failure)
│   └── videos/                        # Optional video recordings
│
├── testomat_api.yaml                  # OpenAPI schema (reference)
├── .env                               # Environment configuration (create locally)
├── pyproject.toml                     # Project configuration (deps, pytest, ruff)
└── uv.lock                            # Dependency lock file (if using uv)
```

Notes about API layer usage

- The low-level `src/api/client.py` API client is reused across the project, including within UI tests, to set up or
  clean up preconditions (e.g., creating projects, suites, or tests via API before visiting pages). This keeps UI flows
  fast and focused on UI assertions instead of data creation.
- API tests follow an MVC-like structure: Pydantic models under `src/api/models` represent data (M), while
  `src/api/controllers/*_controller.py` encapsulate higher-level operations (C). The tests in `tests/api/` call these
  controllers and validate responses via the models. There is no separate View layer for API tests.

## Requirements

- Python >= 3.14
- Google Chrome installed (Playwright is launched with `channel="chrome"`)
- Recommended: `uv` package manager

## Installation

### Using uv (Recommended)

```powershell
# Install uv if not already installed
pip install uv

# Create virtual environment and install dependencies
uv sync

# Install Playwright browsers (Chromium/Firefox/WebKit)
uv run playwright install
```

### Using pip

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# Install Playwright browsers
python -m playwright install
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
BASE_URL=https://testomat.io
BASE_APP_URL=https://app.testomat.io
EMAIL=your_email@example.com
PASSWORD=your_password
TESTOMAT_TOKEN=your_access_token
```

Notes

- Default Playwright context `base_url` is set to `https://app.testomat.io` in `tests/fixtures/config.py`.
- Auth/session state is cached in `playwright/.auth/storage_state.json` between runs by session fixtures.
- Generate an access token at https://app.testomat.io/account/access_tokens and set it as `TESTOMAT_TOKEN` in your
  `.env`. This token is required for API interactions/tests.

## Running Tests

Pytest discovery is scoped to `tests/` by default (see `pyproject.toml`).

```powershell
# Run all the tests with uv:
uv run pytest

or in case of pip:
pytest

# Run smoke or regression subsets
uv run pytest -m smoke
uv run pytest -m regression

# Run only web UI tests
uv run pytest -m web

# Run API tests
uv run pytest -m api

# Run a specific test file or test
uv run pytest tests\web\login_page_tests.py
uv run pytest tests\web\login_page_tests.py::test_login_invalid

# Verbose output
uv run pytest -v

# Run tests failed on previous run
uv run pytest --lf
```

Headed vs Headless

- Default is headed (`headless=False`) with Chrome channel. To run headless, set
  `BROWSER_LAUNCH_ARGS["headless"] = True` in `tests/fixtures/config.py`.

## Test Markers

Configured in `pyproject.toml`:

- `smoke` – Quick validation tests
- `regression` – Full test suite
- `web` – Web UI specific tests
- `api` – API tests
- `slow` – Long-running tests
- `flaky` – Flaky tests to retry on failure
- `selenium` – UI tests using Selenium

## Selenium UI Tests

This project also contains a minimal Selenium-based UI automation layer and tests. Use it when you want to demonstrate
WebDriver usage or compare approaches with Playwright.

Structure:

```
src/web/selenium/
├── core/
│   ├── base_page.py      # BasePage: navigation, interactions, waits wrapper
│   └── waits.py          # Wait helper around WebDriverWait + EC
└── pages/
    ├── login_page.py     # Page Object using static locators
    └── login_page_v2.py  # Page Object using properties + typed elements

tests/fixtures/selenium.py  # Selenium fixtures and auth state helpers
tests/web/selenium/         # Selenium tests (@pytest.mark.selenium)
```

### Requirements for Selenium

- Python >= 3.14 (same virtualenv as the project)
- Google Chrome installed
- Chromedriver is resolved automatically by Selenium Manager (bundled with Selenium >= 4.6); no manual driver download
  is required

## Architecture

### Page Object Model (POM)

All pages live under `src/web/pages` and are wired via the `Application` facade:

```python
from playwright.sync_api import Page
from src.web.pages import HomePage, LoginPage, NewProjectPage, ProjectPage, ProjectsPage


class Application:
    def __init__(self, page: Page):
        self.home_page = HomePage(page)
        self.project_page = ProjectPage(page)
        self.login_page = LoginPage(page)
        self.new_project_page = NewProjectPage(page)
        self.projects_page = ProjectsPage(page)
```

### Fixture Strategy

Key fixtures (in `tests/fixtures`):

- `browser` (session) – shared Playwright browser
- `browser_context` (module) – clean context per module
- `app` (function) – fresh `Application` per test, tracing enabled
- `logged_context` (session) – cached logged-in context with storage state
- `logged_app` (function) – `Application` using logged-in context per test, tracing enabled
- `free_plan_context`/`free_plan_app` – variants for free plan flows
- `configs` (session) – environment configuration loaded from `.env`

Playwright tracing is automatically started for each test and saved on failure under `test-result/traces`.

### Viewing Playwright Traces

Traces are saved as `.zip` archives in `test-result\traces` when a test fails, e.g.:

```
test-result\traces\2026-03-06_19-47-test_random_project_side_bar_navigation-trace.zip
```

Open a trace with the Playwright Trace Viewer in either way:

- Using the Playwright CLI (via uv):

  ```powershell
  uv run playwright show-trace "test-result\traces\<your-trace-file>.zip"
  ```

- Using the Playwright CLI (plain pip environment):

  ```powershell
  playwright show-trace "test-result\traces\<your-trace-file>.zip"
  ```

- In the browser: drag-and-drop the `.zip` file onto https://trace.playwright.dev

Tips

- If no trace file appears: ensure the test actually failed — by default this project only saves traces on failures.
- To inspect another run, delete old zips from `test-result\traces` and re-run tests to generate fresh artifacts.

## Code Quality

Ruff is configured for linting and formatting.

```powershell
# Check for linting issues
ruff check .

# Fix linting issues automatically
ruff check --fix .

# Format code
ruff format .
```

## Browser and Locale Settings

Defaults (see `tests/fixtures/config.py`):

- Browser: Chrome channel
- Headless: False
- Viewport: 1540x728
- Locale: uk-UA
- Timezone: Europe/Kyiv
- Permissions: geolocation
- Timeout: 120s

## Troubleshooting

- Browser fails to launch: ensure Google Chrome is installed; or switch to bundled Chromium by removing `channel` from
  `BROWSER_LAUNCH_ARGS` and running `python -m playwright install chromium`.
- Login tests failing: verify `.env` `EMAIL`/`PASSWORD` and `BASE_APP_URL`.
- Elements not found/timeouts: UI or selectors may have changed; inspect selectors in `src/web/pages` and
  `src/web/components`.
