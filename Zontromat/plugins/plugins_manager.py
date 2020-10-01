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

import traceback

from enum import Enum

from utils.logger import get_logger

# Plugins
from plugins.access_control.access_control import AccessControl
from plugins.blinds.blinds import Blinds
from plugins.monitoring.monitoring import Monitoring
from plugins.environment.environment import Environment
from plugins.hvac.hvac import HVAC
from plugins.lighting.lighting import Lighting
from plugins.sys.sys import Sys

from services.global_error_handler.global_error_handler import GlobalErrorHandler

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
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

class Plugins(Enum):
    """Zone device enumerator."""

    AccessControl = 1
    Blinds = 2
    Monitoring = 3
    Environment = 4
    HVAC = 5
    MainLight = 6
    Sys = 7

class PluginsManager:
    """Template class doc."""

#region Attributes

    __logger = None
    """Logger"""

    __registers = None
    """Registers"""

    __controller = None
    """Controller"""

    __plugins = None
    """Plugins"""

#endregion

#region Constructor

    def __init__(self, registers, controller):
        """Constructor

        Parameters
        ----------
        registers : Registers
            Registers class instance.
        controller : mixed
            Hardware controller.
        """

        self.__logger = get_logger(__name__)
        self.__plugins = {}
        self.__registers = registers
        self.__controller = controller
        self.__add_handlers()

#endregion

#region Private Methods

    def __prepare_config(self, name, key):

        config = {
            "name": name,
            "key": key,
            "registers": self.__registers,
            "controller": self.__controller,
        }

        return config

    def __access_control_enabled(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and Plugins.AccessControl not in self.__plugins:
            config = self.__prepare_config("Access control", register.base_name)
            self.__plugins[Plugins.AccessControl] = AccessControl(config)
            self.__plugins[Plugins.AccessControl].init()

        elif not register.value and Plugins.AccessControl in self.__plugins:
            self.__plugins[Plugins.AccessControl].shutdown()
            del self.__plugins[Plugins.AccessControl]

    def __blinds_enabled(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and Plugins.Blinds not in self.__plugins:
            config = self.__prepare_config("Blinds", register.base_name)
            self.__plugins[Plugins.Blinds] = Blinds(config)
            self.__plugins[Plugins.Blinds].init()

        elif not register.value and Plugins.Blinds in self.__plugins:
            self.__plugins[Plugins.Blinds].shutdown()
            del self.__plugins[Plugins.Blinds]

    def __monitoring_enabled(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and Plugins.Monitoring not in self.__plugins:
            config = self.__prepare_config("Monitoring", register.base_name)
            self.__plugins[Plugins.Monitoring] = Monitoring(config)
            self.__plugins[Plugins.Monitoring].init()

        elif not register.value and Plugins.Monitoring in self.__plugins:
            self.__plugins[Plugins.Monitoring].shutdown()
            del self.__plugins[Plugins.Monitoring]

    def __env_enabled(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and Plugins.Environment not in self.__plugins:
            config = self.__prepare_config("Environment", register.base_name)
            self.__plugins[Plugins.Environment] = Environment(config)
            self.__plugins[Plugins.Environment].init()

        elif not register.value and Plugins.Environment in self.__plugins:
            self.__plugins[Plugins.Environment].shutdown()
            del self.__plugins[Plugins.Environment]

    def __hvac_enabled(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and Plugins.HVAC not in self.__plugins:
            config = self.__prepare_config("HVAC", register.base_name)
            self.__plugins[Plugins.HVAC] = HVAC(config)
            self.__plugins[Plugins.HVAC].init()

        elif not register.value and Plugins.HVAC in self.__plugins:
            self.__plugins[Plugins.HVAC].shutdown()
            del self.__plugins[Plugins.HVAC]

    def __light_enabled(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and Plugins.MainLight not in self.__plugins:
            config = self.__prepare_config("Lamps", register.base_name)
            self.__plugins[Plugins.MainLight] = Lighting(config)
            self.__plugins[Plugins.MainLight].init()

        elif not register.value and Plugins.MainLight in self.__plugins:
            self.__plugins[Plugins.MainLight].shutdown()
            del self.__plugins[Plugins.MainLight]

    def __sys_enabled(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and Plugins.Sys not in self.__plugins:
            config = self.__prepare_config("System", register.base_name)
            self.__plugins[Plugins.Sys] = Sys(config)
            self.__plugins[Plugins.Sys].init()

        elif not register.value and Plugins.Sys in self.__plugins:
            self.__plugins[Plugins.Sys].shutdown()
            del self.__plugins[Plugins.Sys]

    def __add_handlers(self):

        register = self.__registers.by_name("ac.enabled")
        if register is not None:
            register.update_handler = self.__access_control_enabled

        register = self.__registers.by_name("blinds.enabled")
        if register is not None:
            register.update_handler = self.__blinds_enabled

        register = self.__registers.by_name("monitoring.enabled")
        if register is not None:
            register.update_handler = self.__monitoring_enabled

        register = self.__registers.by_name("env.enabled")
        if register is not None:
            register.update_handler = self.__env_enabled

        register = self.__registers.by_name("hvac.enabled")
        if register is not None:
            register.update_handler = self.__hvac_enabled

        register = self.__registers.by_name("light.enabled")
        if register is not None:
            register.update_handler = self.__light_enabled

        register = self.__registers.by_name("sys.last_minute_errs")
        if register is not None:
            GlobalErrorHandler.set_register(register)

        register = self.__registers.by_name("sys.enabled")
        if register is not None:
            register.update_handler = self.__sys_enabled

#endregion

#region Public Methods

    def update(self):
        """Update plugins."""

        for key in self.__plugins:

            try:
                self.__plugins[key].update()

            except:
                self.__logger.error(traceback.format_exc())

    def shutdown(self):
        """Shutdown plugins."""

        for key in self.__plugins:

            try:
                self.__plugins[key].shutdown()

            except:
                pass

#endregion
