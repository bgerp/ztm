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

class Rule:
    """Rule description."""

#region Attributes

    __name = ""
    """Name of the rule."""

    __level = 0
    """Monitoring level."""

    __count = 1
    """Allowed count"""

#endregion

#region Constructor

    def __init__(self, name: str, level: int = 0, count: int = 1):
        """Constructor

        Parameters
        ----------
        self : Current class.
            Current class instance.

        name : str
            Name of the resource.

        level : int/enum
            Level of information.

        count : int
            Possible using of the resource.
        """

        self.__name = name

        self.__level = level

        self.__count = count

    def __str__(self):
        """String representation."""

        return "Name: {}; Level: {}; Count: {}"\
            .format(self.__name, self.__level, self.__count)

    __repr__ = __str__
    """Represent as string representation."""

#endregion

#region Properties

    @property
    def name(self):
        """Name of the resource.

        Returns
        -------
        str
            Name of the resource.
        """

        return self.__name

    @property
    def level(self):
        """Level of monitoring.

        Returns
        -------
        int/enum
            Level of monitoring.
        """

        return self.__level

    @property
    def count(self):
        """Level of monitoring.

        Returns
        -------
        int/enum
            Level of monitoring.
        """

        return self.__count

#endregion
