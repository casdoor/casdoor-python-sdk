# Copyright 2026 The Casdoor Authors. All Rights Reserved.
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

from typing import Dict, List, Optional

from .util import get_id, get_owner


class Order:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.updateTime = ""
        self.displayName = ""
        self.products = []
        self.productInfos = []
        self.user = ""
        self.payment = ""
        self.price = 0.0
        self.currency = ""
        self.state = ""
        self.message = ""
        self.couponName = ""
        self.couponDiscount = 0.0

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _OrderSDK:
    def get_orders(self) -> List[Order]:
        """
        Get all the orders from Casdoor.
        """
        data = self.do_get("get-orders", {"owner": self.org_name})
        return [Order.from_dict(item) for item in data or []]

    def get_pagination_orders(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the orders from Casdoor, return a tuple of the orders and the total count.
        """
        data, total = self.get_pagination("get-orders", p, page_size, query_map)
        return [Order.from_dict(item) for item in data or []], total

    def get_order(self, name: str) -> Optional[Order]:
        """
        Get the order by name, or by "owner/name" ID.
        """
        return Order.from_dict(self.do_get("get-order", {"id": get_id(name, self.org_name)}))

    def get_user_orders(self, user_name: str) -> List[Order]:
        data = self.do_get("get-user-orders", {"owner": self.org_name, "user": user_name})
        return [Order.from_dict(item) for item in data or []]

    def place_order(self, product_infos: List[Dict], user_name: str = "") -> Optional[Order]:
        """
        Create an order of the products, e.g. [{"name": "product", "quantity": 1}], for the user.
        """
        params = {"owner": self.org_name, "userName": user_name or None}
        return Order.from_dict(self.do_post("place-order", params, {"productInfos": product_infos})["data"])

    def pay_order(self, order_name: str, provider_name: str) -> Dict:
        """
        Create a payment of the order with the payment provider, return the payment.
        """
        params = {"id": get_id(order_name, self.org_name), "providerName": provider_name}
        return self.do_post("pay-order", params, "")["data"]

    def buy_product(self, name: str, provider_name: str, user_name: str = "") -> Optional[Order]:
        """
        Place an order of a single product, provider_name is kept for compatibility.
        """
        return self.place_order([{"name": name, "quantity": 1}], user_name)

    def cancel_order(self, name: str) -> Dict:
        return self.do_post("cancel-order", {"id": get_id(name, self.org_name)}, "")

    def modify_order(
        self, method: str, order: Order, columns: Optional[List[str]] = None, params: Optional[Dict] = None
    ) -> Dict:
        order.owner = get_owner(order.owner, self.org_name)
        query = dict(params or {})
        query["id"] = f"{order.owner}/{order.name}"
        if columns:
            query["columns"] = ",".join(columns)
        return self.do_post(method, query, order.to_dict())

    def add_order(self, order: Order) -> Dict:
        return self.modify_order("add-order", order)

    def update_order(self, order: Order) -> Dict:
        return self.modify_order("update-order", order)

    def delete_order(self, order: Order) -> Dict:
        return self.modify_order("delete-order", order)
