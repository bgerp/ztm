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

        self.__vcg_ahu_warehouse = None
        """VCG TVA warhorse.
        """

        self.__state = 0


        # self.__convectors_kitchen = None
        # """VCG Convectors kitchen.
        # """

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

    def __attach_valve(self, valve_name: str, settings_cb, position_cb):
        """Attach valve callbacks.

        Args:
            valve_name (str): Name of the valve.
            settings_cb ([type]): Enable callback.
            position_cb ([type]): Position callback.
        """

        # Generators cooling valve settings.
        reg_name = f"{self.key}.{valve_name}.valve.settings"
        settings = self._registers.by_name(reg_name)
        if settings is not None:
            settings.update_handlers = settings_cb
            settings.update()

        # Generators cooling valve position.
        reg_name = "{}.{}.valve.position".format(self.key, valve_name)
        position = self._registers.by_name(reg_name)
        if position is not None:
            position.update_handlers = position_cb
            position.update()

    def __ahu_warehouse_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__vcg_ahu_warehouse is not None:
                self.__vcg_ahu_warehouse.shutdown()
                del self.__vcg_ahu_warehouse

            # AHU Warehouse (RED and BLUE)
            self.__vcg_ahu_warehouse = ValveControlGroup(\
                name="VCG AHU warhorse",
                key=f"{register.name}",
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold"],
                rev_valves=["hot"],
                mode = ValveControlGroupMode.DualSide)

            if self.__vcg_ahu_warehouse is not None:
                self.__vcg_ahu_warehouse.init()

        elif register.value == {}:
            if self.__vcg_ahu_warehouse is not None:
                self.__vcg_ahu_warehouse.shutdown()
                del self.__vcg_ahu_warehouse

    def __ahu_warehouse_pos_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < -100 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__vcg_ahu_warehouse is not None:
            self.__vcg_ahu_warehouse.target_position = register.value

    def __init_registers(self):

        self.__attach_valve("ahu_warehouse",
                                   self.__ahu_warehouse_settings_cb,
                                   self.__ahu_warehouse_pos_cb)

        # self.__attach_valve("conv_kitchen",
        #                            self.__conv_kitchen_settings_cb,
        #                            self.__conv_kitchen_pos_cb)

        # self.__attach_valve("ahu_conf_hall",
        #                            self.__ahu_conf_hall_settings_cb,
        #                            self.__ahu_conf_hall_pos_cb)

        # self.__attach_valve("floor_west",
        #                            self.__floor_west_settings_cb,
        #                            self.__floor_west_pos_cb)

        # self.__attach_valve("conv_west",
        #                            self.__conv_west_settings_cb,
        #                            self.__conv_west_pos_cb)

        # self.__attach_valve("ahu_floor",
        #                            self.__ahu_floor_settings_cb,
        #                            self.__ahu_floor_cb)

        # self.__attach_valve("ahu_fitness",
        #                            self.__ahu_fitness_settings_cb,
        #                            self.__ahu_fitness_pos_cb)

        # self.__attach_valve("floor_east",
        #                            self.__floor_east_settings_cb,
        #                            self.__floor_east_pos_cb)

        # self.__attach_valve("conv_east",
        #                            self.__conv_east_settings_cb,
        #                            self.__conv_east_pos_cb)

        # self.__attach_valve("ahu_pool",
        #                            self.__ahu_pool_settings_cb,
        #                            self.__ahu_pool_pos_cb)

        # self.__attach_valve("heat_pool",
        #                            self.__ahu_heat_settings_cb,
        #                            self.__ahu_heat_pos_cb)

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

        position = self._registers.by_name("ecd.ahu_warehouse.valve.position")
        position.value = self.__state

        if self.__state == 0:
            self.__state = 100

        elif self.__state == 100:
            self.__state = -100

        elif self.__state == -100:
            self.__state = 100

        if self.__vcg_ahu_warehouse is not None:
            self.__vcg_ahu_warehouse.update()

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

        # if self.__convectors_kitchen is not None:
        #     self.__convectors_kitchen.update()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

        if self.__vcg_ahu_warehouse is not None:
            self.__vcg_ahu_warehouse.shutdown()

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

        # if self.__convectors_kitchen is not None:
        #     self.__convectors_kitchen.shutdown()

#endregion
