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
from collections import deque

from utils.logger import get_logger

from utils.logic.functions import l_scale
from utils.logic.state_machine import StateMachine
from utils.logic.timer import Timer
from utils.logic.temp_processor import TemperatureProcessor

from plugins.base_plugin import BasePlugin
from plugins.hvac.thermal_mode import ThermalMode

from devices.HangzhouAirflowElectricApplications.f3p146ec072600.f3p146ec072600 import F3P146EC072600
from devices.TONHE.a20m15b2c.a20m15b2c import A20M15B2C
from devices.SILPA.klimafan.klimafan import Klimafan
from devices.no_vendors.no_vendor_1.flowmeter import Flowmeter
from devices.Dallas.ds18b20.ds18b20 import DS18B20
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

class AirConditioner(BasePlugin):

#region Attributes

    __logger = None
    """Logger"""

    __identifier = 0
    """Air conditioner identifier."""


    __temp_proc = None
    """Temperature processor."""

    __air_temp_upper_dev = None
    """Air thermometer upper."""

    __air_temp_cent_dev = None
    """Air thermometer central."""

    __air_temp_lower_dev = None
    """Air thermometer lower."""

    __queue_temperatures = None
    """Queue of the temperatures."""    


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

    __loop1_leak_test = None
    """Loop 1 leak test."""


    __loop2_fan_dev = None
    """Loop 1 fan device."""

    __loop2_temp_dev = None
    """Loop 2 thermometer."""

    __loop2_valve_dev = None
    """Loop 2 valve device."""

    __loop2_cnt_dev = None
    """Loop 2 flow metter."""

    __loop2_leak_teat = None
    """Loop 2 leak test."""


    __update_timer = None
    """Main process update timer."""

    __stop_timer = None
    """Stop timer."""


    __thermal_mode = None
    """Thermal mode of the HVAC."""

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

    __stop_flag = 0
    """HVAC Stop flag."""

    __window_closed_input = verbal_const.OFF
    """Window closed sensor input."""

#endregion

#region Constructor / Destructor

    def __init__(self, **kwargs):
        """Constructor"""

        super().__init__(kwargs)

        if "identifier" in kwargs:
            self.__identifier = kwargs["identifier"]

    def __del__(self):
        """Destructor"""

        super().__del__()

        if self.__logger is not None:
            del self.__logger

        if self.__loop1_fan_dev is not None:
            del self.__loop1_fan_dev

        if self.__loop1_temp_dev is not None:
            del self.__loop1_temp_dev

        if self.__loop1_valve_dev is not None:
            del self.__loop1_valve_dev

        if self.__loop1_cnt_dev is not None:
            del self.__loop1_cnt_dev

        if self.__loop2_fan_dev is not None:
            del self.__loop2_fan_dev

        if self.__loop2_temp_dev is not None:
            del self.__loop2_temp_dev

        if self.__loop2_valve_dev is not None:
            del self.__loop2_valve_dev

        if self.__loop2_cnt_dev is not None:
            del self.__loop2_cnt_dev

        if self.__thermal_mode is not None:
            del self.__thermal_mode

        if self.__update_timer is not None:
            del self.__update_timer

        if self.__stop_timer is not None:
            del self.__stop_timer

        if self.__loop1_leak_test is not None:
            del self.__loop1_leak_test

        if self.__loop2_leak_teat is not None:
            del self.__loop2_leak_teat

        if self.__queue_temperatures is not None:
            del self.__queue_temperatures

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

#region Private Methods (Parameters callbacks)

    def __update_rate_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # Check value.
        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__update_rate = register.value

    def __delta_time_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # Check value.
        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__delta_time = register.value

    def __thermal_mode_cb(self, register):

        # Check data type.
        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        mode = ThermalMode(register.value)
        self.__thermal_mode.set_state(mode)

    def __thermal_force_limit_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # Check value.
        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        self.__thermal_force_limit = register.value

    def __adjust_temp_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if self.__adjust_temp == register.value:
            return

        # @see https://experta.bg/L/S/122745/m/Fwntindd
        min_temp = 2.5
        max_temp = -2.5

        min_temp_reg = self._registers.by_name("{}.temp_{}.min".format(self.key, self.__identifier))
        if min_temp_reg is not None:
            if min_temp_reg.is_int_or_float():
                min_temp = min_temp_reg.value

        max_temp_reg = self._registers.by_name("{}.temp_{}.max".format(self.key, self.__identifier))
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
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
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

    def __window_closed_input_cb(self, register):

          # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__window_closed_input = register.value

