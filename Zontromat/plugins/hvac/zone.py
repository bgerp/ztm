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
from collections import deque

from utils.logger import get_logger

from utils.logic.functions import l_scale, filter_measurements_by_time
from utils.logic.state_machine import StateMachine
from utils.logic.timer import Timer
from utils.logic.timer_pwm import TimerPWM
from utils.logic.temp_processor import TemperatureProcessor

from plugins.base_plugin import BasePlugin

from devices.factories.valve.valve_factory import ValveFactory
from devices.factories.convectors.convectors_factory import ConvectorsFactory
from devices.factories.flowmeters.flowmeters_factory import FlowmeterFactory
from devices.factories.thermometers.thermometers_factory import ThermometersFactory

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

#region Table of control

"""
1. Get temperature of the zone: 

2. Get temperature of the slider:

3. 
+-----------------+---+-----+-----+---+---+---+---+
|  Device/State   | 0 |  1  |  2  | 3 | 4 | 5 | 6 |
+-----------------+---+-----+-----+---+---+---+---+
| Valve convector | 0 | 1   | 1   | 1 | 1 | 1 | 1 |
| Valve floor     | 0 | 1/3 | 1/2 | 1 | 1 | 1 | 1 |
| Convector       | 0 | 0   | 0   | 0 | 1 | 2 | 3 |
+-----------------+---+-----+-----+---+---+---+---+
"""

#endregion

