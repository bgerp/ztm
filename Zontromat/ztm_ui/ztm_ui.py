#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""

Zontromat - Zonal Electronic Automation

Copyright (C) [2020] [POLYGONTeam Ltd.]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import json
import time
from urllib.parse import urlparse

from utils.logger import get_logger, crate_log_file
from utils.logic.timer import Timer

from ztm_ui.login_state import LoginState

import requests

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov"]
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "or.dimitrov@polygonteam.com"
"""E-mail of the author.
@see or.dimitrov@polygonteam.com"""

__status__ = "Debug"
"""File status."""

#endregion

class ZtmUI():
    """Zontromat UI interface client.
    """

#region Attributes

#endregion

#region Properties

    @property
    def host(self):
        """Returns Host URL of the servie.

        Returns
        -------
        str
            Host URL of the servie.
        """
        return self.__host

    @host.setter
    def host(self, host):
        """Set Host URL of the service.

        Parameters
        ----------
        host : str
            Host URL of the servie.
        """

        host_no_slash = host

        if host_no_slash.endswith("/"):
            host_no_slash = host_no_slash[:-1]

        self.__host = host_no_slash

    @property
    def timeout(self):
        """Get timeout.

        Returns
        -------
        int
            Timeout.
        """

        return self.__timeout

    @timeout.setter
    def timeout(self, timeout):
        """Set timeout.

        Parameters
        ----------
        timeout : int
            Timeout.
        """

        self.__timeout = timeout

    @property
    def last_sync(self):
        """Last sync time.

        Returns
        -------
        float
            Unix timestamp.
        """

        return self.__last_sync

    @property
    def is_logged_in(self):
        return self.__login_state == LoginState.Accept

#endregion

#region Constructor

    def __init__(self, **kwargs):
        """Constructor
        """

        self.__logger = get_logger(__name__)
        """Logger
        """

        self.__email = None
        """E-Mail
        """

        self.__password = None
        """Password
        """

        self.__host = "127.0.0.1"
        """Host address.
        """

        self.__timeout = 5
        """Communication timeout.
        """

        self.__last_sync = 0
        """Last sync time.
        """

        self.__login_state = LoginState.Wait
        """Login state.
        """

        self.__token = ""
        """Access token.
        """
        
        self.__temporary_registers = None
        """Temporary register data.
        """

        self.__api_login = "/api/login"
        """Login to ZtmUI.
        """

        self.__api_data_get = "/api/data/get"
        """Get data from ZtmUI.
        """

        self.__api_data_post = "/api/data/post"
        """Set data to ZtmUI.
        """

        self.__api_settings_get = "/api/settings/get"
        """Get settings ZtmUI.
        """

        self.__api_settings_post = "/api/settings/post"
        """Get settings ZtmUI.
        """

        self.__api_sync = "/api/sync"
        """Sync data between ZtmUI and Zontromat.
        """

        if "email" in kwargs:
            self.__email = kwargs["email"]

        if self.__email is None:
            raise ValueError("E-mail can not be None.")

        if self.__email == "":
            raise ValueError("E-mail can not be empty string.")

        if "password" in kwargs:
            self.__password = kwargs["password"]

        if self.__password is None:
            raise ValueError("Password can not be None.")

        if self.__password == "":
            raise ValueError("Password can not be empty string.")

        if "host" in kwargs:
            self.__host = kwargs["host"]

        if self.__host is None:
            raise ValueError("Host name can not be None.")

        if self.__host == "":
            raise ValueError("Host name can not be empty string.")

        if not self.__url_validate(self.__host):
            raise ValueError(f"Invalid host name: {self.__host}")

        if self.__host.endswith("/"):
            self.__host = self.__host[:-1]

        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]

        if self.timeout is None:
            raise ValueError("Timeout can not be None.")

        if self.timeout == "":
            raise ValueError("Timeout can not be empty string.")

        self.timeout = int(self.timeout)
        if self.timeout < 0:
            raise ValueError("Timeout can not be less then 0.")

#endregion

#region Private Methods

    def __url_validate(self, x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc])

        except:
            return False

#endregion

