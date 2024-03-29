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

        return



        # Convectors West (RED and BLUE)
        self.__vcg_convectors_west = ValveControlGroup(\
            name="VCG Convectors west",
            key="{}.convectors_west".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_convectors_west.mode = ValveControlGroupMode.DualSide

        # TVA Fitness (RED and BLUE)
        self.__vcg_tva_fitness = ValveControlGroup(\
            name="VCG TVA fitness",
            key="{}.tva_fitness".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_tva_fitness.mode = ValveControlGroupMode.DualSide

        # TVA Roof Floor (RED and BLUE)
        self.__vcg_tva_roof_floor = ValveControlGroup(\
            name="VCG TVA roof floor",
            key="{}.tva_roof_floor".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_tva_roof_floor.mode = ValveControlGroupMode.DualSide

        # Floor West (RED and BLUE)
        self.__vcg_underfloor_west = ValveControlGroup(\
            name="VCG Floor west",
            key="{}.floor_west".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_underfloor_west.mode = ValveControlGroupMode.DualSide

        # TVA Conference (RED and BLUE)
        self.__vcg_tva_conference_center = ValveControlGroup(\
            name="VCG TVA conference center",
            key="{}.tva_conference_center".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_tva_conference_center.mode = ValveControlGroupMode.DualSide

        # Convectors Kitchen (RED and BLUE)
        self.__vcg_convectors_kitchen = ValveControlGroup(\
            name="VCG Convectors kitchen",
            key="{}.convectors_kitchen".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold_in", "cold_out"],
            rev_valves=["hot_in", "hot_out"],
            fw_pumps=["pump"])
        self.__vcg_convectors_kitchen.mode = ValveControlGroupMode.DualSide

        # TVA Wearhouse (RED and BLUE)
        self.__vcg_tva_warehouse = ValveControlGroup(\
            name="VCG TVA warehouse",
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

    def __attach_single_valve(self, valve_name: str, enable_cb, position_cb, calibration_cb):
        """Attach valve callbacks.

        Args:
            valve_name (str): Name of the valve.
            enable_cb ([type]): Enable callback.
            position_cb ([type]): Position callback.
            calibration_cb ([type]): Calibration callback.
        """

        # Generators cooling valve enabled.
        reg_name = "{}.{}.valve.enabled".format(self.key, valve_name)
        enabled = self._registers.by_name(reg_name)
        if enabled is not None:
            enabled.update_handlers = enable_cb
            enabled.update()

        # Generators cooling valve postition.
        reg_name = "{}.{}.valve.position".format(self.key, valve_name)
        position = self._registers.by_name(reg_name)
        if position is not None:
            position.update_handlers = position_cb
            position.update()

        # Generators cooling valve calibrate.
        reg_name = "{}.{}.valve.calibrate".format(self.key, valve_name)
        calibration = self._registers.by_name(reg_name)
        if calibration is not None:
            calibration.update_handlers = calibration_cb
            calibration.update()


    def __underfloor_heating_foyer_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_heating_foyer is None:

            self.__v_underfloor_heating_foyer = ValveFactory.create(
                name="Valve Underfloor Heating Foyer",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_underfloor_heating_foyer is not None:
                self.__v_underfloor_heating_foyer.init()

        elif register.value == {} and self.__v_underfloor_heating_foyer is not None:
            self.__v_underfloor_heating_foyer.shutdown()
            del self.__v_underfloor_heating_foyer

    def __underfloor_heating_foyer_pos_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_heating_foyer is not None:
            self.__v_underfloor_heating_foyer.target_position = register.value

    def __underfloor_heating_foyer_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_underfloor_heating_foyer is not None:
                self.__v_underfloor_heating_foyer.calibrate()


    def __underfloor_heating_trestle_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_heating_trestle is None:

            self.__v_underfloor_heating_trestle = ValveFactory.create(
                name="Valve Underfloor Heating Trestle",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_underfloor_heating_trestle is not None:
                self.__v_underfloor_heating_trestle.init()

        elif register.value == {} and self.__v_underfloor_heating_trestle is not None:
            self.__v_underfloor_heating_trestle.shutdown()
            del self.__v_underfloor_heating_trestle

    def __underfloor_heating_trestle_pos_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_heating_trestle is not None:
            self.__v_underfloor_heating_trestle.target_position = register.value

    def __underfloor_heating_trestle_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_underfloor_heating_trestle is not None:
                self.__v_underfloor_heating_trestle.calibrate()


    def __underfloor_heating_pool_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_heating_pool is None:

            self.__v_underfloor_heating_pool = ValveFactory.create(
                name="Valve Underfloor Heating Pool",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_underfloor_heating_pool is not None:
                self.__v_underfloor_heating_pool.init()

        elif register.value == {} and self.__v_underfloor_heating_pool is not None:
            self.__v_underfloor_heating_pool.shutdown()
            del self.__v_underfloor_heating_pool

    def __underfloor_heating_pool_pos_cb(self, register: Register):

          # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_heating_pool is not None:
            self.__v_underfloor_heating_pool.target_position = register.value

    def __underfloor_heating_pool_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_underfloor_heating_pool is not None:
                self.__v_underfloor_heating_pool.calibrate()


    def __air_cooling_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_air_cooling is None:

            self.__v_air_cooling = ValveFactory.create(
                name="Valve Air Cooling",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_air_cooling is not None:
                self.__v_air_cooling.init()

        elif register.value == {} and self.__v_air_cooling is not None:
            self.__v_air_cooling.shutdown()
            del self.__v_air_cooling

    def __air_cooling_pos_cb(self, register: Register):

          # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_air_cooling is not None:
            self.__v_air_cooling.target_position = register.value

    def __air_cooling_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_air_cooling is not None:
                self.__v_air_cooling.calibrate()


    def __ground_drill_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_ground_drill is None:

            self.__v_ground_drill = ValveFactory.create(
                name="Valve Ground Drilling",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_ground_drill is not None:
                self.__v_ground_drill.init()

        elif register.value == {} and self.__v_ground_drill is not None:
            self.__v_ground_drill.shutdown()
            del self.__v_ground_drill

    def __ground_drill_pos_cb(self, register: Register):

          # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_ground_drill is not None:
            self.__v_ground_drill.target_position = register.value

    def __ground_drill_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_ground_drill is not None:
                self.__v_ground_drill.calibrate()


    def __generators_cooling_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_generators_cooling is None:

            self.__v_generators_cooling = ValveFactory.create(
                name="Valve Generators Cooling",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_generators_cooling is not None:
                self.__v_generators_cooling.init()

        elif register.value == {} and self.__v_generators_cooling is not None:
            self.__v_generators_cooling.shutdown()
            del self.__v_generators_cooling

    def __generators_cooling_pos_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_generators_cooling is not None:
            self.__v_generators_cooling.target_position = register.value

    def __generators_cooling_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_generators_cooling is not None:
                self.__v_generators_cooling.calibrate()


    def __short_green_purple_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_short_green_purple is None:

            self.__v_short_green_purple = ValveFactory.create(
                name="Valve Short Green Purple",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_short_green_purple is not None:
                self.__v_short_green_purple.init()

        elif register.value == {} and self.__v_short_green_purple is not None:
            self.__v_short_green_purple.shutdown()
            del self.__v_short_green_purple

    def __short_green_purple_pos_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_short_green_purple is not None:
            self.__v_short_green_purple.target_position = register.value

    def __short_green_purple_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_short_green_purple is not None:
                self.__v_short_green_purple.calibrate()


    def __underfloor_west_bypass_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_west_bypass is None:

            self.__v_underfloor_west_bypass = ValveFactory.create(
                name="Valve Underfloor West Bypass",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_underfloor_west_bypass is not None:
                self.__v_underfloor_west_bypass.init()

        elif register.value == {} and self.__v_underfloor_west_bypass is not None:
            self.__v_underfloor_west_bypass.shutdown()
            del self.__v_underfloor_west_bypass

    def __underfloor_west_bypass_pos_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_west_bypass is not None:
            self.__v_underfloor_west_bypass.target_position = register.value

    def __underfloor_west_bypass_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_underfloor_west_bypass is not None:
                self.__v_underfloor_west_bypass.calibrate()


    def __underfloor_east_bypass_enabled_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_underfloor_east_bypass is None:

            self.__v_underfloor_east_bypass = ValveFactory.create(
                name="Valve Underfloor East Bypass",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__v_underfloor_east_bypass is not None:
                self.__v_underfloor_east_bypass.init()

        elif register.value == {} and self.__v_underfloor_east_bypass is not None:
            self.__v_underfloor_east_bypass.shutdown()
            del self.__v_underfloor_east_bypass

    def __underfloor_east_bypass_pos_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0 or register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__v_underfloor_east_bypass is not None:
            self.__v_underfloor_east_bypass.target_position = register.value

    def __underfloor_east_bypass_calib_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value:
            if self.__v_underfloor_east_bypass is not None:
                self.__v_underfloor_east_bypass.calibrate()


    def __vcg_pool_heating_enable_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_pool_heating is None:

            # Consumers (RED)
            self.__vcg_pool_heating = ValveControlGroup(
                name="VCG Pool Heating",
                key="{}.vcg_pool_heating".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["valve"],
                fw_pumps=["pump"])
            self.__vcg_pool_heating.mode = ValveControlGroupMode.Proportional

            if self.__vcg_pool_heating is not None:
                self.__vcg_pool_heating.init()

        elif register.value == False and self.__vcg_pool_heating is not None:
            self.__vcg_pool_heating.shutdown()
            del self.__vcg_pool_heating

    def __vcg_tva_pool_enable_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_tva_pool is None:

            # Consumers (RED)
            self.__vcg_tva_pool = ValveControlGroup(
                name="VCG TVA Pool",
                key="{}.vcg_tva_pool".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_tva_pool.mode = ValveControlGroupMode.Proportional

            if self.__vcg_tva_pool is not None:
                self.__vcg_tva_pool.init()

        elif register.value == False and self.__vcg_tva_pool is not None:
            self.__vcg_tva_pool.shutdown()
            del self.__vcg_tva_pool

    def __convectors_east_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_convectors_east is None:

            # Consumers (RED)
            self.__vcg_convectors_east = ValveControlGroup(
                name="VCG Convectors east",
                key="{}.convectors_east".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_convectors_east.mode = ValveControlGroupMode.Proportional

            if self.__vcg_convectors_east is not None:
                self.__vcg_convectors_east.init()

        elif register.value == False and self.__vcg_convectors_east is not None:
            self.__vcg_convectors_east.shutdown()
            del self.__vcg_convectors_east

    def __underfloor_east_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_underfloor_east is None:

            # Floor East (RED and BLUE)
            self.__vcg_underfloor_east = ValveControlGroup(\
                name="VCG Underfloor east",
                key="{}.underfloor_east".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_underfloor_east.mode = ValveControlGroupMode.DualSide

            if self.__vcg_underfloor_east is not None:
                self.__vcg_underfloor_east.init()

        elif register.value == False and self.__vcg_underfloor_east is not None:
            self.__vcg_underfloor_east.shutdown()
            del self.__vcg_underfloor_east

    def __convectors_west_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_convectors_west is None:

            # Floor East (RED and BLUE)
            self.__vcg_convectors_west = ValveControlGroup(\
                name="VCG Convectors west",
                key="{}.convectors_west".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_convectors_west.mode = ValveControlGroupMode.DualSide

            if self.__vcg_convectors_west is not None:
                self.__vcg_convectors_west.init()

        elif register.value == False and self.__vcg_convectors_west is not None:
            self.__vcg_convectors_west.shutdown()
            del self.__vcg_convectors_west

    def __tva_fitness_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_tva_fitness is None:

            # Floor East (RED and BLUE)
            self.__vcg_tva_fitness = ValveControlGroup(\
                name="VCG tva fitness",
                key="{}.tva_fitness".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_tva_fitness.mode = ValveControlGroupMode.DualSide

            if self.__vcg_tva_fitness is not None:
                self.__vcg_tva_fitness.init()

        elif not register.value and self.__vcg_tva_fitness is not None:
            self.__vcg_tva_fitness.shutdown()
            del self.__vcg_tva_fitness

    def __tva_roof_floor_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_tva_roof_floor is None:

            # Floor East (RED and BLUE)
            self.__vcg_tva_roof_floor = ValveControlGroup(\
                name="VCG tva roof floor",
                key="{}.tva_roof_floor".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_tva_roof_floor.mode = ValveControlGroupMode.DualSide

            if self.__vcg_tva_roof_floor is not None:
                self.__vcg_tva_roof_floor.init()

        elif not register.value and self.__vcg_tva_roof_floor is not None:
            self.__vcg_tva_roof_floor.shutdown()
            del self.__vcg_tva_roof_floor

    def __underfloor_west_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_underfloor_west is None:

            # Floor East (RED and BLUE)
            self.__vcg_underfloor_west = ValveControlGroup(\
                name="VCG underfloor west",
                key="{}.floor_west".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_underfloor_west.mode = ValveControlGroupMode.DualSide

            if self.__vcg_underfloor_west is not None:
                self.__vcg_underfloor_west.init()

        elif not register.value and self.__vcg_underfloor_west is not None:
            self.__vcg_underfloor_west.shutdown()
            del self.__vcg_underfloor_west

    def __vcg_tva_conference_center_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_tva_conference_center is None:

            # Floor East (RED and BLUE)
            self.__vcg_tva_conference_center = ValveControlGroup(\
                name="VCG tva conference center",
                key="{}.tva_conference_center".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_tva_conference_center.mode = ValveControlGroupMode.DualSide

            if self.__vcg_tva_conference_center is not None:
                self.__vcg_tva_conference_center.init()

        elif not register.value and self.__vcg_tva_conference_center is not None:
            self.__vcg_tva_conference_center.shutdown()
            del self.__vcg_tva_conference_center

    def __vcg_convectors_kitchen_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_convectors_kitchen is None:

            # Floor East (RED and BLUE)
            self.__vcg_convectors_kitchen = ValveControlGroup(\
                name="VCG convectors kitchen",
                key="{}.convectors_kitchen".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_convectors_kitchen.mode = ValveControlGroupMode.DualSide

            if self.__vcg_convectors_kitchen is not None:
                self.__vcg_convectors_kitchen.init()

        elif not register.value and self.__vcg_convectors_kitchen is not None:
            self.__vcg_convectors_kitchen.shutdown()
            del self.__vcg_convectors_kitchen

    def __vcg_tva_warehouse_enable_cb(self, register: Register):

        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value and self.__vcg_tva_warehouse is None:

            # Floor East (RED and BLUE)
            self.__vcg_tva_warehouse = ValveControlGroup(\
                name="VCG tva warehouse",
                key="{}.tva_warehouse".format(self.key),
                controller=self._controller,
                registers=self._registers,
                fw_valves=["cold_in", "cold_out"],
                rev_valves=["hot_in", "hot_out"],
                fw_pumps=["pump"])
            self.__vcg_tva_warehouse.mode = ValveControlGroupMode.DualSide

            if self.__vcg_tva_warehouse is not None:
                self.__vcg_tva_warehouse.init()

        elif not register.value and self.__vcg_tva_warehouse is not None:
            self.__vcg_tva_warehouse.shutdown()
            del self.__vcg_tva_warehouse


    def __init_registers(self):

        # =========================== Valve group. (PURPLE) ===========================
        # Generators cooling valve.
        self.__attach_single_valve("underfloor_heating_foyer",
                                   self.__underfloor_heating_foyer_enabled_cb,
                                   self.__underfloor_heating_foyer_pos_cb,
                                   self.__underfloor_heating_foyer_calib_cb)

        # Underfloor heating trestle valve.
        self.__attach_single_valve("underfloor_heating_trestle",
                                   self.__underfloor_heating_trestle_enabled_cb,
                                   self.__underfloor_heating_trestle_pos_cb,
                                   self.__underfloor_heating_trestle_calib_cb)

        self.__attach_single_valve("underfloor_heating_pool",
                                   self.__underfloor_heating_pool_enabled_cb,
                                   self.__underfloor_heating_pool_pos_cb,
                                   self.__underfloor_heating_pool_calib_cb)

        # Air cooling valve.
        self.__attach_single_valve("air_cooling",
                                   self.__air_cooling_enabled_cb,
                                   self.__air_cooling_pos_cb,
                                   self.__air_cooling_calib_cb)

        # Ground drill valve.
        self.__attach_single_valve("ground_drill",
                                   self.__ground_drill_enabled_cb,
                                   self.__ground_drill_pos_cb,
                                   self.__ground_drill_calib_cb)

        # =========================== Generators Cooling (GREEN) ===========================
        # Generators Cooling valve.
        self.__attach_single_valve("generators_cooling",
                                   self.__generators_cooling_enabled_cb,
                                   self.__generators_cooling_pos_cb,
                                   self.__generators_cooling_calib_cb)

        # Short valve between green and purple pipes.
        self.__attach_single_valve("short_green_purple",
                                   self.__short_green_purple_enabled_cb,
                                   self.__short_green_purple_pos_cb,
                                   self.__short_green_purple_calib_cb)

        # Underfloor west bypass valve.
        self.__attach_single_valve("underfloor_west_bypass",
                                   self.__underfloor_west_bypass_enabled_cb,
                                   self.__underfloor_west_bypass_pos_cb,
                                   self.__underfloor_west_bypass_calib_cb)

        # Underfloor east bypass valve.
        self.__attach_single_valve("air_cooling",
                                   self.__underfloor_east_bypass_enabled_cb,
                                   self.__underfloor_east_bypass_pos_cb,
                                   self.__underfloor_east_bypass_calib_cb)

        # =========================== Valve Controll Groups ===========================
        reg_name = "{}.vcg_pool_heating.enabled".format(self.key)
        vcg_pool_heating = self._registers.by_name(reg_name)
        if vcg_pool_heating is not None:
            vcg_pool_heating.update_handlers = self.__vcg_pool_heating_enable_cb
            vcg_pool_heating.update()

        reg_name = "{}.vcg_tva_pool.enabled".format(self.key)
        vcg_tva_pool = self._registers.by_name(reg_name)
        if vcg_tva_pool is not None:
            vcg_tva_pool.update_handlers = self.__vcg_tva_pool_enable_cb
            vcg_tva_pool.update()

        reg_name = "{}.convectors_east.enabled".format(self.key)
        convectors_east = self._registers.by_name(reg_name)
        if convectors_east is not None:
            convectors_east.update_handlers = self.__convectors_east_enable_cb
            convectors_east.update()

        reg_name = "{}.underfloor_east.enabled".format(self.key)
        underfloor_east = self._registers.by_name(reg_name)
        if underfloor_east is not None:
            underfloor_east.update_handlers = self.__underfloor_east_enable_cb
            underfloor_east.update()

        reg_name = "{}.convectors_west.enabled".format(self.key)
        convectors_west = self._registers.by_name(reg_name)
        if convectors_west is not None:
            convectors_west.update_handlers = self.__convectors_west_enable_cb
            convectors_west.update()

        reg_name = "{}.tva_fitness.enabled".format(self.key)
        tva_fitness = self._registers.by_name(reg_name)
        if tva_fitness is not None:
            tva_fitness.update_handlers = self.__tva_fitness_enable_cb
            tva_fitness.update()

        reg_name = "{}.tva_roof_floor.enabled".format(self.key)
        tva_roof_floor = self._registers.by_name(reg_name)
        if tva_roof_floor is not None:
            tva_roof_floor.update_handlers = self.__tva_roof_floor_enable_cb
            tva_roof_floor.update()

        reg_name = "{}.floor_west.enabled".format(self.key)
        underfloor_west = self._registers.by_name(reg_name)
        if underfloor_west is not None:
            underfloor_west.update_handlers = self.__underfloor_west_enable_cb
            underfloor_west.update()

        reg_name = "{}.tva_conference_center.enabled".format(self.key)
        tva_conference_center = self._registers.by_name(reg_name)
        if tva_conference_center is not None:
            tva_conference_center.update_handlers = self.__vcg_tva_conference_center_enable_cb
            tva_conference_center.update()

        reg_name = "{}.convectors_kitchen.enabled".format(self.key)
        convectors_kitchen = self._registers.by_name(reg_name)
        if convectors_kitchen is not None:
            convectors_kitchen.update_handlers = self.__vcg_convectors_kitchen_enable_cb
            convectors_kitchen.update()

        reg_name = "{}.tva_warehouse.enabled".format(self.key)
        tva_warehouse = self._registers.by_name(reg_name)
        if tva_warehouse is not None:
            tva_warehouse.update_handlers = self.__vcg_tva_warehouse_enable_cb
            tva_warehouse.update()

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

        if self.__v_underfloor_heating_foyer is not None:
            self.__v_underfloor_heating_foyer.update()

        if self.__v_underfloor_heating_trestle is not None:
            self.__v_underfloor_heating_trestle.update()

        if self.__v_underfloor_heating_pool is not None:
            self.__v_underfloor_heating_pool.update()

        if self.__v_air_cooling is not None:
            self.__v_air_cooling.update()

        if self.__v_ground_drill is not None:
            self.__v_ground_drill.update()

        if self.__v_generators_cooling is not None:
            self.__v_generators_cooling.update()

        if self.__v_short_green_purple is not None:
            self.__v_short_green_purple.update()

        if self.__v_underfloor_west_bypass is not None:
            self.__v_underfloor_west_bypass.update()

        if self.__v_underfloor_east_bypass is not None:
            self.__v_underfloor_east_bypass.update()


        if self.__vcg_pool_heating is not None:
            self.__vcg_pool_heating.update()

        if self.__vcg_tva_pool is not None:
            self.__vcg_tva_pool.update()

        if self.__vcg_convectors_east is not None:
            self.__vcg_convectors_east.update()

        if self.__vcg_underfloor_east is not None:
            self.__vcg_underfloor_east.update()

        if self.__vcg_convectors_west is not None:
            self.__vcg_convectors_west.update()

        if self.__vcg_tva_fitness is not None:
            self.__vcg_tva_fitness.update()

        if self.__vcg_tva_roof_floor is not None:
            self.__vcg_tva_roof_floor.update()

        if self.__vcg_underfloor_west is not None:
            self.__vcg_underfloor_west.update()

        if self.__vcg_tva_conference_center is not None:
            self.__vcg_tva_conference_center.update()

        if self.__vcg_convectors_kitchen is not None:
            self.__vcg_convectors_kitchen.update()

        if self.__vcg_tva_warehouse is not None:
            self.__vcg_tva_warehouse.update()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

        if self.__v_underfloor_heating_foyer is not None:
            self.__v_underfloor_heating_foyer.shutdown()

        if self.__v_underfloor_heating_trestle is not None:
            self.__v_underfloor_heating_trestle.shutdown()

        if self.__v_underfloor_heating_pool is not None:
            self.__v_underfloor_heating_pool.shutdown()

        if self.__v_air_cooling is not None:
            self.__v_air_cooling.shutdown()

        if self.__v_ground_drill is not None:
            self.__v_ground_drill.shutdown()

        if self.__v_generators_cooling is not None:
            self.__v_generators_cooling.shutdown()

        if self.__v_short_green_purple is not None:
            self.__v_short_green_purple.shutdown()

        if self.__v_underfloor_west_bypass is not None:
            self.__v_underfloor_west_bypass.shutdown()

        if self.__v_underfloor_east_bypass is not None:
            self.__v_underfloor_east_bypass.shutdown()



        if self.__vcg_pool_heating is not None:
            self.__vcg_pool_heating.shutdown()

        if self.__vcg_tva_pool is not None:
            self.__vcg_tva_pool.shutdown()

        if self.__vcg_convectors_east is not None:
            self.__vcg_convectors_east.shutdown()

        if self.__vcg_underfloor_east is not None:
            self.__vcg_underfloor_east.shutdown()

        if self.__vcg_convectors_west is not None:
            self.__vcg_convectors_west.shutdown()

        if self.__vcg_tva_fitness is not None:
            self.__vcg_tva_fitness.shutdown()

        if self.__vcg_tva_roof_floor is not None:
            self.__vcg_tva_roof_floor.shutdown()

        if self.__vcg_underfloor_west is not None:
            self.__vcg_underfloor_west.shutdown()

        if self.__vcg_tva_conference_center is not None:
            self.__vcg_tva_conference_center.shutdown()

        if self.__vcg_convectors_kitchen is not None:
            self.__vcg_convectors_kitchen.shutdown()

        if self.__vcg_tva_warehouse is not None:
            self.__vcg_tva_warehouse.shutdown()

#endregion
