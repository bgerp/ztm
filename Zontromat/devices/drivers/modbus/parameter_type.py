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

class ParameterType(Enum):
    """Parameter data type enumeration class."""

    UINT16_T_LE = "uint16_t_le"
    INT16_T_LE = "int16_t_le"
    UINT32_T_LE = "uint32_t_le"
    INT32_T_LE = "int32_t_le"
    UINT32_T_BE = "uint32_t_be"
    UINT64_T_LE = "uint64_t_le"
    INT64_T_LE = "int64_t_le"
    FLOAT = "float"
    STRING = "string"
    REAL = "real"
    ARR_UINT16_T_LE = "arr_uint16_t_le"

#region Public static Methods

    @staticmethod
    def is_valid(value):
        """Check validity of the data type.

        Args:
            value (str): Target data type for check.

        Return:
            bool: Valid data type.
        """
        state = False

        for item in ParameterType:
            if value == item:
                state = True
                break

        return state

#endregion
