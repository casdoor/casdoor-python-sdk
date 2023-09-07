# Copyright 2021 The Casbin Authors. All Rights Reserved.
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

from .main import CasdoorSDK


class Payment:
    def __init__(self):
        self.owner = "string"
        self.name = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.provider = "string"
        self.type = "string"
        self.productName = "string"
        self.productDisplayName = "string"
        self.detail = "string"
        self.tag = "string"
        self.currency = "string"
        self.price = 0.0
        self.returnUrl = "string"
        self.user = "string"
        self.personName = "string"
        self.personIdCard = "string"
        self.personEmail = "string"
        self.personPhone = "string"
        self.invoiceType = "string"
        self.invoiceTitle = "string"
        self.invoiceTaxId = "string"
        self.invoiceRemark = "string"
        self.invoiceUrl = "string"
        self.outOrderId = "string"
        self.payUrl = "string"
        self.state = "string"
        self.message = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class PaymentSDK(CasdoorSDK):
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
        payments = r.json()
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
        payment = r.json()
        return payment

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
