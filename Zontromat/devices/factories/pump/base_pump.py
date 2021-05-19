
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

from devices.base_device import BaseDevice

from devices.factories.valve.valve_state import ValveState

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

class BaseValve(BaseDevice):
    """Card reader base class."""

#region Attributes

    _valve_state = ValveState.NONE

    __target_position = 0

    __current_position = 0

#endregion

#region Constructor

    def __init__(self, config):

        super().__init__(config)

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
        self._valve_state.set_state(ValveState.Prepare)

        self.__logger.debug("Set position of {} to {}".format(self.name, self.__target_position))

#endregion

#region Protected Methods

#region Public Methods

    def get_pos(self):
        """Set position of the output.

        Args:
            position (int): Output position.
        """

        return 0

    def set_pos(self, position):
        """Set position of the output.

        Args:
            position (int): Output position.
        """

        return 0

    def in_place(self):
        """Returns if the valve is in place."""

        return 0

#endregion
