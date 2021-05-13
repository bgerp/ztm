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
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from devices.vendors.Super.s8_3cn.s8_3cn import S8_3CN as BlackIsland

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
    parser.add_argument("--port", type=str, default="COM12", help="Serial port.")
    parser.add_argument("--baudrate", type=int, default=9600, help="Serial port.")
    parser.add_argument("--unit", type=int, default=1, help="Unit ID.")

    # Take arguments.
    args = parser.parse_args()

    # Get args.
    port = args.port
    baudrate=args.baudrate
    unit = args.unit

    black_island = BlackIsland()

    # Create client.
    with ModbusClient(method="rtu", port=port, baudrate=baudrate, timeout=1,
        xonxoff=False, rtscts=False, dsrdtr=False) as client:

        #---------------------------------------------------------------------------#
        # Read Coils.
        #---------------------------------------------------------------------------#
        request = black_island.generate_request(unit, "GetRelays")
        response = client.execute(request)
        
        # Check the response.
        assert(not response.isError())

        # Check the content.
        is_ok = response.bits == [False]*12 + [False]*4
        assert(is_ok)

        print(response)
        print()

        #---------------------------------------------------------------------------#
        # Read Discrete Inputs.
        #---------------------------------------------------------------------------#
        request = black_island.generate_request(unit, "GetDigitalInputs")
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())

        #Check the content.
        is_ok = response.bits == [False]*8
        assert(is_ok)

        print(response)
        print()

        #---------------------------------------------------------------------------#
        # Read Holding Registers.
        #---------------------------------------------------------------------------#
        request = black_island.generate_request(unit, "GetAnalogOutputs")
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())

        #Check the content.
        is_ok = response.registers == [0]*4
        assert(is_ok)

        print(response)
        print()

        #---------------------------------------------------------------------------#
        # Read Input Registers.
        #---------------------------------------------------------------------------#
        request = black_island.generate_request(unit, "GetAnalogInputs")
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())

        #Check the content.
        is_ok = response.registers == [0]*8
        assert(is_ok)

        print(response)
        print()

        #---------------------------------------------------------------------------#
        # Write Coils.
        #---------------------------------------------------------------------------#
        request = black_island.generate_request(unit, "SetRelays", SetRelays=[True]*12 + [False]*4)
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())
        print(response)

        request = black_island.generate_request(unit, "GetRelays")
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())

        #Check the content.
        is_ok = response.bits == [True]*12 + [False]*4
        assert(is_ok)

        print(response)
        print()

        #---------------------------------------------------------------------------#
        # Write Holding Registers.
        #---------------------------------------------------------------------------#
        request = black_island.generate_request(unit, "SetAnalogOutputs", SetAnalogOutputs=[10000]*8)
        hrw_response = client.execute(request)

        # Check the response.
        assert(not hrw_response.isError())
        print(hrw_response)

        request = black_island.generate_request(unit, "GetAnalogOutputs")
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())

        #Check the content.
        is_ok = response.registers == [10000]*4
        assert(is_ok)

        print(response)
        print()

        #---------------------------------------------------------------------------#
        # Write Coils.
        #---------------------------------------------------------------------------#
        request = black_island.generate_request(unit, "SetRelays", SetRelays=[False]*12 + [False]*4)
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())
        print(response)

        request = black_island.generate_request(unit, "GetRelays")
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())

        #Check the content.
        is_ok = response.bits == [False]*12 + [False]*4
        assert(is_ok)

        print(response)
        print()

        #---------------------------------------------------------------------------#
        # Write Holding Registers.
        #---------------------------------------------------------------------------#
        request = black_island.generate_request(unit, "SetAnalogOutputs", SetAnalogOutputs=[0]*8)
        hrw_response = client.execute(request)

        # Check the response.
        assert(not hrw_response.isError())
        print(hrw_response)

        request = black_island.generate_request(unit, "GetAnalogOutputs")
        response = client.execute(request)

        # Check the response.
        assert(not response.isError())

        #Check the content.
        is_ok = response.registers == [0]*4
        assert(is_ok)

        print(response)
        print()

if __name__ == "__main__":
    main()
