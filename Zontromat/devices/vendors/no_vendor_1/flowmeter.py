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

from devices.base_device import BaseDevice

from data import verbal_const

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

class Flowmeter(BaseDevice):
    """Flowmeter input device."""

#region Attributes

    __tpl = 1
    """Ticks per liter."""

    __input = verbal_const.OFF # "DI0"
    """Input pin of the controller."""

#endregion

#region Properties

    @property
    def input(self):
        """Input pin of the controller.

        Returns
        -------
        string
        """

        return self.__input

    @input.setter
    def input(self, value):
        """Input pin of the controller.

        Parameters
        ----------
        value : string
        """

        self.__input = value

    @property
    def tpl(self):
        """Tics per liter.

        Returns
        -------
        float
        """

        return self.__tpl

    @tpl.setter
    def tpl(self, value):
        """Tics per liter.

        Parameters
        ----------
        value : float
            Value.
        """

        if value < 0:
            value = 0

        self.__tpl = value



#endregion

#region Public Methods

    def init(self):

        if "tpl" in  self._config:
            self.__tpl = self._config["tpl"]

        if "input" in  self._config:
            self.__input = self._config["input"]

    def get_counter(self):
        """Get flowmeter counter."""

        value = 0

        if self.input != verbal_const.OFF and self.input != "":
            value = self._controller.read_counter(self.__input)

        return value

    def get_liters(self):
        """Get value."""

        return self.get_counter() * self.__tpl

#endregion

#region Public Static Methods

    @staticmethod
    def create(name, key, registers, controller):
        """Value of the thermometer."""

        instance = None

        cnt_input = registers.by_name(key + ".input").value
        cnt_tpl = registers.by_name(key + ".tpl").value

        if cnt_input is not None and\
            cnt_tpl is not None:

            config = \
            {\
                "name": name,
                "input": cnt_input,
                "tpl": cnt_tpl,
                "controller": controller
            }

            instance = Flowmeter(config)

        return instance

#endregion
