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

from devices.base_device import BaseDevice

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

class DS18B20(BaseDevice):
    """Digital thermometer by Dalas."""

#region Public Methods

    def value(self):
        """Value of the thermometer."""

        return self._controller.read_temperature(self._config["dev"], self._config["circuit"])

#endregion

#region Public Static Methods

    @classmethod
    def create(self, name, key, register, controller):
        """Value of the thermometer."""

        instance = None

        params = register.split("/")

        circuit = params[2]
        dev = params[0]
        typ = params[1]

        if circuit is not None and\
            dev is not None and\
            typ is not None:

            config = \
            {\
                "name": name,
                "dev": dev,
                "circuit": circuit,
                "typ": typ,
                "controller": controller
            }

            instance = DS18B20(config)

        return instance

#endregion
