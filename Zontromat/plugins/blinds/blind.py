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

import math

from utils.logger import get_logger
from utils.logic.timer import Timer
from utils.logic.functions import to_rad, shadow_length

from plugins.base_plugin import BasePlugin

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from devices.factories.blinds.blinds_factory import BlindsFactory

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

#endregion

class Blind(BasePlugin):
    """Blind controller device."""

#region Attributes

    __logger = None
    """Logger"""

    __identifier = 0
    """Identifier
    """

    __blind_mechanism = None
    """Blkind mechanism
    """

    __sun_spot_update_timer = None
    """Sun spot update timer.
    """

    __sun_azm = 0
    """Sun azimuth.
    """

    __sun_elev = 0
    """Sun elevation.
    """

    __sun_spot_limit = 0
    """Sun spot limit.
    """

    __object_height = 0
    """Object height [m]
    """

    __zone_occupation = False
    """Zone occupation flag.
    """

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        if "identifier" in config:
            self.__identifier = config["identifier"]

    def __del__(self):
        """Destructor"""

        super().__del__()

        if self.__logger is not None:
            del self.__logger

#endregion

#region Private Methods (Registers)

    def __blind_cb(self, register):

        # Check data type.
        if not register.data_type == "json":
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        # Create
        if register.value != {} and self.__blind_mechanism is None:

            self.__blind_mechanism = BlindsFactory.create(
                controller=self._controller,
                name="Blind",
                vendor=register.value['vendor'],
                model=register.value['model'],
                options=register.value['options'])

            if self.__blind_mechanism is not None:
                self.__blind_mechanism.init()

        # Delete
        elif register.value == {} and self.__blind_mechanism is not None:
            del self.__blind_mechanism

    def __position_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__blind_mechanism is not None:
            self.__blind_mechanism.set_position(register.value)

    def __object_height_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__object_height != register.value:
            self.__object_height = register.value

    def __sunspot_limit_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__sun_spot_limit != register.value:
            self.__sun_spot_limit = register.value

    def __zone_occupation_cb(self, register):

        # Check data type.
        if not ((register.data_type == "float") or (register.data_type == "int")):
            GlobalErrorHandler.log_bad_register_value(self.__logger, register)
            return

        if self.__zone_occupation != register.value:
            self.__zone_occupation = register.value

    def __init_registers(self):

        blind = self._registers.by_name("{}.blind_{}.mechanism".format(self.key, self.__identifier))
        if blind is not None:
            blind.update_handlers = self.__blind_cb
            blind.update()

        position = self._registers.by_name("{}.blind_{}.position".format(self.key, self.__identifier))
        if position is not None:
            position.update_handlers = self.__position_cb
            position.update()

        object_height = self._registers.by_name("{}.blind_{}.object_height".format(self.key, self.__identifier))
        if object_height is not None:
            object_height.update_handlers = self.__object_height_cb
            object_height.update()

        sunspot_limit = self._registers.by_name("{}.blind_{}.sunspot_limit".format(self.key, self.__identifier))
        if sunspot_limit is not None:
            sunspot_limit.update_handlers = self.__sunspot_limit_cb
            sunspot_limit.update()

        ac_zone_occupied = self._registers.by_name("ac.zone_{}_occupied".format(self.__identifier))
        if ac_zone_occupied is not None:
            ac_zone_occupied.update_handlers = self.__zone_occupation_cb
            ac_zone_occupied.update()

    def __get_sun_pos(self):

        sun_elev_reg = self._registers.by_name("envm.sun.elevation")
        if sun_elev_reg is not None:
            if not ((sun_elev_reg.data_type == "float") or (sun_elev_reg.data_type == "int")):
                GlobalErrorHandler.log_bad_register_value(self.__logger, sun_elev_reg)
                return

            if self.__sun_elev != sun_elev_reg.value:
                self.__sun_elev = sun_elev_reg.value

        sun_azm_reg = self._registers.by_name("envm.sun.azimuth")
        if sun_azm_reg is not None:
            if not ((sun_azm_reg.data_type == "float") or (sun_azm_reg.data_type == "int")):
                GlobalErrorHandler.log_bad_register_value(self.__logger, sun_azm_reg)
                return

            if self.__sun_azm != sun_azm_reg.value:
                self.__sun_azm = sun_azm_reg.value

#endregion

#region Private Methods

    def __calc_sun_spot(self):

        if (self.__sun_azm > 0) and (self.__sun_elev > 0):
            # print(f"Blinds -> Azm: {self.__sun_azm:03.2f}; Elev: {self.__sun_elev:03.2f}")

            # Calculate the shadow length.
            shadow_l = shadow_length(self.__object_height, to_rad(self.__sun_elev))
            # print(f"Blinds -> Shadow: {shadow_l:03.2f}")

            theta = 360 - (self.__sun_azm + 180)
            # print(f"Blinds -> Theta: {theta:03.2f}")

            # Calculate cartesian
            x = shadow_l * math.cos(to_rad(abs(theta)))
            y = shadow_l * math.sin(to_rad(abs(theta)))
            # print(f"Blinds -> X: {x:03.2f}; Y: {y:03.2f}")

            is_cloudy = False
            if (x > self.__sun_spot_limit or y > self.__sun_spot_limit) and not is_cloudy:
                
                # If is not cloudy and the sun spot is too big, just close the blinds.
                if not self.__blind_mechanism is None:
                    self.__blind_mechanism.set_position(0)

#endregion

#region Public Methods

    def _init(self):
        """Initialize the plugin.
        """

        self.__logger = get_logger(__name__)
        self.__logger.info("Starting up the {} {}".format(self.name, self.__identifier))

        self.__sun_spot_update_timer = Timer(2)

        self.__init_registers()

        if not self.__blind_mechanism is None:
            self.__blind_mechanism.set_position(90)

    def _update(self):
        """Update the plugin.
        """

        # Update occupation flags.
        if not self.__zone_occupation:
            if not self.__blind_mechanism is None:
                # self.__blind_mechanism.set_position(0)
                pass

        self.__sun_spot_update_timer.update()
        if self.__sun_spot_update_timer.expired:
            self.__sun_spot_update_timer.clear()

            self.__get_sun_pos()
            self.__calc_sun_spot()

        if not self.__blind_mechanism is None:
            self.__blind_mechanism.update()

    def _shutdown(self):
        """Shutting down the plugin.
        """

        self.__logger.info("Shutting down the {} {}".format(self.name, self.__identifier))

        if not self.__blind_mechanism is None:
            self.__blind_mechanism.shutdown()

#endregion