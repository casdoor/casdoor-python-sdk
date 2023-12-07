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
from src.casdoor.adapter import Adapter
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class AdapterTest(unittest.TestCase):
    def test_adapter(self):
        name = get_random_name("Adapter")

        # Add a new object
        adapter = Adapter.new(
            owner="admin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            host=name,
            user="https://casdoor.org",
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )

        try:
            sdk.add_adapter(adapter=adapter)
        except Exception as e:
            self.fail("Failed to add object: " + str(e))

        # Get all objects, check if our added object is inside the list
        try:
            adapters = sdk.get_adapters()
        except Exception as e:
            self.fail("Failed to get objects: " + str(e))
        names = [item.name for item in adapters]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            adapter = sdk.get_adapter(name)
        except Exception as e:
            self.fail("Failed to get object: " + str(e))

        self.assertEqual(adapter.name, name, "Retrieved object does not match added object")

        # Update the object
        updated_user = "Updated Casdoor Website"
        adapter.user = updated_user
        try:
            sdk.update_adapter(adapter)
        except Exception as e:
            self.fail("Failed to update object: " + str(e))

        # Validate the update
        try:
            updated_adapter = sdk.get_adapter(name)
        except Exception as e:
            self.fail("Failed to get updated object: " + str(e))

        self.assertEqual(updated_adapter.user, updated_user, "Failed to update object, display_name mismatch")

        # Delete the object
        try:
            sdk.delete_adapter(adapter)
        except Exception as e:
            self.fail("Failed to delete object: " + str(e))

        # Validate the deletion
        try:
            deleted_adapter = sdk.get_adapter(name)
        except Exception as e:
            self.fail("Failed to delete object: " + str(e))

        self.assertIsNone(deleted_adapter, "Failed to delete object, it's still retrievable")
