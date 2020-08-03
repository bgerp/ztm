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
import configparser

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

class EvokSettings:
    """EVOK Settings parser."""

#region Attributes

    __file_path = ""
    """File path."""

    __config = None
    """Configuration"""

#endregion

#region Constructor

    def __init__(self, file_path):
        """Constructor"""

        self.__file_path = file_path
        self.__config = configparser.ConfigParser()
        self.load()
        
#endregion

#region Private Methods

    def __get_next_extension(self):

        main_key = "EXTENSION"
        sections = self.__config.sections()

        index = 0

        # Go through all.
        for section_key in sections:

            # Find only external.
            if main_key in section_key:
                segments = section_key.split("_")
                segments_index = segments[1]
                segments_index = int(segments_index)

                # Filter the maximum.
                if segments_index > index:
                    index = segments_index

        # Increment by one.
        index += 1

        # Return the name.
        return main_key + "_" + str(index)

#endregion

#region Public Methods

    def load(self):
        """Load EVOK config."""

        if os.path.exists(self.__file_path):
            self.__config.read(self.__file_path)

    def save(self):
        """Save EVOK config."""

        with open(self.__file_path, 'w') as configfile:
            self.__config.write(configfile)

    def add_device(self, config):
        """Add device by nex extension name."""

        if config is None:
            raise ValueError("Config should not be None.")

        extension_name = self.__get_next_extension()
        existing_sections = self.__config.sections()

        if extension_name in existing_sections:
            raise ValueError("Extention allready exists.")

        if not isinstance(config, dict):
            raise ValueError("Configuration should be list.")

        self.__config.add_section(extension_name)

        # Add the configuration.
        for row in config:
            self.__config[extension_name][row] = str(config[row])

    def add_named_device(self, config, extension_name):
        """Add device by name."""

        if config is None:
            raise ValueError("Config should not be None.")

        existing_sections = self.__config.sections()

        if extension_name in existing_sections:
            raise ValueError("Extention allready exists.")

        if not isinstance(config, list):
            raise ValueError("Configuration should be list.")

        self.__config.add_section(extension_name)

        # Add the configuration.
        for row in config:
            self.__config[extension_name][row] = config[row]

    def remove_device(self, extension_name):
        """Remove extension."""

        existing_sections = self.__config.sections()

        if extension_name in existing_sections:
            raise ValueError("Extention allready exists.")

        self.__config.remove_section(extension_name)

#endregion
