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

    @classmethod
    def new(cls, owner, name, created_time, display_name, description):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.description = description
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        role = cls()
        for key, value in data.items():
            if hasattr(role, key):
                setattr(role, key, value)
        return role

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
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        roles = []
        for role in response["data"]:
            roles.append(Role.from_dict(role))
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
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Role.from_dict(response["data"])

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
        if response["status"] != "ok":
            raise Exception(response["msg"])
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

    def assign_role_to_user(self, username: str, role_name: str) -> Dict:
        """
        Assign a role to a user by adding the user to the role's users list.

        :param username: the username to assign the role to
        :param role_name: the name of the role to assign
        :return: response dict with status
        """
        user_id = f"{self.org_name}/{username}"

        role = self.get_role(role_name)
        if role is None:
            raise Exception(f"Role {role_name} not found")

        if not hasattr(role, "users") or role.users is None:
            role.users = []

        if user_id not in role.users:
            role.users.append(user_id)
            return self.update_role(role)

        return {"status": "ok", "msg": "User already has this role"}

    def remove_role_from_user(self, username: str, role_name: str) -> Dict:
        """
        Remove a role from a user by removing the user from the role's users list.

        :param username: the username to remove the role from
        :param role_name: the name of the role to remove
        :return: response dict with status
        """
        user_id = f"{self.org_name}/{username}"

        role = self.get_role(role_name)
        if role is None:
            raise Exception(f"Role {role_name} not found")

        if hasattr(role, "users") and role.users and user_id in role.users:
            role.users.remove(user_id)
            return self.update_role(role)

        return {"status": "ok", "msg": "User does not have this role"}

    def get_user_roles(self, username: str) -> List[Role]:
        """
        Get all roles assigned to a user.

        :param username: the username to get roles for
        :return: list of Role objects assigned to the user
        """
        user_id = f"{self.org_name}/{username}"
        all_roles = self.get_roles()

        user_roles = []
        for role in all_roles:
            if hasattr(role, "users") and role.users and user_id in role.users:
                user_roles.append(role)

        return user_roles
