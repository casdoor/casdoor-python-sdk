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

from src.casdoor import CasdoorSDK

from .user import User


class Model:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.updatedTime = "string"
        self.displayName = "string"
        self.manager = "string"
        self.contactEmail = "string"
        self.type = "string"
        self.parentId = "string"
        self.isTopModel = True
        self.users = [User]
        self.title = "string"
        self.key = "string"
        self.children = [Model]
        self.isEnabled = True

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class ModelSDK(CasdoorSDK):
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
        r = requests.get(url, params)
        models = r.json()
        return models

    def get_model(self, model_id: str) -> Dict:
        """
        Get the model from Casdoor providing the model_id.

        :param model_id: the id of the model
        :return: a dict that contains model's info
        """
        url = self.endpoint + "/api/get-model"
        params = {
            "id": f"{self.org_name}/{model_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        model = r.json()
        return model

    def modify_model(self, method: str, model: Model) -> Dict:
        url = self.endpoint + f"/api/{method}"
        model.owner = self.org_name
        params = {
            "id": f"{model.owner}/{model.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        model_info = json.dumps(model.to_dict())
        r = requests.post(url, params=params, data=model_info)
        response = r.json()
        return response

    def add_model(self, model: Model) -> Dict:
        response = self.modify_model("add-model", model)
        return response

    def update_model(self, model: Model) -> Dict:
        response = self.modify_model("update-model", model)
        return response

    def delete_model(self, model: Model) -> Dict:
        response = self.modify_model("delete-model", model)
        return response
