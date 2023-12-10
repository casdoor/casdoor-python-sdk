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
from src.casdoor.session import Session
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


class sessionTest(unittest.TestCase):
    def test_session(self):
        name = get_random_name("Session")

        # Add a new object
        session = Session.new(
            owner="casbin",
            name=name,
            application="app-built-in",
            created_time=datetime.datetime.now().isoformat(),
            session_id=[],
        )

        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        try:
            sdk.add_session(session=session)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            sessions = sdk.get_sessions()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in sessions]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            session = sdk.get_session(name, session.application)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(session.name, name)

        # Update the object
        updated_time = "Updated Casdoor Website"
        session.createdTime = updated_time
        try:
            sdk.update_session(session)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_session = sdk.get_session(name, session.application)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_session.createdTime, updated_time)

        # Delete the object
        try:
            sdk.delete_session(session)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_session = sdk.get_session(name, session.application)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_session, "Failed to delete object, it's still retrievable")
