
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

from utils.logger import get_logger

from devices.factories.valve.base_valve import BaseValve
from devices.factories.valve.valve_state import ValveState

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

#endregion

class A20M15B2C(BaseValve):
    """Hydro Valve. Model: A20-M15-B2-C"""

#region Attributes

    __logger = None
    """Logger"""

    __feedback = None
    """Feedback of the valve position."""

    __output = None
    """Output physical signal."""

#endregion

#region Properties

#endregion

#region Constructor

    def __init__(self, **config):

        super().__init__(config)

        self._vendor = "Tonhe"

        self._model = "A20M15B2C"

        self.__logger = get_logger(__name__)

        if "min_pos" in self._config:
            self.min_pos = self._config["min_pos"]

        if "max_pos" in self._config:
            self.max_pos = self._config["max_pos"]

        if "feedback" in self._config:
            self.__feedback = self._config["feedback"]

        if "output" in self._config:
            self.__output = self._config["output"]

#endregion

#region Private Methods

    def __reed_fb(self):
        """Feedback function from the valve.

        Returns:
            float: State of the feedback.
        """

        position = 0.0

        # Determin is it analog or digital output.
        if "D" in self.__feedback:
            position = self._controller.digital_read(self.__feedback)

        elif "A" in self.__feedback:
            position = self._controller.analog_read(self.__feedback)

        return position * 10.0

    def __set_postion(self, position):

        # Determin is it analog or digital output.
        if "D" in self.__output:

            if position > 50:
                self._controller.digital_write(self.__output, True)

            else:
                self._controller.digital_write(self.__output, False)

        if "R" in self.__output:

            if position > 50:
                self._controller.digital_write(self.__output, True)

            else:
                self._controller.digital_write(self.__output, False)

        elif "A" in self.__output:
            value_pos = position / 10
            self._controller.analog_write(self.__output, value_pos)

#endregion

#region Public Methods

    def init(self):
        """Init the module.
        """

        self.min_pos = 0
        self.target_position = 0
        self.update()

    def update(self):
        """Update the valve.
        """

        # If the feedback is not switched off then read it.
        if self.__feedback != verbal_const.OFF:
            self._current_position = self.__reed_fb()

        # Else just update the current position.
        else:
            if self._current_position != self.target_position:
                self._current_position = self.target_position

        # If it is time then move the valve.
        if self._state.is_state(ValveState.Prepare):

            self.__set_postion(self.target_position)

            self.__logger.debug("{} @ {}".format(self.name, self.target_position))

            self._state.set_state(ValveState.Wait) 

    def shutdown(self):
        """Shutdown"""

        self.min_pos = 0
        self.target_position = 0
        self.update()

#endregion
