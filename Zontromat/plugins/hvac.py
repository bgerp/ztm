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

from plugins.base_plugin import BasePlugin

from devices.HangzhouAirflowElectricApplications.f3p146ec072600 import F3P146EC072600
from devices.TONHE.a20m15b2c import A20M15B2C
from devices.SILPA.klimafan import Klimafan
from devices.Dallas.ds18b20 import DS18B20

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

class TestState(Enum):
    """Test state"""

    NONE = 0
    TekeFirstMeasurement = 1
    TurnOffPeripheral = 2
    WaitForLeak = 3
    TekeSecondMeasurement = 1

class OperationMode(Enum):
    """Operation modes description."""

    NONE = 0
    Operational = 1
    LeakTest = 2
    LeakInLoop1 = 3
    LeakInLoop2 = 4
    LeaInBothLoops = 6

class ThermalMode(Enum):
    """Thermal modes description."""

    NONE = 0
    COLD_SESON = 1
    TRANSISION_SEASON = 2
    WARM_SEASON = 3

class HVAC(BasePlugin):
    """Heating ventilation and air conditioning."""

#region Attributes

    __logger = None
    """Logger"""

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


    __loop2_fan_dev = None
    """Loop 1 fan device."""

    __loop2_temp_dev = None
    """Loop 2 thermometer."""

    __loop2_valve_dev = None
    """Loop 2 valve device."""


    __test_state = None
    """Test state machine."""

    __operation_mode = None
    """Operation mode machine."""

    __thermal_mode = None
    """Thermal mode of the HVAC."""


    __update_timer = None
    """Main process update timer."""

    __test_time_timer = None
    """Test time timer."""

    __leak_test_timer = None
    """Leak test timer."""


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

    __room_temp = 0
    """Средна температура на стаята.
    (измерва се от датчиците)
    Limits: (0-40)"""

    __delta_temp = 0
    """Изменението на температурата от последните минути.
    Limits: (-3 : 3)"""

    __thermal_force = 0
    """Каква топлинна сила трябва да приложим към системата
    (-100% означава максимално да охлаждаме, +100% - максимално да отопляваме)"""

    __update_rate = 5
    """Update rate in seconds."""

    __test_rate = 120 # 3600
    """Test rate in seconds."""

    __fm_loop1 = 0
    """First measuremtn of loop 1 flow meter."""

    __fm_loop2 = 0
    """First measuremtn of loop 2 flow meter."""

    __sm_loop1 = 0
    """Second measuremtn of loop 1 flow meter."""

    __sm_loop2 = 0
    """Second measuremtn of loop 2 flow meter."""

#endregion

