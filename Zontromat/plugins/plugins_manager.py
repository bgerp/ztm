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
import importlib

from utils.logger import get_logger

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

#endregion

class PluginsManager:
    """Plugin manager."""

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

        Args:
            registers (Registers): Registers class instance.
            controller (BaseController): Hardware controller.
        """

        self.__logger = get_logger(__name__)
        self.__plugins = {}
        self.__registers = registers
        self.__controller = controller
        self.__add_enable_handlers()

#endregion

#region Private Methods

    def __find_plugins(self):

        list_of_dirs = []

        dir_path = os.path.dirname(os.path.realpath(__file__))

        dirs = os.listdir(dir_path)
        for item in dirs:

            if item.startswith("__"):
                continue

            if item == "template_plugin":
                continue

            plugin_path = os.path.join(dir_path, item)

            if os.path.isdir(plugin_path):
                list_of_dirs.append(item)

        return list_of_dirs

    def __prepare_config(self, name, key):
        """Prepare configuration of the plugin.

        Args:
            name (str): Name of the plugin.
            key (str): Key of the plugin.

        Returns:
            dict: Configuration of the plugin.
        """

        config = {
            "name": name,
            "key": key,
            "registers": self.__registers,
            "controller": self.__controller,
        }

        return config

    def __load_plugin(self, module_name):
        """Load the plugin.

        Args:
            module_name (str): Name of the plugin.

        Raises:
            ImportError: Raise when module can not me imported.
            ModuleNotFoundError: Raise when module can not be found.
            AttributeError: Not existing attribute.
            ValueError: Attribute __class_name__ is not set properly.

        Returns:
            [mixed]: Instance of the class module.
        """

        module_path = "plugins.{}.{}".format(module_name, module_name)

        module = importlib.import_module(module_path)
        if module is None:
            raise ImportError("{}".format(module_path))

        if not hasattr(module, "__class_name__"):
            raise AttributeError("Module: {}, has no attribute __class_name__.".format(module_path))

        if module.__class_name__ == "":
            raise ValueError("Module: {}.__class_name__ is empty.".format(module_path))

        class_module = getattr(module, module.__class_name__)
        if class_module is None:
            raise ModuleNotFoundError("{}.{}".format(module_path, module.__class_name__))

        config = self.__prepare_config(module.__class_name__, module_name)

        class_isinstance = class_module(config)

        return class_isinstance

    def __enable_plugin_cb(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        name = register.base_name
        if register.value and name not in self.__plugins:
            self.__plugins[name] = self.__load_plugin(name)
            self.__plugins[name].init()

        elif not register.value and name in self.__plugins:
            self.__plugins[name].shutdown()
            del self.__plugins[name]

    def __add_enable_handlers(self):

        names = self.__find_plugins()
        for name in names:
            self.__logger.info("Found plugin: {}".format(name))

            register = self.__registers.by_name("{}.enabled".format(name))
            if register is not None:
                register.update_handlers = self.__enable_plugin_cb
                register.update()

#endregion

#region Public Methods

    def update(self):
        """Update plugins.
        """

        for key in self.__plugins:
            self.__plugins[key].update()

    def shutdown(self):
        """Shutdown plugins.
        """

        for key in self.__plugins:
            self.__plugins[key].shutdown()

#endregion
