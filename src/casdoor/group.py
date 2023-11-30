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

from .user import User


class Group:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.updatedTime = ""
        self.displayName = ""
        self.manager = ""
        self.contactEmail = ""
        self.type = ""
        self.parentId = ""
        self.isTopGroup = False
        self.users = [User]
        self.title = ""
        self.key = ""
        self.children = [Group]
        self.isEnabled = False

    @classmethod
    def new(cls, owner, name, created_time, display_name):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        group = cls()
        for key, value in data.items():
            if hasattr(group, key):
                setattr(group, key, value)
        return group

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _GroupSDK:
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
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])

        res = []
        for element in response["data"]:
            res.append(Group.from_dict(element))

        return res

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
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])
        return Group.from_dict(response["data"])

    def modify_group(self, method: str, group: Group) -> Dict:
        url = self.endpoint + f"/api/{method}"
        # if group.owner == "":
        #     group.owner = self.org_name
        group.owner = self.org_name
        params = {
            "id": f"{group.owner}/{group.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }

        # group_info = json.dumps(group.to_dict())
        group_info = json.dumps(group.to_dict(), default=self.custom_encoder)
        r = requests.post(url, params=params, data=group_info)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])

        return str(response["data"])

    def add_group(self, group: Group) -> Dict:
        response = self.modify_group("add-group", group)
        return response

    def update_group(self, group: Group) -> Dict:
        response = self.modify_group("update-group", group)
        return response

    def delete_group(self, group: Group) -> Dict:
        response = self.modify_group("delete-group", group)
        return response

    def custom_encoder(self, o):
        if isinstance(o, (Group, User)):
            return o.__dict__
