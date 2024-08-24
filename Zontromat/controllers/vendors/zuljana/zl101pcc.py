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

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from utils.logger import get_logger
from utils.logic.functions import l_scale
from .utils.generate_uuid import UUID

from controllers.base_controller import BaseController

# from devices.vendors.super.s8_3cn.s8_3cn import S83CN as BlackIsland
from devices.vendors.cwt.mb308v.mb308v import MB308V as BlackIsland
from devices.drivers.modbus.function_code import FunctionCode

# Import MODBUS clients.
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.client.tcp import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer

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

        self.__logger = get_logger(__name__)
        """Logger
        """

        self.__uuid = UUID()
        """UUID handler.
        """

        modbus_config = self.is_valid_port_cfg(0)
        self.__local_io_address=modbus_config["rtu_unit"]

        # TODO: Migrate all indexes with dynamic calls to the remote island.
        self._gpio_map = \
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
        """GPIO mapping.
        """        

        # TODO: Remove below.
        self.__DI = [False]*8
        """Digital inputs.
        """

        # TODO: Remove below.
        self.__DORO = [False]*12
        """Digital & Relay outputs.
        """

        # TODO: Remove below.
        self.__AI = [0]*8
        """Analog inputs.
        """

        # TODO: Remove below.
        self.__AO = [0]*4
        """Analog outputs.
        """

        self.__interfaces_count = 2
        """Interfaces count.
        """

        self.__modbus_rtu_clients = {}
        """Modbus-RTU clients.
        """

        self.__black_island = None
        """IO
        """

        for index in range(0, self.__interfaces_count):
            # TODO: move this method to thiss class, this is specific for this controller.
            # It is not commont thing.
            modbus_config = self.is_valid_port_cfg(index)
            if (not index in self.__modbus_rtu_clients) and (not modbus_config is {}):
                if modbus_config["interface"] == "RTU":
                    self.__modbus_rtu_clients[index] = ModbusSerialClient(
                        method="rtu",
                        port=modbus_config["rtu_port"],
                        baudrate=modbus_config["rtu_baudrate"],
                        timeout=modbus_config["timeout"],
                        bytesize=modbus_config["rtu_bytesize"],
                        parity=modbus_config["rtu_parity"],
                        stopbits=modbus_config["rtu_stopbits"]
                        )
                elif modbus_config["interface"] == "TCP":
                    self.__modbus_rtu_clients[index] = ModbusTcpClient(
                        modbus_config["tcp_address"],
                        port=modbus_config["tcp_port"],
                        timeout=modbus_config["timeout"],
                        )
                elif modbus_config["interface"] == "RTUOverTCP":
                    self.__modbus_rtu_clients[index] = ModbusTcpClient(
                        modbus_config["tcp_address"],
                        port=modbus_config["tcp_port"],
                        timeout=modbus_config["timeout"],
                        framer=ModbusFramer
                        )
            else:
                # TODO: move this method to this calss. This is speciffic thing for this controller.
                self.show_valid_serial_ports(modbus_config["port"])
        
            # TODO: Remove below.
            # This hot fix is mandatory, because "black island" is part of the logical body of the master controller.
            if index == 0:
                # TODO: Remove below.
                self.__black_island = BlackIsland(mb_id=modbus_config["rtu_unit"])

        self.__analog_limits = [0.0, 10.0]
        """Analog I/O volts.
        """

        # TODO: Remove below.
        self.__di_count = 0
        # TODO: Remove below.
        self.__do_count = 0
        # TODO: Remove below.
        self.__ai_count = 0
        # TODO: Remove below.
        self.__ao_count = 0

        self.__data_tree = {}

#endregion

