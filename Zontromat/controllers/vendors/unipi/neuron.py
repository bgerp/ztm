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

from controllers.vendors.unipi.evok.evok import Evok

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

class Neuron(Evok):
    """Neuron base class.
    """

#region Constructor

    def __init__(self, config):
        """Class constructor."""

        super().__init__(config)

        # Read PLC information.
        plc_info = Evok.read_eeprom()

        # Read serial number.
        if plc_info is not None and "serial" in plc_info:
            if (plc_info["serial"] is not None) and ("serial" in config)\
                and (config["serial"] is None):
                config["serial"] = plc_info["serial"]

        # Read serial number.
        if plc_info is not None and "model" in plc_info:
            if plc_info["model"] is not None and config["model"] is None:
                config["model"] = plc_info["model"]

#endregion
