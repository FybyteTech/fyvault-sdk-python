from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..http import HttpClient


class SandboxesResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def _path(self, suffix: str = "") -> str:
        return f"/orgs/{self._org_id}/environments/sandbox{suffix}"

    def create(
        self,
        parent_env_id: str,
        secret_names: List[str],
        ttl_minutes: int = 30,
    ) -> Dict[str, Any]:
        """Create an ephemeral sandbox environment.

        Copies the specified secrets from the parent environment into
        a short-lived sandbox that auto-destroys after the TTL.

        Args:
            parent_env_id: Environment ID to clone secrets from.
            secret_names: List of secret names to copy into the sandbox.
            ttl_minutes: Time-to-live in minutes (1-1440). Default 30.
        """
        return self._http.post(
            self._path(),
            {
                "parentEnvId": parent_env_id,
                "secretNames": secret_names,
                "ttlMinutes": ttl_minutes,
            },
        )

    def list(self) -> List[Dict[str, Any]]:
        """List all active ephemeral sandboxes."""
        return self._http.get(self._path())

    def destroy(self, env_id: str) -> None:
        """Destroy a sandbox environment early."""
        self._http.delete(self._path(f"/{env_id}"))
