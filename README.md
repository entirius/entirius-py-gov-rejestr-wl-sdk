# entirius-py-gov-rejestr-wl-sdk

A Python client for the Polish VAT taxpayers registry (Wykaz podatników VAT), part of
Entirius, the open-source modular ecommerce platform. It queries the public registry API at `wl-api.mf.gov.pl` by NIP
or REGON and can return the result as a flat company and address record.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-gov-rejestr-wl-sdk.svg)](https://pypi.org/project/entirius-py-gov-rejestr-wl-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-gov-rejestr-wl-sdk.svg)](https://pypi.org/project/entirius-py-gov-rejestr-wl-sdk/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-gov-rejestr-wl-sdk/blob/develop/LICENSE)

## What it does

- Looks up a taxpayer by NIP (`search_by_nip()`) or REGON (`search_by_regon()`), for today or for a given date.
- Returns the registry subject as received, or transformed into a flat company and address record
  (`return_transformed`).
- Splits a registry address into street, postal code and city (`separate_address_data()`).
- Switches between the production and the test API (`use_prod_environment`).

## Installation

```shell
uv add entirius-py-gov-rejestr-wl-sdk
pip install entirius-py-gov-rejestr-wl-sdk
```

The import name is `gov_rejestr_wl_sdk`.

## Quick start

```python
from gov_rejestr_wl_sdk.services.client import GovRejestrWL

client = GovRejestrWL(use_prod_environment=True)  # False = the test API
company = client.search_by_nip("1234567890")  # raises ValueError when nothing is found
print(company["Nazwa"], company["StatusNip"])
```

## Requirements

- Python 3.11 or newer.
- `requests` (installed as a dependency).
- Outbound HTTPS to `wl-api.mf.gov.pl`.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-gov-rejestr-wl-sdk/blob/develop/CHANGELOG.md

## Part of Entirius

This SDK is the VAT registry client of the Entirius backend service (Volkanos) and its modules.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Consumer module: https://github.com/entirius/entirius-django-regon-api

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: https://github.com/entirius/entirius-py-gov-rejestr-wl-sdk/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-gov-rejestr-wl-sdk/blob/develop/LICENSE.