#region Private Methods

    def __get_hardware_id(self):

        self.__uuid.generate()
        return self.__uuid.uuid_value


        # uuid = ""

        # if "nt" in os.name:
        #     result = subprocess.check_output("wmic csproduct get uuid")

        #     if result is not None:
        #         result = result.decode("utf-8")
        #         result = result.replace(" ", "")
        #         result = result.replace("\n", "")
        #         split_result = result.split("\r")

        #         uuid = split_result[2]

        # elif "posix" in os.name:

        #     # https://askubuntu.com/questions/1200357/an-unique-key-id-that-corresponds-to-only-one-combination-of-ubuntu-os-and-hardw
        #     try:
        #         uuid = os.popen("cat /etc/machine-id").read().split()[-1]

        #     except Exception:
        #         pass

        # return uuid

    def __get_tree_element(self, remote_gpio):
        return False

    def __set_tree_element(self, remote_gpio, value):

        if remote_gpio["uart"] in self.__data_tree:
            if remote_gpio["mb_id"] in self.__data_tree[remote_gpio["uart"]]:
                if remote_gpio["mb_fc"] in self.__data_tree[remote_gpio["uart"]][remote_gpio["mb_id"]]:
                    if remote_gpio["io_reg"] in self.__data_tree[remote_gpio["uart"]][remote_gpio["mb_id"]][remote_gpio["mb_fc"]]:
                        if remote_gpio["io_index"] in self.__data_tree[remote_gpio["uart"]][remote_gpio["mb_id"]][remote_gpio["mb_fc"]][remote_gpio["io_reg"]]:
                            self.__data_tree[remote_gpio["uart"]][remote_gpio["mb_id"]][remote_gpio["mb_fc"]][remote_gpio["io_reg"]][remote_gpio["io_index"]] = value
                        else:
                            self.__data_tree[remote_gpio["uart"]][remote_gpio["mb_id"]][remote_gpio["mb_fc"]][remote_gpio["io_reg"]][remote_gpio["io_index"]] = value
                    else:
                        self.__data_tree[remote_gpio["uart"]][remote_gpio["mb_id"]][remote_gpio["mb_fc"]][remote_gpio["io_reg"]] = {remote_gpio["io_index"]: value}
                else:
                    self.__data_tree[remote_gpio["uart"]][remote_gpio["mb_id"]][remote_gpio["mb_fc"]] = {remote_gpio["io_reg"]: {remote_gpio["io_index"]: value}}
            else:
                self.__data_tree[remote_gpio["uart"]][remote_gpio["mb_id"]] = {remote_gpio["mb_fc"]: {remote_gpio["io_reg"]: {remote_gpio["io_index"]: value}}}
        else:
            self.__data_tree[remote_gpio["uart"]] = {remote_gpio["mb_id"]: {remote_gpio["mb_fc"]: {remote_gpio["io_reg"]: {remote_gpio["io_index"]: value}}}}

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

        for interface in self.__data_tree:
            devices = self.__data_tree[interface]
            # TODO: Create connection with interface.
            for device in devices:
                fcs = devices[device]
                sorted_fcs = dict(sorted(fcs.items()))
                for fc in sorted_fcs:
                    if fc == 1:
                        pass
                    elif fc == 2:
                        for address in fcs[fc]:
                            print(f"response = read_discrete_inputs({address}, 8, {device})")
                            data = fcs[fc][address]
                            data_len = 8 if len(data) < 8 else 16
                            # TODO: With connection create call with printed parameters.
                            map_data = [None]*data_len
                            for bit_index in data:
                                map_data[bit_index] = data[bit_index]
                    elif fc == 3:
                        for address in fcs[fc]:
                            print(f"response = read_holding_registers({address}, 8, {device})")
                            data = fcs[fc][address]
                            data_len = 8 if len(data) < 8 else 16
                            # TODO: With connection create call with printed parameters.
                            map_data = [None]*data_len
                            for bit_index in data:
                    elif fc == 4:
                        for address in fcs[fc]:
                            print(f"response = read_input_registers({address}, 8, {device})")
                            data = fcs[fc][address]
                            data_len = 8 if len(data) < 8 else 16
                            # TODO: With connection create call with printed parameters.
                            map_data = [None]*data_len
                            for bit_index in data:
                                map_data[bit_index] = data[bit_index]
                    elif fc == 5:
                        pass
                    elif fc == 6:
                        pass
                    elif fc == 15:
                        for address in fcs[fc]:
                            data = fcs[fc][address]
                            data_len = 8 if len(data) < 8 else 16
                            map_data = [None]*data_len
                            for bit_index in data:
                                map_data[bit_index] = data[bit_index]
                            print(f"write_coils({address}, {map_data}, {device})")
                            # TODO: With connection create call with printed parameters.
                    elif fc == 16:
                        for address in fcs[fc]:
                            data = fcs[fc][address]
                            data_len = 8 if len(data) < 8 else 16
                            map_data = [None]*data_len
                            for bit_index in data:
                                map_data[bit_index] = data[bit_index]
                            print(f"write_holding_registers({address}, {map_data}, {device})")
                            # TODO: With connection create call with printed parameters.


        return self.__modbus_rtu_clients is not None or {}

    # TODO: Refactor below.
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
        def get_local_gpio(pin):

            lgpio_response = False

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

            lgpio_response = self.__DI[self._gpio_map[pin]]

            # Inversion
            if self.is_gpio_inverted(pin):
                lgpio_response = not lgpio_response

            return lgpio_response

        # Remote GPIO.
        def get_remote_gpio(pin):

            rgpio_response = False

            remote_gpio = self.parse_remote_gpio(pin)
            self.__set_tree_element(remote_gpio)

            if not remote_gpio["uart"] in self.__modbus_rtu_clients:
                GlobalErrorHandler.log_missing_resource("Missing MODBUS-RTU UART{} interface".format(remote_gpio["uart"]))
                return False

            read_response = self.__modbus_rtu_clients[remote_gpio["uart"]].read_discrete_inputs(
                remote_gpio["io_reg"],
                remote_gpio["io_index"]+1,
                remote_gpio["mb_id"])

            if not read_response.isError():
                rgpio_response = read_response.bits[remote_gpio["io_index"]]

                # Inversion
                if self.is_gpio_inverted(pin):
                    rgpio_response = not rgpio_response

            return rgpio_response

        if isinstance(pin, str):
            if self.is_gpio_off(pin):
                return response
            elif self.is_gpio_local(pin):
                response = get_local_gpio(pin)
            elif self.is_gpio_remote(pin):
                response = get_remote_gpio(pin)
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "Remote GPIO: {} @ {} Pin does not exists in pin map.".format(pin, self))

        elif isinstance(pin, list):
            response = []
            # Go trough all pins.
            for p in pin:
                if self.is_gpio_off(p):
                    break
                elif self.is_gpio_local(p):
                    response.append(get_local_gpio(p))
                elif self.is_gpio_remote(p):
                    response.append(get_remote_gpio(p))
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "Remote GPIO: {} @ {} Pin does not exists in pin map.".format(pin, self))

        else:
             GlobalErrorHandler.log_missing_resource(f"Pin ({pin}) does not confirm list or str.")

        self.__di_count += 1

        return response

    # TODO: Refactor below.
    def digital_write(self, pin, value):
        """Write the digital output pin.

        Args:
            pin (str, list): Pin
            value (_type_): Value for the output pin.

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            any: State of the pin.
        """

        response = False
        
        # Local GPIO.
        def set_local_gpio(pin, state):

            state = False

            if self.is_gpio_off(pin):
                state = False

            if self.is_gpio_nothing(pin):
                raise ValueError("Pin can not be None or empty string.")

            # Make is bool.
            state = bool(value)

            # Inversion
            if self.is_gpio_inverted(pin):
                state = not state

            gpio = self._gpio_map[pin]
            self.__DORO[gpio] = state
            # Write device digital & relay outputs.
            request = self.__black_island.generate_request("SetRelays", SetRelays=self.__DORO)
            cw_response = self.__modbus_rtu_clients[0].execute(request)

            if cw_response is not None:
                if cw_response.isError():
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "Local GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))
                    state = False
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "Local GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))
                state = False
            
            # self.__logger.debug("digital_write({}, {}, {})".format(self.model, pin, value))
            return state

        # Remote GPIO.
        def set_remote_gpio(pin, state):

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

            remote_gpio = self.parse_remote_gpio(pin)
            self.__set_tree_element(remote_gpio, value)

            if remote_gpio["mb_fc"] == FunctionCode.WriteSingleCoil.value:
                write_response = self.__modbus_rtu_clients[remote_gpio["uart"]].write_coil(
                    remote_gpio["io_reg"]+remote_gpio["io_index"],
                    value,
                    remote_gpio["mb_id"])

                if not write_response.isError():
                    response = True
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            elif remote_gpio["mb_fc"] == FunctionCode.WriteMultipleCoils.value:
                write_response = self.__modbus_rtu_clients[remote_gpio["uart"]].write_coils(
                    remote_gpio["io_reg"]+remote_gpio["io_index"],
                    [value],
                    remote_gpio["mb_id"])

                if not write_response.isError():
                    response = True
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            return state

        if isinstance(pin, str):
            if self.is_gpio_off(pin):
                return response
            elif self.is_gpio_local(pin):
                response = set_local_gpio(pin, value)
            elif self.is_gpio_remote(pin):
                response = set_remote_gpio(pin, value)
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "Remote GPIO: {} @ {} Pin does not exists in pin map.".format(pin, self))

        elif isinstance(pin, list):
            # Go trough all pins.
            for p in pin:
                if self.is_gpio_off(p):
                    break
                elif self.is_gpio_local(p):
                    response = set_local_gpio(p, value)
                elif self.is_gpio_remote(p):
                    response = set_remote_gpio(p, value)
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "Remote GPIO: {} @ {} Pin does not exists in pin map.".format(pin, self))

        else:
             GlobalErrorHandler.log_missing_resource(f"Pin ({pin}) does not confirm list or str.")

        self.__do_count += 1

        return response

    # TODO: Refactor below.
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

        value = int(value)

        response = False

        # Local GPIO.
        if self.is_gpio_local(pin):

            # Transform values from 0-10V to device specific values.
            param_name = "SetAnalogOutputs"
            parameter = self.__black_island.get_parameter_by_name(param_name)
            result_value = l_scale(value, self.__analog_limits, parameter.limits)
            self.__AO[self._gpio_map[pin]] = int(result_value)

            # Write device analog outputs.
            request = self.__black_island\
                .generate_request(param_name, SetAnalogOutputs=self.__AO)
            hrw_response = self.__modbus_rtu_clients[0].execute(request)
            if hrw_response is not None:
                if not hrw_response.isError():
                    response = True
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            # self.__logger.debug("analog_write({}, {}, {})".format(self.model, pin, value))

        # Remote GPIO.
        elif self.is_gpio_remote(pin):
            remote_gpio = self.parse_remote_gpio(pin)
            self.__set_tree_element(remote_gpio, value)

            if remote_gpio["mb_fc"] == FunctionCode.WriteSingleHoldingRegister.value:
                write_response = self.__modbus_rtu_clients[remote_gpio["uart"]].write_register(
                    remote_gpio["io_reg"]+remote_gpio["io_index"],
                    value,
                    remote_gpio["mb_id"])

                if not write_response.isError():
                    response = True
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            elif remote_gpio["mb_fc"] == FunctionCode.WriteMultipleHoldingRegisters.value:
                result_value = l_scale(value, self.__analog_limits, [0, 24000])
                result_value = int(result_value)
                write_response = self.__modbus_rtu_clients[remote_gpio["uart"]].write_registers(
                    remote_gpio["io_reg"]+remote_gpio["io_index"],
                    [result_value],
                    remote_gpio["mb_id"])

                if not write_response.isError():
                    response = True
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

        else:
            raise ValueError("Pin does not exists in pin map.")

        self.__ao_count += 1

        return response

    # TODO: Refactor below.
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

        state = {"value": 0.0, "min": 0.0, "max": 10.0}

        # Local GPIO.
        if self.is_gpio_local(pin):

            # Read device analog inputs.
            param_name = "GetAnalogInputs"
            request = self.__black_island.generate_request(param_name)
            irr_response = self.__modbus_rtu_clients[0].execute(request)
            if irr_response is not None:
                if not irr_response.isError():
                    self.__AI = irr_response.registers
                else:
                    GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))
            else:
                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "GPIO: {} @ {} malfunctioning, check modbus cables and connections.".format(pin, self))

            # Scale analog inputs value in 0 to 10 volts.
            input_value = self.__AI[self._gpio_map[pin]]
            param = self.__black_island.get_parameter_by_name(param_name)
            state["value"] = l_scale(input_value, param.limits, self.__analog_limits)

            # self.__logger.debug("analog_read({}, {})".format(self.model, pin))

        # Remote GPIO.
        elif self.is_gpio_remote(pin):
            remote_gpio = self.parse_remote_gpio(pin)
            self.__set_tree_element(remote_gpio, False)

            # self.__logger.debug(f"GPIO: {remote_gpio}")

            if isinstance(pin, str):
                read_response = self.__modbus_rtu_clients[remote_gpio["uart"]].read_input_registers(
                    remote_gpio["io_reg"]+remote_gpio["io_index"],
                    1,
                    remote_gpio["mb_id"])

                if not read_response.isError():
                    input_value = read_response.registers[0]
                    param_name = "GetAnalogInputs"
                    param = self.__black_island.get_parameter_by_name(param_name)
                    state["value"] = l_scale(input_value, param.limits, self.__analog_limits)

        else:
            raise ValueError("Pin does not exists in pin map.")

        self.__ai_count += 1

        return state

    # Is this thing mandatory?
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

#endregion
