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

from data import verbal_const

from utils.logger import get_logger
#from utils.logic.timer import Timer
#from utils.logic.state_machine import StateMachine

from plugins.base_plugin import BasePlugin

from devices.factories.valve.valve_factory import ValveFactory
from devices.utils.valve_control_group.valve_control_group import ValveControlGroup
from devices.utils.valve_control_group.valve_control_group_mode import ValveControlGroupMode

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from data.register import Register

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

        self.__vcg_pool_air_heating = None
        """VCG TVA warhorse.
        """

        self.__vcg_conv_kitchen = None
        """VCG Convectors kitchen.
        """

        self.__vcg_ahu_conf_hall = None
        """VCG AHU conference hall.
        """

        self.__vcg_floor_west = None
        """VCG Floor west.
        """

        self.__vcg_conv_west = None
        """VCG Convectors west.
        """

        self.__vcg_ahu_roof_floor = None
        """VCG AHU roof floor.
        """

        self.__vcg_ahu_fitness = None
        """VCG AHU fitness.
        """

        # self.__v_underfloor_heating_foyer = None
        # """Valve foyer.
        # """

        # self.__v_underfloor_heating_trestle = None
        # """Underfloor heating trestle.
        # """

        # self.__v_underfloor_heating_pool = None
        # """Underfloor heating pool.
        # """

        # self.__v_air_cooling = None
        # """Valve air cooling.
        # """

        # self.__v_ground_drill = None
        # """Valve ground drilling.
        # """

        # self.__v_generators_cooling = None
        # """Generators cooling.
        # """

        # self.__v_short_green_purple = None
        # """Short valve between green and purple pipes.
        # """

        # self.__v_underfloor_west_bypass = None
        # """Valve underfloor west bypass.
        # """

        # self.__v_underfloor_east_bypass = None
        # """Valve underfloor east bypass.
        # """

        # self.__pool_heating = None
        # """VCG Pool heating.
        # """

        # self.__tva_pool = None
        # """VCG TVA pool.
        # """

        # self.__convectors_east = None
        # """VCG Convectors east.
        # """

        # self.__underfloor_east = None
        # """VCG Underfloor east.
        # """

        # self.__convectors_west = None
        # """VCG Convectors west.
        # """

        # self.__tva_fitness = None
        # """VCG TVA fitness.
        # """

        # self.__tva_roof_floor = None
        # """VCG TVA roof floor.
        # """

        # self.__underfloor_west = None
        # """VCG Underfloor west.
        # """

        # self.__tva_conference_center = None
        # """VCG TVA conference centre.
        # """

#endregion

