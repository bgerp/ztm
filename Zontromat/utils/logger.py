#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from time import gmtime, strftime
import logging

from utils.settings import ApplicationSettings

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

#region Variables

__modules_names = []
"""Modules names."""

#endregion

#region Public Functions

def crate_log_file(logs_dir_name="logs/"):
    """This method create a new instance of the LOG direcotry.

    Parameters
    ----------
    logs_dir_name : str
        Path to the log direcotory.
    """

    debug_level = ApplicationSettings.get_instance().debug_level

    # Crete log directory.
    if not os.path.exists(logs_dir_name):
        os.makedirs(logs_dir_name)

    # File name.
    log_file = ""
    log_file += logs_dir_name
    log_file += strftime("%Y%m%d", gmtime())
    log_file += ".log"

    # create message format.
    log_format = "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"

    logging.basicConfig( \
        filename=log_file, \
        level=debug_level, \
        format=log_format)

def get_logger(module_name):
    """Get logger instance.

    Parameters
    ----------
    module_name : str
        Logger module name.

    Returns
    -------
    logger
        Logger instance.
    """

    global __modules_names


    logger = logging.getLogger(module_name)

    if module_name in __modules_names:
        return logger
    else:
        __modules_names.append(module_name)

    # Get debug level.
    debug_level = ApplicationSettings.get_instance().debug_level

    # Create console handler.
    console_handler = logging.StreamHandler()

    # Set debug level.
    console_handler.setLevel(debug_level)

    # Add console handler to logger.
    logger.addHandler(console_handler)

    return logger

#endregion
