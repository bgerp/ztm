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
from utils.logic.timer import Timer

from plugins.base_plugin import BasePlugin

from devices.factories.light_sensor.light_sensor_factory import LightSensorFactory

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

__class_name__ = "Light"
"""Plugin class name."""

#endregion

class Light(BasePlugin):
    """Light controller plugin."""

#region Attributes

    __logger = None
    """Logger
    """

    __update_timer = None
    """Update timer.
    """

    __light_sensor = None
    """Light sensor.
    """

    __v1_output = verbal_const.OFF
    """Analog voltage output 1.
    """

    __v2_output = verbal_const.OFF
    """Analog voltage output 2.
    """

    __last_target_illum = 0
    """Last target illumination.
    """

    __target_illumination = 700
    """Target illumination. [Lux]
    """    

    __error_gain = 0.01
    """Gain of the error. This parameter is the smoothness of the curve.
    """

    __output_limit = 10000 
    """Illumination force limit. [V]
    """   

    __tmp_output = 0
    """Temporary output. [V]
    """

    __output = 0
    """Main output. [V]
    """

#endregion

#region Private Methods Registers Interface

    def __error_gain_cb(self, register):
        
        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__error_gain != register.value:
            self.__error_gain = register.value  

    def __target_illum_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__target_illumination != register.value:
            self.__target_illumination = register.value

    def __sensor_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__light_sensor is None:

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__light_sensor = LightSensorFactory.create(
                controller=self._controller,
                name="Room light sensor.",
                params=params)

            if self.__light_sensor is not None:
                self.__light_sensor.init()

        elif register.value == verbal_const.OFF and self.__light_sensor is not None:
            self.__light_sensor.shutdown()
            del self.__light_sensor

    def __v1_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__v1_output = register.value

    def __v2_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__v2_output = register.value

    def __init_registers(self):

        sensor_enabled = self._registers.by_name(self.key + ".sensor.settings")
        if sensor_enabled is not None:
            sensor_enabled.update_handlers = self.__sensor_settings_cb
            sensor_enabled.update()

        v1_output = self._registers.by_name(self.key + ".v1.output")
        if v1_output is not None:
            v1_output.update_handlers = self.__v1_output_cb
            v1_output.update()

        v2_output = self._registers.by_name(self.key + ".v2.output")
        if v2_output is not None:
            v2_output.update_handlers = self.__v2_output_cb
            v2_output.update()

        target_illum = self._registers.by_name(self.key + ".target_illum")
        if target_illum is not None:
            target_illum.update_handlers = self.__target_illum_cb
            target_illum.update()

        error_gain = self._registers.by_name(self.key + ".error_gain")
        if error_gain is not None:
            error_gain.update_handler = self.__error_gain_cb
            error_gain.update()

    def __is_empty(self):

        value = False

        is_empty = self._registers.by_name("envm.is_empty")
        if is_empty is not None:
            value = is_empty.value

        return value

#endregion

#region Private Methods Controller Interface

    def __set_voltages(self, v1, v2):
        """Set the voltage outputs.

        Parameters
        ----------
        v1 : float
            Voltage 1.
        v2 : float
            Voltage 2.
        """

        value_v1 = v1

        if value_v1 > 10:
            value_v1 = 10

        if value_v1 < 0:
            value_v1 = 0

        value_v2 = v2

        if value_v2 > 10:
            value_v2 = 10

        if value_v2 < 0:
            value_v2 = 0


        if self._controller.is_valid_gpio(self.__v1_output):
            self._controller.analog_write(self.__v1_output, value_v1)
    
        if self._controller.is_valid_gpio(self.__v2_output):
            self._controller.analog_write(self.__v2_output, value_v2)

#endregion

#region Private Methods

    def __calculate(self):
        """ Apply thermal force to the devices. """

        current_illumination = 0
        delta = 0
        error = 0

        # Read sensor.
        current_illumination = self.__light_sensor.get_value()

        # Calculate the target error.
        error = self.__target_illumination - current_illumination

        # Integrate the delta to temporal output.
        delta = error * self.__error_gain
        self.__tmp_output += delta

        # Limitate the output by target value.
        if self.__tmp_output > abs(self.__output_limit):
            self.__tmp_output = self.__output_limit

        # Limitate by absolute maximum and minimum.
        if self.__tmp_output < 0:
            self.__tmp_output = 0
        if self.__tmp_output > 10000:
            self.__tmp_output = 10000

        # Apply the output if it is different.
        if self.__tmp_output != self.__output:
            self.__output = self.__tmp_output

            # Convert to volgate.
            out_to_v = self.__output * 0.001

            self.__set_voltages(out_to_v, out_to_v)

            self.__logger.debug("TRG {:3.3f}\tINP {:3.3f}\tERR: {:3.3f}\tOUT: {:3.3f}"\
                .format(self.__target_illumination, current_illumination, delta, out_to_v))

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__update_timer = Timer(1)

        self.__target_illum = 0

        self.__init_registers()

        self.__set_voltages(0, 0)

    def _update(self):
        """Update the plugin.
        """

        # If there is no one at the zone, just turn off the lights.
        is_empty = self.__is_empty()
        
        # If the zone is empty, turn the lights off.
        if is_empty:
            self.__last_target_illum = self.__target_illum
            self.__target_illum = 0

        else:
            self.__target_illum = self.__last_target_illum

        # Update sensor data.
        self.__light_sensor.update()

        self.__update_timer.update()
        if self.__update_timer.expired:
            self.__update_timer.clear()

            self.__calculate()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))
        self.__set_voltages(0, 0)

#endregion
