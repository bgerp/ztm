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

from data.register import Register

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

class Registers:
    """Registers"""

#region Attributes

    __instance = None
    """Singelton instance."""

#endregion

#region Constructor

    def __init__(self):
        """Constructor

        Parameters
        ----------
        self : Template
            Current class instance.
        """

        self.__container = []

#endregion

#region Built In Methods

    def __getitem__(self, item):
        return self.__container[item] # delegate to li.__getitem__

    def __len__(self):
        return len(self.__container)

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

        bad_regs = Registers()
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
                bad_regs.add(register)

    def add(self, register):
        """Add register.

        Parameters
        ----------
        register : mixed
            Register instance.
        """

        self.__container.append(register)

    def delete(self):
        """Clear registers."""

        self.__container.clear()

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

        for register in self.__container:
            if name in register.name:
                result = True
                break

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

        for register in self.__container:
            if ts < register.ts:
                result.add(register)

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

        for register in self.__container:
            if scope == register.scope:
                result.add(register)

        return result

    def by_source(self, source):
        """Get registers with specified source.

        Parameters
        ----------
        source : Source(Enum)
            Source

        Returns
        -------
        array
            Registers with source.
        """

        result = Registers()

        for register in self.__container:
            if source == register.source:
                result.add(register)

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

        for register in self.__container:
            if key in register.name:
                result.add(register)

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

        for register in self.__container:
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

        for register in self.__container:
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

        for register in self.__container:
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

        for register in self.__container:
            if register.name.startswith("{}.".format(name)):
                result.append(register)

        return result

#endregion

#region Static Methods

    @staticmethod
    def get_instance():
        """Singelton instance."""

        if Registers.__instance is None:
            Registers.__instance = Registers()

        return Registers.__instance

#endregion
