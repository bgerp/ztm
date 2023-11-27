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

    __logger = None
    """Logger"""

    __email = None
    """E-Mail
    """

    __password = None
    """Password
    """

    __host = "127.0.0.1"
    """Host address.
    """

    __api_login = "/api/login"
    """Login to ZtmUI.
    """

    __api_data_get = "/api/data/get"
    """Get data from ZtmUI.
    """

    __api_data_set = "/api/data/set"
    """Set data to ZtmUI.
    """

    __api_settings_get = "/api/settings/get"
    """Get settings ZtmUI.
    """

    __api_settings_post = "/api/settings/post"
    """Get settings ZtmUI.
    """

    __timeout = 5
    """Communication timeout.
    """

    __last_sync = 0
    """Last sync time.
    """

    __login_state = LoginState.Wait
    """Login state.
    """

    __token = ""
    """Access token.
    """

    __heart_beat_timer = None

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

#endregion

#region Constructor

    def __init__(self, **kwargs):
        """Constructor
        """
        
        # Create logger.
        self.__logger = get_logger(__name__)

        # User
        email = None
        if "email" in kwargs:
            email = kwargs["email"]

        if email is None:
            raise ValueError("E-mail can not be None.")

        if email == "":
            raise ValueError("E-mail can not be empty string.")

        self.__email = email

        # Password
        password = None
        if "password" in kwargs:
            password = kwargs["password"]

        if password is None:
            raise ValueError("Password can not be None.")

        if password == "":
            raise ValueError("Password can not be empty string.")

        self.__password = password

        # Host
        host = None
        if "host" in kwargs:
            host = kwargs["host"]

        if host is None:
            raise ValueError("Host name can not be None.")

        if host == "":
            raise ValueError("Host name can not be empty string.")

        if not self.__url_validate(host):
            raise ValueError(f"Invalid host name: {host}")

        if host.endswith("/"):
            host = host[:-1]

        self.__host = host

        # Host
        timeout = None
        if "timeout" in kwargs:
            timeout = kwargs["timeout"]

        if timeout is None:
            raise ValueError("Timeout can not be None.")

        if timeout == "":
            raise ValueError("Timeout can not be empty string.")

        timeout = int(timeout)
        if timeout < 0:
            raise ValueError("Timeout can not be less then 0.")

        self.timeout = timeout

        self.__heart_beat_timer = Timer(60)

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

    def is_logged_in(self):

        return self.__login_state == LoginState.Accept

    def get(self):
        """Get UI registers.

        Returns:
            dict: Response
        """

        response_registers = []

        # URI
        uri = self.host + self.__api_data_get

        # Headers
        headers = {"Accept": "application/json", "Authorization": "Bearer {}".format(self.__token)}

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
        uri = self.host + self.__api_data_get

        # Convert to JSON.
        str_registers = json.dumps(registers).replace("\'", "\"")

        # Payload
        payload = {}
        # payload = {"token": self.__session.session,\
        #     "registers": str_registers, "last_sync": self.__last_sync}

        # self.__logger.info("SYNC; To ZtmUI: {}".format(payload))

        # Headers
        headers = {"Accept": "application/json", "Authorization": "Bearer {}".format(self.__token)}

        # The request.
        response = requests.get(uri, headers=headers, data=payload, timeout=self.timeout)

        if response is not None:

            # OK
            if response.status_code == 200:

                if response.text != "":

                    response_registers = json.loads(response.text)

                    # self.__logger.info("SYNC; From ZtmUI: {}".format(response_registers))

                    # Update last successful time.
                    self.__last_sync = time.time()

            else:
                # self.__logger.error("HTTP Error code: {}".format(response.status_code))
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

    def heart_beat(self):

        # settings = self.get_settings()

        self.__heart_beat_timer.update()

        if self.__heart_beat_timer.expired:
            self.__heart_beat_timer.clear()

            ztm_last_sync = time.time()

            data = [
                {'parameter_name': 'ztm_last_sync', 'parameter_value': ztm_last_sync, 'bgerp_sync': 0}, # Last update time.
                {'parameter_name': 'python_version', 'parameter_value': str(sys.version), 'bgerp_sync': 0}  # Python version.
                ]
            
            self.set_settings(data)

#endregion
