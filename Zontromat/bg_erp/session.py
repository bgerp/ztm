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

import os

from utils.logger import get_logger

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

class Session():
    """Session control"""

#region Attributes

    __file_name = "\\"
    """Season file path."""

    __session_value = ""
    """Session"""

    __logger = None
    """Logger"""

#endregion

#region Properties

    @property
    def session(self):
        """Session ID"""
        return self.__session_value

#endregion

#region Constructor

    def __init__(self):
        """Constructor"""

        # Current file path. & Go to file.
        cwf = os.path.dirname(os.path.abspath(__file__))
        self.__file_name = os.path.join(cwf, "..", "..", "session.txt")

        self.__logger = get_logger(__name__)

#endregion

#region Public Methods

    def load(self):
        """Load session.

        Returns
        -------
        string
            Session string.
        """

        content = ""

        if os.path.exists(self.__file_name):
            with open(self.__file_name, "r+") as stream:
                content = stream.read()
                stream.close()

        else:
            self.__logger.error("No session file is found.")

        self.__session_value = content

    def save(self, season):
        """Save session.

        Parameters
        ----------
        season : string
            Session string.
        """

        with open(self.__file_name, "w+") as stream:
            stream.write(season)
            stream.close()

#endregion
