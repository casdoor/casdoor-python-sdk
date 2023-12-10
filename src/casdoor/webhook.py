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

from .syncer import TableColumn


class Webhook:
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
    def new(cls, owner, name, created_time, organization):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.organization = organization
        return self

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return None
        webhook = cls()
        for key, value in d.items():
            if hasattr(webhook, key):
                setattr(webhook, key, value)
        return webhook

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _WebhookSDK:
    def get_webhooks(self) -> List[Dict]:
        """
        Get the webhooks from Casdoor.

        :return: a list of dicts containing webhook info
        """
        url = self.endpoint + "/api/get-webhooks"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        webhooks = []
        for webhook in response["data"]:
            webhooks.append(Webhook.from_dict(webhook))
        return webhooks

    def get_webhook(self, webhook_id: str) -> Dict:
        """
        Get the webhook from Casdoor providing the webhook_id.

        :param webhook_id: the id of the webhook
        :return: a dict that contains webhook's info
        """
        url = self.endpoint + "/api/get-webhook"
        params = {
            "id": f"{self.org_name}/{webhook_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Webhook.from_dict(response["data"])

    def modify_webhook(self, method: str, webhook: Webhook) -> Dict:
        url = self.endpoint + f"/api/{method}"
        webhook.owner = self.org_name
        params = {
            "id": f"{webhook.owner}/{webhook.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        webhook_info = json.dumps(webhook.to_dict(), default=self.custom_encoder)
        r = requests.post(url, params=params, data=webhook_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def add_webhook(self, webhook: Webhook) -> Dict:
        response = self.modify_webhook("add-webhook", webhook)
        return response

    def update_webhook(self, webhook: Webhook) -> Dict:
        response = self.modify_webhook("update-webhook", webhook)
        return response

    def delete_webhook(self, webhook: Webhook) -> Dict:
        response = self.modify_webhook("delete-webhook", webhook)
        return response

    def custom_encoder(self, o):
        if isinstance(o, (TableColumn)):
            return o.__dict__
