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

from devices.vendors.enbra.sk09 import SK09
from devices.vendors.mainone.flowmeter_dn20.flowmeter_dn20 import FlowmeterDN20
from devices.vendors.smii.mw_uml_15.mw_uml_15 import MW_UML_15

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

class FlowmeterFactory:
    """Flowmeters factory.
    """

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

        # enbra / SK09
        if vendor == "enbra" and  model == "sk09":

            device = SK09(
                name=name,
                controller=controller,
                input=config["options"]["input"]
            )

        # mainone / flowmeter_dn20
        elif vendor == "mainone" and  model == "flowmeter_dn20":

            device = FlowmeterDN20(
                name=name,
                controller=controller,
                uart=config["options"]["uart"],
                mb_id=config["options"]["mb_id"]
            )

        # Shanghai Mingwan Inteligent Instrument Com.Ltd. / MW-UML-15
        # Wattmeter subcontractor of Mainone.
        elif vendor == "smii" and model == "mw_uml_15":

            device = MW_UML_15(
                name=name,
                controller=controller,
                uart=config["options"]["uart"],
                mb_id=config["options"]["mb_id"]
            )

        else:
            raise NotImplementedError("The {} and {}, is not supported.".format(vendor, model))

        # Return the instance.
        return device
