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

import os

from utils.logger import get_logger
from utils.logic.timer import Timer
from utils.utils import disk_size

from plugins.base_plugin import BasePlugin
from plugins.sys.monitoring_level import MonitoringLevel
from plugins.sys.rule import Rule
from plugins.sys.rules import Rules

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

__class_name__ = "Sys"
"""Plugin class name."""

#endregion

class Sys(BasePlugin):
    """Blinds controller device."""

#region Attributes

    __logger = None
    """Logger"""

    __led_state = 0
    """LED State."""

    __blink_timer = None
    """Update timestamp."""

    __led_out = verbal_const.OFF
    """LED Output"""

    __collission_timer = None
    """Update timer."""

    __rules = None
    """Rules"""

    __enable_info_msg = True
    """Enable info messages."""

    __enable_wrn_msg = True
    """Enable warning messages."""

    __enable_err_msg = True
    """Enable error messages."""

    __disc_status_timer = None
    """Disc check timer."""

#endregion

#region Destructor

    def __del__(self):

        if self.__blink_timer is not None:
            del self.__blink_timer

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods (Status LED)

    def __set_led(self, state):

        if self._controller.is_valid_gpio(self.__led_out):
            self._controller.set_led(self.__led_out, state)

#endregion

#region Private Methods (Colision Detection)

    def __setup_rules(self):

        self.__rules = Rules()

        # GPIOs
        for index in range(12):
            self.__rules.add(Rule("DO{}".format(index), MonitoringLevel.Error))
            self.__rules.add(Rule("DI{}".format(index), MonitoringLevel.Warning))
            self.__rules.add(Rule("AO{}".format(index), MonitoringLevel.Error))
            self.__rules.add(Rule("AI{}".format(index), MonitoringLevel.Warning))
            self.__rules.add(Rule("RO{}".format(index), MonitoringLevel.Error))

        # 1 Wire devices
        ow_devices = self._controller.get_1w_devices()
        for ow_device in ow_devices:
            self.__rules.add(Rule(ow_device["circuit"], MonitoringLevel.Info))

        # Serial Ports
        if os.name == "nt":
            for index in range(1, 11):
                self.__rules.add(Rule("COM{}".format(index), MonitoringLevel.Error))

        elif os.name == "posix":
            for index in range(0, 11):
                self.__rules.add(Rule("/dev/ttyS{}".format(index), MonitoringLevel.Error))
                self.__rules.add(Rule("/dev/ttyUSB{}".format(index), MonitoringLevel.Error))
                self.__rules.add(Rule("/dev/ttyACM{}".format(index), MonitoringLevel.Error))

        # Add event.
        self.__rules.on_event(self.__on_event)

    def __on_event(self, intersections, rule: Rule):
        """On event callback for collisions."""

        level = MonitoringLevel(rule.level)

        if level == MonitoringLevel.Debug:
            self.__logger.debug("Debug")
            self.__logger.debug(intersections)

        if level == MonitoringLevel.Info and self.__enable_info_msg:
            self._registers.write("{}.col.info_message".format(self.key), intersections)

        if level == MonitoringLevel.Warning and self.__enable_wrn_msg:
            self._registers.write("{}.col.warning_message".format(self.key), intersections)

        if level == MonitoringLevel.Error and self.__enable_err_msg:
            self._registers.write("{}.col.error_message".format(self.key), intersections)

#endregion

#region Private Methods (Registers Interface)

    def __blink_time_cb(self, register):

        # Check data type.
        if not (register.data_type == "int" or register.data_type == "float"):
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__blink_timer.expiration_time = register.value

    def __led_out_cb(self, register):

        # Check data type.
        if not register.data_type == "str":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__led_out = register.value

    def __clear_errors_cb(self, register):
        """Clear errors callback."""

        if register.value == 1:
            # Clear the flag.
            register.value = 0

            # Clear info messages.
            self._registers.write("{}.col.info_message".format(self.key), {})

            # Clear warning messages.
            self._registers.write("{}.col.warning_message".format(self.key), {})

            # Clear error messages.
            self._registers.write("{}.col.error_message".format(self.key), {})

    def __enable_info_msg_cb(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__enable_info_msg = register.value

    def __enable_wrn_msg_cb(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__enable_wrn_msg = register.value

    def __enable_err_msg_cb(self, register):

        # Check data type.
        if not register.data_type == "bool":
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        self.__enable_err_msg = register.value

    def __init_registers(self):

        # Status LED blink time.
        blink_time = self._registers.by_name(self.key + ".sl.blink_time")
        if blink_time is not None:
            blink_time.update_handlers = self.__blink_time_cb
            blink_time.update()

        # Status LED output.
        output = self._registers.by_name(self.key + ".sl.output")
        if output is not None:
            output.update_handlers = self.__led_out_cb
            output.update()

        clear_errors = self._registers.by_name(self.key + ".col.clear_errors")
        if clear_errors is not None:
            clear_errors.update_handlers = self.__clear_errors_cb
            clear_errors.value = 1

        # Enable info messages.
        enable_info_msg = self._registers.by_name(self.key + ".col.info_message.enable")
        if enable_info_msg is not None:
            enable_info_msg.update_handlers = self.__enable_info_msg_cb
            enable_info_msg.update()

        # Enable warning messages.
        enable_wrn_msg = self._registers.by_name(self.key + ".col.warning_message.enable")
        if enable_wrn_msg is not None:
            enable_wrn_msg.update_handlers = self.__enable_wrn_msg_cb
            enable_wrn_msg.update()

        # Enable error messages.
        enable_err_msg = self._registers.by_name(self.key + ".col.error_message.enable")
        if enable_err_msg is not None:
            enable_err_msg.update_handlers = self.__enable_err_msg_cb
            enable_err_msg.update()

    def __update_disc_space(self):

        total, used, free = disk_size()

        self._registers.write("sys.disc.total", total)
        self._registers.write("sys.disc.used", used)
        self._registers.write("sys.disc.free", free)

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        # Create logger.
        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        # Status LED blink timer.
        self.__blink_timer = Timer(1)

        # Colission detection.
        self.__collission_timer = Timer(1)

        # Create disc check timer.
        self.__disc_status_timer = Timer(10)

        self.__init_registers()

        self.__setup_rules()

    def _update(self):
        """Update the plugin.
        """

        # Update the Blink LED timer.
        self.__blink_timer.update()
        if self.__blink_timer.expired:
            self.__blink_timer.clear()

            if self.__led_state:
                self.__led_state = 0
            else:
                self.__led_state = 1

            # update the LED state.
            self.__set_led(self.__led_state)

        # Update the collision timer.
        self.__collission_timer.update()
        if self.__collission_timer.expired:
            self.__collission_timer.clear()

             # Check for collision.
            self.__rules.check(self._registers)

        # Update disc space.
        self.__disc_status_timer.update()
        if self.__disc_status_timer.expired:
            self.__disc_status_timer.clear()

            # Update the disck space registers.
            self.__update_disc_space()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))
        self.__set_led(0)

#endregion
