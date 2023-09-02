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

class Permission:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.description = "string"
        self.users = ["string"]
        self.roles = ["string"]
        self.domains = ["string"]
        self.model = "string"
        self.adapter = "string"
        self.resourceType = "string"
        self.resources = ["string"]
        self.actions = ["string"]
        self.effect = "string"
        self.isEnabled = True
        self.submitter = "string"
        self.approver = "string"
        self.approveTime = "string"
        self.state = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__
