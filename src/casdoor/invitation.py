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


class Invitation:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.updatedTime = ""
        self.displayName = ""
        self.code = ""
        self.isRegexp = False
        self.quota = 0
        self.usedCount = 0
        self.application = ""
        self.username = ""
        self.email = ""
        self.phone = ""
        self.signupGroup = ""
        self.defaultCode = ""
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


class _InvitationSDK:
    def get_invitations(self) -> List[Invitation]:
        """
        Get all the invitations from Casdoor.
        """
        data = self.do_get("get-invitations", {"owner": self.org_name})
        return [Invitation.from_dict(item) for item in data or []]

    def get_pagination_invitations(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the invitations from Casdoor, return a tuple of the invitations and the total count.
        """
        data, total = self.get_pagination("get-invitations", p, page_size, query_map)
        return [Invitation.from_dict(item) for item in data or []], total

    def get_invitation(self, name: str) -> Optional[Invitation]:
        """
        Get the invitation by name, or by "owner/name" ID.
        """
        return Invitation.from_dict(self.do_get("get-invitation", {"id": get_id(name, self.org_name)}))

    def get_invitation_info(self, code: str, application_name: str) -> Optional[Invitation]:
        """
        Get the invitation of the invitation code for the application.
        """
        data = self.do_get("get-invitation-info", {"applicationId": f"admin/{application_name}", "code": code})
        return Invitation.from_dict(data)

    def modify_invitation(
        self, method: str, invitation: Invitation, columns: Optional[List[str]] = None, params: Optional[Dict] = None
    ) -> Dict:
        invitation.owner = get_owner(invitation.owner, self.org_name)
        query = dict(params or {})
        query["id"] = f"{invitation.owner}/{invitation.name}"
        if columns:
            query["columns"] = ",".join(columns)
        return self.do_post(method, query, invitation.to_dict())

    def add_invitation(self, invitation: Invitation) -> Dict:
        return self.modify_invitation("add-invitation", invitation)

    def update_invitation(self, invitation: Invitation) -> Dict:
        return self.modify_invitation("update-invitation", invitation)

    def update_invitation_for_columns(self, invitation: Invitation, columns: List[str]) -> Dict:
        return self.modify_invitation("update-invitation", invitation, columns)

    def delete_invitation(self, invitation: Invitation) -> Dict:
        return self.modify_invitation("delete-invitation", invitation)
