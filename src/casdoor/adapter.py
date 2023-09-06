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

from src.casdoor import CasdoorSDK


class Adapter:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.type = "string"
        self.databaseType = "string"
        self.host = "string"
        self.port = 0
        self.user = "string"
        self.password = "string"
        self.database = "string"
        self.table = "string"
        self.tableNamePrefix = "string"
        self.isEnabled = True

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class AdapterSDK(CasdoorSDK):
    def get_adapters(self) -> List[Dict]:
        """
        Get the adapters from Casdoor.

        :return: a list of dicts containing adapter info
        """
        url = self.endpoint + "/api/get-adapters"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        adapters = r.json()
        return adapters

    def get_adapter(self, adapter_id: str) -> Dict:
        """
        Get the adapter from Casdoor providing the adapter_id.

        :param adapter_id: the id of the adapter
        :return: a dict that contains adapter's info
        """
        url = self.endpoint + "/api/get-adapter"
        params = {
            "id": f"{self.org_name}/{adapter_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        adapter = r.json()
        return adapter

    def modify_adapter(self, method: str, adapter: Adapter) -> Dict:
        url = self.endpoint + f"/api/{method}"
        adapter.owner = self.org_name
        params = {
            "id": f"{adapter.owner}/{adapter.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        adapter_info = json.dumps(adapter.to_dict())
        r = requests.post(url, params=params, data=adapter_info)
        response = r.json()
        return response

    def add_adapter(self, adapter: Adapter) -> Dict:
        response = self.modify_adapter("add-adapter", adapter)
        return response

    def update_adapter(self, adapter: Adapter) -> Dict:
        response = self.modify_adapter("update-adapter", adapter)
        return response

    def delete_adapter(self, adapter: Adapter) -> Dict:
        response = self.modify_adapter("delete-adapter", adapter)
        return response
