
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

    __speed_limit_value = 100
    """Speed limit."""

#endregion

#region Properties

    @property
    def speed_limit(self):
        """Speed limit.

        Returns:
            float: Speed limit.
        """
        return self.__speed_limit_value

    @speed_limit.setter
    def speed_limit(self, value):
        """Speed limit.

        Args:
            value (float): Speed limit.
        """

        self.__speed_limit_value = value

#endregion

#region Constructor

    def init(self):
        """Constructor

        Args:
            config (mixed): Device configuration.
            neuron (Neuron): Neuron instance.
        """

        self.__logger = get_logger(__name__)

        if "speed_limit" in self._config:
            self.speed_limit = self._config["speed_limit"]

#endregion

#region Public Methods

    def set_state(self, value):
        """Set value of the output.

        Args:
            value (int): Output value.
        """

        if value >= 100:
            value = 100

        if value >= self.speed_limit:
            value = self.speed_limit

        self._controller.analog_write(self._config["output"], value)
        self.__logger.debug("Name: {}; Value {:3.3f}".format(self.name, value))

#endregion
