from __future__ import annotations

from typing import List, Optional

from ..http import HttpClient
from ..types import Environment


class EnvironmentsResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/environments{suffix}"

    def list(self) -> List[Environment]:
        return self._http.get(self._path())

    def get(self, env_id: str) -> Environment:
        return self._http.get(self._path(f"/{env_id}"))

    def create(self, name: str, description: Optional[str] = None) -> Environment:
        body = {"name": name}
        if description is not None:
            body["description"] = description
        return self._http.post(self._path(), body)

    def update(
        self,
        env_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Environment:
        body = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        return self._http.patch(self._path(f"/{env_id}"), body)

    def delete(self, env_id: str) -> None:
        self._http.delete(self._path(f"/{env_id}"))

    def set_default(self, env_id: str) -> None:
        self._http.post(self._path(f"/{env_id}/set-default"))
