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
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.category = "string"
        self.type = "string"
        self.subType = "string"
        self.method = "string"
        self.clientId = "string"
        self.clientSecret = "string"
        self.clientId2 = "string"
        self.clientSecret2 = "string"
        self.cert = "string"
        self.customAuthUrl = "string"
        self.customTokenUrl = "string"
        self.customUserInfoUrl = "string"
        self.customLogo = "string"
        self.scopes = "string"
        self.userMapping = {"string": "string"}
        self.host = "string"
        self.port = 0
        self.disableSsl = True
        self.title = "string"
        self.content = "string"
        self.receiver = "string"
        self.regionId = "string"
        self.signName = "string"
        self.templateCode = "string"
        self.appId = "string"
        self.endpoint = "string"
        self.intranetEndpoint = "string"
        self.domain = "string"
        self.bucket = "string"
        self.pathPrefix = "string"
        self.metadata = "string"
        self.idP = "string"
        self.issuerUrl = "string"
        self.enableSignAuthnRequest = False
        self.providerUrl = "string"

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
        providers = r.json()
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
        provider = r.json()
        return provider

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
