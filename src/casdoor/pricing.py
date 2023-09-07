# Copyright 2021 The Casbin Authors. All Rights Reserved.
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

from .main import CasdoorSDK


class Pricing:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.description = "string"
        self.plans = ["string"]
        self.isEnabled = False
        self.trialDuration = 0
        self.application = "string"
        self.submitter = "string"
        self.approver = "string"
        self.approveTime = "string"
        self.state = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class PricingSDK(CasdoorSDK):
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
        pricings = r.json()
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
        pricing = r.json()
        return pricing

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