#region Properties

    @property
    def thermal_mode(self):
        """Thermal mode.

        Returns
        -------
        float
            Thermal mode.
        """

        return self.__thermal_mode.get_state()

    @thermal_mode.setter
    def thermal_mode(self, value):
        """This method is setting the HVAC system send by the central system.

        Parameters
        ----------
        value : ThermalMode
            Thermal mode
        """

        self.__thermal_mode.set_state(value)

    @property
    def adjust_temp(self):
        """Adjustment temperature.

        Returns
        -------
        float
            Adjust temperature.
        """

        return self.__adjust_temp

    @adjust_temp.setter
    def adjust_temp(self, value):
        """This method is setting the adjustment temperature from the user panel.

        Parameters
        ----------
        value : float
            Adjust temperature.
        """

        self.__adjust_temp = value

    @property
    def building_temp(self):
        """Building temperature.

        Returns
        -------
        float
            Building temperature.
        """

        return self.__goal_building_temp

    @building_temp.setter
    def building_temp(self, value):
        """This method is setting the building temperature send by the central system.

        Parameters
        ----------
        value : float
            Building temperature.
        """

        self.__goal_building_temp = value

    @property
    def thermal_force_limit(self):
        """Thermal force limit.

        Returns
        -------
        float
            Thermal force limit.
        """

        return self.__thermal_force_limit

    @thermal_force_limit.setter
    def thermal_force_limit(self, value):
        """This method is setting the thermal force limit.

        Parameters
        ----------
        value : float
            Thermal force limit.
        """

        self.__thermal_force_limit = value

    @property
    def delta_time(self):
        """Delta time.

        Returns
        -------
        float
            Delta time.
        """

        return self.__delta_time

    @delta_time.setter
    def delta_time(self, value):
        """This method is setting the delta time.

        Parameters
        ----------
        delta_time : float
            Delta time.
        """

        if value > 3:
            value = 3

        if value < 1:
            value = 1

        self.__delta_time = value

    @property
    def room_temperature(self):
        """Measure temperature from the sensors.

        Returns
        -------
        float
            Actual temperatre in the room.
        """

        # Create array.
        temperaures = []

        # Add temperatures.
        temperaures.append(self.__air_temp_upper_dev.value())
        temperaures.append(self.__air_temp_cent_dev.value())
        temperaures.append(self.__air_temp_lower_dev.value())        

        # Find min and max.
        minimum = min(temperaures)
        maximum = max(temperaures)
 
        # Take mediane.
        median = minimum + ((maximum - minimum) / 2)
 
        # Divide data by two arrays.
        upper_values = []
        lower_values = []
        for item in temperaures:
            if item >= median:
                upper_values.append(item)
            else:
                lower_values.append(item)        

        # Use the bigger one, to create average.
        value = 0
        if len(upper_values) >= len(lower_values):
            value = sum(upper_values) / len(upper_values)
        else:
            value = sum(lower_values) / len(lower_values)

        # # Troom = t1 * 20% + t2 * 60% + t3 * 20%
        # value = upper * 0.2 + cent * 0.6 + lower * 0.2

        # return the temperature.
        return value

#endregion

