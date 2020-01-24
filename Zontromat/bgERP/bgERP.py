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

    __api_login = "/api/v1/zone/login" # /bcvt.eu/ztm/Ztm/login
    """Login API call."""

    __api_sync = "/api/v1/zone/sync" # /bcvt.eu/ztm/Ztm/sync
    """Notify bgERP about the zone state API call."""

    __timeout = 5
    """Communication timeout."""

    __logger = None
    """Logger"""

    __session = None
    """Session control."""

    __instance = None
    """Singelton instance."""

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
        self.__host = host

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

        # TODO: bgERP ID to authorize the building.

        login_state = False

        uri = self.host + self.__api_login
        response = requests.post(uri, data=credentials, timeout=self.timeout)

        if response is not None:

            if response.status_code == 200:
                data = response.json()
                if data is not None:
                    if "session_id" in data:
                        self.__session.save(data["session_id"])
                        self.__session.load()
                        login_state = self.__session.session != ""

            elif response.status_code == 403:
                login_state = False

            elif response.status_code == 423:
                self.__session.load()
                login_state = self.__session.session != ""

            else:
                login_state = False

        return login_state

    def sync(self, regs):
        """Update zone regs.

        Parameters
        ----------
        regs : mixed
            Room regs.

        Returns
        -------
        bool
            Success
        """

        # global STATE
        # # self.__logger.debug(regs)
        # json_state_data = json.loads(STATE)
        # return json_state_data

        registers = None

        uri = self.host + self.__api_sync
        payload = {"session_id": self.__session.session, "regs": regs}
        response = requests.post(uri, data=payload, timeout=self.timeout)

        if response is not None:

            if response.status_code == 200:
                if response.text != "":
                    registers = json.loads(response.text)

            elif response.status_code == 403:
                registers = None

            elif response.status_code == 429:
                registers = None

            else:
                registers = None
        else:
            registers = None

        return registers

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
