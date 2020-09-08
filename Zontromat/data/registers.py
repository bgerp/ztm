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
import json

from Zontromat.data.register import Register

from Zontromat.utils.logger import get_logger

from Zontromat.services.global_error_handler.global_error_handler import GlobalErrorHandler

from Zontromat.data.register import Scope

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2019, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
"""Credits"""

__license__ = "MIT"
"""License
@see https://opensource.org/licenses/MIT"""

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

class Registers(list):
    """Registers"""

#region Attributes

    __instance = None
    """Singelton instance."""

    __logger = None
    """Logger"""

#endregion

#region Constructor

    def __init__(self):
        """Constructor

        Parameters
        ----------
        self : Template
            Current class instance.
        """

        super().__init__()

        # Create logger.
        self.__logger = get_logger(__name__)

#endregion

#region Private Methods

#endregion

#region Public Methods

    def update(self, registers):
        """Update registers content.

        Parameters
        ----------
        registers : mixed
            Registers content.
        """

        if registers is None:
            raise ValueError("Registers can not be None.")

        # Go through registers.
        for name in registers:

            register = None

            # Update registers.
            if name in self.names():
                register = self.by_name(name)
                register.value = registers[name]

            # Add missing register.
            else:
                register = Register(name)
                register.value = registers[name]
                self.append(register)

                GlobalErrorHandler.log_unexpected_register(self.__logger, register)

    def exists(self, name):
        """Update registers content.

        Parameters
        ----------
        name : string
            Name of the register.

        Returns
        -------
        bool
            Exists or not.
        """

        result = False

        for register in self:
            if name in register.name:
                result = True
                break

        if not result:
            GlobalErrorHandler.log_register_not_found(self.__logger, name)

        return result

    def by_ts(self, ts):
        """Get registers with specified scope.

        Parameters
        ----------
        ts : float
            Timestamp

        Returns
        -------
        array
            Registers specified time.
        """

        result = Registers()

        for register in self:
            if ts < register.ts:
                result.append(register)

        return result

    def new_then(self, seconds):
        """Get registers newer then specific time from time of calling.

        Parameters
        ----------
        seconds : float
            seconds

        Returns
        -------
        array
            Registers specified time.
        """

        result = Registers()

        time_now = time.time()

        for register in self:

            delta_t = time_now - register.ts
            if delta_t < seconds:
                result.append(register)

        return result

    def by_scope(self, scope):
        """Get registers with specified scope.

        Parameters
        ----------
        scope : Scope(Enum)
            Scope

        Returns
        -------
        array
            Registers with scope.
        """

        result = Registers()

        for register in self:
            if scope == register.scope:
                result.append(register)

        return result

    def by_key(self, key):
        """Get registers with specified key in name.

        Parameters
        ----------
        key : string
            Key in name.

        Returns
        -------
        array
            Registers with key names.
        """

        result = Registers()

        for register in self:
            if key in register.name:
                result.append(register)

        return result

    def by_name(self, name):
        """Get register with specified name.

        Parameters
        ----------
        name : string
            Name of the register.

        Returns
        -------
        Register
            Registers with name.
        """

        result = None

        for register in self:
            if name == register.name:
                result = register
                break

        return result

    def names(self):
        """Get registers names.

        Returns
        -------
        array
            Array of names.
        """

        result = []

        for register in self:
            result.append(register.name)

        return result

    def to_dict(self):
        """Converts array in to dictionary.
        Consisted of name and value as (key and value).

        Returns
        -------
        array
            Array of names.
        """

        result = {}

        for register in self:
            result[register.name] = register.value

        return result

    def get_group(self, name):
        """Get registerr with specified group name.

        Parameters
        ----------
        name : string
            Name of the registers.

        Returns
        -------
        Register
            Registers with name.
        """

        result = []

        for register in self:
            if register.name.startswith("{}.".format(name)):
                result.append(register)

        return result

#endregion

#region Static Methods

    @staticmethod
    def __csv_escape(value):

        result = value

        if isinstance(value, str):
            if "," in value:
                result = "\"" + value + "\""

        elif isinstance(value, list):
            result = "\"" + str(value) + "\""

        elif isinstance(value, dict):
            result = "\"" + str(value) + "\""

        return result

    @staticmethod
    def __to_scope(scope):

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

    @staticmethod
    def __to_value(typ, value):

        out_value = None

        # bool
        if typ == "bool":
            if value == "False":
                out_value = False

            if value == "True":
                out_value = True

        # int
        elif typ == "int":
            out_value = int(value)

        # float
        elif typ == "float":
            out_value = float(value)

        # json
        elif typ == "json":

            # if value.startswith("\""):

            out_value = json.loads(value)

        return out_value

    @staticmethod
    def get_instance():
        """Singelton instance."""

        if Registers.__instance is None:
            Registers.__instance = Registers()

        return Registers.__instance

    @staticmethod
    def to_CSV(registers, file_path="registers.csv"):

        import csv

        with open("registers.csv", "w", newline="") as csv_file:

            fieldnames = ["name", "type", "range", "plugin", "scope", "default", "description"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

            for register in registers:

                value = Registers.__csv_escape(register.value)
                reg_range = Registers.__csv_escape(register.range)
                scope = str(register.scope).replace("Scope.", "").lower()
                description = Registers.__csv_escape(register.description)

                writer.writerow({"name": register.name,\
                                "type": register.data_type,\
                                "range": reg_range,\
                                "plugin": register.plugin_name,\
                                "scope": scope,\
                                "default": value,\
                                "description": description,\
                                })

            csv_file.close()

    @staticmethod
    def from_CSV(file_path=""):
        """Load registers from CSV"""

        registers = Registers()

        import csv
        
        with open(file_path, newline='') as csv_file:

            rows = csv.DictReader(csv_file)
            for row in rows:

                register = Register(row["name"])
                register.range = row["range"]
                register.plugin_name = row["plugin"]
                register.scope = Registers.__to_scope(row["scope"])
                register.value = Registers.__to_value(row["type"], row["default"])
                register.description = row["description"]

                registers.append(register)

        return registers

    @staticmethod
    def to_JSON(registers):
        """JSON output"""

        dict_regs = registers.to_dict()
        text = json.dumps(dict_regs, indent=4, sort_keys=True)

        with open("registers.json", "w") as json_file:
            json_file.write(text)
            json_file.close()

#endregion