class Zone(BasePlugin):
    """HVAC control logic.
    """

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self.__identifier = 1
        if "identifier" in config:
            self.__identifier = config["identifier"]

        self.__logger = get_logger(__name__)
        """Logger
        """

        self.__thermal_mode = 0
        """Thermal mode.
        """

        self.__update_now_flag = True
        """Fire update event every time when settings are changed.
        """        

        self.__stop_flag = False
        """HVAC Stop flag.
        """

        self.__update_timer = Timer(60)
        """Update timer
        """        

        self.__stop_timer = Timer(10)
        """Stop timer
        """        

        self.__vlv_fl_1_tmr = TimerPWM()
        self.__vlv_fl_1_tmr.upper_limit = 3600
        self.__vlv_fl_1_tmr.duty_cycle = 0
        self.__vlv_fl_1_tmr.set_cb(lambda: self.__vlv_fl_1(100), lambda: self.__vlv_fl_1(0))

        self.__vlv_fl_2_tmr = TimerPWM()
        self.__vlv_fl_2_tmr.upper_limit = 3600
        self.__vlv_fl_2_tmr.duty_cycle = 0
        self.__vlv_fl_2_tmr.set_cb(lambda: self.__vlv_fl_2(100), lambda: self.__vlv_fl_2(0))

        self.__vlv_fl_3_tmr = TimerPWM()
        self.__vlv_fl_3_tmr.upper_limit = 3600
        self.__vlv_fl_3_tmr.duty_cycle = 0
        self.__vlv_fl_3_tmr.set_cb(lambda: self.__vlv_fl_3(100), lambda: self.__vlv_fl_3(0))

        # Create temperature processor.
        self.__temp_proc = TemperatureProcessor()

        self.__air_temp_upper_dev = None
        """Air thermometer upper.
        """

        self.__air_temp_cent_dev = None
        """Air thermometer central.
        """

        self.__air_temp_lower_dev = None
        """Air thermometer lower.
        """

        self.__fl_1_vlv_dev = None
        """Floor valve device.
        """

        self.__fl_2_vlv_dev = None
        """Floor valve device.
        """

        self.__fl_3_vlv_dev = None
        """Floor valve device.
        """

        self.__conv_1_dev = None
        """Convector 1 device.
        """

        self.__cl_1_vlv_dev = None
        """Convector valve device.
        """

        self.__conv_2_dev = None
        """Convector 2 device.
        """

        self.__cl_2_vlv_dev = None
        """Convector valve device.
        """

        self.__conv_3_dev = None
        """Convector 2 device.
        """

        self.__cl_3_vlv_dev = None
        """Convector valve device.
        """

        self.__window_closed_input = verbal_const.OFF
        """Window closed sensor input.
        """

        self.__conversion_table = \
        {
            -3.0: 0,
            -2.5: 1,
            -2.0: 1,
            -1.5: 2,
            -1.0: 2,
            -0.5: 3,
            0.0: 4,
            0.5: 5,
            1.0: 6,
            1.5: 6,
            2.0: 7,
            2.5: 7,
            3.0: 8
        }

        # Floor valve control table.
        self.__fl_control_table = \
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],       # 0 - Спряно
            [0, 0, 0, 0, 0, 1/4, 1/2, 1, 1], # 1 - Охлаждане 
            [1, 1, 1/2, 1/4, 0, 0, 0, 0, 0]  # 2 - Отопление
        ]

        # Convector control table.
        self.__conv_control_table = \
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0 - Спряно
            [0, 0, 0, 0, 0, 0, 1, 2, 3, 4], # 1 - Охлаждане 
            [4, 3, 2, 1, 0, 0, 0, 0, 0, 0]  # 2 - Отопление
        ]

        # Fan control table.
        self.__fan_control_table = \
        [
            [0, 0, 0, 0, 0, 50, 80, 120, 140], # 0 - Спряно
            [80, 50, 30, 0, 0, 0, 30, 50, 80], # 1 - Охлаждане 
            [0, 0, 0, 0, 0, 0, 0, 0, 0]        # 2 - Отопление
        ]


        self.__dt_temp = 0

        self.__thermal_force_limit = 0
        """Limit thermal force."""

        self.__delta_time = 1
        """Конфигурационен параметър, показващ за какво време
        назад се отчита изменението на температурата.
        Limits: (1 - 3)"""

        self.__adjust_temp = 0
        """Зададено отклонение от температурата
        (задава се от дисплея до вратата или през мобилен телефон, вързан в локалната мрежа)
        Limits: (-2.5 : 2.5)"""

        self.__goal_building_temp = 0
        """Целева температура на сградата.
        (подава се от централния сървър)
        Limits: (18-26)"""

        self.__delta_temp = 0
        """Изменението на температурата от последните минути.
        Limits: (-3 : 3)"""

        self.__thermal_force = 0
        """Каква топлинна сила трябва да приложим към системата
        (-100% означава максимално да охлаждаме, +100% - максимално да отопляваме)"""

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

        return

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

        self.__delta_time = register.value

    def __thermal_mode_cb(self, register):

        # Check data type.
        if not register.data_type == "int":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if ThermalMode.is_valid(register.value):
            self.__thermal_mode = ThermalMode(register.value)

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

        # Evry time you move the slider, it will take affec momentary.
        self.__update_now_flag = True

        # @see https://experta.bg/L/S/122745/m/Fwntindd
        min_temp = 2.5
        max_temp = -2.5

        min_temp_reg = self._registers.by_name(f"{self.key}.temp_{self.__identifier}.min")
        if min_temp_reg is not None:
            min_temp = min_temp_reg.value

        max_temp_reg = self._registers.by_name(f"{self.key}.temp_{self.__identifier}.max")
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

