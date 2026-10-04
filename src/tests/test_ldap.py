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
from src.casdoor.ldap import Ldap
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


def new_sdk():
    return CasdoorSDK(TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class LdapTest(unittest.TestCase):
    def test_ldap(self):
        sdk = new_sdk()
        id = get_random_name("Ldap")

        # an LDAP server belongs to an organization, the synced users are added to it
        ldap = Ldap()
        ldap.id = id
        ldap.createdTime = now()
        ldap.serverName = "Test LDAP Server"
        ldap.host = "localhost"
        ldap.port = 389
        ldap.username = "cn=admin,dc=example,dc=com"
        ldap.password = "password"
        ldap.baseDn = "dc=example,dc=com"
        sdk.add_ldap(ldap)
        self.assertEqual(ldap.owner, TestOrganization)

        self.assertIn(id, [item.id for item in sdk.get_ldaps()])

        ldap = sdk.get_ldap(id)
        self.assertEqual(ldap.id, id)

        ldap.serverName = "Updated LDAP Server"
        sdk.update_ldap(ldap)
        self.assertEqual(sdk.get_ldap(id).serverName, "Updated LDAP Server")

        sdk.delete_ldap(ldap)
        self.assertIsNone(sdk.get_ldap(id))
