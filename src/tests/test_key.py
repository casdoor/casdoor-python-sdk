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
from src.casdoor.key import Key
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


def new_key(owner, name):
    key = Key()
    key.owner = owner
    key.name = name
    key.createdTime = datetime.datetime.now(datetime.timezone.utc).isoformat()
    key.displayName = "Test Key"
    key.type = "Organization"
    key.organization = owner
    key.state = "Active"
    return key


def find(keys, name):
    return next((key for key in keys if key.name == name), None)


class KeyTest(unittest.TestCase):
    def test_key(self):
        sdk = new_sdk()
        name = get_random_name("Key")

        key = new_key(TestOrganization, name)
        key.accessKey = get_random_name("ak")
        key.accessSecret = "test-secret-value"
        self.assertEqual(sdk.add_key(key)["data"], "Affected")
        self.addCleanup(sdk.delete_key, new_key(TestOrganization, name))

        # Casdoor generates the credentials and ignores the given ones
        got = sdk.get_key(name)
        self.assertEqual(got.type, "Organization")
        self.assertEqual(got.displayName, "Test Key")
        self.assertNotIn(got.accessKey, ["", key.accessKey])
        self.assertNotIn(got.accessSecret, ["", key.accessSecret])
        access_key, access_secret = got.accessKey, got.accessSecret

        # get_keys() masks the access secrets
        keys = sdk.get_keys()
        self.assertEqual(find(keys, name).accessSecret, "***")

        # get_global_keys() includes the keys of the other organizations
        other_name = get_random_name("Key")
        sdk.add_key(new_key("built-in", other_name))
        self.addCleanup(sdk.delete_key, new_key("built-in", other_name))
        global_keys = sdk.get_global_keys()
        self.assertIsNotNone(find(global_keys, name))
        self.assertIsNotNone(find(global_keys, other_name))
        self.assertIsNone(find(keys, other_name))

        page_keys, total = sdk.get_pagination_keys(1, 100, {"field": "name", "value": name})
        self.assertEqual(total, 1)
        self.assertEqual([item.name for item in page_keys], [name])

        # The access key and the access secret can't be changed
        got.displayName = "Test Key Updated"
        got.state = "Suspended"
        got.accessKey, got.accessSecret = "changed", "changed"
        sdk.update_key(got)
        got = sdk.get_key(name)
        self.assertEqual(got.displayName, "Test Key Updated")
        self.assertEqual(got.state, "Suspended")
        self.assertEqual((got.accessKey, got.accessSecret), (access_key, access_secret))

        self.assertEqual(sdk.delete_key(got)["data"], "Affected")
        self.assertIsNone(sdk.get_key(name))
