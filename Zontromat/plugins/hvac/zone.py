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



    __fl_1_temp_dev = None
    """Floor thermometer device.
    """

    __fl_1_vlv_dev = None
    """Floor valve device.
    """

    __fl_1_hm_dev = None
    """Floor heat meter.
    """

    __fl_1_hm_measurements = []
    """Floor loop heat meter measurements.
    """


    __fl_2_temp_dev = None
    """Floor thermometer device.
    """

    __fl_2_vlv_dev = None
    """Floor valve device.
    """

    __fl_2_hm_dev = None
    """Floor heat meter.
    """

    __fl_2_hm_measurements = []
    """Floor loop heat meter measurements.
    """


    __fl_3_temp_dev = None
    """Floor thermometer device.
    """

    __fl_3_vlv_dev = None
    """Floor valve device.
    """

    __fl_3_hm_dev = None
    """Floor heat meter.
    """

    __fl_3_hm_measurements = []
    """Floor loop heat meter measurements.
    """


    __conv_1_dev = None
    """Convector 1 device.
    """

    __cl_1_temp_dev = None
    """Convector thermometer.
    """

    __cl_1_hm_dev = None
    """Convector heat meter.
    """

    __cl_1_vlv_dev = None
    """Convector valve device.
    """

    __cl_1_hm_measurements = []
    """Convector loop heat meter measurements.
    """


    __conv_2_dev = None
    """Convector 2 device.
    """

    __cl_2_temp_dev = None
    """Convector thermometer.
    """

    __cl_2_hm_dev = None
    """Convector heat meter.
    """

    __cl_2_vlv_dev = None
    """Convector valve device.
    """

    __cl_2_hm_measurements = []
    """Convector loop heat meter measurements.
    """


    __conv_3_dev = None
    """Convector 2 device.
    """

    __cl_3_temp_dev = None
    """Convector thermometer.
    """

    __cl_3_hm_dev = None
    """Convector heat meter.
    """

    __cl_3_vlv_dev = None
    """Convector valve device.
    """

    __cl_3_hm_measurements = []
    """Convector loop heat meter measurements.
    """


    __hm_demand_timer = None
    """Floor loop demand timer.
    """




    __update_timer = None
    """Main process update timer."""

    __stop_timer = None
    """Stop timer."""

    __experimental_update_timer = None
    """Experimental timer."""

    __experimental_counter = 0
    """Experimental timer."""

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

        if self.__fl_1_temp_dev is not None:
            del self.__fl_1_temp_dev

        if self.__fl_1_vlv_dev is not None:
            del self.__fl_1_vlv_dev

        if self.__fl_1_hm_dev is not None:
            del self.__fl_1_hm_dev

        if self.__cl_1_temp_dev is not None:
            del self.__cl_1_temp_dev

        if self.__cl_1_vlv_dev is not None:
            del self.__cl_1_vlv_dev

        if self.__cl_1_hm_dev is not None:
            del self.__cl_1_hm_dev

        if self.__thermal_mode is not None:
            del self.__thermal_mode

        if self.__update_timer is not None:
            del self.__update_timer

        if self.__stop_timer is not None:
            del self.__stop_timer

        if self.__queue_temperatures is not None:
            del self.__queue_temperatures

        if self.__experimental_update_timer is not None:
            del self.__experimental_update_timer

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
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

        elif register.value != {} and self.__air_temp_cent_dev is not None:
            self.__temp_proc.remove(self.__air_temp_cent_dev)
            self.__air_temp_cent_dev.shutdown()
            del self.__air_temp_cent_dev
            self.__air_temp_cent_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

        elif register.value == {} and self.__air_temp_cent_dev is not None:
            self.__temp_proc.remove(self.__air_temp_cent_dev)
            self.__air_temp_cent_dev.shutdown()
            del self.__air_temp_cent_dev

        if self.__air_temp_cent_dev is not None:
            self.__air_temp_cent_dev.init()
            self.__temp_proc.add(self.__air_temp_cent_dev)


    def __air_temp_lower_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {} and self.__air_temp_lower_dev is None:
            self.__air_temp_lower_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

        elif register.value != {} and self.__air_temp_lower_dev is not None:
            self.__temp_proc.remove(self.__air_temp_lower_dev)
            self.__air_temp_lower_dev.shutdown()
            del self.__air_temp_lower_dev
            self.__air_temp_lower_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

        elif register.value == {} and self.__air_temp_lower_dev is not None:
            self.__temp_proc.remove(self.__air_temp_lower_dev)
            self.__air_temp_lower_dev.shutdown()
            del self.__air_temp_lower_dev

        if self.__air_temp_lower_dev is not None:
            self.__air_temp_lower_dev.init()
            self.__temp_proc.add(self.__air_temp_lower_dev)

    def __air_temp_upper_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {} and self.__air_temp_upper_dev is None:
            self.__air_temp_upper_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

        elif register.value != {} and self.__air_temp_upper_dev is not None:
            self.__temp_proc.remove(self.__air_temp_upper_dev)
            self.__air_temp_upper_dev.shutdown()
            del self.__air_temp_upper_dev
            self.__air_temp_upper_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

        elif register.value == {} and self.__air_temp_upper_dev is not None:
            self.__temp_proc.remove(self.__air_temp_upper_dev)
            self.__air_temp_upper_dev.shutdown()
            del self.__air_temp_upper_dev

        if self.__air_temp_upper_dev is not None:
            self.__air_temp_upper_dev.init()
            self.__temp_proc.add(self.__air_temp_upper_dev)

