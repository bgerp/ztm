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

import sys
import traceback
import os

from enum import Enum

from utils.logger import get_logger, crate_log_file

from data.register import Scope
from data.registers import Registers
from data.registers import Register

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

def update(target_version: Register, current_version: Register):

    logger = get_logger(__file__)

    # Check the consistency of the software version.
    if current_version.value != target_version.value:

        if target_version.value["repo"] != current_version.value["repo"]:
            logger.info("Changed repo: from {} to {}".format(current_version.value["repo"], target_version.value["repo"]))

        if target_version.value["branch"] != current_version.value["branch"]:
            logger.info("Changed branch: from {} to {}".format(current_version.value["branch"], target_version.value["branch"]))

        if target_version.value["commit"] != current_version.value["commit"]:
            logger.info("Changed commit: from {} to {}".format(current_version.value["commit"], target_version.value["commit"]))

        # Current file path. & Go to file.
        cwf = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(cwf, "..", "..", "sh", "test.sh")
        response = os.system("{}".format(file_name)) # Thanks @Jim Dennis for suggesting the []
        print(response)