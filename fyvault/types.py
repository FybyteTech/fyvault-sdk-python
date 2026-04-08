from __future__ import annotations

from typing import Any, Dict, List, Optional

from typing_extensions import TypedDict


# ------------------------------------------------------------------
# Secrets
# ------------------------------------------------------------------

class Secret(TypedDict):
    secret_id: str
    name: str
    description: Optional[str]
    secret_type: str
    injection_config: Dict[str, Any]
    encryption_mode: str
    current_version: int
    last_rotated_at: Optional[str]
    created_at: str
    updated_at: str


class SecretVersion(TypedDict):
    version_id: str
    version: int
    created_by: int
    created_at: str


class SecretValue(TypedDict):
    name: str
    value: str


class CreateSecretInput(TypedDict, total=False):
    name: str
    description: str
    secret_type: str
    value: str
    client_encrypted_value: str
    injection_config: Dict[str, Any]


class SecretHandle(TypedDict):
    handle: str
    handle_id: str
    expires_at: str
    secret_name: str


class RotateResult(TypedDict):
    secretId: str
    name: str
    version: int


# ------------------------------------------------------------------
# Devices
# ------------------------------------------------------------------

class Device(TypedDict):
    device_id: str
    name: str
    fingerprint: str
    status: str
    agent_version: Optional[str]
    last_boot_at: Optional[str]
    last_heartbeat_at: Optional[str]
    created_at: str


class RegisterDeviceInput(TypedDict):
    name: str
    fingerprint: str


# ------------------------------------------------------------------
# Organizations
# ------------------------------------------------------------------

class Organization(TypedDict):
    org_id: str
    name: str
    slug: str
    created_at: str


# ------------------------------------------------------------------
# Environments
# ------------------------------------------------------------------

class Environment(TypedDict):
    environment_id: str
    name: str
    description: Optional[str]
    is_default: bool
    sort_order: int
    created_at: str
    updated_at: str


class CreateEnvironmentInput(TypedDict, total=False):
    name: str
    description: str


# ------------------------------------------------------------------
# Access Tokens
# ------------------------------------------------------------------

ApiScope = str  # e.g. "SECRETS_READ", "SECRETS_WRITE", etc.


class MintSessionTokenResult(TypedDict):
    token: str
    session_token_id: str
    expires_at: str
    scopes: List[str]


# ------------------------------------------------------------------
# Agent Credentials
# ------------------------------------------------------------------

class AgentCredential(TypedDict):
    credential_id: str
    name: str
    description: Optional[str]
    agent_type: str
    scopes: List[str]
    allowed_secrets: List[str]
    allowed_environments: List[str]
    max_ttl_seconds: int
    rate_limit_rpm: Optional[int]
    expires_at: Optional[str]
    is_active: bool
    last_used_at: Optional[str]
    created_at: str


# ------------------------------------------------------------------
# Scanner
# ------------------------------------------------------------------

class ScanFinding(TypedDict):
    pattern_name: str
    matched_text: str
    line_number: int
    confidence: str  # "high" | "medium" | "low"


# ------------------------------------------------------------------
# Integrations
# ------------------------------------------------------------------

class SyncResult(TypedDict):
    platform: str
    synced: int
    failed: int
    errors: List[str]


class GenerateResult(TypedDict):
    format: str
    filename: str
    content: str
    count: int


class ImportResult(TypedDict):
    created: int
    skipped: int
    overwritten: int


# ------------------------------------------------------------------
# Generic API response
# ------------------------------------------------------------------

class ApiResponse(TypedDict):
    success: bool
    data: Any
    error: Optional[str]
