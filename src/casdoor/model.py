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

from .user import User
from .util import get_id, get_owner


class Model:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.updatedTime = ""
        self.displayName = ""
        self.manager = ""
        self.contactEmail = ""
        self.type = ""
        self.parentId = ""
        self.isTopModel = False
        self.users = [User]
        self.title = ""
        self.key = ""
        self.children = [Model]
        self.modelText = ""
        self.isEnabled = False
        self.description = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name, model_text):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.modelText = model_text
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        model = cls()
        for key, value in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _ModelSDK:
    def get_models(self) -> List[Dict]:
        """
        Get the models from Casdoor.

        :return: a list of dicts containing model info
        """
        url = self.endpoint + "/api/get-models"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        models = []
        for model in response["data"]:
            models.append(Model.from_dict(model))
        return models

    def get_model(self, model_id: str) -> Dict:
        """
        Get the model from Casdoor providing the model_id.

        :param model_id: the id of the model
        :return: a dict that contains model's info
        """
        url = self.endpoint + "/api/get-model"
        params = {
            "id": get_id(model_id, self.org_name),
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = self._http_get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Model.from_dict(response["data"])

    def modify_model(self, method: str, model: Model, columns: Optional[List[str]] = None) -> Dict:
        url = self.endpoint + f"/api/{method}"
        model.owner = get_owner(model.owner, self.org_name)
        params = {
            "id": f"{model.owner}/{model.name}",
            "columns": ",".join(columns) if columns else None,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        model_info = json.dumps(model.to_dict(), default=self.custom_encoder)
        r = self._http_post(url, params=params, data=model_info)
        response = r.json()
        return response

    def get_pagination_models(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the models from Casdoor.

        :param p: the page number, starting from 1
        :param page_size: the count of models in a page
        :param query_map: the filters, e.g. {"field": "name", "value": "abc", "sortOrder": "descend"}
        :return: a tuple of the list of Model objects and the total count
        """
        data, total = self.get_pagination("get-models", p, page_size, query_map, owner=self.org_name)
        return [Model.from_dict(item) for item in data or []], total

    def add_model(self, model: Model) -> Dict:
        response = self.modify_model("add-model", model)
        return response

    def update_model(self, model: Model) -> Dict:
        response = self.modify_model("update-model", model)
        return response

    def delete_model(self, model: Model) -> Dict:
        response = self.modify_model("delete-model", model)
        return response

    def custom_encoder(self, o):
        if isinstance(o, (Model, User)):
            return o.__dict__
