
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

from utils.logic.state_machine import StateMachine

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
    """Valve base class."""

#region Attributes

    _state = None
    """Valve state.
    """

    _min_pos = 0
    """Minimum allowed position.
    """

    _max_pos = 100
    """Maximum allowed position.
    """

    __target_position = 0
    """Target position.
    """

    _current_position = 0
    """Current position.
    """

    _in_place_err = 0.1
    """In place error.
    """

#endregion

#region Constructor

    def __init__(self, config):
        """Convector

        Args:
            config (dict): Configuration
        """

        super().__init__(config)

        self._state = StateMachine(ValveState.NONE)

#endregion

#region Properties

    @property
    def min_pos(self):
        """Minimum position.

        Returns:
            float: Minimum position.
        """
        return self._min_pos

    @min_pos.setter
    def min_pos(self, value):
        """Minimum position.

        Args:
            value (float): Minimum position.
        """

        in_value = value

        if value > 100:
            in_value = 100

        if value < 0:
            in_value = 0

        if in_value > self.max_pos:
            in_value = self.max_pos

        self._min_pos = value

    @property
    def max_pos(self):
        """Maximum position.

        Returns:
            float: Maximum position.
        """
        return self._max_pos

    @max_pos.setter
    def max_pos(self, value):
        """Maximum position.

        Args:
            value (float): Maximum position.
        """

        in_value = value

        if value > 100:
            in_value = 100

        if value < 0:
            in_value = 0

        if value < self.min_pos:
            in_value = self.min_pos

        self._max_pos = in_value

    @property
    def current_position(self):
        """Current position.

        Returns:
            float: Current position [%]
        """

        return self._current_position

    @property
    def target_position(self):
        """Target postion.

        Returns:
            float: Target position [%]
        """
        return self.__target_position

    @target_position.setter
    def target_position(self, position):
        """Set the position of the valve.

        Args:
            position (int): Position of the valve.
        """

        if position == self.__target_position:
            return

        if self.target_position > 100:
            position = 100

        if self.target_position > self.max_pos:
            position = self.max_pos

        if self.target_position < 0:
            position = 0

        if self.target_position < self.min_pos:
            position = self.min_pos

        self.__target_position = position
        self._state.set_state(ValveState.Prepare)

    @property
    def in_place(self):
        """Returns if the valve is in place.

        Returns:
            bool: In place flag.
        """

        # Calculate the delta between target and current positions.
        delta = abs(self.current_position - self.target_position)

        # If the delta is less then in place error we acpt that the valve is in position.
        return delta < self._in_place_err

#endregion

#region Protected Methods

#endregion

#region Public Methods

    def calibrate(self):
        """Calibrate the valve.
        """

        pass

#endregion
