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

from plugins.blinds.blind import Blind

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

__class_name__ = "Blinds"
"""Plugin class name."""

#endregion

class Blinds(BasePlugin):
    """Blinds controller."""

#region Attributes

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
        self.__logger.info("Starting up the {}".format(self.name))

        self.__blinds = {}
        """Blinds.
        """

    def __del__(self):
        """Destructor"""

        for blind in self.__blinds:
            if blind is not None:
                del blind

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods (Registers)

    def __reg_blinds_count_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        def shutdown():
            for blind in self.__blinds:
                if blind is not None:
                    self.__blinds[blind].shutdown()
            self.__blinds = {}

        def init():
            # Name the zones.
            prototype = "BLIND_{}"
            blinds_count = register.value + 1
            for index in range(1, blinds_count):

                # Create name.
                name = prototype.format(index)

                # Register the zone.
                self.__blinds[name] = Blind(registers=self._registers,
                    controller=self._controller, identifier=index,
                    key=self.key, name="Blind")

                # Initialize the module.
                self.__blinds[name].init()

        try:
            if register.value != len(self.__blinds):
                shutdown()
                init()

            elif register.value == 0:
                shutdown()
        except Exception as e:
            self.__logger.error(e)

    def __init_registers(self):
        reg_name = f"{self.key}.count"
        reg_blinds_count = self._registers.by_name(reg_name)
        if reg_blinds_count is not None:
            reg_blinds_count.update_handlers = self.__reg_blinds_count_cb
            reg_blinds_count.update()

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__init_registers()

    def _update(self):
        """Update the plugin.
        """

        for key in self.__blinds:
            self.__blinds[key].update()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))
        for key in self.__blinds:
            self.__blinds[key].shutdown()

#endregion
