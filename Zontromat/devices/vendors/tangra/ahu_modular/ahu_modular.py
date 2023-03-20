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

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

class AHUModular(ModbusDevice):
    """This class is dedicated to read/write data from Tangra AHU Modular.

    See: https://www.tangra.bg/products_EN_86_232_1.html"""

    __logger = None
    """Logger
    """

#region Constructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "Tangra"

        self._model = "AHU_Modular"

        # Create logger.
        self.__logger = get_logger(__name__)

        self.__set_registers()

#endregion

#region Private Methods

    def __set_registers(self):

        self._parameters.append(
            Parameter(
                "GlobalAlarm",
                "Bits",
                ParameterType.UINT16_T,
                [0],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "RotaryREC_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [5],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "PreHeater_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [6],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "EF_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [7],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "Heater_Supply_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [8],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "PJR_Baypas_Rec_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [9],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "PJR_In_Out_FreshAir_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [10],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "PJR_Recirculation_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [11],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "SF_R_Device",
                "Bits",
                ParameterType.UINT16_T,
                [12],
                FunctionCode.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "GetMode",
                "State", # 0->Stop, 1->Cool, 2->Heat, 3->Fan, 4->Auto, 5->Dry
                ParameterType.UINT16_T,
                [0],
                FunctionCode.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SetMode",
                "State", # 0->Stop, 1->Cool, 2->Heat, 3->Fan, 4->Auto, 5->Dry
                ParameterType.UINT16_T,
                [0],
                FunctionCode.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "GetTemperatureSetpoint",
                "degC", # TODO: Give possible values.
                ParameterType.UINT16_T,
                [1],
                FunctionCode.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SetTemperatureSetpoint",
                "degC", # TODO: Give possible values.
                ParameterType.UINT16_T,
                [1],
                FunctionCode.WriteMultipleHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "FreshAir",
                "State", # 0..10->Manual (0..100%), 11->Auto,
                ParameterType.UINT16_T,
                [2],
                FunctionCode.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "StateSpeedSFEF",
                "State", # How to choice fan speed: 0-Together, 1-Individually
                ParameterType.UINT16_T,
                [3],
                FunctionCode.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "ValueSpeedSFEF",
                "State", # 0..10->Manual (0..100%), 11->Auto,
                ParameterType.UINT16_T,
                [4],
                FunctionCode.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SpeedSF",
                "State", # 0..10->Manual (0..100%), 11->Auto
                ParameterType.UINT16_T,
                [5],
                FunctionCode.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SpeedEF",
                "State", # 0..10->Manual (0..100%), 11->Auto
                ParameterType.UINT16_T,
                [6],
                FunctionCode.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "UnitStatus",
                "State", # TODO: Give the states,
                ParameterType.UINT16_T,
                [0],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TE1Return", # TODO: What is this type.
                "degC",
                ParameterType.REAL,
                [1],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TE2Exhaust",
                "degC",
                ParameterType.REAL,
                [2],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TS1Ambient",
                "degC",
                ParameterType.REAL,
                [3],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TS4SupplyDEX",
                "",
                ParameterType.REAL,
                [4],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "TS3SupplyHeater",
                "",
                ParameterType.REAL,
                [5],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "PreHeaterPower",
                "Percentage",
                ParameterType.UINT16_T,
                [18],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "RotaryRECPower",
                "Percentage",
                ParameterType.UINT16_T,
                [19],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SFPower",
                "Percentage",
                ParameterType.UINT16_T,
                [20],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "EFPower",
                "Percentage",
                ParameterType.UINT16_T,
                [21],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "PJRInOutFreshAirPower",
                "Percentage",
                ParameterType.UINT16_T,
                [22],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "PJRRecirculationPower",
                "Percentage",
                ParameterType.UINT16_T,
                [23],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "PJRBaypasRecPower",
                "Percentage",
                ParameterType.UINT16_T,
                [24],
                FunctionCode.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "HeaterSupplyPower",
                "Percentage",
                ParameterType.UINT16_T,
                [25],
                FunctionCode.ReadInputRegisters
            )
        )

#endregion

