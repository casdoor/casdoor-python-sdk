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


class Provider:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.category = "string"
        self.type = "string"
        self.subType = "string"
        self.method = "string"
        self.clientId = "string"
        self.clientSecret = "string"
        self.clientId2 = "string"
        self.clientSecret2 = "string"
        self.cert = "string"
        self.customAuthUrl = "string"
        self.customTokenUrl = "string"
        self.customUserInfoUrl = "string"
        self.customLogo = "string"
        self.scopes = "string"
        self.userMapping = {"string": "string"}
        self.host = "string"
        self.port = 0
        self.disableSsl = True
        self.title = "string"
        self.content = "string"
        self.receiver = "string"
        self.regionId = "string"
        self.signName = "string"
        self.templateCode = "string"
        self.appId = "string"
        self.endpoint = "string"
        self.intranetEndpoint = "string"
        self.domain = "string"
        self.bucket = "string"
        self.pathPrefix = "string"
        self.metadata = "string"
        self.idP = "string"
        self.issuerUrl = "string"
        self.enableSignAuthnRequest = False
        self.providerUrl = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__
