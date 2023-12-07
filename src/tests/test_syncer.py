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
from src.casdoor.syncer import Syncer
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class SyncerTest(unittest.TestCase):
    def test_syncer(self):
        name = get_random_name("Syncer")

        # Add a new object
        syncer = Syncer.new(
            owner="admin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            organization="casbin",
            host="localhost",
            port=3306,
            user="root",
            password="123",
            database_type="mysql",
            database="syncer_db",
            table="user-table",
            sync_interval=1,
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        try:
            sdk.add_syncer(syncer=syncer)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            syncers = sdk.get_syncers()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in syncers]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            syncer = sdk.get_syncer(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(syncer.name, name)

        # Update the object
        updated_password = "123456"
        syncer.password = updated_password
        try:
            sdk.update_syncer(syncer)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_syncer = sdk.get_syncer(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_syncer.password, updated_password)

        # Delete the object
        try:
            sdk.delete_syncer(syncer)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_syncer = sdk.get_syncer(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_syncer, "Failed to delete object, it's still retrievable")
