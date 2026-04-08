from __future__ import annotations

from typing import Any, Dict

from ..http import HttpClient


class ComplianceResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def generate_report(
        self,
        report_type: str = "soc2",
        period_days: int = 90,
    ) -> Dict[str, Any]:
        """Generate a compliance report.

        Args:
            report_type: One of ``"soc2"``, ``"hipaa"``, or ``"iso27001"``.
            period_days: Reporting period in days (1-365). Default 90.
        """
        return self._http.get(
            f"/orgs/{self._org_id}/compliance/report"
            f"?type={report_type}&period={period_days}"
        )
