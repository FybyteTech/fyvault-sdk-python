# fyvault

The official FyVault SDK for Python. Manage secrets, environments, rotating handles, integrations, and security scans.

## Install

```bash
pip install fyvault
```

Or install from source:

```bash
pip install git+https://github.com/FybyteTech/fyvault-sdk-python.git
```

## Quick Start

```python
from fyvault import FyVault

fv = FyVault(
    api_key="fv_live_...",
    org_id="org_acme",
    environment="production",  # optional
)

# Fetch a secret
db_url = fv.secrets.get_value_by_name("DATABASE_URL")
```

## Features

### Secrets

```python
# List all secrets in the current environment
secrets = fv.secrets.list()

# Get value by name
value = fv.secrets.get_value_by_name("STRIPE_KEY")

# Create
fv.secrets.create(
    name="API_KEY",
    secret_type="API_KEY",
    value="sk_live_...",
)

# Update
fv.secrets.update(secret_id, "new-value")

# Delete
fv.secrets.delete(secret_id)

# Versions
versions = fv.secrets.versions(secret_id)
```

### Secret Rotation

```python
# Auto-generate new value
result = fv.secrets.rotate(secret_id)
# result = {"secretId": "...", "name": "API_KEY", "version": 4}

# Custom value
fv.secrets.rotate(secret_id, new_value="custom-value")
```

### Rotating Handles

```python
# Mint a handle (5 min TTL)
handle = fv.secrets.get_handle("STRIPE_KEY", ttl_seconds=300)

# Resolve to real value
real_value = fv.secrets.resolve_handle(handle["handle"])

# Revoke early
fv.secrets.revoke_handle(handle["handle_id"])
```

### Environments

```python
# List
envs = fv.environments.list()

# Create
fv.environments.create(name="preview", description="PR previews")

# Set default
fv.environments.set_default(env_id)

# Delete
fv.environments.delete(env_id)
```

### Session Tokens

```python
# Mint a scoped session token
session = fv.access_tokens.create(ttl_seconds=900, scopes=["SECRETS_READ"])

# Use in another context
runner = FyVault(api_key=session["token"], org_id="org_acme")
```

### Security Scanner

```python
findings = fv.scanner.scan_text("AWS_KEY=AKIAIOSFODNN7EXAMPLE")
for f in findings:
    print(f"{f['confidence']}: {f['pattern_name']} on line {f['line_number']}")
```

### Integrations

```python
# Sync to Vercel
fv.integrations.sync("vercel", env_id, {"token": "...", "projectId": "prj_xxx"})

# Generate K8s manifest
result = fv.integrations.generate("k8s", env_id, {"name": "app-secrets"})
print(result["content"])

# Import from Doppler
fv.integrations.import_from_provider("doppler", doppler_json, env_id)

# Send Slack notification
fv.integrations.notify("slack", {"webhookUrl": "..."}, "Secret rotated")
```

### Devices

```python
devices = fv.devices.list()
fv.devices.register(name="prod-1", fingerprint="fp_...")
fv.devices.assign_secret(device_id, secret_id)
fv.devices.unassign_secret(device_id, secret_id)
fv.devices.revoke(device_id)
```

## Error Handling

```python
from fyvault import FyVault, FyVaultError

try:
    fv.secrets.get_value_by_name("MISSING")
except FyVaultError as e:
    print(e.status_code)  # 404
    print(e.code)         # "NOT_FOUND"
    print(str(e))         # "Secret not found"
```

## Environment Scoping

```python
# All operations scoped to staging
fv = FyVault(api_key="...", org_id="...", environment="staging")
db_url = fv.secrets.get_value_by_name("DATABASE_URL")  # staging value
```

## API Reference

| Resource | Methods |
|----------|---------|
| `secrets` | `list`, `get`, `get_by_name`, `get_value`, `get_value_by_name`, `create`, `update`, `delete`, `versions`, `rotate`, `get_handle`, `resolve_handle`, `revoke_handle` |
| `environments` | `list`, `get`, `create`, `update`, `delete`, `set_default` |
| `devices` | `list`, `get`, `register`, `update`, `revoke`, `assign_secret`, `unassign_secret` |
| `access_tokens` | `create`, `revoke` |
| `scanner` | `scan_text` |
| `integrations` | `sync`, `generate`, `import_from_provider`, `notify` |
| `orgs` | `get` |

## Links

- [FyVault Dashboard](https://fyvault.com)
- [Documentation](https://fyvault.com/docs)
- [Node.js SDK](https://github.com/FybyteTech/fyvault-sdk-node)

## License

Proprietary. Copyright 2026 Fybyte.