#region Private Methods (Registers)

    def __attach_valve(self, valve_name: str, settings_cb, mode_cb):
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

    def __pool_air_heating_settings_cb(self, register: Register):

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
                name="VCG pool air heating",
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

    def __pool_air_heating_mode_cb(self, register: Register):

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

    def __conv_kitchen_settings_cb(self, register: Register):

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
                name="VCG convectors kitchen",
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

    def __conv_kitchen_mode_cb(self, register: Register):

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

    def __ahu_conf_hall_settings_cb(self, register: Register):

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
                name="VCG AHU conference hall",
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

    def __ahu_conf_hall_mode_cb(self, register: Register):

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

    def __floor_west_settings_cb(self, register: Register):

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
                name="VCG AHU conference hall",
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

    def __floor_west_mode_cb(self, register: Register):

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

    def __conv_west_settings_cb(self, register: Register):

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
                name="VCG Convectors west",
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

    def __conv_west_mode_cb(self, register: Register):

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

    def __ahu_roof_floor_settings_cb(self, register: Register):

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
                name="VCG Convectors west",
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

    def __ahu_roof_floor_mode_cb(self, register: Register):

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

    def __ahu_fitness_settings_cb(self, register: Register):

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
                name="VCG Convectors west",
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

    def __ahu_fitness_mode_cb(self, register: Register):

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


    def __init_registers(self):

        # -=== Left Side Valves ===-

        # self.__attach_valve("floor_entrance",
        #                            self.__floor_entrance_settings_cb,
        #                            self.__floor_entrance_mode_cb)

        # self.__attach_valve("drilling",
        #                            self.__drilling_settings_cb,
        #                            self.__drilling_mode_cb)

        # self.__attach_valve("floor_pool",
        #                            self.__floor_pool_settings_cb,
        #                            self.__floor_pool_mode_cb)

        # self.__attach_valve("air_tower_green",
        #                            self.__air_tower_green_settings_cb,
        #                            self.__air_tower_green_mode_cb)

        # self.__attach_valve("air_tower_purple",
        #                            self.__air_tower_purple_settings_cb,
        #                            self.__air_tower_purple_mode_cb)

        # self.__attach_valve("generators",
        #                            self.__generators_settings_cb,
        #                            self.__generators_mode_cb)

        # -=== Right Side Valves ===-

        self.__attach_valve("pool_air_heating",
                                   self.__pool_air_heating_settings_cb,
                                   self.__pool_air_heating_mode_cb)

        self.__attach_valve("conv_kitchen",
                                   self.__conv_kitchen_settings_cb,
                                   self.__conv_kitchen_mode_cb)

        self.__attach_valve("ahu_conf_hall",
                                   self.__ahu_conf_hall_settings_cb,
                                   self.__ahu_conf_hall_mode_cb)

        self.__attach_valve("floor_west",
                                   self.__floor_west_settings_cb,
                                   self.__floor_west_mode_cb)

        self.__attach_valve("conv_west",
                                   self.__conv_west_settings_cb,
                                   self.__conv_west_mode_cb)

        self.__attach_valve("ahu_roof_floor",
                                   self.__ahu_roof_floor_settings_cb,
                                   self.__ahu_roof_floor_mode_cb)

        self.__attach_valve("ahu_fitness",
                                   self.__ahu_fitness_settings_cb,
                                   self.__ahu_fitness_mode_cb)

        # self.__attach_valve("floor_east",
        #                            self.__floor_east_settings_cb,
        #                            self.__floor_east_mode_cb)

        # self.__attach_valve("conv_east",
        #                            self.__conv_east_settings_cb,
        #                            self.__conv_east_mode_cb)

        # self.__attach_valve("pool_drying",
        #                            self.__pool_drying_settings_cb,
        #                            self.__pool_drying_mode_cb)

        # self.__attach_valve("pool_heating",
        #                            self.__pool_heating_settings_cb,
        #                            self.__pool_heating_mode_cb)

#endregion

#region Properties

#endregion

