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

from pymodbus.pdu import ModbusRequest
from pymodbus.pdu import ModbusExceptions as merror

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

class CustomModbusRequest(ModbusRequest):
    """Custume modbus string.
    """

    function_code = 1

    def __init__(self, address):
        ModbusRequest.__init__(self)
        self.address = address
        self.count = 16

    def encode(self):
        return struct.pack(">HH", self.address, self.count)

    def decode(self, data):
        self.address, self.count = struct.unpack(">HH", data)

    def execute(self, context):
        """Execute the request.

        Args:
            context (Modbusrequest): The request.

        Returns:
            ModbusResponse: Response from the server.
        """

        if not 1 <= self.count <= 0x7d0:
            return self.doException(merror.IllegalValue)

        if not context.validate(self.function_code, self.address, self.count):
            return self.doException(merror.IllegalAddress)

        values = context.getValues(self.function_code, self.address, self.count)

        return values
