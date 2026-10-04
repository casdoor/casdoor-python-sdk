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

from typing import Dict


class _MessageSDK:
    def send_email(self, title: str, content: str, sender: str, *receivers: str) -> Dict:
        """
        Send an email by the email provider of the application.
        """
        body = {"title": title, "content": content, "sender": sender, "receivers": list(receivers)}
        return self.do_post("send-email", None, body)

    def send_email_by_provider(self, title: str, content: str, sender: str, provider: str, *receivers: str) -> Dict:
        """
        Send an email by the given email provider.
        """
        body = {"title": title, "content": content, "sender": sender, "receivers": list(receivers)}
        return self.do_post("send-email", {"provider": provider}, body)

    def send_sms(self, content: str, *receivers: str) -> Dict:
        """
        Send an SMS by the SMS provider of the application.
        """
        return self.do_post("send-sms", None, {"content": content, "receivers": list(receivers)})

    def send_sms_by_provider(self, content: str, provider: str, *receivers: str) -> Dict:
        """
        Send an SMS by the given SMS provider.
        """
        return self.do_post("send-sms", {"provider": provider}, {"content": content, "receivers": list(receivers)})

    def send_notification(self, content: str, recipient: str) -> Dict:
        """
        Send a notification by the notification provider of the organization.
        """
        return self.do_post("send-notification", None, {"content": content, "recipient": recipient})
