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
import json
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
        permission_id: str,
        model_id: str,
        resource_id: str,
        enforce_id: str,
        owner: str,
        casbin_request: Optional[List[str]] = None,
    ) -> bool:
        """
        Send data to Casdoor enforce API asynchronously

        :param permission_id: the permission id (i.e. organization name/permission name)
        :param model_id: the model id
        :param resource_id: the resource id
        :param enforce_id: the enforcer id (note: uses 'enforcerId' parameter in API)
        :param owner: the owner of the permission
        :param casbin_request: a list containing the request data (i.e. sub, obj, act)
        :return: a boolean value indicating whether the request is allowed
        """
        url = "/api/enforce"

        # Build params with only non-empty values
        # API requires exactly one of: permissionId, modelId, resourceId, enforcerId, owner
        params: Dict[str, str] = {}
        if permission_id:
            params["permissionId"] = permission_id
        if model_id:
            params["modelId"] = model_id
        if resource_id:
            params["resourceId"] = resource_id
        if enforce_id:
            params["enforcerId"] = enforce_id  # Fixed: was "enforceId"
        if owner:
            params["owner"] = owner

        # Validate exactly one parameter is provided
        if len(params) != 1:
            raise ValueError(
                "Exactly one of (permission_id, model_id, resource_id, enforce_id, owner) "
                "must be provided and non-empty. "
                f"Got {len(params)} parameters: {list(params.keys())}"
            )

        async with self._session as session:
            response = await session.post(
                url,
                params=params,
                data=json.dumps(casbin_request),
                auth=aiohttp.BasicAuth(self.client_id, self.client_secret),
                headers={"Content-Type": "application/json"},
            )

        if isinstance(response, dict):
            data = response.get("data")
            if isinstance(data, list) and len(data) > 0:
                has_permission = data[0]
            else:
                has_permission = response
        else:
            has_permission = response

        if not isinstance(has_permission, bool):
            error_str = f"Casdoor response error (invalid type {type(has_permission)}):\n{json.dumps(response)}"
            raise ValueError(error_str)

        return has_permission

    async def batch_enforce(
        self,
        permission_id: str,
        model_id: str,
        enforce_id: str,
        owner: str,
        casbin_request: Optional[List[List[str]]] = None,
    ) -> List[bool]:
        """
        Send data to Casdoor batch enforce API asynchronously

        :param permission_id: the permission id (i.e. organization name/permission name)
        :param model_id: the model id
        :param enforce_id: the enforcer id (note: uses 'enforcerId' parameter in API)
        :param owner: the owner of the permission
        :param casbin_request: a list of lists containing the request data
        :return: a list of boolean values indicating whether each request is allowed
        """
        url = "/api/batch-enforce"

        # Build params with only non-empty values
        # API requires exactly one of: permissionId, modelId, enforcerId, owner
        params: Dict[str, str] = {}
        if permission_id:
            params["permissionId"] = permission_id
        if model_id:
            params["modelId"] = model_id
        if enforce_id:
            params["enforcerId"] = enforce_id  # Fixed: was "enforceId"
        if owner:
            params["owner"] = owner

        # Validate exactly one parameter is provided
        if len(params) != 1:
            raise ValueError(
                "Exactly one of (permission_id, model_id, enforce_id, owner) "
                "must be provided and non-empty. "
                f"Got {len(params)} parameters: {list(params.keys())}"
            )

        async with self._session as session:
            response = await session.post(
                url,
                params=params,
                data=json.dumps(casbin_request),
                auth=aiohttp.BasicAuth(self.client_id, self.client_secret),
                headers={"Content-Type": "application/json"},
            )

        data = response.get("data")
        if data is None:
            error_str = "Casdoor response error: 'data' field is missing\n" + json.dumps(response)
            raise ValueError(error_str)

        if not isinstance(data, list):
            error_str = f"Casdoor 'data' is not a list (got {type(data)}):\n{json.dumps(response)}"
            raise ValueError(error_str)

        enforce_results = data[0] if data else []

        if (
            not isinstance(enforce_results, list)
            or len(enforce_results) > 0
            and not isinstance(enforce_results[0], bool)
        ):
            error_str = (
                f"Casdoor response contains invalid results (got {type(enforce_results)}):\n{json.dumps(response)}"
            )
            raise ValueError(error_str)

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
