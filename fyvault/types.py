from __future__ import annotations

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


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


class CreateSecretInput(TypedDict, total=False):
    name: str
    description: str
    secret_type: str
    value: str
    client_encrypted_value: str
    injection_config: Dict[str, Any]


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


class Organization(TypedDict):
    org_id: str
    name: str
    slug: str
    created_at: str
