
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

class A20T20B2C(BaseValve):
    """Hydro Valve. Model: A20-T20-B2-C"""

#region Attributes

    __logger = None
    """Logger"""

    __output = None
    """Output physical signal."""

    __example_settings = {
        "vendor": "Tonhe",
        "model": "a20t20b2c",
        "options":
        {
            "output": "RO1",
        }
    }

#endregion

#region Properties

#endregion

#region Constructor

    def __init__(self, **config):

        super().__init__(config)

        self._vendor = "Tonhe"

        self._model = "A20T20B2C"

        self.__logger = get_logger(__name__)

        if "output" in self._config:
            self.__output = self._config["output"]

#endregion

#region Private Methods

    def __set_position(self, position):

        # Determine is it analog or digital output.
        # if ("D" in self.__output) or ("R" in self.__output):

        if position > 0:
            self._controller.digital_write(self.__output, True)
        else:
            self._controller.digital_write(self.__output, False)

#endregion

#region Public Methods

    def init(self):
        """Initialize the valve.
        """

        self.target_position = 0
        self.update()

    def update(self):
        """Update the valve.
        """

        if self._current_position != self.target_position:
            self._current_position = self.target_position

        # If it is time then move the valve.
        if self._state.is_state(ValveState.Prepare):
            self.__set_position(self.target_position)
            self.__logger.debug("{} @ {}".format(self.name, self.target_position))
            self._state.set_state(ValveState.Wait)

#endregion
