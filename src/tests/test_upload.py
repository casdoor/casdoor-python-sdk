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
import io
import unittest
import zipfile
from unittest import mock
from xml.sax.saxutils import escape

from src.casdoor import CasdoorSDK
from src.casdoor.group import Group
from src.casdoor.permission import Permission
from src.casdoor.role import Role
from src.casdoor.user import User
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)

XML_HEADER = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
DOC_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
OOXML = "application/vnd.openxmlformats-officedocument.spreadsheetml"

CONTENT_TYPES = (
    XML_HEADER + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    f'<Override PartName="/xl/workbook.xml" ContentType="{OOXML}.sheet.main+xml"/>'
    f'<Override PartName="/xl/worksheets/sheet1.xml" ContentType="{OOXML}.worksheet+xml"/>'
    f'<Override PartName="/xl/sharedStrings.xml" ContentType="{OOXML}.sharedStrings+xml"/>'
    "</Types>"
)
ROOT_RELS = (
    XML_HEADER + f'<Relationships xmlns="{REL_NS}">'
    f'<Relationship Id="rId1" Type="{DOC_REL}/officeDocument" Target="xl/workbook.xml"/>'
    "</Relationships>"
)
WORKBOOK = (
    XML_HEADER + f'<workbook xmlns="{MAIN_NS}" xmlns:r="{DOC_REL}">'
    '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>'
)
WORKBOOK_RELS = (
    XML_HEADER + f'<Relationships xmlns="{REL_NS}">'
    f'<Relationship Id="rId1" Type="{DOC_REL}/worksheet" Target="worksheets/sheet1.xml"/>'
    f'<Relationship Id="rId2" Type="{DOC_REL}/sharedStrings" Target="sharedStrings.xml"/>'
    "</Relationships>"
)


def new_xlsx(rows):
    """
    Build a minimal Excel (.xlsx) file whose first sheet has the given rows.
    """
    shared, sheet_rows, count = [], [], 0
    for i, row in enumerate(rows):
        cells = []
        for j, cell in enumerate(row):
            cells.append(f'<c r="{chr(ord("A") + j)}{i + 1}" t="s"><v>{count}</v></c>')
            shared.append(f"<si><t>{escape(cell)}</t></si>")
            count += 1
        sheet_rows.append(f'<row r="{i + 1}">{"".join(cells)}</row>')

    sheet = XML_HEADER + f'<worksheet xmlns="{MAIN_NS}"><sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    shared_strings = (
        XML_HEADER + f'<sst xmlns="{MAIN_NS}" count="{count}" uniqueCount="{count}">{"".join(shared)}</sst>'
    )

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("xl/workbook.xml", WORKBOOK)
        z.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
        z.writestr("xl/sharedStrings.xml", shared_strings)
    return buf.getvalue()


