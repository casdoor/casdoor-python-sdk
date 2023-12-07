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


class User:
    def __init__(self):
        self.address = [""]
        self.affiliation = ""
        self.avatar = ""
        self.createdTime = ""
        self.dingtalk = ""
        self.displayName = ""
        self.email = ""
        self.facebook = ""
        self.gitee = ""
        self.github = ""
        self.google = ""
        self.hash = ""
        self.id = ""
        self.isAdmin = False
        self.isForbidden = False
        self.isGlobalAdmin = False
        self.language = ""
        self.name = ""
        self.owner = ""
        self.password = ""
        self.phone = ""
        self.preHash = ""
        self.qq = ""
        self.score = 0
        self.signupApplication = ""
        self.tag = ""
        self.type = ""
        self.updatedTime = ""
        self.wechat = ""
        self.weibo = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name):
        self = cls()
        self.name = name
        self.owner = owner
        self.createdTime = created_time
        self.displayName = display_name
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        user = cls()
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _UserSDK:
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
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        users = []
        for user in response["data"]:
            users.append(User.from_dict(user))
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
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return User.from_dict(response["data"])

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
        if response["status"] != "ok":
            raise Exception(response["msg"])
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
