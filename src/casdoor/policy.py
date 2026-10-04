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

from typing import Dict, List

from .util import get_id, get_owner


class Policy:
    def __init__(self):
        self.id = 0
        self.ptype = ""
        self.v0 = ""
        self.v1 = ""
        self.v2 = ""
        self.v3 = ""
        self.v4 = ""
        self.v5 = ""

    @classmethod
    def new(cls, ptype: str, *values: str):
        self = cls()
        self.ptype = ptype
        for i, value in enumerate(values):
            setattr(self, f"v{i}", value)
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        policy = cls()
        for key, value in data.items():
            setattr(policy, key[0].lower() + key[1:], value)
        return policy

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        # the policies are xorm CasbinRule objects without JSON tags, so the keys are capitalized
        return {key[0].upper() + key[1:]: value for key, value in self.__dict__.items()}


class _PolicySDK:
    def get_policies(self, enforcer_name: str, adapter_id: str = "") -> List[Policy]:
        """
        Get the policies of the enforcer, or of the adapter when adapter_id is given.
        """
        data = self.do_get("get-policies", {"id": get_id(enforcer_name, self.org_name), "adapterId": adapter_id})
        return [Policy.from_dict(item) for item in data or []]

    def get_filtered_policies(self, enforcer_id: str, filters: List[Dict]) -> List[Policy]:
        """
        Get the policies of the enforcer that match all the filters,
        e.g. [{"ptype": "p", "fieldIndex": 0, "fieldValues": ["alice"]}].
        """
        data = self.do_post("get-filtered-policies", {"id": get_id(enforcer_id, self.org_name)}, filters)["data"]
        return [Policy.from_dict(item) for item in data or []]

    def modify_policy(self, method: str, enforcer, policies: List[Policy]) -> Dict:
        enforcer.owner = get_owner(enforcer.owner, self.org_name)
        body = [p.to_dict() for p in policies] if method == "update-policy" else policies[0].to_dict()
        return self.do_post(method, {"id": f"{enforcer.owner}/{enforcer.name}"}, body)

    def add_policy(self, enforcer, policy: Policy) -> Dict:
        return self.modify_policy("add-policy", enforcer, [policy])

    def update_policy(self, enforcer, old_policy: Policy, new_policy: Policy) -> Dict:
        return self.modify_policy("update-policy", enforcer, [old_policy, new_policy])

    def remove_policy(self, enforcer, policy: Policy) -> Dict:
        return self.modify_policy("remove-policy", enforcer, [policy])
