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

from .provider import Provider
from .organization import Organization, ThemeData


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
