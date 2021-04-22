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

from devices.drivers.modbus.device import Device
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.register_type import RegisterType

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

class XYMD02(Device):
    """This class is dedicated to read data from XY-MD02 high precision humidity and temperature sensor.

    See: http://sahel.rs/media/sah/techdocs/xy-md02-manual.pdf"""

#region Constructor

    def __init__(self):
        """Constructor"""

        self._parameters.append(
            Parameter("Temperature", "C",\
            ParameterType.INT16_T, [0x0001], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Humidity", "Rh%",\
            ParameterType.INT16_T, [0x0002], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("GetDeviceAddress", "Enum",\
            ParameterType.INT16_T, [0x0101], RegisterType.ReadHoldingRegisters))

        self._parameters.append(\
            Parameter("GetBaudRate", "Enum",\
            ParameterType.INT16_T, [0x0102], RegisterType.ReadHoldingRegisters))

        self._parameters.append(\
            Parameter("GetTemperatureCorrection", "C",\
            ParameterType.INT16_T, [0x0103], RegisterType.ReadHoldingRegisters))

        self._parameters.append(\
            Parameter("GetHumidityCorrection", "Rh%",\
            ParameterType.INT16_T, [0x0104], RegisterType.ReadHoldingRegisters))

        self._parameters.append(\
            Parameter("SetDeviceAddress", "Enum",\
            ParameterType.INT16_T, [0x0101], RegisterType.WriteSingleHoldingRegister))

        self._parameters.append(\
            Parameter("SetBaudRate", "Enum",\
            ParameterType.INT16_T, [0x0102], RegisterType.WriteSingleHoldingRegister))

        self._parameters.append(\
            Parameter("SetTemperatureCorrection", "C",\
            ParameterType.INT16_T, [0x0103], RegisterType.WriteSingleHoldingRegister))

        self._parameters.append(\
            Parameter("SetHumidityCorrection", "Rh%",\
            ParameterType.INT16_T, [0x0104], RegisterType.WriteSingleHoldingRegister))

#endregion