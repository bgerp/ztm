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

from utils.logger import get_logger

from utils.logic.timer import Timer
from utils.logic.state_machine import StateMachine

from devices.factories.valve.base_valve import BaseValve
from devices.factories.valve.valve_state import ValveState

from data import verbal_const

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

#region Attributes

    __logger = None
    """Logger
    """

    __scale_per_sec = 1.111

    __move_timer = None

    __output_cw = verbal_const.OFF
    """Valve output CW GPIO.
    """    

    __output_ccw = verbal_const.OFF
    """Valve output CCW GPIO.
    """    

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self._vendor = "Flowx"

        self._model = "Valve"

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        self.__move_timer = Timer()

        if "output_cw" in config:
            self.__output_cw = config["output_cw"]

        if "output_ccw" in config:
            self.__output_ccw = config["output_ccw"]

        self.target_position = 0

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods

    def __to_time(self, position):
        """Convert position in to time.

        Args:
            position (float): Position in %.

        Returns:
            float: Time in seconds.
        """

        return position / self.__scale_per_sec

    def __stop(self):
        """Stop the valve motor.
        """

        if self._controller.is_valid_gpio(self.__output_cw):
            self._controller.digital_write(self.__output_cw, 0)

        if self._controller.is_valid_gpio(self.__output_ccw):
            self._controller.digital_write(self.__output_ccw, 0)

    def __turn_cw(self):
        """Turn to CW direction.
        """
        
        if self._controller.is_valid_gpio(self.__output_cw):
            self._controller.digital_write(self.__output_cw, 1)

    def __turn_ccw(self):
        """Turn to CCW direction.
        """

        if self._controller.is_valid_gpio(self.__output_ccw):
            self._controller.digital_write(self.__output_ccw, 1)

    def __reed_fb(self):
        """Feedback function from the valve.

        Returns:
            bool: State of the feedback.
        """

        return False

#endregion

#region Public Methods

    def init(self):
        """Init the valve.
        """

        self.shutdown()

    def shutdown(self):
        """Shutdown the valve.
        """

        self.target_position = 0
        while self.current_position != self.target_position:
            self.update()

        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):
        """Update the valve state.
        """

        if self._valve_state.is_state(ValveState.Prepare):

            delta_pos = self.target_position - self.current_position

            if delta_pos == 0:
                self.__stop()
                self._valve_state.set_state(ValveState.Wait)
                return

            time_to_move = self.__to_time(abs(delta_pos))
            self.__logger.debug("Time: {}".format(time_to_move))

            self.__move_timer.expiration_time = time_to_move
            self.__move_timer.update_last_time()

            if delta_pos > 0:
                self.__turn_cw()

            elif delta_pos < 0:
                self.__turn_ccw()

            self._valve_state.set_state(ValveState.Execute)

        elif self._valve_state.is_state(ValveState.Execute):

            self.__move_timer.update()
            if self.__move_timer.expired:
                self.__move_timer.clear()
                self.__stop()
                self.__current_position = self.__target_position
                self._valve_state.set_state(ValveState.Wait)

            input_fb = self.__reed_fb()
            if input_fb:
                self.__stop()
                self.__logger.warning("{} has raised end position.".format(self.name))
                self.__current_position = self.__target_position
                self._valve_state.set_state(ValveState.Wait)

        elif self._valve_state.is_state(ValveState.Calibrate):

            # TODO: Calibration sequence.

            self._valve_state.set_state(ValveState.Wait)

#endregion