#region Private Methods

    def __op_mode_on_change(self, machine):
        self.__logger.info("Operation mode: {}".format(machine.get_state()))

        if machine.is_state(OperationMode.LeakTest):
            self._controller.set_led("LED1", 1)

        if machine.is_state(OperationMode.LeakInLoop1)\
             or machine.is_state(OperationMode.LeakInLoop2)\
             or machine.is_state(OperationMode.LeaInBothLoops):
            self._controller.set_led("LED2", 1)
            self._controller.set_led("LED1", 0)

        if machine.is_state(OperationMode.Operational):
            self._controller.set_led("LED1", 0)
            self._controller.set_led("LED2", 0)

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

        if self.__thermal_mode.is_state(ThermalMode.COLD_SESON):

            if thermal_force > 0:
                self.__loop1_valve_dev.set_state(0)
                self.__loop2_valve_dev.set_state(0)

            elif thermal_force <= 0:
                self.__loop1_valve_dev.set_state(100)
                self.__loop2_valve_dev.set_state(100)

        elif self.__thermal_mode.is_state(ThermalMode.TRANSISION_SEASON):

            if thermal_force < 0:
                self.__loop1_valve_dev.set_state(100)
                self.__loop2_valve_dev.set_state(0)

            elif thermal_force > 0:
                self.__loop1_valve_dev.set_state(0)
                self.__loop2_valve_dev.set_state(100)

            else:
                self.__loop1_valve_dev.set_state(0)
                self.__loop2_valve_dev.set_state(0)

        elif self.__thermal_mode.is_state(ThermalMode.WARM_SEASON):

            if thermal_force < 0:
                self.__loop1_valve_dev.set_state(100)
                self.__loop2_valve_dev.set_state(100)

            elif thermal_force > 0:
                self.__loop1_valve_dev.set_state(0)
                self.__loop2_valve_dev.set_state(0)

        # If thermal mode set properly apply thermal force
        if not self.__thermal_mode.is_state(ThermalMode.NONE):

            # Set upper fan.
            if thermal_force < 0:
                u_fan = l_scale(thermal_force, [0, 100], [0, 10])
                self.__loop1_fan_dev.set_state(abs(u_fan))
            else:
                self.__loop1_fan_dev.set_state(0)

            # Set lowe fan.
            if thermal_force > 0:
                l_fan = l_scale(thermal_force, [0, 100], [0, 10])
                self.__loop2_fan_dev.set_state(abs(l_fan))
            else:
                self.__loop2_fan_dev.set_state(0)

            # Set convector fan.
            conv_tf = l_scale(thermal_force, [0, 100], [0, 3])
            conv_tf = int(conv_tf)
            self.__convector_dev.set_state(abs(conv_tf))

        else:
            pass

    def __opmode_normal(self):

        # Main update rate at ~ 20 second.
        # На всеки 20 секунди се правят следните стъпки:
        self.__update_timer.update()
        if self.__update_timer.expired:
            self.__update_timer.clear()

            crg_temp = 0
            expected_room_temp = 0

            # Update current room temperature.
            self.__room_temp = self.room_temperature
            self.__logger.debug("ROOM: {:3.3f}".format(self.__room_temp))

            # 1. Изчислява се целевата температура на стаята:
            goal_room_temp = self.__goal_building_temp + self.__adjust_temp

            # 2. Изчислява се очакваната температура на стаята:
            expected_room_temp = self.__room_temp + self.__delta_temp
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

        # Recalculate delta time.
        # pass_time = time.time() - self.__lastupdate_delta_time
        # if pass_time > self.__delta_time:
        #     self.__delta_temp = self.__room_temp - self.__delta_temp
        #     self.__logger.debug("DT: {:3.3f}".format(self.__delta_temp))

        #     # Update current time.
        #     self.__lastupdate_delta_time = time.time()

    def __opmode_leak_test(self):

        # Take measurements of the flow meters.
        if self.__test_state.is_state(TestState.TekeFirstMeasurement):

            self.__fm_loop1 = self._controller\
                .read_counter(self._config["loop1_cnt_input"]) * self._config["loop1_cnt_tpl"]

            self.__fm_loop2 = self._controller\
                .read_counter(self._config["loop2_cnt_input"]) * self._config["loop2_cnt_tpl"]

            self.__test_state.set_state(TestState.TurnOffPeripheral)

        # Turn off the convector, fans and valves.
        if self.__test_state.is_state(TestState.TurnOffPeripheral):
            self.__thermal_force = 0
            self.__set_thermal_force(self.__thermal_force)
            self.__leak_test_timer.update_last_time()
            self.__test_state.set_state(TestState.WaitForLeak)

        # Wait 20 seconds.
        if self.__test_state.is_state(TestState.WaitForLeak):
            # Recalculate passed time.
            self.__leak_test_timer.update()
            if self.__leak_test_timer.expired:
                self.__leak_test_timer.clear()
                self.__test_state.set_state(TestState.TekeSecondMeasurement)

        # Take measurements of the flow meters.
        if self.__test_state.is_state(TestState.TekeSecondMeasurement):
            self.__sm_loop1 = self._controller\
                .read_counter(self._config["loop1_cnt_input"]) * self._config["loop1_cnt_tpl"]

            self.__sm_loop2 = self._controller\
                .read_counter(self._config["loop2_cnt_input"]) * self._config["loop2_cnt_tpl"]

            # Calculate the difference.
            leakage_loop1 = self.__sm_loop1 - self.__fm_loop1
            leakage_loop2 = self.__sm_loop2 - self.__fm_loop2

            # If there is something else then 0.
            # Then raice the alarm flag of the leak.
            if leakage_loop1 > 0 and leakage_loop2 > 0:
                self.__set_thermal_force(0)
                self.__operation_mode.set_state(OperationMode.LeaInBothLoops)

            if leakage_loop1 > 0:
                self.__set_thermal_force(0)
                self.__operation_mode.set_state(OperationMode.LeakInLoop1)

            if leakage_loop2 > 0:
                self.__set_thermal_force(0)
                self.__operation_mode.set_state(OperationMode.LeakInLoop2)


            # Else return to the normal operation mode.
            if leakage_loop1 == 0 and leakage_loop2 == 0:
                self.__operation_mode.set_state(OperationMode.Operational)

            self.__test_state.set_state(TestState.TekeFirstMeasurement)

#endregion

