from typing import Any


def _get(d: dict[str, Any], key: str, default: Any = None) -> Any:
    """Helper to safely get keys that may contain hyphens in JSON."""
    if key in d:
        return d[key]
    # try common conversions between snake_case and kebab-case
    kebab = key.replace("_", "-")
    snake = key.replace("-", "_")
    if kebab in d:
        return d[kebab]
    if snake in d:
        return d[snake]
    return default
