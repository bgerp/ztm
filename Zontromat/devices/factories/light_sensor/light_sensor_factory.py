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

from devices.vendors.SEDtronic.u1wtvs.u1wtvs import U1WTVS

from devices.vendors.PT.light_sensor.light_sensor import LightSensor

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

class LightSensorFactory:

    @staticmethod
    def create(**config):
        """Create device instace.
        """

        # The device instance.
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

        # POLYGON Team / light_sensor
        if vendor == "PT" and  model == "light_sensor":

            device = LightSensor(
                name=name,
                controller=controller,
                analog_input=config["params"][2]
            )

        # SEDtronic / u1wtvs
        elif vendor == "SEDtronic" and model == "u1wtvs":

            device = U1WTVS(
                name=name,
                controller=controller,
                dev=config["params"][2],
                circuit=config["params"][3],
            )

        # Not implemented device.
        else:
            raise NotImplementedError("The {} and {}, is not supported.".format(vendor,model))

        # Return the instance.
        return device
