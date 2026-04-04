from __future__ import annotations

from typing import Optional

from .http import HttpClient
from .resources.secrets import SecretsResource
from .resources.devices import DevicesResource
from .resources.orgs import OrgsResource
from .resources.access_tokens import AccessTokensResource
from .resources.environments import EnvironmentsResource
from .resources.scanner import ScannerResource
from .resources.integrations import IntegrationsResource


class FyVault:
    """FyVault SDK client.

    Args:
        api_key: API key (``fv_live_...`` or a short-lived session token).
        org_id: Organization ID.
        base_url: API base URL.  Defaults to the FyVault cloud endpoint.
        environment: Optional environment name or ID.  When set, all
            secret operations are scoped to this environment.
    """

    def __init__(
        self,
        api_key: str,
        org_id: str,
        base_url: str = "https://api.fyvault.com/api/v1",
        environment: Optional[str] = None,
    ) -> None:
        self._http = HttpClient(api_key, base_url)
        self._org_id = org_id

        self.secrets = SecretsResource(self._http, org_id, environment)
        self.devices = DevicesResource(self._http, org_id)
        self.orgs = OrgsResource(self._http, org_id)
        self.access_tokens = AccessTokensResource(self._http, org_id)
        self.environments = EnvironmentsResource(self._http, org_id)
        self.scanner = ScannerResource(self._http, org_id)
        self.integrations = IntegrationsResource(self._http, org_id)

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._http.close()

    def __enter__(self) -> "FyVault":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
