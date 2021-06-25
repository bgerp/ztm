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
import signal
import os
import time

from utils.logger import get_logger, crate_log_file
from utils.settings import ApplicationSettings

from zone import Zone

if os.name == "posix":
    import setproctitle

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

#region Variables

__logger = None
"""Logger"""

__zone = None
"""Zone"""

__time_to_stop = False
"""Time to stop flag."""

#endregion

def interupt_handler(signum, frame):
    """Interupt handler.

    Args:
        signum (int): Interupt signal type (number).
        frame (frame): Frame when this is happend.
    """

    global __zone, __logger, __time_to_stop

    __time_to_stop = True

    if signum == 2:
        __logger.warning("Stopped by interupt.")

    elif signum == 15:
        __logger.warning("Stopped by termination.")

    else:
        __logger.warning("Signal handler called. Signal: {}; Frame: {}".format(signum, frame))

    if __zone is not None:
        __zone.shutdown()

def main():
    """Main"""

    global __zone, __logger, __time_to_stop

    # Create process name.
    if os.name == "posix":
        setproctitle.setproctitle("Zontromat")

    # Add signal handler.
    signal.signal(signal.SIGINT, interupt_handler)
    signal.signal(signal.SIGTERM, interupt_handler)

    settings = ApplicationSettings.get_instance()

    # Create log.
    crate_log_file()
    __logger = get_logger(__name__)

    # Wait for settings.
    while not settings.exists:
        if __time_to_stop:
            sys.exit(0)

        __logger.error("Missing settings file.")
        time.sleep(5)

    # Read settings content.
    settings.read()

    __logger.info("Starting")

    # Create zone.
    __zone = Zone()

    # Init the zone.
    __zone.init()

    # Run the zone.
    __zone.run()

if __name__ == "__main__":
    main()
