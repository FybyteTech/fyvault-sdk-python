from __future__ import annotations

from typing import Any, Dict, List, Optional
from urllib.parse import quote

from ..http import HttpClient
from ..types import Secret, SecretVersion, SecretHandle, RotateResult


class SecretsResource:
    def __init__(self, http: HttpClient, org_id: str, environment: Optional[str] = None) -> None:
        self._http = http
        self._org_id = org_id
        self._environment = environment

    def _env_q(self, extra: Optional[str] = None) -> str:
        """Append ?environment= when environment is configured."""
        parts: List[str] = []
        if self._environment:
            parts.append(f"environment={quote(self._environment)}")
        if extra:
            parts.append(extra)
        return f"?{'&'.join(parts)}" if parts else ""

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/secrets{suffix}"

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def list(self) -> List[Secret]:
        return self._http.get(self._path() + self._env_q())

    def get(self, secret_id: str) -> Secret:
        return self._http.get(self._path(f"/{secret_id}"))

    def get_by_name(self, name: str) -> Secret:
        return self._http.get(self._path(f"/by-name/{quote(name)}"))

    def get_value(self, secret_id: str) -> str:
        result = self._http.get(self._path(f"/{secret_id}/value") + self._env_q())
        return result["value"]

    def get_value_by_name(self, name: str) -> str:
        result = self._http.get(
            self._path(f"/by-name/{quote(name)}/value") + self._env_q()
        )
        return result["value"]

    def create(
        self,
        name: str,
        secret_type: str,
        value: Optional[str] = None,
        description: Optional[str] = None,
        client_encrypted_value: Optional[str] = None,
        injection_config: Optional[Dict[str, Any]] = None,
    ) -> Secret:
        body: Dict[str, Any] = {"name": name, "secretType": secret_type}
        if value is not None:
            body["value"] = value
        if description is not None:
            body["description"] = description
        if client_encrypted_value is not None:
            body["clientEncryptedValue"] = client_encrypted_value
        if injection_config is not None:
            body["injectionConfig"] = injection_config
        return self._http.post(self._path(), body)

    def update(self, secret_id: str, value: str) -> Secret:
        return self._http.patch(
            self._path(f"/{secret_id}") + self._env_q(),
            {"value": value},
        )

    def delete(self, secret_id: str) -> None:
        self._http.delete(self._path(f"/{secret_id}"))

    # ------------------------------------------------------------------
    # Versions & rotation
    # ------------------------------------------------------------------

    def versions(self, secret_id: str) -> List[SecretVersion]:
        return self._http.get(self._path(f"/{secret_id}/versions"))

    def rotate(self, secret_id: str, new_value: Optional[str] = None) -> RotateResult:
        """Rotate a secret -- creates a new version with a new value.

        If no value is provided, one is auto-generated based on the secret type.
        """
        body: Dict[str, Any] = {}
        if new_value is not None:
            body["value"] = new_value
        return self._http.post(
            self._path(f"/{secret_id}/rotate") + self._env_q(),
            body,
        )

    # ------------------------------------------------------------------
    # Sharing
    # ------------------------------------------------------------------

    def share(self, secret_id: str, ttl_seconds: int = 86400) -> Dict[str, Any]:
        """Create a one-time, time-limited share link for a secret.

        The link can be viewed exactly once and expires after the specified TTL.
        Default TTL is 24 hours (86400 seconds).
        """
        return self._http.post(
            self._path(f"/{secret_id}/share"),
            {"ttlSeconds": ttl_seconds},
        )

    # ------------------------------------------------------------------
    # Rotating handles
    # ------------------------------------------------------------------

    def get_handle(self, name: str, ttl_seconds: int = 300) -> SecretHandle:
        """Mint a rotating handle for a named secret.

        The handle is a short-lived token (default 5 min) that maps to the
        real secret. Resolve it via ``resolve_handle()`` or through the
        FyVault local proxy.
        """
        return self._http.post(
            self._path(f"/by-name/{quote(name)}/handle"),
            {"ttlSeconds": ttl_seconds},
        )

    def resolve_handle(self, handle: str) -> str:
        """Resolve a rotating handle to the real secret value."""
        result = self._http.post(
            f"/orgs/{self._org_id}/handles/resolve",
            {"handle": handle},
        )
        return result["value"]

    def revoke_handle(self, handle_id: str) -> None:
        """Revoke a handle before its natural TTL expiry."""
        self._http.delete(f"/orgs/{self._org_id}/handles/{handle_id}")

    # ------------------------------------------------------------------
    # Dependencies
    # ------------------------------------------------------------------

    def add_dependency(
        self,
        secret_id: str,
        target_secret_id: str,
        dep_type: str = "rotates_with",
        auto_cascade: bool = False,
    ) -> Dict[str, Any]:
        """Add a dependency between two secrets.

        When the source secret rotates, the target can optionally cascade.
        """
        return self._http.post(
            self._path(f"/{secret_id}/dependencies"),
            {
                "targetSecretId": target_secret_id,
                "type": dep_type,
                "autoCascade": auto_cascade,
            },
        )

    def list_dependencies(self, secret_id: str) -> Dict[str, Any]:
        """List upstream and downstream dependencies for a secret."""
        return self._http.get(self._path(f"/{secret_id}/dependencies"))

    def remove_dependency(self, secret_id: str, dep_id: str) -> None:
        """Remove a dependency by its ID."""
        self._http.delete(self._path(f"/{secret_id}/dependencies/{dep_id}"))
