from __future__ import annotations

import pytest

from src.api import ApiClient

from .config import Config


@pytest.fixture(scope="session")
def api_client(configs: Config) -> ApiClient:
    """Session-scoped API client authenticated with email/password from configs."""
    return ApiClient(base_url=configs.base_app_url, email=configs.email, password=configs.password)
