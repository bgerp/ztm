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

from controllers.vendors.unipi.neuron import Neuron

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

__class_name__ = "L503"
"""Controller target class.
"""

#endregion

class L503(Neuron):
    """Neuron L503
    """

#region Attributes

    __map = \
    {\
        "identification": {"vendor": "unipi", "model": "L503"},\

        "LED0": {"dev": "led", "major_index": 1, "minor_index": 1},\
        "LED1": {"dev": "led", "major_index": 1, "minor_index": 2},\
        "LED2": {"dev": "led", "major_index": 1, "minor_index": 3},\
        "LED3": {"dev": "led", "major_index": 1, "minor_index": 4},\

        "DI0": {"dev": "input", "major_index": 1, "minor_index": 1},\
        "DI1": {"dev": "input", "major_index": 1, "minor_index": 2},\
        "DI2": {"dev": "input", "major_index": 1, "minor_index": 3},\
        "DI3": {"dev": "input", "major_index": 1, "minor_index": 4},\

        "DI4": {"dev": "input", "major_index": 2, "minor_index": 1},\
        "DI5": {"dev": "input", "major_index": 2, "minor_index": 2},\
        "DI6": {"dev": "input", "major_index": 2, "minor_index": 3},\
        "DI7": {"dev": "input", "major_index": 2, "minor_index": 4},\
        "DI8": {"dev": "input", "major_index": 2, "minor_index": 5},\
        "DI9": {"dev": "input", "major_index": 2, "minor_index": 6},\

        "DI10": {"dev": "input", "major_index": 3, "minor_index": 1},\
        "DI11": {"dev": "input", "major_index": 3, "minor_index": 2},\
        "DI12": {"dev": "input", "major_index": 3, "minor_index": 3},\
        "DI13": {"dev": "input", "major_index": 3, "minor_index": 4},\
        "DI14": {"dev": "input", "major_index": 3, "minor_index": 5},\
        "DI15": {"dev": "input", "major_index": 3, "minor_index": 6},\
        "DI16": {"dev": "input", "major_index": 3, "minor_index": 7},\
        "DI17": {"dev": "input", "major_index": 3, "minor_index": 8},\
        "DI18": {"dev": "input", "major_index": 3, "minor_index": 9},\
        "DI19": {"dev": "input", "major_index": 3, "minor_index": 10},\
        "DI20": {"dev": "input", "major_index": 3, "minor_index": 11},\
        "DI21": {"dev": "input", "major_index": 3, "minor_index": 12},\
        "DI22": {"dev": "input", "major_index": 3, "minor_index": 13},\
        "DI23": {"dev": "input", "major_index": 3, "minor_index": 14},\

        "DO0": {"dev": "do", "major_index": 1, "minor_index": 1},\
        "DO1": {"dev": "do", "major_index": 1, "minor_index": 2},\
        "DO2": {"dev": "do", "major_index": 1, "minor_index": 3},\
        "DO3": {"dev": "do", "major_index": 1, "minor_index": 4},\

        "RO0": {"dev": "relay", "major_index": 2, "minor_index": 1},\
        "RO1": {"dev": "relay", "major_index": 2, "minor_index": 2},\
        "RO2": {"dev": "relay", "major_index": 2, "minor_index": 3},\
        "RO3": {"dev": "relay", "major_index": 2, "minor_index": 4},\
        "RO4": {"dev": "relay", "major_index": 3, "minor_index": 1},\
        "RO5": {"dev": "relay", "major_index": 3, "minor_index": 2},\
        "RO6": {"dev": "relay", "major_index": 3, "minor_index": 3},\
        "RO7": {"dev": "relay", "major_index": 3, "minor_index": 4},\
        "RO8": {"dev": "relay", "major_index": 3, "minor_index": 5},\
        "RO9": {"dev": "relay", "major_index": 3, "minor_index": 6},\
        "RO10": {"dev": "relay", "major_index": 3, "minor_index": 7},\
        "RO11": {"dev": "relay", "major_index": 3, "minor_index": 8},\
        "RO12": {"dev": "relay", "major_index": 3, "minor_index": 9},\
        "RO13": {"dev": "relay", "major_index": 3, "minor_index": 10},\
        "RO14": {"dev": "relay", "major_index": 3, "minor_index": 11},\
        "RO15": {"dev": "relay", "major_index": 3, "minor_index": 12},\
        "RO16": {"dev": "relay", "major_index": 3, "minor_index": 13},\
        "RO17": {"dev": "relay", "major_index": 3, "minor_index": 14},\

        "AI0": {"dev": "ai", "major_index": 1, "minor_index": 1},\
        "AI1": {"dev": "ai", "major_index": 2, "minor_index": 1},\
        "AI2": {"dev": "ai", "major_index": 2, "minor_index": 2},\
        "AI3": {"dev": "ai", "major_index": 2, "minor_index": 3},\
        "AI4": {"dev": "ai", "major_index": 2, "minor_index": 4},\

        "AO0": {"dev": "ao", "major_index": 1, "minor_index": 1},\
        "AO1": {"dev": "ao", "major_index": 2, "minor_index": 1},\
        "AO2": {"dev": "ao", "major_index": 2, "minor_index": 2},\
        "AO3": {"dev": "ao", "major_index": 2, "minor_index": 3},\
        "AO4": {"dev": "ao", "major_index": 2, "minor_index": 4},\
    }

#endregion

#region Constructor

    def __init__(self, config):
        """Class constructor."""

        super().__init__(config)

        self._gpio_map = self.__map

#endregion
