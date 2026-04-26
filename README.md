Testomat E2E Tests

Playwright-based end-to-end and API testing framework for the Testomat application.

## Quickstart

1. Install uv and sync deps

   ```powershell
   pip install uv
   uv sync
   uv run playwright install
   ```

2. Create .env

   ```env
   BASE_URL=https://testomat.io
   BASE_APP_URL=https://app.testomat.io
   EMAIL=your_email@example.com
   PASSWORD=your_password
   TESTOMAT_TOKEN=your_access_token
   ```

3. Run a quick smoke

   ```powershell
   uv run pytest -m smoke
   ```

4. Generate and open the Allure report

   ```powershell
   allure generate test-result/allure-results
   allure open allure-report
   ```

   Alternatives:
    - View Playwright traces for failed tests:
      playwright show-trace test-result/traces/
   ```powershell
   playwright show-trace test-result/traces/trace_file_name.zip
   ```
    - View the simple HTML report instead: `start .\test-result\report.html`

#### Quickstart (pip)

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
python -m playwright install
pytest -m smoke
# Allure report (generate and open)
allure generate test-result/allure-results
allure open allure-report

```

## Requirements

- Python >= 3.14
- Google Chrome installed (Playwright is launched with `channel="chrome"`)
- Recommended: `uv` package manager

## Project Structure

```
testomat_tests/
├── .github/                           # GitHub configuration
│   ├── workflows/                     # CI workflows (linter + tests + schedule)
│   │   └── tests.yml                  # Main pipeline (PRs, cron, manual)
│   └── actions/                       # Reusable composite actions
│       └── setup/                     # Python + uv setup used by workflows
├── src/                               # Source code
│   ├── api/                           # API layer (client + MVC for API tests)
│   │   ├── client.py                  # API client (used for UI tests preconditions)
│   │   ├── controllers/               # Controllers (C in MVC) – API use-cases
│   │   │   ├── base_controller.py
│   │   │   ├── project_controller.py
│   │   │   ├── suite_controller.py
│   │   │   └── tests_controller.py
│   │   └── models/                    # Pydantic models (M in MVC)
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
│   │   ├── free_plan/
│   │   └── enterprise_plan/
│   └── api/                           # API tests (use MVC controllers + models)
│       ├── api_tests.py
│       ├── projects_tests.py
│       ├── suites_tests.py
│       └── tests_tests.py
│
├── test-result/                       # Test artifacts
│   ├── report.html                    # Pytest HTML report (self-contained)
│   ├── allure-results/                # Files for allure report
│   ├── traces/                        # Playwright traces (on failure)
│   └── videos/                        # Optional video recordings
│
├── .env                               # Environment configuration (create locally)
├── pyproject.toml                     # Project configuration (deps, pytest, ruff)
└── uv.lock                            # Dependency lock file (if using uv)
```

## Installation and Configuration

Covered in Quickstart above. Use either uv or plain pip, and create a `.env` with the variables shown there.

Notes

- Playwright `base_url` defaults to https://app.testomat.io (see `tests/fixtures/config.py`).
- Auth state is cached at `tests/.auth_state/playwright/storage_state.json` between runs.
- Create an access token at https://app.testomat.io/account/access_tokens and set `TESTOMAT_TOKEN` in `.env`.
- The low-level API client (`src/api/client.py`) is reused to set up/clean up test data, including in UI tests.
- API tests use lightweight MVC: Pydantic models (`src/api/models`) + controllers (`src/api/controllers`); tests call
  controllers and validate models.
- A minimal Selenium UI layer is included for WebDriver comparison with Playwright.
- Allure reporting is used across the project. Failed Playwright web tests attach traces and screenshots to Allure; API
  tests attach request/response logs.
- GitHub Actions CI is configured to run ruff linter and test suites on pull requests and on a scheduled trigger; see
  `.github/workflows/tests.yml`.
- CI publishes a combined Allure report to GitHub Pages on each run. Find the deployed link in the run’s deployment
  summary for the "github-pages" environment.
- CI also uploads Allure results and, on Playwright failures, trace archives as workflow artifacts. These artifacts are
  retained for 3 days and can be downloaded to generate/open reports locally.

### Environment variables explained

| Variable         | Used by                        | Purpose                                      |
|------------------|--------------------------------|----------------------------------------------|
| `BASE_URL`       | UI tests                       | Marketing site base (rarely changed)         |
| `BASE_APP_URL`   | UI + API                       | App base, e.g. https://app.testomat.io       |
| `EMAIL`          | UI + `ApiClient`               | Email for login + precondition API calls     |
| `PASSWORD`       | UI + `ApiClient`               | Password for login + precondition API        |
| `TESTOMAT_TOKEN` | Controllers-based API fixtures | Access token exchanged for a short‑lived JWT |

Tip: If only running controller‑based API tests, you can omit `EMAIL`/`PASSWORD`. If only using `ApiClient`, you can
omit `TESTOMAT_TOKEN`.

### Test Markers

Configured in `pyproject.toml`:

- `smoke` – Quick validation tests
- `regression` – Full test suite
- `web` – Web UI specific tests
- `api` – API tests
- `slow` – Long-running tests
- `flaky` – Flaky tests to retry on failure
- `selenium` – UI tests using Selenium

### Continuous Integration (CI)

This project includes a GitHub Actions workflow that automatically lints and tests the codebase.

- Triggers: on pull requests, on a nightly schedule (cron), and on manual runs (workflow_dispatch).
- Jobs: ruff linter plus API and Web UI test suites (Playwright; Selenium subset) executed with uv.
- Artifacts: Allure results are uploaded for each job and retained for 3 days; on Playwright failures, traces are also
  uploaded and retained for 3 days.
- Publishing: A combined Allure report is generated from all jobs and published to GitHub Pages.
- Configuration: see `.github/workflows/tests.yml` and the reusable setup action in `.github/actions/setup/`.

### API Authentication

There are two authentication flows used in this repository, depending on the layer:

- Controllers-based API tests (fixtures `project_controller`, `suite_controller`, `tests_controller`) authenticate via
  an API token. The fixture first exchanges `TESTOMAT_TOKEN` for a short-lived JWT by POSTing to `/api/login` with
  body `{ "api_token": <TESTOMAT_TOKEN> }`, then uses that JWT for subsequent requests. See `tests/fixtures/api.py`.

- The low-level `ApiClient` (used mainly for UI preconditions) authenticates with email/password: it POSTs to
  `/api/login` with form data `{ "email": <EMAIL>, "password": <PASSWORD> }` and stores the returned JWT. See
  `src/api/client.py`.

As a result, your `.env` should normally provide all of the following so both flows work out of the box:

- `EMAIL` / `PASSWORD` — for UI login and `ApiClient`
- `TESTOMAT_TOKEN` — for controllers-based API tests

Optional: OpenAPI schema `testomat_api.yaml` and `tool.datamodel-codegen` settings in `pyproject.toml` allow
regenerating
typed Pydantic models into `src/api/models/models.py` if the API changes.

### Resetting cached login state

If login flows act inconsistently, delete cached storage states and re‑run:

```powershell
Remove-Item -Force -ErrorAction SilentlyContinue tests\.auth_state\playwright\*.json
```

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

- Default is headed (`headless=False`) with Chrome channel. To run headless, set in `tests/fixtures/config.py`:

```python
BROWSER_LAUNCH_ARGS = {
    "channel": "chrome",
    "headless": True,
    "slow_mo": 0,
    "timeout": 120000,
}
```

### Viewing Playwright Traces

Playwright tracing is automatically started for each test and saved on failure under `test-result/traces`.

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

### Recording videos (optional)

Uncomment `record_video_dir` in `tests/fixtures/config.py` and re‑run tests:

```python
CONTEXT_ARGS = {
    # ...
    "record_video_dir": "test-result/videos",  # enable video capture
}
```

Videos will be saved under `test-result/videos`.

## Selenium UI Tests

This repo also contains a minimal Selenium layer. To run only Selenium tests:

```powershell
uv run pytest -m selenium
```

Requirements: Selenium Manager (bundled with Selenium >= 4.6) auto‑resolves drivers on Windows, so no manual
ChromeDriver install is needed.

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
