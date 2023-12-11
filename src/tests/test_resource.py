# Copyright 2023 The Casdoor Authors. All Rights Reserved.
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

import os
import unittest

from src.casdoor import CasdoorSDK
from src.casdoor.resource import Resource
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
)


class ResourceTest(unittest.TestCase):
    def test_resource(self):
        # upload_resource
        filename = "casbinTest.svg"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        with open(file_path, "rb") as file:
            data = file.read()
            name = f"/casdoor/{filename}"
            resource = Resource.new(owner="casbin", name=name)

            sdk = CasdoorSDK(
                TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
            )

            response = sdk.upload_resource(resource.owner, name, "", filename, data)
            self.assertEqual("ok", response["status"])

            # Delete the resource
            delete_resource = sdk.delete_resource(name)
            self.assertEqual("ok", delete_resource["status"])
            # There is no get method
            # so there is no way to test the effect of deletion, only to assert the returned status code
