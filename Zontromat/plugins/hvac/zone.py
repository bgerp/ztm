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

from devices.factories.valve.valve_factory import ValveFactory
from devices.factories.convectors.convectors_factory import ConvectorsFactory
from devices.factories.flowmeters.flowmeters_factory import FlowmetersFactory
from devices.factories.thermometers.thermometers_factory import ThermometersFactory

from devices.tests.leak_test.leak_test import LeakTest
from devices.tests.electrical_performance.electrical_performance import ElectricalPerformance

from data import verbal_const
from data.thermal_mode import ThermalMode

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

class Zone(BasePlugin):
    """Air conditioner control logic.
    """

#region Attributes

    __logger = None
    """Logger"""

    __identifier = 0
    """Number identifier."""


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


    __loop1_temp_dev = None
    """Loop 2 thermometer."""

    __loop1_valve_dev = None
    """Loop 1 valve device."""

    __loop1_flowmeter = None
    """Loop 1 flow metter."""

    __loop1_leak_test = None
    """Loop 1 leak test."""


    __loop2_temp_dev = None
    """Loop 2 thermometer."""

    __loop2_valve_dev = None
    """Loop 2 valve device."""

    __loop2_flowmeter = None
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

    __stop_flag = False
    """HVAC Stop flag."""

    __window_closed_input = verbal_const.OFF
    """Window closed sensor input."""

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        if "identifier" in config:
            self.__identifier = config["identifier"]

    def __del__(self):
        """Destructor"""

        if self.__loop1_temp_dev is not None:
            del self.__loop1_temp_dev

        if self.__loop1_valve_dev is not None:
            del self.__loop1_valve_dev

        if self.__loop1_flowmeter is not None:
            del self.__loop1_flowmeter

        if self.__loop2_temp_dev is not None:
            del self.__loop2_temp_dev

        if self.__loop2_valve_dev is not None:
            del self.__loop2_valve_dev

        if self.__loop2_flowmeter is not None:
            del self.__loop2_flowmeter

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

        super().__del__()

        if self.__logger is not None:
            del self.__logger

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

#region Private Methods (Registers Parameters)

    def __update_rate_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # Check value.
        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__update_timer.expiration_time != register.value:
            self.__update_timer.expiration_time = register.value

    def __delta_time_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # Check value.
        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__delta_time != register.value:
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
            min_temp = min_temp_reg.value

        max_temp_reg = self._registers.by_name("{}.temp_{}.max".format(self.key, self.__identifier))
        if max_temp_reg is not None:
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

        if self.__goal_building_temp != actual_temp:
            self.__goal_building_temp = actual_temp

    def __window_closed_input_cb(self, register):

          # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__window_closed_input = register.value

#endregion

