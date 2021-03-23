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

from controllers.zuljana.requests.read_device_coils import ReadDeviceCoils
from controllers.zuljana.requests.read_device_discrete_inputs import ReadDeviceDiscreteInputs
from controllers.zuljana.requests.read_device_holding_registers import ReadDeviceHoldingRegisters
from controllers.zuljana.requests.read_device_input_registers import ReadDeviceInputRegisters

from controllers.zuljana.requests.write_device_coils import WriteDeviceCoils
from controllers.zuljana.requests.write_device_registers import WriteDeviceRegisters

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

    with ModbusClient(
        method="rtu",
        port="COM13", 
        timeout=1,
        baudrate=19200,
        rtscts=0,
        dsrdtr=0) as client:

        # Read device coils.
        cr_request = ReadDeviceCoils(unit)
        cr_response = client.execute(cr_request)
        print(cr_response)

        di_request = ReadDeviceDiscreteInputs(unit)
        di_response = client.execute(di_request)
        print(di_response)

        hrr_request = ReadDeviceHoldingRegisters(unit)
        hrr_response = client.execute(hrr_request)
        print(hrr_response)

        irr_request = ReadDeviceInputRegisters(unit)
        irr_response = client.execute(irr_request)
        print(irr_response)

        cw_request = WriteDeviceCoils(unit)
        cw_response = client.execute(cw_request)
        print(cw_response)

        hrw_request = WriteDeviceRegisters(unit)
        hrw_response = client.execute(hrw_request)
        print(hrw_response)

if __name__ == "__main__":
    main()
