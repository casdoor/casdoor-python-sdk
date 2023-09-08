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

from .organization import Organization, ThemeData
from .provider import Provider


class ProviderItem:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.canSignUp = True
        self.canSignIn = True
        self.canUnlink = True
        self.prompted = True
        self.alertType = "string"
        self.rule = "string"
        self.provider = Provider

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class SignupItem:
    def __init__(self):
        self.name = "string"
        self.visible = True
        self.required = True
        self.prompted = True
        self.rule = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class Application:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.logo = "string"
        self.homepageUrl = "string"
        self.description = "string"
        self.organization = "string"
        self.cert = "string"
        self.enablePassword = True
        self.enableSignUp = True
        self.enableSigninSession = True
        self.enableAutoSignin = True
        self.enableCodeSignin = True
        self.enableSamlCompress = True
        self.enableWebAuthn = True
        self.enableLinkWithEmail = True
        self.orgChoiceMode = "string"
        self.samlReplyUrl = "string"
        self.providers = [ProviderItem]
        self.signupItems = [SignupItem]
        self.grantTypes = ["string"]
        self.organizationObj = Organization
        self.tags = ["string"]
        self.clientId = "string"
        self.clientSecret = "string"
        self.redirectUris = ["string"]
        self.tokenFormat = "string"
        self.expireInHours = 0
        self.refreshExpireInHours = 0
        self.signupUrl = "string"
        self.signinUrl = "string"
        self.forgetUrl = "string"
        self.affiliationUrl = "string"
        self.termsOfUse = "string"
        self.signupHtml = "string"
        self.signinHtml = "string"
        self.themeData = ThemeData

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _ApplicationSDK:
    def get_applications(self) -> List[Dict]:
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
        applications = r.json()
        return applications

    def get_application(self, application_id: str) -> Dict:
        """
        Get the application from Casdoor providing the application_id.

        :param application_id: the id of the application
        :return: a dict that contains application's info
        """
        url = self.endpoint + "/api/get-application"
        params = {
            "id": f"{self.org_name}/{application_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        application = r.json()
        return application

    def modify_application(self, method: str, application: Application) -> Dict:
        url = self.endpoint + f"/api/{method}"
        application.owner = self.org_name
        params = {
            "id": f"{application.owner}/{application.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        application_info = json.dumps(application.to_dict())
        r = requests.post(url, params=params, data=application_info)
        response = r.json()
        return response

    def add_application(self, application: Application) -> Dict:
        response = self.modify_application("add-application", application)
        return response

    def update_application(self, application: Application) -> Dict:
        response = self.modify_application("update-application", application)
        return response

    def delete_application(self, application: Application) -> Dict:
        response = self.modify_application("delete-application", application)
        return response
