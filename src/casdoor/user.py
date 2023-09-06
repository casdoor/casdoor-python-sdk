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


class User:
    def __init__(self):
        self.address = ["string"]
        self.affiliation = "string"
        self.avatar = "string"
        self.createdTime = "string"
        self.dingtalk = "string"
        self.displayName = "string"
        self.email = "string"
        self.facebook = "string"
        self.gitee = "string"
        self.github = "string"
        self.google = "string"
        self.hash = "string"
        self.id = "string"
        self.isAdmin = True
        self.isForbidden = True
        self.isGlobalAdmin = True
        self.language = "string"
        self.name = "string"
        self.owner = "string"
        self.password = "string"
        self.phone = "string"
        self.preHash = "string"
        self.qq = "string"
        self.score = 0
        self.signupApplication = "string"
        self.tag = "string"
        self.type = "string"
        self.updatedTime = "string"
        self.wechat = "string"
        self.weibo = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class UserSDK(CasdoorSDK):
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
