# Copyright 2026 The Casdoor Authors. All Rights Reserved.
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
from src.casdoor.record import Record
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class RecordTest(unittest.TestCase):
    def test_record(self):
        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        name = get_random_name("Record")

        # Add a new object
        record = Record()
        record.owner = TestOrganization
        record.name = name
        record.createdTime = datetime.datetime.now(datetime.timezone.utc).isoformat()
        record.organization = TestOrganization
        record.user = "admin"
        record.action = "test-record"
        sdk.add_record(record)

        # Reading the records needs the access token of an admin user
        token = sdk.get_oauth_token(username="admin", password="123")
        admin_sdk = sdk.with_access_token(token["access_token"])

        # Get all objects, check if our added object is inside the list
        self.assertIn(name, [item.name for item in admin_sdk.get_records()])

        # Get the object
        self.assertEqual(admin_sdk.get_record(name).name, name)

        # Get an object that doesn't exist
        self.assertIsNone(admin_sdk.get_record(name + "_missing"))
