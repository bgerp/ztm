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

from devices.drivers.modbus.device import ModbusDevice
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.register_type import RegisterType

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

class MB308V(ModbusDevice):
    """This class is dedicated to read/write data from S8-3CN GPIO expander.

     - See: http://bends.se/?page=notebook/hardware/gecon-tcp-508n
     - See: http://www.comwintop.com/prod_view.aspx?nid=3&typeid=67&id=245
    """

#region Constructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "Super"

        self._model = "S8_3CN"

        self._parameters.append(
            Parameter(
                "GetRelays",
                "Bits",
                ParameterType.INT16_T,
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                RegisterType.ReadCoil
            )
        )

        self._parameters.append(
            Parameter(
                "GetDigitalInputs",
                "Bits",
                ParameterType.INT16_T,
                [0, 1, 2, 3, 4, 5, 6, 7],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "GetAnalogOutputs",
                "Registers",
                ParameterType.INT16_T,
                [0, 1, 2, 3],
                RegisterType.ReadHoldingRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "GetAnalogInputs",
                "Registers",
                ParameterType.INT16_T,
                [0, 1, 2, 3, 4, 5, 6, 7],
                RegisterType.ReadInputRegisters
            )
        )

        self._parameters.append(
            Parameter(
                "SetRelays",
                "Bits",
                ParameterType.INT16_T,
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                RegisterType.WriteMultipleCoils
            )
        )

        self._parameters.append(
            Parameter(
                "SetAnalogOutputs",
                "Registers",
                ParameterType.INT16_T,
                [0, 1, 2, 3],
                RegisterType.WriteMultipleHoldingRegisters
            )
        )



#endregion
