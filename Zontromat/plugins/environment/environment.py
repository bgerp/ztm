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

from datetime import datetime

# https://github.com/s-bear/sun-position
# from sunposition import sunpos
from plugins.environment.sunposition import sunpos
from plugins.base_plugin import BasePlugin

from utils.logger import get_logger
from utils.timer import Timer

from data import verbal_const

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

class Environment(BasePlugin):
    """Environment control and provisioning."""

#region Attributes

    __logger = None
    """Logger"""

    __update_timer = None
    """Update timer."""

    __sunpos_enabled_value = verbal_const.NO
    """Sun position local calculation enabled."""

#endregion

#region Private Methods

    def __sunpos_enabled(self):

        return (self.__sunpos_enabled_value != verbal_const.NO and self.__sunpos_enabled_value != "")

    def __sunpos_enabled_cb(self, register):

        # Check data type.
        if not register.is_str():
            self._log_bad_value_register(self.__logger, register)
            return

        if self.__sunpos_enabled_value != register.value:
            self.__sunpos_enabled_value = register.value

    def __calculate_position(self):

        # TODO: To add registers for current position and parameters of the building

        # Latitude of the target.
        lat = 43.07779

        # Longtitude of the target.
        lon = 25.59549

        # Elevation, in meters.
        # It is formed by the sum of altitude in [m] + heightof the object (building) in [m]
        elev = 210

        # Temperature, in degrees celcius.
        temp = 20

        # Atmospheric pressure, in millibar.
        presure = 1013.0

        # Difference between earth\'s rotation time (TT) and universal time (UT1).
        diff_time = 3600 * 2

        # Output in radians instead of degrees.
        mou = False

        # Get sun position.
        time_now = datetime.now()

        azm, zen, ra, dec, h = sunpos(time_now, lat, lon, elev, temp, presure, diff_time, mou)
        elev = 90 - zen - 2
        azm = azm - 39

        # self.__logger.info(f"Azimuth: {azm:.2f}; Elevation: {elev:.2f}")
        # print(f"SunPos -> Azm: {azm:.2f}; Elev: {elev:.2f}")

        self._registers.by_name("blinds.sun.elevation.value").value = elev
        self._registers.by_name("blinds.sun.azimuth.value").value = azm

#endregion

#region Public Methods

    def init(self):

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__update_timer = Timer(2)

        # Software sun position enabled.
        sunpos_enabled = self._registers.by_name(self._key + ".sunpos.enabled")
        if sunpos_enabled is not None:
            sunpos_enabled.update_handler = self.__sunpos_enabled_cb

    def update(self):

        self.__update_timer.update()
        if self.__update_timer.expired:
            self.__update_timer.clear()

            if self.__sunpos_enabled():
                self.__calculate_position()

            # TODO: Software update weathercast.

    def shutdown(self):
        """Shutdown the tamper."""

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
