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
from utils.timer import Timer

from plugins.base_plugin import BasePlugin
from plugins.ec.heat_pump_mode import HeatPumpMode

from devices.base_device import BaseDevice

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


class Boiler(BaseDevice):
    """Boiler.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __heat = 0
    """Debit of the pump.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_heat(self, debit):

        self.__debit = debit

        self.__logger.debug("Set the heat of {} to {}".format(self.name, self.__debit))

    def init(self):

        self.__logger.debug("Init the: {}".format(self.name))

    def shutdown(self):

        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):

        self.__logger.debug("The heat of {} is {}.".format(self.name, self.__debit))

#endregion


class WaterPump(BaseDevice):
    """Water pump.
    """

#region Attributes

    __logger = None
    """Logger
    """

    __debit = 0
    """Debit of the pump.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_debit(self, debit):

        self.__debit = debit

        self.__logger.debug("Set the debit of {} to {}".format(self.name, self.__debit))

    def init(self):

        self.__logger.debug("Init the: {}".format(self.name))

    def shutdown(self):

        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):

        self.__logger.debug("The debit of {} is {}.".format(self.name, self.__debit))

#endregion


class Valve(BaseDevice):

#region Attributes

    __logger = None
    """Logger
    """

    __position = 0
    """Position of the valve.
    """    

#endregion

#region Constructor / Destructor

    def __init__(self, **config):

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_position(self, position):
        """Set the position of the valve.

        Args:
            position (int): Position of the valve.
        """

        self.__position = position
        self.__logger.debug("Set position of {} to {}".format(self.name, position))

    def init(self):
        """Init the valve.
        """

        self.__logger.debug("Init the: {}".format(self.name))

    def shutdown(self):
        """Shutdown the valve.
        """

        self.set_position(0)
        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):
        """Update the valve state.
        """

        self.__logger.debug("Valve {} is on position {}.".format(self.name, self.__position))

#endregion


class ValveControlGroup(BaseDevice):

#region Attributes

    __logger = None
    """Logger
    """

    __input_valve = None
    """Input valve.
    """

    __output_valve = None
    """Output valve.
    """

    __short_valve = None
    """Short valve.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        if "input" in config:
            self.__input_valve = config["input"]

        if "output" in config:
            self.__output_valve = config["output"]

        if "short" in config:
            self.__short_valve = config["short"]

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_position(self, position):

        if self.__input_valve is not None:
            self.__input_valve.set_position(position)

        if self.__output_valve is not None:
            self.__output_valve.set_position(position)

        if self.__short_valve is not None:
            self.__short_valve.set_position(-position)

    def init(self):
        """Init the group.
        """

        if self.__input_valve is not None:
            self.__input_valve.init()

        if self.__output_valve is not None:
            self.__output_valve.init()

        if self.__short_valve is not None:
            self.__short_valve.init()

    def shutdown(self):
        """Shutdown the group.
        """

        if self.__input_valve is not None:
            self.__input_valve.shutdown()

        if self.__output_valve is not None:
            self.__output_valve.shutdown()

        if self.__short_valve is not None:
            self.__short_valve.shutdown()

    def update(self):
        """Update valve state.
        """

        if self.__input_valve is not None:
            self.__input_valve.update()

        if self.__output_valve is not None:
            self.__output_valve.update()

        if self.__short_valve is not None:
            self.__short_valve.update()

#endregion


class TempSwitch(BaseDevice):

#region Attributes

    __logger = None
    """Logger
    """

    __v_cold = None
    """Valve cold water.
    """    

    __v_hot = None
    """Valve hot water.
    """ 

    __position = 0
    """Position
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

        if "v_hot" in config:
            self.__v_hot = config["v_hot"]

        if "v_cold" in config:
            self.__v_cold = config["v_cold"]

    def __del__(self):
        """Destructor
        """

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Public Methods

    def set_position(self, position):
        """Set position of the 

        Args:
            position ([type]): [description]
        """

        if self.__position != position:
            self.__position = position


        if self.__v_hot is not None:
            self.__v_hot.set_position(self.__position)

        if self.__v_cold is not None:
            self.__v_cold.set_position(-self.__position)

    def init(self):

        self.__logger.debug("Init the: {}".format(self.name))

    def shutdown(self):

        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):

        self.__logger.debug("The heat of {} is {}.".format(self.name, self.__position))

#endregion


class HeatPump(BaseDevice):

#region Attributes

    __logger = None
    """Logger
    """

    __mode = HeatPumpMode.NONE
    """Mode of the heat pump.
    """

    __power = 0
    """Power of the pump.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the: {}".format(self.name))

    def __del__(self):
        """Destructor
        """

        super().__del__()

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

        self.__logger.debug(self.__mode.name)

    def set_power(self, power):
        """Set heat pump power.

        Args:
            power (int): Power of the machine.
        """

        if self.__power == power:
            return

        self.__power = power

        self.__logger.debug(self.__power)

    def init(self):
        """Init the heat pump.
        """

        self.__logger.debug("Init the: {}".format(self.name))

    def shutdown(self):
        """Shutdown the heat pump.
        """

        self.set_power(0)
        self.__logger.debug("Shutdown the: {}".format(self.name))

    def update(self):
        """Update heat pump state.
        """

        self.__logger.debug("Het pump mode: {} and power {}".format(self.__mode.name, self.__power))

