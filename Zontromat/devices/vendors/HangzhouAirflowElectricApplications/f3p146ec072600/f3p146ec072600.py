
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

from devices.factories.fan.base_fan import BaseFan

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

class F3P146EC072600(BaseFan):
    """Model: F3P146-EC072-600
    
    See http://www.shidaqian.com/Upload/SDQ_ECqqlxfj/F3P146-EC072-600.PDF"""

#region Attributes

    __logger = None
    """Logger"""

    __output = "AO0"
    """Output physical signal."""

    __speed = -1

#endregion

#region Properties

#endregion

#region Public Methods

    def init(self):
        """Constructor

        Args:
            config (mixed): Device configuration.
            neuron (Neuron): Neuron instance.
        """

        self._vendor = "HangzhouAirflowElectricApplications"

        self._model = "F3P146EC072600"

        self.__logger = get_logger(__name__)

        if "output" in self._config:
            self.__output = self._config["output"]

        self.shutdown()

    def update(self):
        """Update device.
        """

        if self.__speed == self.speed:
            return

        self.__speed = self.speed
        value_speed = self.speed / 10
        self._controller.analog_write(self.__output, value_speed)
        self.__logger.debug(self)

    def shutdown(self):
        """Shutdown"""

        self.min_speed = 0
        self.speed = 0
        self.update()

#endregion

 # TODO: Create test.