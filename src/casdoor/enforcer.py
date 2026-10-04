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
from typing import Dict, List, Optional

from .util import get_id, get_owner


class Enforcer:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.updatedTime = ""
        self.displayName = ""
        self.description = ""
        self.model = ""
        self.adapter = ""
        self.isEnabled = False
        self.modelCfg = {}

    @classmethod
    def new(cls, owner, name, created_time, display_name, description, model, adapter):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.description = description
        self.model = model
        self.adapter = adapter
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        enforcer = cls()
        for key, value in data.items():
            if hasattr(enforcer, key):
                setattr(enforcer, key, value)
        return enforcer

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _EnforcerSDK:
    def get_enforcers(self) -> List[Dict]:
        """
        Get the enforcers from Casdoor.

        :return: a list of dicts containing enforcer info
        """
        url = self.endpoint + "/api/get-enforcers"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        enforcers = []
        for enforcer in response["data"]:
            enforcers.append(Enforcer.from_dict(enforcer))
        return enforcers

    def get_enforcer(self, enforcer_id: str) -> Dict:
        """
        Get the enforcer from Casdoor providing the enforcer_id.

        :param enforcer_id: the id of the enforcer
        :return: a dict that contains enforcer's info
        """
        url = self.endpoint + "/api/get-enforcer"
        params = {
            "id": get_id(enforcer_id, self.org_name),
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])

        return Enforcer.from_dict(response["data"])

    def modify_enforcer(self, method: str, enforcer: Enforcer, columns: Optional[List[str]] = None) -> Dict:
        url = self.endpoint + f"/api/{method}"
        enforcer.owner = get_owner(enforcer.owner, self.org_name)
        params = {
            "id": f"{enforcer.owner}/{enforcer.name}",
            "columns": ",".join(columns) if columns else None,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        enforcer_info = json.dumps(enforcer.to_dict())
        r = self._http_post(url, params=params, data=enforcer_info)
        response = r.json()
        return response

    def get_pagination_enforcers(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the enforcers from Casdoor.

        :param p: the page number, starting from 1
        :param page_size: the count of enforcers in a page
        :param query_map: the filters, e.g. {"field": "name", "value": "abc", "sortOrder": "descend"}
        :return: a tuple of the list of Enforcer objects and the total count
        """
        data, total = self.get_pagination("get-enforcers", p, page_size, query_map, owner=self.org_name)
        return [Enforcer.from_dict(item) for item in data or []], total

    def add_enforcer(self, enforcer: Enforcer) -> Dict:
        response = self.modify_enforcer("add-enforcer", enforcer)
        return response

    def update_enforcer(self, enforcer: Enforcer) -> Dict:
        response = self.modify_enforcer("update-enforcer", enforcer)
        return response

    def delete_enforcer(self, enforcer: Enforcer) -> Dict:
        response = self.modify_enforcer("delete-enforcer", enforcer)
        return response