#endregion

#region Private Methods (Thermometers callbacks)

    def __air_temp_cent_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__air_temp_cent_dev is None:

            self.__air_temp_cent_dev = DS18B20.create(\
                "Air temperature lower",\
                self.key + ".air_temp_cent",\
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
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__air_temp_lower_dev is None:
            self.__air_temp_lower_dev = DS18B20.create(\
                "Air temperature lower",\
                self.key + ".air_temp_lower",\
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
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__air_temp_upper_dev is None:
            self.__air_temp_upper_dev = DS18B20.create(\
                "Air temperature upper",\
                self.key + ".air_temp_upper",\
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
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__convector_dev is None:
            self.__convector_dev = Klimafan.create(\
                "Convector 1",\
                "{}.convector_{}".format(self.key, self.__identifier),\
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
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop1_cnt_dev is None:
            self.__loop1_cnt_dev = Flowmeter.create(\
                "Loop 2 flowmeter",\
                "{}.loop2_{}.cnt".format(self.key, self.__identifier),\
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
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop1_fan_dev is None:
            # Filter by model.
            if "f3p146ec072600" in register.value:
                self.__loop1_fan_dev = F3P146EC072600.create(\
                    "Loop 1 fan",\
                    "{}.loop1_{}.fan".format(self.key, self.__identifier),\
                    self._registers,\
                    self._controller)

            if self.__loop1_fan_dev is not None:
                self.__loop1_fan_dev.init()

        elif register.value == verbal_const.OFF and self.__loop1_fan_dev is not None:
            self.__loop1_fan_dev.shutdown()
            del self.__loop1_fan_dev

    def __loop1_fan_min_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__loop1_fan_dev is not None:
            self.__loop1_fan_dev.min_speed = register.value

    def __loop1_fan_max_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__loop1_fan_dev is not None:
            self.__loop1_fan_dev.max_speed = register.value

    def __loop1_temp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop1_temp_dev is None:
            self.__loop1_temp_dev = DS18B20.create(\
                "Loop 1 temperature",\
                "{}.loop1_{}.temp".format(self.key, self.__identifier),\
                register.value,\
                self._controller)

            if self.__loop1_temp_dev is not None:
                self.__loop1_temp_dev.init()

        elif register.value == verbal_const.OFF and self.__loop1_temp_dev is not None:
            self.__loop1_temp_dev.shutdown()
            del self.__loop1_temp_dev

    def __loop1_valve_enabled_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop1_valve_dev is None:
            self.__loop1_valve_dev = A20M15B2C.create(\
                "Loop 1 valve",\
                "{}.loop1_{}.valve".format(self.key, self.__identifier),\
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
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop2_cnt_dev is None:
            self.__loop2_cnt_dev = Flowmeter.create(\
                "Loop 2 flowmeter",\
                "{}.loop2_{}.cnt".format(self.key, self.__identifier),\
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
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop2_fan_dev is None:
            # Filter by model.
            if "f3p146ec072600" in register.value:
                self.__loop2_fan_dev = F3P146EC072600.create(\
                    "Loop 2 fan",\
                    "{}.loop2_{}.fan".format(self.key, self.__identifier),\
                    self._registers,\
                    self._controller)

            if self.__loop2_fan_dev is not None:
                self.__loop2_fan_dev.init()

        elif register.value == verbal_const.OFF and self.__loop2_fan_dev is not None:
            self.__loop2_fan_dev.shutdown()
            del self.__loop2_fan_dev

    def __loop2_fan_min_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__loop2_fan_dev is not None:
            self.__loop2_fan_dev.min_speed = register.value

    def __loop2_fan_max_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__loop2_fan_dev is not None:
            self.__loop2_fan_dev.max_speed = register.value

    def __loop2_temp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop2_temp_dev is None:
            self.__loop2_temp_dev = DS18B20.create(\
                "Loop 2 temperature",\
                "{}.loop2_{}.temp".format(self.key, self.__identifier),\
                register.value,\
                self._controller)

            if self.__loop2_temp_dev is not None:
                self.__loop2_temp_dev.init()

        elif register.value == verbal_const.OFF and self.__loop2_temp_dev is not None:
            self.__loop2_temp_dev.shutdown()
            del self.__loop2_temp_dev

    def __loop2_valve_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__loop2_valve_dev is None:
            self.__loop2_valve_dev = A20M15B2C.create(\
                "Loop 2 valve",\
                "{}.loop2_{}.valve".format(self.key, self.__identifier),\
                self._registers,\
                self._controller)

            if self.__loop2_valve_dev is not None:
                self.__loop2_valve_dev.init()

        elif register.value == verbal_const.OFF and self.__loop2_valve_dev is not None:
            self.__loop2_valve_dev.shutdown()
            del self.__loop2_valve_dev

#endregion

#region Private Methods (Registers Interface)

    def __init_registers_cb(self):
        """Initialize the registers callbacks.
        """

        # Air temperatures.
        air_temp_cent_enabled = self._registers.by_name("{}.air_temp_cent_{}.settings".format(self.key, self.__identifier))
        if air_temp_cent_enabled is not None:
            air_temp_cent_enabled.update_handlers = self.__air_temp_cent_settings_cb
            air_temp_cent_enabled.update()

        air_temp_lower_enabled = self._registers.by_name("{}.air_temp_lower_{}.settings".format(self.key, self.__identifier))
        if air_temp_lower_enabled is not None:
            air_temp_lower_enabled.update_handlers = self.__air_temp_lower_settings_cb
            air_temp_lower_enabled.update()

        air_temp_upper_enabled = self._registers.by_name("{}.air_temp_upper_{}.settings".format(self.key, self.__identifier))
        if air_temp_upper_enabled is not None:
            air_temp_upper_enabled.update_handlers = self.__air_temp_upper_settings_cb
            air_temp_upper_enabled.update()

        # Region parameters
        update_rate = self._registers.by_name("{}.update_rate_{}".format(self.key, self.__identifier))
        if update_rate is not None:
            update_rate.update_handlers = self.__update_rate_cb
            update_rate.update()

        delta_time = self._registers.by_name("{}.delta_time_{}".format(self.key, self.__identifier))
        if delta_time is not None:
            delta_time.update_handlers = self.__delta_time_cb
            delta_time.update()

        thermal_mode = self._registers.by_name("{}.thermal_mode_{}".format(self.key, self.__identifier))
        if thermal_mode is not None:
            thermal_mode.update_handlers = self.__thermal_mode_cb
            thermal_mode.update()

        thermal_force_limit = self._registers.by_name("{}.thermal_force_limit_{}".format(self.key, self.__identifier))
        if thermal_force_limit is not None:
            thermal_force_limit.update_handlers = self.__thermal_force_limit_cb
            thermal_force_limit.update()

        adjust_temp = self._registers.by_name("{}.adjust_temp_{}".format(self.key, self.__identifier))
        if adjust_temp is not None:
            adjust_temp.update_handlers = self.__adjust_temp_cb
            adjust_temp.update()

        goal_building_temp = self._registers.by_name("{}.goal_building_temp".format(self.key))
        if goal_building_temp is not None:
            goal_building_temp.update_handlers = self.__goal_building_temp_cb
            goal_building_temp.update()



        # Convector
        convector_enable = self._registers.by_name("{}.convector_{}.settings".format(self.key, self.__identifier))
        if convector_enable is not None:
            convector_enable.update_handlers = self.__convector_settings_cb
            convector_enable.update()

        # Loop 1
        loop1_cnt_enabled = self._registers.by_name("{}.loop1_{}.cnt.input".format(self.key, self.__identifier))
        if loop1_cnt_enabled is not None:
            loop1_cnt_enabled.update_handlers = self.__loop1_cnt_input_cb
            loop1_cnt_enabled.update()

        loop1_fan_enabled = self._registers.by_name("{}.loop1_{}.fan.settings".format(self.key, self.__identifier))
        if loop1_fan_enabled is not None:
            loop1_fan_enabled.update_handlers = self.__loop1_fan_settings_cb
            loop1_fan_enabled.update()

        loop1_fan_min = self._registers.by_name("{}.loop1_{}.fan.min_speed".format(self.key, self.__identifier))
        if loop1_fan_min is not None:
            loop1_fan_min.update_handlers = self.__loop1_fan_min_cb
            loop1_fan_min.update()

        loop1_fan_max = self._registers.by_name("{}.loop1_{}.fan.max_speed".format(self.key, self.__identifier))
        if loop1_fan_max is not None:
            loop1_fan_max.update_handlers = self.__loop1_fan_max_cb
            loop1_fan_max.update()

        loop1_temp_enabled = self._registers.by_name("{}.loop1_{}.temp.settings".format(self.key, self.__identifier))
        if loop1_temp_enabled is not None:
            loop1_temp_enabled.update_handlers = self.__loop1_temp_settings_cb
            loop1_temp_enabled.update()

        loop1_valve_enabled = self._registers.by_name("{}.loop1_{}.valve.settings".format(self.key, self.__identifier))
        if loop1_valve_enabled is not None:
            loop1_valve_enabled.update_handlers = self.__loop1_valve_enabled_cb
            loop1_valve_enabled.update()

        # Loop 2
        loop2_cnt_enabled = self._registers.by_name("{}.loop2_{}.cnt.input".format(self.key, self.__identifier))
        if loop2_cnt_enabled is not None:
            loop2_cnt_enabled.update_handlers = self.__loop2_cnt_input_cb
            loop1_cnt_enabled.update()

        loop2_fan_enabled = self._registers.by_name("{}.loop2_{}.fan.settings".format(self.key, self.__identifier))
        if loop2_fan_enabled is not None:
            loop2_fan_enabled.update_handlers = self.__loop2_fan_settings_cb
            loop2_fan_enabled.update()

        loop2_fan_min = self._registers.by_name("{}.loop2_{}.fan.min_speed".format(self.key, self.__identifier))
        if loop2_fan_min is not None:
            loop2_fan_min.update_handlers = self.__loop2_fan_min_cb
            loop2_fan_min.update()

        loop2_fan_max = self._registers.by_name("{}.loop2_{}.fan.max_speed".format(self.key, self.__identifier))
        if loop2_fan_max is not None:
            loop2_fan_max.update_handlers = self.__loop2_fan_max_cb
            loop2_fan_max.update()

        loop2_temp_enabled = self._registers.by_name("{}.loop2_{}.temp.settings".format(self.key, self.__identifier))
        if loop2_temp_enabled is not None:
            loop2_temp_enabled.update_handlers = self.__loop2_temp_settings_cb
            loop2_temp_enabled.update()

        loop2_valve_enabled = self._registers.by_name("{}.loop2_{}.valve.settings".format(self.key, self.__identifier))
        if loop2_valve_enabled is not None:
            loop2_valve_enabled.update_handlers = self.__loop2_valve_settings_cb
            loop2_valve_enabled.update()

        # Create window closed sensor.
        window_closed_input = self._registers.by_name("{}.window_closed_{}.input".format("ac", 1))
        if window_closed_input is not None:
            window_closed_input.update_handlers = self.__window_closed_input_cb
            window_closed_input.update()

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

    def __update_thermometers_values(self):

        # TODO: Get all thermometers and load its values to the folowing registers.

        # 1. If thermometer is available, gets its value.
        air_temp_lower_value = 0
        if self.__air_temp_lower_dev is not None:
            air_temp_lower_value = self.__air_temp_lower_dev.value()

        # 1. If thermometer is available, gets its value.
        air_temp_cent_value = 0
        if self.__air_temp_cent_dev is not None:
            air_temp_cent_value = self.__air_temp_cent_dev.value()

        # 1. If thermometer is available, gets its value.
        air_temp_upper_value = 0
        if self.__air_temp_upper_dev is not None:
            air_temp_upper_value = self.__air_temp_upper_dev.value()

        # 1. If thermometer is available, gets its value.
        loop1_temp_value = 0
        if self.__loop1_temp_dev is not None:
            loop1_temp_value = self.__loop1_temp_dev.value()

        # 1. If thermometer is available, gets its value.
        loop2_temp_value = 0
        if self.__loop2_temp_dev is not None:
            loop2_temp_value = self.__loop2_temp_dev.value()

        # 2. If the folowing register is available then set ist value to the thermometers value.
        air_temp_lower = self._registers.by_name("{}.air_temp_lower_{}.value".format(self.key, self.__identifier))
        if air_temp_lower is not None:
            air_temp_lower.value = air_temp_lower_value

        # 2. If the folowing register is available then set ist value to the thermometers value.
        air_temp_cent = self._registers.by_name("{}.air_temp_cent_{}.value".format(self.key, self.__identifier))
        if air_temp_cent is not None:
            air_temp_cent.value = air_temp_cent_value

        # 2. If the folowing register is available then set ist value to the thermometers value.
        air_temp_upper = self._registers.by_name("{}.air_temp_upper_{}.value".format(self.key, self.__identifier))
        if air_temp_upper is not None:
            air_temp_upper.value = air_temp_upper_value

        # 2. If the folowing register is available then set ist value to the thermometers value.
        loop1_temp = self._registers.by_name("{}.loop1_{}.temp.value".format(self.key, self.__identifier))
        if loop1_temp is not None:
            loop1_temp.value = loop1_temp_value

        # 2. If the folowing register is available then set ist value to the thermometers value.
        loop2_temp = self._registers.by_name("{}.loop2_{}.temp.value".format(self.key, self.__identifier))
        if loop2_temp is not None:
            loop2_temp.value = loop2_temp_value

    def __read_zoneoccupied_flag(self):

        state = False

        ac_zone_occupied = self._registers.by_name("ac.zone_1_occupied")
        if ac_zone_occupied is not None:
            state = ac_zone_occupied.value

        return state

    def __read_window_closed_sensor(self):

        state = False

        if self._controller.is_valid_gpio(self.__window_closed_input):
            state = self._controller.digital_read(self.__window_closed_input)

        return state

    def __is_hot_water(self):

        # Request: Eml6419
        down_limit_value = 10

        down_limit = self._registers.by_name("{}.loop1_{}.temp.down_limit".format(self.key, self.__identifier))
        if down_limit is not None:
            down_limit_value = down_limit.value

        temperature = 0
        if self.__loop1_temp_dev is not None:
            temperature = self.__loop1_temp_dev.value()

        return temperature >= down_limit_value

    def __thermal_mode_on_change(self, machine):
        self.__logger.info("Thermal mode: {}".format(machine.get_state()))

    def __set_thermal_force(self, thermal_force):
        """ Apply thermal force to the devices. """

        # 6. Ако модула на пределната термална сила е по-малък от модула на термалната сила,
        # тогава Термалата сила = Пределната термала сила
        if thermal_force > abs(self.__thermal_force_limit):
            thermal_force = self.__thermal_force_limit
        elif thermal_force < -abs(self.__thermal_force_limit):
            thermal_force = -abs(self.__thermal_force_limit)

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
            self.__convector_dev.set_state(abs(conv_tf))

#endregion

#region Public Methods

    def init(self):
        """Init the module.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {} {}".format(self.name, self.__identifier))

        # Create thermal mode.
        self.__thermal_mode = StateMachine(ThermalMode.NONE)
        self.__thermal_mode.on_change(self.__thermal_mode_on_change)

        # Create update timer.
        self.__update_timer = Timer(self.__update_rate)
        self.__stop_timer = Timer(10)

        # Create temperature processor.
        self.__temp_proc = TemperatureProcessor()

        # Create temperature queue.
        self.__queue_temperatures = deque([], maxlen = 20)

        # Create registers callbacks.
        self.__init_registers_cb()

        # Shutting down all the devices.
        self.__set_thermal_force(0)

    def update(self):
        """ Update cycle.
        """

        # Update thermometres values.
        self.__update_thermometers_values()

        # If there is no one at the zone, just turn off the lights.
        ac_zone_occupied_flag = self.__read_zoneoccupied_flag()

        # If the window is opened, just turn off the HVAC.
        window_closed_1_state = self.__read_window_closed_sensor()

        # If temperature is less then 10 deg on loop 1.
        hot_water = self.__is_hot_water()

        # Take all necessary condition for normal operation of the HVAC.
        stop_flag = (not ac_zone_occupied_flag or not window_closed_1_state or not hot_water)

        if stop_flag:
            self.__stop_timer.update()
            if self.__stop_timer.expired:
                self.__stop_timer.clear()
                if self.__stop_flag != stop_flag:
                    self.__stop_flag = stop_flag
                    self.__set_thermal_force(0)

        if not stop_flag:
            self.__stop_flag = False
            self.__stop_timer.update_last_time()

        # Main update rate at ~ 20 second.
        # На всеки 20 секунди се правят следните стъпки:
        self.__update_timer.update()
        if self.__update_timer.expired and not self.__stop_flag:
            self.__update_timer.clear()

            # Recalculate the temperatures.
            self.__temp_proc.update() # Add thermometers : DS18B20 - 28B802B5030000CF 11.8 °C

            crg_temp = 0
            expected_room_temp = 0

            # Update current room temperature.
            temperature = self.temperature

            # Add temperature to the queue.
            self.__queue_temperatures.append(temperature)
            self.__logger.debug("ROOM: {:3.3f}".format(temperature))

            # 1. Изчислява се целевата температура на стаята:
            goal_room_temp = self.__goal_building_temp + self.__adjust_temp

            # 2. Изчислява се очакваната температура на стаята:
            expected_room_temp = temperature + self.__delta_temp


            # 3. Намира се коригиращата разлика между
            # Целевата температура и Очакваната температура на стаята:
            crg_temp = goal_room_temp - expected_room_temp
            self.__logger.debug("GRT {:3.3f}\t ERT {:3.3f}\t CRG: {:3.3f}"\
                .format(goal_room_temp, expected_room_temp, crg_temp))

            # 4.
            # Колкото е по-отрицателна температурата, толкова повече трябва да охлаждаме,
            # колкото е по-положителна - толкова повече трябва да отопляваме.
            # Определяме минималната термална сила, на база Корекционната температура:
            #self.__thermal_force_limit = aprox(-5 => -100, 5 => 100)

            # 5. Интегрираме термалната сила:
            self.__thermal_force += crg_temp

            # Apply the integrated force.
            self.__set_thermal_force(self.__thermal_force)

            if self.__loop1_valve_dev is not None:
                if self.__loop1_valve_dev.set_point <= 0:
                    if self.__loop1_leak_test is not None: 
                        self.__loop1_leak_test.run()

            if self.__loop2_valve_dev is not None:
                if self.__loop2_valve_dev.set_point <= 0:
                    if self.__loop2_leak_teat is not None: 
                        self.__loop2_leak_teat.run()

            temp_actual = self._registers.by_name("{}.temp_{}.actual".format(self.key, self.__identifier))
            if temp_actual is not None:
                temp_actual.value = temperature

        # Recalculate delta time.
        # pass_time = time.time() - self.__lastupdate_delta_time
        # if pass_time > self.__delta_time:
        #     self.__delta_temp = temperature - self.__delta_temp
        #     self.__logger.debug("DT: {:3.3f}".format(self.__delta_temp))

        #     # Update current time.
        #     self.__lastupdate_delta_time = time.time()

    def shutdown(self):
        """Shutdown the tamper.
        """

        self.__logger.info("Shutting down the {} {}".format(self.name, self.__identifier))
        self.__set_thermal_force(0)

#endregion
