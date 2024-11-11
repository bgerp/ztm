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

from datetime import date

from utils.logger import get_logger
from utils.logic.functions import rotate_list
from utils.logic.timer import Timer

from plugins.base_plugin import BasePlugin

from devices.vendors.hstars_guangzhou_refrigerating_equipment_group.heat_pump import HP_40STD_N420WHSB4
from devices.utils.valve_control_group.valve_control_group import ValveControlGroup
from devices.utils.valve_control_group.valve_control_group_mode import ValveControlGroupMode

from devices.factories.pumps.pump_factory import PumpFactory
from devices.factories.heat_pumps.heat_pump_factory import HeatPumpFactory
from services.global_error_handler.global_error_handler import GlobalErrorHandler

from data.register import Register, Scope

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

class HeatPumpControlGroup(BasePlugin):
    """Heat pump control group class.
    """

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, **config):

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        self.__heat_pumps_count = 3
        """Het pump count.
        """

        self.__heat_pump_index = 0
        """Heat pump index.
        """

        self.__heat_pump_orders = []
        """Het pump priority order.
        """

        self.__day_order = -1
        """Day order index.
        """

        self.__interval_step = 3
        """Interval step.
        """

        self.__cold_interval = 0
        """Cold interval.
        """

        self.__hot_interval = 0
        """Hot interval.
        """

        self.__cold_min = 5
        """Cold water minimum.
        """

        self.__cold_max = 7
        """Cold water maximum.
        """

        self.__hot_min = 41
        """Hot water minimum.
        """

        self.__hot_max = 46
        """Hot water maximum.
        """

        self.__temp_cold = 0
        """Temperature cold water.
        """

        self.__temp_hot = 0
        """Temperature hot water.
        """

        self.__winter_power = 0
        """Winter power.
        """

        self.__summer_power = 0
        """Summer power.
        """

        self.__heat_pump_mode = 0
        """Heat pump mode.
        """

        self.__heat_pump_power = 0
        """Heat pump power.
        """

        self.__heat_pump_run = False
        """Heat pump run flag.
        """


        self.__vcg_cold = None
        """Valve group cold buffer. (BLUE)
        """

        self.__vcg_cold_geo = None
        """Valve group cold geo. (GREEN)
        """

        self.__vcg_warm_geo = None
        """Valve group warm geo. (GREEN)
        """

        self.__vcg_warm = None
        """Valve group warm floor. (PURPLE)
        """

        self.__vcg_hot = None
        """Valve group warm floor. (RED)
        """

        self.__wp_cold = None
        """Water Pump (BLUE)
        """

        self.__wp_warm = None
        """Water Pump (PURPLE)
        """

        self.__wp_hot = None
        """Water Pump (RED)
        """

        self.__heat_pump = None
        """Heat Pump
        """

        self.__animation_timer = Timer()

    def __del__(self):
        """Destructor
        """

        # Valve Control Groups
        if self.__vcg_cold is not None:
            del self.__vcg_cold

        if self.__vcg_cold_geo is not None:
            del self.__vcg_cold_geo

        if self.__vcg_warm_geo is not None:
            del self.__vcg_warm_geo

        if self.__vcg_warm is not None:
            del self.__vcg_warm

        if self.__vcg_hot is not None:
            del self.__vcg_hot

        # Thermal agents pumps.
        if self.__wp_cold is not None:
            del self.__wp_cold

        if self.__wp_hot is not None:
            del self.__wp_hot

        if self.__wp_warm is not None:
            del self.__wp_warm

        # Heat pump.
        if self.__heat_pump is not None:
            del self.__heat_pump

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods

    def __attach_vcg(self, valve_name: str, settings_cb, mode_cb):
        """Attach valve callbacks.

        Args:
            valve_name (str): Name of the valve.
            settings_cb ([type]): Enable callback.
            mode_cb ([type]): Position callback.
        """

        # Valves settings.
        reg_name = f"{self.key}.{valve_name}.valves.settings"
        settings = self._registers.by_name(reg_name)
        if settings is not None:
            settings.update_handlers = settings_cb
            settings.update()

        # Valves mode.
        reg_name = f"{self.key}.{valve_name}.valves.mode"
        mode = self._registers.by_name(reg_name)
        if mode is not None:
            mode.update_handlers = mode_cb
            mode.update()

    def __attach_pump(self, pump_name: str, settings_cb, mode_cb):
        """Attach pump callbacks.

        Args:
            valve_name (str): Name of the pump.
            settings_cb ([type]): Enable callback.
            mode_cb ([type]): Mode callback.
        """

        # Valves settings.
        reg_name = f"{self.key}.{pump_name}.pump.settings"
        settings = self._registers.by_name(reg_name)
        if settings is not None:
            settings.update_handlers = settings_cb
            settings.update()

        # Valves mode.
        reg_name = f"{self.key}.{pump_name}.pump.mode"
        mode = self._registers.by_name(reg_name)
        if mode is not None:
            mode.update_handlers = mode_cb
            mode.update()

    # TODO: How every individual machine to know which number is for today?

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

        # TODO: How to verify that the registers is out of date?

        # Take information from register.
        # If there is no connection with bgERP, take this information from zontromat sensors.
        # If there is no sensor connected to the zontromat.
        # Or no connection to the sensor, take the information from machines.

        # Тези температури ще се вземат:
        # или от bgERP
        # или от директно свързаните датчици към Зонтромат
        # или от датчиците на машините на техните съответни входове.

        self.temp_cold = 2.5

    def __update_temp_hot(self):
        """Update hotwater temperature.
        """

        # TODO: How to verify that the registers is out of date?

        # Take information from register.
        # If there is no connection with bgERP, take this information from zontromat sensors.
        # If there is no sensor connected to the zontromat.
        # Or no connection to the sensor, take the information from machines.

        # Тези температури ще се вземат
        # или от bgERP
        # или от директно свързаните датчици към Зонтромат
        # или от датчиците на машините на техните съответни входове.

        self.temp_hot = 42.5

    def __update_winter_power(self):
        """Update winter power.
        """

        # TODO: Add schema how to work if the device is 0, 1 or 2
        # It will be better to be done with formula for smooth control.

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

        # TODO: Add schema how to work if the device is 0, 1 or 2
        # It will be better to be done with formula for smooth control.

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
            self.__heat_pump_mode = 1
            self.__heat_pump_power = self.__summer_power

        if self.__summer_power < self.__winter_power:
            self.__heat_pump_mode = 2
            self.__heat_pump_power = self.__winter_power

        if self.__summer_power == self.__winter_power:
            self.__heat_pump_power = self.__winter_power
            if self.__heat_pump_mode == 0:
                self.__heat_pump_mode = 1

    def __update_run_flag(self):
        """Update run flag.
        """

        self.__heat_pump_run = \
            (self.__heat_pump_power == 33 and self.__day_order == 0) or\
            (self.__heat_pump_power == 66 and self.__day_order <= 1) or\
            (self.__heat_pump_power == 100)

