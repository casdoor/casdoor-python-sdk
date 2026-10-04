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

import datetime
import unittest

from src.casdoor import CasdoorSDK
from src.casdoor.order import Order
from src.casdoor.product import Product
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


def new_sdk():
    return CasdoorSDK(TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class OrderTest(unittest.TestCase):
    def test_order(self):
        sdk = new_sdk()
        product_name = get_random_name("OrderProduct")
        order_name = get_random_name("Order")

        product = Product()
        product.owner = TestOrganization
        product.name = product_name
        product.createdTime = now()
        product.displayName = product_name
        product.image = "https://cdn.casbin.org/img/casdoor-logo_1185x256.png"
        product.description = "Casdoor Website"
        product.tag = "auto_created_product_for_plan"
        product.quantity = 999
        product.state = "Published"
        product.providers = ["provider_payment_dummy"]
        product.price = 1
        product.currency = "USD"
        sdk.add_product(product)

        order = Order()
        order.owner = TestOrganization
        order.name = order_name
        order.createdTime = now()
        order.displayName = order_name
        order.products = [product_name]
        order.productInfos = [
            {
                "owner": TestOrganization,
                "name": product_name,
                "displayName": product_name,
                "price": 1,
                "currency": "USD",
                "quantity": 1,
            }
        ]
        order.user = "admin"
        order.price = 1
        order.currency = "USD"
        order.state = "Created"
        sdk.add_order(order)

        self.assertIn(order_name, [item.name for item in sdk.get_orders()])
        _, total = sdk.get_pagination_orders(1, 10)
        self.assertGreater(total, 0)
        self.assertIn(order_name, [item.name for item in sdk.get_user_orders("admin")])

        order = sdk.get_order(order_name)
        self.assertEqual(order.name, order_name)

        order.message = "Updated order message"
        sdk.update_order(order)
        self.assertEqual(sdk.get_order(order_name).message, "Updated order message")

        sdk.cancel_order(order_name)

        sdk.delete_order(order)
        self.assertIsNone(sdk.get_order(order_name))

        sdk.delete_product(product)

    def test_order_pay(self):
        sdk = new_sdk()
        product_name = get_random_name("OrderPayProduct")

        product = Product()
        product.owner = TestOrganization
        product.name = product_name
        product.createdTime = now()
        product.displayName = product_name
        product.image = "https://cdn.casbin.org/img/casdoor-logo_1185x256.png"
        product.description = "Casdoor Website"
        product.tag = "auto_created_product_for_plan"
        product.quantity = 999
        product.state = "Published"
        product.providers = ["provider_payment_dummy"]
        product.price = 1
        product.currency = "USD"
        sdk.add_product(product)

        order = sdk.place_order([{"name": product_name, "quantity": 1}], "admin")
        self.assertTrue(order.name)

        payment = sdk.pay_order(order.name, "provider_payment_dummy")
        self.assertTrue(payment)

        order = sdk.buy_product(product_name, "provider_payment_dummy", "admin")
        self.assertTrue(order.name)

        sdk.delete_product(product)
