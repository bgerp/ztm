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

__class_name__ = "EnergyCenter"
"""Plugin class name."""

#endregion

class ControlMode(Enum):
    """Controm Mode

    See: 9.5 Pump control register block

    Notes: Sets the control mode enumeration. Some modes are not supported by all E-pumps.
    """

    ConstantSpeed = 0
    ConstantFrequency = 1
    ConstantHead = 3
    ConstantPressure = 4
    ConstantDifferentialPressure = 5
    ProportionalPressure = 6
    ConstantFlow = 7
    ConstantTemperature = 8
    ConstantLevel = 10
    AUTOADAPT = 128
    FLOWADAPT = 129 # (set FLOWLIMIT in register 00106)
    ClosedLoopSensor = 130
