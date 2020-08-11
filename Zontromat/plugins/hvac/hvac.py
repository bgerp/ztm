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

from enum import Enum

from utils.logger import get_logger
from utils.utils import l_scale
from utils.state_machine import StateMachine
from utils.timer import Timer
from utils.temp_processor import TemperatureProcessor

from plugins.base_plugin import BasePlugin

from devices.HangzhouAirflowElectricApplications.f3p146ec072600 import F3P146EC072600
from devices.TONHE.a20m15b2c import A20M15B2C
from devices.SILPA.klimafan import Klimafan
from devices.no_vendor.flowmeter import Flowmeter
from devices.Dallas.ds18b20 import DS18B20
from devices.tests.leak_test.leak_test import LeakTest
from devices.tests.electrical_performance.electrical_performance import ElectricalPerformance

from data import verbal_const

from services.global_error_handler.global_error_handler import GlobalErrorHandler

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
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

class ThermalMode(Enum):
    """Thermal modes description."""

    NONE = 0
    COLD_SEASON = 1
    TRANSISION_SEASON = 2
    WARM_SEASON = 3

class HVAC(BasePlugin):
    """Heating ventilation and air conditioning."""

#region Attributes

    __logger = None
    """Logger"""

    __temp_proc = None
    """Temperature processor."""

    __air_temp_upper_dev = None
    """Air thermometer upper."""

    __air_temp_cent_dev = None
    """Air thermometer central."""

    __air_temp_lower_dev = None
    """Air thermometer lower."""

    __convector_dev = None
    """Convector device."""

    __loop1_fan_dev = None
    """Loop 3 fan device."""

    __loop1_temp_dev = None
    """Loop 2 thermometer."""

    __loop1_valve_dev = None
    """Loop 1 valve device."""

    __loop1_cnt_dev = None
    """Loop 1 flow metter."""

    __loop2_fan_dev = None
    """Loop 1 fan device."""

    __loop2_temp_dev = None
    """Loop 2 thermometer."""

    __loop2_valve_dev = None
    """Loop 2 valve device."""

    __loop2_cnt_dev = None
    """Loop 2 flow metter."""


    __thermal_mode = None
    """Thermal mode of the HVAC."""

    __update_timer = None
    """Main process update timer."""

    __loop1_leak_test = None
    """Loop 1 leak test."""

    __loop2_leak_teat = None
    """Loop 2 leak test."""

    __thermal_force_limit = 0
    """Limit thermal force."""



    __delta_time = 1
    """Конфигурационен параметър, показващ за какво време
    назад се отчита изменението на температурата.
    Limits: (1 - 3)"""

    __adjust_temp = 0
    """Зададено отклонение от температурата
    (задава се от дисплея до вратата или през мобилен телефон, вързан в локалната мрежа)
    Limits: (-2.5 : 2.5)"""

    __goal_building_temp = 0
    """Целева температура на сградата.
    (подава се от централния сървър)
    Limits: (18-26)"""

    __delta_temp = 0
    """Изменението на температурата от последните минути.
    Limits: (-3 : 3)"""

    __thermal_force = 0
    """Каква топлинна сила трябва да приложим към системата
    (-100% означава максимално да охлаждаме, +100% - максимално да отопляваме)"""

    __update_rate = 5
    """Update rate in seconds."""

#endregion

#region Properties

    @property
    def temperature(self):
        """Measure temperature from the sensors.

            Средна температура на стаята.
            (измерва се от датчиците)
            Limits: (0-40)

        Returns
        -------
        float
            Actual temperature in the room.
        """

        # return the temperature.
        return self.__temp_proc.value

#endregion

#region Destructor

    def __del__(self):
        """Destructor"""

        del self.__loop1_fan_dev
        del self.__loop1_temp_dev
        del self.__loop1_valve_dev
        del self.__loop1_cnt_dev
        del self.__loop2_fan_dev
        del self.__loop2_temp_dev
        del self.__loop2_valve_dev
        del self.__loop2_cnt_dev
        del self.__thermal_mode
        del self.__update_timer
        del self.__loop1_leak_test
        del self.__loop2_leak_teat
        del self.__logger

#endregion