def new_sdk():
    return CasdoorSDK(TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def new_object(cls, name):
    obj = cls()
    obj.owner = TestOrganization
    obj.name = name
    return obj


class UploadRequestTest(unittest.TestCase):
    def test_upload_request(self):
        sdk = new_sdk()
        user_sdk = sdk.with_access_token("userToken")
        content = b"xlsx content"
        cases = [
            ("upload-users", user_sdk.upload_users, True),
            ("upload-groups", sdk.upload_groups, False),
            ("upload-roles", sdk.upload_roles, False),
            ("upload-permissions", sdk.upload_permissions, False),
        ]
        for action, upload, as_user in cases:
            with self.subTest(action=action), mock.patch("requests.post") as post:
                post.return_value.json.return_value = {"status": "ok", "msg": ""}
                self.assertEqual(upload(content)["status"], "ok")
                args, kwargs = post.call_args
                self.assertEqual(args[0], f"{TestEndpoint}/api/{action}")
                self.assertEqual(kwargs["files"]["file"][1], content)
                if as_user:
                    self.assertEqual(kwargs["headers"]["Authorization"], "Bearer userToken")
                else:
                    self.assertEqual(kwargs["params"]["clientId"], TestClientId)

                post.return_value.json.return_value = {"status": "error", "msg": "Failed to import"}
                with self.assertRaisesRegex(Exception, "Failed to import"):
                    upload(content)


class UploadTest(unittest.TestCase):
    def test_upload_groups(self):
        sdk = new_sdk()
        names = [get_random_name("UploadGroup"), get_random_name("UploadGroup")]
        header = ["Owner", "Name", "CreatedTime", "DisplayName", "Type", "IsEnabled"]
        file = new_xlsx(
            [
                header,
                [TestOrganization, names[0], now(), "Uploaded 1", "Virtual", "1"],
                [TestOrganization, names[1], now(), "Uploaded 2", "Virtual", "1"],
            ]
        )
        sdk.upload_groups(file)
        for name in names:
            self.addCleanup(sdk.delete_group, new_object(Group, name))
        for i, name in enumerate(names):
            group = sdk.get_group(name)
            self.assertEqual(group.displayName, f"Uploaded {i + 1}")
            self.assertTrue(group.isEnabled)

        # The groups that already exist are skipped, so there is nothing to import
        with self.assertRaisesRegex(Exception, "Failed to import"):
            sdk.upload_groups(file)

        # The new groups are still imported along with the existing ones
        new_name = get_random_name("UploadGroup")
        sdk.upload_groups(
            new_xlsx(
                [
                    header,
                    [TestOrganization, names[0], now(), "Changed", "Virtual", "1"],
                    [TestOrganization, new_name, now(), "Uploaded 3", "Virtual", "1"],
                ]
            )
        )
        self.addCleanup(sdk.delete_group, new_object(Group, new_name))
        self.assertIsNotNone(sdk.get_group(new_name))
        self.assertEqual(sdk.get_group(names[0]).displayName, "Uploaded 1")

    def test_upload_roles(self):
        sdk = new_sdk()
        name = get_random_name("UploadRole")
        file = new_xlsx(
            [
                ["Owner", "Name", "CreatedTime", "DisplayName", "Users", "IsEnabled"],
                [TestOrganization, name, now(), "Uploaded role", '["casbin/admin"]', "1"],
            ]
        )
        sdk.upload_roles(file)
        self.addCleanup(sdk.delete_role, new_object(Role, name))
        role = sdk.get_role(name)
        self.assertEqual(role.displayName, "Uploaded role")
        self.assertEqual(role.users, ["casbin/admin"])
        self.assertTrue(role.isEnabled)

        with self.assertRaisesRegex(Exception, "Failed to import"):
            sdk.upload_roles(file)

    def test_upload_permissions(self):
        sdk = new_sdk()
        name = get_random_name("UploadPermission")
        header = ["Owner", "Name", "CreatedTime", "DisplayName", "Users", "ResourceType", "Resources"]
        header += ["Actions", "Effect", "IsEnabled", "State"]
        row = [TestOrganization, name, now(), "Uploaded permission", '["casbin/admin"]', "Application"]
        row += ['["app-casibase"]', '["Read","Write"]', "Allow", "1", "Approved"]
        # The rows without an owner or a name are ignored
        invalid = ["", "", now(), "Invalid", "", "", "", "", "", "", ""]
        file = new_xlsx([header, row, invalid])
        sdk.upload_permissions(file)
        self.addCleanup(sdk.delete_permission, new_object(Permission, name))
        permission = sdk.get_permission(name)
        self.assertEqual(permission.displayName, "Uploaded permission")
        self.assertEqual(permission.effect, "Allow")
        self.assertTrue(permission.isEnabled)
        self.assertEqual(permission.actions, ["Read", "Write"])
        self.assertEqual(permission.resources, ["app-casibase"])

        with self.assertRaisesRegex(Exception, "Failed to import"):
            sdk.upload_permissions(file)

    def test_upload_users(self):
        sdk = new_sdk()
        names = [get_random_name("UploadUser"), get_random_name("UploadUser")]
        file = new_xlsx(
            [
                ["Owner", "Name", "CreatedTime", "DisplayName", "Email", "IsAdmin", "Groups"],
                [TestOrganization, names[0], now(), "Uploaded 1", f"{names[0]}@example.com", "1", '["casbin/group1"]'],
                [TestOrganization, names[1], now(), "Uploaded 2", f"{names[1]}@example.com", "", ""],
                # Excel keeps blank rows in a sheet, they are skipped
                ["", "", "", "", "", "", ""],
            ]
        )

        # The upload-users API acts on behalf of an admin user, not of the application
        with self.assertRaisesRegex(Exception, "Unauthorized operation"):
            sdk.upload_users(file)

        token = sdk.get_oauth_token_by_password("admin", "123")
        user_sdk = sdk.with_access_token(token["access_token"])
        user_sdk.upload_users(file)
        for name in names:
            self.addCleanup(sdk.delete_user, new_object(User, name))
        for i, name in enumerate(names):
            user = sdk.get_user(name)
            self.assertEqual(user.displayName, f"Uploaded {i + 1}")
            self.assertEqual(user.email, f"{name}@example.com")
            self.assertEqual(user.isAdmin, i == 0)

        with self.assertRaisesRegex(Exception, "already exist"):
            user_sdk.upload_users(file)
