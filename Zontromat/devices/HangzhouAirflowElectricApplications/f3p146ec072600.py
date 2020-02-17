
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
from devices.base_device import BaseDevice

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

class F3P146EC072600(BaseDevice):
    """FAN"""

#region Attributes

    __logger = None
    """Logger"""

    __max_speed = 10
    """Speed limit."""

    __speed = -1
    """Speed"""

    __output = "AO0"
    """Output phizical signal."""

#endregion

#region Properties

    @property
    def max_speed(self):
        """Speed limit.

        Returns:
            float: Speed limit.
        """
        return self.__max_speed

    @max_speed.setter
    def max_speed(self, value):
        """Speed limit.

        Args:
            value (float): Speed limit.
        """

        self.__max_speed = value

#endregion

#region Constructor

    def init(self):
        """Constructor

        Args:
            config (mixed): Device configuration.
            neuron (Neuron): Neuron instance.
        """

        self.__logger = get_logger(__name__)

        if "max_speed" in self._config:
            self.max_speed = self._config["max_speed"]

        if "output" in self._config:
            self.__output = self._config["output"]


#endregion

#region Public Methods

    def set_speed(self, speed):
        """Set speed of the fan.

        Args:
            speed (int): Output speed of the fan.
        """

        if speed >= 10:
            speed = 10

        if speed < 0:
            speed = 0

        if speed >= self.max_speed:
            speed = self.max_speed

        if self.__speed == speed:
            return

        self.__speed = speed

        self._controller.analog_write(self.__output, self.__speed)
        self.__logger.debug("Name: {}; Value {:3.3f}".format(self.name, self.__speed))

#endregion
