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

import requests
import jwt
import json
from .user import User
from typing import List
from cryptography import x509
from cryptography.hazmat.backends import default_backend


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
            raise TypeError('certificate field must be str type')
        return self.certificate.encode('utf-8')

    def get_auth_link(self, redirect_uri: str, response_type: str = "code", scope: str = "read"):
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

    def get_oauth_token(self, code: str) -> str:
        """
        Request the Casdoor server to get access_token.
        :param code: the code that sent from Casdoor using redirect url back to your server.
        :return: access_token
        """
        r = self.oauth_token_request(code)
        access_token = r.json().get("access_token")

        return access_token

    def oauth_token_request(self, code: str) -> requests.Response:
        """
        Request the Casdoor server to get access_token.
        :param code: the code that sent from Casdoor using redirect url back to your server.
        :return: Response from Casdoor
        """
        url = self.endpoint + "/api/login/oauth/access_token"
        params = {
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }
        return requests.post(url, params)

    def refresh_token_request(self, refresh_token: str, scope: str = "") -> requests.Response:
        """
        Request the Casdoor server to get access_token.
        :param refresh_token: refresh_token for send to Casdoor
        :param scope: OAuth scope
        :return: Response from Casdoor
        """
        url = self.endpoint + "/api/login/oauth/refresh_token"
        params = {
            "grant_type": self.grant_type,
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

    def parse_jwt_token(self, token: str) -> dict:
        """
        Converts the returned access_token to real data using jwt (JSON Web Token) algorithms.
        :param token: access_token
        :return: the data in dict format
        """
        certificate = x509.load_pem_x509_certificate(self.certification, default_backend())

        return_json = jwt.decode(
            token,
            certificate.public_key(),
            algorithms=self.algorithms,
            audience=self.client_id,
        )
        return return_json

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
