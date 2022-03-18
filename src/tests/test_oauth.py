# Copyright 2021 The Casbin Authors. All Rights Reserved.
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

from src.casdoor.main import CasdoorSDK, User
from unittest import TestCase


class TestOAuth(TestCase):
    """
    You should replace the code content below and
    the get_sdk() method's content with your own Casdoor
    instance and such if you need to. And running these tests successfully
    proves that your connection to Casdoor is good-and-working!
    """

    # server returned authorization code
    code = "6d038ac60d4e1f17e742"

    @staticmethod
    def get_sdk():

        sdk = CasdoorSDK(
            endpoint="http://test.casbin.com:8000",
            client_id="3267f876b11e7d1cb217",
            client_secret="3f0d1f06d28d65309c8f38b505cb9dcfa487754d",
            jwt_secret="CasdoorSecret",
            org_name="built-in",
        )
        return sdk

    def test_get_oauth_token(self):
        sdk = self.get_sdk()
        access_token = sdk.get_oauth_token(self.code)
        self.assertIsInstance(access_token, str)

    def test_parse_jwt_token(self):
        sdk = self.get_sdk()
        access_token = sdk.get_oauth_token(self.code)
        decoded_msg = sdk.parse_jwt_token(access_token)
        self.assertIsInstance(decoded_msg, dict)

    def test_get_users(self):
        sdk = self.get_sdk()
        users = sdk.get_users()
        self.assertIsInstance(users, list)

    def test_get_user(self):
        sdk = self.get_sdk()
        user = sdk.get_user("admin")
        self.assertIsInstance(user, dict)

    def test_modify_user(self):
        sdk = self.get_sdk()
        user = User()
        user.name = "test_ffyuanda"
        sdk.delete_user(user)

        response = sdk.add_user(user)
        self.assertEqual(response["data"], "Affected")

        response = sdk.delete_user(user)
        self.assertEqual(response["data"], "Affected")

        response = sdk.add_user(user)
        self.assertEqual(response["data"], "Affected")

        user.phone = "phone"
        response = sdk.update_user(user)
        self.assertEqual(response["data"], "Affected")

        self.assertIn("status", response)
        self.assertIsInstance(response, dict)