#endregion

#region Registers (Parameters)

    def __hp_count_cb(self, register: Register):
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

    def __hp_index_cb(self, register: Register):
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

    def __hp_cold_min_cb(self, register: Register):
        """Heat pump control group cold minimum callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__cold_min = register.value

    def __hp_cold_max_cb(self, register: Register):
        """Heat pump control group cold maximum callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__cold_min = register.value

    def __hp_hot_min_cb(self, register: Register):
        """Heat pump control group hot maximum callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__hot_min = register.value

    def __hp_hot_max_cb(self, register: Register):
        """Heat pump control group hot maximum callback.

        Args:
            register (Register): Register container.
        """

        # Check data type.
        if not register.data_type == "float":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__hot_max = register.value

#endregion

#region Private Methods (Registers for VCG)

    def __cold_valves_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_cold is not None:
                self.__vcg_cold.shutdown()
                del self.__vcg_cold

            # Valve group cold buffer. (BLUE)
            self.__vcg_cold= ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["input"], # This is this way, because the automation is done by wire, now by software.
                mode = ValveControlGroupMode.Proportional)

            if self.__vcg_cold is not None:
                self.__vcg_cold.init()

        elif register.value == {}:
            if self.__vcg_cold is not None:
                self.__vcg_cold.shutdown()
                del self.__vcg_cold

    def __cold_valves_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__vcg_cold is None:
            return

        if register.value == 0:
            self.__vcg_cold.target_position = 0
        elif register.value == 1:
            self.__vcg_cold.target_position = 100

    def __cold_geo_valves_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_cold_geo is not None:
                self.__vcg_cold_geo.shutdown()
                del self.__vcg_cold_geo

            self.__vcg_cold_geo = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["input"], # This is this way, because the automation is done by wire, now by software.
                mode = ValveControlGroupMode.Proportional)

            if self.__vcg_cold_geo is not None:
                self.__vcg_cold_geo.init()

        elif register.value == {}:
            if self.__vcg_cold_geo is not None:
                self.__vcg_cold_geo.shutdown()
                del self.__vcg_cold_geo

    def __cold_geo_valves_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__vcg_cold_geo is None:
            return

        input_value = register.value

        if input_value < 0:
            input_value = 0

        elif input_value > 100:
            input_value = 100

        self.__vcg_cold_geo.target_position = input_value

    def __warm_geo_valves_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_warm_geo is not None:
                self.__vcg_warm_geo.shutdown()
                del self.__vcg_warm_geo

            # Valve group warm geo. (GREEN)
            self.__vcg_warm_geo = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["input"], # This is this way, because the automation is done by wire, now by software.
                mode = ValveControlGroupMode.Proportional)

            if self.__vcg_warm_geo is not None:
                self.__vcg_warm_geo.init()

        elif register.value == {}:
            if self.__vcg_warm_geo is not None:
                self.__vcg_warm_geo.shutdown()
                del self.__vcg_warm_geo

    def __warm_geo_valves_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__vcg_warm_geo is None:
            return

        input_value = register.value

        if input_value < 0:
            input_value = 0

        elif input_value > 100:
            input_value = 100

        self.__vcg_warm_geo.target_position = input_value

    def __warm_valves_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_warm is not None:
                self.__vcg_warm.shutdown()
                del self.__vcg_warm

            # Valve group warm geo. (GREEN)
            self.__vcg_warm = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["input"], # This is this way, because the automation is done by wire, now by software.
                mode = ValveControlGroupMode.Proportional)

            if self.__vcg_warm is not None:
                self.__vcg_warm.init()

        elif register.value == {}:
            if self.__vcg_warm is not None:
                self.__vcg_warm.shutdown()
                del self.__vcg_warm

    def __warm_valves_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__vcg_warm is None:
            return

        input_value = register.value

        if input_value < 0:
            input_value = 0

        elif input_value > 100:
            input_value = 100

        self.__vcg_warm.target_position = input_value

    def __hot_valves_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_hot is not None:
                self.__vcg_hot.shutdown()
                del self.__vcg_hot

            self.__vcg_hot = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["input"], # This is this way, because the automation is done by wire, now by software.
                mode = ValveControlGroupMode.Proportional)

            if self.__vcg_hot is not None:
                self.__vcg_hot.init()

        elif register.value == {}:
            if self.__vcg_hot is not None:
                self.__vcg_hot.shutdown()
                del self.__vcg_hot

    def __hot_valves_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__vcg_hot is None:
            return

        if register.value == 0:
            self.__vcg_hot.target_position = 0
        elif register.value == 1:
            self.__vcg_hot.target_position = 100

    def __update_valves_states(self):
        if self.__vcg_cold is not None:
            self._registers.write(f"{self.key}.cold.valves.state", self.__vcg_cold.target_position)

        if self.__vcg_cold_geo is not None:
            self._registers.write(f"{self.key}.cold_geo.valves.state", self.__vcg_cold_geo.target_position)

        if self.__vcg_warm_geo is not None:
            self._registers.write(f"{self.key}.warm_geo.valves.state", self.__vcg_warm_geo.target_position)

        if self.__vcg_warm is not None:
            self._registers.write(f"{self.key}.warm.valves.state", self.__vcg_warm.target_position)

        if self.__vcg_hot is not None:
            self._registers.write(f"{self.key}.hot.valves.state", self.__vcg_hot.target_position)

#endregion

#region Private Methods (Registers for Pumps)

    def __pump_cold_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__wp_cold is not None:
                self.__wp_cold.shutdown()
                del self.__wp_cold

            self.__wp_cold = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__wp_cold is not None:
                self.__wp_cold.init()

        elif register.value == {}:
            if self.__wp_cold is not None:
                self.__wp_cold.shutdown()
                del self.__wp_cold

    def __pump_cold_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__wp_cold is None:
            return

        self.__wp_cold.e_stop(register.value)

    def __pump_warm_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__wp_warm is not None:
                self.__wp_warm.shutdown()
                del self.__wp_warm

            self.__wp_warm = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__wp_warm is not None:
                self.__wp_warm.init()

        elif register.value == {}:
            if self.__wp_warm is not None:
                self.__wp_warm.shutdown()
                del self.__wp_warm

    def __pump_warm_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__wp_warm is None:
            return

        self.__wp_warm.e_stop(register.value)

    def __pump_hot_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__wp_hot is not None:
                self.__wp_hot.shutdown()
                del self.__wp_hot

            self.__wp_hot = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__wp_hot is not None:
                self.__wp_hot.init()

        elif register.value == {}:
            if self.__wp_hot is not None:
                self.__wp_hot.shutdown()
                del self.__wp_hot

    def __pump_hot_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__wp_hot is None:
            return

        self.__wp_hot.e_stop(register.value)

    def __update_pumps_states(self):
        if self.__wp_cold is not None:
            self.__wp_cold.update()
            reg_state = self._registers.by_name("ecd.pool_air_heating.pump.state")
            if reg_state is not None:
                e_status = self.__wp_cold.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__wp_warm is not None:
            self.__wp_warm.update()
            reg_state = self._registers.by_name("ecd.conv_kitchen.pump.state")
            if reg_state is not None:
                e_status = self.__wp_warm.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__wp_hot is not None:
            self.__wp_hot.update()
            reg_state = self._registers.by_name("ecd.ahu_conf_hall.pump.state")
            if reg_state is not None:
                e_status = self.__wp_hot.e_status()
                reg_state.value = {"e_status" : e_status}

#endregion

#region Private Methods (Registers for Heat Pump)

    def __hp_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__heat_pump is not None:
                self.__heat_pump.shutdown()
                del self.__heat_pump

            self.__heat_pump = HeatPumpFactory.create(
                name="Heat Pump",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__heat_pump is not None:
                self.__heat_pump.init()

        elif register.value == {}:
            if self.__heat_pump is not None:
                self.__heat_pump.shutdown()
                del self.__heat_pump

    def __update_hp_states(self):
        if self.__heat_pump is not None:
            operation_mode = self.__heat_pump.get_operation_mode()
            self._registers.write(f"{self.key}.hp.get_op_mode", operation_mode)
            
            operation_status = self.__heat_pump.get_operation_status()
            self._registers.write(f"{self.key}.hp.get_op_status", operation_status)

            cooling_set_temperature = self.__heat_pump.get_cooling_set_temperature()
            self._registers.write(f"{self.key}.hp.get_cooling_temp", cooling_set_temperature)

            heating_set_temperature = self.__heat_pump.get_heating_set_temperature()
            self._registers.write(f"{self.key}.hp.get_heating_temp", heating_set_temperature)

            system_evaporation_return_water_temperature = self.__heat_pump.get_system_evaporation_return_water_temperature()
            get_system_evaporation_water_temperature = self.__heat_pump.get_system_evaporation_water_temperature()
            system_condensate_returnWater_temperature = self.__heat_pump.get_system_condensate_return_water_temperature()
            system_condensate_water_temperature = self.__heat_pump.get_system_condensate_water_temperature()
            ambient_temperature = self.__heat_pump.get_ambient_temperature()
            hot_water_temperature = self.__heat_pump.get_hot_water_temperature()
            get_temps = {"SystemEvaporationReturnWaterTemperature": system_evaporation_return_water_temperature,
                    "SystemEvaporationWaterTemperature": get_system_evaporation_water_temperature,
                    "SystemCondensateReturnWaterTemperature": system_condensate_returnWater_temperature,
                    "SystemCondensateWaterTemperature": system_condensate_water_temperature,
                    "AmbientTemperature": ambient_temperature,
                    "HotWaterTemperature": hot_water_temperature}
            self._registers.write(f"{self.key}.hp.get_temps", get_temps)

#endregion

#region Private Methods (Registers)

    def __init_registers(self):
        """Initialize the registers callbacks.
        """

        self.__attach_vcg("cold",
                                self.__cold_valves_settings_cb,
                                self.__cold_valves_mode_cb)

        self.__attach_vcg("cold_geo",
                                self.__cold_geo_valves_settings_cb,
                                self.__cold_geo_valves_mode_cb)

        self.__attach_vcg("warm_geo",
                                self.__warm_geo_valves_settings_cb,
                                self.__warm_geo_valves_mode_cb)

        self.__attach_vcg("warm",
                                self.__warm_valves_settings_cb,
                                self.__warm_valves_mode_cb)

        self.__attach_vcg("hot",
                                self.__hot_valves_settings_cb,
                                self.__hot_valves_mode_cb)

        self.__attach_pump("cold",
                                    self.__pump_cold_settings_cb,
                                    self.__pump_cold_mode_cb)

        self.__attach_pump("warm",
                                    self.__pump_warm_settings_cb,
                                    self.__pump_warm_mode_cb)
        
        self.__attach_pump("hot",
                                    self.__pump_hot_settings_cb,
                                    self.__pump_hot_mode_cb)

        hp_settings = self._registers.by_name(f"{self.key}.hp.settings")
        if hp_settings is not None:
            hp_settings.update_handlers = self.__hp_settings_cb
            hp_settings.update()


        hp_count = self._registers.by_name(f"{self.key}.hp.count")
        if hp_count is not None:
            hp_count.update_handlers = self.__hp_count_cb
            hp_count.update()

        hp_index = self._registers.by_name(f"{self.key}.hp.index")
        if hp_index is not None:
            hp_index.update_handlers = self.__hp_index_cb
            hp_index.update()

        hp_cold_min = self._registers.by_name(f"{self.key}.hp.cold_min")
        if hp_cold_min is not None:
            hp_cold_min.update_handlers = self.__hp_cold_min_cb
            hp_cold_min.update()

        hp_cold_max = self._registers.by_name(f"{self.key}.hp.cold_max")
        if hp_cold_max is not None:
            hp_cold_max.update_handlers = self.__hp_cold_max_cb
            hp_cold_max.update()

        hp_hot_min = self._registers.by_name(f"{self.key}.hp.hot_min")
        if hp_hot_min is not None:
            hp_hot_min.update_handlers = self.__hp_hot_min_cb
            hp_hot_min.update()

        hp_hot_max = self._registers.by_name(f"{self.key}.hp.hot_max")
        if hp_hot_max is not None:
            hp_hot_max.update_handlers = self.__hp_hot_max_cb
            hp_hot_max.update()

    def __update_registers(self):

        # Update machine status.
        self._registers.write(f"{self.key}.hp.power", self.__heat_pump_power)
        self._registers.write(f"{self.key}.hp.run", self.__heat_pump_run)

        self.__update_valves_states()

        # self.__update_pumps_states()

        # self.__update_hp_states()

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
        """Initialize the group.
        """

        # Set default values for temperatures.
        self.temp_cold = ((self.__cold_max - self.__cold_min) / 2) + self.__cold_min
        self.temp_hot = ((self.__hot_max - self.__hot_min) / 2) + self.__hot_min

        # Set intervals.
        self.__cold_interval = (self.__cold_max - self.__cold_min) / self.__interval_step
        self.__hot_interval = (self.__hot_max - self.__hot_min) / self.__interval_step

        # Initialize the registers callbacks.
        self.__init_registers()

        # Generate order.
        self.__generate_order()

        # self.__animation_timer.expiration_time = 40
        # self.__animation_timer.update_last_time()

    def update(self):
        """Update control group.
        """

        # Update day order.
        # self.__update_day_order()

        # Update temperatures.
        # self.__update_temp_cold()
        # self.__update_temp_hot()

        # Update powers and mode.
        # self.__update_winter_power()
        # self.__update_summer_power()
        # self.__update_power_and_mode()
        # self.__update_run_flag()

        # ========================================================================

        # -=== UNDER TEST ===-

        # output_power = self.__heat_pump_run * self.__heat_pump_power

        # # Open cold circuit.
        # self.__vcg_cold.target_position = output_power
        # self.__wp_cold.set_setpoint(output_power)

        # # Open warm circuit.
        # self.__vcg_warm_geo.target_position = output_power
        # self.__warm_p_water_pump.set_setpoint(output_power)

        # # run pump for hot circuit.
        # self.__wp_hot.set_setpoint(output_power)

        # ========================================================================
        # self.__animation_timer.update()
        # if self.__animation_timer.expired:
        #     self.__animation_timer.clear()
        #     if self.__vcg_cold.target_position != 50:
        #         self.__vcg_cold.target_position = 50


        if self.__vcg_cold is not None:
            self.__vcg_cold.update()

        if self.__vcg_cold_geo is not None:
            self.__vcg_cold_geo.update()

        if self.__vcg_warm_geo is not None:
            self.__vcg_warm_geo.update()

        if self.__vcg_warm is not None:
            self.__vcg_warm.update()

        if self.__vcg_hot is not None:
            self.__vcg_hot.update()

        if self.__wp_cold is not None:
            self.__wp_cold.update()

        if self.__wp_warm is not None:
            self.__wp_warm.update()

        if self.__wp_hot is not None:
            self.__wp_hot.update()

        if self.__heat_pump is not None:
            self.__heat_pump.update()

        self.__update_registers()

    def shutdown(self):

        # Valve Control Groups
        if self.__vcg_cold is not None:
            self.__vcg_cold.shutdown()

        if self.__vcg_cold_geo is not None:
            self.__vcg_cold_geo.shutdown()

        if self.__vcg_warm_geo is not None:
            self.__vcg_warm_geo.shutdown()

        if self.__vcg_warm is not None:
            self.__vcg_warm.shutdown()

        if self.__vcg_hot is not None:
            self.__vcg_hot.shutdown()

        # Thermal agents pumps.
        if self.__wp_cold is not None:
            self.__wp_cold.shutdown()

        if self.__wp_hot is not None:
            self.__wp_hot.shutdown()

        if self.__wp_warm is not None:
            self.__wp_warm.shutdown()

        # Heat pump.
        if self.__heat_pump is not None:
            self.__heat_pump.shutdown()

#endregion
