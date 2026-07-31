# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime
import json

import requests

API_PROD = "https://wl-api.mf.gov.pl"
API_TEST = "https://wl-test.mf.gov.pl"


class GovRejestrWL:
    use_prod_environment: bool = None

    def __init__(self, use_prod_environment: bool = False):
        self.use_prod_environment = use_prod_environment

    def get_api_url(self) -> str:
        if self.use_prod_environment:
            return API_PROD
        return API_TEST

    def _build_url(self, endpoint: str) -> str:
        url = self.get_api_url()
        separator = "/" if not url.endswith("/") and not endpoint.startswith("/") else ""
        return self.get_api_url() + separator + endpoint

    @staticmethod
    def separate_address_data(address: str) -> tuple[str, str, str]:
        """ŻNIWNA 5, 62-025 KOSTRZYN"""
        street, rest = address.split(",", 1) if address else (None, None)
        postal_code, city = rest.strip().split(" ", 1) if rest else (None, None)
        return street, postal_code, city

    def transform_data_address(self, input_data):
        subject = input_data.get("subject", {})
        street, postal_code, city = self.separate_address_data(subject.get("workingAddress", ""))
        if not street:
            street, postal_code, city = self.separate_address_data(subject.get("residenceAddress", ""))
        output_data = {
            "Ulica": street.title() if street else None,
            "Miejscowosc": city.title() if city else None,
            "KodPocztowy": postal_code,
            "Nip": subject.get("nip", None),
            "NrLokalu": street.split(" ")[-1],
            "Regon": subject.get("regon", None),
            "Nazwa": subject.get("name", None),
            "NrNieruchomosci": street.split(" ")[-1],
            "StatusNip": subject.get("statusVat", None),
            # nie osiąganlne dane z API GOV
            "DataZakonczeniaDzialalnosci": None,
            "MiejscowoscPoczty": None,
            "Wojewodztwo": None,
            "SilosID": None,
            "Powiat": None,
            "Gmina": None,
            "Typ": None,
        }
        return output_data

    def proces_search_data(self, endpoint, date: str = None, return_transformed: bool = True):
        url = self._build_url(endpoint)
        params = {"date": datetime.datetime.now().strftime("%Y-%m-%d") if not date else date}
        response = requests.request("GET", url, params=params)  # noqa: S113 — timeout policy stays with the caller
        try:
            response_body = json.loads(response.text)

        except Exception as err:
            raise ValueError("JSON decode error") from err

        if "result" in response_body:
            if not response_body["result"].get("subject", {}):
                raise ValueError("No data found")
            elif return_transformed:
                return self.transform_data_address(response_body["result"])
            else:
                return response_body["result"].get("subject", {})
        else:
            raise ValueError("Unrecoginzed response")

    def search_by_nip(self, nip: str, date: str = None, return_transformed: bool = True):
        endpoint = f"/api/search/nip/{nip}/"
        return self.proces_search_data(endpoint, date, return_transformed)

    def search_by_regon(self, regon: str, date: str = None, return_transformed: bool = True):
        endpoint = f"/api/search/regon/{regon}"
        return self.proces_search_data(endpoint, date, return_transformed)
