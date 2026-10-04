# Casdoor Python SDK

<p align="center">
  <a href="#badge">
    <img alt="semantic-release" src="https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg">
  </a>
  <a href="https://github.com/casdoor/casdoor-python-sdk/actions/workflows/build.yml">
    <img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/actions/workflow/status/casdoor/casdoor-python-sdk/build.yml?branch=master">
  </a>
  <a href="https://github.com/casdoor/casdoor-python-sdk/releases/latest">
    <img alt="GitHub Release" src="https://img.shields.io/github/v/release/casdoor/casdoor-python-sdk.svg">
  </a>
  <a href="https://pypi.org/project/casdoor">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/casdoor.svg">
  </a>
  <a href="https://pypi.org/project/casdoor">
    <img alt="Python versions" src="https://img.shields.io/pypi/pyversions/casdoor.svg">
  </a>
</p>

<p align="center">
  <a href="https://github.com/casdoor/casdoor-python-sdk/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/casdoor/casdoor-python-sdk?style=flat-square" alt="license">
  </a>
  <a href="https://github.com/casdoor/casdoor-python-sdk/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/casdoor/casdoor-python-sdk?style=flat-square">
  </a>
  <a href="#">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/casdoor/casdoor-python-sdk?style=flat-square">
  </a>
  <a href="https://github.com/casdoor/casdoor-python-sdk/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/casdoor/casdoor-python-sdk?style=flat-square">
  </a>
  <a href="https://discord.gg/5rPsrAzK7S">
    <img alt="Casdoor" src="https://img.shields.io/discord/1022748306096537660?style=flat-square&logo=discord&label=discord&color=5865F2">
  </a>
</p>

