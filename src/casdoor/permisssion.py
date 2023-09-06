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

from src.casdoor import CasdoorSDK


class Permission:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.description = "string"
        self.users = ["string"]
        self.roles = ["string"]
        self.domains = ["string"]
        self.model = "string"
        self.adapter = "string"
        self.resourceType = "string"
        self.resources = ["string"]
        self.actions = ["string"]
        self.effect = "string"
        self.isEnabled = True
        self.submitter = "string"
        self.approver = "string"
        self.approveTime = "string"
        self.state = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class PermissionSDK(CasdoorSDK):
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
