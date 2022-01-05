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
from enum import Enum

from utils.logger import get_logger

from utils.logic.timer import Timer
from utils.logic.state_machine import StateMachine

from devices.factories.valve.base_valve import BaseValve
from devices.factories.valve.valve_state import ValveState

from data import verbal_const

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

__class_name__ = "EnergyCenter"
"""Plugin class name."""

#endregion

class CalibrationState(Enum):
    """Calibration state description.
    """

    NONE = 0
    OpenValve = 1
    EnsureOpen = 2
    CloseValve = 3
    EnsureClose = 4
    YouDoTheMath = 5
    Error = 6

    # - Use dT and end position contacts to ensure that the valve is closed and opened.

class FLX05F(BaseValve):
    """Hydro Valve. Model: FLX-05F"""

#region Attributes

    __logger = None
    """Logger
    """

    __move_timer = None
    """Move timer.
    """

    __calibration_state = None
    """Calibration state machine.
    """

    __output_cw = verbal_const.OFF
    """Valve output CW GPIO.
    """

    __output_ccw = verbal_const.OFF
    """Valve output CCW GPIO.
    """

    __limit_cw = verbal_const.OFF
    """Limit switch for CW direction.
    """

    __limit_ccw = verbal_const.OFF
    """Limit switch for CCW direction.
    """

    __t0 = 0
    """T0 moment.
    """

    __t1 = 0
    """T1 moment.
    """

    __dt = 0
    """Delta time consumed for one full open and close cycle.
    """

    __limit_timer = None
    """Limit timer.
    """

    __close_on_shutdown = True
    """Close on shutdown flag.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self._vendor = "Flowx"

        self._model = "FLX-05F"

        # Create logger.
        self.__logger = get_logger(__name__)

        self.__move_timer = Timer()

        # 13 seconds absolute time to react the valve.
        # Number is measured by emperic way.
        self.__limit_timer = Timer(13)

        self.__calibration_state = StateMachine(CalibrationState.NONE)

        if "output_cw" in config:
            self.__output_cw = config["output_cw"]

        if "output_ccw" in config:
            self.__output_ccw = config["output_ccw"]

        if "limit_cw" in config:
            self.__limit_cw = config["limit_cw"]

        if "limit_ccw" in config:
            self.__limit_ccw = config["limit_ccw"]

        if "close_on_shutdown" in config:
            self.__close_on_shutdown = config["close_on_shutdown"]


    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Properties

    @property
    def is_calibrating(self):
        """Return is it in calibration state.

        Returns:
            bool: True if calibrating, else false.
        """

        return self._state.is_state(ValveState.Calibrate)

#endregion

#region Private Methods

    def __to_time(self, position):
        """Convert position in to time.

        Args:
            position (float): Position in %.

        Returns:
            float: Time in seconds.
        """

        return position * (self.__dt / 100.0)

#endregion

#region Private Messatages (PLC I/O)

    def __stop(self):
        """Stop the valve motor.
        """

        if self._controller.is_valid_gpio(self.__output_cw):
            self._controller.digital_write(self.__output_cw, 0)

        if self._controller.is_valid_gpio(self.__output_ccw):
            self._controller.digital_write(self.__output_ccw, 0)

    def __close_valve(self):
        """Turn to CW direction.
        """

        if self._controller.is_valid_gpio(self.__output_cw):
            self._controller.digital_write(self.__output_cw, 1)

    def __open_valve(self):
        """Turn to CCW direction.
        """

        if self._controller.is_valid_gpio(self.__output_ccw):
            self._controller.digital_write(self.__output_ccw, 1)

    def __get_open_limit(self):

        state = False

        if self._controller.is_valid_gpio(self.__limit_ccw):
            state = self._controller.digital_read(self.__limit_ccw)
        else:
            state = True

        return state

    def __get_close_limit(self):

        state = False

        if self._controller.is_valid_gpio(self.__limit_cw):
            state = self._controller.digital_read(self.__limit_cw)
        else:
            state = True

        return state

#endregion

#region Public Methods

    def init(self):
        """Initialize the device.
        """

        self.target_position = 0
        while self.current_position != self.target_position:
            self.update()

        self.__logger.debug("Starting up the: {}".format(self.name))

    def shutdown(self):
        """Shutdown the valve.
        """

        if self.__close_on_shutdown:

            self.__close_valve()

            while self.__get_close_limit() == False:
                self.update()

            self.__stop()

        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):
        """Update the valve state.
        """

        if self._state.is_state(ValveState.Prepare):

            delta_pos = self.target_position - self.current_position

            if delta_pos == 0:
                self.__stop()
                self._state.set_state(ValveState.Wait)
                return

            time_to_move = self.__to_time(abs(delta_pos))
            self.__logger.debug("Time: {}".format(time_to_move))

            self.__move_timer.expiration_time = time_to_move
            self.__move_timer.update_last_time()

            if delta_pos > 0:
                self.__open_valve()

            elif delta_pos < 0:
                self.__close_valve()

            self._state.set_state(ValveState.Execute)

        elif self._state.is_state(ValveState.Execute):

            self.__move_timer.update()
            if self.__move_timer.expired:
                self.__move_timer.clear()
                self.__stop()
                self._current_position = self.target_position
                self._state.set_state(ValveState.Wait)

            cw_limit_state = False # self.__get_close_limit()
            ccw_limit_state = False # self.__get_open_limit()
            if cw_limit_state or ccw_limit_state:
                self.__stop()
                GlobalErrorHandler.log_hardware_limit(self.__logger, "{} has raised end position.".format(self.name))
                self._current_position = self.target_position
                self._state.set_state(ValveState.Wait)

        elif self._state.is_state(ValveState.Calibrate):

            # Wait to start.
            if self.__calibration_state.is_state(CalibrationState.NONE):
                self.__calibration_state.set_state(CalibrationState.OpenValve)
                self.__stop()

            # Open the valve.
            if self.__calibration_state.is_state(CalibrationState.OpenValve):
                self.__stop()
                self.__open_valve()
                self.__calibration_state.set_state(CalibrationState.EnsureOpen)
                self.__limit_timer.update_last_time()

            # Wait until it si open at 100%.
            if self.__calibration_state.is_state(CalibrationState.EnsureOpen):

                # Get CCW limit switch state.
                ccw_limit_state = self.__get_open_limit()
                if ccw_limit_state:
                    self.__t0 = time.time()
                    self.__calibration_state.set_state(CalibrationState.CloseValve)

                # Prevent with timer,
                # if the valve is not reacting properly.
                self.__limit_timer.update()
                if self.__limit_timer.expired:
                    self.__limit_timer.clear()
                    self.__calibration_state.set_state(CalibrationState.Error)

            # Close the valve.
            if self.__calibration_state.is_state(CalibrationState.CloseValve):
                self.__stop()
                self.__close_valve()
                self.__calibration_state.set_state(CalibrationState.EnsureClose)
                self.__limit_timer.update_last_time()

            # Wait until it si open at 100%.
            if self.__calibration_state.is_state(CalibrationState.EnsureClose):

                # Get CW limit switch state.
                cw_limit_state = self.__get_close_limit()
                if cw_limit_state:
                    self.__t1 = time.time()
                    self.__calibration_state.set_state(CalibrationState.YouDoTheMath)

                # Prevent with timer,
                # if the valve is not reacting properly.
                self.__limit_timer.update()
                if self.__limit_timer.expired:
                    self.__limit_timer.clear()
                    self.__calibration_state.set_state(CalibrationState.Error)

            # Make calculations.
            if self.__calibration_state.is_state(CalibrationState.YouDoTheMath):
                self.__stop()
                self.__dt = self.__t1 - self.__t0
                self._state.set_state(ValveState.Wait)

            # Close the valve.
            if self.__calibration_state.is_state(CalibrationState.Error):

                GlobalErrorHandler.log_hardware_malfunction(self.__logger, "The valve {} can not calibrated.".format(self.name))
                self._state.set_state(ValveState.Wait)

            # - Close the valve.
            # - Ensure that the valve is closed 0deg.
            # - Record the time in T0.
            # - Open the valve.
            # - Ensure the the valve is opened 90deg.
            # - Record the time in T1.
            # - Store (T0 - T1) in dT
            # - Use dT and end position contacts to ensure that the valve is closed and opened.

    def calibrate(self):

        self._state.set_state(ValveState.Calibrate)

    def update_sync(self):
        """Update synchronious.
        """

        while self.current_position != self.target_position:
            self.update()

#endregion
