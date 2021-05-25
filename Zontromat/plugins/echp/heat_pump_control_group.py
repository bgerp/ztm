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
from datetime import date

from utils.logger import get_logger
from utils.logic.timer import Timer
from utils.logic.state_machine import StateMachine
from utils.logic.functions import rotate_list

from plugins.base_plugin import BasePlugin

from devices.vendors.HstarsGuangzhouRefrigeratingEquipmentGroup.heat_pump import HeatPump, HeatPumpMode
from devices.utils.valve_control_group.valve_control_group import ValveControlGroup

from devices.factories.pump.pump_factory import PumpFactory
from devices.factories.heat_pump.heat_pump_factory import HeatPumpFactory
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

#endregion

class HeatPumpControllGroup(BasePlugin):

#region Attributes

    __logger = None
    """Logger
    """

    __heat_pump_orders = []
    """Het pump priority order.
    """

    __day_order = -1
    """Day order index.
    """

    __interval_step = 3
    """Interval step.
    """

    __cold_interval = 0
    """Cold interval.
    """

    __hot_interval = 0
    """Hot interval.
    """

    __vcg_cold_buff = None

    __vcg_cold_geo = None

    __v_warm_geo = None

    __v_warm_floor = None

    __v_hot = None

    __heat_pump = None

    __cold_water_pump = None

    __hot_water_pump = None

    __warm_g_water_pump = None

    __warm_p_water_pump = None

#endregion

#region Attributes Registers Values

    __heat_pumps_count = 3
    """Het pump count.
    """

    __heat_pump_index = 0
    """Heat pump index.
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

    __temp_cold = 0
    """Temperature cold water.
    """

    __temp_hot = 0
    """Temperature hot water.
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

#endregion

#region Constructor / Destructor

    def __init__(self, **config):

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        # Valve group cold buffer. (BLUE)
        self.__vcg_cold_buff = ValveControlGroup.create(
            name="VCG Cold Buffer",
            key="{}.vcg_cold_buf".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["input", "output"],
            rev_valves=["short"])

        # Valve group cold geo. (GREEN)
        self.__vcg_cold_geo = ValveControlGroup.create(
            name="VCG Cold Geo",
            key="{}.vcg_cold_geo".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["input", "output"])

        # Valve group warm geo. (GREEN)
        self.__vcg_warm_geo = ValveControlGroup.create(
            name="VCG Warm Geo",
            key="{}.vcg_warm_geo".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["input", "output"],
            rev_valves=["short"])

        # Valve group warm floor. (PURPLE)
        self.__vcg_warm_floor = ValveControlGroup.create(
            name="VCG Warm floor",
            key="{}.vcg_warm_floor".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["input", "output"],
            rev_valves=["short"])

        registers = config["registers"]

        register = registers.by_name("{}.wp_cold.settings".format(self.key))
        if register is not None:
            wp_setting = register.value

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__cold_water_pump = PumpFactory.create(name="WP Cold", controller=self._controller, params=params)

        register = registers.by_name("{}.wp_hot.settings".format(self.key))
        if register is not None:
            wp_setting = register.value

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__hot_water_pump = PumpFactory.create(name="WP Hot", controller=self._controller, params=params)

        
        register = registers.by_name("{}.wp_warm_g.settings".format(self.key))
        if register is not None:
            wp_setting = register.value

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__warm_g_water_pump = PumpFactory.create(name="WP Warm G", controller=self._controller, params=params)

        register = registers.by_name("{}.wp_warm_p.settings".format(self.key))
        if register is not None:
            wp_setting = register.value

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__warm_p_water_pump = PumpFactory.create(name="WP Warm P", controller=self._controller, params=params)

        register = registers.by_name("{}.hp.settings".format(self.key))
        if register is not None:
            wp_setting = register.value

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__heat_pump = HeatPumpFactory.create(name="Heat Pump", controller=self._controller, params=params)

    def __del__(self):
        """Destructor
        """

        # Valve Control Groups
        if self.__vcg_cold_buff is not None:
            del self.__vcg_cold_buff

        if self.__vcg_cold_geo is not None:
            del self.__vcg_cold_geo

        if self.__v_warm_geo is not None:
            del self.__v_warm_geo

        if self.__v_warm_floor is not None:
            del self.__v_warm_floor

        if self.__v_hot is not None:
            del self.__v_hot

        # Thermal agents pumps.
        if self.__cold_water_pump is not None:
            del self.__cold_water_pump
        
        if self.__hot_water_pump is not None:
            del self.__hot_water_pump
        
        if self.__warm_g_water_pump is not None:
            del self.__warm_g_water_pump
        
        if self.__warm_p_water_pump is not None:
            del self.__warm_p_water_pump

        # Heat pump.
        if self.__heat_pump is not None:
            del self.__heat_pump

        super().__del__()

        if self.__logger is not None:
            del self.__logger
