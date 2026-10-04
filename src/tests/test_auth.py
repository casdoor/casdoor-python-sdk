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
from src.casdoor.user import User
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


# the CI user "admin" of the CI application's organization (built-in) has the password "123"
TestUsername = "admin"
TestPassword = "123"


class AuthTest(unittest.TestCase):
    def test_oauth_token_by_password(self):
        sdk = new_sdk()
        token = sdk.get_oauth_token_by_password(TestUsername, TestPassword)
        self.assertTrue(token["access_token"])
        self.assertTrue(token["refresh_token"])

        with self.assertRaisesRegex(Exception, "password"):
            sdk.get_oauth_token_by_password(TestUsername, "wrong-password")

        introspection = sdk.introspect_token(token["access_token"], "access_token")
        self.assertTrue(introspection["active"])

        # the token is signed by the cert of the CI application
        sdk.certificate = sdk.get_cert("admin/cert-built-in").certificate
        claims = sdk.parse_jwt_token(token["access_token"])
        self.assertEqual(claims["name"], TestUsername)

        # refreshing the token revokes the old access token
        refreshed = sdk.refresh_oauth_tokens(token["refresh_token"])
        self.assertTrue(refreshed["access_token"])

    def test_with_access_token(self):
        sdk = new_sdk()
        token = sdk.get_oauth_token_by_password(TestUsername, TestPassword)

        user_sdk = sdk.with_access_token(token["access_token"])
        account = user_sdk.get_account()
        self.assertEqual(account.name, TestUsername)

        # the original SDK still calls the APIs as the application
        self.assertEqual(sdk.access_token, "")
        with self.assertRaisesRegex(Exception, "."):
            sdk.get_account()

        self.assertEqual(sdk.logout_current_session(token["access_token"])["status"], "ok")

        another = sdk.get_oauth_token_by_password(TestUsername, TestPassword)
        self.assertEqual(sdk.logout(another["access_token"])["status"], "ok")

        with self.assertRaises(ValueError):
            sdk.logout("")

    def test_urls(self):
        sdk = new_sdk()
        self.assertEqual(
            sdk.get_signin_url("http://localhost:9000/callback"),
            f"{TestEndpoint}/login/oauth/authorize?client_id={TestClientId}&response_type=code"
            f"&redirect_uri=http%3A%2F%2Flocalhost%3A9000%2Fcallback&scope=read&state={TestApplication}",
        )
        self.assertEqual(sdk.get_signup_url(True), f"{TestEndpoint}/signup/{TestApplication}")
        self.assertIn("/signup/oauth/authorize?", sdk.get_signup_url(False, "http://localhost:9000/callback"))
        self.assertEqual(sdk.get_user_profile_url("alice"), f"{TestEndpoint}/users/{TestOrganization}/alice")
        self.assertEqual(sdk.get_my_profile_url("token"), f"{TestEndpoint}/account?access_token=token")

    def test_user_extra(self):
        sdk = new_sdk()
        name = get_random_name("User")
        user = User.new(TestOrganization, name, now(), name, f"{name}@example.com", f"202555{get_random_code(4)}")
        user.countryCode = "US"
        user.password = "123456"
        sdk.add_user(user)

        by_email = sdk.get_user_by_email(user.email)
        self.assertEqual(by_email.name, name)
        self.assertEqual(sdk.get_user_by_phone(user.phone).name, name)
        self.assertEqual(sdk.get_user_by_user_id(by_email.id).name, name)

        users, total = sdk.get_pagination_users(1, 100)
        self.assertGreater(total, 0)
        self.assertGreater(len(users), 0)
        self.assertEqual(len(sdk.get_sorted_users("created_time", 1)), 1)
        self.assertIn(name, [item.name for item in sdk.get_global_users()])

        by_email.displayName = "Updated by columns"
        by_email.bio = "should not be updated"
        sdk.update_user_for_columns(by_email, ["displayName"])
        updated = sdk.get_user(name)
        self.assertEqual(updated.displayName, "Updated by columns")
        self.assertFalse(updated.bio)

        updated.displayName = "Updated by user id"
        sdk.update_user_by_user_id(TestOrganization, updated.id, updated)
        self.assertEqual(sdk.get_user(name).displayName, "Updated by user id")

        updated.password = "123456"
        self.assertTrue(sdk.check_user_password(updated))
        updated.password = "wrong-password"
        self.assertFalse(sdk.check_user_password(updated))

        self.assertTrue(sdk.set_password(TestOrganization, name, "123456", "654321"))
        updated.password = "654321"
        self.assertTrue(sdk.check_user_password(updated))

        sdk.delete_user(updated)
        self.assertIsNone(sdk.get_user(name))

    def test_owner(self):
        sdk = new_sdk()
        self.assertEqual(sdk.get_id("role"), f"{TestOrganization}/role")
        self.assertEqual(sdk.get_id("other/role"), "other/role")

        self.assertGreater(len(sdk.get_organization_names()), 0)
        self.assertIn("app-casbin", [item.name for item in sdk.get_organization_applications()])
        self.assertGreater(len(sdk.get_global_certs()), 0)

        # an "owner/name" ID addresses an object of another organization
        application = sdk.get_application(f"admin/{TestApplication}")
        self.assertEqual(application.organization, "built-in")
