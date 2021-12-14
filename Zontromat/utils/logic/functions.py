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

import math

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

def l_scale(target, in_limit, out_limit):
    """Linear scaling function.

    Args:
        target (float): Input scalar.
        in_limit (list): List of two elements with input minimum and maximum.
        out_limit ([type]): List of two elements with output minimum and maximum.

    Returns:
        float: Output scaled value.
    """

    return (target - in_limit[0]) * (out_limit[1] - out_limit[0]) / \
        (in_limit[1] - in_limit[0]) + out_limit[0]

def to_deg(rad):
    """Radians to Degree.

    Args:
        rad (float): Radians input.

    Returns:
        float: Degres output.
    """

    return rad * (180.0 / math.pi)

def to_rad(deg):
    """Degrees to Radians.

    Args:
        deg (float): Degrees input.

    Returns:
        float: Radians output.
    """

    return deg * (math.pi / 180.0)

def shadow_length(height, alpha):
    """Length of the shadow.
        This simple online calculator gives a vertical object
        shadow length for specified day and geographic coordinate.
        The calculator uses Sun position algorithm to calculate sun altitude.

        Then it uses this formula to calculate shadow length:

        L = h/tan(alpha),

        where
        h - object height,
        a - angle between Sun and horizon.

        @see https://planetcalc.com/1875/

    Args:
        height (float): Height of the target object.
        alpha (float): Angle between Sun and horizon.

    Returns:
        float: Length of the shadow.
    """

    return height / math.tan(alpha)

def rotate_list(target_list, rotations):
    """Rotate list.

    Args:
        target_list (list): Target list.
        rotations (int): Rotations count.

    Returns:
        list: Rotated list.
    """

    return target_list[-rotations:] + target_list[:-rotations]
