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

from utils.logger import get_logger

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

class FlowmeterDN20(ModbusDevice):
    """Flowmeter input device Flowmeter DN20."""

#region Attributes

    __logger = None
    """Logger
    """

    __uart = 0
    """UART index.
    """

    __mb_id = 0
    """Modbus ID
    """

    __example_settings = {
        "vendor": "mainone",
        "model": "flowmeter_dn20",
        "options":
        {
            "uart": 1,
            "mb_id": 3,
        }
    }

#endregion

#region Properties

#endregion

#region Constructor

    def __init__(self, **config):

        super().__init__(config)

        self._vendor = "Mainone"

        self._model = "FlowmeterDN20"

        self._parameters.append(
            Parameter("PositiveCumulativeEnergy", "KW/h",\
            ParameterType.UINT32_T_BE, [0x204, 0x205], FunctionCode.ReadHoldingRegisters))

        # self._parameters.append(
        #     Parameter("InstantaneousFlow", "mL/h",\
        #     ParameterType.UINT32_T_LE, [0x206, 0x207], FunctionCode.ReadHoldingRegisters))

        # self._parameters.append(
        #     Parameter("WaterTemperature", "0.01",\
        #     ParameterType.UINT16_T_LE, [0x20B], FunctionCode.ReadHoldingRegisters))

        # self._parameters.append(
        #     Parameter("BatteryVoltage", "0.1",\
        #     ParameterType.UINT16_T_LE, [0x80C], FunctionCode.ReadHoldingRegisters))

    # # ===== Settings =====
    # 40001: ["Positive cumulative energy",                     4, PT.UINT32_T_BE, "KW/h",            FC.ReadHoldingRegisters, None, [0x00, 0x00]],
    # 40005: ["Inlet temperature",                              4, PT.UINT32_T_BE, "⁰C",              FC.ReadHoldingRegisters, None, [0x00, 0x04]],
    # 40007: ["Return water temperature",                       4, PT.UINT32_T_BE, "⁰C",              FC.ReadHoldingRegisters, None, [0x00, 0x06]],

#endregion

#region Public Methods

    def get_pcenergy(self):
        return self.get_value("PositiveCumulativeEnergy")

    def get_temp(self):
        """Get temperature.

        Returns:
            float: Value of the temperature.
        """

        return 20.0

#endregion
