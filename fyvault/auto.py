"""
FyVault.auto() — Zero-config SDK initialization for Python.

Automatically detects:
  1. Auth method (agent token file → env vars → GitHub OIDC)
  2. Organization ID
  3. Environment (platform signals → NODE_ENV/PYTHON_ENV → org default)
"""

import json
import os
import platform
from pathlib import Path
from typing import Optional

from .client import FyVault
from .errors import FyVaultError


def detect_environment() -> Optional[dict]:
    """
    Detect the current environment from platform signals.
    Returns {"name": "production", "source": "VERCEL_ENV"} or None.
    """
    env = os.environ

    # 1. Explicit override
    if env.get("FYVAULT_ENV"):
        return {"name": env["FYVAULT_ENV"], "source": "FYVAULT_ENV"}

    # 2. Vercel
    if env.get("VERCEL") == "1" or env.get("VERCEL_ENV"):
        vercel_env = env.get("VERCEL_ENV", "production")
        if vercel_env == "preview":
            return {"name": "staging", "source": "VERCEL_ENV=preview"}
        if vercel_env == "development":
            return {"name": "development", "source": "VERCEL_ENV=development"}
        return {"name": "production", "source": "VERCEL_ENV=production"}

    # 3. Netlify
    if env.get("NETLIFY") == "true" or env.get("CONTEXT"):
        ctx = env.get("CONTEXT", "production")
        if ctx == "deploy-preview":
            return {"name": "staging", "source": "NETLIFY CONTEXT=deploy-preview"}
        if ctx in ("branch-deploy", "dev"):
            return {"name": "development", "source": f"NETLIFY CONTEXT={ctx}"}
        return {"name": "production", "source": "NETLIFY CONTEXT=production"}

    # 4. Railway
    if env.get("RAILWAY_ENVIRONMENT_NAME"):
        return {"name": env["RAILWAY_ENVIRONMENT_NAME"].lower(), "source": "RAILWAY_ENVIRONMENT_NAME"}
    if env.get("RAILWAY_ENVIRONMENT"):
        return {"name": env["RAILWAY_ENVIRONMENT"].lower(), "source": "RAILWAY_ENVIRONMENT"}

    # 5. Render
    if env.get("RENDER") == "true":
        if env.get("IS_PULL_REQUEST") == "true":
            return {"name": "staging", "source": "RENDER IS_PULL_REQUEST"}
        return {"name": "production", "source": "RENDER"}

    # 6. Fly.io
    if env.get("FLY_APP_NAME"):
        return {"name": "production", "source": "FLY_APP_NAME"}

    # 7. AWS Lambda / ECS
    if env.get("AWS_LAMBDA_FUNCTION_NAME") or env.get("ECS_CONTAINER_METADATA_URI"):
        func_name = env.get("AWS_LAMBDA_FUNCTION_NAME", "")
        if "staging" in func_name or "stag" in func_name:
            return {"name": "staging", "source": "AWS_LAMBDA (staging in name)"}
        if "dev" in func_name:
            return {"name": "development", "source": "AWS_LAMBDA (dev in name)"}
        return {"name": "production", "source": "AWS_LAMBDA_FUNCTION_NAME"}

    # 8. GitHub Actions
    if env.get("GITHUB_ACTIONS") == "true":
        ref = env.get("GITHUB_REF_NAME", env.get("GITHUB_REF", ""))
        if ref in ("main", "master") or ref.startswith("refs/tags/"):
            return {"name": "production", "source": f"GITHUB_REF={ref}"}
        if ref in ("staging", "stage"):
            return {"name": "staging", "source": f"GITHUB_REF={ref}"}
        return {"name": "development", "source": f"GITHUB_REF={ref}"}

    # 9. GitLab CI
    if env.get("GITLAB_CI") == "true" or env.get("CI_ENVIRONMENT_NAME"):
        if env.get("CI_ENVIRONMENT_NAME"):
            return {"name": env["CI_ENVIRONMENT_NAME"].lower(), "source": "CI_ENVIRONMENT_NAME"}
        branch = env.get("CI_COMMIT_BRANCH", "")
        if branch in ("main", "master"):
            return {"name": "production", "source": "GITLAB main"}
        return {"name": "development", "source": f"GITLAB {branch}"}

    # 10. Python/Node env
    for var in ("PYTHON_ENV", "FLASK_ENV", "DJANGO_ENV", "NODE_ENV"):
        val = env.get(var)
        if val:
            if val == "production":
                return {"name": "production", "source": var}
            if val in ("test", "testing", "staging"):
                return {"name": "staging", "source": var}
            return {"name": "development", "source": var}

    return None


