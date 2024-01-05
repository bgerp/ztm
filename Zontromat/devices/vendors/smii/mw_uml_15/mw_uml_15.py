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

class MW_UML_15(ModbusDevice):
    """This class is dedicated to read data from MU-UML-15 flow meter."""

#region Constructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "SMII"

        self._model = "MW-UML-15"

        self._parameters.append(
            Parameter("CumulativeTraffic", "mL",\
            ParameterType.UINT32_T_LE, [0x207, 0x208], FunctionCode.ReadHoldingRegisters))

        self._parameters.append(
            Parameter("InstantaneousFlow", "mL/h",\
            ParameterType.UINT32_T_LE, [0x206, 0x207], FunctionCode.ReadHoldingRegisters))

        self._parameters.append(
            Parameter("WaterTemperature", "0.01",\
            ParameterType.UINT16_T_LE, [0x20B], FunctionCode.ReadHoldingRegisters))

        self._parameters.append(
            Parameter("BatteryVoltage", "0.1",\
            ParameterType.UINT16_T_LE, [0x80C], FunctionCode.ReadHoldingRegisters))

    # ===== Settings =====
    # 40001: ["Seconds", 2, PT.UINT16_T_LE, "", None, FC.WriteSingleRegister, [0x000, 0x001]],
    # 40002: ["Minute", 2, PT.UINT16_T_LE, "", None, FC.WriteSingleRegister, [0x000, 0x002]],
    # 40003: ["Hour", 2, PT.UINT16_T_LE, "", None, FC.WriteSingleRegister, [0x000, 0x003]],
    # 40004: ["Day", 2, PT.UINT16_T_LE, "", None, FC.WriteSingleRegister, [0x000, 0x004]],
    # 40005: ["Month", 2, PT.UINT16_T_LE, "", None, FC.WriteSingleRegister, [0x000, 0x005]],
    # 40006: ["Hears", 2, PT.UINT16_T_LE, "", None, FC.WriteSingleRegister, [0x000, 0x006]],

    # 40512: ["Reverse traffic", 4, PT.UINT32_T_LE, "Unit: mL (according to the customer's own needs to read the data to choose mL or 0.1L)", FC.ReadHoldingRegisters, None, [0x00, 0x200]],

    # 40514: ["Reverse traffic", 4, PT.FLOAT, "Unit: mL (according to the customer's own needs to read the data to choose mL or 0.1L)", FC.ReadHoldingRegisters, None, [0x00, 0x202]],

    # 40516: ["Cumulative traffic", 4, PT.UINT32_T_LE, "Unit mL (according to the customer's own needs to read the data to choose mL or 0.1L)", FC.ReadHoldingRegisters, None, [0x000, 0x204]],

    # 40518: ["Cumulative traffic", 4, PT.FLOAT, "Unit: mL (according to the customer's own needs to read the data to choose mL or 0.1L)", FC.ReadHoldingRegisters, None, [0x000, 0x206]],

    # 40520: ["Instrument status word", 2, PT.UINT16_T_LE, "Bitwise parsing", FC.ReadHoldingRegisters, None, [0x000, 0x208]],

    # 40521: ["Instantaneous flow", 4, PT.UINT32_T_LE, "Unit： 1 mL/h", FC.ReadHoldingRegisters, None, [0x000, 0x209]],
    # # 40001: ["The Low 16 bits of the instantaneous flow", 2, PT.UINT16_T_LE, "Unit： 1 mL/h", FC.ReadHoldingRegisters, None, 0x000, 0x20A],

    # 40523: ["Current water meter temperature", 2, PT.UINT16_T_LE, "Unit: 0.01", FC.ReadHoldingRegisters, None, [0x000, 0x20B]],

    # 40524: ["Date", 12, PT.ARRAY, "Date and time", FC.ReadHoldingRegisters, None, [0x000, 0x20C]],
    # # 40524: ["Seconds", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x20C]],
    # # 40525: ["Minute", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x20D]],
    # # 40526: ["Hour", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x20E]],
    # # 40527: ["Day", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x20F]],
    # # 40528: ["Month", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x210]],
    # # 40529: ["Hears", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x211]],

    # 40530: ["The battery voltage", 2, PT.UINT16_T_LE, "0.01V", FC.ReadHoldingRegisters, None, [0x000, 0x212]],

    # 40540: ["Additional status word", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x213]],

    # 40541: ["Water meter address", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x214]],

    # 40542: ["Program version number 1", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x215]],

    # 40543: ["Program version No. 2", 2, PT.UINT16_T_LE, "", FC.ReadHoldingRegisters, None, [0x000, 0x216]],

    # 42048: ["Reverse traffic", 4, PT.FLOAT, "Unit: 0.1L", FC.ReadHoldingRegisters, None, [0x000, 0x800]],
    # # 40001: ["The Low 16 bits of reverse traffic", 2, PT.UINT16_T_LE, "Unit: 0.1L", FC.ReadHoldingRegisters, None, 0x000, 0x801],

    # 42050: ["Accumulated traffic", 4, PT.FLOAT, "Unit: 0.1L", FC.ReadHoldingRegisters, None, [0x000, 0x802]],
    # # 40001: ["The Low 16 bits of accumulated traffic", 2, PT.UINT16_T_LE, "Unit: 0.1L", FC.ReadHoldingRegisters, None, 0x000, 0x803],

    # 42052: ["Instrument status word", 2, PT.UINT16_T_LE, "Bitwise parsing", FC.ReadHoldingRegisters, None, [0x000, 0x804]],
    # 42053: ["Instantaneous flow", 2, PT.UINT16_T_LE, "Unit: 1L/h", FC.ReadHoldingRegisters, None, [0x000, 0x805]],
    # 42054: ["Current water meter temperature", 2, PT.UINT16_T_LE, "Unit: 0.01", FC.ReadHoldingRegisters, None, [0x000, 0x806]],
    # 42055: ["Minutes and hours", 2, PT.UINT16_T_LE, "Minutes and hours each occupy a byte", FC.ReadHoldingRegisters, None, [0x000, 0x807]],
    # 42056: ["Day and month", 4, PT.UINT16_T_LE, "Day and month are one byte each", FC.ReadHoldingRegisters, None, [0x000, 0x808]],
    # 42057: ["years", 2, PT.UINT16_T_LE, "Day and month are one byte each", FC.ReadHoldingRegisters, None, [0x000, 0x809]],
    # 42058: ["Accumulated working time", 4, PT.UINT32_T_BE, "", FC.ReadHoldingRegisters, None, [0x000, 0x80A]],
    # 42060: ["Battery voltage", 2, PT.UINT16_T_LE, "0.01V", FC.ReadHoldingRegisters, None, [0x000, 0x80C]],
    # 42061: ["Additional status word", 2, PT.UINT16_T_LE, "Bitwise parsing", FC.ReadHoldingRegisters, None, [0x000, 0x80D]],
    # 42062: ["Water meter address", 2, PT.UINT16_T_LE, "int", FC.ReadHoldingRegisters, None, [0x000, 0x80E]],
    # 42063: ["Program version number 1", 2, PT.UINT16_T_LE, "int", FC.ReadHoldingRegisters, None, [0x000, 0x80F]],
    # 42064: ["Program version No. 2", 2, PT.UINT16_T_LE, "int", FC.ReadHoldingRegisters, None, [0x000, 0x810]],

#endregion

    def get_liters(self):
        return self.get_value("CumulativeTraffic")
