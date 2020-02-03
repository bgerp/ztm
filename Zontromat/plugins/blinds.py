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

from enum import Enum

from utils.logger import get_logger
from utils.state_machine import StateMachine
from utils.timer import Timer

from plugins.base_plugin import BasePlugin

class Directions(Enum):
    """Motor directions."""

    NONE = 0
    CW = 1
    CCW = 2

class BlindsState(Enum):
    """Blinds functional states."""

    NONE = 0,
    Wait = 1,
    Prepare = 2,
    Execute = 3,

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

class Blinds(BasePlugin):
    """Blinds controller device."""

#region Attributes

    __logger = None
    """Logger"""

    __blinds_state = None
    """Blinds state."""

    __deg_per_sec = 18
    """Degreeses per sec."""

    __curretnt_position = 0
    """Current position of the blinds."""

    __new_position = 0
    """New position."""

    __move_timer = None
    """Move timer."""

#endregion

#region Private Methods
    def __to_time(self, degrees):
        return (degrees / self.__deg_per_sec)

#endregion


#region Public Methods

    def init(self):

        self.__logger = get_logger(__name__)

        self.__blinds_state = StateMachine(BlindsState.NONE)

        self.__move_timer = Timer()

    def update(self):

        if self.__blinds_state.is_state(BlindsState.Prepare):

            delta_pos = self.__new_position - self.__curretnt_position

            if delta_pos > 0:
                self.__direction = Directions.CW

            elif delta_pos < 0:
                self.__direction = Directions.CCW

            else:
                self.__direction = Directions.NONE
                self.__blinds_state.set_state(BlindsState.Wait)
                return

            time_to_move = self.__to_time(abs(delta_pos))

            self.__move_timer.expiration_time = time_to_move
            self.__move_timer.update_last_time()

            if self.__direction == Directions.CW:
                self._controller.digital_write(self._config["output_ccw"], 0)
                self._controller.digital_write(self._config["output_cw"], 1)

            elif self.__direction == Directions.CCW:
                self._controller.digital_write(self._config["output_cw"], 0)
                self._controller.digital_write(self._config["output_ccw"], 1)

            else:
                self._controller.digital_write(self._config["output_cw"], 0)
                self._controller.digital_write(self._config["output_ccw"], 0)

            self.__blinds_state.set_state(BlindsState.Execute)

        if self.__blinds_state.is_state(BlindsState.Execute):

            self.__move_timer.update()
            if self.__move_timer.expired:
                self.__move_timer.clear()
                self._controller.digital_write(self._config["output_cw"], 0)
                self._controller.digital_write(self._config["output_ccw"], 0)
                self.__curretnt_position = self.__new_position
                self.__blinds_state.set_state(BlindsState.Wait)

            # input_active = self._controller.digital_read(self._config["input_active"])
            # if not input_active:
            #     self._controller.digital_write(self._config["output_cw"], 0)
            #     self._controller.digital_write(self._config["output_ccw"], 0)
            #     self.__curretnt_position = self.__new_position
            #     self.__blinds_state.set_state(BlindsState.Wait)

        # "blinds.sun.elevation.value": 0,
        # "blinds.sun.elevation.mou": "deg",
        # "blinds.sun.azimuth.value": 0,
        # "blinds.sun.azimuth.mou": "deg",

    def shutdown(self):
        """Shutdown the blinds."""

        self._controller.digital_write(self._config["output_cw"], 0)
        self._controller.digital_write(self._config["output_ccw"], 0)

    def get_state(self):
        """Returns the state of the device.

        Returns
        -------
        mixed
            State of the device.
        """

        return None

    def set_position(self, position):

        if position > 180:
            position = 180

        elif position < 0:
            position = 0

        self.__new_position = position
        self.__blinds_state.set_state(BlindsState.Prepare)

#endregion
