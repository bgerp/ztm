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

from devices.drivers.modbus.function_code import FunctionCode
from devices.drivers.modbus.parameter_type import ParameterType

class Parameter:
    """Modbus parameter descriptor."""

#region Attributes

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
            addresses (list): Data type.
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
    def addresses(self):
        """addresses

        Return:
            addresses (list): addresses.
        """

        return self.__addresses

    @addresses.setter
    def addresses(self, addresses):
        """addresses

        Args:
            addresses (list): addresses.
        """

        self.__addresses = addresses

    @property
    def function_code(self):
        """Register type."""

        return self.__function_code

    @function_code.setter
    def function_code(self, function_code):
        """Register type.

        Args:
            function_code (string): Register type.
        """

        self.__function_code = function_code

    @property
    def limits(self):
        """Limits"""

        return self.__limits

    @limits.setter
    def limits(self, limits):
        """Limits

        Args:
            limits (list): Limits values.
        """

        self.__limits = limits

#endregion

#region Constructor

    def __init__(self, parameter_name: str, mou: str, data_type: ParameterType, addresses: [], function_code: FunctionCode, limits=[0, 100]):
        """Constructor

        Args:
            parameter_name (string): Parameter name..
            mou (string): Measure of unit.
            data_type (string): Data type.
            addresses (list): Modbus addresses.
            function_code (string)
        """

        self.parameter_name = parameter_name
        """Parameter name.
        """

        self.mou = mou
        """Measure of unit.
        """

        self.data_type = data_type
        """Data type.
        """

        self.addresses = addresses
        """Modbus addresses.
        """

        self.function_code = function_code
        """Register type.
        """

        self.limits = limits
        """Limits.
        """

#endregion