#region Private Methods (Registers Air Thermometers)

    def __air_temp_cent_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {}:
            if self.__air_temp_cent_dev is not None:
                self.__temp_proc.remove(self.__air_temp_cent_dev)
                self.__air_temp_cent_dev.shutdown()
                del self.__air_temp_cent_dev

            self.__air_temp_cent_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__air_temp_cent_dev is not None:
                self.__air_temp_cent_dev.init()
                self.__temp_proc.add(self.__air_temp_cent_dev)

        elif register.value == {}:
            if self.__air_temp_cent_dev is not None:
                self.__temp_proc.remove(self.__air_temp_cent_dev)
                self.__air_temp_cent_dev.shutdown()

    def __air_temp_lower_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {}:
            if self.__air_temp_lower_dev is not None:
                self.__temp_proc.remove(self.__air_temp_lower_dev)
                self.__air_temp_lower_dev.shutdown()
                del self.__air_temp_lower_dev

            self.__air_temp_lower_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__air_temp_lower_dev is not None:
                self.__air_temp_lower_dev.init()
                self.__temp_proc.add(self.__air_temp_lower_dev)

        elif register.value == {}:
            if self.__air_temp_lower_dev is not None:
                self.__temp_proc.remove(self.__air_temp_lower_dev)
                self.__air_temp_lower_dev.shutdown()

    def __air_temp_upper_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {}:
            if self.__air_temp_upper_dev is not None:
                self.__temp_proc.remove(self.__air_temp_upper_dev)
                self.__air_temp_upper_dev.shutdown()
                del self.__air_temp_upper_dev

            self.__air_temp_upper_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__air_temp_upper_dev is not None:
                self.__air_temp_upper_dev.init()
                self.__temp_proc.add(self.__air_temp_upper_dev)

        elif register.value == {}:
            if self.__air_temp_upper_dev is not None:
                self.__temp_proc.remove(self.__air_temp_upper_dev)
                self.__air_temp_upper_dev.shutdown()

    def __update_measurements(self):

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

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write(f"{self.key}.air_temp_lower_{self.__identifier}.value",
                              air_temp_lower_value)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write(f"{self.key}.air_temp_cent_{self.__identifier}.value",
                              air_temp_cent_value)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write(f"{self.key}.air_temp_upper_{self.__identifier}.value",
                              air_temp_upper_value)

#endregion

#region Private Methods (Registers envm)

    def __envm_energy_cb(self, register):

        # Check data type.
        if not ((register.data_type == "int") or (register.data_type == "float")):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # TODO: Get energy mode for the building.
        pass

    def __is_empty(self):

        value = False

        is_empty = self._registers.by_name("envm.is_empty")
        if is_empty is not None:
            value = is_empty.value

        return value

#endregion

#region Private Methods (Registers Devices)

    def __conv_1_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__conv_1_dev is not None:
                self.__conv_1_dev.shutdown()

            self.__conv_1_dev = ConvectorsFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__conv_1_dev is not None:
                self.__conv_1_dev.init()

        elif register.value == {}:
            if self.__conv_1_dev is not None:
                self.__conv_1_dev.shutdown()

    def __cl_1_vlv_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__cl_1_vlv_dev is not None:
                self.__cl_1_vlv_dev.shutdown()

            self.__cl_1_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_1_vlv_dev is not None:
                self.__cl_1_vlv_dev.init()

        elif register.value == {}:
            if self.__cl_1_vlv_dev is not None:
                self.__cl_1_vlv_dev.shutdown()

    def __conv_2_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__conv_2_dev is not None:
                self.__conv_2_dev.shutdown()

            self.__conv_2_dev = ConvectorsFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__conv_2_dev is not None:
                self.__conv_2_dev.init()

        elif register.value == {}:
            if self.__conv_2_dev is not None:
                self.__conv_2_dev.shutdown()

    def __cl_2_vlv_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__cl_2_vlv_dev is not None:
                self.__cl_2_vlv_dev.shutdown()

            self.__cl_2_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_2_vlv_dev is not None:
                self.__cl_2_vlv_dev.init()

        elif register.value == {}:
            if self.__cl_2_vlv_dev is not None:
                self.__cl_2_vlv_dev.shutdown()

    def __conv_3_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__conv_3_dev is not None:
                self.__conv_3_dev.shutdown()
                del self.__conv_3_dev

            self.__conv_3_dev = ConvectorsFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__conv_3_dev is not None:
                self.__conv_3_dev.init()

        elif register.value == {}:
            if self.__conv_3_dev is not None:
                self.__conv_3_dev.shutdown()

    def __cl_3_vlv_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__cl_3_vlv_dev is not None:
                self.__cl_3_vlv_dev.shutdown()
                del self.__cl_3_vlv_dev

            self.__cl_3_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_3_vlv_dev is not None:
                self.__cl_3_vlv_dev.init()

        elif register.value == {}:
            if self.__cl_3_vlv_dev is not None:
                self.__cl_3_vlv_dev.shutdown()

    def __fl_vlv_1_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__fl_1_vlv_dev is not None:
                self.__fl_1_vlv_dev.shutdown()
                del self.__fl_1_vlv_dev

            self.__fl_1_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_1_vlv_dev is not None:
                self.__fl_1_vlv_dev.init()

        elif register.value == {}:
            if self.__fl_1_vlv_dev is not None:
                self.__fl_1_vlv_dev.shutdown()

    def __fl_vlv_2_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__fl_2_vlv_dev is not None:
                self.__fl_2_vlv_dev.shutdown()
                del self.__fl_2_vlv_dev

            self.__fl_2_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_2_vlv_dev is not None:
                self.__fl_2_vlv_dev.init()

        elif register.value == {}:
            if self.__fl_2_vlv_dev is not None:
                self.__fl_2_vlv_dev.shutdown()

    def __fl_vlv_3_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {}:
            if self.__fl_3_vlv_dev is not None:
                self.__fl_3_vlv_dev.shutdown()
                del self.__fl_3_vlv_dev

            self.__fl_3_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_3_vlv_dev is not None:
                self.__fl_3_vlv_dev.init()

        elif register.value == {}:
            if self.__fl_3_vlv_dev is not None:
                self.__fl_3_vlv_dev.shutdown()

