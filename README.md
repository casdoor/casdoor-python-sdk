# casdoor-python-sdk
Casdoor's SDK for Python will allow you to easily connect your application to the Casdoor authentication system without having to implement it from scratch.

Casdoor SDK is simple to use. We will show you the steps below.

## Step1. Init Config
Initialization requires 5 parameters, which are all str type:
| Name (in order)  | Must | Description                                         |
| ---------------- | ---- | --------------------------------------------------- |
| endpoint         | Yes  | Casdoor Server Url, such as `http://localhost:8000` |
| client_id         | Yes  | Application.client_id                               |
| client_secret     | Yes  | Application.client_secret                           |
| jwt_secret        | Yes  | Same as Casdoor JWT secret                         |
| org_name | Yes  |Organization name


```python
from oauth.main import CasdoorSDK

sdk = CasdoorSDK(
    endpoint,
    client_id,
    client_secret,
    jwt_secret,
    org_name,
)
```
## Step2. Get token and parse

After casdoor verification passed, it will be redirected to your application with code and state, like `http://forum.casbin.org?code=xxx&state=yyyy`.

Your web application can get the `code` and call `get_oauth_token(code)`, then parse out jwt token.

The general process is as follows:

```python
access_token = sdk.get_oauth_token(code)
decoded_msg = sdk.parse_jwt_token(access_token)
```

`decoded_msg` is the JSON data decoded from the `access_token`, which contains user info and other useful stuff.

## Step3. Interact with the users

casdoor-python-sdk support basic user operations, like:

- `get_user(user_id: str)`, get one user by user name.
- `get_users()`, get all users.
- `modify_user(method: str, user: User)/add_user(user: User)/update_user(user: User)/delete_user(user: User)`, write user to database.



