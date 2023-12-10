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
from src.casdoor.model import Model
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class ModelTest(unittest.TestCase):
    def test_model(self):
        name = get_random_name("model")

        # Add a new object
        model = Model.new(
            owner="casbin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            display_name=name,
            model_text="[request_definition]\n"
            + "r = sub, obj, act\n"
            + "\n"
            + "[policy_definition]\n"
            + "p = sub, obj, act\n"
            + "\n"
            + "[role_definition]\n"
            + "g = _, _\n"
            + "\n"
            + "[policy_effect]\n"
            + "e = some(where (p.eft == allow))\n"
            + "\n"
            + "[matchers]\n"
            + "m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act",
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        try:
            sdk.add_model(model=model)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            models = sdk.get_models()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in models]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            model = sdk.get_model(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(model.name, name)

        # Update the object
        updated_display_name = "Updated Casdoor Website"
        model.displayName = updated_display_name
        try:
            sdk.update_model(model)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_model = sdk.get_model(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_model.displayName, updated_display_name)

        # Delete the object
        try:
            sdk.delete_model(model)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_model = sdk.get_model(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_model, "Failed to delete object, it's still retrievable")
