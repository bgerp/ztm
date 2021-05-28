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

    __v_foyer = None
    """Valve foyer.
    """

    __v_underfloor_heating_trestle = None
    """Underfloor heating trestle.
    """

    __v_underfloor_heating_pool = None
    """Underfloor heating pool.
    """

    __vcg_pool_heating = None
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

    __v_short_green_purple = None
    """Short valve between green and purple pipes.
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

        # TVA Pool (RED and BLUE)
        self.__vcg_tva_pool = ValveControlGroup.create(\
            name="TVA Pool",
            key="{}.vcg_tva_pool".format(self.key),
            controller=self._controller,
            registers=self._registers,
            fw_valves=["cold"],
            rev_valves=["hot"],
            fw_pumps=["pump"])

        return

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

        # Short valve between green and purple pipes.
        self.__v_short_green_purple = Valve(name="v_short_green_purple", controller=self._controller, registers=self._registers)

    def __del__(self):
        """Destructor
        """

        # Worm circle (PURPLE)
        if self.__v_foyer is not None:
            del self.__v_foyer

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

        if self.__v_short_green_purple is not None:
            del self.__v_short_green_purple

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#region Private Methods

    def __underfloor_heating_foyer_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__v_foyer is None:

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__v_foyer = ValveFactory.create(
                name="Valve Underfloor Heating Foyer", 
                controller=self._controller,
                params=params)

            if self.__v_foyer is not None:
                self.__v_foyer.init()

        elif register.value == verbal_const.OFF and self.__v_foyer is not None:
            self.__v_foyer.shutdown()
            del self.__v_foyer

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

        elif register.value == verbal_const.OFF and self.__v_foyer is not None:
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
                name="Valve Underfloor Heating Trestle", 
                controller=self._controller,
                params=params)

            if self.__v_underfloor_heating_pool is not None:
                self.__v_underfloor_heating_pool.init()

        elif register.value == verbal_const.OFF and self.__v_foyer is not None:
            self.__v_underfloor_heating_pool.shutdown()
            del self.__v_underfloor_heating_pool

    def __init_registers(self):

        # === Valve group. (PURPLE) ===

        underfloor_heating_foyer = self._registers.by_name("{}.underfloor_heating_foyer.valve.enabled".format(self.key))
        if underfloor_heating_foyer is not None:
                underfloor_heating_foyer.update_handlers = self.__underfloor_heating_foyer_enabled_cb
                underfloor_heating_foyer.update()

        underfloor_heating_trestle = self._registers.by_name("{}.underfloor_heating_trestle.valve.enabled".format(self.key))
        if underfloor_heating_trestle is not None:
                underfloor_heating_trestle.update_handlers = self.__underfloor_heating_trestle_enabled_cb
                underfloor_heating_trestle.update()

        underfloor_heating_pool = self._registers.by_name("{}.underfloor_heating_pool.valve.enabled".format(self.key))
        if underfloor_heating_pool is not None:
                underfloor_heating_pool.update_handlers = self.__underfloor_heating_pool_enabled_cb
                underfloor_heating_pool.update()


#endregion

#region Properties

#endregion

#region Public Methods

    def init(self):
        """Init the plugin.
        """

        self.__init_registers()

        # Valve Control Groups (RED and BLUE)
        self.__vcg_pool_heating.init()
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

        # Short valve between green and purple pipes.
        self.__v_short_green_purple.init()

    def update(self):
        """Update the plugin state.
        """

        self.__v_foyer.update()
        self.__v_underfloor_heating_trestle.update()
        self.__v_underfloor_heating_pool.update()

        # Valve Control Groups
        self.__vcg_pool_heating.update()
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

        # Short valve between green and purple pipes.
        self.__v_short_green_purple.update()

    def shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

        # Valves
        self.__v_foyer.shutdown()
        self.__v_underfloor_heating_trestle.shutdown()
        self.__v_underfloor_heating_pool.shutdown()

        # Valve Control Groups
        self.__vcg_pool_heating.shutdown()
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

        # Short valve between green and purple pipes.
        self.__v_short_green_purple.shutdown()

#endregion
