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
import json
from datetime import date
from enum import Enum

from utils.logger import get_logger
#from utils.logic.timer import Timer
#from utils.logic.state_machine import StateMachine

from plugins.base_plugin import BasePlugin

from devices.vendors.no_vendor_6.boiler import Boiler

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

__class_name__ = "EnergyCenterCommon"
"""Plugin class name."""

#endregion

class EnergyCenterCommon(BasePlugin):
    """Energy center control plugin."""

#region Attributes

    __logger = None
    """Logger
    """

    __boilers = []
    """Electrical heater.s
    """

#endregion

#region Constructor / Destructor

    def __init__(self, config):
        """Constructor

        Args:
            config (config): Configuration of the object.
        """

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        self.__boilers.append(Boiler(name="B1", controller=self._controller, registers=self._registers))
        self.__boilers.append(Boiler(name="B2", controller=self._controller, registers=self._registers))
        self.__boilers.append(Boiler(name="B3", controller=self._controller, registers=self._registers))

    def __del__(self):
        """Destructor
        """

        # Boilers (RED)
        for boiler in self.__boilers:
            if boiler is not None:
                del boiler

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#region Private Methods

#endregion

#region Properties

#endregion

#region Public Methods

    def init(self):
        """Init the plugin.
        """

        # Boilers (RED)
        for boiler in self.__boilers:
            if boiler is not None:
                boiler.init()

    def update(self):
        """Update the plugin state.
        """

        # Boilers (RED)
        for boiler in self.__boilers:
            if boiler is not None:
                boiler.update()

    def shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

        # Boilers (RED)
        for boiler in self.__boilers:
            if boiler is not None:
                boiler.shutdown()

#endregion
