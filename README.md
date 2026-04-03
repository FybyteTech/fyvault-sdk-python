# fyvault

Official Python SDK for [FyVault](https://fyvault.dev).

## Install

```bash
pip install fyvault
```

## Usage

```python
from fyvault import FyVault

client = FyVault(api_key="your-api-key")

# List secrets
secrets = client.secrets.list()

# Get a secret
secret = client.secrets.get("my-secret")
```

## Related

- [fyvault-cloud](https://github.com/fybyte/fyvault-cloud) — Cloud API
- [fyvault-node](https://github.com/fybyte/fyvault-node) — Node.js SDK
- [fyvault-agent](https://github.com/fybyte/fyvault-agent) — Agent & CLI
- [fyvault](https://github.com/fybyte/fyvault) — Frontend dashboard

## License

Proprietary. All rights reserved.
