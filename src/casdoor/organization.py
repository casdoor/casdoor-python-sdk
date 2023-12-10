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


class AccountItem:
    def __init__(self):
        self.name = ""
        self.visible = False
        self.viewRule = ""
        self.modifyRule = ""

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class ThemeData:
    def __init__(self):
        self.themeType = ""
        self.colorPrimary = ""
        self.borderRadius = 0
        self.isCompact = False
        self.isEnabled = False

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class MfaItem:
    def __init__(self):
        self.name = ""
        self.rule = ""

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class Organization:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.websiteUrl = ""
        self.favicon = ""
        self.passwordType = ""
        self.passwordSalt = ""
        self.passwordOptions = [""]
        self.countryCodes = [""]
        self.defaultAvatar = ""
        self.defaultApplication = ""
        self.tags = [""]
        self.languages = [""]
        # self.themeData = ThemeData
        self.masterPassword = ""
        self.initScore = 0
        self.enableSoftDeletion = False
        self.isProfilePublic = False
        # self.mfaItems = [MfaItem]
        # self.accountItems = [AccountItem]

    @classmethod
    def new(
        cls,
        owner,
        name,
        created_time,
        display_name,
        website_url,
        password_type,
        password_options,
        country_codes,
        tags,
        languages,
        init_score,
        enable_soft_deletion,
        is_profile_public,
    ):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.websiteUrl = website_url
        self.passwordType = password_type
        self.passwordOptions = password_options
        self.countryCodes = country_codes
        self.tags = tags
        self.languages = languages
        self.initScore = init_score
        self.enableSoftDeletion = enable_soft_deletion
        self.isProfilePublic = is_profile_public

        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        org = cls()
        for key, value in data.items():
            if hasattr(org, key):
                setattr(org, key, value)
        return org

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
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response.msg)

        res = []
        for element in response["data"]:
            res.append(Organization.from_dict(element))
        return res

    def get_organization(self, organization_id: str) -> Dict:
        """
        Get the organization from Casdoor providing the organization_id.

        :param organization_id: the id of the organization
        :return: a dict that contains organization's info
        """
        url = self.endpoint + "/api/get-organization"
        params = {
            "id": f"admin/{organization_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response.msg)
        return Organization.from_dict(response["data"])

    def modify_organization(self, method: str, organization: Organization) -> Dict:
        url = self.endpoint + f"/api/{method}"

        params = {
            "id": f"{organization.owner}/{organization.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        organization_info = json.dumps(organization.to_dict())
        r = requests.post(url, params=params, data=organization_info)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response)
        return str(response["data"])

    def add_organization(self, organization: Organization) -> Dict:
        organization.owner = "admin"
        response = self.modify_organization("add-organization", organization)
        return response

    def update_organization(self, organization: Organization) -> Dict:
        organization.owner = "admin"
        response = self.modify_organization("update-organization", organization)
        return response

    def delete_organization(self, organization: Organization) -> Dict:
        organization.owner = "admin"
        response = self.modify_organization("delete-organization", organization)
        return response
