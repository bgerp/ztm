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
import sys
import argparse

from prettytable import PrettyTable

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from controllers.unipi.neuron import Neuron

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

__neuron = None
"""Neuron"""

__table_data = None
"""Table data."""


#endregion

def get_temp(device):
    """Returns the actual temperature of the device."""

    value = 0

    dev_type = device["typ"]

    if dev_type == "DS2438":
        value = device["temp"]

    elif dev_type == "DS18B20":
        value = device["value"]

    return value

def get_temp_by_circuit(devices, circuit):

    device = None

    for dev in devices:
        if dev["circuit"] == circuit:
            device = dev
            break

    if device is None:
        temp = None
    else:
        temp = get_temp(device)

    return temp

def main():
    """Main"""

    global __neuron

    __table_data = PrettyTable()

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="http://176.33.1.249", help="IP Address")
    parser.add_argument("--port", type=int, default=8080, help="Port")

    args = parser.parse_args()

    # Create cabinet
    __neuron = Neuron(args.ip, args.port)
    __neuron.update()

    # Begin identification procedure.

    # Get all 1 wire devices (thermometers).
    onew_devices = __neuron.get_1w_devices()

    # Create columns of the table.
    names = []

    # From their circuits create column names.
    for device in onew_devices:
        names.append(device["circuit"])

    # TODO: Add more columns in case of more data (outputs).
    names.append("GPIO 1")
    names.append("GPIO 2")
    names.append("GPIO 3")
    names.append("GPIO 4")

    __table_data.field_names = names

    # Add columns of the row.
    row = []
    for name in names:
        temp = get_temp_by_circuit(onew_devices, name)
        if temp is not None:
            temp = float("{:06.2f}".format(float(temp)))
            row.append(temp)

    # TODO: Append more columns for te state of every single test.
    row.append(1)
    row.append(0)
    row.append(0)
    row.append(0)

    # Add row of the table.
    __table_data.add_row(row)

    # Show the table.
    print(__table_data)

def kb_interupt():
    """Keyboard interupt handler."""

    global time_to_stop

    time_to_stop = True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        kb_interupt()