def _agent_token_paths() -> list:
    """Return paths where the agent may have written a token file."""
    paths = []
    if platform.system() == "Linux":
        paths += ["/var/run/fyvault/token", "/tmp/fyvault-token"]
    elif platform.system() == "Darwin":
        paths.append("/tmp/fyvault-token")
    elif platform.system() == "Windows":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            paths.append(os.path.join(appdata, "fyvault", "token"))
        paths.append(os.path.join(os.environ.get("TEMP", "/tmp"), "fyvault-token"))

    home = Path.home()
    paths.append(str(home / ".fyvault" / "token"))
    return paths


def _try_agent_token() -> Optional[dict]:
    """Try reading auth from agent token file."""
    for p in _agent_token_paths():
        try:
            content = Path(p).read_text().strip()
            try:
                data = json.loads(content)
                if data.get("token"):
                    return {
                        "api_key": data["token"],
                        "org_id": data.get("org_id"),
                        "source": f"agent token: {p}",
                    }
            except json.JSONDecodeError:
                if content.startswith("fv") and len(content) > 20:
                    return {"api_key": content, "source": f"agent token: {p}"}
        except (FileNotFoundError, PermissionError):
            continue
    return None


def _try_env_vars() -> Optional[dict]:
    """Try reading auth from environment variables."""
    api_key = os.environ.get("FYVAULT_API_KEY") or os.environ.get("FYVAULT_TOKEN")
    if not api_key:
        return None
    return {
        "api_key": api_key,
        "org_id": os.environ.get("FYVAULT_ORG_ID"),
        "source": "environment variable",
    }


def auto(
    *,
    base_url: Optional[str] = None,
    org_id: Optional[str] = None,
    environment: Optional[str] = None,
    api_key: Optional[str] = None,
) -> FyVault:
    """
    Zero-config FyVault initialization.

    Automatically detects auth, org, and environment from the runtime context.

    Args:
        base_url: Override API base URL
        org_id: Override organization ID
        environment: Override environment name
        api_key: Override API key (skips auto-detection)

    Returns:
        Configured FyVault client

    Raises:
        FyVaultError: If credentials cannot be found

    Example::

        fv = FyVault.auto()
        db_url = fv.secrets.get_value_by_name("DATABASE_URL")
    """
    resolved_base = (
        base_url
        or os.environ.get("FYVAULT_API_BASE")
        or os.environ.get("FYVAULT_BASE_URL")
        or "https://api.fyvault.com/api/v1"
    )

    # Step 1: Detect auth
    auth = None
    if api_key:
        auth = {"api_key": api_key, "source": "explicit"}

    if not auth:
        auth = _try_agent_token()
    if not auth:
        auth = _try_env_vars()

    if not auth:
        raise FyVaultError(
            "FyVault.auto() could not find credentials.\n\n"
            "Tried (in order):\n"
            "  1. Agent token file (/var/run/fyvault/token)\n"
            "  2. FYVAULT_API_KEY environment variable\n\n"
            "To fix, do one of:\n"
            "  - Set FYVAULT_API_KEY and FYVAULT_ORG_ID env vars\n"
            "  - Install the agent: curl -fsSL https://get.fyvault.com | bash\n\n"
            "Docs: https://fyvault.com/docs/quickstart",
            status_code=0,
            code="AUTH_NOT_FOUND",
        )

    # Step 2: Resolve org ID
    resolved_org = org_id or auth.get("org_id") or os.environ.get("FYVAULT_ORG_ID")
    if not resolved_org:
        raise FyVaultError(
            "FyVault.auto() found credentials but no organization ID.\n"
            "Set FYVAULT_ORG_ID or pass org_id to FyVault.auto(org_id='...')",
            status_code=0,
            code="ORG_NOT_FOUND",
        )

    # Step 3: Detect environment
    resolved_env = environment
    if not resolved_env:
        detected = detect_environment()
        if detected:
            resolved_env = detected["name"]

    # Step 4: Create client
    return FyVault(
        api_key=auth["api_key"],
        org_id=resolved_org,
        base_url=resolved_base,
        environment=resolved_env,
    )
