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

from plugins.base_plugin import BasePlugin

from devices.SEDtronic.u1wtvs import U1WTVS

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

class Lighting(BasePlugin):
    """Lamp controller"""

#region Attributes

    __logger = None
    """Logger"""

    __v1_output = "AO0"
    """Analog voltage output 0"""

    __v2_output = "AO1"
    """Analog voltage output 1"""

    __v1_value = 0
    """V1 value."""

    __v2_value = 0
    """V2 value."""

    __light_sensor = None
    """Light sensor."""

    __animation_bit = True
    """Animation purpose only."""

    __animation_step = 0.01
    """Animation purpose only."""

    __animation_max = 5
    """Animation purpose only."""

    __animation_min = 0
    """Animation purpose only."""

#endregion

#region Properties

    @property
    def v1(self):
        """Voltage 1.

        Returns
        -------
        float
            Voltage 1.
        """

        return self.__v1_value

    @v1.setter
    def v1(self, value):
        """Voltage 1.

        Parameters
        ----------
        value : float
            Voltage 1
        """

        if value > 10:
            value = 10

        if value < 0:
            value = 0

        self.__v1_value = value

    @property
    def v2(self):
        """Voltage 2.

        Returns
        -------
        float
            Voltage 2.
        """

        return self.__v2_value

    @v2.setter
    def v2(self, value):
        """Voltage 2.

        Parameters
        ----------
        value : float
            Voltage 2
        """

        if value > 10:
            value = 10

        if value < 0:
            value = 0

        self.__v2_value = value

#endregion

#region Private Methods

    def __set_voltages(self, v1, v2):
        """Set the voltage outputs.

        Parameters
        ----------
        v1 : float
            Voltage 1.
        v2 : float
            Voltage 2.
        """

        self._controller.analog_write(self.__v1_output, v1)
        self._controller.analog_write(self.__v2_output, v2)

    def __sensor_enabled_cb(self, register):

        if register.value == 1 and self.__light_sensor is None:
            sensor_dev = self._config["registers"].by_name(self._key + ".sensor.dev").value
            sensor_circuit = self._config["registers"].by_name(self._key + ".sensor.circuit").value

            config = \
            {\
                "name": "Room light sensor.",
                "dev": sensor_dev,
                "circuit": sensor_circuit,
                "controller": self._controller
            }

            self.__light_sensor = U1WTVS(config)
            self.__light_sensor.init()

        elif register.value == 0 and self.__light_sensor is not None:
            self.__light_sensor.shutdown()
            del self.__light_sensor

    def __v1_output_cb(self, register):
        if self.__v1_output != register.value:
            self.__v1_output = register.value

    def __v2_output_cb(self, register):
        if self.__v2_output != register.value:
            self.__v2_output = register.value

#endregion

#region Public Methods

    def init(self):
        """Init the Lighting."""

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {} with name {}".format(__name__, self.name))

        self.__set_voltages(0, 0)

        sensor_enabled = self._config["registers"].by_name(self._key + ".sensor.enabled")
        if sensor_enabled is not None:
            sensor_enabled.update_handler = self.__sensor_enabled_cb
            sensor_enabled.value = 1

        v1_output = self._config["registers"].by_name(self._key + ".v1.output")
        if v1_output is not None:
            v1_output.update_handler = self.__v1_output_cb

        v2_output = self._config["registers"].by_name(self._key + ".v2.output")
        if v2_output is not None:
            v2_output.update_handler = self.__v2_output_cb

        self.v1 = 1.0 #TODO: Only test purpose.

    def update(self):
        """Update the lights state."""

        # Update sensor data.
        self.__light_sensor.update()

        #self.__animation_max = self.__light_sensor.get_value() / 10

        # TODO: After repairing sensor create negative proportional feedback controll.
        if self.__animation_bit:
            self.v1 += self.__animation_step
            if self.v1 >= self.__animation_max:
                self.__animation_bit = False

        if not self.__animation_bit:
            self.v1 -= self.__animation_step
            if self.v1 <= self.__animation_min:
                self.__animation_bit = True

        # This is for test purpose of lamp lightsup ramp.
        if self.v1 >= 1.18:
            self.__animation_step = 0.0
        # print("Analog output 1: {:03}".format(self.v1))

        self.__set_voltages(self.v1, self.v2)

    def shutdown(self):
        """Shutting down the lights."""

        self.__logger.info("Shutting down the {} with name {}".format(__name__, self.name))
        self.__set_voltages(0, 0)

    def get_state(self):
        return self.__light_sensor.get_value()

#endregion
