from __future__ import annotations

from typing import Any, Dict, Optional

from ..http import HttpClient


class BreakGlassResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def create(
        self,
        reason: str,
        environment: Optional[str] = None,
        ttl_minutes: int = 60,
    ) -> Dict[str, Any]:
        """Create a break-glass emergency access session.

        Requires OWNER role. Returns a short-lived token that grants
        full access to the organization.

        Args:
            reason: Incident reference or justification for break-glass access.
            environment: Optional environment to scope the session to.
            ttl_minutes: Time-to-live in minutes (1-240). Default 60.
        """
        body: Dict[str, Any] = {
            "reason": reason,
            "ttlMinutes": ttl_minutes,
        }
        if environment is not None:
            body["environmentId"] = environment
        return self._http.post(
            f"/orgs/{self._org_id}/break-glass",
            body,
        )