#region Private Methods (Parameters callbacks)

    def __update_rate_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return
        
        if self.__update_rate != register.value:
            self.__update_rate = register.value

    def __delta_time_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return
        
        if self.__delta_time != register.value:
            self.__delta_time = register.value

    def __thermal_mode_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return
        
        mode = ThermalMode(register.value)

        if not self.__thermal_mode.is_state(mode):
            self.__thermal_mode.set_state(ThermalMode(register.value))

    def __thermal_force_limit_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return
        
        if self.__thermal_force_limit != register.value:
            self.__thermal_force_limit = register.value

    def __adjust_temp_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__adjust_temp == register.value:
            return

        # @see https://experta.bg/L/S/122745/m/Fwntindd
        min_temp = 2.5
        max_temp = -2.5

        min_temp_reg = self._registers.by_name(self._key + ".temp.min")
        if min_temp_reg is not None:
            if min_temp_reg.is_int_or_float():
                min_temp = min_temp_reg.value

        max_temp_reg = self._registers.by_name(self._key + ".temp.max")
        if max_temp_reg is not None:
            if max_temp_reg.is_int_or_float():
                max_temp = max_temp_reg.value

        actual_temp = register.value

        if actual_temp < min_temp:
            actual_temp = min_temp

        if actual_temp > max_temp:
            actual_temp = max_temp

        self.__adjust_temp = actual_temp

    def __goal_building_temp_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        # @see https://experta.bg/L/S/122745/m/Fwntindd
        min_temp = 18
        max_temp = 26

        actual_temp = register.value

        if actual_temp < min_temp:
            actual_temp = min_temp

        if actual_temp > max_temp:
            actual_temp = max_temp

        self.__goal_building_temp = actual_temp

#endregion

#region Private Methods (Thermometers callbacks)

    def __air_temp_cent_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__air_temp_cent_dev is None:

            self.__air_temp_cent_dev = DS18B20.create(\
                "Air temperature lower",\
                self._key + ".air_temp_cent",\
                register.value,\
                self._controller)

            if self.__air_temp_cent_dev is not None:
                self.__air_temp_cent_dev.init()
                self.__temp_proc.add(self.__air_temp_cent_dev)

        elif register.value == verbal_const.OFF and self.__air_temp_cent_dev is not None:

            self.__temp_proc.add(self.__air_temp_cent_dev)
            self.__air_temp_cent_dev.shutdown()
            del self.__air_temp_cent_dev

    def __air_temp_lower_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__air_temp_lower_dev is None:
            self.__air_temp_lower_dev = DS18B20.create(\
                "Air temperature lower",\
                self._key + ".air_temp_lower",\
                register.value,\
                self._controller)

            if self.__air_temp_lower_dev is not None:
                self.__air_temp_lower_dev.init()
                self.__temp_proc.add(self.__air_temp_lower_dev)

        elif register.value == verbal_const.OFF and self.__air_temp_lower_dev is not None:

            self.__temp_proc.remove(self.__air_temp_lower_dev)
            self.__air_temp_lower_dev.shutdown()
            del self.__air_temp_lower_dev

    def __air_temp_upper_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__air_temp_upper_dev is None:
            self.__air_temp_upper_dev = DS18B20.create(\
                "Air temperature upper",\
                self._key + ".air_temp_upper",\
                register.value,\
                self._controller)

            if self.__air_temp_upper_dev is not None:
                self.__air_temp_upper_dev.init()
                self.__temp_proc.add(self.__air_temp_upper_dev)

        elif register.value == verbal_const.OFF and self.__air_temp_upper_dev is not None:

            self.__temp_proc.remove(self.__air_temp_upper_dev)
            self.__air_temp_upper_dev.shutdown()
            del self.__air_temp_upper_dev

#endregion

#region Private Methods (Convector callbacks)

    def __convector_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__convector_dev is None:
            self.__convector_dev = Klimafan.create(\
                "Convector 1",\
                self._key + ".convector",\
                self._registers,\
                self._controller)

            if self.__convector_dev is not None:
                self.__convector_dev.init()

        elif register.value == verbal_const.OFF and self.__convector_dev is not None:
            self.__convector_dev.shutdown()
            del self.__convector_dev

#endregion

