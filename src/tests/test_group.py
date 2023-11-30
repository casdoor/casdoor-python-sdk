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
from src.casdoor.group import Group
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class GroupTest(unittest.TestCase):
    def test_group(self):
        name = get_random_name("group")

        # Add a new object
        group = Group.new(owner="admin", name=name, created_time=datetime.datetime.now().isoformat(), display_name=name)

        sdk = CasdoorSDK(TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication)

        try:
            sdk.add_group(group)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            groups = sdk.get_groups()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in groups]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            retrieved_group = sdk.get_group(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(name, retrieved_group.name, "Retrieved object does not match added object")

        # Update the object
        updated_display_name = "updated_display_name"
        retrieved_group.displayName = updated_display_name
        try:
            updated_group = sdk.update_group(retrieved_group)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_group = sdk.get_group(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(
            updated_display_name, updated_group.displayName, "Failed to update object, display_name mismatch"
        )

        # Delete the object
        try:
            sdk.delete_group(group)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_group = sdk.get_group(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_group, "Failed to delete object, it's still retrievable")