#endregion

#region Private Methods (Registers Floor Loop 1)

    def __fl_1_update_measurements(self):

        if self.__fl_1_temp_dev is None and self.__fl_1_hm_dev is None:
            return

        measurement = {}

        measurement["PositiveCumulativeEnergy"] = self.__fl_1_hm_dev.get_pcenergy()
        measurement["InletWaterTemperature"] = self.__fl_1_hm_dev.get_inlet_temp()
        measurement["ReturnWaterTemperature"] = self.__fl_1_hm_dev.get_return_temp()

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__fl_1_hm_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        # filter_measurements_by_time(self.__fl_1_hm_measurements, 86400)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write("{}.floor_loop_{}.temp.measurements".format(self.key, self.__identifier), json.dumps(self.__fl_1_hm_measurements))

    def __fl_hm_1_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__fl_1_hm_dev is None:
            self.__fl_1_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_1_hm_dev is not None:
                self.__fl_1_hm_dev.init()

        elif register.value != {} and self.__fl_1_hm_dev is not None:
            self.__fl_1_hm_dev.shutdown()
            del self.__fl_1_hm_dev
            self.__fl_1_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_1_hm_dev is not None:
                self.__fl_1_hm_dev.init()

        elif register.value == {} and self.__fl_1_hm_dev is not None:
            self.__fl_1_hm_dev.shutdown()
            del self.__fl_1_hm_dev

    def __fl_temp_1_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__fl_1_temp_dev is None:

            self.__fl_1_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_1_temp_dev is not None:
                self.__fl_1_temp_dev.init()

        elif register.value != {} and self.__fl_1_temp_dev is not None:
            self.__fl_1_temp_dev.shutdown()
            del self.__fl_1_temp_dev
            self.__fl_1_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_1_temp_dev is not None:
                self.__fl_1_temp_dev.init()

        elif register.value == {} and self.__fl_1_temp_dev is not None:
            self.__fl_1_temp_dev.shutdown()
            del self.__fl_1_temp_dev

    def __fl_vlv_1_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__fl_1_vlv_dev is None:

            self.__fl_1_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_1_vlv_dev is not None:
                self.__fl_1_vlv_dev.init()

        elif register.value != {} and self.__fl_1_vlv_dev is not None:
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

        elif register.value == {} and self.__fl_1_vlv_dev is not None:
            self.__fl_1_vlv_dev.shutdown()
            del self.__fl_1_vlv_dev

#endregion

