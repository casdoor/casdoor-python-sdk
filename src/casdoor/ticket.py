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

from typing import Dict, List, Optional

from .util import get_id, get_owner


class TicketMessage:
    def __init__(self):
        self.author = ""
        self.text = ""
        self.timestamp = ""
        self.isAdmin = False

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class Ticket:
    """
    The ticket APIs act on behalf of a signed-in user, Casdoor rejects the application's own credentials
    with "Please sign in first". Call them on an SDK from with_access_token(), with the access token of
    the user who owns the tickets, or of an admin.
    """

    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.updatedTime = ""
        self.displayName = ""
        self.user = ""
        self.title = ""
        self.content = ""
        self.state = ""
        self.messages = []

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _TicketSDK:
    def get_tickets(self) -> List[Ticket]:
        """
        Get the tickets of the organization. An admin gets all the tickets, the other users only get their own ones.
        """
        data = self.do_get("get-tickets", {"owner": self.org_name})
        return [Ticket.from_dict(item) for item in data or []]

    def get_pagination_tickets(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the tickets, return a tuple of the tickets and the total count. Only an admin gets paging,
        searching and sorting, the other users always get all their own tickets.
        """
        data, total = self.get_pagination("get-tickets", p, page_size, query_map)
        return [Ticket.from_dict(item) for item in data or []], total

    def get_ticket(self, name: str) -> Optional[Ticket]:
        """
        Get the ticket by name, or by "owner/name" ID. A user who isn't an admin can only get their own tickets.
        """
        return Ticket.from_dict(self.do_get("get-ticket", {"id": get_id(name, self.org_name)}))

    def modify_ticket(self, method: str, ticket: Ticket) -> Dict:
        ticket.owner = get_owner(ticket.owner, self.org_name)
        return self.do_post(method, {"id": f"{ticket.owner}/{ticket.name}"}, ticket.to_dict())

    def add_ticket(self, ticket: Ticket) -> Dict:
        """
        Add a ticket, Casdoor sets its user to the signed-in user.
        """
        return self.modify_ticket("add-ticket", ticket)

    def update_ticket(self, ticket: Ticket) -> Dict:
        """
        Update a ticket. A user who isn't an admin can only close their own tickets.
        """
        return self.modify_ticket("update-ticket", ticket)

    def delete_ticket(self, ticket: Ticket) -> Dict:
        """
        Delete a ticket, only an admin can do it.
        """
        return self.modify_ticket("delete-ticket", ticket)

    def add_ticket_message(self, name: str, message: TicketMessage) -> Dict:
        """
        Append a message to the ticket. Casdoor sets the author and the isAdmin of the message according to
        the signed-in user.
        """
        return self.do_post("add-ticket-message", {"id": get_id(name, self.org_name)}, message.to_dict())
