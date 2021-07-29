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
from utils.logic.timer import Timer

from plugins.base_plugin import BasePlugin

from data.register import Register

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

__class_name__ = "Alarm"
"""Plugin class name."""

#endregion

class Alarm(BasePlugin):
    """Blinds controller device."""

#region Attributes

    __logger = None
    """Logger"""

    __update_timer = None
    """Update timer."""

#endregion

#region Private Methods (Registers Interface)

    def __sound_device_settings_cb(self, register: Register):

        # TODO:  - Call the visual device factory.
        # TODO:  - Build the visual device interface.
        # TODO:  - Check is it possible to build.

        self.__logger.debug("Init the sound device.")

    def __visual_device_settings_cb(self, register: Register):

        # TODO:  - Call the visual device factory.
        # TODO:  - Build the visual device interface.
        # TODO:  - Check is it possible to build.

        self.__logger.debug("Init the visual device.")

    def __init_registers(self):

        visual_device_settings = self._registers.by_name("{}.device.visual.settings".format(self.key))
        if visual_device_settings is not None:
            visual_device_settings.update_handlers = self.__visual_device_settings_cb
            visual_device_settings.update()

        sound_device_settings = self._registers.by_name("{}.device.sound.settings".format(self.key))
        if sound_device_settings is not None:
            sound_device_settings.update_handlers = self.__sound_device_settings_cb
            sound_device_settings.update()

#endregion

#region Private Methods

    def __do_job(self):
        """Do the JOB method."""

        self.__logger.info("Do some job.")

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__update_timer = Timer(1)

        self.__init_registers()

    def _update(self):
        """Update the plugin.
        """
        # Update the timer.
        self.__update_timer.update()

        if self.__update_timer.expired:
        
            self.__update_timer.clear()
        
            self.__do_job()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
