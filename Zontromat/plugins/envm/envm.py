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
from datetime import datetime

from plugins.base_plugin import BasePlugin

# https://github.com/s-bear/sun-position
# from sunposition import sunpos
# from plugins.envm.sunposition import sunpos
from plugins.envm.sunposition2 import sunpos

from devices.factories.pir.pir_factory import PIRFactory

from utils.logger import get_logger
from utils.logic.timer import Timer

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

#endregion

#region Constructor / Destructor

    def __init__(self, config):
        """Constructor"""

        super().__init__(config)

        self.__identifier = 1
        if "identifier" in config:
            self.__identifier = config["identifier"]

        self.__logger = None
        """Logger
        """

        self.__update_timer = None
        """Update timer.
        """

        self.__sunpos_enabled_value = False
        """Sun position local calculation enabled.
        """

        self.__location_lat = 0.0
        """Location latitude.
        """

        self.__location_lon = 0.0
        """Location longitude.
        """

        self.__location_elv = 0.0
        """Location elevation.
        """

        self.__time_zone = 0
        """Location time zone.
        """

        self.__temperature = 0
        """Temperature
        """

        self.__pirs = {}
        """PIR sensors in the zone.
        """

        self.__pirs_states = {}
        """PIR sensors in the zone states.
        """

        self.__pirs_activations = {}
        """PIR sensors in the zone activations.
        """

        self.__win_tamps = {}
        """Windows tampers in the zone.
        """

        self.__win_tamps_states = {}
        """Windows tampers in the zone activations.
        """

        self.__win_tamps_activations = {}
        """Windows tampers in the zone.
        """

        self.__activations_count = 2
        """Activations count:
            - One for current state
            - One for last state.
        """

#endregion

#region Private Methods (PLC)

    def __read_win_tamper(self, pin):

        state = False

        if self._controller.is_valid_gpio(pin):
            state = self._controller.digital_read(pin)

        return state

    def __update_win_tamps(self):

        # If windows tampers are not none.
        if self.__win_tamps is not None:
            # For each window tamper in list get.
            for pin in self.__win_tamps:
                # Get window tamper state.
                state = self.__read_win_tamper(pin)
                # If window tamper state is different in previous moment.
                if self.__win_tamps_states[pin] != state:
                    # Save new state from this moment.
                    self.__win_tamps_states[pin] = state
                    # If window tamper state is true (activated).
                    if state == True:
                        # Save time that has been activated.
                        self.__win_tamps_activations[pin].append(time.time())

                # Remove the oldest activation.
                if len(self.__win_tamps_activations[pin]) > self.__activations_count:
                    self.__win_tamps_activations[pin].pop(0)

    def __update_pirs(self):

        # If PIRs are not none.
        if self.__pirs is not None:
            # For each PIR in list get.
            for pir in self.__pirs:
                # Get PIR state.
                state = self.__pirs[pir].get_motion()
                # If PIR state is different in previous moment.
                if self.__pirs_states[pir] != state:
                    # Save new state from this moment.
                    self.__pirs_states[pir] = state
                    # If PIR state is true (activated).
                    if state == True:
                        # Save time that has been activated.
                        self.__pirs_activations[pir].append(time.time())

                # Remove the oldest activation.
                if len(self.__pirs_activations[pir]) > self.__activations_count:
                    self.__pirs_activations[pir].pop(0)

#endregion

#region Private Methods

    def __old_sunpos(self):
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

        return azm.item(0), zen.item(0)

    def __new_sunpos(self):
        
        now = datetime.now()
        
        # Close Encounters latitude, longitude
        location = (self.__location_lat, self.__location_lon)
        
        # Fourth of July, 2022 at 11:20 am MDT (-6 hours)
        when = (now.year, now.month, now.day, now.hour, now.minute, now.second, self.__time_zone) # ,,19/2022.08.04/16:31
        
        # Get the Sun's apparent location in the sky
        azimuth, elevation = sunpos(when, location, True)
        
        # # Output the results
        # print("\nWhen: ", when)
        # print("Where: ", location)
        # print("Azimuth: ", azimuth)
        # print("Elevation: ", elevation)

        return azimuth, elevation

    def __calculate_position(self):
        """Calculate sun position.
        """

        # elv_out, azm_out = self.__old_sunpos()
        azm_out, elv_out = self.__new_sunpos()

        # self.__logger.info(f"Azimuth: {azm:.2f}; Elevation: {elv:.2f}")
        # print(f"SunPos -> Azm: {azm_out:.2f}; Elev: {elv_out:.2f}")

        # Update sun location.
        self.__azimuth = azm_out
        self.__elevation = elv_out

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

    def __pir_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {}:
            if self.__pirs is not None:
                for pir in self.__pirs:
                    self.__pirs[pir].shutdown()
                self.__pirs.clear()

            for pir in register.value:
                self.__pirs[pir] = PIRFactory.create(
                    controller=self._controller,
                    name=register.description,
                    vendor=register.value['vendor'],
                    model=register.value['model'],
                    options=register.value['options'])
                self.__pirs_activations[pir] = []

            if self.__pirs is not None:
                for pir in self.__pirs:
                    self.__pirs[pir].init()

        elif register.value == {}:
            if self.__pirs is not None:
                for pir in self.__pirs:
                    self.__pirs[pir].shutdown()
                self.__pirs.clear()

    def __win_tamp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {}:
            if self.__win_tamps is not None:
                self.__win_tamps.clear()

            self.__win_tamps = register.value

        elif register.value == {}:
            if self.__win_tamps is not None:
                self.__win_tamps.clear()

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

        pir_settings = self._registers.by_name("envm.pir.settings")
        if pir_settings is not None:
            pir_settings.update_handlers = self.__pir_settings_cb
            pir_settings.update()

        window_tamper = self._registers.by_name("envm.window_tamper.settings")
        if window_tamper is not None:
            window_tamper.update_handlers = self.__win_tamp_settings_cb
            window_tamper.update()

    def __set_sunpos(self):
        """Set sun position.
        """

        self._registers.write("envm.sun.elevation", self.__elevation)
        self._registers.write("envm.sun.azimuth", self.__azimuth)

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__update_timer = Timer(1)

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

            self.__update_pirs()

            self.__update_win_tamps()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