#endregion

#region Private Methods (Ventilation Interface)

    def __set_ventilation(self, value):

        # Set the ventilation.
        self._registers.write(f"vent.hvac_setpoint_{self.__identifier}", value)

#endregion

#region Private Methods (Registers Interface)

    def __init_registers(self):
        """Initialize the registers callbacks.
        """

        # Air temperatures.
        air_temp_cent_settings = self._registers.\
            by_name(f"{self.key}.air_temp_cent_{self.__identifier}.settings")
        if air_temp_cent_settings is not None:
            air_temp_cent_settings.update_handlers = self.__air_temp_cent_settings_cb
            air_temp_cent_settings.update()

        air_temp_lower_settings = self._registers.\
            by_name(f"{self.key}.air_temp_lower_{self.__identifier}.settings")
        if air_temp_lower_settings is not None:
            air_temp_lower_settings.update_handlers = self.__air_temp_lower_settings_cb
            air_temp_lower_settings.update()

        air_temp_upper_settings = self._registers.\
            by_name(f"{self.key}.air_temp_upper_{self.__identifier}.settings")
        if air_temp_upper_settings is not None:
            air_temp_upper_settings.update_handlers = self.__air_temp_upper_settings_cb
            air_temp_upper_settings.update()

        # Floor loop 1
        fl_vlv_1_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_1.valve.settings")
        if fl_vlv_1_dev_settings is not None:
            fl_vlv_1_dev_settings.update_handlers = self.__fl_vlv_1_settings_cb
            fl_vlv_1_dev_settings.update()

        # Floor loop 2
        fl_vlv_2_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_2.valve.settings")
        if fl_vlv_2_dev_settings is not None:
            fl_vlv_2_dev_settings.update_handlers = self.__fl_vlv_2_settings_cb
            fl_vlv_2_dev_settings.update()

        # Floor loop 3
        fl_vlv_3_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_3.valve.settings")
        if fl_vlv_3_dev_settings is not None:
            fl_vlv_3_dev_settings.update_handlers = self.__fl_vlv_3_settings_cb
            fl_vlv_3_dev_settings.update()

        # Convector loop 1
        conv_1_settings = self._registers.by_name(f"{self.key}.convector_1.settings")
        if conv_1_settings is not None:
            conv_1_settings.update_handlers = self.__conv_1_settings_cb
            conv_1_settings.update()


        cl_vlv_1_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_1.valve.settings")
        if cl_vlv_1_dev_settings is not None:
            cl_vlv_1_dev_settings.update_handlers = self.__cl_1_vlv_settings_cb
            cl_vlv_1_dev_settings.update()

        # Convector loop 2
        conv_2_settings = self._registers.by_name(f"{self.key}.convector_2.settings")
        if conv_2_settings is not None:
            conv_2_settings.update_handlers = self.__conv_2_settings_cb
            conv_2_settings.update()

        cl_vlv_2_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_2.valve.settings")
        if cl_vlv_2_dev_settings is not None:
            cl_vlv_2_dev_settings.update_handlers = self.__cl_2_vlv_settings_cb
            cl_vlv_2_dev_settings.update()

        # Convector loop 3
        conv_3_settings = self._registers.by_name(f"{self.key}.convector_3.settings")
        if conv_3_settings is not None:
            conv_3_settings.update_handlers = self.__conv_3_settings_cb
            conv_3_settings.update()

        cl_vlv_3_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_3.valve.settings")
        if cl_vlv_3_dev_settings is not None:
            cl_vlv_3_dev_settings.update_handlers = self.__cl_3_vlv_settings_cb
            cl_vlv_3_dev_settings.update()

        # Create window closed sensor.
        window_closed_input = self._registers.by_name(f"ac.window_closed_{self.__identifier}.input")
        if window_closed_input is not None:
            window_closed_input.update_handlers = self.__window_closed_input_cb
            window_closed_input.update()

        # Region parameters
        update_rate = self._registers.by_name(f"{self.key}.update_rate_{self.__identifier}")
        if update_rate is not None:
            update_rate.update_handlers = self.__update_rate_cb
            update_rate.update()

        delta_time = self._registers.by_name(f"{self.key}.delta_time_{self.__identifier}")
        if delta_time is not None:
            delta_time.update_handlers = self.__delta_time_cb
            delta_time.update()

        thermal_mode = self._registers.by_name(f"{self.key}.thermal_mode_{self.__identifier}")
        if thermal_mode is not None:
            thermal_mode.update_handlers = self.__thermal_mode_cb
            thermal_mode.update()

        thermal_force_limit = self._registers.\
            by_name(f"{self.key}.thermal_force_limit_{self.__identifier}")
        if thermal_force_limit is not None:
            thermal_force_limit.update_handlers = self.__thermal_force_limit_cb
            thermal_force_limit.update()

        adjust_temp = self._registers.by_name(f"{self.key}.temp_{self.__identifier}.adjust")
        if adjust_temp is not None:
            adjust_temp.update_handlers = self.__adjust_temp_cb
            adjust_temp.update()

        goal_building_temp = self._registers.by_name(f"{self.key}.goal_building_temp")
        if goal_building_temp is not None:
            goal_building_temp.update_handlers = self.__goal_building_temp_cb
            goal_building_temp.update()

        # Get the power mode of the building.
        envm_energy = self._registers.by_name("envm.energy")
        if envm_energy is not None:
            envm_energy.update_handlers = self.__envm_energy_cb
            envm_energy.update()

    def __is_hot_water(self):

        # TODO: Return water temperature from monitoring registers plugin.
        # monitoring.cl_1.hm.measurements, take last value to see is there any hot water.
        # monitoring.cl_2.hm.measurements, take last value to see is there any hot water.
        # monitoring.cl_3.hm.measurements, take last value to see is there any hot water.
        # monitoring.fl_1.hm.measurements, take last value to see is there any hot water.
        # monitoring.fl_2.hm.measurements, take last value to see is there any hot water.
        # monitoring.fl_3.hm.measurements, take last value to see is there any hot water.

        # Request: Eml6419
        # down_limit = 10

        # down_limit = self._registers.by_name(f"monitoring.cl_1.hm.measurements")
        # if down_limit is not None:
        #     down_limit_value = down_limit.value

        return True

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

