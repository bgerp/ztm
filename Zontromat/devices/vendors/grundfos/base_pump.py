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

from utils.logger import get_logger

from devices.drivers.modbus.device import ModbusDevice
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.function_code import FunctionCode

from devices.vendors.grundfos.control_mode import ControlMode

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

__class_name__ = "EnergyCenter"
"""Plugin class name."""

#endregion

class BasePump(ModbusDevice):
    """Fluid pump.
    """

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, config):
        """Constructor
        """

        super().__init__(config)

        self.__logger = None
        """Logger
        """

        self._vendor = "grundfos"

        self._e_stop = "off"
        if "e_stop" in config:
            self._e_stop = config["e_stop"]

        self._stop_on_shutdown = False
        if "stop_on_shutdown" in config:
            self._stop_on_shutdown = config["stop_on_shutdown"]

        self._e_status = "off"
        if "e_status" in config:
            self._e_status = config["e_status"]

        self.__set_registers()

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods

    def __set_registers(self):

        self._parameters.append(
            Parameter("GetControlMode", "Enum",\
            ParameterType.UINT16_T_LE, [102], FunctionCode.ReadInputRegisters))

        self._parameters.append(
            Parameter("SetControlMode", "Enum",\
            ParameterType.UINT16_T_LE, [102], FunctionCode.WriteSingleHoldingRegister))

        self._parameters.append(
            Parameter("GetSetpoint", "%",\
            ParameterType.UINT16_T_LE, [104], FunctionCode.ReadInputRegisters))

        self._parameters.append(
            Parameter("SetSetpoint", "%",\
            ParameterType.UINT16_T_LE, [104], FunctionCode.WriteSingleHoldingRegister))

#endregion

#region Public Methods

    def get_mode(self):
        """Get the control mode of the E-Pump module.

        Returns:
            ControlMode: Control mode.
        """

        name = "GetControlMode"

        value = -1 # This value means problem.

        request = self.generate_request(name)
        if request is not None:
            response = self._controller.execute_mb_request(request, self.uart)
            if not response.isError():
                value = response.registers[0]
                value = ControlMode(value)

        return value

    def set_mode(self, mode: ControlMode):
        """Set the control mode of the E-Pump module.

        Args:
            mode (ControlMode): Control mode.

        Returns:
            ControlMode: Control mode.
        """

        name = "SetControlMode"

        value = -1 # This value means problem.

        request = self.generate_request(name, SetControlMode=mode.value)
        if request is not None:
            response = self._controller.execute_mb_request(request, self.uart)
            if not response.isError():
                registers = {}
                for index in range(request.address, request.address + request.count):
                    registers[index] = response.registers[index - request.address]
                value = self.get_parameter_value(name, registers)

        return value

    def get_setpoint(self):
        """[summary]

        Returns:
            [type]: [description]
        """

        name = "SetSetpoint"

        value = -1 # This value means problem.

        request = self.generate_request(name)
        if request is not None:
            response = self._controller.execute_mb_request(request, self.uart)
            if not response.isError():
                value = response.registers[0] / 100

        return value

    def set_setpoint(self, value):
        """Set the setpoint of the pump.

        Args:
            value (float): Percentage of the control loop of the E-Pump module.

        Returns:
            float: Percentage of the control loop of the E-Pump module.
        """

        temp_value = value

        if temp_value < 0:
            temp_value = 0

        if temp_value > 100:
            temp_value = 100

        temp_value = temp_value * 100

        name = "SetSetpoint"

        value = -1 # This value means problem.

        request = self.generate_request(name, SetSetpoint=temp_value)
        if request is not None:
            response = self._controller.execute_mb_request(request, self.uart)
            if not response.isError():
                registers = {}
                for index in range(request.address, request.address + request.count):
                    if hasattr(response, 'registers'):
                        registers[index] = response.registers[index - request.address]

                value = self.get_parameter_value(name, registers)

        return value

    def e_stop(self, value):

        if (value != 1) and (value != 0):
            return

        if self._controller.is_valid_gpio(self._e_stop):
            self._controller.digital_write(self._e_stop, value)

    def e_status(self):

        status = 0

        if self._controller.is_valid_gpio(self._e_status):
            status = self._controller.digital_read(self._e_status)

        return status

    def init(self):
        """Initialize the pump.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

    def update(self):
        """Update the pump logic.
        """

    def shutdown(self):
        """Shutdown the pump.
        """
        self.__logger.info("Shuting down the: {}".format(self.name))

        if self._stop_on_shutdown:
            self.e_stop(0)

        self.__logger.info("Shuted down the: {}".format(self.name))

#endregion
