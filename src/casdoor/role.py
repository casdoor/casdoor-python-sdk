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


class Role:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.description = ""
        self.users = [""]
        self.roles = [""]
        self.domains = [""]
        self.isEnabled = False

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _RoleSDK:
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
        if role.owner == "":
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
