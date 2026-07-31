# GOV Rejestr WL SDK

SDK for the Polish government VAT taxpayers registry (Wykaz podatników VAT / GOV Rejestr WL) —
a REST client for `wl-api.mf.gov.pl` with NIP/REGON search and address parsing helpers.

## Install

```bash
uv pip install entirius-py-gov-rejestr-wl-sdk
```

Or as a dependency in `pyproject.toml`:

```toml
"entirius-py-gov-rejestr-wl-sdk>=2.0.0"
```

## Use

```python
from gov_rejestr_wl_sdk.services.client import GovRejestrWL

client = GovRejestrWL(use_prod_environment=True)  # False = sandbox API
```

## Development and testing

```bash
make install   # uv sync, incl. extras
make check     # ruff lint + format-check
make test      # pytest
```
