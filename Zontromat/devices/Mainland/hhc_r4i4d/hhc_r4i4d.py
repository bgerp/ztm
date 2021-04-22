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

from devices.drivers.modbus.device import Device
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

class HHC_R4I4D(Device):
    """This class is dedicated to communicate with remote modbus module HHC-R4I4D.

    See: README.md"""

#region Constructor

    def __init__(self):
        """Constructor"""

        self._parameters.append(
            Parameter(
                "GetRelays",
                "Bits",
                ParameterType.INT16_T,
                [16, 17, 18, 19],
                RegisterType.ReadCoil
            )
        )

        self._parameters.append(
            Parameter(
                "GetDigitalInputs",
                "Bits",
                ParameterType.INT16_T,
                [32, 33, 34, 35],
                RegisterType.ReadDiscreteInput
            )
        )

        self._parameters.append(
            Parameter(
                "SetRelays",
                "Bits",
                ParameterType.INT16_T,
                [16, 17, 18, 19],
                RegisterType.WriteMultipleCoils
            )
        )

#endregion