#region Private Methods (Registers Thermometers)

    def __air_temp_cent_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {} and self.__air_temp_cent_dev is None:

            self.__air_temp_cent_dev = ThermometersFactory.create(
                name="Air temperature center",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__air_temp_cent_dev is not None:
                self.__air_temp_cent_dev.init()
                self.__temp_proc.add(self.__air_temp_cent_dev)

        elif register.value == {} and self.__air_temp_cent_dev is not None:

            self.__temp_proc.add(self.__air_temp_cent_dev)
            self.__air_temp_cent_dev.shutdown()
            del self.__air_temp_cent_dev

    def __air_temp_lower_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {} and self.__air_temp_lower_dev is None:

            self.__air_temp_lower_dev = ThermometersFactory.create(
                controller=self._controller,
                name="Air temperature lower",
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__air_temp_lower_dev is not None:
                self.__air_temp_lower_dev.init()
                self.__temp_proc.add(self.__air_temp_lower_dev)

        elif register.value == {} and self.__air_temp_lower_dev is not None:

            self.__temp_proc.remove(self.__air_temp_lower_dev)
            self.__air_temp_lower_dev.shutdown()
            del self.__air_temp_lower_dev

    def __air_temp_upper_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {} and self.__air_temp_upper_dev is None:

            self.__air_temp_upper_dev = ThermometersFactory.create(
                controller=self._controller,
                name="Air temperature upper",
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__air_temp_upper_dev is not None:
                self.__air_temp_upper_dev.init()
                self.__temp_proc.add(self.__air_temp_upper_dev)

        elif register.value == {} and self.__air_temp_upper_dev is not None:

            self.__temp_proc.remove(self.__air_temp_upper_dev)
            self.__air_temp_upper_dev.shutdown()
            del self.__air_temp_upper_dev

#endregion

#region Private Methods (Registers Convector)

    def __convector_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__convector_dev is None:

            self.__convector_dev = ConvectorsFactory.create(
                name="Convector {}".format(self.__identifier),
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__convector_dev is not None:
                self.__convector_dev.init()

        elif register.value == {} and self.__convector_dev is not None:
            self.__convector_dev.shutdown()
            del self.__convector_dev

#endregion

#region Private Methods (Registers Loop 1)

    def __loop1_flowmeter_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__loop1_flowmeter is None:
            self.__loop1_flowmeter = FlowmetersFactory.create(
                name="Loop 1 flowmeter",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__loop1_flowmeter is not None:
                self.__loop1_flowmeter.init()

                # 20 seconds is time for leak testing.
                self.__loop1_leak_test = LeakTest(self.__loop1_flowmeter, 20)
                self.__loop1_leak_test.on_result(self.__loop1_leaktest_result)

        elif register.value == {} and self.__loop1_flowmeter is not None:
            self.__loop1_flowmeter.shutdown()
            del self.__loop1_flowmeter
            del self.__loop1_leak_test

    def __loop1_temp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__loop1_temp_dev is None:

            self.__loop1_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name="Loop 1 temperature",
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__loop1_temp_dev is not None:
                self.__loop1_temp_dev.init()

        elif register.value == {} and self.__loop1_temp_dev is not None:
            self.__loop1_temp_dev.shutdown()
            del self.__loop1_temp_dev

    def __loop1_valve_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__loop1_valve_dev is None:

            self.__loop1_valve_dev = ValveFactory.create(
                name="Loop 1 valve",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__loop1_valve_dev is not None:
                self.__loop1_valve_dev.init()

        elif register.value == {} and self.__loop1_valve_dev is not None:
            self.__loop1_valve_dev.shutdown()
            del self.__loop1_valve_dev

#endregion

#region Private Methods (Registers Loop 2)

    def __loop2_flowmeter_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__loop2_flowmeter is None:
            self.__loop2_flowmeter = FlowmetersFactory.create(
                name="Loop 2 flowmeter",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__loop2_flowmeter is not None:
                self.__loop2_flowmeter.init()

                self.__loop2_leak_teat = LeakTest(self.__loop2_flowmeter, 20)
                self.__loop2_leak_teat.on_result(self.__loop2_leaktest_result)

        elif register.value == {} and self.__loop2_flowmeter is not None:
            self.__loop2_flowmeter.shutdown()
            del self.__loop2_flowmeter
            del self.__loop2_leak_teat

    def __loop2_temp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__loop2_temp_dev is None:

            self.__loop2_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name="Loop 2 temperature",
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])


            if self.__loop2_temp_dev is not None:
                self.__loop2_temp_dev.init()

        elif register.value == {} and self.__loop2_temp_dev is not None:
            self.__loop2_temp_dev.shutdown()
            del self.__loop2_temp_dev

    def __loop2_valve_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__loop2_valve_dev is None:

            self.__loop2_valve_dev = ValveFactory.create(
                name="Loop 2 valve",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__loop2_valve_dev is not None:
                self.__loop2_valve_dev.init()

        elif register.value == {} and self.__loop2_valve_dev is not None:
            self.__loop2_valve_dev.shutdown()
            del self.__loop2_valve_dev

#endregion

#region Private Methods (Registers envm)

    def __envm_energy_cb(self, register):

        # Check data type.
        if not ((register.data_type == "int") or (register.data_type == "float")):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # TODO: Get energy mode for the building.
        pass

#endregion

#region Private Methods (Ventilation Interface)

    def __set_ventilation(self, value):

        # Set the ventilation.
        self._registers.write("vent.hvac_setpoint_{}".format(self.__identifier), value)

#endregion

#region Private Methods (Registers Interface)

    def __init_registers(self):
        """Initialize the registers callbacks.
        """

        # Air temperatures.
        air_temp_cent_settings = self._registers.by_name("{}.air_temp_cent_{}.settings".format(self.key, self.__identifier))
        if air_temp_cent_settings is not None:
            air_temp_cent_settings.update_handlers = self.__air_temp_cent_settings_cb
            air_temp_cent_settings.update()

        air_temp_lower_settings = self._registers.by_name("{}.air_temp_lower_{}.settings".format(self.key, self.__identifier))
        if air_temp_lower_settings is not None:
            air_temp_lower_settings.update_handlers = self.__air_temp_lower_settings_cb
            air_temp_lower_settings.update()

        air_temp_upper_settings = self._registers.by_name("{}.air_temp_upper_{}.settings".format(self.key, self.__identifier))
        if air_temp_upper_settings is not None:
            air_temp_upper_settings.update_handlers = self.__air_temp_upper_settings_cb
            air_temp_upper_settings.update()

        # Convector
        convector_enable = self._registers.by_name("{}.convector_{}.settings".format(self.key, self.__identifier))
        if convector_enable is not None:
            convector_enable.update_handlers = self.__convector_settings_cb
            convector_enable.update()

        # Loop 1
        loop1_flowmeter = self._registers.by_name("{}.loop1_{}.flowmeter.settings".format(self.key, self.__identifier))
        if loop1_flowmeter is not None:
            loop1_flowmeter.update_handlers = self.__loop1_flowmeter_settings_cb
            loop1_flowmeter.update()

        loop1_temp_settings = self._registers.by_name("{}.loop1_{}.temp.settings".format(self.key, self.__identifier))
        if loop1_temp_settings is not None:
            loop1_temp_settings.update_handlers = self.__loop1_temp_settings_cb
            loop1_temp_settings.update()

        loop1_valve_enabled = self._registers.by_name("{}.loop1_{}.valve.settings".format(self.key, self.__identifier))
        if loop1_valve_enabled is not None:
            loop1_valve_enabled.update_handlers = self.__loop1_valve_settings_cb
            loop1_valve_enabled.update()

        # Loop 2
        loop2_flowmeter_settings = self._registers.by_name("{}.loop2_{}.flowmeter.settings".format(self.key, self.__identifier))
        if loop2_flowmeter_settings is not None:
            loop2_flowmeter_settings.update_handlers = self.__loop2_flowmeter_settings_cb
            loop2_flowmeter_settings.update()

        loop2_temp_settings = self._registers.by_name("{}.loop2_{}.temp.settings".format(self.key, self.__identifier))
        if loop2_temp_settings is not None:
            loop2_temp_settings.update_handlers = self.__loop2_temp_settings_cb
            loop2_temp_settings.update()

        loop2_valve_settings = self._registers.by_name("{}.loop2_{}.valve.settings".format(self.key, self.__identifier))
        if loop2_valve_settings is not None:
            loop2_valve_settings.update_handlers = self.__loop2_valve_settings_cb
            loop2_valve_settings.update()

        # Create window closed sensor.
        window_closed_input = self._registers.by_name("{}.window_closed_{}.input".format("ac", self.__identifier))
        if window_closed_input is not None:
            window_closed_input.update_handlers = self.__window_closed_input_cb
            window_closed_input.update()

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

        # Get the power mode of the building.
        envm_energy = self._registers.by_name("envm.energy")
        if envm_energy is not None:
            envm_energy.update_handlers = self.__envm_energy_cb
            envm_energy.update()

    def __update_thermometers_values(self):

        # 1. If thermometer is available, gets its value.
        air_temp_lower_value = 0
        if self.__air_temp_lower_dev is not None:
            air_temp_lower_value = self.__air_temp_lower_dev.get_temp()

        # 1. If thermometer is available, gets its value.
        air_temp_cent_value = 0
        if self.__air_temp_cent_dev is not None:
            air_temp_cent_value = self.__air_temp_cent_dev.get_temp()

        # 1. If thermometer is available, gets its value.
        air_temp_upper_value = 0
        if self.__air_temp_upper_dev is not None:
            air_temp_upper_value = self.__air_temp_upper_dev.get_temp()

        # 1. If thermometer is available, gets its value.
        loop1_temp_value = 0
        if self.__loop1_temp_dev is not None:
            loop1_temp_value = self.__loop1_temp_dev.get_temp()

        # 1. If thermometer is available, gets its value.
        loop2_temp_value = 0
        if self.__loop2_temp_dev is not None:
            loop2_temp_value = self.__loop2_temp_dev.get_temp()

        # 2. If the folowing register is available then set ist value to the thermometers value.
        self._registers.write("{}.air_temp_lower_{}.value".format(self.key, self.__identifier), air_temp_lower_value)

        # 2. If the folowing register is available then set ist value to the thermometers value.
        self._registers.write("{}.air_temp_cent_{}.value".format(self.key, self.__identifier), air_temp_cent_value)

        # 2. If the folowing register is available then set ist value to the thermometers value.
        self._registers.write("{}.air_temp_upper_{}.value".format(self.key, self.__identifier), air_temp_upper_value)

        # 2. If the folowing register is available then set ist value to the thermometers value.
        self._registers.write("{}.loop1_{}.temp.value".format(self.key, self.__identifier), loop1_temp_value)

        # 2. If the folowing register is available then set ist value to the thermometers value.
        self._registers.write("{}.loop2_{}.temp.value".format(self.key, self.__identifier), loop2_temp_value)

    def __is_empty(self):

        value = False

        is_empty = self._registers.by_name("envm.is_empty")
        if is_empty is not None:
            value = is_empty.value

        return value

    def __get_down_limit_temp(self):

        # Request: Eml6419
        value = 10

        down_limit = self._registers.by_name("{}.loop1_{}.temp.down_limit".format(self.key, self.__identifier))
        if down_limit is not None:
            down_limit_value = down_limit.value

        return value

#endregion

#region Private Methods (PLC)

    def __read_window_tamper(self):

        state = False

        if self._controller.is_valid_gpio(self.__window_closed_input):
            state = self._controller.digital_read(self.__window_closed_input)

        if self.__window_closed_input == verbal_const.OFF:
            state = True

        return state

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

    def __is_hot_water(self):

        down_limit_value = self.__get_down_limit_temp()

        temperature = 0
        if self.__loop1_temp_dev is not None:
            temperature = self.__loop1_temp_dev.get_temp()

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

        if self.__thermal_mode.is_state(ThermalMode.ColdSeason):
            if thermal_force > 0:
                self.__loop1_valve_dev.target_position = 0
                self.__loop2_valve_dev.target_position = 0
            elif thermal_force <= 0:
                self.__loop1_valve_dev.target_position = 100
                self.__loop2_valve_dev.target_position = 100

        elif self.__thermal_mode.is_state(ThermalMode.TransisionSeason):
            if thermal_force < 0:
                self.__loop1_valve_dev.target_position = 100
                self.__loop2_valve_dev.target_position = 0
            elif thermal_force > 0:
                self.__loop1_valve_dev.target_position = 0
                self.__loop2_valve_dev.target_position = 100
            else:
                self.__loop1_valve_dev.target_position = 0
                self.__loop2_valve_dev.target_position = 0

        elif self.__thermal_mode.is_state(ThermalMode.WarmSeason):
            if thermal_force < 0:
                self.__loop1_valve_dev.target_position = 100
                self.__loop2_valve_dev.target_position = 100
            elif thermal_force > 0:
                self.__loop1_valve_dev.target_position = 0
                self.__loop2_valve_dev.target_position = 0

        # If thermal mode set properly apply thermal force
        if not self.__thermal_mode.is_state(ThermalMode.NONE):

            self.__set_ventilation(thermal_force)

            # Set convector fan.
            conv_tf = l_scale(thermal_force, [0, 100], [0, 3])
            conv_tf = abs(conv_tf)
            conv_tf = int(conv_tf)
            self.__convector_dev.set_state(conv_tf)

#endregion

#region Protected Methods

    def _init(self):
        """Initialize the module.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {} {}".format(self.name, self.__identifier))

        # Create thermal mode.
        self.__thermal_mode = StateMachine(ThermalMode.NONE)
        self.__thermal_mode.on_change(self.__thermal_mode_on_change)

        # Create update timer.
        self.__update_timer = Timer(5)

        # Stop timer.
        self.__stop_timer = Timer(10)

        # Create temperature processor.
        self.__temp_proc = TemperatureProcessor()

        # Create temperature queue.
        self.__queue_temperatures = deque([], maxlen=20)

        # Create registers callbacks.
        self.__init_registers()

        # Shutting down all the devices.
        self.__set_thermal_force(0)

    def _update(self):
        """ Update cycle.
        """

        # Update thermometres values.
        self.__update_thermometers_values()

        # Update occupation flags.
        is_empty = self.__is_empty()

        # If the window is opened, just turn off the HVAC.
        window_tamper_state = self.__read_window_tamper()

        # If temperature is less then 10 deg on loop 1.
        is_hot_water = self.__is_hot_water()

        # Take all necessary condition for normal operation of the HVAC.
        # stop_flag = (not is_empty or not window_tamper_state or not is_hot_water)
        stop_flag = False

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
            self.__temp_proc.update()

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
                if self.__loop1_valve_dev.current_position <= 0:
                    if self.__loop1_leak_test is not None:
                        self.__loop1_leak_test.run()

            if self.__loop2_valve_dev is not None:
                if self.__loop2_valve_dev.current_position <= 0:
                    if self.__loop2_leak_teat is not None:
                        self.__loop2_leak_teat.run()

            self._registers.write("{}.temp_{}.actual".format(self.key, self.__identifier), temperature)

        # Recalculate delta time.
        # pass_time = time.time() - self.__lastupdate_delta_time
        # if pass_time > self.__delta_time:
        #     self.__delta_temp = temperature - self.__delta_temp
        #     self.__logger.debug("DT: {:3.3f}".format(self.__delta_temp))

        #     # Update current time.
        #     self.__lastupdate_delta_time = time.time()

        self.__loop1_valve_dev.update()
        self.__loop2_valve_dev.update()

    def _shutdown(self):
        """Shutdown the tamper.
        """

        self.__logger.info("Shutting down the {} {}".format(self.name, self.__identifier))
        self.__set_thermal_force(0)

        self.__loop1_valve_dev.shutdown()
        self.__loop2_valve_dev.shutdown()

#endregion
