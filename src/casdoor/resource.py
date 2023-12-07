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


class Resource:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.user = ""
        self.provider = ""
        self.application = ""
        self.tag = ""
        self.parent = ""
        self.fileName = ""
        self.fileType = ""
        self.fileFormat = ""
        self.fileSize = 0
        self.url = ""
        self.description = ""

    @classmethod
    def new(cls, owner, name):
        self = cls()
        self.owner = owner
        self.name = name
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None
        resource = cls()
        for key, value in data.items():
            setattr(resource, key, value)
        return resource

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _ResourceSDK:
    def get_resources(self, owner, user, field, value, sort_field, sort_order) -> List[Dict]:
        """
        Get the resources from Casdoor.

        :return: a list of dicts containing resource info
        """
        url = self.endpoint + "/api/get-resources"
        params = {
            "owner": owner,
            "user": user,
            "field": field,
            "value": value,
            "sortField": sort_field,
            "sortOrder": sort_order,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        resources = []
        for resource in response["data"]:
            resources.append(Resource.from_dict(resource))
        return resources

    def get_resource(self, resource_id: str) -> Dict:
        """
        Get the resource from Casdoor providing the resource_id.

        :param resource_id: the id of the resource
        :return: a dict that contains resource's info
        """
        url = self.endpoint + "/api/get-resource"
        params = {
            "id": f"{self.org_name}/{resource_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])

        return Resource.from_dict(response["data"])

    def modify_resource(self, method: str, resource: Resource) -> Dict:
        url = self.endpoint + f"/api/{method}"
        resource.owner = self.org_name
        params = {
            "id": f"{resource.owner}/{resource.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        resource_info = json.dumps(resource.to_dict())
        r = requests.post(url, params=params, data=resource_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def add_resource(self, resource: Resource) -> Dict:
        response = self.modify_resource("add-resource", resource)
        return response

    def update_resource(self, resource: Resource) -> Dict:
        response = self.modify_resource("update-resource", resource)
        return response

    def delete_resource(self, resource: Resource) -> Dict:
        response = self.modify_resource("delete-resource", resource)
        return response
