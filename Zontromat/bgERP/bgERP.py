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

import json
import time
import traceback

import requests

from utils.logger import get_logger

from bgERP.session import Session

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
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

class bgERP():
    """bgERP service communicator"""

#region Attributes

    __host = ""
    """Base URI."""

    __api_login = "/ztm/register" # /bcvt.eu/ztm/Ztm/login
    """Login API call."""

    __api_sync = "/ztm/sync" # /bcvt.eu/ztm/Ztm/sync
    """Notify bgERP about the zone state API call."""

    __timeout = 5
    """Communication timeout."""

    __logger = None
    """Logger"""

    __session = None
    """Session control."""

    __instance = None
    """Singelton instance."""

    __last_sync = 0
    """Last sync time."""

    __erp_id = None
    """ERP identification."""

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
            host_no_slash = host_no_slash.replace(".*/","")

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
    def erp_id(self):
        """ERP identity.

        Returns
        -------
        mix
            ERP identity.
        """

        return self.__erp_id

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

    def __init__(self, host="http://127.0.0.1", timeout=5):
        """Constructor

        Parameters
        ----------
        host : str
            URI of the service.
        timeout : int
            Connection timeout.
        """

        self.host = host
        self.timeout = timeout
        self.__logger = get_logger(__name__)
        self.__session = Session()

#endregion

#region Public Methods

    def login(self, credentials):
        """Log in to the service.

        Parameters
        ----------
        credentials : mixed
            Credentials of the device for the service.

        Returns
        -------
        bool
            Success
        """

        login_state = False

        uri = self.host + self.__api_login

        # self.__logger.info("LOGIN; To bgERP: {}".format(credentials))

        try:
            response = requests.post(uri, data=credentials, timeout=self.timeout)

            if response is not None:

                # Take new login session key.
                if response.status_code == 200:
                    data = response.json()
                    if data is not None:

                        response_data = json.loads(response.text)

                        # self.__logger.info("LOGIN; From bgERP: {}".format(response_data))

                        # Authorization token.
                        if "token" in data:
                            self.__session.save(data["token"])
                            self.__session.load()
                            login_state = self.__session.session != ""

                        # ERP identity.
                        if "bgerp_id" in data:
                            self.__erp_id = data["bgerp_id"]

                # Use saved session key.
                elif response.status_code == 423:
                    self.__session.load()
                    login_state = self.__session.session != ""
                    self.__erp_id = credentials["bgerp_id"]

                # Not authorized.
                elif response.status_code == 403:
                    login_state = False

                else:
                    self.__logger.error("HTTP Error code: {}".format(response.status_code))
                    login_state = False

        except Exception as e:
            self.__logger.error(traceback.format_exc())
            login_state = False

        return login_state

    def sync(self, registers):
        """Update zone registers.

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
        uri = self.host + self.__api_sync

        # Convert to JSON.
        str_registers = json.dumps(registers).replace("\'", "\"")

        # Payload
        payload = {"token": self.__session.session, "registers": str_registers, "last_sync": self.__last_sync } 

        # self.__logger.info("SYNC; To bgERP: {}".format(payload))

        # Headers
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # The request.
        response = requests.post(uri, headers=headers, data=payload, timeout=self.timeout)

        if response is not None:

            # OK
            if response.status_code == 200:

                if response.text != "":
 
                    # TODO: Test is ti JSON.
                    response_registers = json.loads(response.text)

                    # self.__logger.info("SYNC; From bgERP: {}".format(response_registers))

                    # Update last successful time.
                    self.__last_sync = time.time()

            else:
                self.__logger.error("HTTP Error code: {}".format(response.status_code))
                response_registers = False

        else:
            response_registers = None

        return response_registers

#endregion

#region Public Static Methods

    @staticmethod
    def get_instance(host=None, timeout=None):
        """Singelton instance."""

        instance = None

        if host is not None and timeout is not None:
            bgERP.__instance = bgERP(host=host, timeout=timeout)

        if bgERP.__instance is not None:
            instance = bgERP.__instance

        return instance

#endregion
