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
from typing import Dict, List, Optional

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
        self.invitation = ""
        self.invitationCode = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name, email="", phone=""):
        self = cls()
        self.name = name
        self.owner = owner
        self.createdTime = created_time
        self.displayName = display_name
        self.email = email
        self.phone = phone
        return self

    @classmethod
    def from_dict(cls, data: dict) -> Optional["User"]:
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

    def get_id(self) -> str:
        return f"{self.owner}/{self.name}"


class _UserSDK:
    def get_global_users(self) -> List[User]:
        """ """
        url = self.endpoint + "/api/get-global-users"
        params = {
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

    def get_sorted_users(self, sorter: str, limit: str) -> List[User]:
        """
        Get the sorted users from Casdoor.

        :param sroter: the DB column name to sort by, e.g., created_time
        :param limiter: the count of users to return, e.g., 25
        """
        url = self.endpoint + "/api/get-sorted-users"
        params = {
            "owner": self.org_name,
            "sorter": sorter,
            "limit": limit,
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

    def get_users(self) -> List[User]:
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

    def get_user(self, name: str) -> User:
        """
        Get the user from Casdoor providing the name.

        :param name: the name of the user
        :return: a dict that contains user's info
        """
        url = self.endpoint + "/api/get-user"
        params = {
            "id": f"{self.org_name}/{name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return User.from_dict(response["data"])

    def get_user_by_email(self, email: str) -> User:
        """
        Get the user from Casdoor providing the email.

        :param email: the email of the user
        :return: a User object that contains user's info
        """
        url = self.endpoint + "/api/get-user"
        params = {
            "email": email,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return User.from_dict(response["data"])

    def get_user_by_phone(self, phone: str) -> User:
        """
        Get the user from Casdoor providing the phone number.

        :param phone: the phone number of the user
        :return: a User object that contains user's info
        """
        url = self.endpoint + "/api/get-user"
        params = {
            "phone": phone,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return User.from_dict(response["data"])

    def get_user_by_user_id(self, user_id: str) -> User:
        """
        Get the user from Casdoor providing the user ID.

        :param user_id: the user ID of the user
        :return: a User object that contains user's info
        """
        url = self.endpoint + "/api/get-user"
        params = {
            "userId": user_id,
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
        response = r.json()
        count = response.get("data")
        return count

    def modify_user(self, method: str, user: User) -> Dict:
        """
        modifyUser is an encapsulation of user CUD(Create, Update, Delete) operations.
        possible actions are `add-user`, `update-user`, `delete-user`,
        """
        id = user.get_id()
        return self.modify_user_by_id(method, id, user)

    def modify_user_by_id(self, method: str, id: str, user: User) -> Dict:
        """
        Modify the user from Casdoor providing the ID.

        :param id: the id ( owner/name ) of the user
        :param user: a User object that contains user's info
        """

        url = self.endpoint + f"/api/{method}"
        user.owner = self.org_name
        params = {
            "id": id,
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

    def update_user_by_id(self, id: str, user: User) -> Dict:
        response = self.modify_user_by_id("update-user", id, user)
        return response

    def delete_user(self, user: User) -> Dict:
        response = self.modify_user("delete-user", user)
        return response
