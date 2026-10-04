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


class Transaction:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.application = ""
        self.domain = ""
        self.category = ""
        self.type = ""
        self.subtype = ""
        self.provider = ""
        self.user = ""
        self.tag = ""
        self.amount = 0.0
        self.currency = ""
        self.payment = ""
        self.state = ""

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


class _TransactionSDK:
    def get_transactions(self) -> List[Transaction]:
        """
        Get all the transactions from Casdoor.
        """
        data = self.do_get("get-transactions", {"owner": self.org_name})
        return [Transaction.from_dict(item) for item in data or []]

    def get_pagination_transactions(self, p: int, page_size: int, query_map: Optional[Dict[str, str]] = None):
        """
        Get a page of the transactions from Casdoor, return a tuple of the transactions and the total count.
        """
        data, total = self.get_pagination("get-transactions", p, page_size, query_map)
        return [Transaction.from_dict(item) for item in data or []], total

    def get_transaction(self, name: str) -> Optional[Transaction]:
        """
        Get the transaction by name, or by "owner/name" ID.
        """
        return Transaction.from_dict(self.do_get("get-transaction", {"id": get_id(name, self.org_name)}))

    def get_user_transactions(self, user_name: str) -> List[Transaction]:
        data = self.do_get("get-user-transactions", {"owner": self.org_name, "user": user_name})
        return [Transaction.from_dict(item) for item in data or []]

    def add_transaction_with_dry_run(self, transaction: Transaction, dry_run: bool) -> Dict:
        """
        Add the transaction, when dry_run is True it's only validated (e.g. the user's balance) and not saved.
        The data of the response is the name of the transaction.
        """
        params = {"dryRun": "1"} if dry_run else None
        return self.modify_transaction("add-transaction", transaction, params=params)

    def modify_transaction(
        self, method: str, transaction: Transaction, columns: Optional[List[str]] = None, params: Optional[Dict] = None
    ) -> Dict:
        transaction.owner = get_owner(transaction.owner, self.org_name)
        query = dict(params or {})
        query["id"] = f"{transaction.owner}/{transaction.name}"
        if columns:
            query["columns"] = ",".join(columns)
        return self.do_post(method, query, transaction.to_dict())

    def add_transaction(self, transaction: Transaction) -> Dict:
        return self.modify_transaction("add-transaction", transaction)

    def update_transaction(self, transaction: Transaction) -> Dict:
        return self.modify_transaction("update-transaction", transaction)

    def delete_transaction(self, transaction: Transaction) -> Dict:
        return self.modify_transaction("delete-transaction", transaction)
