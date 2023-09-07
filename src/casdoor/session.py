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
import json
from typing import Dict, List

import requests

from .main import CasdoorSDK


class Session:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.application = "string"
        self.createdTime = "string"
        self.sessionId = ["string"]

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class SessionSDK(CasdoorSDK):
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
        r = requests.get(url, params)
        sessions = r.json()
        return sessions

    def get_session(self, session_id: str) -> Dict:
        """
        Get the session from Casdoor providing the session_id.

        :param session_id: the id of the session
        :return: a dict that contains session's info
        """
        url = self.endpoint + "/api/get-session"
        params = {
            "id": f"{self.org_name}/{session_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        session = r.json()
        return session

    def modify_session(self, method: str, session: Session) -> Dict:
        url = self.endpoint + f"/api/{method}"
        session.owner = self.org_name
        params = {
            "id": f"{session.owner}/{session.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        session_info = json.dumps(session.to_dict())
        r = requests.post(url, params=params, data=session_info)
        response = r.json()
        return response

    def add_session(self, session: Session) -> Dict:
        response = self.modify_session("add-session", session)
        return response

    def update_session(self, session: Session) -> Dict:
        response = self.modify_session("update-session", session)
        return response

    def delete_session(self, session: Session) -> Dict:
        response = self.modify_session("delete-session", session)
        return response
