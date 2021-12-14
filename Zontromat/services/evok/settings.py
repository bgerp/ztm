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
import re
import subprocess
import json

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

class EvokSettings:
    """EVOK Settings parser."""

#region Attributes

    __file_path = ""
    """File path."""

    __config = None
    """Configuration"""

#endregion

#region Properties

    @property
    def webhook_enabled(self):
        """WEB hook enable flag."""

        return self.__config["MAIN"]["webhook_enabled"]

    @property
    def webhook_address(self):
        """WEB hook address."""

        return self.__config["MAIN"]["webhook_address"]

    @property
    def webhook_device_mask(self):
        """WEB hook mask."""

        return self.__config["MAIN"]["webhook_device_mask"]

    @property
    def webhook_complex_events(self):
        """WEB hook complex event flag."""

        return self.__config["MAIN"]["webhook_complex_events"]

    @webhook_enabled.setter
    def webhook_enabled(self, value):
        """WEB hook enable flag."""

        if value is None:
            raise ValueError("Value should not be None.")

        if not isinstance(value, bool):
            raise TypeError("Value should be bool.")

        self.__config["MAIN"]["webhook_enabled"] = str(value)

    @webhook_address.setter
    def webhook_address(self, value):
        """WEB hook address."""

        if value is None:
            raise ValueError("Value should not be None.")

        if not isinstance(value, str):
            raise TypeError("Value should be string.")

        compiled = re.compile(r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?")
        matched = compiled.match(value)
        if matched:
            self.__config["MAIN"]["webhook_address"] = str(value)
        else:
            raise ValueError("String should be URL.")

    @webhook_device_mask.setter
    def webhook_device_mask(self, value):
        """WEB hook mask."""

        if value is None:
            raise ValueError("Value should not be None.")

        if not isinstance(value, list):
            raise TypeError("Value should be bool.")

        self.__config["MAIN"]["webhook_device_mask"] = json.dumps(value)

    @webhook_complex_events.setter
    def webhook_complex_events(self, value):
        """WEB hook enable flag."""

        if value is None:
            raise ValueError("Value should not be None.")

        if not isinstance(value, bool):
            raise TypeError("Value should be bool.")

        self.__config["MAIN"]["webhook_complex_events"] = str(value)

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

        with open(self.__file_path, "w") as configfile:
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
            raise ValueError("Configuration should be dict.")

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
            raise ValueError("Extention allready exists: {}".format(extension_name))

        if not isinstance(config, dict):
            raise ValueError("Configuration should be dict.")

        self.__config.add_section(extension_name)

        # Add the configuration.
        for row in config:
            self.__config[extension_name][row] = str(config[row])

    def remove_device(self, extension_name):
        """Remove extension."""

        existing_sections = self.__config.sections()

        if extension_name not in existing_sections:
            raise ValueError("Extention does not exists.")

        self.__config.remove_section(extension_name)

    def device_exists(self, extension_name):
        """Extension has exists."""

        extensions = self.__config.sections()
        return extension_name in extensions

#endregion

#region Public Static Methods

    @staticmethod
    def restart():
        """Restart EVOK service."""

        try:
            subprocess.call("systemctl restart evok", shell=True)

        except Exception as exception:
            print(exception)

#endregion
