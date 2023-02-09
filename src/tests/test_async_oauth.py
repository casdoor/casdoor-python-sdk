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

from unittest import IsolatedAsyncioTestCase

from src.casdoor.async_main import AsyncCasdoorSDK, User


class TestOAuth(IsolatedAsyncioTestCase):
    """
    You should replace the code content below and
    the get_sdk() method's content with your own Casdoor
    instance and such if you need to. And running these tests successfully
    proves that your connection to Casdoor is good-and-working!
    """

    # server returned authorization code
    code = "6d038ac60d4e1f17e742"

    # Casdoor user and password for auth with
    # Resource Owner Password Credentials Grant.
    # Grant type "Password" must be enabled in Casdoor Application.
    username = ""
    password = ""

    @staticmethod
    def get_sdk():

        sdk = AsyncCasdoorSDK(
            endpoint="http://test.casbin.com:8000",
            client_id="3267f876b11e7d1cb217",
            client_secret="3f0d1f06d28d65309c8f38b505cb9dcfa487754d",
            certificate="CasdoorSecret",
            org_name="built-in",
            application_name="app-built-in"
        )
        return sdk

    async def test__oauth_token_request(self):
        sdk = self.get_sdk()
        data = {
            "grant_type": sdk.grant_type,
            "client_id": sdk.client_id,
            "client_secret": sdk.client_secret,
            "code": self.code,
        }
        response = await sdk._oauth_token_request(payload=data)
        self.assertIsInstance(response, dict)

    async def test__get_payload_for_authorization_code(self):
        sdk = self.get_sdk()
        result = sdk._AsyncCasdoorSDK__get_payload_for_authorization_code(  # noqa: It's private method
            code=self.code
        )
        self.assertEqual("authorization_code", result.get("grant_type"))

    async def test__get_payload_for_password_credentials(self):
        sdk = self.get_sdk()
        result = sdk._AsyncCasdoorSDK__get_payload_for_password_credentials(  # noqa: It's private method
            username="test",
            password="test"
        )
        self.assertEqual("password", result.get("grant_type"))

    async def test__get_payload_for_client_credentials(self):
        sdk = self.get_sdk()
        result = sdk._AsyncCasdoorSDK__get_payload_for_client_credentials()  # noqa: It's private method
        self.assertEqual("client_credentials", result.get("grant_type"))

    async def test__get_payload_for_access_token_request_with_code(self):
        sdk = self.get_sdk()
        result = sdk._get_payload_for_access_token_request(code="test")
        self.assertEqual("authorization_code", result.get("grant_type"))

    async def test__get_payload_for_access_token_request_with_cred(self):
        sdk = self.get_sdk()
        result = sdk._get_payload_for_access_token_request(
            username="test",
            password="test"
        )
        self.assertEqual("password", result.get("grant_type"))

    async def test_get_payload_for_access_token_request_with_client_cred(self):
        sdk = self.get_sdk()
        result = sdk._get_payload_for_access_token_request()
        self.assertEqual("client_credentials", result.get("grant_type"))

    async def test_get_oauth_token_with_password(self):
        sdk = self.get_sdk()
        access_token = await sdk.get_oauth_token(
            username=self.username,
            password=self.password
        )
        self.assertIsInstance(access_token, str)

    async def test_get_oauth_token_with_client_cred(self):
        sdk = self.get_sdk()
        access_token = await sdk.get_oauth_token()
        self.assertIsInstance(access_token, str)

    async def test_get_oauth_token(self):
        sdk = self.get_sdk()
        access_token = await sdk.get_oauth_token(code=self.code)
        self.assertIsInstance(access_token, str)

    async def test_oauth_token_request(self):
        sdk = self.get_sdk()
        response = await sdk.oauth_token_request(self.code)
        self.assertIsInstance(response, dict)

    async def test_refresh_token_request(self):
        sdk = self.get_sdk()
        response = await sdk.oauth_token_request(self.code)
        refresh_token = response.get("refresh_token")
        response = await sdk.refresh_token_request(refresh_token)
        self.assertIsInstance(response, dict)

    async def test_get_oauth_refreshed_token(self):
        sdk = self.get_sdk()
        response = await sdk.oauth_token_request(self.code)
        refresh_token = response.get("refresh_token")
        response = await sdk.refresh_oauth_token(refresh_token)
        self.assertIsInstance(response, str)

    async def test_parse_jwt_token(self):
        sdk = self.get_sdk()
        access_token = await sdk.get_oauth_token(code=self.code)
        decoded_msg = sdk.parse_jwt_token(access_token)
        self.assertIsInstance(decoded_msg, dict)

    async def test_enforce(self):
        sdk = self.get_sdk()
        status = await sdk.enforce(
            "built-in/permission-built-in", "admin", "a", "ac"
        )
        self.assertIsInstance(status, bool)

    async def test_get_users(self):
        sdk = self.get_sdk()
        users = await sdk.get_users()
        self.assertIsInstance(users, list)

    async def test_get_user(self):
        sdk = self.get_sdk()
        user = await sdk.get_user("admin")
        self.assertIsInstance(user, dict)

    async def test_modify_user(self):
        sdk = self.get_sdk()
        user = User()
        user.name = "test_ffyuanda"
        await sdk.delete_user(user)

        response = await sdk.add_user(user)
        self.assertEqual(response["data"], "Affected")

        response = await sdk.delete_user(user)
        self.assertEqual(response["data"], "Affected")

        response = await sdk.add_user(user)
        self.assertEqual(response["data"], "Affected")

        user.phone = "phone"
        response = await sdk.update_user(user)
        self.assertEqual(response["data"], "Affected")

        self.assertIn("status", response)
        self.assertIsInstance(response, dict)
