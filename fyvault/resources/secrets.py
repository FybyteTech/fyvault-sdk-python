from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..http import HttpClient
from ..types import Secret, SecretVersion


class SecretsResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/secrets{suffix}"

    def list(self) -> List[Secret]:
        return self._http.get(self._path())

    def get(self, secret_id: str) -> Secret:
        return self._http.get(self._path(f"/{secret_id}"))

    def create(
        self,
        name: str,
        secret_type: str,
        value: Optional[str] = None,
        description: Optional[str] = None,
        injection_config: Optional[Dict[str, Any]] = None,
    ) -> Secret:
        body: Dict[str, Any] = {"name": name, "secret_type": secret_type}
        if value is not None:
            body["value"] = value
        if description is not None:
            body["description"] = description
        if injection_config is not None:
            body["injection_config"] = injection_config
        return self._http.post(self._path(), body)

    def update(self, secret_id: str, value: str) -> Secret:
        return self._http.patch(self._path(f"/{secret_id}"), {"value": value})

    def delete(self, secret_id: str) -> None:
        self._http.delete(self._path(f"/{secret_id}"))

    def versions(self, secret_id: str) -> List[SecretVersion]:
        return self._http.get(self._path(f"/{secret_id}/versions"))
