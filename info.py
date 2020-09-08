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

import struct
import getopt
import sys
import traceback

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

def read_eeprom():
    """Read the EEPROM."""

    device_cfg = {
        "version": "UniPi 1.0",
        "devices": {
            "ai": {
                "1": 5.564920867,
                "2": 5.564920867,
            }
        },
        "version1": None,
        "version2": None,
        "model": None,
        "serial": None
    }

    # Try to access the EEPROM at /sys/bus/i2c/devices/1-0050/eeprom
    try:
        with open("/sys/bus/i2c/devices/1-0050/eeprom", "rb") as eeprom:

            content = eeprom.read()

            control = struct.unpack(">H", content[224:226])[0]

            if control == 64085:

                if ord(content[226]) == 1 and ord(content[227]) == 1:
                    device_cfg["version"] = "UniPi 1.1"

                elif ord(content[226]) == 11 and ord(content[227]) == 1:
                    device_cfg["version"] = "UniPi Lite 1.1"

                else:
                    device_cfg["version"] = "UniPi 1.0"

                device_cfg["version1"] = device_cfg["version"]

                #AIs coeff
                if device_cfg["version"] in ("UniPi 1.1", "UniPi 1.0"):
                    device_cfg["devices"] = {
                        "ai": {
                            "1": struct.unpack("!f", content[240:244])[0],
                            "2": struct.unpack("!f", content[244:248])[0],
                            }
                        }

                else:
                    device_cfg["devices"] = {
                        "ai": {
                            "1": 0,
                            "2": 0,
                            }
                        }

                device_cfg["serial"] = struct.unpack("i", content[228:232])[0]
    except Exception:
        pass

    # Try to access the EEPROM at /sys/bus/i2c/devices/1-0057/eeprom
    try:
        with open("/sys/bus/i2c/devices/1-0057/eeprom", "rb") as eeprom:

            # Get content.
            content = eeprom.read()

            # Get control sum.
            control = struct.unpack(">H", content[96:98])[0]
            if control == 64085:

                # Version
                v1 = content[99]
                v2 = content[98]
                version2 = "{}.{}".format(v1, v2)
                device_cfg["version2"] = version2

                # Model
                model = struct.unpack("4s", content[106:110])
                model = model[0]
                model = model.decode("utf8")
                device_cfg["model"] = model

                # Serial Number
                device_cfg["serial"] = struct.unpack("i", content[100:104])[0]
    except Exception:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" %ex_value)
        print("Stack trace : %s" %stack_trace)

    # Try to access the EEPROM at /sys/bus/i2c/devices/0-0057/eeprom
    try:
        with open("/sys/bus/i2c/devices/0-0057/eeprom", "rb") as eeprom:

            # Get content.
            content = eeprom.read()

            # Get control sum.
            control = struct.unpack(">H", content[96:98])[0]
            if control == 64085:

                # Version
                v1 = content[99]
                v2 = content[98]
                version2 = "{}.{}".format(v1, v2)
                device_cfg["version2"] = version2

                # Model
                model = struct.unpack("4s", content[106:110])
                model = model[0]
                model = model.decode("utf8")
                device_cfg["model"] = model

                # Serial Number
                device_cfg["serial"] = struct.unpack("i", content[100:104])[0]
    except Exception:
        pass

    return device_cfg

def main(argv):
    """Main function."""

    opts, args = getopt.getopt(argv, "ms", ["model=", "serial="])

    just_model = False
    just_sn = False
    show_all = True

    for opt, arg in opts:

        if opt == "-m":
            just_model = True
            show_all = False

        if opt == "-s":
            just_sn = True
            show_all = False

    configuration = read_eeprom()

    if just_model:
        print(configuration["model"])

    if just_sn:
        print(configuration["serial"])

    if show_all:
        print(configuration)

if __name__ == "__main__":
    main(sys.argv[1:])
