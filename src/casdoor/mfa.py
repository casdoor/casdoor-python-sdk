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

from typing import Dict, Optional

EMAIL = "email"
SMS = "sms"
APP = "app"


class _MfaSDK:
    def mfa_initiate(self, owner: str, mfa_type: str, name: str) -> Dict:
        """
        Start setting up the MFA of the user, mfa_type is "app", "email" or "sms".
        The data of the response contains the secret and the recovery codes.
        """
        return self.do_post("mfa/setup/initiate", None, form={"owner": owner, "mfaType": mfa_type, "name": name})

    def mfa_verify(self, owner: str, mfa_type: str, name: str, secret: str, passcode: str) -> Dict:
        """
        Verify the passcode of the MFA being set up.
        """
        form = {"owner": owner, "mfaType": mfa_type, "name": name, "secret": secret, "passcode": passcode}
        return self.do_post("mfa/setup/verify", None, form=form)

    def mfa_enable(self, owner: str, mfa_type: str, name: str, secret: str, recovery_code: Optional[str] = "") -> Dict:
        """
        Enable the MFA after it's verified.
        """
        form = {"owner": owner, "mfaType": mfa_type, "name": name, "secret": secret, "recoveryCode": recovery_code}
        return self.do_post("mfa/setup/enable", None, form=form)

    def mfa_set_preferred(self, owner: str, mfa_type: str, name: str, secret: str = "") -> Dict:
        """
        Set the preferred MFA type of the user.
        """
        form = {"owner": owner, "mfaType": mfa_type, "name": name, "secret": secret}
        return self.do_post("set-preferred-mfa", None, form=form)

    def mfa_delete(self, owner: str, name: str) -> Dict:
        """
        Delete all the MFA settings of the user.
        """
        return self.do_post("delete-mfa", {"owner": owner, "name": name})
