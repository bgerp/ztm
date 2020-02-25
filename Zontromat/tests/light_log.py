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
import time
from time import gmtime, strftime
import logging
import argparse
import requests

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

time_to_stop = False
"""Time to stop flag."""

logger_name = "LightData"
"""Data logger name."""

logger = None
"""Data logger object."""

prev_time = 0
"""Previous time to update queue."""

update_rate = 60
"""Queue update rate."""

send_lock = False
"""Send lock mechanism flag."""

#endregion

#region Logger

def crate_log_file(logs_dir_name='logs/'):
    """This method create a new instance of the LOG direcotry.

    Parameters
    ----------
    logs_dir_name : str
        Path to the log direcotory.
    """

    # Crete log directory.
    if not os.path.exists(logs_dir_name):
        os.makedirs(logs_dir_name)

    # File name.
    log_file = ''
    log_file += logs_dir_name
    log_file += strftime("%Y%m%d", gmtime())
    log_file += '.log'

    # create message format.
    log_format = "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"

    logging.basicConfig( \
        filename=log_file, \
        level=logging.INFO, \
        format=log_format)

def get_logger(logger_name):
    """Generate a device circuit for major and minor index.

    Parameters
    ----------
    logger_name : str
        Logger name.

    Returns
    -------
    logger
        Logger object.
    """

    logger = logging.getLogger(logger_name)

    # create console handler and set level to debug
    ch = logging.StreamHandler()

    # Set level
    ch.setLevel(logging.INFO)

    # add ch to logger
    logger.addHandler(ch)

    return logger

#endregion

#region Runtime

def time_to_measure():
    """Time to measure procedure."""

    global logger

    # API-endpoint.
    URL = "http://176.33.1.249:8080/json/temp/26607314020000F8"

    # Defining a params dict for the parameters to be sent to the API.
    PARAMS = {}

    # Sending get request and saving the response as response object.
    response = requests.get(url=URL, params=PARAMS)

    # Extracting data in json format.
    data = response.json()

    # Get VIS value.
    vsi = data["data"]["vis"]

    # Log VIS value.
    logger.info(vsi)

def update():
    """Update procedure."""

    global prev_time, send_lock

    # Main update rate at ~ 20 second.
    # На всеки 20 секунди се правят следните стъпки:
    diff = time.time() - prev_time

    if diff > update_rate:
        # Update current time.
        prev_time = time.time()

        if not send_lock:
            send_lock = True
            time_to_measure()
            send_lock = False

#endregion

def main():
    """Main"""

    global logger, logger_name, time_to_stop

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="s", help="Mode of execution")

    args = parser.parse_args()

    # Create LOG file.
    crate_log_file()

    # Get loger.
    logger = get_logger(logger_name)

    if args.mode == "c":
        logger.info("Starting")
        # Keep application alive.
        while not time_to_stop:
            update()
    elif args.mode == "s":
        time_to_measure()

def kb_interupt():
    """Keyboard interupt handler."""

    global logger, time_to_stop

    time_to_stop = True
    logger.info("Manual stop.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        kb_interupt()
