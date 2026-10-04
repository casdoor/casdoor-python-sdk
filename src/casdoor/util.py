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

import json
from typing import Any, Dict, Optional, Tuple

import requests


def get_id(name: str, default_owner: str) -> str:
    """
    Return name as is if it's already an "owner/name" ID, otherwise prefix it with default_owner.
    """
    if "/" in name:
        return name
    return f"{default_owner}/{name}"


def get_admin_id(name: str) -> str:
    """
    get_id for the object types that are owned by "admin" instead of an organization.
    """
    return get_id(name, "admin")


def get_owner(owner: Optional[str], default_owner: str) -> str:
    """
    Keep the caller-provided owner and only fall back to default_owner when it's empty.
    """
    return owner if owner else default_owner


class _HttpSDK:
    """
    The HTTP helpers shared by all the API methods: they authenticate the requests as the
    application (client ID and secret), or as the user when the SDK is created by
    with_access_token(), and add the custom headers.
    """

    access_token: str = ""
    custom_headers: Dict[str, str] = {}

    def _auth(self, params: Optional[Dict]) -> Tuple[Dict, Dict]:
        params = dict(params or {})
        headers = dict(self.custom_headers or {})
        if self.access_token:
            params.pop("clientId", None)
            params.pop("clientSecret", None)
            headers["Authorization"] = f"Bearer {self.access_token}"
        else:
            params["clientId"] = self.client_id
            params["clientSecret"] = self.client_secret
        return params, headers

    def _http_get(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        params, headers = self._auth(params)
        return requests.get(url, params=params, headers=headers, verify=self.verify)

    def _http_post(
        self, url: str, params: Optional[Dict] = None, data: Any = None, files: Optional[Dict] = None
    ) -> requests.Response:
        params, headers = self._auth(params)
        return requests.post(url, params=params, data=data, files=files, headers=headers, verify=self.verify)

    def get_response(self, action: str, params: Optional[Dict] = None) -> Dict:
        """
        GET /api/<action> and return the whole response, raise an Exception when its status is not "ok".
        """
        r = self._http_get(f"{self.endpoint}/api/{action}", {k: v for k, v in (params or {}).items() if v is not None})
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def do_get(self, action: str, params: Optional[Dict] = None) -> Any:
        """
        GET /api/<action> and return the data of the response.
        """
        return self.get_response(action, params)["data"]

    def do_post(
        self,
        action: str,
        params: Optional[Dict] = None,
        body: Any = None,
        form: Optional[Dict] = None,
        files: Optional[Dict] = None,
    ) -> Dict:
        """
        POST /api/<action> with a JSON body, a multipart form or files, and return the whole response,
        raise an Exception when its status is not "ok".
        """
        params = {k: v for k, v in (params or {}).items() if v is not None}
        if form is not None:
            files = {k: (None, str(v)) for k, v in form.items()}
            data = None
        else:
            data = None if body is None else json.dumps(body)
        r = self._http_post(f"{self.endpoint}/api/{action}", params=params, data=data, files=files)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return response

    def get_pagination(self, action: str, p: int, page_size: int, query_map: Optional[Dict] = None, owner=None):
        """
        Get a page of objects, return (data, total count).
        """
        params = dict(query_map or {})
        params["owner"] = owner if owner is not None else self.org_name
        params["p"] = str(p)
        params["pageSize"] = str(page_size)
        response = self.get_response(action, params)
        return response["data"], response["data2"]
