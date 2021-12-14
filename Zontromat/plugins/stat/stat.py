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
from time import gmtime, strftime
import logging

from utils.logger import get_logger
from utils.logic.timer import Timer

from plugins.base_plugin import BasePlugin

from data.register import Register

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from devices.factories.light_sensor.light_sensor_factory import LightSensorFactory

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2021, POLYGON Team Ltd."
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

__class_name__ = "Statistics"
"""Plugin class name."""

#endregion

class Statistics(BasePlugin):
    """Template plugin controller."""

#region Attributes

    __logger = None
    """Logger"""

    __update_timer = None
    """Update timer."""

    __light_sensor = None
    """Light sensor target.
    """

#endregion

#region Private Methods

    def __get_todays_path(self, name=""):

        # Current file path.
        cwf = os.path.dirname(os.path.abspath(__file__))

        # Statistics path.
        full_dir_path = os.path.join(cwf, "..", "..", "..", "statistics")

        # Crete log directory.
        if not os.path.exists(full_dir_path):
            os.makedirs(full_dir_path)

        # Todays filename.
        todays_file_name = strftime("%Y%m%d_%H%M%S", gmtime())
        if not name != "":
            todays_file_name += "_"
            todays_file_name += name
        todays_file_name += ".log"

        # File name.
        file_name = os.path.join(full_dir_path, todays_file_name)

        return file_name

    def __create_logger(self, name, level=logging.INFO):
        """To setup as many loggers as you want"""

        log_file = self.__get_todays_path(name)

        # Formater
        # log_format = "%(asctime)s\t%(levelname)s\t%(name)s\t%(lineno)s\t%(message)s"
        log_format = "%(asctime)s\t%(name)s\t%(message)s"
        formatter = logging.Formatter(log_format)

        # Handler
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)

        # Logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    def __periodic_job(self):
        """Do the JOB method."""

        if self.__light_sensor is not None:
            self.__light_sensor.update()
            measured_value = self.__light_sensor.get_value()
            if self.__light_sensor_logger is not None:
                self.__light_sensor_logger.info("{}".format(measured_value))

#endregion

#region Private Methods (Registers Interface)

    def __light_sensor_settings_cb(self, register: Register):

                # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if register.value != None and self.__light_sensor is None:

            dev_name = "{} {}".format("Test sensor", self.name)
            self.__light_sensor = LightSensorFactory.create(
                name=dev_name,
                controller=self._controller,
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__light_sensor is not None:
                self.__light_sensor.init()

    def __init_registers(self):

        sensor_enabled = self._registers.by_name("light.sensor.settings")
        if sensor_enabled is not None:
            sensor_enabled.update_handlers = self.__light_sensor_settings_cb
            sensor_enabled.update()

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {}".format(self.name))

        self.__update_timer = Timer(1)

        self.__light_sensor_logger = self.__create_logger("LightSensor")

        self.__init_registers()


    def _update(self):
        """Update the plugin.
        """

        # Update the timer.
        self.__update_timer.update()

        if self.__update_timer.expired:

            self.__update_timer.clear()

            self.__periodic_job()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {}".format(self.name))

#endregion
