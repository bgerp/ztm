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

# from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.serial import ModbusSerialClient as ModbusClient

from devices.vendors.mainland.hhc_r4i4d.hhc_r4i4d import HHCR4I4D as Island

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

def main():
    """Main function.
    """

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    parser.add_argument("--port", type=str, default="COM10", help="Serial port.")
    parser.add_argument("--unit", type=int, default=1, help="Unit ID.")

    # Take arguments.
    args = parser.parse_args()

    # Get args.
    unit = args.unit
    port = args.port

    # Island interface.
    island = Island()

    # Create client.
    with ModbusClient(method="rtu", port=port, baudrate=9600, timeout=0.2,
        xonxoff=False, rtscts=False, dsrdtr=False) as client:

        #---------------------------------------------------------------------------#
        # Generate request.
        #---------------------------------------------------------------------------#
        requests = island.generate_requests(unit, SetRelays=[False]*4)

        #---------------------------------------------------------------------------#
        # Read Discrete Inputs.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["GetDigitalInputs"])

        # Check the response.
        assert not response.isError(), "Device did not respond properly to the request."

        #Check the content.
        is_ok = response.bits == [False]*4 + [False]*4
        assert is_ok, "Device did not respond with proper bit count."

        print(response)
        print(response.bits)
        print()

        #---------------------------------------------------------------------------#
        # Generate request.
        #---------------------------------------------------------------------------#
        requests = island.generate_requests(unit, SetRelays=[True]*4)

        #---------------------------------------------------------------------------#
        # Write Coils.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["SetRelays"])

        # Check the response.
        assert not response.isError(), "Device did not respond properly to the request."
        print(response)

        response = client.execute(requests["GetRelays"])

        # Check the response.
        assert not response.isError(), "Device did not respond properly to the request."

        #Check the content.
        is_ok = response.bits == [True]*4 + [False]*4
        assert is_ok

        print(response)
        print(response.bits)
        print()

        #---------------------------------------------------------------------------#
        # Generate request.
        #---------------------------------------------------------------------------#
        requests = island.generate_requests(unit, SetRelays=[False]*4)

        #---------------------------------------------------------------------------#
        # Write Coils.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["SetRelays"])

        # Check the response.
        assert not response.isError(), "Device did not respond properly to the request."
        print(response)

        response = client.execute(requests["GetRelays"])

        # Check the response.
        assert not response.isError(), "Device did not respond properly to the request."

        #Check the content.
        is_ok = response.bits == [False]*4 + [False]*4
        assert is_ok

        print(response)
        print()

if __name__ == "__main__":
    main()
