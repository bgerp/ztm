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

import time
from enum import Enum

from utils.logger import get_logger
from utils.logic.timer import Timer
from utils.logic.state_machine import StateMachine

from devices.drivers.modbus.device import ModbusDevice
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.register_type import RegisterType

# (Request from mail: Eml6429)

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

__class_name__ = "EnergyCenter"
"""Plugin class name."""

#endregion

class Pump(ModbusDevice):
    """Fluid pump.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __debit = 0
    """Debit of the pump.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "Grundfos"

        self._model = "Pump"

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_debit(self, debit):

        if self.__debit == debit:
            return

        temp_debit = debit

        if temp_debit < 0:
            temp_debit = 0

        if temp_debit > 100:
            temp_debit = 100

        self.__debit = temp_debit

        self.__logger.debug("Set debit of {} to {}".format(self.name, self.__debit))

    def init(self):
        """Init the pump.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

    def update(self):
        """Update the pump logic.
        """

        # TODO: Check which register is responsible for controlling the debit of the pump.

        pass

    def shutdown(self):
        """Shutdown the pump.
        """

        pass

#endregion
