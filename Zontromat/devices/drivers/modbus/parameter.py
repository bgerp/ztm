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

class Parameter:
    """Modbus parameter descriptor."""

#region Atributes

    __parameter_name = "Parameter"
    """Parameter name."""

    __mou = "Unit"
    """Measure of unit."""

    __data_type = ""
    """Data type."""

    __adresses = []
    """Modbus addresses."""

    __register_type = ""
    """Register type."""

#endregion

#region Getters and Setters

    @property
    def parameter_name(self):
        """Parameter name."""

        return self.__parameter_name

    @parameter_name.setter
    def parameter_name(self, parameter_name):
        """Parameter name.

        Args:
            parameter_name (string): Parameter name.
        """
        self.__parameter_name = parameter_name

    @property
    def mou(self):
        """Unit of measurement."""

        return self.__mou

    @mou.setter
    def mou(self, mou):
        """Unit of measurement.

        Args:
            mou (string): Unit of measurement.
        """

        self.__mou = mou

    @property
    def data_type(self):
        """Data type

        Return:
            adresses (list): Data type.
        """
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        """Data type

        Args:
            data_type (string): Data type.
        """

        self.__data_type = data_type

    @property
    def adresses(self):
        """Adresses

        Return:
            adresses (list): Adresses.
        """

        return self.__adresses

    @adresses.setter
    def adresses(self, adresses):
        """Adresses

        Args:
            adresses (list): Adresses.
        """

        self.__adresses = adresses

    @property
    def register_type(self):
        """Register type."""

        return self.__register_type

    @register_type.setter
    def register_type(self, register_type):
        """Register type.

        Args:
            register_type (string): Register type.
        """

        self.__register_type = register_type

#endregion

#region Constructor

    def __init__(self, parameter_name, mou, data_type, adresses, register_type):
        """Constructor

        Args:
            parameter_name (string): Parameter name..
            mou (string): Measure of unit.
            data_type (string): Data type.
            adresses (list): Modbus addresses.
            register_type (string)
        """

        self.parameter_name = parameter_name
        self.mou = mou
        self.data_type = data_type
        self.adresses = adresses
        self.register_type = register_type

#endregion
