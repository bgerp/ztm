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

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from data import verbal_const

from devices.factories.blinds.base_blind import BaseBlind
from devices.drivers.modbus.device import ModbusDevice
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.function_code import FunctionCode

from utils.logger import get_logger
from utils.logic.functions import l_scale

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

class BlindsV2(BaseBlind, ModbusDevice):
    """Electronic blinds"""

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        # Pass specific options.
        config["uart"] = config["options"]["uart"]
        config["mb_id"] = config["options"]["mb_id"]

        super().__init__(config)

        self.__new_position = 0

        self._vendor = "YIHAO"

        self._model = "BlindsV2"

        self.__logger = get_logger(__name__)

        self._parameters.append(
            Parameter("Position", "%",\
            ParameterType.UINT16_T_LE, [0x9C43], FunctionCode.WriteSingleHoldingRegister))

#endregion

#region Private Methods

#endregion

#region Public Methods

    def init(self):
        pass

    def update(self):
        pass

    def shutdown(self):
        pass

    def set_position(self, position):
        """Set position of the blinds.

        Args:
            position (float): Position of the blinds.
        """

        if self.__new_position == position:
            return

        if position > 100:
            position = 100

        elif position < 0:
            position = 0

        scaled_position = l_scale(position, [0, 100], [0, 100])

        try:
            request = self.generate_request("Position", Position=int(scaled_position))
            response = self._controller.execute_mb_request(request, self.uart)
            if response is not None:
                if not response.isError():
                    pass
                    # value = response.registers[0] / 10

        except Exception:
            pass

        # TODO: Calculations.

        restored_position = l_scale(scaled_position, [0, 100], [0, 180])

        self.__new_position = restored_position

#endregion
