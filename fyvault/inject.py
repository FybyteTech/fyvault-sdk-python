from __future__ import annotations

import os
from typing import Optional

from .client import FyVault


def inject(
    api_key: str,
    org_id: str,
    base_url: str = "https://api.fyvault.com/api/v1",
    prefix: Optional[str] = None,
) -> int:
    """Load all secrets for the org and inject them into os.environ.

    Args:
        api_key: FyVault API key.
        org_id: Organization ID.
        base_url: API base URL.
        prefix: Optional prefix to prepend to secret names.

    Returns:
        Number of secrets injected.
    """
    client = FyVault(api_key=api_key, org_id=org_id, base_url=base_url)
    try:
        secrets = client.secrets.list()
        count = 0
        for secret in secrets:
            key = secret["name"]
            if prefix:
                key = f"{prefix}{key}"
            # Only set env var if the secret has a value available
            # (server-encrypted secrets expose the name; value comes from boot)
            os.environ[key] = secret.get("value", "")  # type: ignore[arg-type]
            count += 1
        return count
    finally:
        client.close()
