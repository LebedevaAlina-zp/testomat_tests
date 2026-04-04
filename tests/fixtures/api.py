from __future__ import annotations

import pytest
import requests

from src.api import ApiClient
from src.api.controllers import ProjectController, SuiteController

from .config import Config


@pytest.fixture(scope="session")
def auth_token(configs: Config) -> str:
    """Single authentication token shared across all controllers."""
    response = requests.post(
        f"{configs.base_app_url}/api/login",
        json={"api_token": configs.testomat_token},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["jwt"]


@pytest.fixture(scope="session")
def project_controller(configs: Config, auth_token: str) -> ProjectController:
    controller = ProjectController(
        base_url=configs.base_app_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def suite_controller(configs: Config, auth_token: str) -> SuiteController:
    controller = SuiteController(
        base_url=configs.base_app_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def api_client(configs: Config) -> ApiClient:
    """Session-scoped API client authenticated with email/password from configs."""
    return ApiClient(
        base_url=configs.base_app_url, email=configs.email, password=configs.password
    )
