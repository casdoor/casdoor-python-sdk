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
