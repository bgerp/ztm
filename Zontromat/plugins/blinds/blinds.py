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

from enum import Enum

from utils.logger import get_logger
from utils.state_machine import StateMachine
from utils.timer import Timer
from utils.utils import to_rad, shadow_length

from plugins.base_plugin import BasePlugin

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

class BlindsState(Enum):
    """Blinds functional states."""

    NONE = 0
    Wait = 1
    Prepare = 2
    Execute = 3

class Blinds(BasePlugin):
    """Blinds controller device."""

#region Attributes

    __logger = None
    """Logger"""

    __blinds_state = None
    """Blinds state."""

    __move_timer = None
    """Move timer."""

    __input_stop = None
    """Input active."""

    __output_ccw = None
    """Ouput CCW"""

    __output_cw = None
    """Output CW"""

    __curretnt_position = 0
    """Current position of the blinds."""

    __new_position = 0
    """New position."""

    __deg_per_sec = 18
    """Degreeses per sec."""

    __limit = 1

    __delay_timer = Timer(2)
    __sun_azm = 0
    __sun_elev = 0

#endregion

#region Private Methods

    def __stop(self):
        """Stop the engine."""

        self._controller.digital_write(self.__output_cw, 0)
        self._controller.digital_write(self.__output_ccw, 0)

    def __on_new_pos(self, register):
        """Callback function that sets new position."""
        self.__set_position(register.value)

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

    def __calculate_position(self):

        sun_elev_reg = self._registers.by_name(self._key + ".sun.elevation.value")
        if sun_elev_reg:
            self.__sun_elev = sun_elev_reg.value

        sun_azm_reg = self._registers.by_name(self._key + ".sun.azimuth.value")
        if sun_azm_reg:
            self.__sun_azm = sun_azm_reg.value

        if (self.__sun_azm > 0) and (self.__sun_elev > 0):
            print(f"Blinds -> Azm: {self.__sun_azm:.2f}; Elev: {self.__sun_elev:.2f}")

            # Calculate the shadow length.
            shadow_l = shadow_length(1, to_rad(self.__sun_elev))
            print(f"Blinds -> Shadow: {shadow_l:.2f}")

            thita = 360 - (self.__sun_azm + 180)
            print(f"Blinds -> Thita: {thita:.2f}")

            # Calculate cartesian
            x = shadow_l * math.cos(to_rad(thita))
            y = shadow_l * math.sin(to_rad(thita))
            print(f"Blinds -> X: {x:.2f}; Y: {y:.2f}")

            is_cloudy = False
            if (x > self.__limit or y > self.__limit) and not is_cloudy:
                if self.__blinds_state.is_state(BlindsState.Wait):
                    print("Signal to close")
                    self.__set_position(180)

#endregion

#region Public Methods

    def init(self):

        self.__logger = get_logger(__name__)

        self.__blinds_state = StateMachine(BlindsState.Wait)

        self.__move_timer = Timer()

        input_stop = self._registers.by_name(self._key + ".input_stop")
        if input_stop is not None:
            self.__input_stop = input_stop.value

        output_ccw = self._registers.by_name(self._key + ".output_ccw")
        if output_ccw is not None:
            self.__output_ccw = output_ccw.value

        output_cw = self._registers.by_name(self._key + ".output_cw")
        if output_cw is not None:
            self.__output_cw = output_cw.value

        # position = self._registers.by_name(self._key + ".position")
        # if position is not None:
        #     position.update_handler = self.__on_new_pos

    def update(self):

        self.__delay_timer.update()
        if self.__delay_timer.expired:
            self.__delay_timer.clear()
            self.__calculate_position()

        if self.__blinds_state.is_state(BlindsState.Prepare):

            delta_pos = self.__new_position - self.__curretnt_position

            if delta_pos == 0:
                self._controller.digital_write(self.__output_cw, 0)
                self._controller.digital_write(self.__output_ccw, 0)
                self.__blinds_state.set_state(BlindsState.Wait)
                return

            time_to_move = self.__to_time(abs(delta_pos))

            self.__move_timer.expiration_time = time_to_move
            self.__move_timer.update_last_time()

            if delta_pos > 0:
                self._controller.digital_write(self.__output_ccw, 0)
                self._controller.digital_write(self.__output_cw, 1)

            elif delta_pos < 0:
                self._controller.digital_write(self.__output_cw, 0)
                self._controller.digital_write(self.__output_ccw, 1)

            self.__blinds_state.set_state(BlindsState.Execute)

        elif self.__blinds_state.is_state(BlindsState.Execute):

            self.__move_timer.update()
            if self.__move_timer.expired:
                self.__move_timer.clear()
                self.__stop()
                self.__curretnt_position = self.__new_position
                self.__blinds_state.set_state(BlindsState.Wait)

            input_stop = self._controller.digital_read(self.__input_stop)
            if not input_stop:
                self.__stop()
                self.__logger.warning("{} has raised end position.".format(self.name, ))
                self.__curretnt_position = self.__new_position
                self.__blinds_state.set_state(BlindsState.Wait)

    def shutdown(self):
        """Shutdown the blinds."""

        self.__logger.info("Shutdown the {}".format(self.name))
        self.__stop()

#endregion
