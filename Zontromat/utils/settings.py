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

import yaml

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

class ApplicationSettings():
    """Application settings class."""

#region Attributes

    __file_name = ""
    """File name"""

    __settings = None
    """Actual settings."""

    __instance = None
    """Singelton instance object."""

#endregion

#region Properties

    @property
    def ram_usage(self):
        """Ram usage flag.

        Returns
        -------
        int
            Enable flag.
        """

        if self.__settings is not None:
            return self.__settings["application"]["ram_usage"]

        return 0

    @property
    def run_time_usage(self):
        """Run time usage.

        Returns
        -------
        int
            Enable flag.
        """

        if self.__settings is not None:
            return self.__settings["application"]["run_time_usage"]

        return 0

    @property
    def debug_level(self):
        """Debug level.

        Returns
        -------
        int
            Debug level.
        """

        if self.__settings is not None:
            return self.__settings["application"]["debug_level"]

        return 0

    @property
    def get_controller(self):
        """Host name of the Neuron..

        Returns
        -------
        str
            Host name of the Neuron.
        """
        return self.__settings["controller"]

    @property
    def get_erp_service(self):
        """Host name of the Neuron..

        Returns
        -------
        str
            Host name of the Neuron.
        """
        return self.__settings["erp_service"]

    @property
    def exists(self):
        """Does the the settings file exists.

        Returns
        -------
        bool
            File exists.
        """

        return os.path.exists(self.__file_name)

#endregion

#region Constructor

    def __init__(self, file_name=None):
        """Constructor

        Parameters
        ----------
        file_name : str
            File name.
        """

        if file_name is None:
            cwd = os.getcwd()
            self.__file_name = os.path.join(cwd, "settings.yaml")

        else:
            self.__file_name = file_name

#endregion

#region Private Methods

    def read(self):
        """Read YAML file."""

        if self.exists:
            with open(self.__file_name, 'r') as stream:
                self.__settings = yaml.safe_load(stream)
                stream.close()

#endregion

#region Static Methods

    @staticmethod
    def get_instance():
        """Singelton instance."""

        if ApplicationSettings.__instance is None:
            ApplicationSettings.__instance = ApplicationSettings()

        return ApplicationSettings.__instance

#endregion
