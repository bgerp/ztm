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

from utils.logger import get_logger

from devices.factories.flowmeters.base_flowmeter import BaseFlowmeter

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

class FlowmeterDN20(BaseFlowmeter):
    """Flowmeter input device Flowmeter DN20."""

#region Attributes

    __logger = None
    """Logger
    """

    __uart = 0
    """UART index.
    """

    __mb_id = 0
    """Modbus ID
    """

    __example_settings = {
        "vendor": "mainone",
        "model": "flowmeter_dn20",
        "options":
        {
            "uart": 1,
            "mb_id": 3,
        }
    }

#endregion

#region Properties

#endregion

#region Constructor

    def __init__(self, **config):

        super().__init__(config)

        self._vendor = "Mainone"

        self._model = "FlowmeterDN20"

        self.__logger = get_logger(__name__)

        if "uart" in self._config:
            self.__uart = self._config["uart"]

        if "mb_id" in self._config:
            self.__mb_id = self._config["mb_id"]

#endregion

#region Public Methods

    def init(self):

        pass


    def get_liters(self):
        """Get value."""

        # TODO: Read the device.
        # 0x000A	Int	0x03	Positive cumulative flow (unit: 1 / 100m³) 16 bits higher 	Read only
        # 0x000B	Int	0x03	Positive cumulative flow (unit: 1 / 100m³) lower 16 bits 	Read only
        # self._controller
        return 0

#endregion
