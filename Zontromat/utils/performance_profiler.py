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

import time
import tracemalloc
from functools import wraps

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
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

class CurrentConsuption:
    """Curent consumptnio."""

    __max_mem = 0
    __min_mem = 0
    __cur_mem = 0

    __max_time = 0
    __min_time = 0
    __cur_time = 0

class PerformanceProfiler:
    """Performance profiler."""

#region Attributes

    __enable = False
    """General enable."""

    __enable_mem_profile = False
    """Enable memory profiler."""

    __enable_time_profile = False
    """Enable time consumption prifiler."""

    __on_memory_change_callback = None
    """On memory change callback."""

    __on_time_change_callback = None
    """On time change callback."""

    __on_change_callback = None
    """On change time callback."""

#endregion

#region Properties

    @property
    def enable(self):
        """Enable time profile.

        Returns:
            float: Time profile flag.
        """

        return self.__enable

    @enable.setter
    def enable(self, value):
        """Enable time profile.

        Args:
            value (float): Time profile flag.
        """

        self.__enable = value

    @property
    def enable_mem_profile(self):
        """Enable memory profile.

        Returns:
            float: Memory profile flag.
        """

        return self.__enable_mem_profile

    @enable_mem_profile.setter
    def enable_mem_profile(self, value):
        """Enable memory profile.

        Args:
            value (float): Memory profile flag.
        """

        self.__enable_mem_profile = value

    @property
    def enable_time_profile(self):
        """Enable time profile.

        Returns:
            float: Time profile flag.
        """

        return self.__enable_time_profile

    @enable_time_profile.setter
    def enable_time_profile(self, value):
        """Enable time profile.

        Args:
            value (float): Time profile flag.
        """

        self.__enable_time_profile = value

#endregion

#region Public Methods

    def on_time_change(self, callback):
        """Set on time change callback."""

        if callback is not None:
            self.__on_time_change_callback = callback

    def on_memory_change(self, callback):
        """Set on memory change callback."""

        if callback is not None:
            self.__on_memory_change_callback = callback

    def on_change(self, callback):
        """Set on change callback."""

        if callback is not None:
            self.__on_change_callback = callback

    def profile(self, function):
        """Mesure consumed RAM and Time for execution.

        Parameters
        ----------
        function : object
            Pointer to function.

        Returns
        -------
        mix
            Result depends on measured function.

        """

        @wraps(function)
        def fn_measure(*args, **kwargs):

            current = 0
            peak = 0
            passed_time = 0

            if self.__enable_mem_profile and self.__enable:
                tracemalloc.start()

            if self.__enable_time_profile and self.__enable:
                t0 = time.time()

            result = function(*args, **kwargs)

            if self.__enable_time_profile and self.__enable:
                t1 = time.time()
                passed_time = t1-t0

            if self.__enable_mem_profile and self.__enable:
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                # print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")

                if self.__on_memory_change_callback is not None:
                    self.__on_memory_change_callback(current, peak)

            if self.__enable_time_profile and self.__enable:

                # print("Total time: {0:.3f} sec".format(passed_time))

                if self.__on_time_change_callback is not None:
                    self.__on_time_change_callback(passed_time)

            if (self.__enable_mem_profile or self.__enable_time_profile) and self.__enable:

                if self.__on_change_callback is not None:
                    self.__on_change_callback(current, peak, passed_time)

            return result

        return fn_measure

#endregion
