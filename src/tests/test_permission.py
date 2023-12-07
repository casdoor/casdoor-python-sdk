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
from src.casdoor.permission import Permission
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class permissionTest(unittest.TestCase):
    def test_permission(self):
        name = get_random_name("Permission")

        # Add a new object
        permission = Permission.new(
            owner="casbin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            display_name=name,
            description="Casdoor Website",
            users=["casbin/*"],
            roles=[],
            domains=[],
            model="user-model-built-in",
            resource_type="Application",
            resources=["app-casbin"],
            actions=["Read", "Write"],
            effect="Allow",
            is_enabled=True,
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        try:
            sdk.add_permission(permission=permission)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            permissions = sdk.get_permissions()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in permissions]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            permission = sdk.get_permission(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(permission.name, name)

        # Update the object
        updated_description = "Updated Casdoor Website"
        permission.description = updated_description
        try:
            sdk.update_permission(permission)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_permission = sdk.get_permission(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_permission.description, updated_description)

        # Delete the object
        try:
            sdk.delete_permission(permission)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_permission = sdk.get_permission(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_permission, "Failed to delete object, it's still retrievable")
