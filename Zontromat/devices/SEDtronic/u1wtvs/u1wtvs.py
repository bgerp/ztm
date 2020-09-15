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

class U1WTVS(BaseDevice):
    """Tamper input device."""

#region Attributes

    __device = None
    """Device"""

    __neuron = None
    """Neuron"""

    # Straight
    __data2 = [\
        -0.249958, -0.24491081, -0.23986362, -0.23481642, -0.22976923,\
        -0.22472204, -0.21967485, -0.21462766, -0.20958046, -0.20453327,\
        -0.19948608, -0.19443889, -0.1893917, -0.18434451, -0.17929731,\
        -0.17425012, -0.16920293, -0.16415574, -0.15910855, -0.15406135,\
        -0.14901416, -0.14396697, -0.13891978, -0.13387259, -0.12882539,\
        -0.1237782, -0.11873101, -0.11368382, -0.10863663, -0.10358943,\
        -0.09854224, -0.09349505, -0.08844786, -0.08340067, -0.07835347,\
        -0.07330628, -0.06825909, -0.0632119, -0.05816471, -0.05311752,\
        -0.04807032, -0.04302313, -0.03797594, -0.03292875, -0.02788156,\
        -0.02283436, -0.01778717, -0.01273998, -0.00769279, -0.0026456,\
        0.0024016, 0.00744879, 0.01249598, 0.01754317, 0.02259036,\
        0.02763756, 0.03268475, 0.03773194, 0.04277913, 0.04782632,\
        0.05287352, 0.05792071, 0.0629679, 0.06801509, 0.07306228,\
        0.07810947, 0.08315667, 0.08820386, 0.09325105, 0.09829824,\
        0.10334543, 0.10839263, 0.11343982, 0.11848701, 0.1235342,\
        0.12858139, 0.13362859, 0.13867578, 0.14372297, 0.14877016,\
        0.15381735, 0.15886455, 0.16391174, 0.16895893, 0.17400612,\
        0.17905331, 0.18410051, 0.1891477, 0.19419489, 0.19924208,\
        0.20428927, 0.20933646, 0.21438366, 0.21943085, 0.22447804,\
        0.22952523, 0.23457242, 0.23961962, 0.24466681, 0.249714\
    ]

    # Inverse
    __data = [\
        0.000, -0.002, -0.005, -0.007, -0.010,\
        -0.012, -0.015, -0.017, -0.020, -0.023,\
        -0.025, -0.028, -0.030, -0.033, -0.035,\
        -0.038, -0.040, -0.043, -0.045, -0.048,\
        -0.050, -0.053, -0.055, -0.058, -0.060,\
        -0.063, -0.065, -0.068, -0.071, -0.073,\
        -0.076, -0.078, -0.081, -0.083, -0.086,\
        -0.088, -0.091, -0.093, -0.096, -0.098,\
        -0.101, -0.103, -0.106, -0.108, -0.111,\
        -0.113, -0.116, -0.119, -0.121, -0.124,\
        -0.126, -0.129, -0.131, -0.134, -0.136,\
        -0.139, -0.141, -0.144, -0.146, -0.149,\
        -0.151, -0.154, -0.156, -0.159, -0.162,\
        -0.164, -0.167, -0.169, -0.172, -0.174,\
        -0.177, -0.179, -0.182, -0.184, -0.187,\
        -0.189, -0.192, -0.194, -0.197, -0.199,\
        -0.202, -0.204, -0.207, -0.210, -0.212,\
        -0.215, -0.217, -0.220, -0.222, -0.225,\
        -0.227, -0.230, -0.232, -0.235, -0.237,\
        -0.240, -0.242, -0.245, -0.247, -0.250\
    ]

#endregion

#region Private Methods

    def __to_prs(self, value):

        output = 0

        end = len(self.__data) - 1
        for index in range(0, end):
            min_cond = value <= self.__data[index]
            max_cond = value >= self.__data[index+1]
            if min_cond and max_cond:
                output = (index + index+1) / 2
                break

        return output

#endregion

#region Public Methods

    def update(self):
        """Update sensor data."""
        self.__device = self._controller.get_device(self._config["dev"], self._config["circuit"])

    def get_value(self):
        """Get value."""

        raw = float(self.__device["vis"])
        prs = self.__to_prs(raw)

        return prs

#endregion
