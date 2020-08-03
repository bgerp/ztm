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

class CircularBuffer(object):

    def __init__(self, size):
        """initialization"""

        self.index= 0
        self.size= size
        self._data = []

    def put(self, value):
        """append an element"""

        if len(self._data) == self.size:
            self._data[self.index]= value
        else:
            self._data.append(value)

        self.index= (self.index + 1) % self.size

    def __getitem__(self, key):
        """get element by index like a regular array"""

        return self._data[key]

    def __repr__(self):
        """return string representation"""

        return self._data.__repr__() + ' (' + str(len(self._data))+' items)'

    def __str__(self):
        """String representation."""
        
        return self._data.__repr__()

    def __len__(self):
        """Length"""

        return len(self._data)

    def get_all(self):
        """return a list of all the elements"""

        return self._data
    