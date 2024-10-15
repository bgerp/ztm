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

from plugins.base_plugin import BasePlugin
from devices.factories.fans.fans_factory import FansFactory
from devices.factories.air_dampers.air_dampers_factory import AirDampersFactory

from data.register import Register
from data.thermal_mode import ThermalMode
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

__class_name__ = "Vent"
"""Plugin class name."""

#endregion

class AirValveState(Enum):
    """Ventilation states.
    """    

    NONE = 0
    Off = 1
    Open = 2
    Close = 3

class Zone(BasePlugin):
    """Ventilation zone control."""

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self.__identifier = 0
        """Number identifier.
        """

        if "identifier" in config:
            self.__identifier = config["identifier"]

        self.__logger = None
        """Logger"""

        self.__fans_power_gpio_name = verbal_const.OFF
        """Fans power control GPIO.
        """

        self.__upper_air_damper_dev = None
        """Upper air damper settings.
        """

        self.__lower_air_damper_dev = None
        """Lower air damper settings.
        """

        self.__upper_fan_dev = None
        """Upper fan.
        """

        self.__lower_fan_dev = None
        """Lower fan.
        """

        self.__set_point_op = 0
        """Operators Panel set point.
        """
        
        self.__set_point_hvac = 0
        """HVAC set point.
        """

        self.__set_point_ac = 0
        """Access Control set point.
        """

        self.__window_tamper_settings = {}
        """Window closed sensor input.
        """

    def __del__(self):

        if self.__upper_fan_dev is not None:
            del self.__upper_fan_dev

        if self.__lower_fan_dev is not None:
            del self.__lower_fan_dev

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods (PLC)

    def __read_window_tamper(self):

        state = False

        for tamper in self.__window_tamper_settings:
            # {'WINT_1': '!U0:ID2:FC2:R0:DI0'}

            if self._controller.is_valid_gpio(self.__window_tamper_settings[tamper]):
                state |= self._controller.digital_read(self.__window_tamper_settings[tamper])

            if self.__window_tamper_settings[tamper] == verbal_const.OFF:
                state |= True

        return state

    def __set_upper_air_damper(self, position):

        if not self.__upper_air_damper_dev is None:
            self.__upper_air_damper_dev.position = position
            
    def __set_lower_air_damper(self, position):

        if not self.__lower_air_damper_dev is None:
            self.__lower_air_damper_dev.position = position

    def __set_upper_fan(self, speed):

        if self.__upper_fan_dev is not None:
            self.__upper_fan_dev.speed = speed

    def __set_lower_fan(self, speed):

        if self.__lower_fan_dev is not None:
            self.__lower_fan_dev.speed = speed

#endregion

#region Private Methods

    def __first_index_of_max(self, setpoints):
        for index, etpoint in enumerate(setpoints):
            setpoints[index] = abs(setpoints[index])
        max_value = max(setpoints)
        return setpoints.index(max_value)

#endregion

