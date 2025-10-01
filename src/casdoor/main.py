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

import jwt
import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from .adapter import _AdapterSDK
from .application import _ApplicationSDK
from .cert import _CertSDK
from .enforcer import _EnforcerSDK
from .group import _GroupSDK
from .model import _ModelSDK
from .organization import _OrganizationSDK
from .payment import _PaymentSDK
from .permission import _PermissionSDK
from .plan import _PlanSDK
from .pricing import _PricingSDK
from .product import _ProductSDK
from .provider import _ProviderSDK
from .resource import _ResourceSDK
from .role import _RoleSDK
from .session import _SessionSDK
from .subscription import _SubscriptionSDK
from .syncer import _SyncerSDK
from .token import _TokenSDK
from .user import _UserSDK
from .webhook import _WebhookSDK


def _build_enforce_params(
    permission_id: str,
    model_id: str,
    resource_id: str,
    enforce_id: str,
    owner: str,
) -> Dict[str, str]:
    """
    Build and validate parameters for enforce API calls.

    Exactly one of the parameters must be provided and non-empty.

    :return: Dictionary with exactly one parameter set
    :raises ValueError: If zero or multiple parameters are provided
    """
    params = {}
    if permission_id:
        params["permissionId"] = permission_id
    if model_id:
        params["modelId"] = model_id
    if resource_id:
        params["resourceId"] = resource_id
    if enforce_id:
        params["enforcerId"] = enforce_id
    if owner:
        params["owner"] = owner

    if len(params) != 1:
        raise ValueError(
            "Exactly one of (permission_id, model_id, resource_id, enforce_id, owner) "
            "must be provided and non-empty. "
            f"Got {len(params)} parameters: {list(params.keys())}"
        )

    return params


class CasdoorSDK(
    _UserSDK,
    _AdapterSDK,
    _OrganizationSDK,
    _ApplicationSDK,
    _CertSDK,
    _ResourceSDK,
    _RoleSDK,
    _SessionSDK,
    _SyncerSDK,
    _EnforcerSDK,
    _GroupSDK,
    _ModelSDK,
    _PaymentSDK,
    _PermissionSDK,
    _PlanSDK,
    _PricingSDK,
    _ProviderSDK,
    _ProductSDK,
    _SubscriptionSDK,
    _TokenSDK,
    _WebhookSDK,
):
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

    @property
    def certification(self) -> bytes:
        if not isinstance(self.certificate, str):
            raise TypeError("certificate field must be str type")
        return self.certificate.encode("utf-8")

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

    def get_oauth_token(
        self, code: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None
    ) -> Dict:
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
        self, code: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None
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

    def oauth_token_request(
        self, code: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None
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
        params = self._get_payload_for_access_token_request(code=code, username=username, password=password)
        return self._oauth_token_request(payload=params)

    def _oauth_token_request(self, payload: Dict) -> requests.Response:
        """
        Request the Casdoor server to get access_token.

        :param payload: Body for POST request.
        :return: Response from Casdoor
        """
        url = self.endpoint + "/api/login/oauth/access_token"
        response = requests.post(url, payload)
        return response

    def refresh_token_request(self, refresh_token: str, scope: str = "") -> requests.Response:
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

    def refresh_oauth_tokens(self, refresh_token: str, scope: str = "") -> Dict:
        """
        Request the Casdoor server to get a refreshed Token.

        :param refresh_token: refresh_token for send to Casdoor
        :param scope: OAuth scope
        :return: Response from Casdoor
        """
        r = self.refresh_token_request(refresh_token, scope)
        refreshed_token = r.json()

        return refreshed_token

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

    def enforce(
        self,
        permission_id: str,
        model_id: str,
        resource_id: str,
        enforce_id: str,
        owner: str,
        casbin_request: Optional[List[str]] = None,
    ) -> bool:
        """
        Send data to Casdoor enforce API

        :param permission_id: the permission id (i.e. organization name/permission name)
        :param model_id: the model id
        :param resource_id: the resource id
        :param enforce_id: the enforcer id (note: uses 'enforcerId' parameter in API)
        :param owner: the owner of the permission
        :param casbin_request: a list containing the request data (i.e. sub, obj, act)
        :return: a boolean value indicating whether the request is allowed
        """
        url = self.endpoint + "/api/enforce"
        params = _build_enforce_params(permission_id, model_id, resource_id, enforce_id, owner)

        r = requests.post(
            url,
            params=params,
            data=json.dumps(casbin_request),
            auth=(self.client_id, self.client_secret),
        )
        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "Casdoor response error:\n" + str(r.text)
            raise ValueError(error_str)

        response = r.json()
        if isinstance(response, dict):
            data = response.get("data")
            if isinstance(data, list) and len(data) > 0:
                has_permission = data[0]
            else:
                has_permission = response
        else:
            has_permission = response
        if not isinstance(has_permission, bool):
            error_str = "Casdoor response error:\n" + r.text
            raise ValueError(error_str)

        return has_permission

    def batch_enforce(
        self,
        permission_id: str,
        model_id: str,
        enforce_id: str,
        owner: str,
        casbin_request: Optional[List[List[str]]] = None,
    ) -> List[bool]:
        """
        Send data to Casdoor enforce API

        :param permission_id: the permission id (i.e. organization name/permission name)
        :param model_id: the model id
        :param enforce_id: the enforcer id (note: uses 'enforcerId' parameter in API)
        :param owner: the owner of the permission
        :param casbin_request: a list of lists containing the request data
        :return: a list of boolean values indicating whether each request is allowed
        """
        url = self.endpoint + "/api/batch-enforce"
        params = _build_enforce_params(permission_id, model_id, "", enforce_id, owner)

        r = requests.post(
            url,
            params=params,
            data=json.dumps(casbin_request),
            auth=(self.client_id, self.client_secret),
        )

        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "Casdoor response error:\n" + str(r.text)
            raise ValueError(error_str)

        response = r.json()
        data = response.get("data")
        if data is None:
            error_str = "Casdoor response error:\n" + r.text
            raise ValueError(error_str)
        if not isinstance(data, list):
            error_str = f"Casdoor 'data' is not a list (got {type(data)}):\n" + r.text
            raise ValueError(error_str)
        enforce_results = data[0]

        if (
            not isinstance(enforce_results, list)
            or len(enforce_results) == 0
            or not isinstance(enforce_results[0], bool)
        ):
            error_str = "Casdoor response error:\n" + r.text
            raise ValueError(error_str)

        return enforce_results
