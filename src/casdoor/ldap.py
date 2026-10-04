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

from .util import get_admin_id, get_id, get_owner


class Ldap:
    def __init__(self):
        self.id = ""
        self.owner = ""
        self.createdTime = ""
        self.serverName = ""
        self.host = ""
        self.port = 0
        self.enableSsl = False
        self.allowSelfSignedCert = False
        self.username = ""
        self.password = ""
        self.baseDn = ""
        self.filter = ""
        self.filterFields = []
        self.defaultGroup = ""
        self.defaultGroups = []
        self.passwordType = ""
        self.customAttributes = {}
        self.autoSync = 0
        self.lastSync = ""
        self.enableGroups = False
        self.enablePasswordReset = False

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


class _LdapSDK:
    def get_ldaps(self) -> List[Ldap]:
        """
        Get all the ldaps from Casdoor.
        """
        data = self.do_get("get-ldaps", {"owner": "admin"})
        return [Ldap.from_dict(item) for item in data or []]

    def get_ldap(self, id: str) -> Optional[Ldap]:
        """
        Get the ldap by name, or by "owner/name" ID.
        """
        return Ldap.from_dict(self.do_get("get-ldap", {"id": get_admin_id(id)}))

    def get_ldap_users(self, id: str) -> Dict:
        """
        Get the users of the LDAP server, return {"users": [...], "existUuids": [...]}.
        """
        return self.do_get("get-ldap-users", {"id": get_id(id, self.org_name)})

    def sync_ldap_users(self, id: str, users: List[Dict]) -> Dict:
        """
        Sync the LDAP users into Casdoor, return {"exist": [...], "failed": [...]}.
        """
        return self.do_post("sync-ldap-users", {"id": get_id(id, self.org_name)}, users)["data"]

    def sync_ldap_users_from_server(self, id: str) -> Dict:
        """
        Fetch all the users from the LDAP server and sync them into Casdoor.
        """
        users = self.get_ldap_users(id).get("users") or []
        return self.sync_ldap_users(id, users)

    def modify_ldap(
        self, method: str, ldap: Ldap, columns: Optional[List[str]] = None, params: Optional[Dict] = None
    ) -> Dict:
        ldap.owner = get_owner(ldap.owner, "admin")
        query = dict(params or {})
        query["id"] = f"{ldap.owner}/{ldap.id}"
        if columns:
            query["columns"] = ",".join(columns)
        return self.do_post(method, query, ldap.to_dict())

    def add_ldap(self, ldap: Ldap) -> Dict:
        return self.modify_ldap("add-ldap", ldap)

    def update_ldap(self, ldap: Ldap) -> Dict:
        return self.modify_ldap("update-ldap", ldap)

    def delete_ldap(self, ldap: Ldap) -> Dict:
        return self.modify_ldap("delete-ldap", ldap)
