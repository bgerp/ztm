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

from numpy import true_divide
from utils.logger import get_logger
from utils.logic.timer import Timer

from plugins.base_plugin import BasePlugin

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

__class_name__ = "OfficeConferenceHall"
"""Plugin class name."""

#endregion

from enum import Enum

class SwitchType(Enum):

    NONE = 0
    Push = 1
    Switch = 2

class SwitchLogic():

#region Attributes

    __switch_type = SwitchType.NONE

    __active_state = True

    __in_state = False

    __out_state = False

    __is_pushed = False

#endregion

#region Properties

    @property
    def switch_type(self):

        return self.__switch_type

    @switch_type.setter
    def switch_type(self, value):

        self.__switch_type = value

    @property
    def active_state(self):

        return self.__active_state

    @active_state.setter
    def active_state(self, value):

        self.__active_state = value

#endregion

#region Constructor

    def __init__(self):

        pass

#endregion

#region Public Methods

    def set(self, state):

        self.__in_state = state

    def get(self):

        return self.__out_state

    def update(self):

        # Is it push button?
        if self.switch_type == SwitchType.Push:

            # Is it active state.
            if self.__in_state == self.active_state:

                # Is it pushed?
                if self.__is_pushed == False:

                    # Mark as pushed.
                    self.__is_pushed = True

                    # Flip the state.
                    self.__out_state = not self.__out_state

            else:

                # Un mark the pushed.
                self.__is_pushed = False

        elif self.switch_type == SwitchType.Switch:

            # The output is equal to input.
            self.__out_state = self.__in_state

    def off(self):

        if self.switch_type == SwitchType.Push:
            self.__out_state = False

        elif self.switch_type == SwitchType.Switch:
            self.__in_state = False

#endregion

class OfficeConferenceHall(BasePlugin):
    """Office conference hall controller."""

#region Attributes

    __logger = None
    """Logger"""

    __update_timer = None
    """Update timer."""

    __switch_logic = None
    """Switch logic.
    """    

    __test_bit = False

    __test_counter = 0

#endregion

#region Private Methods

    def __do_job(self):
        """Do the JOB method."""

        # self._controller.digital_read(self.__lamp_switch)

        if self.__test_counter <= 8:
            self.__test_bit = not self.__test_bit
            self.__switch_logic.set(self.__test_bit)
            self.__test_counter += 1

        else:
            self.__switch_logic.off()

        self.__switch_logic.update()
        test_b = self.__switch_logic.get()
        self.__logger.info("Out state: {}".format(test_b))

        # self._controller.digital_write(self.__lamp_switch)

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__update_timer = Timer(1)

        self.__switch_logic = SwitchLogic()
        self.__switch_logic.switch_type = SwitchType.Push
        self.__switch_logic.switch_type = SwitchType.Switch

    def _update(self):
        """Update the plugin.
        """

        # Update the timer.
        self.__update_timer.update()

        if self.__update_timer.expired:

            self.__update_timer.clear()

            self.__do_job()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
