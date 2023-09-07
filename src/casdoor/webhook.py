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

from .syncer import TableColumn


class Webhook:
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


class WebhookSDK(CasdoorSDK):
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
        webhooks = r.json()
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
        webhook = r.json()
        return webhook

    def modify_webhook(self, method: str, webhook: Webhook) -> Dict:
        url = self.endpoint + f"/api/{method}"
        webhook.owner = self.org_name
        params = {
            "id": f"{webhook.owner}/{webhook.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        webhook_info = json.dumps(webhook.to_dict())
        r = requests.post(url, params=params, data=webhook_info)
        response = r.json()
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
