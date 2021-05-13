
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
from devices.base_device import BaseDevice

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

class Klimafan(BaseDevice):
    """Convector"""

#region Attributes

    __logger = None
    """Logger"""

    __state = -1
    """State of the convector."""

#endregion

#region Public Methods

    def init(self):
        """Init the convector."""

        self.__logger = get_logger(__name__)

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

        self._controller.digital_write(self._config["stage_1"], 0)
        self._controller.digital_write(self._config["stage_2"], 0)
        self._controller.digital_write(self._config["stage_3"], 0)

        if self.__state == 1:
            self._controller.digital_write(self._config["stage_1"], 1)
            self._controller.digital_write(self._config["stage_2"], 0)
            self._controller.digital_write(self._config["stage_3"], 0)

        elif self.__state == 2:
            self._controller.digital_write(self._config["stage_1"], 0)
            self._controller.digital_write(self._config["stage_2"], 1)
            self._controller.digital_write(self._config["stage_3"], 0)

        elif self.__state == 3:
            self._controller.digital_write(self._config["stage_1"], 0)
            self._controller.digital_write(self._config["stage_2"], 0)
            self._controller.digital_write(self._config["stage_3"], 1)

        self.__logger.debug("Name: {}; State: {}".format(self.name, self.__state))

#endregion

#region Public Static Methods

    @staticmethod
    def create(name, key, registers, controller):
        """Value of the thermometer."""

        instance = None

        stage_1 = registers.by_name(key + ".stage_1.output").value
        stage_2 = registers.by_name(key + ".stage_2.output").value
        stage_3 = registers.by_name(key + ".stage_3.output").value

        if stage_1 is not None and\
            stage_2 is not None and\
            stage_3 is not None:

            config = \
            {\
                "name": name,\
                "stage_1": stage_1,\
                "stage_2": stage_2,\
                "stage_3": stage_3,\
                "controller": controller\
            }

            instance = Klimafan(config)

        return instance

#endregion
