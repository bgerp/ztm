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

from devices.drivers.modbus.requests.read_device_coils import ReadDeviceCoils
from devices.drivers.modbus.requests.read_device_discrete_inputs import ReadDeviceDiscreteInputs
from devices.drivers.modbus.requests.read_device_holding_registers import ReadDeviceHoldingRegisters
from devices.drivers.modbus.requests.read_device_input_registers import ReadDeviceInputRegisters

from devices.drivers.modbus.requests.write_device_coils import WriteDeviceCoils
from devices.drivers.modbus.requests.write_device_registers import WriteDeviceRegisters

from devices.super.s8_3cn.s8_3cn import S8_3CN as BlackIsland

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

    # Black Island interface.
    bi = BlackIsland()

    # Create client.
    with ModbusClient(method="rtu", port=port, baudrate=9600, timeout=1,
        xonxoff=False, rtscts=False, dsrdtr=False) as client:

        #---------------------------------------------------------------------------#
        # Generate request.
        requests = bi.generate_requests(1, coils=[False]*16, registers=[0]*4)
        #---------------------------------------------------------------------------#

        #---------------------------------------------------------------------------#
        # Read Coils.
        #---------------------------------------------------------------------------#
        cr_request = requests["ReadDeviceCoils"]
        cr_response = client.execute(cr_request)
        
        # Check the response.
        assert not cr_response.isError(), "All relays should be OFF."

        # Check the content.
        is_ok = cr_response.bits == [False]*12 + [False]*4
        assert is_ok, "All the relays should be OFF."

        print(cr_response)
        print()

        #---------------------------------------------------------------------------#
        # Read Discrete Inputs.
        #---------------------------------------------------------------------------#
        di_request = requests["ReadDeviceDiscreteInputs"]
        di_response = client.execute(di_request)

        # Check the response.
        assert(not di_response.isError())

        #Check the content.
        is_ok = di_response.bits == [False]*8
        assert(is_ok)

        print(di_response)
        print()

        #---------------------------------------------------------------------------#
        # Read Holding Registers.
        #---------------------------------------------------------------------------#
        hrr_request = requests["ReadDeviceHoldingRegisters"]
        hrr_response = client.execute(hrr_request)

        # Check the response.
        assert(not hrr_response.isError())

        #Check the content.
        is_ok = hrr_response.registers == [0]*4
        assert(is_ok)

        print(hrr_response)
        print()

        #---------------------------------------------------------------------------#
        # Read Input Registers.
        #---------------------------------------------------------------------------#
        irr_request = requests["ReadDeviceInputRegisters"]
        irr_response = client.execute(irr_request)

        # Check the response.
        assert(not irr_response.isError())

        #Check the content.
        is_ok = irr_response.registers == [0]*8
        assert(is_ok)

        print(irr_response)
        print()

        #---------------------------------------------------------------------------#
        # Generate request.
        requests = bi.generate_requests(1, coils=[True]*16, registers=[50000]*4)
        #---------------------------------------------------------------------------#

        #---------------------------------------------------------------------------#
        # Write Coils.
        #---------------------------------------------------------------------------#
        cw_request = requests["WriteDeviceCoils"]
        cw_response = client.execute(cw_request)

        # Check the response.
        assert(not cw_response.isError())
        print(cw_response)

        cr_request = requests["ReadDeviceCoils"]
        cr_response = client.execute(cr_request)

        # Check the response.
        assert(not cr_response.isError())

        #Check the content.
        is_ok = cr_response.bits == [True]*12 + [False]*4
        assert(is_ok)

        print(cr_response)
        print()

        #---------------------------------------------------------------------------#
        # Write Holding Registers.
        #---------------------------------------------------------------------------#
        hrw_request = requests["WriteDeviceRegisters"]
        hrw_response = client.execute(hrw_request)

        # Check the response.
        assert(not hrw_response.isError())
        print(hrw_response)

        hrr_request = requests["ReadDeviceHoldingRegisters"]
        hrr_response = client.execute(hrr_request)

        # Check the response.
        assert(not hrr_response.isError())

        #Check the content.
        is_ok = hrr_response.registers == [50000]*4
        assert(is_ok)

        print(hrr_response)
        print()

        #---------------------------------------------------------------------------#
        # Generate request.
        requests = bi.generate_requests(1, coils=[False]*16, registers=[0]*4)
        #---------------------------------------------------------------------------#

        #---------------------------------------------------------------------------#
        # Write Coils.
        #---------------------------------------------------------------------------#
        cw_request = requests["WriteDeviceCoils"]
        cw_response = client.execute(cw_request)

        # Check the response.
        assert(not cw_response.isError())
        print(cw_response)

        cr_request = requests["ReadDeviceCoils"]
        cr_response = client.execute(cr_request)

        # Check the response.
        assert(not cr_response.isError())

        #Check the content.
        is_ok = cr_response.bits == [False]*12 + [False]*4
        assert(is_ok)

        print(cr_response)
        print()

        #---------------------------------------------------------------------------#
        # Write Holding Registers.
        #---------------------------------------------------------------------------#
        hrw_request = requests["WriteDeviceRegisters"]
        hrw_response = client.execute(hrw_request)

        # Check the response.
        assert(not hrw_response.isError())
        print(hrw_response)

        hrr_request = requests["ReadDeviceHoldingRegisters"]
        hrr_response = client.execute(hrr_request)

        # Check the response.
        assert(not hrr_response.isError())

        #Check the content.
        is_ok = hrr_response.registers == [0]*4
        assert(is_ok)

        print(hrr_response)
        print()

if __name__ == "__main__":
    main()
