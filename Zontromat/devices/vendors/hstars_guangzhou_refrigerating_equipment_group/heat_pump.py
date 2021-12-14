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

from enum import Enum

from utils.logger import get_logger

from devices.base_device import BaseDevice

# (Request from mail: Eml6429)

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

class HeatPumpMode(Enum):
    """Heat pumps mode.
    """

    NONE = 0
    Summer = 1
    Winter = 2

class HeatPump(BaseDevice):
    """Heat pump description. (40STD-N420WHSB4)
    """

#region Attributes

    __logger = None
    """Logger
    """

    __mode = HeatPumpMode.NONE
    """Mode of the heat pump.
    """

    __power = 0
    """Power of the pump.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self._vendor = "Hstars Guangzhou Refrigerating Equipment Group.Co.,Ltd"

        self._model = "40STD-N420WHSB4"

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_mode(self, mode):
        """Set heat pump mode.

        Args:
            mode (HeatPumpMode): Heat pump mode.
        """

        if self.__mode == mode:
            return

        self.__mode = mode

        self.__logger.debug(self.__mode.name)

    def set_power(self, power):
        """Set heat pump power.

        Args:
            power (int): Power of the machine.
        """

        if self.__power == power:
            return

        self.__power = power

        self.__logger.debug(self.__power)

    def init(self):
        """Initialize the heat pump.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

    def shutdown(self):
        """Shutdown the heat pump.
        """

        self.set_power(0)
        self.__logger.debug("Shutdown the: {}".format(self.name))

#endregion
