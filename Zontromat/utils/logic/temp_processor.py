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

class TemperatureProcessor():
    """State machine class"""

#region Attributes

    __thermometers = []
    """Thermometers"""

    __value = 0
    """Calculated value of the thermometers."""

#endregion

#region Constructor

    def __init__(self, thermometers=None):
        """Constructor

        Parameters
        ----------
        thermometers : Array
            Array of thermometers.
        """

        if thermometers is not None:
            self.__thermometers = thermometers

#endregion

#region Properties

    @property
    def value(self):
        """Value of the calculated temperature."""

        return self.__value

#endregion

#region Private Methods (Temporary)

    def __old_update(self):
        temperatures = []

        for thermometer in self.__thermometers:
            if thermometer is not None:
                temperatures.append(thermometer.get_temp())

        temps = len(temperatures)
        if temps <= 0:
            temperatures.append(0.0)

        # Find min and max.
        minimum = min(temperatures)
        maximum = max(temperatures)

        # Take medians.
        median = minimum + ((maximum - minimum) / 2)

        # Divide data by two arrays.
        upper_values = []
        lower_values = []

        for item in temperatures:
            if item >= median:
                upper_values.append(item)
            else:
                lower_values.append(item)

        # Use the bigger one, to create average.
        value = 0

        if len(upper_values) >= len(lower_values):
            value = sum(upper_values) / len(upper_values)

        elif len(upper_values) <= len(lower_values):
            value = sum(lower_values) / len(lower_values)

        # Return the temperature.
        self.__value = value

#endregion

#region Public Methods

    def add(self, thermometer):
        """Add thermometer.

        Parameters
        ----------
        thermometer : object.
            Device of type thermometer.
        """

        if thermometer is None:
            return

        self.__thermometers.append(thermometer)

    def remove(self, thermometer):
        """Remove thermometer.

        Parameters
        ----------
        thermometer : object.
            Device of type thermometer.
        """

        if thermometer is not None:
            self.__thermometers.remove(thermometer)

    def clear(self):
        """Clear all thermometers."""

        if self.__thermometers is not None:
            self.__thermometers.clear()

    def update(self):
        """Update temperature."""

        temperatures = []

        for thermometer in self.__thermometers:
            if thermometer is not None:
                current_temp = thermometer.get_temp()
                if current_temp > 0:
                    temperatures.append(current_temp)

        size = len(temperatures)
        if size > 0:
            self.__value = sum(temperatures) / len(temperatures)
        else:
            self.__value = 0

        # Return the temperature.
        return self.__value

#endregion
