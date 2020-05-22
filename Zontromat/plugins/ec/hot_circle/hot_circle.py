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

from utils.logger import get_logger
from utils.timer import Timer
from utils.pid import PID
from utils.temp_processor import TemperatureProcessor

from plugins.base_plugin import BasePlugin

from devices.Dallas.ds18b20 import DS18B20
from devices.Boiler.boiler import Boiler

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

class HotCircle(BasePlugin):
    """Hot circle control loop. (for BT2)"""

#region Attributes

    __logger = None
    """Logger"""

    __update_timer = None
    """Main process update timer."""

    __update_rate = 5
    """Update rate in seconds."""

    __goal_temp = 20
    """Goal temperature."""

    __temp_proc = None
    """Temperature processor."""

    __tank_temp_dev = None
    """Air thermometer central."""

    __boiler_dev = None
    """Electric Boiler 1 - EB1"""

    __pid_controller = None
    """PID Controller."""

#endregion

#region Destructor

    def __del__(self):
        """Destructor"""

        del self.__tank_temp_dev
        del self.__logger

#endregion

#region Properties

    @property
    def temp(self):
        """Measure temperature from the sensors.

            Средна температура на стаята.
            (измерва се от датчиците)
            Limits: (0-40)

        Returns
        -------
        float
            Actual temperatre in the room.
        """

        # Return the temperature.
        return self.__temp_proc.value

#endregion

#region Private Methods

    def __update_rate_cb(self, register):

        self.__update_rate = register.value

    def __tank_temp_enabled_cb(self, register):

        if register.value == 1 and self.__tank_temp_dev is None:
            self.__tank_temp_dev = DS18B20.create(\
                "Tank temperature",\
                self._key + ".tank_temp",\
                self._registers,\
                self._controller)

            if self.__tank_temp_dev is not None:
                self.__tank_temp_dev.init()
                self.__temp_proc.add(self.__tank_temp_dev)

        elif register.value == 0 and self.__tank_temp_dev is not None:
            self.__temp_proc.remove(self.__tank_temp_dev)
            self.__tank_temp_dev.shutdown()
            del self.__tank_temp_dev

    def __boiler_dev_enabled_cb(self, register):

        if register.value == 1 and self.__boiler_dev is None:
            self.__boiler_dev = Boiler.create(\
                "EB1",\
                self._key + ".electric_boiler",\
                self._registers,
                self._controller)

            if self.__boiler_dev is not None:
                self.__boiler_dev.init()

        elif register.value == 0 and self.__boiler_dev is not None:
            self.__boiler_dev.shutdown()
            del self.__boiler_dev

    def __goal_temp_cb(self, register):

        self.__goal_temp = register.value

#endregion

#region Public Methods

    def init(self):
        """Init the Hot circle."""

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {} with name {}".format(__name__, self.name))

        self.__update_timer = Timer(self.__update_rate)

        self.__temp_proc = TemperatureProcessor()

        # Region parameters
        update_rate = self._registers.by_name(self._key + ".update_rate")
        if update_rate is not None:
            update_rate.update_handler = self.__update_rate_cb

        # Tank temperatures enable.
        tank_temp_enabled = self._registers.by_name(self._key + ".tank_temp.enabled")
        if tank_temp_enabled is not None:
            tank_temp_enabled.update_handler = self.__tank_temp_enabled_cb

        # Goal temperature callback.
        goal_temp = self._registers.by_name(self._key + ".goal_temp")
        if goal_temp is not None:
            goal_temp.update_handler = self.__goal_temp_cb

        P = 1.0
        I = 0.0
        D = 0.0
        self.__pid_controller = PID(P, I, D)
        self.__pid_controller.SetPoint = 0.0
        self.__pid_controller.setSampleTime(0.01)

    def update(self):
        """ Update cycle. """

        # Main update rate at ~ 20 second.
        self.__update_timer.update()
        if self.__update_timer.expired:
            self.__update_timer.clear()

            # update temperatures.
            self.__temp_proc.update()

            # Set the goal.
            self.__pid_controller.SetPoint = self.__goal_temp

            # Get temperature.
            tank_temp = self.__temp_proc.value

            # Recalculate
            self.__pid_controller.update(tank_temp)

            # Get the output.
            output = self.__pid_controller.output

            print("UPDATE: I:{:.2f} O:{:.2f}".format(tank_temp, output))

    def shutdown(self):
        """ Shutting down the HVAC. """

        self.__logger.info("Shutting down the {} with name {}".format(__name__, self.name))

#endregion
