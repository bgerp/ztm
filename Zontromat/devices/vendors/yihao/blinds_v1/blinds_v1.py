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

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from data import verbal_const

from devices.factories.blinds.base_blind import BaseBlind

from utils.logger import get_logger
from utils.logic.functions import l_scale

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

class BlindsV1(BaseBlind):
    """Electronic blinds"""

#region Attributes

    __new_position = 0
    """New position of the blinds."""

#endregion

#region constructor / Destructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "YIHAO"

        self._model = "BlindsV1"

        self.__logger = get_logger(__name__)

#endregion

#region Public Methods

    def init(self):
        pass

    def update(self):
        pass

    def shutdown(self):
        pass

    def set_position(self, position):
        """Set position of the blinds.

        Args:
            position (float): Position of the blinds.
        """

        if self.__new_position == position:
            return

        if position > 180:
            position = 180

        elif position < 0:
            position = 0

        scaled_position = l_scale(position, [0, 180], [0, 100])

        # TODO: Calculations.

        restored_position = l_scale(scaled_position, [0, 100], [0, 180])

        self.__new_position = restored_position

#endregion
