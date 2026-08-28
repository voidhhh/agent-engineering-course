from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


class ApplicationAPIError(RuntimeError):
    """Normalized error returned by a local application control API."""


def validate_local_base_url(base_url: str) -> str:
    parsed = urlsplit(base_url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("application API must use HTTP on a loopback host")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("application API base URL contains unsupported components")
    return base_url.rstrip("/") + "/"


def request_json(
    base_url: str,
    token: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    timeout: float = 3.0,
) -> Any:
    if not token:
        raise ValueError("application API token must not be empty")
    safe_base = validate_local_base_url(base_url)
    body = None if payload is None else json.dumps(payload).encode()
    request = Request(
        urljoin(safe_base, path.lstrip("/")),
        data=body,
        method=method,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read(1_000_001)
    except HTTPError as exc:
        detail = exc.read(4096).decode(errors="replace")
        raise ApplicationAPIError(f"application API returned {exc.code}: {detail}") from exc
    except URLError as exc:
        raise ApplicationAPIError(f"application API is unavailable: {exc.reason}") from exc
    if len(raw) > 1_000_000:
        raise ApplicationAPIError("application API response exceeds 1 MB")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ApplicationAPIError("application API returned invalid JSON") from exc
