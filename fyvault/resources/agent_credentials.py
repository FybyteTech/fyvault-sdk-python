from __future__ import annotations

from typing import Any, Dict, List, Optional
from urllib.parse import quote

from ..http import HttpClient
from ..types import AgentCredential


class AgentCredentialsResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/agent-credentials{suffix}"

    def create(
        self,
        name: str,
        scopes: List[str],
        *,
        agent_type: Optional[str] = None,
        allowed_secrets: Optional[List[str]] = None,
        allowed_environments: Optional[List[str]] = None,
        max_ttl_seconds: Optional[int] = None,
        rate_limit_rpm: Optional[int] = None,
        ip_allowlist: Optional[List[str]] = None,
        expires_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new agent credential.

        Returns a dict with ``credential`` (shown once), ``credential_id``, and ``name``.
        """
        body: Dict[str, Any] = {"name": name, "scopes": scopes}
        if agent_type is not None:
            body["agentType"] = agent_type
        if allowed_secrets is not None:
            body["allowedSecrets"] = allowed_secrets
        if allowed_environments is not None:
            body["allowedEnvironments"] = allowed_environments
        if max_ttl_seconds is not None:
            body["maxTtlSeconds"] = max_ttl_seconds
        if rate_limit_rpm is not None:
            body["rateLimitRpm"] = rate_limit_rpm
        if ip_allowlist is not None:
            body["ipAllowlist"] = ip_allowlist
        if expires_at is not None:
            body["expiresAt"] = expires_at
        return self._http.post(self._path(), body)

    def list(self) -> List[AgentCredential]:
        """List all active agent credentials for the organization."""
        return self._http.get(self._path())

    def revoke(self, credential_id: str) -> None:
        """Revoke an agent credential."""
        self._http.delete(self._path(f"/{quote(credential_id)}"))
