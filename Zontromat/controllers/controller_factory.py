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

from controllers.neuron.l503 import L503
from controllers.neuron.m503 import M503
from controllers.neuron.m523 import M523
from controllers.neuron.s103 import S103
from controllers.picons.x1_black_titanium import X1BlackTitanium

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

class ControllerFactory():
    """Controller factory class."""

#region Public Methods

    @staticmethod
    def create(**config):
        """Create controller."""

        controller = None

        if config["vendor"] == "unipi":

            if config["model"] == "S103":
                controller = S103(config)

            elif config["model"] == "M503":
                controller = M503(config)

            elif config["model"] == "M523":
                controller = M523(config)

            elif config["model"] == "L503":
                controller = L503(config)


        elif config["vendor"] == "pt":

            if config["model"] == "X1BlackTitanium":
                controller = X1BlackTitanium(config)

        return controller

    @staticmethod
    def get_info():
        """Get controller info."""

        config = None


        # Try to read NEURON
        try:
            config = Neuron.read_eeprom()
        except:
            pass

        return config

#endregion
