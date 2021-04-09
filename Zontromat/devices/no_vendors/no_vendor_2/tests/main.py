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

# from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from devices.no_vendors.no_vendor_2.requests.read_device_holding_registers import ReadDeviceHoldingRegisters
from devices.no_vendors.no_vendor_2.requests.read_device_input_registers import ReadDeviceInputRegisters

from devices.no_vendors.no_vendor_2.requests.write_device_registers import WriteDeviceRegisters

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

    unit = 1

    # Create client.
    with ModbusClient(method="rtu", port="COM12", baudrate=9600, timeout=1,
        xonxoff=False, rtscts=False, dsrdtr=False) as client:

        #---------------------------------------------------------------------------#
        # Read Holding Registers.
        #---------------------------------------------------------------------------#
        hrr_request = ReadDeviceHoldingRegisters(unit)
        hrr_response = client.execute(hrr_request)

        # Check the response.
        assert(not hrr_response.isError())

        #Check the content.
        is_ok = hrr_response.registers == [1, 9600, 0, 0]
        assert(is_ok)

        print(hrr_response)
        print()

        #---------------------------------------------------------------------------#
        # Read Input Registers.
        #---------------------------------------------------------------------------#
        irr_request = ReadDeviceInputRegisters(unit)
        irr_response = client.execute(irr_request)

        # Check the response.
        assert(not irr_response.isError())

        print(irr_response)
        print("Temp: {0}".format(irr_response.registers[0]/10))
        print("Hum: {0}".format(irr_response.registers[1]/10))
        print()

        #---------------------------------------------------------------------------#
        # Write Holding Registers.
        #---------------------------------------------------------------------------#
        # hrw_request = WriteDeviceRegisters(unit, [10000]*8)
        # hrw_response = client.execute(hrw_request)

        # # Check the response.
        # assert(not hrw_response.isError())
        # print(hrw_response)

        # hrr_request = ReadDeviceHoldingRegisters(unit)
        # hrr_response = client.execute(hrr_request)

        # # Check the response.
        # assert(not hrr_response.isError())

        # #Check the content.
        # is_ok = hrr_response.registers == [10000]*8
        # assert(is_ok)

        # print(hrr_response)
        # print()

if __name__ == "__main__":
    main()
