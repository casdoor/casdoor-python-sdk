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

from src.casdoor import CasdoorSDK


class Cert:
    def __init__(self):
        self.name = "string"
        self.owner = "string"
        self.createdTime = "string"
        self.displayName = "string"
        self.type = "string"
        self.scope = "string"
        self.cryptoAlgorithm = "string"
        self.bitSize = 0
        self.expireInYears = 0
        self.certificate = "string"
        self.privateKey = "string"
        self.authorityPublicKey = "string"
        self.authorityRootPublicKey = "string"

    def __str__(self):
        return str(self.__dict__)

    def to_dict(self) -> dict:
        return self.__dict__


class CertSDK(CasdoorSDK):
    def get_certs(self) -> List[Dict]:
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
        certs = r.json()
        return certs

    def get_cert(self, cert_id: str) -> Dict:
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
        cert = r.json()
        return cert

    def modify_cert(self, method: str, cert: Cert) -> Dict:
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
        return response

    def add_cert(self, cert: Cert) -> Dict:
        response = self.modify_cert("add-cert", cert)
        return response

    def update_cert(self, cert: Cert) -> Dict:
        response = self.modify_cert("update-cert", cert)
        return response

    def delete_cert(self, cert: Cert) -> Dict:
        response = self.modify_cert("delete-cert", cert)
        return response
