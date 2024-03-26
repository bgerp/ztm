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

# import time
# import json
# from datetime import date
# from enum import Enum
import re

from data import verbal_const

from utils.logger import get_logger
#from utils.logic.timer import Timer
#from utils.logic.state_machine import StateMachine

from plugins.base_plugin import BasePlugin

from devices.factories.valve.valve_factory import ValveFactory
from devices.factories.pumps.pump_factory import PumpFactory
from devices.utils.valve_control_group.valve_control_group import ValveControlGroup
from devices.utils.valve_control_group.valve_control_group_mode import ValveControlGroupMode

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from data.register import Register, Scope

from .thermal_mode import ThermalMode

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

__class_name__ = "EnergyCenterDistribution"
"""Plugin class name."""

#endregion

class EnergyCenterDistribution(BasePlugin):
    """Energy center distribution control plugin."""

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, config):
        """Constructor

        Args:
            config (config): Configuration of the object.
        """

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        """Logger
        """

        self.__logger.info("Starting up the: {}".format(self.name))

        self.__state = ThermalMode.Stop
        """JUST for test.
        """

        # ====================================================================================================
        # ======================================= VCG Left door panel ========================================
        # ====================================================================================================

        self.__vcg_floor_entrance = None
        """VCG floor entrance.
        """

        self.__vcg_pool_floor = None
        """VCG pool floor.
        """

        self.__vcg_ground_drilling = None
        """Valve ground drilling.
        """

        self.__vcg_air_tower_green = None
        """VCG Air tower green.
        """

        self.__vcg_air_tower_purple = None
        """Short valve between green and purple pipes.
        """

        self.__vcg_generators = None
        """Short valve between green and purple pipes.
        """

        # ====================================================================================================
        # ======================================= VCG Right door panel =======================================
        # ====================================================================================================

        self.__vcg_pool_air_heating = None
        """VCG air heating.
        """

        self.__vcg_conv_kitchen = None
        """VCG convectors kitchen.
        """

        self.__vcg_ahu_conf_hall = None
        """VCG AHU conference hall.
        """

        self.__vcg_floor_west = None
        """VCG floor west.
        """

        self.__vcg_conv_west = None
        """VCG convectors west.
        """

        self.__vcg_ahu_roof_floor = None
        """VCG AHU roof floor.
        """

        self.__vcg_ahu_fitness = None
        """VCG AHU fitness.
        """

        self.__vcg_floor_east = None
        """VCG floor east.
        """

        self.__vcg_conv_east = None
        """VCG convectors east.
        """

        self.__vcg_pool_air_cooling = None
        """VCG air cooling.
        """

        self.__vcg_pool_heating = None
        """VCG pool heating.
        """

        # ====================================================================================================
        # ============================================== Pumps ===============================================
        # ====================================================================================================

        self.__pump_pool_air_heating = None
        """Pump air heating.
        """

        self.__pump_conv_kitchen = None
        """Pump convectors kitchen.
        """

        self.__pump_ahu_conf_hall = None
        """Pump AHU conference hall.
        """

        self.__pump_floor_west = None
        """Pump floor west.
        """

        self.__pump_conv_west = None
        """Pump convectors west.
        """

        self.__pump_ahu_roof_floor = None
        """Pump AHU roof floor.
        """

        self.__pump_ahu_fitness = None
        """Pump AHU fitness.
        """

        self.__pump_floor_east = None
        """Pump floor east.
        """

        self.__pump_conv_east = None
        """Pump convectors east.
        """

        self.__pump_pool_air_cooling = None
        """Pump air cooling.
        """

        self.__pump_pool_heating = None
        """Pump pool heating.
        """

        self.__pump_servers_cooling = None
        """Pump servers cooling.
        """

#endregion

#region Private Methods

    def __update_animations(self):
        # ====================================================================================================
        # =========================================== Test purpose ===========================================
        # ====================================================================================================

        if self.__state == ThermalMode.Stop:
            self.__state = ThermalMode.Heating

        elif self.__state == ThermalMode.Heating:
            self.__state = ThermalMode.Cooling

        elif self.__state == ThermalMode.Cooling:
            self.__state = ThermalMode.Heating

        elif self.__state == ThermalMode.Heating:
            self.__state = ThermalMode.Stop

        vcg_names = ["ecd.pool_air_heating.valves.mode", "ecd.conv_kitchen.valves.mode",
                     "ecd.ahu_conf_hall.valves.mode", "ecd.ahu_conf_hall.valves.mode",
                     "ecd.floor_west.valves.mode", "ecd.conv_west.valves.mode",
                     "ecd.ahu_roof_floor.valves.mode", "ecd.ahu_fitness.valves.mode",
                     "ecd.ahu_fitness.valves.mode", "ecd.floor_east.valves.mode",
                     "ecd.conv_east.valves.mode", "ecd.pool_air_cooling.valves.mode",
                     "ecd.pool_heating.valves.mode", "ecd.floor_entrance.valves.mode",
                     "ecd.pool_floor.valves.mode", "ecd.ground_drilling.valves.mode",
                     "ecd.air_tower_green.valves.mode", "ecd.air_tower_purple.valves.mode",
                     "ecd.generators.valves.mode"]

        for vcg_name in vcg_names:
            mode = self._registers.by_name(vcg_name)
            mode.value = self.__state.value

        mode = self._registers.by_name("ecd.pool_air_heating.pump.mode")
        if mode.value != 0:
            mode.value = 0
        elif mode.value == 0:
            mode.value = 1

        # ====================================================================================================
        # =========================================== Test purpose ===========================================
        # ====================================================================================================

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