#region Protected Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__init_registers()

    def _update(self):
        """Update the plugin.
        """

        if self.__state == ThermalMode.Stop:
            self.__state = ThermalMode.Heating

        elif self.__state == ThermalMode.Heating:
            self.__state = ThermalMode.Cooling

        elif self.__state == ThermalMode.Cooling:
            self.__state = ThermalMode.Heating

        elif self.__state == ThermalMode.Heating:
            self.__state = ThermalMode.Stop

        mode = self._registers.by_name("ecd.pool_air_heating.valves.mode")
        mode.value = self.__state.value

        if self.__vcg_pool_air_heating is not None:
            self.__vcg_pool_air_heating.update()

        mode = self._registers.by_name("ecd.conv_kitchen.valves.mode")
        mode.value = self.__state.value

        if self.__vcg_conv_kitchen is not None:
            self.__vcg_conv_kitchen.update()

        mode = self._registers.by_name("ecd.ahu_conf_hall.valves.mode")
        mode.value = self.__state.value

        if self.__vcg_ahu_conf_hall is not None:
            self.__vcg_ahu_conf_hall.update()

        mode = self._registers.by_name("ecd.floor_west.valves.mode")
        mode.value = self.__state.value

        if self.__vcg_floor_west is not None:
            self.__vcg_floor_west.update()

        mode = self._registers.by_name("ecd.conv_west.valves.mode")
        mode.value = self.__state.value

        if self.__vcg_conv_west is not None:
            self.__vcg_conv_west.update()

        mode = self._registers.by_name("ecd.ahu_roof_floor.valves.mode")
        mode.value = self.__state.value

        if self.__vcg_ahu_roof_floor is not None:
            self.__vcg_ahu_roof_floor.update()

        mode = self._registers.by_name("ecd.ahu_fitness.valves.mode")
        mode.value = self.__state.value

        if self.__vcg_ahu_fitness is not None:
            self.__vcg_ahu_fitness.update()


        # if self.__v_underfloor_heating_foyer is not None:
        #     self.__v_underfloor_heating_foyer.update()

        # if self.__v_underfloor_heating_trestle is not None:
        #     self.__v_underfloor_heating_trestle.update()

        # if self.__v_underfloor_heating_pool is not None:
        #     self.__v_underfloor_heating_pool.update()

        # if self.__v_air_cooling is not None:
        #     self.__v_air_cooling.update()

        # if self.__v_ground_drill is not None:
        #     self.__v_ground_drill.update()

        # if self.__v_generators_cooling is not None:
        #     self.__v_generators_cooling.update()

        # if self.__v_short_green_purple is not None:
        #     self.__v_short_green_purple.update()

        # if self.__v_underfloor_west_bypass is not None:
        #     self.__v_underfloor_west_bypass.update()

        # if self.__v_underfloor_east_bypass is not None:
        #     self.__v_underfloor_east_bypass.update()

        # if self.__pool_heating is not None:
        #     self.__pool_heating.update()

        # if self.__tva_pool is not None:
        #     self.__tva_pool.update()

        # if self.__convectors_east is not None:
        #     self.__convectors_east.update()

        # if self.__underfloor_east is not None:
        #     self.__underfloor_east.update()

        # if self.__convectors_west is not None:
        #     self.__convectors_west.update()

        # if self.__tva_fitness is not None:
        #     self.__tva_fitness.update()

        # if self.__tva_roof_floor is not None:
        #     self.__tva_roof_floor.update()

        # if self.__underfloor_west is not None:
        #     self.__underfloor_west.update()

        # if self.__tva_conference_center is not None:
        #     self.__tva_conference_center.update()



    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

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


        # if self.__v_underfloor_heating_foyer is not None:
        #     self.__v_underfloor_heating_foyer.shutdown()

        # if self.__v_underfloor_heating_trestle is not None:
        #     self.__v_underfloor_heating_trestle.shutdown()

        # if self.__v_underfloor_heating_pool is not None:
        #     self.__v_underfloor_heating_pool.shutdown()

        # if self.__v_air_cooling is not None:
        #     self.__v_air_cooling.shutdown()

        # if self.__v_ground_drill is not None:
        #     self.__v_ground_drill.shutdown()

        # if self.__v_generators_cooling is not None:
        #     self.__v_generators_cooling.shutdown()

        # if self.__v_short_green_purple is not None:
        #     self.__v_short_green_purple.shutdown()

        # if self.__v_underfloor_west_bypass is not None:
        #     self.__v_underfloor_west_bypass.shutdown()

        # if self.__v_underfloor_east_bypass is not None:
        #     self.__v_underfloor_east_bypass.shutdown()

        # if self.__pool_heating is not None:
        #     self.__pool_heating.shutdown()

        # if self.__tva_pool is not None:
        #     self.__tva_pool.shutdown()

        # if self.__convectors_east is not None:
        #     self.__convectors_east.shutdown()

        # if self.__underfloor_east is not None:
        #     self.__underfloor_east.shutdown()

        # if self.__convectors_west is not None:
        #     self.__convectors_west.shutdown()

        # if self.__tva_fitness is not None:
        #     self.__tva_fitness.shutdown()

        # if self.__tva_roof_floor is not None:
        #     self.__tva_roof_floor.shutdown()

        # if self.__underfloor_west is not None:
        #     self.__underfloor_west.shutdown()

        # if self.__tva_conference_center is not None:
        #     self.__tva_conference_center.shutdown()



#endregion
