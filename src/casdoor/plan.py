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


class Plan:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.description = ""
        self.pricePerMonth = 0.0
        self.pricePerYear = 0.0
        self.currency = ""
        self.isEnabled = False
        self.role = ""
        self.options = [""]

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

        plan = cls()
        for key, value in data.items():
            if hasattr(plan, key):
                setattr(plan, key, value)
        return plan

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _PlanSDK:
    def get_plans(self) -> List[Dict]:
        """
        Get the plans from Casdoor.

        :return: a list of dicts containing plan info
        """
        url = self.endpoint + "/api/get-plans"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        plans = []
        for plan in response["data"]:
            plans.append(Plan.from_dict(plan))
        return plans

    def get_plan(self, plan_id: str) -> Dict:
        """
        Get the plan from Casdoor providing the plan_id.

        :param plan_id: the id of the plan
        :return: a dict that contains plan's info
        """
        url = self.endpoint + "/api/get-plan"
        params = {
            "id": f"{self.org_name}/{plan_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])

        return Plan.from_dict(response["data"])

    def modify_plan(self, method: str, plan: Plan) -> Dict:
        url = self.endpoint + f"/api/{method}"
        plan.owner = self.org_name
        params = {
            "id": f"{plan.owner}/{plan.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        plan_info = json.dumps(plan.to_dict())
        r = requests.post(url, params=params, data=plan_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def add_plan(self, plan: Plan) -> Dict:
        response = self.modify_plan("add-plan", plan)
        return response

    def update_plan(self, plan: Plan) -> Dict:
        response = self.modify_plan("update-plan", plan)
        return response

    def delete_plan(self, plan: Plan) -> Dict:
        response = self.modify_plan("delete-plan", plan)
        return response
