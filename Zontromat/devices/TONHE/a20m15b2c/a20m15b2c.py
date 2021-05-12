
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

class A20M15B2C(BaseDevice):
    """Hydro Valve. Model: A20-M15-B2-C"""

#region Attributes

    __logger = None
    """Logger"""

    __position = -1
    """Position of the valve."""

    __min_pos = 0
    """Minimum allowed position."""

    __max_pos = 100
    """Maximum allowed position."""

    __feedback = None
    """Feedback of the valve position."""

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

        in_value = value

        if value > 100:
            in_value = 100

        if value < 0:
            in_value = 0

        if in_value > self.max_pos:
            in_value = self.max_pos

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

        in_value = value

        if value > 100:
            in_value = 100

        if value < 0:
            in_value = 0

        if value < self.min_pos:
            in_value = self.min_pos

        self.__max_pos = in_value

    @property
    def set_point(self):
        """Set point."""

        return self.__position

#endregion

#region Public Methods

    def init(self):
        """Init the module."""

        self.__logger = get_logger(__name__)

        if "min_pos" in self._config:
            self.min_pos = self._config["min_pos"]

        if "max_pos" in self._config:
            self.max_pos = self._config["max_pos"]

        if "feedback" in self._config:
            self.__feedback = self._config["feedback"]

        if "output" in self._config:
            self.__output = self._config["output"]

    def get_pos(self):
        """Set position of the output.

        Args:
            position (int): Output position.
        """

        position = 0

        # Determin is it analog or digital output.
        if "D" in self.__feedback:
            position = self._controller.digital_read(self.__feedback)

        elif "A" in self.__feedback:
            position = self._controller.analog_read(self.__feedback)

        self.__logger.debug("Name: {}; Position: {:3.3f}".format(self.name, position))

        return position * 10.0

    def set_pos(self, position):
        """Set position of the output.

        Args:
            position (int): Output position.
        """

        if self.__position == position:
            return

        in_position = position

        if position > 100:
            in_position = 100

        if position > self.__max_pos:
            in_position = self.__max_pos

        if position < 0:
            in_position = 0

        if position < self.__min_pos:
            in_position = self.__min_pos

        self.__position = in_position

        # Determin is it analog or digital output.
        if "D" in self.__output:

            if self.__position > 50:
                self._controller.digital_write(self.__output, 1)

            else:
                self._controller.digital_write(self.__output, 0)

        if "R" in self.__output:

            if self.__position > 50:
                self._controller.digital_write(self.__output, 1)

            else:
                self._controller.digital_write(self.__output, 0)

        elif "A" in self.__output:
            value_pos = self.__position / 10
            self._controller.analog_write(self.__output, value_pos)

        self.__logger.debug("Name: {}; Position: {}".format(self.name, self.__position))

    def in_place(self):
        """Returns if the valve is in place."""

        in_place = False

        actual_pos = self.get_pos()
        target_pos = self.set_point

        delta = abs(actual_pos - target_pos)

        if delta < 0.1:
            in_place = True

        return in_place

    def shutdown(self):
        """Shutdown"""

        self.min_pos = 0
        self.set_pos(0)

#endregion

#region Public Static Methods

    @staticmethod
    def create(name, key, registers, controller):
        """Create instance of the class."""

        instance = None

        valve_output = registers.by_name(key + ".output").value
        valve_fb = registers.by_name(key + ".feedback").value
        max_pos = registers.by_name(key + ".max_pos").value
        min_pos = registers.by_name(key + ".min_pos").value

        config = \
        {\
            "name": name,
            "output": valve_output,
            "feedback": valve_fb,
            "min_pos": min_pos,
            "max_pos": max_pos,
            "controller": controller
        }

        instance = A20M15B2C(config)

        return instance

#endregion
