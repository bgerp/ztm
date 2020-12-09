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

from plugins.base_plugin import BasePlugin
from plugins.hvac.air_conditioner import AirConditioner

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

class HVAC(BasePlugin):
    """Heating ventilation and air conditioning."""

#region Attributes

    __logger = None
    """Logger"""

    __thermal_zones = None
    """Therml zones."""

#endregion

#region Destructor

    def __del__(self):
        """Destructor"""

        if self.__logger is not None:
            del self.__logger

        if self.__thermal_zones is not None:
            del self.__thermal_zones

#endregion

#region Public Methods

    def init(self):
        """Init the HVACs."""

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__thermal_zones = []

        ac1 = AirConditioner(\
            registers=self._registers, controller=self._controller,\
            identifier=1, key=self._key, name="AC")
        self.__thermal_zones.append(ac1)

        for ac in self.__thermal_zones:
            ac.init()


    def update(self):
        """ Update cycle. """

        for ac in self.__thermal_zones:
            ac.update()

    def shutdown(self):
        """Shutdown the tamper."""

        self.__logger.info("Shutting down the {}".format(self.name))
        
        for ac in self.__thermal_zones:
            ac.shutdown()

        if __thermal_zones is not None:
            del __thermal_zones

#endregion
