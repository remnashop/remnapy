# Remnawave Python SDK

> [!WARNING]
> This repository is a fork of the official SDK [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).

[![Stars](https://img.shields.io/github/stars/remnashop/remnapy.svg?style=social)](https://github.com/remnashop/remnapy/stargazers)
[![Forks](https://img.shields.io/github/forks/remnashop/remnapy.svg?style=social)](https://github.com/remnashop/remnapy/network/members)
[![Issues](https://img.shields.io/github/issues/remnashop/remnapy.svg)](https://github.com/remnashop/remnapy/issues)
[![Supported python versions](https://img.shields.io/pypi/pyversions/remnapy.svg)](https://pypi.python.org/pypi/remnapy)
[![Downloads](https://img.shields.io/pypi/dm/remnapy.svg)](https://pypi.python.org/pypi/remnapy)
[![PyPi Package Version](https://img.shields.io/pypi/v/remnapy)](https://pypi.python.org/pypi/remnapy)

A Python SDK client for interacting with the **[Remnawave API](https://docs.rw/)**.
This library simplifies working with the API by providing convenient controllers, Pydantic models for requests and responses, and fast serialization with `orjson`. 

## 📦 Installation

### Release
Install the latest release from PyPI:

```bash
pip install remnapy
```

Pin the SDK line you build against:

```toml
# pyproject.toml
dependencies = ["remnapy (>=3.2.1, <3.3.0)"]
```

### Unreleased
Code merged since the last release lives in the `production` branch:

```bash
pip install git+https://github.com/remnashop/remnapy.git@production
```

---

## 🫥 Compatible versions

The package version names its **target** panel — the version it covers endpoint for endpoint and field for field: `remnapy` **3.2.1** targets Remnawave **3.2.1**.

Every call the SDK has also works with the other panels of the 3.x line, from **3.0.0** through **3.4.8**. That is checked offline against each panel's OpenAPI spec (`tests/spec/`, see [Tests](#-tests)).

| Package Version | Target panel | Works with panels |
| --------------- | ------------ | ----------------- |
| unreleased      | 3.2.1        | 3.0.0 – 3.4.8     |
| 3.2.1           | 3.2.1        | 3.1.0 – 3.4.8 ¹   |

¹ Panel 3.4 ignores host squad exclusions sent by this release.

### Differences between panel versions

- **3.0.0** — nodes have no numeric `id` and subscription requests no `srr_response_type`: those fields are `None`. `system.get_configuration()` arrived in 3.2.0.
- **3.3.0+** — hosts gained `mapper`, per-client rewrites of the generated config.
- **3.4.0+** — hosts pick visible internal squads through `internal_squads` (`EXCLUDE` or `ALLOW_ONLY` mode). `excluded_internal_squads` is ignored by these panels and always empty in their responses; on older panels it is the only option.
- Endpoints added after 3.2.1 (tags of profiles, squads, plugins and templates; node integrations; shared lists; host cloning; geocheck; sync actions) are not in the SDK yet.

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

- `test_spec_conformance.py` — the SDK matches its target panel (`tests/spec/remnawave-3.2.1.json`) field for field.
- `test_spec_compat.py` — the SDK keeps working with every panel in `tests/spec/`: each endpoint it calls exists, every field the panel requires is sent, every response and webhook parses.

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
