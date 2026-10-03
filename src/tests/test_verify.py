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
import ipaddress
import os
import ssl
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest import IsolatedAsyncioTestCase, TestCase

import aiohttp
import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from src.casdoor.async_main import AsyncCasdoorSDK
from src.casdoor.main import CasdoorSDK


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'{"status": "ok", "msg": "", "data": []}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


class _SelfSignedServer:
    """
    A local HTTPS server that uses a self-signed certificate for 127.0.0.1.
    """

    def __enter__(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1")])
        now = datetime.datetime.now(datetime.timezone.utc)
        cert = (
            x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=1))
            .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]), False)
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), True)
            .sign(key, hashes.SHA256())
        )

        self.tmpdir = tempfile.TemporaryDirectory()
        self.cert_path = os.path.join(self.tmpdir.name, "cert.pem")
        key_path = os.path.join(self.tmpdir.name, "key.pem")
        with open(self.cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        with open(key_path, "wb") as f:
            f.write(
                key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.TraditionalOpenSSL,
                    serialization.NoEncryption(),
                )
            )

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(self.cert_path, key_path)
        self.server = HTTPServer(("127.0.0.1", 0), _Handler)
        self.server.socket = context.wrap_socket(self.server.socket, server_side=True)
        self.endpoint = f"https://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.shutdown()
        self.server.server_close()
        self.tmpdir.cleanup()


def _sdk_args(endpoint):
    return {
        "endpoint": endpoint,
        "client_id": "client_id",
        "client_secret": "client_secret",
        "certificate": "",
        "org_name": "built-in",
        "application_name": "app-built-in",
    }


class TestVerify(TestCase):
    def test_self_signed_rejected_by_default(self):
        with _SelfSignedServer() as server:
            sdk = CasdoorSDK(**_sdk_args(server.endpoint))
            with self.assertRaises(requests.exceptions.SSLError):
                sdk.get_users()

    def test_self_signed_with_ca_bundle(self):
        with _SelfSignedServer() as server:
            sdk = CasdoorSDK(**_sdk_args(server.endpoint), verify=server.cert_path)
            self.assertEqual(sdk.get_users(), [])

    def test_self_signed_without_verification(self):
        with _SelfSignedServer() as server:
            sdk = CasdoorSDK(**_sdk_args(server.endpoint), verify=False)
            self.assertEqual(sdk.get_users(), [])


class TestAsyncVerify(IsolatedAsyncioTestCase):
    async def test_self_signed_rejected_by_default(self):
        with _SelfSignedServer() as server:
            sdk = AsyncCasdoorSDK(**_sdk_args(server.endpoint))
            with self.assertRaises(aiohttp.ClientConnectorCertificateError):
                await sdk.get_users()

    async def test_self_signed_with_ca_bundle(self):
        with _SelfSignedServer() as server:
            sdk = AsyncCasdoorSDK(**_sdk_args(server.endpoint), verify=server.cert_path)
            self.assertEqual(await sdk.get_users(), [])

    async def test_self_signed_without_verification(self):
        with _SelfSignedServer() as server:
            sdk = AsyncCasdoorSDK(**_sdk_args(server.endpoint), verify=False)
            self.assertEqual(await sdk.get_users(), [])