#region Private Methods (Registers Floor Loop 2)

    def __fl_2_update_measurements(self):

        if self.__fl_2_temp_dev is None and self.__fl_2_hm_dev is None:
            return

        measurement = {}

        measurement["PositiveCumulativeEnergy"] = self.__fl_2_hm_dev.get_pcenergy()
        measurement["InletWaterTemperature"] = self.__fl_2_hm_dev.get_inlet_temp()
        measurement["ReturnWaterTemperature"] = self.__fl_2_hm_dev.get_return_temp()

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__fl_2_hm_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        filter_measurements_by_time(self.__fl_2_hm_measurements, 86400)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write(f"{self.key}.floor_loop_2.temp.measurements", json.dumps(self.__fl_2_hm_measurements))

    def __fl_hm_2_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__fl_2_hm_dev is None:
            self.__fl_2_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_2_hm_dev is not None:
                self.__fl_2_hm_dev.init()

        elif register.value != {} and self.__fl_2_hm_dev is not None:
            self.__fl_2_hm_dev.shutdown()
            del self.__fl_2_hm_dev
            self.__fl_2_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_2_hm_dev is not None:
                self.__fl_2_hm_dev.init()

        elif register.value == {} and self.__fl_2_hm_dev is not None:
            self.__fl_2_hm_dev.shutdown()
            del self.__fl_2_hm_dev

    def __fl_temp_2_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__fl_2_temp_dev is None:

            self.__fl_2_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_2_temp_dev is not None:
                self.__fl_2_temp_dev.init()

        elif register.value != {} and self.__fl_2_temp_dev is not None:
            self.__fl_2_temp_dev.shutdown()
            del self.__fl_2_temp_dev
            self.__fl_2_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_2_temp_dev is not None:
                self.__fl_2_temp_dev.init()

        elif register.value == {} and self.__fl_2_temp_dev is not None:
            self.__fl_2_temp_dev.shutdown()
            del self.__fl_2_temp_dev

    def __fl_vlv_2_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__fl_2_vlv_dev is None:

            self.__fl_2_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_2_vlv_dev is not None:
                self.__fl_2_vlv_dev.init()

        elif register.value != {} and self.__fl_2_vlv_dev is not None:
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

        elif register.value == {} and self.__fl_2_vlv_dev is not None:
            self.__fl_2_vlv_dev.shutdown()
            del self.__fl_2_vlv_dev

#endregion

#region Private Methods (Registers Floor Loop 3)

    def __fl_3_update_measurements(self):

        if self.__fl_3_temp_dev is None and self.__fl_3_hm_dev is None:
            return

        measurement = {}

        measurement["PositiveCumulativeEnergy"] = self.__fl_3_hm_dev.get_pcenergy()
        measurement["InletWaterTemperature"] = self.__fl_3_hm_dev.get_inlet_temp()
        measurement["ReturnWaterTemperature"] = self.__fl_3_hm_dev.get_return_temp()

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__fl_3_hm_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        filter_measurements_by_time(self.__fl_3_hm_measurements, 86400)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write(f"{self.key}.floor_loop_3.temp.measurements", json.dumps(self.__fl_3_hm_measurements))

    def __fl_hm_3_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return
        
        if register.value != {} and self.__fl_3_hm_dev is None:
            self.__fl_3_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_3_hm_dev is not None:
                self.__fl_3_hm_dev.init()
        
        elif register.value != {} and self.__fl_3_hm_dev is not None:
            self.__fl_3_hm_dev.shutdown()
            del self.__fl_3_hm_dev
            self.__fl_3_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_3_hm_dev is not None:
                self.__fl_3_hm_dev.init()

        elif register.value == {} and self.__fl_3_hm_dev is not None:
            self.__fl_3_hm_dev.shutdown()
            del self.__fl_3_hm_dev

    def __fl_temp_3_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__fl_3_temp_dev is None:

            self.__fl_3_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_3_temp_dev is not None:
                self.__fl_3_temp_dev.init()

        elif register.value != {} and self.__fl_3_temp_dev is not None:
            self.__fl_3_temp_dev.shutdown()
            del self.__fl_3_temp_dev
            self.__fl_3_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_3_temp_dev is not None:
                self.__fl_3_temp_dev.init()

        elif register.value == {} and self.__fl_3_temp_dev is not None:
            self.__fl_3_temp_dev.shutdown()
            del self.__fl_3_temp_dev

    def __fl_vlv_3_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__fl_3_vlv_dev is None:
            self.__fl_3_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__fl_3_vlv_dev is not None:
                self.__fl_3_vlv_dev.init()

        if register.value != {} and self.__fl_3_vlv_dev is None:
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

        elif register.value == {} and self.__fl_3_vlv_dev is not None:
            self.__fl_3_vlv_dev.shutdown()
            del self.__fl_3_vlv_dev

#endregion

