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

from controllers.neuron.neuron import Neuron

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
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

class S103(Neuron):
    """Neuron S103
    """

#region Attributes

    __map = \
    {\
        "identification": {"vendor": "unipi", "model": "S103"},\

        "LED0": {"dev": "led", "major_index": 1, "minor_index": 1},\
        "LED1": {"dev": "led", "major_index": 1, "minor_index": 2},\
        "LED2": {"dev": "led", "major_index": 1, "minor_index": 3},\
        "LED3": {"dev": "led", "major_index": 1, "minor_index": 4},\

        "DI0": {"dev": "input", "major_index": 1, "minor_index": 1},\
        "DI1": {"dev": "input", "major_index": 1, "minor_index": 2},\
        "DI2": {"dev": "input", "major_index": 1, "minor_index": 3},\
        "DI3": {"dev": "input", "major_index": 1, "minor_index": 4},\

        "DO0": {"dev": "do", "major_index": 1, "minor_index": 1},\
        "DO1": {"dev": "do", "major_index": 1, "minor_index": 2},\
        "DO2": {"dev": "do", "major_index": 1, "minor_index": 3},\
        "DO3": {"dev": "do", "major_index": 1, "minor_index": 4},\

        "AI0": {"dev": "ai", "major_index": 1, "minor_index": 1},\

        "AO0": {"dev": "ao", "major_index": 1, "minor_index": 1},\
    }

#endregion

#region Constructor

    def __init__(self, config):
        """Class constructor."""

        super().__init__(config)

        self._gpio_map = self.__map

#endregion
