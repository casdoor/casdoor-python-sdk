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
        self.name = ""
        self.type = ""
        self.casdoorName = ""
        self.isKey = False
        self.isHashed = False
        self.values = [""]

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class Syncer:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.organization = ""
        self.type = ""
        self.host = ""
        self.port = 0
        self.user = ""
        self.password = ""
        self.databaseType = ""
        self.database = ""
        self.table = ""
        self.tablePrimaryKey = ""
        self.tableColumns = [TableColumn]
        self.affiliationTable = ""
        self.avatarBaseUrl = ""
        self.errorText = ""
        self.syncInterval = 0
        self.isReadOnly = False
        self.isEnabled = False

    @classmethod
    def new(
        cls,
        owner,
        name,
        created_time,
        organization,
        host,
        port,
        user,
        password,
        database_type,
        database,
        table,
        sync_interval,
    ):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.organization = organization
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.databaseType = database_type
        self.database = database
        self.table = table
        self.syncInterval = sync_interval
        return self

    @classmethod
    def from_dict(cls, d: dict):
        if not d:
            return None

        syncer = cls()
        for key, value in d.items():
            if hasattr(syncer, key):
                setattr(syncer, key, value)
        return syncer

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
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        syncers = []
        for syncer in response["data"]:
            syncers.append(Syncer.from_dict(syncer))
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
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Syncer.from_dict(response["data"])

    def modify_syncer(self, method: str, syncer: Syncer) -> Dict:
        url = self.endpoint + f"/api/{method}"
        syncer.owner = self.org_name
        params = {
            "id": f"{syncer.owner}/{syncer.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        syncer_info = json.dumps(syncer.to_dict(), default=self.custom_encoder)
        r = requests.post(url, params=params, data=syncer_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
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

    def custom_encoder(self, o):
        if isinstance(o, (TableColumn)):
            return o.__dict__