#region Private Methods (Registers Convector Loop 1)

    def __cl_1_update_measurements(self):

        if self.__cl_1_temp_dev is None and self.__cl_1_hm_dev is None:
            return

        measurement = {}

        measurement["PositiveCumulativeEnergy"] = self.__cl_1_hm_dev.get_pcenergy()
        measurement["InletWaterTemperature"] = self.__cl_1_hm_dev.get_inlet_temp()
        measurement["ReturnWaterTemperature"] = self.__cl_1_hm_dev.get_return_temp()

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__cl_1_hm_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        filter_measurements_by_time(self.__cl_1_hm_measurements, 86400)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write(f"{self.key}.conv_loop_1.temp.measurements", json.dumps(self.__cl_1_hm_measurements))

    def __conv_1_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__conv_1_dev is None:

            self.__conv_1_dev = ConvectorsFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__conv_1_dev is not None:
                self.__conv_1_dev.init()

        elif register.value != {} and self.__conv_1_dev is not None:
            self.__conv_1_dev.shutdown()
            del self.__conv_1_dev
            self.__conv_1_dev = ConvectorsFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__conv_1_dev is not None:
                self.__conv_1_dev.init()

        elif register.value == {} and self.__conv_1_dev is not None:
            self.__conv_1_dev.shutdown()
            del self.__conv_1_dev

    def __cl_1_hm_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_1_hm_dev is None:
            self.__cl_1_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_1_hm_dev is not None:
                self.__cl_1_hm_dev.init()

        elif register.value != {} and self.__cl_1_hm_dev is not None:
            self.__cl_1_hm_dev.shutdown()
            del self.__cl_1_hm_dev
            self.__cl_1_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_1_hm_dev is not None:
                self.__cl_1_hm_dev.init()

        elif register.value == {} and self.__cl_1_hm_dev is not None:
            self.__cl_1_hm_dev.shutdown()
            del self.__cl_1_hm_dev

    def __cl_1_temp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_1_temp_dev is None:

            self.__cl_1_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_1_temp_dev is not None:
                self.__cl_1_temp_dev.init()

        elif register.value != {} and self.__cl_1_temp_dev is None:
            self.__cl_1_temp_dev.shutdown()
            del self.__cl_1_temp_dev
            self.__cl_1_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_1_temp_dev is not None:
                self.__cl_1_temp_dev.init()

        elif register.value == {} and self.__cl_1_temp_dev is not None:
            self.__cl_1_temp_dev.shutdown()
            del self.__cl_1_temp_dev

    def __cl_1_vlv_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_1_vlv_dev is None:

            self.__cl_1_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_1_vlv_dev is not None:
                self.__cl_1_vlv_dev.init()

        elif register.value != {} and self.__cl_1_vlv_dev is not None:
            self.__cl_1_vlv_dev.shutdown()
            del self.__cl_1_vlv_dev
            self.__cl_1_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_1_vlv_dev is not None:
                self.__cl_1_vlv_dev.init()

        elif register.value == {} and self.__cl_1_vlv_dev is not None:
            self.__cl_1_vlv_dev.shutdown()
            del self.__cl_1_vlv_dev

#endregion

#region Private Methods (Registers Convector Loop 2)

    def __cl_2_update_measurements(self):

        if self.__cl_2_temp_dev is None and self.__cl_2_hm_dev is None:
            return

        measurement = {}

        measurement["PositiveCumulativeEnergy"] = self.__cl_2_hm_dev.get_pcenergy()
        measurement["InletWaterTemperature"] = self.__cl_2_hm_dev.get_inlet_temp()
        measurement["ReturnWaterTemperature"] = self.__cl_2_hm_dev.get_return_temp()

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__cl_2_hm_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        filter_measurements_by_time(self.__cl_2_hm_measurements, 86400)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write(f"{self.key}.conv_loop_2.temp.measurements", json.dumps(self.__cl_2_hm_measurements))

    def __conv_2_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__conv_2_dev is None:

            self.__conv_2_dev = ConvectorsFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__conv_2_dev is not None:
                self.__conv_2_dev.init()

        elif register.value != {} and self.__conv_2_dev is not None:
            self.__conv_2_dev.shutdown()
            del self.__conv_2_dev
            self.__conv_2_dev = ConvectorsFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__conv_2_dev is not None:
                self.__conv_2_dev.init()

        elif register.value == {} and self.__conv_2_dev is not None:
            self.__conv_2_dev.shutdown()
            del self.__conv_2_dev

    def __cl_2_hm_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_2_hm_dev is None:
            self.__cl_2_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_2_hm_dev is not None:
                self.__cl_2_hm_dev.init()

        elif register.value != {} and self.__cl_2_hm_dev is not None:
            self.__cl_2_hm_dev.shutdown()
            del self.__cl_2_hm_dev
            self.__cl_2_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_2_hm_dev is not None:
                self.__cl_2_hm_dev.init()

        elif register.value == {} and self.__cl_2_hm_dev is not None:
            self.__cl_2_hm_dev.shutdown()
            del self.__cl_2_hm_dev

    def __cl_2_temp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_2_temp_dev is None:

            self.__cl_2_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_2_temp_dev is not None:
                self.__cl_2_temp_dev.init()

        elif register.value != {} and self.__cl_2_temp_dev is not None:
            self.__cl_2_temp_dev.shutdown()
            del self.__cl_2_temp_dev
            self.__cl_2_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_2_temp_dev is not None:
                self.__cl_2_temp_dev.init()

        elif register.value == {} and self.__cl_2_temp_dev is not None:
            self.__cl_2_temp_dev.shutdown()
            del self.__cl_2_temp_dev

    def __cl_2_vlv_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_2_vlv_dev is None:

            self.__cl_2_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_2_vlv_dev is not None:
                self.__cl_2_vlv_dev.init()

        elif register.value != {} and self.__cl_2_vlv_dev is not None:
            self.__cl_2_vlv_dev.shutdown()
            del self.__cl_2_vlv_dev
            self.__cl_2_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_2_vlv_dev is not None:
                self.__cl_2_vlv_dev.init()

        elif register.value == {} and self.__cl_2_vlv_dev is not None:
            self.__cl_2_vlv_dev.shutdown()
            del self.__cl_2_vlv_dev

