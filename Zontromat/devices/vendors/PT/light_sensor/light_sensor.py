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

from data import verbal_const

from utils.logic.functions import l_scale

from devices.factories.light_sensor.base_light_sensor import BaseLightSensor

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

class LightSensor(BaseLightSensor):
    """Light sensor."""

#region Attributes

    __analog_input = verbal_const.OFF
    """Sensor analog input.
    """

    __state = 0
    """Value from the input.
    """

#endregion

#region Public Methods

    def init(self):
        """Init the sensor.
        """

        self._vendor = "POLYGONTeam"

        self._model = "MI"

        self.__analog_input = self._config["analog_input"]

    def update(self):
        """Update sensor data.
        """

        self.__state = self._controller.analog_read(self.__analog_input)

    def get_value(self):
        """Get value.
        """

        # Add scaling coefficient.
        raw = l_scale(self.__state["value"], [0, 10], [0, 15000])

        return raw

#endregion
