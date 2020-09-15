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

import argparse
import os
import csv

from services.global_error_handler.error_codes import ErrorCodes

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

def __to_name(name):

    out_name = ""

    out_name = name.replace("ErrorCodes.", "")

    return out_name

def __add_error(writer, name, code, description):

    writer.writerow({"name": name,\
                    "code": code,\
                    "description": description,\
                    })

def __to_CSV(file_path):
    
    with open(file_path, "w", newline="") as csv_file:

        fieldnames = ["name", "code", "description"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        __add_error(writer, ErrorCodes.Error.name, ErrorCodes.Error.value, "General error")
        __add_error(writer, ErrorCodes.NoConnectionWithERP.name, ErrorCodes.NoConnectionWithERP.value, "No connection with ERP")
        __add_error(writer, ErrorCodes.NoConnectionWithPLC.name, ErrorCodes.NoConnectionWithPLC.value, "No connection with PLC")
        __add_error(writer, ErrorCodes.BadRegisterValue.name, ErrorCodes.BadRegisterValue.value, "Bad register value")
        __add_error(writer, ErrorCodes.BadRegisterDataType.name, ErrorCodes.BadRegisterDataType.value, "Bad register data type")
        __add_error(writer, ErrorCodes.UnexpectedRegister.name, ErrorCodes.UnexpectedRegister.value, "Unexpected register")
        __add_error(writer, ErrorCodes.CartReaderStop.name, ErrorCodes.CartReaderStop.value, "Cart reader has stopped")
        __add_error(writer, ErrorCodes.CartReaderNone.name, ErrorCodes.CartReaderNone.value, "Cart reader has None")

        csv_file.close()

def main():

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    parser.add_argument("--typ", type=str, default="csv", help="Export type.")

    # Take arguments.
    args = parser.parse_args()

    if args.typ == "csv":
        __to_CSV("error.csv")

if __name__ == "__main__":
    main()
