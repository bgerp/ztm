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

class Scope(Enum):
    """Registers scope.
    """
    NONE = 0
    Global = 1 # Global is like system.
    Device = 2 #
    System = 4 #
    Both = 7 #

class Register:
    """Register"""

#region Attributes

    __name = ""
    """Register name."""

    __ts = 0
    """Timestamp of last update."""

    __value = None
    """Value of the register."""

    __scope = Scope.Global
    """Scope of register."""

    __handlers = None
    """Update handler."""

    __force = False
    """"""

    __plugin_name = ""
    """Plugin name."""

    __description = ""
    """Verbal register description."""

    __range = ""
    """Range!"""

    __limit = 0.0
    """Limit!"""

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

        if self.__handlers is None:
            self.__handlers = []

    def __str__(self):
        """As string

        Returns
        -------
        str
            String representation of the instance.

        """

        return "Name: {}; Type: {}; Range: {}; Plugin: {}; Scope: {}; Value: {}; Description: {}; TS: {}"\
            .format(self.name, self.data_type,\
                    self.range, self.plugin_name,\
                    self.scope, self.value,\
                    self.description, self.ts)

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

        split = self.name.split(".")
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

        # Pass if the value is the same from the last time.
        if value == self.__value:
            return

        if self.data_type == "float":
            if abs(self.value - value) < self.limit:
                return

        # Update time.
        self.__ts = int(time.time())

        # Update value.
        self.__value = value

        self.update()

    @property
    def scope(self):
        """Returns the value of the scope flag.

        Returns
        -------
        Enum
            Value of the scope flag.
        """

        return self.__scope

    @property
    def data_type(self):
        """Data type of the register."""

        str_type = "None"

        if isinstance(self.__value, str):
            str_type = "str"

        elif isinstance(self.__value, bool):
            str_type = "bool"

        elif isinstance(self.__value, int):
            str_type = "int"

        elif isinstance(self.__value, float):
            str_type = "float"

        elif isinstance(self.__value, list):
            str_type = "json"

        elif isinstance(self.__value, dict):
            str_type = "json"

        return str_type

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
    def update_handlers(self):
        """Returns list of the handlers.

        Returns
        -------
        function
            List of the handlers.
        """

        return self.__handlers

    @update_handlers.setter
    def update_handlers(self, update_handler):
        """Add update handler to the list of the handlers.

        Parameters
        ----------
        update_handler : function
            Callback pointer.
        """

        if self.update_handlers is not None:
            self.update_handlers.append(update_handler)

    @property
    def force(self):
        """Returns force flag of the register.

        Returns
        -------
        bool
            Force flag value.
        """

        return self.__force

    @force.setter
    def force(self, value):
        """Set force flag of the register.

        Parameters
        ----------
        bool
            Force flag value.
        """

        self.__force = value

    @property
    def plugin_name(self):
        """Plugin Name"""

        return self.__plugin_name

    @plugin_name.setter
    def plugin_name(self, value):
        """Plugin name."""

        self.__plugin_name = value

    @property
    def description(self):
        """Description"""

        return self.__description

    @description.setter
    def description(self, value):
        """Description"""

        self.__description = value

    @property
    def range(self):
        """Range!"""

        return self.__range

    @range.setter
    def range(self, value):
        """Range!"""

        self.__range = value

    @property
    def limit(self):
        """Limit!"""

        return self.__limit

    @limit.setter
    def limit(self, value):
        """Limit!"""

        self.__limit = value

#endregion

#region Public Methods

    def update(self):

        # Execute CB.
        if self.update_handlers is not None:
            for item in self.update_handlers:
                if item is not None:
                    item(self)

    def get_json(self):
        """Converts register in to JSON ready dictionary.

        Returns:
            dict: JSON dict.
        """

        dict_obj = {
            "name": self.name,
            "data_type": self.data_type,
            "range": self.range,
            "plugin": self.plugin_name,
            "scope": self.scope.name,
            "default": self.value,
            "description": self.description,
            "limit": self.limit,
        }

        return dict_obj

#endregion
