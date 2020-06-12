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

from utils.logger import get_logger

from plugins.base_plugin import BasePlugin

from devices.Eastron.sdm120 import SDM120
from devices.Eastron.sdm630 import SDM630

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
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

class PowerMeter(BasePlugin):
    """Power meter device."""

#region Attributes

    __logger = None
    """Logger"""

    __power_meter = None
    """Power metter."""

    __parameters_values = {}
    """Parameters values."""

    __uart = None
    """UART"""

    __dev_id = None
    """Device ID"""

    __register_type = None
    """Register Type"""

#endregion

#region Destructor

    def __del__(self):
        del self.__logger

#endregion

#region Public Methods

    def init(self):

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {} with name {}".format(__name__, self.name))

        uart = self._registers.by_name(self._key + ".sub_dev.uart")
        if uart is not None:
            self.__uart = uart.value

        dev_id = self._registers.by_name(self._key + ".sub_dev.dev_id")
        if dev_id is not None:
            self.__dev_id = dev_id.value

        vendor = self._registers.by_name(self._key + ".sub_dev.vendor").value
        if vendor == "Eastron":

            model = self._registers.by_name(self._key + ".sub_dev.model").value
            if model == "SDM120":
                self.__power_meter = SDM120()
                self.__register_type = "inp"

            elif model == "SDM630":
                self.__power_meter = SDM630()
                self.__register_type = "inp"

    def update(self):

        # Get structure data.
        registers_ids = self.__power_meter.get_registers_ids()

        # Get values by the structure.
        registers_values = self._controller.read_mb_registers(\
            self.__uart, \
            self.__dev_id, \
            registers_ids, \
            self.__register_type)

        # Convert values to human readable.
        parameters_values = self.__power_meter.get_parameters_values(registers_values)

        # Format the floating points.
        for parameter_value in parameters_values:
            try:
                parameters_values[parameter_value] = \
                    float('{:06.3f}'.format(float(parameters_values[parameter_value])))

            except ValueError:
                parameters_values[parameter_value] = float('{:06.3f}'.format(000.0))

        self.__parameters_values = parameters_values


        if  isinstance(self.__power_meter, SDM120):

            # Update parameters in the registers.
            self._registers.by_name("self_current.sub_dev.current").value\
                = self.__parameters_values["Current"]

            self._registers.by_name("self_current.sub_dev.total_energy").value\
                = self.__parameters_values["ExportActiveEnergy"]

            self._registers.by_name("self_current.sub_dev.current_power").value\
                = self.__parameters_values["ApparentPower"]

    def shutdown(self):

        self.__logger.info("Shutting down the {} with name {}".format(__name__, self.name))

#endregion
