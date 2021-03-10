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

class Configuarable:
    """This class is dedicated to be base for each configurable class."""

#region Attributes

    _config = None
    """Configuration.
    """

    __key = ""
    """Key of the plugin.
    """

    __name = ""
    """Name
    """    

#endregion

#region Properties

    @property
    def name(self):
        """Name

        Returns:
            str: Name of the object.
        """

        return self.__name

    @property
    def key(self):
        """Key

        Returns:
            str: Key of the object.
        """

        return self.__key

#endregion

#region Constructor

    def __init__(self, config):
        """Constructor

        Args:
            config (mixed): Device configuration.
        """

        self._config = config

        if "name" in self._config:
            self.__name = self._config["name"]

        if "key" in config:
            self.__key = self._config["key"]

    def __del__(self):

        pass

#endregion
