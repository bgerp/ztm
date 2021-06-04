
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

class BaseFan(BaseDevice):
    """Fan base class."""

#region Attributes

    _min_speed = 0
    """Minimum speed limit."""

    _max_speed = 100
    """Minimum speed limit."""

    _speed = -1
    """Speed"""

#endregion

#region Properties

    @property
    def min_speed(self):
        """Minimum speed limit.

        Returns:
            float: Minimum speed limit.
        """
        return self._min_speed

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

        self._min_speed = in_value

    @property
    def max_speed(self):
        """Maximum speed limit.

        Returns:
            float: Maximum speed limit.
        """
        return self._max_speed

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

        self._max_speed = in_value

    @property
    def speed(self):
        """Get speed of the fan.

        Returns:
            int: Output speed of the fan.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """Set speed of the fan.

        Args:
            value (int): Output speed of the fan.
        """

        if self._speed == value:
            return

        in_value = value

        if value > 100:
            in_value = 100

        if value > self.max_speed:
            in_value = self.max_speed

        if value < 0:
            in_value = 0

        if value < self.min_speed:
            in_value = self.min_speed

        self._speed = in_value

#endregion

#region Constructor

    def __init__(self, config):

        super().__init__(config)

        if "max_speed" in config:
            self.max_speed = config["max_speed"]

        if "min_speed" in config:
            self.min_speed = config["min_speed"]

    def __str__(self):

        return "{} @ {:3.3f}".format(self.name, self.speed)

    __repr__ = __str__

#endregion

#region Public Methods

#endregion
