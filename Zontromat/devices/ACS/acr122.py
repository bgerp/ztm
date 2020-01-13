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

class ACR122():
    """ACR122 NFC Card Reader"""

    def __init__(self, config):
        """Constructor

        Args:
            config (mixed): Device configuration.
            neuron (Neuron): Neuron instance.
        """

        # from devices.device_factory import DeviceFactory

        self.__logger = get_logger(__name__)

        self.__config = config

        # params = self.__config["params"]

        # if "speed_limit" in params:
        #     self.speed_limit = params["speed_limit"]

        # if "analog_output" in params:
        #     analog_output = params["analog_output"]
        #     self.__analog_output = DeviceFactory.get_device(analog_output)
        #     self.__analog_output.init()


    def init(self):
        """Initialize the device."""

        pass

    def update(self):
        """Update the device."""

        pass

    def shutdown(self):
        """Shutdown the device."""

        pass

    def get_state(self):
        """Return device state."""

        return None

    def set_state(self, state):
        """Set device state."""

        pass