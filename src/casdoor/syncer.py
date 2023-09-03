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


class TableColumn:
    def __init__(self):
        self.name = "string"
        self.type = "string"
        self.casdoorName = "string"
        self.isKey = True
        self.isHashed = True
        self.values = ["string"]

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class Syncer:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.organization = "string"
        self.type = "string"
        self.host = "string"
        self.port = 0
        self.user = "string"
        self.password = "string"
        self.databaseType = "string"
        self.database = "string"
        self.table = "string"
        self.tablePrimaryKey = "string"
        self.tableColumns = [TableColumn]
        self.affiliationTable = "string"
        self.avatarBaseUrl = "string"
        self.errorText = "string"
        self.syncInterval = 0
        self.isReadOnly = True
        self.isEnabled = True

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__
