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
from controllers.neuron.neuron import Neuron

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

class ControllerFactory():
    """Controller factory class."""

#region Public Methods

    @staticmethod
    def create(**kwargs):
        """Create controller."""

        controller = None

        # Unipi suport 
        if kwargs["vendor"] == "unipi":

            # Read PLC information.
            plc_info = Neuron.read_eeprom()

            # Read serial number.
            if plc_info is not None and "serial" in plc_info:
                if (plc_info["serial"] is not None) and ("serial" in kwargs) and (kwargs["serial"] is None):
                    kwargs["serial"] = plc_info["serial"]   

            # Read serial number.
            if plc_info is not None and "model" in plc_info:
                if plc_info["model"] is not None and kwargs["model"] is None:
                    kwargs["model"] = plc_info["model"]   

            if kwargs["model"] == "S103":
                controller = S103(kwargs)

            elif kwargs["model"] == "M503":
                controller = M503(kwargs)

            elif kwargs["model"] == "M523":
                controller = M523(kwargs)

            elif kwargs["model"] == "L503":
                controller = L503(kwargs)

        # Pi-Cons Suport by POLYGONTeam Ltd.
        elif kwargs["vendor"] == "pt":

            if kwargs["model"] == "X1BlackTitanium":
                controller = X1BlackTitanium(kwargs)

        elif kwargs["vendor"] == "some_chines":
            # TODO: If the serial is not in the controller load it from file, if not create it and save it.
            pass 

        return controller

#endregion
