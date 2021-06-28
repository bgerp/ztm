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

import os

from utils.logger import get_logger
from utils.logic.timer import Timer
from utils.utils import disk_size

from plugins.base_plugin import BasePlugin
from plugins.vent.ventilation import Ventilation

from data import verbal_const

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

__class_name__ = "Vent"
"""Plugin class name."""

#endregion

class Vent(BasePlugin):
    """Ventilation controll plugin."""

#region Attributes

    __logger = None
    """Logger
    """

    __zones = {}
    """Zones.
    """

#endregion

#region Constructor / Destructor

    def __del__(self):
        """Destructor"""

        for zone in self.__zones:
            if zone is not None:
                del zone

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        zones_count = 0
        reg_zones_count = self._registers.by_name(self.key + ".zones_count")
        if reg_zones_count is not None:
            zones_count = reg_zones_count.value

        # Name the zones.
        prototype = "Ventilation {}"
        zones_count += 1
        for index in range(1, zones_count):

            # Create name.
            name = prototype.format(index)

            self.__zones[name] = Ventilation(\
                registers=self._registers, controller=self._controller,\
                identifier=index, key=self.key, name=name)

            # Initialize the module.
            self.__zones[name].init()

    def _update(self):
        """Update the plugin.
        """

        for key in self.__zones:
            self.__zones[key].update()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

        for key in self.__zones:
            self.__zones[key].shutdown()

#endregion
