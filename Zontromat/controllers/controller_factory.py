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
from os import path

import importlib

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

class ControllerFactory():
    """Controller factory class."""

    @staticmethod
    def __load_controller(vendor, model, config):
        """Load controller.

        Args:
            vendor (str): Vendor name.
            model (str): Model name.
            config (dict): Controller configuration.

        Raises:
            ImportError: Raise when module can not me imported.
            ModuleNotFoundError: Raise when module can not be found.
            AttributeError: Not existing attribute.
            ValueError: Attribute __class_name__ is not set properly.

        Returns:
            mixed: Instance of the class module.
        """

        module_path = "controllers.{}.{}".format(vendor, model)

        module_path = module_path.lower()

        current_directory = os.path.dirname(os.path.realpath(__file__))
        module_file_path = os.path.join(current_directory, vendor, model) + ".py"
        exists = path.exists(module_file_path)
        if not exists:
            raise FileNotFoundError("Controller file \"{}\" does not exit.".format(module_path))

        module = importlib.import_module(module_path)
        if module is None:
            raise ImportError("{}".format(module_path))        

        if not hasattr(module, "__class_name__"):
            raise AttributeError("Controller file: {}, has no attribute __class_name__.".format(module_path))

        if module.__class_name__ == "":
            raise ValueError("Controller file: {}.__class_name__ is empty.".format(module_path))

        class_module = getattr(module, module.__class_name__)
        if class_module is None:
            raise ModuleNotFoundError("Controller: \"{}.{}\" not found.".format(module_path, module.__class_name__))

        class_isinstance = class_module(config)

        return class_isinstance

#region Public Methods

    @staticmethod
    def create(config):
        """Create controller."""

        # TODO: If the serial is not in the controller load it from file, if not create it and save it.
        controller = None

        if "vendor" not in config:
            raise ValueError("Missing vendor descriptor.")

        if "model" not in config:
            raise ValueError("Missing model descriptor.")

        # Load controller module.
        controller = ControllerFactory.__load_controller(config["vendor"], config["model"], config)

        return controller

#endregion