#region Public Methods

    def login(self):
        """Login to UI.

        Returns:
            _type_: _description_
        """

        # URI
        uri = self.host + self.__api_login

        # Headers
        headers = {"Accept": "application/json"}

        # Payload
        payload = {"email": self.__email,\
            "password": self.__password}

        try:
            # The request.
            response = requests.post(uri, headers=headers, data=payload, timeout=self.timeout)

            if response is not None:

                if response.status_code == 200:

                    if response.text != "":

                        json_response = json.loads(response.text)

                        if "data" in json_response:
                            data = json_response["data"]

                            if "token" in data:
                                token = data["token"]
        
                                if token is None:
                                    raise ValueError("Token can not be None.")

                                if token == "":
                                    raise ValueError("Token can not be empty string.")

                                self.__token = token

                                self.__login_state = LoginState.Accept

                            else:
                                raise ValueError("No field token in data.")
                        else:
                            raise ValueError("No field data.")
                    else:
                        raise ValueError("Invalid response body.")
                else:
                    raise ValueError("Authentication failed: {}".format(response.status_code))
            else:
                raise ValueError("Invalid response.")

        except Exception as e:
            
            self.__logger.error(e)

            self.__login_state = LoginState.Wait

    def get(self):
        """Get UI registers.

        Returns:
            dict: Response
        """

        response_registers = []

        # URI
        uri = self.host + self.__api_data_get

        # Headers
        headers = {"Accept": "application/json", "Content-type": "application/json", "Authorization": "Bearer {}".format(self.__token)}

        try:
            # The request.
            response = requests.get(uri, headers=headers, timeout=self.timeout)

            if response is not None:

                if response.status_code == 200:

                    if response.text != "":

                        json_response = json.loads(response.text)

                        if "data" in json_response:
                            data = json_response["data"]

                            # Cionbvert to registers.
                            response_registers = data

                            # Update last successful time.
                            self.__last_sync = time.time()

                        else:
                            raise ValueError("No field data.")
                    else:
                        raise ValueError("Invalid response body.")
                else:
                    self.__login_state = LoginState.Wait
                    raise ValueError("Invalid response code: {}".format(response.status_code))
            else:
                raise ValueError("Invalid response.")

        except Exception as e:
            
            self.__logger.error(e)

        return response_registers

    def set(self, registers=[]):
        """Get UI registers.

        Parameters
        ----------
        registers : mixed
            Room registers.

        Returns
        -------
        bool
            Success
        """

        response_registers = None

        # URI
        uri = self.host + self.__api_data_post

        # Convert to JSON.
        str_registers = json.dumps(registers).replace("\'", "\"")

        # Payload
        payload = str_registers

        # Headers
        headers = {"Accept": "application/json", "Content-type": "application/json", "Authorization": "Bearer {}".format(self.__token)}
        # self.__logger.info("1 SYNC; From ZtmUI: {}".format(str_registers))

        # The request.
        response = requests.post(uri, headers=headers, data=payload, timeout=self.timeout)
        # self.__logger.info("2 SYNC; From ZtmUI: {}".format(response_registers))

        if response is not None:
            # self.__logger.info("3 SYNC; From ZtmUI: {}".format(response_registers))

            # OK
            if response.status_code == 200:
                # self.__logger.info("4 SYNC; From ZtmUI: {}".format(response_registers))

                if response.text != "":
                    # self.__logger.info("5 SYNC; From ZtmUI: {}".format(response_registers))

                    response_registers = json.loads(response.text)

                    # self.__logger.info("Sync result: {}".format(response_registers))
                    # self.__logger.info("Registers: {}".format(str_registers))

                    # Update last successful time.
                    self.__last_sync = time.time()

            else:
                self.__logger.error("HTTP Error code: {}".format(response.status_code))
                response_registers = None

        else:
            response_registers = None

        return response_registers

    def set_settings(self, data):

        response_registers = []

        # URI
        uri = self.host + self.__api_settings_post

        # Headers
        headers = {'Accept': 'application/json', "Authorization": "Bearer {}".format(self.__token)}

        try:
            # The request.
            response = requests.post(uri, headers=headers, json=data, timeout=self.timeout)

            if response is not None:

                if response.status_code == 200:

                    if response.text != "":

                        json_response = json.loads(response.text)

                        if "data" in json_response:
                            data = json_response["data"]

                            # Convert to registers.
                            response_registers = data

                            # Update last successful time.
                            self.__last_sync = time.time()

                        else:
                            raise ValueError("No field data.")
                    else:
                        raise ValueError("Invalid response body.")
                else:
                    self.__login_state = LoginState.Wait
                    raise ValueError("Invalid response code: {}".format(response.status_code))
            else:
                raise ValueError("Invalid response.")

        except Exception as e:
            
            self.__logger.error(e)

        return response_registers

    def get_settings(self):

        response_registers = []

        # URI
        uri = self.host + self.__api_settings_get

        # Headers
        headers = {'Accept': 'application/json', "Authorization": "Bearer {}".format(self.__token)}

        try:
            # The request.
            response = requests.get(uri, headers=headers, timeout=self.timeout)

            if response is not None:

                if response.status_code == 200:

                    if response.text != "":

                        json_response = json.loads(response.text)

                        if "data" in json_response:
                            data = json_response["data"]

                            # Convert to registers.
                            response_registers = data

                            # Update last successful time.
                            self.__last_sync = time.time()

                        else:
                            raise ValueError("No field data.")
                    else:
                        raise ValueError("Invalid response body.")
                else:
                    self.__login_state = LoginState.Wait
                    raise ValueError("Invalid response code: {}".format(response.status_code))
            else:
                raise ValueError("Invalid response.")

        except Exception as e:
            
            self.__logger.error(e)

        return response_registers

    def sync(self, registers=[]):
        """Sync registers between ZtmUI and Zontromat.

        Args:
            registers (list, optional): Transmitted registers. Defaults to [].

        Returns:
            []: Received registers.
        """

        response_registers = None

        # URI
        uri = self.host + self.__api_sync

        target_registers = []
        for register in registers:
            name = register.name
            value = register.value
            minimum = 0
            maximum = 0
            status = "Normal" # enum('Rising', 'Falling', 'Normal')
            reg = {"name": name, "value": value, "min": minimum, "max": maximum, "status": status}
            target_registers.append(reg)

        # Convert to JSON.
        str_registers = json.dumps(target_registers).replace("\'", "\"")

        # Payload
        payload = str_registers

        # Headers
        headers = {"Accept": "application/json", "Content-type": "application/json", "Authorization": "Bearer {}".format(self.__token)}
        # self.__logger.info("1 SYNC; From ZtmUI: {}".format(str_registers))

        # The request.
        response = requests.post(uri, headers=headers, data=payload, timeout=self.timeout)
        # self.__logger.info("2 SYNC; From ZtmUI: {}".format(response_registers))

        if response is not None:
            if response.status_code == 200:
                if response.text != "":
                    json_response = json.loads(response.text)
                    if "data" in json_response:
                        data = json_response["data"]
                        # Cionbvert to registers.
                        response_registers = data
                        # Update last successful time.
                        self.__last_sync = time.time()

            else:
                self.__logger.error("HTTP Error code: {}".format(response.status_code))
                response_registers = None

        else:
            response_registers = None

        if self.__temporary_registers != response_registers:
            self.__temporary_registers = response_registers
            return response_registers
        
        return None

#endregion
