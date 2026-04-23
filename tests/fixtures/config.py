import os
from dataclasses import dataclass
from pathlib import Path

import pytest
from dotenv import load_dotenv

from tests.conftest import TEST_RESULT_DIR

load_dotenv()


STORAGE_STATE_PATH = Path("tests/.auth_state/playwright/storage_state.json")
FREE_PROJECT_STORAGE_STATE = Path(
    "tests/.auth_state/playwright/free_project_storage_state.json"
)


VIDEO_DIR = TEST_RESULT_DIR / "videos"
TRACES_DIR = TEST_RESULT_DIR / "traces"

headless = os.getenv("CI", "false").lower() == "true"

BROWSER_LAUNCH_ARGS = {
    "channel": "chromium",
    "headless": headless,
    "slow_mo": 0,
    "timeout": 120000,
}

CONTEXT_ARGS = {
    "base_url": "https://app.testomat.io",
    "viewport": {"width": 1540, "height": 728},
    "locale": "uk-UA",
    "timezone_id": "Europe/Kyiv",
    #    "record_video_dir": str(VIDEO_DIR),
    "permissions": ["geolocation"],
}


@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    base_app_url: str
    email: str
    password: str
    testomat_token: str


@pytest.fixture(scope="session")
def configs() -> Config:
    return Config(
        base_url=os.getenv("BASE_URL"),
        base_app_url=os.getenv("BASE_APP_URL"),
        login_url=os.getenv("BASE_APP_URL") + "/users/sign_in",
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        testomat_token=os.getenv("TESTOMAT_TOKEN"),
    )
