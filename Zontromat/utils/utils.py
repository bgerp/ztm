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
from functools import wraps
import tracemalloc
import shutil

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

def mem_time_usage(function):
    """Measure consumed RAM for execution.

    Parameters
    ----------
    function : object
        Pointer to function.

    """

    @wraps(function)
    def function_timer(*args, **config):
        tracemalloc.start()
        t0 = time.time()
        result = function(*args, **config)
        t1 = time.time()
        passed_time = t1-t0
        current, peak = tracemalloc.get_traced_memory()
        print("Current memory usage is {}MB; Peak was {}MB".format(current / 10**6, peak / 10**6))
        print("Total time: {0:.3f} sec".format(passed_time))
        tracemalloc.stop()

        return result

    return function_timer

def mem_usage(function):
    """Mesure consumed RAM for execution.

    Parameters
    ----------
    function : object
        Pointer to function.

    """

    @wraps(function)
    def function_timer(*args, **config):
        tracemalloc.start()
        result = function(*args, **config)
        current, peak = tracemalloc.get_traced_memory()
        print("Current memory usage is {}MB; Peak was {}MB".format(current / 10**6, peak / 10**6))
        tracemalloc.stop()

        return result

    return function_timer

def time_usage(function):
    """Measure consumed time for execution.

    Parameters
    ----------
    function : object
        Pointer to function.

    """

    @wraps(function)
    def function_timer(*args, **config):
        t0 = time.time()
        result = function(*args, **config)
        t1 = time.time()
        passed_time = t1-t0
        print("Total time: {0:.3f} sec".format(passed_time))

        return result

    return function_timer

def disk_size():

    total, used, free = shutil.disk_usage("/")

    return (total, used, free)