#endregion

#region Private Methods (Registers Convector Loop 3)

    def __cl_3_update_measurements(self):

        if self.__cl_3_temp_dev is None and self.__cl_3_hm_dev is None:
            return

        measurement = {}

        measurement["PositiveCumulativeEnergy"] = self.__cl_3_hm_dev.get_pcenergy()
        measurement["InletWaterTemperature"] = self.__cl_3_hm_dev.get_inlet_temp()
        measurement["ReturnWaterTemperature"] = self.__cl_3_hm_dev.get_return_temp()

        # Set the time of the measurement.
        measurement["ts"] = time.time()

        # Add measurement to the tail.
        self.__cl_3_hm_measurements.append(measurement)

        # This magical number represents seconds for 24 hours.
        filter_measurements_by_time(self.__cl_3_hm_measurements, 86400)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write(f"{self.key}.conv_loop_3.temp.measurements", json.dumps(self.__cl_3_hm_measurements))

    def __conv_3_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__conv_3_dev is None:

            self.__conv_3_dev = ConvectorsFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__conv_3_dev is not None:
                self.__conv_3_dev.init()

        elif register.value != {} and self.__conv_3_dev is not None:
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

        elif register.value == {} and self.__conv_3_dev is not None:
            self.__conv_3_dev.shutdown()
            del self.__conv_3_dev

    def __cl_3_hm_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_3_hm_dev is None:
            self.__cl_3_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_3_hm_dev is not None:
                self.__cl_3_hm_dev.init()

        elif register.value != {} and self.__cl_3_hm_dev is not None:
            self.__cl_3_hm_dev.shutdown()
            del self.__cl_3_hm_dev
            self.__cl_3_hm_dev = FlowmeterFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_3_hm_dev is not None:
                self.__cl_3_hm_dev.init()

        elif register.value == {} and self.__cl_3_hm_dev is not None:
            self.__cl_3_hm_dev.shutdown()
            del self.__cl_3_hm_dev

    def __cl_3_temp_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_3_temp_dev is None:

            self.__cl_3_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_3_temp_dev is not None:
                self.__cl_3_temp_dev.init()

        elif register.value != {} and self.__cl_3_temp_dev is not None:
            self.__cl_3_temp_dev.shutdown()
            del self.__cl_3_temp_dev
            self.__cl_3_temp_dev = ThermometersFactory.create(
                controller=self._controller,
                name=register.description,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_3_temp_dev is not None:
                self.__cl_3_temp_dev.init()

        elif register.value == {} and self.__cl_3_temp_dev is not None:
            self.__cl_3_temp_dev.shutdown()
            del self.__cl_3_temp_dev

    def __cl_3_vlv_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__cl_3_vlv_dev is None:

            self.__cl_3_vlv_dev = ValveFactory.create(
                name=register.description,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__cl_3_vlv_dev is not None:
                self.__cl_3_vlv_dev.init()

        if register.value != {} and self.__cl_3_vlv_dev is not None:
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

        elif register.value == {} and self.__cl_3_vlv_dev is not None:
            self.__cl_3_vlv_dev.shutdown()
            del self.__cl_3_vlv_dev

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


        # Floor loop 1
        fl_hm_1_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_1.flowmeter.settings")
        if fl_hm_1_dev_settings is not None:
            fl_hm_1_dev_settings.update_handlers = self.__fl_hm_1_settings_cb
            fl_hm_1_dev_settings.update()

        fl_temp_1_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_1.temp.settings")
        if fl_temp_1_dev_settings is not None:
            fl_temp_1_dev_settings.update_handlers = self.__fl_temp_1_settings_cb
            fl_temp_1_dev_settings.update()

        fl_vlv_1_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_1.valve.settings")
        if fl_vlv_1_dev_settings is not None:
            fl_vlv_1_dev_settings.update_handlers = self.__fl_vlv_1_settings_cb
            fl_vlv_1_dev_settings.update()

        # Floor loop 2
        fl_hm_2_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_2.flowmeter.settings")
        if fl_hm_2_dev_settings is not None:
            fl_hm_2_dev_settings.update_handlers = self.__fl_hm_2_settings_cb
            fl_hm_2_dev_settings.update()

        fl_temp_2_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_2.temp.settings")
        if fl_temp_2_dev_settings is not None:
            fl_temp_2_dev_settings.update_handlers = self.__fl_temp_2_settings_cb
            fl_temp_2_dev_settings.update()

        fl_vlv_2_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_2.valve.settings")
        if fl_vlv_2_dev_settings is not None:
            fl_vlv_2_dev_settings.update_handlers = self.__fl_vlv_2_settings_cb
            fl_vlv_2_dev_settings.update()

        # Floor loop 3
        fl_hm_3_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_3.flowmeter.settings")
        if fl_hm_3_dev_settings is not None:
            fl_hm_3_dev_settings.update_handlers = self.__fl_hm_3_settings_cb
            fl_hm_3_dev_settings.update()

        fl_temp_3_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_3.temp.settings")
        if fl_temp_3_dev_settings is not None:
            fl_temp_3_dev_settings.update_handlers = self.__fl_temp_3_settings_cb
            fl_temp_3_dev_settings.update()

        fl_vlv_3_dev_settings = self._registers.by_name(f"{self.key}.floor_loop_3.valve.settings")
        if fl_vlv_3_dev_settings is not None:
            fl_vlv_3_dev_settings.update_handlers = self.__fl_vlv_3_settings_cb
            fl_vlv_3_dev_settings.update()

        # Convector loop 1
        conv_1_settings = self._registers.by_name(f"{self.key}.convector_1.settings")
        if conv_1_settings is not None:
            conv_1_settings.update_handlers = self.__conv_1_settings_cb
            conv_1_settings.update()

        cl_hm_1_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_1.flowmeter.settings")
        if cl_hm_1_dev_settings is not None:
            cl_hm_1_dev_settings.update_handlers = self.__cl_1_hm_settings_cb
            cl_hm_1_dev_settings.update()

        cl_temp_1_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_1.temp.settings")
        if cl_temp_1_dev_settings is not None:
            cl_temp_1_dev_settings.update_handlers = self.__cl_1_temp_settings_cb
            cl_temp_1_dev_settings.update()

        cl_vlv_1_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_1.valve.settings")
        if cl_vlv_1_dev_settings is not None:
            cl_vlv_1_dev_settings.update_handlers = self.__cl_1_vlv_settings_cb
            cl_vlv_1_dev_settings.update()

        # Convector loop 2
        conv_2_settings = self._registers.by_name(f"{self.key}.convector_2.settings")
        if conv_2_settings is not None:
            conv_2_settings.update_handlers = self.__conv_2_settings_cb
            conv_2_settings.update()

        cl_hm_2_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_2.flowmeter.settings")
        if cl_hm_2_dev_settings is not None:
            cl_hm_2_dev_settings.update_handlers = self.__cl_2_hm_settings_cb
            cl_hm_2_dev_settings.update()

        cl_temp_2_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_2.temp.settings")
        if cl_temp_2_dev_settings is not None:
            cl_temp_2_dev_settings.update_handlers = self.__cl_2_temp_settings_cb
            cl_temp_2_dev_settings.update()

        cl_vlv_2_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_2.valve.settings")
        if cl_vlv_2_dev_settings is not None:
            cl_vlv_2_dev_settings.update_handlers = self.__cl_2_vlv_settings_cb
            cl_vlv_2_dev_settings.update()

        # Convector loop 3
        conv_3_settings = self._registers.by_name(f"{self.key}.convector_3.settings")
        if conv_3_settings is not None:
            conv_3_settings.update_handlers = self.__conv_3_settings_cb
            conv_3_settings.update()

        cl_hm_3_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_3.flowmeter.settings")
        if cl_hm_3_dev_settings is not None:
            cl_hm_3_dev_settings.update_handlers = self.__cl_3_hm_settings_cb
            cl_hm_3_dev_settings.update()

        cl_temp_3_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_3.temp.settings")
        if cl_temp_3_dev_settings is not None:
            cl_temp_3_dev_settings.update_handlers = self.__cl_3_temp_settings_cb
            cl_temp_3_dev_settings.update()

        cl_vlv_3_dev_settings = self._registers.by_name(f"{self.key}.conv_loop_3.valve.settings")
        if cl_vlv_3_dev_settings is not None:
            cl_vlv_3_dev_settings.update_handlers = self.__cl_3_vlv_settings_cb
            cl_vlv_3_dev_settings.update()


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

        adjust_temp = self._registers.by_name("{}.temp_{}.adjust".format(self.key, self.__identifier))
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
        self._registers.write("{}.air_temp_lower_{}.value".format(self.key, self.__identifier), air_temp_lower_value)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write("{}.air_temp_cent_{}.value".format(self.key, self.__identifier), air_temp_cent_value)

        # 2. If the following register is available then set ist value to the thermometers value.
        self._registers.write("{}.air_temp_upper_{}.value".format(self.key, self.__identifier), air_temp_upper_value)

    def __is_empty(self):

        value = False

        is_empty = self._registers.by_name("envm.is_empty")
        if is_empty is not None:
            value = is_empty.value

        return value

    def __get_down_limit_temp(self):

        # Request: Eml6419
        value = 10

        down_limit = self._registers.by_name("{}.floor_{}.temp.down_limit".format(self.key, self.__identifier))
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

#region Private Methods

    def __is_hot_water(self):

        down_limit_value = self.__get_down_limit_temp()

        temperature = 0
        if self.__fl_1_temp_dev is not None:
            temperature = self.__fl_1_temp_dev.get_temp()

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
                self.__fl_1_vlv_dev.target_position = 0
                self.__cl_1_vlv_dev.target_position = 0
            elif thermal_force <= 0:
                self.__fl_1_vlv_dev.target_position = 100
                self.__cl_1_vlv_dev.target_position = 100

        elif self.__thermal_mode.is_state(ThermalMode.TransisionSeason):
            if thermal_force < 0:
                self.__fl_1_vlv_dev.target_position = 100
                self.__cl_1_vlv_dev.target_position = 0
            elif thermal_force > 0:
                self.__fl_1_vlv_dev.target_position = 0
                self.__cl_1_vlv_dev.target_position = 100
            else:
                self.__fl_1_vlv_dev.target_position = 0
                self.__cl_1_vlv_dev.target_position = 0

        elif self.__thermal_mode.is_state(ThermalMode.WarmSeason):
            if thermal_force < 0:
                self.__fl_1_vlv_dev.target_position = 100
                self.__cl_1_vlv_dev.target_position = 100
            elif thermal_force > 0:
                self.__fl_1_vlv_dev.target_position = 0
                self.__cl_1_vlv_dev.target_position = 0

        # If thermal mode set properly apply thermal force
        if not self.__thermal_mode.is_state(ThermalMode.NONE):

            self.__set_ventilation(thermal_force)

            # Set convector fan.
            conv_tf = l_scale(thermal_force, [0, 100], [0, 3])
            conv_tf = abs(conv_tf)
            conv_tf = int(conv_tf)
            self.__conv_1_dev.set_state(conv_tf)

    def __calc(self):
        """_summary_
        """

        # Update thermometers values.
        self.__update_measurements()

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

            self._registers.write("{}.temp_{}.actual".format(self.key, self.__identifier), temperature)

        # Recalculate delta time.
        # pass_time = time.time() - self.__lastupdate_delta_time
        # if pass_time > self.__delta_time:
        #     self.__delta_temp = temperature - self.__delta_temp
        #     self.__logger.debug("DT: {:3.3f}".format(self.__delta_temp))

        #     # Update current time.
        #     self.__lastupdate_delta_time = time.time()

        self.__fl_1_vlv_dev.update()
        self.__cl_1_vlv_dev.update()
        self.__conv_1_dev.update()

    def __test_update(self):

        self.__hm_demand_timer.update()
        if self.__hm_demand_timer.expired:
            self.__hm_demand_timer.clear()

            self.__fl_1_update_measurements()
            self.__fl_2_update_measurements()
            self.__fl_3_update_measurements()
            self.__cl_1_update_measurements()
            self.__cl_2_update_measurements()
            self.__cl_3_update_measurements()

        self.__experimental_update_timer.update()
        if self.__experimental_update_timer.expired:
            self.__experimental_update_timer.clear()

            # Update thermometers values.
            self.__update_measurements()

            if self.__experimental_counter == 0:
                if self.__fl_1_vlv_dev is not None:
                    self.__fl_1_vlv_dev.target_position = 100

            elif self.__experimental_counter == 5:
                if self.__fl_2_vlv_dev is not None:
                    self.__fl_2_vlv_dev.target_position = 100

            elif self.__experimental_counter == 10:
                if self.__fl_3_vlv_dev is not None:
                    self.__fl_3_vlv_dev.target_position = 100

            elif self.__experimental_counter == 15:
                if self.__cl_1_vlv_dev is not None:
                    self.__cl_1_vlv_dev.target_position = 100
                # if self.__conv_1_dev is not None:
                #     self.__conv_1_dev.set_state(1)

            elif self.__experimental_counter == 20:
                if self.__cl_2_vlv_dev is not None:
                    self.__cl_2_vlv_dev.target_position = 100
                # if self.__conv_2_dev is not None:
                #     self.__conv_2_dev.set_state(1)

            elif self.__experimental_counter == 25:
                if self.__cl_3_vlv_dev is not None:
                    self.__cl_3_vlv_dev.target_position = 100
                # if self.__conv_3_dev is not None:
                #     self.__conv_3_dev.set_state(1)

            # Increment
            self.__experimental_counter += 1

            # Reset
            if self.__experimental_counter > 25:
                self.__experimental_counter = 0

        if self.__fl_1_vlv_dev is not None:
            self.__fl_1_vlv_dev.update()
        if self.__cl_1_vlv_dev is not None:
            self.__cl_1_vlv_dev.update()
        if self.__conv_1_dev is not None:
            self.__conv_1_dev.update()

        if self.__fl_2_vlv_dev is not None:
            self.__fl_2_vlv_dev.update()
        if self.__cl_2_vlv_dev is not None:
            self.__cl_2_vlv_dev.update()
        if self.__conv_2_dev is not None:
            self.__conv_2_dev.update()
        
        if self.__fl_3_vlv_dev is not None:
            self.__fl_3_vlv_dev.update()
        if self.__cl_3_vlv_dev is not None:
            self.__cl_3_vlv_dev.update()
        if self.__conv_3_dev is not None:
            self.__conv_3_dev.update()

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

        # Only for test.
        self.__experimental_update_timer = Timer(1)

        self.__hm_demand_timer = Timer(10)

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

        self.__test_update()

    def _shutdown(self):
        """Shutdown the tamper.
        """

        self.__logger.info("Shutting down the {} {}".format(self.name, self.__identifier))
        self.__set_thermal_force(0)


        if self.__fl_1_vlv_dev is not None:
            self.__fl_1_vlv_dev.shutdown()
            self.__fl_1_vlv_dev.update()
        if self.__cl_1_vlv_dev is not None:
            self.__cl_1_vlv_dev.shutdown()
            self.__cl_1_vlv_dev.update()
        if self.__conv_1_dev is not None:
            self.__conv_1_dev.shutdown()
            self.__conv_1_dev.update()

        if self.__fl_2_vlv_dev is not None:
            self.__fl_2_vlv_dev.shutdown()
            self.__fl_2_vlv_dev.update()
        if self.__cl_2_vlv_dev is not None:
            self.__cl_2_vlv_dev.shutdown()
            self.__cl_2_vlv_dev.update()
        if self.__conv_2_dev is not None:
            self.__conv_2_dev.shutdown()
            self.__conv_2_dev.update()

        if self.__fl_3_vlv_dev is not None:
            self.__fl_3_vlv_dev.shutdown()
            self.__fl_3_vlv_dev.update()
        if self.__cl_3_vlv_dev is not None:
            self.__cl_3_vlv_dev.shutdown()
            self.__cl_3_vlv_dev.update()
        if self.__conv_3_dev is not None:
            self.__conv_3_dev.shutdown()
            self.__conv_3_dev.update()

#endregion
