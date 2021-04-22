
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

class F3P146EC072600(BaseDevice):
    """Model: F3P146-EC072-600
    
    See http://www.shidaqian.com/Upload/SDQ_ECqqlxfj/F3P146-EC072-600.PDF"""

#region Attributes

    __logger = None
    """Logger"""

    __min_speed = 0
    """Minimum speed limit."""

    __max_speed = 100
    """Minimum speed limit."""

    __speed = 0
    """Speed"""

    __output = "AO0"
    """Output physical signal."""

#endregion

#region Properties

    @property
    def min_speed(self):
        """Minimum speed limit.

        Returns:
            float: Minimum speed limit.
        """
        return self.__min_speed

    @min_speed.setter
    def min_speed(self, value):
        """Minimum speed limit.

        Args:
            value (float): Minimum speed limit.
        """

        in_value = value

        if value > 100:
            in_value = 100

        if value < 0:
            in_value = 0

        if in_value > self.max_speed:
            in_value = self.max_speed

        self.__min_speed = in_value

    @property
    def max_speed(self):
        """Maximum speed limit.

        Returns:
            float: Maximum speed limit.
        """
        return self.__max_speed

    @max_speed.setter
    def max_speed(self, value):
        """Maximum speed limit.

        Args:
            value (float): Speed limit.
        """

        in_value = value

        if value > 100:
            in_value = 100

        if value < 0:
            in_value = 0

        if value < self.min_speed:
            in_value = self.min_speed

        self.__max_speed = in_value

#endregion

#region Public Methods

    def init(self):
        """Constructor

        Args:
            config (mixed): Device configuration.
            neuron (Neuron): Neuron instance.
        """

        self.__logger = get_logger(__name__)

        if "max_speed" in self._config:
            self.max_speed = self._config["max_speed"]

        if "min_speed" in self._config:
            self.min_speed = self._config["min_speed"]

        if "output" in self._config:
            self.__output = self._config["output"]

    def set_speed(self, speed):
        """Set speed of the fan.

        Args:
            speed (int): Output speed of the fan.
        """

        in_value = speed

        if speed > 100:
            in_value = 100

        if speed > self.max_speed:
            in_value = self.max_speed

        if speed < 0:
            in_value = 0

        if speed < self.min_speed:
            in_value = self.min_speed

        if self.__speed == in_value:
            return
        
        self.__speed = in_value

        value_speed = self.__speed / 10
        self._controller.analog_write(self.__output, value_speed)
        self.__logger.debug("Name: {}; Speed {:3.3f}".format(self.name, self.__speed))

    def shutdown(self):
        """Shutdown"""

        self.min_speed = 0
        self.set_speed(0)

#endregion

#region Public Static Methods

    @staticmethod
    def create(name, key, registers, controller):
        """Value of the thermometer."""

        instance = None

        output = registers.by_name(key + ".output").value
        min_speed = registers.by_name(key + ".min_speed").value
        max_speed = registers.by_name(key + ".max_speed").value

        config = \
        {\
            "name": name,
            "output": output,
            "min_speed": min_speed,
            "max_speed": max_speed,
            "controller": controller
        }

        instance = F3P146EC072600(config)

        return instance

#endregion

 # TODO: Create test.