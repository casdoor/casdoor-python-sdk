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
from src.casdoor.invitation import Invitation
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_code,
    get_random_name,
)


def new_sdk():
    return CasdoorSDK(TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class InvitationTest(unittest.TestCase):
    def test_invitation(self):
        sdk = new_sdk()
        name = get_random_name("Invitation")
        code = f"TEST{get_random_code(6)}"

        invitation = Invitation()
        invitation.owner = TestOrganization
        invitation.name = name
        invitation.createdTime = now()
        invitation.displayName = "Test Invitation"
        invitation.code = code
        invitation.defaultCode = code
        invitation.quota = 10
        invitation.application = "app-casbin"
        invitation.email = "test@example.com"
        invitation.state = "Active"
        sdk.add_invitation(invitation)

        self.assertIn(name, [item.name for item in sdk.get_invitations()])
        invitations, total = sdk.get_pagination_invitations(1, 100)
        self.assertGreater(total, 0)
        self.assertIn(name, [item.name for item in invitations])

        invitation = sdk.get_invitation(name)
        self.assertEqual(invitation.code, code)

        invitation.state = "Suspended"
        sdk.update_invitation(invitation)
        self.assertEqual(sdk.get_invitation(name).state, "Suspended")

        invitation.state = "Active"
        invitation.displayName = "Updated Invitation"
        sdk.update_invitation_for_columns(invitation, ["state", "display_name"])
        updated = sdk.get_invitation(name)
        self.assertEqual(updated.state, "Active")
        self.assertEqual(updated.displayName, "Updated Invitation")

        info = sdk.get_invitation_info(code, "app-casbin")
        self.assertEqual(info.name, name)

        sdk.delete_invitation(invitation)
        self.assertIsNone(sdk.get_invitation(name))