#endregion

#region Private Methods

    def __generate_order(self):

        first_order = []

        for index in range(self.__heat_pumps_count):

            first_order.append(index)

        for index in range(self.__heat_pumps_count):

            temp_list = rotate_list(first_order, index)

            self.__heat_pump_orders.append(temp_list.copy())

    def __get_days(self):
        """Get days till now from 1970 January 1st.

        Returns:
            [int]: Days
        """

        days = -1

        day_0 = date(1970, 1, 1)
        day_1 = date.today()
        delta = day_1 - day_0
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

        # Тези температури ще се вземат:
        # или от bgERP
        # или от директно свързаните датчици към Зонтромат
        # или от датчиците на машините на техните съответни входове.

        self.temp_cold = 2.5

    def __update_temp_hot(self):
        """Update hotwater temperature.
        """

        # Тези температури ще се вземат
        # или от bgERP
        # или от директно свързаните датчици към Зонтромат
        # или от датчиците на машините на техните съответни входове.

        self.temp_hot = 42.5

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

#region Registers Interface

    def __hp_count_cb(self, register):
        """Heat pump control group count callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__heat_pumps_count = register.value

    def __hp_index_cb(self, register):
        """Heat pump control group index callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__heat_pump_index = register.value

    def __hp_cold_min_cb(self, register):
        """Heat pump control group cold minimum callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__cold_min = register.value

    def __hp_cold_max_cb(self, register):
        """Heat pump control group cold maximum callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__cold_min = register.value

    def __hp_hot_min_cb(self, register):
        """Heat pump control group hot maximum callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__hot_min = register.value

    def __hp_hot_max_cb(self, register):
        """Heat pump control group hot maximum callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__hot_max = register.value

    def __init_registers_cb(self):
        """Initialize the registers callbacks.
        """

        hp_count = self._registers.by_name("{}.hp.count".format(self.key))
        if hp_count is not None:
            hp_count.update_handlers = self.__hp_count_cb
            hp_count.update()

        hp_index = self._registers.by_name("{}.hp.index".format(self.key))
        if hp_index is not None:
            hp_index.update_handlers = self.__hp_index_cb
            hp_index.update()

        hp_cold_min = self._registers.by_name("{}.hp.cold_min".format(self.key))
        if hp_cold_min is not None:
            hp_cold_min.update_handlers = self.__hp_cold_min_cb
            hp_cold_min.update()

        hp_cold_max = self._registers.by_name("{}.hp.cold_max".format(self.key))
        if hp_cold_max is not None:
            hp_cold_max.update_handlers = self.__hp_cold_max_cb
            hp_cold_max.update()

        hp_hot_min = self._registers.by_name("{}.hp.hot_min".format(self.key))
        if hp_hot_min is not None:
            hp_hot_min.update_handlers = self.__hp_hot_min_cb
            hp_hot_min.update()

        hp_hot_max = self._registers.by_name("{}.hp.hot_max".format(self.key))
        if hp_hot_max is not None:
            hp_hot_max.update_handlers = self.__hp_hot_max_cb
            hp_hot_max.update()

    def __update_registers(self):

        # Update machine power.
        hp_power = self._registers.by_name("{}.hp.power".format(self.key))
        if hp_power is not None:
            hp_power.value = self.__heat_pump_power

        # Update machine mode.
        hp_mode = self._registers.by_name("{}.hp.mode".format(self.key))
        if hp_mode is not None:
            hp_mode.value = self.__heat_pump_mode

        hp_mode = self._registers.by_name("{}.hp.run".format(self.key))
        if hp_mode is not None:
            hp_mode.value = self.__heat_pump_run

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

        if self.__temp_cold == value:
            return

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

        if self.__temp_hot == value:
            return

        temp_value = value

        if temp_value < self.__hot_min:
            temp_value = self.__hot_min

        if temp_value > self.__hot_max:
            temp_value = self.__hot_max

        self.__temp_hot = temp_value

