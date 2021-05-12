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

from devices.base_device import BaseDevice

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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


class ValveState(Enum):
    """Valve states.
    """

    NONE = 0
    Wait = 1
    Prepare = 2
    Execute = 3
    Calibrate = 4


class Valve(BaseDevice):

#region Attributes

    __logger = None
    """Logger
    """

    __target_position = 0

    __current_position = 0

    __valve_state = None

    __scale_per_sec = 1.111

    __move_timer = None

    __output_fw = verbal_const.OFF
    """Valve output forward GPIO.
    """    

    __output_rev = verbal_const.OFF
    """Valve output revers GPIO.
    """    

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        if "output_fw" in config:
            self.__output_fw = config["output_fw"]

        if "output_rev" in config:
            self.__output_rev = config["output_rev"]

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

        if self._controller.is_valid_gpio(self.__output_fw):
            self._controller.digital_write(self.__output_fw, 0)

        if self._controller.is_valid_gpio(self.__output_rev):
            self._controller.digital_write(self.__output_rev, 0)

    def __turn_cw(self):
        """Turn to CW direction.
        """
        
        if self._controller.is_valid_gpio(self.__output_fw):
            self._controller.digital_write(self.__output_fw, 1)

    def __turn_ccw(self):
        """Turn to CCW direction.
        """

        if self._controller.is_valid_gpio(self.__output_rev):
            self._controller.digital_write(self.__output_rev, 1)

    def __reed_fb(self):
        """Feedback function from the valve.

        Returns:
            bool: State of the feedback.
        """

        return False

#endregion

#region Properties

    @property
    def current_position(self):

        return self.__current_position

    @property
    def target_position(self):

        return self.__target_position

    @target_position.setter
    def target_position(self, position):
        """Set the position of the valve.

        Args:
            position (int): Position of the valve.
        """

        if position == self.__target_position:
            return

        if position > 100:
            position = 100

        elif position < 0:
            position = 0

        self.__target_position = position
        self.__valve_state.set_state(ValveState.Prepare)

        self.__logger.debug("Set position of {} to {}".format(self.name, self.__target_position))

#endregion

#region Public Methods

    def init(self):
        """Init the valve.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        self.__valve_state = StateMachine(ValveState.Wait)
        self.__valve_state.set_state(ValveState.Wait)

        self.__move_timer = Timer()

        self.target_position = 0

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

        if self.__valve_state.is_state(ValveState.Prepare):

            delta_pos = self.__target_position - self.__current_position

            if delta_pos == 0:
                self.__stop()
                self.__valve_state.set_state(ValveState.Wait)
                return

            time_to_move = self.__to_time(abs(delta_pos))
            self.__logger.debug("Time: {}".format(time_to_move))

            self.__move_timer.expiration_time = time_to_move
            self.__move_timer.update_last_time()

            if delta_pos > 0:
                self.__turn_cw()

            elif delta_pos < 0:
                self.__turn_ccw()

            self.__valve_state.set_state(ValveState.Execute)

        elif self.__valve_state.is_state(ValveState.Execute):

            self.__move_timer.update()
            if self.__move_timer.expired:
                self.__move_timer.clear()
                self.__stop()
                self.__current_position = self.__target_position
                self.__valve_state.set_state(ValveState.Wait)

            input_fb = self.__reed_fb()
            if input_fb:
                self.__stop()
                self.__logger.warning("{} has raised end position.".format(self.name))
                self.__current_position = self.__target_position
                self.__valve_state.set_state(ValveState.Wait)

        elif self.__valve_state.is_state(ValveState.Calibrate):

            # TODO: Calibration sequence.

            self.__valve_state.set_state(ValveState.Wait)

#endregion

#region Public Static Methods

    @staticmethod
    def create(name, key, registers, controller):
        """Create instance of the class.

        Args:
            name (str): Name of the object.
            key (str): Key used for registers base path.
            registers (Registers): System registers.
            controller (BaseController): Controller instance.

        Returns:
            Valve: Valve control instance.
        """

        instance = None

        output_fw = registers.by_name("{}.output_fw".format(key)).value
        output_rev = registers.by_name("{}.output_rev".format(key)).value
        valve_fb = registers.by_name("{}.feedback".format(key)).value
        max_pos = registers.by_name("{}.max_pos".format(key)).value
        min_pos = registers.by_name("{}.min_pos".format(key)).value

        instance = Valve(
            name=name,
            key=key,
            controller=controller,
            output_fw=output_fw,
            output_rev=output_rev,
            feedback=valve_fb,
            min_pos=min_pos,
            max_pos=max_pos)

        return instance

#endregion
