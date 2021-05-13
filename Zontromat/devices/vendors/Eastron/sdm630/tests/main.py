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

from devices.drivers.modbus.requests.read_device_holding_registers import ReadDeviceHoldingRegisters
from devices.drivers.modbus.requests.read_device_input_registers import ReadDeviceInputRegisters

from devices.drivers.modbus.requests.write_device_registers import WriteDeviceRegisters

from devices.vendors.Eastron.sdm630.sdm630 import SDM630 as PowerAnalyser

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

def convert_reg_offset(addresses, values):

    registers = {}
    index = 0
    for address in addresses:
        registers[address] = values[index]
        index += 1

    return registers

def main():
    """Main function.
    """

    print("Begin...")

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
    p_analyser = PowerAnalyser()

    # Create client.
    with ModbusClient(method="rtu", port=port, baudrate=19200, timeout=1,
        xonxoff=False, rtscts=False, dsrdtr=False) as client:

        params_names = p_analyser.get_parameters_names()

        #---------------------------------------------------------------------------#
        # Generate request.
        #---------------------------------------------------------------------------#
        requests = p_analyser.generate_requests(unit)

        #---------------------------------------------------------------------------#
        # Run thought device parameters.
        #---------------------------------------------------------------------------#
        for param_name in params_names:

            # Execute request for the given parameter.
            response = client.execute(requests[param_name])

            # Check the response.
            assert(not response.isError(), "Device did not respond properly to the request.")

            # Get parameter by name
            parameter = p_analyser.get_parameter_by_name(param_name)

            # Convert register offset indexes.
            registers = convert_reg_offset(parameter.addresses, response.registers)

            # Convert registers to actual value.
            param_value = p_analyser.get_parameter_value(param_name, registers)

            print(response)
            print("Name: {}; Value: {:.2f}".format(param_name, param_value))
            print()

    print("End...")

if __name__ == "__main__":
    main()
