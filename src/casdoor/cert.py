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
from typing import List

import requests


class Cert:
    def __init__(self):
        self.name = ""
        self.owner = ""
        self.createdTime = ""
        self.displayName = ""
        self.type = ""
        self.scope = ""
        self.cryptoAlgorithm = ""
        self.bitSize = 0
        self.expireInYears = 0
        self.certificate = ""
        self.privateKey = ""
        self.authorityPublicKey = ""
        self.authorityRootPublicKey = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name, scope, type, crypto_algorithm, bit_size, expire_in_years):
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        self.scope = scope
        self.type = type
        self.cryptoAlgorithm = crypto_algorithm
        self.bitSize = bit_size
        self.expireInYears = expire_in_years
        return self

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        cert = cls()
        for key, value in data.items():
            if hasattr(cert, key):
                setattr(cert, key, value)
        return cert

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class _CertSDK:
    def get_certs(self) -> List[Cert]:
        """
        Get the certs from Casdoor.

        :return: a list of dicts containing cert info
        """
        url = self.endpoint + "/api/get-certs"
        params = {
            "owner": self.org_name,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])

        res = []
        for element in response["data"]:
            res.append(Cert.from_dict(element))
        return res

    def get_cert(self, cert_id: str) -> Cert:
        """
        Get the cert from Casdoor providing the cert_id.

        :param cert_id: the id of the cert
        :return: a dict that contains cert's info
        """
        url = self.endpoint + "/api/get-cert"
        params = {
            "id": f"{self.org_name}/{cert_id}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])

        return Cert.from_dict(response["data"])

    def modify_cert(self, method: str, cert: Cert) -> str:
        url = self.endpoint + f"/api/{method}"
        cert.owner = self.org_name
        params = {
            "id": f"{cert.owner}/{cert.name}",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
        }
        cert_info = json.dumps(cert.to_dict())
        r = requests.post(url, params=params, data=cert_info)
        response = r.json()
        if response["status"] != "ok":
            raise ValueError(response["msg"])
        return str(response["data"])

    def add_cert(self, cert: Cert) -> str:
        response = self.modify_cert("add-cert", cert)
        return response

    def update_cert(self, cert: Cert) -> str:
        response = self.modify_cert("update-cert", cert)
        return response

    def delete_cert(self, cert: Cert) -> str:
        response = self.modify_cert("delete-cert", cert)
        return response
