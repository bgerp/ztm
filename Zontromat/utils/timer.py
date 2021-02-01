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

class Timer:
    """Timer class."""

#region Attributes

    __expired = False
    """Expired flag."""

    __expiration_time = 0
    """Expiration time."""

    __last_time = 0
    """Last time."""

    __now = 0
    """Current time."""

    __callback = None
    """Callback when expire."""

#endregion

#region Constructor

    def __init__(self, expiration_time=None):
        """Constructor

        Parameters
        ----------
        self : Template
            Current class instance.
        """

        if expiration_time is not None:
            self.expiration_time = expiration_time

#endregion

#region Properties

    @property
    def now(self):
        """Now time.

        Returns
        -------
        float
            Current time of the timer.
        """

        return self.__now

    @property
    def expired(self):
        """Expired flag.

        Returns
        -------
        bool
            expired flag.
        """

        return self.__expired

    @property
    def expiration_time(self):
        """Get expiration time in seconds.

        Returns
        -------
        float
            Expiration time.
        """

        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, value):
        """Set expiration time in seconds.

        Parameters
        ----------
        value : value
            Expiration time in seconds.
        """

        self.__expiration_time = value

#endregion

#region Public Methods

    def update_last_time(self, value=None):
        """Update last time.

        Parameters
        ----------
        value : value
            Last update in time.
        """

        if value is None:
            self.__last_time = time.time()
        else:
            self.__last_time = value

    def update(self):
        """Update cycle of the timer."""

        # Recalculate passed time.
        self.__now = time.time()
        pass_time = self.__now - self.__last_time
        if pass_time > self.__expiration_time:
            self.__expired = True

            # Execute if there is callback attached.
            if self.__callback is not None:
                self.__callback(self)

            # Update current time.
            self.__last_time = time.time()

    def clear(self):
        """Clear"""

        if self.__expired:
            self.__expired = False

    def set_callback(self, value):
        """Set callback.

        Parameters
        ----------
        value : value
            Expiration time in seconds.
        """

        self.__callback = value

#endregion
