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

import unittest
import datetime

from src.casdoor import CasdoorSDK
from src.casdoor.application import Application
from src.tests.test_util import *


class TestApplication(unittest.TestCase):
    def setUp(self):
        CasdoorSDK(TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication)

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
            organization="casbin"
        )

        result, err = CasdoorSDK.add_application(application)
        self.assertIsNone(err, f"Failed to add object: {err}")

        # Get all objects, check if our added object is inside the list
        applications, err = CasdoorSDK.get_applications()
        self.assertIsNone(err, f"Failed to get objects: {err}")
        names = [item.name for item in applications]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        retrieved_application, err = CasdoorSDK.get_application(name)
        self.assertIsNone(err, f"Failed to get object: {err}")
        self.assertEqual(retrieved_application.name, name)

        # Update the object
        updated_description = "Updated Casdoor Website"
        application.description = updated_description
        result, err = CasdoorSDK.update_application(application)
        self.assertIsNone(err, f"Failed to update object: {err}")

        # Validate the update
        updated_application, err = CasdoorSDK.get_application(name)
        self.assertIsNone(err, f"Failed to get updated object: {err}")
        self.assertEqual(updated_application.description, updated_description)

        # Delete the object
        result, err = CasdoorSDK.delete_application(application)
        self.assertIsNone(err, f"Failed to delete object: {err}")

        # Validate the deletion
        deleted_application, err = CasdoorSDK.get_application(name)
        self.assertIsNone(err)
        self.assertIsNone(deleted_application, "Failed to delete object, it's still retrievable")
