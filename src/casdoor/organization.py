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
from typing import Dict, List

import requests


class AccountItem:
    def __init__(self):
        self.name = "string"
        self.visible = False
        self.viewRule = "string"
        self.modifyRule = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class ThemeData:
    def __init__(self):
        self.themeType = "string"
        self.colorPrimary = "string"
        self.borderRadius = 0
        self.isCompact = False
        self.isEnabled = False

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class MfaItem:
    def __init__(self):
        self.name = "string"
        self.rule = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class Organization:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.websiteUrl = "string"
        self.favicon = "string"
        self.passwordType = "string"
        self.passwordSalt = "string"
        self.passwordOptions = ["string"]
        self.countryCodes = ["string"]
        self.defaultAvatar = "string"
        self.defaultApplication = "string"
        self.tags = ["string"]
        self.languages = ["string"]
        self.themeData = ThemeData
        self.masterPassword = "string"
        self.initScore = 0
        self.enableSoftDeletion = True
        self.isProfilePublic = True
        self.mfaItems = [MfaItem]
        self.accountItems = [AccountItem]

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _OrganizationSDK:
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