#region Public Methods

    def init(self):
        """Init the HVAC."""

        self.__logger = get_logger(__name__)

        self.__logger.info("Starting the {}".format(self.name))

        self.__test_state = StateMachine(TestState.TekeFirstMeasurement)
        self.__operation_mode = StateMachine(OperationMode.NONE)
        self.__operation_mode.on_change(self.__op_mode_on_change)
        self.__thermal_mode = StateMachine(ThermalMode.NONE)
        self.__thermal_mode.on_change(self.__thermal_mode_on_change)
        self.__update_timer = Timer(self.__update_rate)
        self.__test_time_timer = Timer(self.__test_rate)
        self.__leak_test_timer = Timer(20)

        # Region parameters
        if "update_rate" in self._config:
            self.__update_rate = self._config["update_rate"]

        if "delta_time" in self._config:
            self.delta_time = self._config["delta_time"]

        if "thermal_mode" in self._config:
            self.thermal_mode = ThermalMode(self._config["thermal_mode"])

        if "thermal_force_limit" in self._config:
            self.thermal_force_limit = self._config["thermal_force_limit"]

        if "adjust_temp" in self._config:
            self.adjust_temp = self._config["adjust_temp"]

        # Air thermometers
        if "air_temp_cent_enabled" in self._config:
            if self._config["air_temp_cent_enabled"] == 1:
                if self._config["air_temp_cent_type"] == "DS18B20":

                    config = \
                    {\
                        "name": "Air temperature central",
                        "dev": self._config["air_temp_cent_dev"],
                        "circuit": self._config["air_temp_cent_circuit"],
                        "controller": self._controller
                    }

                    self.__air_temp_cent_dev = DS18B20(config)
                    self.__air_temp_cent_dev.init()

        if "air_temp_lower_enabled" in self._config:
            if self._config["air_temp_lower_enabled"] == 1:
                if self._config["air_temp_lower_type"] == "DS18B20":

                    config = \
                    {\
                        "name": "Air temperature lower",
                        "dev": self._config["air_temp_lower_dev"],
                        "circuit": self._config["air_temp_lower_circuit"],
                        "controller": self._controller
                    }

                    self.__air_temp_lower_dev = DS18B20(config)
                    self.__air_temp_lower_dev.init()

        if "air_temp_upper_enabled" in self._config:
            if self._config["air_temp_upper_enabled"] == 1:
                if self._config["air_temp_upper_type"] == "DS18B20":

                    config = \
                    {\
                        "name": "Air temperature upper",
                        "dev": self._config["air_temp_upper_dev"],
                        "circuit": self._config["air_temp_upper_circuit"],
                        "controller": self._controller
                    }

                    self.__air_temp_upper_dev = DS18B20(config)
                    self.__air_temp_upper_dev.init()

        # Convector
        if "convector_enable" in self._config:
            if self._config["convector_enable"] == 1:
                if self._config["convector_vendor"] == "silpa":
                    if  self._config["convector_model"] == "klimafan":

                        config = \
                        {\
                            "name": "Convector 1",
                            "stage_1": self._config["convector_stage_1"],
                            "stage_2": self._config["convector_stage_2"],
                            "stage_3": self._config["convector_stage_3"],
                            "controller": self._controller\
                        }

                        self.__convector_dev = Klimafan(config)
                        self.__convector_dev.init()

        # Loop 1
        if "loop1_cnt_enabled" in self._config:
            if self._config["loop1_cnt_enabled"] == 1:
                self.__logger.debug("Enabled loop 1.")

        if "loop1_fan_enabled" in self._config:
            if self._config["loop1_fan_enabled"] == 1:
                if self._config["loop1_fan_vendor"] == "HangzhouAirflowElectricApplications":
                    if  self._config["loop1_fan_model"] == "f3p146ec072600":

                        config = \
                        {\
                            "name": "Upper FAN",
                            "output": self._config["loop1_fan_output"],
                            "controller": self._controller,
                            "speed_limit": 100\
                        }

                        self.__loop1_fan_dev = F3P146EC072600(config)
                        self.__loop1_fan_dev.init()

        if "loop1_temp_enabled" in self._config:
            if self._config["loop1_temp_enabled"] == 1:
                if self._config["loop1_temp_type"] == "DS18B20":

                    config = \
                    {\
                        "name": "Loop 1 temperature",
                        "dev": self._config["loop1_temp_dev"],
                        "circuit": self._config["loop1_temp_circuit"],
                        "controller": self._controller
                    }

                    self.__loop1_temp_dev = DS18B20(config)
                    self.__loop1_temp_dev.init()

        if "loop1_valve_enabled" in self._config:
            if self._config["loop1_valve_enabled"] == 1:
                if self._config["loop1_valve_vendor"] == "TONHE":
                    if  self._config["loop1_valve_model"] == "a20m15b2c":

                        config = \
                        {\
                            "name": "Upper Valve",
                            "output": self._config["loop1_valve_output"],
                            "controller": self._controller\
                        }

                        self.__loop1_valve_dev = A20M15B2C(config)
                        self.__loop1_valve_dev.init()

        # Loop 2
        if "loop2_cnt_enabled" in self._config:
            if self._config["loop1_cnt_enabled"] == 1:
                self.__logger.debug("Enabled loop 2.")

        if "loop2_fan_enabled" in self._config:
            if self._config["loop2_fan_enabled"] == 1:
                if self._config["loop2_fan_vendor"] == "HangzhouAirflowElectricApplications":
                    if  self._config["loop2_fan_model"] == "f3p146ec072600":

                        config = \
                        {\
                            "name": "Upper FAN",
                            "output": self._config["loop2_fan_output"],
                            "controller": self._controller,
                            "speed_limit": 100\
                        }

                        self.__loop2_fan_dev = F3P146EC072600(config)
                        self.__loop2_fan_dev.init()

        if "loop2_temp_enabled" in self._config:
            if self._config["loop2_temp_enabled"] == 1:
                if self._config["loop2_temp_type"] == "DS18B20":

                    config = \
                    {\
                        "name": "Loop 2 temperature",
                        "dev": self._config["loop2_temp_dev"],
                        "circuit": self._config["loop2_temp_circuit"],
                        "controller": self._controller
                    }

                    self.__loop2_temp_dev = DS18B20(config)
                    self.__loop2_temp_dev.init()

        if "loop2_valve_enabled" in self._config:
            if self._config["loop2_valve_enabled"] == 1:
                if self._config["loop2_valve_vendor"] == "TONHE":
                    if  self._config["loop2_valve_model"] == "a20m15b2c":
                        config = \
                        {\
                            "name": "Upper Valve",
                            "output": self._config["loop2_valve_output"],
                            "controller": self._controller\
                        }

                        self.__loop2_valve_dev = A20M15B2C(config)
                        self.__loop2_valve_dev.init()

        # Shutdown all the devices.
        self.__set_thermal_force(0)

        # Set the operation mode.
        self.__operation_mode.set_state(OperationMode.Operational)

    def update(self):
        """ Update cycle. """

        # Recalculate passed time.
        self.__test_time_timer.update()
        if self.__test_time_timer.expired:
            self.__test_time_timer.clear()
            self.__operation_mode.set_state(OperationMode.LeakTest)

        if self.__operation_mode.is_state(OperationMode.Operational):
            self.__opmode_normal()

        elif self.__operation_mode.is_state(OperationMode.LeakTest):
            self.__opmode_leak_test()

        elif self.__operation_mode.is_state(OperationMode.LeakInLoop1):
            pass

        elif self.__operation_mode.is_state(OperationMode.LeakInLoop2):
            pass

    def shutdown(self):
        """ Shutdown the HVAC. """

        self.__logger.info("Shutdown the {}".format(self.name))
        self.__set_thermal_force(0)

    def get_state(self):
        """Returns the state of the device.

        Returns
        -------
        mixed
            State of the device.
        """

        # state = { \
        #     "time": time.time(), \
        #     "parameters" :{ \
        #         "thermal_mode": self.thermal_mode.value, \
        #         "adjust_temp": self.adjust_temp, \
        #         "building_temp": self.building_temp, \
        #         "thermal_force_limit": self.thermal_force_limit, \
        #         "delta_time": self.delta_time, \
        #     } \
        # }

        return None

#endregion
