from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .errors import FyVaultError


class HttpClient:
    """Low-level HTTP transport for the FyVault API."""

    def __init__(self, api_key: str, base_url: str) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    # ------------------------------------------------------------------
    # Response handling
    # ------------------------------------------------------------------

    def _handle(self, response: httpx.Response) -> Any:
        try:
            data = response.json()
        except Exception:
            raise FyVaultError(
                f"Unexpected response ({response.status_code}): unable to parse JSON",
                status_code=response.status_code,
                code="PARSE_ERROR",
            )

        if not data.get("success"):
            status = response.status_code
            if status == 401:
                code = "UNAUTHORIZED"
            elif status == 403:
                code = "FORBIDDEN"
            elif status == 404:
                code = "NOT_FOUND"
            else:
                code = "API_ERROR"
            raise FyVaultError(
                data.get("error", f"API error ({status})"),
                status_code=status,
                code=code,
            )

        return data.get("data")

    # ------------------------------------------------------------------
    # HTTP verbs
    # ------------------------------------------------------------------

    def get(self, path: str) -> Any:
        try:
            return self._handle(self._client.get(path))
        except FyVaultError:
            raise
        except Exception as exc:
            raise FyVaultError(
                f"Network error: {exc}",
                status_code=0,
                code="NETWORK_ERROR",
            ) from exc

    def post(self, path: str, body: Optional[Dict[str, Any]] = None) -> Any:
        try:
            return self._handle(self._client.post(path, json=body))
        except FyVaultError:
            raise
        except Exception as exc:
            raise FyVaultError(
                f"Network error: {exc}",
                status_code=0,
                code="NETWORK_ERROR",
            ) from exc

    def patch(self, path: str, body: Optional[Dict[str, Any]] = None) -> Any:
        try:
            return self._handle(self._client.patch(path, json=body))
        except FyVaultError:
            raise
        except Exception as exc:
            raise FyVaultError(
                f"Network error: {exc}",
                status_code=0,
                code="NETWORK_ERROR",
            ) from exc

    def delete(self, path: str) -> Any:
        try:
            return self._handle(self._client.delete(path))
        except FyVaultError:
            raise
        except Exception as exc:
            raise FyVaultError(
                f"Network error: {exc}",
                status_code=0,
                code="NETWORK_ERROR",
            ) from exc

    def close(self) -> None:
        self._client.close()
