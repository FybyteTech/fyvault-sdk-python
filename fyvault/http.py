from __future__ import annotations

from typing import Any, Dict, Optional

import httpx


class HttpClient:
    def __init__(self, api_key: str, base_url: str) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    def _handle(self, response: httpx.Response) -> Any:
        data = response.json()
        if not data.get("success"):
            raise Exception(data.get("error", f"API error ({response.status_code})"))
        return data.get("data")

    def get(self, path: str) -> Any:
        return self._handle(self._client.get(path))

    def post(self, path: str, body: Optional[Dict[str, Any]] = None) -> Any:
        return self._handle(self._client.post(path, json=body))

    def patch(self, path: str, body: Optional[Dict[str, Any]] = None) -> Any:
        return self._handle(self._client.patch(path, json=body))

    def delete(self, path: str) -> None:
        self._handle(self._client.delete(path))

    def close(self) -> None:
        self._client.close()
