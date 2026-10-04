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
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .util import get_id, get_owner


class Subscription:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.startTime = datetime.now(timezone.utc).isoformat()
        self.endTime = datetime.now(timezone.utc).isoformat()
        self.duration = 0
        self.description = ""
        self.user = ""
        self.plan = ""
        self.isEnabled = False
        self.submitter = ""
        self.approver = ""
        self.approveTime = ""
        self.state = ""
        self.group = ""
        self.pricing = ""
        self.payment = ""
        self.period = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name, description):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.description = description
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        subscription = cls()
        for key, value in data.items():
            if hasattr(subscription, key):
                setattr(subscription, key, value)
        return subscription

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
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        subscriptions = []
        for subscription in response["data"]:
            subscriptions.append(Subscription.from_dict(subscription))
        return subscriptions

    def get_subscription(self, subscription_id: str) -> Dict:
        """
        Get the subscription from Casdoor providing the subscription_id.

        :param subscription_id: the id of the subscription
        :return: a dict that contains subscription's info
        """
        url = self.endpoint + "/api/get-subscription"
        params = {
            "id": get_id(subscription_id, self.org_name),
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Subscription.from_dict(response["data"])

    def modify_subscription(self, method: str, subscription: Subscription, columns: Optional[List[str]] = None) -> Dict:
        url = self.endpoint + f"/api/{method}"
        subscription.owner = get_owner(subscription.owner, self.org_name)
        params = {
            "id": f"{subscription.owner}/{subscription.name}",
            "columns": ",".join(columns) if columns else None,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        subscription_info = json.dumps(subscription.to_dict())
        r = self._http_post(url, params=params, data=subscription_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def get_pagination_subscriptions(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the subscriptions from Casdoor.

        :param p: the page number, starting from 1
        :param page_size: the count of subscriptions in a page
        :param query_map: the filters, e.g. {"field": "name", "value": "abc", "sortOrder": "descend"}
        :return: a tuple of the list of Subscription objects and the total count
        """
        data, total = self.get_pagination("get-subscriptions", p, page_size, query_map, owner=self.org_name)
        return [Subscription.from_dict(item) for item in data or []], total

    def add_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("add-subscription", subscription)
        return response

    def update_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("update-subscription", subscription)
        return response

    def delete_subscription(self, subscription: Subscription) -> Dict:
        response = self.modify_subscription("delete-subscription", subscription)
        return response
