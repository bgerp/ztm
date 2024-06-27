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

from enum import Enum

from utils.logger import get_logger

from devices.base_device import BaseDevice

from devices.drivers.modbus.device import ModbusDevice
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.function_code import FunctionCode

# (Request from mail: Eml6429)

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

class HP_40STD_N420WHSB4(ModbusDevice):
    """Heat pump description. (40STD-N420WHSB4)
    """

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """
        super().__init__(config)

        self._vendor = "HstarsGuangzhouRefrigeratingEquipmentGroup"
        """Hstars Guangzhou Refrigerating Equipment Group.Co.,Ltd
        """        

        self._model = "40STD-N420WHSB4"

        self.__valid_modes = [1,2,3,4,5]

#region Start /Stop
        self._parameters.append(
            Parameter(
                "Start",
                "Enum",
                ParameterType.INT16_T_LE,
                [0],
                FunctionCode.WriteSingleCoil,
                [0x0000, 0xFF00]
            )
        )

        self._parameters.append(
            Parameter(
                "Stop",
                "Enum",
                ParameterType.INT16_T_LE,
                [1],
                FunctionCode.WriteSingleCoil,
                [0x0000, 0xFF00]
            )
        )
#endregion

#region Operation Status
        self._parameters.append(
            Parameter(
                "OperatingStatus",
                "Enum",
                ParameterType.INT16_T_LE,
                [5],
                FunctionCode.ReadInputRegisters,
                [0, 2]
            )
        )
#endregion

#region Operation Mode
        self._parameters.append(
            Parameter(
                "GetMode",
                "Enum",
                ParameterType.INT16_T_LE,
                [0],
                FunctionCode.ReadHoldingRegisters,
                [1, 5]
            )
        )

        self._parameters.append(
            Parameter(
                "SetMode",
                "Enum",
                ParameterType.INT16_T_LE,
                [0],
                FunctionCode.WriteSingleHoldingRegister,
                [1, 5]
            )
        )
#endregion

#region Cooling Set Temperature
        self._parameters.append(
            Parameter(
                "GetCoolingSetTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [1],
                FunctionCode.ReadHoldingRegisters,
                []
            )
        )

        self._parameters.append(
            Parameter(
                "SetCoolingSetTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [1],
                FunctionCode.WriteSingleHoldingRegister,
                []
            )
        )
#endregion

#region Heating Set Temperature
        self._parameters.append(
            Parameter(
                "GetHeatingSetTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [2],
                FunctionCode.ReadHoldingRegisters,
                []
            )
        )

        self._parameters.append(
            Parameter(
                "SetHeatingSetTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [2],
                FunctionCode.WriteSingleHoldingRegister,
                []
            )
        )
#endregion

#region System evaporation return water temperature

        self._parameters.append(
            Parameter(
                "GetSystemEvaporationReturnWaterTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [0x20],
                FunctionCode.ReadInputRegisters,
                []
            )
        )

#endregion

#region System evaporation temperature

        self._parameters.append(
            Parameter(
                "GetSystemEvaporationWaterTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [0x21],
                FunctionCode.ReadInputRegisters,
                []
            )
        )

#endregion

#region System condensate return water temperature

        self._parameters.append(
            Parameter(
                "GetSystemCondensateReturnWaterTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [0x22],
                FunctionCode.ReadInputRegisters,
                []
            )
        )

#endregion

#region System condensate water temperature

        self._parameters.append(
            Parameter(
                "GetSystemCondensateWaterTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [0x23],
                FunctionCode.ReadInputRegisters,
                []
            )
        )

#endregion

#region Ambient temperature

        self._parameters.append(
            Parameter(
                "GetAmbientTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [0x24],
                FunctionCode.ReadInputRegisters,
                []
            )
        )

#endregion

#region Hot water temperature

        self._parameters.append(
            Parameter(
                "GetHotWaterTemperature",
                "C",
                ParameterType.INT16_T_LE,
                [0x26],
                FunctionCode.ReadInputRegisters,
                []
            )
        )

#endregion

    def __del__(self):
        """Destructor
        """

        super().__del__()

#endregion

    def set_mode(self, mode):
        """Set heat pump mode.

        Args:
            mode (HeatPumpMode): Heat pump mode.
        """

        if mode in self.__valid_modes:
            try:
                request = self.generate_request("SetMode", SetMode=int(mode))
                response = self._controller.execute_mb_request(request, self._uart)
                if response is not None:
                    if not response.isError():
                        pass
                        # value = response.registers[0] / 10

            except Exception:
                pass

    def get_mode(self):
        """Get heat pump mode.

        Returns:
            int: Heat pump mode. [1 to 5]
        """

        return self.get_value("GetMode")

#endregion
