
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

from devices.factories.convectors.convector_base import BaseConvector

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

class Klimafan(BaseConvector):
    """Convector Manufacturer: Silpa; Model: Klimafan"""

#region Attributes

    __logger = None
    """Logger"""

    __state = -1
    """State of the convector."""

#endregion

#region Constructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self._vendor = "Silpa"

        self._model = "Klimafan"

        self.__logger = get_logger(__name__)

#region Public Methods

    def init(self):
        """Initialize the convector."""

        self.set_state(0)

    def get_state(self):
        """Return value of the output.

        Returns
        -------
        float
            Circuit state.
        """

        return self.__state

    def set_state(self, state):
        """Set value of the output.

        Args:
            value (int): Output value.
        """

        if self.__state == state:
            return

        self.__state = state

        self._controller.digital_write(self._config["stage1"], 0)
        self._controller.digital_write(self._config["stage2"], 0)
        self._controller.digital_write(self._config["stage3"], 0)

        if self.__state == 1:
            self._controller.digital_write(self._config["stage1"], 1)
            self._controller.digital_write(self._config["stage2"], 0)
            self._controller.digital_write(self._config["stage3"], 0)

        elif self.__state == 2:
            self._controller.digital_write(self._config["stage1"], 0)
            self._controller.digital_write(self._config["stage2"], 1)
            self._controller.digital_write(self._config["stage3"], 0)

        elif self.__state == 3:
            self._controller.digital_write(self._config["stage1"], 0)
            self._controller.digital_write(self._config["stage2"], 0)
            self._controller.digital_write(self._config["stage3"], 1)

        self.__logger.debug("{} @ {}".format(self.name, self.__state))

    def shutdown(self):

        self.set_state(0)

#endregion
