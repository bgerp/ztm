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
from devices.vendors.flowx.flx05f.io_mode import IOMode
from devices.vendors.flowx.flx05f.calibration_state import CalibrationState
from devices.vendors.flowx.flx05f.control_mode import ControlMode

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

class FLX05F(BaseValve):
    """Hydro Valve. Model: FLX-05F"""

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self._vendor = "Flowx"

        self._model = "FLX-05F"

        self.__logger = get_logger(__name__)
        """Logger
        """

        self.__move_timer = Timer()
        """Move timer.
        """

        # 13 seconds absolute time to react the valve.
        # Number is measured by empiric way.
        self.__limit_timer = Timer(13)
        """Limit timer.
        """

        self.__calibration_state = StateMachine(CalibrationState.NONE)
        """Calibration state machine.
        """

        self.__output_cw = verbal_const.OFF
        """Valve output CW GPIO.
        """
        if "output_cw" in config:
            self.__output_cw = config["output_cw"]

        self.__output_ccw = verbal_const.OFF
        """Valve output CCW GPIO.
        """
        if "output_ccw" in config:
            self.__output_ccw = config["output_ccw"]

        self.__output_enable = verbal_const.OFF
        """Valve output enable GPIO.
        """
        if "output_enable" in config:
            self.__output_enable = config["output_enable"]

        self.__limit_cw = verbal_const.OFF
        """Limit switch for CW direction.
        """
        if "limit_cw" in config:
            self.__limit_cw = config["limit_cw"]

        self.__limit_ccw = verbal_const.OFF
        """Limit switch for CCW direction.
        """
        if "limit_ccw" in config:
            self.__limit_ccw = config["limit_ccw"]

        self.__close_on_shutdown = False
        """Close on shutdown flag.
        """
        if "close_on_shutdown" in config:
            self.__close_on_shutdown = config["close_on_shutdown"]

        self.__wait_on_shutdown = False
        """Wait on shutdown flag.
        """
        if "wait_on_shutdown" in config:
            self.__wait_on_shutdown = config["wait_on_shutdown"]

        self.__io_mode = IOMode(0)
        """IO mode of the valve.
        """
        if "io_mode" in config:
            if IOMode.is_valid(config["io_mode"]):
                self.__io_mode = IOMode(config["io_mode"])

        self.__control_mode = ControlMode.ON_OFF_TIMED
        """Control mode of the valve.
        """
        if "control_mode" in config:
            if ControlMode.is_valid(config["control_mode"]):
                self.__control_mode = ControlMode(config["control_mode"])

        # This number is given from the client. (#C4348)
        self.__number_of_moves_to_calibration = 20
        """Number of moves to calibration
        """
        if "number_of_moves_to_calibration" in config:
            self.__number_of_moves_to_calibration = config["number_of_moves_to_calibration"]

        self.__t0 = 0
        """T0 moment.
        """

        self.__t1 = 0
        """T1 moment.
        """

        self.__dt = 0
        """Delta time consumed for one full open and close cycle.
        """
        # - Use dT and end position contacts to ensure that the valve is closed and opened.

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

#region Private Messages (PLC I/O)

    def __stop(self):
        """Stop the valve motor.
        """

        if self.__io_mode == IOMode.SingleWire:
            if self._controller.is_valid_gpio(self.__output_cw):
                self._controller.digital_write(self.__output_cw, 0)
        elif self.__io_mode == IOMode.TwoWire:
            if self._controller.is_valid_gpio(self.__output_cw):
                self._controller.digital_write(self.__output_cw, 0)
            if self._controller.is_valid_gpio(self.__output_ccw):
                self._controller.digital_write(self.__output_ccw, 0)

    def __close_valve(self):
        """Turn to CW direction.
        """

        if self.__io_mode == IOMode.SingleWire:
            if self._controller.is_valid_gpio(self.__output_cw):
                self._controller.digital_write(self.__output_cw, 0)
        elif self.__io_mode == IOMode.TwoWire:
            if self._controller.is_valid_gpio(self.__output_cw):
                self._controller.digital_write(self.__output_cw, 1)

    def __open_valve(self):
        """Turn to CCW direction.
        """

        if self.__io_mode == IOMode.SingleWire:
            if self._controller.is_valid_gpio(self.__output_cw):
                self._controller.digital_write(self.__output_cw, 1)
        elif self.__io_mode == IOMode.TwoWire:
            if self._controller.is_valid_gpio(self.__output_ccw):
                self._controller.digital_write(self.__output_ccw, 1)

    def __get_open_limit(self):

        state = False

        if self._controller.is_valid_gpio(self.__limit_cw):
            state = self._controller.digital_read(self.__limit_cw)

        return state

    def __get_close_limit(self):

        state = False

        if self._controller.is_valid_gpio(self.__limit_ccw):
            state = self._controller.digital_read(self.__limit_ccw)

        return state

    def __enable_valve(self, state=0):
        if self.__io_mode == IOMode.SingleWire:
            if self._controller.is_valid_gpio(self.__output_enable):
                self._controller.digital_write(self.__output_enable, state)

