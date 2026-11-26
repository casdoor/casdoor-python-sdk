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
from src.casdoor.ticket import Ticket, TicketMessage
from src.tests.test_util import (
    TestApplication,
    TestClientId,
    TestClientSecret,
    TestEndpoint,
    TestJwtPublicKey,
    TestOrganization,
    get_random_name,
)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def new_message(text, author=""):
    message = TicketMessage()
    message.author = author
    message.text = text
    message.timestamp = now()
    return message


class TicketTest(unittest.TestCase):
    def test_ticket(self):
        sdk = CasdoorSDK(
            TestEndpoint, TestClientId, TestClientSecret, TestJwtPublicKey, TestOrganization, TestApplication
        )
        name = get_random_name("Ticket")

        ticket = Ticket()
        ticket.owner = TestOrganization
        ticket.name = name
        ticket.createdTime = now()
        ticket.displayName = "Test Ticket"
        ticket.user = "somebody/else"
        ticket.title = "Test title"
        ticket.content = "Test content"
        ticket.state = "Open"

        # The ticket APIs act on behalf of a user, not of the application
        with self.assertRaisesRegex(Exception, "Please sign in first"):
            sdk.add_ticket(ticket)

        token = sdk.get_oauth_token_by_password("admin", "123")
        user_sdk = sdk.with_access_token(token["access_token"])

        self.assertEqual(user_sdk.add_ticket(ticket)["data"], "Affected")
        self.addCleanup(lambda: user_sdk.get_ticket(name) and user_sdk.delete_ticket(ticket))

        # Casdoor sets the user to the signed-in user
        got = user_sdk.get_ticket(name)
        self.assertEqual((got.title, got.content, got.state), ("Test title", "Test content", "Open"))
        self.assertEqual(got.user, "built-in/admin")

        self.assertIn(name, [item.name for item in user_sdk.get_tickets()])
        tickets, total = user_sdk.get_pagination_tickets(1, 100, {"field": "name", "value": name})
        self.assertEqual(total, 1)
        self.assertEqual([item.name for item in tickets], [name])

        # Casdoor sets the author and the isAdmin of the messages
        self.assertEqual(
            user_sdk.add_ticket_message(name, new_message("first message", "somebody/else"))["data"], "Affected"
        )
        user_sdk.add_ticket_message(name, new_message("second message"))
        got = user_sdk.get_ticket(name)
        self.assertEqual([message["text"] for message in got.messages], ["first message", "second message"])
        self.assertEqual(got.messages[0]["author"], "built-in/admin")
        self.assertTrue(got.messages[0]["isAdmin"])

        with self.assertRaisesRegex(Exception, "not found"):
            user_sdk.add_ticket_message(get_random_name("NotExist"), new_message("lost"))

        got.state = "Closed"
        got.title = "Test title updated"
        user_sdk.update_ticket(got)
        got = user_sdk.get_ticket(name)
        self.assertEqual((got.state, got.title, len(got.messages)), ("Closed", "Test title updated", 2))

        self.assertEqual(user_sdk.delete_ticket(got)["data"], "Affected")
        self.assertIsNone(user_sdk.get_ticket(name))
