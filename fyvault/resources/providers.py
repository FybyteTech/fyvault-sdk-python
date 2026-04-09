from __future__ import annotations

from typing import Any, Dict, List, Optional
from urllib.parse import quote

from ..http import HttpClient


class ProvidersResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/providers{suffix}"

    def register(
        self,
        name: str,
        *,
        description: Optional[str] = None,
        provider_type: Optional[str] = None,
        allowed_environments: Optional[List[str]] = None,
        allowed_secret_prefix: Optional[str] = None,
        rate_limit_rpm: Optional[int] = None,
        ip_allowlist: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Register a new provider integration.

        Returns a dict with ``provider``, ``token`` (shown once), and ``webhookSecret``.
        """
        body: Dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if provider_type is not None:
            body["providerType"] = provider_type
        if allowed_environments is not None:
            body["allowedEnvironments"] = allowed_environments
        if allowed_secret_prefix is not None:
            body["allowedSecretPrefix"] = allowed_secret_prefix
        if rate_limit_rpm is not None:
            body["rateLimitRpm"] = rate_limit_rpm
        if ip_allowlist is not None:
            body["ipAllowlist"] = ip_allowlist
        return self._http.post(self._path(), body)

    def list(self) -> List[Dict[str, Any]]:
        """List all provider integrations for the organization."""
        return self._http.get(self._path())

    def get(self, provider_id: str) -> Dict[str, Any]:
        """Get a single provider integration by ID."""
        return self._http.get(self._path(f"/{quote(provider_id)}"))

    def update(
        self,
        provider_id: str,
        *,
        description: Optional[str] = None,
        allowed_environments: Optional[List[str]] = None,
        allowed_secret_prefix: Optional[str] = None,
        rate_limit_rpm: Optional[int] = None,
        ip_allowlist: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Update a provider integration."""
        body: Dict[str, Any] = {}
        if description is not None:
            body["description"] = description
        if allowed_environments is not None:
            body["allowedEnvironments"] = allowed_environments
        if allowed_secret_prefix is not None:
            body["allowedSecretPrefix"] = allowed_secret_prefix
        if rate_limit_rpm is not None:
            body["rateLimitRpm"] = rate_limit_rpm
        if ip_allowlist is not None:
            body["ipAllowlist"] = ip_allowlist
        return self._http.patch(self._path(f"/{quote(provider_id)}"), body)

    def revoke(self, provider_id: str) -> None:
        """Revoke a provider integration."""
        self._http.delete(self._path(f"/{quote(provider_id)}"))
