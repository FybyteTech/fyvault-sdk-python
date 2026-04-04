from __future__ import annotations

from typing import List, Optional
from urllib.parse import quote

from ..http import HttpClient
from ..types import MintSessionTokenResult


class AccessTokensResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/access-tokens{suffix}"

    def create(
        self,
        ttl_seconds: int = 900,
        scopes: Optional[List[str]] = None,
    ) -> MintSessionTokenResult:
        """Mint a short-lived session token using a long-lived API key.

        Use the returned token as ``Authorization: Bearer <token>``
        instead of the API key at runtime.
        """
        body = {"ttlSeconds": ttl_seconds}
        if scopes is not None:
            body["scopes"] = scopes  # type: ignore[assignment]
        return self._http.post(self._path(), body)

    def revoke(self, session_token_id: str) -> None:
        self._http.delete(self._path(f"/{quote(session_token_id)}"))
