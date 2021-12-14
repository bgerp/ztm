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

from plugins.base_plugin import BasePlugin

# https://github.com/s-bear/sun-position
# from sunposition import sunpos
from plugins.envm.sunposition import sunpos

from utils.logger import get_logger
from utils.logic.timer import Timer

from data import verbal_const

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

__class_name__ = "Environment"
"""Plugin class name."""

#endregion

class Environment(BasePlugin):
    """Environment control and provisioning."""

#region Attributes

    __logger = None
    """Logger"""

    __update_timer = None
    """Update timer."""

    __sunpos_enabled_value = False
    """Sun position local calculation enabled."""

    __location_lat = 0.0
    """Location latitude.
    """

    __location_lon = 0.0
    """Location longitude.
    """

    __location_elv = 0.0
    """Location elevation.
    """

    __time_zone = 0
    """Location time zone.
    """

    __temperature = 0
    """Temperature
    """

#endregion

#region Private Methods (Registers)

    def __sunpos_enabled_cb(self, register):
        """Sun position calculation enable flag handler.

        Args:
            register (Register): The register.
        """

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__sunpos_enabled_value != register.value:
            self.__sunpos_enabled_value = register.value

    def __location_lat_cb(self, register):
        """Get latitude of the building.

        Args:
            register (Register): The register.
        """

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__location_lat != register.value:
            self.__location_lat = register.value

    def __location_lon_cb(self, register):
        """Get longitude of the building.

        Args:
            register (Register): The register.
        """

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__location_lon != register.value:
            self.__location_lon = register.value

    def __location_elv_cb(self, register):
        """Get elevation of the building.

        Args:
            register (Register): The register.
        """

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__location_elv != register.value:
            self.__location_elv = register.value

    def __time_zone_cb(self, register):
        """Get time zone.

        Args:
            register (Register): The register.
        """

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__time_zone != register.value:
            self.__time_zone = register.value

    def __temperature_cb(self, register):
        """Get environment temperature.

        Args:
            register (Register): The register.
        """

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__temperature != register.value:
            self.__temperature = register.value

    def __init_registers(self):

        # Software sun position enabled.
        # sunpos_enabled = self._registers.by_name(self.key + ".sunpos.enabled")
        sunpos_enabled = self._registers.by_name("envm.sunpos.enabled")
        if sunpos_enabled is not None:
            sunpos_enabled.update_handlers = self.__sunpos_enabled_cb
            sunpos_enabled.update()

        location_lat = self._registers.by_name("envm.building.location.lat")
        if location_lat is not None:
            location_lat.update_handlers = self.__location_lat_cb
            location_lat.update()

        location_lon = self._registers.by_name("envm.building.location.lon")
        if location_lon is not None:
            location_lon.update_handlers = self.__location_lon_cb
            location_lon.update()

        location_elv = self._registers.by_name("envm.building.location.elv")
        if location_elv is not None:
            location_elv.update_handlers = self.__location_elv_cb
            location_elv.update()

        time_zone = self._registers.by_name("envm.building.location.time_zone")
        if time_zone is not None:
            time_zone.update_handlers = self.__time_zone_cb
            time_zone.update()

        temperature = self._registers.by_name("envm.temp.actual")
        if temperature is not None:
            temperature.update_handlers = self.__temperature_cb
            temperature.update()

    def __set_sunpos(self):
        """Set sun position.
        """

        self._registers.write("envm.sun.elevation", self.__elevation)
        self._registers.write("envm.sun.azimuth", self.__azimuth)

#endregion

#region Private Methods

    def __calculate_position(self):
        """Calculate sun position.
        """

        # https://www.suncalc.org/#/43.0781,25.5955,17/2021.05.07/11:09/1/1

        # Latitude of the target.
        lat = self.__location_lat

        # Longitude of the target.
        lon = self.__location_lon

        # Elevation, in meters.
        # It is formed by the sum of altitude in [m] + height of the object (building) in [m]
        elv = self.__location_elv

        # Temperature, in degrees celsius.
        temp = self.__temperature

        # Atmospheric pressure, in millibar.
        presure = 1013.0

        # Difference between earth\'s rotation time (TT) and universal time (UT1).
        diff_time = 3600 * self.__time_zone

        # Output in radians instead of degrees.
        mou = False

        # Get sun position.
        time_now = datetime.now()

        azm, zen, ra, dec, h = sunpos(time_now, lat, lon, elv, temp, presure, diff_time, mou)
        elv_out = 90 - zen - 2
        azm_out = azm

        # self.__logger.info(f"Azimuth: {azm:.2f}; Elevation: {elv:.2f}")
        # print(f"SunPos -> Azm: {azm_out:.2f}; Elev: {elv_out:.2f}")

        # Update sun location.
        self.__azimuth = azm_out
        self.__elevation = elv_out

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__update_timer = Timer(2)

        self.__init_registers()

    def _update(self):
        """Update the plugin.
        """

        self.__update_timer.update()
        if self.__update_timer.expired:
            self.__update_timer.clear()

            if self.__sunpos_enabled_value:
                self.__calculate_position()
                self.__set_sunpos()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
