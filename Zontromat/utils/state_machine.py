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

class StateMachine():
    """State machine class"""

#region Attributes

    __state = None
    """State of the machine."""

    __cb_on_change = None
    """On change callback."""

    __last_state = None
    """Last state."""

#endregion

#region Constructor

    def __init__(self, state=None):
        """Constructor

        Parameters
        ----------
        self : Template
            Current class instance.
        """

        if state is not None:
            self.set_state(state)

    def __str__(self):
        """String reprezentation of the state.

        Returns
        -------
        mixed
            State of the machine.
        """

        return str(self.get_state())

    __repr__ = __str__
    """Repr is Str"""

#endregion

#region Public Methods

    def get_state(self):
        """Get state machine.

        Returns
        -------
        enum
            State of the machine.
        """

        return self.__state

    def set_state(self, state):
        """Set state machine.

        Parameters
        ----------
        state : enum
            State of the machine.
        """

        if state != self.__state:

            # Set previous state.
            self.__last_state = self.__state

            # Set current state.
            self.__state = state
            if self.__cb_on_change is not None:
                self.__cb_on_change(self)

    def is_state(self, state):
        """Is eqals of the state of the machine.

        Returns
        -------
        bool
            Is eqals of the state of the machine.
        """

        return self.__state == state

    def on_change(self, callback):
        """Set on change callback.

        Parameters
        ----------
        callback : function pointer
            Pointer of the function callback.
        """

        if callback is not None:
            self.__cb_on_change = callback

    def was(self, state):
        """Check previous state.

        Parameters
        ----------
        state : enum
            Previous state of the machine.

        Returns
        -------
        bool
            Match to the given state.
        """
        return self.__last_state == state

#endregion
