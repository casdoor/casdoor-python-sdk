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

class Cert:
    def __init__(self):
        self.name = "string"
        self.owner = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.type = "string"
        self.scope = "string"
        self.cryptoAlgorithm = "string"
        self.bitSize = 0
        self.expireInYears = 0
        self.certificate = "string"
        self.privateKey = "string"
        self.authorityPublicKey = "string"
        self.authorityRootPublicKey = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__
