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

import time
import os
import argparse
import logging
import traceback
from struct import pack, unpack

from pymodbus.client.sync import ModbusSerialClient as ModbusClient

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

__registers_ids = [ \
    [0, 1], [6, 7], [12, 13], [18, 19], [24, 25],\
    [30, 31], [70, 71], [72, 73], [74, 75], [76, 77],\
    [78, 79], [84, 85], [86, 87], [88, 89], [90, 91],\
    [92, 93], [94, 95], [258, 259], [264, 265], [342, 343], [344, 345]\
]
"""Target device registers."""

__log_format = ('%(asctime)-15s %(threadName)-15s '
                '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
"""Logging format."""

__logger = None
"""Logger"""

#endregion

def to_float(registers):
    """Convers two registers to float value."""

    bin_data = pack('<HH', registers[1], registers[0])
    value = unpack('f', bin_data)[0]
    return value

def main():
    """Main function."""

    # Global variables.
    global __logger, __registers_ids, __log_format

    # Create logging.
    logging.basicConfig(format=__log_format)
    __logger = logging.getLogger()
    __logger.setLevel(logging.INFO)

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    if os.name == "nt":
        parser.add_argument("--port", type=str, default="COM3", help="Serial port")

    if os.name == "posix":
        parser.add_argument("--port", type=str, default="/dev/extcomm/1/0", help="Serial port")

    parser.add_argument("--baud", type=int, default=2400, help="Baudrate")
    parser.add_argument("--mbid", type=int, default=1, help="Modbus ID")

    # Take arguments.
    args = parser.parse_args()

    # Create client.
    client = ModbusClient(method="rtu", port=args.port, timeout=1, baudrate=args.baud)

    # Connect
    client.connect()

    # Read modbus parameters.
    __logger.info("Begin reading input registers.")

    for register_ids in __registers_ids:

        try:
            rr = client.read_input_registers(register_ids[0], len(register_ids), unit=args.mbid)
            value = to_float(rr.registers)
            __logger.info("Reg IDs: {}; Reg Values: {}; Actual Value: {:06.3f}".format(register_ids, rr.registers, value))

        except Exception:
            trace_back = traceback.format_exc()
            __logger.error(trace_back)

        time.sleep(1)

    __logger.info("End reading input registers.")

    # Close the client
    client.close()

if __name__ == "__main__":
    main()
