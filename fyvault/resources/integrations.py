from __future__ import annotations

from typing import Dict, Optional

from ..http import HttpClient
from ..types import SyncResult, GenerateResult, ImportResult


class IntegrationsResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/integrations{suffix}"

    def sync(
        self,
        platform: str,
        environment_id: str,
        config: Dict[str, str],
    ) -> SyncResult:
        return self._http.post(self._path("/sync"), {
            "platform": platform,
            "environmentId": environment_id,
            "config": config,
        })

    def generate(
        self,
        format: str,
        environment_id: str,
        options: Optional[Dict[str, str]] = None,
    ) -> GenerateResult:
        return self._http.post(self._path("/generate"), {
            "format": format,
            "environmentId": environment_id,
            "options": options,
        })

    def import_from_provider(
        self,
        provider: str,
        content: str,
        environment_id: str,
        duplicate_strategy: str = "skip",
    ) -> ImportResult:
        return self._http.post(self._path("/import"), {
            "provider": provider,
            "content": content,
            "environmentId": environment_id,
            "duplicateStrategy": duplicate_strategy,
        })

    def notify(
        self,
        platform: str,
        config: Dict[str, str],
        message: str,
    ) -> None:
        self._http.post(self._path("/notify"), {
            "platform": platform,
            "config": config,
            "message": message,
        })
