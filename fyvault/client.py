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
from .resources.agent_credentials import AgentCredentialsResource
from .resources.break_glass import BreakGlassResource
from .resources.sandboxes import SandboxesResource
from .resources.compliance import ComplianceResource
from .resources.providers import ProvidersResource


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
        self.agent_credentials = AgentCredentialsResource(self._http, org_id)
        self.break_glass = BreakGlassResource(self._http, org_id)
        self.sandboxes = SandboxesResource(self._http, org_id)
        self.compliance = ComplianceResource(self._http, org_id)
        self.providers = ProvidersResource(self._http, org_id)

    @classmethod
    def auto(
        cls,
        *,
        base_url: Optional[str] = None,
        org_id: Optional[str] = None,
        environment: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> "FyVault":
        """Zero-config initialization. Auto-detects auth, org, and environment.

        Auth detection: agent token file → env vars → GitHub OIDC
        Env detection: FYVAULT_ENV → platform signals → NODE_ENV/PYTHON_ENV

        Example::

            fv = FyVault.auto()
            db_url = fv.secrets.get_value_by_name("DATABASE_URL")
        """
        from .auto import auto as _auto
        return _auto(
            base_url=base_url,
            org_id=org_id,
            environment=environment,
            api_key=api_key,
        )

    @staticmethod
    def detect_environment():
        """Detect environment from platform signals without creating a client."""
        from .auto import detect_environment
        return detect_environment()

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._http.close()

    def __enter__(self) -> "FyVault":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
