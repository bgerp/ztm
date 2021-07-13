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

class AHUModular(ModbusDevice):
    """This class is dedicated to read/write data from Tangra AHU Modular.

    See: https://www.tangra.bg/products_EN_86_232_1.html"""

#region Constructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "Tangra"

        self._model = "AHU_Modular"

        self._parameters.append(
            Parameter(
                "GlobalAlarm",
                "Bits",
                ParameterType.UINT16_T,
                [0],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "RotaryREC_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [5],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "PreHeater_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [6],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "EF_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [7],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "Heater_Supply_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [8],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "PJR_Baypas_Rec_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [9],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "PJR_In_Out_FreshAir_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [10],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "PJR_Recirculation_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [11],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "SF_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [12],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "ReadMode",
                "State", # 0->Stop, 1->Cool, 2->Heat, 3->Fan, 4->Auto, 5->Dry
                ParameterType.UINT16_T,
                [0],
                RegisterType.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SP",
                "degC", # TODO: Give possible values.
                ParameterType.UINT16_T,
                [1],
                RegisterType.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "FreshAir",
                "State", # 0..10->Manual (0..100%), 11->Auto,
                ParameterType.UINT16_T,
                [2],
                RegisterType.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "StateSpeedSFEF",
                "State", # How to choice fan speed: 0-Together, 1-Individually
                ParameterType.UINT16_T,
                [3],
                RegisterType.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "ValueSpeedSFEF",
                "State", # 0..10->Manual (0..100%), 11->Auto,
                ParameterType.UINT16_T,
                [4],
                RegisterType.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SpeedSF",
                "State", # 0..10->Manual (0..100%), 11->Auto
                ParameterType.UINT16_T,
                [5],
                RegisterType.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SpeedEF",
                "State", # 0..10->Manual (0..100%), 11->Auto
                ParameterType.UINT16_T,
                [6],
                RegisterType.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "UnitStatus",
                "State", # TODO: Give the states,
                ParameterType.UINT16_T,
                [0],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TE1Return", # TODO: What is this type.
                "degC",
                ParameterType.REAL,
                [1],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TE2Exhaust",
                "degC",
                ParameterType.REAL,
                [2],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TS1Ambient",
                "degC",
                ParameterType.REAL,
                [3],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TS4SupplyDEX",
                "",
                ParameterType.REAL,
                [4],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TS3SupplyHeater",
                "",
                ParameterType.REAL,
                [5],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "PreHeaterPower",
                "Percentage",
                ParameterType.UINT16_T,
                [18],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "RotaryRECPower",
                "Percentage",
                ParameterType.UINT16_T,
                [19],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SFPower",
                "Percentage",
                ParameterType.UINT16_T,
                [20],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "EFPower",
                "Percentage",
                ParameterType.UINT16_T,
                [21],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "PJRInOutFreshAirPower",
                "Percentage",
                ParameterType.UINT16_T,
                [22],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "PJRRecirculationPower",
                "Percentage",
                ParameterType.UINT16_T,
                [23],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "PJRBaypasRecPower",
                "Percentage",
                ParameterType.UINT16_T,
                [24],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "HeaterSupplyPower",
                "Percentage",
                ParameterType.UINT16_T,
                [25],
                RegisterType.ReadInputRegisters
            )
        )
    """





Dev_PreHeater_PowerPercent_USINT
Dev_RotaryREC_PowerPercent_USINT
Dev_SF_PowerPercent_USINT
Dev_EF_PowerPercent_USINT
Dev_PJR_In_Out_FreshAir_PowerPercent_USINT
Dev_PJR_Recirculation_PowerPercent_USINT
Dev_PJR_Baypas_Rec_PowerPercent_USINT
Dev_Heater_Supply_PowerPercent_USINT
    """

#endregion
