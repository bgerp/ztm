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
from utils.logic.timer import Timer
from utils.utils import disk_size

from plugins.base_plugin import BasePlugin
from devices.factories.fan.fan_factory import FanFactory

from data import verbal_const
from data.register import Register
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

__class_name__ = "Vent"
"""Plugin class name."""

#endregion

class AirValveState(Enum):
    NONE = 0
    Off = 1
    Open = 2
    Close = 3

class Ventilation(BasePlugin):
    """Ventilation zone controll."""

#region Attributes

    __logger = None
    """Logger"""

    __identifier = 0
    """Number identifier.
    """

    __upper_fan_dev = None
    """Upper fan.
    """    

    __lower_fan_dev = None
    """Lower fan.
    """

    __occupied_flag = False
    """Occupied flag.
    """

    __set_point_op = 0
    """Operators Panel set point.
    """    
    __set_point_hvac = 0
    """HVAC set point.
    """    
    __set_point_ac = 0
    """Access Control set point. 
    """

    __upper_valve_settings = {}
    """Lower valve settings.
    """

    __lower_valve_settings = {}
    """Lower valve settings.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        if "identifier" in config:
            self.__identifier = config["identifier"]

    def __del__(self):

        if self.__upper_fan_dev is not None:
            del self.__upper_fan_dev

        if self.__lower_fan_dev is not None:
            del self.__lower_fan_dev

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods (PLC IO)

    def __set_upper_valve(self, state: AirValveState = AirValveState.NONE):

        if self.__upper_valve_settings == None:
            return

        if len(self.__upper_valve_settings) == 0:
            return

        if state == AirValveState.Close:
            self._controller.digital_write(self.__upper_valve_settings["open"], 0)
            self._controller.digital_write(self.__upper_valve_settings["close"], 1)

        elif state == AirValveState.Open:
            self._controller.digital_write(self.__upper_valve_settings["close"], 0)
            self._controller.digital_write(self.__upper_valve_settings["open"], 1)

        elif state == AirValveState.Off:
            self._controller.digital_write(self.__upper_valve_settings["close"], 0)
            self._controller.digital_write(self.__upper_valve_settings["open"], 0)

    def __set_lower_valve(self, state):

        if self.__lower_valve_settings == None:
            return

        if len(self.__lower_valve_settings) == 0:
            return

        if state == AirValveState.Close:
            self._controller.digital_write(self.__lower_valve_settings["open"], 0)
            self._controller.digital_write(self.__lower_valve_settings["close"], 1)

        elif state == AirValveState.Open:
            self._controller.digital_write(self.__lower_valve_settings["close"], 0)
            self._controller.digital_write(self.__lower_valve_settings["open"], 1)

        elif state == AirValveState.Off:
            self._controller.digital_write(self.__lower_valve_settings["close"], 0)
            self._controller.digital_write(self.__lower_valve_settings["open"], 0)

#endregion

#region Private Methods (Registers)

    # Upper valve.
    def __upper_valve_settings_cb(self, register: Register):
        
        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        register_value = register.value
        if register_value is not None:
            segments = register_value.split("/")
            self.__upper_valve_settings["close"] = segments[2]
            self.__upper_valve_settings["open"] = segments[3]

    # Lower valve.
    def __lower_valve_settings_cb(self, register: Register):
        
        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        register_value = register.value
        if register_value is not None:
            segments = register_value.split("/")
            self.__lower_valve_settings["close"] = segments[2]
            self.__lower_valve_settings["open"] = segments[3]

    # Params
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

        self.__logger.info("Ventilation OP set point: {}".format(self.__set_point_op))

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


    # Upper fan
    def __upper_fan_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__upper_fan_dev is None:

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__upper_fan_dev = FanFactory.create(
                controller=self._controller,
                name="Upper fan {}".format(self.__identifier),
                params=params)

            if self.__upper_fan_dev is not None:
                self.__upper_fan_dev.init()

        elif register.value == verbal_const.OFF and self.__upper_fan_dev is not None:
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

        if self.__upper_fan_dev is not None:
            self.__upper_fan_dev.speed = register.value

            
            if abs(register.value) > 0:
                self.__set_lower_valve(AirValveState.Close)
                self.__set_upper_valve(AirValveState.Open)
            else:
                self.__set_upper_valve(AirValveState.Close)

    # Lower fan
    def __lower_fan_settings_cb(self, register: Register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value != verbal_const.OFF and self.__lower_fan_dev is None:

            params = register.value.split("/")

            if len(params) <= 2:                
                raise ValueError("Not enough parameters.")

            self.__lower_fan_dev = FanFactory.create(
                controller=self._controller,
                name="Lower fan {}".format(self.__identifier),
                params=params)

            if self.__lower_fan_dev is not None:
                self.__lower_fan_dev.init()

        elif register.value == verbal_const.OFF and self.__lower_fan_dev is not None:
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

        if self.__lower_fan_dev is not None:
            self.__lower_fan_dev.speed = register.value


            if abs(register.value) > 0:
                self.__set_upper_valve(AirValveState.Close)
                self.__set_lower_valve(AirValveState.Open)
            else:
                self.__set_lower_valve(AirValveState.Close)


    def __init_registers(self):

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

        # Upper fan
        upper_fan_enabled = self._registers.by_name("{}.upper_{}.fan.settings".format(self.key, self.__identifier))
        if upper_fan_enabled is not None:
            upper_fan_enabled.update_handlers = self.__upper_fan_settings_cb
            upper_fan_enabled.update()

        upper_fan_min = self._registers.by_name("{}.upper_{}.fan.min_speed".format(self.key, self.__identifier))
        if upper_fan_min is not None:
            upper_fan_min.update_handlers = self.__upper_fan_min_cb
            upper_fan_min.update()

        upper_fan_max = self._registers.by_name("{}.upper_{}.fan.max_speed".format(self.key, self.__identifier))
        if upper_fan_max is not None:
            upper_fan_max.update_handlers = self.__upper_fan_max_cb
            upper_fan_max.update()

        upper_fan_speed = self._registers.by_name("{}.upper_{}.fan.speed".format(self.key, self.__identifier))
        if upper_fan_speed is not None:
            upper_fan_speed.update_handlers = self.__upper_fan_speed_cb
            upper_fan_speed.update()

        # Lower fan
        lower_fan_enabled = self._registers.by_name("{}.lower_{}.fan.settings".format(self.key, self.__identifier))
        if lower_fan_enabled is not None:
            lower_fan_enabled.update_handlers = self.__lower_fan_settings_cb
            lower_fan_enabled.update()

        lower_fan_min = self._registers.by_name("{}.lower_{}.fan.min_speed".format(self.key, self.__identifier))
        if lower_fan_min is not None:
            lower_fan_min.update_handlers = self.__lower_fan_min_cb
            lower_fan_min.update()

        lower_fan_max = self._registers.by_name("{}.lower_{}.fan.max_speed".format(self.key, self.__identifier))
        if lower_fan_max is not None:
            lower_fan_max.update_handlers = self.__lower_fan_max_cb
            lower_fan_max.update()

        lower_fan_speed = self._registers.by_name("{}.lower_{}.fan.speed".format(self.key, self.__identifier))
        if lower_fan_speed is not None:
            lower_fan_speed.update_handlers = self.__lower_fan_speed_cb
            lower_fan_speed.update()

        lower_valve_settings = self._registers.by_name("{}.lower_{}.valve.settings".format(self.key, self.__identifier))
        if lower_valve_settings is not None:
            lower_valve_settings.update_handlers = self.__lower_valve_settings_cb
            lower_valve_settings.update()

        upper_valve_settings = self._registers.by_name("{}.upper_{}.valve.settings".format(self.key, self.__identifier))
        if upper_valve_settings is not None:
            upper_valve_settings.update_handlers = self.__upper_valve_settings_cb
            upper_valve_settings.update()

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
        self.__set_point_op = 50.0

    def _update(self):
        """Runtime of the plugin."""

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

        elif mid_1 < self.__set_point_op and self.__set_point_op  < mid_2:
            first = max(self.__set_point_ac, abs(self.__set_point_hvac))
            second = (1 + ((50.0 - self.__set_point_op) / 100.0))
            calculated_value = first * second

        elif mid_2 <= self.__set_point_op and self.__set_point_op  <= upper_limit:
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
            lower_fan_speed.update()

        upper_fan_speed = self._registers.by_name("{}.upper_{}.fan.speed".format(self.key, self.__identifier))
        if upper_fan_speed is not None:
            upper_fan_speed.value = speed_upper
            upper_fan_speed.update()

        self.__upper_fan_dev.update()
        self.__lower_fan_dev.update()

    def _shutdown(self):
        """Shutting down the blinds.
        """

        self.__logger.info("Shutting down the {}".format(self.name))
        self.__upper_fan_dev.shutdown()
        self.__lower_fan_dev.shutdown()
        self.__set_upper_valve(AirValveState.Close)
        self.__set_lower_valve(AirValveState.Close)
        
#endregion

    # TODO: Change the formula. Ventilation will call the HVAC, AC, MANUAL registers.