#region Public Methods

    def get_alarms(self):
        """Get alarm bit.

        Returns:
            bool: Value of the alarm.
        """

        value = False

        try:
            request = self.generate_request("GlobalAlarm")
            response = self._controller.execute_mb_request(request, self.uart)
            if response is not None:
                if not response.isError():
                    value = response.registers[0] != 0

                else:
                    GlobalErrorHandler.log_hardware_malfunction(
                        self.__logger, "Device: {}; ID: {}; Response error.".format(
                            self.name, request.unit_id))

            else:
                GlobalErrorHandler.log_hardware_malfunction(
                    self.__logger, "Device: {}; ID: {}; Invalid response.".format(
                        self.name, request.unit_id))

        except Exception:
            GlobalErrorHandler.log_hardware_malfunction(
                self.__logger, "Device: {}; ID: {}; Can not read the temperature value.".format(
                    self.name, request.unit_id))

        return value


    def get_status(self):
        """Get status.

        Returns:
            int: Value of the status.
        """

        value = None

        try:
            request = self.generate_request("UnitStatus")
            response = self._controller.execute_mb_request(request, self.uart)
            if response is not None:
                if not response.isError():
                    value = response.registers[0]

                else:
                    GlobalErrorHandler.log_hardware_malfunction(
                        self.__logger, "Device: {}; ID: {}; Response error.".format(
                            self.name, request.unit_id))

            else:
                GlobalErrorHandler.log_hardware_malfunction(
                    self.__logger, "Device: {}; ID: {}; Invalid response.".format(
                        self.name, request.unit_id))

        except Exception:
            GlobalErrorHandler.log_hardware_malfunction(
                self.__logger, "Device: {}; ID: {}; Can not read the unit status value.".format(
                    self.name, request.unit_id))

        return value


    def get_mode(self):
        """Get mode.

        Returns:
            int: Value of the mode of the air camber.
        """

        value = None

        try:
            request = self.generate_request("GetMode")
            response = self._controller.execute_mb_request(request, self.uart)
            if response is not None:
                if not response.isError():
                    value = response.registers[0]

                else:
                    GlobalErrorHandler.log_hardware_malfunction(
                        self.__logger, "Device: {}; ID: {}; Response error.".format(
                            self.name, request.unit_id))

            else:
                GlobalErrorHandler.log_hardware_malfunction(
                    self.__logger, "Device: {}; ID: {}; Invalid response.".format(
                        self.name, request.unit_id))

        except Exception:
            GlobalErrorHandler.log_hardware_malfunction(
                self.__logger, "Device: {}; ID: {}; Can not read the mode.".format(
                    self.name, request.unit_id))

        return value

    def set_mode(self, mode):
        """Set mode of the air chamber.

        Args:
            mode (int): Mode of the chamber.

        Returns:
            int: Value of the mode of the air camber.
        """

        value = None

        try:
            request = self.generate_request("SetMode")
            response = self._controller.execute_mb_request(request, SetMode=mode)
            if response is not None:
                if not response.isError():
                    value = response.registers[0]

                else:
                    GlobalErrorHandler.log_hardware_malfunction(
                        self.__logger, "Device: {}; ID: {}; Response error.".format(
                            self.name, request.unit_id))

            else:
                GlobalErrorHandler.log_hardware_malfunction(
                    self.__logger, "Device: {}; ID: {}; Invalid response.".format(
                        self.name, request.unit_id))

        except Exception:
            GlobalErrorHandler.log_hardware_malfunction(
                self.__logger, "Device: {}; ID: {}; Can not read the mode.".format(
                    self.name, request.unit_id))

        return value


    def get_fresh_air(self):
        """Get fresh air.

        Returns:
            int: Value of the mode of the air camber.
        """

        value = None

        try:
            request = self.generate_request("FreshAir")
            response = self._controller.execute_mb_request(request, self.uart)
            if response is not None:
                if not response.isError():
                    value = response.registers[0]
                    # Multiply
                    value = value * 10.0

                else:
                    GlobalErrorHandler.log_hardware_malfunction(
                        self.__logger, "Device: {}; ID: {}; Response error.".format(
                            self.name, request.unit_id))

            else:
                GlobalErrorHandler.log_hardware_malfunction(
                    self.__logger, "Device: {}; ID: {}; Invalid response.".format(
                        self.name, request.unit_id))

        except Exception:
            GlobalErrorHandler.log_hardware_malfunction(
                self.__logger, "Device: {}; ID: {}; Can not read the fresh air value.".format(
                    self.name, request.unit_id))

        return value

    def set_fresh_air(self, setpiont):
        """Set fresh air of the air chamber.

        Args:
            setpiont (float): Percentage

        Returns:
            int: Value of the mode of the air camber.
        """

        # get the value.
        local_setpiont = setpiont

        # Filter the minimum.
        if local_setpiont < 0:
            local_setpiont = 0

        # Filter the maximum.
        if local_setpiont > 100:
            local_setpiont = 100

        # Divide by 10 to get in nominal.
        local_setpiont = local_setpiont / 10.0

        # Take only integer part without rounding.
        local_setpiont = int(local_setpiont)

        value = None

        try:
            request = self.generate_request("FreshAir")
            response = self._controller.execute_mb_request(request, FreshAir=local_setpiont)
            if response is not None:
                if not response.isError():
                    value = response.registers[0]

                else:
                    GlobalErrorHandler.log_hardware_malfunction(
                        self.__logger, "Device: {}; ID: {}; Response error.".format(
                            self.name, request.unit_id))

            else:
                GlobalErrorHandler.log_hardware_malfunction(
                    self.__logger, "Device: {}; ID: {}; Invalid response.".format(
                        self.name, request.unit_id))

        except Exception:
            GlobalErrorHandler.log_hardware_malfunction(
                self.__logger, "Device: {}; ID: {}; Can not read the mode.".format(
                    self.name, request.unit_id))

        return value


    def get_setpoint_temp(self):
        """Get mode.

        Returns:
            int: Value of the mode of the air camber.
        """

        value = None

        try:
            request = self.generate_request("GetTemperatureSetpoint")
            response = self._controller.execute_mb_request(request, self.uart)
            if response is not None:
                if not response.isError():
                    value = response.registers[0]

                else:
                    GlobalErrorHandler.log_hardware_malfunction(
                        self.__logger, "Device: {}; ID: {}; Response error.".format(
                            self.name, request.unit_id))

            else:
                GlobalErrorHandler.log_hardware_malfunction(
                    self.__logger, "Device: {}; ID: {}; Invalid response.".format(
                        self.name, request.unit_id))

        except Exception:
            GlobalErrorHandler.log_hardware_malfunction(
                self.__logger, "Device: {}; ID: {}; Can not read the mode.".format(
                    self.name, request.unit_id))

        return value

#endregion
