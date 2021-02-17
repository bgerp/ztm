#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Zontromat - Zonal Electronic Automation

Copyright (C) [2021] [POLYGONTeam Ltd.]

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

class Write1LowTime(Enum):
    """(W1LT) Write-1 Low Time, μs Configurable at flexible mode only. (0_100_bbb_1)
    """

    US8 = 0x41
    """8 μs [0x41] '0b0_100_000_1' (default in Regular / Flexible mode)
    """

    US9 = 0x43
    """9 μs [0x43] '0b0_100_001_1'
    """

    US10 = 0x45
    """10 μs [0x45] '0b0_100_010_1'
    """

    US11 = 0x47
    """11 μs [0x47] '0b0_100_011_1'
    """

    US12 = 0x49
    """12 μs [0x49] '0b0_100_100_1'
    """

    US13 = 0x4B
    """13 μs [0x4B] '0b0_100_101_1'
    """

    US14 = 0x4D
    """14 μs [0x4D] '0b0_100_110_1'
    """

    US15 = 0x4F
    """15 μs [0x4F] '0b0_100_111_1'
    """
    