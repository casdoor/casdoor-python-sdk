# Copyright 2021 The Casdoor Authors. All Rights Reserved.
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

from unittest import IsolatedAsyncioTestCase, mock

import src.tests.test_util as test_util
from src.casdoor.async_main import AsyncCasdoorSDK
from src.casdoor.user import User


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
            endpoint=test_util.TestEndpoint,
            client_id=test_util.TestClientId,
            client_secret=test_util.TestClientSecret,
            certificate=test_util.TestJwtPublicKey,
            org_name=test_util.TestOrganization,
            application_name=test_util.TestApplication,
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
        auth_token = await sdk._oauth_token_request(payload=data)
        self.assertIn("access_token", auth_token)

    async def test__get_payload_for_authorization_code(self):
        sdk = self.get_sdk()
        result = sdk._AsyncCasdoorSDK__get_payload_for_authorization_code(code=self.code)
        self.assertEqual("authorization_code", result.get("grant_type"))

    async def test__get_payload_for_password_credentials(self):
        sdk = self.get_sdk()
        result = sdk._AsyncCasdoorSDK__get_payload_for_password_credentials(username="test", password="test")
        self.assertEqual("password", result.get("grant_type"))

    async def test__get_payload_for_client_credentials(self):
        sdk = self.get_sdk()
        result = sdk._AsyncCasdoorSDK__get_payload_for_client_credentials()
        self.assertEqual("client_credentials", result.get("grant_type"))

    async def test__get_payload_for_access_token_request_with_code(self):
        sdk = self.get_sdk()
        result = sdk._get_payload_for_access_token_request(code="test")
        self.assertEqual("authorization_code", result.get("grant_type"))

    async def test__get_payload_for_access_token_request_with_cred(self):
        sdk = self.get_sdk()
        result = sdk._get_payload_for_access_token_request(username="test", password="test")
        self.assertEqual("password", result.get("grant_type"))

    async def test_get_payload_for_access_token_request_with_client_cred(self):
        sdk = self.get_sdk()
        result = sdk._get_payload_for_access_token_request()
        self.assertEqual("client_credentials", result.get("grant_type"))

    async def test_get_oauth_token_with_password(self):
        sdk = self.get_sdk()
        token = await sdk.get_oauth_token(username=self.username, password=self.password)
        access_token = token.get("access_token")
        self.assertIsInstance(access_token, str)

    async def test_get_oauth_token_with_client_cred(self):
        sdk = self.get_sdk()
        token = await sdk.get_oauth_token()
        access_token = token.get("access_token")
        self.assertIsInstance(access_token, str)

    async def test_get_oauth_token(self):
        sdk = self.get_sdk()
        token = await sdk.get_oauth_token(code=self.code)
        access_token = token.get("access_token")
        self.assertIsInstance(access_token, str)

    async def test_oauth_token_request(self):
        sdk = self.get_sdk()
        response = await sdk.oauth_token_request(self.code)
        self.assertIsInstance(response, dict)

    async def test_refresh_token_request(self):
        sdk = self.get_sdk()
        response = await sdk.oauth_token_request(self.code)
        refresh_token = response.get("refresh_token")
        self.assertIsInstance(refresh_token, str)
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
        token = await sdk.get_oauth_token(code=self.code)
        access_token = token.get("access_token")
        decoded_msg = sdk.parse_jwt_token(access_token)
        self.assertIsInstance(decoded_msg, dict)

    async def test_enforce(self):
        sdk = self.get_sdk()
        status = await sdk.enforce("built-in/permission-built-in", "admin", "a", "ac")
        self.assertIsInstance(status, bool)

    def mocked_enforce_requests_post(*args, **kwargs):
        class MockResponse:
            def __init__(
                self,
                json_data,
                status_code=200,
            ):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        result = True
        for i in range(0, 5):
            if kwargs.get("json").get(f"v{i}") != f"v{i}":
                result = False

        return MockResponse(result)

    @mock.patch("aiohttp.ClientSession.post", side_effect=mocked_enforce_requests_post)
    async def test_enforce_parmas(self, mock_post):
        sdk = self.get_sdk()
        status = await sdk.enforce(
            "built-in/permission-built-in",
            "v0",
            "v1",
            "v2",
            v3="v3",
            v4="v4",
            v5="v5",
        )
        self.assertEqual(status, True)

    def mocked_batch_enforce_requests_post(*args, **kwargs):
        class MockResponse:
            def __init__(
                self,
                json_data,
                status_code=200,
            ):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        json = kwargs.get("json")
        result = [True for i in range(0, len(json))]
        for k in range(0, len(json)):
            for i in range(0, len(json[k]) - 1):
                if json[k].get(f"v{i}") != f"v{i}":
                    result[k] = False

        return MockResponse(result)

    @mock.patch(
        "aiohttp.ClientSession.post",
        side_effect=mocked_batch_enforce_requests_post,
    )
    def test_batch_enforce(self, mock_post):
        sdk = self.get_sdk()
        status = sdk.batch_enforce(
            "built-in/permission-built-in",
            [
                ["v0", "v1", "v2", "v3", "v4", "v5"],
                ["v0", "v1", "v2", "v3", "v4", "v1"],
            ],
        )
        self.assertEqual(len(status), 2)
        self.assertEqual(status[0], True)
        self.assertEqual(status[1], False)

    @mock.patch(
        "aiohttp.ClientSession.post",
        side_effect=mocked_batch_enforce_requests_post,
    )
    def test_batch_enforce_raise(self, mock_post):
        sdk = self.get_sdk()
        with self.assertRaises(ValueError) as context:
            sdk.batch_enforce("built-in/permission-built-in", [["v0", "v1"]])
        self.assertEqual("Invalid permission rule[0]: ['v0', 'v1']", str(context.exception))

    async def test_get_users(self):
        sdk = self.get_sdk()
        users = await sdk.get_users()
        self.assertIsInstance(users, list)

    async def test_get_user(self):
        sdk = self.get_sdk()
        user = await sdk.get_user("admin")
        self.assertIsInstance(user, dict)
        self.assertEqual(user["name"], "admin")

    async def test_get_user_count(self):
        sdk = self.get_sdk()
        online_count = await sdk.get_user_count(is_online=True)
        offline_count = await sdk.get_user_count(is_online=False)
        all_count = await sdk.get_user_count()
        self.assertIsInstance(online_count, int)
        self.assertIsInstance(offline_count, int)
        self.assertIsInstance(all_count, int)
        self.assertEqual(online_count + offline_count, all_count)

    async def test_modify_user(self):
        sdk = self.get_sdk()
        user = User()
        user.name = "test_ffyuanda"
        user.owner = sdk.org_name
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

    def check_enforce_request(*args, **kwargs):
        return True

    async def test_auth_link(self):
        sdk = self.get_sdk()
        redirect_uri = "http://localhost:9000/callback"
        response = await sdk.get_auth_link(redirect_uri=redirect_uri)
        self.assertEqual(
            response,
            f"{sdk.front_endpoint}/login/oauth/authorize?client_id={sdk.client_id}&response_type=code&redirect_uri={redirect_uri}&scope=read&state={sdk.application_name}",
        )