#region Private Methods (Registers Devices)

    # Fans power GPIO control.
    def __fans_power_gpio(self, register: Register):

        # Check data type.
        if not (register.data_type == "str"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__fans_power_gpio_name = register.value

    # Upper
    def __upper_air_damper_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__upper_air_damper_dev is None:

            self.__upper_air_damper_dev = AirDampersFactory.create(
                name="Air damper upper",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__upper_air_damper_dev is not None:
                self.__upper_air_damper_dev.init()

        elif register.value == {} and self.__upper_air_damper_dev is not None:
            self.__upper_air_damper_dev.shutdown()
            del self.__upper_air_damper_dev

    def __upper_fan_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__upper_fan_dev is None:

            self.__upper_fan_dev = FansFactory.create(
                controller=self._controller,
                name="Upper fan {}".format(self.__identifier),
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__upper_fan_dev is not None:
                self.__upper_fan_dev.init()

        elif register.value == {} and self.__upper_fan_dev is not None:
            self.__upper_fan_dev.shutdown()
            del self.__upper_fan_dev

    def __upper_fan_min_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__upper_fan_dev is not None:
            self.__upper_fan_dev.min_speed = register.value

    def __upper_fan_max_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__upper_fan_dev is not None:
            self.__upper_fan_dev.max_speed = register.value

    def __upper_fan_speed_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # Set the air dampers.
        if abs(register.value) > 0:
            self.__set_lower_air_damper(0)
            self.__set_upper_air_damper(100)
        else:
            self.__set_upper_air_damper(0)

        # Set the speed of the fan.
        self.__set_upper_fan(register.value)

    # Lower
    def __lower_air_damper_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__lower_air_damper_dev is None:

            self.__lower_air_damper_dev = AirDampersFactory.create(
                name="Air damper lower",
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__lower_air_damper_dev is not None:
                self.__lower_air_damper_dev.init()

        elif register.value == {} and self.__lower_air_damper_dev is not None:
            self.__lower_air_damper_dev.shutdown()
            del self.__lower_air_damper_dev

    def __lower_fan_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != {} and self.__lower_fan_dev is None:

            self.__lower_fan_dev = FansFactory.create(
                controller=self._controller,
                name="Lower fan {}".format(self.__identifier),
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__lower_fan_dev is not None:
                self.__lower_fan_dev.init()

        elif register.value == {} and self.__lower_fan_dev is not None:
            self.__lower_fan_dev.shutdown()
            del self.__lower_fan_dev

    def __lower_fan_min_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value < 0:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__lower_fan_dev is not None:
            self.__lower_fan_dev.min_speed = register.value

    def __lower_fan_max_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value > 100:
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__lower_fan_dev is not None:
            self.__lower_fan_dev.max_speed = register.value

    def __lower_fan_speed_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        # Set the air dampers.
        if abs(register.value) > 0:
            self.__set_upper_air_damper(0)
            self.__set_lower_air_damper(100)
        else:
            self.__set_lower_air_damper(0)

        # Set the speed of the fan.
        self.__set_lower_fan(register.value)

    def __window_tamper_settings_cb(self, register):

          # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__window_tamper_settings = register.value

#endregion

#region Private Methods (Registers Parameters)

    def __op_setpoint_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        temp_value = register.value

        if temp_value > 100:
            temp_value = 100

        if temp_value < 0:
            temp_value = 0

        self.__set_point_op = temp_value

        # self.__logger.info("Ventilation OP set point: {}".format(self.__set_point_op))

    def __hvac_setpoint_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        temp_value = register.value

        if temp_value > 100.0:
            temp_value = 100

        if temp_value < -100.0:
            temp_value = 0

        self.__set_point_hvac = temp_value

        self.__logger.info("Ventilation HVAC set point: {}".format(self.__set_point_hvac))

    def __ac_setpoint_cb(self, register: Register):

        # Check data type.
        if not (register.data_type == "float" or register.data_type == "int"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        temp_value = register.value

        if temp_value > 100:
            temp_value = 100

        if temp_value < 0:
            temp_value = 0

        self.__set_point_ac = temp_value

        self.__logger.info("Ventilation AC set point: {}".format(register.value))

#endregion

#region Private Methods (Registers Initialization)

    def __init_registers(self):

        # Fans power GPIO
        fans_power_gpio = self._registers.by_name("{}.power_gpio_{}".format(self.key, self.__identifier))
        if fans_power_gpio is not None:
            fans_power_gpio.update_handlers = self.__fans_power_gpio
            fans_power_gpio.update()

        # Operator setpoint.
        op_setpoint = self._registers.by_name("{}.op_setpoint_{}".format(self.key, self.__identifier))
        if op_setpoint is not None:
            op_setpoint.update_handlers = self.__op_setpoint_cb
            op_setpoint.update()

        hvac_setpoint = self._registers.by_name("{}.hvac_setpoint_{}".format(self.key, self.__identifier))
        if hvac_setpoint is not None:
            hvac_setpoint.update_handlers = self.__hvac_setpoint_cb
            hvac_setpoint.update()

        ac_setpoint = self._registers.by_name("{}.ac_setpoint_{}".format(self.key, self.__identifier))
        if ac_setpoint is not None:
            ac_setpoint.update_handlers = self.__ac_setpoint_cb
            ac_setpoint.update()

        # Air damper upper.
        upper_air_damper_settings = self._registers.by_name("{}.upper_{}.air_damper.settings".format(self.key, self.__identifier))
        if upper_air_damper_settings is not None:
            upper_air_damper_settings.update_handlers = self.__upper_air_damper_settings_cb
            upper_air_damper_settings.update()


        # Upper fan
        upper_fan_settings = self._registers.by_name("{}.upper_{}.fan.settings".format(self.key, self.__identifier))
        if upper_fan_settings is not None:
            upper_fan_settings.update_handlers = self.__upper_fan_settings_cb
            upper_fan_settings.update()

        upper_fan_min = self._registers.by_name("{}.upper_{}.fan.min_speed".format(self.key, self.__identifier))
        if upper_fan_min is not None:
            upper_fan_min.update_handlers = self.__upper_fan_min_cb
            upper_fan_min.update()

        upper_fan_max = self._registers.by_name("{}.upper_{}.fan.max_speed".format(self.key, self.__identifier))
        if upper_fan_max is not None:
            upper_fan_max.update_handlers = self.__upper_fan_max_cb
            upper_fan_max.update()

        # Air damper lower.
        lower_air_damper_settings = self._registers.by_name("{}.lower_{}.air_damper.settings".format(self.key, self.__identifier))
        if lower_air_damper_settings is not None:
            lower_air_damper_settings.update_handlers = self.__lower_air_damper_settings_cb
            lower_air_damper_settings.update()

        # Lower fan
        lower_fan_settings = self._registers.by_name("{}.lower_{}.fan.settings".format(self.key, self.__identifier))
        if lower_fan_settings is not None:
            lower_fan_settings.update_handlers = self.__lower_fan_settings_cb
            lower_fan_settings.update()

        lower_fan_min = self._registers.by_name("{}.lower_{}.fan.min_speed".format(self.key, self.__identifier))
        if lower_fan_min is not None:
            lower_fan_min.update_handlers = self.__lower_fan_min_cb
            lower_fan_min.update()

        lower_fan_max = self._registers.by_name("{}.lower_{}.fan.max_speed".format(self.key, self.__identifier))
        if lower_fan_max is not None:
            lower_fan_max.update_handlers = self.__lower_fan_max_cb
            lower_fan_max.update()

        # Speeds
        upper_fan_speed = self._registers.by_name("{}.upper_{}.fan.speed".format(self.key, self.__identifier))
        if upper_fan_speed is not None:
            upper_fan_speed.update_handlers = self.__upper_fan_speed_cb
            upper_fan_speed.update()

        lower_fan_speed = self._registers.by_name("{}.lower_{}.fan.speed".format(self.key, self.__identifier))
        if lower_fan_speed is not None:
            lower_fan_speed.update_handlers = self.__lower_fan_speed_cb
            lower_fan_speed.update()

        # Create window closed sensor.
        window_tamper_settings = self._registers.by_name(f"envm.window_tamper.settings")
        if window_tamper_settings is not None:
            window_tamper_settings.update_handlers = self.__window_tamper_settings_cb
            window_tamper_settings.update()

#endregion

#region Private Methods (DEPRECATED)

    def __is_empty(self):

        value = False

        is_empty = self._registers.by_name("envm.is_empty")
        if is_empty is not None:
            value = is_empty.value

        return value

    def __get_thermal_mode(self):

        value = None

        thermal_mode = self._registers.by_name("hvac.thermal_mode_{}".format(self.__identifier))
        if thermal_mode is not None:
            if thermal_mode.value > -1:
                value = ThermalMode(thermal_mode.value)

        return value

    def __calc(self):

        #
        speed_upper = 0
        speed_lower = 0
        calculated_value = 0.0

        #
        thermal_mode = self.__get_thermal_mode()
        is_empty = self.__is_empty()

        # Limits
        lower_limit = 0.0
        mid_1 = 20.0
        mid_2 = 80.0
        upper_limit = 100.0

        # Check the limits.
        if lower_limit <= self.__set_point_op and self.__set_point_op <= mid_1:
            calculated_value = (self.__set_point_op / mid_1) * 20.0

        elif mid_1 < self.__set_point_op and self.__set_point_op < mid_2:
            first = max(self.__set_point_ac, abs(self.__set_point_hvac))
            second = (1 + ((50.0 - self.__set_point_op) / 100.0))
            calculated_value = first * second

        elif mid_2 <= self.__set_point_op and self.__set_point_op <= upper_limit:
            calculated_value = (self.__set_point_op / upper_limit) * 100.


        # if not is_empty:
        if is_empty and (thermal_mode != ThermalMode.NONE):

            # Set upper fan.
            if self.__set_point_hvac < 0:
                speed_upper = calculated_value
            else:
                speed_upper = 0

            # Set lowe fan.
            if self.__set_point_hvac > 0:
                speed_lower = calculated_value
            else:
                speed_lower = 0

        lower_fan_speed = self._registers.by_name("{}.lower_{}.fan.speed".format(self.key, self.__identifier))
        if lower_fan_speed is not None:
            lower_fan_speed.value = speed_lower

        upper_fan_speed = self._registers.by_name("{}.upper_{}.fan.speed".format(self.key, self.__identifier))
        if upper_fan_speed is not None:
            upper_fan_speed.value = speed_upper

        # Update devices.
        if not self.__upper_fan_dev is None:
            self.__upper_fan_dev.update()
        
        if not self.__lower_fan_dev is None:
            self.__lower_fan_dev.update()
        
        if not self.__upper_air_damper_dev is None:
            self.__upper_air_damper_dev.update()
        
        if not self.__lower_air_damper_dev is None:
            self.__lower_air_damper_dev.update()

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin."""

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        # Initialize the registers.
        self.__init_registers()

        # Manually set to automatic mode on wake up.
        self.__set_point_op = 0.0

        # Turn OFF the power for initial step.
        if not self.__fans_power_gpio_name is None:
            self._controller.digital_write(self.__fans_power_gpio_name, 0)

    def _update(self):
        """Runtime of the plugin."""

        # Update occupation flags.
        is_empty = self.__is_empty()

        # If the window is opened, just turn off the HVAC.
        window_tamper_state = self.__read_window_tamper()

        # Take all necessary condition for normal operation of the HVAC.
        stop_flag = (is_empty or window_tamper_state)
        # stop_flag = False

        # Set fan speeds.
        speed_lower = 0
        speed_upper = 0

        # 0 - Set point from the operators panel.
        # 1 - Set point from the HVAC.
        # 2 - Set point from the AC.
        set_points = [self.__set_point_op, self.__set_point_hvac, self.__set_point_ac]
        leading_index = self.__first_index_of_max(set_points)
        leading_setpoint = set_points[leading_index]

        # Power ON/OFF the power of the fans.
        if leading_setpoint != 0 and stop_flag == False:
            self._controller.digital_write(self.__fans_power_gpio_name, 1)
        else:
            self._controller.digital_write(self.__fans_power_gpio_name, 0)

        # If the OP is leading.
        if leading_index == 0:
            # Set the value of the speeds.
            speed_lower = leading_setpoint
            speed_upper = leading_setpoint

        # If HVAC is leading.
        elif leading_index == 1:
            if leading_setpoint == 0:
                speed_lower = 0
                speed_upper = 0
            elif leading_setpoint > 100:
                speed_lower = max(leading_setpoint - 100, 0)
                speed_upper = min(leading_setpoint, 100)
            elif leading_setpoint > 0:
                speed_lower = 0
                speed_upper = leading_setpoint
            elif leading_setpoint < -100:
                speed_lower = min(abs(leading_setpoint), 100)
                speed_upper = max(abs(leading_setpoint) - 100, 0)
            elif leading_setpoint < 0:
                speed_lower = abs(leading_setpoint)
                speed_upper = 0

        # If AC is leading.
        elif leading_index == 2:
            # Set the value of the speeds.
            speed_lower = leading_setpoint
            speed_upper = leading_setpoint

        lower_fan_speed = self._registers.by_name(f"{self.key}.lower_{self.__identifier}.fan.speed")
        if lower_fan_speed is not None:
            lower_fan_speed.value = speed_lower

        upper_fan_speed = self._registers.by_name(f"{self.key}.upper_{self.__identifier}.fan.speed")
        if upper_fan_speed is not None:
            upper_fan_speed.value = speed_upper

        # #C3168
        max_speed = self._registers.by_name(f"{self.key}.fans.max_speed_{self.__identifier}")
        if max_speed is not None:
            max_speed.value = max(speed_lower, speed_upper)

        # Update devices.
        if not self.__lower_fan_dev is None:
            self.__lower_fan_dev.update()

        if not self.__upper_fan_dev is None:
            self.__upper_fan_dev.update()
                
        if not self.__upper_air_damper_dev is None:
            self.__upper_air_damper_dev.update()
        
        if not self.__lower_air_damper_dev is None:
            self.__lower_air_damper_dev.update()

    def _shutdown(self):
        """Shutting down the blinds.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

        # Turn OFF the power affter usage.
        if not self.__fans_power_gpio_name is None:
            self._controller.digital_write(self.__fans_power_gpio_name, 0)

        if not self.__upper_fan_dev is None:
            self.__upper_fan_dev.shutdown()
        
        if not self.__lower_fan_dev is None:
            self.__lower_fan_dev.shutdown()
        
        if not self.__upper_air_damper_dev is None:
            self.__upper_air_damper_dev.shutdown()
        
        if not self.__lower_air_damper_dev is None:
            self.__lower_air_damper_dev.shutdown()

#endregion
