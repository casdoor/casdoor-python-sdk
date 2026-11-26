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

from .util import get_id, get_owner


class Key:
    """
    An access key and access secret, whose type is the scope it belongs to: "Organization", "Application",
    "User" or "General".
    """

    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.updatedTime = ""
        self.displayName = ""
        self.type = ""
        self.organization = ""
        self.application = ""
        self.user = ""
        self.accessKey = ""
        self.accessSecret = ""
        self.expireTime = ""
        self.state = ""

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


class _KeySDK:
    def get_global_keys(self) -> List[Key]:
        """
        Get the keys of all organizations.
        """
        data = self.do_get("get-global-keys")
        return [Key.from_dict(item) for item in data or []]

    def get_keys(self) -> List[Key]:
        """
        Get the keys of the organization, the access secrets are masked.
        """
        data = self.do_get("get-keys", {"owner": self.org_name})
        return [Key.from_dict(item) for item in data or []]

    def get_pagination_keys(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the keys, return a tuple of the keys and the total count.
        """
        data, total = self.get_pagination("get-keys", p, page_size, query_map)
        return [Key.from_dict(item) for item in data or []], total

    def get_key(self, name: str) -> Optional[Key]:
        """
        Get the key by name, or by "owner/name" ID, with its access secret in plain text.
        """
        return Key.from_dict(self.do_get("get-key", {"id": get_id(name, self.org_name)}))

    def modify_key(self, method: str, key: Key) -> Dict:
        key.owner = get_owner(key.owner, self.org_name)
        return self.do_post(method, {"id": f"{key.owner}/{key.name}"}, key.to_dict())

    def add_key(self, key: Key) -> Dict:
        """
        Add a key. Casdoor generates the access key and the access secret, use get_key() to read them.
        """
        return self.modify_key("add-key", key)

    def update_key(self, key: Key) -> Dict:
        """
        Update a key. The access key and the access secret can't be changed.
        """
        return self.modify_key("update-key", key)

    def delete_key(self, key: Key) -> Dict:
        return self.modify_key("delete-key", key)
