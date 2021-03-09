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

import time
from enum import Enum

from utils.logger import get_logger

from plugins.base_plugin import BasePlugin

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from devices.no_vendors.no_vendor_3.valve import Valve
from devices.no_vendors.no_vendor_4.water_pump import WaterPump

# (Request from mail: Eml6429)

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

__class_name__ = "EnergyCenter"
"""Plugin class name."""

#endregion

class ValveControlGroup(BasePlugin):

#region Attributes

    __logger = None
    """Logger
    """

    __fw_valves = []
    """Forward valves.
    """

    __rev_valves = []
    """Reverse valves.
    """

    __fw_pumps = []
    """Forward pumps control.
    """    

    __rev_pumps = []
    """Revers pumps control.
    """    

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        if "fw_valves" in config:
            self.__fw_valves = config["fw_valves"]

        if "rev_valves" in config:
            self.__rev_valves = config["rev_valves"]

        if "fw_pumps" in config:
            self.__fw_pumps = config["fw_pumps"]

        if "rev_pumps" in config:
            self.__rev_pumps = config["rev_pumps"]

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                del valve

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                del valve

        if self.__fw_pumps is not None:
            for valve in self.__fw_pumps:
                del valve

        if self.__rev_pumps is not None:
            for valve in self.__rev_pumps:
                del valve

#endregion

#region Public Methods

    def set_position(self, position):
        """Set position.

        Args:
            position (int): Position of the valve.
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.set_position(position)

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.set_position(-position)

    def init(self):
        """Init the group.
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.init()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.init()

        if self.__fw_pumps is not None:
            for valve in self.__fw_pumps:
                valve.init()

        if self.__rev_pumps is not None:
            for valve in self.__rev_pumps:
                valve.init()

    def shutdown(self):
        """Shutdown the group.
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.shutdown()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.shutdown()

        if self.__fw_pumps is not None:
            for valve in self.__fw_pumps:
                valve.shutdown()

        if self.__rev_pumps is not None:
            for valve in self.__rev_pumps:
                valve.shutdown()

    def update(self):
        """Update valve state.
        """

        if self.__fw_valves is not None:
            for valve in self.__fw_valves:
                valve.update()

        if self.__rev_valves is not None:
            for valve in self.__rev_valves:
                valve.update()

        if self.__fw_pumps is not None:
            for valve in self.__fw_pumps:
                valve.update()

        if self.__rev_pumps is not None:
            for valve in self.__rev_pumps:
                valve.update()

#endregion

#region Public Static Methods

    @staticmethod
    def create(**kwargs):
        """Create the group by given settings.

        Returns:
            ValveControlGroup: Instance of the control group.
        """


        controller = None
        if "controller" in kwargs:
            controller = kwargs["controller"]

        registers = None
        if "registers" in kwargs:
            registers = kwargs["registers"]

        key = None
        if "key" in kwargs:
            key = kwargs["key"]

        group_name = None
        if "name" in kwargs:
            group_name = kwargs["name"]

        fw_valves = []
        if "fw_valves" in kwargs:
            fw_valves = kwargs["fw_valves"]

        rev_valves = []
        if "rev_valves" in kwargs:
            rev_valves = kwargs["rev_valves"]

        fw_pumps = []
        if "fw_pumps" in kwargs:
            fw_pumps = kwargs["fw_pumps"]

        rev_pumps = []
        if "rev_pumps" in kwargs:
            rev_pumps = kwargs["rev_pumps"]

        f_valves = []
        for name in fw_valves:
            f_valves.append(Valve(name=name, controller=controller, registers=registers, key="{}.{}".format(key, name)))

        r_valves = []
        for name in rev_valves:
            r_valves.append(Valve(name=name, controller=controller, registers=registers))

        f_pumps = []
        for name in fw_pumps:
            f_pumps.append(WaterPump(name=name, controller=controller, registers=registers))

        r_pumps = []
        for name in rev_pumps:
            r_pumps.append(WaterPump(name=name, controller=controller, registers=registers))

        control_group = ValveControlGroup(\
            name=group_name,\
            fw_valves=f_valves,\
            rev_valves=r_valves,\
            fw_pumps=f_pumps,\
            rev_pumps=r_pumps)

        return control_group

#endregion
