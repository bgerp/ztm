
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

    __position = -1
    """Position of the valve."""

#endregion

#region Constructor

    def init(self):
        """Init the module."""

        self.__logger = get_logger(__name__)

#endregion

#region Public Methods

    def set_state(self, position):
        """Set position of the output.

        Args:
            position (int): Output position.
        """

        if position > 10:
            position = 10

        if position < 0:
            position = 0

        if self.__position == position:
            return

        self.__position = position

        output = self._config["output"]

        # Determin is it analog or digital output.
        if "D" in output:
            self._controller.digital_write(output, self.__position)

        if "R" in output:
            self._controller.digital_write(output, self.__position)

        elif "А" in output:
            self._controller.analog_write(output, self.__position)

        self.__logger.debug("Name: {}; Value: {}".format(self.name, self.__position))

#endregion
