from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .helper import _get
from .suite import Suite


@dataclass(frozen=True)
class SuitesMeta:
    total_pages: int | None = None
    per_page: int | None = None
    num: int | None = None
    page: int | None = None
    rId: Any | None = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SuitesMeta:
        return SuitesMeta(
            total_pages=_get(data, "total_pages"),
            per_page=_get(data, "per_page"),
            num=_get(data, "num"),
            page=_get(data, "page"),
            rId=_get(data, "rId"),
        )


@dataclass(frozen=True)
class SuitesResponse:
    """Response for GET /api/{project_id}/suites."""

    data: list[Suite]
    meta: SuitesMeta | None = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SuitesResponse:
        items = _get(data, "data")
        suites: list[Suite] = []
        if isinstance(items, list):
            suites = [Suite.from_dict(x) for x in items if isinstance(x, dict)]

        meta_raw = _get(data, "meta")
        meta = SuitesMeta.from_dict(meta_raw) if isinstance(meta_raw, dict) else None

        return SuitesResponse(data=suites, meta=meta)

    @staticmethod
    def from_json(
        payload: Any,
    ) -> list[SuitesResponse] | SuitesResponse:
        """Parse JSON payload into models."""
        if isinstance(payload, list):
            return [SuitesResponse.from_dict(x) for x in payload if isinstance(x, dict)]
        if isinstance(payload, dict):
            return SuitesResponse.from_dict(payload)
        return SuitesResponse(data=[])
