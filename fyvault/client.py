from __future__ import annotations

from .http import HttpClient
from .resources.secrets import SecretsResource
from .resources.devices import DevicesResource


class FyVault:
    """FyVault SDK client."""

    def __init__(
        self,
        api_key: str,
        org_id: str,
        base_url: str = "https://api.fyvault.dev/api/v1",
    ) -> None:
        self._http = HttpClient(api_key, base_url)
        self._org_id = org_id
        self.secrets = SecretsResource(self._http, org_id)
        self.devices = DevicesResource(self._http, org_id)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "FyVault":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