#endregion

#region Public Methods

    def init(self):
        """Init the group.
        """

        # Set default values for temperatures.
        self.temp_cold = ((self.__cold_max - self.__cold_min) / 2) + self.__cold_min
        self.temp_hot = ((self.__hot_max - self.__hot_min) / 2) + self.__hot_min

        # Set intervals.
        self.__cold_interval = (self.__cold_max - self.__cold_min) / self.__interval_step
        self.__hot_interval = (self.__hot_max - self.__hot_min) / self.__interval_step

        # init the registers callbacks.
        self.__init_registers_cb()

        # Generate order.
        self.__generate_order()

        # Heat pump.
        self.__heat_pump.init()

        # Thermal agents pumps.
        self.__cold_water_pump.init()
        self.__hot_water_pump.init()
        self.__warm_p_water_pump.init()
        self.__warm_g_water_pump.init()

        # Valve Control Groups (RED, BLUE, PURPLE and GREEN)
        self.__vcg_cold_buff.init()
        self.__vcg_cold_geo.init()
        self.__vcg_warm_geo.init()
        self.__vcg_warm_floor.init()

    def update(self):
        """Update control group.
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
        self.__update_run_flag()

        # ========================================================================

        # -=== UNDER TEST ===-

        output_power = self.__heat_pump_run * self.__heat_pump_power

        # Open cold circuit.
        self.__vcg_cold_buff.target_position = output_power
        self.__cold_water_pump.set_debit(output_power)

        # Open warm circuit.
        self.__vcg_warm_geo.target_position = output_power
        self.__warm_p_water_pump.set_debit(output_power)

        # run pump for hot circuit.
        self.__hot_water_pump.set_debit(output_power)

        # ========================================================================

        # Valve Control Groups
        self.__vcg_cold_buff.update()
        self.__vcg_cold_geo.update()
        self.__vcg_warm_geo.update()
        self.__vcg_warm_floor.update()

        # Thermal agents pumps.
        self.__cold_water_pump.update()
        self.__hot_water_pump.update()
        self.__warm_g_water_pump.update()
        self.__warm_p_water_pump.update()

        # Heat pump.
        self.__heat_pump.set_mode(self.__heat_pump_mode)
        self.__heat_pump.set_power(self.__heat_pump_power)
        self.__heat_pump.update()

        self.__update_registers()

    def shutdown(self):

        # Valve Control Groups
        self.__vcg_cold_buff.shutdown()
        self.__vcg_cold_geo.shutdown()
        self.__vcg_warm_geo.shutdown()
        self.__vcg_warm_floor.shutdown()

        # Thermal agents pumps.
        self.__cold_water_pump.shutdown()
        self.__hot_water_pump.shutdown()
        self.__warm_g_water_pump.shutdown()
        self.__warm_p_water_pump.shutdown()

        # Heat pump.
        self.__heat_pump.shutdown()

#endregion
