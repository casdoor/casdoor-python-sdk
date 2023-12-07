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

import json
from typing import Dict, List

import requests


class Payment:
    def __init__(self):
        self.owner = ""
        self.name = ""
        self.createdTime = ""
        self.displayName = ""
        self.provider = ""
        self.type = ""
        self.productName = ""
        self.productDisplayName = ""
        self.detail = ""
        self.tag = ""
        self.currency = ""
        self.price = 0.0
        self.returnUrl = ""
        self.user = ""
        self.personName = ""
        self.personIdCard = ""
        self.personEmail = ""
        self.personPhone = ""
        self.invoiceType = ""
        self.invoiceTitle = ""
        self.invoiceTaxId = ""
        self.invoiceRemark = ""
        self.invoiceUrl = ""
        self.outOrderId = ""
        self.payUrl = ""
        self.state = ""
        self.message = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name, product_name):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.productName = product_name
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        payment = cls()
        for key, value in data.items():
            if hasattr(payment, key):
                setattr(payment, key, value)
        return payment

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _PaymentSDK:
    def get_payments(self) -> List[Dict]:
        """
        Get the payments from Casdoor.

        :return: a list of dicts containing payment info
        """
        url = self.endpoint + "/api/get-payments"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        payments = []
        for payment in response["data"]:
            payments.append(Payment.from_dict(payment))
        return payments

    def get_payment(self, payment_id: str) -> Dict:
        """
        Get the payment from Casdoor providing the payment_id.

        :param payment_id: the id of the payment
        :return: a dict that contains payment's info
        """
        url = self.endpoint + "/api/get-payment"
        params = {
            "id": f"{self.org_name}/{payment_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Payment.from_dict(response["data"])

    def modify_payment(self, method: str, payment: Payment) -> Dict:
        url = self.endpoint + f"/api/{method}"
        payment.owner = self.org_name
        params = {
            "id": f"{payment.owner}/{payment.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        payment_info = json.dumps(payment.to_dict())
        r = requests.post(url, params=params, data=payment_info)
        response = r.json()
        return response

    def add_payment(self, payment: Payment) -> Dict:
        response = self.modify_payment("add-payment", payment)
        return response

    def update_payment(self, payment: Payment) -> Dict:
        response = self.modify_payment("update-payment", payment)
        return response

    def delete_payment(self, payment: Payment) -> Dict:
        response = self.modify_payment("delete-payment", payment)
        return response
