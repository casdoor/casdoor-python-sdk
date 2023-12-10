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


class Provider:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.category = ""
        self.type = ""
        self.subType = ""
        self.method = ""
        self.clientId = ""
        self.clientSecret = ""
        self.clientId2 = ""
        self.clientSecret2 = ""
        self.cert = ""
        self.customAuthUrl = ""
        self.customTokenUrl = ""
        self.customUserInfoUrl = ""
        self.customLogo = ""
        self.scopes = ""
        self.userMapping = {"": ""}
        self.host = ""
        self.port = 0
        self.disableSsl = False
        self.title = ""
        self.content = ""
        self.receiver = ""
        self.regionId = ""
        self.signName = ""
        self.templateCode = ""
        self.appId = ""
        self.endpoint = ""
        self.intranetEndpoint = ""
        self.domain = ""
        self.bucket = ""
        self.pathPrefix = ""
        self.metadata = ""
        self.idP = ""
        self.issuerUrl = ""
        self.enableSignAuthnRequest = False
        self.providerUrl = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name, category, type):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.category = category
        self.type = type
        return self

    @classmethod
    def from_dict(cls, d: dict):
        if not d:
            return None
        provider = cls()
        for key, value in d.items():
            if hasattr(provider, key):
                setattr(provider, key, value)
        return provider

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _ProviderSDK:
    def get_providers(self) -> List[Dict]:
        """
        Get the providers from Casdoor.

        :return: a list of dicts containing provider info
        """
        url = self.endpoint + "/api/get-providers"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        providers = []
        for provider in response["data"]:
            providers.append(Provider.from_dict(provider))
        return providers

    def get_provider(self, provider_id: str) -> Dict:
        """
        Get the provider from Casdoor providing the provider_id.

        :param provider_id: the id of the provider
        :return: a dict that contains provider's info
        """
        url = self.endpoint + "/api/get-provider"
        params = {
            "id": f"{self.org_name}/{provider_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])

        return Provider.from_dict(response["data"])

    def modify_provider(self, method: str, provider: Provider) -> Dict:
        url = self.endpoint + f"/api/{method}"
        provider.owner = self.org_name
        params = {
            "id": f"{provider.owner}/{provider.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        provider_info = json.dumps(provider.to_dict())
        r = requests.post(url, params=params, data=provider_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def add_provider(self, provider: Provider) -> Dict:
        response = self.modify_provider("add-provider", provider)
        return response

    def update_provider(self, provider: Provider) -> Dict:
        response = self.modify_provider("update-provider", provider)
        return response

    def delete_provider(self, provider: Provider) -> Dict:
        response = self.modify_provider("delete-provider", provider)
        return response
