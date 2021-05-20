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

from plugins.base_plugin import BasePlugin
from plugins.echp.heat_pump_control_group import HeatPumpControllGroup

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

__class_name__ = "EnergyCenterHeatpump"
"""Plugin class name."""

#endregion

class EnergyCenterHeatpump(BasePlugin):
    """Energy center heat pump controll plugin."""

#region Attributes

    __logger = None
    """Logger
    """

    __heat_pump_control_group = None
    """Heat pump controll group.
    """

#endregion

#region Constructor / Destructor

    def __del__(self):
        """Destructor
        """

        # Heat pump
        if self.__heat_pump_control_group is not None:
            del self.__heat_pump_control_group

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def init(self):
        """Init the plugin.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        # Card reader allowed IDs.
        hp_count = 0
        reg_hp_count = self._registers.by_name(self.key + ".hp.count")
        if reg_hp_count is not None:
            hp_count = reg_hp_count.value

        self.__heat_pump_control_group = HeatPumpControllGroup(
            name="Heat Pump Controll Group",
            key="{}.hpcg".format(self.key),
            controller=self._controller,
            registers=self._registers)

        if self.__heat_pump_control_group is not None:
            self.__heat_pump_control_group.init()

    def update(self):
        """Update the plugin state.
        """

        self.__heat_pump_control_group.update()

    def shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

        # Shutdown in order the heatpump.
        self.__heat_pump_control_group.shutdown()

#endregion
