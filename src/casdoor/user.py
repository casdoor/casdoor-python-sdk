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

from .util import get_id, get_owner


class User:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.updatedTime = ""

        self.id = ""
        self.externalId = ""
        self.type = ""
        self.password = ""
        self.passwordSalt = ""
        self.passwordType = ""

        self.displayName = ""
        self.firstName = ""
        self.lastName = ""
        self.avatar = ""
        self.avatarType = ""
        self.permanentAvatar = ""
        self.email = ""
        self.emailVerified = False
        self.phone = ""
        self.countryCode = ""
        self.region = ""
        self.location = ""
        self.address = []
        self.affiliation = ""
        self.title = ""
        self.idCardType = ""
        self.idCard = ""
        self.homepage = ""
        self.bio = ""
        self.tag = ""
        self.language = ""
        self.gender = ""
        self.birthday = ""
        self.education = ""

        self.score = 0
        self.karma = 0
        self.ranking = 0
        self.isDefaultAvatar = False
        self.isOnline = False
        self.isAdmin = False
        self.isForbidden = False
        self.isDeleted = False
        self.signupApplication = ""

        self.hash = ""
        self.preHash = ""
        self.accessKey = ""
        self.accessSecret = ""

        self.createdIp = ""
        self.lastSigninTime = ""
        self.lastSigninIp = ""

        self.github = ""
        self.google = ""
        self.qq = ""
        self.wechat = ""
        self.facebook = ""
        self.dingtalk = ""
        self.weibo = ""
        self.gitee = ""
        self.linkedin = ""
        self.wecom = ""
        self.lark = ""
        self.gitlab = ""
        self.adfs = ""
        self.baidu = ""
        self.alipay = ""
        self.casdoor = ""
        self.infoflow = ""
        self.apple = ""
        self.azureAd = ""
        self.slack = ""
        self.steam = ""
        self.bilibili = ""
        self.okta = ""
        self.douyin = ""
        self.line = ""
        self.amazon = ""
        self.auth0 = ""
        self.battleNet = ""
        self.bitbucket = ""
        self.box = ""
        self.cloudFoundry = ""
        self.dailymotion = ""
        self.deezer = ""
        self.digitalOcean = ""
        self.discord = ""
        self.dropbox = ""
        self.eveOnline = ""
        self.fitbit = ""
        self.gitea = ""
        self.heroku = ""
        self.influxCloud = ""
        self.instagram = ""
        self.intercom = ""
        self.kakao = ""
        self.lastfm = ""
        self.mailru = ""
        self.meetup = ""
        self.microsoftOnline = ""
        self.naver = ""
        self.nextcloud = ""
        self.onedrive = ""
        self.oura = ""
        self.patreon = ""
        self.paypal = ""
        self.salesForce = ""
        self.shopify = ""
        self.soundcloud = ""
        self.spotify = ""
        self.strava = ""
        self.stripe = ""
        self.tiktok = ""
        self.tumblr = ""
        self.twitch = ""
        self.twitter = ""
        self.typetalk = ""
        self.uber = ""
        self.vk = ""
        self.wepay = ""
        self.xero = ""
        self.yahoo = ""
        self.yammer = ""
        self.yandex = ""
        self.zoom = ""
        self.metaMask = ""
        self.web3Onboard = ""
        self.custom = ""

        self.preferredMfaType = ""
        self.recoveryCodes = []
        self.totpSecret = ""
        self.mfaPhoneEnabled = False
        self.mfaEmailEnabled = False

        self.invitation = ""
        self.invitationCode = ""

        self.ldap = ""
        self.properties = {}

        self.roles = []
        self.permissions = []
        self.groups = []

        self.lastSigninWrongTime = ""
        self.signinWrongTimes = 0

        self.managedAccounts = []
        self.needUpdatePassword = False
        self.deletedTime = ""
        self.addresses = []
        self.realName = ""
        self.isVerified = False
        self.balance = 0.0
        self.balanceCredit = 0.0
        self.currency = ""
        self.balanceCurrency = ""
        self.registerType = ""
        self.registerSource = ""
        self.accessToken = ""
        self.originalToken = ""
        self.originalRefreshToken = ""
        self.azuread = ""
        self.azureadb2c = ""
        self.kwai = ""
        self.battlenet = ""
        self.cloudfoundry = ""
        self.digitalocean = ""
        self.eveonline = ""
        self.influxcloud = ""
        self.microsoftonline = ""
        self.salesforce = ""
        self.telegram = ""
        self.metamask = ""
        self.web3onboard = ""
        self.oidc = ""
        self.custom2 = ""
        self.custom3 = ""
        self.custom4 = ""
        self.custom5 = ""
        self.custom6 = ""
        self.custom7 = ""
        self.custom8 = ""
        self.custom9 = ""
        self.custom10 = ""
        self.webauthnCredentials = None
        self.mfaRadiusEnabled = False
        self.mfaRadiusUsername = ""
        self.mfaRadiusProvider = ""
        self.mfaPushEnabled = False
        self.mfaPushReceiver = ""
        self.mfaPushProvider = ""
        self.multiFactorAuths = []
        self.faceIds = []
        self.cart = []
        self.uidNumber = 0
        self.thirdPartyLinks = []
        self.lastChangePasswordTime = ""
        self.mfaAccounts = []
        self.mfaItems = []
        self.mfaRememberDeadline = ""
        self.ipWhitelist = ""
        self.applicationScopes = []

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
        url = self.endpoint + "/api/get-global-users"
        params = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
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
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        users = []
        for user in response["data"]:
            users.append(User.from_dict(user))
        return users

    def get_account(self) -> Optional[User]:
        """
        Get the user of the access token, i.e. "who am I", the SDK must be created by with_access_token().
        """
        return User.from_dict(self.do_get("get-account"))

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
        r = self._http_get(url, params)
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
            "id": get_id(name, self.org_name),
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
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
            "owner": self.org_name,
            "email": email,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
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
            "owner": self.org_name,
            "phone": phone,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
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
            "owner": self.org_name,
            "userId": user_id,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
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

        r = self._http_get(url, params)
        response = r.json()
        count = response.get("data")
        return count

    def modify_user(self, method: str, user: User, columns: Optional[List[str]] = None) -> Dict:
        """
        modifyUser is an encapsulation of user CUD(Create, Update, Delete) operations.
        possible actions are `add-user`, `update-user`, `delete-user`,
        """
        user.owner = get_owner(user.owner, self.org_name)
        return self.modify_user_by_id(method, user.get_id(), user, columns)

    def modify_user_by_id(self, method: str, id: str, user: User, columns: Optional[List[str]] = None) -> Dict:
        """
        Modify the user from Casdoor providing the ID.

        :param id: the id ( owner/name ) of the user
        :param user: a User object that contains user's info
        """

        url = self.endpoint + f"/api/{method}"
        user.owner = get_owner(user.owner, self.org_name)
        params = {
            "id": id,
            "columns": ",".join(columns) if columns else None,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        user_info = json.dumps(user.to_dict())
        r = self._http_post(url, params=params, data=user_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def get_pagination_users(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the users from Casdoor.

        :param p: the page number, starting from 1
        :param page_size: the count of users in a page
        :param query_map: the filters, e.g. {"field": "name", "value": "abc", "sortOrder": "descend"}
        :return: a tuple of the list of User objects and the total count
        """
        data, total = self.get_pagination("get-users", p, page_size, query_map, owner=self.org_name)
        return [User.from_dict(item) for item in data or []], total

    def add_user(self, user: User) -> Dict:
        response = self.modify_user("add-user", user)
        return response

    def update_user(self, user: User) -> Dict:
        response = self.modify_user("update-user", user)
        return response

    def update_user_by_id(self, id: str, user: User) -> Dict:
        response = self.modify_user_by_id("update-user", id, user)
        return response

    def update_user_for_columns(self, user: User, columns: List[str]) -> Dict:
        """
        Only update the given columns of the user, e.g. ["displayName", "email"].
        """
        return self.modify_user("update-user", user, columns)

    def update_user_by_user_id(self, owner: str, user_id: str, user: User) -> Dict:
        """
        Update the user identified by its user ID (the "id" field of the user).
        """
        return self.do_post("update-user", {"owner": owner, "userId": user_id}, user.to_dict())

    def delete_user(self, user: User) -> Dict:
        response = self.modify_user("delete-user", user)
        return response

    def check_user_password(self, user: User) -> bool:
        """
        Check if user.password is the password of the user.
        """
        user.owner = get_owner(user.owner, self.org_name)
        r = self._http_post(
            self.endpoint + "/api/check-user-password",
            params={"id": user.get_id()},
            data=json.dumps(user.to_dict()),
        )
        return r.json()["status"] == "ok"

    def set_password(self, owner: str, name: str, old_password: str, new_password: str) -> bool:
        """
        Change the password of the user, old_password can be empty for the admin.
        """
        form = {"userOwner": owner, "userName": name, "oldPassword": old_password, "newPassword": new_password}
        return self.do_post("set-password", None, form=form)["status"] == "ok"