#endregion

#region Public Methods

    def init(self):
        """Initialize the device.
        """

        def init_on_off():
            self.target_position = 0
            while self.current_position != self.target_position:
                self.update()

        def init_on_off_timed():
            pass

        if self.__control_mode == ControlMode.ON_OFF:
            init_on_off()
        elif self.__control_mode == ControlMode.ON_OFF_TIMED:
            init_on_off_timed()

        self.__logger.debug("Starting up the: {}".format(self.name))

    def shutdown(self):
        """Shutdown the valve.
        """

        def shutdown_on_off():
            if self.__close_on_shutdown:
                self.__close_valve()

            if self.__wait_on_shutdown:
                while self.__get_close_limit() == False:
                    self.update()
                self.__stop()

        def shutdown_on_off_timed():
            pass

        if self.__control_mode == ControlMode.ON_OFF:
            shutdown_on_off()
        elif self.__control_mode == ControlMode.ON_OFF_TIMED:
            shutdown_on_off_timed()

        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):
        """Update the valve state.
        """

        def update_on_off():
            if self._state.is_state(ValveState.Prepare):

                delta_pos = self.target_position - self.current_position

                if delta_pos == 0:
                    self.__stop()
                    self._state.set_state(ValveState.Wait)
                    return

                time_to_move = self.__to_time(abs(delta_pos))
                # self.__logger.debug("Time: {}".format(time_to_move))

                self.__move_timer.expiration_time = time_to_move
                self.__move_timer.update_last_time()

                if delta_pos > 0:
                    self.__open_valve()

                elif delta_pos < 0:
                    self.__close_valve()

                self._state.set_state(ValveState.Execute)

            elif self._state.is_state(ValveState.Execute):

                self._state.set_state(ValveState.Wait)

                # self.__move_timer.update()
                # if self.__move_timer.expired:
                #     self.__move_timer.clear()
                #     self.__stop()
                #     self._current_position = self.target_position
                #     self._state.set_state(ValveState.Wait)

                # cw_limit_state = False # self.__get_close_limit()
                # ccw_limit_state = False # self.__get_open_limit()
                # if cw_limit_state or ccw_limit_state:
                #     self.__stop()
                #     GlobalErrorHandler.log_hardware_limit(self.__logger, "{} has raised end position.".format(self.name))
                #     self._current_position = self.target_position
                #     self._state.set_state(ValveState.Wait)

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

        def update_on_off_timed():
            if self._state.is_state(ValveState.Prepare):

                # Delta
                delta_pos = self._target_position - self._current_position
                if delta_pos == 0:
                    self.__stop()
                    self._state.set_state(ValveState.NONE)
                    return

                # Scale down 10 times.
                # Example: form 100% to 10s is exactly 10 times.
                # Multiplication is safer way,
                # so reciprocal value of 10 in this case is 0.1.
                delta_pos *= 0.1
                time_to_move = abs(delta_pos)

                # time_to_move = self.__to_time(abs(delta_pos))
                # self.__logger.debug("Time: {}".format(time_to_move))

                self.__move_timer.expiration_time = time_to_move
                self.__move_timer.update_last_time()

                if delta_pos > 0:
                    self.__open_valve()

                elif delta_pos < 0:
                    self.__close_valve()

                self._state.set_state(ValveState.Execute)
            
            if self._state.is_state(ValveState.Execute):
                self.__enable_valve(1)
                self._state.set_state(ValveState.Wait)

            if self._state.is_state(ValveState.Wait):
                self.__move_timer.update()
                if self.__move_timer.expired:
                    self.__move_timer.clear()
                    self.__enable_valve(0)
                    self._current_position = self._target_position
                    if self.num_of_moves >= self.__number_of_moves_to_calibration:
                        self._state.set_state(ValveState.Calibrate)
                    else:
                        self._state.set_state(ValveState.NONE)

            elif self._state.is_state(ValveState.Calibrate):
                # Clear the counter.
                self.num_of_moves = 0
                self.__close_valve()
                self.__enable_valve(1)
                if self._current_position == self.min_pos:
                    self._state.set_state(ValveState.Prepare)

        if self.__control_mode == ControlMode.ON_OFF:
            update_on_off()
        elif self.__control_mode == ControlMode.ON_OFF_TIMED:
            update_on_off_timed()

        if self.__get_close_limit():
            self._current_position = self.min_pos
        if self.__get_open_limit():
            self._current_position = self.max_pos

    def calibrate(self):

        self._state.set_state(ValveState.Calibrate)

    def update_sync(self):
        """Update synchronous.
        """

        while self.current_position != self.target_position:
            self.update()

#endregion
