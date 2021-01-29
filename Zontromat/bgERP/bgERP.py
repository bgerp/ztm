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

from utils.logger import get_logger

from bgERP.client import Client
from bgERP.server import Server

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

class bgERP:
    """bgERP service communicator"""

#region Attributes

    __host = "127.0.0.1"
    """Host
    """

    __timeout = 5
    """Timeout
    """

    __client = None
    """Client instance.
    """

    __server = None
    """Server instance.
    """

    __is_logged = False
    """Is logged in flag.
    """

    __get_registers = None
    """Get register callback.
    """

    __set_registers = None
    """Set register callback.
    """

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
        return self.__client.host

    @host.setter
    def host(self, host):
        """Set Host URL of the service.

        Parameters
        ----------
        host : str
            Host URL of the servie.
        """

        self.__client.host = host

    @property
    def timeout(self):
        """Get timeout.

        Returns
        -------
        int
            Timeout.
        """

        return self.__client.timeout

    @timeout.setter
    def timeout(self, timeout):
        """Set timeout.

        Parameters
        ----------
        timeout : int
            Timeout.
        """

        self.__client.timeout = timeout

    @property
    def erp_id(self):
        """ERP identity.

        Returns
        -------
        mix
            ERP identity.
        """

        return self.__client.erp_id

    @property
    def last_sync(self):
        """Last sync time.

        Returns
        -------
        float
            Unix timestamp.
        """

        return self.__client.last_sync

    @property
    def is_logged(self):
        """Is logged.

        Returns:
            bool: Logged in state.
        """
        return self.__is_logged

#endregion

#region Constructor \ Destructor

    def __init__(self, **kwargs):
        """Constructor
        """

        host = "127.0.0.1"
        if "host" in kwargs:
            host = kwargs.get("host")

        timeout = 5
        if "timeout" in kwargs:
            timeout = kwargs.get("timeout")

        self.__logger = get_logger(__name__)

        self.__client = Client(host=host, timeout=timeout)

        self.__server = Server()
        #self.__server.set_sync_cb(lambda: self.sync({}))

    def __del__(self):
        """Destructor
        """

        if self.__server is not None:
            self.__server.stop()

#endregion

#region Public Methods

    def login(self, **credentials):
        """Log in to the service.

        Args:
            credentials (dict): Credentials of the device for the service.

        Returns:
            bool: Success
        """

        self.__is_logged = self.__client.login(credentials)

        if self.__is_logged:
            if self.__server is not None:
                self.__server.set_registers_cb(
                    get_cb=self.__get_registers,\
                    set_cb=self.__set_registers)
                self.__server.start()

        return self.__is_logged

    def sync(self, registers):
        """Sync the registers.

        Args:
            registers (dict): Registers

        Returns:
            bool: Status of sync.
        """

        return self.__client.sync(registers)

    def set_registers_cb(self, **kwargs):
        """Set callback for get/set registers.
        """

        if "get_cb" in kwargs:
            self.__get_registers = kwargs["get_cb"]

        if "set_cb" in kwargs:
            self.__set_registers = kwargs["set_cb"]

#endregion
