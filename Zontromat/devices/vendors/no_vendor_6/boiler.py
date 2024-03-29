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

class Boiler(BaseDevice):
    """Boiler.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __heat = 0
    """Debit of the pump.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_heat(self, heat):
        """Heater setpoint
        """

        self.__heat = heat

        self.__logger.debug("Set the heat of {} to {}".format(self.name, self.__heat))

    def init(self):

        self.__logger.debug("Init the: {}".format(self.name))

    def shutdown(self):

        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):

        self.__logger.debug("The heat of {} is {}.".format(self.name, self.__heat))

#endregion
