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
import json
from datetime import date
from enum import Enum

from utils.logger import get_logger
#from utils.timer import Timer
#from utils.state_machine import StateMachine

from plugins.base_plugin import BasePlugin
from plugins.ec.valve import Valve
from plugins.ec.valve_control_group import ValveControlGroup
from plugins.ec.heat_pump_control_group import HeatPumpControllGroup
from plugins.ec.heat_pump import HeatPumpMode

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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



class EnergyCenter(BasePlugin):
    """Energy center control plugin."""

#region Attributes

    __logger = None
    """Logger
    """

    __cold_min = 5
    """Cold water minimum.
    """

    __cold_max = 7
    """Cold water maximum.
    """

    __hot_min = 41
    """Hot water minimum.
    """

    __hot_max = 46
    """Hot water maximum.
    """

    __cold_interval = 0
    """Cold interval.
    """

    __hot_interval = 0
    """Hot interval.
    """

    __temp_cold = 0
    """Temperature cold water.
    """

    __temp_hot = 0
    """Temperature hot water.
    """

    __day_order = -1
    """Day order index.
    """

    __winter_power = 0
    """Winter power.
    """

    __summer_power = 0
    """Summer power.
    """

    __heat_pump_mode = HeatPumpMode.NONE
    """Heat pump mode.
    """

    __heat_pump_power = 0
    """Heat pump power.
    """

    __heat_pump_run = False
    """Heat pump run flag.
    """

    __heat_pumps_count = 3
    """Het pump count.
    """

    __interval_step = 3
    """Interval step.
    """

    __heat_pump_orders = []
    """Het pump priority order.
    """

    __heat_pumps = []
    """Heat pumps.
    """

    __v_foyer = None
    """Valve foyer.
    """

    __v_underfloor_heating_trestle = None
    """Underfloor heating trestle.
    """

    __v_underfloor_heating_pool = None
    """Underfloor heating pool.
    """

    __v_pool_heating = None
    """Pool heating.
    """

    __vcg_tva_pool = None
    """TVA pool.
    """

    __vcg_convectors_east = None
    """Convectors east.
    """

    __vcg_floor_east = None
    """Floor east.
    """

    __vcg_convectors_west = None
    """Convectors west.
    """

    __vcg_tva_fitness = None
    """TVA fitness.
    """

    __vcg_tva_roof_floor = None
    """TVA roof floor.
    """

    __v_floor_west = None
    """Floor west.
    """

    __v_tva_conference_center = None
    """TVA conference centre.
    """

    __v_convectors_kitchen = None
    """Convectors kitchen.
    """

    __v_tva_warehouse = None
    """TVA wearhouse.
    """

    __v_generators_cooling = None
    """Generators cooling.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, config):
        """Constructor

        Args:
            config (kwargs): Configuration of the object.
        """

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        # Create heatpump groups.
        self.__heat_pumps.append(HeatPumpControllGroup(name="HP1", controller=self._controller, registers=self._registers))
        self.__heat_pumps.append(HeatPumpControllGroup(name="HP2", controller=self._controller, registers=self._registers))
        self.__heat_pumps.append(HeatPumpControllGroup(name="HP3", controller=self._controller, registers=self._registers))

        # Valve group. (PURPLE)
        self.__v_foyer = Valve(\
            name="v_foyer",
            controller=self._controller,
            registers=self._registers)

        self.__v_underfloor_heating_trestle  = Valve(
            name="v_underfloor_heating_trestle",
            controller=self._controller,
            registers=self._registers)

        self.__v_underfloor_heating_pool  = Valve(
            name="v_underfloor_heating_pool",
            controller=self._controller,
            registers=self._registers)

        # Consumers (RED)
        self.__v_pool_heating = ValveControlGroup.create(\
            name="v_pool_heating",
            fw_valves=["v_hot_pool_heating"],
            fw_pumps=["p_pool_heating"],
            controller=self._controller,
            registers=self._registers)

        # TVA Pool (RED and BLUE)
        self.__vcg_tva_pool = ValveControlGroup.create(\
            name="v_tva_pool",
            fw_valves=["v_cold_tva_pool"],
            rev_valves=["v_hot_tva_pool"],
            fw_pumps=["p_tva_pool"],
            controller=self._controller,
            registers=self._registers)

        # Convectors East (RED and BLUE)
        self.__vcg_convectors_east = ValveControlGroup.create(\
            name="v_convectors_east",
            fw_valves=["v_cold_convectors_east"],
            rev_valves=["v_hot_convectors_east"],
            fw_pumps=["p_convectors_east"],
            controller=self._controller,
            registers=self._registers)

        # Floor East (RED and BLUE)
        self.__vcg_floor_east = ValveControlGroup.create(\
            name="v_floor_east",
            fw_valves=["v_cold_floor_east"],
            rev_valves=["v_hot_floor_east"],
            fw_pumps=["p_floor_east"],
            controller=self._controller,
            registers=self._registers)


        # Convectors West (RED and BLUE)
        self.__vcg_convectors_west = ValveControlGroup.create(\
            name="v_convectors_west",
            fw_valves=["v_cold_convectors_west"],
            rev_valves=["v_hot_convectors_west"],
            fw_pumps=["p_convectors_west"],
            controller=self._controller,
            registers=self._registers)

        # TVA Fitness (RED and BLUE)
        self.__vcg_tva_fitness = ValveControlGroup.create(\
            name="v_tva_fitness",
            fw_valves=["v_cold_tva_fitness"],
            rev_valves=["v_hot_tva_fitness"],
            fw_pumps=["p_tva_fitness"],
            controller=self._controller,
            registers=self._registers)

        # TVA Roof Floor (RED and BLUE)
        self.__vcg_tva_roof_floor = ValveControlGroup.create(\
            name="v_tva_roof_floor",
            fw_valves=["v_cold_tva_roof_floor"],
            rev_valves=["v_hot_tva_roof_floor"],
            fw_pumps=["p_tva_roof_floor"],
            controller=self._controller,
            registers=self._registers)

        # Floor West (RED and BLUE)
        self.__vcg_floor_west = ValveControlGroup.create(\
            name="v_floor_west",
            fw_valves=["v_cold_floor_west"],
            rev_valves=["v_hot_floor_west"],
            fw_pumps=["p_floor_west"],
            controller=self._controller,
            registers=self._registers)

        # TVA Conference (RED and BLUE)
        self.__vcg_tva_conference_center = ValveControlGroup.create(\
            name="v_tva_conference_center",
            fw_valves=["v_cold_tva_conference_center"],
            rev_valves=["v_hot_tva_conference_center"],
            fw_pumps=["p_conference_center"],
            controller=self._controller,
            registers=self._registers)

        # Convectors Kitchen (RED and BLUE)
        self.__vcg_convectors_kitchen = ValveControlGroup.create(\
            name="v_convectors_kitchen",
            fw_valves=["v_cold_convectors_kitchen"],
            rev_valves=["v_hot_convectors_kitchen"],
            fw_pumps=["p_convectors_kitchen"],
            controller=self._controller,
            registers=self._registers)

        # TVA Wearhouse (RED and BLUE)
        self.__vcg_tva_warehouse = ValveControlGroup.create(\
            name="v_tva_warehouse",
            fw_valves=["v_cold_tva_warehouse"],
            rev_valves=["v_hot_tva_warehouse"],
            fw_pumps=["p_tva_warehouse"],
            controller=self._controller,
            registers=self._registers)

        # Generators Cooling (GREEN)
        self.__v_generators_cooling = Valve(name="v_generators_cooling", controller=self._controller, registers=self._registers)
        self.__v_ground_drill = Valve(name="v_ground_drill", controller=self._controller, registers=self._registers)

        # Air cooling tower (PURPLE)
        self.__v_air_cooling = Valve(name="v_air_cooling", controller=self._controller, registers=self._registers)

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

        # Heat pumps
        for heat_pump in self.__heat_pumps:
            if heat_pump is not None:
                del heat_pump

        # Worm circle (PURPLE)
        if self.__v_foyer is not None:
            del self.__v_foyer

        if self.__v_underfloor_heating_trestle is not None:
            del self.__v_underfloor_heating_trestle

        if self.__v_underfloor_heating_pool is not None:
            del self.__v_underfloor_heating_pool

        # Thermal consumers.
        if self.__v_pool_heating is not None:
            del self.__v_pool_heating

        if self.__vcg_tva_pool is not None:
            del self.__vcg_tva_pool

        if self.__vcg_convectors_east is not None:
            del self.__vcg_convectors_east

        if self.__vcg_floor_east is not None:
            del self.__vcg_floor_east

        if self.__vcg_convectors_west is not None:
            del self.__vcg_convectors_west

        if self.__vcg_tva_fitness is not None:
            del self.__vcg_tva_fitness

        if self.__vcg_tva_roof_floor is not None:
            del self.__vcg_tva_roof_floor

        if self.__v_floor_west is not None:
            del self.__v_floor_west

        if self.__v_tva_conference_center is not None:
            del self.__v_tva_conference_center

        if self.__v_convectors_kitchen is not None:
            del self.__v_convectors_kitchen

        if self.__v_tva_warehouse is not None:
            del self.__v_tva_warehouse

#region Private Methods

    def __rotate_list(self, l, n):
        """Rotate list.

        Args:
            l (list): Target list.
            n (int): Rotations count.

        Returns:
            list: Rotated list.
        """

        return l[-n:] + l[:-n]

    def __generate_order(self):

        first_order = []

        for index in range(self.__heat_pumps_count):

            first_order.append(index)

        for index in range(self.__heat_pumps_count):

            temp_list = self.__rotate_list(first_order, index)

            self.__heat_pump_orders.append(temp_list.copy())

    def __get_days(self):
        """Get days till now from 1970 January 1st.

        Returns:
            [int]: Days
        """

        days = -1

        d0 = date(1970, 1, 1)
        d1 = date.today()
        delta = d1 - d0
        days = delta.days

        return days

    def __unit_order(self):
        """Get machine index based on division with reminder 3.

        Returns:
            [int]: Machine index.
        """

        index = -1

        index = self.__get_days() % self.__heat_pumps_count

        return index

    def __update_day_order(self):
        """Update day order.
        """

        day_order = self.__unit_order()
        if day_order != self.__day_order:
            self.__day_order = day_order

    def __update_temp_cold(self):
        """Update cold temperature.
        """

        # Тези температури ще се вземат или от bgERP или от директно свързаните датчици към Зонтромат или от датчиците на машините на техните съответни входове.
        pass

    def __update_temp_hot(self):
        """Update hotwater temperature.
        """

        # Тези температури ще се вземат или от bgERP или от директно свързаните датчици към Зонтромат или от датчиците на машините на техните съответни входове.
        pass

    def __update_winter_power(self):
        """Update winter power.
        """

        if self.temp_cold < self.__cold_min:
            self.__winter_power = 0

        elif self.temp_cold < self.__cold_min + self.__cold_interval:
            self.__winter_power = 33

        elif self.temp_cold < self.__cold_min + 2 * self.__cold_interval:
            self.__winter_power = 66

        else:
            self.__winter_power = 100

    def __update_summer_power(self):
        """Update summer power.
        """

        if self.temp_hot > self.__hot_max:
            self.__summer_power = 0

        elif self.temp_hot > self.__hot_max - self.__hot_interval:
            self.__summer_power = 33

        elif self.temp_hot > self.__hot_max - 2 * self.__hot_interval:
            self.__summer_power = 66

        else:
            self.__summer_power = 100

    def __update_power_and_mode(self):
        """Update power and mode.
        """

        if self.__summer_power > self.__winter_power:
            self.__heat_pump_mode = HeatPumpMode.Summer
            self.__heat_pump_power = self.__summer_power

        if self.__summer_power < self.__winter_power:
            self.__heat_pump_mode = HeatPumpMode.Winter
            self.__heat_pump_power = self.__winter_power

        if self.__summer_power == self.__winter_power:
            self.__heat_pump_power = self.__winter_power
            if self.__heat_pump_mode == HeatPumpMode.NONE:
                self.__heat_pump_mode = HeatPumpMode.Summer

    def __update_run_flag(self):
        """Update run flag.
        """

        self.__heat_pump_run = \
            (self.__heat_pump_power == 33 and self.__day_order == 0) or\
            (self.__heat_pump_power == 66 and self.__day_order <= 1) or\
            (self.__heat_pump_power == 100)

#endregion

#region Properties

    @property
    def temp_cold(self):
        """Cold water temperature.
        """

        return self.__temp_cold

    @temp_cold.setter
    def temp_cold(self, value):
        """Cold water temperature.
        """

        temp_value = value

        if temp_value < self.__cold_min:
            temp_value = self.__cold_min

        if temp_value > self.__cold_max:
            temp_value = self.__cold_max

        self.__temp_cold = temp_value

    @property
    def temp_hot(self):
        """Hot water temperature.
        """

        return self.__temp_hot

    @temp_hot.setter
    def temp_hot(self, value):
        """Hot water temperature.
        """

        temp_value = value

        if temp_value < self.__hot_min:
            temp_value = self.__hot_min

        if temp_value > self.__hot_max:
            temp_value = self.__hot_max

        self.__temp_hot = temp_value

#endregion

#region Public Methods

    def init(self):
        """Init the plugin.
        """

        # Set default values for temperatures.
        self.temp_cold = ((self.__cold_max - self.__cold_min) / 2) + self.__cold_min
        self.temp_hot = ((self.__hot_max - self.__hot_min) / 2) + self.__hot_min

        # Set intervals.
        self.__cold_interval = (self.__cold_max - self.__cold_min) / self.__interval_step
        self.__hot_interval = (self.__hot_max - self.__hot_min) / self.__interval_step

        self.__generate_order()

        # Heat Pumps
        for heat_pump in self.__heat_pumps:
            heat_pump.init()
            heat_pump.set_mode(HeatPumpMode.NONE)
            heat_pump.set_power(0)

        # Warm (PURPLE)
        self.__v_foyer.init()
        self.__v_underfloor_heating_trestle.init()
        self.__v_underfloor_heating_pool.init()

        # Valve Control Groups (RED and BLUE)
        self.__v_pool_heating.init()
        self.__vcg_tva_pool.init()
        self.__vcg_convectors_east.init()
        self.__vcg_floor_east.init()
        self.__vcg_convectors_west.init()
        self.__vcg_tva_fitness.init()
        self.__vcg_tva_roof_floor.init()
        self.__vcg_floor_west.init()
        self.__vcg_tva_conference_center.init()
        self.__vcg_convectors_kitchen.init()
        self.__vcg_tva_warehouse.init()

        # Generators (GREEN)
        self.__v_generators_cooling.init()

    def update(self):
        """Update the plugin state.
        """

        # Update day order.
        self.__update_day_order()

        # Update temperatures.
        self.__update_temp_cold()
        self.__update_temp_hot()

        # Update powers and mode.
        self.__update_winter_power()
        self.__update_summer_power()
        self.__update_power_and_mode()
        self.__update_run_flag() # TODO: Ask how to set run flag for each machine.

        # SET HEAT PUMPS
        # -----
        for index in range(self.__heat_pumps_count):
            self.__heat_pumps[self.__heat_pump_orders[self.__day_order][index]].set_mode(self.__heat_pump_mode)
            self.__heat_pumps[self.__heat_pump_orders[self.__day_order][index]].set_power(self.__heat_pump_power)
        # -----

        # Update the heat pump groups.
        for index in range(self.__heat_pumps_count):
            self.__heat_pumps[self.__heat_pump_orders[self.__day_order][index]].update()

        self.__v_foyer.update()
        self.__v_underfloor_heating_trestle.update()
        self.__v_underfloor_heating_pool.update()

        # Valve Control Groups
        self.__v_pool_heating.update()
        self.__vcg_tva_pool.update()
        self.__vcg_convectors_east.update()
        self.__vcg_floor_east.update()
        self.__vcg_convectors_west.update()
        self.__vcg_tva_fitness.update()
        self.__vcg_tva_roof_floor.update()
        self.__vcg_floor_west.update()
        self.__vcg_tva_conference_center.update()
        self.__vcg_convectors_kitchen.update()
        self.__vcg_tva_warehouse.update()

        # Generator
        self.__v_generators_cooling.update()

    def shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))
        for heat_pump in self.__heat_pumps:
            heat_pump.shutdown()

        #
        self.__v_foyer.shutdown()
        self.__v_underfloor_heating_trestle.shutdown()
        self.__v_underfloor_heating_pool.shutdown()

        # Valve Control Groups
        self.__v_pool_heating.shutdown()
        self.__vcg_tva_pool.shutdown()
        self.__vcg_convectors_east.shutdown()
        self.__vcg_floor_east.shutdown()
        self.__vcg_convectors_west.shutdown()
        self.__vcg_tva_fitness.shutdown()
        self.__vcg_tva_roof_floor.shutdown()
        self.__vcg_floor_west.shutdown()
        self.__vcg_tva_conference_center.shutdown()
        self.__vcg_convectors_kitchen.shutdown()
        self.__vcg_tva_warehouse.shutdown()

        # Generator
        self.__v_generators_cooling.shutdown()

#endregion
