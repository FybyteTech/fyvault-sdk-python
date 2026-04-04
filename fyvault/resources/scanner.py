from __future__ import annotations

from typing import List, Optional

from ..http import HttpClient
from ..types import ScanFinding


class ScannerResource:
    def __init__(self, http: HttpClient, org_id: str) -> None:
        self._http = http
        self._org_id = org_id

    def scan_text(self, text: str, source_ref: Optional[str] = None) -> List[ScanFinding]:
        """Scan a block of text for leaked secrets / credentials."""
        result = self._http.post(
            f"/orgs/{self._org_id}/scan/text",
            {"text": text, "sourceRef": source_ref},
        )
        return result["findings"]
