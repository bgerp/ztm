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

import subprocess
import os

# Import MODBUS clients.
# from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from services.global_error_handler.global_error_handler import GlobalErrorHandler

from utils.logger import get_logger
from utils.logic.functions import l_scale

from controllers.base_controller import BaseController

# from devices.vendors.super.s8_3cn.s8_3cn import S83CN as BlackIsland
from devices.vendors.cwt.mb308v.mb308v import MB308V as BlackIsland

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

__class_name__ = "ZL101PCC"
"""Controller target class.
"""

#endregion

class ZL101PCC(BaseController):
    """ZL101PCC PLC class.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __modbus_rtu_clients_count = 2
    """Modbus-RTU clients count.
    """

    __modbus_rtu_clients = {}
    """Modbus-RTU clients.
    """

    __black_island = None
    """IO
    """

    __map = \
    {\
        "identification": {"vendor": "bao bao industries", "model": "zl101pcc"},\

        # LEDs
        "LED0": 0, "LED1": 1, "LED2": 2, "LED3": 3,

        # Digital Inputs
        "DI0": 0, "DI1": 1, "DI2": 2, "DI3": 3,
        "DI4": 4, "DI5": 5, "DI6": 6, "DI7": 7,
        "DI8": 8, "DI9": 9,

        # Digital Outputs
        "DO0": 0, "DO1": 1, "DO2": 2, "DO3": 3,
        "DO4": 4, "DO5": 5, "DO6": 6, "DO7": 7,
        "DO8": 8, "DO9": 9, "DO10": 10, "DO11": 11,

        # Relay Outputs
        "RO0": 0, "RO1": 1, "RO2": 2, "RO3": 3,
        "RO4": 4, "RO5": 5, "RO6": 6, "RO7": 7,
        "RO8": 8, "RO9": 9, "RO10": 10, "RO11": 11,

        # Analog Inputs
        "AI0": 0, "AI1": 1, "AI2": 2, "AI3": 3,
        "AI4": 4, "AI5": 5, "AI6": 6, "AI7": 7,

        # Analog Outputs
        "AO0": 0, "AO1": 1, "AO2": 2, "AO3": 3,
    }

    __DI = [False]*8
    """Digital inputs.
    """

    __DORO = [False]*12
    """Digital & Relay outputs.
    """

    __AI = [0]*8
    """Analog inputs.
    """

    __AO = [0]*4
    """Analog outputs.
    """

#endregion

#region Properties

    @property
    def vendor(self):
        """Get device vendor.

        Returns:
            str: Vendor
        """

        return "Bao Bao Industries"

    @property
    def model(self):
        """Get device model.

        Returns:
            str: Model
        """

        return __class_name__

    @property
    def serial_number(self):
        """Get device serial number.

        Returns:
            str: Serial number.
        """

        return self.__get_hardware_id()

    @property
    def version(self):
        """Get device version.

        Returns:
            str: Version
        """

        return "1"

#endregion

#region Constructor

    def __init__(self, config):
        """Constructor
        """

        super().__init__(config)

        # Validate GPIO map.
        if self.__map is None:
            raise ValueError("Invalid GPIO map.")

        self._gpio_map = self.__map

        self.__logger = get_logger(__name__)

        for index in range(0, self.__modbus_rtu_clients_count):
            modbus_rtu_cfg = self.is_valid_port_cfg(index)
            if (not index in self.__modbus_rtu_clients) and (not modbus_rtu_cfg is {}):
                self.__modbus_rtu_clients[index] = ModbusClient(
                    method="rtu",
                    port=modbus_rtu_cfg["port"],
                    baudrate=modbus_rtu_cfg["baudrate"],
                    timeout=modbus_rtu_cfg["timeout"],
                    bytesize=modbus_rtu_cfg["bytesize"],
                    parity=modbus_rtu_cfg["parity"],
                    stopbits=modbus_rtu_cfg["stopbits"]
                    )
            else:
                self.show_valid_serial_ports(modbus_rtu_cfg["port"])

        self.__black_island = BlackIsland(unit=1)

#endregion

#region Private Methods

    def __get_hardware_id(self):

        uuid = ""

        if "nt" in os.name:
            result = subprocess.check_output("wmic csproduct get uuid")

            if result is not None:
                result = result.decode("utf-8")
                result = result.replace(" ", "")
                result = result.replace("\n", "")
                split_result = result.split("\r")

                uuid = split_result[2]

        elif "posix" in os.name:

            # https://askubuntu.com/questions/1200357/an-unique-key-id-that-corresponds-to-only-one-combination-of-ubuntu-os-and-hardw
            try:
                uuid = os.popen("cat /etc/machine-id").read().split()[-1]

            except Exception:
                pass

        return uuid

#endregion

#region Protected Methods

#endregion

#region Static Methods

#endregion

#region Public Methods

#endregion

#region Base Controller Implementation

    def update(self):
        """Update controller state."""

        return self.__modbus_rtu_clients is not None or {}

    def digital_read(self, pin):
        """Read the digital input pin.

        Args:
            pin (int): Pin index.

        Returns:
            int: State of the pin.
        """

        if self.is_gpio_off(pin):
            return False

        if self.is_gpio_nothing(pin):
            raise ValueError("Pin can not be None or empty string.")

        response = False

        # Local GPIO.
        if self.is_gpio_local(pin):

            # Read device digital inputs.
            request = self.__black_island.generate_request("GetDigitalInputs")
            di_response = self.__modbus_rtu_clients[0].execute(request)
            if di_response is not None:
                if not di_response.isError():
                    self.__DI = di_response.bits
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            response = self.__DI[self._gpio_map[pin]]

            # Inversion
            if self.is_gpio_inverted(pin):
                response = not response

        # Remote GPIO.
        elif self.is_gpio_remote(pin):

            remote_gpio = self.parse_remote_gpio(pin)

            if not remote_gpio["uart"] in self.__modbus_rtu_clients:
                GlobalErrorHandler.log_missing_resource("Missing MODBUS-RTU UART{} interface".format(remote_gpio["uart"]))
                return False

            read_response = self.self.__modbus_rtu_clients[remote_gpio["uart"]].read_discrete_inputs(
                remote_gpio["io_reg"],
                remote_gpio["io_index"]+1,
                unit=remote_gpio["mb_id"])

            if not read_response.isError():
                response = read_response.bits[remote_gpio["io_index"]]

                # Inversion
                if self.is_gpio_inverted(pin):
                    response = not response

        else:
             GlobalErrorHandler.log_missing_resource("Pin does not exists in pin map.")

        return response

    def digital_write(self, pin, value):
        """Write the digital output pin.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the output pin.

        Returns
        -------
        mixed
            State of the pin.
        """

        response = False
        state = False

        if self.is_gpio_off(pin):
            return False

        if self.is_gpio_nothing(pin):
            raise ValueError("Pin can not be None or empty string.")
        
        # Make is bool.
        state = bool(value)

        # Inversion
        if self.is_gpio_inverted(pin):
            state = not state

        # Local GPIO.
        if self.is_gpio_local(pin):

            gpio = self._gpio_map[pin]
            self.__DORO[gpio] = state

            # Write device digital & relay outputs.
            request = self.__black_island.generate_request("SetRelays", SetRelays=self.__DORO)
            cw_response = self.__modbus_rtu_clients[0].execute(request)
            if cw_response is not None:
                if not cw_response.isError():
                    response = True
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            # self.__logger.debug("digital_write({}, {}, {})".format(self.model, pin, value))

        # Remote GPIO.
        elif self.is_gpio_remote(pin):
            remote_gpio = self.parse_remote_gpio(pin)

            write_response = self.__modbus_rtu_clients[remote_gpio["uart"]].write_coil(
                remote_gpio["io_reg"]+remote_gpio["io_index"],
                state,
                unit=remote_gpio["mb_id"])

            if not write_response.isError():
                response = True

        else:
            raise ValueError("Pin does not exists in pin map.")

        return response

    def analog_write(self, pin, value):
        """Write the analog input pin.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the output pin.

        Returns
        -------
        int
            State of the pin.
        """

        if self.is_gpio_off(pin):
            return False

        if self.is_gpio_nothing(pin):
            raise ValueError("Pin can not be None or empty string.")

        response = False

        # Local GPIO.
        if self.is_gpio_local(pin):

            value = l_scale(value, [0, 10], [0, 50000])

            value = int(value)

            self.__AO[self._gpio_map[pin]] = value

            # Write device analog outputs.
            request = self.__black_island\
                .generate_request("SetAnalogOutputs", SetAnalogOutputs=self.__AO)
            hrw_response = self.__modbus_rtu_clients[0].execute(request)
            if hrw_response is not None:
                if not hrw_response.isError():
                    response = True
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            # self.__logger.debug("analog_write({}, {}, {})".format(self.model, pin, value))

        else:
            raise ValueError("Pin does not exists in pin map.")

        return response

    def analog_read(self, pin):
        """Write the analog input pin.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the output pin.

        Returns
        -------
        int
            State of the pin.
        """

        if self.is_gpio_off(pin):
            return False

        if self.is_gpio_nothing(pin):
            raise ValueError("Pin can not be None or empty string.")

        value = 0.0
        state = {"value": value, "min": 0.0, "max": 10.0}

        # Local GPIO.
        if self.is_gpio_local(pin):

            # Read device analog inputs.
            request = self.__black_island.generate_request("GetAnalogInputs")
            irr_response = self.__modbus_rtu_clients[0].execute(request)
            if irr_response is not None:
                if not irr_response.isError():
                    self.__AI = irr_response.registers
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            value = self.__AI[self._gpio_map[pin]]

            value = l_scale(value, [0, 50000], [0, 10])

            state["value"] = value

            # self.__logger.debug("analog_read({}, {})".format(self.model, pin))

        # Remote GPIO.
        elif self.is_gpio_remote(pin):
            remote_gpio = self.parse_remote_gpio(pin)

            self.__logger.debug(f"GPIO: {remote_gpio}")

            # write_response = self.__modbus_rtu_clients[remote_gpio["uart"]].write_coil(
            #     remote_gpio["io_reg"]+remote_gpio["io_index"],
            #     state,
            #     unit=remote_gpio["mb_id"])

            # if not write_response.isError():
            #     response = True

        else:
            raise ValueError("Pin does not exists in pin map.")

        return state

    def execute_mb_request(self, request, uart):
        """Execute modbus request.

        Args:
            request (ModbusRequest): PyMODBUS request instance.

        Returns:
            ModbusResponse: PyMODBUS response instance.
        """
        response = None

        if self.__modbus_rtu_clients is not None:
            response = self.__modbus_rtu_clients[uart].execute(request)

        return response
