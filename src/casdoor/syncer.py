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
from typing import Dict, List

import requests


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


class _SyncerSDK:
    def get_syncers(self) -> List[Dict]:
        """
        Get the syncers from Casdoor.

        :return: a list of dicts containing syncer info
        """
        url = self.endpoint + "/api/get-syncers"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        syncers = r.json()
        return syncers

    def get_syncer(self, syncer_id: str) -> Dict:
        """
        Get the syncer from Casdoor providing the syncer_id.

        :param syncer_id: the id of the syncer
        :return: a dict that contains syncer's info
        """
        url = self.endpoint + "/api/get-syncer"
        params = {
            "id": f"{self.org_name}/{syncer_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        syncer = r.json()
        return syncer

    def modify_syncer(self, method: str, syncer: Syncer) -> Dict:
        url = self.endpoint + f"/api/{method}"
        syncer.owner = self.org_name
        params = {
            "id": f"{syncer.owner}/{syncer.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        syncer_info = json.dumps(syncer.to_dict())
        r = requests.post(url, params=params, data=syncer_info)
        response = r.json()
        return response

    def add_syncer(self, syncer: Syncer) -> Dict:
        response = self.modify_syncer("add-syncer", syncer)
        return response

    def update_syncer(self, syncer: Syncer) -> Dict:
        response = self.modify_syncer("update-syncer", syncer)
        return response

    def delete_syncer(self, syncer: Syncer) -> Dict:
        response = self.modify_syncer("delete-syncer", syncer)
        return response
