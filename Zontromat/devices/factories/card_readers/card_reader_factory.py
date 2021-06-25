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

class CardReaderFactory:

    @staticmethod
    def create(**config):
        """Create device instace.
        """

        # The device instance.
        device = None

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

        # Port name
        port_name = None
        if "port_name" in config:
            port_name = config["port_name"]

        else:
            raise ValueError("No \"port_name\" argument has been passed.") 

        # Serial number
        serial_number = None
        if "serial_number" in config:
            serial_number = config["serial_number"]

        else:
            raise ValueError("No \"serial_number\" argument has been passed.") 

        # Teracom / ACT230
        if vendor == "Teracom" and  model == "act230":

            from devices.vendors.Teracom.act230.act230 import ACT230

            # Port name
            baudrate = None
            if "baudrate" in config:
                baudrate = config["baudrate"]

            else:
                raise ValueError("No \"baudrate\" argument has been passed.") 

            device = ACT230(
                port_name=port_name,
                baudrate=baudrate,
                serial_number=serial_number
            )

        # ACS / ACR122
        elif vendor == "ACS" and model == "acr122u":

            from devices.vendors.ACS.acr122u.acr122u import ACR122U

            device = ACR122U(
                port_name=port_name,
                serial_number=serial_number
            )

        else:
            raise NotImplementedError("The {} and {}, is not supported.".format(vendor,model))

        # Return the instance.
        return device
