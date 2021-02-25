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

from controllers.picons.picons import PiCons

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

__class_name__ = "X1BlackTitanium"
"""Controller target class.
"""

#endregion

class X1BlackTitanium(PiCons):
    """This class is dedicated to transfer information from and to PiCons series."""

#region Attributes

    __map = \
    {\
        "identification": {"vendor": "pt", "model": "X1BlackTitanium"},\

        "DO0": {"dev": "do", "unit": "LogicLevel", "id": 0, "name": "Relay 1"},\
        "DO1": {"dev": "do", "unit": "LogicLevel", "id": 1, "name": "Relay 2"},\
        "DO2": {"dev": "do", "unit": "LogicLevel", "id": 2, "name": "Relay 3"},\
        "DO3": {"dev": "do", "unit": "LogicLevel", "id": 3, "name": "Relay 4"},\

        "DI0": {"dev": "input", "unit": "LogicLevel", "id": 4, "name": "Digital In 1"},\
        "DI1": {"dev": "input", "unit": "LogicLevel", "id": 5, "name": "Digital In 2"},\
        "DI2": {"dev": "input", "unit": "LogicLevel", "id": 6, "name": "Digital In 3"},\
        "DI3": {"dev": "input", "unit": "LogicLevel", "id": 7, "name": "Digital In 4"},\
        "DI4": {"dev": "input", "unit": "LogicLevel", "id": 8, "name": "Digital In 5"},\
        "DI5": {"dev": "input", "unit": "LogicLevel", "id": 9, "name": "Digital In 6"},\

        "AI0": {"dev": "ai", "unit": "V", "id": 12, "name": "Analog In 1"},\
        "AI1": {"dev": "ai", "unit": "V", "id": 13, "name": "Analog In 2"},\
        "AI2": {"dev": "ai", "unit": "V", "id": 14, "name": "Analog In 3"},\
        "AI3": {"dev": "ai", "unit": "V", "id": 15, "name": "Analog In 4"},\
        "AI4": {"dev": "ai", "unit": "V", "id": 16, "name": "Analog In 5"},\
        "AI5": {"dev": "ai", "unit": "V", "id": 17, "name": "Analog In 6"},\
        "AI6": {"dev": "ai", "unit": "V", "id": 18, "name": "Analog In 7"},\
        "AI7": {"dev": "ai", "unit": "V", "id": 19, "name": "Analog In 8"},\
    }

#endregion

#region Constructor

    def __init__(self, config):
        """Class constructor."""

        super().__init__(config)

        self._gpio_map = self.__map

#endregion
