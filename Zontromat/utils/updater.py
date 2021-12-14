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

from utils.logger import get_logger, crate_log_file

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

def update(target_version: dict, current_version: dict):
    """Update the application.

    Args:
        target_version (dict): Dictionary that holds target version.
        current_version (dict): Dictionary that holds the current version.
    """

    # Updater job file.
    update_file_name = "ztm_auto_update.sh"

    logger = get_logger(__file__)

    # Check the consistency of the software version.
    if current_version != target_version:

        if target_version["repo"] != current_version["repo"]:
            logger.info("Changed repo: from {} to {}"
                        .format(current_version["repo"], target_version["repo"]))

        if target_version["branch"] != current_version["branch"]:
            logger.info("Changed branch: from {} to {}"
                        .format(current_version["branch"], target_version["branch"]))

        if target_version["commit"] != current_version["commit"]:
            logger.info("Changed commit: from {} to {}"
                        .format(current_version["commit"], target_version["commit"]))

        # Current file path. & Go to file.
        cwf = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(cwf, "..", "..", "sh", update_file_name)

        if not os.path.exists(file_name):
            GlobalErrorHandler.log_missing_resource(logger, "Automatic update procedure: {}".format(file_name))
            return

        # Run the job in background.
        response = os.system("{} {} {} {} &".format(
            file_name,
            target_version["repo"],
            target_version["branch"],
            target_version["commit"]))
        logger.info(response)
