# Copyright 2021 The Casdoor Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import Dict, List

import requests


class Pricing:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.description = ""
        self.plans = [""]
        self.isEnabled = False
        self.trialDuration = 0
        self.application = ""
        self.submitter = ""
        self.approver = ""
        self.approveTime = ""
        self.state = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name, description, application):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.description = description
        self.application = application
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        pricing = cls()
        for key, value in data.items():
            if hasattr(pricing, key):
                setattr(pricing, key, value)
        return pricing

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _PricingSDK:
    def get_pricings(self) -> List[Dict]:
        """
        Get the pricings from Casdoor.

        :return: a list of dicts containing pricing info
        """
        url = self.endpoint + "/api/get-pricings"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        pricings = []
        for pricing in response["data"]:
            pricings.append(Pricing.from_dict(pricing))
        return pricings

    def get_pricing(self, pricing_id: str) -> Dict:
        """
        Get the pricing from Casdoor providing the pricing_id.

        :param pricing_id: the id of the pricing
        :return: a dict that contains pricing's info
        """
        url = self.endpoint + "/api/get-pricing"
        params = {
            "id": f"{self.org_name}/{pricing_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])

        return Pricing.from_dict(response["data"])

    def modify_pricing(self, method: str, pricing: Pricing) -> Dict:
        url = self.endpoint + f"/api/{method}"
        pricing.owner = self.org_name
        params = {
            "id": f"{pricing.owner}/{pricing.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        pricing_info = json.dumps(pricing.to_dict())
        r = requests.post(url, params=params, data=pricing_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def add_pricing(self, pricing: Pricing) -> Dict:
        response = self.modify_pricing("add-pricing", pricing)
        return response

    def update_pricing(self, pricing: Pricing) -> Dict:
        response = self.modify_pricing("update-pricing", pricing)
        return response

    def delete_pricing(self, pricing: Pricing) -> Dict:
        response = self.modify_pricing("delete-pricing", pricing)
        return response
