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

import math
import time

from enum import Enum

from data import verbal_const

from utils.logger import get_logger
from utils.logic.state_machine import StateMachine
from utils.logic.timer import Timer
from utils.logic.functions import to_rad, shadow_length

from plugins.base_plugin import BasePlugin

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

__class_name__ = "Blinds"
"""Plugin class name."""

#endregion

class FeedbackType(Enum):
    """Blinds feedback type."""

    NONE = 0
    Analog = 1
    Digital = 2

class CalibrationState(Enum):
    """Calibration process states."""

    NONE = 0
    Stop = 1
    TurnCW = 2
    WaitCurStabCW = 3
    WaitLimitCW = 4
    TurnCCW = 5
    WaitCurStabCCW = 6
    WaitLimitCCW = 7
    ExitTightness = 8
    WaitCurrentStab = 9
    GoTo90 = 10

class BlindsState(Enum):
    """Blinds functional states."""

    NONE = 0
    Wait = 1
    Prepare = 2
    Execute = 3
    Calibrate = 4

class Blinds(BasePlugin):
    """Blinds controller device."""

#region Attributes

    __logger = None
    """Logger"""

    __blinds_state = None
    """Blinds state."""

    __move_timer = None
    """Move timer."""

    __input_fb = None
    """Input feedback."""

    __output_ccw = verbal_const.OFF
    """Output CCW"""

    __output_cw = verbal_const.OFF
    """Output CW"""

    __current_position = 0
    """Current position of the blinds."""

    __new_position = 0
    """New position of the blinds."""

    __sun_spot_update_timer = None
    """Sun spot update timer."""

    __calibration_state = None
    """"Calibration state."""

    __feedback_type = FeedbackType.NONE
    """Feedback type."""

    __timout_counter = 0
    """Timeout counter."""

    __t1 = 0
    """T1 moment of first limit."""

    __t2 = 0
    """T2 moment of second limit."""

    __deg_per_sec = 0
    """Degreases per sec."""

    __feedback_treshold = 0
    """Feedback threshold."""

    __sun_azm = 0
    """Sun azimuth."""

    __sun_elev = 0
    """Sun elevation."""

    __sun_spot_limit = 0
    """Sun spot limit."""

    __object_height = 0
    """Object height [m]
    """    

#endregion

#region Private Methods (registers)

    def __object_height_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__object_height != register.value:
            self.__object_height = register.value

    def __sunspot_limit_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__sun_spot_limit != register.value:
            self.__sun_spot_limit = register.value    

    def __feedback_treshold_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__feedback_treshold != register.value:
            self.__feedback_treshold = register.value      

    def __deg_per_sec_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__deg_per_sec != register.value:
            self.__deg_per_sec = register.value  

    def __input_fb_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__input_fb != register.value:
            self.__input_fb = register.value

        if "D" in self.__input_fb.upper():
            self.__feedback_type = FeedbackType.Digital

        elif "A" in self.__input_fb.upper():
            self.__feedback_type = FeedbackType.Analog

    def __output_cw_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__output_cw != register.value:
            self.__output_cw = register.value

    def __output_ccw_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__output_ccw != register.value:
            self.__output_ccw = register.value

    def __new_pos_cb(self, register):
        """Callback function that sets new position."""

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__set_position(register.value)

    def __init_registers(self):

        input_fb = self._registers.by_name(self.key + ".input_fb")
        if input_fb is not None:
            input_fb.update_handlers = self.__input_fb_cb
            input_fb.update()

        output_cw = self._registers.by_name(self.key + ".output_cw")
        if output_cw is not None:
            output_cw.update_handlers = self.__output_cw_cb
            output_cw.update()

        output_ccw = self._registers.by_name(self.key + ".output_ccw")
        if output_ccw is not None:
            output_ccw.update_handlers = self.__output_ccw_cb
            output_ccw.update()

        position = self._registers.by_name(self.key + ".position")
        if position is not None:
            position.update_handlers = self.__new_pos_cb
            position.update()

        object_height = self._registers.by_name(self.key + ".object_height")
        if object_height is not None:
            object_height.update_handlers = self.__object_height_cb
            object_height.update()

        sunspot_limit = self._registers.by_name(self.key + ".sunspot_limit")
        if sunspot_limit is not None:
            sunspot_limit.update_handlers = self.__sunspot_limit_cb
            sunspot_limit.update()

        feedback_treshold = self._registers.by_name(self.key + ".feedback_treshold")
        if feedback_treshold is not None:
            feedback_treshold.update_handlers = self.__feedback_treshold_cb
            feedback_treshold.update()

        deg_per_sec = self._registers.by_name(self.key + ".deg_per_sec")
        if deg_per_sec is not None:
            deg_per_sec.update_handlers = self.__deg_per_sec_cb
            deg_per_sec.update()

    def __get_sun_pos(self):

        sun_elev_reg = self._registers.by_name("envm.sun.elevation")
        if sun_elev_reg:
            if not ((sun_elev_reg.data_type == "float") or (sun_elev_reg.data_type == "int")):
                GlobalErrorHandler.log_bad_register_value(self.__logger, sun_elev_reg)
                return

            if self.__sun_elev != sun_elev_reg.value:
                self.__sun_elev = sun_elev_reg.value

        sun_azm_reg = self._registers.by_name("envm.sun.azimuth")
        if sun_azm_reg:
            if not ((sun_azm_reg.data_type == "float") or (sun_azm_reg.data_type == "int")):
                GlobalErrorHandler.log_bad_register_value(self.__logger, sun_azm_reg)
                return

            if self.__sun_azm != sun_azm_reg.value:
                self.__sun_azm = sun_azm_reg.value

    def __get_occupation_flags(self):

        zones_count = 0
        reg_zones_count = self._registers.by_name("ac.zones_count")
        if reg_zones_count is not None:
            zones_count = reg_zones_count.value

        zones_occupation_flags = []
        for index in range(zones_count):

            # To human readable registers index.
            index += 1

            # Sinthesize the name of the occupation flag.
            register_name = "ac.zone_{}_occupied".format(index)

            # If there is no one at the zone, just turn off the lights.
            ac_zone_occupied = self._registers.by_name(register_name)
            if ac_zone_occupied is not None:
                zones_occupation_flags.append(ac_zone_occupied.value)

        return zones_occupation_flags