#endregion

#region Private Methods (Registers for VCG Left door panel)

    def __vcg_floor_entrance_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_floor_entrance is not None:
                self.__vcg_floor_entrance.shutdown()
                del self.__vcg_floor_entrance

            # AHU Warehouse (RED and BLUE)
            self.__vcg_floor_entrance = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_floor_entrance is not None:
                self.__vcg_floor_entrance.init()

        elif register.value == {}:
            if self.__vcg_floor_entrance is not None:
                self.__vcg_floor_entrance.shutdown()
                del self.__vcg_floor_entrance

    def __vcg_floor_entrance_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_floor_entrance is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_floor_entrance.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_floor_entrance.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_floor_entrance.target_position = 100

    def __vcg_pool_floor_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_pool_floor is not None:
                self.__vcg_pool_floor.shutdown()
                del self.__vcg_pool_floor

            # AHU Warehouse (RED and BLUE)
            self.__vcg_pool_floor = ValveControlGroup(\
                nname=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_pool_floor is not None:
                self.__vcg_pool_floor.init()

        elif register.value == {}:
            if self.__vcg_pool_floor is not None:
                self.__vcg_pool_floor.shutdown()
                del self.__vcg_pool_floor

    def __vcg_pool_floor_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_pool_floor is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_pool_floor.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_pool_floor.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_pool_floor.target_position = 100

    def __vcg_ground_drilling_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_ground_drilling is not None:
                self.__vcg_ground_drilling.shutdown()
                del self.__vcg_ground_drilling

            # AHU Warehouse (RED and BLUE)
            self.__vcg_ground_drilling = ValveControlGroup(\
                nname=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_ground_drilling is not None:
                self.__vcg_ground_drilling.init()

        elif register.value == {}:
            if self.__vcg_ground_drilling is not None:
                self.__vcg_ground_drilling.shutdown()
                del self.__vcg_ground_drilling

    def __vcg_ground_drilling_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_ground_drilling is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_ground_drilling.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_ground_drilling.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_ground_drilling.target_position = 100

    def __vcg_air_tower_green_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_air_tower_green is not None:
                self.__vcg_air_tower_green.shutdown()
                del self.__vcg_air_tower_green

            # AHU Warehouse (RED and BLUE)
            self.__vcg_air_tower_green = ValveControlGroup(\
                nname=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_air_tower_green is not None:
                self.__vcg_air_tower_green.init()

        elif register.value == {}:
            if self.__vcg_air_tower_green is not None:
                self.__vcg_air_tower_green.shutdown()
                del self.__vcg_air_tower_green

    def __vcg_air_tower_green_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_air_tower_green is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_air_tower_green.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_air_tower_green.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_air_tower_green.target_position = 100

    def __vcg_air_tower_purple_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_air_tower_purple is not None:
                self.__vcg_air_tower_purple.shutdown()
                del self.__vcg_air_tower_purple

            # AHU Warehouse (RED and BLUE)
            self.__vcg_air_tower_purple = ValveControlGroup(\
                nname=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_air_tower_purple is not None:
                self.__vcg_air_tower_purple.init()

        elif register.value == {}:
            if self.__vcg_air_tower_purple is not None:
                self.__vcg_air_tower_purple.shutdown()
                del self.__vcg_air_tower_purple

    def __vcg_air_tower_purple_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_air_tower_purple is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_air_tower_purple.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_air_tower_purple.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_air_tower_purple.target_position = 100

    def __vcg_generators_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_generators is not None:
                self.__vcg_generators.shutdown()
                del self.__vcg_generators

            # AHU Warehouse (RED and BLUE)
            self.__vcg_generators = ValveControlGroup(\
                nname=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_generators is not None:
                self.__vcg_generators.init()

        elif register.value == {}:
            if self.__vcg_generators is not None:
                self.__vcg_generators.shutdown()
                del self.__vcg_generators

    def __vcg_generators_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_generators is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_generators.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_generators.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_generators.target_position = 100

#endregion

#region Private Methods (Registers for VCG Right door panel)

    def __vcg_pool_air_heating_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_pool_air_heating is not None:
                self.__vcg_pool_air_heating.shutdown()
                del self.__vcg_pool_air_heating

            # AHU Warehouse (RED and BLUE)
            self.__vcg_pool_air_heating = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_pool_air_heating is not None:
                self.__vcg_pool_air_heating.init()

        elif register.value == {}:
            if self.__vcg_pool_air_heating is not None:
                self.__vcg_pool_air_heating.shutdown()
                del self.__vcg_pool_air_heating

    def __vcg_pool_air_heating_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_pool_air_heating is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_pool_air_heating.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_pool_air_heating.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_pool_air_heating.target_position = 100

    def __vcg_conv_kitchen_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_conv_kitchen is not None:
                self.__vcg_conv_kitchen.shutdown()
                del self.__vcg_conv_kitchen

            # AHU Warehouse (RED and BLUE)
            self.__vcg_conv_kitchen = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_conv_kitchen is not None:
                self.__vcg_conv_kitchen.init()

        elif register.value == {}:
            if self.__vcg_conv_kitchen is not None:
                self.__vcg_conv_kitchen.shutdown()
                del self.__vcg_conv_kitchen

    def __vcg_conv_kitchen_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_conv_kitchen is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_conv_kitchen.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_conv_kitchen.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_conv_kitchen.target_position = 100

    def __vcg_ahu_conf_hall_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_ahu_conf_hall is not None:
                self.__vcg_ahu_conf_hall.shutdown()
                del self.__vcg_ahu_conf_hall

            # AHU Warehouse (RED and BLUE)
            self.__vcg_ahu_conf_hall = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_ahu_conf_hall is not None:
                self.__vcg_ahu_conf_hall.init()

        elif register.value == {}:
            if self.__vcg_ahu_conf_hall is not None:
                self.__vcg_ahu_conf_hall.shutdown()
                del self.__vcg_ahu_conf_hall

    def __vcg_ahu_conf_hall_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_ahu_conf_hall is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_ahu_conf_hall.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_ahu_conf_hall.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_ahu_conf_hall.target_position = 100

    def __vcg_floor_west_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_floor_west is not None:
                self.__vcg_floor_west.shutdown()
                del self.__vcg_floor_west

            # AHU Warehouse (RED and BLUE)
            self.__vcg_floor_west = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_floor_west is not None:
                self.__vcg_floor_west.init()

        elif register.value == {}:
            if self.__vcg_floor_west is not None:
                self.__vcg_floor_west.shutdown()
                del self.__vcg_floor_west

    def __vcg_floor_west_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_floor_west is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_floor_west.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_floor_west.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_floor_west.target_position = 100

    def __vcg_conv_west_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_conv_west is not None:
                self.__vcg_conv_west.shutdown()
                del self.__vcg_conv_west

            # AHU Warehouse (RED and BLUE)
            self.__vcg_conv_west = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_conv_west is not None:
                self.__vcg_conv_west.init()

        elif register.value == {}:
            if self.__vcg_conv_west is not None:
                self.__vcg_conv_west.shutdown()
                del self.__vcg_conv_west

    def __vcg_conv_west_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_conv_west is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_conv_west.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_conv_west.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_conv_west.target_position = 100

    def __vcg_ahu_roof_floor_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_ahu_roof_floor is not None:
                self.__vcg_ahu_roof_floor.shutdown()
                del self.__vcg_ahu_roof_floor

            # AHU Warehouse (RED and BLUE)
            self.__vcg_ahu_roof_floor = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_ahu_roof_floor is not None:
                self.__vcg_ahu_roof_floor.init()

        elif register.value == {}:
            if self.__vcg_ahu_roof_floor is not None:
                self.__vcg_ahu_roof_floor.shutdown()
                del self.__vcg_ahu_roof_floor

    def __vcg_ahu_roof_floor_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_ahu_roof_floor is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_ahu_roof_floor.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_ahu_roof_floor.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_ahu_roof_floor.target_position = 100

    def __vcg_ahu_fitness_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_ahu_fitness is not None:
                self.__vcg_ahu_fitness.shutdown()
                del self.__vcg_ahu_fitness

            # AHU Warehouse (RED and BLUE)
            self.__vcg_ahu_fitness = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_ahu_fitness is not None:
                self.__vcg_ahu_fitness.init()

        elif register.value == {}:
            if self.__vcg_ahu_fitness is not None:
                self.__vcg_ahu_fitness.shutdown()
                del self.__vcg_ahu_fitness

    def __vcg_ahu_fitness_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_ahu_fitness is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_ahu_fitness.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_ahu_fitness.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_ahu_fitness.target_position = 100

    def __vcg_floor_east_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_floor_east is not None:
                self.__vcg_floor_east.shutdown()
                del self.__vcg_floor_east

            # AHU Warehouse (RED and BLUE)
            self.__vcg_floor_east = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_floor_east is not None:
                self.__vcg_floor_east.init()

        elif register.value == {}:
            if self.__vcg_floor_east is not None:
                self.__vcg_floor_east.shutdown()
                del self.__vcg_floor_east

    def __vcg_floor_east_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_floor_east is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_floor_east.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_floor_east.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_floor_east.target_position = 100

    def __vcg_conv_east_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_conv_east is not None:
                self.__vcg_conv_east.shutdown()
                del self.__vcg_conv_east

            # AHU Warehouse (RED and BLUE)
            self.__vcg_conv_east = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_conv_east is not None:
                self.__vcg_conv_east.init()

        elif register.value == {}:
            if self.__vcg_conv_east is not None:
                self.__vcg_conv_east.shutdown()
                del self.__vcg_conv_east

    def __vcg_conv_east_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_conv_east is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_conv_east.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_conv_east.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_conv_east.target_position = 100

    def __vcg_pool_air_cooling_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_pool_air_cooling is not None:
                self.__vcg_pool_air_cooling.shutdown()
                del self.__vcg_pool_air_cooling

            # AHU Warehouse (RED and BLUE)
            self.__vcg_pool_air_cooling = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_pool_air_cooling is not None:
                self.__vcg_pool_air_cooling.init()

        elif register.value == {}:
            if self.__vcg_pool_air_cooling is not None:
                self.__vcg_pool_air_cooling.shutdown()
                del self.__vcg_pool_air_cooling

    def __vcg_pool_air_cooling_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_pool_air_cooling is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_pool_air_cooling.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_pool_air_cooling.target_position = 100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_pool_air_cooling.target_position = -100

    def __vcg_pool_heating_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_pool_heating is not None:
                self.__vcg_pool_heating.shutdown()
                del self.__vcg_pool_heating

            # AHU Warehouse (RED and BLUE)
            self.__vcg_pool_heating = ValveControlGroup(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_pool_heating is not None:
                self.__vcg_pool_heating.init()

        elif register.value == {}:
            if self.__vcg_pool_heating is not None:
                self.__vcg_pool_heating.shutdown()
                del self.__vcg_pool_heating

    def __vcg_pool_heating_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_pool_heating is None:
            return

        if register.value == ThermalMode.Stop.value:
            self.__vcg_pool_heating.target_position = 0
        elif register.value == ThermalMode.Cooling.value:
            self.__vcg_pool_heating.target_position = -100
        elif register.value == ThermalMode.Heating.value:
            self.__vcg_pool_heating.target_position = 100

#endregion

#region Private Methods (Registers for Pumps)

    def __pump_pool_air_heating_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_pool_air_heating is not None:
                self.__pump_pool_air_heating.shutdown()
                del self.__pump_pool_air_heating

            self.__pump_pool_air_heating = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_pool_air_heating is not None:
                self.__pump_pool_air_heating.init()

        elif register.value == {}:
            if self.__pump_pool_air_heating is not None:
                self.__pump_pool_air_heating.shutdown()
                del self.__pump_pool_air_heating

    def __pump_pool_air_heating_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_pool_air_heating is None:
            return

        self.__pump_pool_air_heating.e_stop(register.value)

    def __pump_conv_kitchen_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_conv_kitchen is not None:
                self.__pump_conv_kitchen.shutdown()
                del self.__pump_conv_kitchen

            self.__pump_conv_kitchen = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_conv_kitchen is not None:
                self.__pump_conv_kitchen.init()

        elif register.value == {}:
            if self.__pump_conv_kitchen is not None:
                self.__pump_conv_kitchen.shutdown()
                del self.__pump_conv_kitchen

    def __pump_conv_kitchen_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_conv_kitchen is None:
            return

        self.__pump_conv_kitchen.e_stop(register.value)

    def __pump_ahu_conf_hall_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_ahu_conf_hall is not None:
                self.__pump_ahu_conf_hall.shutdown()
                del self.__pump_ahu_conf_hall

            self.__pump_ahu_conf_hall = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_ahu_conf_hall is not None:
                self.__pump_ahu_conf_hall.init()

        elif register.value == {}:
            if self.__pump_ahu_conf_hall is not None:
                self.__pump_ahu_conf_hall.shutdown()
                del self.__pump_ahu_conf_hall

    def __pump_ahu_conf_hall_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_ahu_conf_hall is None:
            return

        self.__pump_ahu_conf_hall.e_stop(register.value)

    def __pump_floor_west_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_floor_west is not None:
                self.__pump_floor_west.shutdown()
                del self.__pump_floor_west

            self.__pump_floor_west = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_floor_west is not None:
                self.__pump_floor_west.init()

        elif register.value == {}:
            if self.__pump_floor_west is not None:
                self.__pump_floor_west.shutdown()
                del self.__pump_floor_west

    def __pump_floor_west_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_floor_west is None:
            return

        self.__pump_floor_west.e_stop(register.value)

    def __pump_conv_west_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_conv_west is not None:
                self.__pump_conv_west.shutdown()
                del self.__pump_conv_west

            self.__pump_conv_west = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_conv_west is not None:
                self.__pump_conv_west.init()

        elif register.value == {}:
            if self.__pump_conv_west is not None:
                self.__pump_conv_west.shutdown()
                del self.__pump_conv_west

    def __pump_conv_west_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_conv_west is None:
            return

        self.__pump_conv_west.e_stop(register.value)

    def __pump_ahu_roof_floor_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_ahu_roof_floor is not None:
                self.__pump_ahu_roof_floor.shutdown()
                del self.__pump_ahu_roof_floor

            self.__pump_ahu_roof_floor = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_ahu_roof_floor is not None:
                self.__pump_ahu_roof_floor.init()

        elif register.value == {}:
            if self.__pump_ahu_roof_floor is not None:
                self.__pump_ahu_roof_floor.shutdown()
                del self.__pump_ahu_roof_floor

    def __pump_ahu_roof_floor_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_ahu_roof_floor is None:
            return

        self.__pump_ahu_roof_floor.e_stop(register.value)

    def __pump_ahu_fitness_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_ahu_fitness is not None:
                self.__pump_ahu_fitness.shutdown()
                del self.__pump_ahu_fitness

            self.__pump_ahu_fitness = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_ahu_fitness is not None:
                self.__pump_ahu_fitness.init()

        elif register.value == {}:
            if self.__pump_ahu_fitness is not None:
                self.__pump_ahu_fitness.shutdown()
                del self.__pump_ahu_fitness

    def __pump_ahu_fitness_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_ahu_fitness is None:
            return

        self.__pump_ahu_fitness.e_stop(register.value)

    def __pump_floor_east_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_floor_east is not None:
                self.__pump_floor_east.shutdown()
                del self.__pump_floor_east

            self.__pump_floor_east = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_floor_east is not None:
                self.__pump_floor_east.init()

        elif register.value == {}:
            if self.__pump_floor_east is not None:
                self.__pump_floor_east.shutdown()
                del self.__pump_floor_east

    def __pump_floor_east_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_floor_east is None:
            return

        self.__pump_floor_east.e_stop(register.value)

    def __pump_conv_east_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_conv_east is not None:
                self.__pump_conv_east.shutdown()
                del self.__pump_conv_east

            self.__pump_conv_east = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_conv_east is not None:
                self.__pump_conv_east.init()

        elif register.value == {}:
            if self.__pump_conv_east is not None:
                self.__pump_conv_east.shutdown()
                del self.__pump_conv_east

    def __pump_conv_east_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_conv_east is None:
            return

        self.__pump_conv_east.e_stop(register.value)

    def __pump_pool_air_cooling_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_pool_air_cooling is not None:
                self.__pump_pool_air_cooling.shutdown()
                del self.__pump_pool_air_cooling

            self.__pump_pool_air_cooling = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_pool_air_cooling is not None:
                self.__pump_pool_air_cooling.init()

        elif register.value == {}:
            if self.__pump_pool_air_cooling is not None:
                self.__pump_pool_air_cooling.shutdown()
                del self.__pump_pool_air_cooling

    def __pump_pool_air_cooling_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_pool_air_cooling is None:
            return

        self.__pump_pool_air_cooling.e_stop(register.value)

    def __pump_pool_heating_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_pool_heating is not None:
                self.__pump_pool_heating.shutdown()
                del self.__pump_pool_heating

            self.__pump_pool_heating = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_pool_heating is not None:
                self.__pump_pool_heating.init()

        elif register.value == {}:
            if self.__pump_pool_heating is not None:
                self.__pump_pool_heating.shutdown()
                del self.__pump_pool_heating

    def __pump_pool_heating_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_pool_heating is None:
            return

        self.__pump_pool_heating.e_stop(register.value)

    def __pump_servers_cooling_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__pump_servers_cooling is not None:
                self.__pump_servers_cooling.shutdown()
                del self.__pump_servers_cooling

            self.__pump_servers_cooling = PumpFactory.create(\
                name=register.description,
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__pump_servers_cooling is not None:
                self.__pump_servers_cooling.init()

        elif register.value == {}:
            if self.__pump_servers_cooling is not None:
                self.__pump_servers_cooling.shutdown()
                del self.__pump_servers_cooling

    def __pump_servers_cooling_mode_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if not ThermalMode.is_valid(register.value):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__pump_servers_cooling is None:
            return

        self.__pump_servers_cooling.e_stop(register.value)

#endregion

#region Private Methods (Registers)

    def __init_registers(self):

        # ====================================================================================================
        # ======================================= VCG Left door panel ========================================
        # ====================================================================================================

        self.__attach_vcg("floor_entrance",
                                    self.__vcg_floor_entrance_settings_cb,
                                    self.__vcg_floor_entrance_mode_cb)

        self.__attach_vcg("pool_floor",
                                    self.__vcg_pool_floor_settings_cb,
                                    self.__vcg_pool_floor_mode_cb)

        self.__attach_vcg("ground_drilling",
                                    self.__vcg_ground_drilling_settings_cb,
                                    self.__vcg_ground_drilling_mode_cb)

        self.__attach_vcg("air_tower_green",
                                    self.__vcg_air_tower_green_settings_cb,
                                    self.__vcg_air_tower_green_mode_cb)

        self.__attach_vcg("air_tower_purple",
                                    self.__vcg_air_tower_purple_settings_cb,
                                    self.__vcg_air_tower_purple_mode_cb)

        self.__attach_vcg("generators",
                                    self.__vcg_generators_settings_cb,
                                    self.__vcg_generators_mode_cb)

        # ====================================================================================================
        # ======================================= VCG Right door panel =======================================
        # ====================================================================================================

        self.__attach_vcg("pool_air_heating",
                                    self.__vcg_pool_air_heating_settings_cb,
                                    self.__vcg_pool_air_heating_mode_cb)

        self.__attach_vcg("conv_kitchen",
                                    self.__vcg_conv_kitchen_settings_cb,
                                    self.__vcg_conv_kitchen_mode_cb)

        self.__attach_vcg("ahu_conf_hall",
                                    self.__vcg_ahu_conf_hall_settings_cb,
                                    self.__vcg_ahu_conf_hall_mode_cb)

        self.__attach_vcg("floor_west",
                                    self.__vcg_floor_west_settings_cb,
                                    self.__vcg_floor_west_mode_cb)

        self.__attach_vcg("conv_west",
                                    self.__vcg_conv_west_settings_cb,
                                    self.__vcg_conv_west_mode_cb)

        self.__attach_vcg("ahu_roof_floor",
                                    self.__vcg_ahu_roof_floor_settings_cb,
                                    self.__vcg_ahu_roof_floor_mode_cb)

        self.__attach_vcg("ahu_fitness",
                                    self.__vcg_ahu_fitness_settings_cb,
                                    self.__vcg_ahu_fitness_mode_cb)

        self.__attach_vcg("floor_east",
                                    self.__vcg_floor_east_settings_cb,
                                    self.__vcg_floor_east_mode_cb)

        self.__attach_vcg("conv_east",
                                    self.__vcg_conv_east_settings_cb,
                                    self.__vcg_conv_east_mode_cb)

        self.__attach_vcg("pool_air_cooling",
                                    self.__vcg_pool_air_cooling_settings_cb,
                                    self.__vcg_pool_air_cooling_mode_cb)

        self.__attach_vcg("pool_heating",
                                    self.__vcg_pool_heating_settings_cb,
                                    self.__vcg_pool_heating_mode_cb)

        # ====================================================================================================
        # ============================================== Pumps ===============================================
        # ====================================================================================================

        self.__attach_pump("pool_air_heating",
                                    self.__pump_pool_air_heating_settings_cb,
                                    self.__pump_pool_air_heating_mode_cb)

        self.__attach_pump("conv_kitchen",
                                    self.__pump_conv_kitchen_settings_cb,
                                    self.__pump_conv_kitchen_mode_cb)

        self.__attach_pump("ahu_conf_hall",
                                    self.__pump_ahu_conf_hall_settings_cb,
                                    self.__pump_ahu_conf_hall_mode_cb)

        self.__attach_pump("floor_west",
                                    self.__pump_floor_west_settings_cb,
                                    self.__pump_floor_west_mode_cb)

        self.__attach_pump("conv_west",
                                    self.__pump_conv_west_settings_cb,
                                    self.__pump_conv_west_mode_cb)

        self.__attach_pump("ahu_roof_floor",
                                    self.__pump_ahu_roof_floor_settings_cb,
                                    self.__pump_ahu_roof_floor_mode_cb)

        self.__attach_pump("ahu_fitness",
                                    self.__pump_ahu_fitness_settings_cb,
                                    self.__pump_ahu_fitness_mode_cb)

        self.__attach_pump("floor_east",
                                    self.__pump_floor_east_settings_cb,
                                    self.__pump_floor_east_mode_cb)

        self.__attach_pump("conv_east",
                                    self.__pump_conv_east_settings_cb,
                                    self.__pump_conv_east_mode_cb)

        self.__attach_pump("pool_air_cooling",
                                    self.__pump_pool_air_cooling_settings_cb,
                                    self.__pump_pool_air_cooling_mode_cb)

        self.__attach_pump("pool_heating",
                                    self.__pump_pool_heating_settings_cb,
                                    self.__pump_pool_heating_mode_cb)

        self.__attach_pump("servers_cooling",
                                    self.__pump_servers_cooling_settings_cb,
                                    self.__pump_servers_cooling_mode_cb)

#endregion

#region Protected Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__init_registers()

    def _update(self):
        """Update the plugin.
        """

        # self.__update_animations()

        # ====================================================================================================
        # ======================================= VCG Left door panel ========================================
        # ====================================================================================================

        if self.__vcg_floor_entrance is not None:
            self.__vcg_floor_entrance.update()
            reg_state = self._registers.by_name("ecd.floor_entrance.valves.state")
            if reg_state is not None:
                if self.__vcg_floor_entrance.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_floor_entrance.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_floor_entrance.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_pool_floor is not None:
            self.__vcg_pool_floor.update()
            reg_state = self._registers.by_name("ecd.pool_floor.valves.state")
            if reg_state is not None:
                if self.__vcg_pool_floor.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_pool_floor.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_pool_floor.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_ground_drilling is not None:
            self.__vcg_ground_drilling.update()
            reg_state = self._registers.by_name("ecd.ground_drilling.valves.state")
            if reg_state is not None:
                if self.__vcg_ground_drilling.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_ground_drilling.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_ground_drilling.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_air_tower_green is not None:
            self.__vcg_air_tower_green.update()
            reg_state = self._registers.by_name("ecd.air_tower_green.valves.state")
            if reg_state is not None:
                if self.__vcg_air_tower_green.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_air_tower_green.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_air_tower_green.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_air_tower_purple is not None:
            self.__vcg_air_tower_purple.update()
            reg_state = self._registers.by_name("ecd.air_tower_purple.valves.state")
            if reg_state is not None:
                if self.__vcg_air_tower_purple.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_air_tower_purple.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_air_tower_purple.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_generators is not None:
            self.__vcg_generators.update()
            reg_state = self._registers.by_name("ecd.generators.valves.state")
            if reg_state is not None:
                if self.__vcg_generators.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_generators.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_generators.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        # ====================================================================================================
        # ======================================= VCG Right door panel =======================================
        # ====================================================================================================

        if self.__vcg_pool_air_heating is not None:
            self.__vcg_pool_air_heating.update()
            reg_state = self._registers.by_name("ecd.pool_air_heating.valves.state")
            if reg_state is not None:
                if self.__vcg_pool_air_heating.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_pool_air_heating.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_pool_air_heating.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_conv_kitchen is not None:
            self.__vcg_conv_kitchen.update()
            reg_state = self._registers.by_name("ecd.conv_kitchen.valves.state")
            if reg_state is not None:
                if self.__vcg_conv_kitchen.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_conv_kitchen.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_conv_kitchen.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_ahu_conf_hall is not None:
            self.__vcg_ahu_conf_hall.update()
            reg_state = self._registers.by_name("ecd.ahu_conf_hall.valves.state")
            if reg_state is not None:
                if self.__vcg_ahu_conf_hall.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_ahu_conf_hall.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_ahu_conf_hall.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_floor_west is not None:
            self.__vcg_floor_west.update()
            reg_state = self._registers.by_name("ecd.floor_west.valves.state")
            if reg_state is not None:
                if self.__vcg_floor_west.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_floor_west.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_floor_west.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_conv_west is not None:
            self.__vcg_conv_west.update()
            reg_state = self._registers.by_name("ecd.conv_west.valves.state")
            if reg_state is not None:
                if self.__vcg_conv_west.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_conv_west.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_conv_west.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_ahu_roof_floor is not None:
            self.__vcg_ahu_roof_floor.update()
            reg_state = self._registers.by_name("ecd.ahu_roof_floor.valves.state")
            if reg_state is not None:
                if self.__vcg_conv_west.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_conv_west.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_conv_west.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_ahu_fitness is not None:
            self.__vcg_ahu_fitness.update()
            reg_state = self._registers.by_name("ecd.ahu_fitness.valves.state")
            if reg_state is not None:
                if self.__vcg_ahu_fitness.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_ahu_fitness.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_ahu_fitness.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_floor_east is not None:
            self.__vcg_floor_east.update()
            reg_state = self._registers.by_name("ecd.floor_east.valves.state")
            if reg_state is not None:
                if self.__vcg_floor_east.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_floor_east.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_floor_east.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_conv_east is not None:
            self.__vcg_conv_east.update()
            reg_state = self._registers.by_name("ecd.conv_east.valves.state")
            if reg_state is not None:
                if self.__vcg_conv_east.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_conv_east.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_conv_east.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_pool_air_cooling is not None:
            self.__vcg_pool_air_cooling.update()
            reg_state = self._registers.by_name("ecd.pool_air_cooling.valves.state")
            if reg_state is not None:
                if self.__vcg_pool_air_cooling.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_pool_air_cooling.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_pool_air_cooling.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        if self.__vcg_pool_heating is not None:
            self.__vcg_pool_heating.update()
            reg_state = self._registers.by_name("ecd.pool_heating.valves.state")
            if reg_state is not None:
                if self.__vcg_pool_heating.target_position == 0:
                    reg_state.value = ThermalMode.Stop.value
                elif self.__vcg_pool_heating.target_position < 0:
                    reg_state.value = ThermalMode.Cooling.value
                elif self.__vcg_pool_heating.target_position > 0:
                    reg_state.value = ThermalMode.Heating.value

        # ====================================================================================================
        # ============================================== Pumps ===============================================
        # ====================================================================================================
        if self.__pump_pool_air_heating is not None:
            self.__pump_pool_air_heating.update()
            reg_state = self._registers.by_name("ecd.pool_air_heating.pump.state")
            if reg_state is not None:
                e_status = self.__pump_pool_air_heating.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_conv_kitchen is not None:
            self.__pump_conv_kitchen.update()
            reg_state = self._registers.by_name("ecd.conv_kitchen.pump.state")
            if reg_state is not None:
                e_status = self.__pump_conv_kitchen.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_ahu_conf_hall is not None:
            self.__pump_ahu_conf_hall.update()
            reg_state = self._registers.by_name("ecd.ahu_conf_hall.pump.state")
            if reg_state is not None:
                e_status = self.__pump_ahu_conf_hall.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_floor_west is not None:
            self.__pump_floor_west.update()
            reg_state = self._registers.by_name("ecd.floor_west.pump.state")
            if reg_state is not None:
                e_status = self.__pump_floor_west.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_conv_west is not None:
            self.__pump_conv_west.update()
            reg_state = self._registers.by_name("ecd.conv_west.pump.state")
            if reg_state is not None:
                e_status = self.__pump_conv_west.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_ahu_roof_floor is not None:
            self.__pump_ahu_roof_floor.update()
            reg_state = self._registers.by_name("ecd.ahu_roof_floor.pump.state")
            if reg_state is not None:
                e_status = self.__pump_ahu_roof_floor.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_ahu_fitness is not None:
            self.__pump_ahu_fitness.update()
            reg_state = self._registers.by_name("ecd.ahu_fitness.pump.state")
            if reg_state is not None:
                e_status = self.__pump_ahu_fitness.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_floor_east is not None:
            self.__pump_floor_east.update()
            reg_state = self._registers.by_name("ecd.floor_east.pump.state")
            if reg_state is not None:
                e_status = self.__pump_floor_east.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_conv_east is not None:
            self.__pump_conv_east.update()
            reg_state = self._registers.by_name("ecd.conv_east.pump.state")
            if reg_state is not None:
                e_status = self.__pump_conv_east.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_pool_air_cooling is not None:
            self.__pump_pool_air_cooling.update()
            reg_state = self._registers.by_name("ecd.pool_air_cooling.pump.state")
            if reg_state is not None:
                e_status = self.__pump_pool_air_cooling.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_pool_heating is not None:
            self.__pump_pool_heating.update()
            reg_state = self._registers.by_name("ecd.pool_heating.pump.state")
            if reg_state is not None:
                e_status = self.__pump_pool_heating.e_status()
                reg_state.value = {"e_status" : e_status}

        if self.__pump_servers_cooling is not None:
            self.__pump_servers_cooling.update()
            reg_state = self._registers.by_name("ecd.servers_cooling.pump.state")
            if reg_state is not None:
                e_status = self.__pump_servers_cooling.e_status()
                reg_state.value = {"e_status" : e_status}

        ztm_regs = self._registers.by_scope(Scope.Device)
        pat = re.compile(r"(ecd\.)(.+?)(\.state)")
        # pat = re.compile(r"(ecd\.)(generators\.valves)(\.state)")
        for register in ztm_regs:
            match = pat.match(register.name)
            if match:
                print(f"{register.name}: {register.value}")


    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

        # ====================================================================================================
        # ======================================= VCG Left door panel ========================================
        # ====================================================================================================

        if self.__vcg_floor_entrance is not None:
            self.__vcg_floor_entrance.shutdown()

        if self.__vcg_pool_floor is not None:
            self.__vcg_pool_floor.shutdown()

        if self.__vcg_ground_drilling is not None:
            self.__vcg_ground_drilling.shutdown()

        if self.__vcg_air_tower_green is not None:
            self.__vcg_air_tower_green.shutdown()

        if self.__vcg_air_tower_purple is not None:
            self.__vcg_air_tower_purple.shutdown()

        if self.__vcg_generators is not None:
            self.__vcg_generators.shutdown()

        # ====================================================================================================
        # ======================================= VCG Right door panel =======================================
        # ====================================================================================================

        if self.__vcg_pool_air_heating is not None:
            self.__vcg_pool_air_heating.shutdown()

        if self.__vcg_conv_kitchen is not None:
            self.__vcg_conv_kitchen.shutdown()

        if self.__vcg_ahu_conf_hall is not None:
            self.__vcg_ahu_conf_hall.shutdown()

        if self.__vcg_floor_west is not None:
            self.__vcg_floor_west.shutdown()

        if self.__vcg_conv_west is not None:
            self.__vcg_conv_west.shutdown()

        if self.__vcg_ahu_roof_floor is not None:
            self.__vcg_ahu_roof_floor.shutdown()

        if self.__vcg_ahu_fitness is not None:
            self.__vcg_ahu_fitness.shutdown()

        if self.__vcg_floor_east is not None:
            self.__vcg_floor_east.shutdown()

        if self.__vcg_conv_east is not None:
            self.__vcg_conv_east.shutdown()

        if self.__vcg_pool_air_cooling is not None:
            self.__vcg_pool_air_cooling.shutdown()

        if self.__vcg_pool_heating is not None:
            self.__vcg_pool_heating.shutdown()

        # ====================================================================================================
        # ============================================== Pumps ===============================================
        # ====================================================================================================

        if self.__pump_pool_air_heating is not None:
            self.__pump_pool_air_heating.shutdown()

        if self.__pump_conv_kitchen is not None:
            self.__pump_conv_kitchen.shutdown()

        if self.__pump_ahu_conf_hall is not None:
            self.__pump_ahu_conf_hall.shutdown()

        if self.__pump_floor_west is not None:
            self.__pump_floor_west.shutdown()

        if self.__pump_conv_west is not None:
            self.__pump_conv_west.shutdown()

        if self.__pump_ahu_roof_floor is not None:
            self.__pump_ahu_roof_floor.shutdown()

        if self.__pump_ahu_fitness is not None:
            self.__pump_ahu_fitness.shutdown()

        if self.__pump_floor_east is not None:
            self.__pump_floor_east.shutdown()

        if self.__pump_conv_east is not None:
            self.__pump_conv_east.shutdown()

        if self.__pump_pool_air_cooling is not None:
            self.__pump_pool_air_cooling.shutdown()

        if self.__pump_pool_heating is not None:
            self.__pump_pool_heating.shutdown()

        if self.__pump_pool_air_heating is not None:
            self.__pump_pool_air_heating.shutdown()

        if self.__pump_servers_cooling is not None:
            self.__pump_servers_cooling.shutdown()

#endregion
