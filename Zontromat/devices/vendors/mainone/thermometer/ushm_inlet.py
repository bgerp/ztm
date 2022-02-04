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

from devices.drivers.modbus.device import ModbusDevice
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.register_type import RegisterType

# (Request from mail: Eml6429)

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

class USHMInlet(ModbusDevice):
    """Mainone - Ultrasonic Heat Metter.
    https://shmw1688.en.alibaba.com/product/62524917832-815102973/Supply_low_power_high_accuracy_ultrasonic_heat_meter_M_BUS_RS_485_NB_IOT_LoRa_wan_pulse_heat_output_brass_heat_meter.html?spm=a2700.shop_index.92937.6.6e3231d4ZOZIQX
    """

#region Attributes

    __logger = None
    """Logger
    """

    __last_good_measurement = 0
    """Last good known value from the thermometer.
    """

    __unsuccessful_times = 0
    """Unsuccessful times counter.
    """

    __unsuccessful_times_limit = 5
    """Unrestful times limit counter.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)

        self._vendor = "Mainone"

        self._model = "USHMInlet"

        self._parameters.append(
            Parameter(
                "AccumulateHeatEnergy",
                "kWh",
                ParameterType.UINT32_T,
                [0, 1],
                RegisterType.ReadHoldingRegisters
            )
        )

#endregion

    def get_temp(self):
        """Get temperature.

        Returns:
            float: Value of the temperature.
        """

        value = 0.0

        # TODO: Split the device.

        try:
            request = self.generate_request("AccumulateHeatEnergy")
            response = self._controller.execute_mb_request(request, self.uart)
            if response is not None:
                if not response.isError():
                    value = response.registers[0] / 10

                    # Dump good value.
                    self.__last_good_measurement = value

                    # Reset the counter.
                    self.__unsuccessful_times = 0

                else:
                    self.__unsuccessful_times += 1
                    value = self.__last_good_measurement

            else:
                self.__unsuccessful_times += 1
                value = self.__last_good_measurement

        except Exception:
            self.__unsuccessful_times += 1
            value = self.__last_good_measurement

        if self.__unsuccessful_times >= self.__unsuccessful_times_limit:
            GlobalErrorHandler.log_hardware_malfunction(
                self.__logger, "Device: {}; ID: {}; Can not read the temperature value.".format(
                    self.name, request.unit_id))

        return value