#endregion

#region Private Methods

    def __stop(self):
        """Stop the engine."""

        if self._controller.is_valid_gpio(self.__output_cw):
            self._controller.digital_write(self.__output_cw, 0)

        if self._controller.is_valid_gpio(self.__output_ccw):
            self._controller.digital_write(self.__output_ccw, 0)

    def __turn_cw(self):
        """Turn the motor CW."""

        if self._controller.is_valid_gpio(self.__output_cw):
            self._controller.digital_write(self.__output_cw, 1)

        if self._controller.is_valid_gpio(self.__output_ccw):
            self._controller.digital_write(self.__output_ccw, 0)

    def __turn_ccw(self):
        """Turn the motor CCW."""

        if self._controller.is_valid_gpio(self.__output_cw):
            self._controller.digital_write(self.__output_cw, 0)

        if self._controller.is_valid_gpio(self.__output_ccw):
            self._controller.digital_write(self.__output_ccw, 1)

    def __reed_fb(self):
        """Read feedback."""

        fb_value = 0

        if not self._controller.is_valid_gpio(self.__input_fb):
            return fb_value

        if self.__feedback_type == FeedbackType.Digital:
            fb_value = self._controller.digital_read(self.__input_fb)

        if self.__feedback_type == FeedbackType.Analog:
            ai = self._controller.analog_read(self.__input_fb)
            value = ai["value"]

            if value < 0:
                value = 0

            fb_value = value >= self.__feedback_treshold
            # self.__logger.debug(f"Voltage: {value:02.4f}")

        return fb_value

    def __set_position(self, position):

        if position == self.__new_position:
            return

        if position > 180:
            position = 180

        elif position < 0:
            position = 0

        self.__new_position = position
        self.__blinds_state.set_state(BlindsState.Prepare)

    def __to_time(self, degrees):
        return degrees / self.__deg_per_sec

    def __calc_sun_spot(self):

        if (self.__sun_azm > 0) and (self.__sun_elev > 0):
            # print(f"Blinds -> Azm: {self.__sun_azm:03.2f}; Elev: {self.__sun_elev:03.2f}")

            # Calculate the shadow length.
            shadow_l = shadow_length(self.__object_height, to_rad(self.__sun_elev))
            # print(f"Blinds -> Shadow: {shadow_l:03.2f}")

            theta = 360 - (self.__sun_azm + 180)
            # print(f"Blinds -> Theta: {theta:03.2f}")

            # Calculate cartesian
            x = shadow_l * math.cos(to_rad(abs(theta)))
            y = shadow_l * math.sin(to_rad(abs(theta)))
            # print(f"Blinds -> X: {x:03.2f}; Y: {y:03.2f}")

            is_cloudy = False
            if (x > self.__sun_spot_limit or y > self.__sun_spot_limit) and not is_cloudy:
                if self.__blinds_state.is_state(BlindsState.Wait):
                    # print("Signal to close")
                    self.__set_position(180)

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__blinds_state = StateMachine(BlindsState.Wait)

        self.__move_timer = Timer()

        self.__sun_spot_update_timer = Timer(2)

        self.__calibration_state = StateMachine(CalibrationState.NONE)

        self.__init_registers()

        self.__stop()

    def _update(self):
        """Update the plugin.
        """

        # Update occupation flags.
        occupation_flags = self.__get_occupation_flags()
        is_occupied = False
        for flag in occupation_flags:
            is_occupied = flag or is_occupied
            # TODO: Close the blinds.

        self.__sun_spot_update_timer.update()
        if self.__sun_spot_update_timer.expired:
            self.__sun_spot_update_timer.clear()

            if self.__blinds_state.is_state(BlindsState.Wait):
                self.__get_sun_pos()
                self.__calc_sun_spot()

        if self.__blinds_state.is_state(BlindsState.Prepare):

            delta_pos = self.__new_position - self.__current_position

            if delta_pos == 0:
                self.__stop()
                self.__blinds_state.set_state(BlindsState.Wait)
                return

            time_to_move = self.__to_time(abs(delta_pos))
            self.__logger.info("Time: {}".format(time_to_move))

            self.__move_timer.expiration_time = time_to_move
            self.__move_timer.update_last_time()

            if delta_pos > 0:
                self.__turn_cw()

            elif delta_pos < 0:
                self.__turn_ccw()

            self.__blinds_state.set_state(BlindsState.Execute)

        elif self.__blinds_state.is_state(BlindsState.Execute):

            self.__move_timer.update()
            if self.__move_timer.expired:
                self.__move_timer.clear()
                self.__stop()
                self.__current_position = self.__new_position
                self.__blinds_state.set_state(BlindsState.Wait)

            input_fb = self.__reed_fb()
            if input_fb:
                self.__stop()
                self.__logger.warning("{} has raised end position.".format(self.name, ))
                self.__current_position = self.__new_position
                self.__blinds_state.set_state(BlindsState.Wait)

        elif self.__blinds_state.is_state(BlindsState.Calibrate):

            if self.__calibration_state.is_state(CalibrationState.Stop):

                self.__stop()

                self.__current_position = 0
                self.__new_position = 0

                self.__calibration_state.set_state(CalibrationState.TurnCW)

            elif self.__calibration_state.is_state(CalibrationState.TurnCW):

                self.__turn_cw()

                self.__calibration_state.set_state(CalibrationState.WaitCurStabCW)

            elif self.__calibration_state.is_state(CalibrationState.WaitCurStabCW):

                if self.__timout_counter >= 5:
                    self.__timout_counter = 0
                    self.__calibration_state.set_state(CalibrationState.WaitLimitCW)
                else:
                    self.__timout_counter += 1

            elif self.__calibration_state.is_state(CalibrationState.WaitLimitCW):

                fb_value = self.__reed_fb()
                if fb_value:

                    self.__stop()

                    self.__t1 = time.time()

                    self.__calibration_state.set_state(CalibrationState.TurnCCW)

            elif self.__calibration_state.is_state(CalibrationState.TurnCCW):

                self.__turn_ccw()

                self.__calibration_state.set_state(CalibrationState.WaitCurStabCCW)

            elif self.__calibration_state.is_state(CalibrationState.WaitCurStabCCW):

                if self.__timout_counter >= 5:
                    self.__timout_counter = 0
                    self.__calibration_state.set_state(CalibrationState.WaitLimitCCW)
                else:
                    self.__timout_counter += 1

            elif self.__calibration_state.is_state(CalibrationState.WaitLimitCCW):

                fb_value = self.__reed_fb()
                if fb_value:

                    self.__stop()

                    self.__t2 = time.time()

                    time_delta = self.__t2 - self.__t1
                    time_delta -= 4
                    self.__deg_per_sec = 180 / time_delta
                    self.__logger.info("DPS: {}".format(self.__deg_per_sec))

                    self.__turn_cw()

                    self.__calibration_state.set_state(CalibrationState.ExitTightness)

            elif self.__calibration_state.is_state(CalibrationState.ExitTightness):

                if self.__timout_counter >= 12:
                    self.__timout_counter = 0
                    self.__stop()
                    self.__calibration_state.set_state(CalibrationState.WaitCurrentStab)
                else:
                    self.__timout_counter += 1

            elif self.__calibration_state.is_state(CalibrationState.WaitCurrentStab):

                if self.__timout_counter >= 4:
                    self.__timout_counter = 0
                    self.__calibration_state.set_state(CalibrationState.GoTo90)
                else:
                    self.__timout_counter += 1

            elif self.__calibration_state.is_state(CalibrationState.GoTo90):

                self.__calibration_state.set_state(CalibrationState.NONE)
                self.__set_position(90)

                return

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))
        self.__stop()

#endregion
