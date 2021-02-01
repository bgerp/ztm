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

class BColors:
    """B Colors text colorization."""

#region Attributes

    __HEADER = "\033[95m"
    __OKBLUE = "\033[94m"
    __OKGREEN = "\033[92m"
    __WARNING = "\033[93m"
    __FAIL = "\033[91m"
    __ENDC = "\033[0m"

#endregion

#region Constructor

    def __init__(self):
        self.enable()

#endregion

#region Public Methods

    def enable(self):
        """Enable
        """

        self.__HEADER = "\033[95m"
        self.__OKBLUE = "\033[94m"
        self.__OKGREEN = "\033[92m"
        self.__WARNING = "\033[93m"
        self.__FAIL = "\033[91m"
        self.__ENDC = "\033[0m"

    def disable(self):
        """Disable
        """
 
        self.__HEADER = ""
        self.__OKBLUE = ""
        self.__OKGREEN = ""
        self.__WARNING = ""
        self.__FAIL = ""
        self.__ENDC = ""

    def header(self, text):
        """Put header.

        Args:
            text (str): Input text.

        Returns:
            str: Output string.
        """

        return "{}{}{}".format(self.__HEADER, text, self.__ENDC)

    def okblue(self, text):
        """OK Blue color.

        Args:
            text (str): Input text.

        Returns:
            str: Output string.
        """
        return "{}{}{}".format(self.__OKBLUE, text, self.__ENDC)

    def okbreen(self, text):
        """OK Green color.

        Args:
            text (str): Input text.

        Returns:
            str: Output string.
        """
        return "{}{}{}".format(self.__OKGREEN, text, self.__ENDC)

    def warning(self, text):
        """Warning color.

        Args:
            text (str): Input text.

        Returns:
            str: Output string.
        """
        return "{}{}{}".format(self.__WARNING, text, self.__ENDC)

    def fail(self, text):
        """Fail color.

        Args:
            text (str): Input text.

        Returns:
            str: Output string.
        """
        return "{}{}{}".format(self.__FAIL, text, self.__ENDC)

#endregion
