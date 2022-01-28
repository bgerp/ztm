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

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from data import verbal_const

from devices.factories.blinds.base_blind import BaseBlind

from devices.factories.blinds.blind_state import BlindsState
from devices.factories.blinds.calibration_state import CalibrationState
from devices.factories.blinds.feedback_type import FeedbackType

from utils.logger import get_logger
from utils.logic.state_machine import StateMachine
from utils.logic.timer import Timer
from utils.logic.functions import to_rad, shadow_length

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

class MODV1(BaseBlind):
    """Electronic blinds"""

#region Attributes

    __input_fb = verbal_const.OFF
    """Input feedback."""

    __output_ccw = verbal_const.OFF
    """Output CCW"""

    __output_cw = verbal_const.OFF
    """Output CW"""

    __deg_per_sec = 0
    """Degreases per sec."""

    __feedback_treshold = 0
    """Feedback threshold."""

    __blinds_state = None
    """Blinds state."""

    __move_timer = None
    """Move timer."""

    __current_position = 0
    """Current position of the blinds."""

    __new_position = 0
    """New position of the blinds."""

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



#endregion

#region constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "POLYGONTeam"

        self._model = "Blind"

        self.__logger = get_logger(__name__)

        self.__blinds_state = StateMachine(BlindsState.Wait)

        self.__move_timer = Timer()

        self.__calibration_state = StateMachine(CalibrationState.NONE)

        options = self._config["options"]

        if "output_cw" in options:
            self.__output_cw = options["output_cw"]

        if "output_ccw" in options:
            self.__output_ccw = options["output_ccw"]

        if "feedback" in options:
            self.__input_fb = options["feedback"]

        if "feedback_tresh" in options:
            self.__feedback_treshold = options["feedback_tresh"]

        if "deg_per_sec" in options:
            self.__deg_per_sec = options["deg_per_sec"]
        

        # Set the feedback type.
        if self.__input_fb.startswith("AI"):
            self.__feedback_type = FeedbackType.Analog
        
        elif self.__input_fb.startswith("DI"):
            self.__feedback_type = FeedbackType.Digital

        else:
            GlobalErrorHandler.log_missing_resource(self.__logger, "{}: feedback not set correct or incomparable. Check feedback settings.".format(self.name))

#endregion

#region Private Methods (PLC I/O)

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

#endregion

#regio Private Methods

    def __to_time(self, degrees):
        return degrees / self.__deg_per_sec

#endregion

#region Public Methods

    def init(self):

        self.__stop()

    def update(self):

        if self.__blinds_state.is_state(BlindsState.Prepare):

            delta_pos = self.__new_position - self.__current_position

            if delta_pos == 0:
                self.__stop()
                self.__blinds_state.set_state(BlindsState.Wait)
                return

            time_to_move = self.__to_time(abs(delta_pos))
            self.__logger.debug("Time: {}".format(time_to_move))

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
                GlobalErrorHandler.log_hardware_limit(self.__logger, "{} has raised end position.".format(self.name))
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

    def shutdown(self):

        self.set_position(0)

        while not self.__blinds_state.is_state(BlindsState.Wait):
            self.update()
            pass

    def set_position(self, position):
        """Set position of the blinds.

        Args:
            position (float): Position of the blinds.
        """

        if self.__new_position == position:
            return

        if position > 180:
            position = 180

        elif position < 0:
            position = 0

        self.__new_position = position
        self.__blinds_state.set_state(BlindsState.Prepare)

#endregion
