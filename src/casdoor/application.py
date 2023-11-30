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
from typing import List

import requests

# from .organization import Organization, ThemeData
from .provider import Provider


class ProviderItem:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.canSignUp = False
        self.canSignIn = False
        self.canUnlink = False
        self.prompted = False
        self.alertType = ""
        self.rule = ""
        self.provider = Provider

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class SignupItem:
    def __init__(self):
        self.name = ""
        self.visible = False
        self.required = False
        self.prompted = False
        self.rule = ""

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class Application:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.logo = ""
        self.homepageUrl = ""
        self.description = ""
        self.organization = ""
        self.cert = ""
        self.enablePassword = False
        self.enableSignUp = False
        self.enableSigninSession = False
        self.enableAutoSignin = False
        self.enableCodeSignin = False
        self.enableSamlCompress = False
        self.enableWebAuthn = False
        self.enableLinkWithEmail = False
        self.orgChoiceMode = ""
        self.samlReplyUrl = ""
        # self.providers = [ProviderItem]
        # self.signupItems = [SignupItem]
        self.grantTypes = [""]
        # self.organizationObj = Organization
        self.tags = [""]
        self.clientId = ""
        self.clientSecret = ""
        self.redirectUris = [""]
        self.tokenFormat = ""
        self.expireInHours = 0
        self.refreshExpireInHours = 0
        self.signupUrl = ""
        self.signinUrl = ""
        self.forgetUrl = ""
        self.affiliationUrl = ""
        self.termsOfUse = ""
        self.signupHtml = ""
        self.signinHtml = ""
        # self.themeData = ThemeData

    @classmethod
    def new(cls, owner, name, created_time, display_name, logo, homepage_url, description, organization):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.logo = logo
        self.homepageUrl = homepage_url
        self.description = description
        self.organization = organization
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        app = cls()
        for key, value in data.items():
            if hasattr(app, key):
                setattr(app, key, value)
        return app

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _ApplicationSDK:
    def get_applications(self) -> List[Application]:
        """
        Get the applications from Casdoor.

        :return: a list of dicts containing application info
        """
        url = self.endpoint + "/api/get-applications"
        params = {
            "owner": "admin",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])

        res = []
        for element in response["data"]:
            res.append(Application.from_dict(element))
        return res

    def get_application(self, application_id: str) -> Application:
        """
        Get the application from Casdoor providing the application_id.

        :param application_id: the id of the application
        :return: a dict that contains application's info
        """
        url = self.endpoint + "/api/get-application"
        params = {
            "id": f"admin/{application_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])
        return Application.from_dict(response["data"])

    def modify_application(self, method: str, application: Application) -> str:
        url = self.endpoint + f"/api/{method}"
        if application.owner == "":
            application.owner = self.org_name
        params = {
            "id": f"{application.owner}/{application.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        application_info = json.dumps(application.to_dict())
        r = requests.post(url, params=params, data=application_info)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])
        return str(response["data"])

    def add_application(self, application: Application) -> str:
        application.owner = "admin"
        response = self.modify_application("add-application", application)
        return response

    def update_application(self, application: Application) -> str:
        application.owner = "admin"
        response = self.modify_application("update-application", application)
        return response

    def delete_application(self, application: Application) -> str:
        application.owner = "admin"
        response = self.modify_application("delete-application", application)
        return response
