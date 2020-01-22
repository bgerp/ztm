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

from utils.timer import Timer

from plugins.base_plugin import BasePlugin

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

class StatusLed(BasePlugin):
    """Status LED indicator device."""

#region Attributes

    __led_state = 0
    """LED State."""

    __blink_timer = None
    """Update timestamp."""

    __blink_time = 1
    """Blink time."""

#endregion

#region Public Methods

    def init(self):

        self.__blink_timer = Timer(1)

        if "blink_time" in self._config:
            self.__blink_timer.expiration_time = self._config["blink_time"]

    def update(self):

        self.__blink_timer.update()
        if self.__blink_timer.expired:
            self.__blink_timer.clear()

            if self.__led_state:
                self.__led_state = 0
            else:
                self.__led_state = 1

            self._controller.set_led(self._config["output"], self.__led_state)

    def shutdown(self):
        self._controller.set_led(self._config["output"], 0)

#endregion
