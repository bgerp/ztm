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
from devices.no_vendor.flowmeter import Flowmeter
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

    __temp_actual = None

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
        if self.__air_temp_upper_dev is not None:
            temperaures.append(self.__air_temp_upper_dev.value())

        if self.__air_temp_cent_dev is not None:
            temperaures.append(self.__air_temp_cent_dev.value())

        if self.__air_temp_lower_dev is not None:
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

        elif len(upper_values) <= len(lower_values):
            value = sum(lower_values) / len(lower_values)

        # # Troom = t1 * 20% + t2 * 60% + t3 * 20%
        # value = upper * 0.2 + cent * 0.6 + lower * 0.2

        # return the temperature.
        return value

#endregion

#region Private Methods

    def __update_rate_cb(self, register):
        self.__update_rate = register.value

    def __delta_time_cb(self, register):
        self.__delta_time = register.value

    def __thermal_mode_cb(self, register):
        self.__thermal_mode.set_state(register.value)

    def __thermal_force_limit_cb(self, register):
        self.__thermal_force_limit = register.value

    def __update_handler_cb(self, register):
        self.__adjust_temp = register.value

    def __temp_actual_cb(self, register):

        min_temp = 2.5
        max_temp = -2.5

        key = "hvac.temp.min"
        if self._registers.exists(key):
            min_temp = self._registers.by_name(key).value

        key = "hvac.temp.max"
        if self._registers.exists(key):
            max_temp = self._registers.by_name(key).value

        actual_temp = register.value

        if actual_temp < min_temp:
            actual_temp = min_temp

        if actual_temp > max_temp:
            actual_temp = max_temp

        self.__temp_actual = actual_temp

    def __goal_building_temp_cb(self, register):

        # @see https://experta.bg/L/S/122745/m/Fwntindd
        min_temp = 18
        max_temp = 26

        actual_temp = register.value

        if actual_temp < min_temp:
            actual_temp = min_temp

        if actual_temp > max_temp:
            actual_temp = max_temp

        self.__goal_building_temp = actual_temp

    def __ventilation_max_cb(self, register):

        if self.__loop1_fan_dev is not None:
            self.__loop1_fan_dev.max_speed = register.value

        if self.__loop2_fan_dev is not None:
            self.__loop2_fan_dev.max_speed = register.value

    def __cirulation_max_cb(self, register):

        if self.__loop1_valve_dev is not None:
            self.__loop1_valve_dev.max_pos = register.value

        if self.__loop2_valve_dev is not None:
            self.__loop2_valve_dev.max_pos = register.value

    def __air_temp_cent_enabled_cb(self, register):

        if register.value == 1:
            air_temp_cent_circuit = self._registers.by_name(self._key + ".air_temp_cent.circuit")
            air_temp_cent_dev = self._registers.by_name(self._key + ".air_temp_cent.dev")
            air_temp_cent_type = self._registers.by_name(self._key + ".air_temp_cent.type")

            if air_temp_cent_circuit is not None and\
                air_temp_cent_dev is not None and\
                air_temp_cent_type is not None:

                config = \
                {\
                    "name": "Air temperature central",
                    "dev": air_temp_cent_dev.value,
                    "circuit": air_temp_cent_circuit.value,
                    "typ": air_temp_cent_type.value,
                    "controller": self._controller
                }

                self.__air_temp_cent_dev = DS18B20(config)
                self.__air_temp_cent_dev.init()

        elif register.value == 0:
            self.__air_temp_cent_dev.shutdown()
            del self.__air_temp_cent_dev

    def __air_temp_lower_enabled_cb(self, register):

        if register.value == 1:
            air_temp_lower_circuit = self._registers.by_name(self._key + ".air_temp_lower.circuit")
            air_temp_lower_dev = self._registers.by_name(self._key + ".air_temp_lower.dev")
            air_temp_lower_type = self._registers.by_name(self._key + ".air_temp_lower.type")

            if air_temp_lower_circuit is not None and\
                air_temp_lower_dev is not None and\
                air_temp_lower_type is not None:

                config = \
                {\
                    "name": "Air temperature lower",
                    "dev": air_temp_lower_dev.value,
                    "circuit": air_temp_lower_circuit.value,
                    "typ": air_temp_lower_type.value,
                    "controller": self._controller
                }

                self.__air_temp_lower_dev = DS18B20(config)
                self.__air_temp_lower_dev.init()

        elif register.value == 0:
            self.__air_temp_lower_dev.shutdown()
            del self.__air_temp_lower_dev

    def __air_temp_upper_enabled_cb(self, register):

        if register.value == 1:
            air_temp_upper_circuit = self._registers.by_name(self._key + ".air_temp_upper.circuit")
            air_temp_upper_dev = self._registers.by_name(self._key + ".air_temp_upper.dev")
            air_temp_upper_type = self._registers.by_name(self._key + ".air_temp_upper.type")

            if air_temp_upper_circuit is not None and\
                air_temp_upper_dev is not None and\
                air_temp_upper_type is not None:

                config = \
                {\
                    "name": "Air temperature upper",
                    "dev": air_temp_upper_dev.value,
                    "circuit": air_temp_upper_circuit.value,
                    "typ": air_temp_upper_type.value,
                    "controller": self._controller
                }

                self.__air_temp_upper_dev = DS18B20(config)
                self.__air_temp_upper_dev.init()

        elif register.value == 0:
            self.__air_temp_upper_dev.shutdown()
            del self.__air_temp_upper_dev

    def __convector_enable_cb(self, register):

        if register.value == 1:
            convector_stage_1 = self._registers.by_name(self._key + ".convector.stage_1.output")
            convector_stage_2 = self._registers.by_name(self._key + ".convector.stage_2.output")
            convector_stage_3 = self._registers.by_name(self._key + ".convector.stage_3.output")

            if convector_stage_1 is not None and\
                convector_stage_2 is not None and\
                convector_stage_3 is not None:

                config = \
                {\
                    "name": "Convector 1",\
                    "stage_1": convector_stage_1.value,\
                    "stage_2": convector_stage_2.value,\
                    "stage_3": convector_stage_3.value,\
                    "controller": self._controller\
                }

                self.__convector_dev = Klimafan(config)
                self.__convector_dev.init()

        elif register.value == 0:
            if self.__convector_dev is not None:
                self.__convector_dev.shutdown()
                del self.__convector_dev

    def __loop1_cnt_enabled_cb(self, register):

        if register.value == 1:
            loop1_cnt_input = self._registers.by_name(self._key + ".loop1.cnt.input")
            loop1_cnt_tpl = self._registers.by_name(self._key + ".loop1.cnt.tpl")

            if loop1_cnt_input is not None and\
                loop1_cnt_tpl is not None:

                config = \
                {\
                    "name": "Convector 1",
                    "input": loop1_cnt_input.value,
                    "tpl": loop1_cnt_tpl.value,
                    "controller": self._controller
                }

                self.__loop1_cnt_dev = Flowmeter(config)
                self.__loop1_cnt_dev.init()

        elif register.value == 0:
            if self.__loop1_cnt_dev is not None:
                self.__loop1_cnt_dev.shutdown()
                del self.__loop1_cnt_dev

    def __loop1_fan_enabled_cb(self, register):

        if register.value == 1:

            loop1_fan_output = self._registers.by_name(self._key + ".loop1.fan.output").value

            config = \
            {\
                "name": "Upper FAN",
                "output": loop1_fan_output,
                "controller": self._controller
            }

            self.__loop1_fan_dev = F3P146EC072600(config)
            self.__loop1_fan_dev.init()

        elif register.value == 0:
            if self.__loop1_fan_dev is not None:
                self.__loop1_fan_dev.shutdown()
                del self.__loop1_fan_dev

    def __loop1_temp_enabled_cb(self, register):

        if register.value == 1:
            loop1_temp_circuit = self._registers.by_name(self._key + ".loop1.temp.circuit")
            loop1_temp_dev = self._registers.by_name(self._key + ".loop1.temp.dev")
            loop1_temp_type = self._registers.by_name(self._key + ".loop1.tempr.type")

            if loop1_temp_circuit is not None and\
                loop1_temp_dev is not None and\
                loop1_temp_type is not None:

                config = \
                {\
                    "name": "Loop 1 temperature",
                    "dev": loop1_temp_dev,
                    "circuit": loop1_temp_circuit,
                    "typ": loop1_temp_type,
                    "controller": self._controller
                }

                self.__loop1_temp_dev = DS18B20(config)
                self.__loop1_temp_dev.init()

        elif register.value == 0:
            if self.__loop1_temp_dev is not None:
                self.__loop1_temp_dev.shutdown()
                del self.__loop1_temp_dev

    def __loop1_valve_enabled_cb(self, register):

        if register.value == 1:

            loop1_valve_output = self._registers.by_name(self._key + ".loop1.valve.output").value

            config = \
            {\
                "name": "Upper Valve",
                "output": loop1_valve_output,
                "controller": self._controller
            }

            self.__loop1_valve_dev = A20M15B2C(config)
            self.__loop1_valve_dev.init()

        if register.value == 0:
            if self.__loop1_valve_dev is not None:
                self.__loop1_valve_dev.shutdown()
                del self.__loop1_valve_dev

    def __loop2_cnt_enabled_cb(self, register):

        if register.value == 1:
            loop2_cnt_input = self._registers.by_name(self._key + ".loop2.cnt.input")
            loop2_cnt_tpl = self._registers.by_name(self._key + ".loop2.cnt.tpl")

            if loop2_cnt_input is not None and\
                loop2_cnt_tpl is not None:

                config = \
                {\
                    "name": "Convector 1",
                    "input": loop2_cnt_input.value,
                    "tpl": loop2_cnt_tpl.value,
                    "controller": self._controller
                }

                self.__loop2_cnt_dev = Flowmeter(config)
                self.__loop2_cnt_dev.init()

        elif register.value == 0:
            if self.__loop2_cnt_dev is not None:
                self.__loop2_cnt_dev.shutdown()
                del self.__loop2_cnt_dev

    def __loop2_fan_enabled_cb(self, register):

        if register.value == 1:
            loop2_fan_output = self._registers.by_name(self._key + ".loop2.fan.output")

            config = \
            {\
                "name": "Upper FAN",
                "output": loop2_fan_output.value,
                "controller": self._controller,
            }

            self.__loop2_fan_dev = F3P146EC072600(config)
            self.__loop2_fan_dev.init()

        elif register.value == 0:
            if self.__loop2_fan_dev is not None:
                self.__loop2_fan_dev.shutdown()
                del self.__loop2_fan_dev

    def __loop2_temp_enabled_cb(self, register):

        if register.value == 1:
            loop2_temp_circuit = self._registers.by_name(self._key + ".loop2.temp.circuit")
            loop2_temp_dev = self._registers.by_name(self._key + ".loop2.temp.dev")
            loop2_temp_type = self._registers.by_name(self._key + ".loop2.temp.type")

            if loop2_temp_circuit is not None and\
                loop2_temp_dev is not None and\
                loop2_temp_type is not None:

                config = \
                {\
                    "name": "Loop 2 temperature",
                    "dev": loop2_temp_dev,
                    "circuit": loop2_temp_circuit,
                    "typ": loop2_temp_type,
                    "controller": self._controller
                }

                self.__loop2_temp_dev = DS18B20(config)
                self.__loop2_temp_dev.init()

        elif register.value == 0:
            if self.__loop2_temp_dev is not None:
                self.__loop2_temp_dev.shutdown()
                del self.__loop2_temp_dev

    def __loop2_valve_enabled_cb(self, register):

        if register.value == 1:
            loop2_valve_output = self._registers.by_name(self._key + ".loop2.valve.output").value

            config = \
            {\
                "name": "Upper Valve",
                "output": loop2_valve_output,
                "controller": self._controller
            }

            self.__loop2_valve_dev = A20M15B2C(config)
            self.__loop2_valve_dev.init()

        elif register.value == 0:
            if self.__loop2_valve_dev is not None:
                self.__loop2_valve_dev.shutdown()
                del self.__loop2_valve_dev

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
                u_fan = l_scale(thermal_force, [0, 100], [0, 10])
                self.__loop1_fan_dev.set_speed(abs(u_fan))
            else:
                self.__loop1_fan_dev.set_speed(0)

            # Set lowe fan.
            if thermal_force > 0:
                l_fan = l_scale(thermal_force, [0, 100], [0, 10])
                self.__loop2_fan_dev.set_speed(abs(l_fan))
            else:
                self.__loop2_fan_dev.set_speed(0)

            # Set convector fan.
            conv_tf = l_scale(thermal_force, [0, 100], [0, 3])
            conv_tf = int(conv_tf)
            self.__convector_dev.set_state(abs(conv_tf))

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
            adjust_temp.update_handler = self.__update_handler_cb

        goal_building_temp = self._registers.by_name(self._key + ".goal_building_temp")
        if goal_building_temp is not None:
            goal_building_temp.update_handler = self.__goal_building_temp_cb

        # temp_actual = self._registers.by_name(self._key + ".temp.actual")
        # if temp_actual is not None:
        #     temp_actual.update_handler = self.__temp_actual_cb

        # temp_max = self._registers.by_name(self._key + ".temp.max")
        # if temp_max is not None:
        #     temp_max.update_handler = self.__temp_max_cb

        # temp_min = self._registers.by_name(self._key + ".temp.min")
        # if temp_min is not None:
        #     temp_min.update_handler = self.__temp_min_cb

        # ventilation_min = self._registers.by_name(self._key + ".ventilation.min")
        # if ventilation_min is not None:
        #     ventilation_min.update_handler = self.__ventilation_min_cb

        ventilation_max = self._registers.by_name(self._key + ".ventilation.max")
        if ventilation_max is not None:
            ventilation_max.update_handler = self.__ventilation_max_cb

        # cirulation_actual = self._registers.by_name(self._key + ".cirulation.actual")
        # if cirulation_actual is not None:
        #     cirulation_actual.update_handler = self.__cirulation_actual_cb

        cirulation_max = self._registers.by_name(self._key + ".cirulation.max")
        if cirulation_max is not None:
            cirulation_max.update_handler = self.__cirulation_max_cb

        # cirulation_min = self._registers.by_name(self._key + ".cirulation.min")
        # if cirulation_min is not None:
        #     cirulation_min.update_handler = self.__cirulation_min_cb

        # Air temperatures.
        air_temp_cent_enabled = self._registers.by_name(self._key + ".air_temp_cent.enabled")
        if air_temp_cent_enabled is not None:
            air_temp_cent_enabled.update_handler = self.__air_temp_cent_enabled_cb

        air_temp_lower_enabled = self._registers.by_name(self._key + ".air_temp_lower.enabled")
        if air_temp_lower_enabled is not None:
            air_temp_lower_enabled.update_handler = self.__air_temp_lower_enabled_cb

        air_temp_upper_enabled = self._registers.by_name(self._key + ".air_temp_upper.enabled")
        if air_temp_upper_enabled is not None:
            air_temp_upper_enabled.update_handler = self.__air_temp_upper_enabled_cb

        # Convector
        convector_enable = self._registers.by_name(self._key + ".convector.enabled")
        if convector_enable is not None:
            convector_enable.update_handler = self.__convector_enable_cb

        # Loop 1
        loop1_cnt_enabled = self._registers.by_name(self._key + ".loop1.cnt.enabled")
        if loop1_cnt_enabled is not None:
            loop1_cnt_enabled.update_handler = self.__loop1_cnt_enabled_cb

        loop1_fan_enabled = self._registers.by_name(self._key + ".loop1.fan.enabled")
        if loop1_fan_enabled is not None:
            loop1_fan_enabled.update_handler = self.__loop1_fan_enabled_cb

        loop1_temp_enabled = self._registers.by_name(self._key + ".loop1.temp.enabled")
        if loop1_temp_enabled is not None:
            loop1_temp_enabled.update_handler = self.__loop1_temp_enabled_cb

        loop1_valve_enabled = self._registers.by_name(self._key + ".loop1.valve.enabled")
        if loop1_valve_enabled is not None:
            loop1_valve_enabled.update_handler = self.__loop1_valve_enabled_cb

        # Loop 2
        loop2_cnt_enabled = self._registers.by_name(self._key + ".loop2.cnt.enabled")
        if loop2_cnt_enabled is not None:
            loop2_cnt_enabled.update_handler = self.__loop2_cnt_enabled_cb

        loop2_fan_enabled = self._registers.by_name(self._key + ".loop2.fan.enabled")
        if loop2_fan_enabled is not None:
            loop2_fan_enabled.update_handler = self.__loop2_fan_enabled_cb

        loop2_temp_enabled = self._registers.by_name(self._key + ".loop2.temp.enabled")
        if loop2_temp_enabled is not None:
            loop2_temp_enabled.update_handler = self.__loop2_temp_enabled_cb

        loop2_valve_enabled = self._registers.by_name(self._key + ".loop2.valve.enabled")
        if loop2_valve_enabled is not None:
            loop2_valve_enabled.update_handler = self.__loop2_valve_enabled_cb

        # Shutdown all the devices.
        self.__set_thermal_force(0)

        # Set the operation mode.
        self.__operation_mode.set_state(OperationMode.Operational)

    def update(self):
        """ Update cycle. """

        # Recalculate passed time.
        # self.__test_time_timer.update()
        # if self.__test_time_timer.expired:
        #     self.__test_time_timer.clear()
        #     self.__operation_mode.set_state(OperationMode.LeakTest)

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

#endregion
