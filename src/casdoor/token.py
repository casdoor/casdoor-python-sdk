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


class Token:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.application = ""
        self.organization = ""
        self.user = ""
        self.code = ""
        self.accessToken = ""
        self.refreshToken = ""
        self.expiresIn = 0
        self.scope = ""
        self.tokenType = ""
        self.codeChallenge = ""
        self.codeIsUsed = False
        self.codeExpireIn = 0

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _TokenSDK:
    def get_tokens(self, p, page_size) -> List[Dict]:
        """
        Get the tokens from Casdoor.

        :return: a list of dicts containing token info
        """
        url = self.endpoint + "/api/get-tokens"
        params = {
            "owner": self.org_name,
            "p": str(p),
            "pageSize": str(page_size),
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        tokens = r.json()
        return tokens

    def get_token(self, token_id: str) -> Dict:
        """
        Get the token from Casdoor providing the token_id.

        :param token_id: the id of the token
        :return: a dict that contains token's info
        """
        url = self.endpoint + "/api/get-token"
        params = {
            "id": f"{self.org_name}/{token_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        token = r.json()
        return token

    def modify_token(self, method: str, token: Token) -> Dict:
        url = self.endpoint + f"/api/{method}"
        token.owner = self.org_name
        params = {
            "id": f"{token.owner}/{token.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        token_info = json.dumps(token.to_dict())
        r = requests.post(url, params=params, data=token_info)
        response = r.json()
        return response

    def add_token(self, token: Token) -> Dict:
        response = self.modify_token("add-token", token)
        return response

    def update_token(self, token: Token) -> Dict:
        response = self.modify_token("update-token", token)
        return response

    def delete_token(self, token: Token) -> Dict:
        response = self.modify_token("delete-token", token)
        return response