#region Private Methods

    def __round_to_nearest_half(self, number):
        value = 0

        if number != 0:
            value = round(number * 2) / 2

        return value

    def __vlv_fl_1(self, position):
        if self.__fl_1_vlv_dev is None:
            return
        
        self.__fl_1_vlv_dev.target_position = position

    def __vlv_fl_2(self, position):
        if self.__fl_2_vlv_dev is None:
            return

        self.__fl_2_vlv_dev.target_position = position

    def __vlv_fl_3(self, position):
        if self.__fl_3_vlv_dev is None:
            return
        
        self.__fl_3_vlv_dev.target_position = position

    def __set_fl_state(self, duty_cycle):
        self.__vlv_fl_1_tmr.duty_cycle = duty_cycle
        self.__vlv_fl_2_tmr.duty_cycle = duty_cycle
        self.__vlv_fl_3_tmr.duty_cycle = duty_cycle

    def __set_cl_state(self, position):
        if self.__cl_1_vlv_dev is not None:
            self.__cl_1_vlv_dev.target_position = position

        if self.__cl_2_vlv_dev is not None:
            self.__cl_2_vlv_dev.target_position = position

        if self.__cl_3_vlv_dev is not None:
           self.__cl_3_vlv_dev.target_position = position

    def __set_conv_state(self, state=0):

        if state < 0:
            state = 0

        if state > 3:
            state = 3

        if self.__conv_1_dev is not None:
            self.__conv_1_dev.set_state(state)

        if self.__conv_2_dev is not None:
            self.__conv_2_dev.set_state(state)

        if self.__conv_3_dev is not None:
            self.__conv_3_dev.set_state(state)

    def __set_devices(self, state):

        last_state = len(self.__conversion_table) - 1

        if state < 0:
            state = 0

        if state > last_state:
            state = last_state

        conv_state = self.__conv_control_table[self.__thermal_mode.value][state]
        fl_state = self.__fl_control_table[self.__thermal_mode.value][state]
        fan_state = self.__fan_control_table[self.__thermal_mode.value][state]

        if state == 0:
            self.__set_fl_state(0)
            self.__set_cl_state(100)
            self.__set_conv_state(1)

        elif state == 1:
            self.__set_fl_state(1/3)
            self.__set_cl_state(100)
            self.__set_conv_state(0)

        elif state == 2:
            self.__set_fl_state(1/2)
            self.__set_cl_state(100)
            self.__set_conv_state(0)

        elif state == 3:
            self.__set_fl_state(1)
            self.__set_cl_state(100)
            self.__set_conv_state(0)

        elif state == 4:
            self.__set_fl_state(1)
            self.__set_cl_state(100)
            self.__set_conv_state(0)

        elif state == 5:
            self.__set_fl_state(1)
            self.__set_cl_state(100)
            self.__set_conv_state(0)

        elif state == 6:
            self.__set_fl_state(1)
            self.__set_cl_state(100)
            self.__set_conv_state(0)

