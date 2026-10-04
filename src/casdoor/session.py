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


class Session:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.application = ""
        self.createdTime = ""
        self.sessionId = [""]
        self.sessionInfos = []
        self.ExclusiveSignin = False

    @classmethod
    def new(cls, owner, name, application, created_time, session_id):
        self = cls()
        self.owner = owner
        self.name = name
        self.application = application
        self.createdTime = created_time
        self.sessionId = session_id
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None
        session = cls()
        for key, value in data.items():
            if hasattr(session, key):
                setattr(session, key, value)
        return session

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _SessionSDK:
    def get_sessions(self) -> List[Dict]:
        """
        Get the sessions from Casdoor.

        :return: a list of dicts containing session info
        """
        url = self.endpoint + "/api/get-sessions"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        sessions = []
        for session in response["data"]:
            sessions.append(Session.from_dict(session))
        return sessions

    def get_session(self, session_id: str, application: str) -> Dict:
        """
        Get the session from Casdoor providing the session_id.

        :param session_id: the id of the session
        :return: a dict that contains session's info
        """
        url = self.endpoint + "/api/get-session"
        params = {
            "id": get_id(session_id, self.org_name),
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "sessionPkId": f"{self.org_name}/{session_id}/{application}",
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Session.from_dict(response["data"])

    def modify_session(self, method: str, session: Session, columns: Optional[List[str]] = None) -> Dict:
        url = self.endpoint + f"/api/{method}"
        session.owner = get_owner(session.owner, self.org_name)
        params = {
            "id": f"{session.owner}/{session.name}",
            "columns": ",".join(columns) if columns else None,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        session_info = json.dumps(session.to_dict())
        r = self._http_post(url, params=params, data=session_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def get_pagination_sessions(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the sessions from Casdoor.

        :param p: the page number, starting from 1
        :param page_size: the count of sessions in a page
        :param query_map: the filters, e.g. {"field": "name", "value": "abc", "sortOrder": "descend"}
        :return: a tuple of the list of Session objects and the total count
        """
        data, total = self.get_pagination("get-sessions", p, page_size, query_map, owner=self.org_name)
        return [Session.from_dict(item) for item in data or []], total

    def update_session_for_columns(self, session: Session, columns: List[str]) -> Dict:
        """
        Only update the given columns of the session, e.g. ["display_name"].
        """
        return self.modify_session("update-session", session, columns)

    def add_session(self, session: Session) -> Dict:
        response = self.modify_session("add-session", session)
        return response

    def update_session(self, session: Session) -> Dict:
        response = self.modify_session("update-session", session)
        return response

    def delete_session(self, session: Session) -> Dict:
        response = self.modify_session("delete-session", session)
        return response
