# Copyright 2026 The Casdoor Authors. All Rights Reserved.
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

from typing import Dict, List, Optional

from .util import get_id


class Record:
    def __init__(self):
        self.id = 0
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.organization = ""
        self.clientIp = ""
        self.user = ""
        self.method = ""
        self.requestUri = ""
        self.action = ""
        self.language = ""
        self.object = ""
        self.response = ""
        self.statusCode = 0
        self.detail = ""
        self.isTriggered = False

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _RecordSDK:
    def get_records(self) -> List[Record]:
        data = self.do_get("get-records", {"owner": self.org_name})
        return [Record.from_dict(item) for item in data or []]

    def get_pagination_records(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        data, total = self.get_pagination("get-records", p, page_size, query_map)
        return [Record.from_dict(item) for item in data or []], total

    def get_record(self, name: str) -> Optional[Record]:
        return Record.from_dict(self.do_get("get-record", {"id": get_id(name, self.org_name)}))

    def add_record(self, record: Record) -> Dict:
        record.owner = record.owner or self.org_name
        record.organization = record.organization or self.org_name
        return self.do_post("add-record", None, record.to_dict())
