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

from devices.vendors.donkger.xy_md02.xy_md02 import XYMD02 as Thermometer

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

    # Modbus thermometer.
    term = Thermometer(unit=unit)

    # Create client.
    with ModbusClient(method="rtu", port=port, baudrate=9600, timeout=1,
        xonxoff=False, rtscts=False, dsrdtr=False) as client:

        #---------------------------------------------------------------------------#
        # Generate request.
        #---------------------------------------------------------------------------#
        requests = term.generate_requests(DeviceAddress=1, BaudRate=0)

        #---------------------------------------------------------------------------#
        # Read device ID.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["GetDeviceAddress"])

        # Check the response.
        assert not response.isError()

        #Check the content.
        is_ok = response.registers == [1]
        assert is_ok

        print(response)
        print("Device ID: {}".format(response.registers[0]))
        print()

        #---------------------------------------------------------------------------#
        # Read device baudrate.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["GetBaudRate"])

        # Check the response.
        assert not response.isError()

        # Check the content. It should be 1.
        is_ok = response.registers == [9600]
        assert is_ok

        print(response)
        print("Device baudrate: {}".format(response.registers[0]))
        print()

        #---------------------------------------------------------------------------#
        # Read device temperature correction.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["GetTemperatureCorrection"])

        # Check the response.
        assert not response.isError()

        # Check the content. It should be 1.
        is_ok = response.registers == [0]
        assert is_ok

        print(response)
        print("Temperature correction: {}".format(response.registers[0]))
        print()

        #---------------------------------------------------------------------------#
        # Read device humidity correction.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["GetHumidityCorrection"])

        # Check the response.
        assert not response.isError()

        # Check the content. It should be 1.
        is_ok = response.registers == [0]
        assert is_ok

        print(response)
        print("Humidity correction: {}".format(response.registers[0]))
        print()

        #---------------------------------------------------------------------------#
        # Read device temperature correction.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["Temperature"])

        # Check the response.
        assert not response.isError()

        # Check the content. It should be 1.
        is_ok = response.registers != None
        assert is_ok

        print(response)
        print("Temperature: {0}".format(response.registers[0]/10))
        print()


        #---------------------------------------------------------------------------#
        # Read device temperature correction.
        #---------------------------------------------------------------------------#
        response = client.execute(requests["Humidity"])

        # Check the response.
        assert not response.isError()

        # Check the content. It should be 1.
        is_ok = response.registers != None
        assert is_ok

        print(response)
        print("Humidity: {0}".format(response.registers[0]/10))
        print()

if __name__ == "__main__":
    main()
