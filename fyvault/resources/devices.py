from __future__ import annotations

from typing import List

from ..http import HttpClient
from ..types import Device


class DevicesResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/devices{suffix}"

    def list(self) -> List[Device]:
        return self._http.get(self._path())

    def get(self, device_id: str) -> Device:
        return self._http.get(self._path(f"/{device_id}"))

    def register(self, name: str, fingerprint: str) -> Device:
        return self._http.post(self._path(), {"name": name, "fingerprint": fingerprint})

    def revoke(self, device_id: str) -> None:
        self._http.delete(self._path(f"/{device_id}"))
