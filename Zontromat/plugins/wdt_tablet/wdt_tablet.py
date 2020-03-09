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

import time

from utils.logger import get_logger

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

class WDTTablet(BasePlugin):
    """Power meter device."""

#region Attributes

    __logger = None
    """Logger"""

    __pulse_time = 1
    """Pulse time"""

    __reset_flag = False
    """Reset flag."""

    __output_state = False
    """Output state."""

    __clear_flag = True
    """Claer flag."""

    __last_timestamp = 0
    """Last timestamp"""

    __output = "DO2"
    """Digital output index."""

#endregion

#region Private Methods

    def __set_output(self, state):
        """Returns the state of the device.

        Returns
        -------
        mixed
            State of the device.
        """

        self._controller.digital_write(self.__output, state)

    def __wdt_tablet_reset(self, register):
        if register.value == 1:
            register.value = 0
            self.reset_device()

#endregion

#region Public Methods

    def init(self):

        # Create logger.
        self.__logger = get_logger(__name__)

        # Get time to open the latch.
        if "pulse_time" in self._config:
            self.__pulse_time = self._config["pulse_time"]

        # Create exit button.
        if "output" in self._config:
            self.__output = self._config["output"]

        self.__set_output(0)

    def update(self):

        if self.__reset_flag and not self.__clear_flag:

            if not self.__output_state:
                self.__set_output(1)
                self.__output_state = True
                self.__last_timestamp = time.time()

            if self.__output_state:

                passed_time = time.time() - self.__last_timestamp

                if passed_time > self.__pulse_time:
                    self.__set_output(0)
                    self.__clear_flag = True
                    self.__output_state = False
                    self.__reset_flag = False
                    self.__last_timestamp = time.time()

        if self.__clear_flag and not self.__reset_flag:
            passed_time = time.time() - self.__last_timestamp
            if passed_time > self.__pulse_time * 2:
                self.__clear_flag = False

    def reset_device(self):
        """Reset device power."""

        if not self.__reset_flag and not self.__output_state:
            self.__reset_flag = True

    def shutdown(self):

        self.__set_output(0)

    def get_state(self):
        """Return device state."""

        return self.__reset_flag

#endregion
