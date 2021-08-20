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

from oauth.main import CasdoorSDK
from unittest import TestCase


class TestOAuth(TestCase):
    """
    You should replace the get_sdk() method's content with your own Casdoor
    instance and such if you need to. And running these tests successfully
    proves that your connection to Casdoor is good-and-working!
    """

    @staticmethod
    def get_sdk():

        sdk = CasdoorSDK(
            endpoint="https://door.casbin.com",
            client_id="0ba528121ea87b3eb54d",
            client_secret="04f4ca22101529a3503d5a653a877b4e8403edf0",
            jwt_secret="CasdoorSecret",
            org_name="built-in",
        )
        return sdk

    def test_get_oauth_token(self):
        sdk = self.get_sdk()
        access_token = sdk.get_oauth_token("91a7e3c2e9aa2baef46a")
        self.assertIsInstance(access_token, str)

    def test_parse_jwt_token(self):
        sdk = self.get_sdk()
        access_token = sdk.get_oauth_token("91a7e3c2e9aa2baef46a")
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
