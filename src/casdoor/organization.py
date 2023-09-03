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


class AccountItem:
    def __init__(self):
        self.name = "string"
        self.visible = False
        self.viewRule = "string"
        self.modifyRule = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class ThemeData:
    def __init__(self):
        self.themeType = "string"
        self.colorPrimary = "string"
        self.borderRadius = 0
        self.isCompact = False
        self.isEnabled = False

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class MfaItem:
    def __init__(self):
        self.name = "string"
        self.rule = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class Organization:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.websiteUrl = "string"
        self.favicon = "string"
        self.passwordType = "string"
        self.passwordSalt = "string"
        self.passwordOptions = ["string"]
        self.countryCodes = ["string"]
        self.defaultAvatar = "string"
        self.defaultApplication = "string"
        self.tags = ["string"]
        self.languages = ["string"]
        self.themeData = ThemeData
        self.masterPassword = "string"
        self.initScore = 0
        self.enableSoftDeletion = True
        self.isProfilePublic = True
        self.mfaItems = [MfaItem]
        self.accountItems = [AccountItem]

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__
