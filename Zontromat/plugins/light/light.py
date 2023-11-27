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
from utils.logger import get_logger
from utils.logic.timer import Timer
from utils.logic.functions import l_scale

from plugins.base_plugin import BasePlugin

from devices.factories.luxmeters.luxmeters_factory import LuxmeterFactory

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

    __r1_output = verbal_const.OFF
    """Relay output R1.
    """

    __r2_output = verbal_const.OFF
    """Relay output R2.
    """


    __hallway_lighting_output = verbal_const.OFF
    """Digital output for controlling hallway lighting.
    """  

    __target_illumination = 50.0
    """Target illumination. [Lux]
    """

    __error_gain = 0.001
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

    __hallway_lighting_time = 0
    """Hallway lighting time. [s]
    """

    __r1_limit = 0.5
    """Resistor current limit.
    note: This value is level when the resistors should be turned on and off. [%]
    """

    __r2_limit = 0.5
    """Resistor current limit.
    note: This value is level when the resistors should be turned on and off. [%]
    """

#endregion

#region Private Methods (Registers Interface)

    def __error_gain_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__error_gain != register.value:
            self.__error_gain = register.value

    def __sensor_settings_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != {} and self.__light_sensor is None:

            self.__light_sensor = LuxmeterFactory.create(
                controller=self._controller,
                name="Room light sensor.",
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__light_sensor is not None:
                self.__light_sensor.init()

        elif register.value == {} and self.__light_sensor is not None:
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

    def __r1_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__r1_output = register.value

    def __r2_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__r2_output = register.value

    def __hallway_lighting_output_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__hallway_lighting_output = register.value

    def __target_illum_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__target_illumination != register.value:
            self.__target_illumination = register.value

    def __hallway_lighting_time_cb(self, register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__hallway_lighting_time != register.value:
            self.__hallway_lighting_time = register.value

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

        r1_output = self._registers.by_name(self.key + ".r1.output")
        if r1_output is not None:
            r1_output.update_handlers = self.__r1_output_cb
            r1_output.update()

        r2_output = self._registers.by_name(self.key + ".r2.output")
        if r2_output is not None:
            r2_output.update_handlers = self.__r2_output_cb
            r2_output.update()

        hallway_lighting_output = self._registers.by_name(self.key + ".hallway_lighting.output")
        if hallway_lighting_output is not None:
            hallway_lighting_output.update_handlers = self.__hallway_lighting_output_cb
            hallway_lighting_output.update()

        error_gain = self._registers.by_name(self.key + ".error_gain")
        if error_gain is not None:
            error_gain.update_handlers = self.__error_gain_cb
            error_gain.update()

        target_illum = self._registers.by_name(self.key + ".target_illum")
        if target_illum is not None:
            target_illum.update_handlers = self.__target_illum_cb
            target_illum.update()

        target_illum = self._registers.by_name(self.key + ".hallway_lighting.time")
        if target_illum is not None:
            target_illum.update_handlers = self.__hallway_lighting_time_cb
            target_illum.update()

    def __is_empty(self):

        value = False

        is_empty = self._registers.by_name("envm.is_empty")
        if is_empty is not None:
            value = is_empty.value

        return value

#endregion

#region Private Methods (Controller Interface)

    def __set_voltages(self, voltage_1, voltage_2):
        """Set the voltage outputs.

        Args:
            voltage_1 (float): Voltage 1.
            voltage_2 (float): Voltage 2.
        """

        value_v1 = voltage_1

        if value_v1 > 10:
            value_v1 = 10

        if value_v1 < 0:
            value_v1 = 0

        value_v2 = voltage_2

        if value_v2 > 10:
            value_v2 = 10

        if value_v2 < 0:
            value_v2 = 0

        # Turn ON and OFF the load resistor of the group 1.
        if value_v1 < self.__r1_limit:
            if self._controller.is_valid_gpio(self.__r1_output):
                self._controller.analog_write(self.__r1_output, 1)
        else:
            if self._controller.is_valid_gpio(self.__r1_output):
                self._controller.analog_write(self.__r1_output, 0)

        # Turn ON and OFF the load resistor of the group 2.
        if value_v2 < self.__r2_limit:
            if self._controller.is_valid_gpio(self.__r2_output):
                self._controller.analog_write(self.__r2_output, 1)
        else:
            if self._controller.is_valid_gpio(self.__r2_output):
                self._controller.analog_write(self.__r2_output, 0)

        # Control the AO2.
        if self._controller.is_valid_gpio(self.__v1_output):
            self._controller.analog_write(self.__v1_output, value_v1)

        # Control the AO3.
        if self._controller.is_valid_gpio(self.__v2_output):
            self._controller.analog_write(self.__v2_output, value_v2)

#endregion

#region Private Methods

    def __flood_fade(self, setpoint):
        """Flood fade generator.

        Args:
            setpoint (float): Setpoint for the hardware.

        Returns:
            list: Output voltages for the two analog outputs.
        """

        # Negative limit.
        if setpoint < 0:
            setpoint = 0

        # Positive limit.
        if setpoint > 100:
            setpoint = 100

        voltage_1 = 0
        voltage_2 = 0

        # The model.
        if setpoint <= 50:
            voltage_1 = l_scale(setpoint, [0, 50], [0, 100])
            voltage_2 = 0
        else:
            voltage_1 = 100
            voltage_2 = l_scale(setpoint, [50, 100], [0, 100])

        # Return the voltages.
        return (voltage_1, voltage_2)

    def __calculate(self):
        """ Apply thermal force to the devices. """

        current_illumination = 0
        target_illumination = 0
        delta = 0
        error = 0

        # If there is no one at the zone, just turn off the lights.
        is_empty = self.__is_empty()

        # Scale t
        target_illumination = l_scale(self.__target_illumination, [0.0, self.__output_limit], [0.0, 100.0])

        # Read sensor.
        if self.__light_sensor is not None:
            current_illumination = self.__light_sensor.get_value()
            current_illumination = l_scale(current_illumination, [0.0, self.__output_limit], [0.0, 100.0])

        # Limits
        lower_limit = 0.0
        mid_1 = 20.0
        mid_2 = 80.0
        upper_limit = 100.0

        # Check the limits.
        if lower_limit <= target_illumination <= mid_1:
            self.__tmp_output = (target_illumination / mid_1) * 20.0

        elif mid_1 < target_illumination < mid_2:

            # Apply the formula.
            first = current_illumination
            second = (1 + ((50.0 - target_illumination) / 100.0))
            calculated_value = first * second

            # Calculate the target error.
            error = calculated_value - current_illumination

            # Integrate the delta to temporal output.
            delta = error * self.__error_gain
            self.__tmp_output += delta

        elif mid_2 <= target_illumination <= upper_limit:
            self.__tmp_output = (target_illumination / upper_limit) * 100.

        # Limitate the output by target value.
        if self.__tmp_output > abs(self.__output_limit):
            self.__tmp_output = self.__output_limit

        # Limitate by absolute maximum and minimum.
        if self.__tmp_output < 0:
            self.__tmp_output = 0
        if self.__tmp_output > 100:
            self.__tmp_output = 100

        # Apply the output if it is different.
        self.__output = self.__tmp_output

        # Convert to volgate.
        to_voltage_scale = 0.1 # Magic number!!!
        voltage_1, voltage_2 = self.__flood_fade(self.__output)
        out_to_v1 = voltage_1 * to_voltage_scale
        out_to_v2 = voltage_2 * to_voltage_scale

        # If the zone is empty, turn the lights off.
        if is_empty:
            pass

        # set the voltage.
        self.__set_voltages(out_to_v1, out_to_v2)

        self.__logger.debug("TRG {:3.3f}\tINP {:3.3f}\tERR: {:3.3f}\tOUT1: {:3.3f}\tOUT2: {:3.3f}"\
            .format(target_illumination, current_illumination, delta, out_to_v1, out_to_v2))

    def __test_update(self):

        # If there is no one at the zone, just turn off the lights.
        is_empty = self.__is_empty()

        # Read sensor.
        if self.__light_sensor is not None:
            current_illumination = self.__light_sensor.get_value()
            current_illumination = l_scale(current_illumination, [0.0, self.__output_limit], [0.0, 100.0])

        # Variate from 0 to 100%.
        self.__output = self.__target_illumination
        fade_data = self.__flood_fade(self.__output)
        result_v1 = l_scale(fade_data[0], [0, 100], [0, 10])
        result_v2 = l_scale(fade_data[1], [0, 100], [0, 10])
        self.__set_voltages(result_v1, result_v2)

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__update_timer = Timer(0.05)

        self.__init_registers()

        self.__set_voltages(0, 0)

    def _update(self):
        """Update the plugin.
        """

        # Calculate hallway lighting time.
        # startup_time = 0
        # startup_time = self._registers.by_name("sys.time.startup")
        # if startup_time is not None:
        #     startup_pass_time = time.time() - startup_time.value

        # state = "OFF"
        # if startup_pass_time <= self.__hallway_lighting_time:
        #     state = "OFF"
            
        # else:
        #     state = "ON"
    
        
        # self.__logger.debug(f"Wait time {self.__hallway_lighting_time - startup_pass_time}; State: {state}")

        # return

        # Update sensor data.
        if self.__light_sensor is not None:
            self.__light_sensor.update()

        self.__update_timer.update()
        if self.__update_timer.expired:
            self.__update_timer.clear()

            # self.__calculate()

            self.__test_update()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))
        self.__set_voltages(0, 0)

#endregion