#region Private Methods (Loop 1 callbacks)

    def __loop1_cnt_input_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop1_cnt_dev is None:
            self.__loop1_cnt_dev = Flowmeter.create(\
                "Loop 2 flowmeter",\
                self._key + ".loop2.cnt",\
                self._registers,\
                self._controller)

            if self.__loop1_cnt_dev is not None:
                self.__loop1_cnt_dev.init()

                # 20 seconds is time for leak testing.
                self.__loop1_leak_test = LeakTest(self.__loop1_cnt_dev, 20)
                self.__loop1_leak_test.on_result(self.__loop1_leaktest_result)

        elif register.value == verbal_const.OFF and self.__loop1_cnt_dev is not None:
            self.__loop1_cnt_dev.shutdown()
            del self.__loop1_cnt_dev
            del self.__loop1_leak_test

    def __loop1_fan_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop1_fan_dev is None:
            # Filter by model.
            if "f3p146ec072600" in register.value:
                self.__loop1_fan_dev = F3P146EC072600.create(\
                    "Loop 1 fan",\
                    self._key + ".loop1.fan",\
                    self._registers,\
                    self._controller)

            if self.__loop1_fan_dev is not None:
                self.__loop1_fan_dev.init()

        elif register.value == verbal_const.OFF and self.__loop1_fan_dev is not None:
            self.__loop1_fan_dev.shutdown()
            del self.__loop1_fan_dev

    def __loop1_fan_min_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__loop1_fan_dev is not None:
            if self.__loop1_fan_dev.min_speed != register.value:
                self.__loop1_fan_dev.min_speed = register.value

    def __loop1_fan_max_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__loop1_fan_dev is not None:
            if self.__loop1_fan_dev.max_speed != register.value:
                self.__loop1_fan_dev.max_speed = register.value

    def __loop1_temp_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop1_temp_dev is None:
            self.__loop1_temp_dev = DS18B20.create(\
                "Loop 1 temperature",\
                self._key + ".loop1.temp",\
                register.value,\
                self._controller)

            if self.__loop1_temp_dev is not None:
                self.__loop1_temp_dev.init()

        elif register.value == verbal_const.OFF and self.__loop1_temp_dev is not None:
            self.__loop1_temp_dev.shutdown()
            del self.__loop1_temp_dev

    def __loop1_valve_enabled_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop1_valve_dev is None:
            self.__loop1_valve_dev = A20M15B2C.create(\
                "Loop 1 valve",\
                self._key + ".loop1.valve",\
                self._registers,\
                self._controller)

            if self.__loop1_valve_dev is not None:
                self.__loop1_valve_dev.init()

        elif register.value == verbal_const.OFF and self.__loop1_valve_dev is not None:
            self.__loop1_valve_dev.shutdown()
            del self.__loop1_valve_dev

#endregion

