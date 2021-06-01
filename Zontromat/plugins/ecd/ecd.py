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

from data import verbal_const

from utils.logger import get_logger
#from utils.logic.timer import Timer
#from utils.logic.state_machine import StateMachine

from plugins.base_plugin import BasePlugin

from devices.factories.valve.valve_factory import ValveFactory
from devices.utils.valve_control_group.valve_control_group import ValveControlGroup
from devices.utils.valve_control_group.valve_control_group_mode import ValveControlGroupMode

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

__class_name__ = "EnergyCenterDistribution"
"""Plugin class name."""

#endregion

class EnergyCenterDistribution(BasePlugin):
    """Energy center distribution control plugin."""

#region Attributes

    __logger = None
    """Logger
    """


    __v_underfloor_heating_foyer = None
    """Valve foyer.
    """

    __v_underfloor_heating_trestle = None
    """Underfloor heating trestle.
    """

    __v_underfloor_heating_pool = None
    """Underfloor heating pool.
    """

    __v_air_cooling = None
    """Valve air cooling.
    """

    __v_ground_drill = None
    """Valve ground drilling.
    """

    __v_generators_cooling = None
    """Generators cooling.
    """

    __v_short_green_purple = None
    """Short valve between green and purple pipes.
    """

    __v_underfloor_west_bypass = None
    """Valve underfloor west bypass.
    """    

    __v_underfloor_east_bypass = None
    """Valve underfloor east bypass.
    """

    __vcg_pool_heating = None
    """VCG Pool heating.
    """

    __vcg_tva_pool = None
    """VCG TVA pool.
    """

    __vcg_convectors_east = None
    """VCG Convectors east.
    """

    __vcg_underfloor_east = None
    """VCG Underfloor east.
    """

    __vcg_convectors_west = None
    """VCG Convectors west.
    """

    __vcg_tva_fitness = None
    """VCG TVA fitness.
    """

    __vcg_tva_roof_floor = None
    """VCG TVA roof floor.
    """

    __vcg_underfloor_west = None
    """VCG Underfloor west.
    """

    __vcg_tva_conference_center = None
    """VCG TVA conference centre.
    """

    __vcg_convectors_kitchen = None
    """VCG Convectors kitchen.
    """

    __vcg_tva_warehouse = None
    """VCG TVA wearhouse.
    """

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
        self.__logger.info("Starting up the: {}".format(self.name))

        # Consumers (RED)
        self.__vcg_pool_heating = ValveControlGroup.create(
            name="VCG Pool Heating",
            key="{}.vcg_pool_heating".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["valve"],
            fw_pumps=["pump"])
        self.__vcg_pool_heating.mode = ValveControlGroupMode.Proportional

        # TVA Pool (RED and BLUE)
        self.__vcg_tva_pool = ValveControlGroup.create(\
            name="TVA Pool",
            key="{}.vcg_tva_pool".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_tva_pool.mode = ValveControlGroupMode.DualSide

        # Convectors East (RED and BLUE)
        self.__vcg_convectors_east = ValveControlGroup.create(\
            name="Convectors east",
            key="{}.convectors_east".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_convectors_east.mode = ValveControlGroupMode.DualSide

        # Floor East (RED and BLUE)
        self.__vcg_underfloor_east = ValveControlGroup.create(\
            name="Underfloor east",
            key="{}.floor_east".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_underfloor_east.mode = ValveControlGroupMode.DualSide

        # Convectors West (RED and BLUE)
        self.__vcg_convectors_west = ValveControlGroup.create(\
            name="Convectors west",
            key="{}.convectors_west".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_convectors_west.mode = ValveControlGroupMode.DualSide

        # TVA Fitness (RED and BLUE)
        self.__vcg_tva_fitness = ValveControlGroup.create(\
            name="TVA fitness",
            key="{}.tva_fitness".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_tva_fitness.mode = ValveControlGroupMode.DualSide

        # TVA Roof Floor (RED and BLUE)
        self.__vcg_tva_roof_floor = ValveControlGroup.create(\
            name="TVA roof floor",
            key="{}.tva_roof_floor".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_tva_roof_floor.mode = ValveControlGroupMode.DualSide

        # Floor West (RED and BLUE)
        self.__vcg_underfloor_west = ValveControlGroup.create(\
            name="Floor west",
            key="{}.floor_west".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_underfloor_west.mode = ValveControlGroupMode.DualSide

        # TVA Conference (RED and BLUE)
        self.__vcg_tva_conference_center = ValveControlGroup.create(\
            name="TVA conference center",
            key="{}.tva_conference_center".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_tva_conference_center.mode = ValveControlGroupMode.DualSide

        # Convectors Kitchen (RED and BLUE)
        self.__vcg_convectors_kitchen = ValveControlGroup.create(\
            name="Convectors kitchen",
            key="{}.convectors_kitchen".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_convectors_kitchen.mode = ValveControlGroupMode.DualSide

        # TVA Wearhouse (RED and BLUE)
        self.__vcg_tva_warehouse = ValveControlGroup.create(\
            name="TVA warehouse",
            key="{}.tva_warehouse".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_tva_warehouse.mode = ValveControlGroupMode.DualSide

    def __del__(self):
        """Destructor
        """

        # Worm circle (PURPLE)
        if self.__v_underfloor_heating_foyer is not None:
            del self.__v_underfloor_heating_foyer

        if self.__v_underfloor_heating_trestle is not None:
            del self.__v_underfloor_heating_trestle

        if self.__v_underfloor_heating_pool is not None:
            del self.__v_underfloor_heating_pool

        # Thermal consumers.
        if self.__vcg_pool_heating is not None:
            del self.__vcg_pool_heating

        if self.__vcg_tva_pool is not None:
            del self.__vcg_tva_pool

        if self.__vcg_convectors_east is not None:
            del self.__vcg_convectors_east

        if self.__vcg_underfloor_east is not None:
            del self.__vcg_underfloor_east

        if self.__vcg_convectors_west is not None:
            del self.__vcg_convectors_west

        if self.__vcg_tva_fitness is not None:
            del self.__vcg_tva_fitness

        if self.__vcg_tva_roof_floor is not None:
            del self.__vcg_tva_roof_floor

        if self.__vcg_underfloor_west is not None:
            del self.__vcg_underfloor_west

        if self.__vcg_tva_conference_center is not None:
            del self.__vcg_tva_conference_center

        if self.__vcg_convectors_kitchen is not None:
            del self.__vcg_convectors_kitchen

        if self.__vcg_tva_warehouse is not None:
            del self.__vcg_tva_warehouse

        if self.__v_short_green_purple is not None:
            del self.__v_short_green_purple

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#region Private Methods (Registers)

    def __underfloor_heating_foyer_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_heating_foyer is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_underfloor_heating_foyer = ValveFactory.create(
                name="Valve Underfloor Heating Foyer",
                controller=self._controller,
                params=params)

            if self.__v_underfloor_heating_foyer is not None:
                self.__v_underfloor_heating_foyer.init()

        elif register.value == verbal_const.OFF and self.__v_underfloor_heating_foyer is not None:
            self.__v_underfloor_heating_foyer.shutdown()
            del self.__v_underfloor_heating_foyer

    def __underfloor_heating_trestle_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_heating_trestle is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_underfloor_heating_trestle = ValveFactory.create(
                name="Valve Underfloor Heating Trestle",
                controller=self._controller,
                params=params)

            if self.__v_underfloor_heating_trestle is not None:
                self.__v_underfloor_heating_trestle.init()

        elif register.value == verbal_const.OFF and self.__v_underfloor_heating_trestle is not None:
            self.__v_underfloor_heating_trestle.shutdown()
            del self.__v_underfloor_heating_trestle

    def __underfloor_heating_pool_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_heating_pool is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_underfloor_heating_pool = ValveFactory.create(
                name="Valve Underfloor Heating Pool",
                controller=self._controller,
                params=params)

            if self.__v_underfloor_heating_pool is not None:
                self.__v_underfloor_heating_pool.init()

        elif register.value == verbal_const.OFF and self.__v_underfloor_heating_pool is not None:
            self.__v_underfloor_heating_pool.shutdown()
            del self.__v_underfloor_heating_pool

    def __generators_cooling_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_generators_cooling is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_generators_cooling = ValveFactory.create(
                name="Valve Generators Cooling",
                controller=self._controller,
                params=params)

            if self.__v_generators_cooling is not None:
                self.__v_generators_cooling.init()

        elif register.value == verbal_const.OFF and self.__v_generators_cooling is not None:
            self.__v_generators_cooling.shutdown()
            del self.__v_generators_cooling

    def __ground_drill_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_ground_drill is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_ground_drill = ValveFactory.create(
                name="Valve Ground Drilling",
                controller=self._controller,
                params=params)

            if self.__v_ground_drill is not None:
                self.__v_ground_drill.init()

        elif register.value == verbal_const.OFF and self.__v_ground_drill is not None:
            self.__v_ground_drill.shutdown()
            del self.__v_ground_drill

    def __air_cooling_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_air_cooling is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_air_cooling = ValveFactory.create(
                name="Valve Air Cooling",
                controller=self._controller,
                params=params)

            if self.__v_air_cooling is not None:
                self.__v_air_cooling.init()

        elif register.value == verbal_const.OFF and self.__v_air_cooling is not None:
            self.__v_air_cooling.shutdown()
            del self.__v_air_cooling

    def __short_green_purple_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_short_green_purple is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_short_green_purple = ValveFactory.create(
                name="Valve Short Green Purple",
                controller=self._controller,
                params=params)

            if self.__v_short_green_purple is not None:
                self.__v_short_green_purple.init()

        elif register.value == verbal_const.OFF and self.__v_short_green_purple is not None:
            self.__v_short_green_purple.shutdown()
            del self.__v_short_green_purple

    def __underfloor_west_bypass_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_west_bypass is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_underfloor_west_bypass = ValveFactory.create(
                name="Valve Underfloor West Bypass",
                controller=self._controller,
                params=params)

            if self.__v_underfloor_west_bypass is not None:
                self.__v_underfloor_west_bypass.init()

        elif register.value == verbal_const.OFF and self.__v_underfloor_west_bypass is not None:
            self.__v_underfloor_west_bypass.shutdown()
            del self.__v_underfloor_west_bypass   

    def __underfloor_east_bypass_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_east_bypass is None:

            params = register.value.split("/")

            if len(params) <= 2:
                raise ValueError("Not enough parameters.")

            self.__v_underfloor_east_bypass = ValveFactory.create(
                name="Valve Underfloor East Bypass",
                controller=self._controller,
                params=params)

            if self.__v_underfloor_east_bypass is not None:
                self.__v_underfloor_east_bypass.init()

        elif register.value == verbal_const.OFF and self.__v_underfloor_east_bypass is not None:
            self.__v_underfloor_east_bypass.shutdown()
            del self.__v_underfloor_east_bypass   


    def __underfloor_heating_foyer_pos_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_heating_foyer is not None:
            self.__v_underfloor_heating_foyer.target_position = register.value

    def __underfloor_heating_trestle_pos_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_heating_trestle is not None:
            self.__v_underfloor_heating_trestle.target_position = register.value

    def __underfloor_heating_pool_pos_cb(self, register):

          # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_heating_pool is not None:
            self.__v_underfloor_heating_pool.target_position = register.value

    def __air_cooling_pos_cb(self, register):

          # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_air_cooling is not None:
            self.__v_air_cooling.target_position = register.value      

    def __ground_drill_pos_cb(self, register):

          # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_ground_drill is not None:
            self.__v_ground_drill.target_position = register.value  

    def __generators_cooling_pos_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_generators_cooling is not None:
            self.__v_generators_cooling.target_position = register.value

    def __short_green_purple_pos_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_short_green_purple is not None:
            self.__v_short_green_purple.target_position = register.value

    def __underfloor_west_bypass_pos_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_west_bypass is not None:
            self.__v_underfloor_west_bypass.target_position = register.value

    def __underfloor_east_bypass_pos_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_east_bypass is not None:
            self.__v_underfloor_east_bypass.target_position = register.value

    def __init_registers(self):

        # === Valve group. (PURPLE) ===
        reg_name = "{}.underfloor_heating_foyer.valve.enabled".format(self.key)
        underfloor_heating_foyer = self._registers.by_name(reg_name)
        if underfloor_heating_foyer is not None:
                underfloor_heating_foyer.update_handlers = self.__underfloor_heating_foyer_enabled_cb
                underfloor_heating_foyer.update()

        reg_name = "{}.underfloor_heating_trestle.valve.enabled".format(self.key)
        underfloor_heating_trestle = self._registers.by_name(reg_name)
        if underfloor_heating_trestle is not None:
                underfloor_heating_trestle.update_handlers = self.__underfloor_heating_trestle_enabled_cb
                underfloor_heating_trestle.update()

        reg_name = "{}.underfloor_heating_pool.valve.enabled".format(self.key)
        underfloor_heating_pool = self._registers.by_name(reg_name)
        if underfloor_heating_pool is not None:
                underfloor_heating_pool.update_handlers = self.__underfloor_heating_pool_enabled_cb
                underfloor_heating_pool.update()

        reg_name = "{}.air_cooling.valve.enabled".format(self.key)
        air_cooling = self._registers.by_name(reg_name)
        if air_cooling is not None:
                air_cooling.update_handlers = self.__air_cooling_enabled_cb
                air_cooling.update()

        reg_name = "{}.ground_drill.valve.enabled".format(self.key)
        ground_drill = self._registers.by_name(reg_name)
        if ground_drill is not None:
                ground_drill.update_handlers = self.__ground_drill_enabled_cb
                ground_drill.update()

        # === Generators Cooling (GREEN) ===
        reg_name = "{}.generators_cooling.valve.enabled".format(self.key)
        generators_cooling = self._registers.by_name(reg_name)
        if generators_cooling is not None:
                generators_cooling.update_handlers = self.__generators_cooling_enabled_cb
                generators_cooling.update()

        # Short valve between green and purple pipes.
        reg_name = "{}.short_green_purple.valve.enabled".format(self.key)
        short_green_purple = self._registers.by_name(reg_name)
        if short_green_purple is not None:
                short_green_purple.update_handlers = self.__short_green_purple_enabled_cb
                short_green_purple.update()

        # Short valve between green and purple pipes.
        reg_name = "{}.underfloor_west_bypass.valve.enabled".format(self.key)
        underfloor_west_bypass = self._registers.by_name(reg_name)
        if underfloor_west_bypass is not None:
                underfloor_west_bypass.update_handlers = self.__underfloor_west_bypass_enabled_cb
                underfloor_west_bypass.update()

        # Short valve between green and purple pipes.
        reg_name = "{}.underfloor_east_bypass.valve.enabled".format(self.key)
        underfloor_east_bypass = self._registers.by_name(reg_name)
        if underfloor_east_bypass is not None:
                underfloor_east_bypass.update_handlers = self.__underfloor_east_bypass_enabled_cb
                underfloor_east_bypass.update()

        # ====================================================================================

        # Generators cooling valve postition.
        reg_name = "{}.underfloor_heating_foyer.valve.position".format(self.key)
        underfloor_heating_foyer_pos = self._registers.by_name(reg_name)
        if underfloor_heating_foyer_pos is not None:
                underfloor_heating_foyer_pos.update_handlers = self.__underfloor_heating_foyer_pos_cb
                underfloor_heating_foyer_pos.update()

        # Underfloor heating trestle valve postition.
        reg_name = "{}.underfloor_heating_trestle.valve.position".format(self.key)
        underfloor_heating_trestle = self._registers.by_name(reg_name)
        if underfloor_heating_trestle is not None:
                underfloor_heating_trestle.update_handlers = self.__underfloor_heating_trestle_pos_cb
                underfloor_heating_trestle.update()

        # Underfloor heating pool valve postition.
        reg_name = "{}.underfloor_heating_pool.valve.position".format(self.key)
        underfloor_heating_pool = self._registers.by_name(reg_name)
        if underfloor_heating_pool is not None:
                underfloor_heating_pool.update_handlers = self.__underfloor_heating_pool_pos_cb
                underfloor_heating_pool.update()

        # Air cooling valve postition.
        reg_name = "{}.air_cooling.valve.position".format(self.key)
        air_cooling = self._registers.by_name(reg_name)
        if air_cooling is not None:
                air_cooling.update_handlers = self.__air_cooling_pos_cb
                air_cooling.update()

        # Ground drill valve postition.
        reg_name = "{}.ground_drill.valve.position".format(self.key)
        ground_drill = self._registers.by_name(reg_name)
        if ground_drill is not None:
                ground_drill.update_handlers = self.__ground_drill_pos_cb
                ground_drill.update()

        # Generators cooling valve postition.
        reg_name = "{}.generators_cooling.valve.position".format(self.key)
        generators_cooling_pos = self._registers.by_name(reg_name)
        if generators_cooling_pos is not None:
                generators_cooling_pos.update_handlers = self.__generators_cooling_pos_cb
                generators_cooling_pos.update()

        # Generators cooling valve postition.
        reg_name = "{}.short_green_purple.valve.position".format(self.key)
        short_green_purple = self._registers.by_name(reg_name)
        if short_green_purple is not None:
                short_green_purple.update_handlers = self.__short_green_purple_pos_cb
                short_green_purple.update()

        # Underfloor west bypass valve postition.
        reg_name = "{}.underfloor_west_bypass.valve.position".format(self.key)
        underfloor_west_bypass = self._registers.by_name(reg_name)
        if underfloor_west_bypass is not None:
                underfloor_west_bypass.update_handlers = self.__underfloor_west_bypass_pos_cb
                underfloor_west_bypass.update()

        # Underfloor east bypass valve postition
        reg_name = "{}.underfloor_west_bypass.valve.position".format(self.key)
        underfloor_west_bypass = self._registers.by_name(reg_name)
        if underfloor_west_bypass is not None:
                underfloor_west_bypass.update_handlers = self.__underfloor_east_bypass_pos_cb
                underfloor_west_bypass.update()

#endregion

#region Properties

#endregion

#region Public Methods

    def init(self):
        """Init the plugin.
        """

        self.__init_registers()

        self.__vcg_pool_heating.init()
        self.__vcg_tva_pool.init()
        self.__vcg_convectors_east.init()
        self.__vcg_underfloor_east.init()
        self.__vcg_convectors_west.init()
        self.__vcg_tva_fitness.init()
        self.__vcg_tva_roof_floor.init()
        self.__vcg_underfloor_west.init()
        self.__vcg_tva_conference_center.init()
        self.__vcg_convectors_kitchen.init()
        self.__vcg_tva_warehouse.init()

        self.ready(True)

    def update(self):
        """Update the plugin state.
        """

        if not self.is_ready():
            return

        self.in_cycle(True)

        self.__v_underfloor_heating_foyer.update()
        self.__v_underfloor_heating_trestle.update()
        self.__v_underfloor_heating_pool.update()
        self.__v_air_cooling.update()
        self.__v_ground_drill.update()
        self.__v_generators_cooling.update()
        self.__v_short_green_purple.update()
        self.__v_underfloor_west_bypass.update()
        self.__v_underfloor_east_bypass.update()


        self.__vcg_pool_heating.update()
        self.__vcg_tva_pool.update()
        self.__vcg_convectors_east.update()
        self.__vcg_underfloor_east.update()
        self.__vcg_convectors_west.update()
        self.__vcg_tva_fitness.update()
        self.__vcg_tva_roof_floor.update()
        self.__vcg_underfloor_west.update()
        self.__vcg_tva_conference_center.update()
        self.__vcg_convectors_kitchen.update()
        self.__vcg_tva_warehouse.update()

        self.in_cycle(False)

    def shutdown(self):
        """Shutting down the plugin.
        """

        self.ready(False)
        self.wait()

        self.__logger.info("Shutting down the {}".format(self.name))

        self.__v_underfloor_heating_foyer.shutdown()
        self.__v_underfloor_heating_trestle.shutdown()
        self.__v_underfloor_heating_pool.shutdown()
        self.__v_air_cooling.shutdown()
        self.__v_ground_drill.shutdown()
        self.__v_generators_cooling.shutdown()
        self.__v_short_green_purple.shutdown()
        self.__v_underfloor_west_bypass.shutdown()
        self.__v_underfloor_east_bypass.shutdown()

        self.__vcg_pool_heating.shutdown()
        self.__vcg_tva_pool.shutdown()
        self.__vcg_convectors_east.shutdown()
        self.__vcg_underfloor_east.shutdown()
        self.__vcg_convectors_west.shutdown()
        self.__vcg_tva_fitness.shutdown()
        self.__vcg_tva_roof_floor.shutdown()
        self.__vcg_underfloor_west.shutdown()
        self.__vcg_tva_conference_center.shutdown()
        self.__vcg_convectors_kitchen.shutdown()
        self.__vcg_tva_warehouse.shutdown()

#endregion
