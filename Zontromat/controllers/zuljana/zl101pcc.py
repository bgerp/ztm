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

from utils.logger import get_logger

from controllers.base_controller import BaseController

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

    __instance = None
    """Singelton instance.
    """

    __modbus_rtu_port = None
    """MODBUS RTU RS485 port.
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

        self.__logger = get_logger(__name__)

        if "modbus_rtu_port" in config:
            self.__modbus_rtu_port = config["modbus_rtu_port"]

    def __del__(self):
        """Destructor
        """

        pass

#endregion

#region Private Methods

    def __get_hardware_id(self):

        uuid = ""

        if 'nt' in os.name:
            result = subprocess.check_output('wmic csproduct get uuid')

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

        return True

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