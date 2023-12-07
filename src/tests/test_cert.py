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
from src.casdoor.cert import Cert
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class CertTest(unittest.TestCase):
    def test_cert(self):
        name = get_random_name("Cert")

        # Add a new object
        cert = Cert.new(
            owner="admin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            display_name=name,
            scope="JWT",
            type="x509",
            crypto_algorithm="RS256",
            bit_size=4096,
            expire_in_years=20,
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )

        try:
            sdk.add_cert(cert=cert)
        except Exception as e:
            self.fail("Failed to add object: " + str(e))

        # Get all objects, check if our added object is inside the list
        try:
            certs = sdk.get_certs()
        except Exception as e:
            self.fail("Failed to get objects: " + str(e))
        names = [item.name for item in certs]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            cert = sdk.get_cert(name)
        except Exception as e:
            self.fail("Failed to get object: " + str(e))

        self.assertEqual(cert.name, name, "Retrieved object does not match added object")

        # Update the object
        updated_display_name = "Updated Casdoor Website"
        cert.displayName = updated_display_name
        try:
            sdk.update_cert(cert)
        except Exception as e:
            self.fail("Failed to update object: " + str(e))

        # Validate the update
        try:
            updated_cert = sdk.get_cert(name)
        except Exception as e:
            self.fail("Failed to get updated object: " + str(e))

        self.assertEqual(
            updated_cert.displayName, updated_display_name, "Failed to update object, display_name mismatch"
        )

        # Delete the object
        try:
            sdk.delete_cert(cert)
        except Exception as e:
            self.fail("Failed to delete object: " + str(e))

        # Validate the deletion
        try:
            deleted_cert = sdk.get_cert(name)
        except Exception as e:
            self.fail("Failed to delete object: " + str(e))

        self.assertIsNone(deleted_cert, "Failed to delete object, it's still retrievable")
