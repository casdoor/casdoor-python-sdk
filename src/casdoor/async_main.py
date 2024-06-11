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

import base64
from typing import Dict, List, Optional

import aiohttp
import jwt
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from yarl import URL

from .user import User


class AioHttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = None

    async def fetch(self, path, method="GET", **kwargs):
        url = self.base_url + path
        async with self.session.request(method, url, **kwargs) as response:
            if response.status != 200 and "application/json" not in response.headers["Content-Type"]:
                raise ValueError(f"Casdoor response error:{response.text}")
            return await response.json()

    async def get(self, path, **kwargs):
        return await self.fetch(path, method="GET", **kwargs)

    async def post(self, path, **kwargs):
        return await self.fetch(path, method="POST", **kwargs)

    async def __aenter__(self):
        self.session = await aiohttp.ClientSession().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                raise exc_val
        finally:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)


class AsyncCasdoorSDK:
    def __init__(
        self,
        endpoint: str,
        client_id: str,
        client_secret: str,
        certificate: str,
        org_name: str,
        application_name: str,
        front_endpoint: str = None,
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
        self._session = AioHttpClient(base_url=self.endpoint)

    @property
    def headers(self) -> Dict:
        basic_auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {basic_auth}",
        }

    @property
    def certification(self) -> bytes:
        if not isinstance(self.certificate, str):
            raise TypeError("certificate field must be str type")
        return self.certificate.encode("utf-8")

    async def get_auth_link(
        self,
        redirect_uri: str,
        response_type: str = "code",
        scope: str = "read",
    ) -> str:
        url = self.front_endpoint + "/login/oauth/authorize"
        params = {
            "client_id": self.client_id,
            "response_type": response_type,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": self.application_name,
        }
        return str(URL(url).with_query(params))

    async def get_oauth_token(
        self,
        code: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict:
        """
        Request the Casdoor server to get OAuth token.
        Must be set code or username and password for grant type.
        If nothing is set then client credentials grant will be used.

        :param code: the code that sent from Casdoor using redirect url
                     back to your server.
        :param username: Casdoor username
        :param password: username password
        :return: OAuth token
        """
        return await self.oauth_token_request(code, username, password)

    def _get_payload_for_access_token_request(
        self,
        code: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict:
        """
        Return payload for request body which was selecting by strategy.
        """
        if code:
            return self.__get_payload_for_authorization_code(code=code)
        elif username and password:
            return self.__get_payload_for_password_credentials(username=username, password=password)
        else:
            return self.__get_payload_for_client_credentials()

    def __get_payload_for_authorization_code(self, code: str) -> Dict:
        """
        Return payload for auth request with authorization code
        """
        return {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }

    def __get_payload_for_password_credentials(self, username: str, password: str) -> Dict:
        """
        Return payload for auth request with resource owner password
        credentials.
        """
        return {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": username,
            "password": password,
        }

    def __get_payload_for_client_credentials(self) -> Dict:
        """
        Return payload for auth request with client credentials.
        """
        return {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

    async def oauth_token_request(
        self,
        code: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict:
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
        params = self._get_payload_for_access_token_request(code=code, username=username, password=password)
        return await self._oauth_token_request(payload=params)

    async def _oauth_token_request(self, payload: Dict) -> Dict:
        """
        Request the Casdoor server to get access_token.

        :param payload: Body for POST request.
        :return: Response from Casdoor
        """
        path = "/api/login/oauth/access_token"
        async with self._session as session:
            return await session.post(path, data=payload)

    async def refresh_token_request(self, refresh_token: str, scope: str = "") -> Dict:
        """
        Request the Casdoor server to get access_token.

        :param refresh_token: refresh_token for send to Casdoor
        :param scope: OAuth scope
        :return: Response from Casdoor
        """
        path = "/api/login/oauth/refresh_token"
        params = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": scope,
            "refresh_token": refresh_token,
        }
        async with self._session as session:
            return await session.post(path, data=params)

    async def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        """
        Request the Casdoor server to get access_token.

        :param refresh_token: refresh_token for send to Casdoor
        :param scope: OAuth scope
        :return: Response from Casdoor
        """
        token = await self.refresh_token_request(refresh_token, scope)
        return token.get("access_token")

    def parse_jwt_token(self, token: str, **kwargs) -> Dict:
        """
        Converts the returned access_token to real data using
        jwt (JSON Web Token) algorithms.

        :param token: access_token
        :return: the data in dict format
        """
        certificate = x509.load_pem_x509_certificate(self.certification, default_backend())

        return_json = jwt.decode(
            token,
            certificate.public_key(),
            algorithms=self.algorithms,
            audience=self.client_id,
            **kwargs,
        )
        return return_json

    async def enforce(
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
        # https://casdoor.org/docs/permission/exposed-casbin-apis#enforce

        :param permission_model_name: Name permission model
        :param sub: sub from Casbin
        :param obj: obj from Casbin
        :param act: act from Casbin
        :param v3: v3 from Casbin
        :param v4: v4 from Casbin
        :param v5: v5 from Casbin
        """
        path = "/api/enforce"
        params = {
            "id": permission_model_name,
            "v0": sub,
            "v1": obj,
            "v2": act,
            "v3": v3,
            "v4": v4,
            "v5": v5,
        }
        async with self._session as session:
            has_permission = await session.post(path, headers=self.headers, json=params)
            if not isinstance(has_permission, bool):
                raise ValueError(f"Casdoor response error: {has_permission}")
            return has_permission

    async def batch_enforce(self, permission_model_name: str, permission_rules: List[List[str]]) -> List[bool]:
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
        path = "/api/batch-enforce"

        def map_rule(rule: List[str], idx) -> Dict:
            if len(rule) < 3:
                raise ValueError(f"Invalid permission rule[{idx}]: {rule}")
            result = {"id": permission_model_name}
            for i in range(len(rule)):
                result.update({f"v{i}": rule[i]})
            return result

        params = [map_rule(permission_rules[i], i) for i in range(len(permission_rules))]

        async with self._session as session:
            enforce_results = await session.post(path, headers=self.headers, json=params)
            if not isinstance(enforce_results, bool):
                raise ValueError(f"Casdoor response error:{enforce_results}")

            return enforce_results

    async def get_users(self) -> Dict:
        """
        Get the users from Casdoor.

        :return: a list of dicts containing user info
        """
        path = "/api/get-users"
        params = {"owner": self.org_name}
        async with self._session as session:
            users = await session.get(path, headers=self.headers, params=params)
            return users["data"]

    async def get_user(self, user_id: str) -> Dict:
        """
        Get the user from Casdoor providing the user_id.

        :param user_id: the id of the user
        :return: a dict that contains user's info
        """
        path = "/api/get-user"
        params = {"id": f"{self.org_name}/{user_id}"}
        async with self._session as session:
            user = await session.get(path, headers=self.headers, params=params)
            return user["data"]

    async def get_user_count(self, is_online: bool = None) -> int:
        """
        Get the count of filtered users for an organization
        :param is_online: True for online users, False for offline users,
                          None for all users
        :return: the count of filtered users for an organization
        """
        path = "/api/get-user-count"
        params = {
            "owner": self.org_name,
        }

        if is_online is None:
            params["isOnline"] = ""
        else:
            params["isOnline"] = "1" if is_online else "0"

        async with self._session as session:
            count = await session.get(path, headers=self.headers, params=params)
            return count["data"]

    async def modify_user(self, method: str, user: User, params=None) -> Dict:
        path = f"/api/{method}"
        async with self._session as session:
            return await session.post(path, params=params, headers=self.headers, json=user.to_dict())

    async def add_user(self, user: User) -> Dict:
        response = await self.modify_user("add-user", user)
        return response

    async def update_user(self, user: User) -> Dict:
        params = {"id": f"{user.owner}/{user.name}"}
        response = await self.modify_user("update-user", user, params)
        return response

    async def delete_user(self, user: User) -> Dict:
        response = await self.modify_user("delete-user", user)
        return response
