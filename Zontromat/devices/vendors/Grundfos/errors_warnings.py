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

class ErrorsWarnings:
    """Code Alarm/warning description

    See: 10.4 Alarms and warnings @ Grundfosliterature-6012947.pdf
    """

    __erros_warnings = {
        1: "Leakage current",
        2: "Missing phase",
        3: "External fault signal",
        4: "Too many restarts",
        7: "Too many hardware shutdowns",
        14: "Electronic DC-link protection activated (ERP)",
        16: "Other",
        29: "Turbine operation, impellers forced backwards",
        30: "Change bearings (specific service information)",
        31: "Change varistor(s) (specific service information)",
        32: "Overvoltage",
        40: "Undervoltage",
        41: "Undervoltage transient",
        42: "Cut-in fault (dV/dt)",
        45: "Voltage asymmetry",
        48: "Overload",
        49: "Overcurrent (i_line, i_dc, i_mo)",
        50: "Motor protection function, general shutdown (MPF)",
        51: "Blocked motor or pump",
        54: "Motor protection function, 3 sec. limit",
        55: "Motor current protection activated (MCP)",
        56: "Underload",
        57: "Dry-running",
        60: "Low input power",
        64: "Overtemperature",
        65: "Motor temperature 1 (t_m or t_mo or t_mo1)",
        66: "Control electronics temperature high",
        67: "Temperature too high, internal frequency converter module (t_m)",
        68: "Water temperature high",
        70: "Thermal relay 2 in motor, for example thermistor",
        72: "Hardware fault, type 1",
        73: "Hardware shutdown (HSD)",
        76: "Internal communication fault",
        77: "Communication fault, twin-head pump",
        80: "Hardware fault, type 2",
        83: "Verification error, FE parameter area (EEPROM)",
        84: "Memory access error",
        85: "Verification error, BE parameter area (EEPROM)",
        88: "Sensor fault",
        89: "Signal fault, (feedback) sensor 1",
        91: "Signal fault, temperature 1 sensor",
        93: "Signal fault, sensor 2",
        96: "Setpoint signal outside range",
        105: "Electronic rectifier protection activated (ERP)",
        106: "Electronic inverter protection activated (EIP)",
        148: "Motor bearing temperature high (Pt100) in drive end (DE)",
        149: "Motor bearing temperature high (Pt100) in non-drive end (NDE)",
        155: "Inrush fault",
        156: "Communication fault, internal frequency converter module",
        157: "Real time clock error",
        161: "Sensor supply fault, 5 V",
        162: "Sensor supply fault, 24 V",
        163: "Measurement fault, motor protection",
        164: "Signal fault, Liqtec sensor",
        165: "Signal fault, analog input 1",
        166: "Signal fault, analog input 2",
        167: "Signal fault, analog input 3",
        175: "Signal fault, temperature 2 sensor",
        176: "Signal fault, temperature 3 sensor",
        190: "Limit exceeded, sensor 1",
        191: "Limit exceeded, sensor 2",
        215: "Soft pressure buildup timeout",
        240: "Lubricate bearings (specific service information)",
        241: "Motor phase failure",
        242: "Automatic motor model recognition failed",
    }

    @staticmethod
    def get_err_wrn_text(code):
        """Returns the error code message text.

        Args:
            code (int): Error or Warning code.

        Raises:
            Exception: Exception(Unidentified code)

        Returns:
            str: Error/WArning text message.
        """

        if not code in ErrorsWarnings.__erros_warnings:
            raise Exception("Unidentified error code: {}".format(code))

        return ErrorsWarnings.__erros_warnings[code]
