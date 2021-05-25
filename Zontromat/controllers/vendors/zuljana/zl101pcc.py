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

from utils.logger import get_logger

from controllers.base_controller import BaseController

from devices.vendors.Super.s8_3cn.s8_3cn import S8_3CN as BlackIsland

from utils.logic.functions import l_scale

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
    """Dummy PLC class.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __modbus_rtu_port = None
    """MODBUS RTU RS485 port.
    """

    __modbus_rtu_baud = 9600
    """MODBUS serial port baudrate.
    """

    __modbus_rtu_client = None
    """Modbus client.
    """

    __black_island = None
    """IO
    """

    __operations_count = 4
    """Operations count.
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
        "DO4": 0, "DO5": 1, "DO6": 2, "DO7": 3,

        # Relay Outputs
        "RO0": 0, "RO1": 1, "RO2": 2, "RO3": 3,
        "RO4": 4, "RO4": 5, "RO4": 6, "RO4": 7,

        # Analog Inputs
        "AI0": 0, "AI1": 1, "AI2": 2, "AI3": 3,
        "AI4": 4, "AI4": 5, "AI4": 6, "AI4": 7,

        # Analog Outputs
        "AO0": 0, "AO1": 1, "AO2": 2, "AO3": 3,
    }

    __DI = [False]*8
    """Digital inputs.
    """

    __DORO = [False]*8
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

        self._gpio_map = self.__map

        self.__logger = get_logger(__name__)

        if "modbus_rtu_port" in config:
            self.__modbus_rtu_port = config["modbus_rtu_port"]

        if "modbus_rtu_baud" in config:
            self.__modbus_rtu_baud = config["modbus_rtu_baud"]

        if self.__modbus_rtu_client is None:
            self.__modbus_rtu_client = ModbusClient(
            method="rtu",
            port=self.__modbus_rtu_port,
            timeout=5,
            baudrate=self.__modbus_rtu_baud)

        self.__black_island = BlackIsland(unit=1)

    def __del__(self):
        """Destructor
        """

        pass

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

        else:
            uuid = subprocess.check_output('dmidecode -s system-uuid')

            if result is not None:
                result = result.decode("utf-8")
                result = result.replace(" ", "")
                result = result.replace("\n", "")
                split_result = result.split("\r")

                uuid = split_result[2]

        return uuid

    def __update_black_island(self):

        control_counter = 0

        # Read device digital inputs.
        request = self.__black_island.generate_request("GetDigitalInputs")
        di_response = self.__modbus_rtu_client.execute(request)
        if di_response is not None:
            if not di_response.isError():
                self.__DI = di_response.bits
                control_counter += 1

        # Read device analog inputs.
        request = self.__black_island.generate_request("GetAnalogInputs")
        irr_response = self.__modbus_rtu_client.execute(request)
        if irr_response is not None:
            if not irr_response.isError():
                self.__AI = irr_response.registers
                control_counter += 1

        # Write device digital & relay outputs.
        request = self.__black_island.generate_request("SetRelays", SetRelays=self.__DORO)
        cw_response = self.__modbus_rtu_client.execute(request)
        if cw_response is not None:
            if not cw_response.isError():
                control_counter += 1

        # Write device analog outputs.
        request = self.__black_island.generate_request("SetAnalogOutputs", SetAnalogOutputs=self.__AO)
        hrw_response = self.__modbus_rtu_client.execute(request)
        if hrw_response is not None:
            if not hrw_response.isError():
                control_counter += 1

        # Read device coils.
        # DEBUG PURPOSE ONLY
        # request = self.__black_island.generate_request("GetRelays")
        # cr_response = self.__modbus_rtu_client.execute(request)
        # if cr_response is not None:
        #     if not cr_response.isError():
        #         self.__logger.debug(str(cr_response))
        #         self.__logger.debug(str(cr_response.bits))

        return (control_counter == self.__operations_count)

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

        state = True

        if self.__modbus_rtu_client is None:
            return False

        # state = self.__update_black_island()

        return state

    def digital_read(self, pin):
        """Read the digital input pin.

        Args:
            pin (int): Pin index.

        Returns:
            int: State of the pin.
        """

        l_pin = pin.replace("!", "")
        response = False
        state = False

        if self.__map is None:
            return state

        if not pin in self.__map:
            return state

        # Branch if it is remote GPIO.
        if self.is_valid_remote_gpio(l_pin):
            data = self.parse_remote_gpio(l_pin)

            read_response = self.__modbus_rtu_client.read_discrete_inputs(data["io_reg"], data["io_index"], unit=data["mb_id"])

            return state

        # Read device digital inputs.
        request = self.__black_island.generate_request("GetDigitalInputs")
        di_response = self.__modbus_rtu_client.execute(request)
        if di_response is not None:
            if not di_response.isError():
                self.__DI = di_response.bits

        state = self.__DI[self.__map[pin]]

        # self.__logger.debug("digital_read({}, {})".format(self.model, pin))

        return state

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

        l_pin = pin.replace("!", "")
        response = False
        state = False

        if self.is_off_gpio(l_pin):
            return response

        if not self.is_valid_gpio_type(l_pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(l_pin):
            raise ValueError("Pin does not exists in pin map.")

        # Inversion
        polarity = pin.startswith("!")

        if polarity:
            state = not value
        else:
            state = bool(value)

        # Branch if it is remote GPIO.
        if self.is_valid_remote_gpio(l_pin):
            data = self.parse_remote_gpio(l_pin)

            # Read the device.
            read_response = self.__modbus_rtu_client.read_coils(
                address=data["io_reg"],
                count=data["io_index"]+1,
                unit=data["mb_id"])

            # Get the bunch of the bits.
            bits = read_response.bits

            # Set target bit.
            bits[data["io_index"]] = state

            write_response = self.__modbus_rtu_client.write_coils(data["io_reg"], bits, unit=data["mb_id"])

            return state

        gpio = self.__map[pin]
        
        self.__DORO[gpio] = state

        # Write device digital & relay outputs.
        request = self.__black_island.generate_request("SetRelays", SetRelays=self.__DORO)
        cw_response = self.__modbus_rtu_client.execute(request)
        if cw_response is not None:
            if not cw_response.isError():
                state = True

        # self.__logger.debug("digital_write({}, {}, {})".format(self.model, pin, value))

        return state

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

        state = {"value": value}

        if self.__map is None:
            return state

        if not pin in self.__map:
            return state

        value = l_scale(value, [0, 10], [0, 50000])

        value = int(value)

        self.__AO[self.__map[pin]] = value

        # Write device analog outputs.
        request = self.__black_island.generate_request("SetAnalogOutputs", SetAnalogOutputs=self.__AO)
        hrw_response = self.__modbus_rtu_client.execute(request)
        if hrw_response is not None:
            if not hrw_response.isError():
                pass
        # self.__logger.debug("analog_write({}, {}, {})".format(self.model, pin, value))

        return state

    def read_counter(self, pin):
        """Read the digital counter input.

        Parameters
        ----------
        pin : str
            Pin index.

        Returns
        -------
        int
            State of the pin.
        """

        self.__logger.debug("read_counter({}, {})".format(self.model, pin))

        return 0

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

        value = 0.0
        state = {"value": value, "min": 0.0, "max": 10.0}

        if self.__map is None:
            return state

        if not pin in self.__map:
            return state

        # Read device analog inputs.
        request = self.__black_island.generate_request("GetAnalogInputs")
        irr_response = self.__modbus_rtu_client.execute(request)
        if irr_response is not None:
            if not irr_response.isError():
                self.__AI = irr_response.registers

        value = self.__AI[self.__map[pin]]

        value = l_scale(value, [0, 50000], [0, 10])

        state["value"] = value

        # self.__logger.debug("analog_read({}, {})".format(self.model, pin))

        return state

    def write_counter(self, pin, value):
        """Write the digital counter value.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the counter.

        Returns
        -------
        int
            State of the pin.
        """

        self.__logger.debug("write_counter({}, {}, {})".format(self.model, pin, value))

        return 0

    def set_led(self, pin, value):
        """Write the LED.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the LED.

        Returns
        -------
        int
            State of the pin.
        """

        # self.__logger.debug("set_led({}, {}, {})".format(self.model, pin, value))

        return 0

    def read_temperature(self, dev, circuit):
        """Read the thermometer.

        Parameters
        ----------
        dev : str
            Dev ID.

        circuit : str
            Circuit ID.

        Returns
        -------
        int
            State of the device.
        """

        # self.__logger.debug("read_temperature({}, {}, {})".format(self.model, dev, circuit))

        return 0

    def read_light(self, dev, circuit):
        """Read the light sensor.

        Parameters
        ----------
        dev : str
            Dev ID.

        circuit : str
            Circuit ID.

        Returns
        -------
        int
            State of the device.
        """

        self.__logger.debug("read_light({}, {}, {})".format(self.model, dev, circuit))

        return 0

    def read_mb_registers(self, uart, dev_id, registers, register_type=None):
        """Read MODBUS register.

        Parameters
        ----------
        uart : int
            UART index.

        dev_id : int
            MODBUS ID.

        registers : array
            Registers IDs.

        register_type : str
            Registers types.

        Returns
        -------
        mixed
            State of the device.
        """

        self.__logger.debug("read_mb_registers({}, {}, {}, {}, {})".format(self.model, uart, dev_id, registers, register_type))

        return 0

    def get_1w_devices(self):
        """Get 1W device from the list of all.

        Returns
        -------
        tuple
            1W devices.
        """

        # self.__logger.debug("get_1w_devices({})".format(self.model))

        return []

    def get_device(self, dev, circuit):
        """Get device.

        Returns:
            [type]: [description]
        """

        # self.__logger.debug("get_device({}, {}, {})".format(self.model, dev, circuit))

        device = None

        if dev == "1wdevice":
            device = {"vis": 0.0}

        return device

    def execute_mb_request(self, request):
        """Execute modbus request.

        Args:
            request (ModbusRequest): PyMODBUS request instance.

        Returns:
            ModbusResponse: PyMODBUS response instance.
        """
        response = None

        if self.__modbus_rtu_client is not None:
            response = self.__modbus_rtu_client.execute(request)

        return response
