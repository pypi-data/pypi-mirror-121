"""
    Class for defining headers for deployment infrastructure
    Copyright (C) 2021  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import smtplib
import ssl

from typing import Any

from blankly.utils.utils import load_notify_preferences
from blankly.frameworks.strategy import Strategy
from blankly.frameworks.signal.signal import Signal


class Reporter:
    def __init__(self):
        self.__live_vars = {}
        self.__signal = None
        pass

    def export_live_var(self, var: Any, name: str, description: str = None):
        """
        Create a variable that can be updated by external processes
        All strings must be in ascii characters

        Args:
            var: Any variable that can represented in a string (ex: float, str, int)
            name: The name of the live_var
            description (optional): A longer description for use in GUIs or other areas where context is important
        """
        self.__live_vars[id(var)] = var

    def update_live_var(self, var):
        """
        Get the variable as with any changes that may have occurred

        Args:
            var: The variable that was exported initially
        """
        return self.__live_vars[id(var)]

    def export_strategy(self, strategy: Strategy):
        """
        Export a strategy for monitoring. This is used internally on the construction of the strategy object

        Args:
            strategy (Strategy): The strategy object to monitor
        """
        pass

    def export_signal(self, signal: Signal):
        """
        Export a signal object to the backend for monitoring

        Args:
            signal: A signal object to export
        """
        if self.__signal is None:
            self.__signal = signal
        else:
            raise RuntimeError("Currently only a single signal can be exported per model.")

    def export_signal_result(self, signal: Signal):
        """
        Re-export for the finished signal result

        Args:
            signal: A signal object to export
        """

        pass

    def log_strategy_event(self, strategy_object, event_name, response, **kwargs):
        """
        Export a strategy event that has occurred
        """
        pass

    def text(self, message_str: str):
        """
        Send a text message to your number

        Args:
            message_str: The message body to be sent to your phone number
        """
        notify_preferences = load_notify_preferences()
        provider = notify_preferences['text']['provider']
        phone_number = notify_preferences['text']['phone_number']

        email_lookup = {
            'att': '@txt.att.net',
            'boost': '@smsmyboostmobile.com',
            'cricket': '@sms.cricketwireless.net',
            'sprint': '@messaging.sprintpcs.com',
            't_mobile': '@tmomail.net',
            'us_cellular': '@email.uscc.net',
            'verizon': '@vtext.com',
            'virgin_mobile': '@vmobl.com'
        }
        try:
            email = email_lookup[provider]
        except KeyError:
            raise KeyError("Provider not found. Check the notify.json documentation to see supported providers.")

        self.email(message_str, override_receiver=phone_number + email)

    def email(self, email_str: str, override_receiver: str = None):
        """
        Send an email to your user account email

        This is only active during live deployment on blankly services because it relies on backend infrastructure

        Args:
            email_str: The body of the email to send
            override_receiver: Change the address that the email is being sent to. This is used to rapidly switch to
             text messages
        """
        notify_preferences = load_notify_preferences()
        port = notify_preferences['email']['port']
        smtp_server = notify_preferences['email']['smtp_server']
        sender_email = notify_preferences['email']['sender_email']
        receiver_email = notify_preferences['email']['receiver_email']
        password = notify_preferences['email']['password']

        if override_receiver is not None:
            receiver_email = override_receiver

        message = email_str

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
