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

from .main import CasdoorSDK
from .user import User


class Group:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.updatedTime = "string"
        self.displayName = "string"
        self.manager = "string"
        self.contactEmail = "string"
        self.type = "string"
        self.parentId = "string"
        self.isTopGroup = True
        self.users = [User]
        self.title = "string"
        self.key = "string"
        self.children = [Group]
        self.isEnabled = True

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class GroupSDK(CasdoorSDK):
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
