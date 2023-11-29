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
from src.casdoor.application import Application
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrg,
    get_random_name,
)


class ApplicationTest(unittest.TestCase):
    def test_application(self):
        name = get_random_name("application")

        # Add a new object
        application = Application.new(
            owner="admin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            display_name=name,
            logo="https://cdn.casbin.org/img/casdoor-logo_1185x256.png",
            homepage_url="https://casdoor.org",
            description="Casdoor Website",
            organization="casbin",
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrg, TestApplication
        )
        try:
            sdk.add_application(application=application)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            applications = sdk.get_applications()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in applications]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            application = sdk.get_application(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(application.name, name)

        # Update the object
        updated_description = "Updated Casdoor Website"
        application.description = updated_description
        try:
            sdk.update_application(application)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_application = sdk.get_application(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_application.description, updated_description)

        # Delete the object
        try:
            sdk.delete_application(application)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_application = sdk.get_application(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_application, "Failed to delete object, it's still retrievable")

if __name__ == "__main__":
    unittest.main()
