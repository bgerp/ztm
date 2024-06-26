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

from devices.vendors.dallas.ds18b20.ds18b20 import DS18B20
from devices.vendors.sed_tronic.u1wtvs.u1wtvs import U1WTVS
from devices.vendors.donkger.xy_md02.xy_md02 import XYMD02
from devices.vendors.mainone.thermometer.ushm_inlet import USHMInlet
from devices.vendors.mainone.flowmeter_dn20.flowmeter_dn20 import FlowmeterDN20
from devices.vendors.gemho.envse.envse import Envse
from devices.vendors.cwt.mb318e.mb318e import MB318E

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

class ThermometersFactory:
    """Thermal sensors factory class.
    """

    @staticmethod
    def create(**config):
        """Create thermal device factory instance."""

        # The device.
        device = None

        # Name
        name = ""
        if "name" in config:
            name = config["name"]

        # Vendor
        vendor = None
        if "vendor" in config:
            vendor = config["vendor"]

        else:
            raise ValueError("No \"vendor\" argument has been passed.")

        # Model
        model = None
        if "model" in config:
            model = config["model"]

        else:
            raise ValueError("No \"model\" argument has been passed.")

        # Controller
        controller = None
        if "controller" in config:
            controller = config["controller"]

        else:
            raise ValueError("No \"controller\" argument has been passed.")

        # Dallas / DS18B20
        if vendor == "Dallas" and  model == "DS18B20":

            device = DS18B20(
                name=name,
                controller=controller,
                dev="temp",
                circuit=config["options"]['circuit']
            )

        # SEDtronic / u1wtvs
        elif vendor == "SEDtronic" and model == "u1wtvs":

            device = U1WTVS(
                name=name,
                controller=controller,
                dev=config["options"]['dev'],
                circuit=config["options"]['circuit']
            )

        # Donkger / u1wtvs
        elif vendor == "Donkger" and model == "XY-MD02":

            device = XYMD02(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id'],
                uart=config["options"]['uart']
            )

        # mainone / flowmeter_dn20
        elif vendor == "mainone" and  model == "flowmeter_dn20":

            device = FlowmeterDN20(
                name=name,
                controller=controller,
                uart=config["options"]["uart"],
                mb_id=config["options"]["mb_id"]
            )

        # Gemho / Envse
        elif vendor == "Gemho" and  model == "Envse":

            device = Envse(
                name=name,
                controller=controller,
                uart=config["options"]["uart"],
                mb_id=config["options"]["mb_id"]
            )

        # CWT / Envse
        elif vendor == "CWT" and  model == "MB318E":

            device = MB318E(
                name=name,
                controller=controller,
                uart=config["options"]["uart"],
                mb_id=config["options"]["mb_id"],
                chanel=config["options"]["chanel"]
            )

        else:
            raise NotImplementedError("The {} and {}, is not supported.".format(vendor, model))

        # Return the instance.
        return device
