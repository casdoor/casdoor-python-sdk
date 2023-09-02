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
from typing import Dict, List, Optional

import jwt
import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from .cert import Cert
from .user import User
from .adapter import Adapter
from .group import Group
from .role import Role
from .organization import Organization
from .payment import Payment
from .provider import Provider
from .application import Application
from .model import Model
from .plan import Plan
from .permisssion import Permission
from .enforcer import Enforcer
from .resource import Resource
from .token import Token
from .session import Session
from .syncer import Syncer
from .webhook import Webhook
from .subscription import Subscription
from .pricing import Pricing
from .product import Product


class CasdoorSDK:
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
        if type(self.certificate) is not str:
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

    def parse_jwt_token(self, token: str, **kwargs) -> Dict:
        """
        Converts the returned access_token to real data using
        jwt (JSON Web Token) algorithms.

        :param token: access_token
        :return: the data in dict format
        """
        certificate = x509.load_pem_x509_certificate(self.certification, default_backend())

        return_json = jwt.decode(
            token, certificate.public_key(), algorithms=self.algorithms, audience=self.client_id, **kwargs
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
        query_params = {"clientId": self.client_id, "clientSecret": self.client_secret}
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

    def batch_enforce(self, permission_model_name: str, permission_rules: List[List[str]]) -> List[bool]:
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
        query_params = {"clientId": self.client_id, "clientSecret": self.client_secret}

        def map_rule(rule: List[str], idx) -> Dict:
            if len(rule) < 3:
                raise ValueError("Invalid permission rule[{0}]: {1}".format(idx, rule))
            result = {"id": permission_model_name}
            for i in range(0, len(rule)):
                result.update({"v{0}".format(i): rule[i]})
            return result

        params = [map_rule(permission_rules[i], i) for i in range(0, len(permission_rules))]
        r = requests.post(url, json=params, params=query_params)
        if r.status_code != 200 or "json" not in r.headers["content-type"]:
            error_str = "Casdoor response error:\n" + str(r.text)
            raise ValueError(error_str)

        enforce_results = r.json()

        if (
            not isinstance(enforce_results, list)
            or len(enforce_results) == 0
            or not isinstance(enforce_results[0], bool)
        ):
            error_str = "Casdoor response error:\n" + r.text
            raise ValueError(error_str)

        return enforce_results

    def get_users(self) -> List[Dict]:
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

    def get_user(self, user_id: str) -> Dict:
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

    def modify_user(self, method: str, user: User) -> Dict:
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

    def add_user(self, user: User) -> Dict:
        response = self.modify_user("add-user", user)
        return response

    def update_user(self, user: User) -> Dict:
        response = self.modify_user("update-user", user)
        return response

    def delete_user(self, user: User) -> Dict:
        response = self.modify_user("delete-user", user)
        return response

    def get_certs(self) -> List[Dict]:
        """
        Get the certs from Casdoor.

        :return: a list of dicts containing cert info
        """
        url = self.endpoint + "/api/get-certs"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        certs = r.json()
        return certs

    def get_cert(self, cert_id: str) -> Dict:
        """
        Get the cert from Casdoor providing the cert_id.

        :param cert_id: the id of the cert
        :return: a dict that contains cert's info
        """
        url = self.endpoint + "/api/get-cert"
        params = {
            "id": f"{self.org_name}/{cert_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        cert = r.json()
        return cert

    def modify_cert(self, method: str, cert: Cert) -> Dict:
        url = self.endpoint + f"/api/{method}"
        cert.owner = self.org_name
        params = {
            "id": f"{cert.owner}/{cert.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        cert_info = json.dumps(cert.to_dict())
        r = requests.post(url, params=params, data=cert_info)
        response = r.json()
        return response

    def add_cert(self, cert: Cert) -> Dict:
        response = self.modify_cert("add-cert", cert)
        return response

    def update_cert(self, cert: Cert) -> Dict:
        response = self.modify_cert("update-cert", cert)
        return response

    def delete_cert(self, cert: Cert) -> Dict:
        response = self.modify_cert("delete-cert", cert)
        return response

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

    def get_groups(self) -> List[Dict]:
        """
        Get the groups from Casdoor.

        :return: a list of dicts containing group info
        """
        url = self.endpoint + "/api/get-groups"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        groups = r.json()
        return groups

    def get_group(self, group_id: str) -> Dict:
        """
        Get the group from Casdoor providing the group_id.

        :param group_id: the id of the group
        :return: a dict that contains group's info
        """
        url = self.endpoint + "/api/get-group"
        params = {
            "id": f"{self.org_name}/{group_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        group = r.json()
        return group

    def modify_group(self, method: str, group: Group) -> Dict:
        url = self.endpoint + f"/api/{method}"
        group.owner = self.org_name
        params = {
            "id": f"{group.owner}/{group.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        group_info = json.dumps(group.to_dict())
        r = requests.post(url, params=params, data=group_info)
        response = r.json()
        return response

    def add_group(self, group: Group) -> Dict:
        response = self.modify_group("add-group", group)
        return response

    def update_group(self, group: Group) -> Dict:
        response = self.modify_group("update-group", group)
        return response

    def delete_group(self, group: Group) -> Dict:
        response = self.modify_group("delete-group", group)
        return response

    def get_roles(self) -> List[Dict]:
        """
        Get the roles from Casdoor.

        :return: a list of dicts containing role info
        """
        url = self.endpoint + "/api/get-roles"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        roles = r.json()
        return roles

    def get_role(self, role_id: str) -> Dict:
        """
        Get the role from Casdoor providing the role_id.

        :param role_id: the id of the role
        :return: a dict that contains role's info
        """
        url = self.endpoint + "/api/get-role"
        params = {
            "id": f"{self.org_name}/{role_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        role = r.json()
        return role

    def modify_role(self, method: str, role: Role) -> Dict:
        url = self.endpoint + f"/api/{method}"
        role.owner = self.org_name
        params = {
            "id": f"{role.owner}/{role.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        role_info = json.dumps(role.to_dict())
        r = requests.post(url, params=params, data=role_info)
        response = r.json()
        return response

    def add_role(self, role: Role) -> Dict:
        response = self.modify_role("add-role", role)
        return response

    def update_role(self, role: Role) -> Dict:
        response = self.modify_role("update-role", role)
        return response

    def delete_role(self, role: Role) -> Dict:
        response = self.modify_role("delete-role", role)
        return response

    def get_organizations(self) -> List[Dict]:
        """
        Get the organizations from Casdoor.

        :return: a list of dicts containing organization info
        """
        url = self.endpoint + "/api/get-organizations"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        organizations = r.json()
        return organizations

    def get_organization(self, organization_id: str) -> Dict:
        """
        Get the organization from Casdoor providing the organization_id.

        :param organization_id: the id of the organization
        :return: a dict that contains organization's info
        """
        url = self.endpoint + "/api/get-organization"
        params = {
            "id": f"{self.org_name}/{organization_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        organization = r.json()
        return organization

    def modify_organization(self, method: str, organization: Organization) -> Dict:
        url = self.endpoint + f"/api/{method}"
        organization.owner = self.org_name
        params = {
            "id": f"{organization.owner}/{organization.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        organization_info = json.dumps(organization.to_dict())
        r = requests.post(url, params=params, data=organization_info)
        response = r.json()
        return response

    def add_organization(self, organization: Organization) -> Dict:
        response = self.modify_organization("add-organization", organization)
        return response

    def update_organization(self, organization: Organization) -> Dict:
        response = self.modify_organization("update-organization", organization)
        return response

    def delete_organization(self, organization: Organization) -> Dict:
        response = self.modify_organization("delete-organization", organization)
        return response

    def get_payments(self) -> List[Dict]:
        """
        Get the payments from Casdoor.

        :return: a list of dicts containing payment info
        """
        url = self.endpoint + "/api/get-payments"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        payments = r.json()
        return payments

    def get_payment(self, payment_id: str) -> Dict:
        """
        Get the payment from Casdoor providing the payment_id.

        :param payment_id: the id of the payment
        :return: a dict that contains payment's info
        """
        url = self.endpoint + "/api/get-payment"
        params = {
            "id": f"{self.org_name}/{payment_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        payment = r.json()
        return payment

    def modify_payment(self, method: str, payment: Payment) -> Dict:
        url = self.endpoint + f"/api/{method}"
        payment.owner = self.org_name
        params = {
            "id": f"{payment.owner}/{payment.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        payment_info = json.dumps(payment.to_dict())
        r = requests.post(url, params=params, data=payment_info)
        response = r.json()
        return response

    def add_payment(self, payment: Payment) -> Dict:
        response = self.modify_payment("add-payment", payment)
        return response

    def update_payment(self, payment: Payment) -> Dict:
        response = self.modify_payment("update-payment", payment)
        return response

    def delete_payment(self, payment: Payment) -> Dict:
        response = self.modify_payment("delete-payment", payment)
        return response

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

    def get_applications(self) -> List[Dict]:
        """
        Get the applications from Casdoor.

        :return: a list of dicts containing application info
        """
        url = self.endpoint + "/api/get-applications"
        params = {
            "owner": "admin",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        applications = r.json()
        return applications

    def get_application(self, application_id: str) -> Dict:
        """
        Get the application from Casdoor providing the application_id.

        :param application_id: the id of the application
        :return: a dict that contains application's info
        """
        url = self.endpoint + "/api/get-application"
        params = {
            "id": f"{self.org_name}/{application_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        application = r.json()
        return application

    def modify_application(self, method: str, application: Application) -> Dict:
        url = self.endpoint + f"/api/{method}"
        application.owner = self.org_name
        params = {
            "id": f"{application.owner}/{application.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        application_info = json.dumps(application.to_dict())
        r = requests.post(url, params=params, data=application_info)
        response = r.json()
        return response

    def add_application(self, application: Application) -> Dict:
        response = self.modify_application("add-application", application)
        return response

    def update_application(self, application: Application) -> Dict:
        response = self.modify_application("update-application", application)
        return response

    def delete_application(self, application: Application) -> Dict:
        response = self.modify_application("delete-application", application)
        return response

    def get_models(self) -> List[Dict]:
        """
        Get the models from Casdoor.

        :return: a list of dicts containing model info
        """
        url = self.endpoint + "/api/get-models"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        models = r.json()
        return models

    def get_model(self, model_id: str) -> Dict:
        """
        Get the model from Casdoor providing the model_id.

        :param model_id: the id of the model
        :return: a dict that contains model's info
        """
        url = self.endpoint + "/api/get-model"
        params = {
            "id": f"{self.org_name}/{model_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        model = r.json()
        return model

    def modify_model(self, method: str, model: Model) -> Dict:
        url = self.endpoint + f"/api/{method}"
        model.owner = self.org_name
        params = {
            "id": f"{model.owner}/{model.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        model_info = json.dumps(model.to_dict())
        r = requests.post(url, params=params, data=model_info)
        response = r.json()
        return response

    def add_model(self, model: Model) -> Dict:
        response = self.modify_model("add-model", model)
        return response

    def update_model(self, model: Model) -> Dict:
        response = self.modify_model("update-model", model)
        return response

    def delete_model(self, model: Model) -> Dict:
        response = self.modify_model("delete-model", model)
        return response

    def get_plans(self) -> List[Dict]:
        """
        Get the plans from Casdoor.

        :return: a list of dicts containing plan info
        """
        url = self.endpoint + "/api/get-plans"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        plans = r.json()
        return plans

    def get_plan(self, plan_id: str) -> Dict:
        """
        Get the plan from Casdoor providing the plan_id.

        :param plan_id: the id of the plan
        :return: a dict that contains plan's info
        """
        url = self.endpoint + "/api/get-plan"
        params = {
            "id": f"{self.org_name}/{plan_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        plan = r.json()
        return plan

    def modify_plan(self, method: str, plan: Plan) -> Dict:
        url = self.endpoint + f"/api/{method}"
        plan.owner = self.org_name
        params = {
            "id": f"{plan.owner}/{plan.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        plan_info = json.dumps(plan.to_dict())
        r = requests.post(url, params=params, data=plan_info)
        response = r.json()
        return response

    def add_plan(self, plan: Plan) -> Dict:
        response = self.modify_plan("add-plan", plan)
        return response

    def update_plan(self, plan: Plan) -> Dict:
        response = self.modify_plan("update-plan", plan)
        return response

    def delete_plan(self, plan: Plan) -> Dict:
        response = self.modify_plan("delete-plan", plan)
        return response

    def get_permissions(self) -> List[Dict]:
        """
        Get the permissions from Casdoor.

        :return: a list of dicts containing permission info
        """
        url = self.endpoint + "/api/get-permissions"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        permissions = r.json()
        return permissions

    def get_permission(self, permission_id: str) -> Dict:
        """
        Get the permission from Casdoor providing the permission_id.

        :param permission_id: the id of the permission
        :return: a dict that contains permission's info
        """
        url = self.endpoint + "/api/get-permission"
        params = {
            "id": f"{self.org_name}/{permission_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        permission = r.json()
        return permission

    def modify_permission(self, method: str, permission: Permission) -> Dict:
        url = self.endpoint + f"/api/{method}"
        permission.owner = self.org_name
        params = {
            "id": f"{permission.owner}/{permission.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        permission_info = json.dumps(permission.to_dict())
        r = requests.post(url, params=params, data=permission_info)
        response = r.json()
        return response

    def add_permission(self, permission: Permission) -> Dict:
        response = self.modify_permission("add-permission", permission)
        return response

    def update_permission(self, permission: Permission) -> Dict:
        response = self.modify_permission("update-permission", permission)
        return response

    def delete_permission(self, permission: Permission) -> Dict:
        response = self.modify_permission("delete-permission", permission)
        return response

    def get_enforcers(self) -> List[Dict]:
        """
        Get the enforcers from Casdoor.

        :return: a list of dicts containing enforcer info
        """
        url = self.endpoint + "/api/get-enforcers"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        enforcers = r.json()
        return enforcers

    def get_enforcer(self, enforcer_id: str) -> Dict:
        """
        Get the enforcer from Casdoor providing the enforcer_id.

        :param enforcer_id: the id of the enforcer
        :return: a dict that contains enforcer's info
        """
        url = self.endpoint + "/api/get-enforcer"
        params = {
            "id": f"{self.org_name}/{enforcer_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        enforcer = r.json()
        return enforcer

    def modify_enforcer(self, method: str, enforcer: Enforcer) -> Dict:
        url = self.endpoint + f"/api/{method}"
        enforcer.owner = self.org_name
        params = {
            "id": f"{enforcer.owner}/{enforcer.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        enforcer_info = json.dumps(enforcer.to_dict())
        r = requests.post(url, params=params, data=enforcer_info)
        response = r.json()
        return response

    def add_enforcer(self, enforcer: Enforcer) -> Dict:
        response = self.modify_enforcer("add-enforcer", enforcer)
        return response

    def update_enforcer(self, enforcer: Enforcer) -> Dict:
        response = self.modify_enforcer("update-enforcer", enforcer)
        return response

    def delete_enforcer(self, enforcer: Enforcer) -> Dict:
        response = self.modify_enforcer("delete-enforcer", enforcer)
        return response

    def get_resources(self,owner,user,field,value,sort_field,sort_order) -> List[Dict]:
        """
        Get the resources from Casdoor.

        :return: a list of dicts containing resource info
        """
        url = self.endpoint + "/api/get-resources"
        params = {
            "owner": owner,
            "user": user,
            "field": field,
            "value": value,
            "sortField": sort_field,
            "sortOrder": sort_order,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        resources = r.json()
        return resources

    def get_resource(self, resource_id: str) -> Dict:
        """
        Get the resource from Casdoor providing the resource_id.

        :param resource_id: the id of the resource
        :return: a dict that contains resource's info
        """
        url = self.endpoint + "/api/get-resource"
        params = {
            "id": f"{self.org_name}/{resource_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        resource = r.json()
        return resource

    def modify_resource(self, method: str, resource: Resource) -> Dict:
        url = self.endpoint + f"/api/{method}"
        resource.owner = self.org_name
        params = {
            "id": f"{resource.owner}/{resource.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        resource_info = json.dumps(resource.to_dict())
        r = requests.post(url, params=params, data=resource_info)
        response = r.json()
        return response

    def add_resource(self, resource: Resource) -> Dict:
        response = self.modify_resource("add-resource", resource)
        return response

    def update_resource(self, resource: Resource) -> Dict:
        response = self.modify_resource("update-resource", resource)
        return response

    def delete_resource(self, resource: Resource) -> Dict:
        response = self.modify_resource("delete-resource", resource)
        return response

    def get_tokens(self, p ,page_size) -> List[Dict]:
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

    def get_sessions(self) -> List[Dict]:
        """
        Get the sessions from Casdoor.

        :return: a list of dicts containing session info
        """
        url = self.endpoint + "/api/get-sessions"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        sessions = r.json()
        return sessions

    def get_session(self, session_id: str) -> Dict:
        """
        Get the session from Casdoor providing the session_id.

        :param session_id: the id of the session
        :return: a dict that contains session's info
        """
        url = self.endpoint + "/api/get-session"
        params = {
            "id": f"{self.org_name}/{session_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        session = r.json()
        return session

    def modify_session(self, method: str, session: Session) -> Dict:
        url = self.endpoint + f"/api/{method}"
        session.owner = self.org_name
        params = {
            "id": f"{session.owner}/{session.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        session_info = json.dumps(session.to_dict())
        r = requests.post(url, params=params, data=session_info)
        response = r.json()
        return response

    def add_session(self, session: Session) -> Dict:
        response = self.modify_session("add-session", session)
        return response

    def update_session(self, session: Session) -> Dict:
        response = self.modify_session("update-session", session)
        return response

    def delete_session(self, session: Session) -> Dict:
        response = self.modify_session("delete-session", session)
        return response

    def get_syncers(self) -> List[Dict]:
        """
        Get the syncers from Casdoor.

        :return: a list of dicts containing syncer info
        """
        url = self.endpoint + "/api/get-syncers"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        syncers = r.json()
        return syncers

    def get_syncer(self, syncer_id: str) -> Dict:
        """
        Get the syncer from Casdoor providing the syncer_id.

        :param syncer_id: the id of the syncer
        :return: a dict that contains syncer's info
        """
        url = self.endpoint + "/api/get-syncer"
        params = {
            "id": f"{self.org_name}/{syncer_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        syncer = r.json()
        return syncer

    def modify_syncer(self, method: str, syncer: Syncer) -> Dict:
        url = self.endpoint + f"/api/{method}"
        syncer.owner = self.org_name
        params = {
            "id": f"{syncer.owner}/{syncer.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        syncer_info = json.dumps(syncer.to_dict())
        r = requests.post(url, params=params, data=syncer_info)
        response = r.json()
        return response

    def add_syncer(self, syncer: Syncer) -> Dict:
        response = self.modify_syncer("add-syncer", syncer)
        return response

    def update_syncer(self, syncer: Syncer) -> Dict:
        response = self.modify_syncer("update-syncer", syncer)
        return response

    def delete_syncer(self, syncer: Syncer) -> Dict:
        response = self.modify_syncer("delete-syncer", syncer)
        return response

    def get_webhooks(self) -> List[Dict]:
        """
        Get the webhooks from Casdoor.

        :return: a list of dicts containing webhook info
        """
        url = self.endpoint + "/api/get-webhooks"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        webhooks = r.json()
        return webhooks

    def get_webhook(self, webhook_id: str) -> Dict:
        """
        Get the webhook from Casdoor providing the webhook_id.

        :param webhook_id: the id of the webhook
        :return: a dict that contains webhook's info
        """
        url = self.endpoint + "/api/get-webhook"
        params = {
            "id": f"{self.org_name}/{webhook_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        webhook = r.json()
        return webhook

    def modify_webhook(self, method: str, webhook: Webhook) -> Dict:
        url = self.endpoint + f"/api/{method}"
        webhook.owner = self.org_name
        params = {
            "id": f"{webhook.owner}/{webhook.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        webhook_info = json.dumps(webhook.to_dict())
        r = requests.post(url, params=params, data=webhook_info)
        response = r.json()
        return response

    def add_webhook(self, webhook: Webhook) -> Dict:
        response = self.modify_webhook("add-webhook", webhook)
        return response

    def update_webhook(self, webhook: Webhook) -> Dict:
        response = self.modify_webhook("update-webhook", webhook)
        return response

    def delete_webhook(self, webhook: Webhook) -> Dict:
        response = self.modify_webhook("delete-webhook", webhook)
        return response

    def get_subscriptions(self) -> List[Dict]:
        """
        Get the subscriptions from Casdoor.

        :return: a list of dicts containing subscription info
        """
        url = self.endpoint + "/api/get-subscriptions"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        subscriptions = r.json()
        return subscriptions

    def get_subscription(self, subscription_id: str) -> Dict:
        """
        Get the subscription from Casdoor providing the subscription_id.

        :param subscription_id: the id of the subscription
        :return: a dict that contains subscription's info
        """
        url = self.endpoint + "/api/get-subscription"
        params = {
            "id": f"{self.org_name}/{subscription_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        subscription = r.json()
        return subscription

    def modify_subscription(self, method: str, subscription: Subscription) -> Dict:
        url = self.endpoint + f"/api/{method}"
        subscription.owner = self.org_name
        params = {
            "id": f"{subscription.owner}/{subscription.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        subscription_info = json.dumps(subscription.to_dict())
        r = requests.post(url, params=params, data=subscription_info)
        response = r.json()
        return response

    def add_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("add-subscription", subscription)
        return response

    def update_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("update-subscription", subscription)
        return response

    def delete_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("delete-subscription", subscription)
        return response

    def get_pricings(self) -> List[Dict]:
        """
        Get the pricings from Casdoor.

        :return: a list of dicts containing pricing info
        """
        url = self.endpoint + "/api/get-pricings"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        pricings = r.json()
        return pricings

    def get_pricing(self, pricing_id: str) -> Dict:
        """
        Get the pricing from Casdoor providing the pricing_id.

        :param pricing_id: the id of the pricing
        :return: a dict that contains pricing's info
        """
        url = self.endpoint + "/api/get-pricing"
        params = {
            "id": f"{self.org_name}/{pricing_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        pricing = r.json()
        return pricing

    def modify_pricing(self, method: str, pricing: Pricing) -> Dict:
        url = self.endpoint + f"/api/{method}"
        pricing.owner = self.org_name
        params = {
            "id": f"{pricing.owner}/{pricing.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        pricing_info = json.dumps(pricing.to_dict())
        r = requests.post(url, params=params, data=pricing_info)
        response = r.json()
        return response

    def add_pricing(self, pricing: Pricing) -> Dict:
        response = self.modify_pricing("add-pricing", pricing)
        return response

    def update_pricing(self, pricing: Pricing) -> Dict:
        response = self.modify_pricing("update-pricing", pricing)
        return response

    def delete_pricing(self, pricing: Pricing) -> Dict:
        response = self.modify_pricing("delete-pricing", pricing)
        return response

    def get_products(self) -> List[Dict]:
        """
        Get the products from Casdoor.

        :return: a list of dicts containing product info
        """
        url = self.endpoint + "/api/get-products"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        products = r.json()
        return products

    def get_product(self, product_id: str) -> Dict:
        """
        Get the product from Casdoor providing the product_id.

        :param product_id: the id of the product
        :return: a dict that contains product's info
        """
        url = self.endpoint + "/api/get-product"
        params = {
            "id": f"{self.org_name}/{product_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        product = r.json()
        return product

    def modify_product(self, method: str, product: Product) -> Dict:
        url = self.endpoint + f"/api/{method}"
        product.owner = self.org_name
        params = {
            "id": f"{product.owner}/{product.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        product_info = json.dumps(product.to_dict())
        r = requests.post(url, params=params, data=product_info)
        response = r.json()
        return response

    def add_product(self, product: Product) -> Dict:
        response = self.modify_product("add-product", product)
        return response

    def update_product(self, product: Product) -> Dict:
        response = self.modify_product("update-product", product)
        return response

    def delete_product(self, product: Product) -> Dict:
        response = self.modify_product("delete-product", product)
        return response