Casdoor Python SDK is the official Python client library for [Casdoor](https://casdoor.ai/). It lets your Python backend (Flask, Django, FastAPI, ...) sign users in with Casdoor (OAuth 2.0 / OIDC), verify the JWT tokens issued by Casdoor, and manage users, organizations, applications, roles, permissions and all the other Casdoor objects through the Casdoor APIs.

The SDK has the same features as [casdoor-go-sdk](https://github.com/casdoor/casdoor-go-sdk).

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#️-configuration)
- [Authentication](#-authentication)
- [Resource Management](#-resource-management)
- [API Reference](#-api-reference)
- [Async SDK](#-async-sdk)
- [Development](#-development)
- [Documentation](#-documentation)
- [License](#-license)

## ✨ Features

- **OAuth 2.0 Authentication**: authorization code, password, client credentials and refresh token grants, token introspection, SSO logout
- **JWT Verification**: verify the tokens signed by Casdoor (RS256, RS512, ES256, ES384, ES512)
- **Calling APIs as the User**: `with_access_token()` calls the APIs with the user's own permissions
- **User Management**: CRUD, lookup by email / phone / user ID, pagination, password check and change
- **Organization & Application Management**: organizations, applications, groups, certificates, providers, LDAP
- **Authorization**: roles, permissions, models, adapters, enforcers, policies, `enforce()` and `batch_enforce()`
- **Billing**: products, orders, payments, plans, pricings, subscriptions and transactions
- **Messaging**: send emails, SMS and notifications
- **Multi-Factor Authentication (MFA)**: TOTP, email and SMS MFA setup
- **Other Objects**: sessions, tokens, webhooks, syncers, invitations, resources (file upload) and records

## 📦 Installation

```bash
pip install casdoor
```

## 🚀 Quick Start

```python
from casdoor import CasdoorSDK

sdk = CasdoorSDK(
    endpoint="http://localhost:8000",
    client_id="<client-id>",
    client_secret="<client-secret>",
    certificate="""-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----""",
    org_name="my-organization",
    application_name="my-application",
)

users = sdk.get_users()
print(f"Found {len(users)} users")
```

## ⚙️ Configuration

### Configuration Parameters

| Parameter        | Required | Description                                                                                        |
|------------------|----------|----------------------------------------------------------------------------------------------------|
| endpoint         | Yes      | Casdoor server URL, such as `http://localhost:8000`                                                |
| client_id        | Yes      | Client ID of the Casdoor application                                                               |
| client_secret    | Yes      | Client secret of the Casdoor application                                                           |
| certificate      | Yes      | x509 certificate (PEM `str`) of the application's cert, used to verify JWT tokens                  |
| org_name         | Yes      | Name of the Casdoor organization                                                                   |
| application_name | Yes      | Name of the Casdoor application                                                                    |
| front_endpoint   | No       | URL of the Casdoor web UI used by `get_auth_link()`, defaults to `endpoint` with port 8000 replaced by 7001 |
| verify           | No       | TLS verification like the `verify` argument of `requests`: `True` (default), a CA bundle path, or `False` |
| custom_headers   | No       | HTTP headers added to all the API requests, e.g. `{"Accept-Language": "de"}`                       |

### Getting the Configuration from Casdoor

1. **endpoint**: the URL of your Casdoor server
2. **client_id** and **client_secret**: the application's edit page in the Casdoor admin panel
3. **certificate**: the certificate of the cert selected in the application's "Cert" field (Certs page → the cert → "Certificate")
4. **org_name**: the organization that owns your users
5. **application_name**: the name of your application

### Self-Signed Certificates and Custom Headers

```python
sdk = CasdoorSDK(
    endpoint, client_id, client_secret, certificate, org_name, application_name,
    verify="/path/to/ca.pem",  # trust this CA bundle; False skips the verification (insecure)
    custom_headers={"Accept-Language": "de", "X-Trace-ID": "trace-abc-123"},
)
```

`Accept-Language` makes Casdoor return localized error messages. The authentication of the requests is always managed by the SDK.

### Errors

The API methods raise an `Exception` with Casdoor's error message when Casdoor returns an error. `get_xxx(name)` returns `None` when the object doesn't exist. `add_xxx()`, `update_xxx()` and `delete_xxx()` return Casdoor's response, whose `data` is `"Affected"` when the object is changed.

## 🔐 Authentication

### OAuth 2.0 Flow

#### Step 1: Redirect the User to Casdoor

```python
import secrets

state = secrets.token_urlsafe()  # save it in the user's session
url = sdk.get_auth_link(redirect_uri="http://localhost:8080/callback", state=state)
```

`state` protects the login against CSRF: generate a random `state` on your backend, save it in the user's session, and on the callback reject the request unless the returned `state` equals the saved one. If you omit it, the application name is used, which gives no CSRF protection. If you use [casdoor-js-sdk](https://github.com/casdoor/casdoor-js-sdk), it already generates and checks `state` in the browser before calling your backend, so the backend only needs to exchange the `code`.

`get_signin_url(redirect_uri)`, `get_signup_url(enable_password, redirect_uri)`, `get_user_profile_url(user_name, access_token)` and `get_my_profile_url(access_token)` build the URLs of the other Casdoor pages.

#### Step 2: Handle the Callback

Casdoor redirects back to your application with `code` and `state`, e.g. `http://localhost:8080/callback?code=xxx&state=yyy`. Exchange the code for the tokens and verify the access token:

```python
token = sdk.get_oauth_token(code=code)
access_token = token["access_token"]

user = sdk.parse_jwt_token(access_token)
print(user["name"], user["email"], user["owner"])
```

`parse_jwt_token()` verifies the signature, the audience and the expiration of the token with the certificate, and raises a `jwt` exception when the token is invalid. Extra keyword arguments are passed to `jwt.decode()`.

### Password and Client Credentials Grants

```python
# Resource Owner Password Credentials grant, the application must enable the "Password" grant type
token = sdk.get_oauth_token_by_password("alice", "password")

# Sign in as any user of the organization with the organization's master password
token = sdk.impersonate_user("alice", "<master password>")

# Client Credentials grant: the token belongs to the application instead of a user
token = sdk.get_oauth_token()
```

### Token Refresh and Introspection

```python
new_token = sdk.refresh_oauth_tokens(token["refresh_token"])  # the whole token
access_token = sdk.refresh_oauth_token(token["refresh_token"])  # only the access token

result = sdk.introspect_token(access_token, "access_token")
print(result["active"])
```

### Calling APIs With the User's Access Token

By default, the SDK calls the Casdoor APIs as the application itself: it authenticates with the client ID and client secret, so the calls have the application's (admin) permissions.

To call the APIs on behalf of the signed-in user instead, use `with_access_token()` with the access token returned by `get_oauth_token()`. It returns a new SDK that sends the `Authorization: Bearer <access_token>` header, so Casdoor treats the requests as being made by that user and the user's own permissions apply:

```python
token = sdk.get_oauth_token(code=code)

# An SDK that acts as the user who owns the access token
user_sdk = sdk.with_access_token(token["access_token"])

# "Who am I"
account = user_sdk.get_account()

# Any other API can be called in the same way
users = user_sdk.get_users()
```

The original SDK is not changed, so it's safe to create one such SDK per incoming HTTP request.

**Note**: a non-admin user can only access their own data. If an API raises a permission error, the user simply isn't allowed to call it — use the application's SDK (without `with_access_token()`) for admin operations.

### Logout

```python
sdk.logout(access_token)  # sign the user out of all the applications and devices (SSO logout)
sdk.logout_current_session(access_token)  # only sign out the session of this access token
```

## 📦 Resource Management

### Object Owner

Every object in Casdoor is identified by an ID of the form `owner/name`, where the owner is an organization (`role`, `group`, `user`, `product`, `ldap`, ...) or the built-in `admin` owner (`organization`, `application`, `token`).

By default the SDK fills in the owner for you: the `org_name` of the SDK, or `admin` for the object types listed above. You can address an object in another organization by passing a qualified `owner/name` ID instead of a plain name, and by setting the `owner` field explicitly when creating or updating an object:

```python
from casdoor.role import Role

sdk.get_role("my-role")  # "my-organization/my-role"
sdk.get_role("other-org/my-role")  # "other-org/my-role"

role = Role.new(owner="other-org", name="my-role", created_time="", display_name="", description="")
sdk.add_role(role)  # created in "other-org"
```

> [!IMPORTANT]
> **Behavior change:** `add_xxx()`, `update_xxx()` and `delete_xxx()` used to overwrite the `owner` field of the object with the SDK's organization (or `admin`), and to ignore any owner set by the caller. They now only fill `owner` in when it is empty. If your code sets `owner` to a value other than the SDK's organization (for example the literal `"admin"`), the request is now sent to that owner instead of being silently redirected, so clear the field or set it to the intended organization.

### Method Patterns

Most objects have the same methods:

- `get_xxxs()` - get all the objects of the organization
- `get_pagination_xxxs(p, page_size, query_map=None)` - get a page of the objects, returns `(objects, total_count)`. `query_map` can filter and sort, e.g. `{"field": "name", "value": "abc", "sortField": "createdTime", "sortOrder": "descend"}`
- `get_xxx(name)` - get an object by name (or `owner/name` ID), `None` if it doesn't exist
- `add_xxx(obj)` - create an object
- `update_xxx(obj)` - update an object
- `update_xxx_for_columns(obj, columns)` - only update the given columns (users, roles, permissions, sessions, tokens, invitations)
- `delete_xxx(obj)` - delete an object

The objects are classes such as `casdoor.user.User` or `casdoor.role.Role`, whose attributes have the same (camelCase) names as Casdoor's JSON fields; `to_dict()` and `from_dict()` convert them.

### Users

```python
from casdoor.user import User

users = sdk.get_users()
users, total = sdk.get_pagination_users(1, 10)
user = sdk.get_user("alice")
sdk.get_user_by_email("alice@example.com")
sdk.get_user_by_phone("2025550123")
sdk.get_user_by_user_id("<user id>")
sdk.get_sorted_users("created_time", 10)
sdk.get_global_users()  # users of all organizations
sdk.get_user_count(is_online=True)

user = User.new(owner="my-organization", name="alice", created_time="", display_name="Alice", email="alice@example.com")
user.password = "123456"
sdk.add_user(user)
sdk.update_user(user)
sdk.update_user_for_columns(user, ["displayName", "email"])
sdk.update_user_by_id("my-organization/alice", user)
sdk.update_user_by_user_id("my-organization", "<user id>", user)
sdk.delete_user(user)

# Check and change the password
user.password = "123456"
sdk.check_user_password(user)  # True or False
sdk.set_password("my-organization", "alice", "123456", "654321")

# Roles of the user
sdk.assign_role_to_user("alice", "admin")
sdk.get_user_roles("alice")
sdk.remove_role_from_user("alice", "admin")
```

### Organizations and Applications

```python
sdk.get_organizations()
sdk.get_organization("my-organization")
sdk.get_organization_names()
sdk.get_applications()
sdk.get_application("my-application")
sdk.get_organization_applications()  # applications of the SDK's organization
```

### Permissions and Enforcement

```python
sdk.get_permissions()
sdk.get_permissions_by_role("admin")

# Check a request against a permission (or a model / resource / enforcer / owner)
allowed = sdk.enforce("my-organization/read-data", "", "", "", "", ["my-organization/alice", "data1", "read"])
results = sdk.batch_enforce(
    "my-organization/read-data", "", "", "",
    [["my-organization/alice", "data1", "read"], ["my-organization/bob", "data1", "read"]],
)
```

### Enforcers and Policies

```python
from casdoor.policy import Policy

enforcer = sdk.get_enforcer("my-enforcer")
sdk.get_policies("my-enforcer")
sdk.get_filtered_policies("my-organization/my-enforcer", [{"ptype": "p", "fieldIndex": 0, "fieldValues": ["alice"]}])
sdk.add_policy(enforcer, Policy.new("p", "alice", "data1", "read"))
sdk.update_policy(enforcer, old_policy, new_policy)
sdk.remove_policy(enforcer, policy)
```

### Billing: Products, Orders, Payments and Transactions

```python
# Place an order of products for a user and pay it with a payment provider
order = sdk.place_order([{"name": "my-product", "quantity": 1}], "alice")
payment = sdk.pay_order(order.name, "my-payment-provider")
sdk.cancel_order(order.name)

sdk.get_user_orders("alice")
sdk.get_user_payments("alice")
sdk.get_user_transactions("alice")

# Validate a transaction (e.g. the balance) without saving it
sdk.add_transaction_with_dry_run(transaction, True)
name = sdk.add_transaction(transaction)["data"]
```

### Email, SMS and Notifications

```python
sdk.send_email("Hello", "Hello world", "Casdoor", "alice@example.com", "bob@example.com")
sdk.send_email_by_provider("Hello", "Hello world", "Casdoor", "my-email-provider", "alice@example.com")
sdk.send_sms("123456", "+12025550123")
sdk.send_sms_by_provider("123456", "my-sms-provider", "+12025550123")
sdk.send_notification("Hello", "alice")
```

### Resources (File Upload)

```python
with open("avatar.png", "rb") as f:
    response = sdk.upload_resource_ex("alice", "avatar", "user", "/avatar/alice.png", f)
file_url, name = response["data"], response["data2"]

sdk.get_resources("my-organization", "alice", "", "", "", "")
sdk.get_pagination_resources("my-organization", "alice", "", "", 10, 1)
sdk.delete_resource_with_tag(resource, "Direct")
```

### LDAP

```python
sdk.get_ldaps()
ldap_users = sdk.get_ldap_users("<ldap id>")
sdk.sync_ldap_users("<ldap id>", ldap_users["users"])
sdk.sync_ldap_users_from_server("<ldap id>")  # fetch and sync all the LDAP users
```

### Multi-Factor Authentication

```python
from casdoor import mfa

setup = sdk.mfa_initiate("my-organization", mfa.APP, "alice")["data"]
sdk.mfa_verify("my-organization", mfa.APP, "alice", setup["secret"], "<passcode>")
sdk.mfa_enable("my-organization", mfa.APP, "alice", setup["secret"], setup["recoveryCodes"][0])
sdk.mfa_set_preferred("my-organization", mfa.APP, "alice")
sdk.mfa_delete("my-organization", "alice")
```

## 📚 API Reference

| Object           | Methods                                                                                                                            |
|------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **Auth**         | `get_auth_link`, `get_oauth_token`, `get_oauth_token_by_password`, `impersonate_user`, `refresh_oauth_token(s)`, `introspect_token`, `parse_jwt_token`, `logout`, `logout_current_session`, `with_access_token`, `get_account` |
| **URL**          | `get_signin_url`, `get_signup_url`, `get_user_profile_url`, `get_my_profile_url`                                                   |
| **User**         | CRUD + pagination, `get_user_by_email`, `get_user_by_phone`, `get_user_by_user_id`, `get_sorted_users`, `get_global_users`, `get_user_count`, `update_user_for_columns`, `update_user_by_id`, `update_user_by_user_id`, `check_user_password`, `set_password`, `assign_role_to_user`, `remove_role_from_user`, `get_user_roles` |
| **Organization** | CRUD, `get_organization_names`                                                                                                     |
| **Application**  | CRUD, `get_organization_applications`                                                                                              |
| **Group**        | CRUD + pagination                                                                                                                  |
| **Cert**         | CRUD, `get_global_certs`                                                                                                           |
| **Provider**     | CRUD + pagination                                                                                                                  |
| **Role**         | CRUD + pagination, `update_role_for_columns`                                                                                       |
| **Permission**   | CRUD + pagination, `update_permission_for_columns`, `get_permissions_by_role`                                                      |
| **Model / Adapter / Enforcer** | CRUD + pagination                                                                                                    |
| **Policy**       | `get_policies`, `get_filtered_policies`, `add_policy`, `update_policy`, `remove_policy`                                            |
| **Enforce**      | `enforce`, `batch_enforce`                                                                                                         |
| **Session**      | CRUD + pagination, `update_session_for_columns`                                                                                    |
| **Token**        | CRUD + pagination, `update_token_for_columns`, `introspect_token`                                                                  |
| **Product**      | CRUD + pagination                                                                                                                  |
| **Order**        | CRUD + pagination, `get_user_orders`, `place_order`, `pay_order`, `buy_product`, `cancel_order`                                    |
| **Payment**      | CRUD + pagination, `get_user_payments`, `notify_payment`, `invoice_payment`                                                        |
| **Plan / Pricing / Subscription** | CRUD + pagination                                                                                                 |
| **Transaction**  | CRUD + pagination, `get_user_transactions`, `add_transaction_with_dry_run`                                                         |
| **Invitation**   | CRUD + pagination, `update_invitation_for_columns`, `get_invitation_info`                                                          |
| **LDAP**         | CRUD, `get_ldap_users`, `sync_ldap_users`, `sync_ldap_users_from_server`                                                           |
| **Syncer / Webhook** | CRUD + pagination                                                                                                              |
| **Resource**     | `get_resources`, `get_pagination_resources`, `get_resource`, `get_resource_ex`, `add_resource`, `update_resource`, `upload_resource`, `upload_resource_ex`, `delete_resource`, `delete_resource_with_tag` |
| **Record**       | `get_records`, `get_pagination_records`, `get_record`, `add_record`                                                                |
| **Email / SMS / Notification** | `send_email`, `send_email_by_provider`, `send_sms`, `send_sms_by_provider`, `send_notification`                      |
| **MFA**          | `mfa_initiate`, `mfa_verify`, `mfa_enable`, `mfa_set_preferred`, `mfa_delete`                                                      |
| **Low-level**    | `get_response`, `do_get`, `do_post`, `get_pagination` to call any other Casdoor API                                                |

## ⚡ Async SDK

`AsyncCasdoorSDK` is an `aiohttp` based SDK for asyncio applications. It supports the OAuth flow, JWT verification, `enforce()` / `batch_enforce()` and the user and role APIs; use `CasdoorSDK` for the other APIs.

```python
from casdoor import AsyncCasdoorSDK

sdk = AsyncCasdoorSDK(endpoint, client_id, client_secret, certificate, org_name, application_name)

async with sdk:
    token = await sdk.get_oauth_token(code=code)
    user = sdk.parse_jwt_token(token["access_token"])
    users = await sdk.get_users()
```

## 🛠 Development

The tests run against a real Casdoor server. CI starts one with Docker and the data in [.ci/casdoor/init_data.json](.ci/casdoor/init_data.json):

```bash
docker run -d --name casdoor -p 8000:8000 \
  -e driverName=sqlite \
  -e dataSourceName='file:casdoor.db?cache=shared' \
  -e initDataFile=/init_data.json \
  -v "$PWD/.ci/casdoor/init_data.json:/init_data.json:ro" \
  casbin/casdoor-all-in-one

pip install -r requirements.txt black ruff
black --check src
ruff check src
python -m unittest src/tests/load_tests.py -v
```

Set `CASDOOR_TEST_ENDPOINT`, `CASDOOR_TEST_CLIENT_ID`, `CASDOOR_TEST_CLIENT_SECRET`, `CASDOOR_TEST_ORGANIZATION` and `CASDOOR_TEST_APPLICATION` to run the tests against another server.

Releases are published to PyPI automatically by semantic-release when commits are pushed to `master`.

## 📖 Documentation

- [Casdoor Documentation](https://casdoor.ai/docs/overview)
- [Casdoor Python SDK Documentation](https://casdoor.ai/docs/how-to-connect/sdk)
- [Casdoor API Documentation](https://door.casdoor.com/swagger)
- [Casdoor GitHub Repository](https://github.com/casdoor/casdoor)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
