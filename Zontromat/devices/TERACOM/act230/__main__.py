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

import argparse
import signal
import time

from devices.TERACOM.act230.act230 import ACT230
from devices.TERACOM.act230.act230 import ReaderState

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

__reader = None
__time_to_stop = False

def reader_read(card_id, reader_id):

    print("Card ID: {}; Reader ID: {}".format(card_id, reader_id))

def stop():
    global __reader, __time_to_stop

    __time_to_stop = True

    print("Stopping")

    if __reader is not None:
        __reader.stop()

        while __reader.reader_state == ReaderState.RUN:
            pass

        del __reader

        print("Stopped")


def start(port_name, sn):
    global __reader, __time_to_stop

    __time_to_stop = False

    print("Starting")

    # Get card reader parameters.
    reader_config = {
        "port_name": port_name,
        "baudrate": 9600,
        "serial_number": sn,
        "controller": None}

    # Create card reader.
    __reader = ACT230(reader_config)
    if __reader.reader_state is ReaderState.NONE:
        __reader.cb_read_card(reader_read)
        __reader.start()

        print("Started")

def update():
    global __reader, __time_to_stop

    # Check the exit card reader.
    if __reader is not None:

        # Update card reader.
        __reader.update()

        if __reader.reader_state == ReaderState.STOP:

            message = "Card reader {}; State {}; Port {}."\
                .format(__reader.reader_id, \
                __reader.reader_state, \
                __reader.port_name)

            print(message)

            __reader.start()

        if __reader.reader_state == ReaderState.NONE:

            message = "Card reader {}; State {}."\
                .format(__reader.reader_id, __reader.reader_state)

            print(message)

            __reader.start()

def interupt_handler(signum, frame):
    """Interupt handler."""

    global __time_to_stop

    __time_to_stop = True

    if signum == 2:
        print("Stopped by interupt.")

    elif signum == 15:
        print("Stopped by termination.")

    else:
        print("Signal handler called. Signal: {}; Frame: {}".format(signum, frame))

    stop()

def main():
    global __time_to_stop


    # Add signal handler.
    signal.signal(signal.SIGINT, interupt_handler)
    signal.signal(signal.SIGTERM, interupt_handler)

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    parser.add_argument("--port", type=str, default="COM11", help="Serial port")
    parser.add_argument("--sn", type=str, default="2911", help="Host of the robot.")

    # Take arguments.
    args = parser.parse_args()

    start(args.port, args.sn)

    while not __time_to_stop:
        update()
        time.sleep(1)

if __name__ == "__main__":
    main()
