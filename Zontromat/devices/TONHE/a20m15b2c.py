
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

class A20M15B2C(BaseDevice):
    """Hydro Valve"""

#region Attributes

    __logger = None
    """Logger"""

    __position = 0
    """Position of the valve."""

    __min_pos = 10
    """Minimum allowed position."""

    __max_pos = 10
    """Maximum allowed position."""

    __output = None
    """Output physical signal."""

#endregion

#region Properties

    @property
    def min_pos(self):
        """Minimum position.

        Returns:
            float: Minimum position.
        """
        return self.__min_pos

    @min_pos.setter
    def min_pos(self, value):
        """Minimum position.

        Args:
            value (float): Minimum position.
        """

        if value < 0:
            value = 0

        self.__min_pos = value

    @property
    def max_pos(self):
        """Maximum position.

        Returns:
            float: Maximum position.
        """
        return self.__max_pos

    @max_pos.setter
    def max_pos(self, value):
        """Maximum position.

        Args:
            value (float): Maximum position.
        """

        if value > 10:
            value = 10

        self.__max_pos = value

    @property
    def position(self):
        return self.__position

#endregion

#region Public Methods

    def init(self):
        """Init the module."""

        self.__logger = get_logger(__name__)

        if "max_pos" in self._config:
            self.max_pos = self._config["max_pos"]

        if "min_pos" in self._config:
            self.min_pos = self._config["min_pos"]

        if "output" in self._config:
            self.__output = self._config["output"]

    def set_pos(self, position):
        """Set position of the output.

        Args:
            position (int): Output position.
        """

        # if self.__position == position:
        #     return

        if position > 10:
            position = 10

        if position > self.__max_pos:
            position = self.__max_pos

        if position < 0:
            position = 0

        if position < self.__min_pos:
            position = self.__min_pos

        self.__position = position

        # Determin is it analog or digital output.
        if "D" in self.__output:
            self._controller.digital_write(self.__output, self.__position)

        if "R" in self.__output:
            self._controller.digital_write(self.__output, self.__position)

        elif "A" in self.__output:
            self._controller.analog_write(self.__output, self.__position)

        self.__logger.debug("Name: {}; Value: {}".format(self.name, self.__position))

    def shutdown(self):
        """Shutdown"""

        self.min_pos = 0
        self.set_pos(0)

#endregion

#region Public Static Methods

    @classmethod
    def create(self, name, key, registers, controller):
        """Value of the thermometer."""

        instance = None

        valve_output = registers.by_name(key + ".output").value

        config = \
        {\
            "name": name,
            "output": valve_output,
            "controller":controller
        }

        instance = A20M15B2C(config)

        return instance

#endregion
