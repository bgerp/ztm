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

from plugins.base_plugin import BasePlugin

from devices.no_vendors.no_vendor_5.heat_pump import HeatPump, HeatPumpMode
from devices.no_vendors.no_vendor_4.water_pump import WaterPump
from devices.utils.valve_control_group.valve_control_group import ValveControlGroup

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

#endregion

class HeatPumpControllGroup(BasePlugin):

#region Attributes

    _registers = None

    __mode = HeatPumpMode.NONE
    """Mode of the heat pump.
    """

    __power = 0
    """Power of the pump.
    """

    __vcg_cold_buff = None

    __vcg_cold_geo = None

    __v_warm_geo = None

    __v_warm_floor = None

    __v_hot = None

    __heat_pump = None

    __cold_water_pump = None

    __hot_water_pump = None

    __warm_water_pump = None

#endregion

#region Constructor / Destructor

    def __init__(self, **config):

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        if "registers" in config:
            self._registers = config["registers"]

        # Valve group cold buffer. (BLUE)
        self.__vcg_cold_buff = ValveControlGroup.create(\
            name="vcg_cold_buff",
            fw_valves=["v_cold_buff_input", "v_cold_buff_output"],
            rev_valves=["v_cold_buff_short"],
            controller=self._controller,
            registers=self._registers,
            key="{}.cold_buf".format(self._key))

        # Valve group cold geo. (GREEN)
        self.__vcg_cold_geo = ValveControlGroup.create(\
            name="vcg_cold_geo",
            fw_valves=["v_cold_geo_input", "v_cold_geo_output"],
            rev_valves=["v_cold_geo_short"],
            controller=self._controller,
            registers=self._registers)

        # Valve group warm geo. (GREEN)
        self.__vcg_warm_geo = ValveControlGroup.create(\
            name="vcg_warm_geo",
            fw_valves=["v_warm_geo_input", "v_warm_geo_output"],
            rev_valves=["v_warm_geo_short"],
            controller=self._controller,
            registers=self._registers)

        # Valve group warm floor. (PURPLE)
        self.__vcg_warm_floor = ValveControlGroup.create(\
            name="vcg_warm_floor",
            fw_valves=["v_warm_floor_input", "v_warm_floor_output"],
            rev_valves=["v_warm_floor_short"],
            controller=self._controller,
            registers=self._registers)

        self.__cold_water_pump = WaterPump(name="wp_cold", controller=self._controller, registers=self._registers)
        self.__hot_water_pump = WaterPump(name="wp_hot", controller=self._controller, registers=self._registers)
        self.__warm_water_pump = WaterPump(name="wp_warm", controller=self._controller, registers=self._registers)

        self.__heat_pump = HeatPump(name=self._config["name"], controller=self._controller, registers=self._registers)

    def __del__(self):
        """Destructor
        """

        super().__del__()

        # Valve Control Groups
        del self.__vcg_cold_buff
        del self.__vcg_cold_geo
        del self.__v_warm_geo
        del self.__v_warm_floor
        del self.__v_hot

        # Thermal agents pumps.
        del self.__cold_water_pump
        del self.__hot_water_pump
        del self.__warm_water_pump

        # Heat pump.
        del self.__heat_pump

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_mode(self, mode):
        """Set heat pump mode.

        Args:
            mode (HeatPumpMode): Heat pump mode.
        """

        if self.__mode == mode:
            return

        self.__mode = mode

        self.__logger.debug("Heatpump {} set on {} mode.".format(self.name, self.__mode))

    def set_power(self, power):
        """Set heat pump power.

        Args:
            power (int): Power of the machine.
        """

        if self.__power == power:
            return

        self.__power = power

        self.__logger.debug("Heatpump {} set on {} power.".format(self.name, self.__power))

    def init(self):
        """Init the group.
        """

        # Valve Control Groups (RED, BLUE, PURPLE and GREEN)
        self.__vcg_cold_buff.init()
        self.__vcg_cold_geo.init()
        self.__vcg_warm_geo.init()
        self.__vcg_warm_floor.init()

        # Thermal agents pumps.
        self.__cold_water_pump.init()
        self.__hot_water_pump.init()
        self.__warm_water_pump.init()

        # Heat pump.
        self.__heat_pump.init()

    def shutdown(self):

        # Valve Control Groups
        self.__vcg_cold_buff.shutdown()
        self.__vcg_cold_geo.shutdown()
        self.__vcg_warm_geo.shutdown()
        self.__vcg_warm_floor.shutdown()

        # Thermal agents pumps.
        self.__cold_water_pump.shutdown()
        self.__hot_water_pump.shutdown()
        self.__warm_water_pump.shutdown()

        # Heat pump.
        self.__heat_pump.shutdown()

    def update(self):

        # Valve Control Groups
        self.__vcg_cold_buff.update()
        self.__vcg_cold_geo.update()
        self.__vcg_warm_geo.update()
        self.__vcg_warm_floor.update()

        # Thermal agents pumps.
        self.__cold_water_pump.update()
        self.__hot_water_pump.update()
        self.__warm_water_pump.update()

        # Heat pump.
        self.__heat_pump.update()
        # self.__logger.info("Update: {}".format(self.name))

#endregion
