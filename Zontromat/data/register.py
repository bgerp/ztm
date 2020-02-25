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
from enum import Enum

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

class Scope(Enum):
    """Registers scope."""

    Global = 1
    Local = 2

class Source(Enum):
    """Source update modifier."""

    Zontromat = 0
    bgERP = 1

class Register:
    """Register"""

#region Attributes

    __name = ""
    """Register name."""

    __ts = None
    """Timestamp of last update."""

    __value = None
    """Value of the register."""

    __scope = Scope.Global
    """Scope of register."""

    __source = Source.bgERP
    """Source update modifier."""

    __update_handler = None
    """Update handler."""

#endregion

#region Constructor

    def __init__(self, name):
        """Constructor

        Parameters
        ----------
        self : Current class.
            Current class instance.
        """

        self.__name = name

    def __str__(self):
        """As string

        Returns
        -------
        str
            String representation of the instance.

        """
        return "Name: {}; TS: {}; Value: {}; Scope: {}; Source: {}"\
            .format(self.name, self.ts, self.value, self.scope, self.source)

    __repr__ = __str__

#endregion

#region Properties

    @property
    def name(self):
        """Returns the name of the register.

        Returns
        -------
        str
            Name of the register.
        """
        return self.__name

    @property
    def base_name(self):
        """Returns the base name of the register.

        Returns
        -------
        str
            Base name of the register.
        """
        value = ""

        split = self.name.split('.')
        if split:
            value = split[0]

        return value

    # @name.setter
    # def name(self, name):
    #     """Set the name of the register.

    #     Parameters
    #     ----------
    #     host : str
    #         Name of the register.
    #     """
    #     self.__name = name

    @property
    def ts(self):
        """Returns the timestamp of the register.

        Returns
        -------
        int
            Timestamp of the register.
        """
        return self.__ts

    @property
    def value(self):
        """Returns the value of the register.

        Returns
        -------
        mixed
            Value of the register.
        """
        return self.__value

    @value.setter
    def value(self, value):
        """Set the value of the register.

        Parameters
        ----------
        value : mixed
            Value of the register.
        """

        # Update time.
        self.__ts = int(time.time())

        # Update value.
        self.__value = value

        # Execute CB.
        if self.__update_handler is not None:
            self.__update_handler(self)

    @property
    def scope(self):
        """Returns the value of the scope flag.

        Returns
        -------
        Enum
            Value of the scope flag.
        """

        return self.__scope

    @scope.setter
    def scope(self, value):
        """Set the value of the scope flag.

        Parameters
        ----------
        scope : Enum
            Value of the scope flag.
        """

        self.__scope = value

    @property
    def source(self):
        """Returns the value of the source flag.

        Returns
        -------
        Enum
            Value of the source flag.
        """

        return self.__source

    @source.setter
    def source(self, value):
        """Set the value of the source flag.

        Parameters
        ----------
        source : Enum
            Value of the source flag.
        """

        self.__source = value

    @property
    def update_handler(self):
        """Returns the timestamp of the register.

        Returns
        -------
        int
            Timestamp of the register.
        """
        return self.__update_handler

    @update_handler.setter
    def update_handler(self, update_handler):
        """Set the timestamp of the register.

        Parameters
        ----------
        host : int
            Timestamp of the register.
        """
        self.__update_handler = update_handler


#endregion
