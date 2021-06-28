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

from utils.configuarable import Configuarable

from data import verbal_const

from controllers.utils.resource_identifiers import Identifiers
from controllers.utils.pin_modes import PinModes

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

class BaseController(Configuarable):
    """Base controller"""

#region Attributes

    _gpio_map = {}
    """GPIO map"""

    _delimiter = ":"

#endregion

#region Constructor

    def __init__(self, config):
        """Constructor"""

        super().__init__(config)

    def __str__(self):
        """Returns controller vendor and model as string.

        Returns:
            str: Short description.
        """
        return "Controller vendor({}) / model({}) ".format(self.vendor, self.model)

    __repr__ = __str__

#endregion

#region Properties

    @property
    def vendor(self):
        """Get device vendor.

        Returns
        -------
        str
            Vendor
        """

        return None

    @property
    def model(self):
        """Get device model.

        Returns
        -------
        str
            Model
        """

        return None

    @property
    def serial_number(self):
        """Get device serial number.

        Returns
        -------
        str
            Serial number.
        """

        return None

#endregion

#region Public Methods

    def is_valid_gpio_type(self, gpio):
        """Is valid GPIO type"""

        return gpio is not None and gpio != ""

    def is_valid_remote_gpio(self, gpio):
        """[summary]

        Args:
            gpio (str): Remote GPIO description
            U1.M1.DI2 -> UART 1; Modbus ID 1; Digital Input 2

        Raises:
            SyntaxError: [description]
            SyntaxError: [description]
            SyntaxError: [description]
            ValueError: [description]
            ValueError: [description]
            SyntaxError: [description]
            ValueError: [description]
            ValueError: [description]
            ValueError: [description]

        Returns:
            [bool]: True - Valid syntax; False Invalid syntax.
        """

        # Capitalize the target.
        io_name = gpio.upper()

        # Remove flip sign.
        io_name = io_name.replace("!", "")

        # Chaeck for splitter symbiol.
        has_delimiter = (self._delimiter in io_name)

        if not has_delimiter:
        #     raise SyntaxError("No delimiter symbol included.") 
            return False

        # Split the target in to chunks.
        chunks = io_name.split(self._delimiter)

        # Get the chunks length.
        chunks_count = len(chunks)

        if chunks_count != 4:
            # raise SyntaxError("Invalid chunks count must be 3. OR Invalid place of the delimiter.")
            return False

        # Check for UART identifier.
        has_uart_identifier = "U" in chunks[Identifiers.UART.value]
        if not has_uart_identifier:
            # raise SyntaxError("UART identifier should be provided. (U1)")
            return False

        # Get the UART identifier.
        uart_identifier = chunks[Identifiers.UART.value].replace("U", "")

        if uart_identifier == "":
            # raise ValueError("UART identifier should be U0 to U255.")
            return False

        uart_identifier = int(uart_identifier)

        # Validate the MODBUS range.
        valid_uart_identifier = (uart_identifier > -1) and (uart_identifier <= 247)

        if not valid_uart_identifier:
        #     raise ValueError("MODBUS identifier should be M1 to M247.")
            return False

        # Check for MODBUS identifier.
        has_mb_identifier = "ID" in chunks[Identifiers.ID.value]

        if not has_mb_identifier:
        #     raise SyntaxError("MODBUS identifier should be provided. (M1)")
            return False

        # Get the MODBUS identifier.
        mb_identifier = chunks[Identifiers.ID.value].replace("ID", "")

        if mb_identifier == "":
        #     raise ValueError("MODBUS identifier should be M1 to M254.")
            return False

        mb_identifier = int(mb_identifier)

        # Validate the MODBUS range.
        valid_mb_identifier = (mb_identifier > 0) and (mb_identifier <= 247)

        if not valid_mb_identifier:
        #     raise ValueError("MODBUS identifier should be M1 to M254.")
            return False

        # Disable mapping check.
        disable_mapping = True

        # Check does the GPIO is part of the map.
        has_io_identifier = False
        for item in self._gpio_map:
            if chunks[Identifiers.IO.value] in item:
                has_io_identifier = True
                break

        if not (has_io_identifier or disable_mapping):
        #     raise ValueError("Target IO is not part of the mapping.")
            return False

        # Combine all requirements to one expresion.
        valid = has_delimiter and (chunks_count == 4) and \
            has_uart_identifier and valid_uart_identifier and \
            has_mb_identifier and valid_mb_identifier and (has_io_identifier or disable_mapping)

        # Return the result.
        return valid

    def is_off_gpio(self, gpio):
        """Is not OFF"""

        return gpio == verbal_const.OFF

    def is_existing_gpio(self, gpio):
        """Is part of the GPIO definitions"""

        return gpio in self._gpio_map

    def is_valid_gpio(self, gpio):
        """Complex check is it valid."""

        is_off_gpio = not self.is_off_gpio(gpio)
        is_existing_gpio = self.is_existing_gpio(gpio)
        is_valid_gpio_type = self.is_valid_gpio_type(gpio)
        valid_remote_gpio = self.is_valid_remote_gpio(gpio)

        result = (is_off_gpio\
            and is_existing_gpio\
            and is_valid_gpio_type) or valid_remote_gpio

        return result

    def parse_remote_gpio(self, gpio):

        io_name = gpio.upper()

        # Remove flip identification.
        io_name = io_name.replace("!", "")

        # Split in to chunks.
        chunks = io_name.split(self._delimiter)

        # Get UART identifier.
        uart = chunks[Identifiers.UART.value].replace("U", "") 
        uart = int(uart)

        # Get MODBUS identifier.
        mb_id = chunks[Identifiers.ID.value].replace("ID", "")
        mb_id = int(mb_id)

        # Get MODBUS register.
        io_reg = chunks[Identifiers.REG.value].replace("R", "")
        io_reg = int(io_reg)

        # Get IO identifier.
        io_identifier = chunks[Identifiers.IO.value]

        # Get IO type.
        io_type = "".join([i for i in io_identifier if not i.isdigit()])

        # Validate IO type.
        valid_io_type = False
        for pin_mode in PinModes:
            if pin_mode.name == io_type:
                valid_io_type = True
                break

        if not valid_io_type:
            raise TypeError("Invalid IO type.")

        # Get IO index.
        io_index = int("".join(filter(str.isdigit, io_identifier)))

        # Create data structure that holds the MODBUS identifier, IO type and IO index.
        identifier = {"uart": uart, "mb_id": mb_id, "io_reg": io_reg, "io_type": io_type, "io_index": io_index}

        return identifier

    def get_gpio_map(self):
        """Return GPIO map.
        """

        return self._gpio_map

#endregion

#region Public Virtual Methods

    def init(self):
        """Initialize the controller.
        """

    def update(self):
        """Update controller state.
        """

    def pin_mode(self, pin, mode):
        """Set the pin mode.

        Parameters
        ----------
        pin : str
            Pin index.

        mode : mixed
            Pin index.

        Returns
        -------
        int
            State of the device.
        """

    def digital_read(self, pin):
        """Read the digital input pin.

        Parameters
        ----------
        pin : str
            Pin index.

        Returns
        -------
        int
            State of the pin.
        """

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

    def analog_read(self, pin):
        """Read the analog input pin.

        Parameters
        ----------
        pin : str
            Pin index.

        Returns
        -------
        int
            State of the pin.
        """

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

    def get_1w_devices(self):
        """Gets all possible 1W devices connected to the controller.

        Returns
        -------
        tuple
            All 1W devices connected to the controller.
        """

    def execute_mb_request(self, request):
        """Execute modbus request.

        Args:
            request (ModbusRequest): PyMODBUS request instance.

        Returns:
            ModbusResponse: PyMODBUS response instance.
        """

#endregion
