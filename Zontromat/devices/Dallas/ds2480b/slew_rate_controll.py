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

class PulldownSlewRateControl(Enum):
    """(PDSRC) Pulldown Slew Rate Control V/μs Configurable at flexible mode only.
        0_001_bbb_1
    """

    V15 = 0x11
    """15 V/μs [0x11] '0b0_001_000_1' (default)
    """

    V2p2 = 0x13
    """2.2 V/μs [0x13] '0b0_001_001_1'
    """

    V1p65 = 0x15
    """1.65 V/μs [0x15] '0b0_001_010_1'
    """

    V1p37 = 0x17
    """1.37 V/μs [0x17] '0b0_001_011_1'
    """

    V1p1 = 0x19
    """1.1 V/μs [0x19] '0b0_001_100_1'
    """

    V0p83 = 0x1B
    """0.83 V/μs [0x1B] '0b0_001_101_1'
    """

    V0p7 = 0x1D
    """0.7 V/μs  [0x1D] '0b0_001_110_1'
    """

    V0p55 = 0x1F
    """0.55 V/μs [0x1F] '0b0_001_111_1'
    """
