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


class Permission:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.description = ""
        self.users = [""]
        self.roles = [""]
        self.domains = [""]
        self.model = ""
        self.adapter = ""
        self.resourceType = ""
        self.resources = [""]
        self.actions = [""]
        self.effect = ""
        self.isEnabled = False
        self.submitter = ""
        self.approver = ""
        self.approveTime = ""
        self.state = ""

    @classmethod
    def new(
        cls,
        owner,
        name,
        created_time,
        display_name,
        description,
        users,
        roles,
        domains,
        model,
        resource_type,
        resources,
        actions,
        effect,
        is_enabled,
    ):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.description = description
        self.users = users
        self.roles = roles
        self.domains = domains
        self.model = model
        self.resourceType = resource_type
        self.resources = resources
        self.actions = actions
        self.effect = effect
        self.isEnabled = is_enabled
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        permission = cls()
        for key, value in data.items():
            if hasattr(permission, key):
                setattr(permission, key, value)
        return permission

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _PermissionSDK:
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
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        permissions = []
        for permission in response["data"]:
            permissions.append(Permission.from_dict(permission))
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
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Permission.from_dict(response["data"])

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
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return str(response["data"])

    def add_permission(self, permission: Permission) -> Dict:
        response = self.modify_permission("add-permission", permission)
        return response

    def update_permission(self, permission: Permission) -> Dict:
        response = self.modify_permission("update-permission", permission)
        return response

    def delete_permission(self, permission: Permission) -> Dict:
        response = self.modify_permission("delete-permission", permission)
        return response
