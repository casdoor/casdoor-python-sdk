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
