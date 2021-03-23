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

from controllers.zuljana.requests.read_device_coils import ReadDeviceCoils
from controllers.zuljana.requests.read_device_discrete_inputs import ReadDeviceDiscreteInputs
from controllers.zuljana.requests.read_device_holding_registers import ReadDeviceHoldingRegisters
from controllers.zuljana.requests.read_device_input_registers import ReadDeviceInputRegisters

from controllers.zuljana.requests.write_device_coils import WriteDeviceCoils
from controllers.zuljana.requests.write_device_registers import WriteDeviceRegisters

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

    __black_island_id = 1
    """Black island ID.
    """

    __map = \
    {\
        "identification": {"vendor": "bao bao industries", "model": "zl101pcc"},\

        "LED0": {"dev": "led", "major_index": 1, "minor_index": 1},\
        "LED1": {"dev": "led", "major_index": 1, "minor_index": 2},\
        "LED2": {"dev": "led", "major_index": 1, "minor_index": 3},\
        "LED3": {"dev": "led", "major_index": 1, "minor_index": 4},\

        "DI0": {"dev": "input", "major_index": 1, "minor_index": 1},\
        "DI1": {"dev": "input", "major_index": 1, "minor_index": 2},\
        "DI2": {"dev": "input", "major_index": 1, "minor_index": 3},\
        "DI3": {"dev": "input", "major_index": 1, "minor_index": 4},\

        "DI4": {"dev": "input", "major_index": 2, "minor_index": 1},\
        "DI5": {"dev": "input", "major_index": 2, "minor_index": 2},\
        "DI6": {"dev": "input", "major_index": 2, "minor_index": 3},\
        "DI7": {"dev": "input", "major_index": 2, "minor_index": 4},\
        "DI8": {"dev": "input", "major_index": 2, "minor_index": 5},\
        "DI9": {"dev": "input", "major_index": 2, "minor_index": 6},\

        "DO0": {"dev": "do", "major_index": 1, "minor_index": 1},\
        "DO1": {"dev": "do", "major_index": 1, "minor_index": 2},\
        "DO2": {"dev": "do", "major_index": 1, "minor_index": 3},\
        "DO3": {"dev": "do", "major_index": 1, "minor_index": 4},\

        "RO0": {"dev": "relay", "major_index": 2, "minor_index": 1},\
        "RO1": {"dev": "relay", "major_index": 2, "minor_index": 2},\
        "RO2": {"dev": "relay", "major_index": 2, "minor_index": 3},\
        "RO3": {"dev": "relay", "major_index": 2, "minor_index": 4},\
        "RO4": {"dev": "relay", "major_index": 2, "minor_index": 5},\

        "AI0": {"dev": "ai", "major_index": 1, "minor_index": 1},\
        "AI1": {"dev": "ai", "major_index": 2, "minor_index": 1},\
        "AI2": {"dev": "ai", "major_index": 2, "minor_index": 2},\
        "AI3": {"dev": "ai", "major_index": 2, "minor_index": 3},\
        "AI4": {"dev": "ai", "major_index": 2, "minor_index": 4},\

        "AO0": {"dev": "ao", "major_index": 1, "minor_index": 1},\
        "AO1": {"dev": "ao", "major_index": 2, "minor_index": 1},\
        "AO2": {"dev": "ao", "major_index": 2, "minor_index": 2},\
        "AO3": {"dev": "ao", "major_index": 2, "minor_index": 3},\
        "AO4": {"dev": "ao", "major_index": 2, "minor_index": 4},\
    }

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

        # Read device coils.
        cr_request = ReadDeviceCoils(self.__black_island_id)
        cr_response = self.__modbus_rtu_client.execute(cr_request)
        print(cr_response)

        di_request = ReadDeviceDiscreteInputs(self.__black_island_id)
        di_response = self.__modbus_rtu_client.execute(di_request)
        print(di_response)

        hrr_request = ReadDeviceHoldingRegisters(self.__black_island_id)
        hrr_response = self.__modbus_rtu_client.execute(hrr_request)
        print(hrr_response)

        irr_request = ReadDeviceInputRegisters(self.__black_island_id)
        irr_response = self.__modbus_rtu_client.execute(irr_request)
        print(irr_response)

        cw_request = WriteDeviceCoils(self.__black_island_id)
        cw_response = self.__modbus_rtu_client.execute(cw_request)
        print(cw_response)

        hrw_request = WriteDeviceRegisters(self.__black_island_id)
        hrw_response = self.__modbus_rtu_client.execute(hrw_request)
        print(hrw_response)

        return True

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

        state = False

        if self.__modbus_rtu_client is None:
            return False

        state = self.__update_black_island()

        return state

    def digital_read(self, pin):
        """Read the digital input pin.

        Args:
            pin (int): Pin index.

        Returns:
            int: State of the pin.
        """

        self.__logger.debug("digital_read({}, {})".format(self.model, pin))

        return False

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

        self.__logger.debug("digital_write({}, {}, {})".format(self.model, pin, value))

        return False

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

        self.__logger.debug("analog_write({}, {}, {})".format(self.model, pin, value))

        return 0

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

        self.__logger.debug("analog_read({}, {})".format(self.model, pin))

        return 0

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

        self.__logger.debug("set_led({}, {}, {})".format(self.model, pin, value))

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

        self.__logger.debug("read_temperature({}, {}, {})".format(self.model, dev, circuit))

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

        self.__logger.debug("get_1w_devices({})".format(self.model))

        return []

    def get_device(self, dev, circuit):
        """Get device.

        Returns:
            [type]: [description]
        """

        self.__logger.debug("get_device({}, {}, {})".format(self.model, dev, circuit))

        device = None

        if dev == "1wdevice":
            device = {"vis": 0.0}

        return device