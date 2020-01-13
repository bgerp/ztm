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

from plugins.base_plugin import BasePlugin

from devices.PT.blnd import BLND

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

class Blinds(BasePlugin):
    """Blinds controller device."""

#region Attributes

    __logger = None
    """Logger"""

    __blinds = None
    """"""

    __parameters_values = []
    """Parameters values."""

    __registers_ids = None
    """Registers IDs."""

#endregion

#region Public Methods

    def init(self):

        self.__logger = get_logger(__name__)

        if self._config["vendor"] == "PT":

            if self._config["model"] == "M1":
                self.__blinds = BLND()

        self.__registers_ids = self.__blinds.get_registers_ids()

    def update(self):

        # "blinds.sun.elevation.value": 0,
        # "blinds.sun.elevation.mou": "deg",
        # "blinds.sun.azimuth.value": 0,
        # "blinds.sun.azimuth.mou": "deg",

        # "blinds.sub_dev.register_type": "inp"

        # Get parameters
        uart = self._config["uart"] # 2
        device_id = self._config["dev_id"] # 3

        registers_values = self._controller.read_mb_registers(uart, device_id, self.__registers_ids)

        # Validate
        is_valid = True
        for index in registers_values:
            if registers_values[index] is None:
                is_valid = False
                break

        if is_valid:
            # Convert values to human readable.
            __parameters_values = self.__blinds.get_parameters_values(registers_values)

    def get_state(self):
        """Returns the state of the device.

        Returns
        -------
        mixed
            State of the device.
        """

        return None

#endregion
