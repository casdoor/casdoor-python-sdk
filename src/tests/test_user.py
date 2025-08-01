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

import src.tests.test_util as test_util
from src.casdoor import CasdoorSDK
from src.casdoor.user import User


class UserTest(unittest.TestCase):
    @staticmethod
    def get_sdk():
        sdk = CasdoorSDK(
            endpoint=test_util.TestEndpoint,
            client_id=test_util.TestClientId,
            client_secret=test_util.TestClientSecret,
            certificate=test_util.TestJwtPublicKey,
            org_name=test_util.TestOrganization,
            application_name=test_util.TestApplication,
        )
        return sdk

    def test_user(self):
        name = test_util.get_random_name("User")
        email = f"{name}@gmail.com"
        phone = test_util.get_random_code(11)

        # Add a new object
        user = User.new(
            owner="admin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            display_name=name,
            email=email,
            phone=phone,
        )

        sdk = UserTest.get_sdk()
        try:
            sdk.add_user(user=user)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            users = sdk.get_users()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in users]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            user = sdk.get_user(name)
            user_id = user.id
            user_by_email = sdk.get_user_by_email(email)
            user_by_phone = sdk.get_user_by_phone(phone)
            user_by_user_id = sdk.get_user_by_user_id(user_id)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(user.name, name)
        self.assertEqual(user_by_email.name, name)
        self.assertEqual(user_by_phone.name, name)
        self.assertEqual(user_by_user_id.name, name)

        # Update the object
        updated_display_name = "Updated Casdoor Website"
        user.displayName = updated_display_name
        try:
            sdk.update_user(user)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_user = sdk.get_user(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_user.displayName, updated_display_name)

        # Delete the object
        try:
            sdk.delete_user(user)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_user = sdk.get_user(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_user, "Failed to delete object, it's still retrievable")

    def test_get_global_users(self):
        sdk = UserTest.get_sdk()
        try:
            users = sdk.get_global_users()
        except Exception as e:
            self.fail(f"Fail to get object:{e}")

        self.assertIsInstance(users, list, "The returned result is not a list")
        for user in users:
            self.assertIsInstance(user, User, "There are non User type objects in the list")

    def test_get_sort_users(self):
        sdk = UserTest.get_sdk()
        try:
            users = sdk.get_sorted_users("created_time", 25)
        except Exception as e:
            self.fail(f"Fail to get object:{e}")
        self.assertIsInstance(users, list, "The returned result is not a list")
        for user in users:
            self.assertIsInstance(user, User, "There are non User type objects in the list")
