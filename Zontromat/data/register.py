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
import json

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

class Profiles(Enum):
    """Profiles enum class.
    """

    NONE = ""
    """Empty profile.
    """

    ZONE = "mz"
    """Micro zone.
    """

    HEAT_PUMP = "hp"
    """Heat pump.
    """

    DISTRIBUTION = "dt"
    """Distribution profile.
    """

    NORTH_SERVER_ROOMS = "ns"
    """North server room.
    """

    @staticmethod
    def from_str(profile):

        p_profile = profile.lower()
        out_profile = Profiles.NONE

        if p_profile == "mz":
            out_profile = Profiles.ZONE

        elif p_profile == "hp":
            out_profile = Profiles.HEAT_PUMP

        elif p_profile == "dt":
            out_profile = Profiles.DISTRIBUTION

        elif p_profile == "ns":
            out_profile = Profiles.NORTH_SERVER_ROOMS

        return out_profile

    def __str__(self):
        return self.value
    
    __repr__ = __str__

class Scope(Enum):
    """Registers scope.
    """
    NONE = 0
    Global = 1 # Global is like system.
    Device = 2 #
    System = 4 #
    Both = 7 #

    @staticmethod
    def from_str(scope):

        p_scope = scope.lower()
        out_scope = Scope.NONE

        if p_scope == "global":
            out_scope = Scope.Global

        elif p_scope == "device":
            out_scope = Scope.Device

        elif p_scope == "system":
            out_scope = Scope.System

        elif p_scope == "both":
            out_scope = Scope.Both

        return out_scope

class Register:
    """Register"""

#region Attributes

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
        """Register name.
        """

        self.__ts = 0
        """Timestamp of last update.
        """

        self.__value = None
        """Value of the register.
        """

        self.__scope = Scope.Global
        """Scope of register.
        """

        self.__handlers = []
        """Update handler.
        """

        self.__force = False
        """"""

        self.__plugin_name = ""
        """Plugin name.
        """

        self.__description = ""
        """Verbal register description.
        """

        self.__range = ""
        """Range!
        """

        self.__limit = 0.0
        """Limit!
        """

        self.__profiles = ""
        """Profiles that register are used from.
        """

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
                    self.description, self.ts,\
                    self.profiles)


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

        # In case of float.
        if self.data_type == "float":

            if value is not None:

                # Roundup to the third sign after the decimal delimiter.
                value = round(value, 3) # no self

                if abs(self.__value - value) < self.limit: # no self
                    return

        # Update time.
        self.__ts = int(time.time())

        # Update value.
        self.__value = value # here OK

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

    @property
    def profiles(self):
        """Profiles that register are used in.

        Returns:
            str: Profiles list that are separated by "|"
        """
        return self.__profiles

    @profiles.setter
    def profiles(self, value: (Profiles)):
        """Setter profiles that registers are used in.

        Args:
            value (str): Profiles list that are separated by "|"
        """
        self.__profiles = value

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
            "profiles": self.profiles,
        }

        return dict_obj

#endregion

#region Public Static Methods

    @staticmethod
    def create_profile(*profiles):
        return f"|".join(profiles)

    @staticmethod
    def to_value(data_type, value):

        out_value = None

        # bool
        if data_type == "bool":
            value_type = type(value)

            if value_type == bool:
                out_value = value

            else:
                if value == "false":
                    out_value = False

                if value == "true":
                    out_value = True

        # int
        elif data_type == "int":
            out_value = int(value)

        # float
        elif data_type == "float":
            out_value = float(value)

        # json
        elif data_type == "json":
            value_type = type(value)

            if value_type == list:
                out_value = value

            elif value_type == dict:
                out_value = value

            elif value_type == str:

                # Remove first "
                if value.startswith("\""):
                    value = value[1:]

                # Remove last "
                if value.endswith("\""):
                    value = value[:-1]

                # Convert single quotes to double.
                value = value.replace("\'", "\"") 

                # Converts to JSON.
                value = json.loads(value)

                out_value = value

            else:
                raise TypeError("Unsupported data type: {}".format(value_type))

        else:
            out_value = value

        return out_value

    @staticmethod
    def from_value(data_type: str, value):
        """Parse from value.

        Args:
            data_type (str): Data type string.
            value (any): Value input.

        Returns:
            _type_: _description_
        """
        out_value = None

        if data_type == "bool":
            if value:
                out_value = "true"
            else:
                out_value = "false"

        elif data_type == "str":
            if "," in value:
                out_value = "\"" + value + "\""
            else:
                out_value = value

        elif data_type == "json":
            out_value = json.dumps(value)

        else:
            out_value = value

        return out_value

#endregion
