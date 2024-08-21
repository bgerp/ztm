#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import os
import configparser
import time

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

class ApplicationSettings:
    """Application settings class."""

#region Attributes

    __file_name = ""
    """File name"""

    __instance = None
    """Singelton instance object."""

    __config = None
    """Actual settings."""

#endregion

#region Properties

    @property
    def exists(self):
        """Does the the settings file exists.

        Returns
        -------
        bool
            File exists.
        """

        return os.path.exists(self.__file_name)

    @property
    def debug_level(self):
        """Debug level.

        Returns
        -------
        int
            Debug level.
        """

        value = 0

        if self.__config is not None:
            if "APPLICATION" in self.__config:
                value = self.__config["APPLICATION"]["debug_level"]
                value = int(value)

        return value

    @property
    def controller(self):
        """Host name of the Neuron.

        Returns
        -------
        str
            Host name of the Neuron.
        """
        return self.__config["CONTROLLER"]

    @property
    def erp_service(self):
        """ERP service domain.

        Returns
        -------
        str
            ERP service domain.
        """

        return self.__config["ERP_SERVICE"]

    @property
    def path(self):
        """File name with settings.
        """

        return self.__file_name

    @property
    def current_version(self):
        """Get the current version.

        Returns:
            dict: Current version dictionary.
        """

        current_version = dict(self.__config["CURRENT_VERSION"])
        # for k in d:
        #     d[k] = dict(self._defaults, **d[k])
        #     d[k].pop('__name__', None)

        return current_version

    @property
    def ui(self):
        """Zontromt UI.

        Returns:
            dict: Current version dictionary.
        """

        return self.__config["UI"]

    @current_version.setter
    def current_version(self, value):
        """Set the current version.
        """

        self.__config["CURRENT_VERSION"] = value

#endregion

#region Constructor

    def __init__(self, file_name=None):
        """Constructor

        Args:
            file_name (str, optional): File name.. Defaults to None.

        Raises:
            Exception: This class is a singleton!
        """

        if ApplicationSettings.__instance is not None:
            raise Exception("This class is a singleton!")

        ApplicationSettings.__instance = self

        self.__file_name = ""

        if file_name is None:

            # Current file path. & Go to file.
            cwf = os.path.dirname(os.path.abspath(__file__))
            self.__file_name = os.path.join(cwf, "..", "..", "settings.ini")

            self.__config = configparser.ConfigParser()
            self.read()

        else:
            self.__file_name = file_name

#endregion

#region Public Methods

    def read(self):
        """Read INI file."""

        if self.exists:
            self.__config.read(self.__file_name)

    def save(self):
        """Read INI file."""

        if self.exists:
            with open(self.__file_name, "w") as stream:
                self.__config.write(stream)
                stream.close()

    def create_default(self):
        """Create default settings.
        """

        # default debug level.
        if self.__config is not None:
            if "APPLICATION" not in self.__config:
                self.__config["APPLICATION"] = {"debug_level": 20}

        # Default controller.
        if self.__config is not None:
            if "CONTROLLER" not in self.__config:
                self.__config["CONTROLLER"] = {
                    "vendor": "zuljana",
                    "model": "zl101pcc",
                    "interface_0":"TCP",
                    "timeout_0": 1.0,
                    "rtu_port_0": "/dev/ttyUSB0",
                    "rtu_baudrate_0": 9600,
                    "rtu_cfg_0": "8N1",
                    "rtu_unit_0": 2,
                    "tcp_address_0":"127.0.0.1",
                    "tcp_port_0":"5030",
                    "interface_1":"TCP",
                    "timeout_1": 1.0,
                    "rtu_port_1": "/dev/ttyS0",
                    "rtu_baudrate_1": 9600,
                    "rtu_cfg_1": "8N1",
                    "tcp_address_1":"127.0.0.1",
                    "tcp_port_1":"5040",
                }

        # # Default software version as current version.
        if self.__config is not None:
            if "CURRENT_VERSION" not in self.__config:
                self.__config["CURRENT_VERSION"] = {
                    "repo":"http://github.com/bgerp/ztm/",
                    "branch":"master",
                    "commit":"e0c1dda"
                }

        # This will be added by the setup script.
        # # Default ERP service.
        if self.__config is not None:
            if "ERP_SERVICE" not in self.__config:
                self.__config["ERP_SERVICE"] = {
                    "enabled": True,
                    "config_time": int(time.time()),
                    # "erp_id": "0082-4140-0042-4216",
                    # "host": "https://test.bcvt.eu/",
                    "erp_id": "0091-7140-2539-6010",
                    "host": "https://bcvt.eu/",
                    "timeout": 5,
                    "update_rate": 60,
                    "serial_number": 0
                    }

        # This will be added by the setup script.
        # # Default UI service.
        if self.__config is not None:
            if "UI" not in self.__config:
                self.__config["UI"] = {
                    "enabled": "True",
                    "host": "http://localhost",
                    "email": "zontromat@bcvt.eu",
                    "password": "Zontromat010203",
                    "timeout": 5,
                    }

        if not self.exists:
            with open(self.__file_name, "w") as stream:
                self.__config.write(stream)
                stream.close()

#endregion

#region Static Methods

    @staticmethod
    def get_instance(file_path=None):
        """Singelton instance."""

        if ApplicationSettings.__instance is None:
            ApplicationSettings(file_path)

        return ApplicationSettings.__instance

#endregion