#region Private Methods (Loop 2 callbacks)

    def __loop2_cnt_input_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop2_cnt_dev is None:
            self.__loop2_cnt_dev = Flowmeter.create(\
                "Loop 2 flowmeter",\
                self._key + ".loop2.cnt",\
                self._registers,\
                self._controller)

            if self.__loop2_cnt_dev is not None:
                self.__loop2_cnt_dev.init()

                self.__loop2_leak_teat = LeakTest(self.__loop2_cnt_dev, 20)
                self.__loop2_leak_teat.on_result(self.__loop2_leaktest_result)

        elif register.value == verbal_const.OFF and self.__loop2_cnt_dev is not None:
            self.__loop2_cnt_dev.shutdown()
            del self.__loop2_cnt_dev
            del self.__loop2_leak_teat

    def __loop2_fan_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop2_fan_dev is None:
            # Filter by model.
            if "f3p146ec072600" in register.value:
                self.__loop2_fan_dev = F3P146EC072600.create(\
                    "Loop 2 fan",\
                    self._key + ".loop2.fan",\
                    self._registers,\
                    self._controller)

            if self.__loop2_fan_dev is not None:
                self.__loop2_fan_dev.init()

        elif register.value == verbal_const.OFF and self.__loop2_fan_dev is not None:
            self.__loop2_fan_dev.shutdown()
            del self.__loop2_fan_dev

    def __loop2_fan_min_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__loop2_fan_dev is not None:
            if self.__loop2_fan_dev.min_speed != register.value:
                self.__loop2_fan_dev.min_speed = register.value

    def __loop2_fan_max_cb(self, register):

        # Check data type.
        if not register.is_int_or_float():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__loop2_fan_dev is not None:
            if self.__loop2_fan_dev.max_speed != register.value:
                self.__loop2_fan_dev.max_speed = register.value

    def __loop2_temp_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop2_temp_dev is None:
            self.__loop2_temp_dev = DS18B20.create(\
                "Loop 2 temperature",\
                self._key + ".loop2.temp",\
                register.value,\
                self._controller)

            if self.__loop2_temp_dev is not None:
                self.__loop2_temp_dev.init()

        elif register.value == verbal_const.OFF and self.__loop2_temp_dev is not None:
            self.__loop2_temp_dev.shutdown()
            del self.__loop2_temp_dev

    def __loop2_valve_settings_cb(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop2_valve_dev is None:
            self.__loop2_valve_dev = A20M15B2C.create(\
                "Loop 2 valve",\
                self._key + ".loop2.valve",\
                self._registers,\
                self._controller)

            if self.__loop2_valve_dev is not None:
                self.__loop2_valve_dev.init()

        elif register.value == verbal_const.OFF and self.__loop2_valve_dev is not None:
            self.__loop2_valve_dev.shutdown()
            del self.__loop2_valve_dev

#endregion

#region Private Methods (Leak tests)

    def __loop1_leaktest_result(self, leaked_liters):
        if leaked_liters > 0:
            self.__logger.error("Loop 1 leak detected liters: {}".format(leaked_liters))

    def __loop2_leaktest_result(self, leaked_liters):
        if leaked_liters > 0:
            self.__logger.error("Loop 2 leak detected liters: {}".format(leaked_liters))

#endregion

#region Private Methods

    def __thermal_mode_on_change(self, machine):
        self.__logger.info("Thermal mode: {}".format(machine.get_state()))

    def __set_thermal_force(self, thermal_force):
        """ Apply thermal force to the devices. """

        # 7. Лимитираме Термалната сила в интервала -100 : + 100:
        if thermal_force < -100:
            thermal_force = -100
        if thermal_force > 100:
            thermal_force = 100

        self.__logger.debug("Mode: {}; TForce: {:3.3f}"\
            .format(self.__thermal_mode.get_state(), thermal_force))

        if self.__thermal_mode.is_state(ThermalMode.COLD_SEASON):
            if thermal_force > 0:
                self.__loop1_valve_dev.set_pos(0)
                self.__loop2_valve_dev.set_pos(0)
            elif thermal_force <= 0:
                self.__loop1_valve_dev.set_pos(100)
                self.__loop2_valve_dev.set_pos(100)

        elif self.__thermal_mode.is_state(ThermalMode.TRANSISION_SEASON):
            if thermal_force < 0:
                self.__loop1_valve_dev.set_pos(100)
                self.__loop2_valve_dev.set_pos(0)
            elif thermal_force > 0:
                self.__loop1_valve_dev.set_pos(0)
                self.__loop2_valve_dev.set_pos(100)
            else:
                self.__loop1_valve_dev.set_pos(0)
                self.__loop2_valve_dev.set_pos(0)

        elif self.__thermal_mode.is_state(ThermalMode.WARM_SEASON):
            if thermal_force < 0:
                self.__loop1_valve_dev.set_pos(100)
                self.__loop2_valve_dev.set_pos(100)
            elif thermal_force > 0:
                self.__loop1_valve_dev.set_pos(0)
                self.__loop2_valve_dev.set_pos(0)

        # If thermal mode set properly apply thermal force
        if not self.__thermal_mode.is_state(ThermalMode.NONE):
            # Set upper fan.
            if thermal_force < 0:
                self.__loop1_fan_dev.set_speed(abs(thermal_force))
            else:
                self.__loop1_fan_dev.set_speed(0)

            # Set lowe fan.
            if thermal_force > 0:
                self.__loop2_fan_dev.set_speed(abs(thermal_force))
            else:
                self.__loop2_fan_dev.set_speed(0)

            # Set convector fan.
            conv_tf = l_scale(thermal_force, [0, 100], [0, 3])
            conv_tf = int(conv_tf)
            # self.__convector_dev.set_state(abs(conv_tf))

#endregion

#region Public Methods

    def init(self):
        """Init the HVAC."""

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        # Create temperature processor.
        self.__temp_proc = TemperatureProcessor()

        # Create thermal mode.
        self.__thermal_mode = StateMachine(ThermalMode.NONE)
        self.__thermal_mode.on_change(self.__thermal_mode_on_change)
        self.__update_timer = Timer(self.__update_rate)

        # Region parameters
        update_rate = self._registers.by_name(self._key + ".update_rate")
        if update_rate is not None:
            update_rate.update_handler = self.__update_rate_cb

        delta_time = self._registers.by_name(self._key + ".delta_time")
        if delta_time is not None:
            delta_time.update_handler = self.__delta_time_cb

        thermal_mode = self._registers.by_name(self._key + ".thermal_mode")
        if thermal_mode is not None:
            thermal_mode.update_handler = self.__thermal_mode_cb

        thermal_force_limit = self._registers.by_name(self._key + ".thermal_force_limit")
        if thermal_force_limit is not None:
            thermal_force_limit.update_handler = self.__thermal_force_limit_cb

        adjust_temp = self._registers.by_name(self._key + ".adjust_temp")
        if adjust_temp is not None:
            adjust_temp.update_handler = self.__adjust_temp_cb

        goal_building_temp = self._registers.by_name(self._key + ".goal_building_temp")
        if goal_building_temp is not None:
            goal_building_temp.update_handler = self.__goal_building_temp_cb

        # Air temperatures.
        air_temp_cent_enabled = self._registers.by_name(self._key + ".air_temp_cent.settings")
        if air_temp_cent_enabled is not None:
            air_temp_cent_enabled.update_handler = self.__air_temp_cent_settings_cb

        air_temp_lower_enabled = self._registers.by_name(self._key + ".air_temp_lower.settings")
        if air_temp_lower_enabled is not None:
            air_temp_lower_enabled.update_handler = self.__air_temp_lower_settings_cb

        air_temp_upper_enabled = self._registers.by_name(self._key + ".air_temp_upper.settings")
        if air_temp_upper_enabled is not None:
            air_temp_upper_enabled.update_handler = self.__air_temp_upper_settings_cb

        # Convector
        convector_enable = self._registers.by_name(self._key + ".convector.settings")
        if convector_enable is not None:
            convector_enable.update_handler = self.__convector_settings_cb

        # Loop 1
        loop1_cnt_enabled = self._registers.by_name(self._key + ".loop1.cnt.input")
        if loop1_cnt_enabled is not None:
            loop1_cnt_enabled.update_handler = self.__loop1_cnt_input_cb

        loop1_fan_enabled = self._registers.by_name(self._key + ".loop1.fan.settings")
        if loop1_fan_enabled is not None:
            loop1_fan_enabled.update_handler = self.__loop1_fan_settings_cb

        loop1_fan_min = self._registers.by_name(self._key + ".loop1.fan.min_speed")
        if loop1_fan_min is not None:
            loop1_fan_min.update_handler = self.__loop1_fan_min_cb

        loop1_fan_max = self._registers.by_name(self._key + ".loop1.fan.max_speed")
        if loop1_fan_max is not None:
            loop1_fan_max.update_handler = self.__loop1_fan_max_cb

        loop1_temp_enabled = self._registers.by_name(self._key + ".loop1.temp.settings")
        if loop1_temp_enabled is not None:
            loop1_temp_enabled.update_handler = self.__loop1_temp_settings_cb

        loop1_valve_enabled = self._registers.by_name(self._key + ".loop1.valve.settings")
        if loop1_valve_enabled is not None:
            loop1_valve_enabled.update_handler = self.__loop1_valve_enabled_cb

        # Loop 2
        loop2_cnt_enabled = self._registers.by_name(self._key + ".loop2.cnt.input")
        if loop2_cnt_enabled is not None:
            loop2_cnt_enabled.update_handler = self.__loop2_cnt_input_cb

        loop2_fan_enabled = self._registers.by_name(self._key + ".loop2.fan.settings")
        if loop2_fan_enabled is not None:
            loop2_fan_enabled.update_handler = self.__loop2_fan_settings_cb

        loop2_fan_min = self._registers.by_name(self._key + ".loop2.fan.min_speed")
        if loop2_fan_min is not None:
            loop2_fan_min.update_handler = self.__loop2_fan_min_cb

        loop2_fan_max = self._registers.by_name(self._key + ".loop2.fan.max_speed")
        if loop2_fan_max is not None:
            loop2_fan_max.update_handler = self.__loop2_fan_max_cb

        loop2_temp_enabled = self._registers.by_name(self._key + ".loop2.temp.settings")
        if loop2_temp_enabled is not None:
            loop2_temp_enabled.update_handler = self.__loop2_temp_settings_cb

        loop2_valve_enabled = self._registers.by_name(self._key + ".loop2.valve.settings")
        if loop2_valve_enabled is not None:
            loop2_valve_enabled.update_handler = self.__loop2_valve_settings_cb


        # Shutting down all the devices.
        # self.__set_thermal_force(0)

    def update(self):
        """ Update cycle. """

        # Main update rate at ~ 20 second.
        # На всеки 20 секунди се правят следните стъпки:
        self.__update_timer.update()
        if self.__update_timer.expired:
            self.__update_timer.clear()

            # Recalculate the temperatures.
            self.__temp_proc.update()

            crg_temp = 0
            expected_room_temp = 0

            # Update current room temperature.
            temperature = self.temperature
            self.__logger.debug("ROOM: {:3.3f}".format(temperature))

            # 1. Изчислява се целевата температура на стаята:
            goal_room_temp = self.__goal_building_temp + self.__adjust_temp

            # 2. Изчислява се очакваната температура на стаята:
            expected_room_temp = temperature + self.__delta_temp
            self.__logger.debug("GRT {:3.3f}; ERT {:3.3f}"\
                .format(goal_room_temp, expected_room_temp))

            # 3. Намира се коригиращата разлика между
            # Целевата температура и Очакваната температура на стаята:
            crg_temp = goal_room_temp - expected_room_temp
            self.__logger.debug("CRG: {:3.3f}".format(crg_temp))
            # 4.
            # Колкото е по-отрицателна температурата, толкова повече трябва да охлаждаме,
            # колкото е по-положителна - толкова повече трябва да отопляваме.
            # Определяме минималната термална сила, на база Корекционната температура:
            #self.__thermal_force_limit = aprox(-5 => -100, 5 => 100)

            # 5. Интегрираме термалната сила:
            self.__thermal_force += crg_temp

            # 6. Ако модула на пределната термална сила е по-малък от модула на термалната сила,
            # тогава Термалата сила = Пределната термала сила
            if self.__thermal_force > abs(self.__thermal_force_limit):
                self.__thermal_force = self.__thermal_force_limit
            elif self.__thermal_force < -abs(self.__thermal_force_limit):
                self.__thermal_force = -abs(self.__thermal_force_limit)

            self.__set_thermal_force(self.__thermal_force)

            if self.__loop1_valve_dev is not None:
                if self.__loop1_valve_dev.set_point <= 0:
                    self.__loop1_leak_test.run()

            if self.__loop2_valve_dev is not None:
                if self.__loop2_valve_dev.set_point <= 0:
                    self.__loop2_leak_teat.run()

            temp_actual = self._registers.by_name(self._key + ".temp.actual")
            if temp_actual is not None:
                temp_actual.value = temperature

        # Recalculate delta time.
        # pass_time = time.time() - self.__lastupdate_delta_time
        # if pass_time > self.__delta_time:
        #     self.__delta_temp = temperature - self.__delta_temp
        #     self.__logger.debug("DT: {:3.3f}".format(self.__delta_temp))

        #     # Update current time.
        #     self.__lastupdate_delta_time = time.time()

        # If there is no one at the zone, just turn off the lights.
        ac_zone_occupied = self._registers.by_name("ac.zone_occupied")
        if ac_zone_occupied is not None:
            if ac_zone_occupied.value == 1:
                self.__logger.debug("Just turn off the HVAC in the zone.")
            if ac_zone_occupied.value == 0:
                # TODO: Pass, but when activity has turnback return to normal state.
                pass

    def shutdown(self):
        """Shutdown the tamper."""

        self.__logger.info("Shutting down the {}".format(self.name))
        self.__thermal_force = 0
        self.__set_thermal_force(self.__thermal_force)

#endregion
