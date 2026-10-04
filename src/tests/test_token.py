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
from src.casdoor.token import Token
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


class TokenTest(unittest.TestCase):
    def test_token(self):
        sdk = new_sdk()
        name = get_random_name("Token")

        token = Token()
        token.owner = "admin"
        token.name = name
        token.createdTime = now()
        token.application = "app-casbin"
        token.organization = TestOrganization
        token.user = "admin"
        token.code = "abc"
        token.accessToken = "123456"
        token.expiresIn = 3600
        token.scope = "read"
        token.tokenType = "Bearer"
        sdk.add_token(token)

        self.assertIn(name, [item.name for item in sdk.get_tokens()])
        _, total = sdk.get_pagination_tokens(1, 10)
        self.assertGreater(total, 0)

        token = sdk.get_token(name)
        self.assertEqual(token.name, name)

        token.code = "Updated Code"
        sdk.update_token(token)

        token.scope = "profile"
        sdk.update_token_for_columns(token, ["scope"])

        updated = sdk.get_token(name)
        self.assertEqual(updated.code, "Updated Code")
        self.assertEqual(updated.scope, "profile")

        sdk.delete_token(token)
        with self.assertRaisesRegex(Exception, "does not exist"):
            sdk.get_token(name)
