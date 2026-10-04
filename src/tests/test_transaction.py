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
from src.casdoor.transaction import Transaction
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
)


def new_sdk():
    return CasdoorSDK(TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class TransactionTest(unittest.TestCase):
    def test_transaction(self):
        sdk = new_sdk()

        # a recharge of the organization doesn't need a user balance, so it can be added in CI
        transaction = Transaction()
        transaction.owner = TestOrganization
        transaction.createdTime = now()
        transaction.application = "app-casbin"
        transaction.domain = "https://casdoor.ai"
        transaction.category = "Recharge"
        transaction.type = "Recharge"
        transaction.tag = "Organization"
        transaction.amount = 100
        transaction.currency = "USD"
        transaction.state = "Paid"

        response = sdk.add_transaction_with_dry_run(transaction, True)
        self.assertEqual(response["status"], "ok")

        name = sdk.add_transaction(transaction)["data"]
        self.assertTrue(name)

        self.assertIn(name, [item.name for item in sdk.get_transactions()])
        _, total = sdk.get_pagination_transactions(1, 10)
        self.assertGreater(total, 0)

        transaction = sdk.get_transaction(name)
        self.assertEqual(transaction.name, name)

        transaction.displayName = "Updated Transaction"
        sdk.update_transaction(transaction)
        self.assertEqual(sdk.get_transaction(name).displayName, "Updated Transaction")

        sdk.delete_transaction(transaction)
        self.assertIsNone(sdk.get_transaction(name))