#endregion


class HeatPumpControllGroup(BaseDevice):

#region Attributes

    _registers = None

    __mode = HeatPumpMode.NONE
    """Mode of the heat pump.
    """

    __power = 0
    """Power of the pump.
    """

    __v_cold_buff = None

    __v_cold_geo = None

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

        # Valve group cold buffer. (Blue)
        v_cold_buff_input = Valve(name="v_cold_buff_input", controller=self._controller, registers=self._registers)
        v_cold_buff_output = Valve(name="v_cold_buff_output", controller=self._controller, registers=self._registers)
        v_cold_buff_short = Valve(name="v_cold_buff_short", controller=self._controller, registers=self._registers)
        self.__v_cold_buff = ValveControlGroup(name="v_cold_buff", input=v_cold_buff_input, output=v_cold_buff_output, short=v_cold_buff_short)
        
        # Valve group cold geo. (Green)
        v_cold_geo_input = Valve(name="v_cold_geo_input", controller=self._controller, registers=self._registers)
        v_cold_geo_output = Valve(name="v_cold_geo_output", controller=self._controller, registers=self._registers)
        v_cold_geo_short = Valve(name="v_cold_geo_short", controller=self._controller, registers=self._registers)
        self.__v_cold_geo = ValveControlGroup(name="v_cold_geo", input=v_cold_geo_input, output=v_cold_geo_output, short=v_cold_geo_short)

        # Valve group warm geo. (Green)
        v_warm_geo_input = Valve(name="v_warm_geo_input", controller=self._controller, registers=self._registers)
        v_warm_geo_output = Valve(name="v_warm_geo_output", controller=self._controller, registers=self._registers)
        v_warm_geo_short = Valve(name="v_warm_geo_short", controller=self._controller, registers=self._registers)
        self.__v_warm_geo = ValveControlGroup(name="v_warm_geo", input=v_warm_geo_input, output=v_warm_geo_output, short=v_warm_geo_short)

        # Valve group warm floor. (Purple)
        v_warm_floor_input = Valve(name="v_warm_floor_input", controller=self._controller, registers=self._registers)
        v_warm_floor_output = Valve(name="v_warm_floor_output", controller=self._controller, registers=self._registers)
        v_warm_floor_short = Valve(name="v_warm_floor_short", controller=self._controller, registers=self._registers)
        self.__v_warm_floor = ValveControlGroup(name="v_warm_floor", input=v_warm_floor_input, output=v_warm_floor_output, short=v_warm_floor_short)

        # Valve group hot. (Red)
        v_hot_input = Valve(name="v_hot_input", controller=self._controller, registers=self._registers)
        v_hot_output = Valve(name="v_hot_output", controller=self._controller, registers=self._registers)
        self.__v_hot = ValveControlGroup(name="v_hot", input=v_hot_input, output=v_hot_output)

        self.__cold_water_pump = WaterPump(name="cold_water_pump", controller=self._controller, registers=self._registers)
        self.__hot_water_pump = WaterPump(name="hot_water_pump", controller=self._controller, registers=self._registers)
        self.__warm_water_pump = WaterPump(name="warm_water_pump", controller=self._controller, registers=self._registers)

        self.__heat_pump = HeatPump(name=self._config["name"], controller=self._controller, registers=self._registers)

    def __del__(self):
        """Destructor
        """

        super().__del__()

        # Valve groups.
        del self.__v_cold_buff
        del self.__v_cold_geo
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

        # Valve groups.
        self.__v_cold_buff.init()
        self.__v_cold_geo.init()
        self.__v_warm_geo.init()
        self.__v_warm_floor.init()
        self.__v_hot.init()

        # Thermal agents pumps.
        self.__cold_water_pump.init()
        self.__hot_water_pump.init()
        self.__warm_water_pump.init()

        # Heat pump.
        self.__heat_pump.init()

    def shutdown(self):

        # Valve groups.
        self.__v_cold_buff.shutdown()
        self.__v_cold_geo.shutdown()
        self.__v_warm_geo.shutdown()
        self.__v_warm_floor.shutdown()
        self.__v_hot.shutdown()

        # Thermal agents pumps.
        self.__cold_water_pump.shutdown()
        self.__hot_water_pump.shutdown()
        self.__warm_water_pump.shutdown()

        # Heat pump.
        self.__heat_pump.shutdown()

    def update(self):

        # Valve groups.
        self.__v_cold_buff.update()
        self.__v_cold_geo.update()
        self.__v_warm_geo.update()
        self.__v_warm_floor.update()
        self.__v_hot.update()

        # Thermal agents pumps.
        self.__cold_water_pump.update()
        self.__hot_water_pump.update()
        self.__warm_water_pump.update()

        # Heat pump.
        self.__heat_pump.update()
        # self.__logger.info("Update: {}".format(self.name))

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

    __v_tva_pool = None
    """TVA pool.
    """

    __v_convectors_east = None
    """Convectors east.
    """

    __v_floor_east = None
    """Floor east.
    """

    __v_convectors_west = None
    """Convectors west.
    """

    __v_tva_fitness = None
    """TVA fitness.
    """

    __v_tva_roof_floor = None
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

        self.__heat_pumps.append(HeatPumpControllGroup(name="HP1", controller=self._controller, registers=self._registers))
        self.__heat_pumps.append(HeatPumpControllGroup(name="HP2", controller=self._controller, registers=self._registers))
        self.__heat_pumps.append(HeatPumpControllGroup(name="HP3", controller=self._controller, registers=self._registers))

        # Valve group. (Purple)
        self.__v_foyer = Valve(name="v_foyer", controller=self._controller, registers=self._registers)
        self.__v_underfloor_heating_trestle  = Valve(name="v_underfloor_heating_trestle", controller=self._controller, registers=self._registers)
        self.__v_underfloor_heating_pool  = Valve(name="v_underfloor_heating_pool", controller=self._controller, registers=self._registers)

        # 
        self.__v_pool_heating = Valve(name="v_pool_heating", controller=self._controller, registers=self._registers)
        self.__v_tva_pool = TempSwitch(name="v_tva_pool", controller=self._controller, registers=self._registers)
        self.__v_convectors_east = TempSwitch(name="v_convectors_east", controller=self._controller, registers=self._registers)
        self.__v_floor_east = TempSwitch(name="v_floor_east", controller=self._controller, registers=self._registers)
        self.__v_convectors_west = TempSwitch(name="v_convectors_west", controller=self._controller, registers=self._registers)
        self.__v_tva_fitness = TempSwitch(name="v_tva_fitness", controller=self._controller, registers=self._registers)
        self.__v_tva_roof_floor = TempSwitch(name="v_tva_roof_floor", controller=self._controller, registers=self._registers)
        self.__v_floor_west = TempSwitch(name="v_floor_west", controller=self._controller, registers=self._registers)
        self.__v_tva_conference_center = TempSwitch(name="v_tva_conference_center", controller=self._controller, registers=self._registers)
        self.__v_convectors_kitchen = TempSwitch(name="v_convectors_kitchen", controller=self._controller, registers=self._registers)
        self.__v_tva_warehouse = TempSwitch(name="v_tva_warehouse", controller=self._controller, registers=self._registers)

        self.__v_generators_cooling = Valve(name="v_generators_cooling", controller=self._controller, registers=self._registers)
        self.__v_air_cooling = Valve(name="v_generators_cooling", controller=self._controller, registers=self._registers)
        self.__v_ = Valve(name="v_generators_cooling", controller=self._controller, registers=self._registers)

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

        if self.__heat_pumps is not None:
            del self.__heat_pumps

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

        if self.__v_tva_pool is not None:
            del self.__v_tva_pool

        if self.__v_convectors_east is not None:
            del self.__v_convectors_east

        if self.__v_floor_east is not None:
            del self.__v_floor_east

        if self.__v_convectors_west is not None:
            del self.__v_convectors_west

        if self.__v_tva_fitness is not None:
            del self.__v_tva_fitness

        if self.__v_tva_roof_floor is not None:
            del self.__v_tva_roof_floor

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

        # 
        for heat_pump in self.__heat_pumps:
            heat_pump.init()
            heat_pump.set_mode(HeatPumpMode.NONE)
            heat_pump.set_power(0)

        # 
        self.__v_foyer.init()
        self.__v_underfloor_heating_trestle.init()
        self.__v_underfloor_heating_pool.init()

        # 
        self.__v_pool_heating.init()
        self.__v_tva_pool.init()
        self.__v_convectors_east.init()
        self.__v_floor_east.init()
        self.__v_convectors_west.init()
        self.__v_tva_fitness.init()
        self.__v_tva_roof_floor.init()
        self.__v_floor_west.init()
        self.__v_tva_conference_center.init()
        self.__v_convectors_kitchen.init()
        self.__v_tva_warehouse.init()

        # Generator
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

        # 
        self.__v_pool_heating.update()
        self.__v_tva_pool.update()
        self.__v_convectors_east.update()
        self.__v_floor_east.update()
        self.__v_convectors_west.update()
        self.__v_tva_fitness.update()
        self.__v_tva_roof_floor.update()
        self.__v_floor_west.update()
        self.__v_tva_conference_center.update()
        self.__v_convectors_kitchen.update()
        self.__v_tva_warehouse.update()

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

        # 
        self.__v_pool_heating.shutdown()
        self.__v_tva_pool.shutdown()
        self.__v_convectors_east.shutdown()
        self.__v_floor_east.shutdown()
        self.__v_convectors_west.shutdown()
        self.__v_tva_fitness.shutdown()
        self.__v_tva_roof_floor.shutdown()
        self.__v_floor_west.shutdown()
        self.__v_tva_conference_center.shutdown()
        self.__v_convectors_kitchen.shutdown()
        self.__v_tva_warehouse.shutdown()

        # Generator
        self.__v_generators_cooling.shutdown()

#endregion
