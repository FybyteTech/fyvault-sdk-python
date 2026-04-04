from __future__ import annotations

from ..http import HttpClient
from ..types import Organization


class OrgsResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def get(self) -> Organization:
        return self._http.get(f"/orgs/{self._org_id}")
