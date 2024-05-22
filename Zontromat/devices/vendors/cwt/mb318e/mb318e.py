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

class MB318E(ModbusDevice):
    """This class is dedicated to read analog inputs and thermo couples data from MB318E expander.

     - See: https://store.comwintop.com/products/cwt-mb318e-12pt-4ai-rs485-rs232-ethernet-modbus-rtu-tcp-io-acquisition-module
    """

#region Constructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "COMWINTOP"

        self._model = "MB318E"

        if "chanel" in config:
            self._chanel = config["chanel"]

        self._parameters.append(
            Parameter(
                "Temperature",
                "DegC",
                ParameterType.INT16_T_LE,
                [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62],
                FunctionCode.ReadHoldingRegisters,
                [-200, 200]
            )
        )

        self._parameters.append(
            Parameter(
                "GetAnalogInputs",
                "Registers",
                ParameterType.INT16_T_LE,
                [63, 64, 65, 66],
                FunctionCode.ReadHoldingRegisters,
                [0, 10216]
            )
        )

#endregion

#region Public Methods

    def get_temp(self):
        """Get temperature.

        Returns:
            float: Value of the temperature.
        """

        value = self.get_value("Temperature")

        if value is not None:
            value = value[self._chanel] # TODO: Do the math.

        return value

#endregion
