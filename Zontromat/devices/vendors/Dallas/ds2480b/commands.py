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

class Commands(Enum):
    """Commands
    """

    SwitchToDataMode = 0xE1
    """[0xE1] Switch to Data Mode
    """


    SwitchToCommandMode = 0xE3
    """[0xE3] Switch to Command Mode
    """

    CommandResetAtFlexSpeed = 0xC5
    """[0xC5] = 110 0 01=flex 01
    """

    CommandSearchAcceleratorControlOnAtRegularSpeed = 0xB1
    """Search accelerator control ON at regular speed.
    """

    CommandSearchAcceleratorControlOffAtRegularSpeed = 0xA1
    """Search accelerator control OFF at regular speed.
    """

    CommandSingleBitReadDataAtFlexSpeed = 0b10010101
    """Single bit read data at flex speed.
    """    