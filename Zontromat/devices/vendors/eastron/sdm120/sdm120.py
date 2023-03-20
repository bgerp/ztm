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

class SDM120(ModbusDevice):
    """This class is dedicated to read data from SDM120 energy meter.

    See: https://www.eastroneurope.com/images/uploads/products/protocol/SDM120-MODBUS_Protocol.pdf"""

#region Constructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "Eastron"

        self._model = "SDM120"

        self._parameters.append(
            Parameter("Voltage", "V",\
            ParameterType.FLOAT, [0, 1], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Current", "A",\
            ParameterType.FLOAT, [6, 7], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ActivePower", "W",\
            ParameterType.FLOAT, [12, 13], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ApparentPower", "VA",\
            ParameterType.FLOAT, [18, 19], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ReactivePower", "VAr",\
            ParameterType.FLOAT, [24, 25], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("PowerFactor", "DEG",\
            ParameterType.FLOAT, [30, 31], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Frequency", "Hz",\
            ParameterType.FLOAT, [70, 71], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ImportActiveEnergy", "kWr",\
            ParameterType.FLOAT, [72, 73], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ExportActiveEnergy", "kWr",\
            ParameterType.FLOAT, [74, 75], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ImportReactiveEnergy", "kvarh",\
            ParameterType.FLOAT, [76, 77], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ExportReactiveEnergy", "kvarh",\
            ParameterType.FLOAT, [78, 79], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemPowerDemand", "W",\
            ParameterType.FLOAT, [84, 85], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumTotalSystemPowerDemand", "W",\
            ParameterType.FLOAT, [86, 87], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ImportSystemPowerDemand", "W",\
            ParameterType.FLOAT, [88, 89], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumImportSystemPowerDemand", "W",\
            ParameterType.FLOAT, [90, 91], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("ExportSystemPowerDemand", "W",\
            ParameterType.FLOAT, [92, 93], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumExportSystemPowerDemand", "W",\
            ParameterType.FLOAT, [94, 95], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("CurrentDemand", "A",\
            ParameterType.FLOAT, [258, 259], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumCurrentDemand", "A",\
            ParameterType.FLOAT, [264, 265], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalActiveEnergy", "kWh",\
            ParameterType.FLOAT, [342, 343], FunctionCode.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalReactiveEnergy", "kVArh",\
            ParameterType.FLOAT, [344, 345], FunctionCode.ReadInputRegisters))

#endregion
