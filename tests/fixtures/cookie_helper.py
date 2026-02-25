from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from .config import STORAGE_STATE_PATH


def _ensure_storage_file(path: Path) -> None:
    """Ensure storage_state.json file exists with a valid base structure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps({"cookies": [], "origins": []}))


def _load_state(path: Path) -> dict[str, Any]:
    _ensure_storage_file(path)
    try:
        return json.loads(path.read_text() or "{}") or {"cookies": [], "origins": []}
    except json.JSONDecodeError:
        # If file is corrupted, reset to base structure
        return {"cookies": [], "origins": []}


def _save_state(path: Path, state: dict[str, Any]) -> None:
    path.write_text(json.dumps(state))


@dataclass
class Cookie:
    name: str
    value: str
    domain: str
    path: str = "/"
    expires: int | None = None
    httpOnly: bool = False
    secure: bool = False
    sameSite: str = "Lax"  # One of: "Lax", "None", "Strict"

    def to_dict(self) -> dict[str, Any]:
        data = {
            "name": self.name,
            "value": self.value,
            "domain": self.domain,
            "path": self.path,
            "httpOnly": self.httpOnly,
            "secure": self.secure,
            "sameSite": self.sameSite,
        }
        if self.expires is not None:
            data["expires"] = self.expires
        return data


class CookieHelper:
    """Utility to manage cookies within Playwright storage_state.json for tests.

    Default storage file is configured via tests.fixtures.config.STORAGE_STATE_PATH.
    """

    def __init__(self, storage_path: Path | str = STORAGE_STATE_PATH):
        self.storage_path = Path(storage_path)

    # ---------- query helpers ----------
    def exists(self, name: str, domain: str | None = None) -> bool:
        state = _load_state(self.storage_path)
        return self._find_cookie(state, name, domain) is not None

    def get_value(self, name: str, domain: str | None = None) -> str | None:
        state = _load_state(self.storage_path)
        cookie = self._find_cookie(state, name, domain)
        return cookie.get("value") if cookie else None

    # ---------- mutation helpers ----------
    def add(
        self,
        name: str,
        value: str,
        domain: str,
        path: str = "/",
        *,
        expires: int | None = None,
        httpOnly: bool = False,
        secure: bool = False,
        sameSite: str = "Lax",
    ) -> None:
        """Add or replace a cookie in storage_state.json.

        If a cookie with the same name (and optional domain) exists, it is replaced.
        """
        state = _load_state(self.storage_path)
        cookies: list[dict[str, Any]] = list(state.get("cookies", []))

        # Remove existing cookie with same name (and domain if provided)
        cookies = [c for c in cookies if not (c.get("name") == name and (domain is None or c.get("domain") == domain))]

        new_cookie = Cookie(
            name=name,
            value=value,
            domain=domain,
            path=path,
            expires=expires,
            httpOnly=httpOnly,
            secure=secure,
            sameSite=sameSite,
        ).to_dict()

        cookies.append(new_cookie)
        state["cookies"] = cookies
        _save_state(self.storage_path, state)

    def add_many(self, items: Iterable[tuple[str, str, str] | dict[str, Any] | Cookie]) -> None:
        """Add multiple cookies.

        Accepts an iterable of:
        - Cookie instances
        - dicts with Playwright cookie fields
        - tuples in form: (name, value, domain)
        """
        for item in items:
            if isinstance(item, Cookie):
                data = item.to_dict()
            elif isinstance(item, tuple) and len(item) == 3:
                data = Cookie(name=item[0], value=item[1], domain=item[2]).to_dict()
            elif isinstance(item, dict):
                # Minimal validation and defaults
                data = {
                    "name": item["name"],
                    "value": item["value"],
                    "domain": item["domain"],
                    "path": item.get("path", "/"),
                    "httpOnly": item.get("httpOnly", False),
                    "secure": item.get("secure", False),
                    "sameSite": item.get("sameSite", "Lax"),
                }
                if "expires" in item and item["expires"] is not None:
                    data["expires"] = item["expires"]
            else:
                raise TypeError("Unsupported cookie item type")

            self.add(
                data["name"],
                data["value"],
                data["domain"],
                path=data.get("path", "/"),
                expires=data.get("expires"),
                httpOnly=data.get("httpOnly", False),
                secure=data.get("secure", False),
                sameSite=data.get("sameSite", "Lax"),
            )

    def clear(self, name: str, domain: str | None = None) -> None:
        """Remove a cookie by name (and optional domain) from storage_state.json."""
        state = _load_state(self.storage_path)
        before = list(state.get("cookies", []))
        after = [c for c in before if not (c.get("name") == name and (domain is None or c.get("domain") == domain))]
        state["cookies"] = after
        _save_state(self.storage_path, state)

    # ---------- internal ----------
    @staticmethod
    def _find_cookie(state: dict[str, Any], name: str, domain: str | None) -> dict[str, Any] | None:
        for c in state.get("cookies", []):
            if c.get("name") == name and (domain is None or c.get("domain") == domain):
                return c
        return None


# Pytest fixture to provide CookieHelper instance in tests
@pytest.fixture(scope="function")
def cookies() -> CookieHelper:
    return CookieHelper(STORAGE_STATE_PATH)