#endregion

#region Protected Methods

    def _init(self):
        """Initialize the module.
        """
        
        self.__logger.info("Starting up the {} {}".format(self.name, self.__identifier))
        
        # Create registers callbacks.
        self.__init_registers()

    def _update(self):
        """ Update cycle.
        """

        # Update occupation flags.
        is_empty = self.__is_empty()

        # If the window is opened, just turn off the HVAC.
        window_tamper_state = self.__read_window_tamper()

        # If temperature is less then 10 deg on loop 1.
        is_hot_water = self.__is_hot_water()

        # Take all necessary condition for normal operation of the HVAC.
        # stop_flag = (not is_empty or not window_tamper_state or not is_hot_water)
        stop_flag = False

        # If it is time to stop.
        if stop_flag:
            # Activate 10 seconds timer to stop the HVAC.
            self.__stop_timer.update()
            # If it si expired.
            if self.__stop_timer.expired:
                # Clear the timer.
                self.__stop_timer.clear()
                # Flip the flag.
                if self.__stop_flag != stop_flag:
                    # And apply the stop flag.
                    self.__stop_flag = stop_flag

        # If it is time to stop.
        if not stop_flag:
            # Stop the HVAC.
            self.__stop_flag = False
            # Clear last time to provoke instant expiration of the update timer.
            self.__stop_timer.update_last_time(0)

        # If update now flag is activated.
        if self.__update_now_flag:
            # Clear the flag.
            self.__update_now_flag = False
            # Clear last time to provoke instant expiration of the update timer.
            self.__update_timer.update_last_time(0)

        # Update control timer.
        self.__update_timer.update()
        # If it is time to update.
        if self.__update_timer.expired:
            # Clear the timer.
            self.__update_timer.clear()

            # Update thermometers values.
            self.__update_measurements()

            # Recalculate the temperatures.
            self.__temp_proc.update()

            print(f"Target: {self.__adjust_temp:2.1f}; Current: {self.__temp_proc.value:2.1f}")

            # Calculate the delta.
            dt = self.__adjust_temp - self.__temp_proc.value

            print(f"dT: {dt:2.1f}")

            # Round to have clear rounded value for state machine currency.
            dt = self.__round_to_nearest_half(dt)

            # Correct the down limit.
            if dt < -3.0:
                dt = -3.0

            # Correct the upper limit.
            if dt > 3.0:
                dt = 3.0

            # Exit if there is no changes.
            # if self.__dt_temp == dt:
            #     return

            # Store last changes.
            self.__dt_temp = dt

            print(f"dT: {dt:2.1f}")

            state = self.__conversion_table[dt]

            print(f"State: {state:2.1f}")

            # Set the devices.
            self.__set_devices(state)

        # Update PWM timers for the valves.
        self.__vlv_fl_1_tmr.update()
        self.__vlv_fl_2_tmr.update()
        self.__vlv_fl_3_tmr.update()

        # Update floor valves.
        if self.__fl_1_vlv_dev is not None:
            self.__fl_1_vlv_dev.update()
        if self.__fl_2_vlv_dev is not None:
            self.__fl_2_vlv_dev.update()
        if self.__fl_3_vlv_dev is not None:
            self.__fl_3_vlv_dev.update()

        # Update convector valves.
        if self.__cl_1_vlv_dev is not None:
            self.__cl_1_vlv_dev.update()
        if self.__conv_1_dev is not None:
            self.__conv_1_dev.update()

        if self.__cl_2_vlv_dev is not None:
            self.__cl_2_vlv_dev.update()
        if self.__conv_2_dev is not None:
            self.__conv_2_dev.update()

        if self.__cl_3_vlv_dev is not None:
            self.__cl_3_vlv_dev.update()
        if self.__conv_3_dev is not None:
            self.__conv_3_dev.update()

    def _shutdown(self):
        """Shutdown the tamper.
        """

        self.__logger.info("Shutting down the {} {}".format(self.name, self.__identifier))

        if self.__cl_1_vlv_dev is not None:
            self.__cl_1_vlv_dev.shutdown()
            self.__cl_1_vlv_dev.update()

        if self.__conv_1_dev is not None:
            self.__conv_1_dev.shutdown()
            self.__conv_1_dev.update()

        if self.__cl_2_vlv_dev is not None:
            self.__cl_2_vlv_dev.shutdown()
            self.__cl_2_vlv_dev.update()

        if self.__conv_2_dev is not None:
            self.__conv_2_dev.shutdown()
            self.__conv_2_dev.update()

        if self.__cl_3_vlv_dev is not None:
            self.__cl_3_vlv_dev.shutdown()
            self.__cl_3_vlv_dev.update()

        if self.__conv_3_dev is not None:
            self.__conv_3_dev.shutdown()
            self.__conv_3_dev.update()

        if self.__fl_1_vlv_dev is not None:
            self.__fl_1_vlv_dev.shutdown()
            self.__fl_1_vlv_dev.update()

        if self.__fl_2_vlv_dev is not None:
            self.__fl_2_vlv_dev.shutdown()
            self.__fl_2_vlv_dev.update()

        if self.__fl_3_vlv_dev is not None:
            self.__fl_3_vlv_dev.shutdown()
            self.__fl_3_vlv_dev.update()

        self.__logger.info("Shuted down the {}".format(self.name))

#endregion
