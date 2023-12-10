# Copyright 2023 The Casdoor Authors. All Rights Reserved.
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


class ProductTest(unittest.TestCase):
    def test_product(self):
        name = get_random_name("Product")

        # Add a new object
        product = Product.new(
            owner="admin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            display_name=name,
            image="https://cdn.casbin.org/img/casdoor-logo_1185x256.png",
            description="Casdoor Website",
            tag="auto_created_product_for_plan",
            quantity=999,
            sold=0,
            state="Published",
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        try:
            sdk.add_product(product=product)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            products = sdk.get_products()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in products]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            product = sdk.get_product(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(product.name, name)

        # Update the object
        updated_description = "Updated Casdoor Website"
        product.description = updated_description
        try:
            sdk.update_product(product)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_product = sdk.get_product(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_product.description, updated_description)

        # Delete the object
        try:
            sdk.delete_product(product)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_product = sdk.get_product(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_product, "Failed to delete object, it's still retrievable")
