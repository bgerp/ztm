#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""

Zontromat - Zonal Electronic Automation

Copyright (C) [2021] [POLYGONTeam Ltd.]

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

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2021, POLYGON Team Ltd."
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

import sys
import signal
import os
import time

import serial
from enum import Enum
from utils.logger import get_logger, crate_log_file

from devices.vendors.dallas.ds2480b.ds2480b import DS2480B
from devices.vendors.dallas.ds18b20.commands import Commands as DS18B20

#region Variables

__time_to_stop = False
"""Time to stop flag."""

#endregion

def interupt_handler(signum, frame):
    """Interupt handler."""

    global __time_to_stop

    __time_to_stop = True

def main():
    """Main"""

    global __time_to_stop


    # Add signal handler.
    signal.signal(signal.SIGINT, interupt_handler)
    signal.signal(signal.SIGTERM, interupt_handler)

    # Create log.
    crate_log_file()

    owbm = DS2480B(port_name="COM13", baudrate=9600)

    owbm.connect()

    owbm.sync_the_uart()
    owbm.reset_the_bus()

    owbm.configure_the_bus()
    owbm.reset_the_bus()

    commands = [DS18B20.SEARCH_ROM.value]
    devices = owbm.search_the_bus(commands=commands)
    print(devices)
    owbm.reset_the_bus()

    commands = [DS18B20.SKIP_ROM.value, DS18B20.READ_POWER_SUPPLY.value]
    owbm.read_device(commands=commands)
    owbm.reset_the_bus()

    commands = [DS18B20.SKIP_ROM.value, DS18B20.CONVERT_T.value]
    owbm.read_device_param(commands=commands)
    owbm.reset_the_bus()

    commands = [DS18B20.MATCH_ROM.value]
    commands.extend([DS18B20.FamilyCode.value, 0xFF, 0xFC, 0xD0, 0x00, 0x17, 0x03, 0xAE])
    commands.append(DS18B20.READ_SCRATCHPAD.value)
    for item in range(9):
        commands.append(0xFF)
    owbm.read_scratchpad(commands=commands)

    owbm.disconnect()

if __name__ == "__main__":
    main()
