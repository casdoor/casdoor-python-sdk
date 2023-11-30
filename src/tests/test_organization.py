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
from src.casdoor.organization import Organization
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class OrganizationTest(unittest.TestCase):
    def test_organization(self):
        name = get_random_name("Organization")

        # Add a new object
        organization = Organization.new(
            owner="admin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            display_name=name,
            website_url="https://example.com",
            password_type="plain",
            password_options=["AtLeast6"],
            country_codes=["US", "ES", "FR", "DE", "GB", "CN", "JP", "KR", "VN", "ID", "SG", "IN"],
            tags=[],
            languages=["en", "zh", "es", "fr", "de", "id", "ja", "ko", "ru", "vi", "pt"],
            init_score=2000,
            enable_soft_deletion=False,
            is_profile_public=False,
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )

        try:
            sdk.add_organization(organization)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            organizations = sdk.get_organizations()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in organizations]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            organization = sdk.get_organization(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(organization.name, name)

        # Update the object
        updated_display_name = "Updated Casdoor Website"
        organization.displayName = updated_display_name
        try:
            sdk.update_organization(organization)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_organization = sdk.get_organization(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(updated_organization.displayName, updated_display_name)

        # Delete the object
        sdk.delete_organization(organization)

        # Validate the deletion
        try:
            deleted_organization = sdk.get_organization(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_organization, "Failed to delete object, it's still retrievable")
