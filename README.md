# Remnawave Python SDK

> [!WARNING]
> This repository is a fork of the official SDK [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).

[![Stars](https://img.shields.io/github/stars/remnashop/remnapy.svg?style=social)](https://github.com/remnashop/remnapy/stargazers)
[![Forks](https://img.shields.io/github/forks/remnashop/remnapy.svg?style=social)](https://github.com/remnashop/remnapy/network/members)
[![Issues](https://img.shields.io/github/issues/remnashop/remnapy.svg)](https://github.com/remnashop/remnapy/issues)
[![Release](https://img.shields.io/github/v/release/remnashop/remnapy)](https://github.com/remnashop/remnapy/releases)

A Python SDK client for interacting with the **[Remnawave API](https://docs.rw/)**.
This library simplifies working with the API by providing convenient controllers, Pydantic models for requests and responses, and fast serialization with `orjson`. 

## 📦 Installation

### Release
A release is a git tag; install it straight from GitHub:

```bash
pip install "remnapy @ git+https://github.com/remnashop/remnapy.git@v3.4.8"
```

With uv:

```toml
# pyproject.toml
[project]
dependencies = ["remnapy"]

[tool.uv.sources]
remnapy = { git = "https://github.com/remnashop/remnapy", tag = "v3.4.8" }
```

Releases up to 3.2.1 are also on PyPI; later ones are published only as tags.

### Unreleased
Code merged since the last release lives in the `production` branch:

```bash
pip install git+https://github.com/remnashop/remnapy.git@production
```

---

## 🫥 Compatible versions

The package version is the panel it covers in full: `remnapy` **3.4.8** has every endpoint and field of Remnawave **3.4.8**. It also works with every older 3.x panel, down to **3.0.0**. Both are checked offline against the panels' OpenAPI specs (`tests/spec/`, see [Tests](#-tests)).

| Package Version | Covered in full | Works with panels |
| --------------- | --------------- | ----------------- |
| 3.4.8           | 3.4.8           | 3.0.0 – 3.4.8     |
| 3.2.1           | 3.2.1           | 3.1.0 – 3.4.8 ¹   |

¹ Panel 3.4 ignores host squad exclusions sent by this release.

### Differences between panel versions

An endpoint a panel does not have answers with an API error (usually 404). A field it does not send is `None` or empty.

| Panel  | Added                                                                                                                                                                             |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3.1.0  | node `id`, subscription request `srr_response_type`                                                                                                                               |
| 3.2.0  | `system.get_configuration()`                                                                                                                                                      |
| 3.2.2  | node `ips`                                                                                                                                                                        |
| 3.2.3  | `snippets.sync_snippet()`, `cipher_suites` in resolved proxy configs                                                                                                              |
| 3.3.0  | `node_integrations`; shared lists and `sync_node_plugin()` in `node_plugins`; geocheck in `connections`; node `integration_uuids`; host `mapper`; SRR `respond_with_remarks` |
| 3.4.0  | `get_tags()` / `set_tags()` on config profiles, internal and external squads, node plugins, subpage configs and subscription templates; `get_shared_list_by_name()`, `delete_shared_list()`; host `internal_squads`; slashes in snippet names |
| 3.4.4  | `hosts.clone_host()`                                                                                                                                                              |

Host squads changed in 3.4.0: older panels take `excluded_internal_squads`, newer ones `internal_squads` (`EXCLUDE` or `ALLOW_ONLY` mode) and ignore the old field, which is always empty in their responses.

### Dependencies
- `rapid-api-client` (==0.6.0)
- `orjson` (>=3.10.15, <4.0.0)
- `httpx` (>=0.27.2, <0.28.0)
- `pydantic[email]` (>=2.9.2, <3.0.0)
- `pydantic-core` (>=2.33.1, <2.34.0)
- `cryptography` (>=46.0.3, <47.0.0)

## 🚀 Usage

Here’s a quick example to get you started:

```python
import os
import asyncio

from remnapy import RemnawaveSDK
from remnapy.models import (
    UsersResponseDto, 
    UserResponseDto,
    GetAllConfigProfilesResponseDto,
    CreateInternalSquadRequestDto
)

async def main():
    # URL to your panel (ex. https://vpn.com or http://127.0.0.1:3000)
    base_url: str = os.getenv("REMNAWAVE_BASE_URL")
    # Bearer Token from panel (section: API Tokens) 
    token: str = os.getenv("REMNAWAVE_TOKEN")

    # Initialize the SDK
    remnawave = RemnawaveSDK(base_url=base_url, token=token)

    # Fetch all users
    response: UsersResponseDto = await remnawave.users.get_all_users()
    total_users: int = response.total
    users: list[UserResponseDto] = response.users
    print("Total users: ", total_users)
    print("List of users: ", users)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧪 Tests

```bash
uv run pytest tests/test_spec_conformance.py tests/test_spec_compat.py
```

These run offline against the bundled OpenAPI specs:

- `test_spec_conformance.py` — the SDK matches panel 3.4.8, the version it covers in full (`tests/spec/remnawave-3.4.8.json`), endpoint for endpoint and field for field.
- `test_spec_compat.py` — the SDK keeps working with every panel in `tests/spec/`: each endpoint exists from the version listed in `ENDPOINT_SINCE`, every field the panel requires is sent, every response and webhook parses.

`tests/spec/` keeps the panels where something the SDK uses changed: 3.0.0, 3.1.0, 3.2.0, 3.2.2, 3.2.3, 3.3.0, 3.4.0, 3.4.4 and 3.4.8.

To check another panel version, add its spec (needs Docker; the panel runs on a throwaway database and is removed afterwards):

```bash
scripts/fetch-panel-spec.sh 3.4.8
```

The remaining tests call a live panel and read its address and fixtures from `.env` (see `tests/conftest.py`).

## ❤️ About

This SDK was originally developed by [@kesevone](https://github.com/kesevone) for integration with Remnawave's API.

Previously maintained by [@sm1ky](https://github.com/sm1ky) at [`sm1ky/remnawave-api`](https://github.com/sm1ky/remnawave-api).

The official Remnawave repository is located at [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).

This repository is a fork of the official SDK.
