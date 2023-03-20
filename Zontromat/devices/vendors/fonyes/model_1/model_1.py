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

from devices.factories.air_dampers.base_air_damper import BaseAirDamper
from devices.factories.air_dampers.air_damper_state import AirDamperState

# (Request from mail: Eml6429)

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

class AirDamper1(BaseAirDamper):
    """Fonyes - Model1. Fire damper
    """

    __example_settings = {"vendor": "fonyes", "model": "model_1", "options": {"output_cw": "off", "output_ccw": "off"}}

#region Attributes

#endregion

#region Constructor / Destructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self._vendor = "Fonyes"

        self._model = "model_1"

        self.__logger = get_logger(__name__)

        if "output_cw" in self._config:
            self.__output_cw = self._config["output_cw"]

        if "output_ccw" in self._config:
            self.__output_ccw = self._config["output_ccw"]

#endregion

#region Private Methods

    def __set_postion(self, position):

        # Determin is it analog or digital output.
        if ("D" in self.__output) or ("R" in self.__output):

            if position > 0:
                self._controller.digital_write(self.__output_cw, 0)
                self._controller.digital_write(self.__output_ccw, 1)

            else:
                self._controller.digital_write(self.__output_ccw, 0)
                self._controller.digital_write(self.__output_cw, 1)

#endregion

#region Public Methods

    def init(self):
        """Initialize the valve.
        """

        self.target_position = 0
        self.update()

    def update(self):
        """Update the valve.
        """

        if self._current_position != self.target_position:
            self._current_position = self.target_position

        # If it is time then move the valve.
        if self._state.is_state(AirDamperState.Prepare):
            self.__set_postion(self.target_position)
            self.__logger.debug("{} @ {}".format(self.name, self.target_position))
            self._state.set_state(AirDamperState.Wait)

#endregion
