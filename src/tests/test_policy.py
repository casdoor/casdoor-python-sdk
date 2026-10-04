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
from src.casdoor.adapter import Adapter
from src.casdoor.enforcer import Enforcer
from src.casdoor.model import Model
from src.casdoor.policy import Policy
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


class PolicyTest(unittest.TestCase):
    def test_policy(self):
        sdk = new_sdk()
        name = get_random_name("Policy")

        model = Model.new(TestOrganization, name, now(), name, "")
        model.modelText = (
            "[request_definition]\nr = sub, obj, act\n\n[policy_definition]\np = sub, obj, act\n\n"
            "[policy_effect]\ne = some(where (p.eft == allow))\n\n"
            "[matchers]\nm = r.sub == p.sub && r.obj == p.obj && r.act == p.act"
        )
        sdk.add_model(model)

        adapter = Adapter.new(TestOrganization, name, now(), "", "")
        adapter.table = f"casbin_rule_{get_random_code(6)}"
        adapter.useSameDb = True
        sdk.add_adapter(adapter)

        enforcer = Enforcer.new(
            TestOrganization, name, now(), name, "", f"{TestOrganization}/{name}", f"{TestOrganization}/{name}"
        )
        sdk.add_enforcer(enforcer)

        policy = Policy.new("p", "alice", "data1", "read")
        sdk.add_policy(enforcer, policy)

        policies = sdk.get_policies(name)
        self.assertIn(("alice", "data1", "read"), [(p.v0, p.v1, p.v2) for p in policies])

        filtered = sdk.get_filtered_policies(
            f"{TestOrganization}/{name}", [{"ptype": "p", "fieldIndex": 0, "fieldValues": ["alice"]}]
        )
        self.assertEqual(len(filtered), 1)

        new_policy = Policy.new("p", "alice", "data1", "write")
        sdk.update_policy(enforcer, policy, new_policy)
        self.assertIn("write", [p.v2 for p in sdk.get_policies(name)])

        sdk.remove_policy(enforcer, new_policy)
        self.assertNotIn("write", [p.v2 for p in sdk.get_policies(name)])

        sdk.delete_enforcer(enforcer)
        sdk.delete_adapter(adapter)
        sdk.delete_model(model)
