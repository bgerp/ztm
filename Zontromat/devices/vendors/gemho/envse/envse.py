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

from devices.drivers.modbus.device import ModbusDevice
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.function_code import FunctionCode

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

class Envse(ModbusDevice):
    """This class is dedicated to read data from environment sensor flow meter."""

#region Constructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "Gemho"

        self._model = "Envse"

        self.__set_registers()

#endregion

#region Private Methods

    def __set_registers(self):

        self._parameters.append(
            Parameter("Temperature", "ºC",\
            ParameterType.UINT16_T_LE, [0], FunctionCode.ReadHoldingRegisters))

        self._parameters.append(
            Parameter("Humidity", "Rh",\
            ParameterType.UINT16_T_LE, [1], FunctionCode.ReadHoldingRegisters))

        self._parameters.append(
            Parameter("Lux", "Lux",\
            ParameterType.UINT16_T_LE, [2], FunctionCode.ReadHoldingRegisters))

        self._parameters.append(
            Parameter("All", "Any",\
            ParameterType.ARR_UINT16_T_LE, [0, 1, 2], FunctionCode.ReadHoldingRegisters))

#endregion

#region Public Methods

    def update(self):
        """Update the data.
        """
        self._update_timer.update()
        if self._update_timer.expired:
            self._update_timer.clear()

            all_values = self.get_value("All")

            if all_values:
                self._parameters_values["Temperature"] = all_values[0] / 10.0
                self._parameters_values["Humidity"] = all_values[1] / 10.0
                self._parameters_values["Lux"] = all_values[2]

    def get_temp(self):
        """Get temperature.

        Returns:
            float: Value of the temperature.
        """
        value = None

        if "Temperature" in self._parameters_values:
            value = self._parameters_values["Temperature"]

        return value

    def get_hum(self):
        """Get humidity.

        Returns:
            float: Value of the humidity.
        """
        value = None

        if "Humidity" in self._parameters_values:
            value = self._parameters_values["Humidity"]

        return value

    def get_lux(self):
        value = None

        if "Lux" in self._parameters_values:
            value = self._parameters_values["Lux"]

        return value

#endregion
