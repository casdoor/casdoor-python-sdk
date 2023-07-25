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
from typing import List, Optional

from cryptography import x509
from cryptography.hazmat.backends import default_backend

import jwt

import requests

from .user import User


class CasdoorSDK:
    def __init__(
        self,
        endpoint: str,
        client_id: str,
        client_secret: str,
        certificate: str,
        org_name: str,
        application_name: str,
        front_endpoint: str = None
    ):
        self.endpoint = endpoint
        if front_endpoint:
            self.front_endpoint = front_endpoint
        else:
            self.front_endpoint = endpoint.replace(":8000", ":7001")
        self.client_id = client_id
        self.client_secret = client_secret
        self.certificate = certificate
        self.org_name = org_name
        self.application_name = application_name
        self.grant_type = "authorization_code"

        self.algorithms = ["RS256"]

    @property
    def certification(self) -> bytes:
        if type(self.certificate) is not str:
            raise TypeError("certificate field must be str type")
        return self.certificate.encode("utf-8")

    def get_auth_link(
            self,
            redirect_uri: str,
            response_type: str = "code",
            scope: str = "read"
    ):
        url = self.front_endpoint + "/login/oauth/authorize"
        params = {
            "client_id": self.client_id,
            "response_type": response_type,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": self.application_name,
        }
        r = requests.request("", url, params=params)
        return r.url

    def get_oauth_token(
            self,
            code: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None
    ) -> dict:
        """
        Request the Casdoor server to get OAuth token.
        Must be set code or username and password for grant type.
        If nothing is set then client credentials grant will be used.

        :param code: the code that sent from Casdoor using redirect url back
                     to your server.
        :param username: casdoor username
        :param password: username password
        :return: token: OAuth token
        """
        response = self.oauth_token_request(code, username, password)
        token = response.json()

        return token

    def _get_payload_for_access_token_request(
            self,
            code: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None
    ) -> dict:
        """
        Return payload for request body which was selecting by strategy.
        """
        if code:
            return self.__get_payload_for_authorization_code(code=code)
        elif username and password:
            return self.__get_payload_for_password_credentials(
                username=username,
                password=password
            )
        else:
            return self.__get_payload_for_client_credentials()

    def __get_payload_for_authorization_code(self, code: str) -> dict:
        """
        Return payload for auth request with authorization code
        """
        return {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }

    def __get_payload_for_password_credentials(
            self,
            username: str,
            password: str
    ) -> dict:
        """
        Return payload for auth request with resource owner password
        credentials.
        """
        return {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": username,
            "password": password
        }

    def __get_payload_for_client_credentials(self) -> dict:
        """
        Return payload for auth request with client credentials.
        """
        return {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

    def oauth_token_request(
            self,
            code: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None
    ) -> requests.Response:
        """
        Request the Casdoor server to get access_token.
        Must be set code or username and password for grant type.
        If nothing is set then client credentials grant will be used.
        Returns full response as dict.

        :param code: the code that sent from Casdoor using redirect url
                     back to your server.
        :param username: Casdoor username
        :param password: username password
        :return: Response from Casdoor
        """
        params = self._get_payload_for_access_token_request(
            code=code,
            username=username,
            password=password
        )
        return self._oauth_token_request(payload=params)

    def _oauth_token_request(self, payload: dict) -> requests.Response:
        """
        Request the Casdoor server to get access_token.

        :param payload: Body for POST request.
        :return: Response from Casdoor
        """
        url = self.endpoint + "/api/login/oauth/access_token"
        response = requests.post(url, payload)
        return response

    def refresh_token_request(
            self,
            refresh_token: str,
            scope: str = ""
    ) -> requests.Response:
        """
        Request the Casdoor server to get access_token.

        :param refresh_token: refresh_token for send to Casdoor
        :param scope: OAuth scope
        :return: Response from Casdoor
        """
        url = self.endpoint + "/api/login/oauth/refresh_token"
        params = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": scope,
            "refresh_token": refresh_token,
        }
        return requests.post(url, params)

    def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        """
        Request the Casdoor server to get access_token.

        :param refresh_token: refresh_token for send to Casdoor
        :param scope: OAuth scope
        :return: Response from Casdoor
        """
        r = self.refresh_token_request(refresh_token, scope)
        access_token = r.json().get("access_token")

        return access_token

    def parse_jwt_token(self, token: str, **kwargs) -> dict:
        """
        Converts the returned access_token to real data using
        jwt (JSON Web Token) algorithms.

        :param token: access_token
        :return: the data in dict format
        """
        certificate = x509.load_pem_x509_certificate(
            self.certification,
            default_backend()
        )

        return_json = jwt.decode(
            token,
            certificate.public_key(),
            algorithms=self.algorithms,
            audience=self.client_id,
            **kwargs
        )
        return return_json

    def enforce(
            self,
            permission_model_name: str,
            sub: str,
            obj: str,
            act: str,
            v3: Optional[str] = None,
            v4: Optional[str] = None,
            v5: Optional[str] = None,
    ) -> bool:
        """
        Send data to Casdoor enforce API

        :param permission_model_name: Name permission model
        :param sub: sub from Casbin
        :param obj: obj from Casbin
        :param act: act from Casbin
        :param v3: v3 from Casbin
        :param v4: v4 from Casbin
        :param v5: v5 from Casbin
        """
        url = self.endpoint + "/api/enforce"
        query_params = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }
        params = {
            "id": permission_model_name,
            "v0": sub,
            "v1": obj,
            "v2": act,
            "v3": v3,
            "v4": v4,
            "v5": v5,
        }
        r = requests.post(url, json=params, params=query_params)
        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "Casdoor response error:\n" + str(r.text)
            raise ValueError(error_str)

        has_permission = r.json()

        if not isinstance(has_permission, bool):
            error_str = "Casdoor response error:\n" + r.text
            raise ValueError(error_str)

        return has_permission

    def batch_enforce(
            self,
            permission_model_name: str,
            permission_rules: list[list[str]]
    ) -> list[bool]:
        """
        Send data to Casdoor enforce API

        :param permission_model_name: Name permission model
        :param permission_rules: permission rules to enforce
                        [][0] -> sub: sub from Casbin
                        [][1] -> obj: obj from Casbin
                        [][2] -> act: act from Casbin
                        [][3] -> v3: v3 from Casbin (optional)
                        [][4] -> v4: v4 from Casbin (optional)
                        [][5] -> v5: v5 from Casbin (optional)
        """
        url = self.endpoint + "/api/batch-enforce"
        query_params = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }

        def map_rule(rule: list[str], idx) -> dict:
            if len(rule) < 3:
                raise ValueError("Invalid permission rule[{0}]: {1}"
                                 .format(idx, rule))
            result = {
                "id": permission_model_name
            }
            for i in range(0, len(rule)):
                result.update({"v{0}".format(i): rule[i]})
            return result
        params = [map_rule(permission_rules[i], i)
                  for i in range(0, len(permission_rules))]
        r = requests.post(url, json=params, params=query_params)
        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "Casdoor response error:\n" + str(r.text)
            raise ValueError(error_str)

        enforce_results = r.json()

        if not isinstance(enforce_results, list) or \
           len(enforce_results) == 0 or \
           not isinstance(enforce_results[0], bool):
            error_str = "Casdoor response error:\n" + r.text
            raise ValueError(error_str)

        return enforce_results

    def get_users(self) -> List[dict]:
        """
        Get the users from Casdoor.

        :return: a list of dicts containing user info
        """
        url = self.endpoint + "/api/get-users"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        users = r.json()
        return users

    def get_user(self, user_id: str) -> dict:
        """
        Get the user from Casdoor providing the user_id.

        :param user_id: the id of the user
        :return: a dict that contains user's info
        """
        url = self.endpoint + "/api/get-user"
        params = {
            "id": f"{self.org_name}/{user_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        user = r.json()
        return user

    def get_user_count(self, is_online: bool = None) -> int:
        """
        Get the count of filtered users for an organization
        :param is_online: True for online users, False for offline users,
                          None for all users
        :return: the count of filtered users for an organization
        """
        url = self.endpoint + "/api/get-user-count"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }

        if is_online is None:
            params["isOnline"] = ""
        else:
            params["isOnline"] = "1" if is_online else "0"

        r = requests.get(url, params)
        count = r.json()
        return count

    def modify_user(self, method: str, user: User) -> dict:
        url = self.endpoint + f"/api/{method}"
        user.owner = self.org_name
        params = {
            "id": f"{user.owner}/{user.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        user_info = json.dumps(user.to_dict())
        r = requests.post(url, params=params, data=user_info)
        response = r.json()
        return response

    def add_user(self, user: User) -> dict:
        response = self.modify_user("add-user", user)
        return response

    def update_user(self, user: User) -> dict:
        response = self.modify_user("update-user", user)
        return response

    def delete_user(self, user: User) -> dict:
        response = self.modify_user("delete-user", user)
        return response
