# casdoor-python-sdk

[![GitHub Action](https://github.com/casdoor/casdoor-python-sdk/workflows/build/badge.svg?branch=master)](https://github.com/casdoor/casdoor-python-sdk/actions)
[![Version](https://img.shields.io/pypi/v/casdoor.svg)](https://pypi.org/project/casdoor/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/casdoor.svg)](https://pypi.org/project/casdoor/)
[![Pyversions](https://img.shields.io/pypi/pyversions/casdoor.svg)](https://pypi.org/project/casdoor/)
[![Gitter](https://badges.gitter.im/casbin/casdoor.svg)](https://gitter.im/casbin/casdoor)

Casdoor's SDK for Python will allow you to easily connect your application to the Casdoor authentication system without having to implement it from scratch.

Casdoor-python-sdk is available on PyPI:

```console
$ pip install casdoor
```

Casdoor SDK is simple to use. We will show you the steps below.

## Step1. Init Config
Initialization requires 5 parameters, which are all str type:
| Name (in order)  | Must | Description                                         |
| ---------------- | ---- | --------------------------------------------------- |
| endpoint         | Yes  | Casdoor Server Url, such as `http://localhost:8000` |
| client_id        | Yes  | Application.client_id                               |
| client_secret    | Yes  | Application.client_secret                           |
| certificate      | Yes  | Same as Casdoor   certificate                       |
| org_name         | Yes  | Organization name                                   |

```python
from casdoor import CasdoorSDK

certificate = b'''-----BEGIN CERTIFICATE-----
MIIE+TCCAuGgAwIBAgIDAeJAMA0GCSqGSIb3DQEBCwUAMDYxHTAbBgNVBAoTFENh
...
-----END CERTIFICATE-----'''

sdk = CasdoorSDK(
    endpoint,
    client_id,
    client_secret,
    certificate,
    org_name,
)
```

OR use async version

```python
from casdoor import AsyncCasdoorSDK

certificate = b'''-----BEGIN CERTIFICATE-----
MIIE+TCCAuGgAwIBAgIDAeJAMA0GCSqGSIb3DQEBCwUAMDYxHTAbBgNVBAoTFENh
...
-----END CERTIFICATE-----'''

sdk = AsyncCasdoorSDK(
    endpoint,
    client_id,
    client_secret,
    certificate,
    org_name,
)
```


## Step2. Authorize with the Casdoor server
At this point, we should use some ways to verify with the Casdoor server.  

To start, we want you understand clearly the verification process of Casdoor.
The following paragraphs will mention your app that wants to use Casdoor as a means
of verification as `APP`, and Casdoor as `Casdoor`.

1. `APP` will send a request to `Casdoor`.  
   Since `Casdoor` is a UI-based OAuth
   provider, you cannot use request management service like Postman to send a URL
   with parameters and get back a JSON file.  
   

2. The simplest way to try it out is to type the URL in your browser (in which JavaScript can be executed to run the UI).

3. Type in the URL in your browser in this format:
`endpoint/login/oauth/authorize?client_id=xxx&response_type=code&redirect_uri=xxx&scope=read&state=xxx`  
In this URL the `endpoint` is your Casdoor's location, as mentioned in Step1; then the `xxx` need to be filled out by yourself.  

Hints:  
1. `redirect_uri` is the URL that your `APP` is configured to
listen to the response from `Casdoor`. For example, if your `redirect_uri` is `https://forum.casbin.com/callback`, then Casdoor will send a request to this URL along with two parameters `code` and `state`, which will be used in later steps for authentication.   

2. `state` is usually your Application's name, you can find it under the `Applications` tab in `Casdoor`, and the leftmost `Name` column gives each application's name. 

3. Of course you want your `APP` to be able to send the URL. For example you should have something like a button, and it carries this URL. So when you click the button, you should be redirected to `Casdoor` for verification. For now you are typing it in the browser simply for testing.
   
## Step3. Get token and parse

After Casdoor verification passed, it will be redirected to your application with code and state as said in Step2, like `https://forum.casbin.com/callback?code=xxx&state=yyyy`.

Your web application can get the `code` and call `get_oauth_token(code=code)`, then parse out jwt token.

The general process is as follows:

```python
access_token = sdk.get_oauth_token(code=code)
decoded_msg = sdk.parse_jwt_token(access_token)
```

`decoded_msg` is the JSON data decoded from the `access_token`, which contains user info and other useful stuff.

## Step4. Interact with the users

casdoor-python-sdk support basic user operations, like:

- `get_user(user_id: str)`, get one user by user name.
- `get_users()`, get all users.
- `modify_user(method: str, user: User)/add_user(user: User)/update_user(user: User)/delete_user(user: User)`, write user to database.
- `refresh_token_request(refresh_token: str, scope: str)`, refresh access token
- `enforce(self, permission_model_name: str, sub: str, obj: str, act: str)`, check permission from model


## Also. Resource Owner Password Credentials Grant

If your application doesn't have a frontend that redirects users to Casdoor and you have Password Credentials Grant enabled, then you may get access token like this:

```python
access_token = sdk.get_oauth_token(username=username, password=password)
decoded_msg = sdk.parse_jwt_token(access_token)
```

`decoded_msg` is the JSON data decoded from the `access_token`, which contains user info and other useful stuff.