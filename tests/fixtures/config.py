import os
from dataclasses import dataclass
from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv()


STORAGE_STATE_PATH = Path("playwright/.auth/storage_state.json")
FREE_PROJECT_STORAGE_STATE = Path("playwright/.auth/free_project_storage_state.json")


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
        password=os.getenv("PASSWORD"),
    )
