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

from enum import Enum

from utils.logger import get_logger
from utils.utils import l_scale

from plugins.base_plugin import BasePlugin

from devices.HangzhouAirflowElectricApplications.f3p146ec072600 import F3P146EC072600
from devices.TONHE.a20m15b2c import A20M15B2C
from devices.SILPA.klimafan import Klimafan

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
    COLD_SESON = 1
    TRANSISION_SEASON = 2
    WARM_SEASON = 3

class HVAC(BasePlugin):
    """Heating ventilation and air conditioning."""

#region Attributes

    __logger = None
    """Logger"""

    __upper_fan_dev = None
    """Upper fan device."""

    __lower_fan_dev = None
    """Lower fan device."""

    __upper_valve_dev = None
    """Upper valve device."""

    __lower_valve_dev = None
    """Lower valve device."""

    __convector_dev = None
    """Convector device."""

    __thermal_mode = 0
    """Thermal mode of the HVAC"""

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
    """Update rate."""

    __last_update_time = 0
    """Last update time."""

    __timestamp_delta_time = 0

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

        return self.__thermal_mode

    @thermal_mode.setter
    def thermal_mode(self, value):
        """This method is setting the HVAC system send by the central system.

        Parameters
        ----------
        value : ThermalMode
            Thermal mode
        """

        self.__thermal_mode = value

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

        value = self._controller.read_temperature(self._config["room_theromometer_dev"],\
             self._config["room_theromometer_circuit"])
        return value

#endregion

#region Private Methods

    def __apply_thermal_force(self, thermal_force):
        """ Apply thermal force to the devices. """

        # 7. Лимитираме Термалната сила в интервала -100 : + 100:
        if thermal_force < -100:
            thermal_force = -100
        if thermal_force > 100:
            thermal_force = 100

        self.__logger.debug("Mode: {}; TForce: {:3.3f}".format(self.__thermal_mode, thermal_force))

        if self.__thermal_mode == ThermalMode.COLD_SESON:

            if thermal_force > 0:
                self.__upper_valve_dev.set_state(0)
                self.__lower_valve_dev.set_state(0)

            elif thermal_force <= 0:
                self.__upper_valve_dev.set_state(100)
                self.__lower_valve_dev.set_state(100)

        elif self.__thermal_mode == ThermalMode.TRANSISION_SEASON:

            if thermal_force < 0:
                self.__upper_valve_dev.set_state(100)
                self.__lower_valve_dev.set_state(0)

            elif thermal_force > 0:
                self.__upper_valve_dev.set_state(0)
                self.__lower_valve_dev.set_state(100)

            else:
                self.__upper_valve_dev.set_state(0)
                self.__lower_valve_dev.set_state(0)

        elif self.__thermal_mode == ThermalMode.WARM_SEASON:

            if thermal_force < 0:
                self.__upper_valve_dev.set_state(100)
                self.__lower_valve_dev.set_state(100)

            elif thermal_force > 0:
                self.__upper_valve_dev.set_state(0)
                self.__lower_valve_dev.set_state(0)

        # If thermal mode set properly apply thermal force
        if self.__thermal_mode is not ThermalMode.NONE:

            # Set upper fan.
            if thermal_force < 0:
                u_fan = l_scale(thermal_force, [0, 100], [0, 10])
                self.__upper_fan_dev.set_state(abs(u_fan))
            else:
                self.__upper_fan_dev.set_state(0)

            # Set lowe fan.
            if thermal_force > 0:
                l_fan = l_scale(thermal_force, [0, 100], [0, 10])
                self.__lower_fan_dev.set_state(abs(l_fan))
            else:
                self.__lower_fan_dev.set_state(0)

            # Set convector fan.
            conv_tf = l_scale(thermal_force, [0, 100], [0, 3])
            conv_tf = int(conv_tf)
            self.__convector_dev.set_state(abs(conv_tf))

        else:
            pass

#endregion

