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

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
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

    _gpio_map = None
    """GPIO map"""

#endregion

#region Constructor

    def __init__(self, config):
        """Constructor"""

        super().__init__(config)

#endregion

#region Public Methods

    def is_valid_gpio_type(self, gpio):
        """Is valid GPIO type"""

        return gpio is not None and gpio != ""

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

        return is_off_gpio\
            and is_existing_gpio\
            and is_valid_gpio_type

    def get_gpio_map(self):
        """Return GPIO map."""

        return self._gpio_map

    def init(self):
        """Init the controller."""

    def update(self):
        """Update controller state."""

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

#endregion
