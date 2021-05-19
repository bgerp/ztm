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

from devices.vendors.Tonhe.a20m15b2c.a20m15b2c import A20M15B2C
from devices.vendors.Flowx.flx05f.flx05f import FLX05F

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

class ValveFactory:

    @staticmethod
    def create(**config):
        """Create valve device instace."""

        # The device.
        device = None

        # Name
        name = ""
        if "name" in config:
            name = config["name"]

        # Vendor
        vendor = None
        if "params" in config:
            vendor = config["params"][0]

        else:
            raise ValueError("No \"vendor\" argument has been passed.") 

        # Model
        model = None
        if "params" in config:
            model = config["params"][1]

        else:
            raise ValueError("No \"model\" argument has been passed.") 

        # Controller
        controller = None
        if "controller" in config:
            controller = config["controller"]

        else:
            raise ValueError("No \"controller\" argument has been passed.") 

        # Flowx / FLX-05F / (DO0,R0) / (DO1,R1) / DI0 / DI1
        if vendor == "Flowx" and  model == "FLX-05F":

            l_config = {
                "name": name,
                "controller": controller,
                "output_cw": config["params"][2],
                "output_ccw": config["params"][3],
                "limit_cw": config["params"][4],
                "limit_ccw": config["params"][5],
            }

            device = FLX05F(l_config)

        # Tonhe / a20m15b2c / (RO0/AO0) / AI0
        elif vendor == "Tonhe" and model == "a20m15b2c":

            l_config = {
                "name": name,
                "controller": controller,
                "output": config["params"][2],
                "feedback": config["params"][3],
                "min_pos": int(config["params"][4]),
                "max_pos": int(config["params"][5]),
            }

            device = A20M15B2C(l_config)

        else:
            raise NotImplementedError("The {} and {}, is not supported.".format(vendor,model))

        # Return the reader.

        return device