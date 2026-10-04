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
from typing import Dict, List, Optional

import requests

from .util import get_admin_id, get_owner


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
        self.idToken = ""
        self.accessTokenHash = ""
        self.refreshTokenHash = ""
        self.idTokenHash = ""
        self.grantType = ""
        self.resource = ""
        self.dPoPJkt = ""
        self.sessionId = ""

    @classmethod
    def new(
        cls,
        owner,
        name,
        created_time,
        application,
        organization,
        user,
        code,
        access_token,
        refresh_token,
        expires_in,
        scope,
        token_type,
        code_challenge,
        code_is_used,
        code_expire_in,
    ):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.application = application
        self.organization = organization
        self.user = user
        self.code = code
        self.accessToken = access_token
        self.refreshToken = refresh_token
        self.expiresIn = expires_in
        self.scope = scope
        self.tokenType = token_type
        self.codeChallenge = code_challenge
        self.codeIsUsed = code_is_used
        self.codeExpireIn = code_expire_in
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        token = cls()
        for key, value in data.items():
            if hasattr(token, key):
                setattr(token, key, value)
        return token

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _TokenSDK:
    def get_tokens(self, p=None, page_size=None) -> List[Dict]:
        """
        Get the tokens from Casdoor.

        :return: a list of dicts containing token info
        """
        url = self.endpoint + "/api/get-tokens"
        params = {
            "owner": "admin",
            "p": None if p is None else str(p),
            "pageSize": None if page_size is None else str(page_size),
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        tokens = []
        for token in response["data"]:
            tokens.append(Token.from_dict(token))
        return tokens

    def get_token(self, token_id: str) -> Dict:
        """
        Get the token from Casdoor providing the token_id.

        :param token_id: the id of the token
        :return: a dict that contains token's info
        """
        url = self.endpoint + "/api/get-token"
        params = {
            "id": get_admin_id(token_id),
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Token.from_dict(response["data"])

    def modify_token(self, method: str, token: Token, columns: Optional[List[str]] = None) -> Dict:
        url = self.endpoint + f"/api/{method}"
        token.owner = get_owner(token.owner, "admin")
        params = {
            "id": f"{token.owner}/{token.name}",
            "columns": ",".join(columns) if columns else None,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        token_info = json.dumps(token.to_dict())
        r = self._http_post(url, params=params, data=token_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def get_pagination_tokens(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the tokens from Casdoor.

        :param p: the page number, starting from 1
        :param page_size: the count of tokens in a page
        :param query_map: the filters, e.g. {"field": "name", "value": "abc", "sortOrder": "descend"}
        :return: a tuple of the list of Token objects and the total count
        """
        data, total = self.get_pagination("get-tokens", p, page_size, query_map, owner="admin")
        return [Token.from_dict(item) for item in data or []], total

    def update_token_for_columns(self, token: Token, columns: List[str]) -> Dict:
        """
        Only update the given columns of the token, e.g. ["display_name"].
        """
        return self.modify_token("update-token", token, columns)

    def introspect_token(self, token: str, token_type_hint: str = "access_token") -> Dict:
        """
        Introspect the token (RFC 7662), the result contains "active" and the claims of the token.
        """
        url = self.endpoint + "/api/login/oauth/introspect"
        r = requests.post(
            url,
            data={"token": token, "token_type_hint": token_type_hint},
            auth=(self.client_id, self.client_secret),
            headers=self.custom_headers,
            verify=self.verify,
        )
        return r.json()

    def add_token(self, token: Token) -> Dict:
        response = self.modify_token("add-token", token)
        return response

    def update_token(self, token: Token) -> Dict:
        response = self.modify_token("update-token", token)
        return response

    def delete_token(self, token: Token) -> Dict:
        response = self.modify_token("delete-token", token)
        return response
