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

from .provider import Provider


class Product:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.image = ""
        self.detail = ""
        self.description = ""
        self.tag = ""
        self.currency = ""
        self.price = 0.0
        self.quantity = 0
        self.sold = 0
        self.providers = [""]
        self.returnUrl = ""
        self.state = ""
        self.providerObjs = [Provider]

    @classmethod
    def new(cls, owner, name, created_time, display_name, image, description, tag, quantity, sold, state):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.image = image
        self.description = description
        self.tag = tag
        self.quantity = quantity
        self.sold = sold
        self.state = state
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        product = cls()
        for key, value in data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        return product

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _ProductSDK:
    def get_products(self) -> List[Dict]:
        """
        Get the products from Casdoor.

        :return: a list of dicts containing product info
        """
        url = self.endpoint + "/api/get-products"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        products = []
        for product in response["data"]:
            products.append(Product.from_dict(product))
        return products

    def get_product(self, product_id: str) -> Dict:
        """
        Get the product from Casdoor providing the product_id.

        :param product_id: the id of the product
        :return: a dict that contains product's info
        """
        url = self.endpoint + "/api/get-product"
        params = {
            "id": f"{self.org_name}/{product_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])

        return Product.from_dict(response["data"])

    def modify_product(self, method: str, product: Product) -> Dict:
        url = self.endpoint + f"/api/{method}"
        product.owner = self.org_name
        params = {
            "id": f"{product.owner}/{product.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        product_info = json.dumps(product.to_dict(), default=self.custom_encoder)
        r = requests.post(url, params=params, data=product_info)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def add_product(self, product: Product) -> Dict:
        response = self.modify_product("add-product", product)
        return response

    def update_product(self, product: Product) -> Dict:
        response = self.modify_product("update-product", product)
        return response

    def delete_product(self, product: Product) -> Dict:
        response = self.modify_product("delete-product", product)
        return response

    def custom_encoder(self, o):
        if isinstance(o, (Provider)):
            return o.__dict__
