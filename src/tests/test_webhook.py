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
from src.casdoor.webhook import Webhook
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class WebhookTest(unittest.TestCase):
    def test_webhook(self):
        name = get_random_name("Webhook")

        # Add a new object
        webhook = Webhook.new(
            owner="casbin", name=name, created_time=datetime.datetime.now().isoformat(), organization="casbin"
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        try:
            sdk.add_webhook(webhook=webhook)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            webhooks = sdk.get_webhooks()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in webhooks]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            webhook = sdk.get_webhook(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(webhook.name, name)

        # Update the object
        updated_organization = "Updated Casdoor Website"
        webhook.organization = updated_organization
        try:
            sdk.update_webhook(webhook)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_webhook = sdk.get_webhook(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_webhook.organization, updated_organization)

        # Delete the object
        try:
            sdk.delete_webhook(webhook)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_webhook = sdk.get_webhook(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_webhook, "Failed to delete object, it's still retrievable")
