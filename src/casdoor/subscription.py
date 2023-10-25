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
from datetime import datetime
from typing import Dict, List

import requests


class Subscription:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.startDate = datetime.now()
        self.endDate = datetime.now()
        self.duration = 0
        self.description = "string"
        self.user = "string"
        self.plan = "string"
        self.isEnabled = True
        self.submitter = "string"
        self.approver = "string"
        self.approveTime = "string"
        self.state = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _SubscriptionSDK:
    def get_subscriptions(self) -> List[Dict]:
        """
        Get the subscriptions from Casdoor.

        :return: a list of dicts containing subscription info
        """
        url = self.endpoint + "/api/get-subscriptions"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        subscriptions = r.json()
        return subscriptions

    def get_subscription(self, subscription_id: str) -> Dict:
        """
        Get the subscription from Casdoor providing the subscription_id.

        :param subscription_id: the id of the subscription
        :return: a dict that contains subscription's info
        """
        url = self.endpoint + "/api/get-subscription"
        params = {
            "id": f"{self.org_name}/{subscription_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        subscription = r.json()
        return subscription

    def modify_subscription(self, method: str, subscription: Subscription) -> Dict:
        url = self.endpoint + f"/api/{method}"
        subscription.owner = self.org_name
        params = {
            "id": f"{subscription.owner}/{subscription.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        subscription_info = json.dumps(subscription.to_dict())
        r = requests.post(url, params=params, data=subscription_info)
        response = r.json()
        return response

    def add_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("add-subscription", subscription)
        return response

    def update_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("update-subscription", subscription)
        return response

    def delete_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("delete-subscription", subscription)
        return response