#region Public Methods

    def init(self):
        """Init the HVAC."""

        self.__logger = get_logger(__name__)

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

        if "room_theromometer_enable" in self._config:
            room_theromometer_enable = self._config["room_theromometer_enable"]

        if "upper_fan_enable" in self._config:
            upper_fan_enable = self._config["upper_fan_enable"]
            if upper_fan_enable:
                if self._config["upper_fan_vendor"] == "HangzhouAirflowElectricApplications":
                    if  self._config["upper_fan_model"] == "f3p146ec072600":
                        config = \
                        {\
                            "name": "Upper FAN",\
                            "output": self._config["upper_fan_output"],\
                            "controller": self._controller,\
                            "speed_limit": 100\
                        }

                        self.__upper_fan_dev = F3P146EC072600(config)
                        self.__upper_fan_dev.init()

        if "lower_fan_enable" in self._config:
            lower_fan_enable = self._config["lower_fan_enable"]
            if lower_fan_enable:
                if self._config["lower_fan_vendor"] == "HangzhouAirflowElectricApplications":
                    if  self._config["lower_fan_model"] == "f3p146ec072600":
                        config = \
                        {\
                            "name": "Lower FAN",\
                            "output": self._config["upper_fan_output"],\
                            "controller": self._controller,\
                            "speed_limit": 100\
                        }

                        self.__lower_fan_dev = F3P146EC072600(config)
                        self.__lower_fan_dev.init()

        if "upper_valve_enable" in self._config:
            upper_valve_enable = self._config["upper_valve_enable"]
            if upper_valve_enable:
                if self._config["upper_valve_vendor"] == "TONHE":
                    if  self._config["upper_valve_model"] == "a20m15b2c":
                        config = \
                        {\
                            "name": "Upper Valve",\
                            "output": self._config["upper_valve_output"],\
                            "controller": self._controller\
                        }

                        self.__upper_valve_dev = A20M15B2C(config)
                        self.__upper_valve_dev.init()

        if "lower_valve_enable" in self._config:
            lower_valve_enable = self._config["lower_valve_enable"]
            if lower_valve_enable:
                if self._config["lower_valve_vendor"] == "TONHE":
                    if  self._config["lower_valve_model"] == "a20m15b2c":
                        config = \
                        {\
                            "name": "Lower Valve",\
                            "output": self._config["lower_valve_output"],\
                            "controller": self._controller\
                        }

                        self.__lower_valve_dev = A20M15B2C(config)
                        self.__lower_valve_dev.init()

        if "convector_enable" in self._config:
            convector_enable = self._config["convector_enable"]
            if convector_enable:
                if self._config["convector_vendor"] == "silpa":
                    if  self._config["convector_model"] == "klimafan":
                        config = \
                        {\
                            "name": "Convector 1",\
                            "stage_1": self._config["convector_stage_1"],\
                            "stage_2": self._config["convector_stage_2"],\
                            "stage_3": self._config["convector_stage_3"],\
                            "controller": self._controller\
                        }

                        self.__convector_dev = Klimafan(config)
                        self.__convector_dev.init()

        self.__apply_thermal_force(0)
        self.__logger.info("Starting the {}".format(self.name))

        # TODO: Remove after test.
        self.__logger.warning("Setting the {} to transision season and 26 deg of temperature of the source."\
            .format(self.name))
        self.thermal_mode = ThermalMode.TRANSISION_SEASON
        self.building_temp = 26

    def update(self):
        """ Update cycle. """

        # Main update rate at ~ 20 second.
        # На всеки 20 секунди се правят следните стъпки:
        diff = time.time() - self.__last_update_time
        if diff > self.__update_rate:

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

            self.__apply_thermal_force(self.__thermal_force)

            # Update current time.
            self.__last_update_time = time.time()

        # Recalculate delta time.
        diff = time.time() - self.__timestamp_delta_time
        if diff > self.__delta_time:
            #self.__delta_temp = self.__room_temp - self.__delta_temp
            #self.__logger.debug("DT: {:3.3f}".format(self.__delta_temp))

            # Update current time.
            self.__timestamp_delta_time = time.time()

    def shutdown(self):
        """ Shutdown the HVAC. """

        self.__logger.info("Shutdown the {}".format(self.name))
        self.__apply_thermal_force(0)

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

    def set_state(self, state):

        parameters = state["parameters"]

        if "thermal_mode" in parameters:
            self.thermal_mode = ThermalMode(parameters["thermal_mode"])

        if "adjust_temp" in parameters:
            self.adjust_temp = parameters["adjust_temp"]

        if "building_temp" in parameters:
            self.building_temp = parameters["building_temp"]

        if "thermal_force_limit" in parameters:
            self.thermal_force_limit = parameters["thermal_force_limit"]

        if "delta_time" in parameters:
            self.delta_time = parameters["delta_time"]

#endregion
