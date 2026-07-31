# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Offline suite — the registry API is mocked at the requests.request boundary.

import json
from unittest.mock import Mock, patch

import pytest

from gov_rejestr_wl_sdk.services.client import API_PROD, API_TEST, GovRejestrWL

FAKE_NIP = "0000000000"
FAKE_SUBJECT = {
    "nip": FAKE_NIP,
    "regon": "000000000",
    "name": "EXAMPLE SP. Z O.O.",
    "statusVat": "Czynny",
    "workingAddress": "ŻNIWNA 5, 62-025 KOSTRZYN",
}


def _response(payload: dict) -> Mock:
    return Mock(text=json.dumps(payload))


def test_api_url_switches_on_environment():
    assert GovRejestrWL(use_prod_environment=True).get_api_url() == API_PROD
    assert GovRejestrWL().get_api_url() == API_TEST


def test_separate_address_data():
    street, postal_code, city = GovRejestrWL.separate_address_data("ŻNIWNA 5, 62-025 KOSTRZYN")
    assert (street, postal_code, city) == ("ŻNIWNA 5", "62-025", "KOSTRZYN")


def test_search_by_nip_transformed():
    with patch("gov_rejestr_wl_sdk.services.client.requests.request") as request:
        request.return_value = _response({"result": {"subject": FAKE_SUBJECT}})
        result = GovRejestrWL().search_by_nip(FAKE_NIP)

    url = request.call_args.args[1]
    assert url == f"{API_TEST}/api/search/nip/{FAKE_NIP}/"
    assert result["Nip"] == FAKE_NIP
    assert result["Miejscowosc"] == "Kostrzyn"
    assert result["KodPocztowy"] == "62-025"
    assert result["StatusNip"] == "Czynny"


def test_search_by_regon_raw():
    with patch("gov_rejestr_wl_sdk.services.client.requests.request") as request:
        request.return_value = _response({"result": {"subject": FAKE_SUBJECT}})
        result = GovRejestrWL().search_by_regon("000000000", return_transformed=False)

    assert result == FAKE_SUBJECT


def test_empty_subject_raises():
    with patch("gov_rejestr_wl_sdk.services.client.requests.request") as request:
        request.return_value = _response({"result": {"subject": {}}})
        with pytest.raises(ValueError, match="No data found"):
            GovRejestrWL().search_by_nip(FAKE_NIP)


def test_unrecognized_response_raises():
    with patch("gov_rejestr_wl_sdk.services.client.requests.request") as request:
        request.return_value = _response({"error": "boom"})
        with pytest.raises(ValueError, match="Unrecoginzed response"):
            GovRejestrWL().search_by_nip(FAKE_NIP)


def test_invalid_json_raises():
    with patch("gov_rejestr_wl_sdk.services.client.requests.request") as request:
        request.return_value = Mock(text="not-json")
        with pytest.raises(ValueError, match="JSON decode error"):
            GovRejestrWL().search_by_nip(FAKE_NIP)
