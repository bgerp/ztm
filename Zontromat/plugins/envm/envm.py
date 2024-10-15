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
import json
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

from data import verbal_const

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

        self.__door_tamps = {}
        """Door tampers in the zone.
        """

        self.__door_tamps_states = {}
        """Door tampers in the zone activations.
        """

        self.__door_tamps_activations = {}
        """Door tampers in the zone.
        """

        self.__activations_count = 1
        """Activations count:
            - One for current state
            - One for last state.
            @28.05.2024y. The owner wants to have only one field for simplicity of the system.
        """

        self.__is_empty_timeout = 1200
        """Is empty timeout time.
            @28.05.2024y. The owner wants to set the value to 1200 seconds to start tests..
        """

        self.__mirror_output = {}
        """Mirror outputs.
        """

#endregion

#region Private Methods (PLC)

    def __update_pirs(self):

        # If PIRs are not none.
        if self.__pirs is not None:
            # For each PIR in list get.
            for pir in self.__pirs:

                # Initialise the arrays.
                if not pir in self.__pirs_states:
                    self.__pirs_states[pir] = None
                if not pir in self.__pirs_activations:
                    self.__pirs_activations[pir] = []

                # Get PIR state.
                state = self.__pirs[pir].get_motion()
                # If PIR state is different in previous moment.
                if self.__pirs_states[pir] != state:
                    # Save new state from this moment.
                    self.__pirs_states[pir] = state
                    # If PIR state is true (activated).
                    if state == True:
                        # Save time that has been activated.
                        self.__pirs_activations[pir].append(int(time.time()))

                # Remove the oldest activation.
                if len(self.__pirs_activations[pir]) > self.__activations_count:
                    self.__pirs_activations[pir].pop(0)

        # If the following register is available then set ist value to the PIRs activations.
        self._registers.write(f"{self.key}.pir.activations",
                              json.dumps(self.__pirs_activations))

    def __update_win_tamps(self):

        # If windows tampers are not none.
        if self.__win_tamps is not None:
            # For each window tamper in list get.

            for window in self.__win_tamps:

                # Initialise the arrays.
                if not window in self.__win_tamps_states:
                    self.__win_tamps_states[window] = None
                if not window in self.__win_tamps_activations:
                    self.__win_tamps_activations[window] = []

                # Get window tamper state.
                state = self._controller.digital_read(self.__win_tamps[window])

                # If window tamper state is different in previous moment.
                if self.__win_tamps_states[window] != state:
                    # Save new state from this moment.
                    self.__win_tamps_states[window] = state

                    # Save time that has been changed.
                    now = int(time.time())
                    self.__win_tamps_activations[window].append({"ts": now, "state": state})

                # Remove the oldest activation.
                if len(self.__win_tamps_activations[window]) > self.__activations_count:
                    self.__win_tamps_activations[window].pop(0)

        # If the following register is available then set its value to the door tampers activations.
        self._registers.write(f"{self.key}.window_tamper.activations",
                              json.dumps(self.__win_tamps_activations))

    def __update_door_tamps(self):

        # If windows tampers are not none.
        if self.__door_tamps is not None:
            # For each window tamper in list get.

            for door in self.__door_tamps:

                # Initialise the arrays.
                if not door in self.__door_tamps_states:
                    self.__door_tamps_states[door] = None
                if not door in self.__door_tamps_activations:
                    self.__door_tamps_activations[door] = []

                # Get window tamper state.
                state = self._controller.digital_read(self.__door_tamps[door])

                # If window tamper state is different in previous moment.
                if self.__door_tamps_states[door] != state:
                    # Save new state from this moment.
                    self.__door_tamps_states[door] = state

                    # Save time that has been changed.
                    now = int(time.time())
                    self.__door_tamps_activations[door].append({"ts": now, "state": state})

                # Remove the oldest activation.
                if len(self.__door_tamps_activations[door]) > self.__activations_count:
                    self.__door_tamps_activations[door].pop(0)

        # If the following register is available then set its value to the door tampers activations.
        self._registers.write(f"{self.key}.door_tamper.activations",
                              json.dumps(self.__door_tamps_activations))

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

    def __update_is_empty(self):

        is_human_presence = False

        # Get the ts with newer activation.
        ts_pir = 0
        ts_pirs = []
        for pir in self.__pirs_activations:
            if len(self.__pirs_activations[pir]) > 0:
                ts_pirs.append(self.__pirs_activations[pir][0])
                ts_pir = max(ts_pirs)

        # Get the ts with newer activation.
        ts_door = 0
        ts_doors = []
        for door in self.__door_tamps_activations:
            if len(self.__door_tamps_activations[door]) > 0:
                ts_doors.append(self.__door_tamps_activations[door][0]["ts"])
                ts_door = max(ts_doors)

        # Time now
        ts_now = int(time.time())

        # Human
        if ts_door < ts_pir:
            is_human_presence = True
        else:
            # No human
            if ts_now > (ts_door + self.__is_empty_timeout):
                is_human_presence = False
            else:
                is_human_presence = True

        self._registers.write("envm.is_empty", not is_human_presence)

    def __read_door_tamper(self):

        state = False

        for tamper in self.__door_tamps_states:
            state |= self.__door_tamps_states[tamper]

        return state


    def __update_mirror_output(self):

        doors_state = self.__read_door_tamper()
        print(f"Doors state: {doors_state}")


        for output in self.__mirror_output:
            print(f"Output: {output}")
            # Get window tamper state.
            self._controller.digital_write(output, doors_state)


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
                    vendor=register.value[pir]['vendor'],
                    model=register.value[pir]['model'],
                    options=register.value[pir]['options'])
                self.__pirs_activations.clear()

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

    def __door_tamp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {}:
            if self.__door_tamps is not None:
                self.__door_tamps.clear()

            self.__door_tamps = register.value

        elif register.value == {}:
            if self.__door_tamps is not None:
                self.__door_tamps.clear()

    def __mirror_output_cb(self, register):
        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {}:
            if self.__mirror_output is not None:
                self.__mirror_output.clear()

            self.__mirror_output = register.value

        elif register.value == {}:
            if self.__mirror_output is not None:
                self.__mirror_output.clear()

    def __is_empty_timeout_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__is_empty_timeout = register.value

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

        door_tamper = self._registers.by_name("envm.door_tamper.settings")
        if door_tamper is not None:
            door_tamper.update_handlers = self.__door_tamp_settings_cb
            door_tamper.update()

        mirror_output = self._registers.by_name("envm.door_tamper.mirror_output")
        if mirror_output is not None:
            mirror_output.update_handlers = self.__mirror_output_cb
            mirror_output.update()

        is_empty_timeout = self._registers.by_name("envm.is_empty_timeout")
        if is_empty_timeout is not None:
            is_empty_timeout.update_handlers = self.__is_empty_timeout_cb
            is_empty_timeout.update()

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

            self.__update_door_tamps()

            self.__update_is_empty()

            self.__update_mirror_output()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
